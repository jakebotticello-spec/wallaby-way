# floor_overlay_v3.py · v1.0 · apparatus S52 "Catechism" · 2026-06-10
# Appends scrub-v3 overlay rows to floor_conv_messages for every message row
# (all 3 snapshots, 29,396 messages). v3 = v1.7 production pattern set (10 classes)
# PLUS 3 new Supabase classes: supabase_secret, supabase_publishable, supabase_ref_url.
# Headers excluded: pure metadata, no scrub_walk (S20 ruling).
# Floor is append-only: INSERT only. UPDATE/DELETE are revoked.
# Output dir: wallaby-way/runs/floor_overlay_v3_S52/
#
# Modes:
#   --dry-run   read-only; walk every row, count hits, write audit artifacts; HALT
#   --execute   batched transactional INSERTs of v3 rows; refuses if v3 rows exist

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ── billing guard ────────────────────────────────────────────────────────────
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY is loaded — HALT')

# ── path setup ───────────────────────────────────────────────────────────────
HERE    = Path(__file__).resolve().parent          # wallaby-way/scripts/
WW      = HERE.parent                              # wallaby-way/
OUT_DIR = WW / 'runs' / 'floor_overlay_v3_S52'

SCRUB_VERSION = 3
CONTENT_FIELDS = ('text', 'content_blocks', 'attachments', 'files')
BATCH_SIZE     = 500

# Expected floor numbers (FLOOR_COUNTS.md, census 2026-06-10)
EXPECTED_TOTAL    = 29_396
EXPECTED_BASELINE = 22_801   # baseline-2026-05-25-ae015455
EXPECTED_DELTA1   = 1_337    # delta-2026-05-28-a61498e6
EXPECTED_DELTA2   = 5_258    # delta-2026-06-09-2748278f

# ── v1.7 production patterns (verbatim from apparatus_freeze_pipeline.py v1.7) ──
# Import if importable; replicate exactly if not.
sys.path.insert(0, str(HERE))
try:
    from apparatus_freeze_pipeline import PATTERNS as _PATTERNS_V17
    _imported = True
except ImportError:
    _imported = False
    _PATTERNS_V17 = [
        ('RTSP',                 r'rtsp://[^/\s:]+:[^/\s@]+@',
                                 '<RTSP_CRED_REDACTED>'),
        ('postgres',             r'postgres(?:ql)?://[^/\s:]+:[^/\s@]+@',
                                 '<POSTGRES_CRED_REDACTED>'),
        ('anthropic',            r'sk-ant-[A-Za-z0-9_-]{20,}',
                                 '<ANTHROPIC_KEY_REDACTED>'),
        ('openai',               r'sk-(?!ant-)[A-Za-z0-9_-]{20,}',
                                 '<OPENAI_KEY_REDACTED>'),
        ('stripe',               r'(?:sk|rk)_live_[A-Za-z0-9]{20,}',
                                 '<STRIPE_KEY_REDACTED>'),
        ('google_oauth_secret',  r'GOCSPX-[A-Za-z0-9_-]{10,}',
                                 '<GOOGLE_OAUTH_REDACTED>'),
        ('google_refresh_token', r'1//[A-Za-z0-9_-]{20,}',
                                 '<GOOGLE_REFRESH_REDACTED>'),
        ('github_token',
         r'(?:ghp|gho|ghs|ghu)_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}',
         '<GITHUB_TOKEN_REDACTED>'),
        ('aws_access_key',       r'AKIA[0-9A-Z]{16}',
                                 '<AWS_KEY_REDACTED>'),
        ('jwt',
         r'eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}',
         '<JWT_REDACTED>'),
    ]

# Three new Supabase classes (S37 flag-#4 queued patterns, from scrub_output.py)
SUPABASE_PATTERNS = [
    ('supabase_secret',      r'sb_secret_[A-Za-z0-9_-]{20,}',
                             '<SUPABASE_SECRET_REDACTED>'),
    ('supabase_publishable', r'sb_publishable_[A-Za-z0-9_-]{20,}',
                             '<SUPABASE_PUBLISHABLE_REDACTED>'),
    ('supabase_ref_url',     r'https://[a-z0-9]{16,}\.supabase\.co',
                             '<SUPABASE_REF_URL_REDACTED>'),
]

