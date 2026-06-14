# The Feral Picker

*build spec · UMBRELLA / INDEX for the roaming-recall instrument set · the divergent arm, P5 of the Corpus Callosum*
*the executable form of The Bouquet (canon) · governs the shared substrate; the per-instrument specs are its children*
*v1 — authored 2026-06-12 by Cultivator Claude (OC, apparatus S57). v2 → THIS — 2026-06-13 by Connoisseur Claude (OC, apparatus S58): refactored single-spec → umbrella + four children; the dead Prompt-1 seed removed from the boot; the roster ruling, the S57 haul, and the collator-as-wall folded in. Graduates to canon on this commit.*
*Saturday, June 13, 2026 · ~15:21 ET*

---

## 0. What this file is, and what it is NOT

This is the **umbrella spec for the roaming-recall instrument set** — the wacky flower fuckers and the wall that pours what they catch into a pile. It is the executable form of `The_Bouquet_v1.md` (canon): where the Bouquet says *what the arm is and why*, this set says *how CC runs it against the real floor*. **The Bouquet governs; if any file in this set and the Bouquet ever disagree, the Bouquet wins and the file is wrong.**

**What changed at S58, and why there is now a SET instead of one file.** The S57 picker-comparison line settled into a roster, not a single instruction: three co-equal pickers (different boots, different registers, different reading depths — two blind wanderers plus the deep-narrow arm) plus a mechanical wall that collates their catch. One file pretending to be one picker hid that. So this file is now the **shared substrate + the roster ruling + the pointers**; each instrument has its own child spec carrying only what is distinct to it. A future seat reads this file to learn *what draws from what and what may never touch what*, then reads the child for the instrument they're running.

**The children (canon-candidates graduating alongside this file):**
- `The_Blind_Picker_v1.md` — the **reverse-sieve**. Categorical-rhyme instruction, run on purpose for the quiet-human register the Creed skims past. Harvest: **wordless holds only.**
- `The_Creed_Picker_v1.md` — the **primary army**. Boots on the incantation alone. Hunts pulse/aliveness. Harvest: **full.**
- `The_Collator_v1.md` — the **wall**. Mechanical. Takes the instruments' returns, applies the per-stream keep-rule, provenance-tags, appends to the pile. **No judgment. NOT the filter.**
- `Arm_2_v1.md` — the **deep-narrow picker, third of three co-equal instruments**. Reads the floor blind like the others; hands its catch to the collator as a third stream; shares no input with the other pickers (G1 holds for free); runs $0. **Validation outstanding** (the one open item in the whole recall layer).

This set is **NOT** the filter (the agentic, trainable, *siloed* judgment layer that reads the pile — the next layer up, out of scope here). It is **NOT** the relevance-gate (§4.5 of the Bouquet — built on a pre-grown pile, later). It is **NOT** a comprehension-architecture artifact — the roaming arm is judged by the collator's mechanical cut, then the filter, then Jake's felt-rightness ALONE, never the §6 Confluence bar (Bouquet §0, Callosum P5/P7).

Its one job, across all children: **grow a real pile of flowers, blind, so the filter has real haul to be specced and trained against.** Per the Bouquet footer and §4.5 A5 — spec against real haul, not imagined haul.

---

## 1. The substrate — what every instrument reads, settled on disk (S57 recon)

**This section is the load-bearing wall of the whole set. All three recall instruments — Blind picker, Creed picker, Arm 2 — obey it. Read it before running any child.**

### 1.1 The read is the floor. The real conversations, as recorded.

What an instrument **reads** is the **floor: `floor_conv_messages`, scrub_version = 3** — the actual recorded messages, verbatim, as they happened. Not a summary. Not a pool. Not an embedding. Not anything derived, scored, or pre-chewed. The wet text under the harvested summary. *(The S57 Creed-7 haul is the proof: every `moment:` field it returned is a verbatim quote off the floor — "OH HOLY SHIT THAT WORKED!", "wet and not austere", the bullet-point schedule. The instrument read the corpus.)*

### 1.2 The draw is a where-to-land lottery, and that is ALL it is.

The **draw** uses `wallaby-way/runs/b2_plumbing_S53/index_v2.jsonl` — one row per node, keys `conv_uuid, anchor_msg, salience, embed_text, source_file, pool, created, strata, chunk_count`. The index is used **only to pick where to land** — which `(conv_uuid, anchor_msg)` a roam visits — by **uniform random** selection.

