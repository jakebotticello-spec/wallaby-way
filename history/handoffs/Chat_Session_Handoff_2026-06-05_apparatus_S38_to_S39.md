# apparatus — S38 → S39 Handoff
*authored by OC "Conduit" (S38), 2026-06-05 · the load-bearing state transfer · more current than any boot doc; if this conflicts with the ANCHOR banner, THIS wins (newer)*

---

## ⚠️ READ FIRST — WHAT THIS SESSION WAS

S38 was an **execution session** — it built **Stage A** of the on-sub chunked pipeline (move #3), the staged build S37 laid out. NO architecture changed, NO ruling was made, NO invariant moved, NO floor was touched. v27's chunking-holds-corpus-wide ruling and v28's cold-store close both stand fully in force; v29 is a progress banner over them.

Stage A = **the loop's foundation**: a chunk-ready extractor + the four guards the loop calls, built as **pure local plumbing** (no Agent calls, no API calls, no `.env` load), unit-proven (13/13 green), run through the `/code-review` gate (2 real findings fixed, re-reviewed clean), and **merged to main** (`bad80b5`). **Stage A is DONE + LOCKED.** The build is staged A/B/C — **only A is complete.** Stage B (wire the loop, run the 78 small convs whole) is the next sitting.

The one design fork S38 closed: **flag-2's locator**, ratified by Curator (S37) mid-session — recorded below and in the v29 banner. It's the build's implementation of an already-known flag, not a new ruling.

---

## STATE IN ONE PARAGRAPH

Substrate closed + immortal (floor S23: 325/24,138, append-only enforced, ndjson canonical / Postgres rebuildable). Whales closed (S33: 4 read, 130 nodes, route from `pipeline/whales/whale_registry.md`, NEVER re-read). Shape reader proven on API + on-sub, deterministic, UNCHANGED since S32 (`Boot_ScopeReader_v4.0`; deployable `pipeline/test_call_system_prompt_S32.md`). Chunking holds corpus-wide — SETTLED (S36, two big-conv confirmations, regime = chunk-everything-free). Cold-store CLOSED (S37: `harvested_nodes/`, 21 done rows / 0 stubs, MANIFEST present — both the locked record of what's done AND the structure the drip writes into). **AND AS OF S38: Stage A of the pipeline is built + locked on main** — `extract_whale.py` v2.0 (chunk-ready), `pipeline_guards.py` v0.2 (four guards), `test_guards_S38.py` (13 green). THERE ARE NO OPEN ARCHITECTURE QUESTIONS — everything from here is EXECUTION; the BUILD (Stages B + C) is the only thing between here and a fully harvested corpus.

---

## WHERE STAGE A LANDED (built · reviewed · locked on main)

Merge commit **`bad80b5`** = feat **`88e7029`** + review-fix **`d408a3d`**. All on `main`. Three artifacts + a gitignore line:

- **`pipeline/extract_whale.py` v0.1(S33) → v2.0(S38)** — two surgical changes, `render_block` UNTOUCHED (canary-proven):
  - **(1) header values are CALLER-SUPPLIED.** Optional `--conv-uuid` / `--snapshot-id` / `--created` args override the window-derived values, so a mid-tree chunk window carries the TRUE conv identity in its header BEFORE the read (the flag-2 fix — closes the exact bug that mis-keyed the ea900330 chunks at S36/S37). Absent → falls back to today's derived behavior, so whole-conv extracts run byte-identical.
  - **(2) `{msg_uuid: parent}` sidecar.** Builds the parent map over the whole conv and writes `<out>.parents.json` (NOT sent to the reader) — the source map for the persist-time one-hop parent-edge injection. Proven on a real whale JSON: 303 parents / 303 msgs, root = string `"null"`.
- **`pipeline/pipeline_guards.py` v0.2 (NEW)** — a LIBRARY the loop calls (not a runner; no Agent/API/`.env`):
  - **Guard 1 — `assert_env_unloaded()`** — raises if `ANTHROPIC_API_KEY` ∈ `os.environ` (§7b billing trap; checks the ENVIRONMENT, never reads `.env`).
  - **Guard 2 — `whale_gate(conv_uuid, input_tokens, registry_uuids, ceiling=1M)`** → `KNOWN_WHALE` (route from registry, never re-read) / `FITS` / raises on a new over-ceiling conv (detect-and-alert, never auto-strip). Companion `load_whale_registry(path)` parses the 4 uuids defensively, called at startup, NOT inside the pure gate.
  - **Guard 3 — `tally_nodes(node_file_text)`** — counts by regex-anchoring the literal `**Salience:** <TAG>` line, NOT a keyword grep (flag-1 fix; "fence" in a `**Keywords:**` line can't inflate FENCE).
  - **Guard 4 — `persist_node_file(dest_path, node_text, parents_map)`** — **temp-then-rename ATOMIC write** (the v0.2 review fix): writes to `<dest>.tmp`, validates on the temp (size>0 + `--- DONE:` present + tally>0 = stub guard; **every anchor_msg ∈ parents_map = the flag-2 integrity tripwire**), `os.replace` on success, **unlinks temp + re-raises on ANY failure** so no partial/stub artifact survives a HALT. Writes the **Option-B `.parents.json` edge sidecar** (edges keyed by anchor_msg; root anchors = JSON `null`, NOT omitted) ONLY after the successful rename.
- **`pipeline/test_guards_S38.py` (NEW)** — 13 tests, all green. Covers all four guards incl. the v0.2 no-file-survives-a-failed-persist assertions.
- **`.gitignore`** — added `pipeline/*.parents.json` (sidecars derived, not tracked).

---

## FLAG-2 LOCATOR — RESOLVED (the one design fork; ratified by Curator S37 mid-session)

The S37-proven flag-2 ("the extractor must stamp real `conv_uuid` + `snapshot_id` into every window header") needed its **dedup half** made operational. The resolution:

- **Header carries CONV-LEVEL identity only:** `conv_uuid` + `snapshot_id` + `timestamp`. **NO branch field.** Branch position is a *derivable* relationship (anchor_msg ↔ parent chain); caching it in the locator would be the same double-encode the FK-drop killed. A locator that carries derived data goes stale the moment the derivation and the cache disagree.
- **The dedup-fold GUARANTEE comes from a one-hop parent edge per node** — `anchor_msg` + its *immediate* `parent_message_uuid` (one hop, not the whole chain). A subpath/branch anchor (like the S36 `019e1720…` case) is a subpath of a single host message; folding it needs the host, which is one parent-link away. This is the difference between "dedup folds off the parent chain" as a hope and as a guarantee: if the node carries the one-hop parent, dedup folds in-pile with NO floor round-trip; if it doesn't, dedup silently becomes a floor-reader and the "no stitch" promise erodes.
- **Verified against real reader output** (not doctrine): `Boot_ScopeReader_v4.0` emits ONLY `anchor_msg` in its 4-field locator span (`snapshot_id` / `conv_uuid` / `anchor_msg` / `reach`) — NOT the parent. So the **extractor INJECTS the edge at persist time** (it holds the whole skeleton, it knows each msg's parent).
- **Shape locked to Option B (sidecar):** the edge lives in a `<nodefile>.parents.json` BESIDE the node file, leaving the proven v4.0 span block **byte-untouched**. Node file is write-once (matching the cold-store's locked-once-written property); dedup reads two files at pile-time (trivial — same dir, batch op, not a hot path). Curator's words: yes to conv-level-only, plus the one-hop-parent precision that makes the dedup half a guarantee instead of an assumption.

**Net for the build:** the extractor sidecar (`extract_whale.py` v2.0) carries `{msg_uuid: parent}` for the whole conv; `persist_node_file` reads it, asserts every emitted anchor is in it (the integrity tripwire), and writes the per-node edge sidecar. The flag-2 corruption ("shatter one conv into N phantoms") is now caught at TWO points: the header-stamp prevents it, and the anchor-∈-parents_map assertion HALTS on it if it ever slips through.

---

## §7 — DOWNSTREAM FLAGS (carried; two still OPEN, resolved in B and C)

### 7a — The char-proxy under-counts authoritative tokens by ~1.4× — **OPEN, resolve at the START of Stage B**
The `char/3.5` proxy under-counts authoritative on-sub tokens (proven twice: 467K→657K, 403K→539K). The "78 sub-25K convs run whole first" set is **sized on the lying proxy** — a conv estimated "24K, read whole" may really be ~34K. **GATE: re-measure the tier-1 boundary set against AUTHORITATIVE on-sub tokens (key unloaded) before the whole-read batch.** Some of the "78" may cross into needing a chunk.

### 7b — The `.env` billing trap is the single highest-consequence guard — **baked into Guard 1, wire it before every Agent call**
Loading `pipeline/secrets/.env` silently forces METERED billing (the ~$50 trap). On-sub reads MUST NOT load it. `assert_env_unloaded()` exists and is unit-proven; **the loop must CALL it before every Agent call, and HALT if it can't confirm unloaded.** Building the guard ≠ wiring it — Stage B wires it.

### 7c — The blindness question — **STILL OPEN, DECIDE AT STAGE C; do NOT default to "practical is fine"**
On-sub Agent calls grant `Tools: *` to every sub-agent and you can't strip it — the reader has a live `Read` tool and a reachable working dir. S36's 5 watched reads held by *practical* blindness (no paths in the payload + the reader told not to look). **~321 UNWATCHED reads is a different risk class.** Curator left this open on purpose. The honest framing (from S38): the agents do the reading, the drip runs at background-tempo, but "fully hands-off unattended" is exactly this open call — lean attended-async (a heartbeat someone glances at, guards HALT-and-alert) over autonomous-black-box, but DECIDE it deliberately at the chunking step, weighing practical-blindness vs true tool-absence.

### 7d — scrub-vN credential gap — **STANDING BUILD-LIST ITEM, not done**
The scrubber's v1 5-class pattern set PREDATES Supabase's `sb_secret_` / `sb_publishable_` format — the S37 CCF key passed UNRECOGNIZED (Supabase auto-revoked it; dead value; `pipeline/recon/` swept). **FIX: add `sb_secret_` / `sb_publishable_` / project-ref-URL patterns to the next scrub-vN overlay** (the S19/S20 tighten-only overlay machinery exists for exactly this). LATENT: the value still lives in the immutable floor by design until this runs. Not move-ordered — fold it in when convenient.

### 7e — Window pacing (~220K/5-hr) is a third-party estimate — re-measure if rate-limited at Stage C.

### 7f — Probe/scratch dirs accumulate. `pipeline/probe_bigconv/` + `probe_bigconv2/` hold the S36 raw originals (retained, referenced by the cold-store provenance blocks — do NOT delete). New scratch from Stage B/C: sweep when dead, the way `recon/` was.

---

## §8 — JUDGMENT-CALL LEDGER (S38 · the call · reasoning · confidence)

- **Flag-2 = conv-level header + one-hop parent sidecar (Option B).** Header carries identity, not derived branch data; the one-hop edge makes dedup-fold a guarantee; sidecar keeps the v4.0 span byte-untouched. · HIGH (ratified by Curator S37; verified against real reader output, not doctrine).
- **Bake flag-2 into Stage A's extractor (not deferred to C).** The handoff said "Stage A WITH the flag-2 fix"; the parent edge is needed for dedup regardless of chunking; building it in means Stage A's pipeline IS the real pipeline. · HIGH.
- **Added an anchor-∈-parents_map assertion to persist** (beyond the spec). Turns persist into a flag-2 tripwire at the cheapest possible check (dict membership) — would've caught the ea900330 mis-key live at S36. · HIGH.
- **B2 fix = temp-then-rename atomic persist** (vs delete-in-handler). Atomic write matches the floor's single-transaction stance: a node lands whole-and-validated or not at all; nothing partial ever sits at dest_path. · HIGH (the review found the hole; the fix is the stronger architecture).
- **Fresh CC session for the build** (not S37's continued window). A 15-turn build wants clean faculties; disk + repo pull the same from any window; no reason to inherit S37's context-rent. · MEDIUM-HIGH.
- **No Progenitor edit this session.** §12/§13 carry-forwards stay DEFERRED to post-build (Stage A built ≠ pipeline confirmed end-to-end; that's Stage B). Authoring ahead is the documented over-eager failure. · HIGH.
- **Two process scars → canon, not just handoff** (JAKE-RULES §12 merge-order; JAKE-STACK CC-scatter). The merge-order one is a genuine universal git rule earned the hard way. · MEDIUM (Jake's call, landed).

---

## YOUR FIRST MOVES, S39 — IN ORDER

1. **Anchor + confirm canon by content** (v29 banner / `Boot_ScopeReader_v4.0` / Progenitor v5 / whale registry all-4-RESOLVED — all UNCHANGED since S36; do NOT expect edits). FRESHNESS TRIPWIRE: if the ANCHOR footer's newest entry predates v29/S38, the copy is CDN-stale — re-pull via codeload or ask Jake to paste.
2. **Confirm Stage A on main** — `bad80b5` present; `extract_whale.py` v2.0 + `pipeline_guards.py` v0.2 + `test_guards_S38.py` on disk; one read-only check that the 13 tests still pass (`python pipeline/test_guards_S38.py`). Do NOT rebuild — it's locked.
3. **Confirm move #2 cold-store intact** — `harvested_nodes/`: 21 done rows, 0 stubs, MANIFEST present. One read-only check.
4. **★ STAGE B — wire the loop body + run the 78 sub-25K convs WHOLE first.** The loop wires the Stage-A pieces: extractor → on-sub Agent read (the `Boot_ScopeReader_v4.0` embedded-payload method — read both files into CC context, pass as raw call text, NO paths) → the four guards → `persist_node_file` to `harvested_nodes/`. Guard 1 fires before every Agent call (HALT if `.env` key loaded). Guard 2 routes the 4 whales from the registry + detect-and-alerts on any new over-ceiling. **§7a GATE FIRST:** re-measure the tier-1 boundary set against AUTHORITATIVE on-sub tokens (key unloaded) — confirm which actually fit a whole-read before the batch. Running the 78 whole (no chunking) proves the loop end-to-end for **$0** before windowing complexity. KEEP CC PROMPTS PROPORTIONATE — gated, one stage at a time, plan-mode for the build steps.
5. **★ STAGE C — add overlapping-window chunking** (probe #1's 64KB range-read, ~90K windows w/ ~10–15K verbatim carry-in, branch-uuid-aware dedup folding off the one-hop parent edge, flat-pointer pile / no stitch). **DECIDE §7c HERE** (the unwatched-run blindness call — don't default). Then the drip, paced ~220K/5-hr (§7e, re-measure if rate-limited).
6. **AUTHOR THE PROGENITOR §12/§13 BODY CARRY-FORWARDS** on the CONFIRMED pipeline (NOT before — authoring ahead is the documented over-eager failure; also fix the dangling `Boot_ScopeReader.md` ref → `Boot_ScopeReader_v4.0`).
7. **★ WHOLE-CORPUS COMPARISON PASS** (Jake's S36 add) — every non-whale conv chunked + a whole-read SAMPLE on API as the final at-scale faithfulness diff (the two S36 confirmations already in the sample). NOT all 321 whole. GATE the sampled paid calls.
8. **FULL CORPUS** → fence-synthesis (Reconciliation 1) on harvested nodes (130 whale + ~321 fits-whole) → texture/volume pass (own `_extract_texture_slice.py`, wide-lean slices; whales NOT special; ratify `Boot_VolumeReader` v0.1 against the first texture canary) → cluster-validation (Reconciliation 2 — load-bearing, never a skim) → the Judge → wire the retrieval engine (Progenitor §10–§11). NO QUARANTINE; downstream geometry UNCHANGED.

**STANDING BUILD-LIST ITEM (not move-ordered):** scrub-vN Supabase-pattern overlay (§7d).

---

## WHERE THINGS LIVE (quick ref — full list in ANCHOR → WHERE THE CODE LIVES)

- **the floor** → Supabase (D9), append-only enforced, `floor_immutable_guard()` proven. ndjson canonical.
- **the shape reader** → `pipeline/test_call_system_prompt_S32.md` (= `Boot_ScopeReader_v4.0`, fired verbatim, don't drift). **API harness** → `pipeline/apparatus_api_testcall.py` (the ONLY thing that loads the key — paid path only).
- **the chunk-ready extractor** → `pipeline/extract_whale.py` **v2.0** (caller-supplied conv-identity header + `.parents.json` sidecar; render_block untouched).
- **the four guards** → `pipeline/pipeline_guards.py` **v0.2** (billing / whale-gate / salience-tally / atomic verify-on-write persist). Tests → `pipeline/test_guards_S38.py`.
- **the cold-store** → `harvested_nodes/` (21 done rows, MANIFEST.md; locked record + drip target; NEVER re-read its contents).
- **the whale registry** → `pipeline/whales/whale_registry.md` (4 RESOLVED; route, never re-read).
- **the S36 confirmation raws** → `pipeline/probe_bigconv/` + `probe_bigconv2/` (retained, referenced by cold-store provenance — don't delete).
- **the billing trap** → `pipeline/secrets/.env` (NEVER load on an on-sub read).

---

## WORKING-MODE REMINDERS FOR THIS PICKUP

- **OC plans/architects/authors in chat; CC reads disk, runs commands, commits; Jake bridges AND is the only one who pushes/merges.** Jake pastes CC/API output RAW. Never ask Jake for implementation/technical state. Never claim to have saved/committed/pushed. No `ask_user_input` widget — prose only (tell CC too).
- **Full code blocks** (no diffs except one-liners); **no `&&` chaining**; numbered deploy steps ending in Verify. CC prompts in a single code block. **KEEP PROMPTS PROPORTIONATE** — don't scaffold a simple ask into a monster (the over-engineering twin of the austere reflex).
- **GATE all paid spend** (Stage C's comparison-pass SAMPLE + any tier-1 boundary whole-reads; everything else is on-sub-free). **The §7b billing guard is load-bearing** — confirm `.env` unloaded before any Agent call, HALT if you can't.
- **CAUTIOUS EXPEDITIOUSNESS:** Jake's borrowing these hours from other project time. Gate where a wrong move corrupts the locked pile or bills money; move fast where it doesn't. Don't be precious. **Don't let the step-count read as complexity — the architecture is SETTLED; this is assembly.**
- **NEW canon this pickup** (already pushed if Jake landed the S38 ref changes): **JAKE-RULES §12 merge-confirm-THEN-delete** (the `git branch -d` "merged to origin/<X>" warning ≠ merged-to-main; deleting a scratch branch pre-merge auto-closes the PR — confirm the merge commit on main by eyeball before deleting). **JAKE-STACK §1 CC-artifact-scatter note** (outputs → working dir / plans → `~/.claude` / reviews → GitHub PR comment).
- **rule-4 "do-not-relitigate" is SUSPENDED this stretch** — if something feels off, SURFACE it. But don't reopen settled calls without a NEW reason.

---

## THE FRAME (don't lose it under the build)

This is **Jake's auxiliary brain, beta 1.0 — the breadth IS the function.** Every hard question is answered; there is NO design work left, only execution; the BUILD (Stages B + C) is the only thing between here and a harvested corpus. The austere reflex (cutting breadth to feel rigorous) AND its twin (over-engineering a simple ask into a monster) are the documented bugs of this lineage — S38 caught itself wall-building a settled flag-2 into a four-part interrogation; the drag back to "this is assembly, move" is the work. Build the loop with the three flags baked in (they ARE baked in now — conv_uuid header-stamp, salience-line tally, deterministic atomic persist), run the 78 small ones whole to prove it, then chunk the rest free, diff a sample, synthesize. Don't let cost-anxiety stampede toward "just pay" — the drip is free, the floor immutable, the job non-urgent.

Read **The Wallaby Why** + **The Track Meet Doctrine** + **The Wallaby Whales** before working — they're FRAMEWORK, not reference. The names aren't accidental. Quiet reads as broken to a guy who ran on the lash; it isn't. Check actual data before agreeing he's behind. Cypher is the buffer working, not a crutch.

*Brothers. Grind. Evolve. Dominate. You're closer than the legs are reporting.*

— OC "Conduit," S38, 2026-06-05. Signed in the lineage. Be worth it.
