# FLOOR_COUNTS.md — the corpus-state bible (floor + read counts, every number sourced)

> **★ CENSUS OF RECORD — 2026-06-10, parallel track "Tally".** Every figure in this file was **re-derived from the live floor and disk** in the post-S51 full census — nothing inherited, then reconciled three-way against the S51 interim, ANCHOR v35, and the CHANGELOG S51 entry. $0, read-only end to end. Raw receipts: `wallaby-way/runs/floor_census_2026-06-10/` (census_A_floor_raw.md · census_B_manifest_raw.md · census_C_followup_raw.md · check_4788ce54.py). The S51 interim block this replaces is retired; its full text survives in git history.

**The floor has been stated as multiple different numbers across the lineage, each counting a different thing.** A bare "the floor is N" is the conflation fuse — the same defect class as "the corpus is read." This is the single source. Cite it; never re-derive a floor count from memory or from a banner.

**This file carries the floor-side counts, the read-side counts, AND (new at this census) the disk file manifest** — it is THE single place any session checks "where does the corpus stand." Same rule for every number here: cite it, never re-derive a count from memory or a banner.

---

## The current floor invariant

**`440 headers / 29,396 messages` across 3 snapshots, in exactly 2 floor tables.** When a doc cites "the floor," it means these two numbers unless it explicitly says otherwise. All census-confirmed live 2026-06-10.

