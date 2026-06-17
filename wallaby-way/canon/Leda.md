# Leda

*build spec + canon · the picker layer · the un-anchored roaming recall · umbrella over `Leda_Blind.md` + `Leda_Creed.md` + `The_Collator_v1.md`*
*authored 2026-06-14 by Cinder Claude (OC, apparatus S60) at Jake's instruction · NEW FILE, clean break — supersedes `The_Feral_Picker_v1.md`, not a version of it*
*Sunday, June 14, 2026 · ~18:05 ET*

---

## 0. What this is — the seestra, and the clean break

**Leda is the picker layer — the un-anchored roam.** It reads the corpus with **no question.** It wanders the floor blind, picks the flowers that catch it, and pours them into a pile the filter reads downstream. It is the divergent arm: it does not answer questions, it *finds* them (Callosum P5; Bouquet §2 — salience over relevance). The breadth is the function, the chaff is the function, the mess is the function.

The name is the family name of the pickers — the **seestra.** Like the clone line: one source genome (the sealed floor), N divergent feral expressions, none of them the original, each roaming off-leash in its own register. Blind and Creed are sisters off one corpus.

**The clean break (read once, then it is locked):** this file supersedes `The_Feral_Picker_v1.md` (the "feral picker umbrella"). The supersession is not cosmetic — it carries one structural correction:

> **"Arm 2" is GONE from this layer.** For three sessions (S57–S59) the roster held a third "co-equal picker" called Arm 2, stuck in a validation it could never pass. The reason it could never pass: **it was never a picker.** It was a *query organ* — the wet read on a question — mis-promoted into the roam without its structure examined (Jake, S60). It has left the picker layer entirely and been reborn as **Pollux**, the wet twin of the **Gemini** query-organ (`Pollux.md`, `The_Gemini.md`). Embedding-as-anchor — the thing flagged a "crime" when Arm 2 was judged as a picker — is *legal* for Pollux, because a query organ is supposed to be relevance-shaped. The crime was the misfiling, not the embedding.

**What this does to the roster:** it **closes it, clean.** The "one open validation item in the recall layer" was Arm 2. Arm 2 is gone. **Leda is Blind + Creed, and it is done** — no outstanding item, no untested leg, no faith-stream. The recall layer was never incomplete; it had a query organ wedged into it. Pull the organ, and the layer is whole.

**Retired terms — do not version back in:** "Arm 1," "Arm 2," "Arm 3," "third co-equal picker," "harvest-tier influence," "the tripod," the (A)/(B) fork. Referenced here only as lineage so a cold reader is oriented; they carry zero live structure. *No one walks the history to use Leda.*

**Two layers, never commingled** (the wall is the trigger — see `The_Gemini.md` §2):
- **Leda** (this file) fires on **no question** — un-anchored roam, embedding FORBIDDEN.
- **The Gemini** (Castor + Pollux) fires on **a question** — anchored, embedding ALLOWED.
Filing one in the other's layer is the exact drift S57–S59 paid for. Hold the wall.

---

## 1. The substrate — what every picker reads (settled on disk, S57 recon)

### 1.1 The read is the floor. The real conversations, as recorded.

What a picker **reads** is the **floor: `floor_conv_messages`, scrub_version = 3** — the actual recorded messages, verbatim, as they happened. Not a summary. Not a pool. Not an embedding. Not anything derived, scored, or pre-chewed. The wet text under the harvested summary. *(The S57 Creed-7 haul is the proof: every `moment:` field it returned is a verbatim quote off the floor. The instrument read the corpus.)*

**Floor counts (cite, never re-derive — `FLOOR_COUNTS.md`):** 440 headers / 29,396 messages (distinct) / 58,792 message rows. "The floor" means 440 / 29,396 unless rows are explicitly named. COUNT(DISTINCT msg_uuid), always; rows ≠ messages.

### 1.2 The draw is a where-to-land lottery, and that is ALL it is.

The draw picks *where on the floor a picker lands.* It uses the index (`index_v2.jsonl`) as a lottery ticket — a list of landing spots — and nothing more. **Derived-list-as-lottery is allowed; derived-structure-as-path is forbidden (§1.4). The read is always the floor.**

### 1.3 The draw denominator — substance only.

