# Devil's Advocate — Phase 5 Debate Round 1

## Position Summary

I hold DO-NOT-LOCK. My objection is not primarily about the *current state* of the
database (which the DB Specialist correctly shows is fixable without touching existing
rows). My objection is about the *act of locking* — declaring an irreversible,
permanent storage commitment using a gate that was scoped so that it cannot, even in
principle, distinguish a good permanent substrate from a bad one. The lock is a
substrate decision; the gate is a value-fidelity check. They are not the same question,
and you cannot answer the first with the second.

I retain the substrate-agnostic-gate objection as my strongest point, I accept that
the reframe (ndjson canonical, Postgres projection) moves the *fidelity* P0s down, and
I promote one genuinely new, unaddressed P1: there is no future-write uniqueness guard,
so post-snapshot ingests can produce semantically colliding rows that no trigger
currently forbids.

## Engagements

### Substrate-agnostic gate: still valid?

The Hawk's response — "the gate was scoped to storage-integrity only, not to substrate
comparison" — is accurate as a description and is *exactly* the problem, not a defense.

A lock is by construction a substrate decision: "Supabase is the permanent floor,
forever." If the gate that authorizes that decision is admittedly incapable of
comparing substrates, then the gate is the wrong instrument for the decision being made.
You can pass a storage-integrity gate on *any* substrate that stores values faithfully —
SQLite, a flat ndjson tree, NornicDB, a hosted Postgres. The gate returning PASS tells
you "this substrate did not corrupt the data," which is necessary but says nothing about
whether it is the *right permanent* substrate. Using a substrate-blind gate to ratify an
irreversible substrate choice is a category error: it launders "did not corrupt values"
into "is the correct forever-home."

The pgvector-not-installed finding reinforces this. The decision is titled around Supabase
as a queryable/vector-capable permanent store, yet the one capability that differentiates
"Postgres-the-substrate" from "any value-faithful store" (pgvector) is absent. So at the
moment of locking, the substrate is operating as a generic value store — precisely the
configuration where the substrate choice is *least* differentiated and therefore *least*
urgent to make permanent.

I am NOT claiming "another substrate wins" (retracted in Phase 4 — insufficient data).
I am claiming the gate cannot license a forever-choice. That stands.

Falsification: Show me a gate criterion, as actually run, whose PASS/FAIL would have
*differed* if the same data were loaded into a different faithful substrate. If even one
criterion is substrate-discriminating, my "the gate cannot differentiate substrates"
claim is falsified. I predict none exists.

### "All gaps fixable": what's left to object to?

I concede the DB Specialist's strongest factual point: every listed P0/P1 (JSONB raw
column, REVOKE TRUNCATE + guard trigger, sidecar pgvector, snapshot_id row doubling as a
line-item) is fixable without destroying existing rows. If the objection were *only*
about the DB's current state, that concession would collapse my position toward
LOCK-WITH-CAVEATS.

But that is exactly why I separate state from process. The remaining objection is:

- **Locking is irreversible; the fixes are not yet applied.** "Fixable" is a future
  tense. You do not lock a vault and *then* install the lock's tamper-proofing. The
  immutability mechanism (REVOKE TRUNCATE + guard trigger + dedicated roles) is the thing
  that makes the lock *mean* something. Locking before it exists means locking a store
  that is still freely mutable — the lock is nominal, not enforced.

- **Locking precedes the read patterns that would validate the schema as permanent.**
  This is the process objection (see sequencing, below). A schema chosen with zero
  retrieval evidence is being declared permanent. Even if rows survive, the *commitment*
  is premature.

So: the objection is ~20% residual current-state (the fixes must actually land and be
*tested*, not merely be "fixable") and ~80% process (locking is the wrong verb to apply
before enforcement exists and read patterns are known).

Falsification (P0 immutability-enforcement, promoted): Run, against the live DB, as the
intended application/owner role: `TRUNCATE <table>;`, `DELETE FROM <table> WHERE true;`,
`UPDATE <table> SET ...;`, and `DROP TABLE`. If all four are rejected by an enforced
mechanism *today*, my "lock is nominal/unenforced" claim is falsified for the
operator-role threat. (Note: the Risk Assessor's platform-root residual is a separate,
non-falsifiable-by-SQL layer and I defer to it there.)

