# Phase 6 — Round 2 Debate Summary

## Score Movement (after Round 2)
| Reviewer | Phase 3 | Round 1 | Round 2 | Direction |
|---|---|---|---|---|
| Database Specialist | 4/10 | 6/10 | 6/10 LOCK-WITH-CAVEATS | STABLE |
| Risk Assessor | 3/10 | 5/10 | 5/10 LOCK-WITH-CAVEATS | STABLE |
| Devil's Advocate | 3/10 | 3/10 | **6/10 LOCK-WITH-CAVEATS** | +3 ↑ (moved) |
| Correctness Hawk | 6/10 | 5/10 | 6/10 LOCK-WITH-CAVEATS | +1 ↑ |

**All four reviewers converge on LOCK-WITH-CAVEATS (5-6/10).**

## What Moved the Devil's Advocate

The DA's signature argument — "substrate-agnostic gate cannot license a permanent choice" — was resolved by the ndjson-canonical reframe: if the ndjson IS the floor (not Postgres), then the integrity gate correctly tested the right artifact. The gate passes the ndjson's integrity. Locking the projection is then a low-stakes schema decision, not an irreversible commitment. The DA's process objection collapsed into a labeling/wording requirement.

The DA introduced a strengthened multi-snapshot uniqueness P1 (concrete failure case: after snapshot 2 ingest, a naive query `WHERE conv_uuid = X` returns messages from both snapshots, delivering stale content from snapshot 1 alongside new content from snapshot 2 with no indicator) and flagged it as a hard-deadline caveat: must be addressed before snapshot 2 is ever ingested.

## Resolved in Round 2

1. **Substrate-agnostic gate** — DA conceded it collapses under ndjson reframe. The gate correctly validates the canonical floor; locking the projection is separately justified. DB Specialist's "category error" argument accepted by DA.

2. **One-way door** — Full consensus: the ndjson is the real unlosable artifact; the Postgres schema is a rebuildable projection. This removes urgency and removes irreversibility from the Postgres lock.

3. **Main panel convergence** — All four on LOCK-WITH-CAVEATS. No surviving DO-NOT-LOCK position.

## Remaining (Minor/Pre-Lock) Disputes

### Multi-snapshot uniqueness: schema gap or design choice?
- DA: concrete failure case — naive query after snapshot 2 returns mixed-version messages
- DB Specialist: design (a)/(b)/(c) — intent is versioned snapshots, but a `current_snapshots` table/view needed before snapshot 2
- RA: downgraded to P2, needs `current_snapshots` view or documented selection policy
- Hawk: real but closeable pre-lock via a tested snapshot-selection view
→ **Consensus: P2, must be addressed BEFORE snapshot 2 is ingested (not required for the current single-snapshot lock)**

### ndjson floor protection: minimum bar
- RA: SHA-256 of ndjson must be recorded in lock artifact; off-site backup; rebuild drill
- Hawk: demonstrated rebuild is pre-lock; SHA-256 is minimum bar
- DB Specialist: naming/anchoring in lock artifact is pre-lock; durability details post-lock
→ **Consensus: minimum bar = SHA-256 of ndjson in lock artifact + demonstrated rebuild drill. Off-site backup is post-lock best practice.**

## Consolidated Caveat List (from all four reviewers)

### PRE-LOCK requirements (before declaring lock)
1. **Relabel decision text**: replace "verbatim" with "value-preserving" for JSONB columns; explicitly state text column IS byte-verbatim; ndjson is the canonical verbatim floor; Postgres is a rebuildable derived index
2. **Designate ndjson as canonical floor**: record SHA-256 hash of ndjson in the lock artifact; demonstrate rebuild-from-ndjson works
3. **Immutability enforcement**: REVOKE TRUNCATE from anon/authenticated/service_role; add BEFORE UPDATE/DELETE/TRUNCATE trigger (statement-level for TRUNCATE)
4. **pgvector in title or decision**: either remove pgvector from D9 title (it is absent) OR explicitly note it is a deferred sidecar capability; pgvector must NEVER be added as a column to immutable tables
5. **Snapshot selection policy**: define the `current_snapshots` view or documented rule (e.g., "SELECT * WHERE snapshot_id = (SELECT max(snapshot_id)...)" before snapshot 2 is ingested; this is not blocking for the single-snapshot lock but must be addressed before re-export

### POST-LOCK best practices (strongly recommended, not blocking)
6. **Pre-ingest lint**: lint future ndjson exports for duplicate keys and null bytes before ingestion
7. **Off-site ndjson backup**: store ndjson in a separate, immutable storage system (e.g., S3 with object lock)
8. **Secondary indexes**: add `idx_msg_parent (snapshot_id, conv_uuid, parent_message_uuid)` for tree traversal; add sender index if analytics needed
9. **Constraints**: add `CHECK (sender IN ('human','assistant'))`, `CHECK (is_root = (parent_message_uuid = '00000000-0000-4000-8000-000000000000'))`, timestamp format CHECK
10. **Confirm PITR**: verify Supabase automated backup is enabled and test a restore (or accept ndjson as the backup strategy)
11. **FK cascade action**: verify FK on messages→headers uses RESTRICT or NO ACTION (not CASCADE DELETE)

## Sycophancy Check
The DA position change in Round 2 was driven by new logical argument (ndjson reframe resolving the substrate-agnostic gate), not by social pressure. The DA introduced a NEW concern (multi-snapshot uniqueness concrete failure case) while moving. Movement is evidence-based, not sycophantic.

## Convergence Assessment
- All disputes now minor/caveat-level (not substantive DO-NOT-LOCK disagreements)
- No new major discoveries expected
→ **Debate STOPS after Round 2. Proceed to Phase 7 (Blind Final).**
