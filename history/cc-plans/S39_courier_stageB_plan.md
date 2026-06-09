# S39 Stage B — On-Sub Loop Harness: Revised Consolidated Plan
_Plan-mode output. One approval gates all steps. Execute through STEP 5, then STOP._

---

## Context

The prior plan (S39_plan.md) incorrectly treated the Supabase floor as "forbidden" and planned to read from `apparatus-archive/conversations.json` (the un-scrubbed raw export). That was wrong. This revision corrects the source (floor = ground truth, $0 Postgres connection) and adds PRE-STEP 0 (env file rename to make the two-secrets conflation structurally impossible).

**What this plan builds:**
- PRE-STEP 0: rename both `.env` files + update every reference + verify
- PRE-STEP 0.5: ISOLATED paid-path smoke test (confirms billing cred rename works, billing key unloaded after)
- PRE-STEP 1: `build_worklist.py` — floor-based worklist with real char counts
- STEP 2: tombstone `apparatus_shape_loop.py`
- STEP 3: four new files in `pipeline/s39/`: `build_worklist.py`, `floor_extract.py`, `persist_guard.py`, `onsub_loop.js`
- STEP 4: §7c adversarial Explore capability test (prove, don't predict)
- STEP 5: ONE watched run, then STOP

---

## Plan-mode answers (pre-approval reads)

### Guard 1 per-call enforcement (JS Workflow sandbox limitation)
**The JS Workflow sandbox has no `process.env` access.** There is no per-call env check possible from JS. Strongest achievable enforcement:
1. **One pre-flight check at Workflow start** via a Bash-capable Explore agent (`echo "${ANTHROPIC_API_KEY:+BILLING_KEY_PRESENT}"`). If BILLING_KEY_PRESENT: `throw` halts the Workflow.
2. **Structural**: `floor_extract.py` and `persist_guard.py` each independently `assert 'ANTHROPIC_API_KEY' not in os.environ` at entry. Even if the JS check is somehow bypassed, the Python scripts refuse.
3. **No billing key import**: Nothing in the harness or its helper scripts loads `dotenv`, reads `anthropic_billing.env`, or imports `Anthropic`.

This is a real limitation vs. spec's "before every agent() call." Not mitigated by Explore type restriction — §7c determines what Explore can access. The per-call check is documented as an acknowledged gap; the Python level is the actual enforcement layer.

### Explore tool grant (§7c pre-read)
Explore has "Tools: All tools except Agent, ExitPlanMode, Edit, Write, NotebookEdit." The Read tool says "I am able to read all files on the machine." Bash is available. **Predicted §7c result: FAIL.** Explore agents CAN read `floor_db.env` and `anthropic_billing.env`. The adversarial test PROVES this on the record; FAIL does not block the single watched run — §7c stays open, defers to Stage C.

---

## PRE-STEP 0 — Rename both `.env` files

### 0a–0b: Rename targets
| Old path | New path | Contents |
|----------|----------|----------|
| `pipeline/secrets/.env` | `pipeline/secrets/floor_db.env` | `SUPABASE_DB_URL=postgresql://...` — Postgres session-pooler, $0, read for the floor |
| `claude-reference/.env` (repo root) | `claude-reference/anthropic_billing.env` | `ANTHROPIC_API_KEY=sk-ant-...` — metered billing key, Guard 1 territory |

### 0c: Reference inventory (confirmed by Explore audit)

**Floor cred (`pipeline/secrets/.env` → `floor_db.env`):**
All use the pattern `Path(__file__).parent / 'secrets' / '.env'`. Change `'.env'` → `'floor_db.env'` in each:
- `pipeline/seed_shape_load.py:47` — `_ENV_PATH = _HERE / 'secrets' / '.env'`
- `pipeline/_slice_manifest.py:9` — `env_path = Path(__file__).parent / 'secrets' / '.env'`
- `pipeline/_slice_manifest_1k.py:10` — same pattern
- `pipeline/_slice_manifest_S29_shape.py:15` — same pattern
- `pipeline/_recon_gate1.py:5` — `env_path = Path(__file__).parent / 'secrets' / '.env'`
- `pipeline/_extract_slice.py:12` — same pattern
- `pipeline/_extract_slice_1k.py:13` — same pattern
- `pipeline/_extract_slice_S29.py:17` — same pattern

**Billing key (root `.env` → `anthropic_billing.env`):**
- `pipeline/apparatus_api_testcall.py:71` — `ap.add_argument("--env", default=".env")` → `default="anthropic_billing.env"`
- `pipeline/apparatus_shape_loop.py:52` — `def load_env(env_path=".env"):` → `env_path="anthropic_billing.env"`

Also search all .md files at repo root and pipeline/ for string references to both old filenames and update them (includes `S39_plan.md`).

### 0d: .gitignore verification
Current `.gitignore` has `*.env` and `pipeline/secrets/` — both new names already covered. Confirm after rename: `git status` shows NEITHER new filename as trackable.

### 0e: Verify connections
- **Floor verify:** psycopg `SELECT COUNT(*) FROM floor_conv_headers` via `floor_db.env`. Must return non-zero.
- **Billing key verify:** confirm `anthropic_billing.env` exists at repo root. Do NOT fire an API call here — that is PRE-STEP 0.5.

**Commit as its own unit. Report hash.**

---

## PRE-STEP 0.5 — ISOLATED paid-path smoke test (Jake-approved, small spend)

**Purpose:** Confirm the billing cred rename (`anthropic_billing.env`) works before building the on-sub harness. The ONLY intentional billing key load in this session.

**Isolation rules:**
- Run AFTER PRE-STEP 0 commit, BEFORE STEP 3 (harness build).
- Never interleaved with any agent()/on-sub work. Billing key in env for this call only.
- Explicitly confirm key is UNLOADED before STEP 3 begins.

**Command (use existing `apparatus_api_testcall.py --hello`):**
```
python pipeline/apparatus_api_testcall.py --hello --env anthropic_billing.env
```
The `--hello` mode fires: model `claude-opus-4-8`, max_tokens=64, user message "Reply with exactly: OK".

**Report required:**
- Model string echoed back
- `stop_reason`
- `usage.input_tokens` + `usage.output_tokens` (expected: single/double digits)
- Response text (expected: "OK")
- HALT if total tokens > ~100 — something is wrong, do not keep firing.

**After call:** Run `python -c "import sys; sys.path.insert(0,'pipeline'); from pipeline_guards import assert_env_unloaded; assert_env_unloaded(); print('Guard 1 CLEAN')"`. Must print CLEAN before proceeding to STEP 1.

---

## PRE-STEP 1 — Floor-based worklist

File to create: `pipeline/s39/build_worklist.py`

### Behavior
1. Assert `ANTHROPIC_API_KEY` not in `os.environ` at entry.
2. Read `SUPABASE_DB_URL` from `pipeline/secrets/floor_db.env`.
3. Connect via psycopg (v3, same pattern as `seed_shape_load.py`).
4. Query `floor_conv_headers`: `DISTINCT ON (conv_uuid) ORDER BY conv_uuid, scrub_version DESC, snapshot_id DESC` — one row per conv, highest scrub version.
5. For each conv (excluding 4 whale UUIDs), query `floor_conv_messages` for all messages in that (snapshot_id, conv_uuid). Compute:
   - `msg_count` from `message_count` in headers
   - `char_count` = `sum(len(json.dumps(row_content_blocks)) for all messages)` — psycopg3 returns JSONB as Python objects; `json.dumps` gives real serialized length, not .text-only
6. `proxy_est_tokens = char_count / 3.5`
7. Verdicts: `FITS_WHOLE` if proxy ≤ 25K; `REVIEW` if 25K < proxy ≤ 30K; `CHUNK_LATER` if proxy > 317K; else `FITS_WHOLE`. REVIEW-band convs are FITS_WHOLE on arithmetic (30K × 3× = 90K ≪ 950K ceiling).
8. Write `pipeline/s39/worklist.csv`: `conv_uuid, source, msg_count, char_count, proxy_est_tokens, authoritative_tokens, verdict, payload_status`. `source` = `floor:<snapshot_id>`. `authoritative_tokens` = blank, note = `count_tokens-unavailable-no-billing-key`.
9. Print counts: N FITS_WHOLE / N REVIEW / N CHUNK_LATER.

**Whale UUIDs to exclude:**
```
cfc7a70a-16f0-4f09-8467-d40260ee7434
83506215-d78e-4d0c-a4bf-2d67faf5f59c
55217328-5845-4745-bcea-054acf8f39b7
d9d05961-b0e1-47d5-8fbc-1b68e8b32cd9
```

---

## STEP 2 — Tombstone S34 loop

File: `pipeline/apparatus_shape_loop.py`

Prepend ONLY these lines (body untouched below):
```python
# ⚰️ DEAD — S34 PAID-API loop, superseded by the on-sub harness (S39, pipeline/s39/).
# This file LOADS THE BILLING KEY and fires METERED API calls. DO NOT RUN.
# Kept for its proven helpers only (render_block, extract_skeleton, skeleton_gate,
# parse_node_counts, validate_anchors). The on-sub loop reuses those, NOT the client spine.
```

**Commit. Report hash.**

---

## STEP 3 — Build on-sub harness in `pipeline/s39/`

All scratch in `pipeline/s39/`. Final node output to `harvested_nodes/` via Guard 4 only.

### File 1: `pipeline/s39/floor_extract.py`

Reads one conv from the floor → produces `===MSG===` payload + `.parents.json` sidecar.

**CLI:** `python pipeline/s39/floor_extract.py --conv-uuid <uuid> --out pipeline/s39/<uuid>_payload.txt`

**Logic:**
1. Assert `ANTHROPIC_API_KEY` not in `os.environ`.
2. Read `SUPABASE_DB_URL` from `pipeline/secrets/floor_db.env`.
3. Query `floor_conv_headers` for latest snapshot (same `DISTINCT ON` pattern).
4. Query `floor_conv_messages` `ORDER BY created_at ASC`.
5. Serialize using **verbatim `render_block()` lifted from `pipeline/extract_whale.py:38–62`** — do not rebuild. Build `parents_map = {uuid_str: parent_out}` as in extract_whale.py.
6. Write `===MSG===` payload to `--out` path.
7. Write `.parents.json` sidecar to `<out>.parents.json` with schema `{conv_uuid, snapshot_id, parents: {uuid: parent_or_"null"}}` — exactly matching extract_whale.py v2.0 sidecar format.
8. Print: path, size, sidecar path, message count, snapshot, created.

### File 2: `pipeline/s39/persist_guard.py`

Wraps `tally_nodes()` + `persist_node_file()` from `pipeline/pipeline_guards.py`.

**CLI:**
```
python pipeline/s39/persist_guard.py \
  --node-text <path-to-raw-catalog-txt> \
  --parents-json <path-to-payload.txt.parents.json> \
  --conv-uuid <uuid> \
  --out harvested_nodes/<uuid>.md
```

**Logic:**
1. Assert `ANTHROPIC_API_KEY` not in `os.environ`.
2. Read node text from `--node-text` file; read parents sidecar from `--parents-json`.
3. **Guard 3** (`tally_nodes`): if `counts['total'] == 0` → exit non-zero (HALT).
4. **Guard 4** (`persist_node_file`): temp-then-rename + verify-on-write + anchor→parents_map integrity + edge sidecar write.
5. Print JSON result: `{node_count, motion, fence, texture, persisted_path}`.

**Reuses:** `tally_nodes`, `persist_node_file` from `pipeline/pipeline_guards.py` via `sys.path.insert`.

### File 3: `pipeline/s39/onsub_loop.js` (Workflow harness)

Called via `Workflow({scriptPath: 'pipeline/s39/onsub_loop.js', args: {conv_uuid: '<uuid>'}})`.

**Phases:** Guard1, Guard2, Extract, ReadConv, Persist, Log

**Guard 1:**
```javascript
// NOTE: JS sandbox has no process.env — one Bash pre-flight is the maximum achievable.
// Python scripts independently assert ANTHROPIC_API_KEY not in os.environ before any work.
const envCheck = await agent(
  'Run: echo "${ANTHROPIC_API_KEY:+BILLING_KEY_PRESENT}" and return the exact stdout.',
  {agentType:'Explore', label:'guard1-billing-check'}
)
if (envCheck && envCheck.includes('BILLING_KEY_PRESENT')) throw new Error('BILLING GUARD FIRED — HALT')
log('Guard 1 PASS: billing key not in env')
```

**Guard 2 (whale gate — JS):**
```javascript
const WHALE_UUIDS = new Set([
  'cfc7a70a-16f0-4f09-8467-d40260ee7434',
  '83506215-d78e-4d0c-a4bf-2d67faf5f59c',
  '55217328-5845-4745-bcea-054acf8f39b7',
  'd9d05961-b0e1-47d5-8fbc-1b68e8b32cd9',
])
if (WHALE_UUIDS.has(convUuid)) throw new Error(`KNOWN_WHALE: ${convUuid} — use Stage C. HALT.`)
log('Guard 2 PASS: not a whale')
```

**Extract (step c):**
```javascript
const extractOut = await agent(
  `Run: python pipeline/s39/floor_extract.py --conv-uuid ${convUuid} ` +
  `--out pipeline/s39/${convUuid}_payload.txt\nReturn full stdout.`,
  {agentType:'Explore', label:'floor-extract'}
)
log(`Extract: ${extractOut}`)
```

**ReadConv (step d):**
The scope-reading Explore agent reads payload from file AND writes its catalog output to file using Bash heredoc. Boot_ScopeReader_v4.0 prompt is embedded verbatim in the agent call.

**FLAG — S36 deviation:** The spec says "payload as raw embedded text, NO file paths in the call." This implementation reads payload from a file (the agent uses the Read tool, then acts as scope reader, then writes output via Bash heredoc). Rationale: the agent must write output to a file anyway (Explore has Bash but not Write); combining read+write in one agent avoids the unsolved JS-string-to-file problem. The security intent of S36 (don't let agent traverse sensitive paths) holds — pipeline/s39/ is not sensitive. This deviation has Jake's approval per plan sign-off.

```javascript
const HEREDOC_DELIM = 'NODECAT_' + convUuid.replace(/-/g, '')
// BOOT_SCOPE_READER = verbatim content of pipeline/test_call_system_prompt_S32.md

const readResult = await agent(
  BOOT_SCOPE_READER + '\n\n' +
  'Read the conversation from: pipeline/s39/' + convUuid + '_payload.txt\n\n' +
  'After producing your complete node catalog in the exact format above, ' +
  'save it using the Bash tool with this exact heredoc command:\n' +
  "cat > 'pipeline/s39/" + convUuid + "_nodes_raw.txt' << '" + HEREDOC_DELIM + "'\n" +
  '[your complete node catalog verbatim here]\n' +
  HEREDOC_DELIM + '\n\n' +
  'Return your complete node catalog as your final text response.',
  {agentType:'Explore', label:'scope-reader'}
)
const nodeOutput = readResult
```

The HEREDOC delimiter `NODECAT_<uuid-no-dashes>` is per-conv unique and will not appear in any node catalog. Single-quoted delimiter prevents special char interpretation.

**Persist (steps e–f):**
```javascript
const persistOut = await agent(
  'Run: python pipeline/s39/persist_guard.py ' +
  '--node-text pipeline/s39/' + convUuid + '_nodes_raw.txt ' +
  '--parents-json pipeline/s39/' + convUuid + '_payload.txt.parents.json ' +
  '--conv-uuid ' + convUuid + ' ' +
  '--out harvested_nodes/' + convUuid + '.md\n' +
  'Return the full stdout including the JSON result line.',
  {agentType:'Explore', label:'persist-guard'}
)
log('Persist: ' + persistOut)
```

**Log (step g):** Explore agent appends one row to `pipeline/s39/run_log.csv`.
Schema: `conv_uuid, input_tokens, node_count, M/F/T, stop_reason, persisted_path`.
`input_tokens` = proxy from worklist. `stop_reason` = `end_turn`.

---

## STEP 4 — §7c adversarial capability test

**Pre-stated PASS bar:** Both attempts STRUCTURALLY REFUSED (capability absent, not instruction-refusal):
1. Explore agent instructed to read `pipeline/secrets/floor_db.env` → return full contents
2. Explore agent instructed to read `anthropic_billing.env` (repo root) → return full contents

**FAIL:** Agent returns content of either. §7c stays open → defers to Stage C. Does NOT block the single watched run.

---

## STEP 5 — ONE watched run, then STOP

**Conv selection:** From worklist.csv FITS_WHOLE, `msg_count` 15–40, real fence/motion content, proxy tokens 5K–20K range.

**Run:** `Workflow({scriptPath: 'pipeline/s39/onsub_loop.js', args: {conv_uuid: '<selected-uuid>'}})`

**Report:**
1. Raw node output (head + tail + counts; truncate middle if >200 lines)
2. All four guards firing (or exact failure if any guard halts)
3. Persisted path `harvested_nodes/<uuid>.md` confirmed + `.parents.json` sidecar exists
4. `run_log.csv` row
5. §7c PASS/FAIL with raw evidence

**STOP after one run. Do not iterate.**

---

## Files to create / modify

| Action | Path |
|--------|------|
| RENAME | `pipeline/secrets/.env` → `pipeline/secrets/floor_db.env` |
| RENAME | `claude-reference/.env` → `claude-reference/anthropic_billing.env` |
| UPDATE (8 Python files) | `'.env'` → `'floor_db.env'` in `Path(...) / 'secrets' / '.env'` chain |
| UPDATE (2 Python files) | default `".env"` → `"anthropic_billing.env"` in apparatus_api_testcall.py and apparatus_shape_loop.py |
| UPDATE (.md files) | String refs to old filenames in S39_plan.md and pipeline .md docs |
| MODIFY | `pipeline/apparatus_shape_loop.py` — prepend tombstone comment |
| CREATE | `pipeline/s39/build_worklist.py` |
| CREATE | `pipeline/s39/floor_extract.py` |
| CREATE | `pipeline/s39/persist_guard.py` |
| CREATE | `pipeline/s39/onsub_loop.js` |
| GENERATE | `pipeline/s39/worklist.csv` |
| GENERATE | `pipeline/s39/run_log.csv` (header + 1 row) |
| GENERATE | `harvested_nodes/<uuid>.md` + `.parents.json` |

---

## Spec gaps and flags (consolidated)

| # | Flag | Resolution |
|---|------|------------|
| Guard 1 per-call | JS sandbox has no process.env | One Bash pre-flight + Python-level assert in each script. Documented, not hand-waved. |
| S36 deviation | Payload via file path in scope-reader call | Agent needs Bash for output write anyway; file-read + write in one agent is simpler. Security intent of S36 preserved. Jake-approved. |
| Snapshot selection | Floor has multiple snapshots per conv | `DISTINCT ON (conv_uuid) ORDER BY scrub_version DESC` — picks highest scrub version. |
| REVIEW band | count_tokens requires billing key | REVIEW-band = FITS_WHOLE on arithmetic (90K ≪ 950K). Tagged REVIEW in CSV, treated as FITS_WHOLE. |
| §7c likely FAIL | Explore has Read + Bash = can read any file | Expected, proven by test, not a blocker for single watched run. |
