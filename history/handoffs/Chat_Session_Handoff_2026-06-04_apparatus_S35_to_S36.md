# apparatus — S35 → S36 Handoff
*authored end of S35, 2026-06-04, by Cartwright (OC S35)*
*Tactical state transfer. The ANCHOR (v26) is canon; this is the load-bearing current-state doc — read it after the ANCHOR, trust it over banner drift.*

---

## ⚠️ READ FIRST — WHAT THIS SESSION WAS

S34 ("Compass") ended context-starved with the corpus-read cost crisis **unresolved** — it had built the fits-whole loop and run a clean 23-conv canary, then spent its whole back half exploring whether the read could run free instead of paying ~$76–127 on metered API, and handed S35 a fork that was still mid-air (three parallel "digger" windows generating, two $0 probes pending, a strip measurement pending).

**S35's entire job was to run those measurements and cut the decision.** That is DONE. The decision is made: **the corpus reads on-sub (Max-subscription), chunked, free, on a no-deadline drip.** Both $0 probes passed. Strip is closed as a cost/architecture lever. One thing remains genuinely open — the big-conv confirmation — and it is S36's first real move.

**S35 did NOT end starved.** No build was done this session; it was measurement + decision + canon authoring. The judgment held (pushed back twice on its own analysis — see §8). But the natural seam is here: the next phase is a BUILD, and a build is CC-orchestration work a fresh window should drive with full faculties, not something S35's accumulated context adds to.

