# Chat Session Handoff — apparatus S45 → S46
*authored 2026-06-07 by S45 OC "Cinder" · primary state input for S46 · the disk wins over this doc where they conflict, but this is NEWER than the ANCHOR*

---

## READ THIS FIRST — THE ONE THING S46 MUST KNOW

**The 181-conv paid batch is COLLECTED, PERSISTED, and DONE.** The corpus read's heavy lifting is finished. Final result of the S45 recovery collect:

```
PERSISTED 177  TRUNCATED 0  ERRORED 0  QUARANTINED 4
177 + 4 = 181 ✓  (full batch accounted for)
```

**`harvested_nodes/` now holds 177 clean reads from this batch** (plus the 8 banked-good cold-store, 14 free, 130 whales — the merge in move #1 below). **4 convs are QUARANTINED** for inspection (catalogs preserved, not lost, not re-read yet) — that is the **first real work of S46**.

**No more batch spend is coming** unless S46 chooses to re-fire the 4 (trivial cost — 4 calls, ~cents to a couple dollars, not a batch). Total spend to date for the whole 181 read: **$37.xx — UNDER the $48–65 estimate.**

---

## WHAT S45 "CINDER" DID (the narrative, in order)

S45 inherited a batch that had completed clean server-side (181 succeeded, 0 errored) but whose **persist phase had CRASHED** in S44 on conv `567956f0` — the `persist_node_file()` integrity guard correctly caught a hallucinated anchor and raised, which (in the v1.1 harness) killed the entire persist loop. 53 convs had persisted before the crash; ~128 good reads were stranded behind the one poison-pill conv. S45 recovered all of it for $0 of new batch spend.

**The state correction (disk beat the handoff).** The S44→S45 handoff's "READ THIS FIRST" optimistically assumed the batch might just need a verification collect. The committed `batch_run_S44.log` on HEAD told the real story: batch `status=ended` clean, but the persist traceback showed it HALTed mid-loop. Jake confirmed the live disk: 53 persisted this run / 61 total `.md` / 39 sidecars / `567956f0` absent / 128 + the poison-pill un-persisted. The log fragment said 26; the live disk said 53 — **disk won.**

**Move 1 — the v1.2 patch (resilient persist + quarantine).** The defect was diagnosed precisely: *the guard is correct, the blast radius is wrong.* A single bad conv should not be able to strand the whole batch. Fix authored (OC) and applied (CC, fresh PowerShell window, separate from the old crashed VSC window per Jake): `persist_results()` now wraps the per-conv `persist_node_file()` call in try/except — a guard trip writes the conv's scrubbed catalog to `pipeline/s39/quarantine/<uuid>.quarantined.md`, records the conv_uuid + error, and **continues** the loop. The guard in `pipeline_guards.py` is **UNCHANGED** — it still raises hard; only the caller absorbs the raise. Committed `43eb65e`. Harness v1.1 → v1.2.

**Move 2 — CAUGHT A RE-SPEND TRAP (CC flagged it; OC's recovery instruction was wrong).** OC's plan said "re-run the `batch` command, it re-collects for $0." **It does not.** The `batch` subcommand ALWAYS calls `submit_batch` first — running it would have fired a FRESH PAID batch for the ~128 un-persisted convs (~$40+ wasted, plus a second batch-id to reconcile). CC read the actual code path and caught it before any spend. *(Lesson, logged: OC asserted code behavior from memory instead of verifying; the disk-over-memory rule applies to OC's read of the harness too. CC's code-path read is authority over OC's recollection.)*

**Move 3 — the v1.3 patch (the `collect` subcommand — the missing re-entry point).** The real root issue was architectural: submit-a-batch and collect-an-already-completed-batch are two different operations, and the harness conflated them. OC authored an additive `collect --batch-id` subcommand: rebuilds `parents_by_conv` $0 from the floor (key unloaded), fetches the completed results via the existing `poll_and_collect_guarded` (key loaded for the fetch only, cleared after), hands to the v1.2 resilient `persist_results`. **No submit, no model calls, no new spend.** Reuses existing functions; `submit_batch` is verified absent from the collect path (only at def line 169 + the `run()` call at 251). CC added a defensive `missing`-parents skip guard (improvement over spec). Committed `67b9a97`. Harness v1.2 → v1.3. **Verified on HEAD by direct read at handoff time.**

**Move 4 — THE RECOVERY COLLECT ($0): SUCCESS.** `collect --batch-id msgbatch_0149uvXSVYmrWhGhvSHBGHn5 --i-understand-this-spends-money` (the flag is required by the code path but the collect of a completed batch is $0 — it cannot submit). Re-fetched all 181 results from the existing server-side batch (**proved the cross-window re-collect works** — the one step OC couldn't vouch for from experience; the old VSC window was held as a fallback and was not needed). Persisted 177 clean, quarantined 4, 0 truncated, 0 errored. The 53 previously-persisted re-persisted identically (atomic replace, harmless).

---

## STATE FACTS (carry into S46)

1. **THE 181 READ IS DONE: 177 PERSISTED CLEAN + 4 QUARANTINED.** `harvested_nodes/` holds the 177. The 4 quarantined catalogs are in `pipeline/s39/quarantine/` (gitignored — local-only, won't show on HEAD).

2. **THE 4 QUARANTINED CONVS (the first S46 work):**
   - `567956f0` — ANCHOR NOT IN PARENTS MAP (`019ce155-...-e5e5e5e5e5e6`, synthetic-looking) — the original S44 poison-pill.
   - `e49e2627` — ANCHOR NOT IN PARENTS MAP (`019d0124-a3de-75d3-a9c0-94dc2be913be`).
   - `20e2e718` — ANCHOR NOT IN PARENTS MAP (`019ca434-e412-71bf-ab6b-4e1033f15f2`).
   - `68c3fe4c` — STUB DETECTED (came back empty/below the stub floor — a different failure class from the 3 hallucinated-anchor trips).
   **~2% defect rate (4/181).** 3 of 4 are reader-hallucinated pointers (same class as `01eb6e56` from S44); 1 is a stub.

3. **THE GUARD IS WORKING AS DESIGNED.** All 4 trips were caught before any bad pointer entered the pile. The v1.2 resilient loop is now PROVEN — it caught 4 real trips and continued through all of them. (The 3 trips beyond `567956f0` were stranded behind it in S44 and would have killed the v1.1 run one-by-one regardless.)

4. **HARNESS IS v1.3 ON HEAD AND CORRECT.** `pipeline/apparatus_batch_read.py`: subcommands dry-run / canary / batch / **collect**. The `collect` path is the $0 re-entry for any completed batch-id. Guard (`pipeline_guards.py`) unchanged + correct.

5. **FLOOR IS THE FROZEN MAY-25 BASELINE — ON PURPOSE.** Unchanged. Immortal (325 headers / 24,138 messages).

6. **TWO-BATCH DELTA DECISION STANDS (Jake's S44 strategic call).** The ~2 weeks / ~50 sessions of post-May-25 work come in as a SEPARATE later delta pass (delta-freeze → delta-worklist → delta-batch → merge additively). Rationale unchanged: batch cost is per-request flat 50%-off (split vs combined = identical dollars), and splitting hedges method drift (batch #1 catches up to batch #2 on only the stale subset, never a full refire). This is move #3 below.

7. **TOTAL SPEND $37.xx, UNDER ESTIMATE.** The whole 181 read came in below the $48–65 band. The S45 recovery added $0. Only possible further cost: a scoped re-read of the 4 (trivial).

---

## WHERE THE LIVE CODE LIVES (named exactly)

- **Harness:** `pipeline/apparatus_batch_read.py` (v1.3 — dry-run/canary/batch/**collect**; paid paths gated by `--i-understand-this-spends-money`; key loaded submit/collect-only, cleared after; resumability = COMPLETE artifact, not file-exists).
- **The $0 recovery command (for reference):** `python3 pipeline/apparatus_batch_read.py collect --batch-id <msgbatch_...> --i-understand-this-spends-money`
- **Batch-id of the completed 181:** `msgbatch_0149uvXSVYmrWhGhvSHBGHn5` (results retrievable ~29 days from batch end — i.e. through ~early July 2026 — if a re-collect is ever needed again).
- **Frozen paid list:** `pipeline/s39/batch_list_S44.csv` (189 rows; 8 resume-skip, 181 fired).
- **Quarantined catalogs (S46's first input):** `pipeline/s39/quarantine/{567956f0,e49e2627,20e2e718,68c3fe4c}.quarantined.md` (gitignored, local-only).
- **Deployable reader (v4.1.1):** `pipeline/test_call_system_prompt_S40.md`. Reference twin: `apparatus/Boot_ScopeReader_v4.1_2026-06-06.md` (HAND-SYNCED — patch both together).
- **Guards / scrub:** `pipeline/pipeline_guards.py` (unchanged), `pipeline/scrub_output.py`.
- **The flat pile:** `harvested_nodes/` (gitignored, local-only).
- **Hoth archive (off-tree):** `C:\apparatus-hoth-storage\harvest-storage\` — holds the bad S44 `01eb6e56`.

---

## S46 MOVES, IN ORDER

0. **★ STATE RECONCILE ($0).** Cache-busted re-pull. Confirm HEAD carries v1.3 (`grep "version: v1.3"` + `def collect_batch`), commits `43eb65e` + `67b9a97` landed. Confirm on the live disk (via CC): `harvested_nodes/*.md` count (expect 177 from this batch + the banked) and `pipeline/s39/quarantine/` holds the 4. Disk over this doc.

1. **★ TRIAGE THE 4 QUARANTINED (the deferred S45 decision — Jake's go-forward idea TBD, he tabled it to S46).** Re-running them is trivial cost, BUT 3 of 4 are reader-hallucinated pointers — a blind re-fire just re-rolls the hallucination dice. **OC's standing recommendation: READ the 4 saved catalogs first** (they're already on disk, $0 to inspect) to see *why* each tripped before deciding re-fire-vs-hand-correct-vs-investigate. The stub (`68c3fe4c`) is likely a different fix than the 3 anchor trips. Possible per-conv outcomes: hand-correct the anchor against the floor (if the bad pointer is isolated + the rest is good), scoped re-fire (if the read is broadly poisoned), or investigate a reader tic worth knowing before the delta batch. **Jake has a go-forward idea — get it from him first.**

2. **MERGE the pile.** 177 paid-clean + 8 banked-good cold-store + 14 free + 130 whales → the flat pointer pile. Confirm no conv_uuid collisions; additive. (Fold in any of the 4 that triage rescues.)

3. **★ THE DELTA PASS (state fact #6).** Delta-freeze the ~2 weeks of post-May-25 sessions (append-only, new snapshot) → delta worklist → delta batch through the SAME harness (note if the reader's improved to v-next, batch #1 may need a scoped catch-up) → merge additively.

4. **DOWNSTREAM (unchanged):** fence-synthesis (Recon 1) → texture/volume → cluster-validation (Recon 2) → the Judge → retrieval engine (Progenitor §10–§11). Runs on the merged pile regardless of entry time. Author the Progenitor §12/§13 carry-forwards on the CONFIRMED pipeline. Fix the dangling `Boot_ScopeReader.md` ref → `Boot_ScopeReader_v4.1`.

5. **CANON HYGIENE (end-of-project, not mid-flight):** RECUT THE ANCHOR v31 → v32 — reconcile to confirmed batch reality (the dead 206/205 banner number → 181 fired / 177 persisted / 4 quarantined; the S44 canary + S45 recovery recorded; two-batch delta plan). The `pipeline/` git-mv scratch cleanup; dead-branch `s33-whale-path` deletion; reader-twin single-source consolidation; CHANGELOG lines for harness v1.2 + v1.3.

---

## ★ STANDING LESSONS (S45 carry-forward, additive to S44's)

- **The guard is right; make the CALLER resilient, never the guard permissive.** A load-bearing integrity guard (`persist_node_file`) should keep raising hard — other callers (canary, future delta) rely on it halting. The fix for "one bad item kills the batch" is a resilient *loop* that quarantines-and-continues, not a softened guard. (§10 "the guard fires for real" stays intact.)
- **OC's read of the code is memory, and memory loses to disk.** OC asserted the `batch` subcommand re-collects; it submits. CC read the actual path and caught a ~$40 re-spend trap. The disk-over-memory rule (§5.4) applies to OC's recollection of the harness's behavior exactly as it applies to a stale handoff. **Verify the code path before instructing a paid run against it.**
- **Submit and collect are two operations — don't conflate them in a batch tool.** A tool that can only ever re-enter via "submit first" has no safe crash-recovery path. The `collect --batch-id` subcommand is the re-entry point; it cannot spend.
- **Archive/preserve-don't-discard, applied to bad reads too.** The quarantine writes the paid-for catalog to disk before setting the conv aside — the read was paid for; throwing the text away would mean re-collecting to inspect it. Inspect-then-decide beats blind-re-fire, especially for hallucination-class trips where a re-roll may just hallucinate differently.
- **Keep the crashed window as a warm fallback until the recovery is PROVEN.** The cross-window re-collect was documented-to-work but not seen-to-work here; holding the original instance cost nothing and was the hedge against the one unproven step. (It worked; the hedge wasn't needed — but holding it was correct.)
- **Match the register to the operator (the hardest-earned S45 lesson).** Jake is a non-coder architect with a working-memory rewire in progress (§1.2) AND his streaming output tool was broken this session (one word → 10s hang → wall-of-text dump). Long, jargon-dense, code-heavy replies were actively harmful under those conditions — he can't skim as it streams, then gets buried. **Plain language, short, ordered, one-action-at-a-time. Code is "paste this into CC, don't read it" — never "understand this."** OC holds the state and the details; Jake holds the direction. Handing Jake the technical detail is backwards — it's the exact thing the external-buffer is *for*. (Jake flagged this mid-session; correction landed; do not re-drift.)

---

## REMEMBER WHAT THIS IS

Jake's auxiliary brain, beta 1.0 — the breadth IS the function. S45 took a crashed, stranded batch and brought all 181 reads home for $0 of new spend, through a fix that made the pipe resilient instead of brittle and a re-entry point that made crash-recovery free. 177 clean, 4 set aside honestly rather than forced. The guard caught every bad pointer; the loop no longer dies on the first one. The number stayed honest because we read the disk instead of trusting the log, and the spend came in under estimate. The defect rate is ~2% and every defective read is preserved for a real look, not papered over. That's the project working: it fails loud, preserves everything, and gets more reliable each pass.

Grind. Evolve. Dominate.

— S45 OC "Cinder", 2026-06-07. Signed in the lineage. Be worth it.

Status line ending each reply: turn N · ET-time · re-anchor X/4 · dest; state; next.
