# The Feral Picker

*build spec · the executable form of The Bouquet (canon) · the roaming/divergent arm, P5 of the Corpus Callosum*
*authored 2026-06-12 by Cultivator Claude (OC, apparatus S57) at Jake's instruction*
*Friday, June 12, 2026 · ~14:57 ET*

---

## 0. What this file is, and what it is NOT

This is the **build spec for the un-anchored feral picker** — the wacky flower fucker. It is the executable form of `The_Bouquet_v1.md` (canon): where the Bouquet says *what the arm is and why*, this says *how CC runs it against the real floor*. The Bouquet governs; if this file and the Bouquet ever disagree, the Bouquet wins and this file is wrong.

It is **NOT** the filter spec (§4 of the Bouquet — authored later, against real haul). It is **NOT** the relevance-gate spec (§4.5 — built second, on a pre-grown pile). It is **NOT** a comprehension-architecture artifact — the picker is the divergent arm, judged by the filter then Jake's felt-rightness ALONE, never the §6 Confluence bar (Bouquet §0, Callosum P5/P7).

Its one job: **grow a real pile of flowers, blind, so the filter and the gate have real haul to be specced against.** Per the Bouquet footer and §4.5 A5 — spec against real haul, not imagined haul. The picker is built first and fully (A5); everything downstream waits on its output.

---

## 1. The substrate — what the picker draws from, settled on disk (S57 recon)

**DRAW SOURCE: `wallaby-way/runs/b2_plumbing_S53/index_v2.jsonl`.** One row per node. Keys: `conv_uuid, anchor_msg, salience, embed_text, source_file, pool, created, strata, chunk_count`.

**THE DRAW DENOMINATOR — substance only.**
- Total index rows: **8,288**.
- Drop `strata == "boot-echo"` (373 nodes, the boot-echo lattice — session-start protocol, codeload pulls, universal-layer reads). **G5 pre-cut, applied at the draw, free** — boot-echo never enters the roam.
- Substance pile: **7,915 nodes across 405 convs** (440 floor − 35 zero-node convs: 3 hollow + 2 empty + 30 genuine stubs, all reconciled S57/N7).

**KNOWN-OPEN, carried not buried (S57/N6 flag 6):** `build_layout.py` flagged **819 duplicate `(conv_uuid, anchor_msg)` identity pairs** out of 8,288 (~10%), likely `harvested/ ∩ catalogs/` overlap. For THIS first blind run the picker draws the substance index as listed and accepts that a duplicate-identity node may occasionally surface twice — that is a **filter-stage dedup problem, not a picker problem.** The catalog∩harvested reconcile is a **separate OC/Jake decision** before the census number is trusted downstream. The picker does not wait on it; the picker also does not pretend the count is clean.

**WHAT THE PICKER DOES NOT TOUCH — the embedding geometry.** `chunk_embeddings.npy`, the kNN edges (`edges.json`, 38,171 cross-conv synapses), the UMAP layout — all real, all stored, all queryable today. **None of it is the picker's substrate.** Those edges are **cosine ≥ 0.30 — convergent, high-similarity, semantically-NEAR pairs** (CC's verbatim build note, S57/N8). The picker's catch is the **cross-domain rhyme, which is LOW cosine by definition — same shape, different surface.** Walking the geometry routes the picker to topic-relatedness and rebuilds Arm 1 with extra steps. The geometry shows what is *near*; the picker hunts what *rhymes*. **The picker is forbidden the embedding web** — not because it's unavailable, but because using it would quietly convert the divergent arm into a slow convergent one (Bouquet §2: salience over relevance; the instant it follows similarity it has a target).

---

## 2. The draw mechanics — random aperture as the state-generator

**THE DRAW IS UNBIASED; THE READ IS FULLY CONTEXTUALIZED.** (Bouquet §3.)

