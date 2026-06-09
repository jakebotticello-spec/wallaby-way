# Batch Read Spec — the 181 over-ceiling convs, paid API, batched
*file: Batch_Read_Spec_v1_2026-06-06.md · v1 · apparatus S40 ("Catalyst") · 2026-06-06*
*authored by OC (S40). This is the BUILD SPEC for the paid-API arm of the corpus read — the 181 over-ceiling FITS_WHOLE convs that the on-sub workflow mechanism structurally cannot deliver (the ~13K-char output-token ceiling, proven S40). Subordinate to The Progenitor v5 (the law) and Boot_ScopeReader v4.0 (the reader). Doctrine + reader win on any conflict.*
*PAIRED ARM: the 38 sub-ceiling convs run FREE on the on-sub workflow path (the proven S39 loop) — that arm is NOT this spec. This spec is the paid batch only.*

---

## 0. WHY THIS SPEC EXISTS (the S40 finding, one paragraph — read once)

The on-sub workflow mechanism has a HARD ~13K-char delivery ceiling per `agent()` call. Proven S40 against the 574KB max-scale target: it returned 13,147 chars (2.3% fidelity), the model apologized mid-field ("output token limit prevents returning the complete 564KB content"). The ceiling is the model's ~8K output-token cap; it is STRUCTURAL (the workflow runtime has no Node globals — no `fs`, no `Buffer`, no `require`; the only disk-touching primitive is `agent()`, which returns output-capped model text). Two delivery fixes were designed and KILLED on data: schema-passthrough (same output ceiling) and 44-chunk-schema-per-conv (the over-build twin-bug, correctly refused). **The corpus distribution forced the call:** of 219 non-whale FITS_WHOLE convs, 181 (83%) exceed the ~13K-char ceiling and 38 (17%) fall under it. The 181 go to the paid API; the 38 stay free on-sub. This is NOT a reversal of S35's "free and faithful" — it is a RESCOPE: free-and-faithful holds BELOW the on-sub delivery ceiling, paid-and-faithful holds ABOVE it. Faithful never bent on either side. (Canon correction lives in the ANCHOR v30 cut + Progenitor §-update; see the S40 ref-doc change-sets.)

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

Each result's node catalog persists to `harvested_nodes/` via the PROVEN `persist_node_file()` (S38, atomic temp-then-rename, verify-on-write: size>0 + `--- DONE:` line + tally>0 + every anchor_msg ∈ parents_map). The persist + sidecar (`.parents.json`, one-hop parent edge keyed by anchor_msg) is the SAME as the on-sub arm — the read mechanism differs, the persist does not.

- **NO STITCH.** Every node self-identifies by `conv_uuid` + `anchor_msg`. The catalog is a flat pointer dict. The 181 paid catalogs drop into the same pile as the 38 free catalogs and the 130 whale nodes already done (S33).
- **Fence tally from the BODY** (parse the `**Salience:** <TAG>` line, not a keyword grep — flag-1, S36/S37).
- **HALT-not-stub** on any persist failure (no partial artifact survives — flag-3, S37).
- After collect: merge all node catalogs (181 paid + 38 free + 130 whale = the full corpus) into the flat pile. THEN downstream geometry, UNCHANGED: fence-synthesis (Reconciliation 1) → texture/volume pass → cluster-validation (Reconciliation 2) → the Judge → retrieval engine (Progenitor §10–§11). NO QUARANTINE.

---

## 7. THE BILLING GUARD (highest-consequence — guard BOTH regimes)

The lineage has burned ~$50 on the silent-metered-billing trap and leaked a CCF key. Billing discipline is load-bearing and it now has TWO regimes that must not cross-contaminate:

