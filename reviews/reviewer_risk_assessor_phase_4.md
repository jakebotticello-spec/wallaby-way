# Risk Assessor — Phase 4 Private Reflection

## Confidence Ratings
- P0 Immutability (hosted): **L** — Once ndjson is the canonical floor, this stops being a P0. A hosted single-Postgres genuinely cannot strip the owner's destructive rights, but that is irrelevant if Postgres is a rebuildable projection rather than the archive of record. I over-escalated by attacking immutability at the wrong layer. The real durability guarantee lives in the immutable ndjson + offsite copies, not in DB grants.
- P0 pgvector absent: **M** — The factual observation (pgvector not enabled/used) is correct and defensible as a labeling/title-accuracy complaint. But framing it as a P0 blocker conflated "the title oversells" with "the decision is wrong." Vector search is an optional projection capability, not a floor requirement. Downgrades to P2 cosmetic/scoping once the floor is ndjson.
- P1 files metadata-only: **H** — This is a real correctness gap regardless of which layer is canonical. If the floor claims "verbatim archive" but the files column only holds metadata and not the bytes/content, the archive is incomplete by its own definition. This survives the reframe intact.
- P1 PITR unverified: **M** — Legitimate to flag that "permanent archive" claims need a tested restore path, but under the ndjson-canonical model, PITR is a convenience for the projection, not the durability backbone. Severity depends entirely on whether ndjson offsite copies are actually verified. Untested-backup risk shifts from Postgres to the ndjson handling.
- P1 Snapshot accumulation: **M** — Real and concrete (each re-export doubles rows, no dedup), but it is an operational/cost problem, not a data-integrity blocker. Bounded growth, easily mitigated with a dedup key or snapshot-id retention policy. Defensible as P1-cost, not P1-correctness.

## Most Defensible Finding
**P1 files metadata-only.** It is layer-independent: it holds whether the canonical store is Postgres or ndjson. If the export pipeline only captures file metadata and not the actual content, then "verbatim/permanent archive" is false on its face, and the gap is silent — nothing in the schema signals that the bytes are missing. This is the one finding I would still raise unchanged at 5/10 LOCK-WITH-CAVEATS, as a required caveat before lock.

## Least Defensible Finding
**P0 Immutability (hosted).** I anchored on a true-but-misplaced systems fact (you can't revoke superuser-equivalent rights from yourself on hosted Postgres) and let it drive a P0 that the architecture never actually depended on. The moment the ndjson-canonical framing surfaced in debate, the entire P0 dissolved — which means it was never a property of the decision, only of my assumed model of the decision. Lesson: confirm the durability layer before assigning severity to durability mechanisms.

## New Issues Noticed on Re-read
1. **ndjson integrity is now the load-bearing assumption but is itself unverified.** By promoting ndjson to canonical, the whole risk case migrates there. I never confirmed checksums/hashing, append-only handling, or offsite replication for the ndjson files. If the floor rests on ndjson, the floor needs a verified write/copy/verify cycle — that should be the new top caveat, replacing the dissolved Postgres P0s.
2. **Re-import determinism untested.** The "rebuildable projection" claim assumes ndjson → Postgres reconstitutes faithfully. No round-trip test was cited. If re-import is lossy (type coercion, ordering, the metadata-only files gap), then "rebuildable" is aspirational, which would re-elevate the files finding and undercut the LOCK.

## Score Adjustment (if any)
Holding at **5/10 LOCK-WITH-CAVEATS**, consistent with where I landed in Round 1. No further movement: the Postgres-specific P0s correctly collapsed under the reframe, but the migration of risk onto unverified ndjson integrity and untested round-trip re-import keeps me from going higher. Required caveats for lock: (1) verify ndjson checksum + offsite copy cycle, (2) resolve files metadata-only vs. verbatim claim, (3) one documented round-trip re-import test.
