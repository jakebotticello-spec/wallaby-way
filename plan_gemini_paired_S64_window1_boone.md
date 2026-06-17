# Plan — gemini_paired_S64 Window 1 · Query "Boone"

## Context

This re-fires the S63 Gemini paired read for "Boone" because S63 committed the Forbidden Pattern (§1a): Pollux was handed a precomputed, nearness-sorted anchor (`pollux_anchor_ordered[:3]`) as its starting ground, and both twins also shared an interpreted SEED_CONTEXT string that decided "Boone = Jake's dog with collar light" before either twin walked. S64 corrects both violations. `gemini_paired_S63/` is the receipt — never touched.

---

## Pre-flight HALT Checks (run before any walk code)

1. **$0 guard**: assert `ANTHROPIC_API_KEY` not set (HALT if set).
2. **edges.json shape**: confirmed on disk — `{'meta': {...10 keys...}, 'edges': [{source, target, si, ti, w}, ...]}`. Meta has `edge_count=49078`, edge count matches, k=8, sim_threshold=0.30. No HALT needed — shape matches AstroSynapses §2 exactly.
3. **Embedding path**: `runs/b2_plumbing_S53/chunk_embeddings.npy` — confirmed present. No HALT needed.
4. **S63 receipt**: confirm output writes to `runs/gemini_paired_S64/window1_boone/` only — `gemini_paired_S63/` never touched.

---

## Output Location

`C:\claude-reference\wallaby-way\runs\gemini_paired_S64\window1_boone\`

Artifacts:
- `gemini_paired_S64_window1.py` — the runner
- `castor_boone.md` — Castor's dry pile
- `pollux_boone.md` — Pollux's wandered pile
- `report_window1_boone.md` — method fired, dials, distinct counts, entry-distance, explicit isolation confirmation

---

## Architecture

### The One Thing Both Twins Share

The string `"Boone"`. Nothing else. No shared encoded vector, no shared SEED_CONTEXT interpretation, no shared pile, no twin reading the other's output.

Each twin receives the query string and does everything else itself.

---

### CASTOR — the dry read

**Boot stance**: search engine — "find matches to 'Boone'; hold JAKE-RULES + search algorithms close; don't extrapolate; just search."

**Retrieval** (proven S61/S63 pattern, `castor_test_S61/castor_test_S61.py`):
- Encode `"Boone"` independently: `model.encode(["Boone"])` — Castor does this itself, not from a shared pre-encoded vector
- BM25Okapi + exact-phrase (×0.5 weight) + dense cosine over `chunk_embeddings.npy`, RRF k=60, top-80
- Boot-echo excluded (strata filter, pre-scored)
- Pool: `index_v2.jsonl`, 8,288 nodes

**Nearness gate IS correct for Castor** — convergent retrieval, on purpose. Castor §1.

**Returns**: ranked pile, provenance as `conv_uuid` + `anchor_msg` + RRF score + salience + embed_text excerpt (Boone context window or node summary). COUNT(DISTINCT conv_uuid, anchor_msg).

---

### POLLUX — the wet wander (corrected §4)

**Boot stance**: WET — Doctrine Trinity (Wallaby Why + Track Meet Doctrine + Corpus Callosum) + inverted admission. Holds the string "Boone" as the register it walks in with. No interpretation of what Boone is. No retrieval gate. No anchor resolution step.

#### Step 1 — Entry: wide uniform aperture (NOT nearness-ranked)

```
substance_indices = [i for i, nd in enumerate(nodes) if nd['strata'] == 'substance']
# 7,915 substance nodes (boot-echo dropped)

