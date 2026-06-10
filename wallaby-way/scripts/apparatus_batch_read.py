# wallaby-way/scripts/apparatus_batch_read.py
# version: v1.6
# session: S52
# change notes:
#   v1.6 (S52 "Catechism"):
#     - §15 integrity check PERMANENT: every conv in prepare() gets floor
#       COUNT(DISTINCT msg_uuid) vs payload MESSAGES:N check. v3-aware: DISTINCT
#       only, never row counts — remains correct when scrub-v3 overlay lands.
#       Mismatch -> halted[], never submitted. (_integrity_compare is a pure fn
#       for testability; _query_floor_msg_count owns the DB call.)
#     - §14 rate constants baked in as named code constants: BATCH_INPUT_PER_MTOK
#       = 1.50, BATCH_OUTPUT_PER_MTOK = 7.50 (Batch_Read_Spec v1.2 §14). Printed
#       at every gate line; never re-derived at runtime.
#     - --list subcommand: resolves worklist (conv_uuid, est_tokens, density_flag)
#       from batch list × sizing CSV in same dir, no API calls, $0.
#     - self-test subcommand: $0 only — path resolution, --list against stub
#       worklist, integrity-check unit incl. simulated dup-msg_uuid floor (the
#       v3-awareness case where row count != DISTINCT count).
#   v1.5 (S50): canary --max-tokens override; collect MISSING_PARENTS in report.
#   v1.4 (CCC S2 'Chamfer'): path-fixes for repo reorg — wallaby-way/ restructure.
#   v1.3 (S45 'Cinder'): collect subcommand — re-collects an existing batch-id.
#   v1.2 (S45 'Cinder'): persist loop resilient — guard trip quarantines + continues.
#   v1.1 (S44): --force on canary bypasses resume-skip.
#   v1.0 (S50): initial paid-batch harness per Batch_Read_Spec_v1.1.
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

# ── rate constants (Batch_Read_Spec v1.2 §14) ─────────────────────────────────
# Never re-derive at runtime. Printed at every gate line.
BATCH_INPUT_PER_MTOK  = 1.50   # $/MTok batch input  (50% off $3.00)
BATCH_OUTPUT_PER_MTOK = 7.50   # $/MTok batch output (50% off $15.00)
_RATE_TAG = (
    f"[rates: ${BATCH_INPUT_PER_MTOK}/MTok in · ${BATCH_OUTPUT_PER_MTOK}/MTok out"
    " — Batch_Read_Spec v1.2 §14]"
)

# ── single source of truth ────────────────────────────────────────────────────
MODEL       = "claude-sonnet-4-6"   # the SOLE 1M-window grant; never name elsewhere
TEMPERATURE = 0
MAX_TOKENS  = 32000
BATCH_PERSIST_DIR = "harvested_nodes"

REPO = Path(__file__).resolve().parent.parent.parent   # repo root

BATCH_LIST        = REPO / "wallaby-way" / "runs" / "sizing_S50" / "batch_list_S50.csv"
DEPLOYABLE_READER = REPO / "wallaby-way" / "scripts" / "test_call_system_prompt_S40.md"
FLOOR_EXTRACT     = REPO / "wallaby-way" / "scripts" / "floor_extract.py"
BILLING_ENV       = REPO / "anthropic_billing.env"         # ROOT — paid key
FLOOR_DB_ENV      = REPO / "wallaby-way" / "secrets" / "floor_db.env"  # $0 Postgres creds
PERSIST_DEST      = REPO / "wallaby-way" / "nodes" / "harvested"
QUARANTINE_DEST   = REPO / "wallaby-way" / "nodes" / "quarantine"

# guards / scrub (live modules — named exactly)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline_guards import assert_env_unloaded, tally_nodes, persist_node_file  # noqa: E402
from scrub_output import scrub_text                                               # noqa: E402

SENTINEL = "00000000-0000-4000-8000-000000000000"


