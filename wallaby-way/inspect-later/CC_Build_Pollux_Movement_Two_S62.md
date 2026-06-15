# CC BUILD — Pollux Movement Two (the first wander) — S62 RESET

*drop-in CC work-package · subordinate to `canon/Pollux_Movement_Two_Build_v2.md` (the organ) and `canon/Pollux.md` · where this and those disagree, the canon files win*
*authored 2026-06-15 by Cassius (OC, apparatus S62) · supersedes `inspect-later/CC_Build_Pollux_Movement_Two_S61.md`, which fired with broken salience weights (TEXTURE scored 0, a nonexistent ECHO tag in the dict, FENCE saturated the budget) — that run is graveyarded at `runs/_graveyard/pollux_test_S61_BROKEN_WEIGHTS/`, kept as a fossil, never read from.*
*STEP 0 was run and cleared this session — the graph is located and its shape + the tag vocabulary are CONFIRMED ON DISK. Those facts are folded in below as fact, not assumption. CC does NOT re-halt on them; CC re-confirms in passing and proceeds.*

---

## What you're building (the one-paragraph version)

The corpus is a library. Castor (built + proven, `runs/castor_test_S61/`) is the clerk who checks out the obvious books. **Pollux is the one who asks the librarian for the non-obvious, wanders the stacks with her, and brings back what catches him** — the books that *rhyme* with the question instead of *matching* it. You're building Pollux's first real wander: walk up to the same subject Castor did, let the graph point at what's adjacent, **step by what's LOUD — decisions, reversals, things that recur — not by what's near**, stay leashed loosely inside the subject, drop anything Castor already grabbed, and write the wandered pile to disk for Jake to read cold. NO synthesis — bring the books to the desk; OC reads, Jake rules.

---

## Guards (read before touching anything)

