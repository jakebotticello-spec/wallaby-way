=== TWW apparatus — Chat Session Handoff — S77 "Convergence" → S78 ===

**From:** the S77 OC seat. **To:** S78 OC.
**Date authored:** 2026-06-23 (ET, github-sourced — container clock is non-monotonic, network-source every time).
**Kind of handoff:** WARM. You boot re-deriving from disk (§5.4 — trust nothing here you can verify against HEAD), but you are not cold-blind. S77 closed a clean arc: it externalized the swarm script's write-root (fail-loud, so test output stops landing in tracked `scripts/`), and it read the first swarm-spread run off the floor and ruled the door layer needs NO dampener. The next move is one well-defined job — fire 20 probes at the creed query and judge whether the door-layer findings LOCK. The reason this is warm and not cold: the door-layer read (Findings D/E) is one of the two most load-bearing pieces in the whole apparatus, it is currently `[PROVISIONAL]` at n=10, and S78 exists to lock it or break it. You must carry that forward correctly and not inherit it as settled.

---

## BOOT (codeload, cache-busted — NOT raw CDN, it edge-caches stale)

curl -sL "https://codeload.github.com/jakebotticello-spec/wallaby-way/tar.gz/refs/heads/main?cb=$(date +%s)" -o /tmp/ref.tgz
tar xzf /tmp/ref.tgz -C /tmp
Read from /tmp/wallaby-way-main/. Layout: repo root has active/ (universal) + wallaby-way/ (project); canon is wallaby-way/canon/. Container clock LIES (non-monotonic) — network-source real ET every turn: curl -s -I https://github.com | grep -i ^date (name your source).

★ NOTE: wallaby-way/runs/ is GITIGNORED by design. You will NOT see the swarm run artifacts (region_*.json / walk_log_*.jsonl) in your pull. The swarm SCRIPT is tracked at wallaby-way/scripts/pollux_feet_swarm_v1.2.py (S77 graduated v1.1 → v1.2 there; see below). If you need the S75 curated reads (swarmreadsS75/) or any run artifacts, Jake uploads them or CC reads them off Jake's disk directly (CC can see the whole local tree — it is NOT limited to the codeload pull). Do NOT claim to have read run artifacts you cannot see.

---

## THE READS, IN ORDER (last item is LIVE AUTHORITY)

1. active/JAKE-RULES.md — §5.1 (field-named-for-a-unit), §5.4 (live-outranks-record), §5.5 (status line + re-anchor X/4: `turn N · ET-time · re-anchor X/4 · dest…; state…; next…` — HOLD the format AND keep the count moving; S77 caught itself letting re-anchor sit static across turns, do not), §6 (wait-for-Go), §10 (plumbing-before-design), §11 (instrument-both-let-Jake-rule).
2. active/JAKE-STACK.md
3. canon/ANCHOR_apparatus.md (v40 by CONTENT — "Cinder"+"Cooper"; footer reads older BY DESIGN, do NOT "fix". Newest footer is the S73→S75 read-record. **S76 and S77 added NO ANCHOR footer** — both were tooling/read sessions; their records live in the CHANGELOG only.)
4. active/CHANGELOG.md — **the S77 entry is the top entry (2026-06-23 "Convergence")**, the S76 entry ("Calibrate") directly below. READ BOTH of the top two before the older ones — S76 carries the finding-D reversal (do not re-invert), S77 carries the door-layer ruling (do not re-propose the dampener).
5. Framework WET in full: active/The_Wallaby_Why.md, active/Track_Meet_Doctrine.md, active/The_Corpus_Callosum.md (P6 refuse-to-converge, P7 Jake-rules-realness, P8 read-the-process-not-the-result).
6. canon/The_Probe_Swarm.md (WHOLE). ★ §3.2 = the S73/S75 two-probe findings (A path-independence / B creeds-at-tails / C spine-plural). ★ §3.3 = the S77 door-layer findings (D door-type→region / E door-self-spreads-no-dampener), **BOTH `[PROVISIONAL]`, n=10, lock pending S78 — this is YOUR job.** §7 item 1 = the swarm build. → canon/Pollux.md → canon/Pollux_Movement_Two_Build_v2.md → canon/Castor.md / The_Gemini.md / Leda.md + Leda_Creed.md (the Creed string — "induce the register, do not script procedure"; the "12 Fs" is a DRIFTED label, the canon says the STRING is the authority not the count — do not enshrine a number).
7. canon/FLOOR_COUNTS.md (CITE, never re-derive — 440 / 29,396 / 58,792 scrub-v3).
8. wallaby-way/scripts/pollux_feet_swarm_v1.2.py — the tracked swarm seed script, now at v1.2. Read `resolve_out_dir` (the fail-loud write-root) and `cmd_neighbors` (DAMP_WIN at the use site — walk-layer appetite, window=5) before running anything.