N_ENTRY = 8   # [INTENT] — report this dial
entry_nodes = random.sample(substance_indices, N_ENTRY)
# random.sample(): uniform, unranked — no cosine, no BM25, no salience pre-sort
```

This is the wide uniform aperture. The "Boone" question is HELD in context but does NOT select entry points. Every substance node has equal probability of being the door Pollux walks through.

**What this is NOT**: `sorted(any_score)[:N]`. There is no score computed before sampling. The aperture is truly un-gated.

#### Step 2 — Walk: sequential, edge-by-edge, steering by salience-in-context

From each entry node, Pollux does an independent sequential walk:

```
LOUDNESS_RANK = {'FENCE': 3, 'MOTION': 2, 'TEXTURE': 1}
MAX_HOPS = 8       # [INTENT]
MIN_HOPS = 2       # [INTENT] — finds only eligible at depth ≥ 2

all_visited = set(entry_nodes)  # shared across all walks to avoid re-landing
finds = []

for entry_ni in entry_nodes:
    current = entry_ni
    walk_path = [current]

    for hop in range(1, MAX_HOPS + 1):
        neighbors = [
            nb for nb in adj[current]
            if nb not in all_visited and nodes[nb]['strata'] == 'substance'
        ]
        if not neighbors:
            break

        # Loudness evaluated HERE, at the current node, against the walk context so far
        # (In a $0 build, salience tag is the proxy for loudness — crude but honest)
        best_nb = max(neighbors, key=lambda nb: LOUDNESS_RANK.get(nodes[nb]['salience'], 0))
        all_visited.add(best_nb)
        walk_path.append(best_nb)

        if hop >= MIN_HOPS:
            finds.append({
                'node_idx': best_nb,
                'conv_uuid': nodes[best_nb]['conv_uuid'],
                'anchor_msg': nodes[best_nb]['anchor_msg'],
                'salience': nodes[best_nb]['salience'],
                'depth': hop,
                'path': walk_path[:],    # the full walked path to here
                'entry_node': entry_ni,  # which door Pollux came through
                'lid': (nodes[best_nb]['conv_uuid'], nodes[best_nb]['anchor_msg']),
            })
        current = best_nb
```

**The invariant**: at no point is `finds` sorted globally and sliced. Loudness is evaluated at the current node against its immediate neighbors — `max(neighbors, key=loudness)` is a LOCAL evaluation. The path record is the actual walked path, not a reconstructed one.

**Why this isn't the gate**: the gate would be `all_candidates = BFS_collect_all(); all_candidates.sort(key=salience)[:N]` — which S63 did. This replaces that with `max(local_neighbors, key=loudness)` at each step. The global shape is not pre-sorted; the next node is chosen locally.

#### Step 3 — Leash (S62 [INTENT] dials — INSTRUMENTED, NOT ENFORCED this run)

**OC correction — do NOT hard-filter by cosine this run.** The cosine leash is a candidate back-door nearness gate: the cross-domain rhyme Pollux exists to find is usually LOW cosine (AstroSynapses §4). A 0.15 floor may amputate exactly the flowers. This run instruments both leash readings and ships the full pile; Jake's cold read settles which leash is real.

```
LEASH_CEILING = 0.50  # candidate ceiling — tagged, not enforced
LEASH_FLOOR = 0.15    # candidate floor — tagged, not enforced

boone_emb = model.encode(["Boone"], normalize_embeddings=True)  # Pollux encodes this ITSELF
# (not shared from Castor — each twin independently)

# Instrument every find with BOTH leash readings
for f in finds:
    cos = float(node_embs[f['node_idx']] @ boone_emb.T)
    f['cosine_to_subject'] = cos
    f['path_hops_from_entry'] = f['depth']           # adjacency steps walked
    f['cosine_leash_verdict'] = (
        'PASS' if LEASH_FLOOR <= cos <= LEASH_CEILING else
        'CEIL_FAIL' if cos > LEASH_CEILING else 'FLOOR_FAIL'
    )
