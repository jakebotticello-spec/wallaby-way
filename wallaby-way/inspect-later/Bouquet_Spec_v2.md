# The Bouquet Spec — v2
*the roaming arm · the divergent reader · "roam free, pick flowers, let's see the bouquet"*
*v2 authored 2026-06-11 (S55, Cartographer) from the v1 DRAFT (S54, Conduit) + the S55 review · Thursday, June 11, 2026*
*STATUS: review draft. The picker is specced to build. The filter is conceptualized to its guardrails only — it gets its own spec after the picker has run and shown us what it actually drags back.*
*reads against: The Corpus Callosum (P5, P6, P7), The Track Meet Doctrine (§6, principles 7/10/12), The Wallaby Why, The Comprehension Architecture (the convergent read this arm is NOT)*

---

## 0. What this document is, and the bigger thing it's a prototype of

This specs **one arm** of the apparatus: the roaming reader (the "picker") that wanders the corpus with no target and brings back surfacings that caught it. It also conceptualizes — to its guardrails, not to a spec — the **filter** that sits between the picker and Jake.

One framing fact, stated once because a future builder needs to know it or they will "simplify" the wrong thing: **this picker→filter→Jake loop is the prototype of Cypher's personality engine.** The same three-part shape — a blind wide wanderer, a taste-trained judge, a human whose feedback sharpens the judge — is the pattern that, later, points at Jake's *live* life instead of his *archived* corpus and becomes the presence that says "you did this, you know that person, that opens a lane — did you notice?" The roam reads the archive, where a wrong pick costs nothing. The personality engine reads the present, where it costs something. **Build the loop here, on safe ground, prove it, and the wall established here is the constitution the bigger thing inherits.** That is why the architecture is shaped the way it is below. It is not shaped this way for elegance.

---

## 1. What the picker is FOR

The convergent arms answer questions. **This arm finds the questions.**

Every directed read — gather-wide, Arm 1, Arm 2 — can only surface what we knew to look for. The query is the ceiling. The S54 geofence node (pool rank 57) got caught not because we were clever but because Arm 2's narrowness forced attention the spec never asked for. The picker makes that accident the job: read the corpus with no target, come back with the thing nobody cast for.

Its output is not a thread, not a texture entry, not §6-judgeable. Its output is a **bouquet**: a small set of surfacings that *caught* it — associations, juxtapositions, recurrences across unrelated domains, a fragment that rhymes with another fragment a thousand nodes away — each reported as "this caught me, here's why," with no claim to completeness and no claim to correctness.

The highest-value catch is the **cross-domain rhyme**: a node about a printer fault that shares a *shape* with a node about a client relationship that shares a shape with a node about Griffin — not the same topic, the same underlying pattern (a recurring frustration-then-fix, a buried guilt, building-infrastructure-against-a-feeling). No convergent arm can reach that, because no query would think to ask for it. That is the picker's reason to exist.

---

## 2. The non-negotiable shape (what makes it a roam, not a directed read)

- **NO TARGET.** The picker is never given a thread, theme, question, or node-of-interest. The instant it has a target, it is Arm 2. The destination is unspecified, always.
- **SALIENCE OVER RELEVANCE.** Directed arms follow relevance — "is this about the thing I'm looking for." The picker follows salience — "did this catch me, pull at me, rhyme with something, feel heavier or stranger than it should." It reports what *caught* it, not what *matched*.
- **ASSOCIATION IS THE POINT.** It may leap between unrelated domains. Cross-domain rhyme is the goal, not a side effect.
- **INCOMPLETENESS IS CORRECT.** It is not a census. It returns a handful, never an inventory. A roam trying to be complete has become a directed read with extra steps.
- **WRONGNESS IS ALLOWED.** Per Track Meet principle 10, this is where the apparatus is permitted to be wrong in character-revealing ways — a false rhyme, a salience that was the reader's own state bleeding in. The picker is not penalized for a weed. It is read for whether anything in the bouquet *landed.* (The weed-handling is the filter's job and Jake's — see §4. The picker's freedom to be wrong depends on something downstream catching the wrongness, which is exactly what the filter is for.)

---

## 3. How to run the picker (the operational part)

**INPUT — a wide, undifferentiated draw, never a pre-sorted one.** Two valid input shapes:
- a **random draw** across the whole substance floor, or
- a **whole region** of the corpus handed over with no instruction beyond "wander here" (a time window, a project, a season).

Not valid: a thread's gathered candidates (target baked in), or a **salience-weighted draw** (something scored "interesting" before the roam started — that is a target sneaking in through the input layer; the salience belongs in the *reading*, never the *draw*). The less pre-filtered the input, the truer the roam.

