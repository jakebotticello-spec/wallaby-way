# foray_draw_S71_replB.py  S71 replB  CC Step 1 — Draw + Render Fresh Region
# Draws a FRESH random region for the Diagnostic Volley Replication B.
# Uses a fresh seed (distinct from S71's 20260620).
# NO tok_hi filter — whale-nodes stay eligible per replB spec.
# Accretes distinct-conv nodes until total tok_hi enters [678K, 828K].
# Renders the region from the floor verbatim.
# $0, read-only against floor, writes ONLY to runs/foray_diagnostic_S71_replB/.
#
# Output:
#   runs/foray_diagnostic_S71_replB/region_frozen_S71_replB.json
#   runs/foray_diagnostic_S71_replB/region_S71_replB.txt

import csv, json, os, random, re, sys
from collections import defaultdict
from pathlib import Path

# ── Hard guard ──────────────────────────────────────────────────────────────────
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY is loaded — HALT. $0 assertion failed.')

# ── Paths ────────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
WALLABY_DIR  = SCRIPT_DIR.parent
CSV_PATH     = WALLABY_DIR / 'runs' / 'foray_discovery_S71' / 'node_size_distribution.csv'
SECRETS_ENV  = WALLABY_DIR / 'secrets' / 'floor_db.env'
OUT_DIR      = WALLABY_DIR / 'runs' / 'foray_diagnostic_S71_replB'
OUT_JSON     = OUT_DIR / 'region_frozen_S71_replB.json'
OUT_REGION   = OUT_DIR / 'region_S71_replB.txt'

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Fresh seed (replB — distinct from S71's 20260620) ──────────────────────────
SEED = 20260621
BAND_LO = 678_000
BAND_HI = 828_000
SENTINEL = '00000000-0000-4000-8000-000000000000'

# ── Read ALL 7,383 rows — no tok_hi filter (whale-nodes stay eligible) ──────────
print(f'Reading {CSV_PATH} ...')
all_nodes = []
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        tok_hi = int(r['tok_hi'])
        all_nodes.append({
            'conv_uuid':      r['conv_uuid'],
            'anchor_msg':     r['anchor_msg'],
            'rendered_chars': int(r['rendered_chars']),
            'tok_hi':         tok_hi,
        })

print(f'  Total rows (no filter): {len(all_nodes):,}')
max_tok = max(n['tok_hi'] for n in all_nodes)
print(f'  Max tok_hi in pile: {max_tok:,}')

# ── Draw: distinct-conv, accrete until total in [678K, 828K] ────────────────────
random.seed(SEED)
pool = list(all_nodes)
random.shuffle(pool)

used_convs = set()
chosen = []
total_tok_hi = 0

for n in pool:
    if n['conv_uuid'] in used_convs:
        continue
    new_total = total_tok_hi + n['tok_hi']
    # If this node would push us from below-band to above-band in one step, skip it.
    # (Keeps the band reachable; whale-nodes can still be drawn if we're near the floor.)
    if total_tok_hi < BAND_LO and new_total > BAND_HI:
        continue
    total_tok_hi = new_total
    chosen.append(n)
    used_convs.add(n['conv_uuid'])
    if BAND_LO <= total_tok_hi <= BAND_HI:
        break
    if total_tok_hi > BAND_HI:
        break  # safety — shouldn't reach here after the skip above

if not (BAND_LO <= total_tok_hi <= BAND_HI):
    print(f'WARNING: total tok_hi {total_tok_hi:,} is outside band [{BAND_LO:,}, {BAND_HI:,}]')
    print(f'         Proceeding with {total_tok_hi:,} tok_hi — may be slightly outside target.')

print(f'\nDraw result: {len(chosen)} nodes from {len(set(n["conv_uuid"] for n in chosen))} distinct convs')
print(f'Total tok_hi: {total_tok_hi:,} (band: {BAND_LO:,}–{BAND_HI:,})')

# ── Verify distinct convs ────────────────────────────────────────────────────────
conv_set = set(n['conv_uuid'] for n in chosen)
if len(conv_set) != len(chosen):
    sys.exit(f'INTEGRITY FAIL: {len(chosen)} nodes but only {len(conv_set)} distinct convs.')

# ── Load DB URL ──────────────────────────────────────────────────────────────────
db_url = None
for line in SECRETS_ENV.read_text(encoding='utf-8').splitlines():
    m = re.match(r'^\s*SUPABASE_DB_URL\s*=\s*(.+)$', line)
    if m:
        db_url = m.group(1).strip().strip('"').strip("'")
if not db_url:
    sys.exit('ERROR: SUPABASE_DB_URL not found in floor_db.env')

# ── render_block — VERBATIM from floor_extract.py:37-62 ──────────────────────────
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

# ── Render region from floor ─────────────────────────────────────────────────────
print('\nRendering region from floor ...')
import psycopg

conv_groups = defaultdict(list)
for n in chosen:
    conv_groups[n['conv_uuid']].append(n)

node_contents = {}

with psycopg.connect(db_url) as conn:
    conn.autocommit = False
    with conn.cursor() as cur:
        for conv_uuid, nodes in conv_groups.items():
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

            for n in nodes:
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

# ── Build region payload ──────────────────────────────────────────────────────────
region_lines = [
    'APPARATUS REGION — REPLB',
    f'Node count: {len(chosen)}',
    f'Multi-conv: {len(conv_groups)} distinct convs',
    '=' * 60,
    '',
]

total_rendered_chars = 0
for i, n in enumerate(chosen, 1):
    key = (n['conv_uuid'], n['anchor_msg'])
    content = node_contents.get(key, '[not rendered]')
    total_rendered_chars += len(content)
    region_lines += [
        f'--- NODE {i} [{n["conv_uuid"][:8]}.../{n["anchor_msg"][:8]}...] tok_hi≈{n["tok_hi"]:,} ---',
        content,
        '',
    ]

payload = '\n'.join(region_lines)
OUT_REGION.write_text(payload, encoding='utf-8')
actual_chars = len(payload)
actual_tok_hi_est = int(actual_chars * 0.72)
print(f'  Wrote {OUT_REGION}')
print(f'  Payload: {actual_chars:,} chars / ~{actual_tok_hi_est:,} tok_hi_est')

# ── Build frozen JSON ────────────────────────────────────────────────────────────
node_list = [
    {
        'node_number': i + 1,
        'conv_uuid':   n['conv_uuid'],
        'anchor_msg':  n['anchor_msg'],
        'tok_hi':      n['tok_hi'],
    }
    for i, n in enumerate(chosen)
]

frozen = {
    'seed':           SEED,
    'arm':            'question',
    'region_file':    str(OUT_REGION),
    'total_nodes':    len(chosen),
    'total_tok_hi':   total_tok_hi,
    'payload_chars':  actual_chars,
    'tok_hi_est':     actual_tok_hi_est,
    'band_lo':        BAND_LO,
    'band_hi':        BAND_HI,
    'nodes':          node_list,
}

OUT_JSON.write_text(json.dumps(frozen, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'  Wrote {OUT_JSON}')

# ── Band check ────────────────────────────────────────────────────────────────────
if BAND_LO <= total_tok_hi <= BAND_HI:
    print(f'\nBAND CHECK: PASS — {total_tok_hi:,} tok_hi in [{BAND_LO:,}, {BAND_HI:,}]')
else:
    print(f'\nBAND CHECK: OUTSIDE BAND — {total_tok_hi:,} tok_hi (band: [{BAND_LO:,}, {BAND_HI:,}])')

# ── Change manifest ───────────────────────────────────────────────────────────────
print()
print('=== CHANGE MANIFEST ===')
print(f'  {OUT_JSON}   ({len(node_list)} nodes, {total_tok_hi:,} tok_hi)')
print(f'  {OUT_REGION}   ({actual_chars:,} chars, ~{actual_tok_hi_est:,} tok_hi_est)')
print(f'  Seed: {SEED}')
print(f'  ANTHROPIC_API_KEY: NOT loaded (guard passed)')
print(f'  Floor: READ-ONLY (no writes, rollback)')
print(f'  Writes: ONLY under runs/foray_diagnostic_S71_replB/')
print(f'  Whale-nodes: ELIGIBLE (no tok_hi filter)')
print(f'  Distinct convs: {len(conv_groups)}')