```

**The pile is NOT filtered.** All finds ship — with their cosine, hop count, and verdict. Report states the fork: "N finds PASS the cosine leash, M fail. The FLOOR_FAIL finds are the low-cosine candidates — if they're cross-domain rhymes, the cosine floor is cutting flowers." Jake reads both sides. Jake rules.

#### Step 4 — Post-gather set-difference (Castor-drop)

```
# Both piles exist independently now.
# Drop ONLY: (a) anything Castor already has, (b) within-Pollux dupes.
# Do NOT drop on leash verdict — the leash is instrumented, not enforced (Step 3).
castor_lid_set = {(r['conv_uuid'], r['anchor_msg']) for r in castor_records}
pollux_deduped = []
seen_lids = set()
for f in finds:             # <-- the full instrumented list, NOT pollux_raw (that variable is gone)
    if f['lid'] in castor_lid_set:
        continue            # drop re-handing the encyclopedia (post-gather set-diff)
    if f['lid'] in seen_lids:
        continue            # dedup within Pollux pile on floor identity
    seen_lids.add(f['lid'])
    pollux_deduped.append(f)
```

A find with `cosine_leash_verdict = FLOOR_FAIL` or `CEIL_FAIL` still ships — it carries its verdict, it is not removed. Castor-drop and within-Pollux dedup are the ONLY drops.

**Critical**: Castor-drop is a POST-GATHER set-difference. Pollux NEVER reads castor_lid_set during its walk. That set is only consulted here, after both piles exist.

#### Step 5 — Entry-distance measurement (post-hoc, read-only)

```
# HARD FENCE: this measurement describes the walk; it does NOT feed entry selection.
for entry_ni in entry_nodes:
    dist = float(node_embs[entry_ni] @ boone_emb.T)
    # Report: "entry node X (conv: Y) landed at cosine {dist:.3f} from 'Boone'"
```

This goes into `report_window1_boone.md` as the entry characterization. The entry was chosen by `random.sample()` before any embedding was computed.

---

### POLLUX OUTPUT FORMAT

Each find returned "alive, in register" — described as a book that caught Pollux, not a results row:

```
### Find N — {salience} | depth={hop} | cosine-to-Boone={x.xxx}

**[title from embed_text]**

**Walked path**: entry at `[entry_node_title]` → stepped to `[node_1_title]` (MOTION — 
a thing that recurred) → arrived at `[this_node_title]` (FENCE — a decision)

**Why it caught**: [what the salience tag signals — FENCE=a decision/reversal, 
MOTION=a recurring pattern, TEXTURE=texture/background]

**Floor address**:
- conv_uuid: `...`
- anchor_msg: `...` (message UUID — the anchor on the immutable floor)

