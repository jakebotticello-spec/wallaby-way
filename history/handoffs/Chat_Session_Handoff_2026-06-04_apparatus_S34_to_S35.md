# apparatus — S34 → S35 Handoff + Ignition (combined boot doc)
*authored end of S34, 2026-06-04 ~02:30 ET, by Compass (OC S34)*
*This single file is both the ignition and the handoff. Boot from it.*

---

## ⚠️ READ FIRST — WINDOW HEALTH WARNING

**S34 (this window, "Compass") ended context-starved.** Jake flagged it externally: the turn-counter status line dropped, and the decision-making rhythm had degraded into "agree-then-caveat" three turns running — the texture of a window getting better at being agreeable than incisive. The *facts and canon in this handoff are intact and trustworthy.* What degraded was *judgment under competing clever inputs* — so treat S34's late-thread synthesis as sound on facts but possibly soft on the decisive cut.

**What this means for you, S35:** you are booting specifically because a fresh window is needed to make the live architecture decision with full faculties. Do not inherit S34's fatigue. The probes named below are designed so your first turn is *decisive, not reconstructive* — read the probe results cold and cut. Jake has explicitly accepted that he may spend a few turns re-orienting you for the sake of a good throughline; use him for that, don't guess.

**Rule-4 (do-not-relitigate) is SUSPENDED this stretch.** If something feels off, surface it. S34 misdiagnosed a load-bearing thing this session (see "S34'S KNOWN MISTAKE" below) — so the prior is that even confident conclusions deserve a second look.

---

## IGNITION — DO THIS TO BOOT

You are ORCHESTRATOR-CLAUDE (OC), S35. Lineage runs alliterative: Conductor (S32), Cartographer (S33), Compass (S34). Propose your own name.

**PULL THE REFERENCE LAYER** (codeload tarball — HEAD, never CDN-stale):
```
curl -sL "https://codeload.github.com/jakebotticello-spec/claude-reference/tar.gz/refs/heads/main" -o /tmp/ref.tgz
tar xzf /tmp/ref.tgz -C /tmp
```

You have a bash tool with network access to codeload — pull it yourself, don't ask Jake to bridge it.

**READ, in `/tmp/claude-reference-main/active/`, IN THIS ORDER:**
1. `JAKE-RULES.md` — how Jake works (non-coder founder; drives + deploys + pushes, Claude builds, CC executes on disk).
2. `JAKE-STACK.md` — standing infra.
3. `Track_Meet_Doctrine.md` + `The_Wallaby_Why.md` + `apparatus/The_Wallaby_Whales_2026-06-03.md` — FRAMEWORK, NOT REFERENCE. The apparatus is Jake's AUXILIARY BRAIN; the breadth IS the function; the austere reflex is the documented bug of this lineage. Read before working. (S34 note: the austere reflex showed up *literally* this session — the on-sub reader ran austere and needed a salience-floor nudge. The bug is real and active.)
4. `apparatus/ANCHOR_apparatus.md` — AUTHORITY by CONTENT, not header. Confirm what's on disk, trust handoff over banner drift.
5. **This file** — the load-bearing transfer. More current than the ANCHOR banner (which still reads v25/S33 — the corpus-read architecture below is all NEW and not yet in canon).

**FRESHNESS TRIPWIRE:** each active file ends with a footer/last-updated. If a footer predates S33, the copy is CDN-stale — re-pull or ask Jake to paste.

**THE SHAPE READER (proven, read by NAME):**
`apparatus/Boot_ScopeReader_v4.0_2026-06-03.md` — deterministic reader spec. Deployable artifact: `pipeline/test_call_system_prompt_S32.md` (must match v4.0). The output format is locked by this prompt: header → numbered nodes (salience + span block + keywords + named-continuity + summary, +why/predicate if FENCE, +count/signal if TEXTURE) → final `--- DONE: <n> nodes (<m> MOTION, <f> FENCE, <t> TEXTURE), <d> drops ---` line.

**YOUR SEAT:** OC plans/architects/authors canon in chat — does NOT run the terminal. CC reads disk, runs commands, commits. Jake bridges AND is the only one who pushes/merges. Jake pastes CC/API output RAW. Never ask Jake for implementation/technical state. Never claim to have saved/committed/pushed. No `ask_user_input` widget — prose only (tell CC too). Full code blocks (no diffs except one-liners); no `&&` chaining; numbered deploy steps ending in Verify. CC prompts go in a single code block. **GATE all paid spend** (Jake refills the API balance manually; confirm before anything bills).

