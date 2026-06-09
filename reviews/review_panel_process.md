# Review Panel Process History — Decision D9: Supabase Floor Lock

Director's cut log of all 15 phases. Each phase entry records: mandate, inputs, outputs, key findings, and decisions made. This is the authoritative process record; the structured summary is in `review_panel_report.md`.

**Protocol:** Agent Review Panel v3.3.0  
**Review date:** 2026-05-29  
**Working directory:** `docs/reviews/2026-05-29-d9-supabase-floor-lock/`

---

## Phase 1 — Setup

### Mandate
Identify the work under review, select personas, detect content signals, gather context, confirm review mode.

### Inputs
Decision D9 summary (provided by user), live Supabase DB access (`SUPABASE_DB_URL` set and confirmed at length 109), source fixture path `apparatus-archive/snapshots/baseline-2026-05-25-ae015455/scrub-v1/records.ndjson` (read-only).

### Decisions
- **Content type:** Mixed (plan/design + live DB schema + NDJSON source data). Review mode: Exhaustive for design claims; Precise for any code/SQL.
- **Personas selected:** Database Specialist (VoltAgent: `voltagent-data-ai:postgres-pro`), Risk Assessor, Devil's Advocate, Correctness Hawk. All agents launched with `model: "opus"`.
- **DB access method:** psycopg3 3.3.4 + Python 3.13 (psql not installed on the host).
- **Constraint confirmed:** Source ndjson is read-only. No git. No canon writes. Scratch only under `docs/reviews/`.

### Context Brief (written: `state/context_brief.md`)
Key verified facts before reviewers launched:
- `floor_conv_headers`: 294 rows; `floor_conv_messages`: 22,801 rows; source: 23,095 lines
- JSONB in Postgres: key-order normalization, whitespace stripping, duplicate-key last-wins collapse
- Sentinel UUID: `00000000-0000-4000-8000-000000000000` (UUIDv4 nil-with-version, not plain all-zeros)
- TOAST storage: ~193 MB of 218 MB total in TOAST
- RLS enabled, zero policies on both tables
- anon/authenticated/service_role: TRUNCATE granted, no INSERT/UPDATE/DELETE/SELECT
- pgvector NOT installed (available as `vector 0.8.0`)
- Supabase extensions: pg_stat_statements, pgcrypto, plpgsql, supabase_vault, uuid-ossp
- Correctness Hawk corrected 6 errors in the brief post-launch (TOAST size, empty row count, sender distribution, max content_blocks discrepancy)

---

## Phase 2 — Data Flow Trace

### Mandate
Trace the critical path from source ndjson to live DB; document schemas and transformation points.

### Key findings
- Record type is inferred from column presence (no `type` discriminator key in source ndjson)
- JSONB path is the loss point: source JSON → JSONB canonical form (key sort + whitespace strip + dup collapse + \u un-escaping + number normalization)
- TEXT path is byte-verbatim: `text`, `created_at`, `updated_at` stored as TEXT
- scrub-v1 ran before ingest: 273 credential redactions across the 23,095 records
- 1,479 source lines contain `\u`-escaped characters (already un-escaped by JSONB on ingest)

---

## Phase 3 — Independent Review (Parallel)

All four reviewers launched in parallel, each with full live DB access, no cross-talk.

### Database Specialist — Score: 4/10 DO-NOT-LOCK

State file: `state/reviewer_database_specialist_phase_3.md`

**P0-A (issued):** JSONB round-trip is NOT verbatim — key-order normalization, dup-key silent collapse, \u un-escaping confirmed by live `SELECT`
**P0-B (issued):** Append-only is unenforced — anon/authenticated/service_role hold TRUNCATE; no triggers; RLS has zero policies
**P2:** pgvector absent vs title; TOAST 193 MB notable
**Corrections to brief:** TOAST = 193 MB (not 199 MB); empty rows = 114 (not 135); no Realtime publication; max content_blocks size = 3,069,442 bytes (via psycopg3 not pg8000)

### Risk Assessor — Score: 3/10 DO-NOT-LOCK

State file: `state/reviewer_risk_assessor_phase_3.md`

