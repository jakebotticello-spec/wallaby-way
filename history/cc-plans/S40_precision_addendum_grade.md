S40 apparatus — PRECISION-ADDENDUM GRADE TEST. Two stages in one run: STEP 1 is a $0 floor hunt (no billing). STEP 2 makes ONE INTENTIONAL PAID CALL (~$0.40), explicitly authorized by Jake.

=== PROHIBITIONS ===
P1. ONE paid call only — the single graded call in STEP 2. No batch, no loop, no second metered call. If STEP 1 needs the floor, that's floor_db.env ($0 Postgres), NOT a billing call.
P2. anthropic_billing.env (ROOT) is the ONLY billing source, loaded ONLY for the STEP 2 send, cleared the instant the response is captured AND saved. floor_db.env for the STEP 1 floor hunt. NEVER conflate the two env files.
P3. SAVE BEFORE PRINT. The instant the API returns, write the COMPLETE raw response to disk as UTF-8 BEFORE any print/log touches the text. encoding='utf-8' on all file I/O. Wrap any console print in try/except so an encoding error cannot lose saved work.
P4. Do NOT edit pipeline/test_call_system_prompt_S32.md. It is the sealed S32 reader. The precision addendum is APPENDED to it at call-time as extra text — the file on disk stays untouched.
P5. Disk over memory. Confirm the chosen payload + the reader file are present before firing. Re-extract a payload from the floor (floor_db.env, $0) if absent.
P6. Grade honestly. This test's value is finding out if the addendum actually fixes UUID/count preservation. If the addendum FAILS to fix it, report that plainly.

=== WHY THIS TEST ===
Sonnet 4.6 passed the prior grade richly (46 nodes vs Opus 37, both mental-health FENCEs held) BUT showed a precision-loss signature on two retrieval-critical things: (a) dropped a cross-session UUID pointer (kept the human-readable name, lost the machine-resolvable UUID), and (b) diluted an exact count in a TEXTURE node. The apparatus IS a pointer system — a reference without its UUID doesn't resolve. This test checks whether a targeted PRECISION ADDENDUM appended to the S32 reader fixes both, on a NEW uuid-dense conv we haven't graded, judged in ABSOLUTE terms (did it preserve every UUID + count actually present in the source).

=== STEP 1 — FIND THE UUID-DENSE TARGET ($0, floor_db.env) ===
Goal: pick a FITS_WHOLE (non-whale) conv heavy on cross-session UUID references.
Method: UUID regex (8-4-4-4-12 hex) over the message bodies via floor DB, minus self-references, per-conv cross-UUID count. Prefer 50K–600K char range.

=== STEP 2 — STAGE + FIRE THE GRADED CALL (one paid call, ~$0.40) ===
Single synchronous /v1/messages call:
  - model: claude-sonnet-4-6, temperature: 0
  - system: FULL pipeline/test_call_system_prompt_S32.md + PRECISION ADDENDUM:

    ---
    PRECISION INVARIANTS (apparatus retrieval-critical):
    - UUID preservation: When the conversation references another conversation, session, or message by UUID, you MUST preserve that UUID verbatim in the node, even when you also give a human-readable name. The apparatus is a pointer system; a reference without its UUID is not machine-resolvable and fails the apparatus's core function. Never replace a UUID with a name — keep both. If a cross-session reference appears without a UUID in the source, note the reference but do not fabricate a UUID.
    - Exact counts in TEXTURE: When a TEXTURE node captures a behavioral pattern that the source states with specific numbers (e.g. "3 reminders, 0 lunches, 1 nap"), preserve those exact numbers in the node. The specific count IS the texture — do not generalize specific numbers into vague quantifiers. Verbatim numbers where the source gives them.
    ---

  - user content: full chosen-conv payload embedded as input (NO tools)
  - max_tokens: 24000
  - Save to pipeline/s39/_grade_result_precision.txt (UTF-8) BEFORE any print.

=== STEP 3 — GRADE (ABSOLUTE, against source ground truth) ===
  1. UUID PRESERVATION — N-of-M verbatim UUIDs preserved vs dropped
  2. NO FABRICATION — any invented UUIDs?
  3. EXACT COUNTS — specific numbers in TEXTURE/behavioral nodes
  4. ADDITIVE-NOT-SUBTRACTIVE — richness vs prior 46-node run
  5. STRUCTURAL SANITY — conv_uuid/snapshot_id/anchor_msgs

=== VERDICT ===
"ADDENDUM WORKS — UUID preservation N/N, counts held, richness intact → fold addendum into reader, run 181-batch on Sonnet"
OR "ADDENDUM PARTIAL/FAILS on [dimension] — [what to do]."