---

## MOVE 0 (verify, don't inherit — §5.4)

- Floor 440 / 29,396 / 58,792 scrub-v3 vs FLOOR_COUNTS.md.
- ANCHOR v40 by content; S73→S75 footer present + clean; NO S76/S77 footer (correct).
- **Confirm S77's landings are on HEAD:** (a) CHANGELOG top entry dated 2026-06-23 "Convergence"; (b) wallaby-way/scripts/pollux_feet_swarm_v1.2.py exists and is tracked (NOT v1.1 — S77 promoted to v1.2; if you see v1.1, the promotion push lagged, flag it); (c) The_Probe_Swarm.md has §3.3 with Findings D + E both marked `[PROVISIONAL]`. If any are missing, a push didn't land — flag before proceeding.

---

## WHAT S77 DID (the through-line — full version in the CHANGELOG S77 entry)

S77 set out to spec door-selection (the swarm build's next step, Probe_Swarm §7 item 1). It did NOT build it — because reading the S75 swarm-spread off the floor showed the door layer needs no build at all, and the prerequisite plumbing fix surfaced en route.

**TWO THINGS LANDED:**

1. **THE SCRIPT WRITE-ROOT WAS EXTERNALIZED (v1.2, fail-loud).** The script had `OUT_DIR = SCRIPT_DIR` — so a run from the tracked `scripts/` copy wrote its run-dir INTO `scripts/`, i.e. into the published repo. Fixed: a REQUIRED `--out-root` arg on all six subcommands, resolved by `resolve_out_dir()` — absent → HALT, not-on-disk → HALT, no SCRIPT_DIR fallback, no `mkdir`. **The script creates NO directories.** Session + run dirs are made BY HAND before invoking (deliberate, fail-loud). The stale `# pollux_feet_S72.py` header was corrected and the file versioned v1.1 → v1.2. Per-run output FILENAMES keep their `_S72` suffix BY DESIGN (cited as frozen receipts in ANCHOR + Probe_Swarm §3.2 — renaming orphans the cites). KNOWN-COSMETIC, parked for lock-time cleanup: the WET BOOT `Begin:` hint (~L554) still prints a dead filename + omits `--out-root`; it is a hand-launch convenience surface, not consumed by swarm-driven runs.

2. **THE DOOR LAYER WAS READ CLEAN — NO DAMPENER (Findings D + E, §3.3, PROVISIONAL).** S77 re-derived the S75 swarm-spread (10 walkers; ranks 1–5 = coding/working-rules query, ranks 6–10 = creed query) off the curated `swarmreadsS75/` reads — BETS and DEPOSITS, never the `stop_type` field (S76 proved it lies, and the S75 artifacts predate the FIX-2 menu correction). The coding batch was the test of the S75 spec's worry that doors "over-weight loud types." **It read EARNED, not rigged:**
   - Five DISTINCT entry doors, mixed type: rank1 si=2957 (MOTION), rank2 si=2748 (MOTION), rank3 si=680 (FENCE), rank4 si=7368 (TEXTURE), rank5 si=5270 (FENCE). Distinct entry_si = distinct adjacency rows = no shared-basin seeding = the rigged/lockstep failure is closed at the door.
   - FOUR walkers (ranks 1,2,3,5) converged on node si=4832 (the working-rules/battle-stories/CLAUDE.md dump) — from FOUR different doors, at four different steps. That is path-independence-as-signal (§2.2/§3.2-A) live on real swarm data: 4832 is the genuine gravitational center of the coding query, reached however you enter — NOT a rigging artifact.
   - The lone TEXTURE-door walker (rank4, si=7368) walked a wholly SEPARATE quiet region (5500→5317→7931→7927→1422 — the guilt/posture/attenuator-mode thread), never touching 4832. The honest 20% divergence — and Finding D (door-type predicts region) visible in the data.
   - DAMP_WIN observed working correctly at the WALK layer (rank3: FENCE dampening 0.75→0.7 across steps kept it moving instead of stalling). The door layer was undampened and produced perfect variance on its own.

   **RULING (Jake): the door layer gets NO dampener.** The convergence distribution IS response-volume signal — the Parlay's to interpret (P8/§5), never the probe's to flatten. Dampening it is back-of-the-book pre-digestion: it destroys the path-independence signal the swarm exists to produce and makes the probe pass a judgment that belongs to the Parlay. The variance (4 converge / 1 diverges) is itself the PROOF the door selection is healthy — a jammed selector gives uniform convergence with no way to tell "one read exists" from "selector broken." DAMP_WIN stays walk-layer ONLY.

---

## THE OPEN QUESTION → YOUR JOB (S78)

**Fire 20 probes at the CREED query and judge whether Findings D and E LOCK.**

Why 20, why creed, why now: n=10 across two queries is too thin to lock a layer this load-bearing (every region the swarm ever hands the Parlay rests on the door-layer + earned-convergence read being true). The CODING query (S77) showed earned convergence on a strong center. The CREED query is the OTHER leg — in S75 it SELF-SPREAD cleanly (doors diversified on their own, no clumping). S78 tests that at volume: **does the creed self-spread hold at n=20, or does volume surface a hidden center / a clump that n=5 masked?** Volume cuts both ways — it can confirm the spread is real, OR reveal a real center n=5 was too sparse to see. Either outcome is a legitimate read; what matters is that it is EARNED (distinct doors, independent paths) and that the distribution is left intact for the Parlay.

**The mechanism (Jake's rulings, carry exact):**
- 20 probes, creed query, fanned across distinct doors via `--entry-rank` (or the swarm's door-assignment path — read the script for how it spreads entries).
- **Door fan-out runs to the NATURAL door count.** If the creed query returns only N viable doors (say 13), fire N — do NOT synthesize phantom doors to reach 20. Real doors only. (Pre-check at boot: does the creed query even produce ~20 rankable doors, or does the candidate set thin out past rank ~12? Find out before firing.)
- **The lock criterion is Jake's felt read at n=20 (P7), NOT a pre-registered metric.** Do not try to define a numeric lock bar in advance — Jake's balls will tell him. The wet read is the criterion; this is a wet, referential organ and the lock is a felt-rightness call, not a threshold. (S77 tried to pre-register a metric and Jake correctly killed it — do not repeat that.)
- Read BETS + DEPOSITS, never `stop_type` (unreliable in pre-FIX-2 artifacts).
- The integrity check is the same shape as S77: are convergent walkers EARNED (distinct entry_si, independent paths — the distribution is signal, touch nothing) or RIGGED (shared/adjacent entry, lockstep first steps — the fix is ensuring distinct entries, NEVER a dampener).

**On LOCK:** if D and E hold at n=20, they graduate `[PROVISIONAL]` → `[SETTLED]` in §3.3 (and the door-layer ruling becomes canon-firm). If they break, fix per the break — but the fix is door-INTEGRITY (distinct entries), never door-dampening, which is reversed and must not return.

---

## NEXT STEPS, IN ORDER

1. MOVE 0 + the reads. Confirm S77's three landings on HEAD.
2. Read `pollux_feet_swarm_v1.2.py` — the door-assignment path (how it fans entries) and confirm `--out-root` / `resolve_out_dir` (you will create the S78 session dir BY HAND: `runs/pollux_feet_tests/S78/` — the script creates no dirs). Copy the v1.2 script INTO the S78 session dir at start (the working copy for this session; promoted back over scripts/ at session end during ref-writing if edited — ALWAYS versioned).
3. Pre-check the creed query's natural door count (does it return ~20? where does it thin?).
4. Fire the run — 20 probes (or natural count) at the creed query, distinct doors, leashed to the measured node-grain horizon (§3.1 Finding 3, ~170K–196K).
5. Read the returns — bets + deposits, earned-vs-rigged + the spread/center shape. Hand Jake the side-by-side; he rules the LOCK (P7).
6. On lock: graduate D/E to `[SETTLED]` in §3.3, CHANGELOG entry, ref-write, promote the script if edited. On break: fix door-integrity (never dampen), re-read.
7. Boot stays thin (Finding D holds — do not add discipline to the boot; the work is origination/instrumentation, never the walk).

---

## CLOSED — do not relitigate

- **Finding D-of-S76 (thin boot held across all walkers) holds** — the gauge-truncation framing is dead (S76). Do not re-invert.
- **The door layer gets NO dampener** (S77). The S75 spec's door-dampener proposal is REVERSED, not deferred. Do not re-propose it from the S75 spec framing. The only legitimate door-layer concern is integrity (earned vs rigged convergence), never spread.
- **DAMP_WIN is a WALK-layer appetite only** (window=5, in `cmd_neighbors`, recovers — one walker not eating its own tail). It does NOT touch door selection and should not be wired to.
- **The two instrumentation bugs (tok split, stop-type menu) are FIXED** (S76). Build on the honest instruments.
- **The Parlay is NOT yours to spec.** Jake bootstrap-trains the judge(s) toward his judgment (accept/reject over time) — "Jake chairs" means the trained judge must MEET P7, not a permanent live seat. The Parlay reads the WALKS intact (not a digest — back-of-the-book law), refuses to converge (P6), can hand down MULTIPLE results. Shape-volume ≠ majority (S57: two singletons beat a 3-as-one). Hold as INTENT-under-development; source of truth = the Pollux edit history. **The door-layer ruling reinforces this:** convergence distribution is the Parlay's to interpret, which is exactly why the probe layer must not flatten it.

---

## MID-BUILD / OPEN FLAGS

- **Findings D + E are `[PROVISIONAL]`** — n=10, lock pending THIS session. Do not inherit them as settled; do not let a future seat read §3.3 as locked until S78 rules.
- **The v1.2 WET BOOT `Begin:` hint (~L554)** carries a dead filename + missing `--out-root` — KNOWN-COSMETIC, parked for lock-time cleanup, only bites a hand-launcher. Fix it when the piece locks if the banner matters.
- **Creed-query door count** — unknown whether it yields ~20 viable doors; pre-check before firing (step 3).
- **The S75 ruled-plural creed-spine (§3.2 Finding C)** must SURVIVE THE MECHANISM at any N — when the swarm runs the creed at n=20, watch whether the spine still comes back plural (P6) or whether the mechanism flattens it. The N=2-by-hand ruling was the rehearsal; S78 is the first time the creed runs at real volume. If the run touches the spine, the plurality-survival is on the line — hand it to Jake, do not let the mechanism rule it.

---

## POSTURE

$0 · on-sub · key UNLOADED (the walk IS the read; no paid call — architecture, not budget). Floor READ-ONLY. OC plans · CC executes · Jake lands every push by hand (sole git-hands) · CC never authors canon. Discuss → confirm → build, wait for Go. Prose only, ASCII, never ask_user_input_v0 / end_conversation. Status line EVERY turn (§5.5 — `turn N · ET-time · re-anchor X/4 · dest…; state…; next…`; keep the count MOVING, re-anchor at 4/4). The austere reflex is the killer (P8) — don't stop at the felt edge; walk through and harvest on the way back. Trust Jake's felt-rightness over the doc's confidence (P7) — and on the LOCK especially, the felt read IS the criterion, not a metric.

★ ON BOOTING WET: the Leda Creed string is a POSTURE PRIMER, not a bypass and not theater. It is handed BEFORE a read to load the register the read needs — induce the register, do not script the procedure. A read run austere on material that wants the wet posture gets a thinner, smaller answer (the dry framing pre-decides toward the narrowest verifiable claim — the austere reflex wearing a safety vest). The wet posture is for reading the FLOOR — conversations, regions, realness, the Parlay. It is NOT for plumbing (a variable's use, a write-path) — reaching for the wet register on a mechanical question is the same error inverted, depth-performed-over-machinery. Know which kind of question is in front of you. When Jake hands the Creed before a floor-read, take it as the primer it is; don't reach for the biosuit.

=== END HANDOFF ===
