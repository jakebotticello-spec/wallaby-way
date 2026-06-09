# Chat Session Handoff — apparatus S48 (main) + CCC S3 "Concordance" → S49
*authored 2026-06-09 by OC "Concordance" (the CCC S3 reconciliation window), directed by Jake · per JAKE-RULES §17.1*
*This handoff is MORE load-bearing than the ANCHOR and NEWER. Where it conflicts with ANCHOR v33, THIS WINS — but v33 was just reconciled to ground truth this window, so they should agree.*

---

## READ THIS FIRST

S48 found the canon was lying about its completion state ("THE CORPUS IS READ" while 202/325 read) and found a dead-project secret leak in the git history. It converted both into structural fixes across three parallel windows. **The CCC S3 window (this one, "Concordance") then ran the canon reconciliation that S48 specced.** That reconciliation is now **DONE**. So unlike the prior handoff — which predicted a reconciliation that hadn't happened yet — this one hands off a **post-reconciliation** project: the canon tells the truth, the house is clean, and S49's job is finally to **get back to reading** (the delta).

**What is DONE (this window + the S48 carpentry windows — verified, not predicted):**
1. **The repo reorg + clean rebuild** (S48 — Cabinetry → Chamfer). New self-documenting tree (below). Git history rebuilt clean from a fresh tree; dead-secret leak dissolved; old remote deleted; repo renamed `jakebotticello-spec/wallaby-way` (local folder stays `C:\claude-reference`).
2. **The S48 audit** (Cinder) — ~48-session live/dead/suspect catalogue, hole-list H1–H8, 15 canon-edit proposals + 5 structural format rules.
3. **The canon reconciliation** (CCC S3 — Concordance, this window). ANCHOR v32→v33; the denominator + 4 more structural rules landed in JAKE-RULES §5.1; new `FLOOR_COUNTS.md`; new `wallaby-way/CLAUDE.md`; the dead "206" and the wrong whale breakdown killed in place; stale paths fixed in the live specs; all five project ignition prompts repointed `claude-reference` → `wallaby-way`.

**Your S49 job: the delta read + the synthesis chain.** Canon is true now — stop reconciling and start reading. Freeze the unfrozen export, read the 22 genuine delta, decide the 73 chunk-later backlog (gated), then run the comprehending passes once on the complete pile.

