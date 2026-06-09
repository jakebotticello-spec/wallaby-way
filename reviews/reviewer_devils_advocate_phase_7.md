# Devil's Advocate — Phase 7 Blind Final Assessment

Score: 6/10
Recommendation: LOCK-WITH-CAVEATS

## Top 3 Findings (most important to verdict)

1. **The ndjson-canonical reframe is what moved me, and it holds up under blind reconsideration.** My original 3/10 rested on a single load-bearing objection: the substrate-agnostic gate was being used to bless a substrate-specific lock, which is a category error. That objection collapses once ndjson is designated the canonical floor and Supabase is reframed as a *projection* of that floor. The gate correctly tested the integrity of the canonical layer; locking a regenerable projection on top of an immutable canonical source is a genuinely lower-stakes decision. If the projection ever proves wrong, you re-project from ndjson — you have not lost the archive. This is the difference between locking the original and locking a photocopy you can re-take. The reframe is not a rhetorical dodge; it changes the actual risk surface. That is why I am at 6 and not 3. But it is *conditional* on the reframe being made explicit in the decision artifact (caveat 1) — without that, the category error returns and I revert to 3.

2. **Multi-snapshot version mixing is an unresolved correctness hazard, and it is the single thing keeping me from 7-8.** Concrete failure case, restated for the record: after snapshot 2 lands, a naive `SELECT ... FROM messages WHERE conversation_id = X` returns rows from both snapshot 1 and snapshot 2 with no discriminator, producing a silently mixed-version result set. This is not hypothetical — it is the default behavior of any append-only store without a snapshot-versioning column and a query discipline that filters on it. The lock decision as written does not commit to a snapshot selection / versioning policy. My position is unchanged from Round 2: this does **not** block locking the *current* single-snapshot state, but it is a **hard deadline** — it must be resolved *before snapshot 2 is written*, not deferred indefinitely as a "nice to have." A lock that ships without a written policy for this is a lock that has a known data-integrity bug scheduled for its second use.

3. **The decision text still overclaims, and overclaiming on an immutability lock is uniquely dangerous.** "Verbatim," "immortal," and the pgvector title error are not cosmetic. An immutability decision is a document people will trust *precisely because* it claims rigor; sloppy absolute language ("immortal," "verbatim") invites future contributors to assume guarantees the system does not actually provide (e.g., that no transformation ever occurs, that storage is eternal regardless of cost/vendor). The fix is cheap — strike the absolutes, state what is actually guaranteed (SHA-256-verifiable ndjson canonical, regenerable projection) — and the cost of *not* fixing it is a decision artifact that misrepresents its own guarantees. Cheap to fix, corrosive if left.

## Caveat List (ordered, pre-lock vs post-lock)

**PRE-LOCK (must be in the lock artifact before D9 is locked):**
1. Designate ndjson as the canonical floor; Supabase explicitly labeled a regenerable projection. *(Load-bearing — without this the lock reverts to a category error and my score drops to 3.)*
2. Record the SHA-256 of the canonical ndjson in the lock artifact. *(This is what makes "verifiable" true rather than aspirational.)*
3. Drop "verbatim" and "immortal" from the decision text; replace with accurate guarantee language. Correct the pgvector error in the title. *(Cheap; prevents the artifact from misrepresenting its own guarantees.)*

**POST-LOCK (required, with a hard deadline — not open-ended):**
4. Immutability enforcement mechanism (append-only constraint / write-protection on the projection) — specify the actual mechanism, not just the intent.
5. Snapshot selection / versioning policy — **HARD DEADLINE: before snapshot 2 is written.** This is the one post-lock item that is a scheduled correctness bug if skipped, not merely a hygiene item.

## One-line verdict
LOCK-WITH-CAVEATS at 6/10: the ndjson-canonical reframe legitimately converts this from a category-error substrate lock into a low-stakes projection lock, but the lock is only sound if the canonical designation and SHA-256 land pre-lock and the multi-snapshot versioning policy is treated as a hard deadline before snapshot 2 — not as deferrable cleanup.
