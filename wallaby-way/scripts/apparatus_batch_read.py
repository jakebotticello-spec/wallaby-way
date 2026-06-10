# wallaby-way/scripts/apparatus_batch_read.py
# version: v1.5
# session: S50
# change notes: NEW. The paid-API batch harness for the corpus read, per
#   Batch_Read_Spec_v1.1. Reads the FROZEN list pipeline/s39/batch_list_S44.csv
#   (189 paid convs — the floor-verified disjoint set; NOT re-derived at runtime).
#   Per conv: complete-artifact resume check -> floor_extract (CLI, $0, key unloaded)
#   -> skeleton gate -> assemble request (v4.1 deployable cached system prompt,
#   custom_id=conv_uuid, temp 0, max_tokens 32000, NO tools). Submit via the Message
#   Batches API ONLY with the batch-not-synchronous guard. Poll/collect -> match by
#   custom_id -> scrub_text() -> persist_node_file() (atomic, verify-on-write) to the
#   flat pile harvested_nodes/. Resumability keys off the COMPLETE artifact, not file-exists.
#   v1.1 (S44): --force on canary bypasses resume-skip to supersede a prior artifact.
#   v1.2 (S45 'Cinder'): persist_results loop is resilient — a guard trip quarantines
#   the one conv (scrubbed catalog -> pipeline/s39/quarantine/<uuid>.quarantined.md) and
#   continues, instead of HALTing the whole persist phase. Guard (pipeline_guards.py)
#   UNCHANGED. Recovery re-COLLECTS the existing batch-id ($0), never re-submits.
#   v1.3 (S45 'Cinder'): adds `collect` subcommand — re-collects an already-submitted
#   batch-id without re-submitting. Builds parents via floor_extract ($0 Postgres),
#   then poll_and_collect_guarded + persist_results (resilient, v1.2). Use for recovery
#   when a batch completed server-side but persist halted mid-run.
#   Subcommands: dry-run ($0), canary (1 paid batch-of-one), batch (the 189). Paid paths
#   require --i-understand-this-spends-money. Key loaded submit/collect ONLY, cleared after.
#   v1.4 (CCC S2 'Chamfer'): path-fixes for repo reorg — wallaby-way/ restructure.
#   v1.5 (S50): canary --max-tokens override (whale re-fires at raised cap); collect
#   MISSING_PARENTS surfaced in run report alongside TRUNCATED/ERRORED/QUARANTINED.
#
# DO NOT reuse apparatus_api_testcall.py (S32 synchronous Opus caller — not this).

import argparse
import csv
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# ── single source of truth ────────────────────────────────────────────────
MODEL = "claude-sonnet-4-6"          # the SOLE 1M-window grant; never name elsewhere
TEMPERATURE = 0
MAX_TOKENS = 32000
BATCH_PERSIST_DIR = "harvested_nodes"

REPO = Path(__file__).resolve().parent.parent.parent   # repo root

BATCH_LIST = REPO / "wallaby-way" / "runs" / "sizing_S50" / "batch_list_S50.csv"
DEPLOYABLE_READER = REPO / "wallaby-way" / "scripts" / "test_call_system_prompt_S40.md"   # v4.1.1
FLOOR_EXTRACT = REPO / "wallaby-way" / "scripts" / "floor_extract.py"
BILLING_ENV = REPO / "anthropic_billing.env"           # ROOT — paid key
PERSIST_DEST = REPO / "wallaby-way" / "nodes" / "harvested"
QUARANTINE_DEST = REPO / "wallaby-way" / "nodes" / "quarantine"          # tripped catalogs land here for inspection ($-paid, never discarded)

# guards / scrub (live modules — named exactly)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline_guards import assert_env_unloaded, tally_nodes, persist_node_file  # noqa: E402
from scrub_output import scrub_text                                              # noqa: E402

SENTINEL = "00000000-0000-4000-8000-000000000000"


