# Review Panel Report — Decision D9: Supabase Floor Lock

**Review date:** 2026-05-29  
**Review subject:** Decision D9 — Committing Supabase (Postgres + pgvector) as the permanent, append-only, immutable substrate for a verbatim archive of Anthropic conversation history (the "floor").  
**Review mode:** Exhaustive (plan/design + mixed content)  
**Review protocol:** Agent Review Panel v3.3.0 (15-phase adversarial multi-agent)

---

## Verdict

> **LOCK-WITH-CAVEATS — 6/10**

| Dimension | Value |
|---|---|
| **Verdict** | LOCK-WITH-CAVEATS |
| **Judge score** | 6/10 |
| **Panel mean** | 5.75/10 |
| **Score spread** | 5–6 (tight) |
| **Rounds of debate** | 2 (debate stopped after full convergence) |
| **Surviving P0 findings** | 0 |
| **Surviving P1 findings** | 1 (P1-A: append-only enforcement absent) |

### Panel Scores

| Reviewer | Phase 3 | Round 1 | Round 2 | Blind Final |
|---|---|---|---|---|
| Database Specialist | 4/10 DO-NOT-LOCK | 6/10 LOCK-WITH-CAVEATS | 6/10 LOCK-WITH-CAVEATS (stable) | 6/10 LOCK-WITH-CAVEATS |
| Risk Assessor | 3/10 DO-NOT-LOCK | 5/10 LOCK-WITH-CAVEATS | 5/10 LOCK-WITH-CAVEATS (stable) | 5/10 LOCK-WITH-CAVEATS |
| Devil's Advocate | 3/10 DO-NOT-LOCK | 3/10 DO-NOT-LOCK (held) | **6/10 LOCK-WITH-CAVEATS** (+3) | 6/10 LOCK-WITH-CAVEATS |
| Correctness Hawk | 6/10 LOCK-WITH-CAVEATS | 5/10 LOCK-WITH-CAVEATS | 6/10 LOCK-WITH-CAVEATS | 6/10 LOCK-WITH-CAVEATS |
| **Supreme Judge** | — | — | — | **6/10 LOCK-WITH-CAVEATS** |

---

## The Decision Under Review

D9 proposes to designate the Supabase Postgres database as the permanent, append-only substrate for 23,095 records (294 conversation headers + 22,801 messages, 367 MB) from an Anthropic conversation export, labeled "records.ndjson." The decision claims: (1) round-trip storage fidelity is "verbatim"; (2) the floor is "immortal / append-only"; (3) pgvector enables future semantic retrieval; (4) four integrity checks passed before lock.

**Scope under review:** Storage integrity only (retrieval/read-path explicitly deferred by the decision). The panel was charged to red-team this — not rubber-stamp — and to verify every claim against the live DB and source fixture directly.

---

## What the Panel Found

### The "verbatim" claim is inaccurate, but fixable

JSONB in Postgres canonically reorders keys alphabetically, strips whitespace, and silently collapses duplicate keys (last-wins, no error). Live measurement confirmed **200/200 sampled content_blocks have key reordering**; zero are byte-identical to source; zero have value loss. The "verbatim" claim is false for JSONB, but there is no data loss — only canonical key-order divergence.

Additionally, the fixture is named "scrub-v1" because a secrets/credential redactor ran on it: 273 redactions (RTSP, Postgres, Anthropic, OpenAI credentials) replaced with fixed tokens. Only 8 of 3,366 thinking blocks were touched, and only to remove a secret that literally appeared inside a thinking block. This is correct archive behavior — but it means the floor is "verbatim-modulo-secrets," not byte-identical to the raw export.

**Resolution:** Relabel the decision text. "Verbatim" → "value-preserving (JSONB canonical form), byte-verbatim (TEXT columns), modulo scrub-v1 secret redaction."

### The "immortal / append-only" claim is unenforceable as deployed

Live catalog reads confirmed:
- `anon`, `authenticated`, and `service_role` each hold **TRUNCATE** (plus REFERENCES, TRIGGER) on BOTH floor tables
- `postgres` holds full SELECT/INSERT/UPDATE/DELETE/TRUNCATE
- **Zero guard triggers** exist on either floor table (pg_trigger has 5 non-internal triggers, none on floor tables)
- RLS is enabled but has **zero policies**; more importantly, RLS never gates TRUNCATE (it is a table-level operation)

