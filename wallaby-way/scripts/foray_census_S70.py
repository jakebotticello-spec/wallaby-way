# foray_census_S70.py  S70  CC Task 1 of 2
# Per-conv size census off the scrub-v3 floor. $0, read-only, no API fired.
# Outputs: wallaby-way/runs/foray_S70/per_conv_census.csv + census_summary.md
#
# Columns:
#   chars        = full payload chars (===MSG=== envelopes + conv header included)
#   content_chars = rendered block content only (no envelope, no header)
#   tok_lo/hi    = chars × 0.32 / × 0.72  (prose / code-dense brackets)
#
# Render path: render_block() VERBATIM from floor_extract.py:37-62 (canary-locked).
# Char count: len(str) — Python Unicode chars, not bytes.

import csv
import json
import os
import re
import statistics
import sys
from pathlib import Path

# ── Guard ─────────────────────────────────────────────────────────────────────
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY is loaded — HALT. $0 assertion failed.')

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
SECRETS_ENV = SCRIPT_DIR.parent / 'secrets' / 'floor_db.env'
OUT_DIR     = SCRIPT_DIR.parent / 'runs' / 'foray_S70'
OUT_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH     = OUT_DIR / 'per_conv_census.csv'
SUMMARY_PATH = OUT_DIR / 'census_summary.md'

# ── Load SUPABASE_DB_URL ──────────────────────────────────────────────────────
db_url = None
for line in SECRETS_ENV.read_text(encoding='utf-8').splitlines():
    m = re.match(r'^\s*SUPABASE_DB_URL\s*=\s*(.+)$', line)
    if m:
        db_url = m.group(1).strip().strip('"').strip("'")
if not db_url:
    sys.exit('ERROR: SUPABASE_DB_URL not found in floor_db.env')

# ── render_block — VERBATIM from floor_extract.py:37-62 ──────────────────────
# Do NOT alter. A change here desyncs from the proven whale/extract render path.
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
# ── end verbatim ──────────────────────────────────────────────────────────────

SENTINEL = '00000000-0000-4000-8000-000000000000'

EXPECTED_V3_ROWS  = 29_396
EXPECTED_V3_MSGS  = 29_396
EXPECTED_V3_CONVS = 437    # 440 headers − 3 hollow stubs (no messages)

import psycopg

print('Connecting to floor DB ...')
with psycopg.connect(db_url) as conn:
    conn.autocommit = False

    with conn.cursor() as cur:

        # ── Step 1: Reconciliation ────────────────────────────────────────────
        print('Running reconciliation query ...')
        cur.execute("""
            SELECT
                COUNT(*)                 AS v3_rows,
                COUNT(DISTINCT msg_uuid) AS v3_msgs,
                COUNT(DISTINCT conv_uuid) AS v3_convs
            FROM floor_conv_messages
            WHERE scrub_version = 3
        """)
        v3_rows, v3_msgs, v3_convs = cur.fetchone()

        print(f'  v3_rows  = {v3_rows:,}  (expect {EXPECTED_V3_ROWS:,})')
        print(f'  v3_msgs  = {v3_msgs:,}  (expect {EXPECTED_V3_MSGS:,})')
        print(f'  v3_convs = {v3_convs:,}  (expect {EXPECTED_V3_CONVS:,})')

        deviations = []
        if v3_rows  != EXPECTED_V3_ROWS:
            deviations.append(f'v3_rows: got {v3_rows:,}, expected {EXPECTED_V3_ROWS:,}')
        if v3_msgs  != EXPECTED_V3_MSGS:
            deviations.append(f'v3_msgs: got {v3_msgs:,}, expected {EXPECTED_V3_MSGS:,}')
        if v3_convs != EXPECTED_V3_CONVS:
            deviations.append(f'v3_convs: got {v3_convs:,}, expected {EXPECTED_V3_CONVS:,}')
        if deviations:
            for d in deviations:
                print(f'RECONCILIATION DELTA: {d}')
            sys.exit('RECONCILIATION FAILED — HALT. Delta vs FLOOR_COUNTS.md printed above.')

        print('Reconciliation PASS.')

        # ── Step 2: Full fetch (all v3 rows) ─────────────────────────────────
        print('Fetching all v3 message rows ...')
        cur.execute("""
            SELECT
                conv_uuid::text,
                msg_uuid::text,
                parent_message_uuid::text,
                is_root,
                sender,
                content_blocks,
                created_at,
                snapshot_id
            FROM floor_conv_messages
            WHERE scrub_version = 3
            ORDER BY conv_uuid, created_at
        """)
        rows = cur.fetchall()
        print(f'  Fetched {len(rows):,} rows.')

    conn.rollback()   # read-only; explicit rollback, no commit

