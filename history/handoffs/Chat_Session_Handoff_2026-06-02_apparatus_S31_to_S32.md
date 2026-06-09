# Chat Session Handoff — apparatus S31 → S32
*authored 2026-06-02 by OC (S31, "Quartermaster"). Read this AFTER the boot canon (ANCHOR, Progenitor, Boot_ScopeReader) and BEFORE acting. NOTE: the on-disk canon is STALE in a specific, known way — see §2 and §7. This handoff supersedes the on-disk ANCHOR banner where they conflict; the banner was not re-cut this session, on purpose.*

**ONE-LINE STATE:** S31 ran the lean-kit (doctrine-diet + fence-anchor-split) experiment on the agentic CC readers, it failed the conv-heavy slices the same way prior runs did, and in diagnosing why we established that the real path is **NOT agentic readers at all** — it is a deterministic **Claude-API pipeline, one conversation per call, on the 1M-token context window.** No floor mutation. No canon pushed. The canon re-cut is OWED and deliberately deferred to S32-after-the-test (do not author it on an unconfirmed design — that was S30's turn-12 mistake).

---

## §0 — FAILURE-MODE GUARD (rule-4 still SUSPENDED this stretch)
Jake's standing call holds: **if something feels off, surface it — do NOT inherit it.** S31 reversed two of its own mid-session conclusions when data contradicted them (see §3). That is the correct behavior, not thrash. Specifically:
1. **Do not author canon on an unconfirmed design.** The whole point of deferring the re-cut to after the S32 test call is to not repeat the turn-12-staged-canon error (enshrining a theory the next run falsifies).
2. **Surface turn count every reply** (counts UP, session age).
3. **The API-pipeline decision is well-supported but the ground-truth test has NOT been run.** Hold it as "the path, pending one confirming call," not "proven."

---

## §1 — WHERE THINGS STAND
- **Floor:** laid, immutable, 325 hdr / 24,138 msg. UNTOUCHED this session. Not OC's to mutate.
- **Retrieval-layer seeding (shape pass):** still the active front. The agentic-CC-reader delivery mechanism is being RETIRED (see §2/§3). The doctrine/bar is SOUND and unchanged (proven — see §4).
- **What S31 did:** authored a lean experimental reader kit (`Boot_ScopeReader_lean_v3.0.md`, in `C:\context-pass\`), restaged slice_01–10 with it (old doctrine loadout removed from the dirs, lean kit + spans + settings only), and fired all 10. Results in §3.
- **41 reader dirs** at `c:\context-pass` still exist; slice_00 + 11–40 (31 dirs) still unfired and now likely moot (we're changing delivery).

---

## §2 — THE SLICE-9 MEASUREMENT THAT REORDERED EVERYTHING (settled, do not re-run)
S31's first move was the pending slice-9 strip measurement. **Result: stripping recovered only 0.6% of slice 9** (62.6 KB of bash-echo out of 10.3 MB). **The whale (95.8% echo) does NOT generalize.** A normal slice's mass is REAL content — thinking, text, long technical exchanges, code deliveries — not strippable echo.

Consequences, all confirmed by the measurement:
- **Stripping is NOT the fix for the general case.** The handoff-§3 lever #1 ("strip makes files fit") is INOPERATIVE on normal slices. This kills the whale-rule-generalized plan.
- **5 of slice-9's 10 conversations individually overflow a 200k window.** Largest single conv `d6e23963` = ~624k tokens (stripped) / 56 msgs. Median conv ~280k tokens. The unit-of-work problem is at the **conversation** level, not the slice level.
- **The real constraint is the context window vs. conversation size** — and that's what makes the 1M window (§5) the actual lever, not stripping.

---

## §3 — THE LEAN-KIT EXPERIMENT + WHAT IT PROVED (settled)
S31 built `Boot_ScopeReader_lean_v3.0` implementing two levers the S30 post-mortems pointed at:
- **Lever A — doctrine diet:** reader loads ONLY the lean kit + its slice (no Progenitor/JAKE-STACK/JAKE-RULES held hot; the ~40-line bar folded in). Kills the universal ~700–1,036-line resident tax.
- **Lever B — fence-anchor split:** Pass 1 lays all nodes in one read, flags uncertain fence anchors `ANCHOR_TODO`, never re-reads; Pass 2 pins only the flagged fences by targeted lookup.

**Fired all 10. Result: same three-population pattern as prior runs.**
- **FINISHED:** slice 2, 3, 4, 6, 8 (structurally simple — slice 4 = the lone whale conv; 6/8 = few short convs).
- **COMPACTED:** slice 1, 5, 7, 9, 10 (conv-COUNT-heavy multi-conversation slices; some looped).

**What this proves (and what it doesn't):**
- The diet did NOT rescue the conv-heavy slices. Slice 1 (previously the cleanest, the worst-behaved-yet-survived reader) compacted under the lean kit — possibly got WORSE.
- **TWO S31 self-reversals, both correct, both data-driven:** (a) I started to pivot "it's all size, go to chunking" at turn 12 — then slice 4 (the WHALE, biggest file) FINISHED while small multi-conv slices died, which falsifies "pure size." (b) I suspected my own Pass-2 design doubled reads and caused the deaths — but the finisher OUTPUTS show survivors' Pass 2 was a near-no-op (slice 3: 1 pin; slice 6: 0 pins), so Pass 2 is not inherently a killer. The honest read: the agentic method is **fragile on conv-count-heavy slices** (nondeterministic cumulative inflation), not broken in one nameable spot.
- **The decisive realization:** we kept trying to make an AUTONOMOUS agent behave. Every failure is the agent inflating its own context through choices we can't see or control. The fix is to stop using an autonomous agent and **control the input directly** — which is the API pipeline (§5).

---

## §4 — THE BAR IS SOUND (proven; do NOT relitigate the doctrine)
The two finisher outputs (`nodes_output_slice03.md`, `nodes_output_slice06.md` — Jake has them; they are the FORMAT SPEC for §5) are REAL, high-quality node catalogs:
- slice 3: 18 nodes / 8 convs (12 MOTION, 5 FENCE, 0 TEXTURE, 0 drops).
- slice 6: 30 nodes / 7 convs (fence-heavy).
- Every locator has a real msg_uuid. Fences carry proper why-chains + live predicates ("verify unsubscribe.js deployed"). Keywords are search-oriented. Named-continuity tokens honest. Fences caught are exactly the load-bearing kind (gmail.readonly→v2; scouts-ref-is-on-Members-not-Scouts; 1-click-warm-2-clicks-hot).
- **NOT thin soft-compaction output.** The bar (default-NODE, Progenitor §3, the lean kit's folded version) produces correct results when the reader survives. **The doctrine was never the problem. The delivery mechanism was.** Do not reopen the bar.

---

## §5 — THE PATH: DETERMINISTIC CLAUDE-API PIPELINE (the S32 build, pending one test)
**Architecture (well-supported, NOT yet ground-truth-tested):**
1. Script walks the floor, **one conversation at a time** (the conversation, not the slice, is the unit).
2. Light echo-strip (cheap, deterministic, code-side — drops confirmed bash/file-cat/base64 payloads; on a normal conv this recovers ~0.6%, on the whale ~95.8% — either way free).
3. Token-count the stripped conv. Under ~900k (output headroom) → send WHOLE to one **Opus API call with the 1M-token beta header**, system prompt = the ~40-line bar + "produce output in EXACTLY this format" + a one-shot example block lifted from the slice_03 finisher. Over 900k after strip → that conv goes to a chunker (the rare-monster edge case; slice-9 data suggests this list is short, maybe just the true whale).
4. Model returns the node block. **No Pass 1 / Pass 2** — a deterministic single call doesn't re-read, so the fence-anchor-split is free by construction; the script can locate fence anchors in code (regex/string-match over the conv it already holds) and hand the model candidates if needed.

**Why this folds A+B+C into one clean thing:**
- Lever A (no doctrine-hot): the bar is in the system prompt, ~40 lines, all that's resident. Free.
- Lever B (no anchor re-reads): no agent, no re-reads. Free.
- Lever C (size): the 1M window holds the worst conv we measured (624k) WHOLE. Chunking shrinks to a rare edge case instead of the core problem.
- Determinism: same input → same behavior. No reader-to-reader variance (the thing that made S28–S31 feel like chasing ghosts). Pre-flight token count replaces the lost human blue-line / soft-compaction catch.

**The 1M window is REAL and current (verified S31 against Anthropic docs):** Opus 4.6 / 4.7 / 4.8 and Sonnet 4.6 have a 1M-token context window on the Claude API (GA since 2026-03-13, standard pricing, enabled via a beta header). The standard window is 200k; the beta header unlocks 1M. This is what makes the whole path work — it is NOT "the same 200k wall as a CC window" (Quartermaster initially said that; it was WRONG, corrected against docs).

**Caveats to test, not assume:**
- **Context rot:** a 624k single call may lay thinner nodes at the FAR END than the start (long-context retrieval degrades even when it fits). Opus scores ~76% on MRCR v2 — strong, not perfect. The test call must check tail-quality, not just "did it run."
- **Cost:** 600k-token calls cost real money per call; confirm Jake's tier/rate before firing 325 of them.

---

## §6 — S32 MOVES (in order)
1. **Anchor + confirm canon by content.** NOTE: on-disk ANCHOR is v23 and is STALE (built on dead prompt-vagueness + dead strip-generalization theories). This handoff supersedes it. Do not inherit the v23 banner's root-cause story.
2. **Confirm the 1M beta header works on an Opus model string on Jake's API account.** (Jake's check — cheap. Possibly already answered in the turn-1 paste.)
3. **FIRE THE GROUND-TRUTH TEST CALL — this is the gate for the whole build.** One conversation, whole, via the API, 1M beta header, the §5 system prompt (bar + format spec + slice_03 one-shot example). **Recommended guinea pig: `d6e23963` (slice 9's 624k-token worst case)** — if the worst case works, everything downhill works. Read the result and judge: (a) did it fit + run; (b) does output quality match the slice_03/06 finishers; (c) **does the TAIL of the conversation get noded as well as the head** (the context-rot check). Read this in a FRESH context — it's a big output (≈ a third finisher file); Quartermaster deferred it precisely because reading it at S31's full context would have blown the budget.
4. **Branch on the test:** clean throughout → build the pipeline. Tail-degrades → find the real per-call ceiling now (cheaply, on this one call) and set the chunk threshold below it; chunking re-enters as a real component for convs above the ceiling.
5. **Build the pipeline** (§5) — script + strip + token-gate + API call + format-locked output. Canary it on a few known convs (the slice_03/06 convs we have human-grade answers for) before running the full 325.
6. **THEN re-cut canon on the CONFIRMED design** (the owed task — see §7).
7. Run the full corpus → fence-synthesis (Reconciliation 1) → texture pass → cluster-validation (Reconciliation 2) → Judge. (The downstream pipeline shape is unchanged; only the shape-READER delivery changed.)

---

## §7 — CANON STATUS (HARD HOLD — re-cut is OWED, deferred ON PURPOSE)
The on-disk canon (ANCHOR v23, Boot_ScopeReader v2.3, Progenitor §0.5 S30 augment) is STALE in these specific ways, ALL to be corrected in the S32 re-cut AFTER the test call confirms the design:
- **The compaction root cause** the v23 banner gives (prompt-vagueness / method-vs-bar) is DEAD. The real story: agentic readers inflate context nondeterministically (doctrine-hot + anchor re-reads + cumulative load); the fix is to STOP using agentic readers, not to tune their prompts.
- **The byte→token correction:** the constraint is the context window in TOKENS vs. conversation size, not slice MB. The "~10MB ceiling" / "~20MB compaction edge" figures are wrong.
- **The whale-rule-generalized plan is DEAD:** stripping recovers ~0.6% on a normal slice (slice-9 measurement). The fat is content, not echo. Do not enshrine "strip every conv to fit."
- **The delivery architecture:** agentic CC-window readers → deterministic Claude-API one-conv-per-call on the 1M window.
- **DO NOT author this canon until the S32 test call confirms the API path holds.** Authoring it now would enshrine an untested architecture — the exact turn-12-staged-canon mistake from S30. The re-cut is move #6, after the test, not before.

The S31 lean kit (`Boot_ScopeReader_lean_v3.0.md`) stays on disk as a tested artifact / record of what was tried; it is not the path forward (it was the last agentic attempt).

---

## §8 — DO-NOT-RELITIGATE (settled S31; rule-4 suspended — surface if it feels off)
- Stripping is NOT the general fix (0.6% on a normal slice — slice-9 measured). The whale was an outlier.
- The constraint is context-window-tokens vs. conversation-size, not slice MB.
- The conversation (not the slice) is the unit of work.
- The API 1M window is real (Opus, beta header) and is 5× a standard window — it fits the 624k worst conv whole.
- Agentic CC-window readers are RETIRED as the shape-reader delivery (fragile/nondeterministic on conv-heavy slices — proven across S30 + S31).
- The doctrine/bar is SOUND (finisher outputs prove it). Do not reopen default-NODE, the two kinds, §3.3, the walls.
- The two finisher outputs (slice_03, slice_06) are the OUTPUT-FORMAT SPEC for the API prompt.
- Floor laid + immutable; no quarantine on personal material; the downstream two-pass→reconciliation→Judge geometry is unchanged.

## §9 — REMEMBER WHAT THIS IS
Jake's auxiliary brain, beta 1.0 — the breadth IS the function. The whole S28→S31 fight was INFRASTRUCTURE (getting a reader to fit the window); the goal underneath is unchanged — a catalog comprehensive enough that a fresh Claude lands in the right neighborhood of Jake's recorded life instead of confidently blind. The API pipeline is just a cleaner way to get there: stop fighting an agent's behavior, control the input, let the model read what it's handed. The bar already works. Build the deterministic delivery and the rest follows.

Status line every reply: turn N · ET-time (TZ=America/New_York) · re-anchor X (counts UP) · dest; state; next.

Brothers. Grind. Evolve. Dominate.
