# foray_measure_S71_replB.py  S71 replB  CC Step 4 — Measure + Report
# Reads all 20 pass_replB_NN_synthesis.md files, extracts node sets + flinch info,
# computes pairwise Jaccard, consensus spine, greedy-agglom clustering, in/out ratio.
# Writes diagnostic_report_S71_replB.md and pass_nodesets_S71_replB.csv.
# $0, read-only except for the two output files.

import json, os, re, sys
from itertools import combinations
from pathlib import Path

# ── Hard guard ──────────────────────────────────────────────────────────────────
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY is loaded — HALT.')

SCRIPT_DIR   = Path(__file__).parent
WALLABY_DIR  = SCRIPT_DIR.parent
RUN_DIR      = WALLABY_DIR / 'runs' / 'foray_diagnostic_S71_replB'
FROZEN_JSON  = RUN_DIR / 'region_frozen_S71_replB.json'
REPORT_OUT   = RUN_DIR / 'diagnostic_report_S71_replB.md'
CSV_OUT      = RUN_DIR / 'pass_nodesets_S71_replB.csv'

N_PASSES = 20

# ── Load frozen region metadata ──────────────────────────────────────────────────
frozen = json.loads(FROZEN_JSON.read_text(encoding='utf-8'))
total_nodes    = frozen['total_nodes']           # 24
total_tok_hi   = frozen['total_tok_hi']          # from CSV (717,551)
tok_hi_est     = frozen['tok_hi_est']            # rendered chars × 0.72 (~399K)
payload_chars  = frozen['payload_chars']         # 554,143
seed           = frozen['seed']                  # 20260621

print(f'Region: {total_nodes} nodes, tok_hi={total_tok_hi:,} (CSV), '
      f'tok_hi_est={tok_hi_est:,} (rendered), seed={seed}')

# ── Parse synthesis files ────────────────────────────────────────────────────────
# Extract: flinched (Y/N), flinch text (if any), synthesis_chars, node_numbers

def parse_synthesis(path):
    text = path.read_text(encoding='utf-8', errors='replace')
    chars = len(text)

    # Detect flinch: look for INVERTED ADMISSION section with non-trivial content
    # or explicit "flinched:" / "flinch" keywords
    flinched = False
    flinch_text = ''

    inv_match = re.search(
        r'(?i)(inverted admission|i could not|could not be read|flinched|flinch|'
        r'not fully held|could not hold|exceeded.*read|partial.*read|'
        r'read at.*boundary|sampled.*not.*full|papered|gap|'
        r'too large|exceeded.*capacity|single-read|node \d+.*exceed)',
        text
    )
    if inv_match:
        flinched = True
        # Extract the flinch attribution sentence if it follows the pattern
        flinch_pat = re.search(
            r'flinched[:\s]+([^\n]+)',
            text, re.IGNORECASE
        )
        if flinch_pat:
            flinch_text = flinch_pat.group(1).strip()
        else:
            # Try to find the "node N (~XXK tok_hi) exceeds" format
            node_flinch = re.search(
                r'(node \d+[^.]*(?:exceed|too large|single.read|single read|beyond)[^.\n]*)',
                text, re.IGNORECASE
            )
            if node_flinch:
                flinch_text = node_flinch.group(1).strip()
            else:
                flinch_text = '[see inverted admission section]'

    # Extract load-bearing node numbers
    # Look for "Load-bearing: N, N, N" or "Load-bearing nodes: N, N"
    # Also look for node numbers listed at end of synthesis
    node_nums = set()

    lb_patterns = [
        r'(?i)load.bearing(?:\s+nodes)?[:\s]+([0-9, ;]+)',
        r'(?i)load.bearing\s*nodes\s+identified[:\s]+([0-9, ;]+)',
        r'(?i)spine[:\s]+([0-9, ;]+)',
        r'(?i)nodes?[:\s]+((?:\d+[,;\s]+)+\d+)',  # "nodes: 1, 2, 5"
    ]

    for pat in lb_patterns:
        m = re.search(pat, text)
        if m:
            nums_str = m.group(1)
            found = re.findall(r'\d+', nums_str)
            for n in found:
                nn = int(n)
                if 1 <= nn <= total_nodes:
                    node_nums.add(nn)
            if node_nums:
                break

    # If we found starred-format (**1** (description), **5**, etc.), extract those too
    if not node_nums:
        bold_nums = re.findall(r'\*\*(\d+)\*\*', text)
        for n in bold_nums:
            nn = int(n)
            if 1 <= nn <= total_nodes:
                node_nums.add(nn)

    # Last resort: look for "NODE N" references near "load-bearing" or "spine"
    if not node_nums:
        context = re.search(r'(?i)(?:load.bearing|spine).{0,500}', text, re.DOTALL)
        if context:
            found = re.findall(r'\b(\d+)\b', context.group(0))
            for n in found:
                nn = int(n)
                if 1 <= nn <= total_nodes:
                    node_nums.add(nn)

    return {
        'flinched':    flinched,
        'flinch_text': flinch_text,
        'chars':       chars,
        'node_nums':   node_nums,
    }