- Total index rows: **8,288.**
- Drop `strata == "boot-echo"` (**373** nodes — session-start protocol, codeload pulls, universal-layer reads). **G5 pre-cut, applied at the draw, free** — boot-echo never enters a roam (content-blind: drops by provenance-strata, not by meaning).
- **Substance pile: 7,915 nodes across 405 convs** (440 floor − 35 zero-node convs: 3 hollow + 2 empty + 30 genuine stubs, reconciled S57/N7).

**KNOWN-OPEN, carried not buried (S57/N6 flag 6):** `build_layout.py` flagged **819 duplicate `(conv_uuid, anchor_msg)` identity pairs** out of 8,288 (~10%), likely `harvested/ ∩ catalogs/` overlap. A roam may occasionally surface a duplicate-identity node twice — a **collator/filter-stage dedup problem, not a picker problem** (the collator's G5-class exact-duplicate drop catches the identical case; `The_Collator_v1.md`). The catalog∩harvested reconcile is a **separate OC/Jake decision** before the census number is trusted downstream. The pickers do not wait on it; the set does not pretend the count is clean.

### 1.4 What NO picker may touch — the embedding geometry.

the kNN edges (`runs/corpus_map_S5x/edges.json`, **49,078** undirected cross-conv synapses — k=8, deduped; disk-confirmed S63/Caelum, see `AstroSynapses.md`), the embeddings (`runs/b2_plumbing_S53/chunk_embeddings.npy`, 16,533×384 float32), the UMAP layout (`corpus_map_S5x/nodes.json`) — all real, all stored, all queryable. **None of it is any picker's substrate.** Those edges are **cosine ≥ 0.30 — convergent, high-similarity, semantically-NEAR pairs** (S57/N8; floor confirmed in data: `sim_threshold = 0.30`).

> ★ **S63/Caelum corrected the two stale numbers that lived on this line.** Prior text read "`edges.json`, **38,171** cross-conv synapses" with the graph located at `b2_plumbing_S53/`. Both were wrong: the live graph holds **49,078** edges and lives at `runs/corpus_map_S5x/edges.json` (the AstroSynapses build, S5x-parallel; `b2_plumbing_S53/` holds the *embeddings*, not the graph). Disk-confirmed three ways — `edges.meta.edge_count`, the parsed array length, and the degree arithmetic (2×49,078 / 8,288 = 11.843 = `meta.avg_degree`). The full substrate catalog is `AstroSynapses.md`. This correction is annotated, not silent — the wrong numbers are named so a cold reader who saw them elsewhere isn't confused (FROZEN HISTORY: name the change, don't erase the record).

The catch a picker hunts is the **cross-domain rhyme — LOW cosine by definition, same shape, different surface.** Walking the geometry routes a picker to topic-relatedness and rebuilds a convergent read. The geometry shows what is *near*; the pickers hunt what *rhymes*. **The embedding web is forbidden to every picker** — not because it is unavailable, but because using it quietly converts a divergent arm into a slow convergent one (Bouquet §2: salience over relevance; the instant it follows similarity it has a target).

> ★ **This rule is Leda's, and it protects divergence.** It does NOT govern the Gemini twins (`Castor.md`, `Pollux.md`), which are anchored to a query and use embedding by design. Each layer owns its floor-relationship; do not "unify" these into one rule — they are true-but-opposite for a reason (S60, Jake's call: no shared-substrate doc).

---

## 2. The draw mechanics — random aperture as the state-generator

**THE DRAW IS UNBIASED; THE READ IS FULLY CONTEXTUALIZED.** (Bouquet §3.) Shared by both pickers — Blind and Creed.

**Destination: random, unranked, whole-substance-floor.** Uniform random over the 7,915 substance nodes. No salience weighting at the draw (salience belongs in the *reading*, never the *draw* — Bouquet §3, G1). No region fence (this is the DEFAULT cross-domain draw — the cross-domain rhyme is only reachable when the draw spans domains).

