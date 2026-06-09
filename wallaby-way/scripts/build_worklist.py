# wallaby-way/scripts/build_worklist.py  v2.2  CCC S2 (Chamfer)
# Builds the DELTA worklist from the Supabase floor (NOT conversations.json).
#
# CHANGE NOTES (v2.0, S48 "Cartographer"):
#   - DELTA EXCLUSION ADDED. v1 (S39) emitted EVERY floor conv minus 4 whales — which,
#     post-merge, means re-reading the entire already-harvested pile (paid-overspend trap).
#     v2 subtracts the already-harvested conv set so the worklist holds ONLY new convs.
#   - BASELINE SOURCE = the merge manifest (full UUIDs, authoritative). --baseline-manifest
#     arg, defaults to harvested_nodes/MERGE_MANIFEST_S47.md. Point future deltas at a newer
#     manifest with ZERO code change (every export is a delta against the then-current pile).
#   - GLOB CROSS-CHECK GUARD. The on-disk harvested_nodes/ files are reduced to conv prefixes
#     and reconciled against the manifest's UUIDs (by 8-char prefix, because result_/confirm_
#     filenames carry only the prefix). Drift beyond tolerance => HALT, write nothing. This is
#     the S47 count-pass discipline applied forward: don't trust the manifest blindly, prove it
#     against disk before it gates a paid run.
#   - Floor-query + char_count + verdict logic carried VERBATIM from v1 (proven S39+).
#   v2.1: cross-check ignore broadened to skip any *MANIFEST* index file (was MERGE_MANIFEST
#         only) — the S37 cold-store MANIFEST.md is a legit index, not a node. Pattern-ignore,
#         NOT a tolerance bump (a tolerance bump would let real drift through later).
#   v2.2 (CCC S2 'Chamfer'): path-fixes for repo reorg — wallaby-way/ restructure.
#
# Source: DISTINCT ON (conv_uuid) highest scrub_version snapshot per conv.
# char_count uses full json.dumps(content_blocks) — not .text only — so tool-heavy convs
#   are not under-counted. proxy_est_tokens = char_count / 3.5.
# Whale UUIDs are excluded (already resolved, handled separately).
# Already-harvested UUIDs are excluded (the delta exclusion — this is the v2 point).
# Billing key must NOT be loaded. Floor read costs $0.
#
# RUN ORDER NOTE: in the delta pass this runs AFTER the delta-freeze writes the new snapshot
#   to the floor. If the floor holds only the pre-delta baseline, the worklist is EMPTY and
#   that is CORRECT (no new convs ingested yet) — not a bug.
#
# USAGE:
#   python build_worklist.py
#   python build_worklist.py --baseline-manifest ../../harvested_nodes/MERGE_MANIFEST_S47.md
#   python build_worklist.py --allow-empty        # suppress the empty-worklist nonzero exit
#   python build_worklist.py --crosscheck-tolerance 0   # default 0; raise only with a reason

import argparse, csv, glob, json, os, re, sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Guard 1 — billing key must not be loaded for a $0 floor read
# ---------------------------------------------------------------------------
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY is loaded — HALT')

# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------
HERE = Path(__file__).parent                      # pipeline/s39/
REPO_PIPELINE = HERE.parent                       # pipeline/
DEFAULT_MANIFEST = REPO_PIPELINE.parent / 'wallaby-way' / 'nodes' / 'manifests' / 'MERGE_MANIFEST_S47.md'
HARVESTED_DIR = REPO_PIPELINE.parent / 'wallaby-way' / 'nodes' / 'harvested'

ap = argparse.ArgumentParser()
ap.add_argument('--baseline-manifest', default=str(DEFAULT_MANIFEST),
                help='Manifest whose conv_uuids are the already-harvested exclusion set.')
ap.add_argument('--harvested-dir', default=str(HARVESTED_DIR),
                help='Dir of node files, for the glob cross-check.')
ap.add_argument('--crosscheck-tolerance', type=int, default=0,
                help='Max allowed prefix mismatches between manifest and disk before HALT.')
ap.add_argument('--allow-empty', action='store_true',
                help='Exit 0 (not 3) when the worklist is empty.')
args = ap.parse_args()

manifest_path = Path(args.baseline_manifest)
harvested_dir = Path(args.harvested_dir)

