# wallaby-way/scripts/persist_guard.py  v1.1  CCC S2 (Chamfer)
# v1.1 (CCC S2 'Chamfer'): path-fixes for repo reorg — wallaby-way/ restructure.
# Guard 3 + Guard 4 wrapper for the on-sub loop.
# Reads raw node catalog text + .parents.json sidecar; tallies nodes (Guard 3);
# persists to harvested_nodes/ with temp-then-rename + verify-on-write + anchor integrity
# + edge sidecar (Guard 4). Prints JSON result.
# Reuses tally_nodes() and persist_node_file() from pipeline/pipeline_guards.py verbatim.
#
# CLI:
#   python pipeline/s39/persist_guard.py \
#     --node-text pipeline/s39/<uuid>_nodes_raw.txt \
#     --parents-json pipeline/s39/<uuid>_payload.txt.parents.json \
#     --conv-uuid <uuid> \
#     --out harvested_nodes/<uuid>.md
import json, os, sys, argparse
from pathlib import Path

# Guard 1
if 'ANTHROPIC_API_KEY' in os.environ:
    sys.exit('BILLING GUARD: ANTHROPIC_API_KEY is loaded — HALT')

# Resolve pipeline/ on sys.path so we can import pipeline_guards
_HERE = Path(__file__).resolve().parent        # pipeline/s39/
_PIPELINE = _HERE.parent                        # pipeline/
sys.path.insert(0, str(_HERE))
from pipeline_guards import assert_env_unloaded, tally_nodes, persist_node_file

assert_env_unloaded()

ap = argparse.ArgumentParser()
ap.add_argument('--node-text',    required=True, dest='node_text')
ap.add_argument('--parents-json', required=True, dest='parents_json')
ap.add_argument('--conv-uuid',    required=True, dest='conv_uuid')
ap.add_argument('--out',          required=True, dest='out')
args = ap.parse_args()

# Read inputs
node_text = Path(args.node_text).read_text(encoding='utf-8')
sidecar   = json.loads(Path(args.parents_json).read_text(encoding='utf-8'))
parents_map = sidecar.get('parents', {})

# Guard 3: tally_nodes — HALT if zero nodes
counts = tally_nodes(node_text)
if counts['total'] == 0:
    print(f'Guard 3 HALT: zero nodes found in {args.node_text}', file=sys.stderr)
    sys.exit(1)

# Guard 4: persist_node_file — temp-then-rename + verify + anchor integrity + edge sidecar
dest = Path(args.out)
dest.parent.mkdir(parents=True, exist_ok=True)
persist_node_file(dest, node_text, parents_map)

result = {
    'node_count': counts['total'],
    'motion':     counts['MOTION'],
    'fence':      counts['FENCE'],
    'texture':    counts['TEXTURE'],
    'persisted_path': str(dest),
}
print(json.dumps(result))
