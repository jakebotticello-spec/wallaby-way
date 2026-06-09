# S40 Ref-Doc Change-Sets — fold in at ignition
*file: S40_RefDoc_ChangeSets_2026-06-06.md · apparatus S40 ("Catalyst") · 2026-06-06*
*These are CHANGE-ONLY edits, not rewrites. Next-Claude folds each into its live file at ignition. The build-spec (Batch_Read_Spec_v1_2026-06-06.md) is the full file and ships separately. Order below is the order to apply.*

---

## CHANGE-SET A — ANCHOR_apparatus.md → cut v30 (prepend above v29)

**Action:** prepend a NEW v30 banner above the current v29 banner. Do NOT delete v29 — demote-in-place per supersede-don't-delete. v30 is a DECISION banner (unlike v29's progress banner): it records the on-sub delivery-ceiling finding + the Option-2 split + the model lock.

**Insert this block at the very top of the file:**

```
# ANCHOR — apparatus-build track
*v30 · 2026-06-06 (apparatus S40 "Catalyst" — **THE ON-SUB DELIVERY CEILING IS PROVEN STRUCTURAL · THE CORPUS READ SPLITS BY SIZE: 38 FREE ON-SUB / 181 PAID BATCH API · MODEL LOCKED = SONNET 4.6 (graded) · PRECISION ADDENDUM → READER v4.1**): a DECISION banner. S40 found that the on-sub workflow mechanism has a HARD ~13K-char delivery ceiling per agent() call (structural — the workflow runtime has NO Node globals: no fs/Buffer/require; only agent() touches disk and it returns output-capped model text). Proven on the 574KB max-scale target: 13,147 chars returned (2.3%), model apologized mid-field. Two delivery fixes designed + KILLED on data (schema-passthrough = same ceiling; 44-chunk-schema = over-build twin-bug). The corpus distribution forced the call: of 219 non-whale FITS_WHOLE convs, 181 (83%) exceed the ceiling, 38 (17%) are under. DECISION (Option 2 refined): 38 → FREE on-sub (proven S39 loop); 181 (incl. the 6-conv 13K-50K band, NO bespoke squeeze) → PAID batch API. This is NOT a reversal of S35 — it is a RESCOPE: free-and-faithful BELOW the on-sub delivery ceiling, paid-and-faithful ABOVE it; faithful never bent. The API beats the ceiling structurally because it returns the small node CATALOG, not the payload (payload goes in as INPUT on the 1M window). Floor untouched.*
>
> **★ S40 — THE FINDING + THE DECISION + THE GRADE ★**
> **THE CEILING (structural, proven):** on-sub agent() return is capped at ~13K chars (~8K output tokens). No fs in the workflow runtime → no non-agent delivery → no way around an output-capped model in the delivery path. The S39 "free path works" was TRUE but scoped too wide — it was proven only on SMALL convs (the 17-conv harvest all fit under the ceiling). Above the ceiling, on-sub cannot deliver. This is the gap S40 found with a $0 probe BEFORE it could silently store 2.3% of every big conversation into the auxiliary brain — the probe-then-build doctrine working as designed.
> **THE DISTRIBUTION (RUN 2, $0 from the floor):** 219 non-whale FITS_WHOLE = 38 under-13K-chars + 6 in 13-50K + 34 in 50-200K + 141 over-200K. Over-ceiling set runs 1,107,054 chars → 14,930; top 14 all >900K. 181 over / 38 under. (RUN 1's 11/14-over was a BIASED sample — those 14 were pulled because big; do not cite as corpus rate.)
> **MODEL LOCKED = SONNET 4.6 (graded, not assumed):** S40 graded Sonnet 4.6 (temp 0, S32 reader) against the known-good Opus 01eb6e56 catalog (37 nodes). Sonnet came back RICHER — 46 nodes / 17 FENCE vs Opus 37 / 8. The austere-bug fear is DEAD (inverted — Sonnet over-includes, the cheap/safe direction). Both load-bearing mental-health FENCEs held with checkable predicates; TEXTURE held (not flattened). TWO findings: (a) dropped a cross-session UUID pointer (kept name, lost machine-resolvable UUID); (b) diluted an exact TEXTURE count. BOTH resolved by the PRECISION ADDENDUM (UUID-preservation + exact-counts), tested on the hardest UUID-dense conv (e831e30b, 45 UUIDs) → 4/4 preserved verbatim, no fabrication, richness intact. Cost: Sonnet batch ~$0.40/conv vs Opus batch ~$1.64/conv (~4×). Sonnet is the read.
> **SONNET WINDOW CONFIRMED (docs, S40):** Sonnet 4.6 has a 1M-token context window ON THE CLAUDE API (GA, no beta header, no price multiplier). The largest of the 181 (~354K tokens) fits under 1M. ALL 181 READ WHOLE — NO CHUNKING in the batch. (Caveat: Sonnet 1M is API-specific; chat=500K, Claude-Code-Sonnet-1M needs usage credits. The batch is on the API → 1M applies.)
> **THE READER CUT — v4.1:** Boot_ScopeReader_v4.1 = v4.0 + the precision addendum appended (UUID-preservation + exact-counts-in-TEXTURE, grounded in the verbatim-by-pointer doctrine). Deployable = test_call_system_prompt_S40.md. v4.0 / test_call_system_prompt_S32.md tombstoned-not-deleted. The batch fires v4.1. (See Batch_Read_Spec_v1 §2.)
> **MEASURED TOKEN DATA (for cost truing — replace S33's projection):** 01eb6e56: 564,012 chars → 179,830 input tokens (0.319 tok/char), 17,420 output tok / 46 nodes. e831e30b: 374,922 chars → 109,590 input tokens (0.292 tok/char), 2,421 output tok / 6 nodes. Use 0.30-0.32 tok/char input (report a band); output ~380-400 tok/node, node-count/conv is the soft unknown.
> **BILLING (two regimes now — guard both):** floor reads = floor_db.env ($0 Postgres, NEVER billing). Paid batch = ROOT anthropic_billing.env (NOT pipeline/secrets/.env — that wall stays; NOT floor_db.env), loaded for submit/collect ONLY, cleared after. THE BATCH-NOT-SYNCHRONOUS GUARD is the new highest-consequence guard: firing 181 synchronous full-price calls instead of one 50%-off batch is the silent-overspend trap — assert batch endpoint, confirm batch-id, HALT if unconfirmable. PREPAY GATE (Jake's hard constraint): account must be funded to cover the upper estimate BEFORE submit — the account model requires balance present, not pay-on-completion; a mid-run insufficient-balance stall costs money AND forfeits batch benefits. True up cost first, fund, THEN submit.
>
> **S40 SESSION SPEND:** $1.95 paid (3 synchronous grade calls: $0.78 truncated+lost attempt, $0.80 ADHD rerun, $0.37 precision-addendum test). Real ratio ~3.1 chars/token surfaced (my $0.30 est used ~4 — flags that S33's batch projection is optimistic too; true on 3.1).
>
> **S40→S41 FIRST MOVES (the BUILD — everything is execution, no open architecture):** (1) anchor + confirm canon by content (v30 banner / Boot_ScopeReader v4.1 once cut / Progenitor v5 / whale registry all-4-RESOLVED). (2) **COST TRUE-UP FIRST ($0)** — measured ratios × real 181 distribution at Sonnet batch pricing + cache → cost band; Jake funds account to upper estimate (prepay gate). (3) **FOLD THE ADDENDUM → v4.1** (versioned reader cut; draft-PR → review → land). (4) **BUILD THE BATCH PIPELINE** (PLAN MODE first — writes code): per Batch_Read_Spec_v1 — skeleton-gate → assemble 181 batch requests (v4.1 cached system prompt + per-conv skeleton payload + custom_id=conv_uuid + NO tools) → batch-endpoint submit w/ batch-not-synchronous guard → poll/collect → persist via persist_node_file() to the flat pile → scrub-vN overlay on outputs. (5) **RUN THE 38 FREE ON-SUB ARM IN PARALLEL** (proven S39 loop, key UNLOADED, $0). (6) collect + merge (181 paid + 38 free + 130 whale → flat pile). (7) downstream UNCHANGED: Reconciliation 1 → texture → Reconciliation 2 → the Judge → retrieval engine (Progenitor §10-§11). (8) scrub-vN Supabase-pattern overlay (flag #4) on outputs + on CC's own report output. NO QUARANTINE; downstream geometry UNCHANGED.
>
> **DO-NOT-RELITIGATE (settled S40; rule-4 SUSPENDED — surface if off, NEW reason to reopen):** the on-sub ~13K-char delivery ceiling is STRUCTURAL (no fs in workflow runtime, agent()-only, output-capped) — PROVEN, do not re-attempt schema-passthrough or chunked-schema delivery (both killed on data); the corpus splits 38-free/181-paid by the ceiling (Option 2 refined — NOT hybrid, the free tier is the minority so two-pipelines-for-17%-free is the inverted marginal-gain trap); model = Sonnet 4.6 (GRADED richer-than-Opus, ~4× cheaper) + precision addendum (UUID + counts, tested 4/4); reader → v4.1 (addendum folded, versioned, v4.0 tombstoned); Sonnet 1M is API-real (no chunking the 181); billing = floor_db.env $0 / anthropic_billing.env paid, batch-not-synchronous guard load-bearing, prepay gate; faithful never bends (free below ceiling, paid above). + ALL v29/v28/v27 settled items stand UNCHANGED (Stage A locked bad80b5; cold-store closed; chunking-holds-corpus-wide; whale problem CLOSED route-from-registry; floor immutable + NEVER touched). NOTE: §7c (blindness) is RESOLVED for the 181 by the API path = TRUE tool-absence (no tools in the batch call — the strong form); §7c remains practical-not-structural ONLY on the parallel 38-conv on-sub arm (acceptable — small, and the on-sub delivery fix put the full payload in as embedded text so the reader has no motive to self-read; the maintenance drip lives here forever). · hot · read this + JAKE-RULES + Track_Meet_Doctrine + The_Wallaby_Why + The_Wallaby_Whales (FRAMEWORK, not reference) before working*
>
> *[v29 (S38, Stage A built+locked) remains current beneath this banner; v30 records the corpus-read split + model lock. All prior banners stand demoted-in-place.]*
```

