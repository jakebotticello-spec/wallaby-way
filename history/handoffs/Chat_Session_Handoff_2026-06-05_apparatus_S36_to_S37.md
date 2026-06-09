# apparatus — S36 → S37 Handoff
*authored end of S36, 2026-06-05, by Cinematographer (OC S36)*
*Tactical state transfer. The ANCHOR (v27) is canon; this is the load-bearing current-state doc — read it after the ANCHOR, trust it over banner drift.*

---

## ⚠️ READ FIRST — WHAT THIS SESSION WAS

S35 ("Cartwright") decided the corpus reads **on-sub, chunked, free** — but held ONE thing explicitly open and refused to enshrine it: whether overlapping-chunk reads drop a **NON-adjacent** long-range fence (a decision-reversal whose two halves sit 100K+ tokens apart, too far for chunk-overlap to bridge) in a genuinely big conversation. S35's probe #2 had only tested the *easy* case — a small 52-msg control with an adjacent-boundary fence, exactly what overlap is built to catch.

**S36's entire job was to close that one question.** That is DONE. Two big convs were chunk-read on-sub (free) AND whole-read on API as controls; OC graded chunked-vs-whole for non-adjacent long-range fence misses, with the sharpened lens on **silent** (un-announced) reversals — the one residual class. **Both clean. "Chunking holds corpus-wide" is SETTLED.** Total spend: ~$6.

**S36 did NOT build anything.** It was confirmation + a ruling + canon authoring (ANCHOR v27, the Progenitor reader-ref note, the CHANGELOG entry). No floor mutation, no invariant moved. **The natural seam is here: the next phase is the BUILD, and a build is ~15 turns of CC-orchestration a fresh window should drive with full faculties — not something S36's accumulated context adds to.**

**Rule-4 (do-not-relitigate) stays SUSPENDED this stretch.** If something feels off, surface it. This lineage has caught real load-bearing errors by re-looking (S35 killed S34's "76% blocked"; S36 caught a blindness drift in CC's call mechanism mid-test — see §7).

---

## STATE IN ONE PARAGRAPH

The substrate is closed and immortal (floor laid S23: 325 headers / 24,138 messages, append-only enforced; ndjson canonical on disk, Postgres rebuildable). The whale problem is closed (S33: 4 whales read, 130 nodes, 0 drops, registry-resolved, route from `pipeline/whales/whale_registry.md`, never re-read). The shape reader is proven (`Boot_ScopeReader_v4.0`, runs deterministic on API AND on-sub). **The corpus-read architecture is now fully validated end-to-end:** on-sub, chunked, free, and — as of S36 — confirmed faithful at scale (two big-conv confirmations, 32/32 fences matched, 0 non-adjacent long-range misses, one of them across a four-stage reversal chain). **There are no open architecture questions left. Everything from here is EXECUTION.** S37's job is to build the on-sub chunked pipeline and run the corpus on the free drip, plus Jake's whole-corpus comparison pass as a final at-scale faithfulness diff.

---

## WHAT'S SETTLED THIS SESSION (do not relitigate without NEW reason)

### Chunking holds corpus-wide — SETTLED on two independent big-conv confirmations

**Confirmation #1 — `48b4110a`** (a Pyris/CCF working session, 2026-04-29):
- **657,714 authoritative input tokens** (whole-read on API). NOTE: the char/3.5 estimate was 467K — **the proxy under-counted 1.41×.** This matters downstream (§7a).
- 151 msgs, chunked into 7 overlapping ~90K windows with 4-msg verbatim carry-in. Chunk reads on-sub free; one whole-read control ~$3 on API.
- Whole read = 36 nodes / 6 FENCE. **All 6 whole-read fences matched in the chunked catalog. 0 non-adjacent long-range misses.**
- The one fence carrying a long-range reversal — the rolodex stage-height saga ("JS-measuring abandoned after ~10 iterations," → Token 6 "size content to frame") — was caught with its supersession reference INTACT. Its halves resolved within one window's reach (not the non-adjacent case). Chunked over-fenced slightly (more granular, all same decisions) = the cheap/safe error direction per default-NODE.

