# Correctness Hawk — Phase 5 Debate Round 2

Frame I am holding into Round 2: under the **ndjson-canonical reframe** (which I introduced and three reviewers accepted), Postgres is *not* the system of record. The ndjson append-only log is canonical; Supabase/Postgres is a **rebuildable projection** of that log, optimized for query. This reframe is load-bearing for every verdict below. It downgrades the JSONB-as-canonical P0, dissolves the hosted-immutability objection (the property lives in the floor, not the substrate), and defuses the one-way-door framing (you can rebuild the projection, so the lock is reversible at the projection layer). But it relocates risk: **whatever durability/integrity we previously demanded of Postgres, we now owe to the ndjson floor.** A reframe that moves the load-bearing wall does not get to skip inspecting the wall it moved the load onto.

---

## Final Caveat List (ordered, pre-lock vs. post-lock)

A "lock" here means: we declare Supabase/Postgres the permanent storage projection and stop evaluating alternatives. My LOCK-WITH-CAVEATS holds **only if the PRE-LOCK items below are satisfied before that declaration.** They are ordered by correctness-blast-radius (a violation of #1 silently corrupts the canon; a violation of #6 merely inconveniences a future reader).

### PRE-LOCK (must be true/done before the lock is declared)

**P-1. ndjson floor integrity is verifiable, not assumed.**
Minimum bar (see ndjson section below). This is #1 because the entire reframe rests on the floor being canonical. If the floor is corruptible or unverifiable, then Postgres silently becomes the de facto canon again and every dissolved objection reanimates. This is the single item whose failure invalidates the reframe itself.

**P-2. Projection-rebuild is demonstrated, not asserted.**
We claim Postgres is "a rebuildable projection." That claim is currently unverified. Pre-lock, we must *actually rebuild* a Postgres instance from the ndjson floor and diff it against the live instance (row count, content hash per message, snapshot lineage). "Reversible one-way door" is only true if rebuild has been executed at least once. An untested restore path is a backup that does not exist. This is the operational proof that the lock is reversible.

**P-3. Multi-snapshot "authoritative version" selection is defined and enforced.**
DA's P1 is correct that this is unresolved. Pre-lock we must answer, in schema or in documented rule: *given N rows for one logical message across N snapshot_ids, which row is "current"?* See dedicated section. The minimum acceptable pre-lock artifact is a **deterministic selection rule** (a view or a documented, tested query). Without it, "the current state of a conversation" is undefined, and an undefined read against an immutable archive is a correctness defect, not a UX nit.

**P-4. Floor↔projection equivalence check exists (reconciliation).**
A repeatable check that every message in the ndjson floor appears exactly once (per its authoritative snapshot) in Postgres, and vice-versa, by content hash. This is distinct from P-2: P-2 proves rebuild *works once*; P-4 proves the live projection has *not drifted* from the floor over time. Pre-lock we need the check to exist and pass once; running it on a schedule is post-lock.

### POST-LOCK (best practices; their absence does not block the lock)

**B-1. Scheduled reconciliation (P-4 on a cron).** Drift detection over time.
**B-2. Floor durability hardening** — offsite/second-region copy of the ndjson, checksummed. (The *existence* and basic integrity of the floor is pre-lock P-1; geographic redundancy is post-lock.)
**B-3. Materialized "current state" view** if the documented selection rule (P-3) proves too slow at read time. The *rule* is pre-lock; *materializing* it is an optimization.
**B-4. JSONB schema-validation / migration tooling** — under the reframe, malformed JSONB in the projection is repairable by re-projecting from the floor, so this is a convenience, not a correctness gate.
**B-5. Documented projection-rebuild runbook** — P-2 proves rebuild works; writing the repeatable runbook is good hygiene but the proof is what gates the lock.

The pre/post line is principled: **pre-lock = anything whose absence means the canon could be silently wrong or unrecoverable. post-lock = anything whose absence means we are merely slower, manual, or less redundant.**

---

## Multi-snapshot uniqueness: schema gap or design choice?

DA's P1 is a *real* correctness gap, but it is **fixable without abandoning the lock** — so it is a pre-lock caveat (P-3), not a DO-NOT-LOCK trigger.

The precise defect: with `snapshot_id` in the primary key, two rows for the same logical message legitimately coexist under different `snapshot_id`s. The PK guarantees *row* uniqueness; it guarantees nothing about *logical-message* uniqueness. So the question "what is the current text of message M in conversation C?" has no answer defined *by the schema*. The schema is internally consistent — it is just answering a different question (give me every version) than the read path needs (give me the authoritative version).

This is **multi-versioning without a version-resolution rule**, which is a classic correctness pitfall: the data is fine, the *read semantics* are undefined. For an immutable archive this matters more, not less — there is no "the app will overwrite it later" escape hatch.

Verdict on the remedy:
- It is **not** acceptable to merely document the constraint and move on. "Authoritative = max(snapshot_id)" or "= snapshot flagged latest" must be *chosen and made executable*, because every consumer that reads "the conversation" will otherwise improvise its own rule, and divergent improvisations against an immutable store produce divergent truths.
- A **view is the right pre-lock artifact**, but it need not be *materialized*. A plain (non-materialized) view encoding the selection rule, e.g. `DISTINCT ON (conversation_id, message_id) ... ORDER BY ... snapshot_id DESC`, makes the rule canonical and testable. Materialization is a post-lock performance decision (B-3).
- The selection rule must be **tested against the floor**: rebuild a known conversation's "current state" from ndjson independently, and confirm the view returns the same. This folds into P-2/P-4.

So: schema gap, yes — but a gap in the *read contract*, not the *write substrate*. Closeable pre-lock with a documented, tested selection view. Pre-lock requirement P-3.

---

## Substrate-agnostic gate: sufficient for what it claims?

This is the crux DA and the DB Specialist deadlocked on, and as the reviewer whose job is to verify claims, I rule on **the fit between the evidence and the proposition**, not on who argued harder.

**DA is correct on the narrow logical point. The DB Specialist is correct that it is the wrong objection to the decision actually before us.** Both can be right because they are measuring the gate against two different propositions.

The DA's argument, stated precisely: a gate that only establishes substrate-*agnostic* properties (durability, immutability, queryability — things any competent store provides) provides zero evidence that *Postgres specifically* is the right choice. Therefore a storage-only gate cannot justify a storage-specific lock. **As pure logic this is valid and I affirm it.** You cannot derive "choose X" from premises that are equally satisfied by Y and Z. The evidence underdetermines the specific conclusion *as the DA frames the conclusion.*

But here is where I rule for the DB Specialist's *category-error* framing on the **decision actually on the table**: under the ndjson-canonical reframe, **the lock is not a substrate-selection decision. It is a projection-substrate decision over an already-canonical floor.** The properties that *matter for canon correctness* (durability, immutability, integrity) genuinely **do** live in the floor and **are** substrate-agnostic — so a substrate-agnostic gate is *exactly the right shape of gate* for them. The DA's "the gate can't pick Postgres over Mongo" is true but, post-reframe, **answers a question we are no longer asking.** We are not asking "is Postgres the uniquely correct canonical store" (answer: nothing is, the floor is). We are asking "is Postgres an *adequate, reversible, rebuildable projection*." For *that* claim, a substrate-agnostic adequacy gate is sufficient evidence — provided P-2 (rebuild demonstrated) converts "reversible in principle" into "reversible in fact."

So my verdict on **sufficiency of evidence for the specific claim being made**:

- Claim "Postgres is the uniquely correct system of record" — **evidence INSUFFICIENT.** DA wins. We should not, and under the reframe need not, make this claim. If anyone in the panel is still making it, strike it.
- Claim "Postgres is an adequate and reversible query projection over the canonical ndjson floor" — **evidence SUFFICIENT IN PRINCIPLE, contingent on P-2.** The substrate-agnostic gate plus a demonstrated rebuild closes it. DB Specialist wins on the decision actually before us.

The DA's gate critique therefore does not survive as a DO-NOT-LOCK once the conclusion is correctly scoped — **but it survives as a documentation requirement**: the lock decision must explicitly state it is locking the *projection*, not the *canon*, and must not be recorded in a way that lets future readers mistake Postgres for the system of record. I add that as a phrasing constraint on the lock declaration itself (covered by P-2's framing).