**P0:** Hosted immutability is architecturally unachievable in Supabase — platform operator retains root; Postgres privilege model cannot achieve absolute immutability
**P0:** pgvector absent while decision commits to "+pgvector" in the title
**P1:** JSONB non-verbatim; decision's "verbatim" claim is false at the storage layer
**P1:** No snapshot-isolation policy; re-ingest with same msg_uuids creates dual-version rows with no selection mechanism
**Note:** Risk Assessor Phase 3 was retried once due to API error (400: thinking/redacted_thinking blocks cannot be modified); launched as fresh agent with simplified prompt

### Devil's Advocate — Score: 3/10 DO-NOT-LOCK

State file: `state/reviewer_devils_advocate_phase_3.md`

**Core objection (procedural):** The integrity gate (Check 1–4) is substrate-agnostic — it would pass on SQLite, NornicDB, or DuckDB. A gate that doesn't discriminate between substrates cannot license a permanent substrate choice.
**Argument:** Sequencing inversion — pgvector (retrieval) was listed first in the title but is absent; the decision is implicitly about a retrieval substrate that doesn't exist yet
**Argument:** "One-way door" is self-contradictory: the decision notes the door is irreversible, then lists the reversibility options (rebuild from ndjson); the reversibility claim should resolve the irreversibility concern
**Argument:** "Immortal floor" language is overclaimed; what is actually permanent is the ndjson, not the projection

### Correctness Hawk — Score: 6/10 LOCK-WITH-CAVEATS (highest Phase 3 score)

State file: `state/reviewer_correctness_hawk_phase_3.md`

**KEY FINDING — Check 3 FALSE:** The decision claims "byte-identical round-trip verified." Hawk ran live JSONB round-trip against 200+300 records: 300/300 reordered, 0/300 byte-identical. Zero value loss, but zero byte identity. Check 3 is false.
**Check 4 CONFIRMED + EXTENDED:** 929 messages carry supplementary-plane Unicode (emoji, CJK extension) — Postgres TEXT stores correctly; JSONB string escaping confirmed safe
**1,479 source lines with `\u` escapes** — already byte-altered on ingest (JSONB un-escapes them)
**Ndjson-canonical reframe INTRODUCED:** If ndjson is designated as the canonical verbatim floor and Postgres is a rebuildable derived index, JSONB key-reordering is a labeling issue not a data integrity failure. This is the framework that later resolves the main panel dispute.
**P1:** TRUNCATE enforcement missing — must REVOKE and add guard triggers
**Post-lock recommendations:** Secondary indexes, CHECK constraints, off-site ndjson backup

---

## Phase 4 — Private Reflection

All four reviewers re-read source independently and rated their own confidence.

