# test_guards_S38.py  v0.2  S38
# Unit tests for pipeline_guards.py — four guards against synthetic fixtures.
# Run: python pipeline/test_guards_S38.py

import json
import os
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pipeline_guards import assert_env_unloaded, whale_gate, tally_nodes, persist_node_file

PASS = 0
FAIL = 0


def ok(label):
    global PASS
    PASS += 1
    print(f"  PASS  {label}")


def fail(label, exc):
    global FAIL
    FAIL += 1
    print(f"  FAIL  {label}: {exc}")


# ── Guard 1: billing guard ────────────────────────────────────────────────
print("\n[Guard 1: billing guard]")

os.environ["ANTHROPIC_API_KEY"] = "sk-fake"
try:
    try:
        assert_env_unloaded()
        fail("raises when key present", "no exception raised")
    except RuntimeError as e:
        assert "BILLING GUARD" in str(e)
        ok("raises RuntimeError when ANTHROPIC_API_KEY is set")
finally:
    del os.environ["ANTHROPIC_API_KEY"]

try:
    assert_env_unloaded()
    ok("passes when ANTHROPIC_API_KEY is unset")
except Exception as e:
    fail("passes when key absent", e)


# ── Guard 2: whale gate ───────────────────────────────────────────────────
print("\n[Guard 2: whale gate]")

KNOWN = frozenset(["aaaa-known"])

try:
    result = whale_gate("aaaa-known", 5_000_000, KNOWN)
    assert result == "KNOWN_WHALE", f"got {result!r}"
    ok("returns KNOWN_WHALE for registered uuid")
except Exception as e:
    fail("KNOWN_WHALE", e)

try:
    result = whale_gate("bbbb-new", 500_000, KNOWN)
    assert result == "FITS", f"got {result!r}"
    ok("returns FITS for unknown uuid under ceiling")
except Exception as e:
    fail("FITS", e)

try:
    whale_gate("cccc-whale", 1_000_000, KNOWN)
    fail("raises on tokens >= ceiling", "no exception raised")
except RuntimeError as e:
    assert "NEW WHALE DETECTED" in str(e)
    ok("raises RuntimeError on tokens >= ceiling")
except Exception as e:
    fail("raises on tokens >= ceiling", e)


# ── Guard 3: tally_nodes ──────────────────────────────────────────────────
print("\n[Guard 3: tally_nodes]")

SYNTHETIC_NODES = """\
### NODE 1
**Salience:** MOTION
**Keywords:** planning fence motion texture boundary
**Summary:** something

---

### NODE 2
**Salience:** FENCE
**Keywords:** fence boundary another fence word here
**Summary:** something else

---

### NODE 3
**Salience:** TEXTURE
**Keywords:** detail color fence also here
**Summary:** detail node
"""

try:
    result = tally_nodes(SYNTHETIC_NODES)
    assert result == {"MOTION": 1, "FENCE": 1, "TEXTURE": 1, "total": 3}, f"got {result}"
    ok("3-node tally correct (MOTION=1, FENCE=1, TEXTURE=1, total=3)")
except Exception as e:
    fail("3-node tally", e)

try:
    result = tally_nodes(SYNTHETIC_NODES)
    assert result["FENCE"] == 1, f"FENCE={result['FENCE']}, expected 1 (Keywords lines must not inflate)"
    ok("**Keywords:** lines containing 'fence' do NOT inflate FENCE count")
except Exception as e:
    fail("fence inflation check", e)


# ── Guard 4: persist ──────────────────────────────────────────────────────
print("\n[Guard 4: persist]")

ANCHOR_UUID = "019e1720-0000-0000-0000-000000000001"
PARENT_UUID = "019e1720-0000-0000-0000-000000000000"

STUB_TEXT = (
    "### NODE 1\n"
    "**Salience:** MOTION\n"
    "```\n"
    "span = {\n"
    '  snapshot_id : "test-snap",\n'
    '  conv_uuid   : "aaaa-0000",\n'
    f'  anchor_msg  : "{ANCHOR_UUID}",\n'
    "  reach       : { up: 0, down: 1 }\n"
    "}\n"
    "```\n"
    "**Summary:** a node with no DONE line (stub)\n"
)