PATTERNS_V3 = _PATTERNS_V17 + SUPABASE_PATTERNS
PATTERN_NAMES = [p[0] for p in PATTERNS_V3]


# ── scrub helpers ─────────────────────────────────────────────────────────────

def scrub_walk(obj, path, audit_fn):
    """Type-agnostic recursive descent — identical contract to pipeline's _scrub_walk.
    Returns rebuilt structure; cred substrings replaced by class tokens."""
    if isinstance(obj, str):
        return audit_fn(obj, path)
    elif isinstance(obj, dict):
        return {k: scrub_walk(v, f'{path}.{k}' if path else k, audit_fn)
                for k, v in obj.items()}
    elif isinstance(obj, list):
        return [scrub_walk(item, f'{path}[{i}]', audit_fn)
                for i, item in enumerate(obj)]
    else:
        return obj


def make_audit_fn(snapshot_id, conv_uuid, msg_uuid, audit_list):
    """Returns a string-replacement function; appends audit entry per match.
    Captured VALUE never enters audit record — original_length only."""
    def audit_fn(s, path):
        result = s
        for pname, pattern, token in PATTERNS_V3:
            def replacer(m, pn=pname, tk=token):
                audit_list.append({
                    'snapshot_id':     snapshot_id,
                    'scrub_version':   SCRUB_VERSION,
                    'conv_uuid':       conv_uuid,
                    'msg_uuid':        msg_uuid,
                    'json_path':       path,
                    'pattern_class':   pn,
                    'redaction_token': tk,
                    'original_length': len(m.group(0)),
                })
                return tk
            result = re.sub(pattern, replacer, result)
        return result
    return audit_fn


def scrub_row(row_dict, audit_list):
    """Apply v3 scrub to content fields of one message row dict.
    Returns new dict with scrubbed fields and scrub_version=3.
    NEVER prints or logs matched secret values."""
    snapshot_id = row_dict.get('snapshot_id', '')
    conv_uuid   = str(row_dict.get('conv_uuid', ''))
    msg_uuid    = str(row_dict.get('msg_uuid', ''))
    out = dict(row_dict)
    audit_fn = make_audit_fn(snapshot_id, conv_uuid, msg_uuid, audit_list)
    for field in CONTENT_FIELDS:
        if field in out and out[field] is not None:
            out[field] = scrub_walk(out[field], field, audit_fn)
    out['scrub_version'] = SCRUB_VERSION
    return out


# ── DB helpers ────────────────────────────────────────────────────────────────

def load_db_url():
    env_path = WW / 'secrets' / 'floor_db.env'
    for line in env_path.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^\s*SUPABASE_DB_URL\s*=\s*(.+)$', line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    sys.exit('ERROR: SUPABASE_DB_URL not found in floor_db.env')


