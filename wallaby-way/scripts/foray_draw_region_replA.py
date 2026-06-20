# foray_draw_region_replA.py  S71 replA  CC Step 1
# Draws a FRESH random ~144K region from the full 7,383-node pool (no whale exclusion).
# Stops at first node that lands cumulative RENDERED tok_hi in [130K-158K].
# $0, floor READ-ONLY, writes only to wallaby-way/runs/foray_diagnostic_S71_replA/
#
# Output:
#   region_frozen_S71_replA.json  -- frozen (conv_uuid, anchor_msg, tok_hi) list
#   region_replA.txt              -- rendered payload (reach=1/0 approximation)

import csv, json, os, random, re, sys
from collections import defaultdict
from pathlib import Path

# ── Hard guard ─────────────────────────────────────────────────────────────────
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY is loaded -- HALT. $0 assertion failed.')

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
WALLABY_DIR  = SCRIPT_DIR.parent
CSV_PATH     = WALLABY_DIR / 'runs' / 'foray_discovery_S71' / 'node_size_distribution.csv'
SECRETS_ENV  = WALLABY_DIR / 'secrets' / 'floor_db.env'
OUT_DIR      = WALLABY_DIR / 'runs' / 'foray_diagnostic_S71_replA'
OUT_JSON     = OUT_DIR / 'region_frozen_S71_replA.json'
OUT_REGION   = OUT_DIR / 'region_replA.txt'

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Band parameters ────────────────────────────────────────────────────────────
BAND_LO = 130_000   # rendered tok_hi lower bound
BAND_HI = 158_000   # rendered tok_hi upper bound

# ── Load DB URL ────────────────────────────────────────────────────────────────
db_url = None
for line in SECRETS_ENV.read_text(encoding='utf-8').splitlines():
    m = re.match(r'^\s*SUPABASE_DB_URL\s*=\s*(.+)$', line)
    if m:
        db_url = m.group(1).strip().strip('"').strip("'")
if not db_url:
    sys.exit('ERROR: SUPABASE_DB_URL not found in floor_db.env')

# ── render_block -- VERBATIM from floor_extract.py ─────────────────────────────
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
            parts = [item.get('text', '') or '' for item in content if isinstance(item, dict)]
            text = '\n'.join(parts)
        else:
            text = str(content)
        header = f'[TOOL_RESULT: {name}]' if name else '[TOOL_RESULT]'
        return f'{header}\n{text}'
    return f'[{btype.upper()}]\n{json.dumps(b, default=str)}'

SENTINEL = '00000000-0000-4000-8000-000000000000'

def render_single_node(conn, conv_uuid, anchor_msg):
    """Render one node (reach=1/0) from the floor. Returns rendered content string."""
    with conn.cursor() as cur:
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

    if anchor_msg not in msg_map:
        return '[anchor not in v3 floor]'

    # Walk up 1
    ancestors = []
    cur_msg = anchor_msg
    parent = msg_map[cur_msg]['parent']
    if parent and parent in msg_map:
        ancestors.append(parent)

    span_uuids = ancestors + [anchor_msg]
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

    return '\n'.join(parts)

# ── Read CSV -- NO tok_hi filter (whale-nodes eligible per replA spec) ──────────
print(f'Reading {CSV_PATH} ...')
all_nodes = []
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        all_nodes.append({
            'conv_uuid':  r['conv_uuid'],
            'anchor_msg': r['anchor_msg'],
            'tok_hi':     int(r['tok_hi']),
        })

print(f'  Total pool (no filter): {len(all_nodes):,} nodes')
whale_count = sum(1 for n in all_nodes if n['tok_hi'] > 200_000)
print(f'  Of which whale-scale (tok_hi > 200K): {whale_count}')

# ── Deterministic seed -- fresh for replA ──────────────────────────────────────
SEED = 130
random.seed(SEED)
print(f'  Seed: {SEED}')

# ── Shuffle draw pool ─────────────────────────────────────────────────────────
pool = list(all_nodes)
random.shuffle(pool)

# ── Draw nodes one by one, render each, stop when cumulative rendered tok_hi enters band ──
print(f'\nDrawing nodes (render-per-node, stop when cumulative rendered tok_hi in [{BAND_LO:,}-{BAND_HI:,}]) ...')

import psycopg

used_convs = set()
chosen = []
node_rendered_contents = []  # parallel list of rendered content strings
cumulative_rendered_chars = 0