The "immortal floor" today is a social convention with zero database-level enforcement. Any role can destroy the floor in one statement. This is the sole P1 finding and the only hard blocker to declaring the lock.

Supabase itself ships `protect_buckets_delete` and `protect_objects_delete` guard triggers in its storage schema — proof the pattern is supported. The floor tables just don't have it yet.

### The "pgvector" title item is inaccurate but minor

`pg_extension` confirms `vector` is NOT installed (though `vector 0.8.0` is available via `CREATE EXTENSION`). The title says "+pgvector." This is a labeling error; pgvector is not required for, or part of, the storage-only floor lock. Drop it from the title or annotate it as a deferred read-path sidecar.

### The FK cascade fear was falsified

Phase 8 raised a concern that `fk_header` might be `ON DELETE CASCADE`, which would silently delete all message rows if a header were deleted. Live query: `confdeltype = 'a'` = **NO ACTION**. The FK *protects* the floor — a header with child messages cannot be deleted. This finding resolved favorably.

### The ndjson-canonical reframe: legitimate resolution

The Correctness Hawk introduced the key reframe that broke the panel deadlock: the ndjson — not the Postgres schema — is the actual "immortal" artifact. Postgres is a **rebuildable derived index** (value-preserving, deterministic projection). This dissolves all Postgres-specific irreversibility concerns: you can always rebuild from the ndjson. The Devil's Advocate's "one-way door" objection collapsed under this logic.

The judge accepts this reframe as legitimate — but only if the lock artifact operationalizes it with (a) the ndjson SHA-256 recorded and (b) a demonstrated rebuild drill. A reframe that merely asserts "ndjson is canonical" without proving it would be an evasion.

---

## Pre-Lock Caveats (Ordered — Hard Blockers First)

All six must be completed before declaring D9 locked. Caveats 1–4 are hard blockers. Caveats 5–6 are lighter (empirical check + acknowledgement).

### Caveat 1 — Enforce append-only at the database [BLOCKER — P1-A]

**The gate:** until a live attempted TRUNCATE is rejected by the DB, D9 is not locked.

On both `floor_conv_headers` and `floor_conv_messages`:
1. `REVOKE TRUNCATE, REFERENCES, TRIGGER FROM anon, authenticated, service_role;`
2. Add a `BEFORE TRUNCATE` statement-level trigger raising with `'immutable floor: TRUNCATE not permitted'`
3. Add a `BEFORE UPDATE OR DELETE` row-level trigger raising with `'immutable floor: UPDATE/DELETE not permitted'`

Model on Supabase's own `protect_objects_delete` / `protect_buckets_delete` (already in storage schema; this pattern is supported).

**Proof test:** Re-run grant query — the three roles show no TRUNCATE; attempt `TRUNCATE floor_conv_messages` and `DELETE FROM floor_conv_messages LIMIT 1` as service_role and observe both rejected. Capture outputs in the lock artifact.

### Caveat 2 — Record the canonical ndjson SHA-256 in the lock artifact [BLOCKER]

The ndjson is the real one-way artifact. The lock must commit to it, not merely assert it.

1. Compute SHA-256 of `records.ndjson` (and record its byte length: 367,494,497)
2. Compute SHA-256 of `scrub-audit.jsonl` and `verify.log` (companion artifacts)
3. Embed all three hashes in the lock document

**Proof test:** An independent recompute matches the recorded hashes.

### Caveat 3 — Demonstrate rebuild-from-ndjson [BLOCKER]

The "Postgres is rebuildable" claim must be proven, not assumed.

1. Rebuild a throwaway copy of both tables from the ndjson
2. Verify row counts: 294 headers + 22,801 messages
3. Run a PK-keyed value comparison on a sample and confirm 0 value-mismatches

**Proof test:** Rebuilt counts equal live counts; comparison reports 0 value-mismatch. Record the procedure and output in the lock artifact.

### Caveat 4 — Relabel the decision text precisely [BLOCKER]

Replace every unqualified "verbatim" with:  
> "value-preserving for JSONB (canonical key ordering), byte-verbatim for TEXT columns and timestamps, modulo secret redaction by scrub-v1"