### ndjson-as-canonical reframe: enough to unlock?

I proposed this reframe, the Hawk adopts it, and I must honor it: if ndjson is the
*designated, verified* canonical verbatim floor and Postgres is an explicitly
*rebuildable projection*, then the fidelity P0s (JSONB byte-verbatim, the 3 empty
headers / 291-vs-294 discrepancy, snapshot row-doubling) all downgrade. A projection is
*allowed* to be lossy and rebuildable; that is its job. I agree with the Hawk that under
this reframe the JSONB fidelity gap becomes a labeling fix, not a P0.

But the reframe *unlocks the wrong object*. It makes the case for not needing to lock
Postgres at all — if Postgres is a rebuildable projection, what is even being locked? You
do not lock a derived index as a "permanent immutable archive"; you lock the *source*.
So the reframe, taken seriously, redirects the lock decision to the ndjson, and the D9
decision as written ("Supabase as permanent storage") is locking the projection, not the
floor. That is still DO-NOT-LOCK *for D9 as titled*.

What specifically remains blocking after the reframe:

1. The ndjson floor must be *proven* canonical: hash-stable, complete (accounts for all
   294 conversations incl. the 3 empty headers), and demonstrably sufficient to rebuild
   the projection. None of that is shown yet. A canonical floor asserted but not verified
   is not a floor.
2. D9 locks Postgres, not ndjson. Until the decision text is rewritten to lock the floor
   and explicitly demote Postgres to rebuildable projection, the reframe is not yet *in
   force* — it is a proposed amendment. You cannot vote LOCK-SAFE on the strength of an
   edit that has not been made.

So the reframe moves me off the *fidelity* P0s but not off DO-NOT-LOCK, because the thing
being locked is still the projection and the floor is still unverified.

Falsification (P0, downgraded-conditional): Produce a documented, hash-verified ndjson
snapshot AND a successful rebuild of the Postgres projection from ndjson alone with a
row/value diff of zero. If that exists, the fidelity-P0 block is falsified and I drop to
LOCK-WITH-CAVEATS on fidelity grounds. The substrate/sequencing/uniqueness objections
would still need separate clearing.

### Sequencing inversion: resolved by schema flexibility?

The DB Specialist's response — "the schema CAN change as long as existing rows aren't
destroyed; Postgres is schema-flexible" — is true and *does* defuse part of the concern.
Additive evolution (new columns, new indexes, sidecar tables) is genuinely available
post-lock. I concede that fully. It means a *wrong-but-additive* schema decision is
recoverable.

What schema-flexibility does NOT resolve:

- **Primary-key and identity structure is not freely flexible.** Changing the PK,
  changing the uniqueness semantics, or re-keying rows in a table you have declared
  immutable is exactly the "touch existing rows" operation the immutability guarantee
  forbids. So the parts of the schema that are *hardest* to get right without read
  patterns (the key/uniqueness model — see next section) are precisely the parts that
  schema-flexibility does *not* cover post-lock. You get to add columns, not redefine
  identity.

- **Sequencing inversion was never only about columns.** It is about committing identity
  and immutability semantics before any retrieval workload has exercised them. "We can
  add a column later" does not answer "we chose the row-identity model with no evidence of
  how rows will be retrieved or de-duplicated."

So: partially resolved (additive schema = recoverable, conceded), not resolved for the
key/identity layer. Net: the sequencing concern survives at reduced scope — it is now
specifically about *identity/uniqueness* commitments, which dovetails with my new P1.

Falsification: Demonstrate that the PK / uniqueness model can be altered *after* the
immutability lock without violating the no-touch-existing-rows guarantee (i.e., without a
table rewrite / DELETE+reinsert). If PK changes are achievable additively, my "identity
layer is not flexible post-lock" claim is falsified.

### New: future snapshot uniqueness guard

This is my cleanest new contribution and it is not addressed by any other reviewer's
fixes. The PK appears to include snapshot_id, so two rows with the *same* msg_uuid and
*same* conv_uuid but *different* snapshot_id can coexist. The DB Specialist already flags
that snapshot_id "doubles rows per re-ingest" and recommends accepting it as a line-item.
I argue that accepting it silently is wrong, because it is not merely a storage-volume
line-item — it is a *semantic collision* risk:

