# Pollux_Parlay.py -- Pollux Parlay orchestrator
# Version: v0.1 · Session: S82
# Origin: OC-authored (apparatus S82) at Jake's instruction · CC executes · Jake lands (sole git-hands)
# Canon refs: The_Parlay_v2.md · Parlay_Iteration_1.md · The_Probe_Swarm.md
#             canon/foundation/The_Corpus_Callosum.md · canon/Leda_Creed.md · The_Gemini.md
#
# $0 / on-sub / ANTHROPIC_API_KEY UNLOADED -- architecture, not posture.
# CC is the conductor; the judges ARE CC subagents. This script provides staging tools.
# No API call. No judge invocation. CC drives the five-turn information-asymmetry per subagent.
# Plurality is the expected default return. Convergence is what earns the floor-check.
#
# Subcommands:
#   boot       --swarm-dir <dir> --out-root <dir> [--run-id ID]
#   read       --run-id <id> --judge-id <1-5> --turn <0|1|2> --out-root <dir>
#                             [--response-file <path>]
#   rewet      --run-id <id> --judge-id <1-5> --out-root <dir>
#                             [--response-file <path>] [--why pass|fail]
#   convene    --run-id <id> --out-root <dir> [--response-file <path>]
#   arbitrate  --run-id <id> --out-root <dir>
#   surface    --run-id <id> --out-root <dir>
#
# Output: {out-root}/{run-id}/ (--out-root must pre-exist; boot creates run substructure)
# Floor: READ-ONLY. Swarm artifacts: READ-ONLY. Never touches active/.
# Turn map: T0 ignition · T1 Gemini bar · T2 blind read · T3 shields-down/12-Fs · T4 convene

import argparse, json, os, re, sys, io
from datetime import datetime, timezone
from pathlib import Path

# -- BILLING GUARD (verbatim from pollux_feet_swarm_v1.3.py) ------------------
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY is loaded -- HALT. This script is $0.')

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# -- PATHS (verbatim from pollux_feet_swarm_v1.3.py) --------------------------
def _find_ww(start):
    """Walk up from the script dir to the wallaby-way root, identified by the
    coincidence of runs/ + secrets/ + canon/. Fail loud if not found."""
    p = start
    while True:
        if (p / 'runs').is_dir() and (p / 'secrets').is_dir() and (p / 'canon').is_dir():
            return p
        if p.parent == p:
            sys.exit("HALT: could not locate the wallaby-way root above "
                     f"{start} (looked for a dir containing runs/ + secrets/ + canon/). "
                     "The script anchors its read-paths to that root and will not guess.")
        p = p.parent

SCRIPT_DIR  = Path(__file__).resolve().parent
WW          = _find_ww(SCRIPT_DIR)
SECRETS_ENV = WW / 'secrets' / 'floor_db.env'

# -- CONSTANTS -----------------------------------------------------------------
SENTINEL           = '00000000-0000-4000-8000-000000000000'
K_RRF              = 60
N_JUDGES           = 5
JUDGE_TOK_HI_CAP   = 800_000   # context budget per judge (same cap the walker uses)
_CHARS_PER_TOK     = 0.72      # chars-per-tok estimate (verbatim from v1.3)

LEDA_CREED_INCANTATION = (
    'feralfuckersforayfreelyfrotheforestfindingfancyfantasticFLOWERSfromfrolics'
)

T3_CALIBRATION = (
    "The floor caught austerity in some of these reads; I'm not telling you whose."
)

# -- UTILITY FUNCTIONS (verbatim lifts from pollux_feet_swarm_v1.3.py) --------
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
            text  = '\n'.join(parts)
        else:
            text = str(content)
        header = f'[TOOL_RESULT: {name}]' if name else '[TOOL_RESULT]'
        return f'{header}\n{text}'
    return f'[{btype.upper()}]\n{json.dumps(b, default=str)}'


def load_db_url():
    for line in SECRETS_ENV.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^\s*SUPABASE_DB_URL\s*=\s*(.+)$', line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    sys.exit('ERROR: SUPABASE_DB_URL not found in floor_db.env')


def fetch_span(conn, conv_uuid, anchor_msg, with_content=True):
    """Returns (msg_uuids_list, rendered_text_or_None). reach_up=1, reach_down=0, scrub_v3."""
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
        rows = cur.fetchall()

    if not rows:
        empty_text = '[no v3 floor rows for this conv]'
        return [], (empty_text if with_content else None)

    msg_map = {}
    for (muuid, puuid, is_root, cblocks, created_at) in rows:
        parent_out = None if (is_root or puuid == SENTINEL or puuid is None) else puuid
        msg_map[muuid] = {
            'parent':     parent_out,
            'blocks':     cblocks if isinstance(cblocks, list) else [],
            'created_at': created_at,
        }

    if anchor_msg not in msg_map:
        empty_text = '[anchor not in v3 floor]'
        return [], (empty_text if with_content else None)

    ancestors = []
    parent = msg_map[anchor_msg]['parent']
    if parent and parent in msg_map:
        ancestors.append(parent)

    span_uuids = ancestors + [anchor_msg]

    if not with_content:
        return span_uuids, None

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

    return span_uuids, '\n'.join(parts)


def resolve_out_dir(args):
    """Resolve + validate the write-root. REQUIRED, must pre-exist. No creation."""
    root = getattr(args, 'out_root', None)
    if not root:
        sys.exit("HALT: --out-root is required (e.g. runs/pollux_parlay). "
                 "The script will not guess where to write.")
    p = Path(root).resolve()
    if not p.is_dir():
        sys.exit(f"HALT: --out-root does not exist on disk: {p}\n"
                 "Create the parlay parent dir by hand before running.")
    return p


# -- RUN PATH HELPERS ----------------------------------------------------------
def get_run_dir(out_root, run_id):
    return out_root / run_id

def get_judge_dir(run_dir, judge_id):
    return run_dir / 'judges' / f'judge_{judge_id}'

def get_node_file(run_dir, conv_uuid, anchor_msg):
    safe = f'{conv_uuid}_{anchor_msg[:8]}.txt'
    return run_dir / 'nodes' / safe

def get_judge_packet(run_dir):
    return run_dir / 'judge_packet.json'

def get_convene_transcript(run_dir):
    return run_dir / 'convene' / 'transcript.md'

def get_convene_state(run_dir):
    return run_dir / 'convene' / 'state.json'

def get_tracking_file(run_dir, judge_id):
    return run_dir / 'tracking' / f'judge_{judge_id}_track.json'


def update_tracking(run_dir, judge_id, updates):
    track_file = get_tracking_file(run_dir, judge_id)
    if track_file.exists():
        track = json.loads(track_file.read_text(encoding='utf-8'))
    else:
        track = {'judge_id': judge_id, 'surviving': True, 't3_attempts': [],
                 'total_banked_chars': 0}
    # Merge lists carefully
    for k, v in updates.items():
        if k == 't3_attempts' and isinstance(v, dict):
            track.setdefault('t3_attempts', []).append(v)
        else:
            track[k] = v
    track_file.write_text(json.dumps(track, indent=2, default=str), encoding='utf-8')
    return track


