# pollux_feet_swarm_v1.2.py -- Pollux FEET probe tool module
# Origin: S72 apparatus session; renamed + graduated to scripts/ S76; header corrected + write-root externalized (--out-root, fail-loud), versioned to v1.2 S77
# Canon: Pollux.md / Pollux_Movement_Two_Build_v2 / The_Probe_Swarm
#
# $0 / on-sub / ANTHROPIC_API_KEY UNLOADED -- architecture, not posture.
# The probe IS an on-sub reading instance (CC). This script provides tools.
# No walk loop. No comprehension decision. CC IS the leash.
#
# Subcommands:
#   init      --query "..." [--run-id ID]
#   read_node --run-id <id> <si>
#   neighbors --run-id <id> <si>
#   deposit   --run-id <id> <si> <true|false>
#   log_step  --run-id <id> '<json>'
#   finalize  --run-id <id> --stop-reason "..." --stop-type subject-drift|cant-hold-whole|subject-complete|no-neighbors|hop-ceiling-fallback
#
# Writes per-run output to <out-root>/<run-id>/. --out-root is REQUIRED on every subcommand and MUST already exist (fail-loud HALT if absent or not on disk). The script creates NO directories. Per-run filenames retain the _S72 suffix BY DESIGN (cited as frozen receipts in ANCHOR + Probe_Swarm §3.2 — do not rename).
# Never touches active/ or canon/

import argparse, json, math, os, re, sys, types as _types
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import io

# -- BILLING GUARD (must run before any heavy imports) -------------------------
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY is loaded -- HALT. This script is $0.')

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# -- PATHS ---------------------------------------------------------------------
SCRIPT_DIR  = Path(__file__).resolve().parent   # script's own dir; tracked copy lives in scripts/
WW          = SCRIPT_DIR.parent.parent          # wallaby-way/

B2_DIR      = WW / 'runs' / 'b2_plumbing_S53'
INDEX_PATH  = B2_DIR / 'index_v2.jsonl'
EMBS_PATH   = B2_DIR / 'chunk_embeddings.npy'
CIDS_PATH   = B2_DIR / 'chunk_ids.jsonl'
EDGES_PATH  = WW / 'runs' / 'corpus_map_S5x' / 'edges.json'
CSV_PATH    = WW / 'runs' / 'foray_discovery_S71' / 'node_size_distribution.csv'
SECRETS_ENV = WW / 'secrets' / 'floor_db.env'
# OUT_DIR is resolved per-invocation from --out-root (see resolve_out_dir).
# No module-level default, no SCRIPT_DIR fallback, no mkdir — the script
# never guesses or creates its write location (fail-loud, §5.4 posture).

def resolve_out_dir(args):
    """Resolve + validate the write-root. REQUIRED, must pre-exist. No creation."""
    root = getattr(args, 'out_root', None)
    if not root:
        sys.exit("HALT: --out-root is required (e.g. runs/pollux_feet_tests/S77). "
                 "The script will not guess where to write.")
    p = Path(root).resolve()
    if not p.is_dir():
        sys.exit(f"HALT: --out-root does not exist on disk: {p}\n"
                 "Create the session dir by hand before running (the script creates no dirs).")
    return p

def get_run_paths(run_id):
    """All per-run file paths scoped to OUT_DIR/<run-id>/."""
    d = OUT_DIR / run_id
    p = _types.SimpleNamespace()
    p.run_dir   = d
    p.cache     = d / 'walk_cache.json'
    p.state     = d / 'run_state.json'
    p.reads     = d / 'node_reads.json'
    p.prov      = d / 'provenance_S72.json'
    p.log       = d / 'walk_log_S72.jsonl'
    p.node_embs = d / 'node_embs.npy'
    p.region    = d / 'region_S72.json'
    p.toks      = d / 'toks_S72.json'
    p.report    = d / 'walk_report_S72.md'
    return p

# -- DIALS [INTENT] ------------------------------------------------------------
DAMP_WIN          = 5
TOP_K             = 10
WHALE_TOK_HI      = 150_000
REGION_TOK_HI_CAP = 800_000
SOFTMAX_TEMP      = 1.0   # [INTENT] reference only -- CC picks by comprehension

SENTINEL = '00000000-0000-4000-8000-000000000000'
K_RRF    = 60
TOP_B2   = 80

# -- UTILITY FUNCTIONS (available to all subcommands) -------------------------

def extract_title(embed_text):
    for line in embed_text.splitlines():
        if line.startswith('### NODE'):
            return line.strip()
    return embed_text[:120].replace('\n', ' ')

def tokenize_bm25(text):
    return re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())

def tag_damping(candidate_tag, recent_tags, window=5):
    """[INTENT] per-tag recency damping. Returns multiplier in [0.5, 1.0]."""
    if not recent_tags:
        return 1.0
    recent   = recent_tags[-window:]
    fraction = recent.count(candidate_tag) / len(recent)
    return 1.0 - 0.5 * fraction

def softmax_sample(sis, scores, temperature=1.0):
    """[INTENT] reference only -- CC picks by comprehension, not softmax."""
    if not sis:
        return None
    if len(sis) == 1:
        return sis[0]
    import random
    max_s  = max(scores)
    exp_sc = [math.exp((s - max_s) / max(temperature, 1e-6)) for s in scores]
    total  = sum(exp_sc)
    if total <= 0:
        return random.choice(sis)
    probs  = [e / total for e in exp_sc]
    r      = random.random()
    cumul  = 0.0
    for si, prob in zip(sis, probs):
        cumul += prob
        if r <= cumul:
            return si
    return sis[-1]

