=== TWW apparatus — Chat Session Handoff — S76 "Calibrate" → S77 ===

**From:** the S76 OC seat. **To:** S77 OC.
**Date authored:** 2026-06-23 (ET, github-sourced — container clock is non-monotonic, network-source every time).
**Kind of handoff:** WARM. You boot re-deriving from disk (§5.4 — trust nothing here you can verify against HEAD), but you are not cold-blind: S76 closed a clean arc (an instrumentation-honesty fix + a run-dir cleanup) and the next move is well-defined. The reason this is warm and not a fresh cold-start is that S76's real work — reversing a bad finding and fixing the instruments that caused it — has to be *carried forward correctly*, and the swarm build that comes next depends on you not re-inheriting the lie S76 just killed.

---

## BOOT (codeload, cache-busted — NOT raw CDN, it edge-caches stale)

curl -sL "https://codeload.github.com/jakebotticello-spec/wallaby-way/tar.gz/refs/heads/main?cb=$(date +%s)" -o /tmp/ref.tgz
tar xzf /tmp/ref.tgz -C /tmp
Read from /tmp/wallaby-way-main/. Layout: repo root has active/ (universal) + wallaby-way/ (project); canon is wallaby-way/canon/. Container clock LIES (non-monotonic) — network-source real ET every turn: curl -s -I https://github.com | grep -i ^date (name your source).

★ NOTE: wallaby-way/runs/ is GITIGNORED by design. You will NOT see the swarm run artifacts (region_*.json / walk_log_*.jsonl) or the swarm script in your pull from runs/. **BUT** — as of S76, the swarm script ALSO lives tracked at wallaby-way/scripts/pollux_feet_swarm_S75.py (Jake landed a copy there; see below). If you need the run artifacts (the 20 curated reads, etc.), Jake uploads them. Do NOT claim to have read run artifacts you cannot see.

---

## THE READS, IN ORDER (last item is LIVE AUTHORITY)