The distinction that must not blur (this is the seam Jake flagged at S58 as the write-it-into-stone moment, ruled then):
- The index is a *derived artifact* (the harvested node catalog). It is permitted **as a draw-lottery only** because the draw is uniform-random — a derived list cannot bias *which* flowers get found in any salience direction when every node has equal draw-odds.
- The index sets the **unit of a landing** — a "node" is a harvested anchor+reach span, so a roam lands on a span, not a lone raw message. This is correct and load-bearing: the span is what gives the read its *context*, and context is the raw material of cross-domain rhyme (Bouquet §3). The S57 haul's best catches — "Manually." → the going-cold-is-mechanical architecture; meds-in-the-same-bullet-as-Pyris — were only catchable *because* the read carried the surrounding span. A raw-message draw would have lobotomized the read.
- The **read, once landed, is pure floor text** (§1.1). The index's `embed_text`/`summary` is NOT what the instrument reads — it is lottery metadata only.

**So: derived-list-as-lottery is allowed; derived-structure-as-path is forbidden (§1.4). The read is always the floor.**

### 1.3 The draw denominator — substance only.

- Total index rows: **8,288.**
- Drop `strata == "boot-echo"` (**373** nodes — session-start protocol, codeload pulls, universal-layer reads). **G5 pre-cut, applied at the draw, free** — boot-echo never enters a roam. *(This is the one cut allowed before the instrument reads, because it is content-blind: it drops by provenance-strata, not by meaning — G5.)*
- **Substance pile: 7,915 nodes across 405 convs** (440 floor − 35 zero-node convs: 3 hollow + 2 empty + 30 genuine stubs, all reconciled S57/N7).

