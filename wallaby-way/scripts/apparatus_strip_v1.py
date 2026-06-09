"""
apparatus_strip_v1.py  ·  v1.0  ·  apparatus S33 ("Cartographer")  ·  2026-06-03

ONE-TIME whale-echo stripper. NOT a pipeline organ.

PURPOSE
-------
The corpus holds 4 conversations over the 1M-token reader ceiling ("whales"),
all from the paste-everything-in-chat era. Each is mostly machine-echo: a
read/echo tool (view, bash_tool) dumping huge files and prior-conversation
transcripts back into the chat. This script lifts a whale's already-lifted
working copy, neutralizes the confirmed echo on a NEW stripped copy (never
mutating the input), writes a per-block audit receipt, and leaves the floor
and the working copy untouched.

Run once per whale. After the 4 are read + cataloged, this script is done.
Going-forward whale handling is detect-and-alert in the 325-loop, NOT this.

THE 5-POINT GATE (The Wallaby Whales) — how this satisfies it
-------------------------------------------------------------
1. POSITIVE-SIGNATURE: a block is stripped ONLY if it is a tool_result whose
   `name` is a known read/echo tool AND it is over THRESHOLD. Tool identity is
   the positive signature (more robust than sniffing returncode/stdout strings).
2. KEEP-BIASED: default is KEEP. Non-tool_result blocks never considered.
   Small tool_results kept unconditionally. tool_results from non-read tools
   (create_file, web_search, str_replace, etc. — deliverables) kept always.
3. KIND-#4 HARDENED vs code-deliverables: satisfied by tool identity. A
   deliverable (create_file/str_replace) is never in the strip allowlist, so a
   big code-delivery block CANNOT be mistaken for echo. No size-and-not-prose
   heuristic exists in this cutter — that was the bug; it is gone.
4. AUDITABLE: every cut writes a receipt row {block_id, host_msg_uuid, conv_uuid,
   tool_name, content_bytes_dropped, display_content_bytes_dropped}. Both payload
   fields logged SEPARATELY so the audit proves BOTH copies were neutralized.
5. LAST-RESORT / LOW-BLAST-RADIUS: enforced by invocation — this is pointed at
   the 4 registry whales by name and nothing else. It is not wired into any loop.

DUAL-PAYLOAD NEUTRALIZATION (Finding 2 — the load-bearing catch)
----------------------------------------------------------------
A tool_result carries its payload TWICE: `content` (the list) AND
`display_content` (a json_block mirror). Stripping only `content` leaves ~half
the echo and the whale may not drop under ceiling. This cutter neutralizes BOTH
on a flagged block and logs each separately.

PLACEHOLDER
-----------
Stripped blocks are replaced with the reader's expected language: a
"[tool_result truncated ... ]" marker. Boot_ScopeReader_v4.0 already instructs the
reader to read that as "a file dump happened here, no decision in it." We align
to the reader's existing, proven wording rather than introduce a new token.

WHAT THIS DOES NOT DO
---------------------
- Does NOT estimate tokens or claim the result "fits." Fit is proven by firing
  the stripped copy at the API and reading usage.input_tokens. (The old
  4.0-bytes/token proxy is dead — it under-counts echo 2-3x; that is why these
  are whales.)
- Does NOT write into the floor or the input working copy. Output is a new file.
- Does NOT run on anything but the file path you hand it.

USAGE
-----
  python apparatus_strip_v1.py --in  pipeline/whales/whale_<uuid>.json \
                               --out pipeline/whales/whale_<uuid>_stripped.json \
                               --receipt pipeline/whales/whale_<uuid>_receipt.json
  (optional) --threshold 50000   # default 50_000 bytes (gentle). Lower only if
                                 # the stripped copy is still over ceiling.
"""

import json
import argparse
from pathlib import Path

# ── tuned to the 4 known whales (grounded in canary tool_result name census) ──
# Read/echo tools whose LARGE results are confirmed machine-echo. Anything not
# in this set is KEPT regardless of size (deliverables: create_file, str_replace,
# web_search, etc.).
STRIP_TOOLS = {"view", "bash_tool", "cat", "str_replace_based_edit_tool"}
# NOTE: str_replace_based_edit_tool's *view* sub-op echoes files, but its edit op
# is a deliverable. On these 4 whales the edit tool does not appear among large
# blocks; it is listed here only because its `view` mode is a read/echo. If a
# future run ever flags one, the receipt catches it — keep-biased + audited.

DEFAULT_THRESHOLD = 50_000  # bytes. Gentle: only the obviously-large echo blocks.