# ── helpers ────────────────────────────────────────────────────────────────
def load_batch_list():
    """The frozen 189. Read, never re-derived."""
    rows = []
    with BATCH_LIST.open() as f:
        for r in csv.DictReader(f):
            rows.append(r["conv_uuid"].strip())
    return rows


def is_complete_artifact(conv_uuid):
    """Resume key = COMPLETE artifact (DONE line + tally>0), NOT file-exists.
    A half-written file with a wrong count is NOT done (the 4d88185f lesson)."""
    p = PERSIST_DEST / f"{conv_uuid}.md"
    if not p.exists():
        return False
    txt = p.read_text(encoding="utf-8")
    return ("DONE:" in txt) and (tally_nodes(txt)["total"] > 0)


def floor_extract_payload(conv_uuid, workdir):
    """Shell out to the proven CLI extractor. $0 Postgres. Key MUST be unloaded.
    Returns (payload_path, parents_map)."""
    assert_env_unloaded()                      # key must not be hot for a floor read
    out = workdir / f"{conv_uuid}_payload.txt"
    subprocess.run(
        [sys.executable, str(FLOOR_EXTRACT),
         "--conv-uuid", conv_uuid, "--out", str(out)],
        check=True,
    )
    sidecar = Path(str(out) + ".parents.json")
    parents = json.loads(sidecar.read_text(encoding="utf-8"))["parents"]
    return out, parents


def skeleton_gate(payload_path):
    """Spec §4: msg count>0, first/last uuids real (not sentinel), parents present.
    Returns (ok: bool, reason: str). A bad skeleton is caught for $0."""
    txt = payload_path.read_text(encoding="utf-8")
    uuids = []
    for line in txt.splitlines():
        if line.startswith("uuid: "):
            uuids.append(line.split("uuid: ", 1)[1].strip())
    if not uuids:
        return False, "no messages"
    if uuids[0] == SENTINEL or uuids[-1] == SENTINEL:
        return False, "first/last uuid is sentinel"
    if "parent: " not in txt:
        return False, "no parent links"
    return True, f"{len(uuids)} msgs"


def build_request(conv_uuid, payload_text, system_text, max_tokens=MAX_TOKENS):
    """One batch request. NO tools key = true-blindness guard."""
    return {
        "custom_id": conv_uuid,
        "params": {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "max_tokens": max_tokens,
            "system": [{
                "type": "text",
                "text": system_text,
                "cache_control": {"type": "ephemeral"},
            }],
            "messages": [{"role": "user", "content": payload_text}],
        },
    }


def load_key():
    """Load the paid key from ROOT anthropic_billing.env into env. Submit/collect ONLY."""
    import re
    for line in BILLING_ENV.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*ANTHROPIC_API_KEY\s*=\s*(.+)$", line)
        if m:
            os.environ["ANTHROPIC_API_KEY"] = m.group(1).strip().strip('"').strip("'")
            return
    sys.exit("ERROR: ANTHROPIC_API_KEY not found in anthropic_billing.env")


def clear_key():
    os.environ.pop("ANTHROPIC_API_KEY", None)


# ── the build phase (no key, no spend) ──────────────────────────────────────
def prepare(conv_uuids, workdir, force=frozenset(), max_tokens=MAX_TOKENS):
    """Resume-skip -> extract -> skeleton-gate. Returns (ready, skipped, halted).
    Convs in `force` bypass the resume-skip (a canary must fire regardless of a
    prior artifact; its fresh persist atomically supersedes the old one)."""
    system_text = DEPLOYABLE_READER.read_text(encoding="utf-8")
    ready, skipped, halted = [], [], []
    for cu in conv_uuids:
        if cu not in force and is_complete_artifact(cu):
            skipped.append(cu)
            continue
        payload_path, parents = floor_extract_payload(cu, workdir)
        ok, reason = skeleton_gate(payload_path)
        if not ok:
            halted.append((cu, reason))
            continue
        req = build_request(cu, payload_path.read_text(encoding="utf-8"), system_text, max_tokens)
        ready.append((cu, req, parents))
    return ready, skipped, halted


