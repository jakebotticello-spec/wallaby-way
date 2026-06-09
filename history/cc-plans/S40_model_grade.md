S40 apparatus — MODEL GRADE TEST (Sonnet 4.6 vs known-good Opus). This makes ONE INTENTIONAL PAID API CALL (~$0.30), explicitly authorized by Jake. Read PROHIBITIONS first.

=== PROHIBITIONS ===
P1. The ONLY paid call permitted is the SINGLE Sonnet grade call described in STEP 3. Do NOT batch, loop, or fire any other metered call. One conv, one call.
P2. anthropic_billing.env (ROOT — not pipeline/secrets/, not floor_db.env) is the ONLY billing key source. Load it ONLY for STEP 3, the authorized paid call. Do NOT load it for any floor read — floor reads use floor_db.env ($0 Postgres). Never conflate the two env files.
P3. Do NOT grade Sonnet's output yourself by vibes. Grade against the KNOWN-GOOD Opus catalog on the SPECIFIC dimensions in STEP 4. If you find yourself softening a difference to make the cheaper model look acceptable, STOP — report the difference raw and let OC rule.
P4. Disk over memory. The known-good Opus catalog and the payload must be CONFIRMED on disk before firing. If either is absent, STOP and report — do NOT fabricate a comparison or substitute a different conv without flagging it.
P5. Do NOT claim "approved/verified/matches" unless it literally does against the criteria. This test's whole value is an honest match/thin verdict.

=== CONTEXT (settled) ===
181 over-ceiling convs are going to the paid batch API. Model choice (Sonnet 4.6 vs Opus 4.8) is a ~40% bill swing ($76 vs $127 batched) and has never been tested. This $0.30 test settles it: does Sonnet hold the reader's quality on the hardest register, or does it run austere / drop fences / flatten TEXTURE? Match → whole batch on Sonnet. Thin → Opus.

=== STEP 1 — CONFIRM THE ANCHOR (read-only, $0) ===
The comparison conv is 01eb6e56-9546-4c91-ab60-0d7ac8ff0a97 (the ADHD/GAD personal-register conv — the highest-stakes register, READ-2 canary).
Confirm on disk, report each:
  a. The known-good Opus catalog for this conv — the node output from the READ-2 run (should be in harvested_nodes/ — find the 01eb6e56 node file). Confirm it exists, report its path + node count (it was reported as 37 nodes, 25M/10F/2T). If it's NOT there or node count differs, STOP and report — do not proceed without the trusted anchor.
  b. The payload for this conv. If 01eb6e56_payload.txt is still on disk in pipeline/s39/, use it. If it was deleted, re-extract it from the floor via floor_extract.py using floor_db.env ($0 — this is a Postgres read, NOT a billing call). Report the payload's byte size (expect ~573,982).
  c. The reader prompt: pipeline/test_call_system_prompt_S32.md (must match Boot_ScopeReader_v4.0). Confirm present, report its char length.
STOP here and report a/b/c before STEP 2 if anything is missing or mismatched.

=== STEP 2 — STAGE THE PAID CALL (do not fire yet) ===
Build the single API call, do NOT send:
  - Endpoint: standard synchronous /v1/messages (one call, synchronous is fine for a single test — NOT the batch endpoint).
  - Model: claude-sonnet-4-6 (Sonnet 4.6). Temperature: 0.
  - System prompt: the FULL contents of pipeline/test_call_system_prompt_S32.md (the toolless deterministic reader — this is the API path, NO tools attached to the call; blindness by absence, the payload is INPUT not a file to read).
  - User content: the full 01eb6e56 payload (the ~574K-char text) as embedded input. (The API 1M input window handles this — this is the whole structural point: payload in as input, small catalog out.)
  - max_tokens: enough for the catalog output (the Opus run produced 37 nodes; set generous headroom, e.g. 16000).
Report: the assembled call's shape (model, temp, system-prompt length, input char count, max_tokens) and the rough input-token estimate. Confirm anthropic_billing.env will be loaded ONLY for the send. STOP and show me the staged call before firing if you want a check — otherwise proceed to STEP 3.

=== STEP 3 — FIRE (the one paid call, ~$0.30) ===
Load anthropic_billing.env, send the single synchronous call, capture the full response. Report actual token usage from the API response (input tokens, output tokens) and the literal node catalog returned. Then UNLOAD/clear the billing key from the environment so it isn't hot for anything after.

=== STEP 4 — GRADE (the honest comparison) ===
Compare Sonnet's catalog against the known-good Opus catalog on these specific dimensions. Report each as MATCH / THIN / DIVERGENT with evidence:
  1. NODE DENSITY — Sonnet's node count vs Opus's 37. Materially fewer = THIN (austere bug surfacing).
  2. FENCE FIDELITY — did Sonnet produce the same FENCEs, especially the load-bearing ones: the ADHD/GAD mental-health FENCE with a checkable predicate (Opus NODE 2), the body-scaffolding/med-timing FENCE (Opus NODE 3), the Cypher-retrospective FENCE (Opus NODE 26)? Missing or de-fenced (downgraded to plain mention) = the critical failure.
  3. TEXTURE on the personal register — did Sonnet hold TEXTURE on the vulnerability-under-productivity moment (Opus NODE 37: "3 Adderall reminders, 0 lunch prompts, 1 late nap")? Flattening this to generic MOTION is the exact thing that makes a cheap model unfit for THIS apparatus.
  4. STRUCTURAL MARKERS — anchor_msg correctness, conv_uuid integrity, predicate quality on fences. Cosmetic typos (like the fb/ff span-block typo Opus had) don't count against either — judge substance.
  5. CROSS-REFS — did Sonnet preserve the cross-session UUID pointer Opus caught (NODE 35)?

=== VERDICT ===
One line: "MATCH — Sonnet holds the register, run the 181-batch on Sonnet (~$76)" OR "THIN/DIVERGENT on [dimension] — Opus required (~$127)." Include the measured token cost of this one call so OC can true-up the batch estimate from real numbers, not S33's projection.

Report cost paid. Confirm billing key unloaded at end. Confirm no other paid calls fired.

---

STEP 1 CONFIRMED (2026-06-06):
  a. Opus catalog: c:\claude-reference\harvested_nodes\01eb6e56-9546-4c91-ab60-0d7ac8ff0a97.md — 37 nodes (25M, 8F, 2T) ✓
  b. Payload: c:\claude-reference\pipeline\s39\01eb6e56-9546-4c91-ab60-0d7ac8ff0a97_payload.txt — 573,982 bytes ✓
  c. Reader prompt: c:\claude-reference\pipeline\test_call_system_prompt_S32.md — 8,427 chars ✓
Re-run: max_tokens=24000, save-before-print UTF-8, prior attempt cost $0.78 truncated+lost.