# HEADER-KEEP: how much of each cut block's head to retain as a pointer-preview.
# ~25 lines reliably captures the version/filename/changelog/deploy-state header
# Jake wants held; the char cap stops a pathological single long line from
# reinflating the block. Tunable; these are not doctrine, just sane defaults.
HEADER_LINES     = 25
HEADER_MAX_CHARS = 4_000


def field_bytes(value) -> int:
    """UTF-8 byte size of a content field (list/dict serialized, str as-is)."""
    if value is None:
        return 0
    s = value if isinstance(value, str) else json.dumps(value, default=str)
    return len(s.encode("utf-8"))


def block_text(block: dict) -> str:
    """Pull plain text out of a tool_result content field (list or str)."""
    c = block.get("content")
    if isinstance(c, list):
        return "\n".join(it.get("text", "") or "" for it in c if isinstance(it, dict))
    return c if isinstance(c, str) else ""


def header_preview(raw_text: str, n_lines: int = 25, max_chars: int = 4000) -> str:
    """
    Keep the first n_lines of the ACTUAL echoed content (the file/transcript
    header — version, filename, changelog, deploy-state — the PROCESS Jake wants
    held). The bash stdout is escaped JSON; decode it so \\n becomes real lines,
    then take the head. Capped at max_chars so a pathological long-line header
    cannot reinflate the stripped block. Best-effort: on any decode failure,
    falls back to the raw head (still bounded). The goal is a faithful POINTER
    preview, not a pristine reproduction.
    """
    txt = raw_text
    try:
        obj = json.loads(raw_text)
        if isinstance(obj, dict) and "stdout" in obj:
            txt = obj["stdout"]            # json.loads already unescaped \n, \u2014, etc.
    except Exception:
        pass                                # not a clean wrapper — use raw text head
    lines = txt.split("\n")
    head = "\n".join(lines[:n_lines]).strip()
    return head[:max_chars]


def should_strip(block: dict, threshold: int):
    """
    POSITIVE-SIGNATURE strip decision. Returns (True, total_bytes) to strip,
    (False, 0) to keep. Default is KEEP.
    """
    if block.get("type") != "tool_result":
        return (False, 0)

    name = (block.get("name") or "").strip()
    if name not in STRIP_TOOLS:
        return (False, 0)  # deliverable or unknown tool → KEEP

    c_bytes  = field_bytes(block.get("content"))
    dc_bytes = field_bytes(block.get("display_content"))
    total    = c_bytes + dc_bytes

    if total < threshold:
        return (False, 0)  # small → KEEP unconditionally

    return (True, total)


def strip_conversation(conv: dict, threshold: int):
    """
    Returns (stripped_conv, receipt_rows). Builds a NEW conv dict; does not
    mutate the input. Neutralizes BOTH content and display_content on flagged
    blocks, logging each separately.
    """
    conv_uuid = conv.get("conv_uuid", "?")
    receipt_rows = []
    new_messages = []

    for msg in conv.get("messages", []):
        host_uuid = msg.get("msg_uuid", "?")
        blocks = msg.get("content_blocks") or []
        if not isinstance(blocks, list):
            blocks = []
        new_blocks = []

        for blk in blocks:
            strip_it, _ = should_strip(blk, threshold)
            if not strip_it:
                new_blocks.append(blk)
                continue

            c_bytes  = field_bytes(blk.get("content"))
            dc_bytes = field_bytes(blk.get("display_content"))
            name     = blk.get("name") or "?"
            block_id = blk.get("tool_use_id") or blk.get("id") or "?"

            # HEADER-KEEP: retain the first ~25 real lines of the echoed content
            # (version/filename/changelog/deploy-state — the process texture).
            # The code body underneath is what gets cut; the header is the pointer.
            header = header_preview(block_text(blk), HEADER_LINES, HEADER_MAX_CHARS)
            header_bytes = len(header.encode("utf-8"))

            receipt_rows.append({
                "conv_uuid": conv_uuid,
                "host_msg_uuid": host_uuid,
                "block_id": block_id,
                "tool_name": name,
                "content_bytes_dropped": c_bytes,
                "display_content_bytes_dropped": dc_bytes,
                "total_bytes_dropped": c_bytes + dc_bytes,
                "header_bytes_kept": header_bytes,
            })

            # Build a neutralized copy of the block — both payload fields replaced
            # with the reader's expected "truncated" language PLUS the kept header,
            # so a future reader sees what was being read (and can follow it to the
            # source conversation) instead of a blind hole. All other metadata
            # (name, tool_use_id, timestamps, is_error) preserved so the skeleton
            # and the tool_use<->tool_result linkage survive intact.
            note = (f"[tool_result truncated — {name} echo, "
                    f"{c_bytes + dc_bytes:,} bytes machine-output removed at strip. "
                    f"Header kept below for context; full content lives in its source conversation.]")
            payload = note + ("\n\n--- kept header ---\n" + header if header else "")
            kept = dict(blk)
            kept["content"] = [{"type": "text", "text": payload}]
            if "display_content" in kept and kept.get("display_content") is not None:
                kept["display_content"] = {"type": "text", "text": payload}
            new_blocks.append(kept)

        new_msg = dict(msg)
        new_msg["content_blocks"] = new_blocks
        new_messages.append(new_msg)

    new_conv = dict(conv)
    new_conv["messages"] = new_messages
    return new_conv, receipt_rows