Bottom line: a category error *about which decision we are making* — but the DA's underlying logic is sound and is the reason P-2 (rebuild proof) is non-negotiable. The DA's objection is what *earns* P-2 its pre-lock status.

---

## ndjson protection: minimum vs. full bar

I raised this in Round 1; here is the concrete bar. The reframe makes the ndjson the thing the canon's correctness now rests on, so this is pre-lock P-1.

**MINIMUM bar (PRE-LOCK — gates the lock):**
1. **Existence + completeness check.** Confirm the ndjson floor actually contains every message currently in Postgres (count + per-message content-hash match). If the floor is incomplete, it is not canonical and the reframe is false.
2. **Append-only integrity, verified once.** Confirm the floor is append-only in practice (not just intent): a tamper/ordering check — e.g. each line independently parseable, monotonic ordering key present, and ideally a running/terminal hash so a mid-file mutation is detectable. Minimum acceptable: a content hash over the whole floor recorded at lock time, so future drift is at least *detectable*.
3. **One successful rebuild from the floor** (this is P-2; it doubles as proof the floor is sufficient to regenerate the projection). A floor you have never restored from is an assumption, not a floor.
4. **Single-copy durability is acknowledged and the floor is at least as durable as Postgres** (i.e., the floor is not sitting on a less-durable medium than the projection it is supposed to be able to rebuild). It need not be *more* durable yet — that is the full bar.

**FULL bar (POST-LOCK — best practice, B-2):**
5. Geographic / cross-provider redundancy of the floor (≥2 independent copies).
6. Per-line cryptographic chaining (hash-linked log) so any historical mutation is provable, not merely detectable in aggregate.
7. Scheduled integrity re-verification (folds into B-1 reconciliation).
8. Documented retention/immutability guarantees of the underlying floor medium (object-lock / WORM if applicable).

The distinction: the **minimum bar proves the floor is real, complete, and restorable today.** The **full bar makes the floor hard to lose and tamper-evident forever.** We can lock on the minimum because the minimum is what makes the *reframe true*; the full bar is what makes it *robust*, and robustness can be hardened after the lock without re-litigating the decision.

---

## Final Position

Score: 6/10 | LOCK-WITH-CAVEATS

Movement from Round 1 (5 → 6): Round 2 convinced me the disputed items are all **closeable pre-lock**, not lock-blockers — the multi-snapshot gap resolves to a tested selection view (P-3), and the DA's gate critique, while logically valid, dissolves once the conclusion is correctly scoped to "projection, not canon" and is *converted into* the P-2 rebuild-proof requirement rather than left as an open objection. I will not go higher than 6 until P-1 and P-2 are actually *executed*: the reframe that powers this entire verdict is only as true as one demonstrated rebuild from a verified-complete ndjson floor. Lock is justified **conditioned on PRE-LOCK P-1 through P-4 being satisfied before the declaration**; absent any of those, my vote reverts to DO-NOT-LOCK.