Additionally:
- Designate the ndjson as the canonical floor and Postgres as a rebuildable derived index
- Either drop "+pgvector" from the D9 title or annotate it as "deferred read-path sidecar — never to be added as a column on the immutable tables"
- Name `scrub-audit.jsonl` and `verify.log` as immutable companion artifacts

**Proof test:** The decision title and body contain no unqualified "verbatim" and no implication that pgvector is currently installed or part of the floor.

### Caveat 5 — Confirm the hosting tier [Pre-lock empirical check]

Open the Supabase dashboard and record:
- Tier (Free vs Pro)
- Auto-pause policy and inactivity window
- Storage cap vs current usage (~218 MB on disk; ~367 MB ndjson)

If free tier: either upgrade, or explicitly accept the rebuild RTO (the floor will look "inactive" to Supabase because archives are rarely written to) AND confirm headroom before snapshot #2 (500 MB free cap is breached at ~2.3 snapshots at current size).

**Proof test:** Tier and cap headroom recorded in the lock artifact. If free, accepted-RTO statement is present.

### Caveat 6 — Acknowledge account_uuid and snapshot-selection scope [Pre-lock acknowledgement]

1. Check `account_uuid` cardinality across the 294 headers (single-account export or multi-account merge)
2. Decide whether `account_uuid` belongs in a floor that may be shared or rebuilt elsewhere (it is a PII-adjacent Anthropic account identifier)
3. State that the snapshot-selection policy (`current_snapshots` view or equivalent rule) and partial-ingest idempotency specification are required before snapshot #2 is ingested

**Proof test:** Account_uuid cardinality recorded; a one-line scope note present for snapshot #2 prerequisites.

---

## Post-Lock Recommendations (Not Blocking)

1. **Off-site immutable ndjson copy** — e.g., object storage with object-lock. Highest-priority post-lock item: the ndjson-canonical reframe makes the ndjson the SPOF. Single-copy canonical artifact is a latent failure.
2. **Verify/enable PITR** — or formally accept ndjson-rebuild as the backup strategy and document the expected RTO.
3. **Pre-ingest lint** — lint future ndjson exports for duplicate keys and null bytes before ingest. Postgres TEXT rejects U+0000; duplicate keys are silently collapsed by JSONB.
4. **Secondary index** — `(snapshot_id, conv_uuid, parent_message_uuid)` for tree traversal once a read path exists. Current plan table has only PK btrees; tree traversal requires a full sequential scan of 22,801 rows.
5. **CHECK constraints** — `CHECK (sender IN ('human','assistant'))`, `CHECK (is_root = (parent_message_uuid = '00000000-0000-4000-8000-000000000000'))`, timestamp format check — added carefully to never rewrite stored bytes.
6. **Header-flag integrity drill** — re-derive `multi_root`, `has_branches`, `message_count` from the current tree and confirm they match the denormalized header values (they are clean today; there is no enforcement for future snapshots).
7. **Single-transaction ingest** — specify an all-or-nothing ingest (single transaction or staging-swap) before snapshot #2 to handle partial-ingest failures without requiring an append-only-violating DELETE.

---

## Claim Verification Summary (Phase 10/11)

