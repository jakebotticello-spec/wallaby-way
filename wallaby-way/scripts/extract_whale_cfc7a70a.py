# extract_whale_cfc7a70a.py  S33
# Serializes the stripped canary whale to ===MSG=== text format for apparatus_api_testcall.py.
# Adapted from extract_one_conv.py — reads a single conv dict (not a spans list).
# Usage: python pipeline/extract_whale_cfc7a70a.py
import json, pathlib

WHALE  = pathlib.Path(__file__).parent / "whales" / "whale_cfc7a70a_stripped.json"
OUT    = pathlib.Path(__file__).parent / "payload_cfc7a70a.txt"
SENTINEL = "00000000-0000-4000-8000-000000000000"

conv = json.loads(WHALE.read_text(encoding="utf-8"))
msgs = conv["messages"]
hdrs = conv.get("headers", [])
conv_uuid = conv["conv_uuid"]
snap      = hdrs[0]["snapshot_id"] if hdrs else "unknown"
created   = hdrs[0].get("created_at", "unknown") if hdrs else "unknown"


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

for msg in msgs:
    uuid      = msg.get("msg_uuid", "")
    parent    = msg.get("parent_message_uuid", "")
    role      = msg.get("sender", "")
    is_root   = msg.get("is_root", False)
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
print(f"Messages: {len(msgs)}")
print(f"Snapshot: {snap}")
print(f"Created:  {created}")
