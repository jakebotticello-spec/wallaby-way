# pipeline/s39/floor_extract.py  S39  (patched S50-wave2)
# Reads ONE conv from the Supabase floor → writes ===MSG=== payload + .parents.json sidecar.
# Messages come from ALL snapshots, deduped on msg_uuid (highest scrub_version wins).
# The conversation is the unit — the snapshot is a storage detail.
# SNAPSHOT_ID in the payload header = the latest scrub_version snapshot (metadata only).
# render_block() is VERBATIM from pipeline/extract_whale.py:38-62 — do not alter.
# Billing key must NOT be loaded. Floor read costs $0.
#
# CLI: python pipeline/s39/floor_extract.py --conv-uuid <uuid> --out pipeline/s39/<uuid>_payload.txt
import json, re, os, sys, argparse
from pathlib import Path

# Guard 1
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY is loaded — HALT')

ap = argparse.ArgumentParser()
ap.add_argument('--conv-uuid', required=True, dest='conv_uuid')
ap.add_argument('--out', required=True, dest='outfile')
args = ap.parse_args()

# Read floor DB URL
env_path = Path(__file__).parent.parent / 'secrets' / 'floor_db.env'
db_url = None
for line in env_path.read_text(encoding='utf-8').splitlines():
    m = re.match(r'^\s*SUPABASE_DB_URL\s*=\s*(.+)$', line)
    if m:
        db_url = m.group(1).strip().strip('"').strip("'")
if not db_url:
    sys.exit('ERROR: SUPABASE_DB_URL not found in floor_db.env')

SENTINEL = '00000000-0000-4000-8000-000000000000'


# ── render_block — VERBATIM from pipeline/extract_whale.py:38-62 ──────────────
# Do NOT alter. A change here desyncs payload rendering from the proven whale path.
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


import psycopg

with psycopg.connect(db_url) as conn:
    with conn.cursor() as cur:
        # Pick highest scrub_version snapshot for this conv
        cur.execute("""
            SELECT DISTINCT ON (conv_uuid)
                snapshot_id, conv_uuid::text, message_count, created_at
            FROM floor_conv_headers
            WHERE conv_uuid::text = %s
            ORDER BY conv_uuid, scrub_version DESC, snapshot_id DESC
        """, (args.conv_uuid,))
        hdr = cur.fetchone()
        if not hdr:
            sys.exit(f'ERROR: conv_uuid {args.conv_uuid} not found in floor_conv_headers')

        snapshot_id, conv_uuid, message_count, created_at = hdr

        # Fetch messages from ALL snapshots for this conv, deduped on msg_uuid.
        # Continuation convs store new messages under a later snapshot_id but have
        # no floor_conv_headers row for that snapshot — header JOIN would drop them.
        # Use snapshot_id DESC as recency proxy (ISO-date-prefixed strings sort correctly).
        cur.execute("""
            SELECT * FROM (
                SELECT DISTINCT ON (msg_uuid)
                    msg_uuid::text,
                    parent_message_uuid::text,
                    is_root,
                    sender,
                    content_blocks,
                    created_at
                FROM floor_conv_messages
                WHERE conv_uuid = %s::uuid
                ORDER BY msg_uuid, snapshot_id DESC
            ) deduped
            ORDER BY created_at ASC
        """, (conv_uuid,))
        msg_rows = cur.fetchall()

    conn.rollback()

# Build payload lines + parents_map
lines = [
    f'CONVERSATION: {conv_uuid}',
    f'SNAPSHOT_ID: {snapshot_id}',
    f'CREATED: {created_at}',
    f'MESSAGES: {len(msg_rows)}',
    '',
]

parents_map = {}

for msg_uuid, parent_message_uuid, is_root, sender, content_blocks, msg_created_at in msg_rows:
    parent_out = 'null' if (is_root or parent_message_uuid == SENTINEL) else parent_message_uuid
    parents_map[msg_uuid] = parent_out

    blocks = content_blocks if isinstance(content_blocks, list) else []
    parts = []
    for b in blocks:
        if isinstance(b, dict):
            rendered = render_block(b)
            if rendered:
                parts.append(rendered)

    content = '\n'.join(parts)

    lines += [
        '===MSG===',
        f'uuid: {msg_uuid}',
        f'parent: {parent_out}',
        f'role: {sender}',
        '---',
        content,
        '===END===',
        '',
    ]

OUT = Path(args.outfile)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text('\n'.join(lines), encoding='utf-8')

sidecar_path = Path(str(OUT) + '.parents.json')
sidecar_path.write_text(
    json.dumps(
        {'conv_uuid': conv_uuid, 'snapshot_id': snapshot_id, 'parents': parents_map},
        indent=2, ensure_ascii=False
    ),
    encoding='utf-8'
)

print(f'Wrote {OUT}  ({OUT.stat().st_size:,} bytes)')
print(f'Sidecar: {sidecar_path}  ({len(parents_map)} parents)')
print(f'Messages: {len(msg_rows)}')
print(f'Snapshot: {snapshot_id}')
print(f'Created:  {created_at}')