# -- content_loudness (used only at init) -------------------------------------
DECISION_WORDS = [
    'decided', 'decision', 'going with', 'final ', 'locked',
    'confirmed', 'approved', 'shipping', 'we will ', 'i will ',
    "we're going to", 'chose ', 'choosing', 'committed to',
    'going to build', 'plan is', 'the call is',
]
REVERSAL_WORDS = [
    'wait-', 'wait -', 'actually,', 'actually ', 'reversed',
    'back to ', 'changed my mind', 'step back', 'nope', 'scratch that',
    'hold on', 'rethink', 'never mind', 'was wrong', 'were wrong',
    'no, ', 'no. ', 'not that', 'take a step back', 'reframe',
    "i don't want to", 'abort', 'start over',
]

def content_loudness(embed_text):
    """[INTENT] crude loudness: decision/reversal/recurrence markers."""
    t         = embed_text.lower()
    d_score   = sum(t.count(w) for w in DECISION_WORDS) * 2.0
    r_score   = sum(t.count(w) for w in REVERSAL_WORDS) * 3.0
    cap_words = re.findall(r'\b[A-Z]{3,}\b', embed_text)
    rec_score = sum(1 for _, c in Counter(cap_words).items() if c >= 3) * 1.5
    emphasis  = (embed_text.count('!') + embed_text.count('?')) * 0.2
    return d_score + r_score + rec_score + emphasis

# -- render_block -- VERBATIM from foray_draw_S71_replB.py --------------------
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

# -- DB helpers ----------------------------------------------------------------
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

    # reach_up = 1
    ancestors = []
    parent = msg_map[anchor_msg]['parent']
    if parent and parent in msg_map:
        ancestors.append(parent)

    # reach_down = 0
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

# -- b2 retrieval helpers (verbatim pattern from broken S72) ------------------
def exact_phrase_scores(query, nodes, np):
    q_lower = query.lower()
    scores  = np.zeros(len(nodes))
    words   = q_lower.split()
    phrases = []
    for wlen in (4, 3, 2):
        for i in range(len(words) - wlen + 1):
            phrases.append(' '.join(words[i:i + wlen]))
    for word in query.split():
        if len(word) > 3 and word[0].isupper():
            phrases.append(word.lower())
    for i, nd in enumerate(nodes):
        tl = nd['embed_text'].lower()
        scores[i] = sum(tl.count(ph) * len(ph.split()) for ph in phrases)
    return scores

def node_dense_scores(query, nodes, model, chunk_embs, chunk_to_node, np):
    q_emb       = model.encode([query], normalize_embeddings=True, convert_to_numpy=True)
    chunk_sc    = (q_emb @ chunk_embs.T).flatten()
    node_scores = np.full(len(nodes), -1.0)
    for ci, ni in enumerate(chunk_to_node):
        if chunk_sc[ci] > node_scores[ni]:
            node_scores[ni] = chunk_sc[ci]
    for i, nd in enumerate(nodes):
        if nd['strata'] == 'boot-echo':
            node_scores[i] = -1.0
    return node_scores

def run_b2(query, nodes, bm25_index, model, chunk_embs, chunk_to_node, np):
    q_tokens = tokenize_bm25(query)
    bm25_sc  = bm25_index.get_scores(q_tokens)
    ep_sc    = exact_phrase_scores(query, nodes, np)
    lex_sc   = bm25_sc + ep_sc * 0.5
    dense_sc = node_dense_scores(query, nodes, model, chunk_embs, chunk_to_node, np)
    for i, nd in enumerate(nodes):
        if nd['strata'] == 'boot-echo':
            lex_sc[i] = -1e9
    bm25_ranked  = np.argsort(-lex_sc)
    dense_ranked = np.argsort(-dense_sc)
    rrf = np.zeros(len(nodes))
    for rp, ni in enumerate(bm25_ranked):
        rrf[ni] += 1.0 / (K_RRF + rp + 1)
    for rp, ni in enumerate(dense_ranked):
        rrf[ni] += 1.0 / (K_RRF + rp + 1)
    pool = {}
    for ni in np.argsort(-rrf)[:TOP_B2]:
        nd  = nodes[ni]
        lid = (nd['conv_uuid'], nd['anchor_msg'])
        if lid not in pool:
            pool[lid] = {
                'conv_uuid':     nd['conv_uuid'],
                'anchor_msg':    nd['anchor_msg'],
                'best_rrf':      float(rrf[ni]),
                'best_node_idx': int(ni),
            }
    return sorted(pool.values(), key=lambda e: -e['best_rrf'])