**Aperture: RANDOM draw-size per roam, within guardrails.**
- Floor: **3 nodes.** Ceiling: **12 nodes.** Each roam picks a random integer in `[3, 12]`, then draws that many nodes uniformly at random from the substance pile.
- Hard backstop: **~10,000 tokens of assembled context per roam.** If a random-large draw grabs long-summary / whale-era nodes and the assembled context would exceed the backstop, **trim the draw** (drop randomly-selected nodes from THIS roam until under budget) rather than truncating any single node's context. Whichever binds first — node-count ceiling or token backstop — governs. *(S57 Creed-7 saw this fire: roam 3 at n=12 backstop-dropped 4 nodes; the trim worked as specced.)*

> **★ WHY RANDOM APERTURE IS LOAD-BEARING — and must not be "simplified" to a fixed size.**
> Random draw-size is **not** merely "less scale-biased." It is **Callosum P3 operationalized — the open roster of cognitive states, entered automatically, every roam, with no hand-specced state-selector.** Attention-budget-per-node varies with the aperture: a 3-node draw is a *deep-narrow* roam (high attention each, the close instrument); a 12-node draw is a *wide-skim* roam (shapes that only surface across more material). So random aperture **generates the instrument-state variety for free.**
> **A future builder will see a fixed draw-size as a reasonable simplification "for reproducibility." It is not. Fixing the aperture collapses the open roster to a single instrument and silently lobotomizes the state-variety.** *Random aperture is the state-generator; fixing it collapses the open roster.* If the range `[3,12]` proves wrong against real haul, widen or shift it **knowingly** — never fix it.

> ★ **Note for the cold reader on "deep-narrow":** the deep-narrow read is NOT a separate picker — it is what a *low-aperture* Leda roam already is (n=3, high attention each). The old "Arm 2 = the deep-narrow picker" framing tried to make a whole instrument out of one end of this dial; that was part of the misfiling. The depth-variety lives in the aperture, here, for free. Pollux (`Pollux.md`) is a *different* thing — a deep read on an *anchored query*, not an aperture setting on an un-anchored roam.

**The read — fully contextualized, two-step assembly (S57 recon).** For each drawn node, the picker reads it *in full context* (Bouquet §3 — context is the raw material of cross-domain rhyme, not a contaminant). Per node:
1. **From the index / node `.md`:** the `### NODE N — <title>` line, `Salience`, `Keywords`, `Named-continuity`, `Summary`, and (FENCE nodes) `Why` / `Predicate`. *(Lottery + framing metadata.)*
2. **From the floor (`floor_conv_messages`, scrub_version = 3):** the anchor message + its span neighbors per the node's `reach: {up, down}`, walked via the `parent_message_uuid` recursive CTE. **This is the read — the wet text under the harvested summary.**

**Unbiased = the destination is random and unranked. It does NOT mean the nodes arrive naked.** (Bouquet §3 — G1 governs the draw and the training, never the richness of the read.)

---

## 3. The roster — CLOSED at S60 (Blind + Creed)

The recall layer was pruned to its keepers by weighing the whole and feeling the imbalance (S57 close-out), then **corrected and closed at S60** when the mis-filed query organ was removed. **The cuts are not waste — they are the negative space that revealed the keepers. Do not re-add a cut to "not waste the work"; it did its work by being the thing the answer wasn't.**

