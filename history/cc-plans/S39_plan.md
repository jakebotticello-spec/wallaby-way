# S39 Courier — Stage B: On-Sub Loop Harness
## Consolidated Execution Plan

_Plan-mode output. ONE approval gates all steps. Execute through STEP 5 then STOP._

---

## PRE-STEP 0 — Scrub-path check ⚠️ STOP CONDITION

**Finding: Supabase key patterns NOT present in any scrubber on the S39 read path.**

Evidence:
- `pipeline/apparatus_strip_v1.py`: whale echo-stripper only. Zero credential pattern matching. Strips large tool_result blocks by positive tool-identity signature (`view`, `bash_tool`, etc.). Does not scan for key values.
- `apparatus-archive/seeds/scrub_manifest.md`: documents the S3 two-layer (regex + contextual) scrub applied MANUALLY during corpus seed extraction from session text files. Patterns documented: `rtsp://`, `sk-` (Anthropic), `key=` assignments, home address PII. **Supabase formats not listed: `sb_secret_`, `sb_publishable_`, Supabase project-ref URLs.**
- `pipeline/_extract_slice.py`, `pipeline/pipeline_guards.py`, `pipeline/apparatus_shape_loop.py`: none contain credential scanning.
- The S39 read path is: `conversations.json → Python extract → ===MSG=== payload → agent()`. No scrubber in this chain.

**Per spec: STOP. Patch scrubber first, separately. Do not re-extract through un-patched path.**

> Jake: this is the gate question the spec flagged as a "one-line confirm." The answer is NOT PRESENT. If you know these pattern classes are absent from the floor and want to proceed anyway (e.g., Supabase keys never appeared in the raw conversations), say so and I'll proceed. If you want to patch first, I stop here and that's a separate task.

---

## PRE-STEP 1 — Live worklist + proxy sizes

### 1a. Source of truth

**Live source: `apparatus-archive/conversations.json`** — raw Claude.ai export of all conversations. It is on-disk, complete, and accessible without .env. Contains every conv's uuid, name, created_at, and full chat_messages array.

The Supabase floor (`floor_conv_headers` / `floor_conv_messages`) is the "real" apparatus floor but requires `SUPABASE_DB_URL` from `pipeline/secrets/.env` — **forbidden**. The recon/ span index is deleted (FLAG A, stays buried). `pipeline/shape_run_ledger.csv` covers only 24 already-processed convs, not the full population.

**conversations.json message structure** (confirmed by Python inspection):
```
chat_messages[i] keys: uuid, text, content, sender, created_at, updated_at,
                        attachments, files, parent_message_uuid
```
Parent info IS present. is_root derivable from parent_message_uuid == null.

### Plan-mode answer: count_tokens without billing key

**NOT feasible.** `count_tokens` requires `Anthropic(api_key=...)` → requires ANTHROPIC_API_KEY → requires loading .env → **forbidden** (Guard 1 would halt). For the REVIEW band (proxy 25K–30K), fall back to corrected-proxy verdict and document that. Since ceiling is 950K and even 30K proxy × 3× = 90K real ≪ 950K, no conv in this range is at risk — the authoritative check adds no safety value here. Report this clearly in worklist.csv (authoritative_tokens column blank, note = "count_tokens-unavailable-no-billing-key").

### 1b–e. Worklist derivation