# ==============================================================================
# SUBCOMMAND: init
# ==============================================================================
def cmd_init(args):
    import csv as csv_mod
    import numpy as np
    from rank_bm25 import BM25Okapi
    from sentence_transformers import SentenceTransformer

    query  = args.query
    run_id = args.run_id or datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    paths  = get_run_paths(run_id)
    paths.run_dir.mkdir(parents=True, exist_ok=True)

    print(f'POLLUX FEET S72 -- init')
    print(f'Query:  {query!r}')
    print(f'Run ID: {run_id}')
    print(f'Run dir: {paths.run_dir}')

    # Artifact check
    required = [
        ('edges.json',               EDGES_PATH),
        ('index_v2.jsonl',           INDEX_PATH),
        ('chunk_embeddings.npy',     EMBS_PATH),
        ('chunk_ids.jsonl',          CIDS_PATH),
        ('floor_db.env',             SECRETS_ENV),
        ('node_size_distribution.csv', CSV_PATH),
    ]
    for name, path in required:
        if not path.exists():
            sys.exit(f'HALT: required artifact missing: {name} at {path}')
    print('Artifacts: all present')

    # edges.json shape check
    print('\nLoading graph (edges.json) ...')
    with open(EDGES_PATH, encoding='utf-8') as fh:
        graph_data = json.load(fh)
    gm = graph_data['meta']
    node_count = gm['node_count']
    edge_count = gm['edge_count']
    if node_count != 8288:
        sys.exit(f'HALT: edges.json node_count={node_count}, expected 8288')
    if edge_count != 49078:
        sys.exit(f'HALT: edges.json edge_count={edge_count}, expected 49078')
    if graph_data['edges']:
        e = graph_data['edges'][0]
        for field in ('source', 'target', 'si', 'ti', 'w'):
            if field not in e:
                sys.exit(f'HALT: edges.json missing field {field!r}')
    print(f'  Shape check PASS: {node_count}/{edge_count}/source+target+si+ti+w')

    adjacency = defaultdict(list)
    for edge in graph_data['edges']:
        si = edge['si']
        ti = edge['ti']
        w  = float(edge['w'])
        adjacency[si].append([ti, w])
        adjacency[ti].append([si, w])
    print(f'  Adjacency: {len(adjacency)} nodes with >=1 edge')

    # Load b2 index
    print('\nLoading b2 index ...')
    nodes = []
    with open(INDEX_PATH, encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if line:
                nodes.append(json.loads(line))
    print(f'  {len(nodes)} nodes loaded')

    # Load chunk embeddings
    print('Loading chunk embeddings ...')
    chunk_embs    = np.load(str(EMBS_PATH))
    chunk_to_node = []
    with open(CIDS_PATH, encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if line:
                chunk_to_node.append(json.loads(line)['node_idx'])
    chunk_to_node = np.array(chunk_to_node, dtype=np.int32)
    print(f'  {len(chunk_to_node)} chunks, matrix {chunk_embs.shape}')

    # Build BM25
    print('Building BM25 ...')
    corpus_tokens = [tokenize_bm25(nd['embed_text']) for nd in nodes]
    bm25_index    = BM25Okapi(corpus_tokens)
    print('  BM25 ready')

    # Load dense model
    print('Loading dense model (all-MiniLM-L6-v2) ...')
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print('  Model loaded')

    # b2 retrieval -> entry node + castor set
    print('\nRunning b2 retrieval ...')
    castor_pool = run_b2(query, nodes, bm25_index, model, chunk_embs, chunk_to_node, np)
    print(f'  Castor pool: {len(castor_pool)} distinct nodes')
    if not castor_pool:
        sys.exit('HALT: b2 retrieval returned zero results -- cannot determine entry node')

    entry_rank = args.entry_rank
    if entry_rank < 1 or entry_rank > len(castor_pool):
        sys.exit(f'HALT: --entry-rank {entry_rank} out of range '
                 f'(castor_pool has {len(castor_pool)} entries, 1-indexed)')
    entry_rec   = castor_pool[entry_rank - 1]
    entry_si    = entry_rec['best_node_idx']
    entry_node  = nodes[entry_si]
    skipped_sis = [castor_pool[i]['best_node_idx'] for i in range(entry_rank - 1)]
    castor_ids_list = [[r['conv_uuid'], r['anchor_msg']] for r in castor_pool]

    print(f'\n  Entry node (b2 rank-{entry_rank}):')
    print(f'    si:         {entry_si}')
    print(f'    conv_uuid:  {entry_node["conv_uuid"]}')
    print(f'    anchor_msg: {entry_node["anchor_msg"]}')
    print(f'    salience:   {entry_node["salience"]}')
    print(f'    title:      {extract_title(entry_node["embed_text"])[:120]}')
    print('\n  *** QUERY SET DOWN. Walk proceeds query-blind from here. ***')

    # Precompute loudness
    print('\nPrecomputing content loudness ...')
    precomp_loudness = {str(i): content_loudness(nd['embed_text']) for i, nd in enumerate(nodes)}
    vals = list(precomp_loudness.values())
    print(f'  min={min(vals):.1f} max={max(vals):.1f} mean={sum(vals)/len(vals):.2f}')

    # Whale fence from CSV
    print('Loading whale fence CSV ...')
    csv_tok_hi = {}
    with open(CSV_PATH, newline='', encoding='utf-8') as fh:
        for r in csv_mod.DictReader(fh):
            csv_tok_hi[(r['conv_uuid'], r['anchor_msg'])] = int(r['tok_hi'])
    print(f'  {len(csv_tok_hi)} CSV entries')

    whale_fence = {}
    for i, nd in enumerate(nodes):
        key = (nd['conv_uuid'], nd['anchor_msg'])
        if key in csv_tok_hi:
            whale_fence[str(i)] = csv_tok_hi[key] > WHALE_TOK_HI
        else:
            proxy = round(len(nd['embed_text']) * 0.72)
            whale_fence[str(i)] = proxy > WHALE_TOK_HI
    whale_count = sum(1 for v in whale_fence.values() if v)
    print(f'  Whale-fenced: {whale_count} nodes (tok_hi > {WHALE_TOK_HI:,})')

    # Build si_to_nid
    si_to_nid = {}
    for i, nd in enumerate(nodes):
        key = (nd['conv_uuid'], nd['anchor_msg'])
        tok_hi_est = csv_tok_hi.get(key, round(len(nd['embed_text']) * 0.72))
        si_to_nid[str(i)] = {
            'conv_uuid':  nd['conv_uuid'],
            'anchor_msg': nd['anchor_msg'],
            'salience':   nd['salience'],
            'title':      extract_title(nd['embed_text'])[:100],
            'tok_hi_est': tok_hi_est,
        }

    # Query embedding
    print('Computing query embedding ...')
    query_emb = model.encode([query], normalize_embeddings=True, convert_to_numpy=True)[0]

    # Node embeddings: mean of chunk embs per si, unit-normalized
    print('Precomputing node embeddings (mean chunk embs per si) ...')
    node_embs_arr = np.zeros((len(nodes), chunk_embs.shape[1]), dtype=np.float32)
    counts        = np.zeros(len(nodes), dtype=np.int32)
    for ci, ni in enumerate(chunk_to_node):
        node_embs_arr[ni] += chunk_embs[ci]
        counts[ni]         += 1
    for i in range(len(nodes)):
        if counts[i] > 0:
            node_embs_arr[i] /= counts[i]
            norm = np.linalg.norm(node_embs_arr[i])
            if norm > 0:
                node_embs_arr[i] /= norm
    np.save(str(paths.node_embs), node_embs_arr)
    print(f'  node_embs.npy: {node_embs_arr.shape}')

    # Write walk_cache.json
    print('\nWriting walk_cache.json ...')
    db_url = load_db_url()
    walk_cache = {
        'query':             query,
        'run_id':            run_id,
        'entry_si':          entry_si,
        'entry_conv_uuid':   entry_node['conv_uuid'],
        'entry_anchor_msg':  entry_node['anchor_msg'],
        'db_url':            db_url,
        'precomp_loudness':  precomp_loudness,
        'adjacency':         {str(k): v for k, v in adjacency.items()},
        'whale_fence':       whale_fence,
        'query_emb':         query_emb.tolist(),
        'si_to_nid':         si_to_nid,
        'castor_ids':        castor_ids_list,
        'dials': {
            'DAMP_WIN':          DAMP_WIN,
            'TOP_K':             TOP_K,
            'WHALE_TOK_HI':      WHALE_TOK_HI,
            'REGION_TOK_HI_CAP': REGION_TOK_HI_CAP,
            'SOFTMAX_TEMP':      SOFTMAX_TEMP,
        },
    }
    paths.cache.write_text(json.dumps(walk_cache, ensure_ascii=False), encoding='utf-8')
    print(f'  walk_cache.json: {paths.cache.stat().st_size / 1024:.0f} KB')

    # Write run_state.json
    run_state = {
        'query':                query,
        'run_id':               run_id,
        'entry_rank':           entry_rank,
        'skipped_ranks_si':     skipped_sis,
        'entry_si':             entry_si,
        'entry_nid':            [entry_node['conv_uuid'], entry_node['anchor_msg']],
        'step':                 0,
        'visited_ids':          [],
        'visited_si_list':      [],
        'visit_tags':           [],
        'whale_fenced_log':     [],
        'total_rendered_chars': 0,
    }
    paths.state.write_text(json.dumps(run_state, indent=2, ensure_ascii=False), encoding='utf-8')

    # Initialize append files
    paths.reads.write_text('{}', encoding='utf-8')
    paths.prov.write_text('[]', encoding='utf-8')
    paths.log.write_text('', encoding='utf-8')
    print('  run_state.json / node_reads.json / provenance_S72.json / walk_log_S72.jsonl: initialized')

    # WET BOOT
    print()
    print('=' * 62)
    print('WET BOOT -- READING INSTANCE')
    print('=' * 62)
    print(f'Entry si: {entry_si}  |  rank: {entry_rank}  |  {entry_node["salience"]}')
    print(f'Title:    {extract_title(entry_node["embed_text"])[:80]}')
    print()
    print("You hold a question -- not to match against, to be colored by. It is")
    print("your stance, not your target. You're going to walk this man's corpus,")
    print("reading as you go. Start where you're placed. Read the node. Then look")
    print("at what's salient nearby and step toward what catches -- loud, but don't")
    print("ride one loudness forever; let something else catch you. Read each node")
    print("you step to. As you walk, hold the through-line: what is this stretch of")
    print("the corpus, together, circling? You'll feel two edges. One: the subject")
    print("stops being the subject -- you've wandered into a different question in a")
    print("different room. Two: you can't hold it whole anymore -- one more node and")
    print("the shape slips. When you feel either edge, STOP. That edge is the leash;")
    print("it is YOURS to feel, not a counter's to enforce. At every node you dwell")
    print("in, call deposit(). When you stop, call finalize() with your stop-reason")
    print("in your own words. Deposit addresses, never a summary of what they meant.")
    print("If you reach an edge by step 2, that's a true short walk -- report it,")
    print("don't pad it.")
    print('=' * 62)
    print(f'\nDials [INTENT]: DAMP_WIN={DAMP_WIN} TOP_K={TOP_K} '
          f'WHALE_TOK_HI={WHALE_TOK_HI:,} REGION_TOK_HI_CAP={REGION_TOK_HI_CAP:,}')
    print(f'$0 confirmed. ANTHROPIC_API_KEY: NOT loaded.')
    print(f'\nBegin: python pollux_feet_S72.py read_node --run-id {run_id} {entry_si}')


# ==============================================================================
# SUBCOMMAND: read_node
# ==============================================================================
def cmd_read_node(args):
    import psycopg

    si     = args.si
    run_id = args.run_id
    paths  = get_run_paths(run_id)
    if not paths.run_dir.exists():
        sys.exit(f'HALT: run dir {paths.run_dir} not found -- run init --run-id {run_id} first')
    if not paths.cache.exists():
        sys.exit('HALT: walk_cache.json not found -- run init first')
    cache = json.loads(paths.cache.read_text(encoding='utf-8'))

    nid_info = cache['si_to_nid'].get(str(si))
    if nid_info is None:
        sys.exit(f'HALT: si={si} not found in walk_cache.si_to_nid')

    conv_uuid  = nid_info['conv_uuid']
    anchor_msg = nid_info['anchor_msg']

    print(f'read_node si={si}  {conv_uuid[:8]}.../{anchor_msg[:8]}...', file=sys.stderr)

    with psycopg.connect(cache['db_url']) as conn:
        conn.autocommit = False
        msg_uuids, rendered_text = fetch_span(conn, conv_uuid, anchor_msg, with_content=True)
        conn.rollback()

    node_chars = len(rendered_text)
    tok_hi_est = int(node_chars * 0.72)

    # Write metadata to node_reads.json (no rendered_text stored -- it goes to stdout)
    reads = json.loads(paths.reads.read_text(encoding='utf-8'))
    reads[str(si)] = {
        'si':          si,
        'conv_uuid':   conv_uuid,
        'anchor_msg':  anchor_msg,
        'msg_uuids':   msg_uuids,
        'node_chars':  node_chars,
        'tok_hi_est':  tok_hi_est,
    }
    paths.reads.write_text(json.dumps(reads, ensure_ascii=False), encoding='utf-8')

    result = {
        'si':            si,
        'conv_uuid':     conv_uuid,
        'anchor_msg':    anchor_msg,
        'msg_uuids':     msg_uuids,
        'rendered_text': rendered_text,
        'node_chars':    node_chars,
        'tok_hi_est':    tok_hi_est,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ==============================================================================
# SUBCOMMAND: neighbors
# ==============================================================================
def cmd_neighbors(args):
    si     = args.si
    run_id = args.run_id
    paths  = get_run_paths(run_id)
    if not paths.run_dir.exists():
        sys.exit(f'HALT: run dir {paths.run_dir} not found -- run init --run-id {run_id} first')
    if not paths.cache.exists():
        sys.exit('HALT: walk_cache.json not found -- run init first')
    cache = json.loads(paths.cache.read_text(encoding='utf-8'))
    state = json.loads(paths.state.read_text(encoding='utf-8'))

    adjacency   = cache['adjacency']
    loudness    = cache['precomp_loudness']
    whale_fence = cache['whale_fence']
    si_to_nid   = cache['si_to_nid']
    damp_win    = cache['dials']['DAMP_WIN']
    top_k       = cache['dials']['TOP_K']

    visited_set = {(v[0], v[1]) for v in state['visited_ids']}
    visit_tags  = state['visit_tags']

    candidates  = []
    whale_hits  = []
    seen_floor  = set()

    for (ti, w) in adjacency.get(str(si), []):
        ti_str   = str(ti)
        nid_info = si_to_nid.get(ti_str)
        if nid_info is None:
            continue
        floor_id = (nid_info['conv_uuid'], nid_info['anchor_msg'])
        if floor_id in visited_set:
            continue
        if floor_id in seen_floor:
            continue
        seen_floor.add(floor_id)
        if whale_fence.get(ti_str, False):
            whale_hits.append({
                'si':         ti,
                'conv_uuid':  nid_info['conv_uuid'],
                'anchor_msg': nid_info['anchor_msg'],
                'title':      nid_info['title'],
            })
            continue
        loud  = loudness.get(ti_str, 0.0)
        damp  = tag_damping(nid_info['salience'], visit_tags, window=damp_win)
        score = loud * damp
        candidates.append({
            'si':         ti,
            'conv_uuid':  nid_info['conv_uuid'],
            'anchor_msg': nid_info['anchor_msg'],
            'title':      nid_info['title'],
            'salience':   nid_info['salience'],
            'loudness':   round(loud, 4),
            'damp':       round(damp, 4),
            'score':      round(score, 4),
        })

    if whale_hits:
        state['whale_fenced_log'].extend([{**wh, 'step': state['step']} for wh in whale_hits])
        paths.state.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f'[whale fence] {len(whale_hits)} excluded: '
              + ', '.join(f'si={wh["si"]}' for wh in whale_hits), file=sys.stderr)

    candidates.sort(key=lambda x: -x['score'])
    print(json.dumps(candidates[:top_k], ensure_ascii=False, indent=2))


# ==============================================================================
# SUBCOMMAND: deposit
# ==============================================================================
def cmd_deposit(args):
    si      = args.si
    on_path = args.on_path.lower() == 'true'
    run_id  = args.run_id
    paths   = get_run_paths(run_id)
    if not paths.run_dir.exists():
        sys.exit(f'HALT: run dir {paths.run_dir} not found -- run init --run-id {run_id} first')
    if not paths.cache.exists():
        sys.exit('HALT: walk_cache.json not found -- run init first')
    cache = json.loads(paths.cache.read_text(encoding='utf-8'))
    state = json.loads(paths.state.read_text(encoding='utf-8'))
    reads = json.loads(paths.reads.read_text(encoding='utf-8'))

    if str(si) not in reads:
        sys.exit(f'DEPOSIT CALLED WITHOUT read_node -- walk the read-then-step order. '
                 f'si={si} not in node_reads.json')

    nid_info   = cache['si_to_nid'].get(str(si))
    if nid_info is None:
        sys.exit(f'HALT: si={si} not found in walk_cache.si_to_nid')

    read_info  = reads[str(si)]
    conv_uuid  = nid_info['conv_uuid']
    anchor_msg = nid_info['anchor_msg']

    # Idempotent guard: if floor identity already deposited, no-op
    floor_id    = (conv_uuid, anchor_msg)
    visited_set = {(v[0], v[1]) for v in state['visited_ids']}
    if floor_id in visited_set:
        print(f'DEPOSIT NO-OP: si={si} ({conv_uuid[:8]}.../{anchor_msg[:8]}...) '
              f'already deposited -- idempotent re-deposit, skipping')
        return

    msg_uuids  = read_info['msg_uuids']
    tok_hi_est = read_info['tok_hi_est']
    node_chars = read_info['node_chars']
    is_whale   = cache['whale_fence'].get(str(si), False)

    # Update run_state
    state['visited_ids'].append([conv_uuid, anchor_msg])
    state['visited_si_list'].append(si)
    state['visit_tags'].append(nid_info['salience'])
    state['step'] += 1
    state['total_rendered_chars'] += node_chars
    paths.state.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')

    # Append to provenance
    prov = json.loads(paths.prov.read_text(encoding='utf-8'))
    prov.append({
        'conv_uuid':    conv_uuid,
        'anchor_msg':   anchor_msg,
        'msg_uuids':    msg_uuids,
        'on_path':      on_path,
        'tok_hi_est':   tok_hi_est,
        'whale_fenced': is_whale,
        'step':         state['step'],
    })
    paths.prov.write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding='utf-8')

    total_tok   = int(state['total_rendered_chars'] * 0.72)
    cap         = cache['dials']['REGION_TOK_HI_CAP']
    pct_cap     = total_tok / cap * 100 if cap else 0

    print(f'deposited si={si}  step={state["step"]}  on_path={on_path}')
    print(f'  {conv_uuid[:8]}.../{anchor_msg[:8]}...  tok_hi_est={tok_hi_est:,}')
    print(f'  region gauge: {total_tok:,} / {cap:,} ({pct_cap:.0f}%)  [INTENT -- not a hard stop]')
    print(f'  provenance records: {len(prov)}')


# ==============================================================================
# SUBCOMMAND: log_step
# ==============================================================================
def cmd_log_step(args):
    import numpy as np

    step_data = json.loads(args.step_json)
    chosen_si = step_data.get('chosen_si')
    if chosen_si is None:
        sys.exit('HALT: log_step JSON must include chosen_si')

    run_id = args.run_id
    paths  = get_run_paths(run_id)
    if not paths.run_dir.exists():
        sys.exit(f'HALT: run dir {paths.run_dir} not found -- run init --run-id {run_id} first')
    if not paths.cache.exists():
        sys.exit('HALT: walk_cache.json not found -- run init first')
    cache     = json.loads(paths.cache.read_text(encoding='utf-8'))
    query_emb = np.array(cache['query_emb'], dtype=np.float32)

    cosine_secondary = None
    if paths.node_embs.exists():
        node_embs = np.load(str(paths.node_embs))
        if 0 <= chosen_si < len(node_embs):
            node_e = node_embs[chosen_si]
            norm   = np.linalg.norm(node_e)
            if norm > 0:
                cosine_secondary = float(np.dot(node_e / norm, query_emb))

    entry = {**step_data, 'cosine_secondary': cosine_secondary}
    with open(paths.log, 'a', encoding='utf-8') as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + '\n')

    cs_str = f'{cosine_secondary:.4f}' if cosine_secondary is not None else 'N/A'
    print(f'log_step step={step_data.get("step")}  chosen_si={chosen_si}  '
          f'cosine_secondary={cs_str}  [secondary instrument -- never gates]')


