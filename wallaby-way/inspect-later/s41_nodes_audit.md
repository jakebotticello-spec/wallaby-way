# APPARATUS S41 — pipeline/nodes/ Forensic Audit
# Built: 2026-06-06 | Session: S41 | OC: CC | READ-ONLY

## Scope
Forensic audit of the 24 root-level *.md files in pipeline/nodes/. Focuses on three questions:
1. SOUNDNESS — are these files structurally valid, correctly tallied, real-anchor?
2. 4d88185f THINNESS — why did S39 produce 3 nodes when S34 produced 7? Floor clean?
3. 2 PENDING CONVS — are bd59de6e and e831e30b genuinely unread, or already banked?

**Provenance settled (not reconstructed here):** The 24 files are S34 shape-loop output.
S34 built + canary-validated apparatus_shape_loop.py; pipeline/nodes/<uuid>.md per-conv
output was produced during that run. Files were orphaned when S34 ended context-starved
and pivoted to the API-vs-subscription cost crisis. Source: S34 conversation transcript
(disk record, artifact list confirmed).

**Not audited:** pipeline/nodes/variance/ (10 files) and pipeline/nodes/variance_tuned/
(10 files) — both are multi-run variance-testing artifacts for conv 4d88185f only.
Their existence is noted; they are NOT batch targets and NOT relevant to promotion.

---

## FOCUS 1 — SOUNDNESS TABLE (all 24 root-level files)

All 24 floor-existence checks performed via direct DB SELECT against floor_conv_headers.
Result: **24/24 confirmed present on floor** (also corroborated: all 24 UUIDs appear in
worklist.csv which was built from floor).

### Extraction method
- **tally_match**: count of `**Salience:** MOTION/FENCE/TEXTURE` lines in body == N from DONE line
- **anchor_ok**: all `anchor_msg` values match UUID regex `^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`
- **shape**: `**Named-continuity:**` present AND (if FENCE nodes exist) `**Why:**`/`**Predicate:**` present → v4.0
- **low_node**: node_count < max(3, round(msg_count × 0.05)) — heuristic thin-harvest flag

