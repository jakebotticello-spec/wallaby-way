# Correctness Hawk — Phase 7 Blind Final Assessment

Score: 6/10
Recommendation: LOCK-WITH-CAVEATS

## Top 3 Findings (most important to verdict)

1. **Rebuild-proof is the load-bearing correctness gate, and it is not yet demonstrated.** The entire case for locking Supabase as permanent immutable storage rests on the claim that the floor can be reconstructed faithfully. That claim is currently asserted, not proven. The decision must not lock until a SHA-256-pinned ndjson floor artifact exists AND a rebuild from that ndjson has been executed and verified to reproduce the floor byte-/record-faithfully. This is the correct reframe of DA's gate logic: procedurally his gate is valid, but under the ndjson framing it collapses cleanly into a single concrete, testable requirement — show the rebuild. Until that runs green, the lock is built on an unverified premise.

2. **The decision record contains unreconciled integrity anomalies that directly undercut a correctness claim.** The empty-record count and the 3 empty headers in the decision record are small in isolation but fatal in posture: you cannot certify a floor as immutable and authoritative while line-items in its own provenance record are unexplained. These must be reconciled (explained, corrected, or formally accepted with rationale) before lock. An immutable archive inherits every defect at the moment of locking — anomalies tolerated now become permanent.

3. **The multi-snapshot gap is real but closeable pre-lock; it is P2, not a P0 blocker.** Snapshot selection (which snapshot is canonical / how a consumer picks the authoritative view) is a genuine correctness concern, but it does not require deferring the lock. A tested snapshot-selection view or policy satisfies it. This keeps the gap honest without inflating it into a reason to halt — consistent with my Round 1/Round 2 position that this is closeable in-band. Note also: pgvector is de-scoped from this decision. This is a storage-floor lock only; vector indexing correctness is a separate gate and must not be smuggled into or used to block D9.

## Ordered Caveat List (pre-lock vs post-lock)

### Pre-lock (MUST satisfy before locking — all four)
1. **Floor integrity verified** — SHA-256 of the ndjson floor recorded in the lock artifact; the artifact is the cryptographic anchor of what "the floor" means.
2. **Demonstrated rebuild from ndjson** — an actual rebuild run from the ndjson that reproduces the floor and is verified equal. Not a plan; an executed, checked result.
3. **Tested snapshot-selection view/policy** — a working, tested mechanism for selecting the canonical snapshot, closing the multi-snapshot gap.
4. **Reconcile decision-record anomalies** — empty-record count and the 3 empty headers explained, fixed, or formally accepted with written rationale.

### Post-lock (best practices — implement after lock, not gating)
1. Duplicate-key lint over the floor (catch identity collisions early).
2. Off-site ndjson backup (the ndjson is the true floor; protect it independently of Supabase).
3. Append-only enforcement: append-only triggers + REVOKE TRUNCATE (make immutability structural, not procedural).
4. Parent/conversation indexes (parent_id, conversation_id) for retrieval correctness and performance.
5. Point-in-time recovery (PITR) enabled.

## One-line verdict
LOCK-WITH-CAVEATS at 6/10: lockable once the four pre-lock gates — SHA-256-pinned ndjson, a demonstrated rebuild, a tested snapshot-selection view, and reconciled decision-record anomalies — are green; the rebuild proof is the one that actually matters.
