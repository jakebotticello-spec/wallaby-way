# TWW SideQuest #6 — Sharpening the Edge(s): Problem-Solve Spec

*problem-solve spec (NOT a build spec) · authored 2026-06-20 by the apparatus S72 seat · the substrate re-spec for Pollux's wander graph*
*subordinate to `AstroSynapses.md`, `Leda.md` §1.4, `Pollux_Movement_Two_Build_v2.md` §3.5.2. Where this and canon disagree, canon wins.*
*This frames the problem and the law any solution obeys. It does NOT choose the edge-math — that is the wet open question (§4), settled by reading a pile, never specced cold.*

---

## 0. The one-line problem

The graph Pollux wanders (`corpus_map_S5x/edges.json`) is a **near-graph** — k=8 nearest neighbors per node, cosine ≥0.30. It connects what is **semantically similar**. Pollux is supposed to find the **cross-domain rhyme — low cosine by definition, same shape, different surface** (`Leda.md` §1.4). The substrate and the catch point in opposite directions. The S72 feet walk proved the consequence on disk: a query-blind wander drifted along the similarity-chain (workshop→nearest-workshop, 49 of 50 hops) and never reached the rhyming material. **The edges lead toward near and away from rhyme.**

## 1. The exact problem — stated precisely, because the obvious framing is WRONG

The near-graph is **not simply "the bug."** Canon (`AstroSynapses.md` §2 ★) is explicit: the near edges are **legal to Pollux** because he is query-anchored — adjacency is the librarian's "what's shelved nearby," and Pollux is supposed to supply the taste by picking **salience, not nearness**, off that adjacency. The graph offers adjacency; Pollux supplies the spark. That is the *designed* relationship.

So the real problem is sharper than "near is bad." It is:

> **A pure-near graph gives the wander nowhere to go but nearer.** Every neighbor of a workshop node is another workshop node, so even a *perfect* salience-pick off that adjacency can only choose among near things. The taste has no rhyming option to pick. Salience-not-nearness is the right rule, but it can only operate on the options the edges present — and a k-nearest graph presents only near options. **The spark needs a graph that occasionally offers a rhyming neighbor, or the spark has nothing to catch.**

This is why it can't be fixed at the walk layer (better loudness, the wet bias) alone: those help the wander *not drift greedily*, but if the adjacency itself is all-near, the best possible non-greedy wander still tours a higher-quality near-basin. **The fix is at the substrate: the edge set must contain reachable rhyme, or no walker can find it.**

(Note for the parallel: S72 was *also* query-blind, which removed the subject-pull — that is a separate, already-named fix, the wet agentic walker, S73. Do NOT conflate. Even a perfectly query-holding walker drifts if the only edges are near. This spec is about the *edges*, not the walker.)

## 2. The law any solution obeys (non-negotiable — from canon)

1. **Grain = distinct floor identity.** A node is `(conv_uuid, anchor_msg)`. The current build has **819 phantom duplicates** (8,288 indices → 7,469 distinct — `AstroSynapses.md` §3 open-item-1). Any rebuilt edge set must key on distinct floor identity, or it inflates breadth with phantom adjacency. Dedup at build.
2. **Node coverage stays complete and one-component.** Current: 8,288 nodes, zero orphans, one connected component (no dead seeds, no islands — §3). A rebuild must preserve "every node is landable AND wanderable-from," or it creates seeds Pollux can land on but not leave.
3. **The 26 empty/hollow convs stay excluded** — that is correct exclusion, not a hole (§3). Don't "fix" it.
4. **The graph is adjacency, never a pre-pick.** It offers where-you-could-step; the walker supplies which step. The rebuild changes *what adjacency is offered*, it does NOT add salience-weighting or query-awareness to the edges themselves (that would move the taste into the substrate — the gate, one layer down).
5. **Dual-duty preserved.** AstroSynapses is also the Pyris corpus-sky showpiece (§1.5). A rebuilt graph that serves Pollux must still render as a sky. (Likely fine — both want structure — but don't break the visual.)

## 3. The north star

> A walker on the rebuilt graph, picking by salience off the offered adjacency, can **reach a rhyming node** — same shape, different surface, low cosine — within a leashed wander. Not on every step (the sky must still cohere), but **reachably**, so the spark has something to catch. The current graph makes rhyme *unreachable*; the rebuild makes it *reachable*.

## 4. THE WET OPEN QUESTION — what is a "rhyme edge," mechanically? (do NOT pre-close)

This is the one genuinely-open thing, and it is wet — settle it by **building a few candidate edge-sets and reading the wander's pile (Jake's cold read), never by choosing the math in the abstract.** An edge is a number; "rhyme not nearness" is a feeling; the parallel's real work is finding the number that produces the feeling. Candidate directions to *prototype and read against each other* (not to pick on paper):

- **Mid-band cosine.** Edges deliberately NOT from the nearest neighbors — e.g. a band like 0.15–0.30, or kth-neighbor for k in a middle range — "near enough to share shape, far enough to differ in surface." Crude, testable first.
- **Anti-clustered / cross-strata edges.** Edges that deliberately *bridge domains* — connect a node to similar-shaped nodes in a *different* strata/topic cluster. Rewards the surface-difference directly.
- **Shape-not-surface features.** Edges on a feature space that is structural (the convergence-meter's signal? salience-pattern? emotional/decision arc?) rather than topical-semantic — so "rhyme" = same arc, different topic.
- **Hybrid: keep a near-backbone for sky-coherence + add a rhyme-layer.** The visual stays a sky (near edges hold it together); the wander gains a sparser rhyme-layer it can occasionally cross. Likely the safest dual-duty answer — but read it, don't assume it.

**The test for each candidate:** rebuild the edge set, re-run the S72 feet walk (same query, same entry — `list some of the symbols/creeds jake uses in his life`), and read whether the wander can now *reach* the Lore Bible creed material (Phoenix Heraldry, "properly attenuated," grind/evolve/dominate) that the near-graph walk could not. The S72 walk is the **before**; each candidate is an **after**. The hand-answer (in the S72 findings doc) is the ground-truth of what reachable-rhyme would surface.

## 5. What this spec deliberately does NOT decide

- The edge-math (§4 — wet, read-don't-spec).
- The build internals / which scripts change (parallel owns this — Jake has it).
- The Octobuild/AstroSynapses-v2 visualizer seam (parallel owns this).
- Whether the rebuild runs before or after S73's wet walker — a sequencing fork for Jake (you can isolate the graph variable by rebuilding first, or isolate the bias variable by building the walker first; can't cleanly do both at once).

*The S72 foot walked an all-near graph and could only get nearer. Salience-not-nearness is the right rule, but a rule that picks among options needs options worth picking — and a k-nearest graph offers only near ones. Sharpening the edges means giving the wander a reachable rhyme to catch, without breaking the sky it also has to be. The edge-math is felt, not specced: build a few, walk them against the S72 before, read which one reaches the flowers. — S72, for SideQuest #6.*
