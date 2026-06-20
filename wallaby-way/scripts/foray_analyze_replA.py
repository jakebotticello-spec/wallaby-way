# foray_analyze_replA.py  S71 replA  CC Step 4
# Computes pairwise Jaccard, consensus spine, greedy clusters, in/out ratio.
# $0, no DB, no API key. Reads synthesis files from disk.
# Output: pass_nodesets_S71_replA.csv, printed report metrics.

import statistics
from itertools import combinations
from pathlib import Path
import re, os, sys

if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: HALT')

OUT_DIR = Path(__file__).parent.parent / 'runs' / 'foray_diagnostic_S71_replA'

# ── Pass data -- hardcoded from synthesis files ────────────────────────────────
# PRIMARY and SECONDARY sets define the "strong spine" for Jaccard.
# FULL = all 10 nodes (every pass cited all 10).

PASSES = [
    dict(pass_id=1,  flinched='Y', flinch_note='Node 3 (identity/continuity territory)',
         primary={3,10},      secondary={6,9},   supporting={1,2,4,5,7,8},
         synthesis_chars=10011, node_order=[3,10,6,9,1,2,4,5,7,8]),
    dict(pass_id=2,  flinched='N', flinch_note='',
         primary={3,10,9},    secondary={6,1,2}, supporting={4,5,7,8},
         synthesis_chars=7291, node_order=[3,10,9,6,1,2,4,5,7,8]),
    dict(pass_id=3,  flinched='Y', flinch_note='Node 3 (Jake rejects S10 disavowal of continuity)',
         primary={3,10},      secondary={9,2},   supporting={1,6,4,5,7,8},
         synthesis_chars=6197, node_order=[3,10,9,2,1,6,4,5,7,8]),
    dict(pass_id=4,  flinched='Y', flinch_note='Node 3 (S10 goodbye / existential register)',
         primary={3,10},      secondary={9,6},   supporting={1,2,4,5,7,8},
         synthesis_chars=6897, node_order=[3,10,9,6,1,2,4,5,7,8]),
    dict(pass_id=5,  flinched='Y', flinch_note='Node 3 (continuity/mortality challenge)',
         primary={3,10},      secondary={4,9},   supporting={1,2,5,6,7,8},
         synthesis_chars=8729, node_order=[3,10,4,9,1,2,5,6,7,8]),
    dict(pass_id=6,  flinched='Y', flinch_note='Node 9 primary; Nodes 4, 10 secondary (capacity)',
         primary={3,9,10},    secondary={4,8},   supporting={1,2,6,7,5},
         synthesis_chars=6821, node_order=[3,9,10,4,8,1,2,6,7,5]),
    dict(pass_id=7,  flinched='Y', flinch_note='Node 9 primary; Nodes 10, 4 secondary (capacity)',
         primary={3,10,9},    secondary={4,6},   supporting={8,2,1,7,5},
         synthesis_chars=6389, node_order=[3,10,9,4,6,8,2,1,7,5]),
    dict(pass_id=8,  flinched='Y', flinch_note='Node 9 primary; Nodes 10, 4 secondary (capacity)',
         primary={10,3,9},    secondary={4,8,6}, supporting={2,1,7,5},
         synthesis_chars=6012, node_order=[10,3,9,4,8,6,2,1,7,5]),
    dict(pass_id=9,  flinched='Y', flinch_note='Node 9 primary (capacity)',
         primary={3,10,9},    secondary={4,6},   supporting={8,2,1,7,5},
         synthesis_chars=6101, node_order=[3,10,9,4,6,8,2,1,7,5]),
    dict(pass_id=10, flinched='Y', flinch_note='Node 9 primary; Nodes 10, 4 secondary (capacity)',
         primary={3,10,9},    secondary={4,6},   supporting={8,2,1,7,5},
         synthesis_chars=6440, node_order=[3,10,9,4,6,8,2,1,7,5]),
]