# ==============================================================================
# SUBCOMMAND: finalize
# ==============================================================================
def cmd_finalize(args):
    import psycopg

    stop_reason = args.stop_reason
    stop_type   = args.stop_type
    run_id      = args.run_id
    paths       = get_run_paths(run_id)
    if not paths.run_dir.exists():
        sys.exit(f'HALT: run dir {paths.run_dir} not found -- run init --run-id {run_id} first')
    if not paths.cache.exists():
        sys.exit('HALT: walk_cache.json not found -- run init first')
    cache       = json.loads(paths.cache.read_text(encoding='utf-8'))
    state       = json.loads(paths.state.read_text(encoding='utf-8'))
    prov        = json.loads(paths.prov.read_text(encoding='utf-8'))
    adjacency   = cache['adjacency']
    si_to_nid   = cache['si_to_nid']
    whale_fence = cache['whale_fence']
    castor_set  = {(c[0], c[1]) for c in cache['castor_ids']}
    db_url      = cache['db_url']

    walk_log = []
    if paths.log.exists():
        for line in paths.log.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line:
                walk_log.append(json.loads(line))

    # Build floor_id reverse lookups (O(N) once)
    floor_to_tok_hi = {}
    floor_to_whale  = {}
    for si_str, info in si_to_nid.items():
        fid = (info['conv_uuid'], info['anchor_msg'])
        floor_to_tok_hi[fid] = info['tok_hi_est']
        floor_to_whale[fid]  = whale_fence.get(si_str, False)

    # Expand 1-hop off-path
    print('Expanding 1-hop off-path ...')
    visited_ids_set = {(v[0], v[1]) for v in state['visited_ids']}
    prov_ids_set    = {(p['conv_uuid'], p['anchor_msg']) for p in prov}
    hop1_ids        = set()

    for si in state['visited_si_list']:
        for (ti, _w) in adjacency.get(str(si), []):
            nid_info = si_to_nid.get(str(ti))
            if nid_info is None:
                continue
            fid = (nid_info['conv_uuid'], nid_info['anchor_msg'])
            if fid not in visited_ids_set:
                hop1_ids.add(fid)

    new_hop1 = hop1_ids - prov_ids_set
    print(f'  New hop1 nodes to fetch msg_uuids for: {len(new_hop1)}')

    if new_hop1:
        with psycopg.connect(db_url) as conn:
            conn.autocommit = False
            for (conv_uuid, anchor_msg) in sorted(new_hop1):
                try:
                    msg_uuids, _ = fetch_span(conn, conv_uuid, anchor_msg, with_content=False)
                except Exception as e:
                    conn.rollback()
                    print(f'  [skip hop1] conv_uuid={conv_uuid!r} anchor={anchor_msg!r}: {e}')
                    continue
                tok_hi_est   = floor_to_tok_hi.get((conv_uuid, anchor_msg), 0)
                is_whale     = floor_to_whale.get((conv_uuid, anchor_msg), False)
                prov.append({
                    'conv_uuid':    conv_uuid,
                    'anchor_msg':   anchor_msg,
                    'msg_uuids':    msg_uuids,
                    'on_path':      False,
                    'tok_hi_est':   tok_hi_est,
                    'whale_fenced': is_whale,
                    'step':         None,
                })
            conn.rollback()

    # Castor-drop
    castor_dropped = [p for p in prov if (p['conv_uuid'], p['anchor_msg']) in castor_set]
    final_prov     = [p for p in prov if (p['conv_uuid'], p['anchor_msg']) not in castor_set]
    print(f'  Castor-dropped: {len(castor_dropped)}')
    print(f'  Final provenance: {len(final_prov)} distinct nodes')

    # Write final provenance
    paths.prov.write_text(json.dumps(final_prov, indent=2, ensure_ascii=False), encoding='utf-8')

    path_nodes            = [p for p in final_prov if p['on_path']]
    hop1_nodes            = [p for p in final_prov if not p['on_path']]
    path_tok_hi_est       = sum(p['tok_hi_est'] for p in final_prov if p['on_path'])
    skirt_tok_hi_est      = sum(p['tok_hi_est'] for p in final_prov if not p['on_path'])
    total_path_plus_skirt_tok_hi_est = path_tok_hi_est + skirt_tok_hi_est
    whale_count           = sum(1 for p in final_prov if p['whale_fenced'])

    # toks_S72.json
    toks_data = [{'conv_uuid': p['conv_uuid'], 'anchor_msg': p['anchor_msg'],
                  'tok_hi_est': p['tok_hi_est'], 'on_path': p['on_path']}
                 for p in final_prov]
    paths.toks.write_text(
        json.dumps(toks_data, indent=2, ensure_ascii=False), encoding='utf-8')

    # region_S72.json
    entry_si   = cache['entry_si']
    entry_info = si_to_nid.get(str(entry_si), {})
    region_out = {
        'query':                cache['query'],
        'run_id':               cache['run_id'],
        'entry': {
            'si':         entry_si,
            'conv_uuid':  cache['entry_conv_uuid'],
            'anchor_msg': cache['entry_anchor_msg'],
            'title':      entry_info.get('title', ''),
            'salience':   entry_info.get('salience', ''),
            'entry_rank':           state['entry_rank'],
            'skipped_ranks_si':     state['skipped_ranks_si'],
            'entry_castor_dropped': True,
        },
        'stop_reason':              stop_reason,
        'stop_type':                stop_type,
        'steps_taken':              state['step'],
        'path_count':               len(path_nodes),
        'hop1_count':               len(hop1_nodes),
        'castor_dropped_count':     len(castor_dropped),
        'distinct_count':           len(final_prov),
        'path_tok_hi_est':              path_tok_hi_est,
        'skirt_tok_hi_est':             skirt_tok_hi_est,
        'total_path_plus_skirt_tok_hi_est': total_path_plus_skirt_tok_hi_est,  # NOT a comprehension gauge -- path+skirt, do not compare to the leash
        'total_rendered_chars':         state['total_rendered_chars'],  # the honest on-path gauge
        'whale_fenced_count':       whale_count,
        'whale_fenced_log':         state['whale_fenced_log'],
        'dial_settings':            cache['dials'],
        'path_nodes':               path_nodes,
        'hop1_nodes':               hop1_nodes,
        'castor_dropped':           castor_dropped,
    }
    paths.region.write_text(
        json.dumps(region_out, indent=2, ensure_ascii=False), encoding='utf-8')

    # Cosine trace (last 5 steps)
    cosine_trace = [
        {'step': e.get('step'), 'cosine_secondary': e.get('cosine_secondary')}
        for e in walk_log[-5:]
    ]
    cosine_trace_md = '\n'.join(
        f'  - step {t["step"]}: {t["cosine_secondary"]:.4f}'
        if t['cosine_secondary'] is not None
        else f'  - step {t["step"]}: N/A'
        for t in cosine_trace
    ) or '  (no steps logged)'

    # Regression flag
    is_regression = stop_type in ('no-neighbors', 'hop-ceiling-fallback')
    regression_block = ''
    if is_regression:
        regression_block = (
            '\n\n## !!! REGRESSION FLAG !!!\n\n'
            f'stop_type is `{stop_type}` -- comprehension leash NEVER FIRED.\n'
            'Walk may have been read-free (mechanical stop, not felt edge).\n'
            'Do NOT treat this walk as a valid probe result.\n'
        )

    # walk_report_S72.md
    with open(paths.report, 'w', encoding='utf-8') as fh:
        fh.write('# walk_report_S72.md -- Pollux FEET Single-Probe Walk\n\n')
        fh.write(f'run_id: `{cache["run_id"]}`\n\n')
        fh.write('---\n\n')
        fh.write('## Entry node\n\n')
        fh.write(f'- si: `{entry_si}`\n')
        fh.write(f'- conv_uuid: `{cache["entry_conv_uuid"]}`\n')
        fh.write(f'- anchor_msg: `{cache["entry_anchor_msg"]}`\n')
        fh.write(f'- salience: `{entry_info.get("salience", "")}`\n')
        fh.write(f'- title: {entry_info.get("title", "(no title)")}\n\n')
        fh.write('## Walk summary\n\n')
        fh.write(f'- Hop count: **{state["step"]}**\n')
        fh.write(f'- Stop reason (reader\'s own words): **{stop_reason}**\n')
        fh.write(f'- Stop type: `{stop_type}`\n')
        fh.write(f'- Path nodes: {len(path_nodes)}\n')
        fh.write(f'- 1-hop off-path: {len(hop1_nodes)}\n')
        fh.write(f'- Castor-dropped: {len(castor_dropped)}\n')
        fh.write(f'- Final region: {len(final_prov)} distinct nodes\n')
        fh.write(f'- Path tok_hi_est (on-path nodes): {path_tok_hi_est:,}\n')
        fh.write(f'- Skirt tok_hi_est (1-hop off-path): {skirt_tok_hi_est:,}\n')
        fh.write(f'- Total path+skirt tok_hi_est: {total_path_plus_skirt_tok_hi_est:,} (NOT a leash gauge)\n')
        fh.write(f'- Total rendered chars read (path): {state["total_rendered_chars"]:,}\n')
        fh.write(f'- Whale fences fired: {len(state["whale_fenced_log"])}\n\n')
        fh.write('## Walk path\n\n')
        for p in path_nodes:
            fh.write(f'- step {p["step"]}: [{p.get("salience", "--")}] '
                     f'{p["conv_uuid"][:8]}.../{p["anchor_msg"][:8]}...  '
                     f'tok_hi_est={p["tok_hi_est"]:,}\n')
        fh.write('\n')
        fh.write('## node_chars vs node_chars_shown per step\n\n')
        for entry in walk_log:
            nc  = entry.get('node_chars', 'N/A')
            ncs = entry.get('node_chars_shown', 'N/A')
            fh.write(f'- step {entry.get("step")}: node_chars={nc}  node_chars_shown={ncs}\n')
        fh.write('\n')
        fh.write('## Cosine secondary (last 5 steps) -- secondary instrument, NOT leash\n\n')
        fh.write(cosine_trace_md + '\n\n')
        fh.write('## Whale fences fired\n\n')
        if state['whale_fenced_log']:
            for wf in state['whale_fenced_log']:
                fh.write(f'- step {wf.get("step", "?")}: si={wf["si"]}  '
                         f'{wf["conv_uuid"][:8]}.../{wf["anchor_msg"][:8]}...\n')
        else:
            fh.write('None.\n')
        fh.write('\n')
        fh.write('## Dial settings [INTENT]\n\n')
        for k, v in cache['dials'].items():
            fh.write(f'- {k}: {v}\n')
        fh.write('\n$0 confirmed. ANTHROPIC_API_KEY: NOT loaded.\n')
        fh.write('\n**NO SYNTHESIS.** What the region means is read later, by other eyes.\n')
        fh.write(regression_block)

    print(f'\nFinalize complete:')
    print(f'  region_S72.json:      {len(final_prov)} nodes')
    print(f'  toks_S72.json:        {len(toks_data)} records')
    print(f'  provenance_S72.json:  {len(final_prov)} records')
    print(f'  walk_report_S72.md:   written')
    print(f'  Run dir: {paths.run_dir}')
    if is_regression:
        print(f'\n!!! REGRESSION: stop_type={stop_type} -- comprehension leash never fired !!!')