def discover_schema(cur):
    """Return (columns list, constraints list). Halts if msg_uuid-alone unique found."""
    # Column names in order
    cur.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'floor_conv_messages'
        ORDER BY ordinal_position
    """)
    columns = [(r[0], r[1], r[2]) for r in cur.fetchall()]

    # All table constraints — fetch column names per constraint separately to
    # avoid array_agg type-coercion issues with psycopg
    cur.execute("""
        SELECT tc.constraint_name, tc.constraint_type
        FROM information_schema.table_constraints tc
        WHERE tc.table_schema = 'public'
          AND tc.table_name = 'floor_conv_messages'
        ORDER BY tc.constraint_type, tc.constraint_name
    """)
    constraint_meta = [(r[0], r[1]) for r in cur.fetchall()]

    constraints = []
    for cname, ctype in constraint_meta:
        cur.execute("""
            SELECT column_name FROM information_schema.key_column_usage
            WHERE table_schema = 'public'
              AND table_name = 'floor_conv_messages'
              AND constraint_name = %s
            ORDER BY ordinal_position
        """, (cname,))
        cols = [r[0] for r in cur.fetchall()]
        constraints.append({'name': cname, 'type': ctype, 'cols': cols})

    # CRITICAL: check for UNIQUE or PK on msg_uuid alone
    for c in constraints:
        if c['type'] in ('UNIQUE', 'PRIMARY KEY') and c['cols'] == ['msg_uuid']:
            sys.exit(
                f"HALT: UNIQUE/PK constraint '{c['name']}' on msg_uuid ALONE detected. "
                f"Overlay INSERT would collide. This is a Jake-gated floor-schema event. "
                f"Constraint detail: {c}"
            )

    return columns, constraints


def check_v3_rows(cur):
    """Return count of existing scrub_version=3 rows."""
    cur.execute("SELECT COUNT(*) FROM floor_conv_messages WHERE scrub_version = %s",
                (SCRUB_VERSION,))
    return cur.fetchone()[0]


def check_output_dir_fresh():
    """HALT if output dir has artifacts fresher than 1 hour (S51 collision rule)."""
    if not OUT_DIR.exists():
        return
    now = time.time()
    for f in OUT_DIR.iterdir():
        if f.is_file() and (now - f.stat().st_mtime) < 3600:
            sys.exit(
                f"HALT: output dir {OUT_DIR} has artifact '{f.name}' "
                f"modified <1 hour ago. Another instance may be live. "
                f"Resolve with Jake before proceeding."
            )


def fetch_all_message_rows(cur):
    """Fetch all 29,396 message rows ordered by snapshot_id, created_at.
    Returns list of dicts."""
    cur.execute("""
        SELECT snapshot_id, scrub_version, conv_uuid::text, msg_uuid::text,
               parent_message_uuid::text, sender, created_at, updated_at,
               text, content_blocks, attachments, files, is_root
        FROM floor_conv_messages
        ORDER BY snapshot_id, created_at
    """)
    col_names = [d[0] for d in cur.description]
    rows = []
    for r in cur.fetchall():
        rows.append(dict(zip(col_names, r)))
    return rows


# ── dry-run ───────────────────────────────────────────────────────────────────

def run_dry_run(cur, constraints=None):
    print('[dry-run] Checking for existing v3 rows ...')
    v3_count = check_v3_rows(cur)
    if v3_count > 0:
        sys.exit(
            f"HALT: {v3_count} scrub_version=3 rows already exist. "
            f"Another instance may be live or a prior run was partial. "
            f"Resolve with Jake before proceeding."
        )
    print('[dry-run] v3 rows: 0 -- OK to proceed')

    print('[dry-run] Fetching all message rows ...')
    rows = fetch_all_message_rows(cur)
    total_fetched = len(rows)
    print(f'[dry-run] Fetched {total_fetched:,} rows')

    audit_list = []
    # per-snapshot × per-class hit tallies
    snap_class_hits = {}  # {snapshot_id: {class: count}}
    # affected conv map: {conv_uuid: {class: count}}
    conv_class_hits = {}

    for i, row in enumerate(rows):
        snap_id = row['snapshot_id']
        if snap_id not in snap_class_hits:
            snap_class_hits[snap_id] = {p[0]: 0 for p in PATTERNS_V3}
        scrub_row(row, audit_list)
        if i % 5000 == 0 and i > 0:
            print(f'[dry-run] ... {i:,} / {total_fetched:,}', flush=True)

    # Tally audit_list into per-snapshot × per-class and per-conv maps
    for entry in audit_list:
        sid   = entry['snapshot_id']
        pname = entry['pattern_class']
        cuuid = entry['conv_uuid']

        if sid not in snap_class_hits:
            snap_class_hits[sid] = {p[0]: 0 for p in PATTERNS_V3}
        snap_class_hits[sid][pname] = snap_class_hits[sid].get(pname, 0) + 1

        if cuuid not in conv_class_hits:
            conv_class_hits[cuuid] = {}
        conv_class_hits[cuuid][pname] = conv_class_hits[cuuid].get(pname, 0) + 1

    total_hits = len(audit_list)
    rows_to_insert = total_fetched  # one v3 row per existing message row

    # ── write dry_run_map.jsonl ───────────────────────────────────────────────
    map_path = OUT_DIR / 'dry_run_map.jsonl'
    with open(map_path, 'w', encoding='utf-8') as f:
        for entry in audit_list:
            # Audit format per Freeze_Pipeline_Spec_v4:
            # {snapshot_id, scrub_version, conv_uuid, msg_uuid, json_path,
            #  pattern_class, redaction_token, original_length}
            # VALUE is never written here — audit_list entries already exclude it
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    print(f'[dry-run] dry_run_map.jsonl: {total_hits:,} entries')

    # ── build dry_run_audit.md ────────────────────────────────────────────────
    lines = []
    lines.append('# dry_run_audit.md — floor_overlay_v3 S52')
    lines.append(f'Run UTC: {datetime.now(timezone.utc).isoformat()}')
    lines.append(f'Pattern import: {"from apparatus_freeze_pipeline (imported)" if _imported else "replicated inline"}')
    lines.append(f'scrub_version: {SCRUB_VERSION}')
    lines.append(f'Patterns applied ({len(PATTERNS_V3)}): {", ".join(PATTERN_NAMES)}')
    lines.append('')

    lines.append('## 1. Row counts')
    lines.append(f'- Total message rows fetched: {total_fetched:,}')
    lines.append(f'- Expected: {EXPECTED_TOTAL:,}')
    match_str = 'MATCH' if total_fetched == EXPECTED_TOTAL else f'MISMATCH — expected {EXPECTED_TOTAL:,}'
    lines.append(f'- Check: {match_str}')
    lines.append(f'- Rows to INSERT (v3 overlay): {rows_to_insert:,}')
    lines.append('')

    lines.append('## 2. Per-snapshot row counts')
    snap_counts = {}
    for row in rows:
        sid = row['snapshot_id']
        snap_counts[sid] = snap_counts.get(sid, 0) + 1
    for sid in sorted(snap_counts):
        lines.append(f'- {sid}: {snap_counts[sid]:,} rows')
    expected_snaps = {
        'baseline-2026-05-25-ae015455': EXPECTED_BASELINE,
        'delta-2026-05-28-a61498e6':    EXPECTED_DELTA1,
        'delta-2026-06-09-2748278f':    EXPECTED_DELTA2,
    }
    lines.append('Expected per snapshot:')
    for sid, exp in sorted(expected_snaps.items()):
        got = snap_counts.get(sid, 0)
        ok  = 'OK' if got == exp else f'MISMATCH (got {got:,})'
        lines.append(f'  - {sid}: {exp:,} → {ok}')
    lines.append('')

    lines.append('## 3. Per-snapshot × per-class hit counts')
    all_classes = [p[0] for p in PATTERNS_V3]
    for sid in sorted(snap_class_hits):
        lines.append(f'### {sid}')
        for cls in all_classes:
            n = snap_class_hits[sid].get(cls, 0)
            lines.append(f'  - {cls}: {n}')
    lines.append('')

    lines.append('## 4. Total hits per class (all snapshots)')
    class_totals = {p[0]: 0 for p in PATTERNS_V3}
    for entry in audit_list:
        class_totals[entry['pattern_class']] += 1
    for cls in all_classes:
        lines.append(f'- {cls}: {class_totals[cls]}')
    lines.append(f'- TOTAL redactions: {total_hits:,}')
    lines.append('')

    lines.append('## 5. Affected conversations (conv_uuid + classes + count)')
    lines.append(f'Total affected convs: {len(conv_class_hits):,}')
    for cuuid in sorted(conv_class_hits):
        cls_summary = ', '.join(
            f'{c}={n}' for c, n in sorted(conv_class_hits[cuuid].items())
        )
        lines.append(f'- {cuuid}: {cls_summary}')
    lines.append('')

    lines.append('## 6. Schema findings')
    # PK collision analysis
    pk_cols = []
    if constraints:
        for c in constraints:
            if c['type'] == 'PRIMARY KEY':
                pk_cols = c['cols']
    lines.append(f'- PRIMARY KEY cols: {pk_cols}')
    pk_includes_scrub = 'scrub_version' in pk_cols
    lines.append(f'- scrub_version in PK: {pk_includes_scrub}')
    if not pk_includes_scrub:
        lines.append('')
        lines.append('### CRITICAL -- PK COLLISION FINDING')
        lines.append(
            f'The PK `{pk_cols}` does NOT include `scrub_version`. '
            f'Inserting a v3 row with the same (snapshot_id, conv_uuid, msg_uuid) '
            f'as an existing v1/v2 row will violate the PK constraint. '
            f'The --execute step CANNOT proceed without a schema change to the PK.'
        )
        lines.append(
            'This is a Jake-gated floor-schema event. '
            'Options: (a) drop + recreate PK as (snapshot_id, conv_uuid, msg_uuid, scrub_version); '
            '(b) alternative overlay design that does not require duplicate (snapshot_id, conv_uuid, msg_uuid). '
            'Do not attempt schema changes from this script.'
        )
    lines.append('')

    lines.append('## 7. Secret-safety statement')
    lines.append(
        'dry_run_map.jsonl contains: snapshot_id, scrub_version, conv_uuid, msg_uuid, '
        'json_path, pattern_class, redaction_token, original_length. '
        'No matched secret VALUE is written anywhere — original_length (integer) only. '
        'This file does NOT contain a plaintext secret.'
    )
    lines.append('')

    lines.append('## 8. Gate')
    if not pk_includes_scrub:
        lines.append(
            'HALT -- DOUBLE GATE: (a) Jake gates --execute on these numbers; '
            '(b) --execute is also blocked by the PK collision (see section 6). '
            'A floor schema change is required before --execute can run. '
            'Do NOT attempt --execute or schema changes without Jake approval.'
        )
    else:
        lines.append(
            'HALT -- Jake gates the execute step on these numbers. '
            'Do NOT run --execute without explicit Jake approval on this audit.'
        )

    audit_path = OUT_DIR / 'dry_run_audit.md'
    audit_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'[dry-run] dry_run_audit.md written')
    print()
    print('=' * 60)
    print('DRY-RUN COMPLETE')
    print(f'  Total message rows   : {total_fetched:,}  (expected {EXPECTED_TOTAL:,})')
    print(f'  Rows to INSERT (v3)  : {rows_to_insert:,}')
    print(f'  Total redactions     : {total_hits:,}')
    print(f'  New Supabase hits    : '
          f'sb_secret={class_totals.get("supabase_secret",0)} '
          f'sb_pub={class_totals.get("supabase_publishable",0)} '
          f'sb_ref_url={class_totals.get("supabase_ref_url",0)}')
    print(f'  Audit file           : {audit_path}')
    print(f'  Machine map          : {map_path}')
    print()
    # PK collision warning
    pk_cols = []
    if constraints:
        for c in constraints:
            if c['type'] == 'PRIMARY KEY':
                pk_cols = c['cols']
    if 'scrub_version' not in pk_cols:
        print(f'  CRITICAL PK FINDING: PK={pk_cols} lacks scrub_version.')
        print(f'  --execute BLOCKED: INSERT would collide on (snapshot_id,conv_uuid,msg_uuid).')
        print(f'  Floor schema change required -- Jake-gated event.')
    print()
    print('HALT -- Jake gates the execute step. Do not run --execute without approval.')
    return rows_to_insert, total_fetched


# ── execute ───────────────────────────────────────────────────────────────────

def run_execute(conn, cur):
    print('[execute] Pre-flight: checking for existing v3 rows ...')
    v3_count = check_v3_rows(cur)
    if v3_count > 0:
        sys.exit(
            f"HALT: {v3_count} scrub_version=3 rows already exist. "
            f"Refusing --execute to prevent double-insert. "
            f"Resolve with Jake before proceeding."
        )
    print('[execute] v3 rows: 0 — safe to insert')

    print('[execute] Fetching all message rows ...')
    rows = fetch_all_message_rows(cur)
    total_fetched = len(rows)
    print(f'[execute] Fetched {total_fetched:,} rows')

    if total_fetched != EXPECTED_TOTAL:
        sys.exit(
            f"HALT: fetched {total_fetched:,} rows, expected {EXPECTED_TOTAL:,}. "
            f"Row count mismatch — do not proceed."
        )

    # Determine column order for INSERT (excluding scrub_version — we set it to 3)
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'floor_conv_messages'
        ORDER BY ordinal_position
    """)
    all_cols = [r[0] for r in cur.fetchall()]

    # Build INSERT column list
    insert_cols = all_cols  # all columns including scrub_version
    col_placeholders = ', '.join(['%s'] * len(insert_cols))
    col_names_sql = ', '.join(insert_cols)
    insert_sql = (
        f"INSERT INTO floor_conv_messages ({col_names_sql}) "
        f"VALUES ({col_placeholders})"
    )

    log_lines = []
    log_lines.append('# execute_log.md — floor_overlay_v3 S52')
    log_lines.append(f'Run UTC: {datetime.now(timezone.utc).isoformat()}')
    log_lines.append(f'Rows to insert: {total_fetched:,}')
    log_lines.append(f'Batch size: {BATCH_SIZE}')
    log_lines.append('')

    audit_list = []
    inserted = 0
    batch_count = 0
    t0 = time.time()

    for batch_start in range(0, total_fetched, BATCH_SIZE):
        batch = rows[batch_start:batch_start + BATCH_SIZE]
        batch_rows = []
        for row in batch:
            scrubbed = scrub_row(row, audit_list)
            # Build tuple in column order
            row_vals = []
            for col in insert_cols:
                val = scrubbed.get(col)
                # JSONB fields: pass as Json-serialized string or native Python
                if col in ('content_blocks', 'attachments', 'files') and val is not None:
                    row_vals.append(json.dumps(val, ensure_ascii=False))
                elif col == 'scrub_version':
                    row_vals.append(SCRUB_VERSION)
                else:
                    row_vals.append(val)
            batch_rows.append(tuple(row_vals))

        cur.executemany(insert_sql, batch_rows)
        conn.commit()
        inserted += len(batch)
        batch_count += 1

        if batch_count % 10 == 0 or inserted == total_fetched:
            elapsed = time.time() - t0
            print(f'[execute] {inserted:,} / {total_fetched:,} inserted '
                  f'({elapsed:.1f}s)', flush=True)

    total_hits = len(audit_list)
    elapsed_total = time.time() - t0

    log_lines.append(f'## Result')
    log_lines.append(f'- Rows inserted: {inserted:,}')
    log_lines.append(f'- Batches: {batch_count}')
    log_lines.append(f'- Total redactions: {total_hits:,}')
    log_lines.append(f'- Elapsed: {elapsed_total:.1f}s')
    log_lines.append(f'Completed UTC: {datetime.now(timezone.utc).isoformat()}')

    log_path = OUT_DIR / 'execute_log.md'
    log_path.write_text('\n'.join(log_lines), encoding='utf-8')
    print(f'[execute] execute_log.md written: {log_path}')
    print(f'[execute] DONE — {inserted:,} v3 rows inserted, {total_hits:,} redactions')
    return inserted


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description='floor scrub-v3 overlay — apparatus S52')
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--dry-run',  action='store_true',
                       help='Read-only: walk all rows, count hits, write audit. HALT.')
    group.add_argument('--execute',  action='store_true',
                       help='INSERT v3 rows. Refuses if v3 rows already exist.')
    args = p.parse_args()

    # Collision guard (S51 rule): for --execute only — two execute instances on
    # one task would double-insert rows. Dry-run is idempotent (read-only).
    if args.execute:
        check_output_dir_fresh()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    db_url = load_db_url()

    import psycopg

    print(f'Pattern source: {"imported from apparatus_freeze_pipeline" if _imported else "replicated inline"}')
    print(f'Pattern count : {len(PATTERNS_V3)} ({len(_PATTERNS_V17)} v1.7 + {len(SUPABASE_PATTERNS)} Supabase)')
    print(f'SCRUB_VERSION : {SCRUB_VERSION}')
    print(f'Output dir    : {OUT_DIR}')
    print()

    connect_kwargs = {}
    if args.dry_run:
        connect_kwargs['autocommit'] = False

    with psycopg.connect(db_url) as conn:
        if args.dry_run:
            # Set read_only before any transaction begins
            conn.read_only = True

        with conn.cursor() as cur:
            # Step 2: schema discovery
            print('== Schema discovery =================================')
            columns, constraints = discover_schema(cur)
            print('Columns (floor_conv_messages):')
            for col_name, dtype, nullable in columns:
                print(f'  {col_name:35s} {dtype}  nullable={nullable}')
            print('Constraints:')
            for c in constraints:
                print(f'  [{c["type"]}] {c["name"]} on {c["cols"]}')
            print()

            if args.dry_run:
                run_dry_run(cur, constraints=constraints)
            else:
                run_execute(conn, cur)


if __name__ == '__main__':
    main()
