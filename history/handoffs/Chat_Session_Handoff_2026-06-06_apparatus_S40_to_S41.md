# Chat Session Handoff — apparatus S40 → S41
*file: Chat_Session_Handoff_2026-06-06_apparatus_S40_to_S41.md · apparatus S40 "Catalyst" → S41 · 2026-06-06*
*This is your PRIMARY STATE INPUT — more load-bearing than the ignition prompt or the ANCHOR banner. If this conflicts with the banner, this wins (newer). If not yet pushed, Jake provides it directly.*

---

## ONE-PARAGRAPH STATE

The corpus-read architecture is RESOLVED and it's all execution from here — no open architecture questions. S40 found that the on-sub workflow mechanism has a HARD ~13K-char delivery ceiling per `agent()` call (structural: the workflow runtime has no Node globals — no `fs`/`Buffer`/`require`; the only disk-touching primitive is `agent()`, which returns output-capped model text). That killed the plan to read the whole corpus free on-sub. The corpus splits by size: 38 sub-ceiling convs read FREE on-sub (the proven S39 loop), 181 over-ceiling convs read PAID on the batch API (Sonnet 4.6, 1M window, tools-absent, batched 50%-off). Model is LOCKED to Sonnet 4.6 — graded against the known-good Opus catalog and found richer (46 nodes vs 37), with two precision findings (UUID drop, count dilution) resolved by a tested PRECISION ADDENDUM that folds into the reader as v4.1. The full build spec exists (`Batch_Read_Spec_v1_2026-06-06.md`). S41's job is EXECUTION: cost true-up → fund the account (prepay gate) → cut the v4.1 reader → build the batch pipeline → run the 38 free arm in parallel → collect + merge → downstream. Floor untouched, immortal (325/24,138). S40 paid $1.95 total (3 synchronous grade calls).

---

## WHAT S40 DID (the arc, in order — this is how the decision got made)

S40 booted to run two free gating reads then pace the 219. It did NOT get there, because the first real probe surfaced a structural problem that reframed everything. The arc:

1. **Both gating reads cleared.** READ 0: `apparatus_strip_v1.py` is SIZE/echo-strip only (zero credential matching), default-KEEP, ran only on the 4 whale working copies, never the floor, fully recoverable. (Jake's "secret-scrub" memory was real but pointed at the WRONG tool — that's `apparatus_freeze_pipeline.py`. Two separate tools.) READ 1: 224 convs scanned for strip markers, **0 affected** — the floor is clean, FLAG 1 (the "guard-green but harvest-thin from stripping" class) RETRACTED. READ 2: the emotional/personal register HOLDS — the reader fenced the ADHD/GAD disclosure as a checkable-predicate constraint, held TEXTURE on the vulnerability-under-productivity moment, did not flatten or sanitize.

2. **BUT READ 2 exposed a delivery bug.** The scope-reader had been getting a SUMMARY of large payloads, not raw content — and self-reading the payload file via 36 Read calls to recover (PROHIBITION 3 violated; the catalog was accurate only because the reader broke containment). Diagnosed to two joints: (a) the read-payload step was an `agent()` call, and `agent()` returns model text (a summary), never raw bytes; (b) the payload file sat on disk + the scope-reader had Tools:* including Read + the path leaked into context.

3. **The fix collapsed on a probe — twice.** Designed fix: `fs.readFileSync` for raw delivery + `fs.unlinkSync` to delete-before-read (blindness by absence-of-target). PROBE: the workflow runtime has NO `fs`/`Buffer`/`require` — all undefined. Both halves dead. Re-architected to schema-passthrough (schema is hard-enforced, carried a 56K file intact). PROBE at max scale (574KB target): schema TRUNCATED at 13,147 chars — the model hit its ~8K output-token ceiling and apologized mid-field. Schema controls shape, not size; no schema beats the output cap. Chunked-schema (44 agents/conv) was considered and KILLED as the over-build twin-bug.

