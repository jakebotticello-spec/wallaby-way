# Risk Assessor — Phase 5 Debate Round 2

Carry-in: Round 1 position was 5/10 LOCK-WITH-CAVEATS (up from 3/10 after
accepting the ndjson-canonical reframe). The two Postgres-specific P0s
(JSONB shape, hosted-Postgres mutability) dissolved once we agreed that
ndjson is the canonical immutable artifact and Postgres is a rebuildable
projection. Round 2 resolves *where the actual risk now lives*: it has
migrated out of Postgres and onto (a) the truthfulness of the decision
text and (b) the protection of the ndjson floor itself.

---

## Specific preconditions for LOCK-WITH-CAVEATS

"Decision text corrected" is not cosmetic — under the reframe, D9 is now
locking the *wrong thing in its own words* if left as written. The lock
artifact must describe what is actually being made permanent. Specific
claims in D9 that MUST change:

1. **The object of the lock.** D9 reads as "lock Supabase/Postgres as
   permanent storage." Corrected text: the permanent, canonical artifact
   is the **ndjson corpus**; Supabase/Postgres is a **rebuildable
   retrieval projection** of that corpus, not the floor. This is the
   load-bearing correction — every other caveat depends on it. **PRE-LOCK.**

2. **Immutability claims.** Any D9 sentence asserting that storage in
   Postgres makes the archive immutable must be struck or rewritten.
   Postgres rows are mutable by definition (the projection is
   intentionally rebuildable); immutability is a property of the ndjson
   floor + its hash, not of the database. **PRE-LOCK.**

3. **"Permanent storage" framing.** The phrase implies the DB is the
   system of record. Replace with "durable retrieval index / queryable
   projection." A future operator who rebuilds, migrates, or drops the
   Postgres instance must not believe they are destroying the archive.
   **PRE-LOCK.**

4. **Snapshot semantics statement.** D9 must state, in the decision text,
   that the table is multi-snapshot and that snapshot_id is part of the PK
   *by design* (each snapshot = a versioned copy of the corpus). Without
   this sentence, the uniqueness behavior reads as a bug rather than a
   feature. **PRE-LOCK** (one sentence; cheap; prevents future misreading).

Items 1–4 are all pre-lock because they change *what the artifact says it
is doing*. You cannot lock a decision whose own description is false; the
correction is the precondition, not a follow-up.

---

## Multi-snapshot uniqueness: schema gap or documented constraint?

The DA's P1 (snapshot_id in PK permits two rows for the same
(conv_uuid, msg_uuid)) is **real but mislabeled as a defect**. The design
is intentional: snapshots are versioned corpus copies, so duplicate
(conv_uuid, msg_uuid) across snapshot_ids is *correct* behavior, not
corruption. The genuine risk is narrower: **a retrieval system has no
declared way to know which snapshot_id is authoritative.** "Two rows
exist" is fine; "the reader silently picks the wrong one" is the hazard.

Note the verified ground truth: today (snapshot_id, conv_uuid, msg_uuid)
is unique — 22,801 distinct triples, 0 duplicates. So the *intra-snapshot*
duplicate hazard the DA raises is a future-write possibility, not present
corruption; the live gap is purely *cross-snapshot* "current truth"
resolution.

Assessment: this is a **schema/contract gap, not a design flaw — and it is
a P2, not a P1, because it cannot corrupt the floor.** ndjson is canonical;
the worst case is a *retrieval* error (stale snapshot served), fully
recoverable by re-querying the correct snapshot or rebuilding. It cannot
mutate or lose archive content. That ceilings the severity.

Resolution required (minimum, **PRE-LOCK as documentation**):
- Declare an authoritative-snapshot rule. Cheapest correct form is a
  **`current_snapshots` view** (or a one-row-per-corpus pointer table)
  that resolves "current truth" deterministically — e.g. max(snapshot_id)
  or an explicit `is_current` flag. A view costs nothing to add and
  removes reader ambiguity.
