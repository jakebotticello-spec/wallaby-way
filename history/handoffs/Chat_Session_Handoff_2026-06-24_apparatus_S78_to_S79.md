# Handoff: S78 — "The Bail" (creed-swarm lock test + two spec fixes) → S79: Proposed "The Re-Fire" (rebuild the feet to v1.3, re-run the lock)

**ONE-LINE STATE:** The first full-size swarm (20 walkers, creed query) fired and did NOT lock Findings D/E — it bailed (17/20 stopped early with context unspent) and in failing surfaced two real mechanism holes, both now `[RULED]` and written to spec; a parallel side-seat ran the first by-hand N=5 Parlay rehearsal (Finding C's plurality survived); **nothing from S78 is confirmed on HEAD yet — S79's move-0 is to reconcile git-state against disk before building on anything below.**

*"Proposed" name because S79 may rename once scope firms (§17.1).*

---

## 0. READ-ORDER + THE FIREWALL ON THIS HANDOFF (read this first)

This session had **two seats running in parallel**, both labeled apparatus-S78:
- **The main-build seat (this handoff's author, OC).** Ran the creed-swarm lock test, read the 20 returns, found the two mechanism holes, authored the spec fixes (Probe_Swarm §3.4 + the v1.3 delta + the S78 "The Bail" CHANGELOG entry).
- **The Parlay side-seat (off-main-build, "S78 Parlay").** Ran the first end-to-end by-hand Parlay rehearsal (five Claude.ai chat-seats) against the *same* 20-walker swarm output, and authored the pollux-parlay canon.

**FIREWALL — load-bearing, do not violate (§5.1):** the main-build seat did **not** run the Parlay experiment. The Parlay findings in §4 below are **locate-and-route only** — pointers to where the side-seat enshrined them, *not* a re-summary. Re-characterizing those findings from a seat that didn't live them re-colors them (the exact reason the experiment was run in a separate seat). **S79: when you read the two Parlay files, read them as the authored record; do not re-derive or re-rule their findings. Point, route, confirm git-state — do not re-interpret.**

---

## 1. SESSION RECORD — what actually happened (honest, including what went sideways)

### 1a. The main build: the creed-swarm lock test (S78 "The Bail")

S78's job (inherited from the S77→S78 handoff): **fire ~20 probes at the creed query and judge whether Findings D + E LOCK** (`The_Probe_Swarm.md` §3.3 — door-type→region, door-self-spread; both `[PROVISIONAL]` at n=10).

What we did, in order:
- **Full re-anchor + MOVE 0.** Fresh HEAD pull, floor verified untouched (440 / 29,396 / 58,792 scrub-v3, cite `FLOOR_COUNTS.md`), ANCHOR v40, D/E confirmed `[PROVISIONAL]`, script confirmed `pollux_feet_swarm_v1.2.py` (promotion did not lag). Re-read the Pollux refs and corrected two of the author-seat's own errors mid-session (§5.4-inward): (1) the leash is **felt drift-from-subject, NOT a hop/node count** (region-leash broad ≥753K, node-grain horizon ~170–196K; §3/§3.1); (2) **the feet had never run** before this — eyes proven 3× (S65/S68/S71), feet `[PLACEHOLDER]`-on-disk; this swarm was plausibly the **maiden feet run**.
- **N-derivation.** Pre-check (one `init` smoke) returned **79 natural doors** for the creed query — no phantom-door risk. Settled N=20 by a real derivation, not the inherited number: it's the ceiling the **no-slice Parlay** can hold whole with reasoning headroom (Jake ruled NO slicing / no chunking the Parlay — sliced judges rule on different evidence = false agreement). Jake's original off-the-cuff "20" turned out to land on that ceiling.
- **Fired 20 walkers, ranks 1–20, creed query, across 4 windows** (A:1-5 / B:6-10 / C:11-15 / D:16-20), parallel, distinct doors via `--entry-rank`, walk discipline = the four S73 corrections (query-blind walk, walk-through-the-hedge, walk-the-extent, honest stop-type) + hard independence rule.
- **What went sideways during the run (all recorded, none fatal):**
  - Windows A/B/C **compacted mid-run.** Jake spotted the pattern: ~2 full walks fit in a window before compaction; the walker mid-flight at the threshold takes the seam. We chose to **let them complete** (natural experiment) rather than refire blind. Finished walks commit to disk as they happen (§5.4) — a compacted *executor* doesn't un-write a finished walk; the Parlay reads the on-disk returns, never the executor's context.
  - A **false alarm** on rank 18 (CC re-reading its artifacts looked like a re-run; it was finalizing rank 19 — forward progress, not a loop).
  - Window D ran long (deep walks); rank 18 ran to **34 steps / 90% of region cap** — the only walker that neared the wall.

### 1b. The read — the spec-solid-at-20 instrument check (this is where the run turned)

Read all 20 returns off disk (extracted `swarmreadsS78.7z`: 20 regions + 20 walk_logs, all finalized). **The honesty axes held** (stops: 17 subject-drift / 3 subject-complete / **zero regression**; token-split present not summed — S76 fix held; whale-fencing active). **But two holes surfaced that were invisible at n=5 and only show at volume — these became the session's real product:**

- **The bail (→ Finding F).** 17 of 20 walkers stopped `subject-drift`; 11 deposited zero. The context column is decisive: only rank 18 neared the cap (90%); the other 19 stopped at **2.6%–37.9%** of budget — i.e. **62–97% of context UNSPENT.** Jake's cut, confirmed on disk: these are **lazy bails, not dry doors.** A walker cannot validly claim `subject-drift` with budget unspent — the justification ("nothing creed-adjacent ahead") is territory-knowledge it only earns by walking. **The leash is context-max, not a "is there maybe more? y/n" checkbox.** The stop-type menu *enabled* the bail by fusing reason-with-permission.
- **The door collision (→ Finding G).** Ranks 14 AND 18 both entered si=425 → **19 distinct doors, not 20.** Cause: the `castor_pool` **re-ranks across separate inits** (b2/MiniLM nondeterminism — the HF-warning model load), so per-window `--entry-rank` firing does not guarantee distinct doors. **NOT rigging** (independent resolution to the same node, no lockstep) — a distinct **door-determinism** failure. *(The staging file Jake proposed pre-fire and the author-seat waved off would have prevented this — needed for door-determinism, not coordination. The collision is the receipt.)*

**Verdict:** the run **underdelivered as a lock test** (19 usable doors, thin harvest, the bail confound — a run where most walkers quit early can't answer whether the door layer self-spreads) and **over-delivered as a spec test** (proved two holes the only convincing way — by letting walkers fall through them on disk). D and E stay `[PROVISIONAL]`. **Re-fire on the fixed spec.**

### 1c. The Parlay side-seat (ran in parallel — locate-and-route, see §4)

Jake ran the first end-to-end Parlay rehearsal by hand: **five separate Claude.ai chat-seats, identical boot, convened across staged turns** against this same 20-walker creed output. The analyst-layer analogue of the S75 N=2 by-hand spine ruling, scaled to N=5 with a real convene+discuss step. **Finding C's pre-registered acceptance test PASSED at N=5, by-hand analyst layer** (the ruled-plural creed-spine survived the mechanism; five fresh boots, none flattened it). Provenance stays honest: five chat-seats, **not the built organ — the Parlay is still UNBUILT** (`The_Probe_Swarm.md` §7 item 1). The side-seat enshrined this in the new `canon/pollux-parlay/` folder + amended Pollux.md. **Details and exact routing in §4; do not re-summarize.**

---

## 2. VERIFIED GROUND-TRUTH STATE (tagged do-not-relitigate)

- **Floor: 440 / 29,396 / 58,792 scrub-v3.** Untouched all session ($0, on-sub, key UNLOADED, floor READ-ONLY). Cite `FLOOR_COUNTS.md`, never re-derive.
- **ANCHOR: v40 by content ("Cinder"/"Cooper").** No S76/S77/S78 footer (correct — all CHANGELOG-only).
- **The feet RAN for the first time at volume** (S78). Prior: 2 single probes (S73), 10-walker spread (S75 / read S77). The maiden full-swarm.
- **Findings D + E: `[PROVISIONAL]`, lock pending a clean re-fire.** S78 did NOT lock them. Do not record them as locked.
- **Finding C (creed-spine plurality): `[RULED]` by Jake, and its acceptance test now PASSED once more at N=5 by-hand** (Parlay side-seat). Still NOT proven by the built organ — the standing bar holds: a future seat must not inherit "the Parlay ruled the creed-spine."
- **The leash is felt drift-from-subject, NOT a hop/node count.** Region-leash broad (shape held ≥753K); node-grain horizon ~170–196K rendered chars; whales fenced at draw time (§3/§3.1).
- **DAMP_WIN stays walk-layer only** (S77 Finding E — the door layer gets NO dampener; do not revive it).
- **`REGION_TOK_HI_CAP = 800,000` is `[INTENT]`, not a hard stop in v1.2** — the run proved nothing auto-halts at it (rank 18 ran to 90% and kept going). Fix F1 changes how it's USED, not its value.

---

## 3. GIT-STATE — UNCONFIRMED, RECONCILE FIRST (§5.4 reconcile-don't-inherit)

**As of this handoff's authoring (2026-06-24 ~14:32 ET), a fresh codeload pull of HEAD shows NONE of the S78 work committed/pushed:** CHANGELOG top is still S77 "Convergence"; no `canon/pollux-parlay/` folder; Probe_Swarm has no §3.4; Pollux.md shows the pre-S78 §4. This means **everything authored this session across both seats is staged/local — not on HEAD, or not yet propagated.**

**S79 MOVE-0 (mandatory, before building anything):** confirm with Jake, file by file, what is committed/pushed vs. staged-only. The candidate staged set across both seats:

*Main-build seat (delivered to Jake as downloads, to commit):*
- `wallaby-way/canon/The_Probe_Swarm.md` — full file with **NEW §3.4** (Findings F + G, both `[RULED]`). Inserted between §3.1 and §3.2 by topic (leash/stop-mechanics), so it reads 3.1 → 3.4 → 3.2 numerically out of order — **OPEN: Jake may want §3.4 moved to after §3.3 for numeric order.** Confirm placement before commit.
- `pollux_feet_swarm_v1.3_DELTA.md` — NEW script-spec note (implements F + G; v1.2→v1.3 promotion deferred to the re-fire build).
- `active/CHANGELOG.md` — S78 "The Bail" entry prepended above S77.

*Parlay side-seat (staged this session per its routing note — 4 files):*
- `wallaby-way/canon/pollux-parlay/Parlay_Iteration_1.md` — the experiment spec. **Blind-firewalled by ruling: stays as authored, no edits from later knowledge.**
- `wallaby-way/canon/pollux-parlay/Parlay_Judges_Responses_1.md` — companion receipts (judge responses SUMMARIZED not verbatim by ruling; raw transcripts off-repo for poison-pill risk; has a §7 bias-flagged late retrospective).
- `wallaby-way/canon/Pollux.md` — amended full-file (S78 lineage block: Pollux is **referential** — "Castor draws the outline, Pollux colors it in"; + §4 guard against unanchored "soul-read" drift). Zero deletions, body byte-faithful.
- `active/CHANGELOG.md` — **POTENTIAL CONFLICT:** both seats touch CHANGELOG. The Parlay seat's routing note says the version it handed S78 has the S77/S76 entries folded intact with its S78 entry above. The main-build seat *also* authored an S78 "The Bail" CHANGELOG entry. **S79: reconcile the two CHANGELOG S78 entries into one coherent newest-first ledger before commit — do not let one clobber the other.** This is the single most likely place for a silent loss.

New folder: `canon/pollux-parlay/` (slug: hyphen, lowercase, shell-safe per §16).

---

## 4. THE PARLAY SIDE-SEAT FINDINGS — LOCATE & ROUTE ONLY (do not re-derive)

*S79: read the two files directly for the substance. Below is WHERE each thing lives and its status — pointers, not a re-summary. The firewall (§0) applies.*

- **The function findings (the experiment's primary deliverable):** `Parlay_Iteration_1.md` **§4** (findings 1–8) + the companion's **§4** (the blind→convened delta). The side-seat flagged findings **3, 4, 5, and 8** as "most at risk of being lost in a naive build implementation" (`Parlay_Iteration_1.md` §8) — route those into the build-acceptance-test list when the Parlay gets specced.
- **Mechanism result:** plurality survived at N=5 — `Parlay_Iteration_1.md` §0 + §7. Finding C acceptance test PASSED, by-hand analyst layer.
- **Provenance + the standing bar + overclaim guards:** `Parlay_Iteration_1.md` **§8** and the companion **§6**. Both restate: do NOT inherit "the Parlay ruled."
- **What the seats proposed for the built Parlay (attributed, hedged, NOT rulings):** companion **§5**.
- **The late bias-flagged retrospective (held as a competing read, NOT part of the blind record):** companion **§7**.
- **Pollux "referential" ruling + the §4 drift-guard:** `Pollux.md` (amended). **DOCTRINE S79 MUST CARRY:** a Pollux read that leaves the query's referents and calls the free-association wetness is **unanchored, not too-wet** (Pollux.md §4). "Castor draws the outline, Pollux colors it in" — the shaping is the product; relevance is the gate.

---

## 5. STILL OPEN — ordered next-steps for S79

**Priority 1 — reconcile git-state (§3).** Confirm committed vs staged file-by-file with Jake; reconcile the two CHANGELOG S78 entries; settle the §3.4 placement question. Nothing else builds until HEAD is known-good.

**Priority 2 — the re-fire build (the main thread): promote v1.2 → v1.3, implement Findings F + G.** Per `pollux_feet_swarm_v1.3_DELTA.md`:
- F1: promote the existing region-gauge from passive print to **active pre-read gate** (refuse a node-read that would tip past cap-minus-one-max-node — serves "never read over 100% and compact").
- F2: make `--stop-type` **repeatable** (plural reasons).
- F3: `cmd_finalize` **HALTs** on `subject-drift` with unspent budget (fail-loud — makes the bail impossible, not just discouraged).
- G1–G3: `stage-doors` subcommand → `door_manifest.json`; fire on `--entry-si` not `--entry-rank`; HALT on rank-based multi-walker firing without a manifest.
- `[INTENT]` to settle at build: the F1 threshold (≈95% of cap vs the cleaner "one-max-node-of-headroom" formulation — the delta recommends the latter).

**Priority 3 — re-fire the 20-walker creed lock test on v1.3.** Staged doors (no collision), forced-to-wall walks (no bail), and THEN read for: (a) the D/E lock, (b) the §3.2-C spine-survival-at-volume through the *built* mechanism path, (c) rank-18's held harvest disposition (deep earned creed-wander vs Leda-shaped off-leash harvest — flagged for the re-fired run's Parlay, not yet ruled).

**Priority 4 (offered, not built):** an `[INTENT]`-flagged build-acceptance-test list for the Parlay, derived from the side-seat's findings (esp. the at-risk 3/4/5/8).

---

## 5b. DOWNSTREAM FLAGS (will bite later if not carried)

- **Off-repo archive the five raw judge transcripts before those windows close — gone otherwise.** (Bites the moment those chat windows are lost; the companion file deliberately keeps them off-repo, so the only copies are in the live windows.)
- **The five Turn-2 baseline reads are owed as receipts** — the companion *points at* the blind→convened delta but the before/after is currently asserted, not shown. Bites when anyone tries to verify the delta independently.
- **OPEN (routed from side-seat):** whether the judges' self-reports/critiques become a separate honestly-late retrospective artifact or stay off-repo-raw.
- **The compaction pattern** (~2 walks/window before compaction) bites every future multi-walker run — the v1.3 re-fire should plan windows in pairs, or the build should externalize walk state so a compacted executor resumes cleanly. Worth a real look during Priority-2.
- **`subject-complete` cannot be machine-validated for "earned closure"** (it's a read) — F's delta surfaces context% in the finalize report so the Parlay/Jake can eyeball whether a pre-wall `subject-complete` was earned by walking. Carry that the 3 S78 subject-completes (ranks 4, 6, 20) were never confirmed as earned.

---

## 5c. JUDGMENT-CALL LEDGER (§17.5c — the call · reasoning · confidence · source)

- **N=20 for the swarm** · sized to the no-slice Parlay's whole-context ceiling (framework + reasoning headroom), not the inherited number · high confidence · derived this session, Jake ruled no-slice.
- **Let A/B/C complete after mid-walk compaction rather than refire** · finished walks commit to disk; a natural experiment on whether compaction corrupts a walk beats refiring blind · medium-high · Jake's call, §5.4 reasoning.
- **The 17 drifts are lazy bails, not dry doors** · the context column (62–97% unspent) is decisive — a dry door read to exhaustion shows a walker that *walked* · high confidence · Jake ruled, confirmed on disk.
- **The collision is door-nondeterminism, not rigging** · independent resolution to the same node, no lockstep first steps · high · read off the two walk_logs + the pre-check-vs-fire door-list mismatch.
- **§3.4 placed by topic (after §3.1) not by number** · it's leash/stop-mechanics canon, belongs with the leash sections · LOW confidence — flagged for Jake to overrule toward numeric order · author-seat judgment.
- **Session named "The Bail"** · the run where 17 walkers bailed and taught why · low stakes, Jake may rename.

---

## 6. PICKUP GUARDRAILS (the working-mode reminders that matter for THIS pickup)

- **OC plans · CC executes · Jake is sole git-hands · CC never authors canon.** Discuss → confirm → build; wait for Go.
- **The firewall (§0) is the load-bearing one for this handoff:** the Parlay findings are locate-and-route. Read the files; do not re-rule them.
- **$0 · on-sub · key UNLOADED · floor READ-ONLY.** Same posture all session.
- **Re-fire is the maiden run of v1.3** — instrument check it the way S78 instrument-checked v1.2 (the spec is only as solid as its first volume run proves; F and G are themselves `[RULED]`-but-unrun).
- **Status line every turn (§5.5), re-anchor count moving.** Prose questions only, ASCII `·` bullets, never `ask_user_input_v0` / `end_conversation`.
- **Disk over handoff (§5.4):** this handoff is a pointer to verify, not a fact to inherit. Move-0 reconciles git-state against HEAD before anything builds.
- **Wet for the floor-read, austere for the plumbing — know which question is in front of you.** The v1.3 build is plumbing (build it clean, austere). The re-fired returns are the floor (read them wet, watch the spine survive). Don't reach for the biosuit on the pipework, don't read the floor in a safety vest.

---

*Handoff authored by the apparatus S78 "The Bail" main-build seat, 2026-06-24. The Parlay side-seat's work is folded in as locate-and-route per its routing note and the §5.1 firewall. Git-state is UNCONFIRMED at authoring — §3 is move-0.*