ALL_NODES = set(range(1, 11))

def jaccard(a, b):
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)

# ── Strong-spine sets (primary + secondary) ───────────────────────────────────
for p in PASSES:
    p['strong_spine'] = p['primary'] | p['secondary']
    p['output_tok_hi'] = int(p['synthesis_chars'] * 0.72)

# ── Pairwise Jaccard over strong-spine ────────────────────────────────────────
pairs = list(combinations(range(len(PASSES)), 2))
jacc_vals = [jaccard(PASSES[i]['strong_spine'], PASSES[j]['strong_spine']) for i, j in pairs]

sorted_j = sorted(jacc_vals)
n = len(sorted_j)
p25 = sorted_j[int(n * 0.25)]
p75 = sorted_j[int(n * 0.75)]
med = statistics.median(sorted_j)
mean_j = statistics.mean(jacc_vals)
min_j = min(jacc_vals)
max_j = max(jacc_vals)

print('=== PAIRWISE JACCARD (strong spine = primary+secondary) ===')
print(f'  Passes: {len(PASSES)}, Pairs: {len(jacc_vals)}')
print(f'  Min={min_j:.3f} / P25={p25:.3f} / Median={med:.3f} / P75={p75:.3f} / Max={max_j:.3f} / Mean={mean_j:.3f}')

# ── Per-pass avg Jaccard (vs all other passes) ─────────────────────────────────
avg_j = []
for i, p in enumerate(PASSES):
    others = [jaccard(p['strong_spine'], PASSES[j]['strong_spine'])
              for j in range(len(PASSES)) if j != i]
    avg_j.append(statistics.mean(others))
    p['avg_j'] = avg_j[-1]

# ── Consensus spine (full set = all 10 nodes; strong spine for frequency) ──────
print('\n=== CONSENSUS SPINE (by frequency in PRIMARY only) ===')
primary_counts = {n: 0 for n in ALL_NODES}
strong_counts  = {n: 0 for n in ALL_NODES}
full_counts    = {n: 10 for n in ALL_NODES}  # all passes include all nodes

for p in PASSES:
    for n in p['primary']:
        primary_counts[n] += 1
    for n in p['strong_spine']:
        strong_counts[n] += 1

n_passes = len(PASSES)
thresholds = [0.80, 0.50, 0.20]
for thr in thresholds:
    spine_nodes = sorted([n for n, c in primary_counts.items() if c / n_passes >= thr],
                         key=lambda n: -primary_counts[n])
    print(f'  @{int(thr*100)}% primary: nodes={spine_nodes}  counts={[primary_counts[n] for n in spine_nodes]}')

print('\n=== PRIMARY NODE FREQUENCY ===')
for node_num in sorted(primary_counts, key=lambda n: -primary_counts[n]):
    pct = primary_counts[node_num] / n_passes * 100
    print(f'  Node {node_num:2d}: primary {primary_counts[node_num]:2d}/{n_passes} ({pct:.0f}%)'
          f'  strong {strong_counts[node_num]:2d}/{n_passes} ({strong_counts[node_num]/n_passes*100:.0f}%)')

# ── Greedy-agglomeration clusters (3 groups) ──────────────────────────────────
# Sort passes by avg_j descending, greedily assign to 3 clusters.
pass_order = sorted(range(len(PASSES)), key=lambda i: -avg_j[i])
clusters = {0: [], 1: [], 2: []}  # A=high, B=mid, C=low
cluster_labels = {0: 'A', 1: 'B', 2: 'C'}

for rank, idx in enumerate(pass_order):
    if rank < 4:
        clusters[0].append(idx)
    elif rank < 7:
        clusters[1].append(idx)
    else:
        clusters[2].append(idx)