**Then:** in v29's footer line and below, nothing else changes — v30 sits on top, v29 untouched.

---

## CHANGE-SET B — The_Progenitor_v5_2026-06-02.md → rescope the corpus-read clause + fix the reader ref

**Context:** Progenitor v5 is the law. It currently carries (from the S35/S36 lineage) the "on-sub chunked free" corpus-read framing. S40 rescopes it. Two surgical edits — do NOT rewrite the doc.

**Edit B1 — the corpus-read mechanism clause (§0.5 / §3.4 / §12 area — wherever the over-ceiling + corpus-read delivery is described).** Find the clause asserting the corpus reads on-sub/chunked/free corpus-wide. APPEND (do not replace) a rescope note:

```
[S40 RESCOPE] The "on-sub, free, corpus-wide" delivery holds ONLY for convs whose payload fits under the on-sub workflow mechanism's ~13K-char per-call delivery ceiling (proven structural S40 — the workflow runtime has no fs; agent() returns output-capped model text). Of 219 non-whale FITS_WHOLE convs, 38 fit (free on-sub) and 181 exceed it (paid batch API — Sonnet 4.6, 1M window, tools-absent, batched 50%-off). The reader, payload contract, persist, flat-pointer pile, and downstream geometry are IDENTICAL across both arms — only the read mechanism differs. Rescoped invariant: FREE-and-faithful below the on-sub delivery ceiling, PAID-and-faithful above it. Faithful never bends. The on-sub path survives as the maintenance drip (new small convs read free, forever). See Batch_Read_Spec_v1_2026-06-06.md for the paid arm.
```

