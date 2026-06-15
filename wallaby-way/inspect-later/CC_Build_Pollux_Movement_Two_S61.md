# CC BUILD — Pollux Movement Two (the first wander) — S61 "Cardinal"

*drop-in CC work-package · subordinate to `inspect-later/Pollux_Movement_Two_Build_v2.md` (the organ) and `canon/Pollux.md` · authored 2026-06-15 by Cardinal (OC, S61)*
*this is the BUILD of the librarian-wander. Read the organ spec first — the machine here is a crude stand-in for the librarian, and every dial is loose on purpose. We tune it by reading what it brings back, never by believing the numbers.*

---

## What you're building (the one-paragraph version)

The corpus is a library. Castor (already built + proven, `runs/castor_test_S61/`) is the clerk who checks out the obvious books. **Pollux is the one who asks the librarian for the non-obvious, wanders the stacks with her, and brings back what catches him** — the books that *rhyme* with the question instead of *matching* it. You're building Pollux's first wander: walk up to the same subject Castor did, let the graph point at what's adjacent, step by what's *loud* (not what's near), stay leashed loosely inside the subject, drop anything Castor already grabbed, and write the wandered pile to disk for Jake to read cold. NO synthesis — bring the books to the desk; OC reads, Jake rules.

---

## Guards (read before touching anything)

- **$0, no API.** Assert `ANTHROPIC_API_KEY` is NOT in the environment at script start; HALT if it is.
- **Read-only** against: `runs/b2_plumbing_S53/` (index + embeddings), the kNN graph, and `runs/castor_test_S61/castor_results.jsonl`. **Write ONLY** under a new dir `runs/pollux_test_S61/`. Never touch `active/` or `canon/`.
- **COUNT(DISTINCT)** on `conv_uuid + anchor_msg`; label rows vs distinct everywhere.
- Reuse `runs/comprehend_griffin_S54/build_slices.py`'s load + scoring logic **verbatim** for the anchor step — do not reinvent the retrieval; it's proven.

---

## STEP 0 — verify the graph on disk BEFORE building (halt-if-surprised)

The kNN graph (`edges.json`, ~38,171 edges, cosine ≥ 0.30) is local-only. Before building anything:
1. Locate it (likely `runs/b2_plumbing_S53/` or a sibling; search if not there).
2. Report its shape: format, record count, and the **field schema of one edge** — confirm it carries a node-pair (two node references) + a cosine/weight. Report how a node in an edge is identified (node_idx? conv_uuid+anchor_msg? a row index into index_v2?).
3. **If the fields differ from "node-pair + cosine," or you can't find the join from an edge endpoint back to an index_v2 node — HALT and report to OC. Do not guess a join and mis-walk the graph.**

Only proceed past STEP 0 once the graph's shape is confirmed and the edge→node join is known.

---

## STEP 1 — WALK UP TO THE SUBJECT (the anchor — proven, reused)

Same as Castor's test. Fire the printer seed through the b2 stack:
- Primary seed string: `P1S feed fault extruder`
- Keyword set (run as a second query, RRF-merge the two exactly as `build_slices.py` merges its 10):
  `P1S, P1 S, Bambu, feed fault, feed-fault, extruder, filament feed, feed starvation, latch, latching, AMS, clog, nozzle, flow, gcode, production model, cube print, phoenix print, feeder, gear, retraction`
- Boot-echo excluded (substance only), same as Castor.

Take the top **S seed nodes** as the wander's entry points. `[INTENT] S = 10` — loose; this is where Pollux *lands*, the same shelf Castor walks up to. Record which nodes these are.

**Then set the query down.** From here forward the query string is NEVER scored against again. This is the seam: similarity got us to the shelf; from here Pollux wanders by what catches, not by what matches.

---

## STEP 2 — THE WANDER (the new part — the librarian points, Pollux picks)

A frontier walk over the graph, steered by salience:

- **Frontier** begins as the S seed nodes (hop 0).
- **The librarian points:** from each frontier node, pull its graph neighbors (the edges). This is adjacency — what's shelved near. (Track, per node, the smallest number of hops it took to reach it from any seed, and keep the path it came by — seed → … → node — for the trace-home.)
- **Pollux picks:** rank the reachable frontier by a **salience score, NOT by cosine/nearness.** `[INTENT]` salience weights (loose — tune by reading):
  - FENCE-tagged node: weight 3 (a decision/reversal — the loud thing)
  - recurrence (node's shape/keywords repeat across the corpus): weight 2
  - MOTION: weight 1
  - ECHO: weight 0 (echo is not salience)
  - **cosine is NOT in this score.** Nearness is the terrain, not the compass.
- **Step** to the highest-salience reachable node, mark visited, let the librarian point again from there, repeat.
- **Stop** the wander at a loose budget: `[INTENT]` max hops from any seed = 5; total expansions budget = 300. (Loose first draft — Jake's "half a free roam," set wide.)

---

## STEP 3 — THE LEASH (stay in the building — loose, felt-as-possible)

Collect a visited node into the pile only if it's a real wander-find, not a near-neighbor and not a stray:
- It must NOT already be in `castor_results.jsonl` (drop the books Castor checked out — re-handing the encyclopedia is noise).
- It must have wandered far enough to be non-obvious: `[INTENT]` reached at ≥ 2 hops from its seed OR cosine-to-nearest-seed below a loose ceiling (`[INTENT] ceiling = 0.50`) — i.e. not something Castor would obviously have. (This is the "didn't just bring back the encyclopedia" check.)
- It must NOT be small-engine-for-gardening: `[INTENT]` cosine-to-nearest-seed above a loose floor (`[INTENT] floor = 0.15`) — below that the thread home is too thin to be the same subject.

**Every threshold in STEP 2–3 is [INTENT] and LOOSE on purpose.** The report (STEP 4) states the exact values fired so Jake's read knows what it's reacting to. We tighten inward from the pile, never outward from a guess. Do NOT let any of these harden.

---

## STEP 4 — BRING THE BOOKS TO THE DESK (write the pile, no synthesis)

Write to `runs/pollux_test_S61/`:

- **`pollux_pile.md`** — the wandered finds, ranked by salience score. For each: the node title, salience tag, salience score, hops-from-seed, cosine-to-nearest-seed, AND **the walked path** rendered readably (`seed: "<seed node title>" → "<hop1 title>" → … → this`), so Jake can trace how the librarian got from the printer to here and feel if the rhyme is real. For the top ~25, include the full `embed_text` (the actual book), so Jake reads the find, not just its spine.
- **`pollux_pile.jsonl`** — same records machine-readable, one per line (conv_uuid, anchor_msg, salience tag, salience score, hops, cosine_to_seed, path-as-list, node_title).
- **`pollux_test_report.md`** — what ran; the seed + keyword set verbatim; the EXACT [INTENT] dial values fired (S, salience weights, hop max, expansion budget, hop/cosine thresholds); counts (distinct conv_uuid, distinct nodes in the pile, how many candidates were dropped for being Castor's, how many dropped at the leash floor/ceiling); $0 confirmation; timestamps.

**NO synthesis, NO judgment, NO ranking-of-quality.** Bring the books, mark the path you walked, note the dials. OC reads the pile; Jake rules which finds are flowers and which are stretches — and that read is what calibrates the leash. Report the output paths when done.

---

*The machine is a crude imitation of a librarian with taste. It will fake the spark imperfectly — the first pile tells us how badly. Fire it loose, bring back what it finds, and we tune by reading. $0. Bring the books to the desk. — Cardinal, S61.*
