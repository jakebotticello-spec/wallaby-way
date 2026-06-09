# CLAUDE.md — The Wallaby Way (the apparatus)

**For Claude Code working in this repo. Read this first, every session.**

> **Universal rules** (Brothers Clause, communication, building, debugging, the denominator rule, etc.) live in:
> `@C:/claude-reference/active/JAKE-RULES.md`
>
> This file is project-specific only. If something belongs everywhere, it goes in JAKE-RULES.md, not here.

---

## What this is

The Wallaby Way (the "apparatus") — Jake's **auxiliary brain**: a corpus-processing pipeline that reads ~325 Claude conversations into an immutable floor, harvests them into a flat pointer-pile of salience nodes, and (eventually) serves them through a retrieval engine. It is NOT a deployed web app — there is no server, no frontend, no deploy target. It is a Supabase floor + a Python batch-read pipeline + a node corpus on disk. Read *The Wallaby Why*, *Track Meet Doctrine*, and *The Wallaby Whales* as **framework** (the breadth IS the function; the record is verbatim) before working — they are posture-setting, not reference.

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
│   │   ├── harvested/               ← the node corpus (194 uuid.md + .parents.json sidecars) — GITIGNORED
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

## Output discipline (load-bearing — the rule that keeps the tree honest)

**Source data is read-only to tooling. Every script writes its output to a named output location (`nodes/`, `runs/`) — never into the dir it lives in or reads from.** The filetree is the evidence of the work. Honor it when you add anything: a script that writes next to its source is a regression.

---

## Hot rules (always apply — project-specific only)

- **The floor is immortal.** 325 headers / 24,138 messages, append-only. NOTHING mutates it. A `--dry-run` reports tables EXIST; never `--execute` against the live floor.
- **Floor numbers carry their unit.** Five legit numbers exist — see `canon/FLOOR_COUNTS.md`. Never write a bare "the floor is N."
- **Denominator rule (universal, but it lives or dies here).** No "the corpus is read/done." Always `N of M + named remainder`. The corpus is **202/325 read; 123 pending** (73 chunk-later + 22 delta + 28 hollow).
- **`Select-String` is UNTRUSTED on this corpus** — BOM/non-ASCII makes it silently skip matches (the S46 false-negative). Verify secret scrubs + content checks by **Read**, not re-grep.
- **`floor_db.env` and `anthropic_billing.env` are gitignored must-exist files — NOT leaks.** Don't flag them.
- **A $0 floor COUNT(*) is a Postgres read, not a paid API call** — it's allowed. The paid path is the Message Batches API (loads `anthropic_billing.env`). GATE every paid call with the real number next to the button.
- **`MERGE_MANIFEST_S47.md` is THE node authority** (202/3,743). The S37 `MANIFEST.md` is a double-count trap — banner-marked NOT-AUTHORITATIVE.
- **The node corpus (`nodes/harvested/`) can hold literal secrets — NEVER push it.** Gitignored by design; keep it that way.

---

## The pipeline (project-specific architecture)

- **Floor** → Supabase, immutable, append-only (D9 lock). Creds in `wallaby-way/secrets/floor_db.env`.
- **Reader** → `Boot_ScopeReader` **v4.1.1** (the deployable is `test_call_system_prompt_S40.md`). Fires **Sonnet 4.6**. [OPEN: the Opus-vs-Sonnet equivalence grade is prose-asserted — locate the S40 grade artifact or treat as asserted-not-proven. The 202 are already harvested on Sonnet.]
- **Whale path** → CLOSED. 4 over-ceiling whales, 130 nodes (62M/62F/6T), route from `whale_registry.md`, NEVER re-read.
- **Harness** → `apparatus_batch_read.py` v1.3, BUILT + fired (181/177 clean). Freeze pipeline `apparatus_freeze_pipeline.py` v1.6. Worklist `build_worklist.py` v2.1.
- **[OPEN] Stage C** (overlapping-window chunking for the 73 unread big convs) — built-vs-not is UNRESOLVED; gates any read of the 73. Decide dead-or-deferred before spending.

---

## On-demand references (in `canon/`, read on demand — don't load all at session start)

- **`canon/ANCHOR_apparatus.md`** (v33) — the authority. Banner = current state; nested banners = history (verbatim, paths describe old layouts).
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

*Repo orientation. Update when working norms change. Last updated: 6-8-26, S49 (authored — first cut, post-uncrappening).*