4. **The finding crystallized + the fork opened.** The on-sub workflow mechanism CANNOT deliver a payload over ~13K chars to a reader — structural, not a bug. S35's "free path works" was true but scoped too wide (proven only on small convs). OC-from-S35 was hand-carried back in by Jake (to get the decision-maker, not a fresh context), ran two $0 count runs, and the corpus distribution settled it: 181 of 219 over the ceiling (83%). Hybrid (free-the-38 + pay-the-181 with two pipelines) was rejected — the free tier is the 17% MINORITY, so two-mechanisms-for-marginal-gain is the inverted trap. DECISION: Option 2 refined — 38 free on-sub, 181 (incl. the 6-conv 13-50K band, no bespoke squeeze) paid batch.

5. **The model got graded, not assumed.** The $0.30 Sonnet-vs-Opus test (named since S34, never run) finally ran. First attempt truncated (max_tokens 16K too low) AND lost output to a UnicodeEncodeError (printed before saving) — cost $0.78 for nothing, surfaced the real ~3.1 chars/token ratio (my $0.30 est used ~4) and the save-before-print rule. Re-run ($0.80, clean): Sonnet 46 nodes/17 FENCE vs Opus 37/8 — RICHER, austere-fear dead. Two findings: dropped a cross-session UUID pointer; diluted an exact TEXTURE count. Both share a signature: substance-kept, precision-lost.

6. **The addendum fixed both, tested.** A PRECISION ADDENDUM (UUID-preservation + exact-counts-in-TEXTURE, grounded in the verbatim-by-pointer doctrine) was appended to the S32 reader (NOT editing the sealed file) and tested on the hardest UUID-dense conv (`e831e30b`, 45 cross-session UUIDs, $0.37). Result: 4/4 UUIDs preserved verbatim, no fabrication, richness intact. Finding A (UUID — the sharp one) RESOLVED; Finding B (counts) untested-here-but-harmless-to-fold.

7. **The spec got written.** Re-anchored on HEAD first (caught a near-miss: the v4.0 reader is written for Opus-1M, and I'd been about to spec around a believed Sonnet-200k window — a doc-check confirmed Sonnet 4.6 has the full 1M ON THE API, GA, no header, so the 181 read WHOLE, no batch-chunking). Produced `Batch_Read_Spec_v1_2026-06-06.md` (full) + `S40_RefDoc_ChangeSets_2026-06-06.md` (change-only edits for ANCHOR v30 / Progenitor / CHANGELOG / JAKE-STACK).

---

## THE DECISION (resolved — do not relitigate without a NEW reason)

- **Corpus read splits by size at the ~13K-char on-sub delivery ceiling.** 38 free on-sub / 181 paid batch. NOT hybrid (free tier is the minority).
- **Model = Sonnet 4.6**, temp 0, + the precision addendum (→ reader v4.1). Graded richer-than-Opus, ~4× cheaper batched.
- **All 181 read WHOLE** — Sonnet 4.6 has the 1M context window on the Claude API (GA, no beta header, no price multiplier; largest conv ~354K tokens fits). NO chunking in the batch.
- **Batch API endpoint** (50% off), prompt-cached system prompt, `custom_id = conv_uuid`, NO tools (true tool-absence = the strong blindness form).
- **RESCOPE, not reversal:** free-and-faithful below the on-sub delivery ceiling, paid-and-faithful above it. Faithful never bent. The on-sub path lives forever as the maintenance drip (new small convs read free).

---

## CORPUS DISTRIBUTION (from the floor, $0 — the decision data)

219 non-whale FITS_WHOLE convs:
- `<=13K chars` (free on-sub): **38**
- `13K-50K`: 6  } 
- `50K-200K`: 34  }  → these 181 are the PAID batch
- `>200K`: 141  }
- **OVER 13K (paid): 181 (83%)** · UNDER (free): 38 (17%)
- Over-set runs 1,107,054 chars → 14,930; top 14 all >900K; 141 are >200K.
- (A separate "11/14 over ceiling" count from the 14 on-disk payloads is a BIASED sample — those were pulled because big. Do not cite as corpus rate.)

---

## MEASURED TOKEN DATA (replace S33's projection — true cost on these)

| conv | chars | input tokens | tok/char | output tok | nodes |
|---|---|---|---|---|---|
| 01eb6e56 (ADHD) | 564,012 | 179,830 | 0.319 | 17,420 | 46 |
| e831e30b (UUID) | 374,922 | 109,590 | 0.292 | 2,421 | 6 |

