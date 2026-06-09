# pipeline_guards.py  v0.2  S38
# Four load-bearing guards for the apparatus chunked-pipeline loop.
# Pure functions + a registry helper — NO Agent calls, NO API calls, NO .env load.
# Guard 1 (S38): billing — assert ANTHROPIC_API_KEY not in os.environ (§7b)
# Guard 2 (S38): whale gate — KNOWN_WHALE / FITS / raise on over-ceiling
# Guard 3 (S38): salience tally — flag-1 fix, anchors on **Salience:** prefix
# Guard 4 (S38): persist — verify-on-write (flag-3 fix) + Option-B parent sidecar
# v0.2: persist_node_file — temp-then-rename; no partial artifact survives a HALT

import json
import os
import pathlib
import re


def assert_env_unloaded():
    """Guard 1 (§7b): raise if ANTHROPIC_API_KEY is present in the process environment."""
    if "ANTHROPIC_API_KEY" in os.environ:
        raise RuntimeError(
            "BILLING GUARD: ANTHROPIC_API_KEY is loaded — on-sub reads MUST NOT load it. HALT."
        )


def load_whale_registry(path):
    """Parse whale_registry.md markdown table → frozenset of uuid strings.
    Called by the loop at startup; NOT called inside whale_gate itself."""
    uuids = set()
    for line in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        if (line.startswith("|")
                and not line.startswith("| uuid")
                and not line.startswith("|---")):
            col = line.split("|")[1].strip()
            if col and "-" in col:
                uuids.add(col)
    return frozenset(uuids)


def whale_gate(conv_uuid, input_tokens, registry_uuids, ceiling=1_000_000):
    """Guard 2: route known whales; halt on new whale over ceiling."""
    if conv_uuid in registry_uuids:
        return "KNOWN_WHALE"
    if input_tokens >= ceiling:
        raise RuntimeError(
            f"NEW WHALE DETECTED: {conv_uuid} at {input_tokens} tokens — "
            "handle manually, do NOT auto-strip. HALT."
        )
    return "FITS"


def tally_nodes(node_file_text):
    """Guard 3 (flag-1 fix): count salience tags anchored on **Salience:** prefix.
    A bare word-grep would inflate off **Keywords:** lines — this does not."""
    tags = re.findall(r'^\*\*Salience:\*\*\s+(\w+)', node_file_text, re.MULTILINE)
    counts = {"MOTION": 0, "FENCE": 0, "TEXTURE": 0}
    for t in tags:
        key = t.upper()
        if key in counts:
            counts[key] += 1
    counts["total"] = sum(counts.values())
    return counts


def persist_node_file(dest_path, node_text, parents_map):
    """Guard 4 (flag-3 fix): write + verify-on-write + Option-B parent sidecar.

    parents_map: {msg_uuid: parent_uuid_or_"null"} — the .parents.json sidecar
    produced by extract_whale.py v2.0. Every anchor_msg found in the node file
    must be a key in this map; absence raises (fabrication / window-mismatch guard).

    Sidecar written to <dest_path>.parents.json:
      { "node_file": "<basename>", "edges": { "<anchor>": "<parent_uuid>"|null } }
    Root anchors (parents_map value == "null") are recorded as JSON null, NOT omitted.
    """
    dest = pathlib.Path(dest_path)
    tmp = dest.parent / (dest.name + ".tmp")

    # write to temp first — no artifact lands at dest_path until all checks pass
    tmp.write_text(node_text, encoding="utf-8")

    try:
        # verify-on-write (flag-3): re-read and assert non-stub
        written = tmp.read_text(encoding="utf-8")
        if not (tmp.stat().st_size > 0
                and "--- DONE:" in written
                and tally_nodes(written)["total"] > 0):
            raise RuntimeError(f"STUB DETECTED at {dest_path} — HALT.")

        # extract anchor_msg values
        anchors = re.findall(r'anchor_msg\s*:\s*"([^"]+)"', written)

        # integrity: every anchor must exist in parents_map (catches hallucinated anchors
        # and conv_uuid/window mismatches before they can poison the pile)
        for anchor in anchors:
            if anchor not in parents_map:
                raise RuntimeError(
                    f"ANCHOR NOT IN PARENTS MAP: {anchor} at {dest_path} — "
                    "the reader emitted an anchor the extractor never saw. HALT."
                )
    except RuntimeError:
        tmp.unlink(missing_ok=True)
        raise

    # all checks passed — atomic rename; replaces any pre-existing file cleanly
    os.replace(tmp, dest)

    # build edges dict — root anchors ("null" string) → JSON null (NOT omitted,
    # so dedup can distinguish "root" from "anchor missing from sidecar = bug")
    edges = {}
    for anchor in anchors:
        val = parents_map[anchor]
        edges[anchor] = None if val == "null" else val

    root_count = sum(1 for v in edges.values() if v is None)

    # write Option-B sidecar ONLY after the successful rename
    sidecar_path = pathlib.Path(str(dest) + ".parents.json")
    sidecar_path.write_text(
        json.dumps(
            {"node_file": dest.name, "edges": edges},
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"NodeSidecar: {sidecar_path}  ({len(edges)} edges, {root_count} roots)")