- A message is identified, in the source conversation, by (conv_uuid, msg_uuid). That
  pair is the natural semantic identity of "this specific message." The current PK lets
  the *same* semantic message exist as N physical rows across N snapshots.

- Is that correct behavior? It depends on an undecided question: do snapshots represent
  *immutable point-in-time captures* (in which case duplicate physical rows are expected
  and the *reader* must always filter to one snapshot) or do they represent *append-only
  corrections* (in which case you need a rule for which row is authoritative)? D9 does not
  state which. Locking before answering means the immutable table bakes in an ambiguity
  that *cannot be re-keyed later* (re-keying = touching existing rows, forbidden by the
  immutability guarantee).

- Concretely: a future ingest of a second snapshot with duplicated (conv_uuid, msg_uuid)
  is *permitted* by the schema with no guard. There is no constraint asserting "a given
  (conv_uuid, msg_uuid) may appear at most once per snapshot" — so even *within* a single
  snapshot, a re-run or partial-retry could insert true duplicates and nothing stops it.
  That is a uniqueness hole, not just a row-count line-item.

The minimal correct behavior, decided *before* lock:
- A UNIQUE constraint on (snapshot_id, conv_uuid, msg_uuid) at minimum, to forbid
  intra-snapshot duplicates (this is the future-write uniqueness guard I called for in
  Phase 4).
- An explicit, documented semantics for cross-snapshot duplicates (point-in-time vs.
  authoritative-latest), since this cannot be retrofitted into an immutable PK.

I promote this to P1 (not P0: it does not corrupt existing rows; it governs future
writes — but it is unfixable-in-the-right-place after lock, which is what makes it
lock-blocking).

Falsification (P1, new): Against the live DB, attempt to INSERT a second row with an
already-present (snapshot_id, conv_uuid, msg_uuid). If the INSERT is rejected by an
existing constraint, the intra-snapshot uniqueness hole is falsified. Separately, point
to documentation stating the cross-snapshot duplicate semantics; if it exists, the
"undecided semantics" half is falsified. I predict the INSERT succeeds and the doc is
absent.

## P1/P0 Falsification Checks

| ID | Severity | Claim | Falsification test |
|----|----------|-------|--------------------|
| DA-1 | P0 (process) | Lock is nominal: immutability not yet enforced at lock time | As owner/app role, run TRUNCATE / DELETE WHERE true / UPDATE / DROP. If all rejected by an enforced mechanism today → falsified |
| DA-2 | structural | Gate cannot license a forever-substrate choice (substrate-agnostic) | Identify one gate criterion, as run, whose PASS/FAIL differs across faithful substrates. One example → falsified |
| DA-3 | P0→conditional | ndjson floor not proven canonical; D9 locks the projection, not the floor | Produce hash-verified ndjson snapshot + zero-diff rebuild of Postgres from ndjson alone, AND D9 text rewritten to lock floor + demote Postgres. Both → falsified |
| DA-4 | P1 (new) | No future-write uniqueness guard; intra-snapshot duplicates allowed; cross-snapshot semantics undecided and un-retrofittable post-lock | INSERT duplicate (snapshot_id, conv_uuid, msg_uuid) is rejected by existing constraint AND documented cross-snapshot duplicate semantics exist → falsified |
| DA-5 | scoped | Sequencing inversion survives for identity/uniqueness layer (not resolved by additive schema flexibility) | Show PK/uniqueness model is alterable post-lock without touching existing rows → falsified |

## Revised Position
Score: 3/10 | DO-NOT-LOCK

Rationale for holding: The fidelity P0s are downgradable under the ndjson reframe (I
concede that to the Hawk), and additive schema flexibility is real (I concede that to the
DB Specialist). But the lock is a substrate/identity commitment, and (a) the gate cannot
discriminate substrates, (b) the immutability enforcement that gives the lock meaning is
not yet in force, (c) the reframe redirects the lock to ndjson while D9 still locks the
projection, and (d) the identity/uniqueness model — the one layer schema-flexibility
does NOT make recoverable — is undecided. LOCK-WITH-CAVEATS becomes available the moment
DA-1, DA-3, and DA-4 are cleared with the tests above; until then, do not lock.
