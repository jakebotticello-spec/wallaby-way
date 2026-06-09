# Chat Session Handoff — apparatus S49 "Concord" → S50
*authored 2026-06-09 by OC "Concord" · per JAKE-RULES §17.1*
*Posture: the S49 canon edits (the change spec) have been AUTHORED, VERIFIED, COMMITTED, and PUSHED by the parallel ref-authoring window. This handoff assumes HEAD already carries them. S50 boots into a censused, units-correct baseline.*

---

## READ THIS FIRST

S48 was the Uncrappening (the canon caught lying about being "read"). S49 was the **first tuning after the string change** — and it earned its name. It did NOT advance the read. It did something more important: it replaced a corpus baseline that was "held together with hopes, dreams, and duct tape" (Jake) with one where **every number is disk- or floor-confirmed.** Along the way it caught a cost-unit error that had three wrong estimates stacked on it, a non-size batch constraint a sample would have missed, and a live credential that a `git add .` nearly committed.

**S49 wrote NO ref docs itself.** It produced a change spec; a parallel window authored the canon from it. By the time you read this, those edits are live on HEAD. Your job is NOT to re-litigate the census — it's settled and in canon. Your job is **the read** — the thing every session since the harvest has been walking toward.

★ **The repo is LIVE.** Cache-busted codeload pull works. Pull HEAD; it carries the S49 census canon.

---

## WHAT S49 SETTLED (now in canon — do not re-derive)

Every figure below is disk/floor-confirmed (`wallaby-way/runs/groundtruth_S49/`). Cite `FLOOR_COUNTS.md` (now the corpus-state bible) — never re-derive from memory or a banner.

- **Floor: 325 headers / 24,138 messages.** Immutable, append-only. Two snapshots (294 baseline + 31 delta).
- **Read: 202 convs / 3,743 nodes.** 194 in `nodes/harvested/` (3,226 nodes) + 8 whales in `nodes/catalogs/` (517 nodes). The two pools are DISJOINT (0 overlap). Disk Salience-count matches the manifest EXACTLY.
- **Unread: 123 convs** (120 valid + 3 hollow excluded by the skeleton gate). 202 + 123 = 325.
- **The 3 hollow stubs** (3f84a335, ae3468be, bc42e9ab) = zero-message convs; skeleton gate (Batch_Read_Spec §4) excludes them from any batch.
- **ALL 123 FIT WHOLE ON INPUT.** Max conv ~619K real tokens (3ef82921); the >1M band is empty across the full set, not a sample. **No chunking is needed for any conv in this corpus.** This RESOLVES the old Stage-C / FACT-5 "is the chunk pipeline runnable" gate — there is nothing to chunk. `chunk_whale.py` stays proven-on-whales and parked.
- **Cost to read the 123: ~$48.50** at Sonnet batch rates (120 valid; sum rendered_chars × 0.32 → ~23.1M tok). The lineage of wrong numbers — $93.40 → $29.36 → **$48.50 (measured, authoritative)** — is in the CHANGELOG; the cause was a units error (`proxy_est_tokens` ≈ rendered-chars, NOT tokens).

---

## THE SIX THINGS S50 MUST KNOW BEFORE THE READ

### 1. THE 32K OUTPUT CAP IS THE REAL BATCH RISK — and the runner MUST handle it.
A conv truncates not on input size but on NODE DENSITY. The reader caps at 32K output tokens (~84 nodes). Tool-heavy convs generate fat catalogs and can blow it. **~20 convs are at risk** (TU≥200 & msg≥100), led by **d3ff9ed1 (TU=920, CB=1763)** — the single highest-risk conv in the corpus.