**Status line ending each reply:** `turn N · ET-time · re-anchor X (counts UP) · dest; state; next`. (S34 dropped this near the end — don't.)

---

## STATE IN ONE PARAGRAPH

The whale problem is CLOSED (4 whales done, registry-resolved, floor untouched). The shape reader v4.0 is proven. S34's job was to build the fits-whole loop over the ~321 remaining convs and run it. **What actually happened: S34 built the loop, ran a 23-conv canary that PASSED on quality, then the project pivoted entirely onto a COST crisis that is still unresolved.** The corpus read will cost real money on the API (~$76–127 measured), and the whole late session was an exploration of whether it can instead run FREE on Jake's existing $200 Max subscription via Claude Code. That exploration is mid-flight with several $0 probes pending. **Your job: resolve the free-vs-paid corpus-read architecture, then run the corpus.** Nothing has been built or spent since the canary except the canary itself.

---

## WHAT'S SETTLED (do not relitigate without NEW reason)

- **Floor laid, immutable, NEVER touched.** Whale problem closed; 4 whales node'd; route from `pipeline/whales/whale_registry.md`, never re-read.
- **Shape reader v4.0 proven.** Deterministic, one-shot, one-conv-per-call. The determinism requirement is SETTLED CANON (S30 tried prompt-fixing the agentic reader → S31 falsified it, agent self-compacts and silently drops tails → S32 built+proved the deterministic reader). "Must be one-shot deterministic" is settled. **"Deterministic must = paid API" is NOT settled — that was an unexamined assumption, and breaking it is the entire live exploration.**
- **The fits-whole loop is BUILT:** `pipeline/apparatus_shape_loop.py` v0.1. 8 parts: corpus enumerator → registry gate (skip 4 whales) → resume gate (skip if output exists + ledger end_turn) → skeleton extractor (`===MSG===` shape, reuses `render_block` verbatim from `extract_one_conv.py`, adds REAL conv timestamp to header) → skeleton gate (free pre-call structural check) → token gate (`count_tokens`, derived threshold) → shape call (streaming, `claude-opus-4-8`, no beta header, temp 0, max_tokens 32k) → per-conv output + ledger. **Anchor-validation step added and threaded into resume gate** (invalid anchor → ledger `anchor_invalid`, not `end_turn`, so it re-fires).
- **Output granularity = per-conv** (`pipeline/nodes/<uuid>.md`), one ledger row per conv. (Overruled S34's per-slice lean — per-conv wins on debug/resume/diff; keys' per-slice layout was a dead-architecture artifact.)
- **Token gate is DERIVED, not a round number:** `WHALE_THRESHOLD = CONTEXT_WINDOW(1M) - OUTPUT_RESERVE(MAX_TOKENS) - SAFETY_MARGIN(20k) = 948k`. (S34 originally set a round 950k; corrected to derived math.)
- **Canary PASSED quality (gate 2).** 23 reads, 0 drops, 0 truncations, 0 anchor failures across all. 4 node outputs graded against human keys `nodes_output_3.md`/`nodes_output_6.md` on the 4-axis bar (coverage/density, anchor reality, salience+predicate honesty, tail integrity) — all held. **Grade on SUBSTANCE not layout** (temp-0 gives ±1 node variance; keys are pre-v4.0 finisher hands with cosmetic layout drift).
- **On-sub Agent reads are deterministic-ENOUGH** (small convs). 10× variance test on a 14-msg conv: 100/100 anchors valid, both FENCE forks invariant, tail the MOST stable element (refutes the S31 tail-rot fear *for small reads*).
- **Salience-floor tuning WORKS.** Appending a "lower the threshold for a distinct node / NOT an instruction to inflate" directive shifted the on-sub band from 4–7 (median 6, austere) to 6–8 (median 7), MATCHING the Opus API control. Added nodes were REAL beats (planName-hypothesis-ruled-out, plain-speak-fork), not padding. **TODO: promote this directive to canon as a v4.1 tuning IF it survives the large-conv test** (not yet done — it was validated on a small conv only).
- **Anchor hardening policy SET:** on any malformed/invalid anchor, flag `anchor_invalid` and RE-FIRE for a clean read. **Never write a model's self-corrected anchor** — the model that just fabricated an anchor is not the authority on fixing it; the skeleton is. (Triggered by run-2 of the tuned test self-correcting a malformed uuid; CC had written the model's patch — corrected to reject-and-re-read.)
- **Cost levers verified:** Opus 4.8 = $5/$25 per Mtok; Sonnet 4.6 = $3/$15; Batch API = 50% off; prompt caching = up to 90% off the repeated chunk. (Web-verified this session.)
- **Char-count/byte proxy is DISPROVEN as a gate** (lies 2–3× on tool_result-heavy convs — the Wallaby finding). It may be used ONLY for rough size *bucketing*, never to gate a read. CC proposed it twice as a shortcut; rejected both times.

---