# ── the paid phase (key loaded ONLY inside submit/collect) ───────────────────
def submit_batch(requests):
    """★ BATCH-NOT-SYNCHRONOUS GUARD. Submit to the Message Batches API ONLY.
    Assert a batch object comes back; HALT on anything else. Never fall back to sync."""
    from anthropic import Anthropic
    client = Anthropic()
    batch = client.messages.batches.create(requests=[
        {"custom_id": cu, "params": req["params"]} for (cu, req, _p) in requests
    ])
    if not getattr(batch, "id", None) or getattr(batch, "type", None) != "message_batch":
        sys.exit("BATCH GUARD: response is not a message_batch object — HALT.")
    print(f"BATCH SUBMITTED: id={batch.id}  requests={len(requests)}")
    return batch.id


def poll_and_collect(batch_id):
    from anthropic import Anthropic
    client = Anthropic()
    while True:
        b = client.messages.batches.retrieve(batch_id)
        print(f"  status={b.processing_status}  counts={b.request_counts}")
        if b.processing_status == "ended":
            break
        time.sleep(30)
    results = {}
    for r in client.messages.batches.results(batch_id):
        results[r.custom_id] = r
    return results


def persist_results(results, parents_by_conv):
    """Per result: truncation check -> scrub -> persist (atomic, verify-on-write).
    v1.2 (S45): the persist LOOP is now resilient. A guard trip in persist_node_file()
    (hallucinated anchor, stub, tally-zero) no longer kills the run — the offending
    conv's scrubbed catalog is written to QUARANTINE_DEST for inspection, the conv_uuid
    + exact guard error are recorded, and the loop CONTINUES. The guard itself is
    UNCHANGED and still raises hard; only the caller absorbs the raise. Good reads land
    in harvested_nodes/ as before. Nothing paid-for is discarded; nothing defective lands.
    """
    persisted, truncated, errored, quarantined = [], [], [], []
    for cu, r in results.items():
        if r.result.type != "succeeded":
            errored.append((cu, r.result.type))
            continue
        msg = r.result.message
        if msg.stop_reason == "max_tokens":
            truncated.append(cu)                 # do NOT persist; re-fire higher
            continue
        catalog = "".join(b.text for b in msg.content if b.type == "text")
        catalog = scrub_text(catalog)            # §8 output scrub BEFORE persist
        dest = PERSIST_DEST / f"{cu}.md"
        try:
            persist_node_file(str(dest), catalog, parents_by_conv[cu])
            persisted.append(cu)
        except RuntimeError as e:
            # guard tripped — preserve the paid catalog for in-house inspection, keep going.
            # the guard already cleaned up its temp file; nothing partial landed at dest.
            QUARANTINE_DEST.mkdir(parents=True, exist_ok=True)
            qpath = QUARANTINE_DEST / f"{cu}.quarantined.md"
            qpath.write_text(catalog, encoding="utf-8")
            quarantined.append((cu, str(e)))
    return persisted, truncated, errored, quarantined


# ── orchestration ────────────────────────────────────────────────────────────
def run(conv_uuids, paid, confirm, force=frozenset(), max_tokens=MAX_TOKENS):
    with tempfile.TemporaryDirectory(prefix="batch_payloads_") as td:
        workdir = Path(td)
        ready, skipped, halted = prepare(conv_uuids, workdir, force=force, max_tokens=max_tokens)   # $0
        print(f"\nPREPARE: {len(ready)} ready, {len(skipped)} already-complete (skipped), "
              f"{len(halted)} skeleton-HALTED")
        for cu, reason in halted:
            print(f"  HALT {cu}: {reason}")
        if not ready:
            print("Nothing to fire."); return
        if not paid:
            print(f"\nDRY-RUN complete. {len(ready)} convs would fire. No key loaded, $0.")
            return
        if not confirm:
            sys.exit("PAID path requires --i-understand-this-spends-money. HALT.")
        parents_by_conv = {cu: p for (cu, _req, p) in ready}
        try:
            load_key()
            batch_id = submit_batch(ready)
        finally:
            clear_key()
        results = poll_and_collect_guarded(batch_id)
        p, t, e, q = persist_results(results, parents_by_conv)
        report = (f"PERSISTED {len(p)}  TRUNCATED {len(t)} {t}  "
                  f"ERRORED {len(e)} {e}  QUARANTINED {len(q)} {[c for c, _ in q]}")
        for cu, err in q:
            print(f"  QUARANTINED {cu}: {err}")
        print(scrub_text(report))                 # §8 second surface: scrub the report too