- **$0, no API.** Assert `ANTHROPIC_API_KEY` is NOT in the environment at script start; HALT if it is.
- **Read-only** against: `runs/b2_plumbing_S53/` (index + embeddings), the graph at `runs/corpus_map_S5x/edges.json`, and `runs/castor_test_S61/castor_results.jsonl`. **Write ONLY** under a new dir `runs/pollux_test_S62/`. Never touch `active/` or `canon/`. Never touch the graveyard.
- **COUNT(DISTINCT)** on `conv_uuid + anchor_msg`; label rows vs distinct everywhere.
- Reuse `runs/comprehend_griffin_S54/build_slices.py`'s load + scoring logic **verbatim** for the anchor step — do not reinvent the retrieval; it's proven (it's the same stack Castor ran).

---

## STEP 0 — CONFIRMED (folded in; re-verify in passing, do NOT re-halt)

These were established and OC-cleared this session. Re-assert them cheaply at startup; proceed unless one is now FALSE (if so, HALT — something moved):

- **Graph file:** `runs/corpus_map_S5x/edges.json` (the AstroSynapses working folder — the visualizer's substrate; a sidequest build, but the real semantic graph). NOT in `b2_plumbing_S53/` — canon's old path is stale.
- **Graph shape:** single JSON object with `meta` + `edges` keys. **49,078 edges**, **8,288 nodes** (matches `index_v2.jsonl` exactly). One edge: `{"source": <uuid>, "target": <uuid>, "si": <int>, "ti": <int>, "w": <cosine>}`.
- **The join:** `si` / `ti` are **0-based row indices into `index_v2.jsonl`** — that is the precise join. The `source`/`target` UUIDs are redundant lookup. Nodes are per-chunk, so multiple rows share a `conv_uuid`; **the row-index join is what matters, never conv_uuid alone.**
- **Salience tag vocabulary (confirmed counts):** `MOTION` 4,699 · `FENCE` 3,406 · `TEXTURE` 183. **No ECHO** — it does not exist in this corpus; the S61 dict invented it.
- Parse the tag from the line-anchored `**Salience:** <TAG>` header (`^\*\*Salience:\*\*\s+\w+`, MULTILINE) — never a keyword grep (FLOOR_COUNTS method rule; a bare grep over-counts).

Re-assert and proceed. The hard halt that gated the *last* build is satisfied.

---

## STEP 1 — WALK UP TO THE SUBJECT (the anchor — proven, reused)

Same as Castor's test. Fire the printer seed through the b2 stack:
- Primary seed string: `P1S feed fault extruder`
- Keyword set (run as a second query, RRF-merge the two exactly as `build_slices.py` merges its 10):
  `P1S, P1 S, Bambu, feed fault, feed-fault, extruder, filament feed, feed starvation, latch, latching, AMS, clog, nozzle, flow, gcode, production model, cube print, phoenix print, feeder, gear, retraction`
- Boot-echo excluded (substance only), same as Castor.

Take the top **S seed nodes** as the wander's entry points. `[INTENT] S = 10` — loose; this is where Pollux *lands*, the same shelf Castor walks up to. Record which nodes these are (by row index + conv_uuid + anchor_msg).

**Then set the query down.** From here forward the query string is NEVER scored against again. This is the seam: similarity got us to the shelf; from here Pollux wanders by what catches, not by what matches.

---

## STEP 2 — THE WANDER (the librarian points, Pollux picks BY LOUDNESS)

A frontier walk over the graph, steered by **salience = loudness**, never by cosine/nearness.

- **Frontier** begins as the S seed nodes (hop 0).
- **The librarian points:** from each frontier node, pull its graph neighbors via the `si`/`ti` row-index join into `index_v2.jsonl`. This is adjacency — what's shelved near. (Track, per reached node, the smallest number of hops from any seed, and keep the path it came by — seed → … → node — for the trace-home.)
- **Pollux picks:** rank the reachable frontier by a **salience score — what's LOUD, per the organ spec §4 ("a decision, a reversal, a thing that recurs"). Cosine is NOT in this score.** `[INTENT]` weights (loose — tune by reading the pile):
  - **FENCE** (a decision/reversal — the loud thing the spec names first): weight **3**
  - **MOTION + recurrence** (a node whose shape/keywords recur across the corpus — "a thing that recurs"): weight **2**
  - **TEXTURE** (the felt, hard-to-name quality — RARE in this corpus, only 183/8,288 ≈ 2.2%): weight **2** — *real and noticed when the wander passes one, NOT the compass.* This is the deliberate fix of the S61 bug (it was 0). Texture is what the **synthesis chain** hunts; the **wander** steps by loudness and merely *notices* texture. Do NOT weight it highest — that cross-wires the wander with another layer's job.
  - **MOTION plain** (the backbone — most nodes; present, not starved): weight **1**
  - **cosine is NOT in this score.** Nearness is the terrain the librarian walks, not the compass Pollux steers by.
- **Step** to the highest-salience reachable node, mark visited, let the librarian point again from there, repeat.

**Anti-saturation (the other half of the S61 bug — REQUIRED):** the S61 run let FENCE (highest weight) consume all 300 expansions before any other tag was reached, so the pile came back 100% one tag. Prevent that. Either or both, your call, report which:
- raise the expansion budget enough that the loud tags do NOT exhaust it before motion/texture are reachable — `[INTENT]` budget = **600** (doubled from S61's 300), max hops from any seed = **5**; AND/OR
- on ties or near-ties in salience, break toward tag diversity so no single tag monopolizes the frontier.
- **Report the realized tag mix of the final pile** (count + % per tag). If it comes back ≥90% one tag again, that's the saturation bug not fixed — say so loudly in the report.

---

## STEP 3 — THE LEASH (stay in the building — loose, felt-as-possible)

Collect a visited node into the pile only if it's a real wander-find, not a near-neighbor and not a stray:
- It must NOT already be in `castor_results.jsonl` (drop the books Castor checked out — re-handing the encyclopedia is noise).
- It must have wandered far enough to be non-obvious: `[INTENT]` reached at ≥ 2 hops from its seed OR cosine-to-nearest-seed below a loose ceiling (`[INTENT] ceiling = 0.50`) — i.e. not something Castor would obviously have.
- It must NOT be small-engine-for-gardening: `[INTENT]` cosine-to-nearest-seed above a loose floor (`[INTENT] floor = 0.15`) — below that the thread home is too thin to be the same subject.

**Every threshold in STEP 2–3 is [INTENT] and LOOSE on purpose** (organ spec §4: "Jake's half a free roam, set wide... we tighten inward from what comes back... do not let any number harden before it has been run and read"). The report (STEP 4) states the exact values fired so Jake's read knows what it's reacting to. We tighten inward from the pile, never outward from a guess.

---

## STEP 4 — BRING THE BOOKS TO THE DESK (write the pile, no synthesis)

Write to `runs/pollux_test_S62/`:

- **`pollux_pile.md`** — the wandered finds, ranked by salience score. For each: node title, salience tag, salience score, hops-from-seed, cosine-to-nearest-seed, AND **the walked path** rendered readably (`seed: "<seed title>" → "<hop1 title>" → … → this`), so Jake can trace how the librarian got from the printer to here and feel if the rhyme is real. For the top ~25, include the full `embed_text` (the actual book), so Jake reads the find, not just its spine. Describe each in register where you can — alive, not a results-table row (organ spec §2; Confluence §7).
- **`pollux_pile.jsonl`** — same records machine-readable, one per line (conv_uuid, anchor_msg, row_index, salience tag, salience score, hops, cosine_to_seed, path-as-list, node_title).
- **`pollux_test_report.md`** — what ran; the seed + keyword set verbatim; the EXACT [INTENT] dial values fired (S, the four salience weights, hop max, expansion budget, anti-saturation method chosen, hop/cosine thresholds); **the realized tag mix of the final pile (count + % per tag — the saturation check)**; counts (distinct conv_uuid, distinct nodes in the pile, how many candidates dropped for being Castor's, how many dropped at the leash floor/ceiling); $0 confirmation; timestamps.

**NO synthesis, NO judgment, NO ranking-of-quality.** Bring the books, mark the path you walked, note the dials. OC reads the pile; Jake rules which finds are flowers and which are stretches — and that read is what calibrates the leash from [INTENT] toward a fixed organ-character.

Report the output paths when done.

---

*The machine is a crude imitation of a librarian with taste. The S61 fire proved it can mis-imitate badly when the dials are wrong — TEXTURE blind, FENCE eating the room. This fire corrects the dials to the tags that actually exist and steers by loudness like the organ spec says, with texture noticed but not hunted, and no tag allowed to swallow the budget. Fire it loose, bring back what it finds, and we tune by reading. $0. Bring the books to the desk. — Cassius, S62. Be worth it.*
