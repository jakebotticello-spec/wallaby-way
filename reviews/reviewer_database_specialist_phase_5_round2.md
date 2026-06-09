# Database Specialist — Phase 5 Debate Round 2

## Substrate-agnostic gate: category error or legitimate objection?

I called this a category error in Round 1. I am sharpening that, not retracting it — but I now concede the DA has surfaced a real *scoping* defect in the decision text, even if the logical objection is mislabeled.

Two distinct claims are tangled in the DA's "substrate-agnostic gate":

**Claim A (the logical one — still a category error):** "A gate that would also pass on SQLite/NornicDB cannot justify Postgres." This conflates *necessity* with *sufficiency*. A storage-integrity gate is a **screening filter**, not a **selection function**. Its job is to reject substrates that *fail* integrity, not to single out the one substrate that *uniquely* passes. Brakes that work on a Honda and a Toyota do not fail to "justify" the Honda you actually bought — passing a safety gate was never the argument for the purchase. D9 is not the proposition "Postgres is the uniquely optimal store." D9 is "Supabase is *adequate and safe* as the floor's serving substrate." For that proposition, a gate other substrates would also pass is exactly the right shape of evidence: it proves the floor is portable (good — that is the ndjson-canonical thesis working as designed) AND that this substrate clears the bar. Demanding a gate that *only* Postgres passes would be demanding we prove a falsehood, because the whole Round 1 reframe established the substrate is **not** load-bearing. The DA cannot have it both ways: he won the "substrate-invariant immutability" point in Round 1 precisely because substrate doesn't matter for the floor — he cannot now demand the lock gate prove that substrate *does* matter.

**Claim B (the scoping one — legitimate, and I concede it):** "A permanent substrate choice cannot be scoped to storage-integrity only." This is *not* the same argument, and here the DA is partly right. The word doing the damage in D9 is **"permanent."** A *storage-integrity-only* gate legitimately licenses "lock Supabase as the **current** serving substrate for the floor." It does **not** legitimately license "lock Supabase as the **permanent, never-revisited** substrate," because permanence implicates retrieval-fitness, cost-at-scale, query-model fit, and migration cost — none of which were gated. So the answer to the task's framing question — "is it legitimate to lock on storage-only evidence?" — is: **yes for an adequacy lock, no for a permanence lock.** The fix is not more evidence; it is honest scoping of the verb. If D9 says "Supabase is the serving substrate and the ndjson is the canonical floor, revisitable if retrieval/scale evidence later warrants," then storage-only evidence fully supports it, *because the ndjson reframe already guarantees substrate exit is a re-projection, not a migration.* That is the caveat, not a blocker.

**Verdict:** Category error on the logic (Claim A). Legitimate on scoping (Claim B). Does not block lock; converts to a wording caveat (C1 below). The DA's 3/10 over-weights this because he is scoring the literal word "permanent" while the substance — an adequate, exitable serving layer over a canonical file — is sound.

## Future-write uniqueness guard: design gap or correct behavior?

The answer is **(a) is the intended model, but the decision as written delivers (b), and the door to (c) is open.** All three are partially true and they are not mutually exclusive — they are three layers of the same hole.

- **(a) is the correct *design intent*.** With `snapshot_id` as a PK component, each snapshot is a complete, versioned, append-only copy of the corpus as of that ingest. Two rows for the same `(conv_uuid, msg_uuid)` under different `snapshot_id`s is **not corruption** — it is exactly the immutability property we want: snapshot N is never mutated when snapshot N+1 lands. This is the right schema for an immutable archive. Mutating-in-place or `ON CONFLICT DO UPDATE` would be the *actual* P0 here, and the snapshot-as-PK-component design correctly avoids it. So the DA is wrong that this is *prima facie* a defect — it is the load-bearing immutability mechanism.

- **(b) is the real, present gap.** Design intent (a) is *unrealized* because nothing in D9 specifies "current truth." With no `latest_snapshot` view, no `is_current` flag, and no documented convention that authoritative = MAX(snapshot_id) per logical key, a naive `SELECT ... WHERE msg_uuid = ?` returns **N rows for N snapshots** and the consumer must dedup by a rule that exists only in someone's head. That is a retrieval-correctness latent bug, not a storage-integrity bug. It is real and it is unspecified — but note *where* it lives: it is a **retrieval/query-contract** problem, which is the gate the DA himself agrees is separate. It does not threaten the bytes on disk or in the table; both versions are intact. It threatens whoever reads them without the convention.

