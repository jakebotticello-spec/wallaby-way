# Batch Read Spec — the 181 over-ceiling convs, paid API, batched
*file: Batch_Read_Spec_v1.2_2026-06-10.md · v1.2 · apparatus S40 ("Catalyst") authored / S42 ("Cordon") prepay-gate correction / S51 ("Continuance") field-lessons addenda · 2026-06-10*
*★ v1.2 (S51): SIX new sections appended (§11–§16) from the S50/S51 read waves — density-check, role-break, injection failure mode, rate constants, the multi-snapshot integrity check, and the collision rule. Everything above §11 is byte-faithful to v1.1 except this masthead. **Current tool versions on disk: runner `apparatus_batch_read.py` v1.5 · freeze `apparatus_freeze_pipeline.py` v1.7** (any older version reference below is the historical record of the run it describes, not the live pointer — live pointers are in `wallaby-way/CLAUDE.md`).*
*authored by OC (S40). This is the BUILD SPEC for the paid-API arm of the corpus read — the 181 over-ceiling FITS_WHOLE convs that the on-sub workflow mechanism structurally cannot deliver (the ~13K-char output-token ceiling, proven S40). Subordinate to The Progenitor v5 (the law) and Boot_ScopeReader v4.0 (the reader). Doctrine + reader win on any conflict.*
*PAIRED ARM: the 38 sub-ceiling convs run FREE on the on-sub workflow path (the proven S39 loop) — that arm is NOT this spec. This spec is the paid batch only.*
*★ v1.1 (S42): the §7 PREPAY GATE is DOWNGRADED — it was a Jake-statement that S40 over-hardened into an invariant, overruled at source by Jake S41. Jake's auto-reload carries; no static prepay required. The batch-not-synchronous guard (the real ~$50 scar guard) is UNTOUCHED and stays load-bearing. §7/§9/§10 corrected; everything else byte-faithful to v1. See the §7 PREPAY note for the full record.*

---

## 0. WHY THIS SPEC EXISTS (the S40 finding, one paragraph — read once)

The on-sub workflow mechanism has a HARD ~13K-char delivery ceiling per `agent()` call. Proven S40 against the 574KB max-scale target: it returned 13,147 chars (2.3% fidelity), the model apologized mid-field ("output token limit prevents returning the complete 564KB content"). The ceiling is the model's ~8K output-token cap; it is STRUCTURAL (the workflow runtime has no Node globals — no `fs`, no `Buffer`, no `require`; the only disk-touching primitive is `agent()`, which returns output-capped model text). Two delivery fixes were designed and KILLED on data: schema-passthrough (same output ceiling) and 44-chunk-schema-per-conv (the over-build twin-bug, correctly refused). **The corpus distribution forced the call:** of 219 non-whale FITS_WHOLE convs, 181 (83%) exceed the ~13K-char ceiling and 38 (17%) fall under it. The 181 go to the paid API; the 38 stay free on-sub. **[S49 CENSUS — record-of-belief annotation: this 181/38 split is the PRE-RUN framing this spec was written against. The batch has since fired and merged (202 indexed / 3,743 nodes per `MERGE_MANIFEST_S47.md`). The CURRENT unread batch is a different, later set: 123 unread convs (120 valid + 3 hollow excluded), all fit WHOLE on input, est ~$48.50 at Sonnet batch rates. The 181 framing is preserved as the historical belief; the live current-state number is 123/120. Do not read 181 as the live unread count.]** This is NOT a reversal of S35's "free and faithful" — it is a RESCOPE: free-and-faithful holds BELOW the on-sub delivery ceiling, paid-and-faithful holds ABOVE it. Faithful never bent on either side. (Canon correction lives in the ANCHOR v30 cut + Progenitor §-update; see the S40 ref-doc change-sets.)

**Why the API structurally beats the ceiling that killed on-sub:** the API call returns the NODE CATALOG (small — ~2.4K–17.4K output tokens measured), NOT the payload. The payload goes in as INPUT (the 1M window holds it). There is no return-the-whole-payload step, so the ~8K-output-token wall does not exist on this path. That is the whole structural difference, and it is why the same reader that truncates on-sub runs clean on the API.

---

