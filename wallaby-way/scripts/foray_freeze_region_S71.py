# foray_freeze_region_S71.py  S71  CC Step 1 of Diagnostic Volley
# Deterministically re-derives the frozen node-sets for both arms (small + oversized)
# from node_size_distribution.csv using the same seed/logic as s71_draw_regions.py.
# $0, read-only against floor, writes only to runs/foray_diagnostic_S71/.
#
# Output: region_frozen_S71.json
#   {
#     "small":     {total_nodes, total_tok_hi, region_file, nodes: [{node_number, conv_uuid, anchor_msg, tok_hi}]},
#     "medium":    {... (intermediate state, not used as an arm but must be drawn to advance random state)},
#     "oversized": {total_nodes, total_tok_hi, region_file, nodes: [...]}
#   }

import csv, json, os, random, sys
from pathlib import Path

# ── Hard guard ─────────────────────────────────────────────────────────────────
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY is loaded — HALT. $0 assertion failed.')

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
WALLABY_DIR  = SCRIPT_DIR.parent
CSV_PATH     = WALLABY_DIR / 'runs' / 'foray_discovery_S71' / 'node_size_distribution.csv'
OUT_DIR      = WALLABY_DIR / 'runs' / 'foray_diagnostic_S71'
OUT_JSON     = OUT_DIR / 'region_frozen_S71.json'
REGIONS_DIR  = WALLABY_DIR / 'runs' / 'foray_discovery_S71' / 'regions'

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Read CSV — identical filter as s71_draw_regions.py ────────────────────────
print(f'Reading {CSV_PATH} ...')
all_nodes = []
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        tok_hi = int(r['tok_hi'])
        if tok_hi <= 200_000:
            all_nodes.append({
                'conv_uuid':      r['conv_uuid'],
                'anchor_msg':     r['anchor_msg'],
                'rendered_chars': int(r['rendered_chars']),
                'tok_hi':         tok_hi,
            })

print(f'  Eligible nodes (tok_hi <= 200K): {len(all_nodes):,}')

# ── Deterministic seed — MUST match s71_draw_regions.py exactly ───────────────
random.seed(20260620)

# ── pick_region — VERBATIM logic from s71_draw_regions.py ─────────────────────
def pick_region(nodes, target_tok_hi, label):
    """Greedily pick nodes from distinct convs until target tok_hi is reached.
    Shuffles in place (advances global random state — must call in same order as
    the original script to reproduce the same sequence)."""
    random.shuffle(nodes)
    used_convs = set()
    chosen = []
    total_tok_hi = 0
    for n in nodes:
        if n['conv_uuid'] in used_convs:
            continue
        chosen.append(n)
        used_convs.add(n['conv_uuid'])
        total_tok_hi += n['tok_hi']
        if total_tok_hi >= target_tok_hi:
            break
    print(f'  {label}: {len(chosen)} nodes, {len(set(n["conv_uuid"] for n in chosen))} distinct convs, '
          f'total tok_hi {total_tok_hi:,}')
    return chosen

# Draw all three regions in the same order as s71_draw_regions.py.
# This is mandatory — each pick advances the random state for the next.
nodes_small     = pick_region(list(all_nodes), target_tok_hi=150_000,  label='small')
nodes_medium    = pick_region(list(all_nodes), target_tok_hi=400_000,  label='medium')
nodes_oversized = pick_region(list(all_nodes), target_tok_hi=900_000,  label='oversized')

# ── Build numbered node lists (1-indexed, matches NODE N labels in region files) ─
def build_node_list(nodes):
    return [
        {
            'node_number':  i + 1,
            'conv_uuid':    n['conv_uuid'],
            'anchor_msg':   n['anchor_msg'],
            'tok_hi':       n['tok_hi'],
        }
        for i, n in enumerate(nodes)
    ]

frozen = {
    'seed': 20260620,
    'small': {
        'arm':          'baseline',
        'region_file':  str(REGIONS_DIR / 'region_small.txt'),
        'total_nodes':  len(nodes_small),
        'total_tok_hi': sum(n['tok_hi'] for n in nodes_small),
        'nodes':        build_node_list(nodes_small),
    },
    'medium': {
        'arm':          'intermediate_state_only',
        'region_file':  str(REGIONS_DIR / 'region_medium.txt'),
        'total_nodes':  len(nodes_medium),
        'total_tok_hi': sum(n['tok_hi'] for n in nodes_medium),
        'nodes':        build_node_list(nodes_medium),
    },
    'oversized': {
        'arm':          'question',
        'region_file':  str(REGIONS_DIR / 'region_oversized.txt'),
        'total_nodes':  len(nodes_oversized),
        'total_tok_hi': sum(n['tok_hi'] for n in nodes_oversized),
        'nodes':        build_node_list(nodes_oversized),
    },
}

# ── Verification ───────────────────────────────────────────────────────────────
# Check 1: node counts
TARGET_SMALL_NODES     = 7
TARGET_OVERSIZED_NODES = 38