with psycopg.connect(db_url) as conn:
    conn.autocommit = False

    for n in pool:
        if n['conv_uuid'] in used_convs:
            continue

        # Render this node
        content = render_single_node(conn, n['conv_uuid'], n['anchor_msg'])
        node_chars = len(content)
        node_tok_hi = int(node_chars * 0.72)

        chosen.append(n)
        used_convs.add(n['conv_uuid'])
        node_rendered_contents.append(content)
        cumulative_rendered_chars += node_chars

        cumulative_tok_hi = int(cumulative_rendered_chars * 0.72)
        print(f'  Node {len(chosen):2d}: {n["conv_uuid"][:8]}.../{n["anchor_msg"][:8]}...  '
              f'csv_tok_hi={n["tok_hi"]:,}  rendered_chars={node_chars:,}  '
              f'cumulative_tok_hi={cumulative_tok_hi:,}')

        if cumulative_tok_hi >= BAND_LO:
            in_band = cumulative_tok_hi <= BAND_HI
            print(f'  --> Cumulative tok_hi={cumulative_tok_hi:,} >= {BAND_LO:,}  '
                  f'{"IN BAND" if in_band else "OVERSHOT BAND"} -- stopping.')
            break

    conn.rollback()

cumulative_tok_hi_est = int(cumulative_rendered_chars * 0.72)
in_band = BAND_LO <= cumulative_tok_hi_est <= BAND_HI

print(f'\nDraw result:')
print(f'  Nodes: {len(chosen)}  |  Distinct convs: {len(set(n["conv_uuid"] for n in chosen))}')
print(f'  Cumulative rendered chars: {cumulative_rendered_chars:,}')
print(f'  Cumulative rendered tok_hi_est: {cumulative_tok_hi_est:,}')
print(f'  Target band [{BAND_LO:,}-{BAND_HI:,}]: {"IN BAND" if in_band else "OUTSIDE BAND -- note in report"}')

# ── Build frozen JSON ─────────────────────────────────────────────────────────
frozen_nodes = [
    {
        'node_number': i + 1,
        'conv_uuid':   n['conv_uuid'],
        'anchor_msg':  n['anchor_msg'],
        'tok_hi':      n['tok_hi'],
    }
    for i, n in enumerate(chosen)
]

frozen = {
    'seed': SEED,
    'arm':  'replA_baseline',
    'total_nodes':             len(chosen),
    'total_csv_tok_hi':        sum(n['tok_hi'] for n in chosen),
    'rendered_payload_chars':  None,   # updated below after building payload
    'rendered_payload_tok_hi_est': None,
    'in_target_band':          in_band,
    'band_lo':                 BAND_LO,
    'band_hi':                 BAND_HI,
    'notes': (
        'No tok_hi filter (whale-nodes eligible). Distinct-conv draw. Reach=1/0 render. '
        'Stopped at first node that brings cumulative rendered tok_hi into [130K,158K] or first overshoot.'
    ),
    'nodes': frozen_nodes,
}

OUT_JSON.write_text(json.dumps(frozen, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'\nFROZEN (pre-payload): {OUT_JSON}')

# ── Build region payload ───────────────────────────────────────────────────────
region_lines = [
    'APPARATUS REGION -- REPLA BASELINE',
    f'Node count: {len(chosen)}',
    f'Multi-conv: {len(set(n["conv_uuid"] for n in chosen))} distinct convs',
    f'Seed: {SEED}  |  Band target: [{BAND_LO:,}-{BAND_HI:,}]  |  '
    f'Cumulative rendered tok_hi: {cumulative_tok_hi_est:,}',
    '=' * 60,
    '',
]

for i, (n, content) in enumerate(zip(chosen, node_rendered_contents)):
    node_num = i + 1
    region_lines += [
        f'--- NODE {node_num} [{n["conv_uuid"][:8]}.../{n["anchor_msg"][:8]}...] tok_hi~={n["tok_hi"]:,} ---',
        content,
        '',
    ]

payload = '\n'.join(region_lines)
OUT_REGION.write_text(payload, encoding='utf-8')
actual_payload_chars = len(payload)
actual_payload_tok_hi = int(actual_payload_chars * 0.72)

# ── Update frozen JSON with payload info ──────────────────────────────────────
frozen['rendered_payload_chars'] = actual_payload_chars
frozen['rendered_payload_tok_hi_est'] = actual_payload_tok_hi
OUT_JSON.write_text(json.dumps(frozen, indent=2, ensure_ascii=False), encoding='utf-8')

print(f'Region file: {OUT_REGION}')
print(f'  Payload chars: {actual_payload_chars:,}  |  tok_hi_est: {actual_payload_tok_hi:,}')

# ── CHANGE MANIFEST ────────────────────────────────────────────────────────────
print()
print('=== CHANGE MANIFEST ===')
print(f'  CREATED: {OUT_JSON}')
print(f'  CREATED: {OUT_REGION}')
print(f'  Nodes drawn: {len(chosen)}  |  Seed: {SEED}')
print(f'  Cumulative rendered tok_hi (content only): {cumulative_tok_hi_est:,}')
print(f'  Payload chars: {actual_payload_chars:,}  |  Payload tok_hi: {actual_payload_tok_hi:,}')
print(f'  In band [{BAND_LO:,}-{BAND_HI:,}]: {in_band}')
print(f'  ANTHROPIC_API_KEY: NOT loaded (guard passed)')
print(f'  Floor: READ-ONLY (SELECT only, conn.rollback() applied)')
print(f'  Writes: ONLY under {OUT_DIR}')
