# FLOOR_COUNTS.md — the corpus-state bible (floor + read counts, every number sourced)

> **★ S51 INTERIM BLOCK — TEMPORARY BY DESIGN.** This update reflects the S51 census (`runs/node_census_S51/census.md`) and the S51 re-read wave. **A full floor census + file manifest next session SUPERSEDES this block.** Numbers here are the best disk/floor-confirmed state as of 2026-06-10; treat the next census as authoritative when it lands.

**The floor has been stated as multiple different numbers across the lineage, each counting a different thing.** A bare "the floor is N" is the conflation fuse — the same defect class as "the corpus is read." This is the single source. Cite it; never re-derive a floor count from memory or from a banner.

**This file carries both the floor-side and the read-side counts** — it is THE single place any session checks "where does the corpus stand." Same rule for every number here: cite it, never re-derive a count from memory or a banner.

*Floor-side updated S51 (post 6-9 delta freeze, confirmed by S51 census). Read-side replaced wholesale at S51 from the post-re-read-wave census. Prior S49 state (325/24,138, READ 202/3,743) is superseded — see CHANGELOG S50/S51 entries for the lineage.*

---

## The current floor invariant

**`440 headers / 29,396 messages` across 3 snapshots.** [S51 fix: was `325 headers / 24,138 messages` across 2 snapshots — superseded by the 6-9 delta freeze, S50.] When a doc cites "the floor," it means these two numbers unless it explicitly says otherwise.

| # | Number | What it counts | Confirmed from |
|---|---|---|---|
| 1 | **22,801** | Raw message rows in the **baseline** export snapshot (`baseline-2026-05-25-ae015455`) | snapshot ledger `message_count` (unchanged from S49) |
| 2 | **23,095** | Total **baseline** rows in the floor — 294 baseline headers + 22,801 baseline messages | ledger math (unchanged from S49) |
| 3 | **29,396** | Total **message** rows in the floor, **across all 3 snapshots** — the production floor message count | S51 census [S51 fix: was 24,138 / 2 snapshots] |
| 4 | **29,836** | Total rows **across all floor tables** — 440 headers + 29,396 messages | *derived: 440 + 29,396 — arithmetic, not a live-query receipt; next census confirms* [S51 fix: was 24,463] |
| 5 | **440** | Distinct **conversation header** rows — one per unique conv across all 3 snapshots | S51 census [S51 fix: was 325] |

---

## How the snapshots add up

- **Baseline** (`baseline-2026-05-25-ae015455`): 294 headers + 22,801 messages.
- **Delta 1** (`delta-2026-05-28-a61498e6`): 31 net-new headers + 1,337 messages.
- **Delta 2** (`delta-2026-06-09-2748278f`): 115 net-new headers + 5,258 messages (frozen S50 under scrub v2; zero deletions, zero trigger rejections, Stage 3 verify-clean — S50 handoff).
- **440 headers** = 294 + 31 + 115. **29,396 messages** = 22,801 + 1,337 + 5,258. The math closes.

**The delta-1 34-vs-31 wrinkle (kept from S49):** the 5-28 delta *export* contained 34 conversations, but only **31 were net-new headers** — the other 3 were continuations of baseline convs (added messages, not headers). If you see "34" anywhere, it's the raw export, not the floor.

**Continuation convs are a standing structural fact, not a wrinkle:** a conv can hold messages in MORE THAN ONE snapshot. This is exactly what the S50 snapshot-boundary bug exposed (`floor_extract.py` rendered only one snapshot per conv → silent partial reads). The S51-patched extractor renders ALL snapshots deduped on `msg_uuid` (highest scrub version, ordered `created_at`). Any read-side claim about a multi-snapshot conv must pass the integrity check (payload msgs vs floor msgs) before it counts WHOLE.

---

## The read-side disposition board (S51 census — the 440, every conv dispositioned)