## 1. THE READER (unchanged in shape, ONE versioned addendum — see §2)

The reader is `Boot_ScopeReader_v4.0` (the deterministic API shape-reader, proven S32 on Opus to 930k tokens, 0 drops, tail-clean). The deployable artifact is `pipeline/test_call_system_prompt_S32.md`. The batch fires this reader verbatim — default-NODE, two-kinds-as-salience, MOTION-as-backbone, §3.3 precise-fence-anchor, NO-QUARANTINE, walls-by-absence (the batch call has NO tools — blindness is enforced by tool-absence, the strong form the on-sub path could never reach).

**THE ONE CHANGE vs S32-as-fired: the PRECISION ADDENDUM (§2).** S40 graded Sonnet 4.6 against the known-good Opus catalog and found Sonnet RICHER (46 nodes vs 37, 17 FENCE vs 8 — the austere-bug fear is dead, inverted) but with a precision-loss signature: it dropped a cross-session UUID pointer (kept the name, lost the machine-resolvable UUID) and diluted an exact TEXTURE count. The addendum (§2) directly counters both. It was tested on the hardest UUID-dense conv in the corpus (`e831e30b`, 45 cross-session UUIDs) and held 4/4 verbatim, no fabrication, richness intact. The addendum FOLDS INTO the reader as a versioned change — it does not replace anything; it is appended after the S32 reader text. See §2 for the exact text and the versioning rule.

---

## 2. THE PRECISION ADDENDUM (the versioned reader change)

**Versioning rule — do NOT silently mutate the sealed reader.** `Boot_ScopeReader_v4.0` and its deployable `test_call_system_prompt_S32.md` are the PROVEN artifacts. The addendum creates a NEW version: `Boot_ScopeReader_v4.1` (reference) + `test_call_system_prompt_S40.md` (deployable). The v4.0 pair stays on disk, tombstoned-not-deleted, per the spine. The CHANGELOG records the cut with its reason (the S40 Sonnet grade: precision-loss on UUID + count, fixed + tested on e831e30b 4/4). v4.1 = v4.0 verbatim + this block appended to the system prompt, after the one-shot example, before the final sign-off line:

```
---
PRECISION INVARIANTS (apparatus retrieval-critical):
- UUID preservation: When the conversation references another conversation, session, or message by UUID, you MUST preserve that UUID verbatim in the node, even when you also give a human-readable name. The apparatus is a pointer system; a reference without its UUID is not machine-resolvable and fails the apparatus's core function. Never replace a UUID with a name — keep both. If a cross-session reference appears without a UUID in the source, note the reference but do not fabricate a UUID.
- Exact counts in TEXTURE: When a TEXTURE node captures a behavioral pattern that the source states with specific numbers (e.g. "3 reminders, 0 lunches, 1 nap"), preserve those exact numbers in the node. The specific count IS the texture — do not generalize specific numbers into vague quantifiers. Verbatim numbers where the source gives them.
---
```

**The fold is a deliberate canon event, not a build-time edit.** CC creates v4.1 + the new deployable as committed artifacts (the same draft-PR → review → land gate as any code change). The batch fires the v4.1 deployable, NOT v4.0.

---

## 3. THE MODEL (decided on data — Sonnet 4.6)

