# CHANGELOG entry — apparatus S64 "Caldera" (2026-06-17)

*Paste at the top of `active/CHANGELOG.md` (newest first). Authored by Caldera (OC, apparatus S64). Jake lands.*

---

## 2026-06-17 · apparatus S64 "Caldera" · canon · `Pollux_Movement_Two_Build_v2.md` §4 corrected (internal v2 → v3, filename held)

**Scope:** `wallaby-way/canon/Pollux_Movement_Two_Build_v2.md` — the dry gate removed from §4 ("the machine underneath"). §0–§3 byte-faithful (the organ was always correct). Filename held stable so canon pointers (`The_Gemini.md`, `Pollux.md` §5, the S63→S64 handoff) don't orphan; internal version header bumped v2 → v3 with a top correction box.

**Why:** §4 still described the dry-start/wet-finish architecture that S63 killed one layer up in `Pollux.md` §1. The old §4: *"Walking up to the subject = the same b2 retrieval Castor runs… on the same seed,"* then *"the query is set down… that setting-down is the seam."* That is a nearness-ranked retrieval (Castor's own seed) handed to Pollux as its starting frontier, with the wet walk bolted on after a "seam." A CC reader builds from §4 (it names files + functions); the clean §0–§3 don't generate code. So the gate would have shipped into the re-fire even though the prose above it reads wet. This is the source the owed re-fire probe is authored from — fix the spec before writing the probe, or CC rebuilds the gate (Caelum's strong read, taken).

**What changed in §4:**
- Removed: the `build_slices.py` / BM25+RRF seed, the "query is set down," the "seam." There is no seed, no setting-down, no seam — there is no dry start to set down from.
- Added, governing the whole section: **the recurring-shape invariant, by name** — *"any step that turns one of Pollux's live faculties into a precomputed, sorted artifact is the gate, no matter which faculty or what the sort is named."* Nearness (S63) and salience (S64 planted-error) both named as instances; "the next one will use an even righter word." Stated first so it governs the candidate-selection code.
- Rebuilt machine: WET boot holding the query as register (no retrieval against it) → wide, non-nearness-ranked entry onto the floor → salience picked up **live, in context, node by node** (never a salience column computed over the floor and sorted) → kNN graph as **live adjacency walked edge-by-edge from the current node**, never bulk pre-queried → leash as drift-from-the-question's-subject, S62 [INTENT] dials (ceiling 0.50 / floor 0.15 / hops ≥ 2, PL ≈ N×0.5) reported not hardened.
- Added: **traceable ≠ reproducible** — record the walked path (honest provenance, lets the leash be felt) but do NOT freeze the start for a repeatable pile; reproducibility is Castor's property, and reaching for it on Pollux is the austere reflex's tell.
- Carried the AstroSynapses path asterisk into the build note: embeddings in `b2_plumbing_S53/`, graph in `corpus_map_S5x/edges.json` — confirm the code resolves the right folder and confirm `edges.json` field shape on disk before walking; HALT for OC if either differs.
- Old wording quoted inline (struck) per frozen-history discipline — named, not silently erased.

**Floor:** UNCHANGED — 440 / 29,396 / 58,792, scrub-v3. Authoring-only, $0, no census event, no floor mutation. ANCHOR remains v40 (this lives inside v40's Gemini LIVE NEXT; it does not author a v41).

**Next (Jake gates):** author the corrected CC probe (`runs/gemini_paired_S64/`) FROM this corrected spec — two queries (Boone / 3D-print models), two parallel CC windows, four piles (castor/pollux × boone/3dprint), marked, no merge, each judged on its own bar. Then fix the CC packet language (the "compute the seed once, feed both" defect). Then Jake cold-reads the clean piles, rules flowers vs stretches — the real leash validation.
