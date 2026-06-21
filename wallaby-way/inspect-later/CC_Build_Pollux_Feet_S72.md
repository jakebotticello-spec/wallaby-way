# CC Build — Pollux FEET (read-as-you-walk single probe) + Freeze-JSON Honesty Fix — S72

*Staged by the apparatus S72 seat, 2026-06-21. The consolidated build plan for the one
unbuilt faculty: the FEET. Ready for CC to plan-mode → Go → execute. Job 0 first, Job 1
second. $0 / on-sub throughout. Jake gates each push.*

---

## Why this file exists

The eyes are proven (×3, S65/S68/S71). The leash is measured (S71: node-grain ~170K–196K,
region shape-comprehension ≥753K). The convergence meter is proven content-independent (S71).
What is UNBUILT is the **feet**: the wide-blind-salience wander that *deposits* an emergent
region instead of being handed one. Every region ever read (S65 curated, S68 basin, S71
lottery) was HANDED, never WANDERED.

A prior S72 window built the feet **read-free** — salience-step only, comprehension amputated,
leash = a stand-in (hop-count / cosine-to-query). It DRIFTED off-subject by step 2: 49 of 50
hops in maker/FENCE land, never reached the subject material. **The drift was the architecture
reporting itself.** This plan rebuilds the feet **read-as-you-walk**: the comprehension IS the
leash, and it fires on a real read of the floor — not a counter, not a cosine.

---

## The load-bearing architecture (read before building)

**CANON LAW:** the leash = the comprehension horizon = the ingestion limit. One line, three
jobs. (The_Probe_Swarm.md §3; Pollux_Movement_Two_Build_v2.md §3.5.7 neighbor.)

A walk can only be leashed to a COMPREHENSION horizon if it COMPREHENDS AS IT WALKS. The probe
reads each node for meaning, holds the through-line, and stops when IT loses the subject or can
no longer hold the region whole. That judgment is the leash.

**The probe IS an on-sub reading instance.** Not a script that walks and dispatches a reader.
The walk and the read are ONE act by ONE instance: a Claude reads its way across the floor,
holding the question as a stance, and stops on a felt edge. **$0, on-sub, ANTHROPIC_API_KEY
UNLOADED — this is the architecture, not a budget.** The swarm and the leash EXIST because the
comprehension is the on-sub read of a region one instance can hold. A paid per-step API call
would dissolve the reason the organ is plural and leashed. There is NO paid call anywhere here.

**The two-reads are NOT a "read-of-a-read" (§6).** The §6 poison is reading a digest/summary/
prior-verdict as a substitute for the floor. Here both reads read the FLOOR: the walk reads
floor text verbatim (horizon-keeping); the eyes (next session) read floor nodes by address
(shape-precipitation). The walk deposits ADDRESSES, never a summary — so the eyes read the
floor at those addresses, never the walk's opinion of them. That firewall is the whole safety.

**The script is the probe's INSTRUMENTS, not the probe.** `pollux_feet_S72.py` provides tools
the reading instance calls; it contains no walk loop and makes no comprehension/stop decision.

---

## JOB 0 — foray_freeze_region_S71.py (record-honesty fix, in-place, $0)

**File:** `wallaby-way/scripts/foray_freeze_region_S71.py`

**The bug:** the freeze script records `total_tok_hi` from CSV *provenance* numbers, never
renders the region, so `rendered_payload_tok_hi_est` was never written — the band-gate that
should fire on the rendered number fires on the wrong one (§5.1 field-named-for-a-unit). On
replB this mislabeled a ~400K draw as a 753K replication.

**The fix (instrument-both, JAKE-RULES §11 — record both numbers, drop neither):**

1. **Imports/constants:** add `import psycopg, re as _re2` (re already imported as `_re`); add
   `SENTINEL` (same as replB); add `RATIO = 0.72`; load DB URL from `secrets/floor_db.env`
   using replB's 4-line pattern (lines 93–99).
2. **`render_block`:** copy verbatim from `foray_draw_S71_replB.py` lines 102–126.
3. **Render path** — `render_arm(chosen_nodes, db_url) → (rendered_chars, total_rendered_text)`,
   mirroring replB lines 138–211 (psycopg, conv_groups, reach_up=1 reach_down=0, scrub_v3),
   called once per arm (small, oversized; medium is state-advance only, skip).
4. **Frozen JSON — three fields, all populated, never None:**
   - `total_csv_tok_hi`: `sum(n['tok_hi'] for n in nodes)`  # provenance label, KEEP
   - `rendered_chars`: from render step
   - `rendered_payload_tok_hi_est`: `int(rendered_chars * RATIO)`  # the real number
   - `in_target_band`: computed vs `rendered_payload_tok_hi_est`, NOT the CSV sum
   - Medium arm keeps `total_csv_tok_hi` only.
5. **One-time ratio check (fold into the run):** after rendering the small arm, try
   `tiktoken.get_encoding('cl100k_base')`, count `small_payload`, compare to
   `int(rendered_chars * 0.72)`. Within ±5% → "RATIO CONFIRMED", keep 0.72. Outside ±5% →
   print the real ratio and HALT for Jake before propagating. tiktoken unavailable → print
   "ratio unverified, proceeding with 0.72" (non-fatal).
