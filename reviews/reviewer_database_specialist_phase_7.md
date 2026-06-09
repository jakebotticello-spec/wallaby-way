# Database Specialist — Phase 7 Blind Final Assessment

Score: 6/10
Recommendation: LOCK-WITH-CAVEATS

## Top 3 Findings (the ones that most affect the verdict)
1. **Scope-the-verb is the gating defect.** "Permanent storage for an immutable conversation archive" overstates what Supabase actually delivers. Supabase is a managed Postgres surface: it gives durable, transactional, point-in-time-recoverable storage — but "immutable" is an application-layer property, not a substrate guarantee. Postgres rows are mutable by definition; immutability must be enforced by append-only schema design, RLS/grant restrictions, and disabled UPDATE/DELETE paths. Until the lock artifact renames the claim to a "value-preserving projection" backed by named integrity controls, the verb is writing a check the substrate doesn't cash. This is the single finding most responsible for holding the score at 6 rather than 8.

2. **Multi-snapshot uniqueness is a real design gap (b), not data loss.** The stated intent is versioned snapshots, but there is no defined retrieval/observability contract for selecting "current truth" among snapshots, nor a uniqueness/ordering key that makes snapshot N addressable and distinguishable from snapshot N+1. No bytes are lost, so this is not a durability failure — but it is a future usability and auditability risk. A versioned archive whose versions cannot be deterministically resolved is a query problem waiting to happen. This must be answered by a documented snapshot selection policy before snapshot-2 is written, otherwise the ambiguity compounds.

3. **The ndjson floor is the durability backstop and must be anchored in the lock artifact.** Supabase is the convenience/projection layer; the ndjson export is the substrate-independent floor that survives provider loss, account loss, or schema drift. Locking Supabase without naming the floor and pinning its SHA-256 in the lock artifact would couple the archive's survival to a single managed vendor — the exact single-point-of-failure an "immutable archive" decision is supposed to eliminate. The floor is what makes "permanent" defensible; it is non-negotiable as a lock condition.

## Caveat List (ordered by severity)

**Pre-lock (must be satisfied in the lock artifact before D9 is locked):**
- **C1 — Scope-the-verb (BLOCKING for wording).** Rename "immutable" to "value-preserving projection." The lock artifact must name the actual immutability-enforcement mechanism (append-only design + restricted grants/RLS + no UPDATE/DELETE path), not assert immutability as if it were a substrate property. The substrate-selection rationale must be stated separately from the storage-integrity claim — these are two gates, not one.
- **C3 — Anchor-the-floor (BLOCKING).** The ndjson export must be named explicitly as the substrate-independent durability floor in the lock artifact, with its SHA-256 recorded. The lock is for Supabase-as-projection over a named floor, not Supabase-as-sole-store.

**Post-lock (operational obligations, must be tracked but do not block the lock):**
- **C2 — Current-truth-before-snapshot-2 (must land before second snapshot, not before lock).** Document the snapshot selection/uniqueness policy: how "current truth" is resolved among versioned snapshots, and the addressable key/ordering that distinguishes one snapshot from the next. Required before snapshot-2 is written; the single-snapshot state is unambiguous, so this is post-lock but time-boxed.
- **Durability verification (post-lock, recurring).** Confirm Supabase PITR/backup retention is enabled and that the ndjson floor SHA-256 is periodically re-verified against the live projection so drift between floor and projection is detectable.

## One-line verdict
Lock it — but lock the right thing: a value-preserving Postgres projection over a SHA-pinned ndjson floor (C1 + C3 pre-lock, C2 before snapshot-2), not an "immutable archive" the substrate cannot guarantee.
