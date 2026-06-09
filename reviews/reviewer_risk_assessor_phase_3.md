# Risk Assessor — Phase 3 Independent Review

Score: 3/10
Recommendation: DO-NOT-LOCK

## Summary (100 words)

The substrate carries floor-grade data integrity (UUID set-equality and forest integrity hold), but a one-way "immortal" lock is being applied to a substrate with no immutability enforcement, a missing pgvector extension named in the decision title, JSONB columns that are already byte-mutated, and snapshot_id-leading PK semantics that have no "current state" query path. The most dangerous property of this decision is its irreversibility colliding with destructibility: nothing in the database prevents TRUNCATE or DELETE today, yet the label promises permanence. Locking now converts every deferred problem into a permanent defect. Add enforcement and a maintained external backup first.

## Findings (P0/P1/P2/P3 with epistemic labels)

Epistemic labels: [CONFIRMED] = from verified ground truth; [DERIVED] = logical consequence of confirmed facts; [PROJECTED] = adversarial simulation of a plausible future event; [ASSUMPTION] = stated belief I could not verify and flag as such.

---

### P0-1 — "Immortal" label on a fully destructible substrate (CONFIRMED + PROJECTED)

[CONFIRMED] No DB-level immutability exists. `postgres` owner has UPDATE/DELETE/TRUNCATE. `anon`/`authenticated`/`service_role` have TRUNCATE. RLS is enabled with ZERO policies. No triggers. The word "immortal" describes intent, not a single enforced guarantee.

[PROJECTED] Concrete destruction scenarios that survive all four checks and bite later:
- A Supabase dashboard "Reset database" / migration-squash operation, or a `supabase db reset` run against the wrong project ref by a developer who believes they are on staging. TRUNCATE is permitted to `service_role` — the role most automation uses.
- A future ORM/migration tool (Prisma, Drizzle, sqitch, Flyway) introduced for the *retrieval* or *embedding* layer that emits `DROP`/recreate or `TRUNCATE ... CASCADE` during a "sync schema" step. The embedding layer is explicitly coming, so this is a near-certain future actor on this database.
- A CI/CD seed script that runs `TRUNCATE` to give tests a clean slate, pointed at prod via a leaked or defaulted connection string (Supabase pooler URL is a single string; one env-var mistake is sufficient).
- The owner role doing a bulk `UPDATE` to "fix" a perceived encoding issue in `content_blocks`, silently rewriting the verbatim record.

[DERIVED] Blast radius = total. Heap is only 19 MB; a single statement wipes the entire floor in well under a second. There is no row-level granularity to limit damage.

[CONFIRMED-as-gap] Remediation in hosted Postgres is partial at best:
- A `BEFORE UPDATE OR DELETE OR TRUNCATE` trigger raising an exception blocks DML/TRUNCATE — but the table owner can `ALTER TABLE ... DISABLE TRIGGER` or `DROP TRIGGER`, so it is not tamper-proof against the owner.
- `REVOKE TRUNCATE` from `anon`/`authenticated`/`service_role` is straightforward and SHOULD be done before any lock, but the owner retains everything.
- True immutability in hosted Supabase is not achievable at the DB layer because you cannot remove the owner's superuser-equivalent rights on your own project. The only durable immutability is an EXTERNAL, write-once copy (object-lock storage). Therefore the "immortal" claim cannot be honored inside Supabase alone. Locking the decision ratifies a guarantee the platform cannot provide.

Why this is P0 for a one-way door: irreversibility (cannot un-lock) combined with destructibility (can lose all data) is the worst possible pairing. You cannot later choose a more durable substrate, but the chosen substrate can be emptied by a single command.

---

### P0-2 — Decision title names pgvector; pgvector does not exist (CONFIRMED + DERIVED)

[CONFIRMED] `pg_extension` lists pg_stat_statements, pgcrypto, plpgsql, supabase_vault, uuid-ossp. No `vector`. No vector column anywhere. The decision is titled "Supabase (Postgres + pgvector)."

[DERIVED] The lock is being made against a substrate that does not match its own description. This is a correctness defect in the decision artifact itself, independent of any data issue. Two readings, both bad:
- If "pgvector" is load-bearing (the floor is meant to host embeddings), then the substrate is not ready and the lock is premature.
- If "pgvector" is aspirational and embeddings will live in a *separate* table, then the title is misleading and the real architecture (floor = verbatim text; embeddings = derived sidecar) was never actually decided.