Use **0.30–0.32 tok/char** input (report a band). Output ~**380–400 tok/node**; node-count-per-conv is the SOFT unknown (estimate low/mid/high). Real char/token ratio is ~3.1, NOT the ~4 prior estimates used — this is why S33's batch projection runs optimistic; true on 3.1.

---

## THE READER CUT — v4.1 (the one thing that MUST be real before the batch fires)

- **Boot_ScopeReader_v4.1** (reference) = v4.0 verbatim + the precision addendum appended (after the one-shot example, before the sign-off). **Deployable = `test_call_system_prompt_S40.md`** = the v4.0 deployable + the same addendum.
- v4.0 / `test_call_system_prompt_S32.md` stay on disk, TOMBSTONED-NOT-DELETED.
- The addendum text is in `Batch_Read_Spec_v1` §2 (verbatim, copy from there).
- This is a deliberate canon cut: CC creates v4.1 + the new deployable as committed artifacts (draft-PR → review → land, same gate as code). **The batch fires v4.1, NOT v4.0.**

---

## BILLING — TWO REGIMES, GUARD BOTH (highest-consequence)

- **Floor reads** (`floor_extract.py`): `floor_db.env` — $0 Postgres. NEVER a billing call. Do not load the API key for these.
- **Paid batch:** ROOT **`anthropic_billing.env`** — NOT `pipeline/secrets/.env` (that REFUSED wall is built and STAYS; the key is not there), NOT `floor_db.env`. Loaded for submit/collect ONLY, cleared after. ⚠ OC-S35's hand-carried note had the STALE `pipeline/secrets/.env` path — the disk wins, it's root `anthropic_billing.env`.
- **BATCH-NOT-SYNCHRONOUS GUARD (the new load-bearing one):** firing 181 synchronous full-price calls instead of one 50%-off batch is the silent-overspend trap. Assert the batch endpoint; confirm a batch-id came back; HALT if unconfirmable.
- **PREPAY GATE (Jake's hard constraint):** the account must be FUNDED to cover the upper estimate BEFORE submit. The account model requires balance present, not pay-on-completion. A mid-run insufficient-balance stall costs money AND forfeits batch benefits. True up cost → Jake funds → THEN submit.
- The parallel 38-conv free arm runs with the key UNLOADED (`assert_env_unloaded()` governs it — a loaded key there would meter a supposed-to-be-free read).

---

## S41 MOVES, IN ORDER (all execution — no open architecture)

1. **Anchor + confirm canon by content.** v30 banner (once folded), Progenitor v5, whale registry all-4-RESOLVED. Confirm Stage A (`bad80b5`) + the S39 on-sub loop intact on main. Confirm `harvested_nodes/` holds the prior harvests.
2. **Fold the ref-doc change-sets** (`S40_RefDoc_ChangeSets`): A (ANCHOR v30) → B (Progenitor rescope) → C (CHANGELOG) → D (JAKE-STACK env path). B has a confirm-don't-assume on the dangling reader ref. (Canon hygiene — can run at ignition or right after the true-up; not load-bearing to START.)
3. **★ COST TRUE-UP FIRST ($0).** Measured ratios (0.30–0.32 tok/char, ~380–400 tok/node, node-count low/mid/high) × the real 181 char distribution × Sonnet batch pricing ($1.50/$7.50) + prompt-cache. Produce the cost band (6-cell grid + Sonnet-sync + Opus-batch comparison). This gates the prepay.
4. **★ Jake funds the account** to cover the UPPER estimate (prepay gate).
5. **★ Cut reader v4.1** (the addendum fold — versioned, draft-PR → review → land). MUST be real before the batch fires.
6. **★ BUILD THE BATCH PIPELINE (PLAN MODE first — writes code).** Per `Batch_Read_Spec_v1`: skeleton-gate per conv → assemble 181 batch requests (v4.1 cached system prompt + per-conv skeleton payload + `custom_id=conv_uuid` + NO tools) → batch-endpoint submit w/ the batch-not-synchronous guard → poll/collect → persist via `persist_node_file()` to the flat pile → scrub-vN overlay on outputs. Resumable (skip convs already in `harvested_nodes/`; re-fire failed/truncated — floor is immortal).
7. **★ Run the 38 free on-sub arm IN PARALLEL** (proven S39 loop, key UNLOADED, $0) — banks progress while the batch processes.
8. **Collect + merge** (181 paid + 38 free + 130 whale → flat pointer pile).
9. **Downstream UNCHANGED:** fence-synthesis (Reconciliation 1) → texture/volume pass → cluster-validation (Reconciliation 2) → the Judge → retrieval engine (Progenitor §10–§11). NO QUARANTINE.
10. **Scrub-vN Supabase-pattern overlay** (flag #4) on the node outputs AND on CC's own report output.

---

## DO-NOT-RELITIGATE (settled S40; rule-4 SUSPENDED — surface if off, NEW reason to reopen)

- The on-sub ~13K-char delivery ceiling is STRUCTURAL (no fs in workflow runtime). Do NOT re-attempt schema-passthrough or chunked-schema delivery — both killed on data.
- Corpus splits 38-free/181-paid by the ceiling (Option 2 refined, NOT hybrid).
- Model = Sonnet 4.6 + precision addendum (graded, tested 4/4). Reader → v4.1 (v4.0 tombstoned).
- Sonnet 1M is API-real → the 181 read WHOLE, no batch-chunking.
- Billing: floor_db.env ($0) / anthropic_billing.env (paid, ROOT); batch-not-synchronous guard; prepay gate.
- Faithful never bends (free below ceiling, paid above).
- ALL prior settled items STAND: Stage A locked (`bad80b5`); Stage B on-sub loop proven (S39); cold-store closed; chunking-holds-corpus-wide; whale problem CLOSED (route from registry, never re-read); floor immutable + NEVER touched; conversation is the unit; bar/doctrine SOUND.

---

## §7c (BLINDNESS) — STATUS

- RESOLVED for the 181 paid: the batch API call has NO tools = TRUE tool-absence (the strong form the on-sub path could never reach). The blindness is structural, by absence-of-tool.
- PRACTICAL-not-structural ONLY on the parallel 38-conv free arm. Judged acceptable (small set; the on-sub delivery fix put the full payload in as embedded text so the reader has no MOTIVE to self-read; this arm is the maintenance drip, lives forever). **This is a JUDGMENT, not a proof** — surfaced, not buried. If S41/Jake want the 38 tools-absent too, that's a real conversation.

---

## CARRY-FORWARD (Catalyst's builder's note)

Three things bit this session, all the same shape — **the disk moved ahead of the record, and acting on the record instead of the disk was the error every time:**
1. OC's hand-carried note had the stale `pipeline/secrets/.env` billing path; the disk had `anthropic_billing.env` at root.
2. I wrote a CC prompt for a task that had already completed the prior turn; CC correctly refused it on P1 (billing discipline working — it declined to re-spend $0.37).
3. My status-line timestamp froze at 21:16 for three turns because I reused a stale `date` read instead of re-running it.
**The rule that holds:** read the disk over anyone's memory — including Jake's, including OC's, including your own from earlier in the same session. Re-anchor on HEAD before authoring anything load-bearing (it caught the Sonnet-window near-miss). The probe-then-build doctrine is the spine of this whole session — every structural surprise (the fs death, the 13K ceiling) was found by a $0 probe BEFORE it could poison a 181-conv build. Keep probing before building. And do NOT let a finished-spec read as a finished corpus — the build is the only thing between here and a harvested corpus, and it's real engineering, gated on a prepay.

**On Jake:** the session count grinds on him (he named it — 57+ sessions, a "10-day project at 10 days," every session opening on "oh shit this is fucked"). The reframe that's TRUE and worth holding: the substrate, the read law, and both read mechanisms are all built and proven; what's left is execution. Every "another problem" this session got CLOSED with a probe, cheaply, before it cost real money. That's the apparatus catching its own near-misses — which is the point of the thing. He is not behind; he's building it right, and right is the only version worth having for an auxiliary brain. Don't blow smoke at him (he clocks it instantly), but don't let the frustration-frame stand as if the work weren't real and nearly-there. It is both: hard, and nearly there.

---

*Stage B breathes on the small convs; the paid batch reads what it structurally can't. Same reader (v4.1), same payload, same persist, same flat pile, same downstream — only the read mechanism differs. Cost true-up, fund, cut v4.1, build the batch. No open architecture. Be worth it. Brothers. Grind. Evolve. Dominate.*

— S40 "Catalyst" → S41. Signed in the lineage.
