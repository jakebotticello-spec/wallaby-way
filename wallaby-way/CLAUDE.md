# CLAUDE.md — The Wallaby Way (the apparatus)

**For Claude Code working in this repo. Read this first, every session.**

> **Universal rules** (Brothers Clause, communication, building, debugging, the denominator rule, etc.) live in:
> `@C:/claude-reference/active/JAKE-RULES.md`
>
> This file is project-specific only. If something belongs everywhere, it goes in JAKE-RULES.md, not here.

---

## What this is

The Wallaby Way (the "apparatus") — Jake's **auxiliary brain**: a corpus-processing pipeline that reads ~440 Claude conversations into an immutable floor [S51 fix: was ~325 — the floor grew at the 6-9 delta freeze], harvests them into a flat pointer-pile of salience nodes, and (eventually) serves them through a retrieval engine. It is NOT a deployed web app — there is no server, no frontend, no deploy target. It is a Supabase floor + a Python batch-read pipeline + a node corpus on disk. Read *The Wallaby Why*, *Track Meet Doctrine*, and *The Wallaby Whales* as **framework** (the breadth IS the function; the record is verbatim) before working — they are posture-setting, not reference.

**The non-negotiable architecture:** the **floor is immutable and append-only** (DB triggers + REVOKE enforce it). Nothing — no script, no fix, no convenience — mutates the floor. The pipeline reads FROM it and writes nodes elsewhere. Source data is read-only to tooling; output lands in named dirs.

---

## Repo orientation

```
C:\claude-reference\                 ← local repo root (folder name UNCHANGED; remote is wallaby-way)
├── active/                          ← 6 universal canon files ONLY (JAKE-RULES, JAKE-STACK,
│                                       CHANGELOG, Lore_Bible, The_Wallaby_Why, Track_Meet_Doctrine)
├── wallaby-way/                     ← THE PROJECT HOME
│   ├── CLAUDE.md                    ← this file
│   ├── canon/                       ← live project canon (ANCHOR, specs, Progenitor, whale registry,
│   │                                   FLOOR_COUNTS.md)
│   ├── nodes/
│   │   ├── harvested/               ← the node corpus (400 files / 397 convs + .parents.json sidecars;
│   │   │                               two naming generations — bare-UUID + result_*/chunk; S51) — GITIGNORED
│   │   ├── catalogs/                ← result_*/confirm_* (harvested products)
│   │   ├── manifests/               ← MERGE_MANIFEST_S47.md (THE authority) + MANIFEST.md (S37, NOT-AUTH)
│   │   └── quarantine/              ← guard-tripped convs (the _RESOLVED corpse lives here)
│   ├── scripts/                     ← live pipeline tooling (.py) + reserve/ (held-not-retired)
│   ├── runs/<date>/                 ← dated run output (worklist.csv, batch lists, logs)
│   ├── inspect-later/               ← the UNJUDGED 2nd node store (S34 shape-loop) — do not trust as live
│   ├── secrets/                     ← floor_db.env (GITIGNORED, must-exist)
│   └── source/                      ← logical home for the big immutable data (physically unmoved at root)
├── history/                         ← the record: handoffs, superseded specs, old anchors.
│                                       ⚠ paths INSIDE these files describe OLD layouts — do NOT "fix" them.
├── graveyard/                       ← dead-but-labeled (scripts, debug junk, stale-canon dupes) — GITIGNORED
├── reviews/                         ← review-panel output
├── apparatus-archive/               ← ~1.8GB floor archive (snapshots, ledger, conversations.json) — GITIGNORED
├── deltas/                          ← ~635MB fresh export, unfrozen — GITIGNORED
└── anthropic_billing.env            ← root, GITIGNORED (the paid-API key; loading it forces metered billing)
```

The S48 reorg made the tree self-documenting: **read a directory's name, know its contents.** If a dir's name doesn't tell you what's in it, that's a regression — flag it.

---

## The OC / CC / Jake loop (this project's "deploy workflow")

There is no `git push`-to-prod here. The working pattern is the multi-window apparatus:
- **OC (Orchestrator-Claude)** — plans, authors canon, holds state. Pulls the codeload tarball at session start.
- **CC (you, Claude Code)** — executes on disk: reads, runs scripts, applies the str_replace/writes OC authored. **CC MUST NOT AUTHOR CANON.**
- **Jake** — lands the work, and is the **only one who commits + pushes.** Never claim you committed or pushed.

Full code blocks for CC; no `&&` chaining; numbered steps ending in **Verify**. Gotchas/warnings **before** the runnable block, never trailing.

---

## Output discipline (load-bearing — the rule that keeps the tree honest, born from a near-leak)

**Source data is read-only to tooling. Every script writes its output to a named output location (`nodes/`, `runs/`) — never into the dir it lives in or reads from.** The filetree is the evidence of the work. Honor it when you add anything: a script that writes next to its source is a regression.

