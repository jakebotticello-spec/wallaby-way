# _uuid_hunt.py  v1.1  CCC S2 (Chamfer)  2026-06-08
# v1.1 (CCC S2 'Chamfer'): path-fixes for repo reorg — wallaby-way/ restructure.
"""
S40 precision-addendum grade — STEP 1: UUID-density floor hunt.
Scans all 219 FITS_WHOLE convs for cross-session UUID references in message text.
Uses floor_db.env ($0 Postgres). No billing key loaded.
"""
import json, re, csv, sys, os
from pathlib import Path
from collections import defaultdict

ROOT = Path(r"c:\claude-reference")

# Guard: billing key must NOT be present
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY loaded — HALT')

# ── Load floor DB URL ─────────────────────────────────────────────────────────
env_path = ROOT / 'wallaby-way' / 'secrets' / 'floor_db.env'
db_url = None
for line in env_path.read_text(encoding='utf-8').splitlines():
    m = re.match(r'^\s*SUPABASE_DB_URL\s*=\s*(.+)$', line)
    if m:
        db_url = m.group(1).strip().strip('"').strip("'")
if not db_url:
    sys.exit('ERROR: SUPABASE_DB_URL not found in floor_db.env')

# ── Load FITS_WHOLE conv list ─────────────────────────────────────────────────
WHALES = {
    'cfc7a70a-16f0-4f09-8467-d40260ee7434',
    '83506215-d78e-4d0c-a4bf-2d67faf5f59c',
    '55217328-5845-4745-bcea-054acf8f39b7',
    'd9d05961-b0e1-47d5-8fbc-1b68e8b32cd9',
}

worklist_path = ROOT / 'wallaby-way' / 'runs' / '2026-06-08' / 'worklist.csv'
fits_whole = []
char_counts = {}
with open(worklist_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        uuid = row['conv_uuid']
        if row['verdict'] == 'FITS_WHOLE' and uuid not in WHALES:
            fits_whole.append(uuid)
            char_counts[uuid] = int(row['char_count'])

print(f"FITS_WHOLE non-whale convs: {len(fits_whole)}", flush=True)

# ── UUID regex (8-4-4-4-12 hex) ───────────────────────────────────────────────
UUID_RE = re.compile(
    r'\b([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\b',
    re.IGNORECASE
)
SENTINEL = '00000000-0000-4000-8000-000000000000'

def extract_text_from_blocks(content_blocks):
    """Pull text content from JSONB content_blocks."""
    if not content_blocks or not isinstance(content_blocks, list):
        return ''
    parts = []
    for block in content_blocks:
        if not isinstance(block, dict):
            continue
        btype = block.get('type', '')
        if btype == 'text':
            parts.append(block.get('text', '') or '')
        elif btype == 'tool_result':
            content = block.get('content', '')
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict):
                        parts.append(item.get('text', '') or '')
            elif isinstance(content, str):
                parts.append(content)
    return '\n'.join(parts)

# ── Single-pass query: get best snapshot per conv, then all messages ──────────
import psycopg

print("Connecting to floor DB...", flush=True)
results = []

with psycopg.connect(db_url) as conn:
    with conn.cursor() as cur:
        # Step A: get the canonical snapshot_id for each FITS_WHOLE conv
        cur.execute("""
            SELECT DISTINCT ON (conv_uuid)
                conv_uuid::text, snapshot_id
            FROM floor_conv_headers
            WHERE conv_uuid::text = ANY(%s)
            ORDER BY conv_uuid, scrub_version DESC, snapshot_id DESC
        """, (fits_whole,))
        snapshot_map = {row[0]: row[1] for row in cur.fetchall()}
        print(f"Found snapshots for {len(snapshot_map)} convs", flush=True)

        # Step B: fetch all messages for all FITS_WHOLE convs in one query
        # Use a VALUES list of (snapshot_id, conv_uuid) pairs
        pairs = [(v, k) for k, v in snapshot_map.items()]
        if not pairs:
            sys.exit("No snapshots found")

        # Build parameterized query
        placeholders = ','.join(['(%s, %s::uuid)'] * len(pairs))
        flat_params = [x for pair in pairs for x in pair]

        cur.execute(f"""
            SELECT conv_uuid::text, msg_uuid::text, content_blocks
            FROM floor_conv_messages
            WHERE (snapshot_id, conv_uuid) IN ({placeholders})
        """, flat_params)

        # Aggregate by conv
        conv_msg_uuids = defaultdict(set)
        conv_text = defaultdict(list)

        row_count = 0
        for conv_uuid, msg_uuid, content_blocks in cur.fetchall():
            conv_msg_uuids[conv_uuid].add(msg_uuid.lower())
            text = extract_text_from_blocks(content_blocks)
            if text:
                conv_text[conv_uuid].append(text)
            row_count += 1

        print(f"Fetched {row_count} message rows", flush=True)

    conn.rollback()

# ── Count cross-session UUIDs per conv ───────────────────────────────────────
print("\nRanking by cross-session UUID density...", flush=True)

for conv_uuid in fits_whole:
    if conv_uuid not in conv_text and conv_uuid not in conv_msg_uuids:
        continue

    combined_text = '\n'.join(conv_text.get(conv_uuid, []))
    own_msg_uuids = conv_msg_uuids.get(conv_uuid, set())

    all_found = set(u.lower() for u in UUID_RE.findall(combined_text))
    self_refs = {conv_uuid.lower(), SENTINEL.lower()} | own_msg_uuids

    cross_uuids = all_found - self_refs
    results.append({
        'conv_uuid': conv_uuid,
        'char_count': char_counts.get(conv_uuid, 0),
        'cross_uuid_count': len(cross_uuids),
        'cross_uuids': sorted(cross_uuids),
    })

results.sort(key=lambda x: -x['cross_uuid_count'])

# ── Report top results ────────────────────────────────────────────────────────
print("\n=== TOP 15 BY CROSS-SESSION UUID COUNT ===")
for r in results[:15]:
    in_range = 50_000 <= r['char_count'] <= 600_000
    marker = " <-- IN-RANGE" if in_range else ""
    print(f"  {r['cross_uuid_count']:3d} cross-UUIDs | {r['char_count']:>9,} chars | {r['conv_uuid']}{marker}")

# Best candidate: highest count in 50K-600K range
in_range = [r for r in results if 50_000 <= r['char_count'] <= 600_000]
if in_range:
    best = in_range[0]
    print(f"\n=== BEST IN-RANGE CANDIDATE ===")
    print(f"  conv_uuid:   {best['conv_uuid']}")
    print(f"  char_count:  {best['char_count']:,}")
    print(f"  cross_uuids: {best['cross_uuid_count']}")
    print(f"\n  DISTINCT CROSS-SESSION UUIDs FOUND:")
    for u in best['cross_uuids']:
        print(f"    {u}")
else:
    print("\nNo in-range candidate found; best overall:")
    best = results[0]
    print(f"  {best}")