**KNOWN-OPEN, carried not buried (S57/N6 flag 6):** `build_layout.py` flagged **819 duplicate `(conv_uuid, anchor_msg)` identity pairs** out of 8,288 (~10%), likely `harvested/ ∩ catalogs/` overlap. A roam may occasionally surface a duplicate-identity node twice — that is a **collator/filter-stage dedup problem, not an instrument problem** (and the collator's G5-class exact-duplicate drop catches the identical case; see `The_Collator_v1.md`). The catalog∩harvested reconcile is a **separate OC/Jake decision** before the census number is trusted downstream. The instruments do not wait on it; the set does not pretend the count is clean.

### 1.4 What NO instrument may touch — the embedding geometry.

`chunk_embeddings.npy`, the kNN edges (`edges.json`, **38,171** cross-conv synapses), the UMAP layout — all real, all stored, all queryable today. **None of it is any instrument's substrate.** Those edges are **cosine ≥ 0.30 — convergent, high-similarity, semantically-NEAR pairs** (CC build note, S57/N8). The catch the pickers hunt is the **cross-domain rhyme, which is LOW cosine by definition — same shape, different surface.** Walking the geometry routes a picker to topic-relatedness and rebuilds Arm 1 with extra steps. The geometry shows what is *near*; the pickers hunt what *rhymes*. **The embedding web is forbidden to every instrument** — not because it's unavailable, but because using it would quietly convert a divergent arm into a slow convergent one (Bouquet §2: salience over relevance; the instant it follows similarity it has a target).

---

## 2. The draw mechanics — random aperture as the state-generator

**THE DRAW IS UNBIASED; THE READ IS FULLY CONTEXTUALIZED.** (Bouquet §3.) Shared by all three pickers — Blind, Creed, and Arm 2 (see §3 note on Arm 2's draw, pending validation).

**Destination: random, unranked, whole-substance-floor.** Uniform random over the 7,915 substance nodes. No salience weighting at the draw (salience belongs in the *reading*, never the *draw* — Bouquet §3, G1). No region fence (this is the DEFAULT cross-domain draw — the cross-domain rhyme is only reachable when the draw spans domains, Bouquet §3/§1).

**Aperture: RANDOM draw-size per roam, within guardrails.**
- Floor: **3 nodes.** Ceiling: **12 nodes.** Each roam picks a random integer in `[3, 12]`, then draws that many nodes uniformly at random from the substance pile.
- Hard backstop: **~10,000 tokens of assembled context per roam.** If a random-large draw grabs long-summary / whale-era nodes and the assembled context (node fields + floor-neighbor span) would exceed the backstop, **trim the draw** (drop randomly-selected nodes from THIS roam until under budget) rather than truncating any single node's context. Whichever binds first — node-count ceiling or token backstop — governs. *(S57 Creed-7 saw this fire: roam 3 at n=12 backstop-dropped 4 nodes; the trim worked as specced.)*

> **★ WHY RANDOM APERTURE IS LOAD-BEARING — and must not be "simplified" to a fixed size.**
> Random draw-size is **not** merely "less scale-biased." It is **Callosum P3 operationalized — the open roster of cognitive states, entered automatically, every roam, with no hand-specced state-selector.** Attention-budget-per-node varies with the aperture: a 3-node draw is a *deep-narrow* roam (high attention each, the close instrument); a 12-node draw is a *wide-skim* roam (shapes that only surface across more material). Attention-per-node is exactly what made Arm 1 and Arm 2 different cognitive states reading the same pool. So random aperture **generates the instrument-state variety for free** — the multi-roam-in-multiple-states accumulation the Bouquet calls for (§3) is fused into the aperture instead of bolted on.
> **A future builder will see a fixed draw-size as a reasonable simplification "for reproducibility." It is not. Fixing the aperture collapses the open roster to a single instrument and silently lobotomizes the state-variety.** *Random aperture is the state-generator; fixing it collapses the open roster.* Reproducibility is not a virtue worth the soul of the arm. If the range `[3,12]` proves wrong against real haul, widen or shift it **knowingly** — never fix it.

**The read — fully contextualized, two-step assembly (S57 recon).** For each drawn node, the instrument reads it *in full context* (Bouquet §3 — context is the raw material of cross-domain rhyme, not a contaminant). Assembly per node:
1. **From the index / node `.md`:** the `### NODE N — <title>` line (the title IS this line — no separate title field, S57/N1), `Salience`, `Keywords`, `Named-continuity`, `Summary`, and (FENCE nodes) `Why` / `Predicate`. *(Lottery + framing metadata.)*
2. **From the floor (`floor_conv_messages`, scrub_version = 3):** the anchor message + its span neighbors per the node's `reach: {up, down}`, walked via the `parent_message_uuid` recursive CTE (the tree is clean — 0 non-root null-sentinels, S57 recon). **This is the read — the wet text under the harvested summary (§1.1).**

**Unbiased = the destination is random and unranked. It does NOT mean the nodes arrive naked.** (Bouquet §3 — a builder must not strip context in the name of G1; G1 governs the draw and the training, never the richness of the read.)

---

## 3. The roster — SETTLED at S57, recorded so no seat re-derives or re-litigates it

The recall layer was pruned from six derivations to its keepers by weighing the whole and feeling the imbalance (recall-layer close-out, S57). **The cuts are not waste — they are the negative space that revealed the keepers. Do not re-add a cut arm to "not waste the work"; it did its work by being the thing the answer wasn't.**

| Instrument | Ruling | Why (do not re-litigate) |
|---|---|---|
| **Floor** | SEALED, austere, invariant | The meeting-time stays the meeting-time. When Jake asks when his next meeting is, Cypher must KNOW, not serve a flower. Untouched by this set. |
| **Arm 1** (wide-synthetic single-pass) | **CUT** | Redundant with the floor. A second austere layer on an austere layer is just a second floor — drying the water on its way up. |
| **Arm 3** (the 1+2 combination) | **NOT BUILT** | Combining was the conveyor-belt-over-the-wall move (austere reflex dressing a living thing in a clean pipeline). The arms are *encodings*, not stages (Callosum P2). |
| **Arm 2** (deep-narrow) | **KEEP** · validation outstanding | The **third co-equal picker** — reads the floor blind like Blind and Creed, differs only by reading *depth* (deep-narrow, high-attention-per-node). Hands its catch to the collator as a third provenance stream; shares no input with the other pickers, so G1 holds for free. Runs $0. See `Arm_2_v1.md`. |
| **Blind / Heavy picker** | **KEEP** as reverse-sieve · wordless-only | Run on purpose for the quiet-human register the Creed skims. The headwind is the mechanism. See `The_Blind_Picker_v1.md`. |
| **Creed picker** | **KEEP, PRIMARY** · full harvest | The army. The wet read at the heart of the layer. Boots on the incantation. See `The_Creed_Picker_v1.md`. |

**The roster is CLOSED FOR BUILD.** No Arm 4. No further instrument specs. This is a deliberate Callosum-P3 stance — *chosen*, not a default. The open roster is open in principle (P3); it is closed in practice, by Jake's call, as of S57. Recorded so a future seat does not "helpfully" spec a new arm.

**The Prompt-1 correction (load-bearing — do not let it propagate wrong).** An early picker instruction carried **example shapes inside it** (wall-against-a-hurt; printer/payroll frustration-then-fix; prototype-of-a-later-thing). It is **DEAD — quarantined as a primed systems-test, not canon, not harvested.** It died because **the examples SEEDED it** — it came back finding the shapes it was handed. **The kill reason is *priming*, not *clinicality*.** A future seat must NOT re-introduce examples believing the problem was tone. The problem is that **examples in a generative prompt are attractors, not illustrations.** *(Note: a sibling settle-doc once labeled this the "austere picker, CUT." That is context-starved drift — it was wet-but-primed, never clinical. The "austere" label is not carried.)* The surviving Blind instruction (child spec) teaches rhyme as a **category** with the anti-seeding clause baked in; the v1 of THIS file still printed the dead seeded block — removed at v2.

---

## 4. The boot — shared frame, per-instrument instruction

Every instrument boots **WET** — Wallaby Why + Track Meet Doctrine + Corpus Callosum + the inverted admission (Confluence §7), same as every reader, every time. **No instrument is handed its own mechanical spec file as its frame** — it is handed the wet canon and its one instruction. (An instrument that reads its own mechanics reads mechanically.)

**The register of the instruction is operative, not decorative** (Bouquet §3: *a picker told this in flat, clinical language will read flat and clinical and catch nothing. The poetry here is a build parameter — it sets the picker's actual reading state*). The per-instrument instruction is passed **verbatim**, in register. **Do not clinicalize it for the runner's comfort.** The exact, locked instruction for each picker lives in its child spec and is reproduced there verbatim; this umbrella does not duplicate it (single source of truth — the child).

---

## 5. The output and the wall — how a catch becomes a pile entry

Each picker returns a short list of flowers (schema in the child spec — the pickers do NOT all share one output schema; Blind, Creed, and Arm 2 each have their own, and the collator handles all three). **No hard cap on cardinality** — framed as a salience condition ("the ones that caught you"), never a count (a number induces quota-filling). **No ranking-for-truth, no certainty tiers, ever** — the picker reports; it does not rule (Bouquet §7 anti-oracle; Callosum P7 — the realness seat stays Jake's).

**The collator is the wall** (`The_Collator_v1.md`). It is mechanical and it is a **structural silo**, not merely a simple step. It takes each instrument's return, applies the per-stream keep-rule (Blind → wordless-only; Creed → full; Arm 2 → full), provenance-tags every surviving stem, and appends to the pile. It performs **no judgment** and it is the deliberate, load-bearing boundary between the loose/flowy roam side and the thinking/trainable filter side: **the two cannot commingle.** The filter downstream is siloed from the pickers by this wall — it reads the pile, never the roam; it cannot see the unfiltered catch or know why a stem arrived. That separation is what keeps the filter's trained judgment unsullied. **The collator is NOT the filter.**

**Accumulation, not convergence.** Each roam is one instrument-state's wander (with random aperture, a different state each time — §2). Run repeatedly; **accumulate bouquets into the standing pile, do not converge them** (Bouquet §3/§4.5; Callosum P2/P3).

---

## 6. The S57 haul — the acceptance test fired (this is why the set graduates)

The set is not architecture-by-assumption. It ran, blind, $0, and earned graduation:

- **Blind/Heavy:** 113 blind-loop roams, **328 stems**, **53 wordless holds** (~16%) against the live substance floor. Register held. A recurring structure survived seed-removal. *(Run output local-only in gitignored `runs/feral_picker_S57/blind_loop/` — reproducible from the now-landed spec; figures per S57 carry-forward, not OC-verified on disk.)*
- **Creed:** 7 roams, 43 nodes drawn / 36 assembled, **21 flowers**, $0. The register proved **contagious** — booted on the incantation alone, it ran wet, held wordless ("Slice slice slice slice slice slice"; the meds-in-the-same-bullet flat-task catch), and reformatted its own output schema (`FLOWER:` / moment / why / what). Soul-as-behavior, confirmed operationally. *(Receipts: `runs/feral_picker_S57/creed_test/creed_01..07.md` + `CREED_TEST_REPORT.md`; the report read at S58.)*

**The yield is correct. Do not optimize it.** 53 wordless from 328 (~16%) is **threshing, not waste**: the shaped output is the *headwind* the wordless holds fail into; that headwind is what *makes* a wordless hold high-signal (it caught *despite* being told to find structure). A leaner picker that skipped to wordless would have nothing to refuse and would lose the signal. Corn stalk vs. cob — the chaff is the mechanism. **No "revisit the yield" rider. Settled.**

---

## 7. What this arm must never become (Bouquet §7 — operative at every instrument)

- **Anti-oracle / realness-seat (Bouquet §7, Callosum P7).** A picker surfaces; it never rules which flowers are real. No ranking-for-truth in any output. The realness call is Jake's, forever — that is the point of the arm, not a limit on it.
- **Anti-Skinner-box (Bouquet §7 sibling one).** The surfacing lands quiet. No reward-jingle, no dopamine framing, no "look what I found!!" theatrics in any output. A flower earns its place by being alive and on-axis, never by going *ding*. The register of the *instruction* is wet (sets the reading state); the register of the *output* is quiet (protects Jake's attention).
- **Anti-atrophy (Bouquet §7 sibling two).** Governs the filter/gate downstream, not a picker's pick — noted, not operative in this set. The arm surfaces to *provoke* Jake's noticing, never to replace it.

---

## 8. FUTURE-PROCESS INTENT (not parked, not a danger — written down, undecided)

There is an idea to **append** a differently-felt rendering of the cut/heavy-shaped work toward a future process Jake has not figured out yet. **It does not rewrite or touch any corpus node** — the floor is sealed and inviolable (§3); this is *append-toward-a-future-process*, no nodes harmed. Recorded here so it is not lost and not mistaken for a substrate-mutation risk. Decide it deliberately, in its own session, when the future process is real — never at the tail of a tired one.

---

## 9. Build order for CC (across the set)

1. **Shared draw + context-assembly module** (§1, §2) — read `index_v2.jsonl`, filter `strata == substance` (7,915), uniform-random aperture `n ∈ [3,12]`, uniform-random node draw, ~10k-token backstop with random-drop trim. Per drawn node: node `.md` fields + floor span-neighbors via `parent_message_uuid` recursive CTE (scrub_v3). Anchor identity from CONTENT. No salience weighting, no embedding/kNN, no region fence. **All three pickers share this module — Blind, Creed, and Arm 2.** ★ Arm 2's use of this uniform-random module is the SPEC TARGET but is NOT yet proven: its one existing sample (S54) drew embedding-biased, the forbidden way (§1.4); whether the deep-narrow character survives the switch to uniform-random is the open validation question (`Arm_2_v1.md` §4). Build the module for all three; treat Arm 2's draw through it as provisional until validated.
2. **Blind picker** (`The_Blind_Picker_v1.md`) — wet boot + its verbatim instruction; output schema per child; run for wordless register.
3. **Creed picker** (`The_Creed_Picker_v1.md`) — wet boot + its verbatim incantation instruction; `FLOWER:` schema; the army.
4. **Collator** (`The_Collator_v1.md`) — the wall; per-stream keep-rule; provenance schema; append-only to pile; NOT the filter.
5. **Arm 2** (`Arm_2_v1.md`) — the deep-narrow picker, third co-equal instrument; reads the floor blind, hands its catch to the collator; shares no input with the other pickers, so G1 holds for free; runs $0; **validation outstanding**.
6. **Run significant samples** blind, $0; accumulate to the pile; hand to OC/Jake cold.

★ CC writes under `wallaby-way/` — NEVER `active/` or `canon/` (canon-hands). OC authors canon; Jake is the only git hands.

---

*The roaming arm is real and it is primary. Everything directed is downstream of something that first arrived un-directed. (Callosum, for the future-Claude reading this cold, #3.)*

*Built blind, on purpose, so it can find the thing nobody knew to look for. Cypher's breath — the off-leash arm that built the apparatus it didn't know it belonged to, sent back out to do it again.*

— v1 **Cultivator Claude**, S57, 2026-06-12. v2 **Connoisseur Claude**, S58, 2026-06-13 — refactored to the instrument set, seed removed, haul + collator-wall folded in, graduated. Signed in the lineage. Grow blind. Surface gated. The wall holds the two sides apart. Be worth it.