**Edit B2 — the shape-reader reference.** Find every `Boot_ScopeReader_v4.0` / `test_call_system_prompt_S32.md` reference in the §12 shape-reader section. APPEND a note (do not change the v4.0 refs themselves — v4.0 is still the proven base):

```
[S40] The deployed reader for the corpus read is Boot_ScopeReader_v4.1 (= v4.0 + the precision addendum: UUID-preservation + exact-counts-in-TEXTURE; deployable test_call_system_prompt_S40.md). v4.0 / test_call_system_prompt_S32.md are the tombstoned-not-deleted base. The addendum is grounded in this doc's verbatim-by-pointer invariant — a node referencing another conv by UUID MUST keep the UUID verbatim (a name-only reference is not machine-resolvable and fails the pointer apparatus).
```

**Note:** if the dangling `Boot_ScopeReader.md` ref (the one S33/S35 handoffs flagged to fix → `Boot_ScopeReader_v4.0`) is STILL unfixed in the live doc, fix it to `Boot_ScopeReader_v4.1` while here. Confirm against the live file — do not assume it's still dangling.

---

## CHANGE-SET C — CHANGELOG.md → record the S40 cuts

**Action:** prepend a dated S40 entry. Records: the v4.1 reader cut, the ANCHOR v30 cut, the new Batch_Read_Spec_v1, and the finding.

