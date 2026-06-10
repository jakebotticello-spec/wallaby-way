# chunk_whale.py  v1.1  S33/patched-S52
# change S52: seam manifest filename derived from conv_uuid (was hardcoded d9d05961);
#             --self-test added ($0, dummy input, verifies derived naming).
# Tree-aware chunker for whale conversations that exceed the 1M-token reader ceiling.
# Splits a conversation into ceiling-fitting ===MSG=== payload files using the SAME
# render_block as extract_whale.py — copied VERBATIM, do NOT alter.
# Usage:
#   python pipeline/chunk_whale.py --in <whale.json> --out-prefix <prefix> [--max-tokens 700000]
#   python pipeline/chunk_whale.py --self-test

import json, argparse, pathlib, sys

SENTINEL = "00000000-0000-4000-8000-000000000000"
DEFAULT_MAX_TOKENS   = 700_000
DEFAULT_BYTES_PER_TOKEN = 3.0  # override via --bytes-per-token


# ─────────────────────────────────────────────────────────────────────────────
# render_block — VERBATIM from extract_whale.py (proven on 3 whales).
# Do NOT modify this function without OC sign-off; a change desyncs chunk nodes
# from the other 3 whales' format.
# ─────────────────────────────────────────────────────────────────────────────
def render_block(b):
    btype = b.get("type", "")
    if btype == "text":
        return b.get("text", "") or ""
    if btype == "thinking":
        t = b.get("thinking") or b.get("text", "") or ""
        return f"[THINKING]\n{t}"
    if btype == "tool_use":
        name = b.get("name", "")
        inp  = json.dumps(b.get("input", {}), indent=2, default=str)
        return f"[TOOL_USE: {name}]\n{inp}"
    if btype == "tool_result":
        name    = b.get("name", "") or ""
        content = b.get("content", "")
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    parts.append(item.get("text", "") or "")
            text = "\n".join(parts)
        else:
            text = str(content)
        header = f"[TOOL_RESULT: {name}]" if name else "[TOOL_RESULT]"
        return f"{header}\n{text}"
    return f"[{btype.upper()}]\n{json.dumps(b, default=str)}"
# ─────────────────────────────────────────────────────────────────────────────


def render_msg_lines(msg):
    """Return the lines list for one message — matches extract_whale.py exactly."""
    uuid       = msg.get("msg_uuid", "")
    parent     = msg.get("parent_message_uuid", "")
    role       = msg.get("sender", "")
    is_root    = msg.get("is_root", False)
    parent_out = "null" if (is_root or parent == SENTINEL) else parent

    blocks = msg.get("content_blocks") or []
    parts  = []
    if isinstance(blocks, list):
        for b in blocks:
            if isinstance(b, dict):
                rendered = render_block(b)
                if rendered:
                    parts.append(rendered)
    if not parts:
        txt = msg.get("text", "") or ""
        if txt:
            parts.append(txt)

    content = "\n".join(parts)
    return [
        "===MSG===",
        f"uuid: {uuid}",
        f"parent: {parent_out}",
        f"role: {role}",
        "---",
        content,
        "===END===",
        "",
    ]


def write_chunk_file(chunk_idx, chunk_msgs, conv_uuid, snap, created, out_prefix):
    """Serialize one chunk's messages to a ===MSG=== payload file."""
    lines = [
        f"CONVERSATION: {conv_uuid}",
        f"SNAPSHOT_ID: {snap}",
        f"CREATED: {created}",
        f"MESSAGES: {len(chunk_msgs)}",
        "",
    ]
    for msg in chunk_msgs:
        lines.extend(render_msg_lines(msg))

    text     = "\n".join(lines)
    out_path = pathlib.Path(f"{out_prefix}_{chunk_idx:02d}.txt")
    out_path.write_text(text, encoding="utf-8")
    return out_path, len(text.encode("utf-8"))