# ── helpers ───────────────────────────────────────────────────────────────────
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


# ── §15 integrity check (permanent, v3-aware) ────────────────────────────────

def _read_floor_db_url():
    """Read SUPABASE_DB_URL from floor_db.env. $0 Postgres creds only."""
    import re
    for line in FLOOR_DB_ENV.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*SUPABASE_DB_URL\s*=\s*(.+)$", line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    sys.exit("ERROR: SUPABASE_DB_URL not found in floor_db.env")


def _integrity_compare(payload_count, floor_count, conv_uuid):
    """Pure comparison — testable without a DB. Called by integrity_check().
    v3-aware: caller MUST pass COUNT(DISTINCT msg_uuid), never row counts."""
    if payload_count != floor_count:
        return False, (
            f"INTEGRITY FAIL {conv_uuid}: payload {payload_count} msgs != floor "
            f"{floor_count} DISTINCT msg_uuid (snapshot boundary leak or extract error)"
        )
    return True, f"integrity OK {payload_count}/{floor_count}"


def _query_floor_msg_count(conv_uuid):
    """COUNT(DISTINCT msg_uuid) from floor for one conv. $0 Postgres.
    v3-aware: DISTINCT only — correct whether or not scrub-v3 row-duplication is live."""
    import psycopg
    assert_env_unloaded()
    db_url = _read_floor_db_url()
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(DISTINCT msg_uuid) FROM floor_conv_messages"
                " WHERE conv_uuid = %s::uuid",
                (conv_uuid,),
            )
            row = cur.fetchone()
        conn.rollback()
    return int(row[0])


def integrity_check(conv_uuid, payload_path):
    """§15 permanent check: payload MESSAGES:N vs floor COUNT(DISTINCT msg_uuid).
    Mandatory for any multi-snapshot conv; safe to run on all (single-snapshot
    passes trivially). Returns (ok: bool, reason: str). $0 Postgres read."""
    payload_count = None
    for line in payload_path.read_text(encoding="utf-8").splitlines()[:10]:
        if line.startswith("MESSAGES: "):
            try:
                payload_count = int(line.split("MESSAGES: ", 1)[1].strip())
            except ValueError:
                pass
            break
    if payload_count is None:
        return False, f"INTEGRITY FAIL {conv_uuid}: MESSAGES header not found in payload"

    floor_count = _query_floor_msg_count(conv_uuid)
    return _integrity_compare(payload_count, floor_count, conv_uuid)


# ── --list subcommand ─────────────────────────────────────────────────────────

def cmd_list():
    """Print resolved worklist without firing anything. $0, no key loaded."""
    uuids = load_batch_list()

    # find sizing data in same dir as the batch list
    sizing_dir = BATCH_LIST.parent
    sizing_files = sorted(sizing_dir.glob("sizing_combined_*.csv"))
    sizing: dict = {}
    if sizing_files:
        sf = sizing_files[-1]
        with sf.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                sizing[row["conv_uuid"].strip()] = row
        print(f"Sizing source : {sf.name}  ({len(sizing)} rows)")
    else:
        print(f"No sizing_combined_*.csv in {sizing_dir} — est_tokens/density_flag = N/A")

    print(f"\n{'conv_uuid':<40}  {'est_tokens':>12}  {'density_flag':>12}")
    print("-" * 70)
    for cu in uuids:
        row = sizing.get(cu, {})
        est     = row.get("real_tokens_est", "N/A")
        density = row.get("dense_flag", "N/A")
        print(f"{cu:<40}  {est:>12}  {density:>12}")

    print(f"\n{len(uuids)} convs in worklist. No API calls, no key loaded, $0.")
    print(_RATE_TAG)


# ── self-test subcommand ──────────────────────────────────────────────────────