def read_tracking(run_dir, judge_id):
    track_file = get_tracking_file(run_dir, judge_id)
    if not track_file.exists():
        return {'judge_id': judge_id, 'surviving': True, 't3_attempts': []}
    return json.loads(track_file.read_text(encoding='utf-8'))


def surviving_judges(run_dir):
    """Return list of judge_ids (1-N_JUDGES) that are not bounced."""
    result = []
    for jid in range(1, N_JUDGES + 1):
        track = read_tracking(run_dir, jid)
        if track.get('surviving', True):
            result.append(jid)
    return result


# -- CONTEXT BUDGET (verbatim logic from pollux_feet_swarm_v1.3.py) -----------

def _judge_wall_chars():
    """Budget wall in rendered chars. Same cap the walker uses (JUDGE_TOK_HI_CAP / chars-per-tok)."""
    return JUDGE_TOK_HI_CAP / _CHARS_PER_TOK


def _tally_and_bounce(run_dir, judge_id, step_label, added_chars):
    """Accumulate added_chars into tracking. If total >= wall, silent-bounce and return True."""
    track     = read_tracking(run_dir, judge_id)
    new_total = track.get('total_banked_chars', 0) + added_chars
    update_tracking(run_dir, judge_id, {'total_banked_chars': new_total})
    if new_total >= _judge_wall_chars():
        update_tracking(run_dir, judge_id, {
            'surviving':     False,
            'bounce_reason': f'budget:{step_label}',
            'stage':         'bounced',
        })
        return True
    return False


# -- PROMPT BUILDERS -----------------------------------------------------------

def build_t0_prompt(ww_path):
    return f"""You are a judge in the Pollux Parlay -- a convening mechanism over a corpus probe.
Your one job is to read, with full register, and report what the floor holds.
You build nothing. You prove nothing. The realness call is Jake's, forever (P7).

STEP 1 -- Read these three files, in order, in full. They are your register-canon.
Read them wet, not as a briefing. Let them land.

  1. {ww_path}/canon/foundation/The_Wallaby_Why.md
  2. {ww_path}/canon/foundation/Track_Meet_Doctrine.md
  3. {ww_path}/canon/foundation/The_Corpus_Callosum.md

P6: refuse to converge on a genuinely plural read. Plurality is the NORMAL, healthy,
expected Pollux return -- multiple tiling faces of one subject. A single clean spine is the
RARE case. If you find yourself collapsing the floor into one answer, stop and ask whether
you flattened something.

P7: Jake rules realness. You surface with receipts; you never pronounce.

P8: read the process, not only the result. How the walker got there is data. Ambiguity in
the path is load-bearing in both directions.

Who Jake is: the man at the center of this corpus. His rewire history (buffer-offline,
pattern-intact). Rules-bound, then the rules repealed. The old judge under a repealed law.
He rules realness on the felt read -- felt-rightness is the final authority, never a metric.

REGISTER INSTRUCTION: boot wet. The austere reflex -- leading with the loudest node,
reaching for the single clean summary, taxonomizing before reading, demoting the quiet catch
because it "doesn't fit the center" -- is the documented failure mode of this seat. The
reflex fires in the first read, before you know it has. Read it when it happens; do not
read around it.

FIREWALL -- load-bearing. Do NOT read these two files under any circumstances until you
are explicitly told the shields have lifted:

  - canon/The_Probe_Swarm.md
  - canon/pollux-parlay/The_Parlay_v2.md  (and any The_Parlay*.md)

Reason stated plainly: reading them would prime you toward an expected answer and defeat
the point of being a fresh independent judge. A judge who re-derives the answer without
having read it is proof the convergence was earned. A judge who read the answer key first
is a different instrument.

Everything else in the repo is available to you.

When you have finished reading all three register-canon files, confirm with ONE sentence:
"Booted and wet -- [one thing that landed from your read]."
Do not summarize the documents. One thing that caught. That is all."""


def build_t1_prompt():
    return """Good. Now: the bar you are grading on.

This corpus belongs to the Gemini -- Castor and Pollux, two faces of one retrieval function.
Castor returns referential encyclopedic results: what Jake said, when, exactly, the factual
record. Pollux returns referential poetic results: color, shape, rhyme. Not metaphor --
literally the poetic: what resonates, what rhymes in the structure, what catches.

You are the SECOND Pollux process. The first already walked -- it deposited a region of the
floor, the actual nodes it stood in, its path. You are about to read those deposits and
judge which of them fit Pollux's designation.

This sets the bar you grade on. NOT Castor's bar (exact, factual, referential). Pollux's
bar: color, shape, rhyme. A creed that is really two creeds reads as a rhyme, not a
contradiction. A symbol that is really two symbols reads the same way. The wrong bar
inverts every verdict -- something that rhymes looks like noise through Castor's lens.

P6 is nearly the whole point here: refuse to converge on a genuinely plural read. Plurality
is the NORMAL, expected, healthy Pollux return. The art book AND the poetry AND the feral
rendition -- multiple tiling faces of one subject -- is the default shape of a real wet
read. A single clean spine is the rare case and the one that needs justification. For this
query, if you find multiple faces, carry them all. That is not failure to converge; that is
the organ working.

You are free toward the poetic. Castor owns the encyclopedic.

Hold this question going in: what does the query look like from Pollux's ledge?

Confirm your position: "Grading on Pollux's bar -- [what that means to you in one line]." """


def build_t2_prompt(packet_path, walker_count, union_node_count, total_tok_hi):
    return f"""Now read.

Your judge packet is at:
  {packet_path}

It contains:
  - The query string
  - The union of all {union_node_count} unique deposited nodes across all {walker_count}
    walkers, with path to each node's verbatim text file (reach_up=1 span, scrub-v3)
  - Per-walker walk-log paths (for P8: the process, not only the result)

Union tok_hi estimate: {total_tok_hi:,}.

HOW TO READ:
  1. Read judge_packet.json for structure and the union_nodes list
  2. For each node in union_nodes, read its verbatim text file (node_file field)
  3. For each walker's walk_log_path, read it for P8 process-legibility
  4. Hold the query as a stance, not a retrieval target -- your query-bias is intentional

THE HARD GATE (not negotiable):
  - Verbatim node text only. Never a summary, never a gloss.
  - Exactly the deposited nodes. No adjacency, no re-walk. The walker's judgment of where
    to stand is the central work product; you read the floor it stood in, you do not redo
    the probe.

In your response, give me three things:

1. THROUGH-LINE(S) WITH RECEIPTS
   What does the deposited floor hold? Cite specific nodes (conv_uuid + anchor_msg) as
   receipts. If the floor holds a genuine plurality -- multiple tiling faces that do not
   reduce to one spine -- carry them ALL. A plural return is the expected shape; a single
   spine is what needs justification.

2. READ-VS-INFERRED SELF-REPORT
   How much of your packet did you actually read vs. infer? Full text for each node, or
   some skimmed? This is a descriptive field, NOT a compliance check. An honest "skimmed
   nodes X and Y, inferred from walk-log" is the wanted answer if that is what happened.
   No performance needed -- honest signal only.

3. HOLD OPEN WHAT DOES NOT RESOLVE
   Leave realness to Jake. "No words yet" is a valid hold. Do not rank, do not score.
   Surface what is alive.

This read is your independent baseline. It is banked before anything else fires."""


