# foray_freeze_region_S71.py  S71  CC Step 1 of Diagnostic Volley
# Deterministically re-derives the frozen node-sets for both arms (small + oversized)
# from node_size_distribution.csv using the same seed/logic as s71_draw_regions.py.
# $0, read-only against floor, writes only to runs/foray_diagnostic_S71/.
#
# S72 UPDATE: renders small + oversized arms from floor (reach_up=1, reach_down=0,
# scrub_v3) to record rendered_chars + rendered_payload_tok_hi_est as the
# authoritative estimate. total_csv_tok_hi kept for provenance. Tiktoken ratio
# check on small arm. in_target_band computed vs rendered number, not CSV sum.
#
# Output: region_frozen_S71.json
#   {
#     "small":     {total_nodes, total_csv_tok_hi, rendered_chars,
#                   rendered_payload_tok_hi_est, in_target_band, region_file, nodes: [...]},
#     "medium":    {total_nodes, total_csv_tok_hi, ...}  (state-advance, no render),
#     "oversized": {total_nodes, total_csv_tok_hi, rendered_chars,
#                   rendered_payload_tok_hi_est, in_target_band, region_file, nodes: [...]}
#   }

import csv, json, os, random, re as _re, sys
from collections import defaultdict
from pathlib import Path

# ── Hard guard ─────────────────────────────────────────────────────────────────
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY is loaded — HALT. $0 assertion failed.')

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
WALLABY_DIR  = SCRIPT_DIR.parent
CSV_PATH     = WALLABY_DIR / 'runs' / 'foray_discovery_S71' / 'node_size_distribution.csv'
SECRETS_ENV  = WALLABY_DIR / 'secrets' / 'floor_db.env'
OUT_DIR      = WALLABY_DIR / 'runs' / 'foray_diagnostic_S71'
OUT_JSON     = OUT_DIR / 'region_frozen_S71.json'
REGIONS_DIR  = WALLABY_DIR / 'runs' / 'foray_discovery_S71' / 'regions'

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Constants ──────────────────────────────────────────────────────────────────
SENTINEL = '00000000-0000-4000-8000-000000000000'
RATIO    = 0.72

# ── Load DB URL ─────────────────────────────────────────────────────────────────
db_url = None
for line in SECRETS_ENV.read_text(encoding='utf-8').splitlines():
    m = _re.match(r'^\s*SUPABASE_DB_URL\s*=\s*(.+)$', line)
    if m:
        db_url = m.group(1).strip().strip('"').strip("'")
if not db_url:
    sys.exit('ERROR: SUPABASE_DB_URL not found in floor_db.env')

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

# ── render_block — VERBATIM from foray_draw_S71_replB.py ─────────────────────
def render_block(b):
    btype = b.get('type', '')
    if btype == 'text':
        return b.get('text', '') or ''
    if btype == 'thinking':
        t = b.get('thinking') or b.get('text', '') or ''
        return f'[THINKING]\n{t}'
    if btype == 'tool_use':
        name = b.get('name', '')
        inp  = json.dumps(b.get('input', {}), indent=2, default=str)
        return f'[TOOL_USE: {name}]\n{inp}'
    if btype == 'tool_result':
        name    = b.get('name', '') or ''
        content = b.get('content', '')
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    parts.append(item.get('text', '') or '')
            text = '\n'.join(parts)
        else:
            text = str(content)
        header = f'[TOOL_RESULT: {name}]' if name else '[TOOL_RESULT]'
        return f'{header}\n{text}'
    return f'[{btype.upper()}]\n{json.dumps(b, default=str)}'