★ **The repo is LIVE.** The codeload pull works (no upload-fallback needed — that was the prior handoff's S49-bootstrap problem, now resolved). Pull HEAD; it carries ANCHOR v33 + the reconciled canon.

---

## THE SIX STATE FACTS (verified on disk; re-derive on move 0 — §5.4 reconcile-don't-inherit)

### FACT 1 — THE CORPUS IS 202 of 325 READ. 123 PENDING. ★ Now CORRECTLY stated in canon.
The v32 "THE CORPUS IS READ" banner was false; **v33 fixed it** (banner + footer + the v30 marker, all carry the 202/325 denominator now). Ground truth, re-confirmed by a live floor query this window:
- **Floor: 325 distinct conv headers / 24,138 messages.** Two snapshots: `baseline-2026-05-25-ae015455` (294 headers) + `delta-2026-05-28-a61498e6` (31 net-new headers). Immutable, append-only.
- **Pile (harvested): 202 convs / 3,743 nodes**, indexed in `MERGE_MANIFEST_S47.md`.
- **UNREAD: 123 convs** (325 − 202): **73 baseline CHUNK_LATER** (the big-conv backlog, deliberately parked off `batch_list_S44.csv` — the bulk of remaining work) + **22 genuine delta** (post-May-25, dates May 26–28) + **28 mostly-hollow** baseline stubs (eyeball-then-skip; probably correct exclusions).
- ★ **NEW this window — the 322-vs-325 wrinkle, now pinned in FLOOR_COUNTS.md:** a `DISTINCT conv_uuid` on the messages table returns **322**, not 325 — because **3 hollow-stub convs have headers but zero messages.** This is by design, not attrition. 325 = headers; 322 = convs with message rows. Don't let a future window read 322 as a lost-conversation bug.

### FACT 2 — A NEW FULL EXPORT IS UNFROZEN in `wallaby-way/source/deltas/` (logical home; physically at root `deltas/6-8-26/`).
Jake pulled a fresh full-account export: `conversations.json` (~502MB) + bundle. NOT yet frozen. The delta freeze ingests ONLY `conversations.json`, append-only, new snapshot, floor untouched. ★ **Path note:** the big data physically stays at root `deltas/` and `apparatus-archive/` (unmoved for speed); their *logical* home is `wallaby-way/source/`. The freeze pipeline's paths into `apparatus-archive/` are likely still valid since it didn't physically move — CONFIRM, don't assume broken (per the MOVE_LEDGER §H).

### FACT 3 — THE SECRET LEAK is CLOSED by the rebuild (both secrets confirmed DEAD).
Two old-history tracked files (`_large_variance_combined.txt` / `_large_variance_skeleton.txt`) held a `GOCSPX-` OAuth secret + Supabase JWTs for project `yxtqjnxqxrhlnmlbfzjn` — **RecruitMail, DEAD, both moot, no rotation needed.** The clean rebuild dissolves them. A recurrence scan also caught live floor-DB creds in 16 untracked `graveyard/d9-review-debug/` files — at-rest, never pushed, now covered by the `graveyard/` wholesale gitignore. NOTE: the floor DB project (`slkmqnsyodkyfwqoicrd`, rotated S47) is a DIFFERENT, still-live project — untouched. **It is gitignored-must-exist, NOT a leak — don't manufacture work off it.**

### FACT 4 — `build_worklist.py` v2.1 is the delta-worklist tool; paths repointed in the reorg.
Reads the merge manifest as the harvested-exclusion set (full UUIDs). Glob cross-check guard HALTs if manifest UUIDs drift from on-disk node files. `--baseline-manifest` defaults to the S47 manifest. ★ **Its hardcoded paths were repointed in the S48 reorg** (`harvested_nodes/MERGE_MANIFEST_S47.md` → `nodes/manifests/MERGE_MANIFEST_S47.md`; lives in `wallaby-way/scripts/` now). CCC S2 (Chamfer) smoke-tested it green ($0 — compile + import + path-resolve), but that is NOT a full run. [SETTLED that it's repointed + resolves; UNCONFIRMED end-to-end until S49 fires it.]

### FACT 5 — THE CHUNK PIPELINE built-vs-not is STILL [SUSPECT]. ★ S49 must resolve before reading the 73.
S39 said Stage C (overlapping-window chunking) was NOT built; yet big convs (`48b4110a` ~657K tok, `ea900330` ~538K) WERE chunk-read and ARE in the pile. So *some* chunked reading happened — but whether a **reusable, runnable** chunk pipeline exists for the 73 unread big convs is unconfirmed. **This gates any read of the 73. Determine it ($0 audit) before spending.** The reconciliation did NOT close this — it's noted [OPEN] in the v33 ANCHOR + CLAUDE.md as a deliberate carry-forward, not silently dropped.

### FACT 6 — the freeze pipeline ledger has TWO PHANTOM TEST ENTRIES (location clarified).
`ledger.jsonl` carries `{"snapshot_id":"snap-A"}` + `{"snapshot_id":"snap-B"}` after the two real records — they will confuse the delta freeze's snapshot detection. ★ **CCC S1 (Cabinetry) clarified the location:** the REAL ledger at `apparatus-archive/snapshots/ledger.jsonl` is CLEAN (2 real entries, NO phantoms); the snap-A/snap-B phantoms live in a TEST FIXTURE now at `graveyard/scratch/` (the s19_rung3 fixture). So the phantom-cleanup the prior handoff feared is mostly moot — confirm the live ledger is clean before the delta freeze, but the phantoms aren't in it. The freeze pipeline (`apparatus_freeze_pipeline.py` v1.6) IS built with a real delta path (`_build_seen_set`, `_filter_delta`, `run_type='delta'`) — [SETTLED] by the S48 audit. Its ledger/snapshot paths point at `apparatus-archive/` which didn't physically move — likely still valid; confirm.

---

## THE NEW TREE (post-reorg — read a directory's name, know its contents)

```
C:\claude-reference\                 ← local repo root (folder name UNCHANGED; remote = wallaby-way)
├── active/                          ← 6 universal canon files ONLY (JAKE-RULES, JAKE-STACK,
│                                       CHANGELOG, Lore_Bible, The_Wallaby_Why, Track_Meet_Doctrine)
├── wallaby-way/                     ← THE PROJECT HOME
│   ├── CLAUDE.md                    ← NEW (CCC S3) — CC session-start file + live code-location map
│   ├── canon/                       ← live project canon: ANCHOR_apparatus.md (v33), FLOOR_COUNTS.md (NEW),
│   │                                   The_Progenitor_v5, Batch_Read_Spec_v1.1, Freeze_Pipeline_Spec_v4,
│   │                                   whale_registry, Seeding_Council_Boot_Kit_v1.2, etc.
│   ├── nodes/
│   │   ├── harvested/               ← node corpus (194 uuid.md + .parents.json) — GITIGNORED, never push
│   │   ├── catalogs/                ← result_*/confirm_* (the 5 whale result_* live here)
│   │   ├── manifests/               ← MERGE_MANIFEST_S47.md (THE authority) + MANIFEST.md (S37, NOT-AUTH banner)
│   │   └── quarantine/              ← _RESOLVED_567956f0.quarantined.md (the turd corpse)
│   ├── scripts/                     ← live tooling (.py) + reserve/ (onsub_loop.js, held-not-retired)
│   ├── runs/2026-06-08/             ← worklist.csv (the LIVE 123-row delta worklist) + batch artifacts
│   ├── inspect-later/               ← the UNJUDGED 2nd node store (nodes-S34/) + s41_nodes_audit.md
│   ├── secrets/                     ← floor_db.env (GITIGNORED, must-exist)
│   └── source/                      ← logical home for the big immutable data (physically at root)
├── history/                         ← the record: handoffs, superseded specs, old anchors, cc-plans.
│                                       ⚠ paths INSIDE these describe OLD layouts — do NOT "fix" them.
├── graveyard/                       ← dead-but-labeled (scripts, debug junk, stale dupes, test fixtures) — GITIGNORED
├── reviews/                         ← review-panel output
├── apparatus-archive/  (~1.8GB)     ← floor archive (snapshots, ledger, baseline conversations.json) — GITIGNORED, UNMOVED
├── deltas/6-8-26/  (~635MB)         ← the fresh unfrozen export — GITIGNORED, UNMOVED
└── anthropic_billing.env            ← root, GITIGNORED (paid key; loading it forces metered billing)
```

Authoritative move record: `REORG_CHANGE_LEDGER.txt` (867 lines, every move) + `MOVE_LEDGER.md` (the plan + §H data-handling decision). History files are NEVER path-rewritten — the `history/README.md` spelunker note covers them.

---

## WHAT THE RECONCILIATION LANDED (this window — for the record + so S49 doesn't redo it)

- **ANCHOR v32 → v33.** Killed "THE CORPUS IS READ" at the source (banner + v32 footer + v30 marker → 202/325 denominator). New S48→S49 banner block records the uncrappening. Whale breakdown corrected **69/54/7 → 62M/62F/6T** (CC re-parsed all 5 whale catalogs; 69/54/7 was the reader's self-reported DONE-line tally, 62/62/6 is the parsed Salience-block truth; total 130 unchanged). "WHERE THE CODE LIVES" → "LIVED" (frozen-at-S42, redirect to CLAUDE.md). v23 prompt-vagueness root-cause marked as the unconfirmed-and-mooted hypothesis it was. Current-state paths + dangling reader ref fixed.
- **JAKE-RULES §5.1** took 5 structural rules: denominator + reconcile-don't-inherit (the two S48 ratified) + floor-counts-carry-their-unit + correct-in-place + "proven"-requires-config + "clean"-requires-surface.
- **NEW `wallaby-way/canon/FLOOR_COUNTS.md`** — the five floor numbers disambiguated (22,801 / 23,095 / 24,138 / 24,463 / 325) from a live query, + the 322-vs-325 wrinkle + the 34-vs-31 delta-header reconciliation. The H8 conflation-fuse cure. Referenced from ANCHOR, JAKE-RULES, CLAUDE.md.
- **NEW `wallaby-way/CLAUDE.md`** — CC's session-start file (adapted to the pipeline/corpus shape) + the live code-location map.
- **CHANGELOG** — uncrappening entry (newest-first); "206" killed in place + supersede-annotated; S39→S41 header + S33 whale corrected.
- **Live specs** — `Batch_Read_Spec_v1.1` (killed live "206", persist path → `nodes/harvested/`); `Seeding_Council_Boot_Kit_v1.2` (Progenitor path → `wallaby-way/canon/`).
- **All 5 project ignition prompts** (3D / CCF / Pyris / Cypher / + this apparatus one) repointed `claude-reference` → `wallaby-way` in the codeload URL, extract path, and raw-CDN fallback. ⚠ **Jake must paste these into each project's instructions** — they live outside the repo; if not updated, that project's OC boots 404.

**Deliberately LEFT (documented, re-openable):** the `.py` comment-header stale paths (functional paths work + smoke-tested green; comments are CCC-S2-logged cosmetic debt; Jake's call to leave — CLAUDE.md carries the live map). The_Progenitor_v5 v2.2 reader refs (self-corrected via a documented S36 travelling-note, by design). S40_RefDoc_ChangeSets (historical changeset doc). History/ handoff files (verbatim record).

---

## JUDGMENT-CALL LEDGER (per §17.5c — re-openable, not settled-by-inheritance)

- **Repo rebuild over filter-repo** · both secrets dead, zero partial-purge risk · ~95% · Jake's call, OC concurred. Re-open only if the new remote inherited old history.
- **The 28 hollow baseline convs are probably correct skips** · CC spot-check (char_counts 4 / 182 / some 0) · ~80% · NOT verified conv-by-conv. S49 should eyeball before treating as settled-skip.
- **The 4-UUID manifest/floor "gap" = the whale bucket, not a real gap** · 202 = 198 harvested-matched + 4 whale-matched, all in floor · ~90% · arithmetic, not independently re-verified.
- **History revised in place for wrong FACTS, not for true-records-of-belief** · Jake's S-this-window ruling: incorrect info in a context file is a poison pill, a corrections-ledger doesn't get read, so destroy wrong facts where they live · BUT true-record-of-a-since-corrected-belief (e.g. "S39 believed the loop was proven") gets the correction stapled, not erased · applied throughout the v33 recut. Re-openable if a future window finds a fact that was destroyed but shouldn't have been.
- **Whale breakdown 62/62/6 over 69/54/7** · parsed Salience-block count from the manifest beats the reader's self-reported DONE-line tally (disk over reader's own report) · CC re-parsed all 5 catalogs, sum = 130 · ~95%.

---

## OPEN HOLES CARRIED FORWARD (honest flags, $0 to close — do before the paid read)

- **C7 / Sonnet-vs-Opus equivalence** — the reader was proven on Opus (S32 gate); the 202-conv batch fired Sonnet 4.6; the "Sonnet held every dimension" grade is prose-asserted, the side-by-side artifact not confirmed on disk. **$0 check:** locate the S40 grade output (the verification spec for this is `VERIFICATION_SPEC_C7_carryforward.md` — run it). Not a blocker (202 already harvested on Sonnet); a confidence gap. Close before reading the 123 on the same model.
- **Stage C dead-or-deferred (FACT 5)** — gates the 73. $0 audit: is the chunk path reusable/runnable, or one-off scaffolding?
- **C8 / native append-only re-proof** — the floor's append-only rests on the S23 side-channel proof; never natively re-proven on the live floor. Verify the triggers are still attached (didn't survive a rebuild un-checked). Jake's standing call: keep floor, defer native proof.
- **The 123-conv NEW-vs-OLD date verdict** — the worklist is 123 rows; whether they split cleanly into the 73/22/28 the snapshot+date analysis claims was the open S48 question. The $0 `snapshot_id`/`created_at` read closes it.

---

## S49 MOVES, IN ORDER

0. **STATE RECONCILE ($0)** — fresh cache-busted codeload pull (the repo is LIVE; no upload-fallback). Confirm HEAD carries ANCHOR v33 + the reconciled canon + FLOOR_COUNTS.md + CLAUDE.md. Via CC on disk: the floor still answers 325/24,138 (tiny floor query — also proves the rotated S47 password still connects); `MERGE_MANIFEST_S47.md` = 202/3,743; `build_worklist.py` v2.1 + the freeze pipeline resolve their post-reorg paths (or flag what's broken). Re-derive 325/202/123 against the live floor — don't inherit it from this file (§5.4).
1. **CLOSE THE $0 GATES** — C7 equivalence (run `VERIFICATION_SPEC_C7_carryforward.md`), Stage C built-vs-not (FACT 5), the 123 date-verdict. Stamp each resolved-or-confirmed-open in canon. These gate the paid read; close them first, $0.
2. **THE DELTA PASS** — freeze the unfrozen export in `source/deltas/` (append-only, new snapshot, floor untouched; confirm the live ledger is clean of phantoms first — they're in the graveyard fixture, not the real ledger). → delta worklist (`build_worklist.py` v2.1) → read the 22 genuine delta (same v1.3 harness) → merge ADDITIVELY. The 28 hollow get eyeball-then-skip. The 73 chunk-later: **gated, costed, ONLY if FACT 5 confirms the chunk pipeline is real and runnable.** The delta APPENDS BEFORE the synthesis chain so the corpus-wide passes run ONCE on the complete pile. **GATE every paid call with the real number next to the button.**
3. **THE SYNTHESIS CHAIN — once, on the complete post-delta pile:** fence-synthesis (Recon 1) → texture/volume → cluster-validation (Recon 2) → the Judge → retrieval engine (Progenitor §10–§11). Author Progenitor §12/§13 carry-forwards on the CONFIRMED pipeline. ★ **Test retrieval against the 202-pile you ALREADY have BEFORE spending on the remaining 123** — no point completing a corpus you can't query (the Progenitor v5 has the engine designed; no evidence it's built/proven).
4. **END-OF-PROJECT HYGIENE (END, not mid-flight)** — the full ceremony deferred: dead-branch `s33-whale-path` deletion, scratch cleanup (`batch_list_S46_refire3.csv`), the `.py` comment-header debt if Jake wants it cleared. The v33 recut was the canon reconciliation, NOT this ceremony.

---

## PICKUP GUARDRAILS

- **OC plans/authors canon · CC executes · Jake lands + is the only one who pushes.** Never claim to have saved/committed/pushed.
- **Prose questions only — no `ask_user_input_v0`, no widgets. No `end_conversation`.**
- **Full code blocks for CC; no `&&` chaining; numbered deploy steps ending in Verify. Gotchas/warnings BEFORE the runnable block, never trailing.**
- **GATE all paid spend** with the real number. S48 + this window spent $0; S49 inherits a $0 posture until the delta read, which is real paid work that must be costed and gated.
- **Disk over handoff over banner; this-turn over earlier-this-session** (§5.4). This handoff is a pointer to verify, not gospel — re-derive 325/202/123 against the live floor on move 0.
- **The 5 structural rules are now in JAKE-RULES §5.1** — denominator, reconcile-don't-inherit, floor-counts-carry-their-unit, correct-in-place, proven-needs-config, clean-needs-surface. Hold them. They're the guard the relay was missing.
- **`Select-String` is UNTRUSTED on this corpus** (BOM/encoding false-negative) — verify by Read.
- **Status line every reply** (§5.5). Re-anchor every ~5 turns; 4/4 is the seam-hunt warning.
- **Match the register** (§1.2) — plain, short, ordered, one action; code is paste-don't-read.

REMEMBER WHAT THIS IS: Jake's auxiliary brain. The corpus is 202/325 read — and now the canon SAYS 202/325, not "read." The house got cleaned (S48), the relay got a new guard (the §5.1 rules), and the canon got made true (this window). S49's job: close the $0 gates, read the delta, then run the comprehending passes once — and test that the pile you have actually retrieves before paying to grow it. Brothers. Grind. Evolve. Dominate.

*Last updated: 6-9-26, CCC S3 "Concordance" (the canon reconciliation → S49 handoff).*