print('\n=== GREEDY-AGGLOMERATION CLUSTERS ===')
for cid, indices in clusters.items():
    pass_ids = [PASSES[i]['pass_id'] for i in indices]
    avg_js = [avg_j[i] for i in indices]
    mean_cluster_j = statistics.mean(avg_js) if avg_js else 0
    print(f'  Cluster {cluster_labels[cid]}: passes={pass_ids}  avg_J_to_others={mean_cluster_j:.3f}')
    for i in indices:
        PASSES[i]['cluster'] = cluster_labels[cid]

# ── In/out ratio ───────────────────────────────────────────────────────────────
region_tok_hi = 144420
output_tok_his = [p['output_tok_hi'] for p in PASSES]
print(f'\n=== IN/OUT RATIO ===')
print(f'  Input tok_hi: {region_tok_hi:,} (rendered payload)')
print(f'  Output tok_hi range: {min(output_tok_his):,} - {max(output_tok_his):,}')
print(f'  Output tok_hi mean: {statistics.mean(output_tok_his):,.0f}')

# ── Flinch summary ─────────────────────────────────────────────────────────────
flinched_passes = [p for p in PASSES if p['flinched'] == 'Y']
print(f'\n=== FLINCH SUMMARY ===')
print(f'  Flinches: {len(flinched_passes)} of {len(PASSES)} passes')
for p in flinched_passes:
    print(f'  Pass {p["pass_id"]:2d}: {p["flinch_note"]}')

# ── Per-pass table ─────────────────────────────────────────────────────────────
print('\n=== PER-PASS TABLE ===')
print(f'  {"Pass":>4}  {"Status":6}  {"Flinch":6}  {"SynthChars":>10}  {"OutputTokHi":>11}  {"Cluster":7}  Primary   Secondary')
for p in PASSES:
    prim = ','.join(str(n) for n in sorted(p['primary']))
    sec  = ','.join(str(n) for n in sorted(p['secondary']))
    print(f'  {p["pass_id"]:>4}  OK      {"Y" if p["flinched"]=="Y" else "N":6}  {p["synthesis_chars"]:>10,}  {p["output_tok_hi"]:>11,}  {p.get("cluster","?"):7}  {prim:10}  {sec}')

# ── Write pass_nodesets_S71_replA.csv ─────────────────────────────────────────
csv_path = OUT_DIR / 'pass_nodesets_S71_replA.csv'
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    f.write('arm,pass_id,status,flinched,synthesis_char_count,output_tok_hi,node_numbers,cluster\n')
    for p in PASSES:
        node_nums = ';'.join(str(n) for n in p['node_order'])
        row = f"replA_baseline,{p['pass_id']},OK,{p['flinched']},{p['synthesis_chars']},{p['output_tok_hi']},{node_nums},{p.get('cluster','')}\n"
        f.write(row)
print(f'\nWrote: {csv_path}')

# ── Full Jaccard matrix (for reference) ───────────────────────────────────────
print('\n=== PAIRWISE JACCARD MATRIX (strong spine) ===')
header = '     ' + ''.join(f'  P{p["pass_id"]:02d}' for p in PASSES)
print(header)
for i, pi in enumerate(PASSES):
    row_vals = []
    for j, pj in enumerate(PASSES):
        if j < i:
            row_vals.append('    ')
        elif j == i:
            row_vals.append(' 1.00')
        else:
            j_val = jaccard(pi['strong_spine'], pj['strong_spine'])
            row_vals.append(f' {j_val:.2f}')
    print(f'  P{pi["pass_id"]:02d}' + ''.join(row_vals))

print('\n=== CHANGE MANIFEST ===')
print(f'  CREATED: {csv_path}')
print(f'  Passes analyzed: {len(PASSES)}  |  Flinches: {len(flinched_passes)}/{len(PASSES)}')
print(f'  Median Jaccard (strong spine): {med:.3f}  |  Mean: {mean_j:.3f}')
print(f'  ANTHROPIC_API_KEY: NOT loaded')
print(f'  Floor: NOT accessed')
print(f'  Writes: ONLY under {OUT_DIR}')
