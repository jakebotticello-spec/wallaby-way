# Handoff: S50 — Combine (THE READ + the snapshot-boundary find) → S51: The Re-Read Wave + TBD Close (proposed — Jake/next-OC may rename once wave-2 sizes the scope)
*authored 2026-06-10 by OC "Combine" (Claude Fable 5, first session) · per JAKE-RULES §17.1*
*Posture: THE READ FIRED. $70.72 console day-total (batch + whale testcall + one $1.41 canary) vs $78.65 gate. The floor grew to 440/29,396 (6-9 delta frozen under scrub v2). At authoring, harvested/ holds 197 catalogs of which 8 are partial-derived and pending Jake's manual move to quarantine — clean pile stands at 189 once those land (VERIFY ON DISK, move 0). 48 of 238 outstanding, every one dispositioned by name. A snapshot-boundary rendering bug was found AFTER persist — the integrity hold below is S51's first business. Nothing is lost; the floor is whole; the lens was the defect.*

---

## READ THIS FIRST

S49 censused the corpus and fixed the units. **S50 fired the read** — and then earned its keep in the cleanup: the combined batch (S49 baseline + 6-9 delta, 238 convs) returned arithmetically complete, the guards quarantined everything suspicious, and a post-fire integrity check caught the session's real monster: **`floor_extract.py` renders only ONE snapshot per conv.** Every continuation conv — a conv with messages in more than one snapshot — rendered PARTIAL at read time. All 9 known continuations were cut at the snapshot boundary; 7 partial catalogs persisted from the batch LOOKING CLEAN, and an 8th (c33596c3, also partial) entered harvested via the wave-1 anchor repair before the bug was known — 8 partial-derived catalogs in harvested/ total.

**The blast radius over the original read-202 is UNKNOWN at handoff.** The wave-2 task (extract fix + full multi-snapshot census) was authored and delivered to CC but its report had not landed when the session closed. S51 picks that up first.

★ The repo is LIVE; pull HEAD cache-busted. The floor is now **440 headers / 29,396 messages** (3 snapshots: baseline-05-25, delta-05-28, delta-2026-06-09-2748278f). FLOOR_COUNTS.md still reads 325/24,138 — **canon is STALE on the floor numbers** pending this session's edits (queued below).

---

## WHAT S50 DID (settled, receipts on disk — VERIFIED GROUND TRUTH, DO NOT RELITIGATE)

