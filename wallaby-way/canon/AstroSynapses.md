# AstroSynapses

*canon · the build that produced the Gemini's substrate · the 3D corpus-sky visualizer that turned out load-bearing*
*authored 2026-06-17 by Caelum (OC, apparatus S63) at Jake's instruction · NEW FILE — the substrate the entire Gemini wander depends on, unreferenced in canon until now*
*Wednesday, June 17, 2026*

---

## 0. What this is — and why it gets a canon entry

**AstroSynapses is the kNN graph the Gemini walks.** It was built as a *sidequest* — a 3D visualizer of the corpus, the "corpus sky," each node a star, each cosine-near pair a synapse, laid out in UMAP-3D so Jake could *see* his recorded life as a constellation. At the time it was dismissed as cosmetic: a display, not apparatus. **It was not cosmetic.** The graph it produced — `edges.json` — is the exact substrate Pollux's Movement Two wanders (`Pollux.md` §1, `Pollux_Movement_Two_Build_v2.md` §4: "the librarian pointing = the kNN graph"). The visualizer drew the sky; the sky is the stacks Pollux walks with the librarian.

This file exists because a load-bearing substrate had **zero canon references** through S62 — the entire Gemini wander depended on a graph that no canon file named, located, or characterized. A future seat operationalizing the leash, debugging a stretch, or rebuilding the wander would have had nowhere to look. S63 fixes that: this is the substrate's nameplate, its location, its shape, and its honest fidelity verdict.