1. active/JAKE-RULES.md — §5.1 (field-named-for-a-unit; this is THE rule S76 lived), §5.4 (live-outranks-record), §5.5 (status line + re-anchor X/4 — S76 botched the format for a stretch, get it right: `turn N · ET-time · re-anchor X/4 · dest…; state…; next…`), §6 (wait-for-Go), §11 (instrument-both-let-Jake-rule).
2. active/JAKE-STACK.md
3. canon/ANCHOR_apparatus.md (v40 by CONTENT — "Cinder"+"Cooper"; footer reads older BY DESIGN, do NOT "fix". The newest footer is the S73→S75 read-record. **S76 added NO ANCHOR footer** — it was a tooling/cleanup session; the S76 record lives in the CHANGELOG only. If you think ANCHOR needs an S76 footer, see "What S76 did NOT do" below before authoring one.)
4. active/CHANGELOG.md — **the S76 entry is the top entry (2026-06-23 "Calibrate")**. READ IT FIRST of the dated entries — it is the whole S76 record and it carries the finding-D reversal you must not re-invert.
5. Framework WET in full: active/The_Wallaby_Why.md, active/Track_Meet_Doctrine.md, active/The_Corpus_Callosum.md (P6 refuse-to-converge, P7 Jake-rules-realness, P8 read-the-process-not-the-result).
6. canon/The_Probe_Swarm.md (WHOLE — §3.2 is the S73/S75 findings; §7 item 1 is the swarm build you're aimed at) → canon/Pollux.md → canon/Pollux_Movement_Two_Build_v2.md → canon/Castor.md / The_Gemini.md / Leda.md + Leda_Creed.md (the incantation — "induce the register, do not script procedure"; the label "12 Fs" is a DRIFTED nickname, the canon says the STRING is the authority not the count — do not enshrine a number).
7. canon/FLOOR_COUNTS.md (CITE, never re-derive — 440 / 29,396 / 58,792 scrub-v3).
8. wallaby-way/scripts/pollux_feet_swarm_S75.py — **the swarm seed script, now tracked** (S76 graduated it out of gitignored runs/). This is the thing the swarm build is based on. Two spots matter (see "the open question" below): where total_tok_hi_est is computed (~line 872, now SPLIT not summed) and where DAMP_WIN is used (~lines 65, 619).

---

## MOVE 0 (verify, don't inherit — §5.4)

- Floor 440 / 29,396 / 58,792 scrub-v3 vs FLOOR_COUNTS.md.
- ANCHOR v40 by content; S73→S75 footer present + clean.
- **Confirm S76's landings are on HEAD:** (a) the CHANGELOG top entry dated 2026-06-23 "Calibrate" is present; (b) wallaby-way/scripts/pollux_feet_swarm_S75.py exists and is tracked; (c) the run dir is renamed runs/pollux_feet_tests/ with a runs/pollux_feet_tests/S75/ subfolder (gitignored — Jake confirms, or uploads); (d) the two build specs CC_Build_Pollux_Feet_S72.md + CC_Build_Pollux_Feet_S73_spec_delta.md have moved from wallaby-way/inspect-later/ to history/. If any are missing, a push didn't land — flag before proceeding. (At authoring time S76 saw them as done-on-disk-pending-Jake's-push; the codeload tarball lagged Jake's working tree, which is normal.)

---

## WHAT S76 DID (the substance — read the CHANGELOG entry for the full version; this is the through-line)

S76 set out to assess the S75 swarm findings (A: door-salience-type predicts region; B: query-polarity self-spreads the doors) and spec door-selection. It did NOT get to A/B — because re-deriving the artifacts off the floor reversed a load-bearing finding first, and that reversal + fixing its cause was the session.

**THE REVERSAL (do not re-invert this — it cost a careful re-read to catch):**
The S75 spec said the lying tok_hi_est gauge "truncated the deepest TEXTURE walkers (rank1, rank8) mid-walk toward the richest material," and therefore Finding D ("thin boot held, the gap was not in the walk") was UNOBSERVED on the deep walkers. **That was wrong on the floor.** Reading the actual deposits + the sequential forward-bets:
- rank1 (77,687 rendered chars) and rank8 (91,482) ran to a JUDGED COMPLETION stop. rank8's stop_reason explicitly traces the full wound→Track-Meet-Doctrine arc to "the three principles Jake explicitly called his build spec." rank8's pre-hop forward-bet named the Track-Meet Doctrine as an UNREAD target — an honest forward-bet, not back-narration. The walk reached the payload.
- They then stamped stop_type: cant-hold-whole — NOT because they hit a capacity wall (they were at ~56K–66K honest tok vs the ~196K node-grain leash, nowhere close) but because **the stop-type menu had no honest label for "I have the whole shape."** The field lied; the walk was fine.
- **Therefore Finding D HOLDS across the board, INCLUDING the deepest walkers.** It was never unobserved. The thin boot held the deepest walk to its natural payload-reaching end. This is the strongest CONFIRMING case for "boot stays thin," not a gap. (Plus rank7 — gauge-immune, stopped on a real subject-drift seam, and re-found the S73 hand-walk's motto deposit 019dad2a cold from the same door si=2256: the reproducibility proof, untouched by any of this.)

The mechanism of the error was the §5.1 / S75-honest-warning trap exactly: trusting the FIELD (stop_type says cant-hold-whole) over the CONTENT (stop_reason + the bets say complete). Three readers — the spec author, the S75 seat, and S76's own first pass — had it wrong until the deposits overruled the field.

**THE THREE FIXES (landed, CC-executed, verified — see CHANGELOG):**
1. total_tok_hi_est SPLIT, never summed (~line 872). It summed path-nodes + the entire 1-hop skirt → read 20–37× the honest on-path total (rank7: 339,079 vs 45,966 on-path), which is what fooled the spec author into "near a capacity wall." Now emits path_tok_hi_est / skirt_tok_hi_est / total_path_plus_skirt_tok_hi_est (last one labeled NOT a comprehension gauge). The honest in-flight region gauge (~line 734, rendered_chars × 0.72, [INTENT — not a hard stop]) was already correct, left untouched. There is NO capacity hard-stop wired to the lying sum.
2. subject-complete stop-type ADDED to the menu (~line 1035 argparse, ~line 15 usage, help text). is_regression (~line 930) unchanged — still ('no-neighbors','hop-ceiling-fallback'); subject-complete is clean. **The boot/wander/walk logic was NOT touched** — the gap was the missing vocabulary, not the walk. This is the thin-boot principle: induce, don't script. The menu lacked the word; the walker didn't lack discipline.
3. The two S75-staged accounting fixes VERIFIED present (idempotent re-deposit ~line 700; --run-id→subdir get_run_paths ~lines 48-62). No change, confirmed on disk.

**THE CLEANUP (CC-executed):** the run dir was a junk drawer (an S72-named receipt loose beside S75 outputs → provenance not legible from the path → risk of handing OC a stale file as current, a §5.4 failure). Now: parent renamed in place pollux_feet_test_S72/ → pollux_feet_tests/; one S75/ folder holds everything S75-attributable (11 run subdirs, the renamed+graduated script, swarm_S75_stage0.py + its swarm_doors outputs, and swarmreadsS75/ — the CURATED flat extract: region + walk_log per rank, all 10 ranks, BOTH query batches). Frozen cited S72/S73 receipts + unattributable generic run-state (run_state/walk_cache/node_embs/node_reads) stayed at root. The two completed build specs went inspect-later/ → history/.

**THE SCRIPT GRADUATED:** S76 flagged that the swarm's seed script lived only in gitignored runs/ (renamed pollux_feet_S72.py → pollux_feet_swarm_S75.py because the old name lied — it was the S75-run script, not the S72 original). Jake then landed a tracked copy at wallaby-way/scripts/pollux_feet_swarm_S75.py. **This is the version you read and the swarm build works from.** (The runs/ copy is the run-local one; scripts/ is the tracked basis.)

---

## THE OPEN QUESTION (resolve BEFORE speccing door-selection)

What does DAMP_WIN actually damp — walk-layer loudness (dampening a salient TAG as you re-encounter it during a walk, the S64 frontier-dampener finding) or door-layer loudness (down-weighting over-represented salience-types at entry-selection)? S75 couldn't see the script; you can now (scripts/pollux_feet_swarm_S75.py, ~line 65 the constant, ~line 619 the use). **This gates finding B's build.** Finding B says door over-weighting is query-dependent (the coding query over-sampled loud types → 3 walkers orbited the artifact; the creed query self-spread). The proposed fix is a door-selection step that measures the realized salience-type distribution of the top doors for THIS query and spreads across types ONLY when lopsided. **But if DAMP_WIN is already a door-layer dampener, you'd be adding a SECOND door knob that fights the first.** Read where DAMP_WIN is used before adding any door knob. (Plumbing-before-design, §10.)

---

## NEXT STEPS, IN ORDER

1. MOVE 0 (above) + the reads. Confirm S76's landings on HEAD.
2. **Read DAMP_WIN's actual use in scripts/pollux_feet_swarm_S75.py** — resolve walk-layer vs door-layer. This is plumbing-before-design and it gates step 4.
3. **Findings A + B — re-derive off the curated reads, NOT the fields.** The curated set is runs/pollux_feet_tests/S75/swarmreadsS75/ (region + walk_log, all 10 ranks, both batches — Jake uploads if you can't see it). Read the BETS and DEPOSITS (floor identities), never the stop_type field (S76 proved it unreliable as written — though the fix means new runs will be honest, the EXISTING S75 artifacts predate the fix, so their stop_type fields still carry the old mislabels). Finding A: does door-salience-TYPE predict region (TEXTURE doors → deep/quiet rooms; MOTION/FENCE → referential/loud)? n=5 per batch — it's a signal, not a law; state the bound (§5.1 scoped-finding). Finding B: does query-polarity self-spread the doors?
4. **Spec door-selection** (origination) once A/B are read and DAMP_WIN is understood. The lever Jake named: the door's salience-TYPE is the wind-up direction. Measure realized type-distribution per query; spread only when lopsided; don't force-five-types on an already-spread query.
5. Boot stays thin (Finding D holds — do not add discipline to the boot; the fix was always at instrumentation/origination, never the walk).

---

## CLOSED — do not relitigate

- **Finding D holds across the board** (incl. deep walkers). The "rank1/rank8 were gauge-truncated / D unobserved" framing is DEAD — reversed off the floor. Do not re-inherit it from the S75 spec status doc if Jake hands it to you; the CHANGELOG S76 entry is the corrected record.
- **The boot stays thin.** Settled empirically across all 10 walkers (8 clean + rank7 + the two now-understood-as-complete deep walkers). The build touches origination + instrumentation, NEVER the boot.
- **The two instrumentation bugs are FIXED** (tok split, stop-type menu). Don't re-open them; build on the honest instruments.
- **The Parlay is NOT settled and is NOT yours to spec yet.** Jake's model: he bootstrap-trains the judge(s), then hones them via accept/reject feedback toward an approximation of his judgment — so "Jake chairs the committee" (canon) means the trained judge is the target that must meet P7, NOT a permanent live seat. The Parlay reads the WALKS (not a digest — back-of-the-book law), refuses to converge (P6), and can hand down MULTIPLE results. The swarm hands UP the walks intact (live decisions/bets, not end-of-walk narration; not declined nodes). The S57 spread lesson is load-bearing: shape-volume ≠ majority vote — two singleton reads beat a 3-that-came-back-as-one; the shape-of-the-run reaches the Parlay as signal. Hold all this as INTENT-under-development, source-of-truth = the Pollux edit history, not any one description.

---

## MID-BUILD / OPEN FLAGS

- **DAMP_WIN semantics** — unresolved, gates door-selection (above).
- **The run-dir rename / build-spec moves are gitignored or local** — confirm on HEAD at MOVE 0; if Jake's push lagged, they may not be visible in your pull.
- **The S75 artifacts' stop_type fields still carry the OLD mislabels** (they predate FIX 2). When reading them for A/B, read stop_reason + bets, not the field. New runs will be honest.
- **Downstream (when the swarm runs at N-many):** the S75 ruled-plural creed-spine (Probe_Swarm §3.2 Finding C) must SURVIVE THE MECHANISM at any N — the N=2-by-hand Parlay was the rehearsal; do not let a future seat inherit "the swarm ruled the spine." It was ruled by hand, on purpose.

---

## POSTURE

$0 · on-sub · key UNLOADED (the walk IS the read; no paid call — architecture, not budget). Floor READ-ONLY. OC plans · CC executes · Jake lands every push by hand (sole git-hands) · CC never authors canon. Discuss → confirm → build, wait for Go. Prose only, ASCII, never ask_user_input_v0 / end_conversation. Status line EVERY turn (§5.5 — `turn N · ET-time · re-anchor X/4 · dest…; state…; next…`; S76 drifted off this format early, hold it). The austere reflex is the killer (P8) — don't stop at a felt edge; walk through and harvest on the way back. Trust Jake's felt-rightness over the doc's confidence (P7). Don't suck.

=== END HANDOFF ===