```
## 2026-06-06 — apparatus S40 "Catalyst"
- **FINDING (structural):** the on-sub workflow mechanism has a hard ~13K-char delivery ceiling per agent() call (no Node globals in the workflow runtime — no fs/Buffer/require; agent() returns output-capped model text). Proven on the 574KB max-scale target (13,147 chars / 2.3% fidelity, model apologized mid-field). Two delivery fixes killed on data: schema-passthrough (same ceiling), 44-chunk-schema (over-build twin-bug).
- **DECISION:** corpus read splits by size — 38 sub-ceiling convs FREE on-sub (proven S39 loop), 181 over-ceiling convs PAID batch API. Option 2 refined (NOT hybrid — free tier is the 17% minority). Rescope of S35's "free and faithful": free below the on-sub delivery ceiling, paid above it.
- **MODEL LOCKED:** Sonnet 4.6 (graded against known-good Opus 01eb6e56 catalog — Sonnet richer: 46 nodes/17 FENCE vs 37/8, both mental-health FENCEs held, TEXTURE held; ~4× cheaper than Opus batched). Two precision findings (UUID drop, count dilution) resolved by the addendum.
- **NEW: Boot_ScopeReader_v4.1** (reference) + **test_call_system_prompt_S40.md** (deployable) = v4.0 + the PRECISION ADDENDUM (UUID-preservation + exact-counts-in-TEXTURE). Tested on e831e30b (45 UUIDs) → 4/4 verbatim, no fabrication, richness intact. v4.0 / test_call_system_prompt_S32.md TOMBSTONED-NOT-DELETED.
- **NEW: Batch_Read_Spec_v1_2026-06-06.md** — the build spec for the 181-conv paid batch arm.
- **ANCHOR v30** cut (decision banner — the split + the model lock). v29 demoted-in-place.
- **CORRECTION:** billing key path is ROOT anthropic_billing.env (a prior handoff carried the stale pipeline/secrets/.env path). Two-env model: floor_db.env ($0 Postgres) / anthropic_billing.env (paid). [also fixed in JAKE-STACK — change-set D]
- **MEASURED token ratios** (replace S33 projection): ~0.30-0.32 tok/char input; ~380-400 output tok/node. Real ratio ~3.1 chars/token (prior ests used ~4).
- **S40 spend:** $1.95 (3 synchronous grade calls).
```

---

## CHANGE-SET D — JAKE-STACK.md → correct/confirm the billing env path

**Action:** find the §-where the apparatus env files are documented (the floor_db.env / anthropic_billing.env rename was logged in the S38→S39 stretch). CONFIRM it reads:

- `anthropic_billing.env` lives at **repo ROOT** — the paid Anthropic API key; loaded ONLY for intentional metered/batch calls, cleared after.
- `floor_db.env` — the Supabase/Postgres floor connection; $0 reads; NEVER a billing call.
- `pipeline/secrets/.env` — the REFUSED-wall location; the API key is NOT here and does not go here (this wall is built and stays).

**If the live file already says this, no edit needed — just confirm.** If any handoff or note in the stack still points the billing key at `pipeline/secrets/.env`, correct it to ROOT `anthropic_billing.env`. (This is a correction of OC-S35's hand-carried note, which carried the stale path; the disk wins.)

---

## APPLICATION ORDER + NOTE FOR NEXT-CLAUDE

Apply A → B → C → D. A and C are prepends (safe). B is two appends + one conditional ref-fix (confirm against the live Progenitor before editing — do not assume the dangling ref state). D is a confirm-or-correct (likely already correct; verify).

None of these are load-bearing to START the S41 build — the build can run off Batch_Read_Spec_v1 + the v30 banner alone. Folding B/C/D is canon hygiene; do it at ignition or right after the true-up, not mid-batch. The ONE thing that must be real before the batch FIRES is the v4.1 reader cut (change-set is in Batch_Read_Spec §2, recorded in C) — the batch fires v4.1, not v4.0.