VALID_NODE_TEXT = (
    "### NODE 1\n"
    "**Salience:** MOTION\n"
    "```\n"
    "span = {\n"
    '  snapshot_id : "test-snap",\n'
    '  conv_uuid   : "aaaa-0000",\n'
    f'  anchor_msg  : "{ANCHOR_UUID}",\n'
    "  reach       : { up: 0, down: 1 }\n"
    "}\n"
    "```\n"
    "**Summary:** valid node\n"
    "\n"
    "--- DONE: 1 nodes (1 MOTION, 0 FENCE, 0 TEXTURE), 0 drops ---\n"
)

with tempfile.TemporaryDirectory() as tmpdir:
    tmp = pathlib.Path(tmpdir)

    # 4a: stub (no DONE line) → raises RuntimeError, no file survives at dest_path
    try:
        persist_node_file(tmp / "stub_test.md", STUB_TEXT, {ANCHOR_UUID: "null"})
        fail("stub raises RuntimeError", "no exception raised")
    except RuntimeError as e:
        assert "STUB DETECTED" in str(e), f"unexpected message: {e}"
        assert not (pathlib.Path(tmpdir) / "stub_test.md").exists(), "stub_test.md survived a failed persist — temp not cleaned up"
        ok("stub (no DONE line) raises RuntimeError, no file at dest_path")
    except Exception as e:
        fail("stub raises RuntimeError", e)

    # 4b: anchor NOT in parents_map → raises RuntimeError, no file survives at dest_path
    try:
        persist_node_file(tmp / "missing_anchor.md", VALID_NODE_TEXT, {})
        fail("missing anchor raises RuntimeError", "no exception raised")
    except RuntimeError as e:
        assert "ANCHOR NOT IN PARENTS MAP" in str(e), f"unexpected message: {e}"
        assert not (pathlib.Path(tmpdir) / "missing_anchor.md").exists(), "missing_anchor.md survived a failed persist — temp not cleaned up"
        ok("anchor absent from parents_map raises RuntimeError, no file at dest_path")
    except Exception as e:
        fail("missing anchor raises RuntimeError", e)

    # 4c: valid node, anchor is a root (parents_map value "null") → JSON null in sidecar
    try:
        out_path = tmp / "valid_root.md"
        persist_node_file(out_path, VALID_NODE_TEXT, {ANCHOR_UUID: "null"})
        sidecar = pathlib.Path(str(out_path) + ".parents.json")
        assert sidecar.exists(), "sidecar not written"
        data = json.loads(sidecar.read_text(encoding="utf-8"))
        assert data["node_file"] == "valid_root.md", f"node_file={data['node_file']!r}"
        assert data["edges"][ANCHOR_UUID] is None, f"expected null, got {data['edges'][ANCHOR_UUID]!r}"
        ok("valid root-anchor: sidecar written with JSON null edge")
    except Exception as e:
        fail("valid root-anchor node", e)

    # 4d: valid node, anchor has a real parent → parent uuid in sidecar
    try:
        out_path = tmp / "valid_child.md"
        persist_node_file(out_path, VALID_NODE_TEXT, {ANCHOR_UUID: PARENT_UUID})
        sidecar = pathlib.Path(str(out_path) + ".parents.json")
        data = json.loads(sidecar.read_text(encoding="utf-8"))
        assert data["edges"][ANCHOR_UUID] == PARENT_UUID, \
            f"expected {PARENT_UUID!r}, got {data['edges'][ANCHOR_UUID]!r}"
        ok("valid child-anchor: sidecar records real parent uuid")
    except Exception as e:
        fail("valid child-anchor node", e)


# ── Summary ───────────────────────────────────────────────────────────────
print(f"\n{'=' * 50}")
print(f"Results: {PASS} PASS / {FAIL} FAIL")
if FAIL:
    sys.exit(1)
