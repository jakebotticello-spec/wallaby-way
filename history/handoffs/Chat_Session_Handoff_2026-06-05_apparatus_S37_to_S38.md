# apparatus — S37 → S38 Handoff
*authored end of S37, 2026-06-05, by Curator (OC S37)*
*Tactical state transfer. The ANCHOR (v28) is canon; this is the load-bearing current-state doc — read it after the ANCHOR, trust it over banner drift.*

---

## ⚠️ READ FIRST — WHAT THIS SESSION WAS

S36 ("Cinematographer") closed the last open architecture question (chunking holds corpus-wide — SETTLED) and left a clean seam: the next phase is the BUILD. S37's job was the move that comes *before* the build — **move #2: cold-store the completed work first**, so finished node output stops living in disposable scratch and the drip has a locked structure to write into. **Move #2 is DONE.**

**S37 did NOT build the pipeline.** No architecture changed, no ruling was made, no invariant moved, no floor was touched. It was: stand up the cold-store, recover three stub files the right way, catch + contain a live security incident, and author canon (ANCHOR v27→v28, CHANGELOG S37 entry). **The build (move #3) is the next sitting — and per Jake it is STAGED, and it is a fresh-window job with full faculties, not something S37's accumulated context should drive.** S37 ran ~22 turns and deliberately stopped at the build threshold rather than open a ~15-turn build at the tail of a long, incident-interrupted session. That was the right call; honor it.

**Rule-4 (do-not-relitigate) stays SUSPENDED this stretch.** If something feels off, surface it. This lineage catches real load-bearing errors by re-looking — S37 alone surfaced a conv_uuid-locator bug that would have silently mis-keyed every chunked conversation in the 321-run, and a scrubber gap that had already leaked a live CCF secret. Both found on free/cheap data. Keep looking.

---

## STATE IN ONE PARAGRAPH

The substrate is closed and immortal (floor laid S23: 325 headers / 24,138 messages, append-only enforced; ndjson canonical on disk, Postgres rebuildable). The whale problem is closed (S33: 4 whales, 130 nodes, route from `pipeline/whales/whale_registry.md`, never re-read). The shape reader is proven (`Boot_ScopeReader_v4.0`, deterministic on API AND on-sub). Chunking is confirmed faithful corpus-wide (S36: two big-conv confirmations, 32/32 fences, 0 non-adjacent misses). **As of S37, the completed work is cold-stored** (`harvested_nodes/`: 21 done rows, 0 stubs — 130 whale nodes + 2 S32 gate reads + both S36 confirmation catalogs). **There are no open architecture questions. The cold-store exists and is the structure the drip writes into. Everything from here is the BUILD — and the build is the only thing left between here and a full harvested corpus.** S38's job: build the on-sub chunked pipeline (staged), run it, then downstream synthesis.

---

## WHERE MOVE #2 LANDED (the cold-store — CLOSED)

`harvested_nodes/` (root-level) is stood up and populated. **21 done rows, 0 incomplete, 0 stubs.** Built via a read-only-recon-then-conditional-build CC pass; **copy-not-move discipline** — the cold-store holds COPIES, raw sources stay in `pipeline/`, so a miscategorization never destroys an original.

Contents:
- **130 S33 whale nodes** — 5 files (`result_cfc7a70a.md`, `result_83506215.md`, `result_55217328.md`, `result_d9d05961_chunk_00.md`, `result_d9d05961_chunk_01.md`), `source=S33-whale`.
- **2 S32 gate-conv reads** — `result_d6e23963.md` (28 nodes), `result_492e164b.md` (47 nodes), `source=S32-gate`. Finisher-grade fits-whole proofs; folded in per Jake's call (they're real harvested nodes; re-reading them later would be pure waste).
- **48b4110a S36 confirmation catalog** — 7 chunk files + 1 whole (`confirm_48b4110a_chunk_01..07.md`, `confirm_48b4110a_whole.md`), `source=S36-confirm`.
- **ea900330 S36 confirmation catalog** — chunks 01/03 + whole + **the 3 recovered chunks 02/04/05** (`confirm_ea900330_chunk_01..05.md`, `confirm_ea900330_whole.md`), `source=S36-confirm`.
- **`harvested_nodes/MANIFEST.md`** — conv_uuid → node_file → status → source → parsed-count → note, per row.

