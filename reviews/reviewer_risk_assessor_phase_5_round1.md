# Risk Assessor — Phase 5 Debate Round 1

## Position Summary

My Phase 3 score was 3/10, DO-NOT-LOCK. The debate has surfaced one genuinely
clarifying idea — the **ndjson-as-canonical-floor reframe** (DA, Hawk, DB
Specialist all converge on it). I credit it heavily below. It dissolves *most*
of my objections, but only if the decision text is rewritten so that the thing
being "locked" is the ndjson floor, not Supabase Postgres.

Crucially, the panel has been arguing past each other on one axis. The DB
Specialist and the Hawk keep repeating "all gaps fixable without rebuild." That
is *true and irrelevant* to my central P0. My P0 was never "the data needs a
rebuild." My P0 is: **D9 as titled asks us to lock a single hosted Postgres
instance as the permanent immutable archive, and that specific artifact cannot
be made immutable by any post-lock patch, because the platform operator and the
project owner retain irrevocable destructive authority over it.** No REVOKE, no
trigger, no role split touches that. The fix is not a patch — it is *changing
what we lock*. That is exactly the ndjson reframe. So I am not in conflict with
the reframe; I am in conflict with the **title of the decision**.

If the title changes, my score moves a lot. If we lock Supabase-as-archive as
literally written, my score does not move.

## Engagements

### vs DB Specialist + Hawk: "All gaps fixable without rebuild"

This consensus is correct on its own terms and I accept it for the data-content
gaps (JSONB key reorder, dup-key collapse, missing `content_blocks_raw`, missing
TRUNCATE revoke, Seq Scan on parent lookup). Those are all forward-only,
non-destructive, additive fixes. The Specialist is right that not one existing
row must be touched. I withdraw any implication that these specific gaps require
a rebuild — they never did, and saying so was imprecise on my part.

But "fixable without rebuild" answers a question I did not ask. There are two
distinct immutability claims fused in D9:

1. **Tamper-evidence / write-discipline** — can ordinary application roles
   mutate or truncate the floor? This is what REVOKE TRUNCATE + guard trigger +
   `floor_reader`/`floor_writer` role separation address. The Specialist's
   remediation genuinely closes this. I concede it fully.

2. **Tamper-impossibility against the privileged principal** — can the entity
   that owns the Supabase project (and Supabase itself, as platform operator)
   destroy or rewrite the archive? In a single hosted Postgres instance the
   answer is permanently *yes*. A superuser/owner can `DROP TRIGGER`, `ALTER
   TABLE`, restore a doctored snapshot, or delete the project. No SQL executed
   *inside* that instance can revoke the authority of the principal who can
   re-grant it. This is not a missing patch; it is a property of hosted Postgres.

The consensus collapses (1) and (2). My P0 lives entirely in (2). "Fixable
without rebuild" is true for (1) and *structurally inapplicable* to (2) — you
cannot patch your way out of who owns root. So the distinction is meaningful,
and the Specialist's remediation list, while correct, does not reach it.

Where this lands: (2) is only a *lock-blocker* if D9 claims the Postgres
instance itself is the immutable permanent archive. If D9 instead claims
"Postgres is a rebuildable projection; ndjson is the floor," then (2) stops
being a defect and becomes an accurate description of the projection's status.
That is the reframe, and it is the resolution.

### vs Hawk: "ndjson as canonical source" reframe

This largely resolves my immutability P0 — with a precisely bounded residual.

If ndjson is the designated verbatim canonical floor and Postgres is an
explicitly rebuildable projection, then yes: a wiped or tampered projection is a
*recoverable* event, not a *catastrophic* one. The threat model for the
projection drops from "loss of the archive" to "downtime + cost of rebuild,"
which is an operational annoyance, not a P0. I accept this. My immutability
concern, *as applied to Postgres*, dissolves under the reframe.

The residual risk does not disappear — it **relocates** from Postgres to the
ndjson floor, and the panel has not yet scrutinized the floor with the same
rigor it applied to the JSONB:

- **The floor inherits the immutability burden.** Whatever guarantees we wanted
  from "permanent immutable archive" must now be proven of the ndjson, not the
  DB. Where do the ndjson files live? If they live in the same Supabase project
  (Storage bucket) under the same owner credential, the reframe is cosmetic —
  the same privileged principal can delete the bucket, and we have relabeled the
  problem rather than solved it. The reframe only works if the floor has an
  *independent* durability/immutability story (object-lock / WORM storage,
  off-platform replication, or content-addressed hashing + external anchoring).

- **Projection-floor divergence detection.** Once Postgres is "just a
  projection," any silent drift between projection and floor is a correctness
  hazard for every downstream consumer that trusts the DB. The reframe is only
  safe if there is a verifiable rebuild: a deterministic ndjson→DB transform
  plus a hash/row-count reconciliation proving the projection faithfully
  represents the floor. Without that, "rebuildable" is an assertion, not a
  guarantee.

So: reframe accepted, P0-on-Postgres-immutability withdrawn, **new P1 raised on
the floor's independent durability and rebuild-verifiability.** Net, this is a
downgrade in my overall severity, not a wash.

### vs DB Specialist: pgvector sidecar sufficient?

The sidecar proposal is architecturally correct and I endorse it — pgvector
indexes are derived, mutable, re-tunable artifacts and have no business inside an
immutable floor table. The Specialist is right.

