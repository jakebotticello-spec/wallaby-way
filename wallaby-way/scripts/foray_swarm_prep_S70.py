# foray_swarm_prep_S70.py  S70  CC Task 2 of 2
# Preprocessing for the Probe Swarm leash measurement.
# Selects candidate convs per payload-size bin × density stratum,
# renders floor payloads, writes probe_manifest.json.
# $0, read-only, no paid API.
#
# Terminology (per Jake's S70 correction):
#   - "node" = (conv_uuid, anchor_msg) pair, NOT a conv
#   - "rung" here = approx message count of the whole-conv test vehicle
#   - We are measuring PAYLOAD SIZE using whole convs as test vehicles
#   - Leash will be stated in tok_hi (primary), node-count derived
#
# Render path: render_block() VERBATIM from floor_extract.py:37-62

import csv, json, os, re, sys, statistics
from pathlib import Path

# ── Guard ─────────────────────────────────────────────────────────────────────
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY is loaded — HALT. $0 assertion failed.')

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
SECRETS_ENV  = SCRIPT_DIR.parent / 'secrets' / 'floor_db.env'
OUT_DIR      = SCRIPT_DIR.parent / 'runs' / 'foray_S70'
REGIONS_DIR  = OUT_DIR / 'regions'
CENSUS_CSV   = OUT_DIR / 'per_conv_census.csv'
MANIFEST_OUT = OUT_DIR / 'probe_manifest.json'
REGIONS_DIR.mkdir(parents=True, exist_ok=True)

# ── Load DB URL ────────────────────────────────────────────────────────────────
db_url = None
for line in SECRETS_ENV.read_text(encoding='utf-8').splitlines():
    m = re.match(r'^\s*SUPABASE_DB_URL\s*=\s*(.+)$', line)
    if m:
        db_url = m.group(1).strip().strip('"').strip("'")
if not db_url:
    sys.exit('ERROR: SUPABASE_DB_URL not found in floor_db.env')

# ── render_block — VERBATIM from floor_extract.py:37-62 ──────────────────────
import json as _json
def render_block(b):
    btype = b.get('type', '')
    if btype == 'text':
        return b.get('text', '') or ''
    if btype == 'thinking':
        t = b.get('thinking') or b.get('text', '') or ''
        return f'[THINKING]\n{t}'
    if btype == 'tool_use':
        name = b.get('name', '')
        inp  = _json.dumps(b.get('input', {}), indent=2, default=str)
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
    return f'[{btype.upper()}]\n{_json.dumps(b, default=str)}'
# ── end verbatim ──────────────────────────────────────────────────────────────

SENTINEL = '00000000-0000-4000-8000-000000000000'