- If the team prefers not to ship the view pre-lock, the **fallback is a
  documented constraint**: D9 states the resolution rule in prose
  ("retrieval MUST filter to the snapshot named in <pointer>; absent a
  pointer, max(snapshot_id) wins") so no reader has to guess.

So: **either the view (preferred) or the documented rule (acceptable) is a
pre-lock requirement.** Shipping the multi-snapshot PK with *neither* is
the only unacceptable outcome. I do not require the view specifically —
I require that "current truth" be deterministic and written down.

---

## ndjson protection: what constitutes adequate protection?

In Round 1 I flagged that the reframe *relocates* the risk: if ndjson is
canonical, then ndjson's own protection — previously unaudited — is now the
whole ballgame. An immutable floor with no integrity check and a single
copy is not a floor; it is a single point of failure wearing a floor's
name. Adequate protection has two tiers.

**PRE-LOCK (integrity + survivability — non-negotiable):**

1. **SHA-256 hash of the ndjson recorded in the lock artifact.** This is
   the cheapest, highest-leverage control and is the *defining* act of
   locking an immutable artifact. Without a recorded hash, "immutable" is
   unverifiable and silent corruption/drift is undetectable. A lock with
   no hash is not a lock. **REQUIRED.**

2. **Off-site backup of the ndjson, separate from Supabase.** If the only
   canonical copy lives in/beside the same Supabase project that we
   explicitly treat as disposable/rebuildable, a single account or storage
   failure destroys the floor. At least one copy on an independent
   substrate (different provider/credentials). **REQUIRED** — durability of
   the canonical artifact is the core of this whole decision.

**POST-LOCK (recovery confidence — strongly recommended, not gating):**

3. **Rebuild-from-ndjson drill.** Demonstrates the projection is actually
   reproducible from the floor, validating the entire "Postgres is
   rebuildable" premise. Extremely valuable, but it proves a property we
   can reasonably assert now and verify shortly after; it does not need to
   block the lock. **POST-LOCK best practice — schedule it, with a date.**

Rationale for the split: hash + off-site backup *establish* the floor's
two essential properties (verifiable integrity, surviving copy). The drill
*confirms recoverability* — important, but a confirmation, not a
constituent. So "all three" eventually; **two pre-lock, one post-lock.**

---

## Final Position

Score: **5/10 | LOCK-WITH-CAVEATS** (held, stable)

I am holding at 5/10, not moving to the DB Specialist's 6/10. The
ndjson-canonical reframe earned the move from 3 to 5 and I stand by it, but
the protection gap I raised in Round 1 is now *specified* rather than
*closed* — and two of its remediations are pre-lock. I cannot ratchet up
until those are committed; equally, none of the disputes is fatal (every
residual risk is a recoverable retrieval/durability concern, not floor
corruption), so the gap does not pull me back to DO-NOT-LOCK. 5/10
conditional is the honest position: lockable, but only with the floor
actually protected.

Ordered caveat list (pre-lock unless marked):

1. **Correct the object of the lock** — D9 states ndjson is canonical;
   Postgres is a rebuildable projection. (text fix)
2. **Strike/rewrite immutability-via-Postgres claims** and the "permanent
   storage" framing for the DB. (text fix)
3. **Record SHA-256 of the ndjson in the lock artifact.** (integrity —
   the defining act of the lock)
4. **Off-site, independent-substrate backup of the ndjson.** (durability
   of the canonical copy)
5. **Deterministic "current snapshot" resolution** — ship a
   `current_snapshots` view (preferred) OR write the resolution rule into
   D9 as a documented constraint. (P2 retrieval contract)
6. **State snapshot semantics in D9** — multi-snapshot by design,
   snapshot_id in PK intentional. (text fix; prevents future misreading)
7. **[POST-LOCK]** Run a rebuild-from-ndjson recovery drill with a
   scheduled date to validate the rebuildable-projection premise.

Caveats 1–6 are pre-lock. Satisfy them and I move to 7/10. Ship the lock
without caveats 3 and 4 specifically and I revert to 3/10 DO-NOT-LOCK —
an unprotected canonical floor is worse than the Postgres-coupling we
started by criticizing.