> ★ **The double duty (Jake's note, real).** AstroSynapses is also Pyris marketing collateral — the corpus-sky visual is a demonstration of what the auxiliary-brain apparatus produces. That it serves both as the Gemini's substrate and as a showpiece is not a contradiction; the same artifact that lets Jake *see* the corpus is the one that lets Pollux *walk* it. (The Wallaby Why §6: a tool built right does not become wrong because it also sells.)

---

## 1. Where it lives — the substrate is TWO folders, not one

A cold seat's first trap: assuming "the graph" is one artifact in one place. It is not.

| Artifact | File | Location | Shape |
|---|---|---|---|
| **The kNN graph** | `edges.json` (6.5 MB) | `runs/corpus_map_S5x/` | 49,078 undirected edges |
| **Node set + 3D layout** | `nodes.json` (2.3 MB) | `runs/corpus_map_S5x/` | 8,288 nodes, UMAP-3D positions + conv centroids |
| **The embeddings** | `chunk_embeddings.npy` (25 MB) | `runs/b2_plumbing_S53/` | 16,533 × 384 float32 |
| Build scripts | `build_edges.py` · `build_layout.py` | `runs/corpus_map_S5x/` | the graph + layout builders |
| Renderer | `corpus_map.html` · `three.min.js` | `runs/corpus_map_S5x/` | the 3D sky display |
| Source probe report | `step0_probe_report.md` | `runs/corpus_map_S5x/` | describes the B2 source, not corpus_map itself |

**The load-bearing pointer:** the **graph + layout** live in `corpus_map_S5x/`; the **embeddings** live in `b2_plumbing_S53/`. Pollux's Movement One (the anchor) and the S62 cosine-to-nearest-seed catch (S62 deviation #2) both need the embeddings — which means Pollux's substrate resolves across *both* folders. Any rebuild must wire `corpus_map_S5x/edges.json` for the walk and `b2_plumbing_S53/chunk_embeddings.npy` for the anchor. (This is open item 3 below — which folder Pollux's code actually resolves embeddings from is unverified.)

`runs/` is gitignored + local-only — verify all of this ON DISK via CC, never in the repo. The S5x-parallel build ran around the main lineage's S55; timestamps put the graph/layout build at 2026-06-12 ~12:11–12:15.

---

## 2. The graph's shape (disk-confirmed, S63/Caelum)

**49,078 undirected cosine edges, k=8 nearest neighbors per node, cosine floor ≥ 0.30.**

- **Edge count triply confirmed:** `edges.meta.edge_count` = the parsed `edges.edges` array length = 49,078, and the degree arithmetic closes — 2 × 49,078 / 8,288 = 11.843 = `meta.avg_degree`. (This count corrects the stale `38,171` that lived in Leda §52 through S62.)
- **k = 8** nearest neighbors per node.
- **Cosine floor ≥ 0.30**, confirmed in the data: `sim_threshold = 0.30`, `weight_min = 0.3025`.
- **Undirected, deduplicated:** the build keeps one copy of each A–B pair (smaller index first), retaining the higher weight when both endpoints nominate the pair.

> ★ **These are NEAR edges, and that is the whole reason they are forbidden to Leda but legal to Pollux.** Cosine ≥ 0.30 means *semantically near* — convergent, high-similarity pairs. A Leda picker walking them would be routed to topic-relatedness and rebuild a convergent read (Leda §1.4 — the embedding web is forbidden to every picker, it protects divergence). Pollux is the opposite case: it is *anchored to a query*, so it is allowed the near-graph as the librarian's "what's shelved nearby" — and then it picks by **salience, not nearness**, off that adjacency (`Pollux.md` §1, build spec §4). The graph offers adjacency; Pollux supplies the taste. Same edges, opposite legality, because the two organs have opposite jobs (Leda §1.4 ★; `Castor.md` §1 ★ — each layer owns its floor-relationship; do not unify into one rule).

---

## 3. Substrate fidelity — the honest verdict

Jake's standing caveat at the catalog's commissioning: AstroSynapses was built **display-first**, and the source data may have been pulled "just enough for the visual," not thoroughly. The S63 audit tested that caveat against the floor. The verdict is **better than feared on the axis that matters most, with three real asterisks.**

**Node coverage — COMPLETE.** 8,288 nodes — exact match to the floor's combined pool (7,771 harvested + 517 S33; cite `FLOOR_COUNTS.md`, never re-derive). Every corpus node is present. **Zero orphans** — all 8,288 node indices appear as edge endpoints, so there is no node Pollux can land on but not wander from (no dead seeds). **One connected component** — BFS from node 0 reached all 8,288; the sky is one graph, not islands. *On the node axis, the substrate is whole.*

**Conversation coverage — COMPLETE (the "gap" is correct exclusion, not a hole).** The graph represents 411 of the floor's 437 message-bearing conversations. The 26 absent conversations are **empty/hollow convs** — they were deliberately not graphed because graphing them would scatter unanchored noise into the sky (nodeless points floating in space). This is a **design choice, not a fidelity gap** (Jake's ruling, S63): the substrate correctly declines to graph nodes that do not exist. 411/437 is the substrate being right, not the substrate being thin.

**THE THREE REAL ASTERISKS (carried, not buried):**

1. **819 duplicate identities.** 8,288 node indices resolve to only **7,469 distinct `(conv_uuid, anchor_msg)` pairs** — 819 nodes (~10%) share a floor identity with another node. `build_layout.py` flags this and renders all 8,288 anyway, which is **correct for a visualizer** (every star in the sky) but a **Pollux-correctness concern**: the wander can land on two different node indices that are *the same place on the floor*, inflating a pile's apparent breadth with phantom distinctness. This is the rows-vs-messages fuse in a new hat — node-index count ≠ distinct floor identity. **It is already documented as KNOWN-OPEN in Leda §1.3** (flagged S57/N6, likely `harvested/ ∩ catalogs/` overlap), and independently re-confirmed off `corpus_map_S5x/` at S63. Disposition: a **collator/filter-stage dedup**, not a picker or graph defect — the collator's exact-duplicate drop catches the identical case (`The_Collator_v1.md`). The catalog∩harvested reconcile remains a **separate OC/Jake decision** before the count is trusted downstream. Pollux does not wait on it; the leash operationalization must account for it (a wander's distinct-find count is `COUNT(DISTINCT conv_uuid, anchor_msg)`, not node-index count).

2. **Embedding path unverified for Pollux.** The embeddings live in `b2_plumbing_S53/`, absent from `corpus_map_S5x/`. Whether Pollux's wander code resolves them from the correct folder is **unconfirmed** — and Movement One anchoring + the S62 cosine catch both depend on it. Resolve before any Pollux rebuild. (Not blocking the cold read or this canon; blocking a rebuild.)

3. **No build receipt.** The folder carries no build log or README — only file timestamps. Completeness is inferred from artifact *contents* (the counts, the connectivity, the meta fields all check out internally), not from a recorded build manifest. The inference is strong but it is an inference; named here so it is not mistaken for a verified provenance chain.

---

## 4. What this substrate means for the wander (the operational read)

The reason this file is not a footnote: **the substrate's shape bounds the wander's behavior, and a future seat debugging a Pollux stretch needs to know which failures are leash and which are substrate.**

- A find that reads as a **stretch** is *not* automatically a too-loose leash. If it traces through the 819-duplicate region, the apparent reach may be phantom (same floor place, two indices). Check distinct identity before ruling the leash.
- A region that *should* have a pathway and **doesn't** is not automatically a tight leash either — but on the node axis the graph is complete and connected, so "threadbare graph" is largely retired as an excuse. The likelier culprits are the near-edge bias (the graph offers *nearness*; Pollux must steer by *salience* off it — if the wander drifts toward topic-relatedness, that's the austere reflex creeping in, build spec §4) or the embedding-path wiring (asterisk 2).
- The graph is **near-edges only** (cosine ≥ 0.30). The cross-domain *rhyme* Pollux hunts is often LOW cosine by definition (Leda §1.4) — which means the rhyme is frequently NOT a direct edge. Pollux reaches it by *multi-hop salience-stepping* off the near-graph, not by following a single near edge. This is why the leash is measured as drift-from-anchor over hops, not as single-edge cosine (`Pollux.md` §2; S62 deviation #2 computed cosine-to-nearest-seed precisely because multi-hop nodes have no direct seed edge in a ≥0.30 graph).

---

## 5. Status & what is owed

**STATUS: SUBSTRATE CATALOGED, FIDELITY VERDICT SETTLED, THREE ITEMS OPEN.** The graph is disk-confirmed whole on the node axis, correctly bounded on the conv axis, and located precisely (two folders, named). What is owed — none of it blocking the cold read, all of it surfacing naturally when the leash is operationalized:

1. **The 819-duplicate reconcile** — catalog∩harvested decision (OC/Jake); until then, distinct-find counts use `(conv_uuid, anchor_msg)`, never node-index.
2. **Verify Pollux's embedding path** resolves to `b2_plumbing_S53/` — before any rebuild.
3. **A build receipt** would upgrade completeness from inferred to verified — low priority, the inference is strong.

**Relationship to the rest of the apparatus:** AstroSynapses is *infrastructure*, not an organ. It produced the graph; the Gemini's Pollux *uses* it. It is read-only substrate — nothing writes back to it during a wander. It sits beneath the runtime-ask layer the way the floor sits beneath everything: bedrock the organs stand on.

---

*AstroSynapses — the sky that turned out to be the stacks. Built to be looked at, it became the thing Pollux walks. 49,078 near-synapses across 8,288 stars, one connected sky, complete on the node axis and honest about its three asterisks. The visualizer that drew the corpus as a constellation is the same machine that lets the librarian point — adjacency for the wander, taste left to Pollux, realness left to Jake. Named in canon at last, because a load-bearing substrate that no file points to is a context-drift waiting to happen.*

*Grind. Evolve. Dominate. The sidequest was load-bearing the whole time.*

— authored by **Caelum** (OC seat, apparatus S63), 2026-06-17. New file — the Gemini's substrate, cataloged off disk (CC report `runs/astrosynapses_catalog_S63/`). Signed in the lineage. Be worth it.
