# FLOOR_COUNTS.md — the corpus-state bible (floor + read counts, every number sourced)

> **★ CENSUS OF RECORD — 2026-06-10, parallel track "Tally" · ★ RECUT S52 "Catechism" (same day): the scrub-v3 overlay landed and the floor's row-shape changed by design.** Every Tally figure was re-derived live ($0, read-only; receipts `wallaby-way/runs/floor_census_2026-06-10/`). The S52 recut adds the v3 overlay facts (receipts `wallaby-way/runs/floor_overlay_v3_S52/` — dry_run_audit.md · dry_run_map.jsonl · execute_log.md · verify.md, 7/7 PASS) and closes both census dispositions. Prior text survives in git history.

**The floor has been stated as multiple different numbers across the lineage, each counting a different thing.** A bare "the floor is N" is the conflation fuse. **As of S52 the fuse has a second wire: ROWS ≠ MESSAGES.** The overlay doubled the message-row count without adding a single message. Any count that *means* messages is `COUNT(DISTINCT msg_uuid)` — always, everywhere, no exceptions. This is the single source. Cite it; never re-derive a floor count from memory or a banner.

---

## The current floor invariant

**`440 headers / 29,396 messages (distinct) / 58,792 message rows` across 3 snapshots × 2 scrub editions, in exactly 2 floor tables.** When a doc cites "the floor," it means `440 / 29,396` unless it explicitly says rows. All v3 figures verified live 2026-06-10 (verify.md V1–V7, 7/7 PASS).

| # | Number | What it counts | Confirmed from |
|---|---|---|---|
| 1 | **29,396** | **Distinct messages** in the floor (`COUNT(DISTINCT msg_uuid)`) — unchanged by the overlay | verify V3, live |
| 2 | **58,792** | Total **message rows** — every message exists in exactly 2 editions: its pre-v3 row + its v3 row | verify V4, live |
| 3 | **59,232** | Total rows **across all floor tables** — 440 headers + 58,792 messages | arithmetic on verify V4 + census A1 |
| 4 | **440** | Conversation header rows — one header per conv, 440 distinct conv_uuids (headers were NOT overlaid; S20 ruling: pure metadata, no scrub_walk) | census A1, live |
| 5 | **29,396** | v3 message rows — exactly one per message, full coverage proven | verify V1, live |
| 6 | **437** | Distinct conv_uuids carrying messages — 440 − the 3 hollow | census A2 + A7 |

**★ RETIRED RECEIPT (by design, not by error):** Tally's receipt #6 — "29,396 distinct msg_uuids = zero duplicate messages, one row each" — described the pre-overlay floor and is **retired as of the S52 execute**. Row identity is now `(snapshot_id, conv_uuid, msg_uuid, scrub_version)`, **PK-enforced** (4-column PK landed S52; preflight clean — 0 FKs, 0 views, 0 dependents; immutability triggers unaffected; duplicate-tuple rejection proven, verify V7). A cold reader applying the old receipt will double-count; a cold reader applying `COUNT(DISTINCT msg_uuid)` cannot.

---

## How the snapshots add up (messages are distinct counts; rows = messages × 2)

| Snapshot | Headers | Messages | Rows | Pre-v3 edition | v3 edition |
|---|---|---|---|---|---|
| `baseline-2026-05-25-ae015455` | 294 | 22,801 | 45,602 | v2 *(S20 synthetic drill lineage — see scrub history)* | v3, full |
| `delta-2026-05-28-a61498e6` | 31 | 1,337 | 2,674 | v1 | v3, full |
| `delta-2026-06-09-2748278f` | 115 | 5,258 | 10,516 | v2 *(production-at-ingest, S50)* | v3, full |
| **Total** | **440** | **29,396** | **58,792** | | **29,396 (verify V2: 22,801 / 1,337 / 5,258 exact)** |

**440 = 294 + 31 + 115. 29,396 = 22,801 + 1,337 + 5,258. 58,792 = 2 × 29,396. The math closes, live.**

**The delta-1 34-vs-31 wrinkle (kept from S49):** the 5-28 *export* contained 34 convs; 31 were net-new headers, 3 were continuations of baseline convs. "34" anywhere = the raw export, never the floor.

**Continuation convs (standing structural fact):** exactly **12** convs span 2 snapshots (census A6, uuid list unchanged): `176476ae` · `2526703b` · `39589260` · `5d0eba7c` · `6cabbba6` · `70ec4abb` · `955cce09` · `a7796a13` · `c00ef343` · `c33596c3` · `cda6d5d1` · `fcbd24fa`. The S51-patched extractor (ALL snapshots, deduped on `msg_uuid`, **highest scrub version** — which is now v3 everywhere, ordered `created_at`) remains mandatory; integrity checks count `COUNT(DISTINCT msg_uuid)` (runner v1.6 bakes this in permanently).

