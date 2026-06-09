# grade_recut_S42.py  v1.1  CCC S2 (Chamfer)  2026-06-08
# v1.1 (CCC S2 'Chamfer'): path-fixes for repo reorg — wallaby-way/ restructure.
"""
S42 recut grade probe — first honest grade of the v4.1 deployable.
Fires pipeline/test_call_system_prompt_S40.md READ FROM DISK — no stitching, no append.
DO NOT EDIT the two broken tombstone probes (_grade_probe_s40.py, _grade_probe_precision.py).

Payload: e831e30b-34fc-4af5-8815-160f4da1c565 (UUID-dense conv_search session, 381773 bytes)
Model:   claude-sonnet-4-6, temperature=0, max_tokens=32000
"""
import os, sys
from pathlib import Path

ROOT = Path(r"c:\claude-reference")

# ── SYSPROMPT PATH — THE REAL RECUT FILE, NOT S32 ───────────────────────────
SYSPROMPT_PATH = ROOT / "wallaby-way" / "scripts" / "test_call_system_prompt_S40.md"

BILLING_ENV  = ROOT / "anthropic_billing.env"
PAYLOAD_PATH = ROOT / "history" / "s39-archived-data" / "e831e30b-34fc-4af5-8815-160f4da1c565_payload.txt"
RESULT_PATH  = ROOT / "wallaby-way" / "runs" / "grade-evidence" / "_grade_result_recut_S42.txt"

# ── billing guard ─────────────────────────────────────────────────────────────
if "ANTHROPIC_API_KEY" in os.environ:
    sys.exit("BILLING GUARD: ANTHROPIC_API_KEY already in env — HALT (do not load on-sub)")

# ── load billing key ──────────────────────────────────────────────────────────
api_key = None
for line in BILLING_ENV.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line.startswith("ANTHROPIC_API_KEY="):
        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
        break

if not api_key:
    sys.exit("ERROR: could not parse ANTHROPIC_API_KEY from billing env — HALT")

# NO key prefix printed — key names only per JAKE-RULES
sys.stdout.buffer.write(b"Billing key loaded (ANTHROPIC_API_KEY)\n")

# ── read system prompt + payload ──────────────────────────────────────────────
system_prompt = SYSPROMPT_PATH.read_text(encoding="utf-8")
payload       = PAYLOAD_PATH.read_text(encoding="utf-8")

sys.stdout.buffer.write(f"System prompt: {SYSPROMPT_PATH.name} ({len(system_prompt):,} chars)\n".encode())
sys.stdout.buffer.write(f"Payload:       {PAYLOAD_PATH.name} ({len(payload):,} chars)\n".encode())
sys.stdout.buffer.flush()

# ── fire single paid call ─────────────────────────────────────────────────────
import anthropic

client = anthropic.Anthropic(api_key=api_key)

sys.stdout.buffer.write(b"\nFiring single streaming call: claude-sonnet-4-6, max_tokens=32000, temp=0...\n")
sys.stdout.buffer.flush()

catalog_text = ""
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=32000,
    temperature=0,
    system=system_prompt,
    messages=[{"role": "user", "content": payload}],
) as stream:
    for text in stream.text_stream:
        catalog_text += text
    response = stream.get_final_message()

# ── CLEAR KEY IMMEDIATELY after response captured ────────────────────────────
del api_key
client = None

usage         = response.usage
input_tokens  = usage.input_tokens
output_tokens = usage.output_tokens
stop_reason   = response.stop_reason
truncated     = stop_reason == "max_tokens"

cost_usd = (input_tokens / 1_000_000) * 3.0 + (output_tokens / 1_000_000) * 15.0

# ── SAVE TO DISK BEFORE ANY PRINT (prior probe crashed and lost catalog) ─────
with open(RESULT_PATH, "w", encoding="utf-8") as f:
    f.write("=== GRADE RECUT S42 ===\n")
    f.write(f"sysprompt: {SYSPROMPT_PATH}\n")
    f.write(f"payload:   {PAYLOAD_PATH}\n\n")
    f.write("=== TOKEN USAGE ===\n")
    f.write(f"input_tokens:  {input_tokens:,}\n")
    f.write(f"output_tokens: {output_tokens:,}\n")
    f.write(f"stop_reason:   {stop_reason}\n")
    f.write(f"truncated:     {truncated}\n")
    f.write(f"cost_usd:      ${cost_usd:.4f}\n\n")
    if truncated:
        f.write("*** TRUNCATED — stop_reason=max_tokens; output is INCOMPLETE ***\n\n")
    f.write("=== S40 RECUT CATALOG OUTPUT ===\n")
    f.write(catalog_text)

sys.stdout.buffer.write(f"\nRESULT SAVED TO: {RESULT_PATH}\n".encode())
sys.stdout.buffer.write(b"=== BILLING KEY: CLEARED ===\n\n")

# ── report usage ──────────────────────────────────────────────────────────────
sys.stdout.buffer.write(b"=== TOKEN USAGE ===\n")
sys.stdout.buffer.write(f"input_tokens:  {input_tokens:,}\n".encode())
sys.stdout.buffer.write(f"output_tokens: {output_tokens:,}\n".encode())
sys.stdout.buffer.write(f"stop_reason:   {stop_reason}\n".encode())
if truncated:
    sys.stdout.buffer.write(b"*** TRUNCATED -- output is INCOMPLETE, do not treat as passing ***\n")
else:
    sys.stdout.buffer.write(b"TRUNCATED:     False\n")
sys.stdout.buffer.write(f"cost_usd:      ${cost_usd:.4f}\n".encode())
sys.stdout.buffer.flush()

# ── print catalog (file saved — console failure is non-fatal) ─────────────────
sys.stdout.buffer.write(b"\n=== S40 RECUT CATALOG OUTPUT ===\n")
try:
    sys.stdout.buffer.write(catalog_text.encode("utf-8"))
except Exception as e:
    sys.stdout.buffer.write(f"[console display error: {e} — but file is saved at {RESULT_PATH}]\n".encode())
sys.stdout.buffer.flush()