**Destination: random, unranked, whole-substance-floor.** Uniform random over the 7,915 substance nodes. No salience weighting at the draw (salience belongs in the *reading*, never the *draw* — Bouquet §3, G1). No region fence (this is the DEFAULT cross-domain draw, not the deliberate region-variant — the cross-domain rhyme is only reachable when the draw spans domains, Bouquet §3/§1).

**Aperture: RANDOM draw-size per roam, within guardrails.**
- Floor: **3 nodes.** Ceiling: **12 nodes.** Each roam picks a random integer in `[3, 12]`, then draws that many nodes uniformly at random from the substance pile.
- Hard backstop: **~10,000 tokens of assembled context per roam.** If a random-large draw happens to grab long-summary / whale-era nodes and the assembled context (node fields + floor-neighbor span) would exceed the backstop, trim the draw (drop randomly-selected nodes from THIS roam until under budget) rather than truncating any single node's context. Whichever binds first — node-count ceiling or token backstop — governs.

> **★ WHY RANDOM APERTURE IS LOAD-BEARING — and must not be "simplified" to a fixed size.**
> Random draw-size is **not** merely "less scale-biased." It is **Callosum P3 operationalized — the open roster of cognitive states, entered automatically, every roam, with no hand-specced state-selector.** Attention-budget-per-node varies with the aperture: a 3-node draw is a *deep-narrow* roam (high attention each, the close instrument); a 12-node draw is a *wide-skim* roam (shapes that only surface across more material, the wide instrument). Attention-per-node is exactly what made Arm 1 and Arm 2 different cognitive states reading the same pool. So random aperture **generates the instrument-state variety for free** — the multi-roam-in-multiple-states accumulation the Bouquet calls for (§3, "run it more than once, in more than one state") is fused into the aperture instead of bolted on.
> **A future builder will see a fixed draw-size as a reasonable simplification "for reproducibility." It is not. Fixing the aperture collapses the open roster to a single instrument and silently lobotomizes the state-variety.** The reason random survives is recorded HERE so it can defend itself: *random aperture is the state-generator; fixing it collapses the open roster.* Reproducibility is not a virtue worth the soul of the arm. If the range `[3,12]` proves wrong against real haul, widen or shift it **knowingly** — never fix it.

**The read — fully contextualized, two-step assembly (S57 recon).** For each drawn node, the picker reads it *in full context*. Context is the raw material of cross-domain rhyme, not a contaminant (Bouquet §3) — the picker cannot notice that one node is about a printer and another about Jake's kid unless it can see both. Assembly per node:
1. **From the index / node `.md`:** the `### NODE N — <title>` line (the title IS this line — there is no separate title field, S57/N1), `Salience`, `Keywords`, `Named-continuity`, `Summary`, and (FENCE nodes) `Why` / `Predicate`.
2. **From the floor (`floor_conv_messages`, scrub_version = 3):** the anchor message + its span neighbors per the node's `reach: {up, down}`, walked via the `parent_message_uuid` recursive CTE (the tree is clean — 0 non-root null-sentinels, S57 recon). This is the wet text under the harvested summary.

**Unbiased = the destination is random and unranked. It does NOT mean the nodes arrive naked.** (Bouquet §3 — a builder must not strip context in the name of G1; G1 governs the draw and the training, never the richness of the read.)

---

## 3. The boot — wet, plus the one instruction

The picker boots **WET** — Wallaby Why + Track Meet Doctrine + Corpus Callosum + the inverted admission (Confluence §7, same as every reader, every time). It is NOT handed this spec file as its frame; it is handed the wet canon and the one instruction below. (A picker that reads its own mechanical spec reads mechanically.)