**Floor hygiene (census A7, unchanged):** 3 zero-message headers = the 3 hollow stubs (`3f84a335`, `ae3468be`, `bc42e9ab`); 0 orphan messages.

---

## ★ THE SCRUB HISTORY — one version label per pattern set, finally (S52)

**THE LINE OF RECORD: the floor was uniformly screened at scrub-v3 — 13 classes, all three snapshots, all 29,396 messages — on 2026-06-10, S52.** Surface named precisely: this line covers the FLOOR's message content. The pile carries its own same-day verdict (shrapnel section below).

| Version | What it actually was | Coverage |
|---|---|---|
| v1 | original 5 classes (RTSP/postgres/anthropic/openai/stripe), at freeze | baseline + delta-1 at their freezes |
| "v2" — S20 lineage | **SYNTHETIC ratify-drill** — redacted the literal token `EXAMPLE` (3 hits) to prove the overlay machinery; NOT a production pass | baseline only |
| "v2" — S50 lineage | **production**: v1 + 5 secret classes (GOCSPX/GitHub/AWS/JWT et al.), pipeline v1.7 at ingest, 264 redactions | delta-2 only |
| **v3** | **THE DEFINITIVE SET — 13 classes: the 10 v1.7 production classes + 3 Supabase classes** (`sb_secret_` / `sb_publishable_` / project-ref URLs — the S37 flag-#4 queue item, CLOSED) | **whole floor, appended S52: 29,396 v3 rows, 1,346 redactions** (51 google_oauth · 174 google_refresh · 882 jwt · 2 sb_secret · 15 sb_pub · 222 sb_ref_url · 0 across the other seven), dry-run vs landed deltas all zero, 20-row sample 0 survivors |

The pre-S52 "v2" label meant **two different pattern sets** depending on snapshot — the label collision is why the v3 pass ran floor-wide rather than delta-1-only (Jake's "no more guesswork" ruling, S52). The empirical confirmation is in the dry-run audit: baseline carried ~1,100+ unredacted v2-production-class strings, exactly as the S20 receipts predicted.

**★ STANDING RULE FOR THE NEXT FREEZE:** `apparatus_freeze_pipeline.py` must ship **v1.8 with SCRUB_VERSION=3 (the 13-class set) BEFORE the next delta freezes**, or the new delta lands beneath the uniform line and the LINE OF RECORD breaks. Carried in ANCHOR v37 NEXT.

---

## The read-side disposition board (unchanged — 440/440, file-side census-receipted)

| Bucket | N | Disposition |
|---|---|---|
| Read WHOLE — `nodes/harvested/` | **397 convs** | 400 .md files (391 bare-UUID + 9 `result_*`); 395 single-file + 2 chunked |
| Read WHOLE — S33-era whale convs, `nodes/catalogs/` | **8 convs** | 21 S33-era files, counted separately |
| **READ WHOLE subtotal** | **405** | |
| Genuine stubs | **30** | zero-node catalogs, correct skips |
| Hollow stubs | **3** | zero messages, floor-confirmed |
| EMPTY-CONFIRMED | **2** | `d2cd71e3`, `d85b4100` — content_blocks null at floor level |
| **Total** | **440** | ✓ |

**THE CORPUS IS CLOSED: 440/440 — 405 + 30 + 3 + 2. A completion claim always carries this full board, never a bare "done."**

**★ NEW RECEIPT (S52): delta-1 dispositioned at uuid level** — all 31: 23 harvested (headers read verbatim on 3) + 7 genuine stubs (`.quarantined.md` confirmed, incl. the all-blank 8-msg `7f6c3654`) + 1 empty-confirmed (`d85b4100`) + 0 hollow + 0 whale. Reconciles bucket-for-bucket against this board. Receipt: `runs/recon_S52/delta1_disposition_map.md`. Delta-1 is corpus, co-equal, proven read (Jake's legitimacy ruling + the map, S52).

---

## The node counts (both pools census-grade; unchanged by S52)

| Count | Value | Notes |
|---|---|---|
| Harvested-pile nodes | **7,771** | 4,408 MOTION / 3,197 FENCE / 166 TEXTURE |
| S33-catalog nodes | **517** | counted separately by design (593 raw − 76 confirm_*_whole alternates) |
| Combined | 8,288 | cite the pools, not the sum — **cross-receipt: the S52 retrieval-probe structural index parsed 8,288/8,288 using the anchored-regex node definition** (`runs/retrieval_probe_S52/index_counts.md`) |

**THE NODE-COUNT METHOD RULE stands:** a node is the line-anchored `**Salience:** <TAG>` header (`^\*\*Salience:\*\*\s+\w+`, MULTILINE). Naive substring counts over-count. **Node identity = conv_uuid + anchor_msg from CONTENT; filenames are NON-AUTHORITATIVE** (two naming generations, both valid).

**★ PILE SHRAPNEL VERDICT (S52):** all 118 convs the v3 dry-run flagged as carrying floor redactions were scanned against the 13 v3 classes — **111 harvested catalogs + 7 S33 whale-catalog convs = 118/118 dispositioned, ZERO shrapnel, 0 encoding issues.** One-time scripted scan sanctioned by Jake (ruling recorded verbatim in the report header); Python `re` only, counts-only output. Receipt: `runs/recon_S52/shrapnel_report.md`. The pile predates v3 and is independently clean against it.

**★ INJECTION SPOT-CHECK CLOSED (S52):** 3 ignition-led piled convs (`b029b9e7` · `b70dfd5c` · `84a2e51c`) — 3/3 CLEAN on all signals. The S51 judgment-ledger expectation confirmed. Receipt: `runs/recon_S52/injection_spotcheck.md`.

---

## The disk file manifest (census B/C4 baseline, updated S52)

| Location | Count | Composition |
|---|---|---|
| `nodes/harvested/` | **800 files** | 400 .md + 400 sidecars, pairing clean, **0 strays** (the 6 `.stale_S50` relocated S52) |
| `nodes/catalogs/` | **39 files** | 21 S33-era + 18 S51-era mirrors (not double-counted) |
| `nodes/quarantine/` | **77 files** | 46 corpses + 22 partial-move files + **6 `.stale_S50` strays (moved S52)** + 3 ledgers (`_PARTIAL_MOVES_S51` · `_SUPERSEDED_S51` · **`_STALE_S50_MOVES_S52`**) |
| `nodes/manifests/` | **2 files** | unchanged |
| `runs/` | 18 dirs + 3 root files | census 14 + S52's four: `floor_overlay_v3_S52/` · `recon_S52/` · `retrieval_probe_S52/` · `tool_pass_S52/` |
| `graveyard/` | present | unchanged, gitignored wholesale |

**★ DISPOSITION CLOSED (was open at the census): the six `.stale_S50` strays** — confirmed S50-era rename-in-place artifacts for `955cce09` / `cda6d5d1` / `fcbd24fa` (canonical S51 re-reads verified separate, multi-snapshot counts intact), relocated to quarantine with ledger, post-op counts exact. Receipt: the ledger + `runs/recon_S52/`.

**★ DISPOSITION CLOSED (was open at the census): the delta-1 scrub_v1 slice** — superseded by the floor-wide v3 overlay (scrub history above). No slice of the floor sits below v3.

---

## Census + recut provenance

- **Tally (census of record), 2026-06-10:** full re-derivation, $0; receipts `runs/floor_census_2026-06-10/`; three-way reconciled; both new facts dispositioned-open.
- **Catechism (S52 recut), 2026-06-10:** the v3 overlay (preflight → Jake-run 4-col PK DDL → execute → verify 7/7) · both census dispositions closed · shrapnel + injection verdicts landed · delta-1 uuid map landed · manifest updated. All S52 figures trace to `runs/floor_overlay_v3_S52/` and `runs/recon_S52/`. Spend: **$0** (no API fires in S52).

---

## The rule this doc enforces (JAKE-RULES §5.1)

No floor or corpus count is ever stated bare. It carries its unit — and as of S52, **`rows` vs `messages` is a mandatory unit distinction**: rows = 58,792, messages = 29,396, and conflating them is the same defect class as "the corpus is read." A true number with its frame stripped is the poison; the frame is non-optional.

---

*Last updated: 6-10-26, apparatus S52 "Catechism" — THE v3 RECUT (floor uniformly scrub-v3; rows-vs-messages discipline; both census dispositions CLOSED; shrapnel 118/118 clean; delta-1 uuid-proven; receipts `runs/floor_overlay_v3_S52/` + `runs/recon_S52/`). Prior: 6-10-26 TWW parallel track "Tally" — THE FULL FLOOR CENSUS (census of record); 6-10-26 S51 "Continuance" REF-EDIT + ADDENDUM 1; 6-9-26 S49 "Concord"; floor-side originally authored TWW CCC S3.*