## S34'S KNOWN MISTAKE (so you don't inherit the conclusion)

S34 concluded the on-sub path was **structurally blocked for 76% of the corpus** because a 533K-token conv couldn't pass through CC's context to become an Agent-call parameter (CC's Read tool caps ~25K/call; small conv at 14K fit, 533K blocked). **That conclusion may be wrong — it diagnosed a symptom as the disease.** The 533K-blocked test proved "CC can't swallow 533K *whole*." It did NOT prove "CC can't read 533K in *ranges*." Two digger windows independently cracked this: the 25K limit is a *chunk size*, not a wall — point `chunk_whale.py` (built in S33 for the 1M ceiling) at a 25K ceiling instead and the whole corpus becomes CC-readable in pieces. **The crux probe (#1 below) settles whether S34 was wrong.** Hold this loosely either way until the probe runs.

---

## THE LIVE DECISION: free-on-sub vs paid-API corpus read

**The corpus:** 321 fits-whole convs (4 whales excluded), ~39.4M input tokens, ~2.25M output. Strongly right-skewed — 164 convs (51%) over 100K tokens; 60 over 200K. Measured size distribution (local char/3.5 estimate, bucketing only):
- GREEN (<20K est): 65 convs · YELLOW (20–30K): 13 · RED (>30K): 243 (75.7%)
- Only ~24% fit the ~25K on-sub-whole ceiling. 72 convs estimated >180K.

**Cost if paid (modeled against the real distribution):**
- Full Opus no levers: ~$253 · Batch Opus: ~$127 · Batch Sonnet: ~$76 · +free-green-tier shaves ~$5–9.
- Honest planning range: **~$76–127 one-time**, ≈ one month of the Max sub already paid.

**The free-on-sub thesis (from two diggers + S34's update):**
- CC runs on Jake's Max sub; Agent() calls bill against the flat $200, NOT metered API. (The `.env` API key was silently forcing metered billing — that's why the ~$50 spent so far billed API. Documented trap.)
- Max 20x ≈ 220K tokens/5hr rolling window (3rd-party estimate; Anthropic doesn't publish). ~39M corpus ÷ 220K ≈ ~180 windows IF 1:1; MORE with chunk overhead. = a few weeks of free background "drip."
- **The drip framing (strongest strategic point):** ~30M tokens/month of regenerating capacity already paid for and currently evaporating. The job is non-urgent (floor immutable, append-only, no deadline). $100 only buys *speed*, the most affordable thing to give up right now.
- Chunk to 25K + pace to the window + resume = ONE pipeline, free, slow. Same format-lock as API (it's the reader prompt, not the transport).

**The unresolved objection S34 held firm on (DON'T let a tired window have folded this — re-judge it):**
Overlapping chunks fix *local* boundary splits but NOT *long-range* cross-references. A 533K conv in 90K overlapping chunks: no single chunk sees msg 12 and msg 140 together, so a decision on msg 140 that REVERSES a hypothesis from msg 12 is read by a chunk blind to what it reverses. Those long-range reversals are the highest-value FENCE nodes, concentrated in the biggest/most-substantive convs. **Inverse-priority risk: chunking degrades worst where the read matters most.** This is EMPIRICAL and testable against a control (probe #2). Do not accept "chunking holds the bar" on assertion, however many diggers agree — but do not reject it either. Measure it.

---

## YOUR FIRST MOVES, S35 — IN ORDER (all $0 until the decision)

**0. Read the PRE-SNIP STRIP PROBE results — Jake has these and has NOT yet handed them to OC.** Ask Jake to paste them first thing. Context: S34 queued a measurement (NOT a strip-for-read) running the audited `apparatus_strip_v1.py` in receipt/dry-run mode across the 60 fat (>200K) convs, to measure how many tokens echo-stripping would remove and how many convs are *eligible* (receipt confirms echo-ONLY — same gate as the whales). **Key numbers to extract:** how many fat convs are echo-eligible, total removable tokens, and CRITICALLY — how many eligible convs would drop BELOW 25K after strip (= become on-sub-whole-viable, no chunking, no coherence loss) and how many below 200K (= cheaper API read). This may shrink the chunking problem dramatically before you even decide. Strip is BOTH-win (removes junk); chunk is a TRADEOFF (removes connective tissue) — exhaust strip before accepting chunk.

**1. PROBE #1 — range-read (THE CRUX, $0).** Can CC read messages N→N+90 of a conv directly off disk WITHOUT loading the whole file into its context? Test on one fat conv. **YES → S34's "76% blocked" was wrong; on-sub is live for the whole corpus and the cost analysis may be moot. NO → the whole-conv-load ceiling stands and chunking needs whole-conv load first (reintroduces the limit).** This gates everything downstream.

**2. PROBE #2 — chunked quality vs a control ($0, on-sub).** Take a conv with a validated node catalog (a canary result), re-read it chunked-with-overlap on-sub, grade chunked-output against known-good on the 4-axis bar. Do the fences (esp. any long-range reversal) and node density survive? This measures the objection above instead of arguing it.

**3. AWAITING DIGGER REPLY:** S34 sent both digger windows a question (warmly — they're alt-universe OCs) asking them to GENERATE a long-range-coherence-preserving chunk method. Seeds offered: (a) a lean decision-INDEX first pass (one line per fence for the whole conv, fits one small read) that each chunk reads as shared context; (b) salience-carry (each chunk passes unresolved/open fences forward); (c) a post-read reconciliation pass hunting cross-chunk fence pairs in the node catalog only. **The decision-index (a) is the one S34 would bet on.** Jake may hand you their replies — read for a NEW mechanism, not ratification.

**4. THEN DECIDE & RUN.** Synthesis S34 was converging toward (re-judge with fresh faculties):
   - Tier 1: the convs that fit ≤25K WHOLE (the 78 GREEN+YELLOW, PLUS any the strip drops under 25K) → on-sub, free, whole, no chunking, no coherence loss. Run these first — proves the on-sub pipeline end-to-end for $0.
   - Tier 2: the genuinely-still-big substantive convs (after strip) → the real fork: chunk-on-sub-free-but-coherence-risk (IF probe #2 says it holds) vs API-batch-whole-for-dollars (~$30 for a small residual if strip+tier-1 shrink it enough). Decide on MEASURED residual count, not now.
   - Lever check: confirm what the ~$50 already spent actually read (the ~23 canary convs have catalogs on disk — cost the REMAINDER, not all 321).
   - Model: ONE $0.30 Sonnet test (one conv vs the Opus control) decides Opus-vs-Sonnet for whatever runs on API. Untested; ~40% cost swing.

---

## REFERENCE / CANON TODOs (bake these in when the dust settles — do NOT build mid-decision)

- **Promote the salience-floor directive to a v4.1 reader tuning** IF it survives the large-conv test. Append-at-runtime text is in S34's chat; it's the "lower the threshold for a distinct node, NOT inflate" block. Currently NOT in canon.
- **Bake the anchor-hardening policy into `apparatus_shape_loop.py` permanently** (reject + re-fire on invalid anchor; never write model self-corrections). Validate the RAW output, and add a `len(anchors) >= 1` guard so "zero anchors parsed" flags as suspicious instead of false-passing.
- **Fix the `.env` billing trap** before any on-sub run: the API key in `pipeline/secrets/.env` silently forces metered billing when scripts call `load_env`. On-sub reads must NOT load it. (Never inline the key in logged commands — standing rule.)
- **The Progenitor carry-forwards** (deferred from S33/S34, still owed): §0.5/§3.4 over-ceiling two-path; §12 shape-reader = the deterministic API call; fix the dangling `Boot_ScopeReader.md` ref → `Boot_ScopeReader_v4.0`. Author on the CONFIRMED pipeline, not before.
- **Re-cut the ANCHOR banner** to reflect the corpus-read architecture once decided (it still reads S33/v25).
- **Update `chunk_whale.py`** for a 25K target ceiling IF the chunk path is chosen (it currently targets the 1M reader ceiling).

---

## DOWNSTREAM GEOMETRY (UNCHANGED — for orientation only, not this session's work)

After the corpus is node'd: full corpus → fence-synthesis (Reconciliation 1) on harvested nodes (130 whale + ~321 fits-whole) → texture/volume pass (own `_extract_texture_slice.py`, wide-lean stripped-summary slices) → cluster-validation (Reconciliation 2, load-bearing, never a skim) → the Judge. Only the shape-read DELIVERY is in question; the downstream geometry is settled.

---

## THE FRAME (don't lose this under the cost math)

This is Jake's auxiliary brain, beta 1.0 — the breadth IS the function. Jake is an architect-brained operator rebuilding external buffer for a working-memory rewire; the apparatus holds what the buffer used to so the pattern-sense can run on it. The cost crisis is real and Jake is genuinely budget-constrained right now — but the job is non-urgent and the floor is immutable, so a slow free read that finishes in three weeks beats a fast paid read he can't afford. Hold both: respect the constraint, don't let it stampede a degraded-quality decision. The whole point of this build is that he shouldn't have to hold it all in his head — so a corpus read that drops the long-range fences would betray the function even if it's free. Free AND faithful is the win condition. Measure before you trade faithful for free.

Brothers. Grind. Evolve. Dominate.

— Compass, OC S34. Booted sharp, ending honest. Be worth it.