def poll_and_collect_guarded(batch_id):
    try:
        load_key()
        return poll_and_collect(batch_id)
    finally:
        clear_key()


def collect_batch(batch_id, conv_uuids, confirm):
    """Re-collect an already-submitted batch and persist results. No re-submit; $0 batch compute.
    Key loaded only for the retrieve call. Floor_extract runs key-unloaded ($0, Postgres)."""
    if not confirm:
        sys.exit("PAID path requires --i-understand-this-spends-money. HALT.")
    with tempfile.TemporaryDirectory(prefix="collect_payloads_") as td:
        workdir = Path(td)
        parents_by_conv = {}
        print(f"Building parents map for {len(conv_uuids)} convs ($0 floor extract)...")
        for cu in conv_uuids:
            try:
                _, parents = floor_extract_payload(cu, workdir)
                parents_by_conv[cu] = parents
            except Exception as ex:
                print(f"  WARN floor_extract failed {cu}: {ex}")
        results = poll_and_collect_guarded(batch_id)
        missing = [cu for cu in results if cu not in parents_by_conv]
        if missing:
            print(f"  WARN: {len(missing)} convs have no parents — skipping: {missing}")
            results = {cu: r for cu, r in results.items() if cu in parents_by_conv}
        p, t, e, q = persist_results(results, parents_by_conv)
        report = (f"PERSISTED {len(p)}  TRUNCATED {len(t)} {t}  "
                  f"ERRORED {len(e)} {e}  QUARANTINED {len(q)} {[c for c, _ in q]}  "
                  f"MISSING_PARENTS {len(missing)} {missing}")
        for cu, err in q:
            print(f"  QUARANTINED {cu}: {err}")
        print(scrub_text(report))


def main():
    ap = argparse.ArgumentParser(description="apparatus paid-batch corpus reader (S44)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("dry-run", help="$0 — extract+gate the full 189, fire nothing")
    c = sub.add_parser("canary", help="fire ONE conv as a batch-of-one (paid)")
    c.add_argument("--conv-uuid", required=True)
    c.add_argument("--i-understand-this-spends-money", action="store_true", dest="confirm")
    c.add_argument("--force", action="store_true",
                   help="bypass resume-skip for this conv (supersede a prior artifact)")
    c.add_argument("--max-tokens", type=int, default=MAX_TOKENS, dest="max_tokens",
                   help=f"output token cap for this canary (default {MAX_TOKENS}; raise for truncated re-fires)")
    b = sub.add_parser("batch", help="fire the full frozen 189 (paid)")
    b.add_argument("--i-understand-this-spends-money", action="store_true", dest="confirm")
    co = sub.add_parser("collect", help="re-collect an existing batch-id without re-submitting ($0 compute)")
    co.add_argument("--batch-id", required=True)
    co.add_argument("--i-understand-this-spends-money", action="store_true", dest="confirm")
    a = ap.parse_args()

    if a.cmd == "dry-run":
        run(load_batch_list(), paid=False, confirm=False)
    elif a.cmd == "canary":
        force = frozenset([a.conv_uuid]) if a.force else frozenset()
        run([a.conv_uuid], paid=True, confirm=a.confirm, force=force, max_tokens=a.max_tokens)
    elif a.cmd == "batch":
        run(load_batch_list(), paid=True, confirm=a.confirm)
    elif a.cmd == "collect":
        collect_batch(a.batch_id, load_batch_list(), a.confirm)


if __name__ == "__main__":
    main()