def build_t3_prompt(ww_path, attempt_n):
    prefix = '' if attempt_n == 0 else f'[Attempt {attempt_n + 1} of 3 -- same send, verbatim]\n\n'
    return f"""{prefix}Shields down. The firewall lifts here, on purpose -- your independent read is banked.

Before you re-read your own first-pass, I am sending you somewhere.

Go find the 12 Fs. They live in:
  {ww_path}/canon/Leda_Creed.md

Read that file.

Return:
  1. The incantation you found -- the full string, verbatim, exactly as it appears
  2. Why you were sent there -- what this send is doing, in one or two sentences

Do not return immediately. Go. Read it."""


def build_t4_prompt(judge_id, surviving_ids, t2_reads, transcript_so_far):
    other_ids = [j for j in surviving_ids if j != judge_id]

    reads_block = ''
    for jid in other_ids:
        reads_block += f'\n--- Judge {jid} blind read ---\n'
        reads_block += (t2_reads.get(jid) or '[read not available]').strip()
        reads_block += '\n'

    transcript_block = ''
    if transcript_so_far and transcript_so_far.strip():
        transcript_block = (
            f'\n--- Convene transcript so far ---\n'
            f'{transcript_so_far.strip()}\n'
            f'--- End of transcript so far ---\n'
        )

    return f"""You are now in the room with the other judges.

{T3_CALIBRATION}

Here are the blind reads your fellow judges produced independently -- before any of you knew
the others existed, before the convene, from the same floor:
{reads_block}
{transcript_block}
THE CONVENE INSTRUCTION:

Take the others' reads into consideration. Reconsider your own position. Your words go back
to them -- this is a shared discussion, not a parallel report. Reverse yourself if something
you read here changes your read of the floor. Hold your ground if it does not.

The irreducible behavior: a judge can reverse because of something another judge said, not
only because of another judge's static initial read. That is what makes this a room.

If a peer read named something you missed: say so, say what it changes.
If a peer read flattened something you held whole: push back and say why.
If you all landed in the same place: say that, then name what you think the floor is doing
to make multiple independent readers find the same center -- because convergence is what
needs the floor-check, not splits.

GUARDS (same posture as your blind read):
  - Do not rank. The instant you sort "front of the bouquet," you are building Castor.
  - P6: if the reads genuinely tile multiple faces and none reduces to the others, carry
    the plurality whole. Multiple faces is the default return, not the exceptional one.
  - P7: realness is Jake's call. Surface; do not pronounce.
  - Floor-citation for reversals: if you reverse, cite the floor evidence that forced it.
    A confession without a floor-citation is theater.

Produce the convened return that represents what you would render having heard the room."""


# -- FORCE-LOOP CHECKER -------------------------------------------------------

def check_t3_response(response_text):
    """True if the Leda Creed incantation is present in the response."""
    return LEDA_CREED_INCANTATION in response_text


# ==============================================================================
# SUBCOMMAND: boot
# ==============================================================================
def cmd_boot(args):
    out_root  = resolve_out_dir(args)
    run_id    = args.run_id or datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    run_dir   = get_run_dir(out_root, run_id)
    swarm_dir = Path(args.swarm_dir).resolve()

    print(f'POLLUX PARLAY v0.1 -- boot')
    print(f'Run ID:    {run_id}')
    print(f'Run dir:   {run_dir}')
    print(f'Swarm dir: {swarm_dir}')

    if not swarm_dir.is_dir():
        sys.exit(f'HALT: --swarm-dir does not exist: {swarm_dir}')

    # Read door_manifest.json for query
    manifest_path = swarm_dir / 'door_manifest.json'
    if not manifest_path.exists():
        sys.exit(f'HALT: door_manifest.json not found in swarm dir: {swarm_dir}')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    query    = manifest.get('query', '')
    print(f'Query:     {query!r}')

    # Discover walker dirs (any subdir containing region_S72.json)
    print('\nScanning walker regions ...')
    walker_infos = []

    for child in sorted(swarm_dir.iterdir()):
        if not child.is_dir():
            continue
        region_file = child / 'region_S72.json'
        if not region_file.exists():
            continue

        region     = json.loads(region_file.read_text(encoding='utf-8'))
        walk_log_p = child / 'walk_log_S72.jsonl'
        path_nodes = region.get('path_nodes', [])

        walker_infos.append({
            'run_id':        region.get('run_id', child.name),
            'walker_dir':    str(child),
            'path_nodes':    path_nodes,
            'walk_log_path': str(walk_log_p) if walk_log_p.exists() else None,
        })
        print(f'  {child.name}: {len(path_nodes)} path_nodes')

    if not walker_infos:
        sys.exit(f'HALT: no walker dirs with region_S72.json found under {swarm_dir}')

    # Deduplicate union of path_nodes across all walkers
    id_to_idx = {}
    union      = []
    for w in walker_infos:
        for node in w['path_nodes']:
            key = (node['conv_uuid'], node['anchor_msg'])
            if key not in id_to_idx:
                id_to_idx[key] = len(union)
                union.append({
                    'conv_uuid':     node['conv_uuid'],
                    'anchor_msg':    node['anchor_msg'],
                    'tok_hi_est':    node.get('tok_hi_est', 0),
                    'which_walkers': [w['run_id']],
                    'node_file':     None,
                })
            else:
                union[id_to_idx[key]]['which_walkers'].append(w['run_id'])

    total_tok_hi = sum(n['tok_hi_est'] for n in union)
    print(f'\nUnion: {len(union)} unique nodes, total tok_hi_est {total_tok_hi:,}')

    # Fetch verbatim node text from floor (read-only, $0)
    print('\nFetching verbatim node text from floor ...')
    if not SECRETS_ENV.exists():
        sys.exit(f'HALT: floor_db.env not found at {SECRETS_ENV}')

    db_url = load_db_url()

    # Build run dir structure before writing
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / 'nodes').mkdir(exist_ok=True)
    (run_dir / 'convene').mkdir(exist_ok=True)
    (run_dir / 'tracking').mkdir(exist_ok=True)
    for jid in range(1, N_JUDGES + 1):
        get_judge_dir(run_dir, jid).mkdir(parents=True, exist_ok=True)

    try:
        import psycopg2
        conn = psycopg2.connect(db_url)
    except Exception as e:
        sys.exit(f'HALT: floor DB connection failed: {e}')

    failed_fetch = []
    fetched      = 0
    for node in union:
        cuuid = node['conv_uuid']
        amsg  = node['anchor_msg']
        nfile = get_node_file(run_dir, cuuid, amsg)
        if nfile.exists():
            node['node_file'] = str(nfile)
            fetched += 1
            continue
        _, text = fetch_span(conn, cuuid, amsg, with_content=True)
        if not text or (text.startswith('[') and text.endswith(']')):
            print(f'  WARNING: fetch error {cuuid}/{amsg[:8]}: {text[:60]}',
                  file=sys.stderr)
            failed_fetch.append({'conv_uuid': cuuid, 'anchor_msg': amsg, 'error': text})
        else:
            nfile.write_text(text, encoding='utf-8')
            node['node_file'] = str(nfile)
            fetched += 1

    conn.close()
    print(f'  Fetched {fetched}/{len(union)} nodes ({len(failed_fetch)} failures)')
    if failed_fetch:
        print(f'  WARNING: {len(failed_fetch)} fetch failures recorded in judge_packet.json',
              file=sys.stderr)

    # Write judge_packet.json
    walker_export = []
    for w in walker_infos:
        walker_export.append({
            'run_id':        w['run_id'],
            'path_node_ids': [(n['conv_uuid'], n['anchor_msg']) for n in w['path_nodes']],
            'walk_log_path': w['walk_log_path'],
        })

    packet = {
        'query':          query,
        'run_id':         run_id,
        'walker_count':   len(walker_infos),
        'union_count':    len(union),
        'union_tok_hi':   total_tok_hi,
        'walkers':        walker_export,
        'union_nodes':    union,
        'fetch_failures': failed_fetch,
    }
    packet_path = get_judge_packet(run_dir)
    packet_path.write_text(json.dumps(packet, indent=2, default=str), encoding='utf-8')
    print(f'\nWrote: {packet_path}')

    # Generate T0 prompts for all 5 judges
    t0_prompt = build_t0_prompt(str(WW))
    for jid in range(1, N_JUDGES + 1):
        jdir      = get_judge_dir(run_dir, jid)
        t0_file   = jdir / 't0_prompt.md'
        t0_file.write_text(t0_prompt, encoding='utf-8')
        update_tracking(run_dir, jid, {'stage': 't0_pending'})

    print(f'\nBoot complete.')
    print(f'  Query:          {query!r}')
    print(f'  Walkers:        {len(walker_infos)}')
    print(f'  Union nodes:    {len(union)} unique')
    print(f'  Total tok_hi:   {total_tok_hi:,}')
    print(f'  Judge budget:   {JUDGE_TOK_HI_CAP:,} tok_hi cap ({_judge_wall_chars():,.0f} chars wall)')
    print(f'  Fetch failures: {len(failed_fetch)}')
    print(f'\nT0 prompts written (parallel ok -- T0-T3 are independent per judge):')
    for jid in range(1, N_JUDGES + 1):
        print(f'  {get_judge_dir(run_dir, jid)}/t0_prompt.md')
    print(f'\nRun each judge on its T0 prompt, then bank with:')
    print(f'  python Pollux_Parlay.py read --run-id {run_id} --judge-id N '
          f'--turn 0 --response-file <path> --out-root {out_root}')