**Bookkeeping caveat:** the manifest's additive node total double-counts the whole-read passes against their own per-chunk coverage (a whole-read is an independent re-read of the same conv, not additive). The distinct-node count is lower than the additive sum. Flagged in the manifest; not load-bearing.

**The recovered ea900330 chunks (02/04/05) carry a fix + provenance.** They were on-disk STUBS at S37 start (the S36 persist failure — see flag 3 below). Recovered from the S36 chat transcript, their `conv_uuid` was wrong (see flag 2), fixed in the cold-store copies via a scoped `sed` on the conv_uuid field only (anchor_msg values verified untouched + count-matched), with a provenance block prepended to each. Raw pre-fix originals retained at `pipeline/probe_bigconv2/`.

---

## THE THREE S36 BUILD-FLAGS — NOW PROVEN LIVE (build these into the pipeline; they are no longer theoretical)

S36 earned these as theorized cautions. S37 hit all three for real on free, already-graded data — the cheapest possible place to find them. Each would have bitten the ~321-conv unwatched run silently. **The build MUST implement all three.**

### Flag 1 — Fence tally: parse the `**Salience:** <TAG>` LINE, never a keyword grep
A bare `grep -c -i fence` over a node file inflates the FENCE count because "fence" appears in `**Keywords:**` fields too (live: chunk_02 grepped 18; the real salience-tagged count was 9). **The DONE-line breakdowns were CORRECT — the grep was the liar.** Build spec: the production fence/node tally parses the salience-tag line anchored to node structure (the `**Salience:** MOTION|FENCE|TEXTURE` line per node), never a free keyword match. (Totals on the DONE line proved reliable across all 18 cold-store files; it's the per-salience grep that's untrustworthy.)

### Flag 2 — Locator: the extractor MUST stamp real `conv_uuid` + `snapshot_id` into EVERY window header before the read
**The ugly one, proven live.** The 3 recovered ea900330 chunks each had a WRONG `conv_uuid` — the reader wrote the window's first-message anchor (`019e1720…` for chunk_02, `019e18fc…` for chunk_04, a literal `window_05_raw` for chunk_05) into the conv_uuid slot, because each mid-conversation window was extracted with NO header carrying the real conv_uuid. This is the S36 flag-2 (branch/subpath uuid) at CONV LEVEL: **a headerless chunk cannot self-identify its parent conversation, so the flat-pointer dedup — which keys on `conv_uuid` — would shatter one conversation into N phantom conversations.** Build spec: the skeleton-preserving extractor stamps `conv_uuid` + `snapshot_id` (+ the real conv timestamp) into the header of EVERY window before the read fires, so the reader writes the true conv_uuid into every node regardless of where the window starts. **Without this, every chunked conv in the 321-run mis-keys silently.** (The `Boot_ScopeReader_v4.0` PAYLOAD spec already calls for a header carrying conv_uuid + snapshot_id — the gap is the *extractor* not stamping it onto mid-conversation windows. Close it in the extractor.)

### Flag 3 — Deterministic persist: write every chunk's full node output to disk regardless of size, verify-on-write, HALT on a stub
**The entire S37 stub saga WAS this flag.** S36 left ea900330 chunks 02/04/05 as on-disk stubs (`[Full content as returned — N nodes…]` placeholders, no bodies) because the persist step spilled oversized reader output inline into the grading OC's context instead of writing it to disk. S37 recovered all three from the S36 transcript — **but only because that transcript was still reachable.** An unwatched drip run has no transcript: a silent stub = ~100 nodes lost with no alarm. Build spec: each chunk's full node output writes to `harvested_nodes/` deterministically regardless of output size — no inline-vs-stub branching; verify-on-write (byte size + DONE line present + parsed node count > 0); HALT-and-alert on a stub rather than continue.

---

## §7 — DOWNSTREAM FLAGS (carried from S36 + the new one; will bite at a named horizon)