# ── Step 3: Render + aggregate ─────────────────────────────────────────────
print('Rendering and aggregating per conv ...')

# Per-conv accumulators
conv_msg_uuids   = {}   # conv_uuid → set of msg_uuids
conv_payload_lines = {}  # conv_uuid → list of payload line strings (full format)
conv_content_parts = {}  # conv_uuid → list of rendered block strings (content only)
conv_meta          = {}  # conv_uuid → (snapshot_id, created_at) of first message

for (conv_uuid, msg_uuid, parent_uuid, is_root, sender,
        content_blocks, created_at, snapshot_id) in rows:

    if conv_uuid not in conv_msg_uuids:
        conv_msg_uuids[conv_uuid]    = set()
        conv_payload_lines[conv_uuid] = []
        conv_content_parts[conv_uuid] = []
        conv_meta[conv_uuid]          = (snapshot_id, created_at)

    conv_msg_uuids[conv_uuid].add(msg_uuid)

    parent_out = 'null' if (is_root or parent_uuid == SENTINEL or parent_uuid is None) else parent_uuid

    blocks = content_blocks if isinstance(content_blocks, list) else []
    parts  = []
    for b in blocks:
        if isinstance(b, dict):
            rendered = render_block(b)
            if rendered:
                parts.append(rendered)

    content_text = '\n'.join(parts)

    # Accumulate rendered block content for content_chars
    if content_text:
        conv_content_parts[conv_uuid].append(content_text)

    # Accumulate full envelope lines for chars
    conv_payload_lines[conv_uuid].extend([
        '===MSG===',
        f'uuid: {msg_uuid}',
        f'parent: {parent_out}',
        f'role: {sender}',
        '---',
        content_text,
        '===END===',
        '',
    ])

# Build per-conv records
records = []
for conv_uuid in sorted(conv_msg_uuids.keys()):
    snapshot_id, first_created_at = conv_meta[conv_uuid]
    msg_count  = len(conv_msg_uuids[conv_uuid])

    # Full payload (header block + message envelopes) — what the reader ingests
    header_lines = [
        f'CONVERSATION: {conv_uuid}',
        f'SNAPSHOT_ID: {snapshot_id}',
        f'CREATED: {first_created_at}',
        f'MESSAGES: {msg_count}',
        '',
    ]
    full_payload = '\n'.join(header_lines + conv_payload_lines[conv_uuid])
    chars = len(full_payload)

    # Content-only chars (block-rendered text, no envelope/header overhead)
    content_chars = sum(len(t) for t in conv_content_parts[conv_uuid])

    tok_lo = int(chars * 0.32)
    tok_hi = int(chars * 0.72)

    records.append({
        'conv_uuid':     conv_uuid,
        'msg_count':     msg_count,
        'chars':         chars,
        'content_chars': content_chars,
        'tok_lo':        tok_lo,
        'tok_hi':        tok_hi,
    })

# Sort by chars DESC (largest convs first)
records.sort(key=lambda r: r['chars'], reverse=True)

# ── Self-check: sum(msg_count) must equal 29,396 ──────────────────────────
total_msgs = sum(r['msg_count'] for r in records)
if total_msgs != EXPECTED_V3_MSGS:
    sys.exit(f'SELF-CHECK FAILED: sum(msg_count) = {total_msgs:,}, expected {EXPECTED_V3_MSGS:,}')
