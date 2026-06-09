# Phase 6 — Round 1 Debate Summary

## Score Movement
| Reviewer | Phase 3 | After Round 1 | Direction |
|---|---|---|---|
| Database Specialist | 4/10 DO-NOT-LOCK | 6/10 LOCK-WITH-CAVEATS | +2 ↑ |
| Risk Assessor | 3/10 DO-NOT-LOCK | 5/10 LOCK-WITH-CAVEATS (conditional) | +2 ↑ |
| Devil's Advocate | 3/10 DO-NOT-LOCK | 3/10 DO-NOT-LOCK | HELD |
| Correctness Hawk | 6/10 LOCK-WITH-CAVEATS | 5/10 LOCK-WITH-CAVEATS | -1 (minor) |

## Resolved in Round 1

### 1. JSONB verbatim: P0 downgraded under ndjson-canonical reframe
What convinced them: The Correctness Hawk's framing — if ndjson is explicitly designated as the canonical verbatim floor and Postgres is a rebuildable derived index, JSONB's key-reordering is a documentation/labeling fix, not a data integrity failure.
- DB Specialist: conceded JSONB P0 → now P2-labeling. Three residuals remain: (a) dup-key silent collapse on future snapshots needs a pre-ingest lint; (b) 1479 \u-escaped lines are byte-altered (document, don't suppress); (c) decision rationale must be reworded from "verbatim" to "value-preserving."
- Risk Assessor: accepted the reframe. Dissolves Postgres-specific JSONB concern.
- Devil's Advocate: partially accepted — the fidelity P0s downgrade, but argues lock targets the projection not the floor.

### 2. Hosted-immutability absolute argument partially resolved
The Risk Assessor's strongest form ("true immutability is architecturally unachievable in hosted Postgres") was accepted by all three others — but they noted this is a UNIVERSAL concern (any hosted database shares this property) and is NOT a Postgres-specific argument. The ndjson reframe dissolves the Postgres-immutability concern: if ndjson is the canonical floor, a truncated or corrupted Postgres DB is a recoverable projection failure, not an irrecoverable archive loss.

### 3. One-way door deflation: emerging consensus
Three of four now agree the "append-only-immortal" description overstates irreversibility. The ndjson is intact, reproducible, and is the actual unlosable artifact. The Postgres DB is a projection. This removes urgency from the lock.

## Still in Dispute

### Dispute 1: DA's "substrate-agnostic gate cannot license a permanent substrate choice"
- **DA position (HELD)**: A gate that would pass on SQLite, NornicDB, or DuckDB cannot justify choosing Postgres permanently. This is a procedural objection about what kind of evidence justifies a forever-choice. The gate tests storage fidelity, not Postgres fitness.
- **DB Specialist's counter**: The gate was scoped to "storage-integrity ONLY" — it was never claimed to be a Postgres-vs-NornicDB comparison gate. Calling it a category error.
- **RA's counter**: Accepted the ndjson reframe makes Postgres a non-permanent projection. If rebuildable, no substrate is permanently locked.
- **Hawk's counter**: Storage integrity was the scope. Retrieval gate is a separate decision.
- **Why unresolved**: DA argues the scope-limitation itself is the problem — you can't scope a permanent substrate decision to "storage only" when retrieval is what justifies the choice.

### Dispute 2: Future-write uniqueness guard (DA's promoted P1)
- **DA new issue**: When a second snapshot is ingested with the same msg_uuids under a new snapshot_id, the PK allows both rows. What are the semantics of two rows for the same logical message under different snapshot_ids? Is this correct behavior (versioning) or a collision risk?
- **Not engaged by others yet** — new issue introduced in Round 1.
- **Relevance**: If a re-ingested snapshot "corrects" a message (Anthropic changes export format), the floor will silently hold both versions. No mechanism selects "current truth."

### Dispute 3: ndjson floor protection is unspecified (Hawk and RA)
- **Hawk**: The ndjson-canonical reframe relocates the protection requirement onto the ndjson itself. But the ndjson's own protection (write-once enforcement, hash verification, off-site backup) is unaudited. If the ndjson is lost or corrupted, the "canonical floor" is gone.
- **RA**: Relabeling Postgres as a projection dissolves Postgres-specific P0s but introduces a new P1: the canonical floor (ndjson) has no verified protection mechanism described in the decision.
- **Not yet resolved**: What protects the ndjson?

## New Discoveries in Round 1
1. **ndjson-canonical reframe** (Correctness Hawk, accepted by 3/4) — This emerged as the consensus-building mechanism and fundamentally reframes the decision: Postgres is a derived index, ndjson is the verbatim floor. This reframe was not in the original decision text.
2. **Hosted Postgres cannot achieve absolute immutability** (Risk Assessor, confirmed by all) — Platform operator retains root. This is substrate-invariant and applies to NornicDB too.
3. **ndjson floor protection gap** (Hawk + RA convergence) — If ndjson is canonical, its own durability/integrity needs to be specified and protected.

## Convergence Assessment
- Score spread: 3-6 (was 3-6 before round; now 3-6 but clustering at 5-6)
- Dominant recommendation: LOCK-WITH-CAVEATS (3 of 4)
- One holdout: Devil's Advocate (procedural objection about gate scope)
- New issues still emerging: future-write uniqueness guard, ndjson floor protection
→ **Continue to Round 2** (substantive unresolved disputes + new issues)

## Key Unresolved Questions for Round 2
1. Is the substrate-agnostic gate a legitimate objection to lock, or a category error?
2. What are the semantics of multi-snapshot rows for the same logical message?
3. What protection does the ndjson floor itself have — and should that be specified in D9?
4. Does the ndjson-canonical reframe require a formal addendum to D9, or can it be added as a caveat?