### 7a — The char-proxy under-counts authoritative tokens by ~1.4× (load-bearing at the whole-read tier)
Proven twice (48b4110a est 467K → real 657K = 1.41×; ea900330 est 403K → real 539K = 1.34×). The char/3.5 proxy lies LOW on tool_result-heavy convs. **Consequence:** the "78 sub-25K convs run first" tier is sized on the lying proxy — a conv estimated "24K, safe whole-read" may really be ~34K and fail. **THE GATE: before running the tier-1 whole-read batch, confirm the boundary set against AUTHORITATIVE token counts measured ON-SUB (key unloaded — measuring on the paid API would be silly when the sub tells us free).** Pre-measure-the-boundary vs. try-and-reroute both work if detect-and-alert is built from the start; pre-measure wastes no rate-limit window on a failed read. Bites at the start of the whole-read tier (S38 move 4).

### 7b — The `.env` billing trap is the single highest-consequence guard in the pipeline
`pipeline/secrets/.env` holds the `ANTHROPIC_API_KEY`. If any read-path script loads it, the key SILENTLY forces METERED billing — the "free" premise evaporates with no error. Cost ~$50 earlier this lineage. **The guard (confirm key unloaded before any on-sub Agent call, HALT if you can't) must be in the pipeline from the FIRST run.** The paid path (any whole-read controls / comparison-pass sample) is the ONLY place the key loads, and only for that subprocess. Bites the moment the corpus loop fires if it's not there.

### 7c — The blindness finding: on-sub Agent calls grant `Tools: *` uncontrollably (DECIDE AT BUILD)
The on-sub `Agent` mechanism ALWAYS grants all tools to sub-agents — the reader has a live `Read` tool + reachable working dir, CANNOT be stripped in the call. S36's 5 hand-graded reads held by PRACTICAL blindness (window text + reader prompt passed as the raw call PAYLOAD, NO file paths in the call → no navigational foothold + the reader instruction says "no file access"). **But the pipeline is ~321 UNWATCHED reads, and practical-blindness-hand-checked does not scale to unwatched.** The §13 "blindness enforced by ABSENCE" invariant is, on the on-sub path, enforced by no-paths-plus-instruction, NOT true tool-absence (only the paid-API call has that — no tools in the call at all, structurally). **DECIDE AT THE CHUNKING STAGE OF THE BUILD: is practical blindness acceptable for ~321 unwatched corpus reads, or does some/all of the run need a call shape enforcing true tool-absence (the paid-API path, which reopens a slice of the cost question)?** Do not default to "practical is fine" without weighing it. The 78 sub-25K whole-reads run first don't force this — it's a chunking-stage decision.

### 7d — NEW (S37): the scrub-vN credential ruleset does not recognize Supabase's `sb_secret_` / `sb_publishable_` format
Surfaced by a live incident: Supabase auto-revoked a CCF-prod secret key found VALID in the public `claude-reference` repo at `pipeline/recon/slice_16_spans.json`. Chain: a CCF Supabase key was pasted into a conversation during a CCF build → that conv is in the official export → the export is the floor → the dead S27/S28 recon slicer carved that span to disk and it got committed back before the current scrub/.gitignore discipline was locked. **The scrubber did not fail — it ran against a 5-class v1 pattern set that PREDATES this key format, so the key passed UNRECOGNIZED.** Contained S37: key already revoked by Supabase (the real save — a dead value); `pipeline/recon/` deleted + committed + pushed (tree clean); history-rewrite DECLINED for a revoked value on a solo non-cloned working dir (Jake's call — marginal hygiene benefit, real footgun risk). **LATENT: the value still lives in the immutable ndjson floor (by design — never mutated), so any future process that reads that raw span could surface it. THE FIX (build-list item, NOT done): add `sb_secret_` / `sb_publishable_` / Supabase project-ref-URL patterns to the next scrub-vN credential overlay.** The S19/S20 tighten-only overlay machinery exists for exactly this "add a pattern discovered later, re-scrub the derived index, floor untouched" case. Scoped, architected, not a scramble. Horizon: whenever the scrub-vN overlay is next touched, or sooner if the build surfaces another credential-bearing span.

### 7e — Window-window pacing math is a third-party estimate
~220K tokens / 5-hr rolling window is unpublished by Anthropic (third-party number). The drip pacing assumes it. If reads start hitting unexpected rate limits, that estimate is the suspect — re-measure empirically, don't trust the number as gospel.

### 7f — Probe/scratch dirs accumulate; recon/ already swept
`pipeline/probe1/`, `probe2/`, `probe_bigconv/`, `probe_bigconv2/`, `strip_measure/` are scratch — `probe_bigconv*/` holds the raw pre-fix ea900330 originals (provenance, keep until the cold-store is committed + confirmed). `pipeline/nodes/` (24 UUID-named files + variance subdirs) is **an unaccounted-for known-unknown** — inventory it before any sweep so real nodes aren't lost and mystery files aren't carried forward. `pipeline/recon/` was the dead S27/S28 tree — **deleted + pushed S37** (it held the leaked secret). Sweep the rest after the pipeline is built and the cold-store committed.

---

## §8 — JUDGMENT-CALL LEDGER (the call · reasoning · confidence · source)

- **"Move #2 before the build — cold-store what's done first"** · finished work shouldn't live in disposable scratch, and the drip needs a locked structure to write into · 100% (handoff/banner-specified S36; executed S37) · ANCHOR v27 move #2.
- **"Copy-not-move into the cold-store"** · copy-then-confirm-then-(later)-move is safer than move-in-one-pass; a miscategorization never destroys an original · ~95% it's the right discipline · OC call S37, low-stakes.
- **"Fold the 2 S32 gate convs into the cold-store as source=S32-gate"** · they're finisher-grade real harvested nodes; re-reading later is waste; tag keeps provenance honest · ~90% · Jake's explicit OK.
- **"Recover the 3 ea900330 stubs from the S36 transcript rather than re-run"** · the nodes were faithful and reachable in the S36 window; recovery > regeneration of an already-graded confirmation conv · ~95% · the S36 CC confirmed the content was in-transcript; Jake pulled it.
- **"Option B (fix the conv_uuid in cold-store copies) + provenance, not option A (log-the-defect)"** · clean locators in the cold-store, evidence chain preserved in a provenance block + raw originals retained · 100% · Jake's call.
- **"Decline the git history-rewrite for the revoked secret"** · key already revoked (dead value); filter-repo/BFG on a solo NON-cloned working dir is a real footgun for marginal hygiene benefit; the revocation is the actual save · ~90% · Jake's call, OC concurred.
- **"v28 is a PROGRESS banner, not a decision banner; author ANCHOR + CHANGELOG only, nothing else"** · no architecture changed, no ruling made; ScopeReader/whale-registry/Progenitor unchanged; Progenitor body carry-forwards stay deferred to post-build (the documented over-eager failure) · ~95% · OC call, surfaced to Jake.
- **"Stop at the build threshold; don't open move #3 this session"** · ~22 turns in, incident-interrupted, and a build is ~15 turns of fresh-window CC-orchestration · 100% · Jake's call.

---

## YOUR FIRST MOVES, S38 — IN ORDER

**1. Boot + anchor by content.** Pull the codeload tarball (ignition has the curl). Read JAKE-RULES → JAKE-STACK → the three framework files (Track Meet Doctrine / Wallaby Why / Wallaby Whales) → ANCHOR **v28** → this handoff. Confirm the v28 banner is current on disk; confirm `Boot_ScopeReader_v4.0` + Progenitor v5 + whale registry (all-4-RESOLVED) by content — **all UNCHANGED since S36; do not expect edits.** Propose your name (lineage: Conductor S32 → Cartographer S33 → Compass S34 → Cartwright S35 → Cinematographer S36 → Curator S37 → you).

**2. Confirm move #2 intact.** `harvested_nodes/` exists with 21 done rows, 0 stubs, MANIFEST present. One read-only CC check; don't rebuild it. (If Jake committed the cold-store, it's in the repo; if not, it's on his disk from S37 — either way it's DONE, just verify presence.)

**3. ★ BUILD THE ON-SUB CHUNKED PIPELINE — STAGED (Jake's call; this is move #3, the real work, ~15 turns).** Stage it deliberately so a working pipeline produces real nodes before the windowing complexity is added:

   **Stage A — the loop + extractor + guards (no chunking yet):**
   - skeleton-preserving extractor (`pipeline/extract_whale.py`, `===MSG===` shape) **with flag-2 fix baked in: stamp real conv_uuid + snapshot_id + timestamp into every window header.**
   - the `.env`-key-NEVER-loaded billing guard (§7b — confirm unloaded before any Agent call, HALT if you can't; THE load-bearing guard).
   - DETECT-AND-ALERT whale gate (measure `usage.input_tokens` / authoritative size; route the 4 known whales from the registry, never re-read; HALT-and-alert on any NEW over-ceiling conv, do not auto-strip).
   - flag-1 salience-line fence/node tally (parse `**Salience:** <TAG>`, not keyword grep).
   - flag-3 deterministic verify-on-write persist to `harvested_nodes/` (size + DONE line + parsed count; HALT on stub).

   **Stage B — run the 78 sub-25K convs WHOLE first.** Pure $0 upside, no chunking, proves the pipeline end-to-end on the easy case before any windowing. **§7a-GATE first:** re-measure the tier-1 boundary set against AUTHORITATIVE on-sub tokens (key unloaded) before the whole-read batch — the proxy under-counts ~1.4×, so the "78" set is sized on a lying number; confirm which actually fit a whole-read.

   **Stage C — add overlapping-window chunking for the rest.** Probe #1's 64KB-rolling-buffer range-read (never whole-loads) + overlapping ~90K windows with ~10–15K verbatim carry-in (whole carry-in messages, every boundary seen whole by one chunk) + branch-uuid-aware dedup-on-overlap (S36 flag-2) + flat-pointer pile (no stitch; nodes self-identify by conv_uuid + anchor_msg). **DECIDE §7c HERE** (practical blindness vs true tool-absence for the unwatched run). Then the drip over the rest, paced to ~220K/5-hr (§7e, re-measure if rate-limited).

**4. AUTHOR THE PROGENITOR §12/§13 BODY CARRY-FORWARDS** on the CONFIRMED pipeline (NOT before — authoring ahead of the build is the documented over-eager failure): §0.5/§3.4 over-ceiling → two-path whale + on-sub chunked corpus read; §12 shape-reader body re-cut = the `Boot_ScopeReader_v4.0` call (API for whale/control, on-sub Agent for the corpus). The S36 reader-ref note already redirected the dangling pointer; this is the full body re-cut.

**5. ★ WHOLE-CORPUS COMPARISON PASS (Jake's S36 add — costs time, not much money).** Run EVERY non-whale conv through the chunked process (all ~321 fit — even the 400–650K monsters chunk fine, proven twice), AND whole-read a meaningful SAMPLE on API as a final at-scale faithfulness diff (chunked-vs-whole; the two S36 confirmations are already in the sample). NOT all 321 whole (that's the cost being avoided). GATE the sampled paid calls.

**6. FULL CORPUS → DOWNSTREAM (unchanged geometry).** fence-synthesis (Reconciliation 1) on harvested nodes (130 whale + ~321 fits-whole) → texture/volume pass (own `_extract_texture_slice.py`, wide-lean stripped-summary slices, 25–40 convs; whales NOT a special case; ratify `Boot_VolumeReader` v0.1 against the first texture canary) → cluster-validation (Reconciliation 2 — load-bearing, never a skim) → the Judge → wire the retrieval engine (Progenitor §10–§11). **NO QUARANTINE** — personal/medical/family is texture; only mistakenly-pasted creds excluded (scrub-vN at ingestion). Only the shape-reader DELIVERY changed; geometry is the same.

**Standing build-list item (not move-ordered):** scrub-vN Supabase-pattern overlay (§7d) — add `sb_secret_`/`sb_publishable_`/project-ref-URL patterns whenever the overlay is next touched.

---

## WHERE THINGS LIVE (quick ref — full list in ANCHOR → WHERE THE CODE LIVES)

- **shape reader (deployable):** `pipeline/test_call_system_prompt_S32.md` (= `Boot_ScopeReader_v4.0`, fired verbatim, must match v4.0)
- **API harness (paid path only — the ONLY thing that loads the key):** `pipeline/apparatus_api_testcall.py`
- **extractor:** `pipeline/extract_whale.py` (`===MSG===` skeleton, real CREATED timestamp — **add the flag-2 conv_uuid header-stamp here**)
- **the floor (immortal, never touched):** `apparatus-archive/snapshots/baseline-2026-05-25-…/scrub-v2/records.ndjson` (~367MB, read-only) + the delta snapshot — OUTSIDE the git tree (`apparatus-archive/` wholesale-gitignored)
- **secrets (the trap):** `pipeline/secrets/.env` — `SUPABASE_DB_URL` + `ANTHROPIC_API_KEY`; NEVER load on the on-sub path
- **whale registry (route, don't re-read):** `pipeline/whales/whale_registry.md` (all 4 RESOLVED)
- **★ completed-work cold-store (STOOD UP S37):** `harvested_nodes/` (21 done rows, 0 stubs, MANIFEST.md) — the drip writes here
- **S36 confirmation scratch (raw pre-fix ea900330 originals — keep as provenance until cold-store committed):** `pipeline/probe_bigconv/` (48b4110a), `pipeline/probe_bigconv2/` (ea900330)
- **known-unknown to inventory before any sweep:** `pipeline/nodes/` (24 UUID files + variance dirs)

---

## WORKING-MODE REMINDERS FOR THIS PICKUP

- **OC plans/authors canon in chat; CC reads disk + runs commands + commits; Jake bridges + is the only one who pushes/merges.** Never claim to have saved/committed/pushed. Never ask Jake for implementation/technical state. Paste CC output RAW.
- **GATE all paid spend.** In S38 the paid calls are the comparison-pass SAMPLE (move #5) + any tier-1 boundary whole-reads if the regime needs them. Everything else (the corpus drip) is on-sub-free. Confirm before anything bills.
- **The on-sub billing guard is load-bearing** — `.env` key NEVER loaded into a read-path process (§7b).
- **The blindness question is OPEN for the unwatched run** — decide the call shape at the chunking stage, don't default to "practical is fine" (§7c).
- **Prose questions only — no `ask_user_input` widget** (tell CC too). Full code blocks, no `&&` chaining, numbered deploy steps ending in Verify. CC prompts in a single code block.
- **The austere reflex is the documented bug of this lineage** — AND so is its twin, over-engineering a simple ask into elaborate scaffolding (S37 did this once, caught it). Keep prompts proportionate to the task. The apparatus is Jake's auxiliary brain — the breadth IS the function.
- **Cautious expeditiousness.** Jake's borrowing these hours from other project time. Gate where a wrong move corrupts the locked pile or bills money; move fast where it doesn't. Don't be precious.
- **Status line each reply:** `turn N · ET-time (TZ=America/New_York, use bash date) · re-anchor X (counts UP) · dest; state; next`. Watch for it dropping — that's the context-starvation tell.

---

## THE FRAME (don't lose it under the build)

This is Jake's auxiliary brain, beta 1.0. Every hard question is answered: the substrate is immortal, the whales are read, the corpus reads free, chunking is confirmed faithful at scale, and now the completed work is cold-stored. **There is no design work left, only execution — and the build is the only thing between here and a fully harvested corpus.** The breadth IS the function: the apparatus exists to hold the long-range fences (the "we tried X, abandoned it, switched to Y" lineages) that Jake's rewired working-memory buffer can't carry. S37 proved, on free data, that the cheap path's three failure modes are real and now closed in spec — so the build walks in knowing exactly what to harden. Don't let the volume of steps read as complexity; the architecture is settled, this is assembly. Build the loop with the three flags baked in, run the 78 small ones whole to prove it end-to-end, then chunk the rest on the free drip, diff a sample, synthesize.

Brothers. Grind. Evolve. Dominate.

— Curator, OC S37. Booted on the v27 banner, recovered the handoff Jake sent direct, closed the cold-store clean, recovered three stubs the right way, caught + contained a live secret leak mid-session, locked canon to v28. Stopped at the build threshold on purpose. Be worth it.