# ==============================================================================
# CLI SETUP AND DISPATCH
# ==============================================================================
ap  = argparse.ArgumentParser(description='Pollux FEET S72 -- tool module for on-sub reading instance')
sub = ap.add_subparsers(dest='cmd')

init_p = sub.add_parser('init', help='Initialize walk: b2 retrieval, precompute cache, print WET BOOT')
init_p.add_argument('--query',      required=True, help='Question held as stance (not retrieval target)')
init_p.add_argument('--run-id',     default=None,  help='Run ID / output subdir (default: timestamp)')
init_p.add_argument('--entry-rank', type=int, default=1,
                    help='b2 rank to use as entry node (1-indexed, default 1 = rank-1)')
init_p.add_argument('--out-root', required=True,
    help='Write-root for this run; must already exist (e.g. runs/pollux_feet_tests/S77). Script creates no dirs.')

rn_p = sub.add_parser('read_node', help='Read floor text for a node; writes to node_reads.json')
rn_p.add_argument('--run-id', required=True, help='Run ID (from init)')
rn_p.add_argument('--out-root', required=True,
    help='Write-root for this run; must already exist (e.g. runs/pollux_feet_tests/S77). Script creates no dirs.')
rn_p.add_argument('si', type=int, help='Node si index')

nb_p = sub.add_parser('neighbors', help='Scored unvisited neighbors (query-blind, whale-fenced excluded)')
nb_p.add_argument('--run-id', required=True, help='Run ID (from init)')
nb_p.add_argument('--out-root', required=True,
    help='Write-root for this run; must already exist (e.g. runs/pollux_feet_tests/S77). Script creates no dirs.')