# ---------------------------------------------------------------------------
# Read floor DB URL
# ---------------------------------------------------------------------------
env_path = REPO_PIPELINE / 'secrets' / 'floor_db.env'
db_url = None
for line in env_path.read_text(encoding='utf-8').splitlines():
    m = re.match(r'^\s*SUPABASE_DB_URL\s*=\s*(.+)$', line)
    if m:
        db_url = m.group(1).strip().strip('"').strip("'")
if not db_url:
    sys.exit('ERROR: SUPABASE_DB_URL not found in floor_db.env')

WHALE_UUIDS = {
    'cfc7a70a-16f0-4f09-8467-d40260ee7434',
    '83506215-d78e-4d0c-a4bf-2d67faf5f59c',
    '55217328-5845-4745-bcea-054acf8f39b7',
    'd9d05961-b0e1-47d5-8fbc-1b68e8b32cd9',
}

UUID_RE = re.compile(
    r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I
)

# ---------------------------------------------------------------------------
# Step A — read the manifest -> the already-harvested FULL-UUID exclusion set
# ---------------------------------------------------------------------------
if not manifest_path.exists():
    sys.exit(f'ERROR: baseline manifest not found: {manifest_path}')

manifest_uuids = set()
for line in manifest_path.read_text(encoding='utf-8').splitlines():
    s = line.strip()
    # Data rows are markdown table rows beginning with a pipe + a full UUID in col 1.
    if not s.startswith('|'):
        continue
    cells = [c.strip() for c in s.strip('|').split('|')]
    if not cells:
        continue
    first = cells[0]
    if UUID_RE.fullmatch(first):
        manifest_uuids.add(first.lower())

if not manifest_uuids:
    sys.exit(f'ERROR: parsed 0 conv_uuids from manifest {manifest_path} — '
             f'format changed? HALT rather than emit a no-exclusion worklist.')

manifest_prefixes = {u[:8] for u in manifest_uuids}
print(f'Manifest baseline : {manifest_path.name}')
print(f'  harvested convs  : {len(manifest_uuids)} (full UUIDs)')

# ---------------------------------------------------------------------------
# Step B — GLOB CROSS-CHECK. Reduce on-disk node files to conv prefixes, reconcile
#          against the manifest by 8-char prefix. Drift > tolerance => HALT.
#
#   File shapes (per S48 format grab):
#     <full-uuid>.md                         -> uuid-node       (full UUID in name)
#     <full-uuid>.md.parents.json            -> sidecar         (IGNORE)
#     result_<prefix>.md                     -> result/whale    (prefix only)
#     result_<prefix>_chunk_NN.md            -> whale chunk      (prefix only)
#     confirm_<prefix>_chunk_NN.md           -> confirm chunk    (prefix only)
#     confirm_<prefix>_whole.md              -> confirm whole    (prefix only)
#     MERGE_MANIFEST_*.md                    -> index            (IGNORE)
# ---------------------------------------------------------------------------
disk_prefixes = set()
unparseable = []
for p in sorted(glob.glob(str(harvested_dir / '*'))):
    name = os.path.basename(p)
    if name.endswith('.parents.json'):
        continue
    if 'MANIFEST' in name.upper():   # index files (MERGE_MANIFEST_S47.md, S37 cold-store MANIFEST.md) — not nodes
        continue
    if not name.endswith('.md'):
        continue
    m = re.match(r'^(?:result_|confirm_)?([0-9a-f]{8})', name, re.I)
    if m:
        disk_prefixes.add(m.group(1).lower())
    else:
        unparseable.append(name)

# Reconcile by prefix
in_manifest_not_disk = manifest_prefixes - disk_prefixes   # manifest says done, no file
in_disk_not_manifest = disk_prefixes - manifest_prefixes   # file on disk, manifest blind

drift = len(in_manifest_not_disk) + len(in_disk_not_manifest) + len(unparseable)
print(f'Glob cross-check  : {len(disk_prefixes)} conv prefixes on disk')
print(f'  manifest-not-disk: {len(in_manifest_not_disk)}  '
      f'disk-not-manifest: {len(in_disk_not_manifest)}  '
      f'unparseable: {len(unparseable)}')

