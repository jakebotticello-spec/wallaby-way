# Devil's Advocate — Phase 5 Debate Round 2

## Substrate-agnostic gate: final position

I accept the "category error" framing — *partially*, and the part I accept is exactly the part that resolves my main objection. The part I do not accept is what generates my one surviving block.

The DB Specialist is right about one thing: the integrity gate was never a substrate-*selection* gate. It tests "does the stored bytestream faithfully preserve the source values, and can I prove it later?" That is a property of an artifact, not a vote between Postgres and anything else. I was wrong to read the gate as a substrate chooser. Conceded.

But here is where the category error cuts *back against* the panel. If the gate only certifies the artifact's integrity, then the gate can only license a lock *on the artifact it certified*. The gate certified ndjson (once ndjson is designated canonical and its hash is recorded). The gate did **not** certify Postgres — Postgres is the projection, and the panel itself now says the projection is rebuildable. So the gate's pass is a license to lock *the ndjson floor*, and nothing more. You cannot launder an integrity pass on artifact A into a forever-lock on artifact B and call the gap a category error on *my* side. The category error runs both directions: a storage-integrity gate licenses a storage-integrity lock *of the thing whose integrity it checked.*

This is no longer a process objection that blocks the decision. It is a **scoping correction to the lock target**. If the decision text says "we lock the ndjson canonical floor; Postgres is a rebuildable, value-preserving projection," the gate fully licenses it. If the decision text says "we lock Supabase/Postgres as permanent storage" (D9's literal title), the gate does *not* license that, because nothing tested the property that makes Postgres permanent-worthy as opposed to disposable. So my main argument survives Round 2 not as "DO-NOT-LOCK" but as a mandatory wording caveat: **lock the floor, not the projection.** That is caveatable. I drop it as a block.

What is NOT a wording fix — and what keeps me adversarial — is that "rebuildable projection" is an *asserted* property, not a *demonstrated* one. The panel dissolved P0s by promising that Postgres can always be regenerated from ndjson. Nobody has run that regeneration and shown byte-or-value equivalence to the live table. A projection you have never rebuilt is a claim, not a fallback. I will accept this as a caveat (a rebuild-and-diff drill) rather than a block, but I want it named, because it is the load-bearing assumption under everyone's comfort.

## Multi-snapshot uniqueness: the concrete failure case

The panel hasn't engaged this, so I'll make it unavoidable. This is the one argument I am *strengthening*, not softening.

**Schema premise (from Round 1):** PK is `(snapshot_id, conv_uuid, msg_uuid)` — or equivalently uniqueness is only guaranteed *within* a snapshot. Two ingests of the same conversation produce two rows with the same `(conv_uuid, msg_uuid)` under different `snapshot_id`.

**Concrete failure case.** Conversation `C`, message `M` is ingested in snapshot 1 (Jan). The same conversation is re-exported and ingested in snapshot 2 (Mar) because three later messages were appended; `M` is unchanged. The table now has `M` twice.

A consumer writes the obvious retrieval query:

```sql
SELECT body FROM messages
WHERE conv_uuid = 'C' AND msg_uuid = 'M';
```

This returns **two rows**. Every downstream assumption that `(conv_uuid, msg_uuid)` identifies one message is now violated:
- A join on `(conv_uuid, msg_uuid)` fans out — row counts double, any aggregate (token totals, message counts) silently inflates.
- A `SELECT ... LIMIT 1` returns a **nondeterministic** winner — snapshot 1's or snapshot 2's row depending on plan/heap order. If snapshot 2 ever *corrected* a field (encoding fix, re-decode), the consumer can get the *stale* version with no error.
- A "reconstruct the conversation" query that orders by timestamp now interleaves two copies of `M`.

**When is it first observed?** Not at lock time — the table looks fine with one snapshot. It is first observed **the day snapshot 2 lands**, which is precisely *after* the lock, when the structure is frozen and hardest to change. That is the trap: the defect is invisible during the exact window in which we are deciding to lock, and becomes load-bearing immediately after. This is the worst possible timing profile for a design gap.

**Why it's a design block, not a query-hygiene problem.** "Just always filter by latest snapshot" pushes a correctness-critical invariant onto every future consumer forever, in an *immutable archive whose whole value proposition is trustworthy retrieval*. An archive that returns two answers to "what did message M say" has failed its core contract, regardless of how clean the bytes are.

**But — and this is my Round 2 concession on this point — it is fixable without touching the locked floor.** A `latest_snapshot` pointer table, or a `current_messages` view defined as "row from the max snapshot_id per (conv_uuid, msg_uuid)," resolves it entirely and lives in the *projection layer*, not the canonical ndjson. Since the panel's reframe makes the projection rebuildable and non-locked, this fix is a post-lock projection change. So my P1 downgrades from "pre-lock block" to "**mandatory caveat that must ship before the second snapshot is ingested**." It blocks *multi-snapshot operation*, not the lock itself — provided the lock artifact records the obligation with a hard deadline (before snapshot 2).

## Is the ndjson reframe + caveat list sufficient to move you?

Yes. Walking the four conditions:

(a) **"value-preserving projection" not "verbatim"** — this directly fixes the integrity-claim overreach. The gate tested value preservation; the words must claim only value preservation. Necessary, and it's offered. Good.

(b) **ndjson designated canonical** — this is what makes the gate's pass *transfer* to the lock. The certified artifact and the locked artifact become the same thing. This is the keystone; without it my substrate objection is a live block, with it it collapses to a wording caveat. Accepted.

(c) **append-only triggers + REVOKE TRUNCATE** — converts immutability from aspiration to enforcement. This was my P0 #3 ("immutability not yet enforced"). Triggers + REVOKE on the table, plus the ndjson being the canonical store, satisfies it. I'd add one rider: REVOKE must cover `DELETE` and `UPDATE` too, and the privilege state must be captured in the lock artifact so a later silent GRANT is detectable. With that rider, accepted.

(d) **ndjson SHA-256 in the lock artifact** — this is what makes the floor *auditable forever* and makes "rebuildable projection" verifiable (you can rebuild and re-hash). Accepted, and I want the rebuild-and-diff drill (above) tied to this hash as the acceptance test.

**Remaining process objection that no caveat satisfies?** No — there is none. My Round 1 framing implied the substrate-agnostic gate was a *procedural* defect (wrong gate for the decision, therefore the decision is unlicensed). Under conditions (a)+(b), the gate and the decision are realigned onto the same artifact, so the procedure is sound. I have no surviving objection that is immune to caveats. The only things left are (1) the wording fix, (2) the multi-snapshot guard, (3) the rebuild-drill verification — all of which are concrete, bounded, and checkable. A genuine forever-process objection would be one where *no artifact change could ever* make the lock safe; I no longer believe I have one. I move.

## Final Position
Score: 6/10 | LOCK-WITH-CAVEATS

I move off DO-NOT-LOCK. The ndjson-canonical reframe (b) is decisive: it makes the integrity gate's pass actually transfer to the locked artifact, dissolving my substrate objection into a wording caveat rather than a procedural block. I remain the most reluctant LOCK vote — 6, not higher — because two of the panel's reassurances are *asserted, not demonstrated* (the rebuildable projection, and multi-snapshot correctness), and the failure timing on the latter is uniquely bad.

Exact caveat list (all are conditions of the lock, not nice-to-haves):

1. **Lock the floor, not the projection.** Decision text must read "lock the ndjson canonical archive; Postgres/Supabase is a rebuildable, value-preserving projection." Do not lock "Supabase as permanent storage" per D9's literal title. (Resolves substrate gate.)
2. **"value-preserving projection," never "verbatim."** Strike any verbatim/byte-identical language. (Condition a.)
3. **ndjson designated canonical, SHA-256 recorded in the lock artifact.** (Conditions b, d.)
4. **Enforced immutability:** append-only trigger; REVOKE TRUNCATE **and DELETE and UPDATE**; capture the resulting privilege state in the lock artifact so later silent GRANTs are auditable. (Condition c + rider.)
5. **Multi-snapshot uniqueness guard — hard deadline: before snapshot 2 is ingested.** Ship a `latest_snapshot` pointer or `current_messages` view (max snapshot_id per `(conv_uuid, msg_uuid)`). Lock artifact must record this as a blocking obligation against multi-snapshot operation. (Resolves new P1.)
6. **Rebuild-and-diff drill, tied to the recorded SHA-256:** before declaring the lock final, regenerate Postgres from the canonical ndjson once and diff against the live table to prove "rebuildable projection" is demonstrated, not merely asserted.