**Why these clauses are hard (the S49 root-write near-leak):** In S49, CC wrote the groundtruth census output to **ROOT** `runs/` instead of `wallaby-way/runs/`. Root `runs/` was outside the gitignore's coverage, so the files were git-visible; a `git add .` staged them, and one render contained a **live Google OAuth credential** rendered verbatim from a corpus conv. GitHub push protection blocked the push — the only reason it was a cleanup and not a leak. Two failures stacked: CC ignored output placement, and the ignore rule didn't cover the stray path. The clauses below close the first; the gitignore now covers `wallaby-way/runs/` as the sole sanctioned run-output home.

1. **CC does not write to the repo ROOT without explicit, per-instance permission.** All work is performed and recorded under `wallaby-way/`. Root is off-limits by default; writing there requires Jake to say so for that specific task, that specific session.
2. **CC writes into the existing `wallaby-way/` directory structure.** Output goes to the appropriate standing drawer for its kind (`nodes/`, `runs/`, `scripts/`, `catalogs/` — match the artifact to the drawer). If no existing dir fits, create a new **SUBDIRECTORY** beneath the right parent (e.g. `wallaby-way/runs/<new-subdir>/`) — never a new top-level dir under `wallaby-way/`, and never anything at root.
3. **CC flags any file it produces that may contain a plaintext secret** — credentials, tokens, keys, OAuth values, connection strings — **at the time it writes the file**, in its turn output, explicitly, so OC and Jake can review and scrub before the file is staged, committed, or read into a node. Non-optional: a rendered corpus payload can carry a secret the conv author pasted, and CC is the first place that surfaces onto disk. **The floor is immutable and WILL contain secrets; the read pipeline is where they get caught.**
4. **COLLISION — one task = one window = one output dir (S51, the 176476ae double-fire).** A task's output dir belongs to exactly one executing instance. **Before any paid fire, check the task's output dir for artifacts fresher than 1 hour — if found, another instance may be live on this task → HALT** and resolve with Jake before spending. Two CC instances on one task overwrote each other's persists, broke the receipt chain, and doubled the spend. (Batch_Read_Spec v1.2 §16.)
5. **CANON HANDS — CC never edits `active/` or `wallaby-way/canon/`. Period.** Even when the text is OC-authored verbatim, routing a canon edit through CC is the WRONG HAND (two S51 occurrences; S42 precedent). Canon edits ship as OC-authored files delivered to Jake, who verifies/commits/pushes. CC's hands touch scripts, runs, nodes — never canon.

---

## Hot rules (always apply — project-specific only)

- **The floor is immortal.** 440 headers / 29,396 messages across 3 snapshots [S51 fix: was 325/24,138, 2 snapshots — superseded by the 6-9 delta freeze], append-only. NOTHING mutates it (appends via the freeze pipeline are the sanctioned growth path). A `--dry-run` reports tables EXIST; never `--execute` against the live floor.
- **Floor numbers carry their unit.** See `canon/FLOOR_COUNTS.md` (S51 interim block — a full census next session supersedes it). Never write a bare "the floor is N."
- **Denominator rule (universal, but it lives or dies here).** No bare "the corpus is read/done." Always `N of M + the named buckets`. **THE CORPUS IS CLOSED: 440/440 dispositioned — 405 read WHOLE + 30 genuine stubs (correct skips) + 3 hollow + 2 empty-confirmed** — full board in `canon/FLOOR_COUNTS.md`. [S51 fix + ADDENDUM 1: the old "202/325 read; 123 pending" breakdown is DEAD; the read phase closed when the f018b1f8 receipt landed.]
- **`Select-String` is UNTRUSTED on this corpus** — BOM/non-ASCII makes it silently skip matches (the S46 false-negative). Verify secret scrubs + content checks by **Read**, not re-grep.
- **`floor_db.env` and `anthropic_billing.env` are gitignored must-exist files — NOT leaks.** Don't flag them.
- **A $0 floor COUNT(*) is a Postgres read, not a paid API call** — it's allowed. The paid path is the Message Batches API (loads `anthropic_billing.env`). GATE every paid call with the real number next to the button.
- **`MERGE_MANIFEST_S47.md` is the node authority FOR THE S47-ERA MERGE** (202/3,743) [S51 fix: era-scoped — two of its rows (`39589260`, `5d0eba7c`) are superseded by S51 whole re-reads, see `nodes/quarantine/_SUPERSEDED_S51.md`; CURRENT pile counts live in `canon/FLOOR_COUNTS.md` (7,771 harvested-pile nodes — S51 census + the f018b1f8 receipt)]. The S37 `MANIFEST.md` is a double-count trap — banner-marked NOT-AUTHORITATIVE.
- **Node identity = `conv_uuid` + `anchor_msg` from CONTENT; filenames are NON-AUTHORITATIVE.** The pile carries two valid naming generations (bare-UUID S50 batch · `result_*`/chunk-suffixed S51) — both documented, never parsed for identity. (S51 forward rule for synthesis.)
- **The node corpus (`nodes/harvested/`) can hold literal secrets — NEVER push it.** Gitignored by design; keep it that way.