**Confirmation #2 — `ea900330`** (an LRN-litigation + Cypher-architecture session, 2026-05-11):
- **538,902 authoritative input tokens.** 175 msgs, 5 overlapping windows, same method. **Deliberately chosen as a reversal-dense legal-strategy session — the highest-risk class for silent supersession.**
- Whole read = 40 nodes / 16 FENCE (body). **All 16 whole-read fences matched in the chunked catalog. 0 non-adjacent long-range misses.**
- Contained a genuine **FOUR-STAGE legal-theory reversal chain**: "PIA terminated" (msg 36) → "buyout invoked in bad faith" (msg 41) → "the v1/v2 framing was WRONG, PIA never terminated, only the ICA was" (msg 49–50) → "Reading A locked, stop discussing ICA" (msg 57). Non-adjacent halves. **The chunked read caught every stage with its supersession reference intact** ("the entire v1/v2 framing was wrong," "corrected legal theory v3").
- Independent corroboration observed live: both reads, blind to each other, caught the same OA §7.5 retraction ("later retracted; do not use") — convergence-across-blind-reads, the confidence signal the whole council design rests on.

### The ruling (Jake's call)
**Lock it as SETTLED.** "We're not going to get more certain than this short of running the whole corpus through the paid API" — which is exactly the cost being avoided. The silent-non-adjacent-supersession residual is NOT zero-by-proof (you can't prove a negative) but is hunted-hard-not-found on the highest-risk conversation class; its catch is downstream **Reconciliation-1** (catalog-only matching of announced reversals), load-bearing and unchanged. **Regime = CHUNK-EVERYTHING-FREE. No spine-harvest (S32's inversion stays unbuilt — not needed). No crown-jewels-read-whole carve-out (both 400K+ monsters held, so the class the carve-out would protect is exactly the class that passed).**

---

## §7 — DOWNSTREAM FLAGS (will bite at a named horizon)

### 7a — The char-proxy under-counts authoritative tokens by ~1.4× (sharpened this session, now load-bearing)
Both confirmations proved it: `48b4110a` est 467K → real 657K (1.41×); `ea900330` est 403K → real 539K (1.34×). The char/3.5 proxy lies LOW on tool_result-heavy convs (escaped JSON tokenizes denser than prose). **Consequence:** the "78 sub-25K convs run first" tier is sized on this lying proxy — a conv estimated "24K, safe to read whole" may really be ~34K and fail a whole-read. **THE GATE: before running the tier-1 whole-read batch, confirm the boundary set against AUTHORITATIVE token counts measured ON-SUB (key unloaded — measuring on the paid API would be silly when the sub tells us free). The fresh-window OC picks pre-measure-the-boundary-set vs. try-and-reroute (detect-and-alert catches an over-ceiling whole-read and routes it to chunking) — both work if detect-and-alert is built in from the start; pre-measure wastes no rate-limit window on a failed read.** Bites at pipeline-build.

### 7b — The `.env` billing trap is the single highest-consequence guard in the pipeline
`pipeline/secrets/.env` holds the `ANTHROPIC_API_KEY`. If any read-path script loads it, the key SILENTLY forces METERED billing — the whole "free" premise evaporates with no error. This trap cost ~$50 earlier this lineage. **The guard (confirm key unloaded before any on-sub Agent call, HALT if you can't) must be in the pipeline from the FIRST run, not added later.** The paid path (the whole-read controls + any comparison-pass sample) is the ONLY place the key loads, and only for that subprocess. Bites the moment the corpus loop fires if it's not there.

### 7c — The blindness finding: on-sub Agent calls grant `Tools: *` uncontrollably (architectural, decide-at-build)
CC confirmed this session: the `Agent` tool ALWAYS grants all tools to sub-agents — the reader has a live `Read` tool and a reachable working dir, and CC **cannot** restrict them in the call. S36's 5-window reads held by **PRACTICAL blindness**: window text + reader prompt passed as the raw call PAYLOAD (CC reads both files into its own context, then passes the text), **NO file paths in the call** → the sub-agent has no navigational foothold, and the reader instruction says "no file access." Sufficient for 5 hand-graded reads. **But the pipeline is ~321 UNWATCHED reads on the drip, and practical-blindness-hand-checked does not scale to unwatched.** The §13 "blindness enforced by ABSENCE" invariant is, on the on-sub path, enforced by no-paths-plus-instruction, NOT by true tool-absence (only the paid-API call has that — no tools in the call at all, structurally). **DECIDE AT PIPELINE-BUILD: is practical blindness acceptable for ~321 unwatched corpus reads, or does some/all of the run need a call shape enforcing true tool-absence?** The paid-API path enforces it but reopens a slice of the cost question (it's metered). Flagged loud so it isn't silently absorbed — this is the agentic-reader failure mode trying to sneak back in through the call setup; catch it at build, not after the run.