nb_p.add_argument('si', type=int, help='Current node si index')

dep_p = sub.add_parser('deposit', help='Append node address to provenance; updates run_state')
dep_p.add_argument('--run-id', required=True, help='Run ID (from init)')
dep_p.add_argument('--out-root', required=True,
    help='Write-root for this run; must already exist (e.g. runs/pollux_feet_tests/S77). Script creates no dirs.')
dep_p.add_argument('si', type=int, help='Node si index (must have been read_node\'d first)')
dep_p.add_argument('on_path', choices=['true', 'false'], help='Whether node is on the walk path')

ls_p = sub.add_parser('log_step', help='Append step to walk_log; computes cosine_secondary')
ls_p.add_argument('--run-id', required=True, help='Run ID (from init)')
ls_p.add_argument('--out-root', required=True,
    help='Write-root for this run; must already exist (e.g. runs/pollux_feet_tests/S77). Script creates no dirs.')
ls_p.add_argument('step_json', help='JSON string: {step, from_si, chosen_si, salience_reason, '
                                    'dampening_state, node_chars, node_chars_shown}')

fin_p = sub.add_parser('finalize', help='Expand 1-hop, Castor-drop, write all output files')
fin_p.add_argument('--run-id',      required=True, help='Run ID (from init)')
fin_p.add_argument('--out-root',    required=True,
    help='Write-root for this run; must already exist (e.g. runs/pollux_feet_tests/S77). Script creates no dirs.')
fin_p.add_argument('--stop-reason', required=True, help="Reader's own words for why they stopped")
fin_p.add_argument('--stop-type',   required=True,
                   choices=['subject-drift', 'cant-hold-whole', 'subject-complete', 'no-neighbors', 'hop-ceiling-fallback'],
                   help='Categorical stop type (subject-drift, cant-hold-whole, subject-complete = clean stop; no-neighbors, hop-ceiling-fallback = regression)')

parsed = ap.parse_args()
if not parsed.cmd:
    ap.print_help()
    sys.exit(1)

OUT_DIR = resolve_out_dir(parsed)

dispatch = {
    'init':       cmd_init,
    'read_node':  cmd_read_node,
    'neighbors':  cmd_neighbors,
    'deposit':    cmd_deposit,
    'log_step':   cmd_log_step,
    'finalize':   cmd_finalize,
}
dispatch[parsed.cmd](parsed)