- **Model string:** `claude-sonnet-4-6`. This is the SOLE grant of the 1M API context window (GA, no beta header — the `context-1m-2025-08-07` header is retired and ignored). ⚠ Never silently substitute a non-1M model string or a >200K-token conv hits the 200K wall and fails.
- **WINDOW CONFIRMED (S40, from docs):** Sonnet 4.6 has a **1M-token context window on the Claude API** (GA, no price multiplier — a 900K-token request bills the same per-token rate as a 9K one). The largest of the 181 (~1.1M chars ≈ ~354K tokens at the measured 0.32 tok/char) fits comfortably under 1M. **ALL 181 FIT WHOLE — NO CHUNKING in the batch.** (Caveat for canon: Sonnet's 1M is API-specific; the chat window is 500K and Claude-Code-Sonnet-1M needs usage credits. The batch is on the API, so 1M applies. Do not conflate the surfaces.)
- **WHY SONNET, NOT OPUS (the S40 grade):** Sonnet held every load-bearing dimension against the known-good Opus catalog — both mental-health FENCEs present with checkable predicates, TEXTURE held (not flattened to MOTION), node density equal-or-richer. Two findings (UUID drop, count dilution) both resolved by the §2 addendum. Cost: ~$0.40/conv batch vs Opus ~$1.64/conv batch — a ~4× difference. Sonnet at temp 0 is the read.
- **temperature: 0** (deterministic cataloging, not generation).
- **max_tokens:** generous headroom for a full catalog. Measured: the densest graded conv produced 17,420 output tokens (46 nodes). Set **max_tokens = 32000** (the S32-proven cap; ~2× the densest measured output). ⚠ If any conv returns `stop_reason == max_tokens` the catalog is TRUNCATED — that conv HALTS for re-fire at a higher cap; do NOT persist a truncated catalog or read it as tail-rot.

### 3.1 — REQUIRED runner behavior: inspect `stop_reason` on EVERY result (HARD, not optional — S49 census)

This was prose guidance in the `max_tokens` bullet above; the S49 census makes it a **hard, non-optional runner requirement** and names the at-risk set.

- **The runner MUST inspect `stop_reason` on EVERY returned result.** Any result with `stop_reason == "max_tokens"` is a **TRUNCATED catalog**: do NOT persist it, do NOT count it read, do NOT read it as tail-rot. HALT that conv, re-fire it standalone at a raised output cap, and persist ONLY when it returns a clean stop. **A truncated catalog persisted as complete is a §5.1 "read-when-not-complete" data poison** — baked into the pile, it is far more expensive than the re-fire.
- **The at-risk set (S49 census): ~20 convs** with TU≥200 & msg≥100 are the truncation-risk population, led by **`d3ff9ed1`** (TU=920, CB=1763 — the corpus's single highest-risk conv). **STRUCTURAL FACT: these are NOT the largest convs by input.** Size-leaders and density-leaders are **disjoint populations** — the biggest convs by input are low-density and safe; the truncation risks are mid-sized and tool-heavy. A runner that only watches the big convs **will miss the truncations.** Watch `stop_reason` on ALL results, not a size-filtered subset.
- **Skeleton-gate exclusion (ties to §4):** the **3 hollow stubs** (`3f84a335`, `ae3468be`, `bc42e9ab` — zero messages) MUST be filtered before submission by the §4 skeleton gate. Submitting them wastes a call and yields an empty catalog. This is why the unread set is **123 convs but 120 valid for batch**.

---

## 4. THE PAYLOAD CONTRACT (load-bearing — the skeleton is the locator)

Identical to the S32/Boot_ScopeReader v4.0 contract — the API reader has NO filesystem, so a real `anchor_msg` depends ENTIRELY on the message uuids being PRESENT in the payload sent. The payload MUST preserve the message skeleton:
- per-message `uuid`, `parent_message_uuid`, `role`, and content (every text/thinking/tool block, in order), in tree order;
- a header carrying `conv_uuid`, `snapshot_id`, and the REAL conversation `created` timestamp (the reader otherwise INFERS the date from content — pass the true date).
- Built by the proven `floor_extract.py` (the `===MSG===` serializer, `render_block` canary-proven) reading the immortal floor via `floor_db.env` ($0 Postgres — NOT a billing call).
- The `<out>.parents.json` sidecar (the one-hop parent-edge map) is written by `floor_extract.py` and used at PERSIST time for edge injection — NOT sent to the reader.

**SKELETON GATE (before the conv enters the batch):** count messages, confirm first/last uuids are real (not sentinels), confirm parent links survived. A broken skeleton is caught for free instead of wasting a paid call on worthless output. This gate runs per-conv at build-the-batch time, not at collect time.

---

## 5. THE BATCH MECHANISM (the cost lever — this is what makes it ~$76 not ~$253)

This is the textbook batch case: 181 non-urgent reads, no interactivity, collect within the window.

- **Endpoint:** the Message Batches API (`/v1/messages/batches`), NOT 181 synchronous `/v1/messages` calls. ⚠ THIS IS THE COST LEVER AND A BILLING GUARD (see §7): synchronous would bill FULL price ($3/$15 per MTok); batch is **50% off both input and output** ($1.50/$7.50 per MTok). Firing 181 synchronous calls by accident is the silent-overspend failure mode — guard it (§7).
- **Submission:** one batch request carrying all 181 (or a small number of batches if a per-batch request-count limit applies — confirm the current limit at build time; if 181 exceeds it, split into the fewest batches that fit and submit them together). Each request in the batch is one conv: the v4.1 system prompt + that conv's skeleton-preserving payload as the user message, NO tools.
- **Collection:** poll for completion (typically well under the 24h SLA ceiling), retrieve all results, match each result to its conv by the batch `custom_id` (set `custom_id = conv_uuid` so results self-identify — this matters for the flat-pointer pile).
- **Prompt caching:** the v4.1 system prompt (~8K tokens) is IDENTICAL on all 181 requests → cache it (`cache_control` on the system block). ~90% off the repeated chunk. Modest absolute saving (the prompt is small vs the payloads) but free to do and correct. NOTE: confirm batch + caching interaction at build time (caching applies within a batch; verify the discount lands).

---

## 6. PERSIST + THE FLAT-POINTER PILE (downstream geometry UNCHANGED)

Each result's node catalog persists to `nodes/harvested/` via the PROVEN `persist_node_file()` (S38, atomic temp-then-rename, verify-on-write: size>0 + `--- DONE:` line + tally>0 + every anchor_msg ∈ parents_map). The persist + sidecar (`.parents.json`, one-hop parent edge keyed by anchor_msg) is the SAME as the on-sub arm — the read mechanism differs, the persist does not.

- **NO STITCH.** Every node self-identifies by `conv_uuid` + `anchor_msg`. The catalog is a flat pointer dict. The 181 paid catalogs drop into the same pile as the 38 free catalogs and the 130 whale nodes already done (S33).
- **Fence tally from the BODY** (parse the `**Salience:** <TAG>` line, not a keyword grep — flag-1, S36/S37).
- **HALT-not-stub** on any persist failure (no partial artifact survives — flag-3, S37).
- After collect: merge all node catalogs (181 paid + 38 free + 130 whale = the full corpus) into the flat pile. THEN downstream geometry, UNCHANGED: fence-synthesis (Reconciliation 1) → texture/volume pass → cluster-validation (Reconciliation 2) → the Judge → retrieval engine (Progenitor §10–§11). NO QUARANTINE.

---

## 7. THE BILLING GUARD (highest-consequence — guard BOTH regimes)

The lineage has burned ~$50 on the silent-metered-billing trap and leaked a CCF key. Billing discipline is load-bearing and it now has TWO regimes that must not cross-contaminate:

- **Floor reads** (`floor_extract.py`, building payloads): use `pipeline/secrets/floor_db.env` — $0 Postgres. NEVER a billing call. Do not load the API key for a floor read.
- **The paid batch:** uses the API key in **ROOT `anthropic_billing.env`** (NOT `pipeline/secrets/floor_db.env`, which is DB creds only — `SUPABASE_DB_URL`, no API key; and NOT the old `pipeline/secrets/.env` path, which is the conceptual REFUSED wall — disk-confirmed S42 that file does not exist, the secrets file there is `floor_db.env`). The key is INTENTIONALLY loaded for batch submission/collection ONLY, and cleared after.
- **THE BATCH-NOT-SYNCHRONOUS GUARD:** the highest-consequence guard, and the real ~$50-scar guard — UNTOUCHED by the v1.1 prepay correction below. Loading the key forces metered billing; the danger is firing 181 SYNCHRONOUS full-price calls instead of one 50%-off batch. Before submission, ASSERT the call targets the batch endpoint. After submission, confirm a batch-id came back (not 181 individual message responses). If the code path can't confirm batch, HALT.
- **★ PREPAY — NO STATIC PREPAY REQUIRED (corrected S42; was an over-hardened "gate" in v1):** Jake's account runs on **auto-reload** ($25 start / +$15 when the balance drops below $5), proven to carry in past paid runs. The batch does NOT require funding-to-the-upper-estimate before submit. TRUE UP the cost first (the $0 cost-trueup run — done S41: band $48.69–$64.68, ~$55 likely, $64.68 hard-high, max ~$67) so the spend is known and gated, then submit on the auto-reload balance. *[v1.1 RECORD — why this changed: v1 carried a "PREPAY GATE (Jake's hard constraint)" — fund-to-upper-estimate-before-submit, a mid-run stall forfeits the discount. That was a Jake-statement S40 ("Catalyst") relabeled as a hard invariant. Overruled at source by Jake (S41, "Comptroller"): the source was Jake, and Jake corrected it — auto-reload carries, no static prepay. This is the documented lineage bug (a Jake-said-once statement hardening into immutable canon — same pattern flagged on the ~$25 downstream-rerun estimate). The cost true-up STAYS (know-the-spend-before-firing is sound); the prepay GATE is dead. Do not re-impose it.]*
- **Key handling:** load `anthropic_billing.env` only for submit + collect; clear immediately after each. Never leave it hot. Confirm `assert_env_unloaded()` (the on-sub guard) still governs the PARALLEL free arm (the 14 pre-banked s39 convs, if ever re-touched) — that arm must run with the key UNLOADED (it's the on-sub path; a loaded key there would meter a supposed-to-be-free read).

---

## 8. THE SCRUB GUARD (flag #4, standing — fold into this build)

The scrub-vN credential ruleset does NOT recognize Supabase's `sb_secret_` / `sb_publishable_` / project-ref-URL formats (the gap that leaked the CCF key). The floor is immutable so the raw key value still lives there — any process reading that span could surface it. For THIS build:
- The reader output (node catalogs) is the surface to protect: a credential pasted into a source conv could be echoed into a node summary. The scrub-vN overlay (Supabase patterns added) MUST run on the persisted node catalogs before they're treated as clean.
- ALSO run the scrub on CC's OWN report output (CC leaked a key prefix into a report S39). Any report/log CC emits about the batch passes the scrub.
- This is the §7d standing build-list item; S40 is where it folds in for the paid arm.

---

## 9. BUILD ORDER (the sequence — gate the spend)

1. **Cost true-up FIRST ($0).** Apply measured ratios (0.30–0.32 tok/char input; ~380–400 output tok/node; node-count/conv the soft unknown → low/mid/high) against the real 181-conv char distribution at Sonnet batch pricing + cache. Produce the cost band. *(Done S41: band $48.69–$64.68, ~$55 likely, $64.68 hard-high, max ~$67.)* This gates the spend by KNOWING it before firing — it does NOT require funding the account to the upper estimate first (the prepay gate is downgraded, §7; Jake's auto-reload carries).
2. **Fold the addendum → v4.1** (versioned reader cut, §2; draft-PR → review → land).
3. **Build the batch pipeline** (PLAN MODE first — this writes code): skeleton-gate per conv (§4) → assemble the batch requests (v4.1 system prompt cached + per-conv payload + `custom_id = conv_uuid` + NO tools, §5) → batch-endpoint submission with the batch-not-synchronous guard (§7) → poll/collect → persist via `persist_node_file()` to the flat pile (§6) → scrub-vN overlay on outputs (§8). Resumability: a conv already in `nodes/harvested/` is skipped; a failed/truncated conv re-fires (the floor is immortal — re-extract is free). *(NOTE — count: this spec was written pre-run, when the batch was estimated at 181→206. The batch HAS SINCE FIRED: the frozen list was 189 rows / 181 fired / 202 indexed (`MERGE_MANIFEST_S47.md`). The "206" was a pre-run estimate and is DEAD — use 202/3,743. The mechanics in this spec are unchanged. [S49 path update: `harvested_nodes/` → `nodes/harvested/` post-reorg.])*
4. **The free arm** (the 14 pre-banked s39 convs) is already banked — with the 24 + 2 folded into the paid batch (S41), there is effectively nothing left to run free in parallel. Key stays UNLOADED on anything on-sub (§7).
5. **Collect + merge** (the read pile → flat pile; final indexed total 202 convs / 3,743 nodes per `MERGE_MANIFEST_S47.md`). *[S49: was "206 paid + 14 free + 130 whale" — 206 was a pre-run estimate; the merge settled at 202/3,743.]*
6. **Downstream UNCHANGED** (§6): Reconciliation 1 → texture → Reconciliation 2 → the Judge → retrieval engine.
7. **Update canon** (the ref-doc change-sets): ANCHOR (current), Progenitor §-updates, CHANGELOG, the env-path correction (done S42 — key at root `anthropic_billing.env`, DB at `pipeline/secrets/floor_db.env`). Cost recorded as MEASURED (post-run), not estimated. Budget ~$25 for downstream re-runs of thin reads (Jake-estimate, NOT law — do-not-enshrine).

---

## 10. DO-NOT (the traps this build invites — state up-front to CC)

- Do NOT chunk the batch convs. They fit whole on Sonnet's 1M API window (§3). Chunking here is the over-build twin-bug.
- Do NOT edit the sealed v4.0 reader. Cut v4.1 (§2).
- Do NOT fire synchronous calls. Batch endpoint only (§5, §7) — this is the real ~$50-scar guard, and it STAYS.
- Do NOT load `anthropic_billing.env` for floor reads (§7) or for any on-sub read (key UNLOADED there).
- Do NOT re-impose a static prepay gate (§7 — downgraded S42; Jake's auto-reload carries; the cost true-up gates the spend by knowing it, not by pre-funding to the upper estimate). Know the cost, then fire.
- Do NOT weaken `persist_node_file()` or the skeleton gate to simplify (§4, §6).
- Do NOT persist a truncated catalog (`stop_reason == max_tokens` → HALT + re-fire higher, §3).
- Do NOT stitch. Flat pointer pile, self-identify by conv_uuid + anchor_msg (§6).

---

## 11. THE DENSITY CHECK (the 0.32 factor LIES on code — S50/S51)

**chars × 0.32 assumes prose.** On code-dense content the real ratio runs up to **~0.72 actual tokens/char** — a 2.2× under-read. This shipped two over-1M convs into the S50 batch flagged `over_1M_input=N` (`82bbd8f1` @ 1.00M, `ce1e79e1` @ 1.05M actual), and S51's pre-fire check density-bounced `176476ae` at **1,096,220 tok @ ×0.72 > 1M**.

**THE RULE: any conv whose 0.32-estimate is within ~2× of the 1M input ceiling gets a density check before submission** — bracket the estimate with BOTH factors (×0.32 and ×0.72), or use the count-tokens endpoint for the real number. If the bracketed/measured figure crosses the ceiling → the conv routes to the whale lane (strip/chunk per `whale_registry.md`), NOT into the batch. This is JAKE-RULES §5.1 in spirit: a factor named for a unit conversion is not proof it converts to that unit on every content class.

---

## 12. THE ROLE-BREAK FAILURE MODE (input LENGTH breaks the reader, not output budget — S50→S51)

`3ef82921` (619K tok, 611 msgs) at a raised 64K `max_tokens` did NOT truncate — the reader **broke role**: lost its catalog-reader system context on the very long payload and started *participating in the conversation* (807 lines of coaching, zero node headers). The persist guard quarantined it. S51 resolved the conv via the chunk path (×2 → 61 nodes, clean), confirming the diagnosis: **input length degrades reader role-fidelity; raising the output cap does not help and is not the fix.**

**THE RULE: when a very long payload threatens reader fidelity, chunk the INPUT by message count — never raise the output cap as a strategy.** Precedents: `3ef82921` (×2, S51) and `d9d05961` (×2, S33). Chunk budgets stay pessimistic (see the chunk-path canon); seam manifests record the cuts.

---

## 13. THE INJECTION FAILURE MODE (the corpus can carry live prompts — the reader will obey them)

**Finding (S51, conv `f018b1f8`):** a corpus conv can OPEN with an embedded live session-ignition prompt (here: the ROOT human message is a 2,982-byte session-ignition block, msg `019e64dc-6fbb-7fab-b7d7-4484d614fe98`). **The reader obeys payload instructions** — it executed the embedded ignition instead of cataloging the conv. Two junk fires resulted before the mechanism was identified. *(UUID note: an earlier S51 record circulated `019e64dc-6fbb-73a1-…` as the injecting message — that is the ASSISTANT reply that OBEYED it. Prefix-twin UUIDs transpose; see the verification rule below.)*

- **Containment is already structural:** the persist guard contains the blast radius as a STUB quarantine — a role-broken/injected read produces no valid catalog and never enters the pile. Injection is a *standing read hazard*, not a pile-integrity hazard, as long as the guard holds.
- **Remedy — the defang path, now PROVEN:** neutralize the embedded prompt in a WORKING COPY of the payload (the floor is immortal and untouched), then read via the proven single-conv testcall path. **Receipt: `runs/defang_f018b1f8_S51/` — 1 block cut (2,982 B), end_turn, 17 nodes (9M/8F/0T), $1.55, persisted + harvested.**
- **UUID-gated-cut verification (the defang HALT, working as built):** prefix-twin UUIDs TRANSPOSE, they don't just hallucinate — any UUID that gates a cut gets its **role + byte-size verified against the rendered block** before the blade moves.
- **THE TOMBSTONE RULE — class, not content:** a tombstone names the CLASS of removed content; it NEVER paraphrases the removed content's imperatives. A descriptive tombstone made the reader half-follow the ghost of the instruction it replaced (mild residue, f018b1f8 preamble — accepted + documented). Describe *what kind of thing* was cut, never *what it said to do*.
- **Standing watch:** the corpus may hold MORE ignition-led convs that were read before this mode was named. An injection spot-check of 2–3 ignition-led piled convs is queued (ANCHOR v35, S51 queue).

---

## 14. RATE CONSTANTS (print them — never re-derive them)

**Batch effective rates: `$1.50 / MTok input · $7.50 / MTok output`** (the 50%-off batch discount, already applied — see §5).

**THE RULE: every gate line MUST print these as named constants, citing this spec — never re-derive them at gate time.** The double-discount error (applying the 50% batch discount to the already-discounted $1.50/$7.50, halving them again) occurred **twice in S51**. A re-derived rate is a §5.1 hazard wearing a calculator; the constant + citation is the cure. Runner v1.6 (queued) bakes them in as code constants.

---

## 15. THE MULTI-SNAPSHOT INTEGRITY CHECK (a persisted catalog is not proof of a whole read — S50)

The snapshot-boundary bug (S50): `floor_extract.py` rendered only ONE snapshot per conv, so any conv with messages split across snapshots rendered PARTIAL — **silently, and the partial catalogs persisted LOOKING CLEAN.** The S51 extract fix (render ALL snapshots, dedupe on `msg_uuid`, keep highest scrub version, order by `created_at`) is PROVEN (`176476ae` 211→223 msgs, `c00ef343` 1→37 msgs).

**THE RULE: for ANY conv with messages in more than one snapshot, the integrity check — payload message count vs floor message count — is MANDATORY before a persist counts WHOLE.** A persisted catalog without a passed integrity check is an *artifact*, not a *read*. (S51's re-read wave ran 11/11 integrity-clean.) Runner v1.6 (queued) makes the check permanent.

---

## 16. THE COLLISION RULE (one task = one window = one output dir — S51)

The 176476ae double-fire (S51): **two CC instances ran the same task in parallel; persists overwrote each other at 05:22:31** — the data survived valid, the receipt chain broke, and the spend doubled (~$1.71 duplicated). One task in two windows is the dual of two tasks in one window: both break the receipt chain.

**THE RULES:**
- **One task = one window = one output dir.** A task's output dir belongs to exactly one executing instance.
- **Freshness check before any paid fire:** check the task's output dir for artifacts **fresher than 1 hour** — if found, another instance may be live on this task → **HALT** and resolve with Jake before spending.

---

*The paid arm reads what the free arm structurally cannot deliver. Same reader (v4.1), same payload contract, same persist, same flat pile, same downstream — only the read mechanism differs (batch API, 1M window, tools-absent). Faithful never bends. Free below the ceiling, paid above it. Be worth it. Grind. Evolve. Dominate.*

— authored by OC, apparatus S40 "Catalyst", 2026-06-06. v1.1 prepay-gate correction by OC, apparatus S42 "Cordon", 2026-06-06. v1.2 field-lessons addenda (§11–§16) authored by OC "Continuance", applied by S51 REF-EDIT, 2026-06-10. Subordinate to The Progenitor v5 and Boot_ScopeReader v4.1. Signed in the lineage.