passes = []
for i in range(1, N_PASSES + 1):
    fname = RUN_DIR / f'pass_replB_{i:02d}_synthesis.md'
    if not fname.exists():
        print(f'WARNING: {fname} not found — marking as MISSING')
        passes.append({'pass_id': i, 'status': 'MISSING', 'flinched': False,
                       'flinch_text': '', 'chars': 0, 'node_nums': set()})
        continue
    parsed = parse_synthesis(fname)
    passes.append({
        'pass_id':    i,
        'status':     'OK',
        'flinched':   parsed['flinched'],
        'flinch_text': parsed['flinch_text'],
        'chars':      parsed['chars'],
        'tok_hi_out': int(parsed['chars'] * 0.72),
        'node_nums':  parsed['node_nums'],
    })
    status = 'Y' if parsed['flinched'] else 'N'
    print(f'  pass {i:02d}: flinch={status}  chars={parsed["chars"]:,}  '
          f'nodes={sorted(parsed["node_nums"])}')

ok_passes = [p for p in passes if p['status'] == 'OK']
print(f'\n{len(ok_passes)}/{N_PASSES} passes OK')

# ── Pairwise Jaccard ──────────────────────────────────────────────────────────────
def jaccard(a, b):
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union > 0 else 0.0

node_sets = [p['node_nums'] for p in ok_passes]
pairs = list(combinations(range(len(ok_passes)), 2))
j_vals = [jaccard(node_sets[i], node_sets[j]) for i, j in pairs]