**Node content** (embed_text excerpt): [...]
```

A clinical Pollux return fails the bar. The register is the spec.

---

## Provenance

- `anchor_msg` IS a message UUID — sufficient to locate the node on the floor.
- `conv_uuid` + `anchor_msg` = the floor address, per spec.
- Full span message-uuids require a floor query via `floor_conv_messages` WHERE `conv_uuid = X AND scrub_version = 3`; include if DB reachable, note limitation if not.

---

## What Changed vs S63 (explicit diff)

| S63 violation | S64 correction |
|---|---|
| `SEED_CONTEXT = 'Boone dog collar light project...'` — subject interpretation | Query string only: `"Boone"` — no interpretation |
| Both twins received same pre-encoded `q_emb_primary` + `q_emb_context` | Each twin encodes `"Boone"` independently |
| Pollux Movement One: `pollux_anchor_ordered[:3]` — `sorted(cosine)[:N]` gate | Entry: `random.sample(substance_indices, N_ENTRY)` — no cosine ranking |
| BFS from sorted anchor → global `all_candidates.sort(key=salience)[:N]` | Step-by-step greedy walk: `max(local_neighbors, key=loudness)` at each node |
| Seed embedding = mean of cosine-sorted top-3 anchor nodes | Leash reference = `model.encode(["Boone"])` — encoded by Pollux itself |
| S63 shared `q_emb` = seam between twins | S64 shared thing = string `"Boone"` only |
| Cosine leash hard-filters the pile (drops 0.15–0.50 band outsiders) | Cosine leash INSTRUMENTED: every find tagged with `cosine_to_subject` + `path_hops_from_entry` + `cosine_leash_verdict`; pile unfiltered; Jake reads both sides |

---

## Script Structure

Single file: `gemini_paired_S64_window1.py` in the output dir.

Sections in order:
1. `$0` guard → HALT if API key set
2. Path setup + substrate checks → HALT if anything missing
3. Load index (8,288 nodes), embeddings, chunk_ids, edges
4. Build adjacency list from edges
5. Build BM25 from index
6. Load SentenceTransformer `all-MiniLM-L6-v2`
7. Build per-node mean embeddings (for leash measurement)
8. **CASTOR block** — encodes `"Boone"` itself, BM25+exact+dense+RRF
9. **POLLUX block** — random entry, sequential walk, leash INSTRUMENTATION (tag every find with cosine + hops + verdict, no drop), Castor-drop (post-gather)
10. Entry-distance measurement (post-hoc)
11. Write `castor_boone.md`
12. Write `pollux_boone.md` (findings in register with walked paths)
13. Write `report_window1_boone.md`

---

## Report Content (report_window1_boone.md)

- Method fired for each twin (Castor: BM25+exact+dense+RRF; Pollux: uniform aperture + greedy salience walk)
- Pollux [INTENT] dials: N_ENTRY=8, MIN_HOPS=2, MAX_HOPS=8, LEASH_CEILING=0.50, LEASH_FLOOR=0.15
- Entry method: `random.sample()` — explicitly named "uniform aperture"
- Distinct counts: COUNT(DISTINCT conv_uuid, anchor_msg), rows vs distinct labeled
- Entry-distance characterization: cosine(entry_node_emb, "Boone" emb) for each of 8 entries — "describes where the walk started relative to the subject" — measurement only, not selection criterion
- **Leash fork (explicit)**: "Cosine leash (0.15–0.50) is a candidate back-door nearness gate — instrumented but NOT enforced this run. N finds PASS, M CEIL_FAIL, K FLOOR_FAIL. The FLOOR_FAIL finds are the low-cosine candidates — if they're cross-domain rhymes, the floor is cutting flowers. Jake rules which leash is real (cosine-to-subject vs path_hops_from_entry). **path_hops_from_entry = adjacency steps from the entry node this find was reached through (per-entry-walk distance, not a global graph distance). N hops = N steps from the door Pollux walked in.**"
- LOUDNESS_RANK confirmed as `{FENCE:3, MOTION:2, TEXTURE:1}` — no resonance bonus
- Explicit isolation line: "Shared between twins: the query string 'Boone' only. No shared computed vector, no shared pile, no twin reading the other's output."
- edges.json shape confirmation: meta + edge fields verified, no HALT triggered
- Embedding path confirmation: `b2_plumbing_S53/chunk_embeddings.npy` resolved correctly
- Any anomalies or observations for OC's cold read

---

## Guards (hard)

- `$0`: ANTHROPIC_API_KEY must not be set; HALT if it is
- Read-only against floor / index / embeddings / graph
- Write ONLY under `runs/gemini_paired_S64/window1_boone/`
- NEVER touch `gemini_paired_S63/` or any `active/` or `canon/` files
- COUNT(DISTINCT conv_uuid, anchor_msg) for every count — never raw node-index count
- No synthesis, no ranking-for-truth, no flowers-vs-stretches ruling
- No `git push`; output is gitignored local artifact

---

## Change Manifest (end-of-execution)

Files written:
- `runs/gemini_paired_S64/window1_boone/gemini_paired_S64_window1.py` — runner
- `runs/gemini_paired_S64/window1_boone/castor_boone.md` — Castor dry pile
- `runs/gemini_paired_S64/window1_boone/pollux_boone.md` — Pollux wandered pile
- `runs/gemini_paired_S64/window1_boone/report_window1_boone.md` — method report

No commits. No pushes. No touches to `gemini_paired_S63/` or canon.