- **(c) is a possible consequence of (b), not an independent integrity gap.** If snapshot 2 "corrects" a message, both original and correction are stored — but in an *immutable archive that is exactly desired*. The "silent" part is the defect: nothing flags that msg X differs across snapshots, so a diff/correction is invisible without a cross-snapshot comparison. This is a **discoverability** gap, not a **durability/integrity** gap. The corrected and original bytes are both present and both recoverable from the ndjson floor regardless. So (c) does not lose data; it can hide that a change occurred. That is a P2 observability item, not a P0/P1 data-loss item.

**Does it block lock?** No — but it requires a caveat, and it sharpens what the lock *is*. Because the current-truth selection rule lives in retrieval, and because the ndjson floor is canonical and append-only-by-snapshot independent of the table, the worst case is "queries return ambiguous results until a `latest` view/convention is added" — fully recoverable, never lossy. This is a **specify-before-second-ingest** condition (C2), not a stop-the-lock condition. Critically: today there is exactly **one** snapshot, so the ambiguity is currently latent, not active. The guard must be specified *before snapshot 2 is ingested*, which is comfortably after the lock.

## ndjson protection: in-scope for D9?

Partly in-scope, and this is where I move *toward* Hawk + RA. The Round 1 reframe did something the decision must now own: it **promoted the ndjson from artifact to canonical floor.** Once you say "the ndjson is the unlosable thing and Postgres is a recoverable projection," the ndjson's own durability/integrity is no longer an external concern — it has become **the single point of failure for the entire D9 thesis.** You cannot rest a "recoverable projection" argument on a floor whose own protection is unaudited; that is circular. If the floor can rot, the projection's recoverability is fiction.

So I split it:

- **In-scope for D9 (must be stated, blocks nothing if added):** the *existence of a protection requirement* and a minimal integrity anchor. Concretely: (1) a recorded content hash of `records.ndjson` (the path `...\baseline-2026-05-25-ae015455\scrub-v1\` already embeds `ae015455`, suggesting a digest convention exists — D9 should *cite* it as the floor's integrity anchor, not leave it implicit), and (2) a one-line assertion that the canonical floor is the object of record and any DB row is verifiable against it. Without this, D9's own reframe is unsupported by its own logic. This is C3.

- **Out-of-scope for D9 (separate architectural decision):** the *full backup/replication/offsite/retention regime* for the ndjson — geo-redundancy, immutable object-store WORM, restore drills. That is a storage-architecture decision in its own right and should not be smuggled into a substrate-lock decision. D9 should *name the dependency* ("floor durability TBD under separate decision") rather than *solve* it.

The session-level read-only state of the file is incidental and gives no durability guarantee — it protects against accidental edit in *this* session only, not against bit-rot, deletion, or single-disk loss. It is not a substitute for C3.

## Final Position

Score: **6/10 | LOCK-WITH-CAVEATS** (held from Round 1; convictions sharpened, not moved)

Required caveats for LOCK-WITH-CAVEATS:

- **C1 — Scope the verb.** D9 must say "Supabase is the **serving substrate** for the canonical floor, revisitable if retrieval/scale/cost evidence later warrants," NOT "permanent, never-revisited substrate." Storage-only evidence supports an adequacy-and-exitability lock; it does not support an unqualified permanence lock. (Addresses DA Claim B; defuses the substrate-agnostic objection by aligning the claim with the evidence.)

- **C2 — Specify current-truth selection before snapshot 2.** Document the authoritative-version rule (recommend: `is_current` flag or a `latest_snapshot` view keyed to MAX(snapshot_id) per logical key) AND a cross-snapshot change-detection/flag so corrections are not silent. Must land before the second ingest, not before the lock. Currently latent (one snapshot exists). (Addresses DA P1 / options b + c.)

- **C3 — Name and anchor the floor.** D9 must (a) declare `records.ndjson` the canonical object of record, (b) cite/record its content hash as the integrity anchor that any DB row is verifiable against, and (c) name floor durability (backup/WORM/retention) as an explicit out-of-scope dependency to be decided separately. (Addresses Hawk + RA; closes the circularity in the reframe.)

None of C1–C3 is a data-loss risk; all are recoverable from the ndjson floor and all are pre-second-ingest specification work, not pre-lock blockers. Hence LOCK-WITH-CAVEATS, not DO-NOT-LOCK.