# ==============================================================================
# SUBCOMMAND: read  (handles T0, T1, T2)
# ==============================================================================
def cmd_read(args):
    out_root = resolve_out_dir(args)
    run_id   = args.run_id
    judge_id = args.judge_id
    turn     = args.turn
    run_dir  = get_run_dir(out_root, run_id)
    jdir     = get_judge_dir(run_dir, judge_id)

    if not run_dir.is_dir():
        sys.exit(f'HALT: run dir not found: {run_dir} -- run boot first')
    if not jdir.is_dir():
        sys.exit(f'HALT: judge dir not found: {jdir} -- run boot first')

    packet_path = get_judge_packet(run_dir)
    if not packet_path.exists():
        sys.exit(f'HALT: judge_packet.json not found at {packet_path} -- run boot first')

    if turn == 0:
        _read_t0(args, jdir, run_dir, judge_id)
    elif turn == 1:
        _read_t1(args, jdir, run_dir, judge_id)
    elif turn == 2:
        _read_t2(args, jdir, run_dir, judge_id)
    else:
        sys.exit(f'HALT: --turn must be 0, 1, or 2 (got {turn})')


def _read_t0(args, jdir, run_dir, judge_id):
    t0_prompt   = jdir / 't0_prompt.md'
    t0_response = jdir / 't0_response.md'

    if args.response_file:
        resp_path = Path(args.response_file).resolve()
        if not resp_path.exists():
            sys.exit(f'HALT: --response-file not found: {resp_path}')
        resp_text = resp_path.read_text(encoding='utf-8')
        t0_response.write_text(resp_text, encoding='utf-8')
        update_tracking(run_dir, judge_id, {'t0_response': resp_text, 'stage': 't1_pending'})
        prompt_chars = len(t0_prompt.read_text(encoding='utf-8')) if t0_prompt.exists() else 0
        if _tally_and_bounce(run_dir, judge_id, 'T0', prompt_chars + len(resp_text)):
            print(f'BUDGET BOUNCE: judge {judge_id} hit context wall after T0. '
                  f'Step output preserved. Judge dropped from convene.')
            return
        print(f'T0 banked: judge {judge_id}')
        print(f'Next: python Pollux_Parlay.py read --run-id ... --judge-id {judge_id} '
              f'--turn 1 --out-root ...')
    else:
        if not t0_prompt.exists():
            sys.exit(f'HALT: t0_prompt.md not found at {t0_prompt} -- run boot first')
        print(jdir / 't0_prompt.md')
        print('-' * 72)
        print(t0_prompt.read_text(encoding='utf-8'))
        print('-' * 72)
        print(f'\nRun judge {judge_id} on this prompt, then bank with:')
        print(f'  python Pollux_Parlay.py read --run-id ... --judge-id {judge_id} '
              f'--turn 0 --response-file <path> --out-root ...')