State files: `state/reviewer_*_phase_4.md` (Database Specialist, Risk Assessor — recovered after Phase 3 retry skip, Correctness Hawk, Devil's Advocate)

**Key confidence ratings:**
- Database Specialist: reduced confidence in P0-A under ndjson reframe; maintained P0-B (enforcement)
- Risk Assessor: "hosted immutability" concern maintained but acknowledged it is substrate-invariant (any hosted DB shares this property)
- Correctness Hawk: high confidence in JSONB findings (directly measured); moderate confidence in ndjson reframe acceptance by panel
- Devil's Advocate: high confidence in procedural/gate objection; acknowledged "one-way door" logical tension

---

## Phase 5 — Debate

### Round 1

State files: `state/reviewer_*_phase_5_round1.md`

**Resolved in Round 1:**

1. **JSONB verbatim P0 downgraded** — Correctness Hawk's ndjson-canonical reframe accepted by Database Specialist and Risk Assessor. If ndjson is the canonical verbatim floor and Postgres is a rebuildable projection, JSONB key-reordering is a documentation fix, not a data integrity failure. Devil's Advocate partially accepted (fidelity P0s downgrade; gate objection remains).

2. **Hosted immutability absolute argument acknowledged as substrate-invariant** — Risk Assessor's strongest form ("true immutability is architecturally unachievable in hosted Postgres") accepted by all three others, but noted it applies equally to NornicDB and any hosted DB. Under the ndjson reframe, Postgres immutability concern dissolves (truncated Postgres = recoverable projection failure, not irrecoverable archive loss).

3. **One-way door emerging consensus** — Three of four agree ndjson is intact and Postgres is rebuildable; this removes urgency from the lock.

**Still in dispute after Round 1:**

1. **DA's "substrate-agnostic gate" objection (HELD):** A gate that passes on any substrate cannot justify a specific substrate choice. DB Specialist: this is a category error (gate was scoped to storage-integrity, not substrate comparison). RA: accepted ndjson reframe makes Postgres non-permanent.

2. **Multi-snapshot uniqueness (DA new issue):** After a second snapshot with same msg_uuids under a new snapshot_id, a naive `WHERE conv_uuid = X` returns rows from both snapshots, delivering mixed-version content with no indicator.

3. **ndjson floor protection gap (Hawk + RA):** If ndjson is canonical, its own protection (SHA-256, off-site backup, rebuild drill) is unaudited.

**Score movement after Round 1:**
- Database Specialist: 4 → 6 (+2)
- Risk Assessor: 3 → 5 (+2)
- Devil's Advocate: 3 → 3 (HELD)
- Correctness Hawk: 6 → 5 (-1 minor, increased uncertainty about some caveats)

### Round 2

State files: `state/reviewer_*_phase_5_round2.md`

**Resolved in Round 2:**

1. **Substrate-agnostic gate objection (DA CONCEDED):** DB Specialist's "category error" argument accepted. The gate was scoped to storage-integrity and correctly tested the ndjson (the canonical floor). Under the ndjson reframe, the gate passed the right artifact; locking the projection is then a low-stakes schema decision. DA's procedural objection collapsed into a labeling/wording requirement.

2. **One-way door — full consensus:** ndjson is the real unlosable artifact. Postgres lock is a rebuildable schema decision. This removes urgency and removes irreversibility.

**Remaining after Round 2 (minor/caveat-level only):**
- Multi-snapshot uniqueness → consensus P2, must be addressed BEFORE snapshot 2 (not blocking for current single-snapshot lock)
- ndjson floor protection → consensus: SHA-256 + rebuild drill = minimum pre-lock; off-site backup = post-lock best practice

**Score movement after Round 2:**
- Database Specialist: 6 LOCK-WITH-CAVEATS (stable)
- Risk Assessor: 5 LOCK-WITH-CAVEATS (stable)
- Devil's Advocate: 3 → **6** LOCK-WITH-CAVEATS (+3, evidence-driven)
- Correctness Hawk: 6 LOCK-WITH-CAVEATS (+1 minor)

**All four converged at LOCK-WITH-CAVEATS (5–6). Debate stopped after Round 2.**

---

## Phase 6 — Round Summaries

State files: `state/phase_6_round1_summary.md`, `state/phase_6_round2_summary.md`

### Consolidated Caveat List from Round 2

**PRE-LOCK (required):**
1. Relabel "verbatim" → "value-preserving (JSONB), byte-verbatim (TEXT), ndjson is canonical floor, Postgres is rebuildable derived index"
2. Record SHA-256 of ndjson in lock artifact + demonstrate rebuild-from-ndjson
3. REVOKE TRUNCATE from anon/authenticated/service_role + add BEFORE UPDATE/DELETE/TRUNCATE guard triggers
4. pgvector in title or decision: drop "+pgvector" from title OR annotate as deferred sidecar; pgvector must never be added as a column on immutable tables
5. Snapshot selection policy: define `current_snapshots` view or documented rule before snapshot 2

**POST-LOCK (strongly recommended, not blocking):**
6–11: Pre-ingest lint, off-site ndjson backup, secondary indexes, CHECK constraints, confirm PITR, verify FK cascade action (note: P10 later CLOSED this as non-issue)

### Sycophancy Assessment
DA movement was evidence-based (new logical argument resolved the signature objection) and DA introduced a NEW concern while moving (multi-snapshot uniqueness concrete failure case). Not sycophantic.

---

## Phase 7 — Blind Final

State files: `state/reviewer_*_phase_7.md`

All four reviewers submitted final scores independently (no cross-talk):
- Database Specialist: 6/10 LOCK-WITH-CAVEATS
- Risk Assessor: 5/10 LOCK-WITH-CAVEATS
- Devil's Advocate: 6/10 LOCK-WITH-CAVEATS
- Correctness Hawk: 6/10 LOCK-WITH-CAVEATS

Panel mean: 5.75/10. Spread: 5–6.

**Panel pre-lock blocker list (compiled from all four blind finals):**
1. REVOKE TRUNCATE + guard triggers (unanimous #1)
2. ndjson SHA-256 in lock artifact + rebuild drill
3. Relabel "verbatim" in decision text
4. Drop or annotate pgvector in title

---

## Phase 8 — Completeness Audit

State file: `state/phase_8_audit.md`

Dedicated auditor reviewed all panel output for what was MISSED. The panel adequately covered encoding fidelity, RLS state, pgvector status, snapshot PK structure, TOAST storage, and the ndjson-canonical reframe. Twelve new issues identified:

**High-priority misses:**

- **MISS-1 (P1):** FK cascade action: raised in Phase 3/5, listed as post-lock caveat #11, never verified despite full live DB access. Audit correctly identifies this as a pre-lock blocker IF the cascade type is bad. (Later resolved in Phase 10: confdeltype='a', NO ACTION — protected, not bypassed.)

- **MISS-2 (P1):** Supabase free-tier auto-pause/deletion on inactivity: an archive's normal access pattern (no writes, rare reads) looks inactive to Supabase free tier. Free projects can be paused and eventually deleted. Panel confirmed the DB works; nobody confirmed the tier or auto-pause policy.

- **MISS-3 (P1):** Thinking-block fidelity under scrub-v1: 3,366 thinking blocks are the highest-value non-reconstructable content, and scrub-v1 by its name asserts a transform ran. No reviewer verified whether thinking blocks are verbatim or modified. (Later resolved in Phase 11: secrets-only redactor; only 8 of 3,366 thinking blocks touched, and only to remove secrets.)

- **MISS-4 (P2):** scrub_version semantics and admission control unexamined
- **MISS-5 (P2):** Partial-ingest recovery: no path that is both idempotent AND append-only-preserving
- **MISS-6 (P2):** Timestamp precision consistency unverified
- **MISS-7 (P2):** multi_root / has_branches header flags never cross-checked against actual tree
- **MISS-8 (P2):** account_uuid role, cardinality, privacy never examined
- **MISS-9 (P3):** message_count verified today but not enforced for future snapshots
- **MISS-10 (P3):** 910 empty-text / non-empty content_blocks recoverability assumed
- **MISS-11 (P3):** Pooler transaction isolation for concurrent ingest
- **MISS-12 (P3):** Supabase row/storage tier limits vs growing snapshots

---

## Phase 9 — Verify Commands

Panel-issued verification commands were reviewed and advisory outputs noted. The primary verification work was performed live in Phases 3 and 10/11 against the actual DB; Phase 9 confirmed no new commands were outstanding.

---

## Phase 10 — Claim Verification

State file: `state/phase_10_claim_verification.md`

The Claim Verifier ran every reviewer claim independently against the live DB and source ndjson. 21/21 claims checked.

**Key verification results:**

| Claim | Result |
|---|---|
| 294 / 22,801 / 23,095 counts | VERIFIED |
| 304 root messages with sentinel | VERIFIED (caveat: sentinel = `00000000-0000-4000-8000-000000000000`, not plain all-zeros) |
| JSONB sorts keys alphabetically | VERIFIED live: `'{"z":1,"a":2}'::jsonb::text` → `{"a": 2, "z": 1}` |
| JSONB dup keys last-wins silently | VERIFIED live: `'{"a":1,"a":2}'::jsonb::text` → `{"a": 2}` |
| content_blocks round-trip 198/200 reordered | **INACCURATE** — clean PK-keyed measure: 200/200 reordered, 0 byte-identical, 0 value loss. Panel's "2 byte-identical" not reproducible. Core conclusion sound. |
| TRUNCATE on floor tables for 3 roles | VERIFIED; also REFERENCES + TRIGGER (panel's "only TRUNCATE" shorthand incomplete) |
| floor_conv_headers: IDENTICAL grant set | VERIFIED — debate centered on messages; headers have same exposure |
| RLS enabled, 0 policies | VERIFIED |
| Only PK btrees | VERIFIED — EXPLAIN: Seq Scan for parent_message_uuid filter |
| FK fk_header: confdeltype='a' = NO ACTION | VERIFIED — **CASCADE FEAR FALSIFIED**; FK protects, does not cascade |
| pgvector NOT installed | VERIFIED |
| 3 headers with 0 messages | VERIFIED |
| 114 strictly-empty messages | VERIFIED |

---

## Phase 11 — Severity Verification

State file: `state/phase_11_severity_verification.md`

Four P1 findings re-verified from ground truth (live catalog reads and direct file reads). Final severity adjustments:

| Finding | Panel | Adjusted | Key evidence |
|---|---|---|---|
| P1-A: Append-only enforcement absent | P1 | **P1 CONFIRMED** | Live: anon/authenticated/service_role/postgres all hold TRUNCATE on both tables; 5 non-internal triggers, none on floor; RLS on but doesn't gate TRUNCATE |
| P1-B: pgvector absent vs title | P1 | **P2 (downgrade)** | pg_extension confirms absent; vector 0.8.0 installable; storage-only lock doesn't require it |
| P1-C: FK cascade | P1 | **Resolved / non-issue (downgrade)** | confdeltype='a' = NO ACTION; FK protects; feared third bypass does not exist |
| P1-D: Thinking-block fidelity under scrub-v1 | P1 | **P2 (downgrade)** | scrub-audit.jsonl: 273 entries, 4 pattern classes (RTSP/postgres/anthropic/openai); only 8 touch thinking paths; verify.log: passed=true, 0 residual hits over 331 MB |

**Net: P1-A is the only surviving P1. All others downgraded or resolved.**

### scrub-v1 detail
- 273 redactions: RTSP 177, postgres 76, anthropic 10, openai 10
- Only 8 touch a `content[N].thinking` path (RTSP 6, anthropic 1, postgres 1)
- verify.log: `{"passed": true, "scanned_bytes": 331359194, "scanned_strings": 673871, "regex_hits_per_class": {all 0}}`
- Thinking blocks are verbatim-modulo-secrets (correct behavior for an archive)

---

## Phase 12 — Verification Tier Assignment

The single verified finding (P1-A) was assigned [LIVE-VERIFIED] (highest confidence tier): based on live catalog reads against the running DB. All other severity-relevant findings tagged [LIVE-VERIFIED] or [STATIC-INFERENCE] as appropriate.

---

## Phase 13 — Targeted Verification

Persona-matched verification agents were dispatched for the two remaining open questions from Phase 8 that Phase 10/11 couldn't close from the DB alone:
- **Free-tier auto-pause (MISS-2):** tagged [STATIC-INFERENCE]; falsification test specified (Supabase dashboard → Settings/Billing); cannot be resolved from catalog
- **account_uuid cardinality (MISS-8):** noted as verifiable from DB but deprioritized as P2 acknowledgement item

---

## Phase 14 — Supreme Judge Ruling

State file: `state/phase_14_judge_ruling.md`

**LOCK-WITH-CAVEATS, 6/10.**

The judge upheld the panel's converged verdict, narrowed what may be claimed at lock time, and issued the following key rulings:

**On P1-A:** Accepted as the load-bearing finding. Added nuance: grant exposure is broader than panel's "only TRUNCATE" shorthand — roles also hold REFERENCES + TRIGGER, and headers table has the identical grant set. Caveat 1 REVOKE scope widened accordingly.

**On the ndjson-canonical reframe:** LEGITIMATE RESOLUTION — ACCEPTED, conditionally. The reframe correctly relocates irreversibility onto the ndjson. But it earns its acceptance only if the lock artifact (a) records the ndjson SHA-256 and (b) demonstrates an actual rebuild. Without those, the reframe launders an unverified durability assumption into a verdict. Caveats 2–3 promoted to hard pre-lock blockers.

**On the "verbatim" claim:** P2 labeling; remediation is precision relabeling in the decision text (Caveat 4).

**On FK cascade / scrub-v1 / pgvector:** Accepted Phase 10/11 downgrades. No reversals.

**On free-tier auto-pause:** [STATIC-INFERENCE] — correct tag. Dashboard check required (Caveat 5).

**On account_uuid:** Elevated from audit mention to named pre-lock acknowledgement (Caveat 6).

**On retrieval deferral:** Acceptable — the storage-integrity-only scope is legitimate to lock on, provided retrieval is named as deferred and no one later loosens floor grants to enable a read path.

**Judge's single most important action:**
> "REVOKE TRUNCATE/DELETE-class grants from anon/authenticated/service_role on both floor tables and add guard triggers, then prove with a live attempted TRUNCATE that the floor rejects destruction — because an 'immortal floor' that any role can erase in one statement is not immortal in any sense the decision claims."

**Debate quality assessment (judge):**
- No sycophancy in panel convergence
- Tight 5–6 spread is appropriate (evidence-driven convergence, not correlated bias)
- One real panel quality defect: collective failure to run the FK query despite unanimous awareness

---

## Phase 14.5 — Post-Judge Verification

State file: `state/phase_14_5_judge_verification.md`

Mandate: Classify every P0/P1 in the judge ruling as [PANEL-RAISED] (already verified in Phase 11) or [JUDGE-INTRODUCED] (verify here).

**Result:** 0 P0 findings in judge ruling. 1 P1 finding (P1-A). P1-A is [PANEL-RAISED] — verified in Phase 11. The judge's grant-scope expansion (ruling line 27: roles also hold REFERENCES + TRIGGER; headers table has identical grant set) was read as potentially judge-introduced but was found, on ground-truth check of `phase_10_claim_verification.md`, to be a Phase 10 live-query result that Phase 11's write-up had compressed. Classified [PANEL-RAISED] / [JUDGE-CONFIRMED].

**Zero judge-introduced P0/P1 findings. Zero hallucinations.**

---

## Phase 15 — Output Generation

### 15.1 — Primary Markdown Report
Written to: `review_panel_report.md`

### 15.2 — Process History
This file: `review_panel_process.md`

### 15.3 — Interactive HTML Dashboard
Written to: `review_panel_report.html`

---

## Appendix — Technical Infrastructure Notes

- **DB access:** psql not installed on host. All DB queries run via Python 3.13 + psycopg3 3.3.4.
- **UnicodeEncodeError on Windows:** Python scripts printing Unicode characters (✓ etc.) failed on CP1252 console. Fixed with `sys.stdout.reconfigure(encoding="utf-8")`.
- **SUPABASE_DB_URL persistence:** Environment variable does not persist across PowerShell sessions. Each script embedded `os.environ["SUPABASE_DB_URL"] = "..."` at the top.
- **Null byte query:** `WHERE position(chr(0) in text) > 0` raises `ProgramLimitExceeded: null character not permitted` in Postgres — this means U+0000 in TEXT would fail ingest (a data characteristic, not a query bug).
- **Risk Assessor Phase 3 API error:** `400: thinking or redacted_thinking blocks cannot be modified` — retried as fresh agent with simplified prompt. Phase 4 reflection was initially skipped; recovered via dedicated recovery agent.
- **Phase 8 scratch files:** Several `_*.py`, `_*.txt`, `zz_*` files in `state/` are working files from verifier agents. Harmless; deletion was blocked by permissions.
- **C8 measurement discrepancy:** Panel reported 198/200 reordered + 2 byte-identical. Phase 10 clean PK-keyed remeasure: 200/200 reordered, 0 byte-identical. The 2 "byte-identical" records were likely an artifact of imprecise join key or sampling order in the original measurement. The substantive conclusion (zero value loss) is unaffected.
- **Sentinel UUID precision:** The sentinel is `00000000-0000-4000-8000-000000000000` (the UUID nil-value with the v4 version and variant nibbles set), not the plain all-zeros UUID. Querying against the plain all-zeros returns 0 rows.