| file (UUID prefix) | msg_ct | nodes (M/F/T) | drops | tally | anchor | shape | floor | low_node | bucket |
|---|---|---|---|---|---|---|---|---|---|
| 0167e58a | 46 | 17 (11/6/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| 09db32a8 | 46 | 21 (14/7/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| 201646e5 | 26 | 13 (8/5/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| 290f6d20 | 14 | 7 (5/2/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| 2fea4234 | 44 | 13 (8/5/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| 3e9a15f1 | 104 | 23 (16/7/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| 43df44a2 | 156 | 37 (22/15/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| 4c725f2a | 22 | 16 (10/5/1) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| **4d88185f** | 14 | 7 (4/3/0) | 0 | OK | OK | v4.0 | ✓ | — | **DUPLICATE+SOUND-v4** |
| 5a5efd53 | 62 | 22 (14/7/1) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| **63b6e85a** | 16 | 6 (4/2/0) | 0 | OK | OK | v4.0 | ✓ | — | **DUPLICATE+SOUND-v4** |
| 642d8365 | 78 | 17 (12/5/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| 6953b3b7 | 40 | 22 (14/8/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| 6a096d18 | 6 | 6 (4/2/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| 6b44447e | 34 | 19 (13/6/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| 80befe2a | 61 | 21 (15/6/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| 9905f7f6 | 40 | 17 (10/7/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| 9bf5733a | 52 | 18 (10/8/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| abe2c722 | 58 | 15 (10/5/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| acd2b950 | 24 | 13 (7/6/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| **b51296dd** | 2 | 2 (2/0/0) | 0 | OK | OK | v4.0 | ✓ | flagged | **THIN*** |
| c3823a3c | 112 | 25 (20/4/1) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| dbb2dacd | 21 | 11 (5/6/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |
| e49e2627 | 91 | 20 (12/8/0) | 0 | OK | OK | v4.0 | ✓ | — | SOUND-v4 |

*b51296dd THIN note: The heuristic flagged it (2 nodes < threshold of 3), but this is a
FALSE POSITIVE. The conv has only 2 messages and both were harvested as nodes — 100% harvest
rate. Not a thin read; re-read in batch will confirm. No concern.

**File mtimes:** All 24 cluster on 2026-06-03 12:34–13:14 (UTC-6 local), consistent with a
single continuous session run. Mtime is WEAK evidence (copy/move resets it), but the tight
cluster corroborates the S34 session attribution.

**FOCUS 1 verdict:** 0 SUSPECT, 0 structural failures, 0 bad anchors. All 24 are structurally
sound v4.0 output. Safe to re-read in v4.1 batch without special flags.

### Duplicate comparison: 4d88185f and 63b6e85a

| location | nodes | M/F/T | note |
|---|---|---|---|
| pipeline/nodes/4d88185f.md | **7** | 4/3/0 | Full v4.0 read, all 14 messages covered |
| harvested_nodes/4d88185f.md | 3 | 2/1/0 | READER FAILURE — see FOCUS 2 |
| pipeline/nodes/63b6e85a.md | 6 | 4/2/0 | Clean v4.0, 16 messages |
| harvested_nodes/63b6e85a.md | **7** | 5/2/0 | One additional MOTION node vs pipeline/nodes/ |

For 4d88185f: pipeline/nodes/ is the authoritative version (see FOCUS 2).
For 63b6e85a: both are valid; harvested_nodes/ captured one more MOTION node. Minor difference,
both are SOUND-v4. Harvested version is canonical (already in cold-store).

---

## FOCUS 2 — 4d88185f THINNESS: SETTLED

### Background
S39 on-sub loop recorded 4d88185f returning 3 nodes (cold-stored in harvested_nodes/). S39
at the time attributed this to [tool_result truncated …KB] strip markers (apparatus_strip_v1.py).
That theory was falsified corpus-wide by S40 READ-0: strip ran only on 4 whale working copies,
never touched the floor. So the strip explanation was superseded and 4d88185f's thinness was
labeled UNEXPLAINED.

### Findings

**(a) Content comparison: pipeline/nodes/ (7 nodes) vs harvested_nodes/ (3 nodes)**

**pipeline/nodes/4d88185f.md — 7 nodes, CLEAN:**
The 7-node read correctly covers the full 14-message conv (LRN "dick balls" client email bug):
- Node 1: Context file load (MOTION)
- Node 2: Security note re athleteName client-side injection (FENCE)
- Node 3: Plain-speak explanation of tampering (MOTION)
- Node 4: Correction — it's the athlete name field, not plan name (FENCE)
- Node 5: Narrowing CMS field source (MOTION)
- Node 6: CMS confirmed clean; embed code requested (MOTION)
- Node 7: Root cause confirmed + fix (FENCE — global memberInfo var editable via console)

All 14 messages are accounted for in node coverage (anchor_msg UUIDs trace contiguously
from msg 1 through msg 14). This is a complete, correct read.

**harvested_nodes/4d88185f.md — 3 nodes, READER FAILURE:**
The file opens with leaked meta-commentary that does NOT belong in v4.0 output:
> "Note — I see this conversation is a **14-message** conversation but the user uploaded a
> context file and the response includes a truncation note. Let me read the actual messages
> in the conversation carefully."

This is the S39 reader's internal deliberation appearing verbatim in the output file.
After that preamble, the reader produced only 3 nodes, with node 3 being a catchall:
> "The remaining 12 messages (not visible in the extraction) contain the actual back-and-forth
> on whatever specific issue he was hunting."

This is a fabricated summary of messages the reader did NOT actually read in the output,
masked as a node.

**(b) Floor payload check**

File: `pipeline/s39/4d88185f-fe6c-495a-9b9e-713d4f532092_payload.txt`
- Size: 55,407 bytes | Messages: 14 (confirmed)
- Truncation markers (`[tool_result truncated`): **ZERO**

The floor payload is completely clean. The conv contains a large [TOOL_RESULT: view] block
(the 1631-line LRN context file uploaded by Jake), but this is NOT a strip artifact —
it is intact tool_result content as stored on the floor. The S39 reader encountered this
large tool_result, got confused (treating it as a truncation signal), leaked its meta-thinking
into the output, and bailed after 3 nodes.

**(c) Verdict**

**S39's strip-truncation explanation: REFUTED.**

The floor payload for 4d88185f has no strip markers and no actual truncation. The 3-node
cold-store output was 100% a reader failure — the S39 on-sub reader version was not robust
to large tool_result blocks containing uploaded files, misread the presence of such a block
as a truncation condition, and produced a corrupt 3-node catalog with leaked internal narration.

**The pipeline/nodes/ 7-node version is the authoritative read.** It was produced by S34's
apparatus_shape_loop.py, which handled the payload correctly.

**Impact on re-read planning:** The floor payload is clean, so v4.1 batch will receive the
same clean 55KB payload as S34 did. Expect ~7 nodes from v4.1 re-read (same content as
pipeline/nodes/ version). No special handling needed.

---

## FOCUS 3 — 2 PENDING FREE CONVS

### bd59de6e-c2ee-498e-905b-b3c38c195c11

Location check across ALL node stores:
- harvested_nodes/: NOT PRESENT
- pipeline/nodes/: NOT PRESENT
- pipeline/s39/\*_nodes_raw.txt: NOT PRESENT
- pipeline/ result_*.md: NOT PRESENT
- pipeline/s39/_grade_result_*.txt: NOT PRESENT

**pipeline/s39/bd59de6e-c2ee-498e-905b-b3c38c195c11_payload.txt: PRESENT** (payload extracted,
conv ready for reading — it was prepared for the free-arm on-sub loop but never ran).

**VERDICT: GENUINELY UNREAD. Fold into paid batch.**

### e831e30b-34fc-4af5-8815-160f4da1c565

Location check:
- harvested_nodes/: NOT PRESENT
- pipeline/nodes/: NOT PRESENT
- pipeline/s39/\*_nodes_raw.txt: NOT PRESENT
- pipeline/ result_*.md: NOT PRESENT

**pipeline/s39/_grade_result_precision.txt: PRESENT — contains a full 6-node read**

File evidence: `_grade_result_precision.txt` contains:
```
=== TOKEN USAGE ===
input_tokens:  109,590
output_tokens: 2,421
stop_reason:   end_turn
truncated:     False
cost_usd:      $0.3651

=== SONNET+ADDENDUM CATALOG OUTPUT ===
# SCOPE READER OUTPUT
# conv e831e30b-34fc-4af5-8815-160f4da1c565 | baseline-2026-05-25-ae015455 | 6 messages
...
--- DONE: 6 nodes (5 MOTION, 1 FENCE, 0 TEXTURE), 0 drops ---
```

This is a paid API call ($0.3651, input 109K tokens) that produced a complete and correct
6-node v4.0 catalog during S40's precision-addendum test. The read was structurally clean:
tally matches (6 nodes in body = 6 in DONE line), all anchors are real UUID v7 values.

However: this is a **TEST ARTIFACT**, not a canonical harvest. The file lives in
`pipeline/s39/_grade_result_precision.txt` (underscore prefix = test/diagnostic), was never
written to harvested_nodes/ or pipeline/nodes/, and will not be found by the batch skip logic.

**VERDICT: NOT PERSISTED AS CANONICAL HARVEST. Fold into paid batch.**

The v4.1 re-read of e831e30b should expect ~6 nodes (5M/1F/0T) based on the S40 test. The
$0.37 previously spent on the test does not protect this conv from being re-read; batch will
spend again on it.

---

## BUCKET SUMMARY

| Bucket | Count | Notes |
|---|---|---|
| SOUND-v4 | 21 | All tally OK, anchors OK, v4.0 shape, floor confirmed |
| THIN (heuristic false positive) | 1 | b51296dd — 2-msg conv, 2/2 nodes = 100% harvest rate |
| SUSPECT | 0 | None |
| DUPLICATE+SOUND-v4 | 2 | 4d88185f, 63b6e85a |

**One-line verdict: PROMOTE-ELIGIBLE / RE-READ-ON-BATCH.** All 24 files are structurally sound
v4.0 output. Zero anchor violations, zero tally mismatches, zero missing floor convs.
The "THIN" flag on b51296dd is a false positive (100% 2-msg harvest). 4d88185f and 63b6e85a
are duplicates of cold-store files; the pipeline/nodes/ version of 4d88185f is MORE authoritative
than the cold-store version. Proceed with v4.1 batch re-read as planned.

---

## CHANGE MANIFEST

**Files read (no changes):**
- pipeline/nodes/*.md (24 root files)
- harvested_nodes/4d88185f-fe6c-495a-9b9e-713d4f532092.md
- harvested_nodes/63b6e85a-2d9a-4b52-8923-d8d3a63f0cf0.md
- pipeline/s39/4d88185f-fe6c-495a-9b9e-713d4f532092_payload.txt
- pipeline/s39/_grade_result_precision.txt
- pipeline/secrets/floor_db.env (read-only, SUPABASE_DB_URL extracted)
- pipeline/s39/worklist.csv (cross-reference)
- pipeline/s39/run_log.csv (cross-reference)

**DB queries:** 24 × `SELECT 1 FROM floor_conv_headers WHERE conv_uuid::text = %s LIMIT 1`
  — read-only, connection.rollback() called. No writes.

**File written:** pipeline/s41_nodes_audit.md (this file — created, not modified)

**No files modified, moved, renamed, or deleted.**
