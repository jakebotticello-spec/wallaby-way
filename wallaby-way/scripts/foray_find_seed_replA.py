# foray_find_seed_replA.py  -- finds a seed that lands cumulative rendered tok_hi in [130K-158K]
# $0, floor READ-ONLY

import csv, json, os, random, re, sys
from pathlib import Path

if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: HALT')

SCRIPT_DIR   = Path(__file__).parent
WALLABY_DIR  = SCRIPT_DIR.parent
CSV_PATH     = WALLABY_DIR / 'runs' / 'foray_discovery_S71' / 'node_size_distribution.csv'
SECRETS_ENV  = WALLABY_DIR / 'secrets' / 'floor_db.env'

BAND_LO = 130_000
BAND_HI = 158_000
SEEDS_TO_TRY = [7, 10, 20, 31, 34, 45, 51, 63, 80, 89, 92, 106, 110, 115, 120, 130, 150, 200, 250, 300, 400, 500]

db_url = None
for line in SECRETS_ENV.read_text(encoding='utf-8').splitlines():
    m = re.match(r'^\s*SUPABASE_DB_URL\s*=\s*(.+)$', line)
    if m:
        db_url = m.group(1).strip().strip('"').strip("'")

import psycopg

all_nodes = []
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        all_nodes.append({'conv_uuid': r['conv_uuid'], 'anchor_msg': r['anchor_msg'], 'tok_hi': int(r['tok_hi'])})

SENTINEL = '00000000-0000-4000-8000-000000000000'

def render_block(b):
    btype = b.get('type', '')
    if btype == 'text': return b.get('text', '') or ''
    if btype == 'thinking': return f'[THINKING]\n{b.get("thinking") or b.get("text","") or ""}'
    if btype == 'tool_use': return f'[TOOL_USE: {b.get("name","")}]\n{json.dumps(b.get("input",{}),indent=2,default=str)}'
    if btype == 'tool_result':
        content = b.get('content', '')
        if isinstance(content, list):
            text = '\n'.join(item.get('text','') or '' for item in content if isinstance(item,dict))
        else:
            text = str(content)
        return f'[TOOL_RESULT]\n{text}'
    return f'[{btype.upper()}]\n{json.dumps(b,default=str)}'

def render_node(conn, conv_uuid, anchor_msg):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT DISTINCT ON (msg_uuid) msg_uuid::text, parent_message_uuid::text, is_root, content_blocks
            FROM floor_conv_messages
            WHERE conv_uuid = %s::uuid AND scrub_version = 3
            ORDER BY msg_uuid, created_at
        """, (conv_uuid,))
        msg_map = {}
        for (muuid, puuid, is_root, cblocks) in cur.fetchall():
            parent_out = None if (is_root or puuid == SENTINEL or puuid is None) else puuid
            msg_map[muuid] = {'parent': parent_out, 'blocks': cblocks if isinstance(cblocks, list) else []}

    if anchor_msg not in msg_map:
        return ''
    parent = msg_map[anchor_msg]['parent']
    span = ([parent] if parent and parent in msg_map else []) + [anchor_msg]
    parts = []
    for muuid in span:
        for b in msg_map.get(muuid, {}).get('blocks', []):
            if isinstance(b, dict):
                r = render_block(b)
                if r: parts.append(r)
    return '\n'.join(parts)

with psycopg.connect(db_url) as conn:
    conn.autocommit = False
    for seed in SEEDS_TO_TRY:
        rng = random.Random(seed)
        pool = list(all_nodes)
        rng.shuffle(pool)

        used = set()
        chosen = []
        cumulative_chars = 0
        final_tok_hi = 0
        in_band = False

        for n in pool:
            if n['conv_uuid'] in used:
                continue
            content = render_node(conn, n['conv_uuid'], n['anchor_msg'])
            used.add(n['conv_uuid'])
            chosen.append({'conv_uuid': n['conv_uuid'], 'anchor_msg': n['anchor_msg'],
                           'csv_tok_hi': n['tok_hi'], 'rendered_chars': len(content)})
            cumulative_chars += len(content)
            final_tok_hi = int(cumulative_chars * 0.72)
            if final_tok_hi >= BAND_LO:
                in_band = BAND_LO <= final_tok_hi <= BAND_HI
                break

        status = 'IN_BAND' if in_band else ('OVERSHOOT' if final_tok_hi > BAND_HI else 'UNDER')
        print(f'seed={seed:4d}  nodes={len(chosen):2d}  tok_hi={final_tok_hi:,}  {status}')

    conn.rollback()