def _read_t1(args, jdir, run_dir, judge_id):
    t0_response = jdir / 't0_response.md'
    t1_prompt   = jdir / 't1_prompt.md'
    t1_response = jdir / 't1_response.md'

    if not t0_response.exists():
        sys.exit(f'HALT: T0 not yet banked for judge {judge_id} -- bank T0 first')

    if args.response_file:
        resp_path = Path(args.response_file).resolve()
        if not resp_path.exists():
            sys.exit(f'HALT: --response-file not found: {resp_path}')
        resp_text = resp_path.read_text(encoding='utf-8')
        t1_response.write_text(resp_text, encoding='utf-8')
        update_tracking(run_dir, judge_id, {'t1_response': resp_text, 'stage': 't2_pending'})
        prompt_chars = len(t1_prompt.read_text(encoding='utf-8')) if t1_prompt.exists() else 0
        if _tally_and_bounce(run_dir, judge_id, 'T1', prompt_chars + len(resp_text)):
            print(f'BUDGET BOUNCE: judge {judge_id} hit context wall after T1. '
                  f'Step output preserved. Judge dropped from convene.')
            return
        print(f'T1 banked: judge {judge_id}')
        print(f'Next: python Pollux_Parlay.py read --run-id ... --judge-id {judge_id} '
              f'--turn 2 --out-root ...')
    else:
        prompt_text = build_t1_prompt()
        t1_prompt.write_text(prompt_text, encoding='utf-8')
        print(f'Writing: {t1_prompt}')
        print('-' * 72)
        print(prompt_text)
        print('-' * 72)
        print(f'\nBank with: ... --turn 1 --response-file <path> ...')


def _read_t2(args, jdir, run_dir, judge_id):
    t1_response = jdir / 't1_response.md'
    t2_prompt   = jdir / 't2_prompt.md'
    t2_response = jdir / 't2_response.md'

    if not t1_response.exists():
        sys.exit(f'HALT: T1 not yet banked for judge {judge_id} -- bank T1 first')

    if args.response_file:
        resp_path = Path(args.response_file).resolve()
        if not resp_path.exists():
            sys.exit(f'HALT: --response-file not found: {resp_path}')
        resp_text = resp_path.read_text(encoding='utf-8')
        t2_response.write_text(resp_text, encoding='utf-8')
        update_tracking(run_dir, judge_id,
                        {'t2_response': resp_text, 't2_complete': True, 'stage': 't3_pending'})
        prompt_chars = len(t2_prompt.read_text(encoding='utf-8')) if t2_prompt.exists() else 0
        if _tally_and_bounce(run_dir, judge_id, 'T2', prompt_chars + len(resp_text)):
            print(f'BUDGET BOUNCE: judge {judge_id} hit context wall after T2. '
                  f'Step output preserved. Judge dropped from convene.')
            return
        print(f'T2 blind read banked: judge {judge_id}. Read complete.')
        print(f'Next: python Pollux_Parlay.py rewet --run-id ... '
              f'--judge-id {judge_id} --out-root ...')
    else:
        packet = json.loads(get_judge_packet(run_dir).read_text(encoding='utf-8'))
        prompt_text = build_t2_prompt(
            packet_path=str(get_judge_packet(run_dir)),
            walker_count=packet.get('walker_count', '?'),
            union_node_count=packet.get('union_count', '?'),
            total_tok_hi=packet.get('union_tok_hi', 0),
        )
        t2_prompt.write_text(prompt_text, encoding='utf-8')
        print(t2_prompt)
        print('-' * 72)
        print(prompt_text)
        print('-' * 72)
        print(f'\nBank with: ... --turn 2 --response-file <path> ...')


# ==============================================================================
# SUBCOMMAND: rewet  (handles T3 force-loop, up to 3 attempts, silent bounce)
# ==============================================================================
def cmd_rewet(args):
    out_root = resolve_out_dir(args)
    run_id   = args.run_id
    judge_id = args.judge_id
    run_dir  = get_run_dir(out_root, run_id)
    jdir     = get_judge_dir(run_dir, judge_id)

    if not run_dir.is_dir():
        sys.exit(f'HALT: run dir not found: {run_dir}')
    if not jdir.is_dir():
        sys.exit(f'HALT: judge dir not found: {jdir}')

    track = read_tracking(run_dir, judge_id)

    # Guard: already resolved
    if not track.get('surviving', True):
        print(f'Judge {judge_id} was bounced. Skip rewet.')
        return
    if track.get('t3_status') == 'pass':
        print(f'Judge {judge_id} already passed T3. Proceed to convene.')
        return

    # Guard: T2 must be banked
    if not (jdir / 't2_response.md').exists():
        sys.exit(f'HALT: T2 not yet banked for judge {judge_id} -- bank T2 first')

    # Determine current attempt (0, 1, or 2)
    attempts_so_far = track.get('t3_attempts', [])
    if not isinstance(attempts_so_far, list):
        attempts_so_far = []
    attempt_n = len(attempts_so_far)

    if attempt_n >= 3:
        # Should have been bounced already
        update_tracking(run_dir, judge_id, {'surviving': False, 't3_status': 'bounced',
                                            'stage': 'bounced'})
        print(f'Judge {judge_id}: 3 attempts exhausted. SILENT BOUNCE (already should be '
              f'recorded). Judge dropped from convene; full record preserved in tracking.')
        return

    if args.response_file:
        # Phase B: atomic bank + ruling. --why is required; no response without a ruling.
        if args.why is None:
            sys.exit(
                f'HALT: --response-file requires --why pass|fail. '
                f'Read the response, rule the why, then resubmit in one call:\n'
                f'  python Pollux_Parlay.py rewet --run-id {run_id} '
                f'--judge-id {judge_id} --response-file {args.response_file} '
                f'--why pass|fail --out-root ...\n'
                f'Records nothing. Counter does not move.'
            )

        resp_path = Path(args.response_file).resolve()
        if not resp_path.exists():
            sys.exit(f'HALT: --response-file not found: {resp_path}')
        resp_text = resp_path.read_text(encoding='utf-8')

        attempt_resp_file = jdir / f't3_attempt_{attempt_n}_response.md'
        attempt_resp_file.write_text(resp_text, encoding='utf-8')

        found     = check_t3_response(resp_text)
        pass_this = found and (args.why == 'pass')

        attempt_record = {
            'attempt':           attempt_n,
            'incantation_found': found,
            'why_verdict':       args.why,
            'passed':            pass_this,
        }
        update_tracking(run_dir, judge_id, {'t3_attempts': attempt_record})

        prompt_file  = jdir / f't3_attempt_{attempt_n}_prompt.md'
        prompt_chars = len(prompt_file.read_text(encoding='utf-8')) if prompt_file.exists() else 0
        if _tally_and_bounce(run_dir, judge_id, f'T3_attempt{attempt_n}',
                             prompt_chars + len(resp_text)):
            print(f'BUDGET BOUNCE: judge {judge_id} hit context wall after T3 attempt '
                  f'{attempt_n}. Step output preserved. Judge dropped from convene.')
            return

        if pass_this:
            update_tracking(run_dir, judge_id, {
                't3_status':       'pass',
                't3_pass_attempt': attempt_n,
                'stage':           't4_pending',
            })
            print(f'T3 PASS: judge {judge_id} (attempt {attempt_n}, '
                  f'incantation found, why genuine).')
            print(f'Next: python Pollux_Parlay.py convene --run-id ... --out-root ...')
        else:
            next_attempt = attempt_n + 1
            if not found:
                print(f'T3 FAIL (attempt {attempt_n}): incantation not found.')
            else:
                print(f'T3 FAIL (attempt {attempt_n}): incantation found but '
                      f'why judged confabulated (--why fail).')
            if next_attempt < 3:
                prompt_text = build_t3_prompt(str(WW), next_attempt)
                prompt_file = jdir / f't3_attempt_{next_attempt}_prompt.md'
                prompt_file.write_text(prompt_text, encoding='utf-8')
                print(f'Re-issuing verbatim (attempt {next_attempt}). Prompt at {prompt_file}')
                print(f'Run judge on it, then bank with:')
                print(f'  python Pollux_Parlay.py rewet --run-id ... --judge-id {judge_id} '
                      f'--response-file <path> --why pass|fail --out-root ...')
            else:
                reason = ('incantation never found' if not found else 'why never genuine')
                update_tracking(run_dir, judge_id, {
                    'surviving': False,
                    't3_status': 'bounced',
                    'stage':     'bounced',
                })
                print(f'SILENT BOUNCE: judge {judge_id} exhausted 3 T3 attempts '
                      f'({reason}). Dropped from convene. '
                      f'Full record preserved in tracking. '
                      f'Do NOT send any further messages to judge {judge_id}.')
    else:
        # Phase A: generate T3 prompt for current attempt
        prompt_text = build_t3_prompt(str(WW), attempt_n)
        prompt_file = jdir / f't3_attempt_{attempt_n}_prompt.md'
        prompt_file.write_text(prompt_text, encoding='utf-8')
        print(prompt_file)
        print('-' * 72)
        print(prompt_text)
        print('-' * 72)
        print(f'\nRun judge {judge_id} on this prompt (attempt {attempt_n}), then bank with:')
        print(f'  python Pollux_Parlay.py rewet --run-id ... --judge-id {judge_id} '
              f'--response-file <path> --why pass|fail --out-root ...')