print(f'Self-check PASS: sum(msg_count) = {total_msgs:,}')

# ── Step 4: Write CSV ───────────────────────────────────────────────────────
FIELDNAMES = ['conv_uuid', 'msg_count', 'chars', 'content_chars', 'tok_lo', 'tok_hi']
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()
    writer.writerows(records)
print(f'Wrote {CSV_PATH}  ({len(records)} rows)')

# ── Step 5: Distribution stats ──────────────────────────────────────────────
def pct(vals, p):
    """Return pth percentile of a sorted list (0–100)."""
    if not vals:
        return 0
    n = len(vals)
    idx = p / 100 * (n - 1)
    lo, hi = int(idx), min(int(idx) + 1, n - 1)
    frac = idx - lo
    return vals[lo] + frac * (vals[hi] - vals[lo])

def dist_stats(vals):
    s = sorted(vals)
    return {
        'min':    s[0],
        'p25':    pct(s, 25),
        'median': statistics.median(s),
        'p75':    pct(s, 75),
        'p90':    pct(s, 90),
        'p95':    pct(s, 95),
        'max':    s[-1],
    }

msg_counts   = [r['msg_count']     for r in records]
chars_vals   = [r['chars']         for r in records]
content_vals = [r['content_chars'] for r in records]
tok_lo_vals  = [r['tok_lo']        for r in records]
tok_hi_vals  = [r['tok_hi']        for r in records]

stats = {
    'msg_count':     dist_stats(msg_counts),
    'chars':         dist_stats(chars_vals),
    'content_chars': dist_stats(content_vals),
    'tok_lo':        dist_stats(tok_lo_vals),
    'tok_hi':        dist_stats(tok_hi_vals),
}

# ── Step 6: Whale-lane crossings (tok_hi) ──────────────────────────────────
whale_200k = sum(1 for v in tok_hi_vals if v > 200_000)
whale_500k = sum(1 for v in tok_hi_vals if v > 500_000)
whale_1m   = sum(1 for v in tok_hi_vals if v > 1_000_000)

# ── Step 7: Write census_summary.md ────────────────────────────────────────
def fmt_int(v):
    return f'{int(v):,}'

summary_lines = [
    '# census_summary.md — S70 Floor Node-Size Census',
    '',
    '## Render path',
    '',
    '- **Full payload (`chars`):** `floor_extract.py` format — conv header block',
    '  (CONVERSATION / SNAPSHOT_ID / CREATED / MESSAGES) + per-message envelopes',
    '  (===MSG=== / uuid / parent / role / --- / rendered blocks / ===END===).',
    '  `chars = len(full_payload_string)` — Python Unicode chars.',
    '- **Content-only (`content_chars`):** rendered block content only',
    '  (no envelope lines, no conv header). Block rendering via `render_block()`',
    '  **VERBATIM** from `floor_extract.py:37-62` (canary-locked, do not alter).',
    '  Used by Task 2 for density stratification (content_chars / msg_count axis).',
    '- **Token brackets:** `tok_lo = int(chars × 0.32)` (prose), `tok_hi = int(chars × 0.72)` (code-dense).',
    '  Computed from full payload chars, not content_chars.',
    '- **$0 assertion:** `ANTHROPIC_API_KEY` not loaded — verified at script start.',
    '',
    '## Floor counts returned by reconciliation query',
    '',
    f'| Metric | Returned | Expected (FLOOR_COUNTS.md) | Match |',
    f'|--------|----------|---------------------------|-------|',
    f'| v3 rows (`COUNT(*)` WHERE scrub_version=3) | {v3_rows:,} | {EXPECTED_V3_ROWS:,} | ✓ |',
    f'| v3 distinct messages (`COUNT(DISTINCT msg_uuid)`) | {v3_msgs:,} | {EXPECTED_V3_MSGS:,} | ✓ |',
    f'| v3 distinct convs (`COUNT(DISTINCT conv_uuid)`) | {v3_convs:,} | {EXPECTED_V3_CONVS:,} | ✓ |',
    '',
    '**Deviation from FLOOR_COUNTS.md:** None.',
    '',
    'The 440-header and 58,792-total-row figures from FLOOR_COUNTS.md are full-floor',
    'counts (all scrub versions). The v3-only query correctly returns a subset:',
    '29,396 rows (one per distinct message, v3 edition). This is consistent with',
    'FLOOR_COUNTS.md line #5. The 437 conv count = 440 headers − 3 hollow stubs',
    '(3f84a335, ae3468be, bc42e9ab: zero messages, floor-confirmed — FLOOR_COUNTS.md line #6).',
    '',
    '## Distribution statistics',
    '',
    f'| Metric | min | p25 | median | p75 | p90 | p95 | max |',
    f'|--------|-----|-----|--------|-----|-----|-----|-----|',
]