Source: `runs/node_census_S51/census.md` + the S51 re-read wave (batch `msgbatch_0141kqFFbKmiuMs3VQpnBcEX`, 15 requests / 15 succeeded / 14 persisted / f018b1f8 quarantined-then-RESOLVED via the proven defang path; integrity checks 11/11; 176476ae density-bounced pre-fire at 1,096,220 tok @ ×0.72 > 1M and read via the chunk path instead).

| Bucket | N | Disposition |
|---|---|---|
| Read WHOLE — `nodes/harvested/` | **397 convs** | 400 files (3ef82921 ×2 + 176476ae ×3 chunk files + f018b1f8; all other convs 1 file each) [ADDENDUM-1 fix: was 396/399 — f018b1f8 receipt landed: read via the PROVEN defang path, 1 block cut (2,982 B), end_turn, 17 nodes, $1.55, persisted + harvested] |
| Read WHOLE — S33-era whale convs, `nodes/catalogs/` | **8 convs** | the original whale pool, counted separately (below) |
| **READ WHOLE subtotal** | **405** | |
| Genuine stubs | **30** | read, zero-node catalogs — CORRECT SKIPS, counted in any completion claim |
| Hollow stubs | **3** | zero messages, never submitted (skeleton-gate exclusions: `3f84a335`, `ae3468be`, `bc42e9ab`) |
| EMPTY-CONFIRMED | **2** | `d2cd71e3` (9 msgs), `d85b4100` (18 msgs) — `content_blocks` null at floor level, verified S51 with the patched extractor; nothing to read |
| **Total** | **440** | ✓ |

**THE CORPUS IS CLOSED: 440/440 dispositioned — 405 read WHOLE + 30 genuine stubs (correct skips) + 3 hollow + 2 empty-confirmed.** [ADDENDUM-1: the f018b1f8 receipt landed; the read phase of the apparatus is complete, denominator whole.] A completion claim still always carries this full board, never a bare "done".

---

## The node counts

| Count | Value | What it counts | Confirmed from |
|---|---|---|---|
| Harvested-pile nodes | **7,771** | salience nodes in `nodes/harvested/` (incl. the 185 harvest-4a nodes + f018b1f8's 17) | S51 census 7,754 (`runs/node_census_S51/census.md`) + f018b1f8's 17 (receipt, `runs/defang_f018b1f8_S51/`) |
| — MOTION | 4,408 | *derived: 4,399 census + 9 f018b1f8* | same |
| — FENCE | 3,197 | *derived: 3,189 census + 8 f018b1f8* | same |
| — TEXTURE | 166 | *(f018b1f8 added 0T)* | same |
| S33-catalog nodes | **517** | the 8 original whale convs in `nodes/catalogs/` — counted separately by design | existing canon (S49 read-side block / `MERGE_MANIFEST_S47.md`); not re-derived at S51 |

The combined pile (7,771 + 517 = 8,288) is a *derived sum across two separately-counted pools* — cite the pools, not the sum, until the next full census unifies them.

**Naming-generation note (load-bearing for synthesis):** the harvested pile carries TWO valid filename generations — bare-UUID files (S50 batch) and `result_*` / chunk-suffixed files (S51). Both are documented and valid. **Node identity = `conv_uuid` + `anchor_msg` from CONTENT; filenames are NON-AUTHORITATIVE and are never parsed for identity.**

---

## The rule this doc enforces (JAKE-RULES §5.1)

No floor or corpus count is ever stated bare. It carries its unit (`messages` / `headers` / `records` / `baseline` / `snapshot`) and, when it matters, links here. A true number with its frame stripped is the poison; the frame is non-optional.

---

*Last updated: 6-10-26, apparatus S51 "Continuance" REF-EDIT + ADDENDUM 1 (S51 INTERIM — floor 440/29,396 across 3 snapshots; THE CORPUS CLOSED at 440/440 dispositioned, f018b1f8 receipt landed; nodes 7,771 harvested + 517 S33-catalog; THIS BLOCK IS TEMPORARY — the full floor census + file manifest next session supersedes it). Prior: 6-9-26 S49 "Concord" (read-side added, became the corpus-state bible); floor-side originally authored TWW CCC S3.*