# ── render_arm — reads nodes from floor (reach_up=1, reach_down=0, scrub_v3) ──
def render_arm(nodes, arm_label):
    """Renders nodes from floor. Returns (rendered_chars, payload_str)."""
    import psycopg
    print(f'\nRendering {arm_label} arm from floor ({len(nodes)} nodes) ...')
    conv_groups = defaultdict(list)
    for n in nodes:
        conv_groups[n['conv_uuid']].append(n)

    node_contents = {}
    with psycopg.connect(db_url) as conn:
        conn.autocommit = False
        with conn.cursor() as cur:
            for conv_uuid, cnodes in conv_groups.items():
                cur.execute("""
                    SELECT DISTINCT ON (msg_uuid)
                        msg_uuid::text,
                        parent_message_uuid::text,
                        is_root,
                        content_blocks,
                        created_at
                    FROM floor_conv_messages
                    WHERE conv_uuid = %s::uuid
                      AND scrub_version = 3
                    ORDER BY msg_uuid, created_at
                """, (conv_uuid,))
                msg_rows = cur.fetchall()

                msg_map = {}
                for (muuid, puuid, is_root, cblocks, created_at) in msg_rows:
                    parent_out = None if (is_root or puuid == SENTINEL or puuid is None) else puuid
                    msg_map[muuid] = {
                        'parent':     parent_out,
                        'blocks':     cblocks if isinstance(cblocks, list) else [],
                        'created_at': created_at,
                    }

                children_map = defaultdict(list)
                for muuid, info in msg_map.items():
                    if info['parent']:
                        children_map[info['parent']].append(muuid)

                for n in cnodes:
                    anchor_msg = n['anchor_msg']
                    reach_up   = 1
                    reach_down = 0

                    if anchor_msg not in msg_map:
                        node_contents[(conv_uuid, anchor_msg)] = '[anchor not in v3 floor]'
                        continue

                    ancestors = []
                    cur_msg = anchor_msg
                    for _ in range(reach_up):
                        parent = msg_map[cur_msg]['parent']
                        if parent is None or parent not in msg_map:
                            break
                        ancestors.append(parent)
                        cur_msg = parent
                    ancestors.reverse()

                    descendants = []
                    cur_msg = anchor_msg
                    for _ in range(reach_down):
                        children = children_map.get(cur_msg, [])
                        if not children:
                            break
                        best = sorted(children, key=lambda c: msg_map[c]['created_at'], reverse=True)[0]
                        descendants.append(best)
                        cur_msg = best

                    span_uuids = ancestors + [anchor_msg] + descendants
                    parts = []
                    for muuid in span_uuids:
                        info = msg_map.get(muuid)
                        if info is None:
                            continue
                        for b in info['blocks']:
                            if isinstance(b, dict):
                                rendered = render_block(b)
                                if rendered:
                                    parts.append(rendered)

                    node_contents[(conv_uuid, anchor_msg)] = '\n'.join(parts)
        conn.rollback()

    print(f'  Rendered {len(node_contents)} nodes from floor.')
    region_lines = [
        f'APPARATUS REGION — {arm_label.upper()}',
        f'Node count: {len(nodes)}',
        f'Multi-conv: {len(conv_groups)} distinct convs',
        '=' * 60,
        '',
    ]
    for i, n in enumerate(nodes, 1):
        key = (n['conv_uuid'], n['anchor_msg'])
        content = node_contents.get(key, '[not rendered]')
        region_lines += [
            f'--- NODE {i} [{n["conv_uuid"][:8]}.../{n["anchor_msg"][:8]}...] tok_hi≈{n["tok_hi"]:,} ---',
            content,
            '',
        ]
    payload = '\n'.join(region_lines)
    rendered_chars = len(payload)
    print(f'  Payload: {rendered_chars:,} chars / ~{int(rendered_chars * RATIO):,} tok_hi_est')
    return rendered_chars, payload

# ── Render small and oversized arms (medium is state-advance only) ─────────────
small_rendered_chars, small_payload         = render_arm(nodes_small,     'small')
oversized_rendered_chars, oversized_payload = render_arm(nodes_oversized, 'oversized')

small_tok_hi_est     = int(small_rendered_chars * RATIO)
oversized_tok_hi_est = int(oversized_rendered_chars * RATIO)

# ── ONE-TIME tiktoken ratio check on small arm ─────────────────────────────────
print('\n-- Tiktoken ratio check (one-time, small arm) --')
try:
    import tiktoken
    enc = tiktoken.get_encoding('cl100k_base')
    real_count = len(enc.encode(small_payload))
    delta_pct  = (real_count - small_tok_hi_est) / small_tok_hi_est * 100 if small_tok_hi_est else 0.0
    print(f'  tiktoken cl100k_base: {real_count:,} tokens')
    print(f'  0.72 estimate:        {small_tok_hi_est:,} tokens')
    print(f'  delta:                {delta_pct:+.1f}%')
    if abs(delta_pct) <= 5.0:
        print(f'RATIO CONFIRMED: 0.72 within {abs(delta_pct):.1f}% of tiktoken cl100k_base')
    else:
        print(f'RATIO DEVIATION: real={real_count} est={small_tok_hi_est} delta={delta_pct:+.1f}%')
        sys.exit('HALT for Jake before propagating — ratio outside ±5%')
except ImportError:
    print('  tiktoken not available — ratio unverified, proceeding with 0.72 as estimate')

# ── Target-band check (vs rendered estimate, not CSV sum) ──────────────────────
SMALL_BAND_LO,     SMALL_BAND_HI     = 100_000,   250_000
OVERSIZED_BAND_LO, OVERSIZED_BAND_HI = 500_000, 1_200_000

small_in_band     = SMALL_BAND_LO     <= small_tok_hi_est     <= SMALL_BAND_HI
oversized_in_band = OVERSIZED_BAND_LO <= oversized_tok_hi_est <= OVERSIZED_BAND_HI

if not small_in_band:
    print(f'WARNING: small rendered_payload_tok_hi_est={small_tok_hi_est:,} outside band '
          f'[{SMALL_BAND_LO:,},{SMALL_BAND_HI:,}]')