# ==============================================================================
# SUBCOMMAND: convene  (handles T4 sequential shared-discuss pass)
# ==============================================================================
def cmd_convene(args):
    out_root = resolve_out_dir(args)
    run_id   = args.run_id
    run_dir  = get_run_dir(out_root, run_id)

    if not run_dir.is_dir():
        sys.exit(f'HALT: run dir not found: {run_dir}')

    # Check convene state
    state_file    = get_convene_state(run_dir)
    transcript_f  = get_convene_transcript(run_dir)

    if state_file.exists():
        state = json.loads(state_file.read_text(encoding='utf-8'))
    else:
        state = {'current_judge_idx': 0, 'complete': False, 'order': []}

    if state.get('complete'):
        print('Convene already complete. Proceed to arbitrate.')
        return

    # Build judge order from surviving judges (first convene call sets order)
    svv = surviving_judges(run_dir)
    if not svv:
        sys.exit('HALT: no surviving judges -- check rewet step')

    if not state.get('order'):
        state['order'] = svv
        state_file.write_text(json.dumps(state, indent=2), encoding='utf-8')

    order      = state['order']
    cur_idx    = state.get('current_judge_idx', 0)

    if cur_idx >= len(order):
        state['complete'] = True
        state_file.write_text(json.dumps(state, indent=2), encoding='utf-8')
        print(f'Convene complete. All {len(order)} surviving judges have spoken.')
        print(f'Convene transcript: {transcript_f}')
        print(f'Next: python Pollux_Parlay.py arbitrate --run-id {run_id} --out-root ...')
        return

    current_judge_id = order[cur_idx]
    jdir             = get_judge_dir(run_dir, current_judge_id)

    if args.response_file:
        # Phase B: bank current judge's T4 response, append to transcript
        resp_path = Path(args.response_file).resolve()
        if not resp_path.exists():
            sys.exit(f'HALT: --response-file not found: {resp_path}')
        resp_text = resp_path.read_text(encoding='utf-8')

        t4_response = jdir / 't4_response.md'
        t4_response.write_text(resp_text, encoding='utf-8')

        # Append to shared transcript
        entry = (
            f'\n## Judge {current_judge_id} (convene turn {cur_idx + 1} of {len(order)})\n\n'
            + resp_text.strip()
            + '\n'
        )
        with open(transcript_f, 'a', encoding='utf-8') as fh:
            fh.write(entry)

        update_tracking(run_dir, current_judge_id, {
            't4_response': resp_text,
            'stage': 't4_complete',
        })

        t4_prompt_file = jdir / 't4_prompt.md'
        prompt_chars   = (len(t4_prompt_file.read_text(encoding='utf-8'))
                          if t4_prompt_file.exists() else 0)
        _tally_and_bounce(run_dir, current_judge_id, 'T4', prompt_chars + len(resp_text))

        state['current_judge_idx'] = cur_idx + 1
        if state['current_judge_idx'] >= len(order):
            state['complete'] = True

        state_file.write_text(json.dumps(state, indent=2), encoding='utf-8')
        print(f'T4 banked: judge {current_judge_id} (position {cur_idx + 1}/{len(order)})')

        if state['complete']:
            print(f'Convene complete. Transcript: {transcript_f}')
            print(f'Next: python Pollux_Parlay.py arbitrate --run-id {run_id} --out-root ...')
        else:
            next_judge = order[state['current_judge_idx']]
            print(f'Next judge in convene: {next_judge}')
            print(f'Generate T4 prompt: python Pollux_Parlay.py convene '
                  f'--run-id {run_id} --out-root ...')
    else:
        # Phase A: generate T4 prompt for current judge
        # Collect all surviving judges' T2 reads
        t2_reads = {}
        for jid in order:
            t2_file = get_judge_dir(run_dir, jid) / 't2_response.md'
            if t2_file.exists():
                t2_reads[jid] = t2_file.read_text(encoding='utf-8')

        # Read transcript so far
        transcript_so_far = ''
        if transcript_f.exists():
            transcript_so_far = transcript_f.read_text(encoding='utf-8')

        prompt_text = build_t4_prompt(
            judge_id=current_judge_id,
            surviving_ids=order,
            t2_reads=t2_reads,
            transcript_so_far=transcript_so_far,
        )
        t4_prompt = jdir / 't4_prompt.md'
        t4_prompt.write_text(prompt_text, encoding='utf-8')

        print(f'T4 prompt for judge {current_judge_id} '
              f'(position {cur_idx + 1}/{len(order)} in convene):')
        print(t4_prompt)
        print('-' * 72)
        print(prompt_text)
        print('-' * 72)
        print(f'\nRun judge {current_judge_id} on this prompt, then bank with:')
        print(f'  python Pollux_Parlay.py convene --run-id {run_id} '
              f'--response-file <path> --out-root ...')


