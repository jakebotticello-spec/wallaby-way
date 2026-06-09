# extract_whale.py  v2.0  S38
# Generalized whale serializer — converts a stripped whale JSON to ===MSG=== text format
# for apparatus_api_testcall.py. render_block logic is identical to extract_whale_cfc7a70a.py
# (proven on the canary — do not alter rendering without OC sign-off).
# Usage: python pipeline/extract_whale.py --in <stripped.json> --out <payload.txt>
# Change 1 (S38): --conv-uuid/--snapshot-id/--created override derived header values (flag-2 fix).
# Change 2 (S38): emits <out>.parents.json sidecar {conv_uuid, snapshot_id, parents: {uuid: parent}}.
import json, argparse, pathlib

SENTINEL = "00000000-0000-4000-8000-000000000000"

ap = argparse.ArgumentParser()
ap.add_argument("--in",          dest="infile",          required=True)
ap.add_argument("--out",         dest="outfile",         required=True)
ap.add_argument("--conv-uuid",   dest="conv_uuid_arg",   default=None)
ap.add_argument("--snapshot-id", dest="snapshot_id_arg", default=None)
ap.add_argument("--created",     dest="created_arg",     default=None)
args = ap.parse_args()

WHALE = pathlib.Path(args.infile)
OUT   = pathlib.Path(args.outfile)

conv     = json.loads(WHALE.read_text(encoding="utf-8"))
msgs     = conv["messages"]
hdrs     = conv.get("headers", [])
conv_uuid = conv["conv_uuid"]
snap      = hdrs[0]["snapshot_id"] if hdrs else "unknown"
created   = hdrs[0].get("created_at", "unknown") if hdrs else "unknown"

if args.conv_uuid_arg:
    conv_uuid = args.conv_uuid_arg
if args.snapshot_id_arg:
    snap = args.snapshot_id_arg
if args.created_arg:
    created = args.created_arg


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


lines = [
    f"CONVERSATION: {conv_uuid}",
    f"SNAPSHOT_ID: {snap}",
    f"CREATED: {created}",
    f"MESSAGES: {len(msgs)}",
    "",
]

parents_map = {}

for msg in msgs:
    uuid       = msg.get("msg_uuid", "")
    parent     = msg.get("parent_message_uuid", "")
    role       = msg.get("sender", "")
    is_root    = msg.get("is_root", False)
    parent_out = "null" if (is_root or parent == SENTINEL) else parent
    parents_map[uuid] = parent_out

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

    lines += [
        "===MSG===",
        f"uuid: {uuid}",
        f"parent: {parent_out}",
        f"role: {role}",
        "---",
        content,
        "===END===",
        "",
    ]

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {OUT}  ({OUT.stat().st_size:,} bytes)")

sidecar_path = pathlib.Path(str(OUT) + ".parents.json")
sidecar_path.write_text(
    json.dumps({"conv_uuid": conv_uuid, "snapshot_id": snap, "parents": parents_map},
               indent=2, ensure_ascii=False),
    encoding="utf-8"
)
print(f"Sidecar:  {sidecar_path}  ({len(parents_map)} parents)")
print(f"Messages: {len(msgs)}")
print(f"Snapshot: {snap}")
print(f"Created:  {created}")