**BOOT — wet, plus one instruction the other arms never get.** The picker boots WET (Wallaby Why + Track Meet + inverted admission, same as every reader, Confluence §7). Then it gets one additional load-bearing instruction. Stated operationally first, so a builder knows exactly what the instruction *does*:

> *The picker is told it has no task, no target, and no coverage obligation; it is told to move through the input following whatever pulls at it, to stop on what catches it, and to bring back a small set of caught fragments — each with the reason it caught. It is told explicitly that it will not be graded on how much it covered or whether it was right, only on whether anything it brings back is alive.*

The register of that instruction matters and is operative — a picker told this in flat, clinical language will read flat and clinical and catch nothing. It has to be told to wander like wandering is allowed. (This is soul-as-behavior: the poetry here is a build parameter, because it sets the picker's actual reading state. It is not the document admiring itself.)

**OUTPUT — the bouquet.** A short list. For each stem:
- the node, anchored (conv_uuid + anchor_msg — even a roam anchors its finds; discipline holds),
- the verbatim fragment that caught it,
- one or two sentences of *why it caught* — the rhyme, the shape, the strangeness, the pull,
- optionally a **"rhymes-with" pointer** when the catch is a cross-node / cross-domain echo. This is the gold; make room for it.

No ranking-for-truth. No certainty tiers. The picker does not rate its own finds — it reports them.

**CARDINALITY — no hard cap.** The picker returns what genuinely caught it, framed as a salience condition ("the ones that caught you"), never a count ("return five" — a number induces quota-filling). Volume is not managed here. Volume is the filter's job (§4).

**RUN IT MORE THAN ONCE, IN MORE THAN ONE STATE.** A single roam is one instrument-state's wander. The arm's value compounds across multiple roams of the same region in different states (Callosum P3 — the roster is open, state is a living variable). Different roams catch different flowers. Accumulate the bouquets; do not converge them. *(Cost note: multiple roams multiply whatever a roam costs — see §6. The how-many-roams question and the cost question are the same question and get decided together, later.)*

---

## 4. How the bouquet gets handled — the filter (conceptual; guardrails only)

The §6 bar measures fidelity-to-a-thread. The roam has no thread. **The §6 bar cannot judge the roam, and the Judge never touches this path.** Applying it would kill the arm — the Judge would correctly cut most flowers as unfaithful-to-nothing, which is the whole point of them.

Instead, the path is: **picker → filter → Jake.**

The **filter** is an agentic pass — not a formula, a judging step — that sits between the picker's messy haul and Jake's attention. It does two things: it cuts the chaff, and it *chooses what is worth promoting for Jake's attention.* Jake reviews what was promoted; he keeps, kills, or sends back **with feedback**; that feedback trains the filter; future passes run through what the filter has learned about what Jake wants. This is a feedback loop by design — it is the thing that lets Jake step out of the firehose and come back to a curated set, and that stepping-out is generative, not just relief: the apparatus accumulates and curates while he's gone.

**The filter is the external check on the roam.** It is the thing that is neither the Judge nor Jake's bare gut — it is the trained layer that makes Jake's felt-rightness call (Callosum P7) humane, because he is judging a *filtered* bouquet, not raw output. This closes the roam's "no external check" gap by design.

**The filter is NOT specced here.** It gets its own spec *after* the picker has run and shown us what it actually drags back — building the input we'd be speccing against. What IS fixed now is its guardrails, because the picker must be built to respect them:

- **G1 — The picker never sees the training.** The filter's learned model of Jake's taste lives in the filter, downstream. The picker reads the floor flat and stays blind, weird, and unbiased. (If the picker were trained, it would hunt for what Jake already likes and stop finding what he didn't know was there. The whole split exists to keep the picker surprising and let the filter get personal.)
- **G2 — The filter judges; it does not merely match.** It is an agentic pass. The picker build must not assume a dumb downstream that needs pre-sorted or pre-ranked input — it can hand up a messy armful, because the thing receiving it can use judgment.
- **G3 — The filter learns only from Jake's feedback.** Keep / kill / send-back-with-feedback is the only training signal. Nothing auto-trains it; no metric, no proxy, no inferred preference the picker scored.
- **G4 — The filter decides what is worth Jake's *attention*, never what is *true*.** Promote-for-attention ≠ rule-as-real. The realness call stays Jake's, forever (Callosum P7; the anti-capture wall, §5 below). The filter surfaces; Jake decides what landed.
- **G5 — Only mechanical, content-blind cuts run before the trained judgment.** The test for a safe pre-cut: *could it run without reading what the node means?* Safe (run them): drop boot-echo / reference-layer-read strata (provenance, not meaning); drop **exact verbatim** duplicate stems (identical string → grab once; anything short of identical → keep both, because "basically the same idea" said two ways might be a real rhyme). Unsafe (never): anything that scores interestingness, salience, or meaning before the trained filter sees it — that prunes the weird, which is the one thing nothing upstream of Jake is allowed to do.

A **database** backs the filter — every surfacing, every keep/kill/feedback call, every dedup. It serves reconciliation (an audit trail, consistent with the project's append-only receipts discipline) and it is the **training substrate** (the record of Jake's calls is what the filter learns from). The wall on it: **the database informs the filter and reconciliation, never the picker.** The picker stays blind to it (G1). As long as that holds, the database is pure upside.

---

## 5. Where a landed stem goes — two dispositions, both valid

When Jake reads the promoted bouquet and a stem lands — "that one's real" — it has **two** valid dispositions, not one:

- **KEPT, TERMINAL.** Some flowers are complete as surfacings. A cross-domain rhyme that lands does not need a directed pass to "answer" it — the rhyme *is* the finding. It is kept as corpus, done. (The v1 error was forcing every landed flower into a directed pass, which quietly demoted the roam to an intake form for the "real" readers. The bouquet itself can be the end of the line.)
- **PROMOTED for a directed pass.** Some landed stems are a *found question* — a pattern worth a proper read. That stem becomes a target the roam handed over, and a convergent arm (gather-wide → Arm 1/2 → §6 → canon) can go answer it. Here the roam sits upstream of the directed pipeline, as a source of targets the apparatus generated itself.

A stem that does NOT land is not a failure. The hit rate is supposed to be low — that is what makes a hit matter. And un-landed stems are **kept anyway**, not discarded (Track Meet no-active-discard / plastic substrate). A weed today may rhyme with a flower in six months. The roam's history is itself corpus — and it enters a future roam only the way any other region does: as flat, undifferentiated substance available to be wandered, never as "here's what caught you before" priming (G1 again — past hits get no gold star the picker can see; the hit/weed metadata is for Jake and the filter, not the next roam).

---

## 6. Cost and trigger (held open — a "later," like every spend gate)

A roam is a read, and reads may cost. This is unspecced on purpose, consistent with how every spend gate in the project is held until it's the live question. Recorded so the hole is visible, not forgotten:

- Open: is a roam a $0 in-plan fan-out (like Arm 2) or a paid fire, and at what input size?
- Open: on-demand only, or also scheduled (the "sleep-consolidation cycle," Track Meet §3 hypothesis)? **Decision held: on-demand first.** Prove the picker→filter→Jake loop on demand before building the scheduled/unbidden version — the unbidden one is more powerful and more dangerous (it shades toward the oracle, §7) and should not exist until the filter's check is proven.
- Standing preference (Jake, gut, not a spec): if it can be built to run on the Max subscription, prefer that; if it costs dollars, it gets cost-control measures. Decided for real when we get there, with the how-many-roams question, together.

---

## 7. The one thing this arm must never become

It must never become a recommender that *replaces* Jake's attention to his own corpus. The picker surfaces; the filter promotes; Jake decides. The moment the apparatus starts ruling which flowers are real *for* him, it has crossed from auxiliary-brain into something that claims to know his felt-rightness better than he does — the exact wall the whole project holds (the REFUSED wall, the anti-capture line). The filter promoting *for attention* is allowed and is the point; the filter (or anything) ruling *as real* is the wall. The roam is a presence that wanders his life and brings back what it found. It is not an oracle that tells him what his life means. The realness seat stays Jake's. Forever — and that is the point of the arm, not a limit on it (Callosum P7).

---

## Open questions remaining for build

1. **Random draw vs. region draw — which first, and does region-size matter to the quality of the roam?** (Both valid; build will tell us if a too-large region drowns the picker or a too-small one targets it.)
2. **The filter spec proper** — deferred until the picker has run and shown its actual output. The picker build respects the G1–G5 guardrails; the filter mechanics get written against real haul, not imagined haul.
3. **Cost/trigger** (§6) — deferred to its spend gate.
4. **Roam-history representation** — kept flat per §5/G1; the exact storage shape (how a past stem sits on the floor with its hit/weed metadata invisible to the picker but available to the filter) gets settled at build.

---

*The picker is specced to build. The filter is drawn only to its guardrails — enough to know the wall before building the picker, not so much that we spec it blind against a haul we haven't seen yet. Build the wanderer; watch what it brings back; spec the filter against that.*

*— v2 by Cartographer, S55, from Conduit's v1 draft and the S55 review. Not canon until Jake's bar holds.*