def main():
    ap = argparse.ArgumentParser(description="One-time whale-echo stripper (apparatus S33).")
    ap.add_argument("--in",      dest="infile",  required=True, help="lifted whale working copy (read-only input)")
    ap.add_argument("--out",     dest="outfile", required=True, help="stripped copy to write (new file)")
    ap.add_argument("--receipt", dest="receipt", required=True, help="audit receipt JSON to write")
    ap.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD, help=f"strip byte threshold (default {DEFAULT_THRESHOLD})")
    args = ap.parse_args()

    in_path  = Path(args.infile)
    out_path = Path(args.outfile)
    rcpt_path = Path(args.receipt)

    if out_path.exists():
        raise SystemExit(f"REFUSE: output already exists ({out_path}). Delete it first — never silently overwrite a strip.")

    raw = in_path.read_bytes()
    data = json.loads(raw.decode("utf-8"))

    # The lifted whale files are a single conv dict (confirmed canary shape:
    # {conv_uuid, headers, messages}). Handle a list-wrapper defensively too.
    convs = data if isinstance(data, list) else [data]

    all_receipts = []
    out_convs = []
    for conv in convs:
        stripped, rows = strip_conversation(conv, args.threshold)
        out_convs.append(stripped)
        all_receipts.extend(rows)

    out_obj = out_convs if isinstance(data, list) else out_convs[0]
    out_json = json.dumps(out_obj, indent=2, default=str)
    out_path.write_text(out_json, encoding="utf-8")

    # ── totals for the receipt header ──
    in_bytes  = len(raw)
    out_bytes = len(out_json.encode("utf-8"))
    content_dropped = sum(r["content_bytes_dropped"] for r in all_receipts)
    display_dropped = sum(r["display_content_bytes_dropped"] for r in all_receipts)
    header_kept     = sum(r.get("header_bytes_kept", 0) for r in all_receipts)

    receipt = {
        "script": "apparatus_strip_v1.py v1.0 (S33)",
        "input_file": str(in_path),
        "output_file": str(out_path),
        "threshold_bytes": args.threshold,
        "strip_tools": sorted(STRIP_TOOLS),
        "blocks_stripped": len(all_receipts),
        "header_lines_kept_per_block": HEADER_LINES,
        "header_bytes_kept_total": header_kept,
        "input_bytes": in_bytes,
        "output_bytes": out_bytes,
        "content_bytes_dropped_total": content_dropped,
        "display_content_bytes_dropped_total": display_dropped,
        "total_bytes_dropped": content_dropped + display_dropped,
        "pct_of_input_dropped": round(100 * (content_dropped + display_dropped) / max(in_bytes, 1), 2),
        "blocks": all_receipts,
    }
    rcpt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")

    # ── console summary (eyeball before trusting) ──
    print("=" * 68)
    print("APPARATUS STRIP v1 — one-time whale neutralization")
    print("=" * 68)
    print(f"  input        : {in_path.name}  ({in_bytes:,} B)")
    print(f"  output       : {out_path.name}  ({out_bytes:,} B)")
    print(f"  receipt      : {rcpt_path.name}")
    print(f"  threshold    : {args.threshold:,} B")
    print(f"  blocks cut   : {len(all_receipts)}")
    print(f"  content drop : {content_dropped:,} B")
    print(f"  display drop : {display_dropped:,} B")
    print(f"  header kept  : {header_kept:,} B  ({HEADER_LINES} lines/block — version/changelog/state preserved)")
    print(f"  total drop   : {content_dropped + display_dropped:,} B  "
          f"({receipt['pct_of_input_dropped']}% of input)")
    print(f"  remaining    : {out_bytes:,} B")
    print("-" * 68)
    print("  Per-block receipt written. Confirm every row is a read/echo tool")
    print("  and BOTH payload columns are accounted for before reading the copy.")
    print("  Fit is NOT claimed here — prove it by firing the copy at the API.")
    print("=" * 68)


if __name__ == "__main__":
    main()