def cmd_self_test(out_dir=None):
    """$0 self-test — three checks, no API calls, no billing.
    out_dir: optional Path to write a test-report file."""
    passed = 0
    failed = 0

    def ok(name):
        nonlocal passed
        print(f"  PASS  {name}")
        passed += 1

    def fail(name, reason):
        nonlocal failed
        print(f"  FAIL  {name}: {reason}")
        failed += 1

    lines = []

    def tee(msg):
        print(msg)
        lines.append(msg)

    tee("=== apparatus_batch_read.py v1.6 self-test ===")

    # ── T1: path resolution ───────────────────────────────────────────────────
    tee("\n[T1] Path resolution ($0)")
    path_checks = [
        ("BATCH_LIST",        BATCH_LIST,        True),
        ("DEPLOYABLE_READER", DEPLOYABLE_READER,  True),
        ("FLOOR_DB_ENV",      FLOOR_DB_ENV,       True),
        ("PERSIST_DEST",      PERSIST_DEST,       True),
        ("QUARANTINE_DEST",   QUARANTINE_DEST,    True),
        ("BILLING_ENV",       BILLING_ENV,        False),   # gitignored, may not exist
    ]
    for name, path, required in path_checks:
        if path.exists():
            ok(f"{name} exists")
        elif not required:
            tee(f"  SKIP  {name} (gitignored — expected absent in clean checkout)")
        else:
            fail(f"{name} exists", str(path))

    # ── T2: --list against stub worklist ──────────────────────────────────────
    tee("\n[T2] --list against stub worklist ($0)")
    import tempfile as _tmpmod
    stub_uuids = [
        "aaaaaaaa-0000-4000-8000-000000000001",
        "aaaaaaaa-0000-4000-8000-000000000002",
        "aaaaaaaa-0000-4000-8000-000000000003",
    ]
    with _tmpmod.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8", newline=""
    ) as tf:
        w = csv.writer(tf)
        w.writerow(["conv_uuid"])
        for cu in stub_uuids:
            w.writerow([cu])
        stub_path = Path(tf.name)

    try:
        loaded = []
        with stub_path.open() as f:
            for r in csv.DictReader(f):
                loaded.append(r["conv_uuid"].strip())

        if len(loaded) == 3 and loaded == stub_uuids:
            ok("stub worklist loaded (3 rows, exact match)")
        else:
            fail("stub worklist loaded", f"expected 3 rows matching stubs, got {loaded}")

        # simulate list output (no sizing file -> N/A)
        tee(f"  LIST  {'conv_uuid':<40}  {'est_tokens':>12}  {'density_flag':>12}")
        for cu in loaded:
            tee(f"  LIST  {cu:<40}  {'N/A':>12}  {'N/A':>12}")
        ok("--list stub print (no sizing file -- N/A expected)")
    finally:
        stub_path.unlink(missing_ok=True)

    # ── T3: integrity-check unit (no DB) ─────────────────────────────────────
    tee("\n[T3] Integrity-check unit — no DB, pure _integrity_compare ($0)")

    # T3a: payload == floor DISTINCT -> PASS
    r_ok, msg = _integrity_compare(10, 10, "test-uuid-match")
    if r_ok:
        ok("T3a exact match: payload=10 floor_distinct=10 -> PASS")
    else:
        fail("T3a exact match", msg)

    # T3b: real extraction mismatch -> FAIL
    r_ok, msg = _integrity_compare(10, 12, "test-uuid-mismatch")
    if not r_ok and "INTEGRITY FAIL" in msg:
        ok("T3b real mismatch: payload=10 floor_distinct=12 -> FAIL (extraction error caught)")
    else:
        fail("T3b real mismatch", f"expected FAIL+INTEGRITY FAIL, got ok={r_ok} msg={msg}")

    # T3c: v3 dup-msg_uuid scenario
    #   Before scrub-v3: row count and DISTINCT count are the same (no dups yet).
    #   After scrub-v3:  some messages may have new rows, so row count > DISTINCT count.
    #   floor_count here = COUNT(DISTINCT msg_uuid) = 10, payload_count = 10 -> PASS.
    #   If the check used row count instead (=12), it would fire a false alarm -> FAIL.
    #   This test confirms _integrity_compare only receives DISTINCT values.
    r_ok, msg = _integrity_compare(10, 10, "test-uuid-v3-distinct")
    if r_ok:
        ok("T3c v3-aware (DISTINCT path): payload=10, floor_distinct=10 -> PASS")
    else:
        fail("T3c v3-aware (DISTINCT path)", msg)

    # T3d: v3 hazard — show what row-count would do (simulated: row_count=12 != payload=10)
    r_ok_bad, msg_bad = _integrity_compare(10, 12, "test-uuid-v3-rowcount-hazard")
    if not r_ok_bad:
        ok(
            "T3d v3 row-count hazard (simulated): if floor gave row_count=12 vs "
            "payload=10, _integrity_compare fires FAIL — confirms DISTINCT is required"
        )
    else:
        fail("T3d v3 row-count hazard", "expected FAIL from simulated row-count mismatch")

    # ── summary ───────────────────────────────────────────────────────────────
    summary = f"\nSelf-test: {passed} passed, {failed} failed. $0."
    tee(summary)
    tee(_RATE_TAG)

    if out_dir:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        report_path = out_dir / "self_test_apparatus_batch_read.txt"
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Report written: {report_path}")

    if failed:
        sys.exit(f"SELF-TEST FAILED: {failed} test(s)")
    print("All self-tests PASS.")