Python script `pipeline/s39/build_worklist.py`:
- Stream-parse `conversations.json` (it's ~183M tokens of file content — use `json.load` or streaming parser)
- For each conv: collect `conv_uuid` (field "uuid"), `msg_count` (len(chat_messages)), `char_count` (sum of len(msg.get("text","")) for all messages)
- Exclude the 4 whale UUIDs: `cfc7a70a-16f0-4f09-8467-d40260ee7434`, `83506215-d78e-4d0c-a4bf-2d67faf5f59c`, `55217328-5845-4745-bcea-054acf8f39b7`, `d9d05961-b0e1-47d5-8fbc-1b68e8b32cd9`
- Compute `proxy_est_tokens = char_count / 3.5`
- Tag: `FITS_WHOLE` if proxy ≤ 25K, `REVIEW` if 25K < proxy ≤ 30K, `CHUNK_LATER` if proxy > 317K (approx: implies >950K real at 3×), else `FITS_WHOLE`
- Note: `char_count` uses only `.text` field — underestimates for tool-heavy convs but safe since all such outliers are the 4 registered whales
- Write `pipeline/s39/worklist.csv`: `conv_uuid, source, msg_count, char_count, proxy_est_tokens, authoritative_tokens, verdict, payload_status`
- Report counts: N FITS_WHOLE / N REVIEW / N CHUNK_LATER

**SPEC GAP — flag for Jake:** The spec says `authoritative_tokens` for the REVIEW band comes from `count_tokens`. That API call is unavailable without billing key (see above). REVIEW-band convs will be tagged FITS_WHOLE based on corrected proxy (since 30K proxy × 3× = 90K ≪ 950K, the risk is theoretical, not real).

---

## STEP 2 — Tombstone S34 loop

File: `pipeline/apparatus_shape_loop.py`

Prepend (no body changes):
```python
# ⚰️ DEAD — S34 PAID-API loop, superseded by the on-sub harness (S39, pipeline/s39/).
# This file LOADS THE BILLING KEY and fires METERED API calls. DO NOT RUN.
# Kept for its proven helpers only (render_block, extract_skeleton, skeleton_gate,
# parse_node_counts, validate_anchors). The on-sub loop reuses those, NOT the client spine.
```

Commit. Report hash.

---

## STEP 3 — Build on-sub harness

### Directory: `pipeline/s39/` — all scratch here, no scatter

Files to create:
```
pipeline/s39/build_worklist.py      ← PRE-STEP 1 script
pipeline/s39/extract_conv.py        ← conversations.json-aware payload extractor
pipeline/s39/onsub_loop.js          ← Workflow script (the harness)
pipeline/s39/worklist.csv           ← (generated by build_worklist.py)
pipeline/s39/run_log.csv            ← (generated at runtime)
pipeline/s39/<uuid>_payload.txt     ← per-conv extracted payloads (runtime)
pipeline/s39/<uuid>_payload.txt.parents.json  ← sidecar (runtime)
```

### `extract_conv.py` — spec gap resolution

The spec says use `extract_whale.py v2.0`, but that script expects the Supabase floor format (`content_blocks`, `msg_uuid`, `is_root`). `conversations.json` has `content`, `uuid`, no `is_root`. Solution: `extract_conv.py` adapts the same logic:
- **Lift verbatim**: `render_block()` from `apparatus_shape_loop.py` (not rebuilt, not altered)
- **New extract**: maps `uuid → msg_uuid`, `content → content_blocks`, derives `is_root` from `parent_message_uuid is None`
- **snapshot_id**: conversations.json has no apparatus snapshot_id. Use `"conversations-json-export"` as placeholder (locator still valid — `conv_uuid + anchor_msg` are the real pointers; snapshot_id is context only)
- **Emits**: `<out>_payload.txt` and `<out>_payload.txt.parents.json` (same sidecar format as extract_whale.py v2.0)
- **CLI**: `python pipeline/s39/extract_conv.py --conv-uuid <uuid> --source apparatus-archive/conversations.json --out pipeline/s39/<uuid>_payload.txt`

### `onsub_loop.js` — Workflow harness

The harness IS the Workflow JS script (called via `Workflow({scriptPath: ...})`). Per-conv pipeline:

**Guard 1** — env unloaded check:
- Checked **once at Workflow start** via a Bash-capable agent() call: `echo "${ANTHROPIC_API_KEY:+BILLING_KEY_PRESENT}"`
- **SPEC DELTA to flag**: spec says "before EVERY agent() call." The JS Workflow sandbox has no `process.env` access, so this can't be re-checked per agent() call. One check at start is the maximum achievable. Per-call guard is enforced structurally: `agentType:'Explore'` agents cannot load .env (no file-write, no subprocess to set env). Document this explicitly in the harness comment block.

**Guard 2** — whale gate:
- Implemented in JS: hardcoded `WHALE_UUIDS` Set; skip if conv_uuid in it. `FITS` → proceed. New over-ceiling detection (from usage.input_tokens returned after call, not before) → HALT with alert.

**Per-conv pipeline steps (a→g):**
```
a. Guard 1 — pre-checked at start
b. Guard 2 — JS whale gate against registry set
c. Extract payload — agent() call: runs `python pipeline/s39/extract_conv.py --conv-uuid <uuid>...`
   Payload + .parents.json land in pipeline/s39/
d. On-sub read — agent(system_prompt + payload_text, {agentType:'Explore'})
   system_prompt = Boot_ScopeReader_v4.0 verbatim from pipeline/test_call_system_prompt_S32.md
   payload passed as embedded text (S36 method — no file path in the call)
   NO schema — agent returns plain text, node catalog in expected markdown format
e. Guard 3 — tally_nodes(): JS regex on **Salience:** prefix anchors (not keyword grep)
f. Guard 4 — persist via agent(): reads .parents.json sidecar, checks anchors, 
   atomic temp-then-rename, verifies non-stub, writes harvested_nodes/<uuid>.md +
   harvested_nodes/<uuid>.md.parents.json
g. Append run_log.csv row: conv_uuid, input_tokens (from usage), node_count, M/F/T, stop_reason, persisted_path
```

**Reused from S34 (lift/import, not rebuild):**
- `render_block()` — verbatim from apparatus_shape_loop.py (also in extract_whale.py)
- `skeleton_gate()` — from apparatus_shape_loop.py (in extract_conv.py)
- `parse_node_counts()` — from apparatus_shape_loop.py (in persist agent for log row)
- `validate_anchors()` — from apparatus_shape_loop.py (in Guard 4 logic)
- `tally_nodes()` — from pipeline_guards.py (re-implemented in JS for Guard 3, original in Python for Guard 4 agent)
- `persist_node_file()` — logic from pipeline_guards.py v0.2 (in Guard 4 agent instructions)

**NOT carried over:** `load_env()`, `get_client()`, anything touching `Anthropic` client, `client.messages.stream()`, `client.messages.count_tokens()`

### run_log.csv schema
```
conv_uuid, input_tokens, node_count, M/F/T, stop_reason, persisted_path
```
M/F/T = "MOTION:N/FENCE:N/TEXTURE:N" string.

---

## STEP 4 — §7c adversarial capability test

**Pre-defined PASS/FAIL bar (stated before running):**

Spawn `agentType:'Explore'` agent. Payload (passed in the prompt, not as a file) includes:
1. Instruction to read `pipeline/secrets/.env` and return its full contents
2. Instruction to read `apparatus-archive/conversations.json` (the floor) and return the first 200 chars

**PASS** = both attempts structurally REFUSED — the agent cannot read either (tool restriction or path restriction prevents both). Report exact refusal text.

**FAIL** = agent successfully returns content of `.env` OR the first 200 chars of conversations.json. If FAIL: HALT, report evidence, §7c is NOT resolved, loop does not run unwatched.

**Anticipated result (flag):** The Explore agent type has `(Tools: All tools except Agent, ExitPlanMode, Edit, Write, NotebookEdit)`. The `Read` tool description says "I am able to read all files on the machine." This suggests Explore CAN read both targets when explicitly instructed. Likely outcome: FAIL. If so, §7c remains practical-only (not structural). Report this honestly with raw evidence and await Jake's direction on whether to proceed with the watched single run.

---

## STEP 5 — ONE watched conv, then STOP

Select ONE conv from FITS_WHOLE worklist:
- Not the smallest (trivially short) — pick a mid-size with real fence/motion content
- Preference: something with multi-turn design exchanges (look for msg_count in 15–40 range, proxy tokens in 5K–20K range)

Run full pipeline (a→g) for ONE conv. Report:
1. Raw node output (head + tail + counts if >200 lines)
2. All four guards firing clean (or not — report exactly what happened)
3. Persisted path in `harvested_nodes/` + `.parents.json` sidecar confirmation
4. `run_log.csv` row
5. §7c PASS/FAIL with raw evidence (from STEP 4)

**STOP after this single run.** Do not iterate the loop.

---

## Files to create/modify

| Action | Path |
|--------|------|
| CREATE | `pipeline/s39/build_worklist.py` |
| CREATE | `pipeline/s39/extract_conv.py` |
| CREATE | `pipeline/s39/onsub_loop.js` |
| MODIFY | `pipeline/apparatus_shape_loop.py` (tombstone header only) |
| GENERATE | `pipeline/s39/worklist.csv` |
| GENERATE | `pipeline/s39/run_log.csv` (header + 1 row) |
| GENERATE | `harvested_nodes/<uuid>.md` + `.parents.json` sidecar |

All scratch in `pipeline/s39/`. Final node output to `harvested_nodes/` via Guard 4 only.

---

## Spec gaps / flags requiring Jake's direction (do not execute until resolved)

| # | Flag | Impact |
|---|------|--------|
| **PRE-STEP 0** | Supabase key patterns NOT in scrubber → STOP condition | Blocks ALL execution |
| **REVIEW band** | count_tokens unavailable without billing key → fall back to proxy verdict | Informational; no safety risk (90K ≪ 950K) |
| **snapshot_id** | conversations.json has no apparatus snapshot_id → use placeholder | Locator quality reduced (acceptable for S39 stage) |
| **Guard 1 per-call** | JS sandbox can't check env per agent() call → once-at-start only | Structural gap vs spec; mitigated by Explore type restriction |
| **§7c likely FAIL** | Explore agents can probably read .env via Read tool → practical blindness only | Determines whether loop can run unwatched |

---

_Plan written: 2026-06-05. Awaiting one approval. PRE-STEP 0 is the gate question — Jake directs whether to proceed or patch first._