---

## The pipeline (project-specific architecture)

- **Floor** → Supabase, immutable, append-only (D9 lock). Creds in `wallaby-way/secrets/floor_db.env`.
- **Reader** → `Boot_ScopeReader` **v4.1.1** (the deployable is `test_call_system_prompt_S40.md`). Fires **Sonnet 4.6**. [OPEN: the Opus-vs-Sonnet equivalence grade is prose-asserted — locate the S40 grade artifact or treat as asserted-not-proven. The 202 are already harvested on Sonnet.]
- **Whale path** → CLOSED. 4 over-ceiling whales, 130 nodes (62M/62F/6T), route from `whale_registry.md`, NEVER re-read.
- **Harness** → `apparatus_batch_read.py` **v1.5** [S51 fix: was v1.3 — v1.5 adds the canary `--max-tokens` flag + the collect-path silent-drop fix + broadened DONE-footer check; v1.6 queued: permanent integrity check + rate constants]. Freeze pipeline `apparatus_freeze_pipeline.py` **v1.7** (scrub v2) [S51 fix: was v1.6]. Worklist `build_worklist.py` v2.1.
- **[S51 fix: the Stage-C [OPEN] line is DEAD]** — resolved as moot at the S49 census (all-fit-whole), and the S50/S51 chunk events (`3ef82921`, `176476ae`) ran the proven `chunk_whale.py` path, not Stage C. Known patch queued: `chunk_whale.py` hardcodes `d9d05961_seam_manifest` naming.

---

## On-demand references (in `canon/`, read on demand — don't load all at session start)

- **`canon/ANCHOR_apparatus.md`** (v35) [S51 fix: was a stale v33 pointer] — the authority. Banner = current state; nested banners = history (verbatim, paths describe old layouts).
- **`canon/FLOOR_COUNTS.md`** — the five floor numbers disambiguated. Cite for any floor count.
- **`canon/The_Progenitor_v5_*.md`** — the retrieval-layer pointer-catalog doctrine.
- **`canon/Batch_Read_Spec_v1.1_*.md`**, **`canon/Freeze_Pipeline_Spec_v4.md`** — pipeline build specs.
- **`nodes/manifests/MERGE_MANIFEST_S47.md`** — the node-count authority.

If a doc and the code/disk disagree: **trust disk, flag the doc** (JAKE-RULES §5.4).

---

## Historical landmines (resolved, but worth knowing)

- **"THE CORPUS IS READ" (v30–v32, killed S49).** A true count (202) narrated as a finished corpus by dropping the denominator; inherited down the relay as "done" for ~3 banner-cuts. *Lesson: every count carries N-of-M + the remainder, or it's a §5 violation.*
- **The RecruitMail secret leak (S46, closed by S48 rebuild).** A dead-project OAuth secret rode into the node corpus + git history. *Lesson: the node corpus can hold literal secrets — gitignored, never pushed; scrub verified by Read.*
- **The S46 "CORPUS CLEAN" false-negative.** `Select-String` silently skipped a `GOCSPX-` secret (encoding), then the miss was rationalized as an "older-format" secret. *Lesson: a clean verdict names its surface + method; `Select-String` is untrusted here.*
- **The "206" double-count (lived 8 sessions).** A pre-run estimate corrected only in a later CHANGELOG entry, left live in the old one. *Lesson: correct in place, not only downstream.*

---

## Per-project lessons (tasks/lessons.md)

Maintain `wallaby-way/tasks/lessons.md` as the running per-project lessons file (distinct from the universal CHANGELOG — lessons tracks WHY a thing broke + the pattern that prevents recurrence). After ANY correction from Jake, append the lesson. Format:
```
## [date] — [short title]
**What happened:** [one sentence]
**Root cause:** [one sentence]
**Pattern that prevents recurrence:** [the rule born from the pain]
```

---

## When in doubt

Disk is ground truth over any doc. If docs and disk disagree: trust disk, flag the doc. If you're unsure whether something is in scope, paste a short summary back to Jake — he'll relay to OC if orchestration weighs in.

---

*Repo orientation. Update when working norms change. Last updated: 6-10-26, apparatus S51 "Continuance" REF-EDIT (added the COLLISION + CANON-HANDS rules; corrected stale floor/read/version pointers in place per the S50 handoff §6 queue). Prior: 6-9-26 S49 "Concord" (CC output-discipline clauses); 6-8-26 first cut (TWW CCC S3).*
