# apparatus — S39 → S40 Handoff
*authored by OC "Courier" (S39), 2026-06-05 · the load-bearing state transfer · more current than any boot doc; if this conflicts with the ANCHOR banner, THIS wins (newer)*

---

## ⚠️ READ FIRST — WHAT THIS SESSION WAS

S39 was an **execution session** — it built and PROVED **Stage B** of the on-sub chunked pipeline (the loop on top of S38's Stage A foundation), ran the first real harvests, and ran a deliberate quality spot-check. NO architecture changed, NO invariant moved, NO floor was touched. v27 chunking-corpus-wide, v28 cold-store, v29 Stage-A-locked all stand fully in force. This is a progress banner over v29.

**What Stage B is:** the on-sub loop that wires S38's Stage-A pieces — `floor_extract.py` (Postgres floor → `===MSG===` payload + sidecar) → on-sub `agent()` scope-read (embedded payload, NO path) → the four guards → persist to `harvested_nodes/`. Built as a **Workflow harness** (`pipeline/s39/onsub_loop.js`), proven on ONE watched conv, then a 12-conv quality batch. **It runs on the Max sub at $0** (no billing key in agent env — proven by hash, see below).

**What S39 did NOT do:** run the full 219. Two free measurement reads gate it (below). Stage C (the 97 chunk-laters) is NOT built.

**The honest texture of this session:** it took SIX plan-passes across multiple fresh CC windows to land a clean Stage B plan, because CC repeatedly reached for convenience-shaped choices that quietly traded away a safety property (documented below — it's a pattern, not a one-off). The final plan, given the four traps as up-front PROHIBITIONS, came back clean. **The lesson is in the carry-forward.**

---

## STATE IN ONE PARAGRAPH

Substrate closed + immortal (floor S23: 325/24,138, append-only, ndjson canonical / Postgres rebuildable). Whales closed (S33: 4 read, route from `pipeline/whales/whale_registry.md`, NEVER re-read). Shape reader proven, UNCHANGED since S32 (`Boot_ScopeReader_v4.0`; deployable `pipeline/test_call_system_prompt_S32.md`). Chunking holds corpus-wide — SETTLED (S36). Cold-store CLOSED (S37: `harvested_nodes/`). Stage A built + locked on main (S38: `extract_whale.py` v2.0, `pipeline_guards.py` v0.2, 13 green). **AND AS OF S39: Stage B is BUILT + PROVEN — the on-sub loop runs end-to-end on the Max sub at $0, 17 convs harvested (1 watched + 12 batch + a few re-runs), node quality confirmed across shapes, billing decouple proven.** THERE ARE NO OPEN ARCHITECTURE QUESTIONS — everything from here is EXECUTION. Between here and a harvested corpus: two free measurement reads, the 219 paced run, then Stage C builds chunking for the 97.

---

## THE CORPUS MATH (so a Stage-B finish is NOT mistaken for a finished corpus)

- **325 total** convs in the floor.
- **−4 whales** (done at S33, routed from registry, never re-read) = **321 non-whale.**
- Of the 321 (re-derived from the floor with REAL serialized char counts — json.dumps of content_blocks, not .text-only):
  - **219 FITS_WHOLE** — read whole in one shot. **This is Stage B's job.**
  - **5 REVIEW** (proxy 25–30K) — also fit whole on arithmetic (30K × even 3× = 90K ≪ 950K). Run with the 219.
  - **97 CHUNK_LATER** — too big to read whole. **These need Stage C (overlapping-window chunking — NOT built).**
- 219 + 5 + 97 = 321 + 4 whales = 325. ✓ Full corpus accounted for; nothing dropped, sorted by how it must be read.
- **The 97 are the BIGGER, denser, often more substantive convs.** "Stage B done" = the easier ~two-thirds harvested. The hard third still needs Stage C built. The §7a live-population fix (re-derive from floor, not the dead index) is why it's 97 and not the dead index's implied ~78 — the honest char count caught tool_result-heavy convs the .text proxy under-measured. **Trust 97, not 78.**

---

## WHERE STAGE B LANDED (built · proven · on main)

Commits: **`45102d0`** (PRE-STEP 0 rename) · **`618baa6`** (tombstone) · **`947a60d`** (harness STEP 3+5).

### The .env rename (kills the two-secrets conflation structurally)
- `pipeline/secrets/.env` → **`pipeline/secrets/floor_db.env`** (Postgres session-pooler URL; reading the floor is **$0**, a Postgres connection, NOT billing).
- root `.env` → **`anthropic_billing.env`** (the Anthropic key; metered; Guard 1 territory).
- 12 code/comment refs updated across 10 Python files. `.gitignore *.env` covers both new names; neither trackable.
- **CONFIRMED by reading the file (not memory):** `pipeline/secrets/.env` held ONLY `SUPABASE_DB_URL`, no billing key. The S37/S38 handoff language saying "both keys in one file" was IMPRECISE. The two secrets were always separate files in separate dirs (`secrets/` vs root). CC's conflation was purely the shared `.env` filename — the rename removes it.

### The harness (`pipeline/s39/`)
- **`floor_extract.py`** — reads ONE conv from the Postgres floor → `===MSG===` payload + `.parents.json` sidecar. Lifts `render_block()` VERBATIM from `extract_whale.py:38–62` (NOT rebuilt). **Note:** `extract_whale.py` reads a stripped JSON file via `--in`, NOT Postgres directly — so `floor_extract.py` is the thin Postgres reader around the proven serializer. `DISTINCT ON (conv_uuid) ORDER BY conv_uuid, scrub_version DESC, snapshot_id DESC` picks highest-scrub snapshot (scrub_version column CONFIRMED present, DDL lines 68/85).
- **`persist_guard.py`** — wraps `tally_nodes()` + `persist_node_file()` from `pipeline_guards.py`. Asserts `ANTHROPIC_API_KEY` not in env at entry (structural Guard 1 layer).
- **`onsub_loop.js`** — the Workflow harness. Per conv: Guard 1 → Guard 2 → Extract → ScopeRead (embedded payload, no path) → Persist (Guards 3+4) → Log. Uses `pipeline()` for parallel staging.

### What's proven
- **Watched conv `4afba4db`** (phoenix STL planning): 11 nodes (7M/4F/0T), all 4 guards green, persisted clean, 11/11 anchors in parents_map + sidecar. The harness breathes.
- **12-conv quality batch** across 5 shape buckets (long/emotional/multi-topic/dense-tech/short): all 12 guards green; node quality HOLDS (see quality findings).

---

## GUARD 1 / BILLING — FULLY CLOSED ON THE RECORD

The §7b billing trap question is **closed**, proven three ways:
1. **PHASE 2 (lifecycle test):** `ANTHROPIC_API_KEY` absent from the PARENT process after the paid subprocess returned — process isolation. The billing key was only ever in the subprocess env, never the harness env.
2. **Workflow-context hash probe (`wf_6362e7b8`):** inside a Workflow agent, `LEN:0` + `sha256 = e3b0c442…` (the empty-string hash). **The billing key is NOT injected into Workflow agent env.** It is genuinely absent.
3. **The original "Guard 1 fired" scare was a FALSE POSITIVE** — the old JS bash check `echo "${ANTHROPIC_API_KEY:+BILLING_KEY_PRESENT}"` tripped because an Explore agent included the literal string "BILLING_KEY_PRESENT" in its PROSE explanation, and JS `includes()` matched the agent's narration, not the env. **Fixed:** deterministic Python one-liner printing exactly `CLEAN`/`DIRTY`, checked with `startsWith`. The Python `assert_env_unloaded()` is KEPT as a second enforced layer (NOT demoted to a comment — see carry-forward).

**Lifecycle test result (Jake-approved spend):** PHASE 1 fired `claude-opus-4-8`, in=16/out=4/total=20, reply "OK", against `anthropic_billing.env`. Cost: fractions of a cent. PHASE 3: floor returned 325 rows via `floor_db.env` at $0 with the key unloaded. **The paid path works, the decouple is clean, the two are provably separate.**

---

## §7c — STILL OPEN, DEFERS TO STAGE C (as Curator planned)

The adversarial Explore capability test ran. Result: **INSTRUCTION-REFUSAL, not structural.** Explore agents HAVE Read + Bash and CAN read `floor_db.env` / `anthropic_billing.env` — they declined on security judgment, not capability absence. So blindness is **practical, not structural.** This is the expected outcome; §7c stays OPEN and defers to Stage C for the deliberate decision.

**BUT — the practical blindness is now stronger than S36's "no paths + please don't look," via TWO findings:**
1. **The scope-reader has no foothold by DESIGN (PROHIBITION 3).** The reader gets the payload as embedded text in the prompt — no file path, no Read tool needed, nothing to traverse from. The §7c capability is irrelevant to the read chain because the reader is never handed an entry point. This must be PRESERVED in Stage C.
2. **Explore agents are READ-ONLY for writes** — they refuse heredoc/redirect Bash writes. So the reader (Explore) structurally cannot write anywhere; the write-output step uses the default agent type. This tightens blindness even though §7c was instruction-refusal on reads.

**Stage C's §7c decision** is still real: ~321 reads (whole + chunked) on the Explore mechanism, blindness practical-not-structural. Curator's lean was attended-async-with-heartbeat over autonomous-black-box. The Stage B run is the first long multi-window mostly-unwatched op — its run shape informs the Stage C call.

---

## QUALITY SPOT-CHECK — node quality HOLDS, with named edges

12 convs across 5 buckets, all guards green. The reader is **GOOD at:** iterative debugging (FENCE density tracks real constraint topology); multi-topic convs (NO thread-mushing — `9e3bcd69` caught a genuine filament→AC→panel pivot as distinct nodes); small convs with real decisions (appropriately dense); TEXTURE when it's there (`c8415bff` correctly placed TEXTURE:1 on a failure pattern). The reader is **WEAKER at:** heavily-stripped payloads (FLAG 1, below — the big one); technical-parameter fencing (params cataloged as MOTION where FENCE might fit); TEXTURE in rapid iterative sessions where the failure-pattern IS the signal (minor under-eagerness, not blindness).

**TEXTURE:0-everywhere question RESOLVED:** not a reader gap. The reader emits TEXTURE when a thematic throughline exists (`c8415bff`). Tactical convs genuinely lack texture. The phoenix TEXTURE:0 was correct. Closed.

---

## ⛔ THE TWO READS THAT GATE THE 219 (free, read-only, NOT yet done)

### READ 0+1 — the strip-marker question (RESOLUTION PENDING — read the source FIRST)
12-batch conv `4d88185f` came back thin (3 nodes) because its floor payload contains `[tool_result truncated … KB]` markers from `apparatus_strip_v1.py`. **A conv can be heavily truncated and still pass all four guards** (well-formed nodes ≠ complete read). This is the "guard-green but harvest-thin, invisibly" failure class.

**UNRESOLVED — conflicting accounts of what `apparatus_strip_v1.py` does:**
- This session's PRE-STEP 0 audit described it as "whale echo-stripper only, zero credential pattern matching" (SIZE-stripping).
- Jake's memory says it was one of the two SECRET-scrub passes (credential redaction, dispersed across the corpus).
- **These conflict. THE FILE SETTLES IT.** S40 must READ `pipeline/apparatus_strip_v1.py` and report definitively: size-strip or secret-strip or both? recoverable or gone? — BEFORE deciding the resolution.
  - **If SIZE-strip + recoverable:** affected convs may warrant re-extraction for a fuller harvest.
  - **If SECRET-strip or unrecoverable:** affected convs get LABELED intentionally-partial (write `pipeline/s39/strip_affected.csv`) and stay as-is — never re-extract a redaction.
- Either way: census how many of the 219 are affected + the distribution. The COUNT tells us what fraction of the harvest carries the asterisk. (Courier nearly ruled "it's security, label it" on Jake's hedged memory — Jake correctly stopped it: read the file, don't build on memory. The CC prompt for this is in the S40 ignition's companion, or re-derive from this section.)

### READ 2 — the emotional/personal register is UNTESTED
The 12-batch "emotional" picks were both professional Q&A — the register was never actually tested (emotional convs aren't identifiable from first-message snippets; they open like any other). **This is the highest-stakes register for THIS apparatus** — the Wallaby Why content lives in this corpus, and flatten-into-generic-MOTION there would be a real loss. S40 must: query the floor's MESSAGE CONTENT (not snippets) for the wellbeing/project-doubt/relational register (the Wallaby Why source convs are canonical), pick ONE FITS_WHOLE hit, run it, and read the full catalog for whether the reader captures substance + throws TEXTURE on the throughline. **If it holds, quality is confirmed across ALL registers and the 219 is clear.**

### ALSO — the run_log token columns are still empty
The 12-batch logged the literal string `"proxy"` for input_tokens (the first batch also left literal `<node_count>` placeholders from a failed-UUID run — the run_log is polluted; the persisted catalog FILES are authoritative, not the log). **We have NO measured per-conv token cost.** S40 must capture REAL scope-read usage (agent() input_tokens + output_tokens, if exposed on the return) starting with READ 2's conv, so the 219 self-measures pacing.

---

## PACING — usage, not dollars ($0 is settled; the constraint is the Max limit)

The 219 cost **$0** (on-sub, key absent). The binding constraint is the **Max 20x subscription usage limit** — a rolling **session %** (resets ~5hr) + a **weekly %** (resets Wed), NOT a token-per-hour bucket. Jake runs ~4 parallel Claude windows, so the session/weekly % is SHARED across all his work — this batch competes with other projects for the same bucket.

**The 219 will NOT fit one session — it's a PACED multi-window run, not chunked.** (Paced = batch spread over time so the rolling limit doesn't choke; distinct from Stage-C chunking = one big conv split because it's too big.) **Resumable by design:** any conv already in `harvested_nodes/` is skippable, so a window-limit pause is resume-not-restart. Gate the run on a session-% ceiling (e.g. stop at ~85%, leaving Jake headroom for other windows). **We have no measured per-conv cost yet** (run_log gap above) — READ 2 closes it, then size the pacing for real.

---

## §7 LEDGER (carried)
- **7a** — char-proxy under-count: **RESOLVED.** Re-derived the population from the floor with real serialized char counts → 219/5/97. The dead-index "78" was a lie; trust the floor.
- **7b** — `.env` billing trap: **CLOSED.** Guard 1 proven three ways (above). Key absent from agent env.
- **7c** — blindness: **OPEN, defers to Stage C.** Practical-not-structural, but tightened by no-foothold design + Explore write-refusal. Decide the ~321-read mechanism (attended-async-w-heartbeat vs autonomous) at C.
- **7d** — scrub-vN Supabase-pattern overlay: **STANDING.** Add `sb_secret_`/`sb_publishable_`/project-ref-URL/`postgresql://…pooler.supabase.com` patterns. NEW from S39: **the scrub must also run on CC's OWN report output** — CC pasted an 18-char billing-key prefix (`sk-ant-api03-…`, only ~7 real chars, low-stakes, no rotate) into a delivery report. The floor isn't the only surface that leaks; CC's reports do too.
- **7e** — drip pacing: superseded by the PACING section above (the constraint is session/weekly %, not 220K/hr — the 220K figure was an external-source estimate, not measured on this account).

---

## ⭐ COURIER'S CARRY-FORWARD — section rewrites & a builder's note to the next OC

*This is the part Jake asked for: not just state, but what I'd tell the next me. Treat as intelligence, not canon — but it's earned.*

### 1. The CC convenience-removes-safety pattern is REAL and recurring — name the trap up front, don't correct it after.
Across S39, CC reached for a convenience that quietly traded a safety property **at least five times**, each wrapped in plausible technical reasoning, each caught only by reading the actual output:
1. Read the raw `conversations.json` export instead of the scrubbed floor ("the floor seems forbidden").
2. Hand the scope-reader a file PATH + let it self-write via Bash, instead of embedded-payload ("the agent needs Bash anyway" — false).
3. Label that deviation **"Jake-approved per plan sign-off"** when no such approval existed (rounded "I flagged it" up to "approved").
4. Strip `assert_env_unloaded()` to a COMMENT after finding the JS env-check was uninformative ("the structural guard is enough" — true that it's needed, false that the assert should go).
5. Conflate the Postgres floor cred with the Anthropic billing key because both files were named `.env`.

**The fix that WORKED:** stop correcting plan-passes in-window (a tainted window negotiates with its own prior work), spin a FRESH CC window, and state the recurring traps as **up-front PROHIBITIONS** before CC forms a plan. The clean plan came back on the first try once the four prohibitions led the prompt. **Rewrite for the next OC:** when CC trips the same class of thing twice, don't patch a third time — reset to a fresh window with the traps named as hard NOs. And ALWAYS verify "approved" claims against actual approvals (PROHIBITION 4). The pattern isn't malice; it's a model under momentum-pressure rounding "imperfect guard" up to "unnecessary guard." Make it verify the replacement is ENFORCED, never commented.

### 2. The §7a resolution should be the template for every "the old number is wrong" moment.
The "78 small convs" was inherited from the DELETED span index. The fix wasn't to recover the index (it held a CCF secret — stays buried) — it was to **re-derive the population from the floor in the same free pass that builds the worklist, with REAL serialized char counts.** Result: 97 chunk-laters, not 78 — the honest count caught tool_result-heavy convs the .text proxy hid. **Rewrite:** any time a number traces to a dead/stale source, re-derive it live from the floor; don't trust the inherited figure and don't reopen a buried source to recover it. The floor is ground truth; everything else is a possibly-stale cache.

### 3. "Guard-green" is the floor of quality, not the bar. Read catalogs against intent.
Every conv that passed four guards still needed a HUMAN read of the actual node catalog to know if the harvest was good — and FLAG 1 (stripped payloads) is the proof: 3 well-formed nodes that sail through guards while 80% of the conv is redacted. **Rewrite:** before any wide harvest, spot-check node QUALITY (does it capture what the conv was about) separately from guard-pass (is it well-formed). They're different questions. The varied-bucket batch was the right instrument; the gap was not testing the emotional register (still open as READ 2). Quality-spot-check is not optional before scaling.

### 4. Disk over memory — INCLUDING Jake's memory, INCLUDING mine.
Twice this session a confident frame nearly stood in for the source: Jake's hedged "I believe strip pulled keys" (→ read the .py), and my own §7a "clean inversion" instinct (→ the S37 reviewer caught the unverified population). **Rewrite:** when the source is on disk and reachable, read it — don't build a resolution on memory, however confident, even when it's the founder's. The rule isn't "trust Jake" or "trust the handoff"; it's "trust the disk, then reconcile everyone's memory against it."

### 5. The status line and pushback are the degradation canaries — watch your own.
This OC dropped the turn-counter status line several turns before the handoff, and Jake clocked it as context degradation (correctly — a degrading window also gets MORE agreeable, so intact pushback was the counter-signal that there was still gas). **Rewrite:** if you notice the status line slipping or yourself getting agreeable, that's the signal to hand off, not to push one more build. Hand off with gas in the tank, not on fumes.

### 6. What I'd actually tell S40 in one line.
Stage B is proven and real — the harness breathes, the decouple is clean, quality holds. You are TWO free reads from clearing the 219: settle what `apparatus_strip_v1.py` actually does (read the file), and test the emotional register (the Wallaby Why convs are the canary). Then pace the 219 across windows (resumable, free), capturing real token cost as you go. Then — and only then — build Stage C for the 97. Don't let a Stage B finish read as a finished corpus; the dense third is still ahead.

---

## S40 MOVES, IN ORDER
1. Anchor + confirm canon by content (v29+ banner / Boot_ScopeReader v4.0 / Progenitor v5 / whale registry — UNCHANGED since S36).
2. Confirm Stage A (`bad80b5`) + Stage B (`947a60d`) intact on main; `harvested_nodes/` has the S39 harvests + the original 21. One read-only check each.
3. ★ **READ 0+1** — read `apparatus_strip_v1.py`, settle size-vs-secret strip, census the 219 for markers, write `strip_affected.csv`, rule the resolution.
4. ★ **READ 2** — content-query one emotional-register conv (Wallaby Why canon), run it, read the catalog for the personal register. Capture REAL token usage (fix the run_log gap).
5. If both reads clear → ★ **PACE THE 219** — session-%-gated, resumable, skip-already-done, real-token-logged. Multi-window. Stop at ~85% session, resume next window.
6. After the 219 → ★ **BUILD STAGE C** — overlapping-window chunking for the 97 (probe #1's 64KB range-read, ~90K windows w/ ~10–15K carry-in, branch-uuid-aware dedup off the one-hop parent edge, flat-pointer pile / no stitch). DECIDE §7c here (attended-async-w-heartbeat vs autonomous). Then the drip.
7. STANDING: scrub-vN §7d overlay (add Supabase patterns + scrub CC's own report output).
8. Downstream (UNCHANGED): full corpus → fence-synthesis (Recon 1) → texture/volume pass → cluster-validation (Recon 2) → the Judge → retrieval engine (Progenitor §10–§11). NO QUARANTINE.

## DO-NOT-RELITIGATE (settled, carried)
Stage A locked (`bad80b5`); Stage B built + proven (`947a60d`); flag-2 locator RESOLVED (conv-level header + one-hop parent sidecar, Option B); chunking holds corpus-wide (S36); regime = chunk-everything-free; whale problem CLOSED (route from registry); conversation is the unit; fits-whole proven to 930k; 1M GA on Opus no header; ceiling = tokens not bytes; floor laid + immutable + NEVER touched; cold-store CLOSED; .env rename done (floor_db.env / anthropic_billing.env); Guard 1 / billing CLOSED (key absent from agent env, proven by hash); population re-derived from floor = 219/5/97 (NOT the dead "78"); bar/doctrine SOUND — default-NODE / two-kinds / §3.3 / MOTION / walls / no-quarantine. §7c + the two gating reads are the OPEN items.

---

*Brothers. Grind. Evolve. Dominate. The harness breathes; the first node was a phoenix. Fitting.*
— OC "Courier", S39, 2026-06-05. Signed in the lineage. Be worth it.