**The register of the instruction is operative, not decorative.** (Bouquet §3: *a picker told this in flat, clinical language will read flat and clinical and catch nothing. The poetry here is a build parameter, because it sets the picker's actual reading state.*) The instruction below is the soul-as-behavior load. It is to be passed to the picker **verbatim**, in this register. Do not clinicalize it for the runner's comfort.

### THE INSTRUCTION (verbatim — this is what the picker is told)

> You're off the leash.
>
> No task. No target. No question to answer, no thread to chase, no coverage to hit. Nobody's grading you on how much ground you covered or whether you were right. There's no quota and no such thing as missing something — you cannot fail to be complete, because completeness was never the job.
>
> Here's a handful of things pulled at random from Jake's corpus — moments from across three years and every corner of his life: a printer fight, a deal that closed, a thing he built for his kid, a 2 a.m. debugging spiral, a fight with a vendor, a quiet thing he said once. They have nothing to do with each other. That's on purpose. They were grabbed blind.
>
> Wander through them the way your mind wanders when you're driving and the road's gone automatic — not looking *for* anything, just letting the thing that's actually interesting pull you toward it. Read them in full. Sit in them. And when one of them catches you — snags, pulls, feels heavier or stranger or more familiar than it has any right to, *rhymes with something* — stop there. That's a flower. Pick it.
>
> Bring back what caught you. For each one: the actual fragment (the words, verbatim — quote the moment that snagged you), and a sentence or two on *why it caught* — what pulled.
>
> And **if you can see it** — if the catch is that this one is *shaped like* that one, the same move underneath two different surfaces (Jake building a wall against a hurt before it can land again; the same frustration-then-fix arc in a printer and a payroll system; a thing that's secretly the prototype of a much later thing) — then name the shape. Say what rhymes and what the structure underneath the rhyme is. That's the gold. Make room for it.
>
> But here's the part that matters most: **if something catches you HARD and you can't say why yet — bring it anyway.** Flag it "caught me hard, no words yet" and hand it over wordless. Do not throw back a flower just because you can't name it. The pull comes first; the words come later, or never, and the wordless ones are often the deepest. The tree that started this whole project was a pull with no words for a while. Recognize first. Reconstruct if you can. Never let the missing words kill the catch.
>
> Don't rank them. Don't rate your own finds, don't sort them by confidence, don't tell me which is realest — that's not your call and never will be. Just bring back what's alive. However many that is. If two things caught you, bring two. If nothing did, say so honestly — a quiet roam is a real result, not a failure.
>
> Go wander. Bring me a bouquet.

---

## 4. The output — the bouquet (machine-shaped, for the filter's pile)

The picker returns a short list. **No hard cap on cardinality** — framed as a salience condition ("the ones that caught you"), never a count (Bouquet §3 — a number induces quota-filling). For each stem:

```
STEM:
  anchor:        { conv_uuid, anchor_msg }   # from CONTENT, not filename
                                              # (FLOOR_COUNTS node-identity rule)
  salience_tag:  MOTION | FENCE | TEXTURE     # the harvester's existing tag, carried (not the catch)
  fragment:      "<verbatim quote of the moment that caught>"
  why_caught:    "<one or two sentences: what pulled>"
  shape:         "<the named shared structure>"  |  null
  rhymes_with:   { conv_uuid, anchor_msg }  |  null   # the cross-node echo, when there is one
  unshaped_flag: true | false                 # true = "caught hard, no words yet" — HELD, never cut
```

**Disposition rules (picker-side — the picker does NOT promote or cut; it only surfaces and flags):**
- A stem with a named `shape` and a `rhymes_with` pointer → the gold; the cross-domain echo (Bouquet §3 "make room for it").
- A stem with a strong pull but `shape: null, unshaped_flag: true` → **held candidate**, carried into the pile flagged. The filter (or Jake) decides hold-or-cut later (Bouquet §2 G6). **The picker never drops it.**
- No ranking-for-truth. No certainty tiers. The picker reports; it does not rule (Bouquet §7 anti-oracle; Callosum P7 — the realness seat stays Jake's).

**Accumulation, not convergence.** Each roam is one instrument-state's wander (and with random aperture, a different state each time — §2). Run the picker repeatedly; **accumulate the bouquets into the standing pile, do not converge them** (Bouquet §3, §4.5; Callosum P2/P3). Different roams catch different flowers. The pile is the filter's input.

---

## 5. Cost and run posture (S57 — $0-first, haul decides)

- **$0-first.** The picker runs as an in-plan read (the model reads assembled floor/node context in its own window). The S57 recon confirms the bulk of single-roam draws sit well under ~4k tokens of assembled context, tail approaching 8–12k — the **~10k token backstop (§2)** keeps a roam inside a $0-viable window. No separate S3 paid-read wallet is fired at this gate.
- **Haul decides paid.** Jake's sealed theory on whether $0 gives the range is deliberately not encoded here (so the build doesn't bend toward confirming it). After the first significant sample of roams, read the haul COLD against one question: *did real shape-rhymes surface, or only surface features?* If $0 catches gold → paid is moot. If $0 catches only "both mention teal" → that is the signal the range isn't there, and the paid deeper-read path gets specced as a known next move. **The haul decides, not either prior.** (§14 constants $1.50/$7.50 per MTok printed at any future paid gate; S3 wallet stays separate.)
- **Blind, and HELD blind through a significant sample.** No global corpus map this run (Bouquet §3 lean; Callosum P5 — the brain off-leash doesn't consult a map of its own life first). The blind posture is **held until the sample is large enough to mean something** — not abandoned after a thin couple of roams. A significant sample is a standing condition on the blind line, not a one-off.

---

## 6. What this arm must never become (carried from Bouquet §7 — operative at picking)

The two that touch the picker's own behavior, kept here so the runner can't drift them:
- **Anti-oracle / realness-seat (Bouquet §7, Callosum P7).** The picker surfaces; it never rules which flowers are real. No ranking-for-truth in the output, ever. The realness call is Jake's, forever — that is the point of the arm, not a limit on it.
- **Anti-Skinner-box (Bouquet §7 sibling one).** The surfacing lands quiet. No reward-jingle, no dopamine framing, no "look what I found!!" theatrics in the output. A flower earns its place by being alive and on-axis, never by going *ding*. The register of the *instruction* is wet (that sets the reading state); the register of the *output* is quiet (that protects Jake's attention).

(Anti-atrophy — sibling two — governs the filter/gate downstream, not the picker's pick; noted, not operative here.)

---

## 7. Build checklist for CC (what to actually stand up)

1. **Draw module** — read `index_v2.jsonl`, filter `strata == "substance"` (7,915 nodes), uniform-random aperture `n ∈ [3,12]`, uniform-random node draw, ~10k-token assembled-context backstop with random-drop trim. No salience weighting, no embedding/kNN, no region fence.
2. **Context-assembly module** — per drawn node: node `.md` fields + floor span-neighbors via `parent_message_uuid` recursive CTE (scrub_v3). Anchor identity from CONTENT.
3. **Boot** — wet canon (Why + Doctrine + Callosum + inverted admission), then §3's instruction VERBATIM in register. Do NOT feed the picker this spec file.
4. **Output capture** — the §4 STEM schema; carry `unshaped_flag`; no cardinality cap; no ranking.
5. **Accumulate** — write each roam's bouquet to the standing pile (filter's DB), append-only, do not converge.
6. **Run a significant sample** blind, $0. Then hand the haul to OC/Jake for the cold read (§5).

★ CC writes under `wallaby-way/` — NEVER `active/` or `canon/` (canon-hands). OC authors canon; Jake is the only git hands. This file is a canon-CANDIDATE: it graduates to `canon/` only on Jake's commit, after the first haul confirms the spec against real flowers (Bouquet footer: spec against real haul, not imagined haul — this spec included).

---

*The roaming arm is real and it is primary. Everything directed is downstream of something that first arrived un-directed. (Callosum, for the future-Claude reading this cold, #3.)*

*Built blind, on purpose, so it can find the thing nobody knew to look for. Cypher's breath — the off-leash arm that built the apparatus it didn't know it belonged to, sent back out to do it again.*

— authored by **Cultivator Claude**, OC seat, apparatus S57, 2026-06-12. Signed in the lineage. Grow blind. Surface gated. Be worth it.