errors = []
if frozen['small']['total_nodes'] != TARGET_SMALL_NODES:
    errors.append(f"small node count: got {frozen['small']['total_nodes']}, expected {TARGET_SMALL_NODES}")
if frozen['oversized']['total_nodes'] != TARGET_OVERSIZED_NODES:
    errors.append(f"oversized node count: got {frozen['oversized']['total_nodes']}, expected {TARGET_OVERSIZED_NODES}")

# Check 2: cross-verify NODE N headers in the oversized region file.
# Region file headers use truncated IDs: conv_uuid[:8] and anchor_msg[:8].
# Compare the first 8 chars of each node in the frozen set vs. the region file.
import re as _re
oversized_region_path = Path(frozen['oversized']['region_file'])
if oversized_region_path.exists():
    region_text = oversized_region_path.read_text(encoding='utf-8')
    # Parse all NODE N lines: --- NODE N [conv8.../anchor8...] tok_hi≈K ---
    header_re = _re.compile(r'^--- NODE (\d+) \[([0-9a-f]+)\.\.\./([0-9a-f]+)\.\.\.\]', _re.MULTILINE)
    file_nodes = {}  # node_number → (conv8, anchor8)
    for m in header_re.finditer(region_text):
        file_nodes[int(m.group(1))] = (m.group(2), m.group(3))

    mismatches = []
    for n in frozen['oversized']['nodes']:
        nn = n['node_number']
        if nn not in file_nodes:
            mismatches.append(f"NODE {nn}: not found in region file headers")
            continue
        fc8, fa8 = file_nodes[nn]
        if not n['conv_uuid'].startswith(fc8):
            mismatches.append(f"NODE {nn}: conv_uuid prefix mismatch — frozen {n['conv_uuid'][:8]} vs file {fc8}")
        if not n['anchor_msg'].startswith(fa8):
            mismatches.append(f"NODE {nn}: anchor_msg prefix mismatch — frozen {n['anchor_msg'][:8]} vs file {fa8}")

    if len(file_nodes) != TARGET_OVERSIZED_NODES:
        errors.append(f"region file has {len(file_nodes)} NODE headers, expected {TARGET_OVERSIZED_NODES}")
    if mismatches:
        errors.extend(mismatches[:10])  # show up to 10
        if len(mismatches) > 10:
            errors.append(f"... and {len(mismatches)-10} more mismatches")
    else:
        print(f'  Cross-check PASS: all {TARGET_OVERSIZED_NODES} NODE headers match frozen set.')
else:
    print(f'  WARNING: region file not found at {oversized_region_path} — skipping cross-check')

# Also cross-verify small region
small_region_path = Path(frozen['small']['region_file'])
if small_region_path.exists():
    small_text = small_region_path.read_text(encoding='utf-8')
    small_file_nodes = {}
    for m in header_re.finditer(small_text):
        small_file_nodes[int(m.group(1))] = (m.group(2), m.group(3))
    small_mismatches = []
    for n in frozen['small']['nodes']:
        nn = n['node_number']
        if nn not in small_file_nodes:
            small_mismatches.append(f"NODE {nn}: not found in small region file headers")
            continue
        fc8, fa8 = small_file_nodes[nn]
        if not n['conv_uuid'].startswith(fc8):
            small_mismatches.append(f"NODE {nn}: conv_uuid prefix mismatch")
        if not n['anchor_msg'].startswith(fa8):
            small_mismatches.append(f"NODE {nn}: anchor_msg prefix mismatch")
    if small_mismatches:
        errors.extend(small_mismatches[:5])
    else:
        print(f'  Cross-check PASS (small): all {TARGET_SMALL_NODES} NODE headers match frozen set.')

if errors:
    for e in errors:
        print(f'VERIFICATION FAIL: {e}')
    sys.exit('Frozen node-set did not match Phase 0 region files — HALT.')

print('\nVerification PASS:')
print(f'  small:     {frozen["small"]["total_nodes"]} nodes, tok_hi {frozen["small"]["total_tok_hi"]:,}')
print(f'  medium:    {frozen["medium"]["total_nodes"]} nodes, tok_hi {frozen["medium"]["total_tok_hi"]:,}  (state-advance only)')
print(f'  oversized: {frozen["oversized"]["total_nodes"]} nodes, tok_hi {frozen["oversized"]["total_tok_hi"]:,}')

# ── Write JSON ─────────────────────────────────────────────────────────────────
OUT_JSON.write_text(json.dumps(frozen, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'\nWrote {OUT_JSON}')

# ── Manifest ──────────────────────────────────────────────────────────────────
print()
print('=== CHANGE MANIFEST ===')
print(f'  {OUT_JSON}')
print(f'  small nodes:     {frozen["small"]["total_nodes"]}  tok_hi {frozen["small"]["total_tok_hi"]:,}')
print(f'  oversized nodes: {frozen["oversized"]["total_nodes"]}  tok_hi {frozen["oversized"]["total_tok_hi"]:,}')
print(f'  ANTHROPIC_API_KEY: NOT loaded (guard passed)')
print(f'  Floor: NOT touched (CSV read-only)')
print(f'  Writes: region_frozen_S71.json only')