if not oversized_in_band:
    print(f'WARNING: oversized rendered_payload_tok_hi_est={oversized_tok_hi_est:,} outside band '
          f'[{OVERSIZED_BAND_LO:,},{OVERSIZED_BAND_HI:,}]')

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
        'arm':                       'baseline',
        'region_file':               str(REGIONS_DIR / 'region_small.txt'),
        'total_nodes':               len(nodes_small),
        'total_csv_tok_hi':          sum(n['tok_hi'] for n in nodes_small),
        'rendered_chars':            small_rendered_chars,
        'rendered_payload_tok_hi_est': small_tok_hi_est,
        'in_target_band':            small_in_band,
        'nodes':                     build_node_list(nodes_small),
    },
    'medium': {
        'arm':              'intermediate_state_only',
        'region_file':      str(REGIONS_DIR / 'region_medium.txt'),
        'total_nodes':      len(nodes_medium),
        'total_csv_tok_hi': sum(n['tok_hi'] for n in nodes_medium),
        'nodes':            build_node_list(nodes_medium),
    },
    'oversized': {
        'arm':                       'question',
        'region_file':               str(REGIONS_DIR / 'region_oversized.txt'),
        'total_nodes':               len(nodes_oversized),
        'total_csv_tok_hi':          sum(n['tok_hi'] for n in nodes_oversized),
        'rendered_chars':            oversized_rendered_chars,
        'rendered_payload_tok_hi_est': oversized_tok_hi_est,
        'in_target_band':            oversized_in_band,
        'nodes':                     build_node_list(nodes_oversized),
    },
}

# ── Verification ───────────────────────────────────────────────────────────────
TARGET_SMALL_NODES     = 7
TARGET_OVERSIZED_NODES = 38

errors = []
if frozen['small']['total_nodes'] != TARGET_SMALL_NODES:
    errors.append(f"small node count: got {frozen['small']['total_nodes']}, expected {TARGET_SMALL_NODES}")
if frozen['oversized']['total_nodes'] != TARGET_OVERSIZED_NODES:
    errors.append(f"oversized node count: got {frozen['oversized']['total_nodes']}, expected {TARGET_OVERSIZED_NODES}")

# Cross-verify NODE N headers in region files.
# Headers use truncated IDs: conv_uuid[:8] and anchor_msg[:8].
header_re = _re.compile(r'^--- NODE (\d+) \[([0-9a-f]+)\.\.\./([0-9a-f]+)\.\.\.\]', _re.MULTILINE)

oversized_region_path = Path(frozen['oversized']['region_file'])
if oversized_region_path.exists():
    region_text = oversized_region_path.read_text(encoding='utf-8')
    file_nodes = {}
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
        errors.extend(mismatches[:10])
        if len(mismatches) > 10:
            errors.append(f"... and {len(mismatches)-10} more mismatches")
    else:
        print(f'  Cross-check PASS: all {TARGET_OVERSIZED_NODES} NODE headers match frozen set.')
else:
    print(f'  WARNING: region file not found at {oversized_region_path} — skipping cross-check')

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
print(f'  small:     {frozen["small"]["total_nodes"]} nodes  '
      f'csv_tok_hi {frozen["small"]["total_csv_tok_hi"]:,}  '
      f'rendered_tok_hi_est {frozen["small"]["rendered_payload_tok_hi_est"]:,}  '
      f'in_target_band={frozen["small"]["in_target_band"]}')
print(f'  medium:    {frozen["medium"]["total_nodes"]} nodes  '
      f'csv_tok_hi {frozen["medium"]["total_csv_tok_hi"]:,}  '
      f'(state-advance only — no render)')
print(f'  oversized: {frozen["oversized"]["total_nodes"]} nodes  '
      f'csv_tok_hi {frozen["oversized"]["total_csv_tok_hi"]:,}  '
      f'rendered_tok_hi_est {frozen["oversized"]["rendered_payload_tok_hi_est"]:,}  '
      f'in_target_band={frozen["oversized"]["in_target_band"]}')

# ── Write JSON ─────────────────────────────────────────────────────────────────
OUT_JSON.write_text(json.dumps(frozen, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'\nWrote {OUT_JSON}')

# ── Manifest ───────────────────────────────────────────────────────────────────
print()
print('=== CHANGE MANIFEST ===')
print(f'  {OUT_JSON}')
print(f'  small:     {frozen["small"]["total_nodes"]} nodes  '
      f'csv_tok_hi {frozen["small"]["total_csv_tok_hi"]:,}  '
      f'rendered_tok_hi_est {frozen["small"]["rendered_payload_tok_hi_est"]:,}')
print(f'  oversized: {frozen["oversized"]["total_nodes"]} nodes  '
      f'csv_tok_hi {frozen["oversized"]["total_csv_tok_hi"]:,}  '
      f'rendered_tok_hi_est {frozen["oversized"]["rendered_payload_tok_hi_est"]:,}')
print(f'  ANTHROPIC_API_KEY: NOT loaded (guard passed)')
print(f'  Floor: READ-ONLY (render pass only)')
print(f'  Writes: region_frozen_S71.json only')