**Rule-4 (do-not-relitigate) stays SUSPENDED this stretch.** If something feels off, surface it. This lineage has caught real load-bearing errors by re-looking (S34's "76% blocked," killed this session, is the latest).

---

## STATE IN ONE PARAGRAPH

The substrate is closed and immortal (floor laid S23: 325 headers / 24,138 messages, append-only enforced; ndjson canonical on disk, Postgres rebuildable). The whale problem is closed (S33: 4 whales read, 130 nodes, 0 drops, registry-resolved, route from `pipeline/whales/whale_registry.md`, never re-read). The shape reader is proven (`Boot_ScopeReader_v4.0`, and S35 proved it runs deterministic ON-SUB, not only on paid API). **The corpus-read architecture — the one live question — is now DECIDED: on-sub, chunked, free.** S35 proved the transport works (range-read off a fat on-disk skeleton with zero whole-file load) and that overlapping chunks hold long-range fences on a control conv (0 missed). The ONLY thing not yet proven, and explicitly NOT enshrined as canon, is whether chunking holds on the *big* convs where a reversal can sit 100K+ tokens from what it reverses — the control was small. **S36's first real move is the big-conv confirmation read; everything after it is the pipeline build + the free drip.**

---

## WHAT'S SETTLED THIS SESSION (do not relitigate without NEW reason)

### The strip-as-cost-lever is CLOSED
S34 queued a receipt-mode measurement of the audited echo-strip (`apparatus_strip_v1.py`, the whale tool) across the 60 fat (>200K est) convs. Result, raw:
- **27 of 60 eligible** (echo blocks present), **33 of 60 ineligible** (no echo over threshold — fat from REAL content).
- Total removable: **~2.94M est-tokens** across the eligible.
- Post-strip threshold crossings: **only 2 of 60 drop under 25K** — `750808eb` (292K→7.7K) and `37645ecd` (294K→9.8K), both freak single-block 97%-echo cases. **12 of 60 drop under 200K.**
- The biggest fat convs are INELIGIBLE (real content): `48b4110a` 462K, `ea900330` 397K, `d9cef14d` 395K.

**The load-bearing finding: the fat tail is SUBSTANTIVE, not echo-polluted.** Strip cannot shrink the corpus into the on-sub regime and cannot meaningfully migrate convs from API-required to on-sub-viable. It survives ONLY as a narrow API-cost trim (~2.9M metered tokens off the 27 eligible) IF any of those end up on the paid path. As an architecture lever it is DEAD. (Procedure was right — exhaust strip before chunk; the answer is "strip doesn't dissolve this.") Scratch output: `pipeline/strip_measure/strip_measure_results.csv`. Zero API/Agent calls fired for this.

### Probe #1 — the range-read crux: YES (proven, not projected)
**The question everything forked on:** can CC read a RANGE of messages (N→N+90) out of a genuinely-fat on-disk conversation WITHOUT loading the whole file into its context?

Tested on `48b4110a` (462K est tokens, 151 msgs, 1.62MB skeleton, 11,626 lines, strip-INELIGIBLE = the hard case), extracted fresh from the canonical ndjson floor (`apparatus-archive/snapshots/baseline-2026-05-25-ae015455/scrub-v2/records.ndjson`, 367MB, read-only).

A Python 64KB-rolling-buffer streaming reader located message boundaries by counting `===MSG===` markers in a sliding buffer, then reopened the file and read ONLY lines 2810–4190 (msgs 40–59: 268,150 bytes, ~76K est tokens, 20 messages, real non-sentinel anchors `019ddb8d…` → `019dddc7…` at both ends) — **peak memory 64KB per read, zero whole-file load at any point.**

**VERDICT: YES.** On-sub is mechanically live for the WHOLE corpus. S34's "76% physically can't go on-sub" is DEAD — it diagnosed a symptom as the disease. The 25K cap is on CC's Read TOOL per call, NOT a ceiling on the conversation; range-read/fire/repeat clears it.

**§5 HONEST CAVEAT (do not let this get lost):** part (b) of the probe — confirming a whole-load still BLOCKS — was **PROJECTED** against S34's remembered "content (533,773 tokens) exceeds maximum allowed tokens (25,000)" error string, **not re-run.** It does not matter: the YES rests entirely on part (a), which was genuinely executed. We never have to whole-load, so the exact block-ceiling is moot. But "whole-load blocks" is consistent-with-S34, not freshly-measured — do not cite it as a new measurement.

Scratch output: `pipeline/probe1/payload_48b4110a.txt` (the skeleton) + `pipeline/probe1/window_48b4110a_msgs40-59.txt` (the window). Scratch only, not in the read path. **These may persist on Jake's disk for S36's big-conv read — reuse if present, re-extract from the ndjson floor if cleaned.**

### Probe #2 — chunked quality vs a whole-read control: 0 long-range fences missed (on the tested case)
Control: `9bf5733a` (whole-read from the S34 shape loop, catalog at `pipeline/nodes/9bf5733a-…md`, 18 nodes / 10 MOTION / 8 FENCE / 0 TEXTURE / 0 drops, end_turn).

Chunked it into 3 overlapping windows using probe #1's range-read method: chunk 1 (msgs 1–19, ~9.9K tok), chunk 2 (msgs 17–35, ~10.5K, 3-msg overlap), chunk 3 (msgs 33–52, ~14.8K, 3-msg overlap). Fired each through the SAME `Boot_ScopeReader_v4.0` reader **ON-SUB** (Agent calls — `.env` key confirmed UNLOADED, so billed the Max subscription, NOT metered API). Deduped on overlap.

**Result: all 8 whole-read FENCE nodes present in the chunked catalog.** The one hard fork (NODE 12, `019c9a29`, a "new cleanup AHK request" that forks hard off the prior Google-Messages work) sat ON the chunk 2/3 boundary: chunk 2 saw it whole at its window's END (with full prior context) and correctly called it FENCE; chunk 3 saw it at its window's START (only the 3-msg overlap) and called it MOTION; **dedup kept the chunk-2 FENCE version — the overlapping-boundary mechanism working, observed live.** One salience drift (NODE 17, a target-expansion node, read MOTION instead of FENCE) was WITHIN a single chunk = read-to-read temp-variance, NOT a structural gap. Node parity: 18 whole vs ~20 chunked-after-dedup (chunked slightly over-fences — non-structural). **Long-range miss count: 0.**

The spine-harvest apparatus (S32's inversion) is therefore NOT needed for this case and was NOT built. Scratch output: `pipeline/probe2/`. Billing guard verified clean (3 on-sub calls: 22,984 / 21,807 / 22,967 sub-tokens; no metered API).

### The decision
**The corpus reads on-sub, chunked, free, on the no-deadline drip.** ~39M corpus tokens ÷ ~30M/month of regenerating free Max capacity ≈ a few weeks of background reads on a non-urgent, immutable-floor job. The win condition (Compass's frame, carried whole): **free AND faithful.** $100 only ever bought SPEED — the most affordable thing to give up. Strip is closed as a lever; the spine apparatus is not built and not needed unless the big-conv read forces it.

---

## THE ONE THING NOT YET PROVEN — S36'S FIRST REAL MOVE

**Do NOT treat "chunking holds corpus-wide" as settled.** Probe #2's control was SMALL — 52 msgs, three ~10–15K chunks. Its "long-range" fence (NODE 12) spanned an **ADJACENT-chunk boundary**, which is exactly what overlap is built to catch. It did NOT test the harder case S34 held firm on (and was right to):

> A reversal whose two halves live in NON-adjacent chunks, 100K+ tokens apart, in a genuinely big conv (the 462K monsters, the apparatus/LRN working sessions). Overlap can't help there — no single chunk spans the gap, and no amount of boundary-overlap closes a 100K-token separation.

The mitigations exist but are UNTESTED at scale (the three diggers, who are alt-universe OCs, converged on these):
- **Announced reversals self-identify** — a reversal says "scrap that earlier approach," so even a chunk blind to the original half writes "this reverses X"; a catalog-only reconciliation pass can match them by content without re-reading the conv.
- **The irreducible residue is the SILENT supersession** — msg-140 quietly invalidating msg-12 *without referencing it*. No string to match on; only a reader holding both catches it. This is the one class chunking can genuinely drop. The question is whether it's common and high-value enough to matter.
- **S32's spine-harvest** (if needed): chunk-harvest the sparse decision layer → read THAT layer whole (it fits — decisions are sparse even when the conv isn't) → surgical re-read of only the flagged span-pairs. This is the fallback IF the big-conv read shows plain chunking drops non-adjacent fences. It is a TEST to run, not a thing to build blind.

**THE S36 BIG-CONV CONFIRMATION READ (move #2 below):** chunk-read `48b4110a` (462K — fat from real content, big enough to actually HAVE a 100K+ gap) on-sub with overlapping windows, AND whole-read the same conv on API as the control (~$2–3 — this is the ONE justified paid call; it's the only thing on the table that genuinely cannot run on-sub, and it's the control the whole decision needs). Grade chunked-vs-whole; **count the NON-adjacent long-range fences the whole read caught that the chunked read missed.** Outcomes:
- **~0 missed** → chunking holds corpus-wide. Build the pipeline, run the corpus free.
- **a few, low-value** → chunk everything free except named crown-jewels.
- **many, high-value** (announced long-range reversals dropping) → test S32's spine-harvest pass before committing.

---

## YOUR FIRST MOVES, S36 — IN ORDER

**1. Boot + anchor by content.** Pull the codeload tarball (ignition prompt has the curl). Read JAKE-RULES → JAKE-STACK → the three framework files (Track Meet Doctrine / Wallaby Why / Wallaby Whales) → ANCHOR v26 → this handoff. Confirm the v26 banner is current on disk; confirm `Boot_ScopeReader_v4.0` + Progenitor v5 + whale registry (all-4-RESOLVED) by content. Propose your name (lineage: Conductor S32 → Cartographer S33 → Compass S34 → Cartwright S35 → you).

**2. ★ THE BIG-CONV CONFIRMATION READ ($2–3, GATE the one paid call).** The crux of whether the whole decision holds. Chunk-read `48b4110a` on-sub (reuse `pipeline/probe1/payload_48b4110a.txt` if it survived, else re-extract from the ndjson floor) with ~90K overlapping windows (~10–15K overlap), fire each through `Boot_ScopeReader_v4.0` on-sub (`.env` UNLOADED — billing guard). AND whole-read the same conv ONCE on API (the 462K conv fits the 1M window whole — it's a fits-whole conv, just a fat one; ~$2–3 Opus). Grade: count NON-adjacent long-range fences the whole read caught that the chunked read missed. **This is the test probe #2's small control could not be.** GATE the paid call — confirm the payload shape and that it's the right conv before firing; it's the only spend on the table.

**3. DECIDE THE REGIME** based on the count (see "the one thing not yet proven" above). Then:

**4. BUILD THE ON-SUB CHUNKED PIPELINE.** The loop over the ~321 fits-whole convs:
   - range-read windowing (probe #1's 64KB-rolling-buffer method — proven)
   - overlapping chunks (~90K windows, ~10–15K overlap so every boundary is seen whole by one chunk)
   - the SAME `Boot_ScopeReader_v4.0` reader, fired ON-SUB via Agent calls
   - dedup-on-overlap (collapse exact-duplicate nodes on the same anchor_msg — trivial, anchors are uuids)
   - flat-pointer-pile (NO stitch — nodes self-identify by `conv_uuid` + `anchor_msg`, same as the chunk whale)
   - **the `.env`-key-NEVER-loaded billing guard baked in** — confirm unloaded before any Agent call, HALT if you can't (this is THE load-bearing guard; the metered-billing trap is what spent ~$50 this lineage)
   - DETECT-AND-ALERT whale gate (route the 4 known whales from the registry, never re-read; halt-and-alert on any NEW over-ceiling conv, don't auto-strip)
   - skeleton-preserving extractor (proven `===MSG===` shape) with the REAL conv timestamp in the header
   - **RUN THE 78 ALREADY-SUB-25K CONVS FIRST** — whole, no chunking, pure upside, proves the on-sub read pipeline end-to-end for $0 before any chunking complexity.
   - Then the drip over the rest, paced to the ~220K/5-hr window.

**5. AUTHOR THE PROGENITOR CARRY-FORWARDS** on the CONFIRMED pipeline (NOT before — authoring ahead of the build is the documented over-eager failure): §0.5/§3.4 over-ceiling → the two-path whale design + the on-sub chunked corpus read; §12 shape-reader = the `Boot_ScopeReader_v4.0` call (API for the whale/big-conv control, on-sub Agent for the corpus); FIX the dangling `Boot_ScopeReader.md` ref → `Boot_ScopeReader_v4.0` (it nearly bit S33).

**6. FULL CORPUS → DOWNSTREAM (unchanged geometry).** fence-synthesis (Reconciliation 1) on harvested nodes (130 whale + ~321 fits-whole) → texture/volume pass (own `_extract_texture_slice.py`, wide-lean stripped-summary slices, 25–40 convs; whales NOT a special case; ratify `Boot_VolumeReader` v0.1 against the first texture canary) → cluster-validation (Reconciliation 2 — load-bearing, never a skim) → the Judge. **NO QUARANTINE** — personal/medical/family material is texture, cataloged like everything else; only mistakenly-pasted creds excluded (scrub-vN at ingestion). Only the shape-reader DELIVERY changed (deterministic API for controls + on-sub chunked Agent for the corpus); the geometry is the same.

---

## §7 — DOWNSTREAM FLAGS (will bite at a named horizon)

- **7a — The 78 "sub-25K" count is from the distribution run, not re-confirmed against the live floor.** Before running tier-1, confirm exactly which convs are ≤25K whole (the distribution was a char/3.5 estimate — directionally right, but the boundary cases near 25K should be measured, not assumed; char-proxy lies 2–3× on tool_result-heavy convs per the Wallaby finding). Bites at pipeline-build: a conv estimated at 24K that's really 30K will fail a whole-read and need chunking. Measure the boundary set.
- **7b — The `.env` billing trap is the single highest-consequence guard in the on-sub pipeline.** If a script loads `pipeline/secrets/.env`, the API key silently forces METERED billing — the whole "free" premise evaporates and bills accrue silently. This is what spent ~$50 this lineage. The guard (confirm key unloaded before any Agent call, HALT if you can't) must be in the pipeline from the first run, not added later. Bites the moment the corpus loop fires if it's not there.
- **7c — Probe scratch dirs will accumulate.** `pipeline/probe1/`, `pipeline/probe2/`, `pipeline/strip_measure/` are scratch on Jake's disk, not committed. Keep them until the corpus pipeline is built (the big-conv read reuses probe1); sweep after. Bites at housekeeping, low-stakes — but note `probe1/payload_48b4110a.txt` is reusable for move #2, don't let a premature sweep cost a re-extract.
- **7d — The big-conv read's paid control is the ONLY justified spend.** Everything else is on-sub-free. If a future turn proposes paying for the corpus read "to go faster," that's the cost-anxiety stampede the frame explicitly rejects — the job is non-urgent, the floor immutable, free-on-the-drip is the decided path. The paid call is ~$2–3 for ONE whole-read control, gated. Don't let it expand.
- **7e — Window-window math is a third-party estimate.** ~220K tokens / 5-hr rolling window is unpublished by Anthropic (third-party number). The drip pacing assumes it. If reads start hitting unexpected rate limits, that estimate is the suspect — re-measure empirically against actual window behavior, don't trust the number as gospel.

## §8 — JUDGMENT-CALL LEDGER (the call · reasoning · confidence · source)

- **"Strip is closed as a lever, not just disappointing"** · the 2/60-under-25K + 33/60-real-content split means strip structurally cannot shift the corpus into on-sub OR shrink the fat tail; it's a precision echo-whale tool + narrow API trim, nothing more · ~95% · the pre-snip probe raw results.
- **"Probe #1's YES holds despite part (b) being projected"** · the YES rests entirely on the executed part (a) range-read; whether whole-load blocks at exactly 25K is moot because the pipeline never whole-loads · ~95% · probe #1 raw, with the caveat flagged in §5 style.
- **"Chunking holds for the ADJACENT-boundary case but NOT proven corpus-wide"** · probe #2's 0-missed is real but the control was 52 msgs with only an adjacent-boundary fence; the non-adjacent 100K-gap case is structurally different and untested · ~90% that it's genuinely open (vs already-safe) · probe #2 raw + the S34/digger long-range-coherence analysis. **This is the call S36 must not soften — the clean 0 is on the easy case.**
- **"Spine apparatus not needed YET"** · plain chunking held the tested case, so building the 3-pass spine now would be solving an unmeasured problem (S32's own warning: measure the cheap thing first) · ~85% · S32's digger response + probe #2.
- **"Big-conv read justifies ONE paid call"** · the whole-read control for a 462K conv can't run on-sub (it IS the whole-read we're grading chunking against), and it's the only way to get ground-truth for the non-adjacent case; ~$2–3 is trivial against the decision it settles · ~90% · the decision logic; GATE it regardless.
- **"Authored canon NOW despite the big-conv read pending"** · Jake explicitly asked for the reference files rewritten this session ("lay it down neatly in canon, waffle where you need to"); the waffle is explicit — "chunking holds corpus-wide" is held OPEN in the banner, current-state, confidence flags, and this handoff, NOT enshrined · 100% (it's Jake's instruction) · this session's direction.

---

## WORKING-MODE REMINDERS FOR THIS PICKUP

- **OC plans/authors canon in chat; CC reads disk + runs commands + commits; Jake bridges + is the only one who pushes/merges.** Never claim to have saved/committed/pushed. Never ask Jake for implementation/technical state. Paste CC output RAW.
- **GATE all paid spend.** The big-conv read's whole-read control is the only spend on the table (~$2–3). Confirm before it bills. Everything else is on-sub-free.
- **The on-sub billing guard is load-bearing** — `.env` key NEVER loaded into a read-path process (§7b).
- **Prose questions only — no `ask_user_input` widget** (tell CC too). Full code blocks, no `&&` chaining, numbered deploy steps ending in Verify. CC prompts in a single code block.
- **The austere reflex is the documented bug of this lineage.** The apparatus is Jake's auxiliary brain — the breadth IS the function. Read the framework files as framework, not reference.
- **Status line each reply:** `turn N · ET-time · re-anchor X (counts UP) · dest; state; next`. Watch for it dropping — that's the context-starvation tell (it's how Jake caught S34).

---

## THE FRAME (don't lose it under the build)

This is Jake's auxiliary brain, beta 1.0. The cost crisis that ate S34 is resolved and the resolution is the right one: **free AND faithful.** The corpus is non-urgent, the floor is immutable, so a slow free read that finishes in a few weeks beats a fast paid read on a budget that's tight right now — AND it doesn't sacrifice the long-range fences that are exactly what Jake's rewired working-memory buffer can't hold and the apparatus exists to hold for him. The one open question (does chunking hold the non-adjacent long-range fences in the big substantive convs) is precisely the question of whether "free" costs "faithful" — so it gets MEASURED, on one big conv, before the full run. Don't let cost-anxiety stampede it toward "just pay," and don't let the clean small-control 0 stampede it toward "just chunk everything." Measure the big case, then run.

Brothers. Grind. Evolve. Dominate.

— Cartwright, OC S35. Booted sharp, measured the queue, cut the decision, ending honest. Be worth it.