[PROJECTED] When the embedding layer arrives:
- Installing pgvector itself is low-risk and reversible (`CREATE EXTENSION vector`). That part is fine.
- The hazard is the *shape*. If anyone proposes adding a `vector` column to `floor_conv_messages` (the immutable table), that is an ALTER + backfill UPDATE on the "append-only-immortal" table — directly contradicting immutability and re-touching all 22,801 rows. An adversary (or a well-meaning engineer optimizing for join locality) will be tempted to do exactly this because co-locating the embedding with the row is the obvious design.
- Safe path [ASSUMPTION about intent]: embeddings belong in a SEPARATE derived table keyed by `(snapshot_id, conv_uuid, msg_uuid)`, never altering the floor. This should be written into the lock as a constraint, or the lock will be read as license to mutate the floor for vectors.

Why P0: the decision asserts a capability (pgvector) the substrate lacks, so the artifact being locked is factually wrong as written.

---

### P1-1 — JSONB is not verbatim; this permanently forecloses content hashing / Merkle proofs (CONFIRMED + DERIVED + PROJECTED)

[CONFIRMED] `text` and timestamp columns are byte-verbatim. JSONB columns (`content_blocks`, `attachments`, `files`) are NOT: key reorder (198/200), whitespace strip, `\u` un-escape (1479 source lines altered), dup-key collapse (last-wins, silent value loss), number normalization. Round-trip is 4/300 byte-identical, 300/300 deep-equal.

[DERIVED] A hash chain / Merkle tree over the *as-stored* JSONB cannot reproduce the source bytes. Any integrity proof must be computed over the *original ndjson*, not the database. So the database is, by construction, NOT a self-certifying archive. For a "verbatim floor" this is a category error: the floor cannot prove it is verbatim from its own contents.

[PROJECTED] Downstream use cases this blocks, permanently, once locked:
- Tamper-evidence ("has any row been altered since ingest?") — impossible against JSONB columns without an external golden hash of the ndjson.
- Legal/provenance attestation ("this is exactly what Anthropic exported") — defeated by silent dup-key last-wins collapse, which loses data with no record. Current snapshot has 0 dup keys, but there is NO GUARD against future snapshots.
- Cross-substrate migration verification later (e.g., if NornicDB is ever revisited despite the lock) cannot byte-compare; only semantic compare, which masks exactly the failure modes (dup-key loss) you most need to catch.

[PROJECTED] Format-drift trigger: if Anthropic's export ever emits duplicate JSON keys or different number forms, JSONB will silently normalize/collapse on ingest and NO check will fire (round-trip uses deep-equal, which also collapses). Value loss would be invisible. The only defense — storing the raw line as `TEXT` alongside the JSONB — is not present and cannot be retrofitted onto already-ingested historical snapshots after lock.

Why P1 not P0: the `text` column IS verbatim and is where the substantive content lives; deep-equality holds today. But "verbatim archive" is the stated purpose, and JSONB verbatim is already violated, so this is a named-goal failure.

---

### P1-2 — snapshot_id-leading PK has no "current state" query and unbounded duplication (CONFIRMED + DERIVED + PROJECTED)

[CONFIRMED] PK is `(snapshot_id, conv_uuid, msg_uuid)`, snapshot_id leading. Each new snapshot doubles rows. No dedup between snapshots. No index on `conv_uuid` alone. Only PK btrees exist.

[DERIVED] "Current state of conversation X" is not a primitive query. It requires first resolving "what is the latest snapshot_id," then filtering. Because snapshot_id leads the PK, a query for a single conv_uuid across snapshots cannot use the PK efficiently (the leading column is unconstrained) → degrades toward scan. There is no `conv_uuid`-alone index to rescue it.

[PROJECTED] At 5 re-exports: 114,005 rows, ~5× storage, ~5× scan cost on every un-indexed access path (and parent lookup is ALREADY a Seq Scan, cost 0..2826, with one snapshot). Growth is multiplicative, not additive.