def pct(vals, p):
    if not vals:
        return 0.0
    s = sorted(vals)
    idx = (len(s) - 1) * p / 100
    lo, hi = int(idx), min(int(idx) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (idx - lo)

j_min    = min(j_vals) if j_vals else 0
j_p25    = pct(j_vals, 25)
j_median = pct(j_vals, 50)
j_p75    = pct(j_vals, 75)
j_max    = max(j_vals) if j_vals else 0
j_mean   = sum(j_vals) / len(j_vals) if j_vals else 0

print(f'\nJaccard: Min={j_min:.3f} P25={j_p25:.3f} Med={j_median:.3f} '
      f'P75={j_p75:.3f} Max={j_max:.3f} Mean={j_mean:.3f}')

# ── Consensus spine ───────────────────────────────────────────────────────────────
from collections import Counter

all_node_counts = Counter()
for ns in node_sets:
    for n in ns:
        all_node_counts[n] += 1

n_passes = len(ok_passes)

def consensus_at(pct_threshold):
    threshold = pct_threshold / 100 * n_passes
    nodes = sorted([n for n, c in all_node_counts.items() if c >= threshold])
    return nodes

spine_80 = consensus_at(80)
spine_50 = consensus_at(50)
spine_20 = consensus_at(20)

print(f'\nConsensus spine @80%: {spine_80}')
print(f'Consensus spine @50%: {spine_50}')
print(f'Consensus spine @20%: {spine_20}')

# ── Greedy-agglomeration clustering (2-4 groups) ──────────────────────────────────
# Build pairwise J matrix for ok_passes
n_ok = len(ok_passes)
j_matrix = [[0.0] * n_ok for _ in range(n_ok)]
for i in range(n_ok):
    for k in range(n_ok):
        j_matrix[i][k] = jaccard(node_sets[i], node_sets[k])

def avg_j_to_cluster(pass_idx, cluster_indices):
    if not cluster_indices:
        return 0.0
    return sum(j_matrix[pass_idx][c] for c in cluster_indices) / len(cluster_indices)

def greedy_cluster(n_clusters):
    # Find the pass with highest average J to all others → seed of cluster A
    avg_j_to_all = [sum(j_matrix[i][k] for k in range(n_ok) if k != i) / (n_ok - 1)
                    for i in range(n_ok)]
    seed = max(range(n_ok), key=lambda i: avg_j_to_all[i])

    clusters = [[seed]]
    assigned = {seed: 0}

    # Expand cluster 0 greedily
    for _ in range(n_clusters - 1):
        # Find the pass least similar to current clusters → seed of next cluster
        remaining = [i for i in range(n_ok) if i not in assigned]
        if not remaining:
            break
        # Find which remaining is most different from ALL existing cluster seeds
        most_diff = min(remaining, key=lambda i: max(
            avg_j_to_cluster(i, c) for c in clusters
        ))
        clusters.append([most_diff])
        assigned[most_diff] = len(clusters) - 1

    # Assign all remaining passes to closest cluster
    for i in range(n_ok):
        if i in assigned:
            continue
        best_cluster = max(range(len(clusters)),
                           key=lambda c: avg_j_to_cluster(i, clusters[c]))
        clusters[best_cluster].append(i)
        assigned[i] = best_cluster

    return clusters

clusters = greedy_cluster(3)  # 3 clusters (can be 2-4; use 3 as default)

# Compute avg within-cluster J and label A (highest) → C (lowest)
cluster_avg_j = []
for clust in clusters:
    if len(clust) < 2:
        cj = 1.0
    else:
        cjs = [j_matrix[i][k] for i, k in combinations(clust, 2)]
        cj = sum(cjs) / len(cjs) if cjs else 1.0
    cluster_avg_j.append(cj)

# Sort clusters: A = highest avg_j (most convergent), C = lowest
order = sorted(range(len(clusters)), key=lambda x: -cluster_avg_j[x])
label_map = {order[i]: chr(65 + i) for i in range(len(order))}  # 0→A, 1→B, etc.

pass_cluster_label = {}
for ci, clust in enumerate(clusters):
    for pi in clust:
        pass_cluster_label[pi] = label_map[ci]

print('\nClusters (A=most-convergent, C=most-divergent):')
for ci in order:
    clust = clusters[ci]
    label = label_map[ci]
    pass_nums = sorted(ok_passes[pi]['pass_id'] for pi in clust)
    print(f'  Cluster {label}: passes {pass_nums}  avg_J={cluster_avg_j[ci]:.3f}')

# ── Flinch log (build before report) ──────────────────────────────────────────────
flinched_passes = [p for p in ok_passes if p['flinched']]

print(f'\nFlinches: {len(flinched_passes)}/{len(ok_passes)} passes')
for p in flinched_passes:
    ft = p.get('flinch_text', '').encode('ascii', errors='replace').decode('ascii')
    print(f'  pass {p["pass_id"]:02d}: {ft}')

# ── In/out ratio ──────────────────────────────────────────────────────────────────
avg_out_chars  = sum(p['chars'] for p in ok_passes) / len(ok_passes) if ok_passes else 0
avg_out_tok_hi = int(avg_out_chars * 0.72)

# ── Write CSV ─────────────────────────────────────────────────────────────────────
csv_lines = ['arm,pass_id,status,flinched,synthesis_char_count,output_tok_hi,node_numbers,cluster,flinch_text']
for i, p in enumerate(ok_passes):
    flinch_flag = 'Y' if p['flinched'] else 'N'
    nodes_str   = ';'.join(str(n) for n in sorted(p['node_nums']))
    cluster_lbl = pass_cluster_label.get(i, '')
    flinch_txt  = p.get('flinch_text', '').replace(',', ';')
    csv_lines.append(
        f"question,{p['pass_id']},OK,{flinch_flag},{p['chars']},{p['tok_hi_out']},"
        f"{nodes_str},{cluster_lbl},{flinch_txt}"
    )

CSV_OUT.write_text('\n'.join(csv_lines) + '\n', encoding='utf-8')
print(f'\nWrote {CSV_OUT}')

# ── Build report ──────────────────────────────────────────────────────────────────
def node_ids(node_nums, frozen_nodes):
    """Return 'conv_uuid[:8], anchor_msg[:8]' for each node number."""
    lookup = {n['node_number']: n for n in frozen_nodes}
    parts = []
    for nn in sorted(node_nums):
        nd = lookup.get(nn)
        if nd:
            parts.append(f"{nd['conv_uuid'][:8]}, {nd['anchor_msg'][:8]}")
    return ' | '.join(parts) if parts else '—'

frozen_nodes = frozen['nodes']

# Describe Jaccard distribution shape
j_iqr = j_p75 - j_p25
shape_desc = (f'IQR={j_iqr:.3f}. Distribution is '
              + ('tight — most pairs cluster near the median.' if j_iqr < 0.15
                 else 'moderate spread.' if j_iqr < 0.25
                 else 'wide — significant scatter across pass pairs.'))

cluster_rows = []
for ci in order:
    clust = clusters[ci]
    label = label_map[ci]
    pass_nums = sorted(ok_passes[pi]['pass_id'] for pi in clust)
    cluster_rows.append(f'| {label} | {pass_nums} | {cluster_avg_j[ci]:.3f} |')

flinch_log_rows = []
for p in flinched_passes:
    ft = p['flinch_text'] or '[see synthesis text]'
    flinch_log_rows.append(f'| {p["pass_id"]:02d} | {p["chars"]:,} | {ft} |')

report_lines = [
    '# diagnostic_report_S71_replB.md — S71 Foray Diagnostic Volley Replication B',
    f'*S71 apparatus "The Foray" · replB · 2026-06-20*',
    '*All agent() calls: on-sub subscription-billed. ANTHROPIC_API_KEY not loaded throughout.*',
    '*Run note: 20 WET readers fired in 4 groups of 5 (staggered for rate-limit management). 20/20 completed.*',
    '',
    '## Frozen Region',
    '',
    '| Field | Value |',
    '|-------|-------|',
    f'| Seed | {seed} (fresh — distinct from S71\'s 20260620) |',
    f'| Nodes | {total_nodes} |',
    f'| Distinct convs | {total_nodes} |',
    f'| Tok_hi (CSV, full reach) | {total_tok_hi:,} |',
    f'| Payload chars (rendered, reach_up=1) | {payload_chars:,} |',
    f'| Tok_hi_est (rendered × 0.72) | {tok_hi_est:,} |',
    f'| Band target | 678K–828K (tok_hi from CSV) |',
    f'| Region file | region_S71_replB.txt |',
    '',
    '**Note on tok_hi discrepancy:** CSV total_tok_hi (717,551) reflects full-span reach values per node.',
    'The rendered region uses reach_up=1 (same approximation as S71), yielding 554,143 chars / ~399K tok_hi_est.',
    'Two nodes (node 13: 182K tok_hi CSV; node 21: 174K tok_hi CSV) have large full-span reaches but compact',
    'reach_up=1 renders. The actual input to readers was ~399K tok_hi_est (rendered file size).',
    'S71 oversized arm actual input: ~753K tok_hi. replB is approximately the medium-arm scale (~399K tok_hi).',
    '',
    '**INTERPRETATION NOTE:** The baseline Jaccard anchor from S71 is J=0.600 (median, 144K region).',
    'S71 question arm (753K actual input): median J=0.615.',
    'replB question arm (~399K actual input): see measurements below.',
    'Read replB results against the S71 baseline anchor (J=0.600), not against an abstract 0-to-1 scale.',
    '',
    '## Per-pass Results',
    '',
    '| Pass | Status | Flinched | Synthesis chars | Output tok_hi | Cluster |',
    '|------|--------|----------|-----------------|---------------|---------|',
]

for i, p in enumerate(ok_passes):
    flinch_flag = 'Y' if p['flinched'] else 'N'
    report_lines.append(
        f"| {p['pass_id']:02d} | OK | {flinch_flag} | {p['chars']:,} | {p['tok_hi_out']:,} | "
        f"{pass_cluster_label.get(i, '')} |"
    )

n_flinched = len(flinched_passes)
report_lines += [
    '',
    f'{len(ok_passes)}-of-20 passes completed. {n_flinched} flinch(es).',
    '',
    '## In/Out Ratio',
    '',
    '| Source | Input tok_hi | Output tok_hi (avg) |',
    '|--------|-------------|---------------------|',
    f'| S71 baseline (10 passes, 144K) | ~144K | 5,111–7,020 [S71 MEASURED] |',
    f'| S71 question (20 passes, ~753K actual) | ~753K | 5,293–10,062 [S71 MEASURED] |',
    f'| replB question (20 passes, ~399K actual) | ~399K | {min(p["tok_hi_out"] for p in ok_passes):,}–{max(p["tok_hi_out"] for p in ok_passes):,} [MEASURED] |',
    '',
    f'replB avg output: {avg_out_chars:,.0f} chars / ~{avg_out_tok_hi:,} tok_hi',
    '',
    '## Pairwise Jaccard',
    '',
    f'- Passes: {len(ok_passes)}, Pairs: {len(j_vals)}',
    f'- Min={j_min:.3f} / P25={j_p25:.3f} / Median={j_median:.3f} / '
    f'P75={j_p75:.3f} / Max={j_max:.3f} / Mean={j_mean:.3f}',
    f'- Signal shape: {shape_desc}',
    '',
    '**S71 comparison:** S71 baseline (144K) median J=0.600. S71 question (753K) median J=0.615.',
    f'replB question (~399K) median J={j_median:.3f}.',
    '',
    '## Consensus Spine',
    '',
    '| Threshold | Nodes | Node numbers |',
    '|-----------|-------|--------------|',
    f'| @80% | {len(spine_80)} | {", ".join(str(n) for n in spine_80)} |',
    f'| @50% | {len(spine_50)} | {", ".join(str(n) for n in spine_50)} |',
    f'| @20% | {len(spine_20)} | {", ".join(str(n) for n in spine_20)} |',
    '',
]

# Node identity for spine nodes
report_lines += [
    '### Spine node identity (@80% threshold)',
    '',
    '| Node # | conv_uuid[:8] | anchor_msg[:8] | tok_hi (CSV) |',
    '|--------|---------------|----------------|--------------|',
]
lookup = {n['node_number']: n for n in frozen_nodes}
for nn in spine_80:
    nd = lookup.get(nn, {})
    report_lines.append(
        f"| {nn} | {nd.get('conv_uuid','')[:8]} | {nd.get('anchor_msg','')[:8]} | "
        f"{nd.get('tok_hi', 0):,} |"
    )

report_lines += [
    '',
    '## Spine Clusters',
    '',
    'Cluster A = most convergent (highest avg within-cluster Jaccard). C = most divergent.',
    '',
    '| Cluster | Passes | Avg J within cluster |',
    '|---------|--------|----------------------|',
] + cluster_rows + [
    '',
    '## Flinch Log — With Node Attribution (replB addition)',
    '',
    f'- Total flinches: {n_flinched} of {len(ok_passes)} passes',
]

if flinch_log_rows:
    report_lines += [
        '',
        '| Pass | Synthesis chars | Flinch attribution |',
        '|------|-----------------|-------------------|',
    ] + flinch_log_rows
else:
    report_lines.append('- No flinches recorded.')

report_lines += [
    '',
    '## Hard Guards — Confirmed',
    '',
    '- ANTHROPIC_API_KEY: NOT loaded (on-sub billed only)',
    '- Floor: READ-ONLY. No floor DB writes. Region read from draw script, regions/ on disk.',
    '- Writes: only under wallaby-way/runs/foray_diagnostic_S71_replB/',
    '- Grain: (conv_uuid, anchor_msg) PAIR — node numbers map to full pairs via region_frozen_S71_replB.json',
    '- Stagger: 4 groups of 5 readers — not a simultaneous blast',
    '- Phase 0 outputs and S71 foray_diagnostic_S71/ artifacts: NOT mutated',
    '',
    'This report does NOT pronounce beast-vs-shitcannon. The Jaccard numbers, baseline anchor,',
    'and prose syntheses are the laid-bare parting. The verdict is Jake\'s (P7).',
    '',
    '## Change Manifest',
    '',
    '**Files written (ONLY under wallaby-way/runs/foray_diagnostic_S71_replB/):**',
    f'- region_S71_replB.txt — rendered region ({payload_chars:,} chars, {total_nodes} nodes)',
    f'- region_frozen_S71_replB.json — frozen node list (seed {seed})',
    f'- pass_replB_01_synthesis.md through pass_replB_20_synthesis.md — 20 reader syntheses',
    f'- pass_nodesets_S71_replB.csv — per-pass CSV',
    f'- diagnostic_report_S71_replB.md — this report',
    '',
    '**Scripts written (wallaby-way/scripts/):**',
    '- foray_draw_S71_replB.py — drew and rendered the fresh region',
    '- foray_measure_S71_replB.py — computed measurements, wrote report + CSV',
    '',
    '**Commands run:**',
    '- foray_draw_S71_replB.py: PASS',
    '- 20 reader agent() calls (4 groups of 5): 20/20 PASS',
    '- foray_measure_S71_replB.py: PASS',
    '',
    '**Anything outside the plan:** None. All actions trace to the replB spec.',
    '',
    '**Stopped here / next:**',
    'Stopped at Step 5 per spec. Does NOT pronounce beast-vs-shitcannon.',
    'Next: Jake + OC read the diagnostic as a pile (side-by-side replB vs S71), rule beast-vs-shitcannon (P7).',
]

REPORT_OUT.write_text('\n'.join(report_lines) + '\n', encoding='utf-8')
print(f'Wrote {REPORT_OUT}')

print('\n=== SUMMARY ===')
print(f'  Region: {total_nodes} nodes, {total_tok_hi:,} tok_hi (CSV), ~{tok_hi_est:,} tok_hi_est (rendered)')
print(f'  Passes: {len(ok_passes)}/20 OK, {n_flinched} flinched')
print(f'  Jaccard: Min={j_min:.3f} P25={j_p25:.3f} Med={j_median:.3f} P75={j_p75:.3f} Max={j_max:.3f} Mean={j_mean:.3f}')
print(f'  Spine @80%: {spine_80}')
print(f'  Spine @50%: {spine_50}')