| Claim | Result |
|---|---|
| 294 headers / 22,801 messages / 23,095 ndjson lines | VERIFIED |
| 304 root messages, all with sentinel `00000000-0000-4000-8000-000000000000` | VERIFIED (caveat: sentinel is UUIDv4 nil-with-version, not plain all-zeros) |
| 9 multi-root conversations | VERIFIED |
| JSONB sorts keys alphabetically | VERIFIED live |
| JSONB duplicate keys → last-wins silently | VERIFIED live |
| content_blocks round-trip: 198/200 reordered, 2 byte-identical | **INACCURATE** — clean PK-keyed remeasure: 200/200 reordered, 0 byte-identical, 0 value loss. Core conclusion stands; exact split was off. |
| 1,479 source ndjson lines contain `\u` escapes | VERIFIED |
| anon/authenticated/service_role hold TRUNCATE on both floor tables | VERIFIED (also hold REFERENCES + TRIGGER — broader than panel's shorthand) |
| RLS enabled, 0 policies | VERIFIED |
| Only PK btrees exist (no secondary indexes) | VERIFIED |
| FK fk_header → NO ACTION (not CASCADE) | VERIFIED — cascade fear falsified |
| pgvector not installed | VERIFIED |
| 3 headers have zero matching messages | VERIFIED |
| 114 messages strictly empty | VERIFIED |
| EXPLAIN shows Seq Scan for parent_message_uuid queries | VERIFIED |

**20/21 claims verified; 1 inaccurate in exact quantitative detail (substantive conclusion correct).**

---

## Severity Register

| Finding | Severity | Tag | Basis |
|---|---|---|---|
| Append-only enforcement absent (TRUNCATE by 4 roles, no triggers, RLS doesn't gate TRUNCATE, both tables) | **P1** | [LIVE-VERIFIED] | Live role_table_grants, pg_trigger, pg_class.relrowsecurity |
| FK cascade (feared third bypass) | **Non-issue / resolved** | [LIVE-VERIFIED] | confdeltype='a' (NO ACTION); FK protects |
| "Verbatim" claim inaccurate (JSONB key reorder; scrub-v1 secret redaction) | P2 | [LIVE-VERIFIED] | JSONB round-trip + scrub-audit.jsonl + verify.log |
| pgvector absent vs "+pgvector" in title | P2 | [LIVE-VERIFIED] | pg_extension |
| scrub-v1 thinking-block fidelity | P2 | [LIVE-VERIFIED] | 8/3,366 thinking redactions, secrets-only; verify.log passed:true |
| Multi-snapshot mixed-version query (no current_snapshots view) | P2 | [LIVE-VERIFIED] structurally | PK includes snapshot_id; no view |
| Partial-ingest idempotency vs append-only | P2 | [STATIC-INFERENCE] | Design gap; no recovery path specified |
| Supabase free-tier auto-pause / 500 MB cap | P2 | [STATIC-INFERENCE] | Platform policy; dashboard-only |
| account_uuid PII-adjacent identifier in content floor | P2 | [LIVE-VERIFIED] present | Schema dump |
| No secondary indexes (seq scan for all tree traversal) | P3 | [LIVE-VERIFIED] | EXPLAIN outputs |
| Denormalized header fields unenforced (message_count, multi_root, has_branches) | P3 | [LIVE-VERIFIED] today clean | Current-snapshot checks |
| TOAST read amplification, timestamp-as-TEXT, empty-content rows | P3 | [LIVE-VERIFIED] | Storage stats, schema |

---

## Debate Quality Assessment

**No sycophancy detected.** The Devil's Advocate moved +3 (3→6) in Round 2 on the strength of the ndjson-canonical reframe logically resolving its signature objection — and it *introduced a new concern* (multi-snapshot mixed-version query concrete failure case) while moving. Position change accompanied by fresh adversarial contribution is evidence-driven movement, not social capitulation.

**One real panel quality defect:** All four reviewers had live DB access and unanimously listed "verify FK is not CASCADE" as a concern — and not one ran the one-line `pg_constraint.confdeltype` query before filing it as post-lock caveat #11. Phase 8 named this gap; Phase 10 ran the query. The answer was favorable (NO ACTION), but the miss exposed the "captured but never verified" failure mode. An immortal-floor decision cannot afford that pattern.

**Score convergence is evidence-based, not anchored.** Panel started at 3–6 and converged to 5–6 after two rounds of structured debate with a genuine reframe. The tight final spread reflects resolved substantive disputes, not herding.

---

## Single Most Important Action

**REVOKE TRUNCATE/DELETE-class grants from anon/authenticated/service_role on both floor tables and add guard triggers, then prove with a live attempted TRUNCATE that the floor rejects destruction.**

An "immortal floor" that any role can erase in one statement is not immortal in any sense the decision claims.

---

## Evidence Provenance

All quantitative claims in this report are based on live verification against the running Supabase DB (`postgresql://aws-1-us-east-2.pooler.supabase.com`) and direct reads of the source fixture. Database access: psycopg3 3.3.4, Python 3.13. Source fixture read-only: `apparatus-archive/snapshots/baseline-2026-05-25-ae015455/scrub-v1/records.ndjson` (23,095 lines, 367,494,497 bytes).

State files for all 15 phases are in `state/`. The process history (full director's cut) is in `review_panel_process.md`.