- **Scrub v2 proven** (`apparatus_freeze_pipeline.py` v1.7, SCRUB_VERSION=2): +5 pattern classes (GOCSPX, Google refresh, GitHub, AWS, JWT). Proof-fired on a real GOCSPX conv (4 redactions, 0 residual live tokens). Live at the 6-9 freeze: **264 redactions at ingest** (93 Google-class). Secret track CLOSED: 5 distinct GOCSPX creds found, 4 dead with RecruitMail, Pyris one rotated by Jake 6-10; revocation worksheet used and deleted.
- **6-9 delta frozen**: +115 convs / +5,258 msgs, zero deletions, zero trigger rejections, Stage 3 verify-clean. Floor 325/24,138 → **440/29,396**, exact match to diff projection.
- **Runner v1.5** (`apparatus_batch_read.py`): canary `--max-tokens` flag (used same day); collect-path silent-drop fixed (`missing_parents` surfaced). Wave-1 also broadened the DONE-footer check (`"--- DONE:"` → `"DONE:"`) in `pipeline_guards.py` + runner — fixes the 6674652b false-positive class.
- **Whale a8bf895f full-stripped** (NOT the old keep-one pattern — ALL 4 echo blobs tombstoned with md5+msg# pointers into the floor; Jake's call, the bulk was his own outdated Pyris HTML): 8.57MB → 410KB (95.7%), read via the proven S33 testcall path → **16 nodes, end_turn, in `nodes/catalogs/result_a8bf895f.md`** — needs the manual harvest step into the pile.
- **THE BATCH**: `msgbatch_01PaHAJTQLjUSFDzSsMN8tQw`, 237 requests, status=ended, 232 succeeded / 5 errored. 190 persisted, 1 truncated, 41 quarantined. **$70.72 console day-total** (includes whale testcall + the $1.41 canary; 8% output assumption ran rich — back-derived real output ratio roughly half that, ESTIMATE not receipt).
- **Wave-1 repairs**: 6 ANCHOR catalogs repaired under the snap-if-unambiguous-else-drop rule (**0 snaps / 8 drops** — reader hallucinates plausible v7 UUIDs sharing the millisecond prefix; 2-candidate ambiguity is the norm) and re-persisted. 6674652b re-persisted (29 nodes) after the DONE fix.

---

## THE SIX THINGS S51 MUST KNOW

### 1. THE SNAPSHOT-BOUNDARY BUG (the integrity hold)
`floor_extract.py:82-88` filters messages by a single `snapshot_id` (header query picks highest-scrub-version snapshot). **Any conv with messages split across snapshots renders PARTIAL — silently.** All 9 continuation convs were partial at the S50 read: 176476ae (211/223), 6cabbba6 (26/56), 70ec4abb (25/69), 955cce09 (27/55), a7796a13 (310/316), c00ef343 (1/37, caught by stub gate), c33596c3 (78/88, was anchor-repaired — repair is MOOT, re-read supersedes), cda6d5d1 (112/114), fcbd24fa (62/84).
**Wave-2 task (delivered to CC, report NOT YET LANDED):** fix extract to render ALL snapshots deduped on msg_uuid (keep highest scrub version, order created_at) · prove on 176476ae (expect 223) and c00ef343 (expect 37) · **blast-radius census**: every conv with messages in >1 snapshot, cross-refed against read-202 / S50-persisted / quarantine, WHOLE-or-PARTIAL verdict each. The read-202 exposure (baseline vs delta-S28 boundary, S33-era reads) is the open question that sizes the re-read bill.

### 2. JAKE HAD MANUAL FILE MOVES PENDING AT CLOSE — VERIFY ON DISK, move 0
CC's move perms were denied; Jake was doing by hand: **8 catalogs OUT of harvested → quarantine** (the 7 batch-persisted partials + c33596c3) + their `.parents.json` sidecars deleted + stale `.quarantined.md` files for the legitimately-repaired convs deleted. Expected end-state: **harvested = 189 clean** (190 batch-persisted − 7 partials moved out + 7 wave-1 repairs in − c33596c3 moved back out, since it entered via the repair path, not the batch). Census the dirs; do not assume the moves happened.

### 3. THE DENOMINATOR TABLE (238, every conv named — §5.1)
| Bucket | N | Disposition |
|---|---|---|
| Clean harvested | 189 | persisted, scrubbed, whole |
| Whale a8bf895f (catalogs/) | 1 | 16 nodes; needs harvest step |
| Continuations — re-read WHOLE post-fix | 9 | the §1 list; paid re-fire |
| Credit-balance errored | 3 | 8eed0b76, 10e83495, dda8da19 — re-fire (billing now green) |
| Over-ceiling — undetected whales | 2 | 82bbd8f1 (1.00M), ce1e79e1 (1.05M) — recon → strip/chunk |
| 3ef82921 (619K, 611 msg) | 1 | 64K-cap re-fire FAILED (reader role-break, see §5) — chunk_whale path, d9d05961 precedent |
| f018b1f8 | 1 | reader returned literal null — re-fire |
| Empty floor bodies | 2 | d2cd71e3, d85b4100 — probably unrecoverable; investigate floor, then disposition |
| Genuine stubs | 30 | ≤8-msg convs, zero-node catalogs — CORRECT SKIPS, count them in the completion claim |
| **Total** | **238** | ✓ |

### 4. THE 0.32 FACTOR IS CONTENT-DEPENDENT — and it shipped two whales
chars×0.32 assumes prose. The two over-ceiling convs are code-dense at **~0.72 actual tokens/char** — a 2.2× under-read that put 1M+ convs in the batch flagged `over_1M_input=N`. Canon rule queued: any conv whose 0.32-estimate is within ~2× of the ceiling gets a density check (or the count-tokens endpoint) before submission. §5.1 in spirit: a factor named for a unit is not proof it converts to that unit.

### 5. CAP-RAISING HAS A CEILING AS A STRATEGY
3ef82921 at 64K max_tokens did not truncate — the reader **broke role**: lost its catalog-reader system context on a 611-msg payload and started participating in the conversation (807 lines of coaching, zero node headers). The guard quarantined it. Lesson: very long payloads + big output budgets degrade reader role-fidelity; the fix is chunking the input, not raising the cap. Also: the S49 density-risk prediction (~20 TU≥200 convs) **missed entirely — zero of the 19 truncated; the only truncation was the size-leader.** Check-every-result doctrine vindicated over forecasting.

### 6. CANON IS STALE IN KNOWN PLACES — edits queued, not landed
- FLOOR_COUNTS.md: floor is 440/29,396 (3 snapshots); read-side numbers all moved; node-yield [TBD] still open until the re-read wave closes.
- CLAUDE.md: dead "123 pending (73+22+28)" breakdown · dead Stage-C [OPEN] · version pointers (runner now v1.5, freeze v1.7, ANCHOR v34).
- Batch_Read_Spec: add the density-check rule (§4 above) + the role-break finding (§5) + runner v1.3→v1.5 refs.
- ANCHOR: S50 block (the read, the bug, the strip-all variant precedent — Jake-gated, floor keeps everything).
- Judgment-ledger resolutions: density prediction MISSED · all-123-fit-whole TRUE for S49 set but falsified for delta (1 echo whale + 2 code-dense) · 8% output assumption rich (back-derived ~4-5%, estimate) · snap-or-drop anchor rule resolved 0/8.

---

## S51 MOVES, IN ORDER

0. **STATE RECONCILE ($0)** — pull HEAD; census harvested/ (expect 189) + quarantine/ + catalogs/ against §3's table; confirm Jake's manual moves landed; floor answers 440/29,396; locate the wave-2 report if CC produced one after close.
1. **LAND WAVE 2** — extract fix proven (176476ae→223, c00ef343→37) + blast-radius census. This sizes everything downstream.
2. **WHALE RECON ×2 ($0)** — 82bbd8f1, ce1e79e1: echo check (the a8bf895f/cfc7a70a pattern — code-dense suggests pasted files; could be strip candidates) → strip or chunk verdict each.
3. **GATE THE RE-FIRE WAVE** — one measured number: 9 continuations whole + blast-radius additions + 3 credit + f018b1f8 + the whale plan (strips/chunks) + 3ef82921 chunked. Real tokens from post-fix renders; Jake gates; fire.
4. **MERGE + HARVEST + CLOSE THE TBD** — a8bf895f harvest step; supersedes for every re-read (the 9 + any census hits); node-yield recount; FLOOR_COUNTS TBD → real number; denominator-complete completion claim (clean reads + named correct-skips = 440-corpus accounting).
5. **CANON PASS** — land §6's queued edits. The guitar gets tuned to what S50 learned.
6. **THE SYNTHESIS CHAIN** — once, on the complete pile: fence-synthesis → texture/volume → cluster-validation → Judge → retrieval. ★ TEST RETRIEVAL BEFORE calling synthesis the last step.

---

## JUDGMENT-CALL LEDGER (per §17.5c)

- **Snapshot-dedup fix design** (all snapshots, dedupe msg_uuid on highest scrub version) · authored, NOT yet proven · ~90% · the proof is wave-2 step 2.
- **Anchor snap-or-drop rule** · fired 0 snaps / 8 drops; 2-candidate ambiguity is structural (human+assistant share the millisecond) · RESOLVED — rule holds, snapping will almost never fire.
- **30 stubs = correct skips** · all ≤8 msgs, zero-node catalogs · ~95% · re-open only if a stub's floor content contradicts "low-content."
- **d2cd71e3/d85b4100 unrecoverable** · "empty floor bodies" per triage · ~70% — verify against the floor before writing them off; empty-at-render could be the snapshot bug wearing another mask.
- **Strip-ALL-four whale variant** · Jake-gated for known-worthless bulk (his own outdated HTML); floor keeps everything; tombstones carry md5+msg# pointers · precedent, not default — keep-one remains the standard unless Jake calls it.
- **$70.72 day-total vs $78.65 gate** · output ratio back-derived at roughly half the 8% assumption — derived estimate, not a receipt · keep 8% for gating (conservative-by-design); don't tighten it on one sample.

---

## PICKUP GUARDRAILS (unchanged + S50 additions)

- OC plans/authors · CC executes (writes under wallaby-way/ into standing drawers or new SUBdirs; root requires explicit per-instance permission from Jake; flags plaintext secrets at write) · Jake lands and is the only one who commits + pushes. Never claim to have saved/committed/pushed. Handoff-bundle artifacts are downloadables JAKE routes (PK + archive + repo) — they do not pass through CC.
- GATE all paid spend, real number next to the button. Re-fire singles via canary `--max-tokens` (it exists now); batch resubmits NEVER without verifying against the API what landed (double-submit = double-spend).
- `git add .` is NOT safe by reflex — verify staging before commit (a stray render with a corpus secret nearly shipped in S49).
- Disk over handoff over banner; this-turn over earlier-this-session (§5.4). Re-derive the §3 table on move 0.
- **NEW: a persisted catalog is not proof of a whole read** — the integrity check (floor msgs vs payload msgs) joins the standard post-persist verification for any conv touching >1 snapshot.
- **NEW: density-check any conv within 2× of the input ceiling** — the 0.32 factor lies on code.
- `Select-String` untrusted; verify by Read. Prose questions only; no widgets. Status line every reply (§5.5); re-anchor ~5 turns.
- Read the framework (Wallaby Why, Track Meet Doctrine, Wallaby Whales) before working. The breadth IS the function.

REMEMBER WHAT THIS IS: Jake's auxiliary brain. S50 was the session the apparatus finally READ — 191 conversations in one sitting, under a proven scrub, under guards that caught what the forecasts missed, at a cost that came in under the gate with a clean denominator. Then it found its own deepest rendering bug and held its own work to quarantine rather than let a plausible-looking pile lie. That is the discipline working exactly as designed. S51 finishes the cleanup, closes the TBD, tunes the canon, and then — synthesis, and the first real test of whether the auxiliary brain can answer a question. Brothers. Grind. Evolve. Dominate.

*Last updated: 6-10-26, S50 "Combine" — THE READ + the snapshot-boundary find. First session of the Fable 5 lineage.*