| # | Number | What it counts | Confirmed from |
|---|---|---|---|
| 1 | **22,801** | Raw message rows in the **baseline** snapshot (`baseline-2026-05-25-ae015455`) | census A3, live |
| 2 | **23,095** | Total **baseline** rows — 294 baseline headers + 22,801 baseline messages | arithmetic on census A3 live counts |
| 3 | **29,396** | Total **message** rows in the floor, across all 3 snapshots | census A2, live |
| 4 | **29,836** | Total rows **across all floor tables** — 440 headers + 29,396 messages | **census A0b, LIVE-QUERY RECEIPT** (the interim's "arithmetic, not a receipt" caveat is retired; schema discovery confirms exactly 2 tables exist: `floor_conv_headers`, `floor_conv_messages`) |
| 5 | **440** | Conversation header rows — **and 440 distinct conv_uuids: one header row per conv, proven** | census A1, live |
| 6 | **29,396** | **Distinct msg_uuids** — zero duplicate messages in the floor | census A2, live (new receipt at this census) |
| 7 | **437** | Distinct conv_uuids carrying messages — 440 headers − the 3 hollow (zero-message) convs | census A2 + A7, live |

---

## How the snapshots add up

| Snapshot | Headers | Messages | scrub_version |
|---|---|---|---|
| `baseline-2026-05-25-ae015455` | 294 | 22,801 | **v2** (all rows) |
| `delta-2026-05-28-a61498e6` | 31 | 1,337 | **v1** (all rows — see the open disposition below) |
| `delta-2026-06-09-2748278f` | 115 | 5,258 | **v2** (all rows) |
| **Total** | **440** | **29,396** | |

**440 = 294 + 31 + 115. 29,396 = 22,801 + 1,337 + 5,258. The math closes, live.** Snapshot IDs are identical across both tables (census A4; symmetric difference empty).

**The delta-1 34-vs-31 wrinkle (kept from S49):** the 5-28 delta *export* contained 34 conversations, but only **31 were net-new headers** — the other 3 were continuations of baseline convs (added messages, not headers). If you see "34" anywhere, it's the raw export, not the floor.

**★ OPEN DISPOSITION — delta-1 scrub version (new fact at this census):** delta-1 sits **entirely at scrub_v1** — both its 31 headers and all 1,337 messages. Baseline and delta-2 are fully v2. The scrub-v2 secret-pattern classes (GOCSPX/GitHub/AWS/JWT, proven S50) have **never run against the delta-1 slice**. No prior canon figure is contradicted (no scrub distribution was ever recorded); the fact is simply now on the record. Ruling needed: a v2 overlay pass for delta-1, or an explicit accept. Carried in ANCHOR v36 NEXT.

**Continuation convs are a standing structural fact, not a wrinkle:** a conv can hold messages in MORE THAN ONE snapshot. Census-verified: **exactly 12 convs span 2 snapshots** (census A6) — uuid-for-uuid the S51 blast-radius set, no more, no fewer:

`176476ae` · `2526703b` · `39589260` · `5d0eba7c` · `6cabbba6` · `70ec4abb` · `955cce09` · `a7796a13` · `c00ef343` · `c33596c3` · `cda6d5d1` · `fcbd24fa`

Header-side multi-snapshot rows: **0** — a continuation conv keeps its single header at its first-seen snapshot, by design, now floor-proven. The census header-vs-actual check (A8) found header.message_count ≠ actual distinct messages for **exactly these 12 and no others**, every fraction matching the quarantine ledgers digit-for-digit (incl. c00ef343's 1/37). The S51-patched extractor (ALL snapshots, deduped on `msg_uuid`, highest scrub version, ordered `created_at`) remains mandatory; any read-side claim about a multi-snapshot conv must pass the integrity check (payload msgs vs floor msgs) before it counts WHOLE.

**Floor hygiene (census A7):** headers with zero messages: **3** — exactly the hollow-stub uuids (`3f84a335`, `ae3468be`, `bc42e9ab`). Orphan messages (no header anywhere): **0**.

---

## The read-side disposition board (the 440, every conv dispositioned — board unchanged from S51, file-side now census-receipted)

| Bucket | N | Disposition |
|---|---|---|
| Read WHOLE — `nodes/harvested/` | **397 convs** | **400 .md files, census-confirmed:** 391 bare-UUID files + 9 `result_*` files (176476ae ×3 chunks · 3ef82921 ×2 chunks · 82bbd8f1 · a8bf895f · ce1e79e1 · f018b1f8); 397 convs = 395 single-file + 2 chunked |
| Read WHOLE — S33-era whale convs, `nodes/catalogs/` | **8 convs** | 21 S33-era files, census-confirmed (counted separately, below) |
| **READ WHOLE subtotal** | **405** | |
| Genuine stubs | **30** | read, zero-node catalogs — CORRECT SKIPS, counted in any completion claim |
| Hollow stubs | **3** | zero messages — **floor-confirmed at this census** (`3f84a335`, `ae3468be`, `bc42e9ab` = exactly the zero-message headers) |
| EMPTY-CONFIRMED | **2** | `d2cd71e3` (9 msgs), `d85b4100` (18 msgs) — `content_blocks` null at floor level (S51, patched extractor); rows exist, consistent with census A8's silence on both |
| **Total** | **440** | ✓ |

**THE CORPUS IS CLOSED: 440/440 dispositioned — 405 read WHOLE + 30 genuine stubs (correct skips) + 3 hollow + 2 empty-confirmed.** A completion claim always carries this full board, never a bare "done".

---

## The node counts (both pools census-grade as of 2026-06-10)

| Count | Value | What it counts | Confirmed from |
|---|---|---|---|
| Harvested-pile nodes | **7,771** | salience nodes in `nodes/harvested/` | **census-confirmed per-file**: C1 per-file diff vs `runs/node_census_S51/census.md` — 399 files identical + f018b1f8's 17; the lone mismatch resolved (see the method rule below) |
| — MOTION | 4,408 | *derived: 4,399 census + 9 f018b1f8* | S51 census + defang receipt |
| — FENCE | 3,197 | *derived: 3,189 census + 8 f018b1f8* | same |
| — TEXTURE | 166 | *(f018b1f8 added 0T)* | same |
| S33-catalog nodes | **517** | the 8 original whale convs in `nodes/catalogs/` — counted separately by design | **LIVE-RECEIPTED at this census** (first re-derivation since the S33 era): 593 raw across the 21 S33-era files − 76 in the two `confirm_*_whole` alternate renderings = 517 exact (census C3) |
| Combined | 8,288 | both pools | both pools are now census-grade; still cite the pools, not the sum |

**★ THE NODE-COUNT METHOD RULE (earned at this census):** a node is the **line-anchored** `**Salience:** <TAG>` header — regex `^\*\*Salience:\*\*\s+\w+` with MULTILINE. **Naive substring counts of the literal marker OVER-COUNT**: `4788ce54-db10-4c41-862f-a491d0517e8d.md` carries one inline literal `**Salience:**` inside node content (naive 25 vs anchored 24, settled by a discriminating test on the live file). Any future node count uses the anchored regex or it isn't a node count.

**The S33 pool decomposition (census C3, per-conv):** 48b4110a chunks **145** · ea900330 chunks **167** · 492e164b **47** · 55217328 **15** · 83506215 **28** · cfc7a70a **23** · d6e23963 **28** · d9d05961 chunks **64** — sum **517**. The two `confirm_*_whole` files (48b4110a whole 36 · ea900330 whole 40) are alternate whole-conv renderings, **excluded from the count as superseded alternates** — and 48b4110a's whole=36 vs chunks=145 is the input-length-degrades-the-reader finding (S51's role-break resolution), visible in fossil form.

**Naming-generation note (load-bearing for synthesis):** the harvested pile carries TWO valid filename generations — bare-UUID files (S50 batch) and `result_*` / chunk-suffixed files (S51). Both are documented and valid. **Node identity = `conv_uuid` + `anchor_msg` from CONTENT; filenames are NON-AUTHORITATIVE and are never parsed for identity.**

---

## The disk file manifest (new at this census — census B, corrected pairing census C4)

| Location | Count | Composition |
|---|---|---|
| `nodes/harvested/` | **806 files** | **400 .md + 400 `.md.parents.json` sidecars (pairing 400/400 clean, receipted at C4) + 6 `.stale_S50` strays** (see the open disposition below) |
| `nodes/catalogs/` | **39 files** | **21 S33-era** (confirm_48b4110a ×8 · confirm_ea900330 ×6 · 5 single results · result_d9d05961 ×2 — the 8 S33 whale convs) **+ 18 S51-era** (the 9 `result_*` .md + 9 sidecars — mirrors of the harvested copies, harvest-4a/whale-lane provenance; NOT double-counted: nodes are counted from `harvested/` only) |
| `nodes/quarantine/` | **70 files** | **46 corpses + 22 partial-move files + 2 ledgers.** The 22 match `_PARTIAL_MOVES_S51.md` row-for-row (all 11 uuid pairs present); every artifact named in `_SUPERSEDED_S51.md` is present (the 7 resolved corpses, c00ef343, f018b1f8, 3ef82921, `_RESOLVED_567956f0`) |
| `nodes/manifests/` | **2 files** | `MANIFEST.md` · `MERGE_MANIFEST_S47.md` |
| `runs/` | 14 dirs + 3 root files | incl. `floor_census_2026-06-10/` (this census's receipts) and `node_census_S51/` (the S51 node-census receipts) |
| `graveyard/` (repo root) | present | turd payload pair + 5 dirs + 1 file — labeled-dead, gitignored wholesale |

**★ OPEN DISPOSITION — the six `.stale_S50` strays (new fact at this census):** `nodes/harvested/` holds renamed pairs for **3 convs** — `955cce09`, `cda6d5d1`, `fcbd24fa` (`.md.stale_S50` + `.md.parents.json.stale_S50` each) — covered by **NEITHER S51 quarantine ledger**. The `_PARTIAL_MOVES_S51` ledger records those 3 convs' partials as moved to quarantine, and quarantine does hold them — so these are a third artifact set. Provenance guess: an S50-era rename-in-place flag step that preceded the S51 move, leaving the renamed originals behind for these 3. Data-safe (the canonical S51 re-reads are separate files, counted clean), but the pile carries 6 unledgered strays until the apparatus rules: relocate + ledger line, or label-in-place. Carried in ANCHOR v36 NEXT.

---

## Census provenance

- **Who/when:** TWW parallel track "Tally", 2026-06-10. Commissioned by the S51 interim block as its replacement.
- **How:** floor via read-only SELECTs (`floor_census_A.py` — read-only session, billing-guarded, $0); disk via Python structural reads (`file_manifest_B.py`, `census_followup_C.py`, `check_4788ce54.py`) — no pattern-matching against `nodes/` or `runs/` contents; the only content reads were the sanctioned Salience-marker counts and verbatim prints of the two OC-authored quarantine ledgers + the S51 node-census receipts.
- **Receipts:** `wallaby-way/runs/floor_census_2026-06-10/` — `census_A_floor_raw.md`, `census_B_manifest_raw.md`, `census_C_followup_raw.md`, plus the scripts. Every number above traces to a line in those files.
- **Reconciliation:** three-way vs the S51 interim FLOOR_COUNTS, ANCHOR v35, and the CHANGELOG S51 entry. All majors matched; the two non-matches were resolved (the 7,772 naive over-count → method rule; the 593 raw S33 total → the whole-file decomposition) and the two new facts were dispositioned-open (stale_S50 strays; delta-1 scrub_v1). One census-script defect (the Part-B pairing stem bug) was owned by Tally, corrected, and re-receipted clean at C4.

---

## The rule this doc enforces (JAKE-RULES §5.1)

No floor or corpus count is ever stated bare. It carries its unit (`messages` / `headers` / `records` / `baseline` / `snapshot`) and, when it matters, links here. A true number with its frame stripped is the poison; the frame is non-optional.

---

*Last updated: 6-10-26, TWW parallel track "Tally" — THE FULL FLOOR CENSUS (census of record; supersedes the S51 interim block; every figure re-derived $0 from the live floor + disk; receipts `runs/floor_census_2026-06-10/`; two dispositions open: the stale_S50 strays + the delta-1 scrub_v1 slice). Prior: 6-10-26 apparatus S51 "Continuance" REF-EDIT + ADDENDUM 1 (S51 interim); 6-9-26 S49 "Concord" (read-side added, became the corpus-state bible); floor-side originally authored TWW CCC S3.*