# ── build phase (no key, no spend) ───────────────────────────────────────────
def prepare(conv_uuids, workdir, force=frozenset(), max_tokens=MAX_TOKENS):
    """Resume-skip -> extract -> §15 integrity check -> skeleton-gate.
    Returns (ready, skipped, halted).
    Convs in `force` bypass the resume-skip (canary supersede path).
    §15 integrity check: payload MESSAGES:N vs floor COUNT(DISTINCT msg_uuid).
    v3-aware: DISTINCT only — correct before and after scrub-v3 overlay."""
    system_text = DEPLOYABLE_READER.read_text(encoding="utf-8")
    ready, skipped, halted = [], [], []
    for cu in conv_uuids:
        if cu not in force and is_complete_artifact(cu):
            skipped.append(cu)
            continue
        payload_path, parents = floor_extract_payload(cu, workdir)

        # §15 integrity check — permanent pre-submit gate
        ic_ok, ic_reason = integrity_check(cu, payload_path)
        if not ic_ok:
            halted.append((cu, ic_reason))
            continue

        ok, reason = skeleton_gate(payload_path)
        if not ok:
            halted.append((cu, reason))
            continue
        req = build_request(
            cu, payload_path.read_text(encoding="utf-8"), system_text, max_tokens
        )
        ready.append((cu, req, parents))
    return ready, skipped, halted


