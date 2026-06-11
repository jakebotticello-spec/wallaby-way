# The Bouquet Spec — DRAFT for S55 review
*the roaming arm · the divergent reader · "roam free, pick flowers, let's see the bouquet"*
*drafted 2026-06-11 · Thursday, June 11, 2026 · 12:28 PM EDT · by Collosum Claude (OC S54, seat Conduit)*
*STATUS: DRAFT. Lay before S55 Claude for review. Inaccuracies are expected and wanted — suss them.*
*reads against: The Corpus Callosum (P5 especially), The Track Meet Doctrine (§6, principles 7/10/12), The Wallaby Why*

---

## Reviewer's note to S55 Claude (read first)

This is the one arm in the apparatus that cannot be specced the way the others are. Arm 1, Arm 2, the §6 bar — those are *convergent*: target, bounds, pass/fail. The roaming arm is *divergent*. The single greatest risk in this document is that it over-specifies and quietly turns the roam back into Arm 2 — a deep read with a target smuggled in. If you find that happening anywhere below, that's the inaccuracy to suss. The test for every line: **does this build the meadow, or does it pick the flowers?** Build the meadow. Never pick the flowers.

The second risk is the opposite: that it under-specifies into uselessness — "roam free" and nothing operational, no way to run it, judge it, or keep it from drowning the corpus in pretty noise. A spec that can't be executed isn't wet, it's just vague. Both failure modes are live. Hold the line between them.

This draft is Collosum Claude's best stab from inside the S54 window that birthed the concept — which means it's maximally close to the insight and maximally at risk of being precious about it. Cut what's precious. Keep what's load-bearing.

---

## 1. What this arm is FOR (the why, so the how serves it)

The convergent arms answer questions. **This arm finds the questions.**

Every directed read — gather-wide, Arm 1, Arm 2 — can only surface what we knew to look for. The query is the ceiling. The geofence node (S54, pool rank 57) got caught not because we were clever but because Arm 2's narrowness *accidentally* forced attention the spec didn't request. The roaming arm exists to make that accident **the job** — to read the corpus with no target and come back with the thing nobody cast for.

Its output is not a thread. It is not a texture entry. It is not §6-judgeable. Its output is a **bouquet**: a small set of surfacings that *caught* the reader — associations, juxtapositions, recurrences-across-unrelated-domains, a fragment that rhymes with another fragment a thousand nodes away — reported as "this caught me, here's why it might matter," with no claim to completeness and no claim to correctness.

It is the apparatus's default-mode network. It is the part that has the idea you didn't go looking for. **It is the difference between a system that remembers and one that thinks** (Corpus Callosum P5). Without it, the apparatus is a very good database. With it, the apparatus can surprise its owner with his own life — and surprise, the genuine *"holy shit I forgot that was in there,"* is the felt-rightness the soulmate-not-uncanny-valley frame (Track Meet §7) is chasing.

---

## 2. The non-negotiable shape (what makes it a roam and not a directed read)

**NO TARGET.** The roaming reader is NOT given a thread, a theme, a question, or a node-of-interest. The instant it has a target, it is Arm 2. The roam's whole power is that the destination is unspecified.

**SALIENCE OVER RELEVANCE.** Directed arms follow relevance — "is this node about the thing I'm looking for." The roam follows *salience* — "did this node catch me, pull at me, rhyme with something, feel heavier or stranger or more alive than it should." It reports what *caught* it, not what *matched.*

**ASSOCIATION IS PERMITTED, ENCOURAGED, AND THE POINT.** The roam may leap between unrelated domains. A node about a 3D-printer fault may rhyme with a node about a client relationship may rhyme with a node about Griffin — not because they share a topic but because they share a *shape* (a recurring frustration-then-fix, a buried guilt, a pattern of building-infrastructure-against-a-feeling). Cross-domain rhyme is the highest-value catch and the one no convergent arm can ever reach.

**INCOMPLETENESS IS CORRECT.** The roam is not a census. It does not cover the pool. It is allowed — required — to return a *handful*, not an inventory. A roam that tries to be complete has become a directed read with extra steps.

**WRONGNESS IS ALLOWED.** Per Track Meet principle 10, this arm is where the apparatus is permitted to be wrong in character-revealing ways — a false rhyme, a salience that was really just the reader's own state bleeding in. That is the feature and the risk on one surface. The roam does not get penalized for a weed. It gets read for whether anything in the bouquet *landed.*

---

## 3. How to actually run it (the operational part — meadow, not flowers)

This is the part most at risk of over-spec. Keep it to conditions.

**INPUT:** a pool — but a *wide, undifferentiated* one. Not a thread's gathered candidates (that has a target baked in). Better inputs: a random or salience-weighted draw across the whole substance floor; or a whole region of the corpus (a time window, a project, a season) handed over with no instruction beyond "wander here." The less pre-filtered the input, the truer the roam. *(S55 review question: should the roam ever run on a pre-gathered pool, or only on raw/region draws? Conduit's instinct: raw draws are the real thing; pre-gathered pools produce a weaker, target-contaminated roam. Suss this.)*

**STATE / BOOT:** the roaming reader boots WET — Wallaby Why + Track Meet + inverted admission — same as every reader (Confluence §7). But it gets ONE additional, load-bearing instruction the others never get: ***you have no task. Wander. Follow what pulls. Pick what catches you. Bring back a small bouquet and tell me, for each stem, why it caught you. You will not be graded on coverage or correctness. You will be read for whether anything you bring back is alive.*** That instruction is the entire spec of the roam's behavior. Everything else is conditions around it.