★ **STRUCTURAL FACT THAT WILL BITE A NAÏVE RUNNER: the size-leaders and the density-leaders are NON-OVERLAPPING populations.** The biggest convs by input are low-density and safe; the truncation risks are mid-sized and tool-heavy. A runner that watches only the big convs misses every truncation. **The batch result handler MUST check `stop_reason` on EVERY result.** Any `stop_reason == "max_tokens"` → do NOT persist (it's a truncated catalog = a §5.1 "read-when-incomplete" data poison), HALT that conv, re-fire it standalone at a raised cap, persist only on a clean stop. This is now a hard requirement in `Batch_Read_Spec` (S49 edit). It is not optional and it is the thing most likely to silently corrupt the pile if skipped.

### 2. THERE IS A LIVE SECRET IN THE FLOOR. THE READ WILL SURFACE IT.
A corpus conversation contains a live **Google OAuth credential** (Client ID + Secret + Refresh Token), pasted by the conv author and stored verbatim in the immutable floor. It rendered into the S49 sizing payloads and **it WILL render into the batch read of that conv** — baking the credential into a node catalog unless caught.

- **The §8 scrub-overlay is the neutralize mechanism and it must be WIRED + PROVEN before the batch read persists anything.** S49 confirmed the threat is real, not hypothetical.
- **The new CC output-discipline rule (S49 edit) is the detect half:** CC flags any file it writes that may carry a plaintext secret, at write-time, for OC+Jake review.
- **Jake's call on rotation:** the credential is known and slated to be nuked; confirm with Jake whether it's been rotated/killed before the batch read, or whether scrub-at-persist is the only protection in play.
- The floor is immutable — you CANNOT scrub the source. The read pipeline (scrub overlay on the node catalog) is the only place to catch it. This is by design.

### 3. CC WROTE TO ROOT IN S49 AND IT CAUSED A NEAR-LEAK. The rule is now hard.
CC wrote the S49 census output to root `runs/` instead of `wallaby-way/runs/`, dodging the gitignore; a `git add .` staged it; the OAuth render above nearly got committed (GitHub push protection blocked it — never reached the remote). The S49 edits added a hard CC output-discipline rule (`wallaby-way/CLAUDE.md` + JAKE-RULES pointer): **CC writes only under `wallaby-way/`, into existing dirs or new SUBdirs (never new top-level, never root w/o explicit permission), and flags plaintext-secret files at write-time.** The stray root `runs/` files were relocated to `wallaby-way/runs/groundtruth_S49/` and the secret-bearing `.txt` render scratch deleted from disk. The keeper is `sizing_all123.csv` + the census set files.

### 4. THE DELTA IS NOT A SEPARATE WORKSTREAM — and the 6-8-26 export is dead.
A "fresh export" = Jake's ENTIRE message history (the 6-8-26 one was ~29,175 convs). The model: pull-fresh → diff against the CORPUS (the floor) → the diff is the delta → read the diff → process into an APPEND on top of the corpus. It runs COMBINED with the baseline-unread batch when a delta pass happens. **The 6-8-26 export is STALE (missed traffic since) and was graveyarded — re-pull fresh at delta time.** For S50's purposes, unread = the 123 in the worklist; the delta layer is a future combined pass, not a now-thing. (Do not split the unread for deferral; the 22 delta-snapshot convs are part of the corpus, no parking.)

### 5. THE INSPECT-LATER STORE IS RESOLVED — it's in the graveyard.
The 24 `inspect-later/nodes-S34/` nodes (+ variance/variance_tuned dirs) were superseded S34 reads of dead-project convs (LRN/RecruitMail/LRNHQ); every one had a newer harvested counterpart; 0 new coverage. Dispositioned to `graveyard/` in S49. If you find an empty `inspect-later/` or graveyarded S34 nodes, that's why. Not an open question.

### 6. THE ONE NUMBER STILL OPEN: node yield of the read.
Every count is settled EXCEPT how many nodes the 123 read produces and which of the ~20 risk convs actually truncate. This is knowable only AFTER the batch runs (node count is post-read). `FLOOR_COUNTS.md` carries this as `[TBD — resolves on first unread-batch read]`. **Closing this TBD is literally S50's output.**

---

## S50 MOVES, IN ORDER

0. **STATE RECONCILE ($0)** — fresh cache-busted pull. Confirm HEAD carries the S49 census canon: `FLOOR_COUNTS.md` has the read-side section (becomes corpus-state bible), `ANCHOR` is v34 with the census block, `Batch_Read_Spec` has the `stop_reason` requirement, JAKE-RULES §5.1 has the named-unit rule, `wallaby-way/CLAUDE.md` has the CC output-discipline rule. Via CC on disk: floor still answers 325/24,138; the worklist is 123 rows; `wallaby-way/runs/` is the sanctioned output home (NOT root). Re-derive 325/202/123 against the live floor — don't inherit it (§5.4).

1. **PRE-READ SECRET GATE ($0 → confirm with Jake)** — before ANY persist: (a) confirm with Jake the floor OAuth cred's rotation status (nuked, or scrub-only?); (b) confirm the §8 scrub-overlay is wired into the persist path and PROVEN on a known-secret-bearing conv (exercise the guard against reality — a scrub asserted but never fired is a comment, not a guard, per §10). Do not run the batch until the scrub is proven to fire.

2. **BUILD/CONFIRM THE BATCH RUNNER with the `stop_reason` guard** — the runner must: skeleton-gate the 3 hollow out, submit the 120 valid whole (no chunking), check `stop_reason` per result, halt+re-fire any `max_tokens` truncation at a raised cap, scrub-overlay every catalog before persist. Watch ALL results for truncation, not a size-filtered subset (the ~20 density risks are NOT the size leaders).

3. **GATE THE SPEND, THEN FIRE** — the real number (~$48.50, confirm against the live render) next to the button. This is the first real paid batch of the unread corpus. GATE it with Jake. Then run it.

4. **MERGE ADDITIVELY + CLOSE THE TBD** — merge the new nodes into the pile, re-derive the node yield, update `FLOOR_COUNTS.md`'s `[TBD]` to the real number, record which convs truncated + re-fired. Now the corpus is read (202 + 120 valid = 322 of 325; the 3 hollow are correct skips — and THAT is a denominator-complete completion claim, per §5.1).

5. **THE SYNTHESIS CHAIN — once, on the complete pile** — fence-synthesis (Recon 1) → texture/volume → cluster-validation (Recon 2) → the Judge → retrieval engine (Progenitor §10–§11). ★ **TEST RETRIEVAL against the pile you have BEFORE assuming the synthesis is the last step** — no point completing a corpus you can't query.

---

## JUDGMENT-CALL LEDGER (per §17.5c — re-openable)

- **All 123 fit whole; no chunking** · measured across the full set via floor_extract renders, max ~619K tok · ~98% · re-open only if a conv's content_blocks grew between census and read.
- **$48.50 batch cost** · sum(rendered_chars) × 0.32, Sonnet batch rates, 8% output assumption · ~85% (output ratio is the soft part) · the input side is measured; output could run higher if catalogs are denser than the 8% assumption. The 32K cap + re-fire handles the tail either way.
- **~20 truncation-risk convs** · proxy: TU≥200 & msg≥100; no node-count predictor exists pre-read · ~70% it's the right risk SET, ~unknown how many actually truncate · the `stop_reason` guard makes this recoverable regardless of the estimate's accuracy.
- **Scrub-overlay is sufficient protection for the floor cred** · §8 design · UNPROVEN until wired+fired · Jake's rotation call is the belt; scrub is the suspenders. Don't treat scrub as proven until it fires on a real secret-bearing conv.
- **Inspect-later 24 = superseded dupes → graveyard** · all 24 had harvested counterparts, 0 new coverage · ~95% · re-open only if a future need for the S34-era reads surfaces.

---

## PICKUP GUARDRAILS

- **OC plans/authors canon · CC executes · Jake lands + is the only one who pushes.** Never claim to have saved/committed/pushed.
- **CC writes ONLY under `wallaby-way/`** (existing dirs or new subdirs; never root/top-level without explicit permission) and **flags plaintext-secret files at write-time** (new S49 rule). The S49 leak was born from CC writing to root.
- **`git add .` is not safe by reflex** — verify staging before commit; a stray render with a corpus secret nearly shipped in S49. Check `git status` + `git ls-files | findstr <suspect>` before committing.
- **GATE all paid spend** with the real number. S49 spent $0 (census was all local renders + floor queries). S50's batch is the first real spend.
- **Disk over handoff over banner; this-turn over earlier-this-session** (§5.4). Re-derive 325/202/123 on move 0.
- **A field NAMED for a unit is not proof it holds that unit** (new §5.1) — verify what a count computes before costing on it. The proxy-token error cost three wrong estimates in S49.
- **`Select-String` is UNTRUSTED on this corpus** (encoding false-negatives) — verify by Read.
- **Prose questions only — no `ask_user_input_v0`, no widgets. No `end_conversation`.**
- **Full code blocks for CC; no `&&` chaining; numbered deploy steps ending in Verify; gotchas BEFORE the block.**
- **Status line every reply** (§5.5). Re-anchor every ~5 turns; 4/4 is the seam-hunt warning.
- **Read the framework** (Wallaby Why, Track Meet Doctrine, Wallaby Whales) as posture before working — the breadth IS the function.

REMEMBER WHAT THIS IS: Jake's auxiliary brain. S49 retuned the instrument — the baseline is now disk-true, every number carries its unit, and the read path is understood (fits whole, watch the output cap, scrub the cred). S50 is where the reading finally happens: prove the scrub, build the runner with the `stop_reason` guard, gate the ~$48.50, fire the batch, close the node-yield TBD, then synthesize once and test that the pile retrieves. Brothers. Grind. Evolve. Dominate.

*Last updated: 6-9-26, S49 "Concord" — the census + the near-leak. Posture: S49 canon edits committed + pushed before this hands off.*