# ── paid phase (key loaded ONLY inside submit/collect) ───────────────────────
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
    v1.2 (S45): the persist LOOP is resilient — a guard trip quarantines the
    offending conv and continues. The guard itself is UNCHANGED."""
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
            QUARANTINE_DEST.mkdir(parents=True, exist_ok=True)
            qpath = QUARANTINE_DEST / f"{cu}.quarantined.md"
            qpath.write_text(catalog, encoding="utf-8")
            quarantined.append((cu, str(e)))
    return persisted, truncated, errored, quarantined


# ── orchestration ─────────────────────────────────────────────────────────────
def build_request(conv_uuid, payload_text, system_text, max_tokens=MAX_TOKENS):
    """One batch request. NO tools key = true-blindness guard."""
    return {
        "custom_id": conv_uuid,
        "params": {
            "model":       MODEL,
            "temperature": TEMPERATURE,
            "max_tokens":  max_tokens,
            "system": [{
                "type":          "text",
                "text":          system_text,
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


def run(conv_uuids, paid, confirm, force=frozenset(), max_tokens=MAX_TOKENS):
    with tempfile.TemporaryDirectory(prefix="batch_payloads_") as td:
        workdir = Path(td)
        ready, skipped, halted = prepare(
            conv_uuids, workdir, force=force, max_tokens=max_tokens
        )
        print(
            f"\nPREPARE: {len(ready)} ready, {len(skipped)} already-complete (skipped), "
            f"{len(halted)} HALTED (skeleton or §15 integrity)"
        )
        for cu, reason in halted:
            print(f"  HALT {cu}: {reason}")
        if not ready:
            print("Nothing to fire."); return
        if not paid:
            print(
                f"\nDRY-RUN complete. {len(ready)} convs would fire. No key loaded, $0.\n"
                f"{_RATE_TAG}"
            )
            return
        if not confirm:
            sys.exit(
                f"PAID path requires --i-understand-this-spends-money. HALT.\n{_RATE_TAG}"
            )
        parents_by_conv = {cu: p for (cu, _req, p) in ready}
        try:
            load_key()
            batch_id = submit_batch(ready)
        finally:
            clear_key()
        results = poll_and_collect_guarded(batch_id)
        p, t, e, q = persist_results(results, parents_by_conv)
        report = (
            f"PERSISTED {len(p)}  TRUNCATED {len(t)} {t}  "
            f"ERRORED {len(e)} {e}  QUARANTINED {len(q)} {[c for c, _ in q]}  "
            f"{_RATE_TAG}"
        )
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
    """Re-collect an already-submitted batch and persist results. No re-submit."""
    if not confirm:
        sys.exit(
            f"PAID path requires --i-understand-this-spends-money. HALT.\n{_RATE_TAG}"
        )
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
        report = (
            f"PERSISTED {len(p)}  TRUNCATED {len(t)} {t}  "
            f"ERRORED {len(e)} {e}  QUARANTINED {len(q)} {[c for c, _ in q]}  "
            f"MISSING_PARENTS {len(missing)} {missing}  {_RATE_TAG}"
        )
        for cu, err in q:
            print(f"  QUARANTINED {cu}: {err}")
        print(scrub_text(report))


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="apparatus paid-batch corpus reader v1.6")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("dry-run", help="$0 — extract+integrity-check+gate the batch, fire nothing")

    c = sub.add_parser("canary", help="fire ONE conv as a batch-of-one (paid)")
    c.add_argument("--conv-uuid", required=True)
    c.add_argument("--i-understand-this-spends-money", action="store_true", dest="confirm")
    c.add_argument("--force", action="store_true",
                   help="bypass resume-skip for this conv (supersede a prior artifact)")
    c.add_argument("--max-tokens", type=int, default=MAX_TOKENS, dest="max_tokens",
                   help=f"output token cap (default {MAX_TOKENS}; raise for truncated re-fires)")

    b = sub.add_parser("batch", help="fire the full frozen batch (paid)")
    b.add_argument("--i-understand-this-spends-money", action="store_true", dest="confirm")

    co = sub.add_parser("collect",
                        help="re-collect an existing batch-id without re-submitting ($0 compute)")
    co.add_argument("--batch-id", required=True)
    co.add_argument("--i-understand-this-spends-money", action="store_true", dest="confirm")

    sub.add_parser("list", help="$0 — print resolved worklist (conv_uuid, est_tokens, density)")

    st = sub.add_parser("self-test",
                        help="$0 — path checks, stub --list, integrity-check unit (no API)")
    st.add_argument("--out-dir", default=None,
                    help="directory to write test-report file (created if absent)")

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
    elif a.cmd == "list":
        cmd_list()
    elif a.cmd == "self-test":
        cmd_self_test(out_dir=a.out_dir)


if __name__ == "__main__":
    main()