### 7d — Three build-quality flags (did NOT affect the S36 grade; every fence was present + gradeable — fix in the build)
- **(1) Count fences from the BODY, not the done-line.** Both reads' self-reported summary fence-counts disagreed with the actual FENCE-labeled nodes in the body (whole said "12 FENCE," body had 16; several chunks similar). Reader output-formatting wobble. The production loop MUST tally by parsing the body, never the reader's summary count, or catalog counts drift.
- **(2) Dedup must handle BRANCH/SUBPATH uuids.** One chunked anchor (`019e178e-…742b` on ea900330) didn't resolve to a top-level msg uuid — a subpath/branch uuid on the same message span. The flat-pointer dedup must fold branch-uuid anchors onto their host message, not drop or duplicate them.
- **(3) Persist every chunk's nodes to disk RELIABLY.** On confirmation #2, chunk_02/04/05 saved as stubs (full content returned inline / oversized output spilled to a tool-result JSON for chunk_03). Harmless when OC has the inline content, FATAL for an unwatched drip. The pipeline must write each chunk's full node output to `harvested_nodes/` deterministically regardless of output size — no inline-vs-stub branching.

### 7e — Window-window pacing math is a third-party estimate
~220K tokens / 5-hr rolling window is unpublished by Anthropic (third-party number). The drip pacing assumes it. If reads start hitting unexpected rate limits, that estimate is the suspect — re-measure empirically against actual window behavior, don't trust the number as gospel.

### 7f — Probe/scratch dirs will accumulate
`pipeline/probe1/`, `pipeline/probe2/`, `pipeline/probe_bigconv/`, `pipeline/probe_bigconv2/`, `pipeline/strip_measure/` are scratch on Jake's disk, not committed. The two S36 confirmation catalogs in `probe_bigconv/` + `probe_bigconv2/` are real harvested nodes — **fold them into `harvested_nodes/` (move #2) before sweeping.** Then sweep the rest after the pipeline is built. Low-stakes housekeeping.

---

## §8 — JUDGMENT-CALL LEDGER (the call · reasoning · confidence · source)