But this concedes my actual pgvector point rather than rebutting it. My P0 was
not "put pgvector in the floor." It was narrower and is about the **decision
document's factual accuracy**: D9 is (per the panel framing) titled/justified in
terms of pgvector-backed semantic retrieval, and pgvector is *not installed
today*. You cannot lock a decision whose stated justification rests on a
capability that is empirically absent at lock time. That is a premise defect, not
an architecture defect.

The sidecar plan actually proves my point: if the right home for vectors is a
*separate, later-built* component, then semantic retrieval is **not yet
designed**, which means the read-pattern that supposedly motivates choosing
Postgres has not been validated (this is exactly the DA's "sequencing inversion"
and "checks are substrate-agnostic" line, and I now align with it).

Resolution: I downgrade pgvector from P0 to **P1**, conditional on the decision
text being corrected to remove/restate any present-tense pgvector claim and to
acknowledge vectors as a future sidecar. If the text keeps asserting pgvector as
a current capability, it stays a P0 factual error. The remedy is a one-line
honesty fix, so it should not block lock by itself — but it must be made.

### Files column: block or document?

I am modifying this down. My original framing ("files column stores metadata
only — verbatim archive incomplete") overstated the blocking severity.

Facts I will commit to: the `files` column holds JSONB metadata
(filenames/sizes/refs), not attachment bytes; some records have non-empty `files`
arrays, so attachments are not hypothetical; but the population of
attachment-bearing conversations is a minority, not the bulk of the corpus. (I do
not have an exact count and will not fabricate one — see falsification note.)

Severity analysis: this is a **scope-of-claim** problem, not a data-integrity
problem. The data that *is* stored is fine. The risk is solely that a reader of
D9 believes "verbatim archive" includes file bytes when it does not. Under the
ndjson-canonical reframe, the correct fix is to state explicitly: *the floor
archives the conversation transcript and file metadata; raw attachment bytes are
out of scope (or stored separately at ref X).* That is a **documentation fix**,
not a rebuild and not a lock-blocker.

I therefore downgrade files from P1 to **P2 (documentation/scope-honesty)**, with
one carve-out: if any downstream consumer is *promised* byte-level attachment
recovery from this floor, the gap re-escalates, because then it is a broken
guarantee rather than an unstated scope boundary.

### PITR under ndjson-canonical model

The DA's reframe genuinely defuses most of this. If "permanent" is delivered by
the ndjson floor and Postgres is a rebuildable projection, then PITR on the
*projection* is an operational nicety (faster recovery), not a durability
guarantee. Losing the projection without PITR costs a rebuild, not data. I
withdraw PITR as a Postgres-side lock-blocker.

But the durability requirement does not vanish — it **transfers to the floor**,
same as immutability did. "Permanent archive" still demands a tested,
demonstrable recovery story *for the ndjson*. The panel has tested nothing on the
floor: no proof the ndjson is backed up, replicated off-platform, or restorable.
So PITR-on-Postgres drops to non-issue, but **"untested durability of the
canonical floor" is a live P1** and is, frankly, the most under-examined risk in
the entire panel — everyone reframed the hard guarantee onto the ndjson and then
nobody audited the ndjson.

Net: PITR-as-written = withdrawn; floor-durability-untested = P1, folded into the
same residual I raised against the Hawk.

## P0 Falsification Checks

I now maintain **one** P0 (down from the multiple I carried into Phase 3), and it
is conditional on the decision text. Single-observation falsifiers:

- **P0 (maintained, conditional): "D9 as literally titled locks a single hosted
  Postgres instance as the permanent immutable archive, which is
  architecturally unachievable."**
  *Falsified by:* a single observation that the decision text does **not** in
  fact designate Postgres as the canonical immutable archive — i.e., the
  document already names ndjson (or an external WORM floor) as canonical and
  Postgres as a rebuildable projection. If that sentence is already in D9, my P0
  is wrong and collapses to "no action needed." (This is why my P0 is really an
  objection to the *title/claim*, and is curable by one paragraph.)

- **P0→P1 (downgraded): pgvector premise.**
  *Falsified by:* observing that `\dx` / `pg_extension` shows pgvector installed
  and an actual vector column populated at lock time — OR observing that D9's
  text makes no present-tense pgvector claim. Either observation removes the
  factual-error charge.

Conceded as not-P0 (moved to P1/P2 above): JSONB verbatim (Specialist's additive
column fixes it), TRUNCATE/role discipline (Specialist's REVOKE+trigger fixes
it), files column (documentation), PITR-on-Postgres (rebuildable).

## Revised Position

I moved. The ndjson-canonical reframe is the right architecture and it dissolves
my immutability and durability objections *as applied to Postgres*. My remaining
hard line is narrow and entirely about decision-text honesty: do not lock a
document that claims hosted Postgres is the permanent immutable archive or that
asserts present-tense pgvector. Fix those two sentences (and add the floor's
durability/rebuild-verification story), and I am at LOCK-WITH-CAVEATS.

The residual risk I am now loudest about is the one the panel under-examined:
having relocated every hard guarantee onto the ndjson floor, **no one has audited
the floor** for independent durability or verifiable rebuild. That gap must be a
named caveat, not an assumption.

Score: 5/10 | DO-NOT-LOCK (as written) / LOCK-WITH-CAVEATS (if decision text is
corrected to ndjson-canonical + pgvector-honest + floor-durability caveat)