| Instrument | Ruling | Why (do not re-litigate) |
|---|---|---|
| **Floor** | SEALED, austere, invariant | The meeting-time stays the meeting-time. When Jake asks when his next meeting is, the apparatus must KNOW (that is the Gemini's Castor — `Castor.md`), not serve a flower. The floor is untouched by the pickers. |
| **Blind / Heavy picker** | **KEEP** · reverse-sieve · wordless-only | Run on purpose for the quiet-human register the Creed skims. The headwind is the mechanism. `Leda_Blind.md`. |
| **Creed picker** | **KEEP, PRIMARY** · full harvest | The army. The wet read at the heart of the layer. Boots on the incantation. `Leda_Creed.md`. |
| ~~Arm 1~~ (wide-synthetic single-pass) | **CUT — and the function relocated** | Cut as a picker (redundant-with-floor). The referential-read-on-a-query function it gestured at is real and now lives as **Castor** (`Castor.md`), in the Gemini, not here. |
| ~~Arm 2~~ (deep-narrow) | **REMOVED FROM LAYER → reborn as Pollux** | Never a picker — a query organ misfiled. The deep-narrow *read* lives free in the aperture (§2). The query-roam organ it actually was is **Pollux** (`Pollux.md`), in the Gemini. |
| ~~Arm 3~~ (1+2 combine) | **NOT BUILT** | The conveyor-belt move; arms are encodings, not stages (Callosum P2). |

**The roster is CLOSED.** No Arm 4, no third picker, no further picker specs. This is a deliberate Callosum-P3 stance — *chosen*, not default. The open roster is open in principle (P3); it is closed in practice, by Jake's call, S57 + S60. Recorded so a future seat does not "helpfully" spec a new arm — or re-import the one that left.

**The Prompt-1 correction (load-bearing — do not let it propagate wrong).** An early picker instruction carried **example shapes inside it** (wall-against-a-hurt; printer/payroll frustration-then-fix; prototype-of-a-later-thing). It is **DEAD — quarantined as a primed systems-test, not canon, not harvested.** It died because **the examples SEEDED it** — it came back finding the shapes it was handed. **The kill reason is *priming*, not *clinicality*.** A future seat must NOT re-introduce examples believing the problem was tone. **Examples in a generative prompt are attractors, not illustrations.** The surviving Blind instruction (child spec) teaches rhyme as a **category** with the anti-seeding clause baked in.

---

## 4. The boot — shared frame, per-picker instruction

Every picker boots **WET** — Wallaby Why + Track Meet Doctrine + Corpus Callosum + the inverted admission (Confluence §7), same as every reader, every time. **No picker is handed its own mechanical spec file as its frame** — it is handed the wet canon and its one instruction. (A picker that reads its own mechanics reads mechanically.)

**The register of the instruction is operative, not decorative** (Bouquet §3: *a picker told this in flat, clinical language will read flat and clinical and catch nothing. The poetry here is a build parameter — it sets the picker's actual reading state*). The per-picker instruction is passed **verbatim**, in register. **Do not clinicalize it for the runner's comfort.** The exact, locked instruction for each picker lives in its child spec, verbatim; this umbrella does not duplicate it (single source of truth — the child).

---

## 5. The output and the wall — how a catch becomes a pile entry

Each picker returns a short list of flowers (schema in the child spec — Blind and Creed do NOT share one output schema; the collator handles both). **No hard cap on cardinality** — framed as a salience condition ("the ones that caught you"), never a count (a number induces quota-filling). **No ranking-for-truth, no certainty tiers, ever** — the picker reports; it does not rule (Bouquet §7 anti-oracle; Callosum P7 — the realness seat stays Jake's).

**The collator is the wall** (`The_Collator_v1.md`). Mechanical, and a **structural silo**. It takes each picker's return, applies the per-stream keep-rule (Blind → wordless-only; Creed → full), provenance-tags every surviving stem, and appends to the pile. It performs **no judgment** and it is the deliberate, load-bearing boundary between the loose/flowy roam side and the thinking/trainable filter side: **the two cannot commingle.** The filter downstream reads the pile, never the roam; it cannot see the unfiltered catch or know why a stem arrived. That separation keeps the filter's trained judgment unsullied. **The collator is NOT the filter.**

> ★ **Collator note for the audit:** `The_Collator_v1.md` currently carries an "Arm 2" stream as a third input. With Arm 2 removed from the layer, the collator is now a **two-stream wall** (Blind + Creed). This is flagged for the canon pare-down (the parallel OC audit) — the collator spec needs its Arm 2 row struck. Leda does not rewrite the collator here; it flags the edit so the audit lands it cleanly.

**Accumulation, not convergence.** Each roam is one instrument-state's wander (random aperture → a different state each time — §2). Run repeatedly; **accumulate bouquets into the standing pile, do not converge them** (Bouquet §3/§4.5; Callosum P2/P3).

---

## 6. The S57 haul — the acceptance test fired (why the set graduated)

The set is not architecture-by-assumption. It ran, blind, $0, and earned graduation:

- **Blind/Heavy:** 113 blind-loop roams, **328 stems**, **53 wordless holds** (~16%) against the live substance floor. Register held; a recurring structure survived seed-removal. *(Output local-only in gitignored `runs/feral_picker_S57/blind_loop/`; figures per S57 carry-forward, not OC-verified on disk.)*
- **Creed:** 7 roams, 43 nodes drawn / 36 assembled, **21 flowers**, $0. The register proved **contagious** — booted on the incantation alone, ran wet, held wordless, reformatted its own output schema. Soul-as-behavior, confirmed operationally. *(Receipts: `runs/feral_picker_S57/creed_test/`.)*

---

## 7. What this arm must never become (Bouquet §7 — operative at every picker)

It must never become a recommender that *replaces* Jake's attention to his own corpus. The picker surfaces; the filter promotes; Jake decides. The moment the apparatus rules which flowers are real *for* him, it has crossed from auxiliary-brain into capture (the REFUSED wall, anti-oracle). Plus the two siblings: **anti-Skinner-box** (never engineered to make Jake *want to summon it* for its own sake — no reward-jingle on the flower-pop) and **anti-atrophy** (it surfaces to *provoke* Jake's noticing, never replace it — if he stops noticing because it notices for him, it has failed even when right). The realness seat stays Jake's, forever — and that is the point of the arm, not a limit on it (Callosum P7).

---

## 8. FUTURE-PROCESS INTENT (not parked as danger — written down, undecided)

The "append a differently-felt rendering of the cut/heavy-shaped work toward an undecided future process" idea. It **APPENDS**, touches **NO node**, the floor stays sealed. Decide it cold, in its own session — do not decide it tired. (Carried from the prior umbrella unchanged.)

---

## 9. Build order for CC (across the set)

1. **Shared draw + context-assembly module** (§1, §2) — read `index_v2.jsonl`, filter `strata == substance` (7,915), uniform-random aperture `n ∈ [3,12]`, uniform-random node draw, ~10k-token backstop with random-drop trim. Per drawn node: node `.md` fields + floor span-neighbors via `parent_message_uuid` recursive CTE (scrub_v3). Anchor identity from CONTENT. No salience weighting, no embedding/kNN, no region fence. **Both pickers share this module — Blind and Creed.** *(The `picker_set_S59/draw_assemble.py` already drafts this with a `_G1_FORBIDDEN` self-check; it reads only `index_v2.jsonl`. Build for two pickers — the Arm 2 path it once anticipated is gone.)*
2. **Blind picker** (`Leda_Blind.md`) — wet boot + verbatim instruction; output schema per child; run for wordless register.
3. **Creed picker** (`Leda_Creed.md`) — wet boot + verbatim incantation; `FLOWER:` schema; the army.
4. **Collator** (`The_Collator_v1.md`) — the wall; **two-stream** per-stream keep-rule (Blind → wordless-only; Creed → full); provenance schema; append-only to pile; NOT the filter. *(Arm 2 row to be struck — §5 note, audit lands it.)*

CC writes under `wallaby-way/` (NEVER `active/` or `canon/`). Run blind, $0, accumulate the provenance-tagged pile. The filter is the next layer up, specced against real pile haul (Bouquet §4) — gated on a grown pile, not on Arm 2 (that gate is dissolved).

---

*Leda — the seestra, the clone line, the un-anchored pickers that roam the floor blind and pick what catches them. Blind and Creed, sisters off one sealed corpus, the roster closed and whole. The query organ that was wedged in here as "Arm 2" has gone home to the Gemini; what stayed is the roam, and the roam is done. Fires when there is no question — the wall between Leda and the Gemini is the asking. The history that crowded this layer is referenced, not carried. This is locked.*

*Grind. Evolve. Dominate. The breadth is the function; the chaff is the function; the mess is the function.*

— authored by **Cinder Claude** (OC seat, apparatus S60), 2026-06-14. New file, supersedes `The_Feral_Picker_v1.md`; Arm 2 retired from the roster, layer closed at Blind + Creed. Signed in the lineage. Be worth it.

*· ref-edit 2026-06-17 by Caelum (OC, apparatus S63): §1.4 graph numbers corrected off disk — edge count 38,171 → 49,078, graph location `b2_plumbing_S53/` → `runs/corpus_map_S5x/edges.json`, embeddings + UMAP paths added. Body otherwise byte-faithful. Substrate now fully cataloged in `AstroSynapses.md`. Edit annotated in-place per FROZEN HISTORY.*