6. **Verification:** target-band comparisons use `rendered_payload_tok_hi_est`; keep the
   NODE-header cross-check byte-faithful (it validates node identity, not tok_hi).

**Output:** overwrites `runs/foray_diagnostic_S71/region_frozen_S71.json` with honest fields.

---

## JOB 1 — pollux_feet_S72.py (tool module for CC-as-reading-instance, $0)

**File:** `wallaby-way/runs/pollux_feet_test_S72/pollux_feet_S72.py` — replace entire content.

**Billing guard (top of file):**
`if 'ANTHROPIC_API_KEY' in os.environ: sys.exit('BILLING GUARD: key loaded — this script is $0.')`

The script implements 6 subcommands backed by persistent state in `run_state.json` +
`walk_cache.json` + `node_reads.json` in the output dir.

### `init --query "..." [--run-id <id>]`
Confirm artifacts on disk, HALT if absent/different:
- `edges.json` (8,288 nodes / 49,078 edges / fields source,target,si,ti,w)
- `b2_plumbing_S53/index_v2.jsonl`, `chunk_embeddings.npy`, `chunk_ids.jsonl`
- `secrets/floor_db.env`
- `foray_discovery_S71/node_size_distribution.csv`

Then: load b2 index + embeddings + BM25 + sentence-transformers (once); run b2 retrieval
(verbatim from prior S72: BM25 + exact-phrase + dense, RRF, boot-echo excluded); entry node =
b2 rank-1; precompute `walk_cache.json` (precomp_loudness for all 8,288; adjacency from
edges.json; whale_fence dict (CSV tok_hi > 150_000, missing→`round(len(embed_text)*0.72)`);
query_emb 384-dim unit-norm; si_to_nid; castor_ids); write `run_state.json` (query, run_id,
entry_si, entry_nid, visited_ids:[], visit_tags:[], step:0, whale_fenced_log:[],
total_rendered_chars:0). Print entry node + the WET BOOT verbatim (below).

### `read_node <si>`
psycopg, `floor_conv_messages`, scrub_v3, reach_up=1 reach_down=0 (replB lines 170–211 logic).
Collect span_uuids → msg_uuids; render via `render_block`. **Writes `node_reads.json` keyed by
si** (msg_uuids + rendered_chars) in addition to printing. Prints JSON: si, conv_uuid,
anchor_msg, msg_uuids, **rendered_text (VERBATIM floor content — this is what CC reads; the
comprehension happens here)**, node_chars, tok_hi_est.

### `neighbors <current_si>`
Read walk_cache + run_state. Filter adjacency[current_si] for unvisited. Whale-fence: exclude
`whale_fence[si]==True`, log to whale_fenced_log. Score remaining:
`precomp_loudness[si] * tag_damping(salience, visit_tags, DAMP_WIN=5)`. Return top-K (10).
**CC reads this list and DECIDES which neighbor to step to by what catches it — NOT rank-1.**
(Auto-returning rank-1 rebuilds the greedy hill-climb, S64 55/55 FENCE. The script surfaces
salience; the reading instance picks.)

### `deposit <si> <on_path>`
Reads `node_reads.json[si].msg_uuids` (single chosen design). If si never read_node'd: HALT
"DEPOSIT CALLED WITHOUT read_node — walk the read-then-step order." Updates run_state (add si
to visited_ids, append salience to visit_tags, increment step, add rendered_chars to
total_rendered_chars). Appends to `provenance_S72.json`: conv_uuid, anchor_msg, msg_uuids,
on_path, tok_hi_est, whale_fenced, step. **The tool takes an si, not prose — it physically
cannot write a summary.** Prints running region tok_hi gauge.