def _run_self_test():
    """$0 self-test: dummy whale input, verifies derived manifest naming (S52 patch)."""
    import tempfile
    passed = failed = 0

    def ok(name):
        nonlocal passed
        print(f"  PASS  {name}")
        passed += 1

    def fail(name, reason):
        nonlocal failed
        print(f"  FAIL  {name}: {reason}")
        failed += 1

    print("=== chunk_whale.py v1.1 self-test ===")

    # build a minimal valid whale JSON with a distinct conv_uuid
    test_uuid = "cccccccc-1234-4000-8000-000000000099"
    whale_data = {
        "conv_uuid": test_uuid,
        "headers": [{"snapshot_id": "snap-test", "created_at": "2026-01-01T00:00:00Z"}],
        "messages": [
            {
                "msg_uuid": "msg00001-0000-4000-8000-000000000001",
                "parent_message_uuid": SENTINEL,
                "is_root": True,
                "sender": "human",
                "content_blocks": [{"type": "text", "text": "Hello world"}],
            },
            {
                "msg_uuid": "msg00002-0000-4000-8000-000000000002",
                "parent_message_uuid": "msg00001-0000-4000-8000-000000000001",
                "is_root": False,
                "sender": "assistant",
                "content_blocks": [{"type": "text", "text": "Hi there"}],
            },
        ],
    }

    with tempfile.TemporaryDirectory(prefix="chunk_whale_test_") as td:
        td_path = pathlib.Path(td)
        whale_file = td_path / "test_whale.json"
        whale_file.write_text(json.dumps(whale_data), encoding="utf-8")

        # simulate what main() does after arg parse
        conv      = json.loads(whale_file.read_text(encoding="utf-8"))
        msgs      = conv["messages"]
        hdrs      = conv.get("headers", [])
        conv_uuid = conv["conv_uuid"]
        snap      = hdrs[0]["snapshot_id"] if hdrs else "unknown"
        created   = hdrs[0].get("created_at", "unknown") if hdrs else "unknown"
        bpt       = DEFAULT_BYTES_PER_TOKEN
        byte_budget = int(DEFAULT_MAX_TOKENS * bpt)

        # tree-order check
        seen = set()
        tree_ok = True
        for i, msg in enumerate(msgs):
            uuid_m   = msg.get("msg_uuid", "")
            parent   = msg.get("parent_message_uuid", "")
            is_root  = msg.get("is_root", False)
            if not is_root and parent != SENTINEL and parent not in seen:
                fail(f"tree-order msg[{i}]", f"parent {parent} not yet seen")
                tree_ok = False
            seen.add(uuid_m)
        if tree_ok:
            ok("tree-order check passes on dummy input")

        # render + chunk
        rendered_texts = ["\n".join(render_msg_lines(m)) for m in msgs]
        sizes = [len(t.encode("utf-8")) + 1 for t in rendered_texts]
        header_template = (
            f"CONVERSATION: {conv_uuid}\nSNAPSHOT_ID: {snap}\n"
            f"CREATED: {created}\nMESSAGES: 000\n\n"
        )
        header_bytes = len(header_template.encode("utf-8"))

        chunks, chunk_start, running_bytes = [], 0, header_bytes
        i = 0
        while i < len(msgs):
            sz = sizes[i]
            if running_bytes + sz > byte_budget and i > chunk_start:
                chunks.append((chunk_start, i))
                chunk_start, running_bytes = i, header_bytes
            else:
                running_bytes += sz
                i += 1
        if chunk_start < len(msgs):
            chunks.append((chunk_start, len(msgs)))

        if len(chunks) >= 1:
            ok(f"chunking produced {len(chunks)} chunk(s) for dummy input")
        else:
            fail("chunking", "no chunks produced")

        # write chunks + manifest
        out_prefix = str(td_path / "test_chunk")
        seams = []
        for ci, (start, end) in enumerate(chunks):
            chunk_msgs = msgs[start:end]
            first_uuid = chunk_msgs[0].get("msg_uuid", "?")
            last_uuid  = chunk_msgs[-1].get("msg_uuid", "?")
            last_sender = chunk_msgs[-1].get("sender", "?")
            est_bytes  = sum(sizes[start:end]) + header_bytes
            out_path, actual_bytes = write_chunk_file(
                ci, chunk_msgs, conv_uuid, snap, created, out_prefix
            )
            seams.append({
                "chunk_index": ci, "first_msg_uuid": first_uuid,
                "last_msg_uuid": last_uuid, "msg_count": len(chunk_msgs),
                "byte_size": actual_bytes, "last_sender": last_sender,
            })

        total_msgs = sum(s["msg_count"] for s in seams)
        if total_msgs == len(msgs):
            ok(f"msg count preserved: {total_msgs}/{len(msgs)}")
        else:
            fail("msg count preserved", f"{total_msgs} != {len(msgs)}")

        # key assertion: manifest named from conv_uuid, NOT d9d05961
        manifest_path = pathlib.Path(out_prefix).parent / f"{conv_uuid}_seam_manifest.json"
        manifest_data = {
            "conv_uuid": conv_uuid, "total_msgs": len(msgs),
            "chunks": len(chunks), "max_tokens_budget": DEFAULT_MAX_TOKENS,
            "bytes_per_token": bpt, "byte_budget": byte_budget, "seams": seams,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        if manifest_path.exists():
            ok(f"manifest written: {manifest_path.name}")
        else:
            fail("manifest written", str(manifest_path))

        expected_name = f"{test_uuid}_seam_manifest.json"
        if manifest_path.name == expected_name:
            ok(f"manifest name derived from conv_uuid: {manifest_path.name}")
        else:
            fail("manifest name derived from conv_uuid",
                 f"got {manifest_path.name!r}, expected {expected_name!r}")

        wrong_name = "d9d05961_seam_manifest.json"
        if not (td_path / wrong_name).exists():
            ok(f"hardcoded d9d05961 name NOT present — patch confirmed")
        else:
            fail("hardcoded name absent", f"{wrong_name} unexpectedly exists")

    print(f"\nSelf-test: {passed} passed, {failed} failed.")
    if failed:
        sys.exit(f"SELF-TEST FAILED: {failed} test(s)")
    print("All self-tests PASS. $0.")


def main():
    if "--self-test" in sys.argv:
        _run_self_test()
        sys.exit(0)

    ap = argparse.ArgumentParser()
    ap.add_argument("--in",              dest="infile",          required=True)
    ap.add_argument("--out-prefix",      dest="out_prefix",      required=True)
    ap.add_argument("--max-tokens",      dest="max_tokens",      type=int,   default=DEFAULT_MAX_TOKENS)
    ap.add_argument("--bytes-per-token", dest="bytes_per_token", type=float, default=DEFAULT_BYTES_PER_TOKEN)
    args = ap.parse_args()

    whale     = pathlib.Path(args.infile)
    conv      = json.loads(whale.read_text(encoding="utf-8"))
    msgs      = conv["messages"]
    hdrs      = conv.get("headers", [])
    conv_uuid = conv["conv_uuid"]
    snap      = hdrs[0]["snapshot_id"] if hdrs else "unknown"
    created   = hdrs[0].get("created_at", "unknown") if hdrs else "unknown"

    bpt         = args.bytes_per_token
    byte_budget = int(args.max_tokens * bpt)
    print(f"conv_uuid   : {conv_uuid}")
    print(f"messages    : {len(msgs)}")
    print(f"max_tokens  : {args.max_tokens:,}")
    print(f"B/token     : {bpt}")
    print(f"byte_budget : {byte_budget:,} B")

    # ── 1. Tree-order verification ──────────────────────────────────────────
    # Every non-root message's parent must have appeared earlier in the list.
    seen = set()
    for i, msg in enumerate(msgs):
        uuid   = msg.get("msg_uuid", "")
        parent = msg.get("parent_message_uuid", "")
        is_root = msg.get("is_root", False)
        if not is_root and parent != SENTINEL and parent not in seen:
            print(f"STOP: msg[{i}] uuid={uuid} has parent={parent} "
                  f"that has not appeared yet — file is NOT in tree order.")
            sys.exit(1)
        seen.add(uuid)
    print(f"Tree-order  : PASS (all {len(msgs)} parents precede children)")

    # ── 2. Pre-render every message to measure rendered byte sizes ───────────
    rendered_texts = []
    for msg in msgs:
        lines = render_msg_lines(msg)
        rendered_texts.append("\n".join(lines))

    # Byte size of the rendered text block for each message (incl. trailing newline
    # that will appear as the element separator in the final join).
    sizes = [len(t.encode("utf-8")) + 1 for t in rendered_texts]  # +1 for the \n join

    # Header overhead per chunk (fixed — N digits don't matter much at this scale)
    header_template = (
        f"CONVERSATION: {conv_uuid}\n"
        f"SNAPSHOT_ID: {snap}\n"
        f"CREATED: {created}\n"
        f"MESSAGES: 000\n\n"
    )
    header_bytes = len(header_template.encode("utf-8"))

    # ── 3. Chunking pass ────────────────────────────────────────────────────
    chunks    = []       # list of (start_idx, end_idx_exclusive)
    chunk_start   = 0
    running_bytes = header_bytes

    i = 0
    while i < len(msgs):
        sz = sizes[i]
        if running_bytes + sz > byte_budget and i > chunk_start:
            # Budget exceeded. Apply seam preference: if the last accumulated
            # message is a human turn and THIS message is its assistant reply,
            # include it to avoid a dangling question — only when it won't
            # push us past 1.5× budget (one message worth of slack).
            last_sender = msgs[i - 1].get("sender", "")
            this_sender = msgs[i].get("sender", "")
            if (last_sender == "human"
                    and this_sender == "assistant"
                    and running_bytes + sz <= byte_budget * 1.5):
                running_bytes += sz
                i += 1
            # Close this chunk.
            chunks.append((chunk_start, i))
            chunk_start   = i
            running_bytes = header_bytes
        else:
            running_bytes += sz
            i += 1

    # Close final chunk.
    if chunk_start < len(msgs):
        chunks.append((chunk_start, len(msgs)))

    print(f"Chunks      : {len(chunks)}")

    # ── 4. Write chunk files + seam manifest ────────────────────────────────
    seams = []
    for ci, (start, end) in enumerate(chunks):
        chunk_msgs = msgs[start:end]
        first_uuid = chunk_msgs[0].get("msg_uuid", "?")
        last_uuid  = chunk_msgs[-1].get("msg_uuid", "?")
        last_sender = chunk_msgs[-1].get("sender", "?")
        est_bytes  = sum(sizes[start:end]) + header_bytes

        out_path, actual_bytes = write_chunk_file(
            ci, chunk_msgs, conv_uuid, snap, created, args.out_prefix
        )

        seams.append({
            "chunk_index":    ci,
            "first_msg_uuid": first_uuid,
            "last_msg_uuid":  last_uuid,
            "msg_count":      len(chunk_msgs),
            "byte_size":      actual_bytes,
            "last_sender":    last_sender,
        })
        print(f"  chunk_{ci:02d} : msgs[{start}:{end-1}]  {len(chunk_msgs):3d} msgs  "
              f"{actual_bytes:>9,} B  last={last_sender}  {out_path.name}")

    total_msgs = sum(s["msg_count"] for s in seams)
    print(f"Total msgs  : {total_msgs} / {len(msgs)}")
    if total_msgs != len(msgs):
        print("WARNING: msg count mismatch — chunking dropped or duplicated messages!")
        sys.exit(1)

    manifest = {
        "conv_uuid":         conv_uuid,
        "total_msgs":        len(msgs),
        "chunks":            len(chunks),
        "max_tokens_budget": args.max_tokens,
        "bytes_per_token":   bpt,
        "byte_budget":       byte_budget,
        "seams":             seams,
    }
    manifest_path = pathlib.Path(args.out_prefix).parent / f"{conv_uuid}_seam_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Manifest    : {manifest_path}")


if __name__ == "__main__":
    main()
