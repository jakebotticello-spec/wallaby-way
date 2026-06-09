# Risk Assessor — Phase 7 Blind Final Assessment

Score: 5/10
Recommendation: LOCK-WITH-CAVEATS

## Top 3 Findings (most important to verdict)

1. **Durability floor is unmet without SHA-256(ndjson) + off-site backup.** Locking Supabase as *permanent* storage for an *immutable* archive while the only copy lives in a single managed Postgres instance is the dominant risk. An immutable archive's whole value proposition is that what you read tomorrow is provably what you wrote today, surviving provider failure. Without a content hash over the canonical artifact and at least one off-site copy, "permanent" and "immutable" are aspirational labels, not enforced properties. This is my hard condition: ship the lock without both of these and the correct score is 3/10 DO-NOT-LOCK. With both present pre-lock, the floor is cleared.

2. **The decision text itself encodes claims the architecture cannot honor — four corrections must land before the words are locked.** Because this is a *floor lock*, the prose becomes load-bearing and hard to revise later. (a) "verbatim" must become "value-preserving" — round-tripping through Postgres/ndjson does not guarantee byte-identity, only semantic fidelity; promising verbatim is a promise we will silently break. (b) ndjson must be explicitly designated the canonical artifact, so the hash, backup, and rebuild drill all have one unambiguous referent. (c) pgvector must be struck from the title/scope or deferred — embedding storage is a query-layer concern, not a property of the immutable floor, and binding it into the lock couples a stable durability decision to a volatile retrieval decision. (d) immutability enforcement must be named as a mechanism (append-only / revoked UPDATE-DELETE / WORM-style discipline), not assumed.

3. **Multi-snapshot uniqueness (P2) is a latent integrity defect that becomes load-bearing at snapshot 2.** Today, with one snapshot, the ambiguity is invisible. The moment a second snapshot lands, "which row is current" has no defined answer without a `current_snapshots` view or a documented selection rule. This does not block the lock, but it must be resolved before snapshot 2 is written, or we lock in a schema that silently returns wrong/ambiguous results. Flagging it now keeps it from being discovered as a data-correctness bug later.

## Ordered Caveat List (pre-lock vs post-lock)

### PRE-LOCK (must land before the floor is declared — failure to do these = revert to 3/10 DO-NOT-LOCK)
1. **SHA-256 over the canonical ndjson artifact** — computed, recorded, and verifiable. (Hard condition.)
2. **Off-site backup of the ndjson** — at least one copy outside the single Supabase instance. (Hard condition.)
3. **Decision-text correction: "verbatim" → "value-preserving"** — stop promising byte-identity.
4. **Decision-text correction: ndjson designated canonical** — single unambiguous referent for hash/backup/rebuild.
5. **Decision-text correction: pgvector removed from title/scope OR explicitly deferred** — decouple durability floor from retrieval layer.
6. **Decision-text correction: immutability enforcement named** — specify the append-only/permission mechanism, don't assume it.

### POST-LOCK (required, but do not block the lock)
7. **Rebuild-from-ndjson drill** — prove the canonical artifact actually reconstitutes the archive end-to-end.
8. **PITR confirmation** — verify point-in-time recovery is enabled and tested on the Supabase instance.

### BEFORE-SNAPSHOT-2 (P2 — not a lock blocker, but a correctness blocker for the next write)
9. **Multi-snapshot uniqueness resolved** — ship a `current_snapshots` view or a documented current-selection rule before the second snapshot is written.

## One-line verdict
LOCK-WITH-CAVEATS at 5/10: the Supabase floor is sound enough to lock only once SHA-256(ndjson) + off-site backup and the four decision-text corrections land pre-lock — ship without the hash/backup and I revert to 3/10 DO-NOT-LOCK.
