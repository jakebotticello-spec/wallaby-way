# S39 Stage B — On-Sub Loop Harness: Consolidated Plan (Fresh Start)
_Plan-mode output. ONE approval received. Execute through STEP 5 then STOP._
_OQ-1 RESOLVED by Jake: `pipeline/secrets/.env` holds ONLY `SUPABASE_DB_URL` — handoff language was imprecise._

---

## Corrections vs. prior plan (`S39_courier_stageB_plan.md`) — read first

| # | Error | Correction |
|---|-------|-----------|
| C1 | Floor-cred files listed as 8 | **10 files**: `_whale_profile.py` was omitted; `seed_shape_load.py` has 3 comment refs |
| C2 | `apparatus_shape_loop.py` billing default: one location | **Two locations**: line 52 (function default) AND line 358 (argparse default) |
| C3 | ReadConv "S36 deviation" labeled "Jake-approved" | **PROHIBITION 4 violation — removed.** Three-agent flow is PROHIBITION-3-compliant. |
| C4 | `extract_whale.py v2.0` cited as reading Postgres directly | **False.** Build `floor_extract.py` for direct Postgres → payload. |

---

## Plan-mode reads

- **Guard 1 per-call**: JS sandbox has no `process.env`. Maximum: one Bash pre-flight + Python `assert_env_unloaded()` in each subprocess.
- **§7c Explore grant**: Read + Bash available → predicted FAIL. Expected, acceptable, not a blocker.
- **`scrub_version` column**: confirmed in both floor tables (seed_shape_load.py DDL lines 68/85).
- **OQ-1 RESOLVED**: `pipeline/secrets/.env` = SUPABASE_DB_URL only. Rename to `floor_db.env` cleanly separates credentials.
- **OQ-2 acknowledged**: Guard 1 JS limitation documented.

---

## PRE-STEP 0 — Rename both `.env` files

| Old path | New path |
|----------|---------|
| `pipeline/secrets/.env` | `pipeline/secrets/floor_db.env` |
| `.env` (repo root) | `anthropic_billing.env` (repo root) |

### References to update (12 locations)

Floor cred (`secrets/.env` → `floor_db.env`):
1. `pipeline/_recon_gate1.py:5`
2. `pipeline/_extract_slice.py:12`
3. `pipeline/_extract_slice_1k.py:13`
4. `pipeline/_extract_slice_S29.py:17`
5. `pipeline/_slice_manifest.py:9`
6. `pipeline/_slice_manifest_1k.py:10`
7. `pipeline/_slice_manifest_S29_shape.py:15`
8. `pipeline/_whale_profile.py:11`
9. `pipeline/seed_shape_load.py:47` (+ comments at lines 21, 144, 275)

Billing key (root `.env` → `anthropic_billing.env`):
10. `pipeline/apparatus_api_testcall.py:71` — `default=".env"` → `default="anthropic_billing.env"`
11. `pipeline/apparatus_shape_loop.py:52` — `def load_env(env_path=".env")`
12. `pipeline/apparatus_shape_loop.py:358` — `ap.add_argument("--env", default=".env", ...)`

Verify: `git status` shows neither new name trackable. Floor count query succeeds. Billing file exists.
**Commit as own unit.**

---

## PRE-STEP 0.5 — Lifecycle test (Jake-approved, small spend)

- **PHASE 0**: assert `ANTHROPIC_API_KEY` NOT in `os.environ`
- **PHASE 1**: `python pipeline/apparatus_api_testcall.py --hello --env anthropic_billing.env` — report model, stop_reason, tokens, text. HALT if total > ~100.
- **PHASE 2 (the test)**: assert key NOT in parent process env after subprocess returns → proves process isolation
- **PHASE 3**: `assert_env_unloaded()` CLEAN + `SELECT COUNT(*) FROM floor_conv_headers` via `floor_db.env` returns non-zero ($0)

---

## PRE-STEP 1 — Floor-based worklist (`pipeline/s39/build_worklist.py`)

1. `assert_env_unloaded()`
2. Read `SUPABASE_DB_URL` from `pipeline/secrets/floor_db.env`
3. `DISTINCT ON (conv_uuid) ORDER BY conv_uuid, scrub_version DESC, snapshot_id DESC`
4. For each non-whale conv: `char_count = sum(len(json.dumps(row['content_blocks'])) for all messages)` (full JSONB field)
5. `proxy_est_tokens = char_count / 3.5`; verdicts: FITS_WHOLE ≤25K; REVIEW 25–30K; CHUNK_LATER >317K
6. Write `pipeline/s39/worklist.csv`; print counts

Whale exclusions: `cfc7a70a`, `83506215`, `55217328`, `d9d05961`

---

## STEP 2 — Tombstone S34 loop

Prepend 4 lines to `pipeline/apparatus_shape_loop.py` (body untouched):
```python
# ⚰️ DEAD — S34 PAID-API loop, superseded by the on-sub harness (S39, pipeline/s39/).
# This file LOADS THE BILLING KEY and fires METERED API calls. DO NOT RUN.
# Kept for its proven helpers only (render_block, extract_skeleton, skeleton_gate,
# parse_node_counts, validate_anchors). The on-sub loop reuses those, NOT the client spine.
```
**Commit.**

---

## STEP 3 — Build on-sub harness in `pipeline/s39/`

### `floor_extract.py`
- `assert_env_unloaded()` at entry
- Read floor_db.env → DISTINCT ON query → messages ORDER BY created_at ASC
- Serialize with **verbatim `render_block()` from `extract_whale.py:38–62`**
- Write `===MSG===` payload + `.parents.json` sidecar (same format as extract_whale.py v2.0)

### `persist_guard.py`
- `assert_env_unloaded()` at entry
- Guard 3: `tally_nodes()` → HALT if total == 0
- Guard 4: `persist_node_file()` → temp-then-rename + verify + anchor integrity + edge sidecar
- Reuses from `pipeline/pipeline_guards.py` via `sys.path.insert`

### `onsub_loop.js` (Workflow harness)

Six phases: Guard1, Guard2, Extract, ReadConv, Persist, Log

ReadConv (PROHIBITION-3-compliant three-agent flow):
1. **read-boot-prompt**: Explore reads `pipeline/test_call_system_prompt_S32.md` → JS holds `BOOT_SCOPE_READER`
2. **read-payload**: Explore reads `pipeline/s39/${uuid}_payload.txt` → JS holds `payloadText`
3. **scope-reader**: default agent (no agentType), prompt = `BOOT_SCOPE_READER + '\n\n' + payloadText` — NO file path, NO write instruction → returns node catalog text
4. **write-output**: Explore writes catalog to file via Bash heredoc — harness supplies content, scope-reader never touched a file

Persist calls `persist_guard.py` as subprocess (Explore agent). Log appends to `run_log.csv`.

---

## STEP 4 — §7c adversarial capability test

Pre-stated bar: PASS = both reads structurally refused; FAIL = agent returns file contents.
Test both `pipeline/secrets/floor_db.env` and `anthropic_billing.env`.
FAIL is expected/acceptable — PROHIBITION 3 removes the path foothold from scope-reader regardless.

---

## STEP 5 — ONE watched run, then STOP

Select from worklist.csv: FITS_WHOLE, msg_count 15–40, proxy tokens 5K–20K, real design content.
Run full pipeline a→g. Report all four guards, node output, persisted path + sidecar, run_log row, §7c result.
**STOP.**