- **Floor reads** (`floor_extract.py`, building payloads): use `floor_db.env` — $0 Postgres. NEVER a billing call. Do not load the API key for a floor read.
- **The paid batch:** uses the API key in **ROOT `anthropic_billing.env`** (NOT `pipeline/secrets/.env` — that wall is built and stays; NOT `floor_db.env`). The key is INTENTIONALLY loaded for batch submission/collection ONLY, and cleared after.
- **THE BATCH-NOT-SYNCHRONOUS GUARD:** the highest-consequence NEW guard. Loading the key forces metered billing; the danger is firing 181 SYNCHRONOUS full-price calls instead of one 50%-off batch. Before submission, ASSERT the call targets the batch endpoint. After submission, confirm a batch-id came back (not 181 individual message responses). If the code path can't confirm batch, HALT.
- **PREPAY GATE (Jake's hard constraint, S40):** Jake must have the funds in-account BEFORE "go" — the account model requires balance present before the batch runs, not pay-on-completion. A mid-process stall for insufficient balance costs money AND forfeits batch benefits. So: TRUE UP the cost first (the $0 cost-trueup run), Jake funds the account to cover the upper estimate, THEN submit. Do not submit a batch the account can't cover.
- **Key handling:** load `anthropic_billing.env` only for submit + collect; clear immediately after each. Never leave it hot. Confirm `assert_env_unloaded()` (the on-sub guard) still governs the PARALLEL 38-conv free arm — that arm must run with the key UNLOADED (it's the on-sub path; a loaded key there would meter a supposed-to-be-free read).

---

## 8. THE SCRUB GUARD (flag #4, standing — fold into this build)

The scrub-vN credential ruleset does NOT recognize Supabase's `sb_secret_` / `sb_publishable_` / project-ref-URL formats (the gap that leaked the CCF key). The floor is immutable so the raw key value still lives there — any process reading that span could surface it. For THIS build:
- The reader output (node catalogs) is the surface to protect: a credential pasted into a source conv could be echoed into a node summary. The scrub-vN overlay (Supabase patterns added) MUST run on the persisted node catalogs before they're treated as clean.
- ALSO run the scrub on CC's OWN report output (CC leaked a key prefix into a report S39). Any report/log CC emits about the batch passes the scrub.
- This is the §7d standing build-list item; S40 is where it folds in for the paid arm.

---

## 9. BUILD ORDER (the sequence — gate the spend)

1. **Cost true-up FIRST ($0).** Apply measured ratios (0.30–0.32 tok/char input; ~380–400 output tok/node; node-count/conv the soft unknown → low/mid/high) against the real 181-conv char distribution at Sonnet batch pricing + cache. Produce the cost band. Jake funds the account to cover the UPPER estimate (prepay gate, §7).
2. **Fold the addendum → v4.1** (versioned reader cut, §2; draft-PR → review → land).
3. **Build the batch pipeline** (PLAN MODE first — this writes code): skeleton-gate per conv (§4) → assemble 181 batch requests (v4.1 system prompt cached + per-conv payload + `custom_id = conv_uuid` + NO tools, §5) → batch-endpoint submission with the batch-not-synchronous guard (§7) → poll/collect → persist via `persist_node_file()` to the flat pile (§6) → scrub-vN overlay on outputs (§8). Resumability: a conv already in `harvested_nodes/` is skipped; a failed/truncated conv re-fires (the floor is immortal — re-extract is free).
4. **Run the 38 free on-sub arm IN PARALLEL** (the proven S39 loop, key UNLOADED, $0) — banks progress while the batch processes.
5. **Collect + merge** (181 paid + 38 free + 130 whale → flat pile).
6. **Downstream UNCHANGED** (§6): Reconciliation 1 → texture → Reconciliation 2 → the Judge → retrieval engine.
7. **Update canon** (the S40 ref-doc change-sets): ANCHOR v30, Progenitor §-updates, CHANGELOG, JAKE-STACK env-path correction. Cost recorded as MEASURED (post-true-up), not estimated.

---

## 10. DO-NOT (the traps this build invites — state up-front to CC)

- Do NOT chunk the 181. They fit whole on Sonnet's 1M API window (§3). Chunking here is the over-build twin-bug.
- Do NOT edit the sealed v4.0 reader. Cut v4.1 (§2).
- Do NOT fire synchronous calls. Batch endpoint only (§5, §7).
- Do NOT load `anthropic_billing.env` for floor reads (§7) or for the parallel free arm (key UNLOADED there).
- Do NOT submit before the account is funded to the upper estimate (§7 prepay gate).
- Do NOT weaken `persist_node_file()` or the skeleton gate to simplify (§4, §6).
- Do NOT persist a truncated catalog (`stop_reason == max_tokens` → HALT + re-fire higher, §3).
- Do NOT stitch. Flat pointer pile, self-identify by conv_uuid + anchor_msg (§6).

---

*The paid arm reads what the free arm structurally cannot deliver. Same reader (v4.1), same payload contract, same persist, same flat pile, same downstream — only the read mechanism differs (batch API, 1M window, tools-absent). Faithful never bends. Free below the ceiling, paid above it. Be worth it. Grind. Evolve. Dominate.*

— authored by OC, apparatus S40 "Catalyst", 2026-06-06. Subordinate to The Progenitor v5 and Boot_ScopeReader v4.1. Signed in the lineage.