# ── Read Task 1 census ────────────────────────────────────────────────────────
all_convs = []
with open(CENSUS_CSV, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        all_convs.append({
            'conv_uuid':     r['conv_uuid'],
            'msg_count':     int(r['msg_count']),
            'chars':         int(r['chars']),
            'content_chars': int(r['content_chars']),
            'tok_lo':        int(r['tok_lo']),
            'tok_hi':        int(r['tok_hi']),
            'density':       int(r['content_chars']) / int(r['msg_count']) if int(r['msg_count']) > 0 else 0,
        })

# ── Compute per-node tok_hi (conversion factor for leash derivation) ──────────
# Per-node tok_hi ≈ tok_hi / msg_count for each conv, then take median.
# Grain: (conv_uuid, anchor_msg) pair approximated as message count.
# Note: this approximation treats msg_count as a proxy for node count within
# a conv; true node count varies by content, but msg is the floor's atomic unit.
per_node_tok_hi_vals = [r['tok_hi'] / r['msg_count'] for r in all_convs if r['msg_count'] > 0]
median_per_node_tok_hi = statistics.median(per_node_tok_hi_vals)
print(f'Median per-node tok_hi (tok_hi/msg_count): {median_per_node_tok_hi:,.1f}')

# ── Rung definitions (non-overlapping message count bins) ─────────────────────
# "Rung" here = payload-size bin using whole-conv message count as the axis.
# NOT "N nodes from floor" — whole convs are the test vehicles.
RUNG_DEFS = [
    ('rung05',  1,  7),
    ('rung10',  8, 14),
    ('rung20', 15, 28),
    ('rung35', 29, 48),
    ('rung55', 49, 75),
]

def pct(lst, p):
    if not lst:
        return 0
    s = sorted(lst)
    n = len(s)
    idx = p / 100 * (n - 1)
    lo, hi = int(idx), min(int(idx) + 1, n - 1)
    return s[lo] + (idx - lo) * (s[hi] - s[lo])

# ── Input context ceiling (on-sub 200K token window) ─────────────────────────
# Boot_ScopeReader_v4.1 ≈ 4K tokens; leaves ~196K tokens for payload.
# At chars × 0.32 (prose): 196K tok ≈ 612K chars.
# At chars × 0.72 (code-dense): 196K tok ≈ 272K chars.
WALL_C_CHARS_THRESHOLD = 612_000   # above this = WALL_C-risk (liberal estimate)

# ── Sample convs per rung ─────────────────────────────────────────────────────
# Oversample dense tail (p75+): 4 per stratum; lighter strata: 2 per stratum.
selected = []

for rung_label, lo, hi in RUNG_DEFS:
    pool = [r for r in all_convs if lo <= r['msg_count'] <= hi]
    if not pool:
        print(f'{rung_label}: no convs in range {lo}-{hi}')
        continue
    pool.sort(key=lambda r: r['density'])
    densities = [r['density'] for r in pool]
    n = len(pool)

    # Assign stratum labels based on density percentile within this rung's pool
    strata_bounds = {
        'sparse':       (0,   25),
        'medium-lo':    (25,  50),
        'medium-hi':    (50,  75),
        'dense':        (75,  90),
        'very-dense':   (90,  95),
        'extreme':      (95, 100),
    }

    for r in pool:
        d = r['density']
        for stratum, (lo_pct, hi_pct) in strata_bounds.items():
            lo_val = pct(densities, lo_pct)
            hi_val = pct(densities, hi_pct)
            if d >= lo_val and (d < hi_val or hi_pct == 100):
                r['density_stratum'] = stratum
                r['rung'] = rung_label
                break

    # Sample: lighter strata → 2 convs each; dense+ strata → 3-4 each
    stratum_counts = {
        'sparse':      2,
        'medium-lo':   2,
        'medium-hi':   2,
        'dense':       3,
        'very-dense':  4,
        'extreme':     4,
    }

    per_stratum = {}
    for r in pool:
        s = r.get('density_stratum', 'sparse')
        per_stratum.setdefault(s, []).append(r)

    rung_selected = []
    for stratum, want in stratum_counts.items():
        candidates = per_stratum.get(stratum, [])
        # Pick: lowest, highest, and middle densities within stratum for spread
        candidates.sort(key=lambda r: r['density'])
        if len(candidates) <= want:
            rung_selected.extend(candidates)
        else:
            # Pick spread: evenly spaced across the stratum
            indices = [int(i * (len(candidates) - 1) / (want - 1)) for i in range(want)]
            rung_selected.extend(candidates[i] for i in sorted(set(indices)))

    print(f'{rung_label} (msg {lo}-{hi}): pool={n}, selected={len(rung_selected)}')
    selected.extend(rung_selected)

print(f'Total selected for rendering: {len(selected)}')

# ── Render floor payloads ─────────────────────────────────────────────────────
import psycopg

print('Connecting to floor DB for payload rendering ...')
manifest_entries = []

with psycopg.connect(db_url) as conn:
    conn.autocommit = False

    with conn.cursor() as cur:
        for i, conv in enumerate(selected):
            conv_uuid = conv['conv_uuid']
            print(f'  [{i+1}/{len(selected)}] {conv_uuid[:8]}  rung={conv["rung"]}  stratum={conv["density_stratum"]}  chars={conv["chars"]:,}', end='', flush=True)

            # Fetch v3 messages for this conv
            cur.execute("""
                SELECT
                    msg_uuid::text,
                    parent_message_uuid::text,
                    is_root,
                    sender,
                    content_blocks,
                    created_at,
                    snapshot_id
                FROM floor_conv_messages
                WHERE conv_uuid = %s::uuid
                  AND scrub_version = 3
                ORDER BY created_at
            """, (conv_uuid,))
            msg_rows = cur.fetchall()

            if not msg_rows:
                print('  ← SKIP (no v3 rows)')
                continue

            # Build payload (same format as floor_extract.py)
            snapshot_id   = msg_rows[0][6]
            first_created = msg_rows[0][5]
            actual_msg_count = len(msg_rows)

            header_lines = [
                f'CONVERSATION: {conv_uuid}',
                f'SNAPSHOT_ID: {snapshot_id}',
                f'CREATED: {first_created}',
                f'MESSAGES: {actual_msg_count}',
                '',
            ]

            msg_lines = []
            for (msg_uuid, parent_uuid, is_root, sender, content_blocks, created_at, snap_id) in msg_rows:
                parent_out = 'null' if (is_root or parent_uuid == SENTINEL or parent_uuid is None) else parent_uuid
                blocks = content_blocks if isinstance(content_blocks, list) else []
                parts  = [render_block(b) for b in blocks if isinstance(b, dict)]
                content_text = '\n'.join(p for p in parts if p)
                msg_lines.extend([
                    '===MSG===',
                    f'uuid: {msg_uuid}',
                    f'parent: {parent_out}',
                    f'role: {sender}',
                    '---',
                    content_text,
                    '===END===',
                    '',
                ])

            payload = '\n'.join(header_lines + msg_lines)

            # Write payload file
            # §7: payload files contain rendered floor content (scrub-v3 screened);
            # no DB URL or raw credential in payload content.
            payload_path = REGIONS_DIR / f'{conv_uuid}_rung{conv["rung"]}_payload.txt'
            payload_path.write_text(payload, encoding='utf-8')

            wall_c_risk = len(payload) > WALL_C_CHARS_THRESHOLD
            print(f'  -> {len(payload):,} chars  wall_c_risk={wall_c_risk}')

            manifest_entries.append({
                'conv_uuid':       conv_uuid,
                'rung':            conv['rung'],
                'msg_count':       actual_msg_count,
                'chars':           len(payload),
                'content_chars':   conv['content_chars'],
                'tok_lo':          int(len(payload) * 0.32),
                'tok_hi':          int(len(payload) * 0.72),
                'density':         round(conv['density'], 1),
                'density_stratum': conv['density_stratum'],
                'wall_c_risk':     wall_c_risk,
                'payload_path':    str(payload_path),
            })

    conn.rollback()

# ── Write manifest ─────────────────────────────────────────────────────────────
MANIFEST_OUT.write_text(
    json.dumps({
        'median_per_node_tok_hi':   round(median_per_node_tok_hi, 1),
        'wall_c_chars_threshold':   WALL_C_CHARS_THRESHOLD,
        'wall_c_convs':             sum(1 for e in manifest_entries if e['wall_c_risk']),
        'total_regions':            len(manifest_entries),
        'note_node_grain':          '(conv_uuid, anchor_msg) pair — NOT conv-count, NOT node-index. Index count overstates distinct pairs by ~10% (8,288 indices → 7,469 distinct, AstroSynapses.md).',
        'regions':                  manifest_entries,
    }, indent=2, ensure_ascii=False),
    encoding='utf-8'
)
print(f'\nWrote manifest: {MANIFEST_OUT}  ({len(manifest_entries)} regions)')
print(f'  WALL_C-risk regions (chars > {WALL_C_CHARS_THRESHOLD:,}): {sum(1 for e in manifest_entries if e["wall_c_risk"])}')
print(f'  Median per-node tok_hi (conversion factor): {median_per_node_tok_hi:,.1f}')