for metric, label in [
    ('msg_count',     'msg_count (distinct messages per conv)'),
    ('chars',         'chars (full payload chars)'),
    ('content_chars', 'content_chars (block-rendered content only)'),
    ('tok_lo',        'tok_lo (chars × 0.32, prose floor)'),
    ('tok_hi',        'tok_hi (chars × 0.72, code-dense ceiling)'),
]:
    s = stats[metric]
    summary_lines.append(
        f'| {label} | {fmt_int(s["min"])} | {fmt_int(s["p25"])} | {fmt_int(s["median"])} | '
        f'{fmt_int(s["p75"])} | {fmt_int(s["p90"])} | {fmt_int(s["p95"])} | {fmt_int(s["max"])} |'
    )

summary_lines += [
    '',
    '## Whale-lane crossings (tok_hi threshold)',
    '',
    f'| Threshold | Conv count | % of {len(records)} convs |',
    f'|-----------|------------|--------------------------|',
    f'| tok_hi > 200,000  | {whale_200k:,} | {whale_200k/len(records)*100:.1f}% |',
    f'| tok_hi > 500,000  | {whale_500k:,} | {whale_500k/len(records)*100:.1f}% |',
    f'| tok_hi > 1,000,000 | {whale_1m:,} | {whale_1m/len(records)*100:.1f}% |',
    '',
    '## Structural notes',
    '',
    '- CSV covers **437 convs** (not 440 — 3 hollow stubs absent by design; documented above).',
    f'- `sum(msg_count)` across all rows = **{total_msgs:,}** (self-check PASS vs expected 29,396).',
    '- 2 EMPTY-CONFIRMED convs (d2cd71e3, d85b4100) have NULL content_blocks at floor level.',
    '  They appear in CSV with msg_count > 0 but content_chars ≈ 0 (envelope overhead in chars only).',
    '- 12 continuation convs span 2 snapshots; aggregated by conv_uuid across all snapshots.',
    '  Snapshot_id in CSV header = first-seen snapshot for that conv_uuid in the v3 result set.',
    '',
    f'*Generated by `wallaby-way/scripts/foray_census_S70.py`, S70 apparatus.*',
]

SUMMARY_PATH.write_text('\n'.join(summary_lines), encoding='utf-8')
print(f'Wrote {SUMMARY_PATH}')

# ── Manifest ────────────────────────────────────────────────────────────────
print()
print('=== CHANGE MANIFEST ===')
print(f'  {CSV_PATH}')
print(f'  {SUMMARY_PATH}')
print(f'  Convs in CSV: {len(records)}')
print(f'  Sum msg_count: {total_msgs:,}')
print(f'  Whale >200K tok_hi: {whale_200k}')
print(f'  Whale >500K tok_hi: {whale_500k}')
print(f'  Whale >1M  tok_hi: {whale_1m}')
print('  Commands run: reconciliation query + full fetch (read-only)')
print('  ANTHROPIC_API_KEY: NOT loaded (guard passed)')
print('  Secrets written to output: NONE (DB URL never appears in CSV or summary)')