if drift > args.crosscheck_tolerance:
    print('\n*** CROSS-CHECK HALT — manifest and disk disagree beyond tolerance '
          f'({drift} > {args.crosscheck_tolerance}). Writing NOTHING. ***')
    if in_manifest_not_disk:
        print(f'  manifest lists, no file on disk: {sorted(in_manifest_not_disk)}')
    if in_disk_not_manifest:
        print(f'  file on disk, not in manifest  : {sorted(in_disk_not_manifest)}')
    if unparseable:
        print(f'  unparseable filenames          : {unparseable}')
    print('  Resolve the drift (manifest stale? stray file? new node un-indexed?) '
          'before building the worklist.')
    sys.exit(2)

print('  cross-check PASS — manifest reconciles with disk.')

# ---------------------------------------------------------------------------
# Step C — query the floor, exclude whales + already-harvested, build rows
#          (floor-query + char_count + verdict carried verbatim from v1)
# ---------------------------------------------------------------------------
import psycopg

EXCLUDE = WHALE_UUIDS | manifest_uuids

print('\nConnecting to floor...', flush=True)
rows = []
skipped_harvested = 0
skipped_whale = 0
with psycopg.connect(db_url) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT DISTINCT ON (conv_uuid)
                conv_uuid::text, snapshot_id, message_count, created_at
            FROM floor_conv_headers
            ORDER BY conv_uuid, scrub_version DESC, snapshot_id DESC
        """)
        headers = cur.fetchall()
        print(f'  Headers: {len(headers)} convs (all snapshots, pre-exclusion)')

        for conv_uuid, snapshot_id, message_count, created_at in headers:
            cu = conv_uuid.lower()
            if cu in WHALE_UUIDS:
                skipped_whale += 1
                continue
            if cu in manifest_uuids:
                skipped_harvested += 1
                continue

            cur.execute("""
                SELECT content_blocks
                FROM floor_conv_messages
                WHERE snapshot_id = %s AND conv_uuid = %s::uuid
            """, (snapshot_id, conv_uuid))
            msg_rows = cur.fetchall()

            char_count = sum(
                len(json.dumps(row[0], default=str))
                for row in msg_rows
            )
            proxy_est_tokens = char_count / 3.5

            if proxy_est_tokens <= 25_000:
                verdict = 'FITS_WHOLE'
            elif proxy_est_tokens <= 30_000:
                verdict = 'REVIEW'   # FITS_WHOLE on arithmetic: 30K*3x=90K << 950K
            elif proxy_est_tokens > 317_000:
                verdict = 'CHUNK_LATER'
            else:
                verdict = 'FITS_WHOLE'

            rows.append({
                'conv_uuid': conv_uuid,
                'source': f'floor:{snapshot_id}',
                'msg_count': message_count,
                'char_count': char_count,
                'proxy_est_tokens': round(proxy_est_tokens),
                'authoritative_tokens': '',  # count_tokens requires billing key
                'verdict': verdict,
                'payload_status': 'pending',
            })

    conn.rollback()

# ---------------------------------------------------------------------------
# Step D — write worklist
# ---------------------------------------------------------------------------
out_path = REPO_PIPELINE.parent / 'wallaby-way' / 'runs' / '2026-06-08' / 'worklist.csv'
fieldnames = ['conv_uuid', 'source', 'msg_count', 'char_count',
              'proxy_est_tokens', 'authoritative_tokens', 'verdict', 'payload_status']
with open(out_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

fits   = sum(1 for r in rows if r['verdict'] == 'FITS_WHOLE')
review = sum(1 for r in rows if r['verdict'] == 'REVIEW')
chunk  = sum(1 for r in rows if r['verdict'] == 'CHUNK_LATER')
print(f'\nWorklist written: {out_path}')
print(f'  Floor convs total     : {len(headers)}')
print(f'  Excluded (whale)      : {skipped_whale}')
print(f'  Excluded (harvested)  : {skipped_harvested}')
print(f'  NEW convs (worklist)  : {len(rows)}')
print(f'    FITS_WHOLE          : {fits}')
print(f'    REVIEW (proxy 25-30K): {review}')
print(f'    CHUNK_LATER         : {chunk}')
print('Note: authoritative_tokens blank — count_tokens unavailable without billing key')
print('Note: REVIEW-band is FITS_WHOLE on arithmetic (30K*3x=90K << 950K ceiling)')

if len(rows) == 0:
    print('\nWORKLIST IS EMPTY — no new convs in the floor beyond the harvested pile.')
    print('If you have NOT yet run the delta-freeze, this is EXPECTED: freeze first, then re-run.')
    if not args.allow_empty:
        sys.exit(3)