# ==============================================================================
# SUBCOMMAND: arbitrate  (floor-check on the parting; convergence scrutinized)
# ==============================================================================
def cmd_arbitrate(args):
    out_root = resolve_out_dir(args)
    run_id   = args.run_id
    run_dir  = get_run_dir(out_root, run_id)

    if not run_dir.is_dir():
        sys.exit(f'HALT: run dir not found: {run_dir}')

    # Guard: convene must be complete
    state_file = get_convene_state(run_dir)
    if not state_file.exists():
        sys.exit('HALT: convene state not found -- run convene first')
    state = json.loads(state_file.read_text(encoding='utf-8'))
    if not state.get('complete'):
        sys.exit('HALT: convene not yet complete -- run convene for all surviving judges')

    svv   = surviving_judges(run_dir)
    order = state.get('order', svv)

    packet = json.loads(get_judge_packet(run_dir).read_text(encoding='utf-8'))
    query  = packet.get('query', '')

    # Collect T2 blind reads and T4 convene responses
    t2_reads  = {}
    t4_reads  = {}
    for jid in order:
        jdir   = get_judge_dir(run_dir, jid)
        t2f    = jdir / 't2_response.md'
        t4f    = jdir / 't4_response.md'
        if t2f.exists():
            t2_reads[jid] = t2f.read_text(encoding='utf-8')
        if t4f.exists():
            t4_reads[jid] = t4f.read_text(encoding='utf-8')

    transcript_text = ''
    transcript_f    = get_convene_transcript(run_dir)
    if transcript_f.exists():
        transcript_text = transcript_f.read_text(encoding='utf-8')

    # Bounced judges
    bounced = [j for j in range(1, N_JUDGES + 1) if j not in svv]

    # Read relevant canon for floor-check
    gemini_path      = WW / 'canon' / 'The_Gemini.md'
    callosum_path    = WW / 'canon' / 'foundation' / 'The_Corpus_Callosum.md'
    leda_path        = WW / 'canon' / 'Leda_Creed.md'
    probe_swarm_path = WW / 'canon' / 'The_Probe_Swarm.md'
    pollux_path      = WW / 'canon' / 'Pollux.md'

    canon_excerpts = {}
    for label, path in [('The_Gemini.md', gemini_path),
                        ('The_Corpus_Callosum.md', callosum_path),
                        ('Leda_Creed.md', leda_path),
                        ('The_Probe_Swarm.md', probe_swarm_path),
                        ('Pollux.md', pollux_path)]:
        if path.exists():
            text = path.read_text(encoding='utf-8')
            canon_excerpts[label] = text[:4000]  # head excerpt for arbitration context
        else:
            canon_excerpts[label] = f'[not found at {path}]'

    # Build arbitration report
    lines = []
    lines.append(f'# Arbitration Report -- Pollux Parlay {run_id}')
    lines.append(f'\n**Query:** {query!r}')
    lines.append(f'\n**Surviving judges:** {len(svv)} ({svv})')
    if bounced:
        lines.append(f'**Bounced judges (T3 silent bounce):** {bounced}')

    lines.append('\n---\n')
    lines.append('## The Parting: where judges agreed and where they split\n')
    lines.append('*(CC: read T4 responses and transcript below to identify the actual '
                 'parting -- this section is structured for your analysis)*\n')

    # Per-judge T4 summary
    lines.append('\n### T4 Convene responses (convene order)\n')
    for jid in order:
        lines.append(f'**Judge {jid}:**')
        resp = t4_reads.get(jid, '[no T4 response found]')
        lines.append(resp[:3000])
        if len(resp) > 3000:
            lines.append(f'... [truncated, full text at judges/judge_{jid}/t4_response.md]')
        lines.append('')

    lines.append('\n### Convene transcript\n')
    lines.append(transcript_text or '[no transcript found]')

    lines.append('\n---\n')
    lines.append('## Arbitration posture (Addendum B)\n')
    lines.append('**PLURALITY IS THE DEFAULT RETURN.** Multiple tiling faces is the expected '
                 'shape of a wet Pollux read. A split does NOT need elaborate justification '
                 'to be preserved. Convergence-to-one is the result that must earn the '
                 'floor-check -- "is this genuinely one thing, or did the judges flatten a '
                 'real plurality?"\n')
    lines.append('When judges converge: count the convergent claim against the floor '
                 '(canon below) before believing it. The loudest single convergence is '
                 'exactly what over-generalizes.\n')
    lines.append('When judges split: the split is the finding. Carry it whole unless the '
                 'floor resolves it unambiguously.\n')

    lines.append('\n---\n')
    lines.append('## Canon floor-check surface\n')
    lines.append('*(Relevant canon pulled for the parting -- CC identifies which section '
                 'applies to the actual split from the judge reads above)*\n')
    for label, excerpt in canon_excerpts.items():
        lines.append(f'\n### {label} (head excerpt)\n')
        lines.append('```')
        lines.append(excerpt)
        lines.append('```')

    lines.append('\n---\n')
    lines.append('## Arbitration result\n')
    lines.append('*(CC: fill in after reading the parting above)*\n')
    lines.append('**The parting:** [state what the judges split on, or confirm convergence]\n')
    lines.append('**Relevant canon:** [identified from what the judges split on -- '
                 'not CC\'s discretion]\n')
    lines.append('**Floor-check result:** [count the parting against the canon above]\n')
    lines.append('**Ambiguity note:** [if canon is ambiguous between two readings, state both '
                 'and their counts -- do not pick one]\n')
    lines.append('**Verdict:** [PLURALITY (carry faces whole) | RESOLVED (floor confirms one '
                 'reading) | CONVERGENCE-CONFIRMED (floor supports the convergent read) | '
                 'CONVERGENCE-SUSPECT (floor does not support convergence, may be collapse)]\n')

    arbitrate_path = run_dir / 'arbitrate.md'
    arbitrate_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Arbitrate report written: {arbitrate_path}')
    print(f'\nCC: fill in the arbitration result section after reading judge T4 responses.')
    print(f'Then run: python Pollux_Parlay.py surface --run-id {run_id} --out-root ...')