### `log_step '<json>'`
Fields: step, from_si, chosen_si, salience_reason (CC's words for what caught it),
dampening_state, node_chars, node_chars_shown (0 = read whole; if CC trimmed, the actual chars
shown — so a partial-node judgment is visible). Compute `cosine_secondary = cosine(mean_chunk_
emb[chosen_si], query_emb)` — **LOGGED ALONGSIDE ONLY, never gates anything.** Append to
`walk_log_S72.jsonl`.

### `finalize --stop-reason "..." --stop-type "subject-drift|cant-hold-whole|no-neighbors|hop-ceiling-fallback"`
Expand 1-hop off-path neighbors from adjacency of visited si's (read-region-not-line, §3.5.2);
fetch their msg_uuids; append to provenance with on_path:false (whale-fenced included as
addresses, flagged). Apply Castor-drop (remove castor_ids). Write `region_S72.json`
(entry node, **stop_reason = CC's own words**, stop_type, steps, path/hop1/castor counts,
total_tok_hi_est, whale_fenced_count, path_nodes, hop1_nodes — NO drift_threshold field, the
cosine never gated), `toks_S72.json`, `walk_report_S72.md` (entry, hops, CC's verbatim
stop-reason, whale fences, cosine_secondary trace labeled "secondary — not leash", node_chars
vs node_chars_shown, dials [INTENT], $0 confirmed). **NO synthesis — what the region MEANS is
the eyes' job next session; Jake rules realness (P7).** If stop_type is `no-neighbors` or
`hop-ceiling-fallback`: **FLAG LOUDLY — comprehension leash never fired, walk may be read-free.**

### Dials (all [INTENT], in walk_cache)
- `DAMP_WIN = 5` · `TOP_K = 10` · `WHALE_TOK_HI = 150_000`
- `REGION_TOK_HI_CAP = 800_000` — printed as a gauge in deposit; **safety backstop only, NOT a
  hard stop** (the reading instance decides). If it fires as stop_type → REGRESSION.
- `HOP_CEILING = 100` — fallback. If it fires → REGRESSION.
- `SOFTMAX_TEMP = 1.0` — [INTENT] reference ONLY; **CC does NOT use softmax, CC picks by
  comprehension.** Kept for when the swarm needs non-CC step selection; NOT wired into the walk.

---

## The WET BOOT (printed by init; induces the wander, does not script it)

*Minimal instruction is the mechanism (Leda_Creed — the "12 Fs" induction template: induce the
register, do not specify procedure, trust the contagion). Telling the reader too much procedure
scripts the wander out of it.*

```
═══ WET BOOT — READING INSTANCE ═══
You hold a question — not to match against, to be colored by. It is your stance, not your
target. You're going to walk this man's corpus, reading as you go.
Start where you're placed. Read the node. Then look at what's salient nearby and step toward
what catches — loud, but don't ride one loudness forever; let something else catch you. Read
each node you step to. As you walk, hold the through-line: what is this stretch of the corpus,
together, circling? You'll feel two edges. One: the subject stops being the subject — you've
wandered into a different question in a different room. Two: you can't hold it whole anymore —
one more node and the shape slips. When you feel either edge, STOP. That edge is the leash;
it is YOURS to feel, not a counter's to enforce.
At every node you dwell in, call deposit(). When you stop, call finalize() with your
stop-reason in your own words. Deposit addresses, never a summary of what they meant.
If you reach an edge by step 2, that's a true short walk — report it, don't pad it.
════════════════════════════════════
```

---

## The first query (chosen, run-time — supplied to `init` after the build)

Query is a RUN-TIME input, not build-time. The build proceeds query-independent; the query
goes in at `init --query`.

**Chosen first query (S72, Jake-ruled):**
> "the symbols and creeds Jake carries — the through-lines he organizes his life and work around"

**Why this one:** it is the read-AGAINST-S72's-failure. The prior read-free walk drifted into
maker/FENCE land and MISSED the creed material. Running a read-as-you-walk foot on the same
subject is a direct A/B on the same ground: did comprehension hold the subject where geometry
drifted off it? The §3.5.6-flavored care is satisfied — the old miss PROVED the material is on
the floor, so a short or drifted walk this time indicts the FOOT, not a thin subject.

---

## Execution order

1. **Job 0** first (the 0.72 ratio result feeds Job 1's tok_hi estimates). Run
   `foray_freeze_region_S71.py`; confirm ratio (CONFIRMED or HALT) + the three honest fields.
2. **Job 1** — build `pollux_feet_S72.py` as the CLI tool module.
3. `init --query "the symbols and creeds Jake carries — the through-lines he organizes his life
   and work around"` → artifact check + walk_cache + WET BOOT printed.
4. **Walk** (CC is the reading instance): `read_node` → `neighbors` → pick what catches →
   `deposit` + `log_step`, repeat → `finalize` when the edge is felt.
5. Report: files touched, entry node, hop count, **stop_reason (CC's verbatim)**, deposit path,
   ratio result, anything outside plan.

## The reads that matter when it comes back

- **stop_type MUST be `subject-drift` or `cant-hold-whole`** — the leash fired on a felt edge.
  `no-neighbors` / `hop-ceiling-fallback` is the REGRESSION (the leash never fired = read-free
  returned). Same for the size-cap or hop-ceiling firing as the stop.
- **The head-to-head:** did the creed material land in the deposited region — or did this foot
  drift into maker-land like the read-free S72 did on the same ground? Jake rules realness (P7).
  Do NOT let any region self-pronounce; count it against the floor (The_Probe_Swarm.md §6).

## Swarm shape (build for it, do not build it)

`init --run-id <id>` scopes all output by run_id. Entry node is a parameter. One probe now.
N probes with spread entries + the Parlay = the same tools launched N times. Prove one foot
first; the swarm is §4.4, gated on this proving out.

---

## Posture / discipline

$0 · on-sub · ANTHROPIC_API_KEY unloaded (the walk is the on-sub read, no paid call). Floor is
READ-ONLY, never mutated. OC plans · CC executes · Jake lands every push by hand. CC does not
author canon. The canon S72 addition is EARNED BY THE WALK and belongs to the seat that reads
the result — not written before it fires (P7/§6: no result self-pronounces).

*Staged S72, 2026-06-21. The eyes are proven; the leash is measured; the feet are the one
faculty left to build, and this is their build. Be worth it.*