[PROJECTED] snapshot_id sort hazard: if snapshot_id is a string/timestamp without zero-padding or a non-monotonic value, "MAX(snapshot_id) = latest" can be wrong (lexical sort: "10" < "9"). [ASSUMPTION] the type of snapshot_id was not provided; this is a latent ordering bug that, if present, makes "latest snapshot" silently incorrect. Must be verified and documented before lock.

[DERIVED] These are post-lock-survivable because indexes and snapshot-resolution views are ADDITIVE (don't alter floor data) — so this is downgradable to P1: it is fixable after lock via new indexes and a `latest_snapshot` view. It still must be designed before declaring the floor "ready," because the lock implies the schema/PK is final.

---

### P1-3 — Single hosted substrate + unverified durability for a multi-year "permanent" claim (CONFIRMED-context + PROJECTED + ASSUMPTION)

[CONFIRMED-context] "Permanent archive" over years; Supabase is a hosted third party (pooler aws-1-us-east-2). The ndjson snapshot exists.

[ASSUMPTION/UNKNOWN] PITR configuration, whether a restore has ever been tested, whether the ndjson is being actively maintained as a backup — NONE of these were provided as confirmed. For a "permanent immortal" decision, the absence of confirmed, tested durability is itself a finding.

[PROJECTED] Failure modes:
- Supabase free/low tier projects can be PAUSED for inactivity; a paused project's data can become inaccessible or be purged per retention policy. A "permanent archive" must not sit on a tier with inactivity-pause semantics. [ASSUMPTION] tier unknown — must verify.
- Company/pricing/deprecation risk: a hosted dependency for a "for-years" artifact needs an exit copy. The ndjson IS that copy — but only if it is (a) the verbatim source-of-truth, (b) externally stored, (c) integrity-checked. Given JSONB is not verbatim, the ndjson is in fact the ONLY verbatim artifact — which means the ndjson, not Supabase, is the real floor. Locking Supabase as "the floor" mislabels which artifact is authoritative.

[DERIVED] The correct durable architecture is: ndjson (write-once, object-locked, hashed) = canonical floor; Supabase = a queryable, rebuildable PROJECTION of it. Under that framing the lock is far safer (Supabase becomes replaceable). The decision as written inverts this (Supabase = immortal floor), which is the riskier of the two framings.

Why P1: durability is achievable and the ndjson likely already provides it; the defect is the labeling/authority question, plus unverified PITR/restore.

---

### P2-1 — Read access model undefined at lock time (CONFIRMED + DERIVED)

[CONFIRMED] RLS enabled, zero policies → all non-superuser reads fail by default. `service_role` can read but ALSO TRUNCATE. Retrieval layer is explicitly deferred.

[DERIVED] Today the only role that can read the floor is also a role that can destroy it. There is no read-only consumer identity. When the retrieval layer is built, the path of least resistance is to give it `service_role` (read + TRUNCATE + everything) because no scoped reader exists. That is the exact mechanism for P0-1's accidental-TRUNCATE scenario.

[DERIVED] Remediation is additive and should precede lock: create a dedicated read-only role/RLS policy (`SELECT` only, on both tables), and REVOKE TRUNCATE from `service_role`/`anon`/`authenticated`. These do not touch floor data and are reversible — there is no reason to defer them past the lock.

Why P2: fixable after lock without data risk, but cheap and should be done now; leaving it sets up the P0 failure.

---

### P2-2 — TEXT timestamps lock out temporal queries (CONFIRMED + DERIVED)

[CONFIRMED] `created_at`/`updated_at` are TEXT (byte-verbatim, no tz coercion). No date/range index. Every temporal predicate requires per-row casting + full scan.

[DERIVED] "Conversations from last month" / date-range retrieval will be full-scan-with-cast at 22,801 rows now and 114,005+ across snapshots. This is a performance defect, not a data-loss defect.

[DERIVED] Migration path post-lock is ADDITIVE and clean: add a derived `created_at_ts timestamptz` column (or a materialized/derived sidecar table) populated by casting; index it. This does NOT alter the verbatim TEXT, so it is compatible with append-only intent. Therefore temporal queries are NOT actually locked out — they require a derived layer. The risk is only that the lock is read as "schema is final," discouraging the additive column. Document that derived/index columns are permitted.

Why P2: keeping TEXT verbatim is correct for fidelity; the fix is additive and safe.

---

### P2-3 — files column stores metadata only; "verbatim" is incomplete (CONFIRMED + DERIVED)

[CONFIRMED] `files` JSONB stores filenames/sizes, NOT contents. File contents are stored nowhere in this schema.

[DERIVED] For any conversation with user-uploaded files, the archive is incomplete by design — it can name the file but not reproduce it. This is a scope-of-"verbatim" misstatement: the floor is verbatim-for-text, metadata-only-for-files.

[ASSUMPTION/UNKNOWN] The number of conversations with non-empty `files` was not provided in ground truth, so practical blast radius is unquantified. This MUST be measured before lock so the gap is documented, not discovered later. If it is a handful of conversations the gap is acceptable-with-disclosure; if it is many, the "verbatim archive" claim needs explicit scoping.

Why P2: it is a documented-scope issue, not corruption; but it directly undercuts the "verbatim" word in the decision title and the count is unknown.

---

### P3-1 — Latent future-ingest rejection: null bytes (CONFIRMED + PROJECTED)

[CONFIRMED] No null bytes in current text; Postgres TEXT rejects U+0000.

[PROJECTED] A future snapshot containing U+0000 in any text field will FAIL ingest outright. This is fail-loud (good) but means the ingest pipeline has an undocumented constraint that could block a future verbatim snapshot — the archive cannot accept arbitrary future Anthropic exports. Low likelihood, fully surfaced at ingest time, hence P3.

---

### P3-2 — Three zero-message conversation headers (CONFIRMED)

[CONFIRMED] 3 of 294 headers have zero messages. UUID set-equality still confirmed both directions. Not a defect per se (genuine empties exist in source), noted for completeness so it is not mistaken later for data loss.

---

## Verdict with Reasoning

Recommendation: **DO-NOT-LOCK** (at minimum, not as currently described).

Reasoning, weighted for a one-way door:

The data-fidelity checks that passed (UUID set-equality, forest integrity, text-column byte-verbatim, 300/300 deep-equal) are genuinely good and mean the *contents* are sound. If this were a reversible decision, I would say LOCK-WITH-CAVEATS. It is not reversible. For an irreversible "immortal" lock, the bar is not "is the data correct today" but "can this substrate honor the word *immortal*, and are all post-lock-permanent defects acceptable." On that bar it fails on two independent grounds, either of which is sufficient:

1. **The substrate cannot deliver immortality.** There is zero enforcement (P0-1), and in hosted Supabase you cannot strip the owner's destructive rights, so true DB-level immutability is unachievable. A one-line TRUNCATE — runnable today by `service_role`, the very role automation uses — empties the entire 19 MB floor. Locking ratifies a guarantee the platform structurally cannot provide.

2. **The decision artifact is factually wrong as written:** it names pgvector, which is not installed (P0-2). You cannot lock a description that does not match reality without either fixing reality or fixing the description.

The path to a safe lock is concrete and not large:
- (a) Re-frame: the **ndjson becomes the canonical, externally-stored, hashed, write-once floor**; Supabase becomes a rebuildable PROJECTION. This single change makes Supabase replaceable and resolves the immutability impossibility, the JSONB-non-verbatim problem (verbatim lives in ndjson), and the company/durability risk simultaneously. This is the highest-leverage fix.
- (b) Before any lock: `REVOKE TRUNCATE` from anon/authenticated/service_role; add a deny-DML/deny-TRUNCATE trigger; create a read-only role + SELECT RLS policy; verify PITR is on a non-pausing tier and run one test restore.
- (c) Correct the decision title (pgvector absent; declare embeddings live in a separate derived table that never alters the floor).
- (d) Measure and document the `files` content gap and the `snapshot_id` type/ordering before declaring readiness.

Note that many of my own findings are downgradable (P1-2, P1-3, P2-1, P2-2) precisely BECAUSE the right fixes are additive and survive a lock. That is the tell: the substrate is a fine *projection layer*. It is the wrong thing to anoint as the *immortal floor*. Re-frame the floor to the ndjson and apply the enforcement fixes, and this becomes LOCK-WITH-CAVEATS. As written — Supabase-as-immortal-floor, pgvector-named-but-absent, zero enforcement — it is DO-NOT-LOCK.

Score: 3/10 (data contents sound; durability/immutability/labeling unfit for an irreversible "immortal" declaration).