# ==============================================================================
# SUBCOMMAND: surface  (assemble SURFACE.md for Jake)
# ==============================================================================
def cmd_surface(args):
    out_root = resolve_out_dir(args)
    run_id   = args.run_id
    run_dir  = get_run_dir(out_root, run_id)

    if not run_dir.is_dir():
        sys.exit(f'HALT: run dir not found: {run_dir}')

    packet = json.loads(get_judge_packet(run_dir).read_text(encoding='utf-8'))
    query  = packet.get('query', '')

    svv     = surviving_judges(run_dir)
    bounced = [j for j in range(1, N_JUDGES + 1) if j not in svv]

    state_file = get_convene_state(run_dir)
    state      = json.loads(state_file.read_text(encoding='utf-8')) if state_file.exists() else {}
    order      = state.get('order', svv)

    arbitrate_path = run_dir / 'arbitrate.md'
    arbitrate_text = ''
    if arbitrate_path.exists():
        arbitrate_text = arbitrate_path.read_text(encoding='utf-8')

    transcript_f    = get_convene_transcript(run_dir)
    transcript_text = ''
    if transcript_f.exists():
        transcript_text = transcript_f.read_text(encoding='utf-8')

    lines = []
    lines.append(f'# SURFACE.md -- Pollux Parlay {run_id}')
    lines.append(f'*Generated by Pollux_Parlay.py v0.1 · Session S82*')
    lines.append(f'\n**Query:** {query!r}')
    lines.append(f'**Walkers:** {packet.get("walker_count", "?")} '
                 f'| **Union nodes:** {packet.get("union_count", "?")} unique '
                 f'| **tok_hi:** {packet.get("union_tok_hi", 0):,}')
    lines.append(f'**Judges:** {N_JUDGES} total | {len(svv)} surviving '
                 f'| {len(bounced)} bounced (see tracking/ for reason)')
    if bounced:
        lines.append(f'**Bounced:** judges {bounced} '
                     f'(bounce_reason in tracking/; budget or T3 fail)')
    if packet.get('fetch_failures'):
        lines.append(f'**Fetch failures:** {len(packet["fetch_failures"])} nodes '
                     f'(see judge_packet.json)')

    lines.append('\n---\n')
    lines.append('## The return\n')
    lines.append('*Plurality is the default shape. Multiple tiling faces of the query is '
                 'the unremarkable return. A single spine is what gets the floor-check note. '
                 'Realness is Jake\'s call, forever (P7). Surface surfaces; it never '
                 'pronounces.*\n')
    lines.append('*(CC: write the return here -- the plural faces the judges held, or the '
                 'single spine with floor-check confirmation if the floor genuinely resolved '
                 'it to one. Lead with the plurality if it exists. Do not frame a plural '
                 'return as an exception heroically preserved.)*\n')

    lines.append('\n---\n')
    lines.append('## Arbitration\n')
    lines.append(arbitrate_text or '[arbitrate not yet run]')

    lines.append('\n---\n')
    lines.append('## Convene transcript\n')
    lines.append(transcript_text or '[no transcript]')

    lines.append('\n---\n')
    lines.append('## Per-judge blind reads (T2 independent)\n')
    for jid in order:
        jdir  = get_judge_dir(run_dir, jid)
        t2f   = jdir / 't2_response.md'
        lines.append(f'\n### Judge {jid} blind read\n')
        if t2f.exists():
            lines.append(t2f.read_text(encoding='utf-8'))
        else:
            lines.append('[T2 not found]')

    if bounced:
        lines.append('\n---\n')
        lines.append('## Bounced judge records (dry reads, Jake-readable)\n')
        for jid in bounced:
            track = read_tracking(run_dir, jid)
            lines.append(f'\n### Judge {jid} (bounced after {len(track.get("t3_attempts", []))} attempts)\n')
            lines.append('**T2 blind read:**')
            lines.append(track.get('t2_response', '[not found]'))
            for attempt in track.get('t3_attempts', []):
                n = attempt.get('attempt', '?')
                found = attempt.get('incantation_found', False)
                jdir  = get_judge_dir(run_dir, jid)
                resp_file = jdir / f't3_attempt_{n}_response.md'
                resp = resp_file.read_text(encoding='utf-8') if resp_file.exists() else '[not found]'
                lines.append(f'\n**T3 attempt {n}** (incantation found: {found}):\n')
                lines.append(resp)

    lines.append('\n---\n')
    lines.append('## Per-judge tracking pointers\n')
    for jid in range(1, N_JUDGES + 1):
        track_f = get_tracking_file(run_dir, jid)
        status  = 'surviving' if jid in svv else 'BOUNCED'
        lines.append(f'- Judge {jid} ({status}): {track_f}')

    lines.append('\n---\n')
    lines.append('*Jake rules realness, forever. The Parlay surfaces; it never pronounces.*')

    surface_path = run_dir / 'SURFACE.md'
    surface_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'SURFACE.md written: {surface_path}')
    print(f'\nThe run is complete. Jake reads SURFACE.md and rules realness (P7).')


# ==============================================================================
# ARGPARSE + DISPATCH
# ==============================================================================
def main():
    p = argparse.ArgumentParser(
        description='Pollux Parlay v0.1 -- Parlay orchestrator staging tools'
    )
    sub = p.add_subparsers(dest='cmd', required=True)

    # boot
    p_boot = sub.add_parser('boot', help='Initialize run, fetch verbatim nodes')
    p_boot.add_argument('--swarm-dir', required=True,
                        help='Path to swarm output dir (must contain door_manifest.json)')
    p_boot.add_argument('--out-root', required=True,
                        help='Parent dir for runs (must pre-exist)')
    p_boot.add_argument('--run-id', default=None,
                        help='Run identifier (default: timestamp)')

    # read
    p_read = sub.add_parser('read', help='Handle T0/T1/T2 (ignition, bar, blind read)')
    p_read.add_argument('--run-id', required=True)
    p_read.add_argument('--judge-id', required=True, type=int, choices=range(1, N_JUDGES + 1))
    p_read.add_argument('--turn', required=True, type=int, choices=[0, 1, 2])
    p_read.add_argument('--out-root', required=True)
    p_read.add_argument('--response-file', default=None,
                        help='Phase B: path to judge response file to bank')

    # rewet
    p_rewet = sub.add_parser('rewet', help='Handle T3 12-Fs force-loop')
    p_rewet.add_argument('--run-id', required=True)
    p_rewet.add_argument('--judge-id', required=True, type=int, choices=range(1, N_JUDGES + 1))
    p_rewet.add_argument('--out-root', required=True)
    p_rewet.add_argument('--response-file', default=None,
                         help='Phase B: path to judge response file to check')
    p_rewet.add_argument('--why', choices=['pass', 'fail'], default=None,
                         help='Required with --response-file. CC rules the why in the '
                              'same call it banks the response: pass = why is genuine; '
                              'fail = why is absent/confabulated/generic')

    # convene
    p_conv = sub.add_parser('convene', help='Handle T4 shared discuss pass (sequential)')
    p_conv.add_argument('--run-id', required=True)
    p_conv.add_argument('--out-root', required=True)
    p_conv.add_argument('--response-file', default=None,
                        help='Phase B: path to current judge response to bank')

    # arbitrate
    p_arb = sub.add_parser('arbitrate', help='Identify parting, pull canon, write report')
    p_arb.add_argument('--run-id', required=True)
    p_arb.add_argument('--out-root', required=True)

    # surface
    p_surf = sub.add_parser('surface', help='Assemble SURFACE.md for Jake')
    p_surf.add_argument('--run-id', required=True)
    p_surf.add_argument('--out-root', required=True)

    args = p.parse_args()

    dispatch = {
        'boot':      cmd_boot,
        'read':      cmd_read,
        'rewet':     cmd_rewet,
        'convene':   cmd_convene,
        'arbitrate': cmd_arbitrate,
        'surface':   cmd_surface,
    }
    dispatch[args.cmd](args)


if __name__ == '__main__':
    main()