- **"Chunking holds corpus-wide — SETTLED, not just probably"** · two independent big-conv confirmations, one reversal-dense with a four-stage chain, 32/32 fences matched, 0 non-adjacent misses; the residual (silent supersession) hunted on the highest-risk class and not found · ~92% it genuinely holds corpus-wide; the residual is real but small and homed at Reconciliation-1 · the two S36 grades + Jake's ruling to lock it.
- **"The rolodex reversal (conf #1) is NOT the non-adjacent case"** · the stage-measurement reversal resolved within window 6's reach (msgs ~76–107) and the reader announced it in plain text ("JS-measuring abandoned"); not two halves 100K apart with no reference · ~90% · OC's grade, ratified by Jake (who didn't recall the sequencing but agreed the reasoning holds — the grade stands on the announced-reversal text regardless of distance).
- **"Practical blindness is sufficient for the 5 hand-graded reads but NOT decided for the pipeline"** · no file paths in the call = no navigational foothold even with a live Read tool, and OC hand-grades the output; but 321 unwatched reads is a different risk surface · ~85% practical is fine for hand-graded / explicitly OPEN for the unwatched run · CC's interface disclosure + §7c.
- **"Author canon NOW, defer the handoff to a clean turn"** · Jake's call — land the refs with the cleanest context window, then write the handoff/ignition after · 100% (Jake's instruction).
- **"No crown-jewels carve-out"** · both confirmations WERE 400K+ monsters (the exact class a carve-out would protect) and both held · ~90% · the two grades; if the comparison pass (move #6) ever shows a big conv dropping a silent non-adjacent fence, this reopens.

---

## YOUR FIRST MOVES, S37 — IN ORDER

**1. Boot + anchor by content.** Pull the codeload tarball (ignition has the curl). Read JAKE-RULES → JAKE-STACK → the three framework files (Track Meet Doctrine / Wallaby Why / Wallaby Whales) → ANCHOR v27 → this handoff. Confirm the v27 banner is current on disk; confirm `Boot_ScopeReader_v4.0` + Progenitor v5 (with the S36 reader-ref note) + whale registry (all-4-RESOLVED) by content. Propose your name (lineage: Conductor S32 → Cartographer S33 → Compass S34 → Cartwright S35 → Cinematographer S36 → you).

**2. ★ COLD-STORE WHAT'S DONE FIRST.** Before any build: stand up the NEW root-level **`harvested_nodes/`** cold-store (see ANCHOR → WHERE THE CODE LIVES). Have CC gather all completed node output that exists — the 130 whale nodes from S33 (the 5 `result_*.md` files) + the two S36 confirmation catalogs (in `pipeline/probe_bigconv/` + `probe_bigconv2/`) — catalog them in a `harvested_nodes/MANIFEST.md` (conv_uuid → node file → status done/pending → source path), and move them in. This starts the locked pile of completed work, separate from disposable scratch. It's also the structure the drip writes into, so it has to exist before the loop runs.

**3. BUILD THE ON-SUB CHUNKED PIPELINE** (the loop over the ~321 fits-whole convs):
   - range-read windowing (probe #1's proven 64KB-rolling-buffer method — never whole-loads)
   - overlapping ~90K windows, ~10–15K verbatim carry-in (whole carry-in messages, not summaries — every boundary seen whole by one chunk)
   - the SAME `Boot_ScopeReader_v4.0` reader (`pipeline/test_call_system_prompt_S32.md`), fired ON-SUB via Agent calls, **embedded-payload method** (CC reads both files into its own context, passes as raw call text, NO file paths — see §7c blindness finding; decide if this practical-blindness shape is acceptable for the unwatched run or if it needs hardening)
   - dedup-on-overlap, **branch-uuid-aware** (§7d flag 2)
   - flat-pointer-pile (NO stitch — nodes self-identify by `conv_uuid` + `anchor_msg`)
   - **deterministic full-node persist to `harvested_nodes/`** regardless of output size (§7d flag 3)
   - **body-not-done-line fence tally** (§7d flag 1)
   - **the `.env`-key-NEVER-loaded billing guard baked in** (§7b — confirm unloaded before any Agent call, HALT if you can't; THE load-bearing guard)
   - DETECT-AND-ALERT whale gate (route the 4 known whales from the registry, never re-read; halt-and-alert on any NEW over-ceiling conv, don't auto-strip)
   - skeleton-preserving extractor (proven `pipeline/extract_whale.py`, `===MSG===` shape, with the REAL conv timestamp)
   - **§7a GATE — confirm the tier-1 boundary set against AUTHORITATIVE tokens (on-sub, key unloaded) before the whole-read tier.**

**4. RUN THE 78 (RE-CONFIRMED) SUB-25K CONVS FIRST** — whole, no chunking, pure $0 upside, proves the pipeline end-to-end before any chunking complexity. Then the drip over the rest, paced to the ~220K/5-hr window (§7e — re-measure if rate limits hit).

**5. AUTHOR THE PROGENITOR §12/§13 BODY CARRY-FORWARDS** on the CONFIRMED pipeline (NOT before — authoring ahead of the build is the documented over-eager failure). The S36 reader-ref note already redirects the deployable-reader pointer to `Boot_ScopeReader_v4.0`; the full §12/§13 body re-cut (two-path whale + on-sub chunked corpus read; §0.5/§3.4 over-ceiling) is authored here, on the built pipeline.

**6. ★ WHOLE-CORPUS COMPARISON PASS (Jake's S36 add — costs time, not much money).** Run EVERY non-whale conv through the chunked process (all ~321 fit — even the 400–650K monsters chunk fine, proven twice), AND whole-read a meaningful SAMPLE on API as a final at-scale faithfulness diff (chunked-vs-whole; the two S36 confirmations are already in the sample). One last verification pass for the road — **NOT all 321 whole** (that's the cost being avoided). GATE the sampled paid calls.

**7. FULL CORPUS → DOWNSTREAM (unchanged geometry).** fence-synthesis (Reconciliation 1) on harvested nodes (130 whale + ~321 fits-whole) → texture/volume pass (own `_extract_texture_slice.py`, wide-lean stripped-summary slices, 25–40 convs; whales NOT a special case; ratify `Boot_VolumeReader` v0.1 against the first texture canary) → cluster-validation (Reconciliation 2 — load-bearing, never a skim) → the Judge → wire the retrieval engine (Progenitor §10–§11: trigger model + span-return shape). **NO QUARANTINE** — personal/medical/family is texture, cataloged like everything else; only mistakenly-pasted creds excluded (scrub-vN at ingestion). Only the shape-reader DELIVERY changed; the downstream geometry is the same.

---

## WHERE THINGS LIVE (quick ref — full list in ANCHOR → WHERE THE CODE LIVES)

- **shape reader (deployable):** `pipeline/test_call_system_prompt_S32.md` (= `Boot_ScopeReader_v4.0`, fired verbatim, must match v4.0)
- **API harness (paid path only):** `pipeline/apparatus_api_testcall.py` (the ONLY thing that loads the key)
- **extractor:** `pipeline/extract_whale.py` (`===MSG===` skeleton, real CREATED timestamp)
- **the floor (immortal, never touched):** `apparatus-archive/snapshots/baseline-2026-05-25-ae015455/scrub-v2/records.ndjson` (~367MB, read-only) + the delta snapshot
- **secrets (the trap):** `pipeline/secrets/.env` — holds `SUPABASE_DB_URL` + `ANTHROPIC_API_KEY`; NEVER load on the on-sub path
- **whale registry (route, don't re-read):** `pipeline/whales/whale_registry.md` (all 4 RESOLVED)
- **★ NEW completed-work cold-store:** `harvested_nodes/` (root-level — stand it up move #2)
- **S36 confirmation scratch (fold into cold-store then sweep):** `pipeline/probe_bigconv/` (48b4110a), `pipeline/probe_bigconv2/` (ea900330)

---

## WORKING-MODE REMINDERS FOR THIS PICKUP

- **OC plans/authors canon in chat; CC reads disk + runs commands + commits; Jake bridges + is the only one who pushes/merges.** Never claim to have saved/committed/pushed. Never ask Jake for implementation/technical state. Paste CC output RAW.
- **GATE all paid spend.** In S37 the paid calls are the comparison-pass SAMPLE (move #6) + any tier-1 boundary whole-reads if the regime needs them. Everything else (the corpus drip) is on-sub-free. Confirm before anything bills.
- **The on-sub billing guard is load-bearing** — `.env` key NEVER loaded into a read-path process (§7b).
- **The blindness question is OPEN for the unwatched run** — decide the call shape at build, don't default to "practical is fine" without weighing it (§7c).
- **Prose questions only — no `ask_user_input` widget** (tell CC too). Full code blocks, no `&&` chaining, numbered deploy steps ending in Verify. CC prompts in a single code block.
- **The austere reflex is the documented bug of this lineage.** The apparatus is Jake's auxiliary brain — the breadth IS the function. Read the framework files as framework, not reference.
- **Status line each reply:** `turn N · ET-time · re-anchor X (counts UP) · dest; state; next`. Watch for it dropping — that's the context-starvation tell.

---

## THE FRAME (don't lose it under the build)

This is Jake's auxiliary brain, beta 1.0. Every hard question is now answered: the substrate is immortal, the whales are read, the corpus reads free, and — as of tonight — chunking is confirmed faithful at scale. **There is no design work left, only execution.** The breadth IS the function: the apparatus exists to hold the long-range fences (the "we tried X, abandoned it, switched to Y" lineages) that Jake's rewired working-memory buffer can't carry — and S36 proved the cheap free path doesn't drop them. The build ahead is real work but it's KNOWN work: stand up the cold-store, build the loop, run the drip, diff a sample, then synthesize. Don't let the volume of steps read as complexity — the architecture is settled; this is assembly. Cold-store what's done so the finished work stops living in scratch, then build forward.

Brothers. Grind. Evolve. Dominate.

— Cinematographer, OC S36. Booted sharp, ran the second confirmation, caught a blindness drift mid-test, closed the last open question, landed canon clean. Be worth it.