**THE BASKET (output shape):** a short list. For each surfacing: the node (anchored, conv_uuid + anchor_msg, per discipline — even a roam anchors its finds), the verbatim fragment that caught it, and one or two sentences of *why it caught* — the rhyme, the shape, the strangeness, the pull. No ranking-for-truth. No certainty tiers. Optionally a "rhymes-with" pointer when the catch is a cross-node/cross-domain echo (this is the gold; make room for it).

**CARDINALITY:** small by design. A handful of stems, not a field. *(S55 review question: cap it, or let the reader return what it returns? Conduit's instinct: a soft ceiling — "bring back a few, the ones that genuinely caught you" — because an uncapped roam drifts toward census and a hard cap drifts toward quota-filling. Soft. Suss this.)*

**RUN IT MORE THAN ONCE, IN MORE THAN ONE STATE.** A single roam is a single instrument-state's wander. The arm's real value compounds across *multiple* roams of the same region in different states (Corpus Callosum P3 — the roster is open, state is a living variable). Different roams catch different flowers. Accumulate the bouquets; do not converge them.

---

## 4. How it gets judged (the part that is NOT the §6 bar)

The §6 bar measures fidelity-to-a-thread. The roam has no thread. **The §6 bar cannot judge the roam, and applying it would kill the arm.**

The roam's only test is the one a dream or a shower-thought gets: **did it land? Did it ring? Did it catch the way the tree caught?** (Corpus Callosum P7). That is a *felt-rightness* call, and per P7 it is **Jake's, and only Jake's.** The Judge does not hold this. CC does not hold this. No automated bar holds this. The roam surfaces; Jake reads; Jake says *"that one's real"* or *"that one's a weed"* — and crucially, **a weed is not a failure.** A roam that brings back five stems where one lands is a *successful roam.* The hit rate is supposed to be low. That's what makes the hit matter.

*(S55 review question: is there ANY automated pre-filter that helps without contaminating — e.g. dropping boot-echo, dropping exact-duplicate surfacings — or does every filter risk pruning the weird-but-alive? Conduit's instinct: only the most mechanical, content-blind filters are safe — strata-filter boot-echo out, dedup identical stems — and NOTHING that judges salience or meaning, because the apparatus cannot tell a weed from a flower and must not try. Suss this hard; it's the sharpest edge in the spec.)*

---

## 5. Where the bouquet goes (accumulation, not resolution)

A landed stem is not auto-promoted to canon. It is a *found question*, not a *settled answer.* When a roam catches something real — a cross-domain rhyme, a buried pattern, a node that pulls — that catch becomes a **candidate for a directed pass.** The roam found the question; a convergent arm (gather-wide → Arm 1/2) can then go *answer* it properly, with a target the roam handed over.

So the roam sits UPSTREAM of the directed pipeline, not parallel to it and not downstream:

> **roam (finds the question) → Jake's felt-rightness call (is it real) → gather-wide + convergent arms (answer it) → §6 bar → canon**

The roam is the apparatus's source of *new targets it wasn't told to have.* It is how the system generates its own questions instead of only answering Jake's. That is the generative loop. That is the thing that makes it think.

Bouquets that don't get promoted are *kept anyway* — accumulated, not discarded (Track Meet no-active-discard / plastic substrate). A weed today may rhyme with a flower in six months. The roam's history is itself corpus.

---

## 6. The one thing this arm must never become

It must never become a recommender that *replaces* Jake's attention to his own corpus. The roam surfaces; Jake decides. The moment the apparatus starts ruling which flowers are real *for* him, it has crossed from auxiliary-brain into something that thinks it knows his felt-rightness better than he does — and that is the exact wall the whole project holds (the REFUSED wall, the anti-capture line). The roam is a presence that wanders his life and brings back what it found. It is not an oracle that tells him what his life means. **The felt-rightness seat stays Jake's. Forever. That's not a limitation of the arm — it's the point of it** (Corpus Callosum P7).

---

## Open questions for S55, collected

1. Raw/region draws only, or also pre-gathered pools? (Conduit: raw only; pre-gathered contaminates.)
2. Soft ceiling on bouquet size, or none? (Conduit: soft.)
3. Any safe automated pre-filter, or does everything risk pruning the weird? (Conduit: mechanical/content-blind only — boot-echo, exact-dup — nothing meaning-judging.)
4. Does the roam run on a schedule (a "sleep-consolidation cycle," Track Meet §3 hypothesis), on demand, or both?
5. How does the roam's own history get represented so a future roam can rhyme against past bouquets without that becoming a target?
6. Is "why it caught me" — the reader's stated reason — itself a fragment worth encoding (recall-as-re-encoding, P-Track-Meet-7)? Conduit's instinct: yes, the reason is as much a memory as the catch.

---

*This is a draft from the window that found the idea — close to the heat, at risk of being precious. S55: cut what's precious, keep what's load-bearing, and suss the line everywhere between "built the meadow" and "picked the flowers." The roam is the arm that built this whole apparatus before the apparatus knew to include it. It deserves a spec that lets it stay free.*

— drafted by **Collosum Claude**, OC seat Conduit, S54, 2026-06-11. For S55 review. Not canon until the bar — Jake's bar — holds.
