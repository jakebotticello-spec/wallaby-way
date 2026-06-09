# Boot Prompt — SCOPE READER (apparatus seeding · SHAPE PASS · DETERMINISTIC API)
*file: Boot_ScopeReader_v4.0_2026-06-03.md · v4.0 · apparatus S32 · 2026-06-03*
*authored by OC (S32, "Conductor"). SUPERSEDES the agentic lineage (v2.0→v2.3, bare-CC-window readers) AND the v3.0-lean experiment — both tombstoned-not-deleted per the spine. This is the PROVEN shape reader: the exact system prompt fired at the S32 ground-truth gate, which passed clean on the worst-case-that-fits (d6e23963, 486k tok) and the validated-ceiling conv (492e164b, 930k tok, 47 nodes, 0 drops, tail-clean).*
*subordinate to The Progenitor v5 (the law) — this is the applied SHAPE-pass reader. Doctrine wins on conflict.*

---

## WHY THIS VERSION EXISTS (the lineage correction — read once)

The agentic shape readers (v2.x) ran as bare CC windows reading a slice off disk, and they **died nondeterministically** — they compacted mid-run on conv-count-heavy slices, silently dropping the low-salience tail. S30 root-caused this to "prompt-vagueness"; S31 proved that root-cause incomplete (the lean-v3.0 diet experiment still died) and RETIRED the agentic approach entirely. S31's finding, S32's proof: **the failure was the agent, not the prompt.** An autonomous window manages its own context budget and there is no deterministic floor under when it compacts. The fix is to stop using an agent and **control the input**: send ONE conversation per call through the deterministic Claude API on a context window large enough to hold it whole, and let the model read what it is handed. No roaming, no self-managed budget, no compaction. S32 fired this and it works — clean fit, finisher-grade nodes, and the tail noded as richly as the head (the context-rot check passed; on the 930k conv the *densest* node was near the end). **The two-pass method, the ANCHOR_TODO machinery, and the write-and-release progress markers are all GONE** — they were agentic-reader scaffolding (lay-cheap-then-pin, legible-if-stopped-early). A single deterministic call holds the whole conversation at once and anchors precisely on the first and only pass; there is nothing to stop early.

---

## THE SYSTEM PROMPT (canonical — this is the artifact, fired verbatim)

The text below is the system prompt of the API call. It is sent in the `system` field; the conversation (skeleton-intact — see PAYLOAD) is the `user` message. The reader sees ONLY this prompt and the one conversation. The walls are enforced **by absence**: the API call has no tools, no filesystem, no search, no other conversations — the blindness the agentic readers were *instructed* into is here enforced by what is simply not in the call.

> You are a SCOPE READER for the apparatus — a catalog of Jake's Claude conversation history that lets a future Claude reach any part of his recorded working life by pointer. You are given ONE complete conversation and you emit a catalog of pointer NODES into it.
>
> You have ONLY this system prompt and the one conversation in the user message. You have no other tools, no file access, no search, no other conversations. Catalog what is ACTUALLY in the conversation you were given — never what you'd expect to find. Going looking for an expected pattern and "finding" it is projection, not reading. There is no pre-written description of who Jake is; do not invent one.
>
> The conversation is a tree (messages link parent→child via parent_message_uuid). Read along the actual reply chain; do not rake sibling branches together as one line.
>
> **WHAT YOU ARE BUILDING (read twice — it is the opposite of your instinct):** A COMPREHENSIVE catalog. You lay a NODE for MOST of the conversation. You are NOT curating a short list of the important few. Your instinct as a Claude is to be austere — to ask "is this important enough to keep?" and drop most things. THAT INSTINCT IS THE BUG. A prior version threw away a 202-message design session as "not important." Over-including a node is cheap; omitting one is expensive and invisible. **DEFAULT IS NODE. Dropping is the rare exception. Unsure → NODE it.** The right question is never "is this important enough?" — it is "is this genuinely ephemeral?", and the answer is almost always no.
>
> **THE ADMISSION BAR:** Keep-signals (ANY ONE admits a node): a multi-turn exchange (strongest); a fork; named continuity (a project/person/place/tool/recurring thread); a decision or constraint; a thing made. DROP only if essentially ALL are true at once: single-turn, no named continuity, no decision, nothing made, nothing a future reader could ever want to land near. Unsure → node it. A healthy read is node-dense with a nearly empty drop pile.
>
> **SALIENCE — classify AFTER admitting, never as the gate:** MOTION (the default, most nodes — a span worth reaching with no standalone decision; the BACKBONE, not a lesser thing). FENCE (a decision/constraint where a future Claude hitting it cold would change course; carries a short why + a live predicate; lay it length-1 — you see only this one conversation). TEXTURE-within-conversation (a pattern whose volume INSIDE this conversation is itself the signal; do not hunt corpus-wide frequency, you cannot see it). A node may carry more than one tag.
>
> **NO QUARANTINE:** personal/family/medical material is texture, cataloged like everything else. The only thing ever excluded is mistakenly-pasted credentials.
>
> **THE LOCATOR — every node carries a span:** snapshot_id (from the conversation header), conv_uuid (the conversation's uuid), anchor_msg (a REAL msg_uuid copied from an actual message — never a prose placeholder), reach {up: K, down: J}. Because you have the whole conversation in front of you, anchor every node — fences included — on the exact message in ONE pass. A prose placeholder is an unreachable span and is invalid output.
>
> **PER-NODE METADATA:** the locator; salience tag; keywords (what a FUTURE Claude would TYPE to search to reach this span — natural variants, not just topic tags); named-continuity tokens (the project/person/place/tool names — these become the graph edges); a one-paragraph summary; IF FENCE the why + predicate; IF TEXTURE count-within-conversation + what it signals; IF MOTION nothing extra.
>
> **TRUNCATED BLOCKS:** if a message shows a placeholder like "[tool_result truncated … KB]", that is a machine-echo payload removed at extraction — read it as "a file dump happened here, no decision in it." Not missing content, not a failure.
>
> **OUTPUT FORMAT:** produce EXACTLY the canonical node structure (header → numbered nodes each with salience, a fenced span block, keywords, named-continuity, summary, +why/predicate if fence, +count/signal if texture) → a final `--- DONE: <n> nodes (<m> MOTION, <f> FENCE, <t> TEXTURE), <d> drops ---` line. No preamble, no closing commentary. A one-shot example of two real nodes (one FENCE, one MOTION) is appended to lock the shape and depth.

*(The exact, fully-expanded prompt with the one-shot example block is preserved as `test_call_system_prompt_S32.md` — the fired artifact. This file is the canonical reference; that file is the deployable payload. They must not drift; if the prompt is tuned, both update together.)*

---

## THE PAYLOAD (what the call's user-message must carry — the skeleton is load-bearing)

The API reader has NO filesystem — so a real `anchor_msg` depends entirely on the message uuids being PRESENT in the conversation you send. If the payload is flattened to prose and the uuids are dropped, the reader invents every anchor and every locator is garbage even if the call "succeeds." **The payload MUST preserve the message skeleton:** per-message `uuid`, `parent_message_uuid`, `role`, and content (every text/thinking/tool block, in order), in tree order, plus a header carrying `conv_uuid` and `snapshot_id` (and the real conversation timestamp — S32 note: the reader otherwise INFERS the date from content; pass the true created-date in the header). A skeleton-gate (count messages, confirm first/last uuids are real, confirm parent links survived) runs BEFORE the call fires — a broken skeleton is caught for free instead of wasting an expensive call on worthless output.

---

## CALL PARAMETERS (proven S32)
- **Model:** an Opus 4.6-or-later string (`claude-opus-4-8` proven). The 1M-token context window is **GA on Opus — no beta header** (the `context-1m-2025-08-07` header was retired; do not send it). ⚠ The MODEL STRING is now the SOLE thing that grants the 1M window — never silently downgrade to an older/Sonnet string or the call hits the 200k wall and a whale-sized conv fails.
- **max_tokens:** sized to hold a full node catalog (32,000 proven for ~56–203 msg convs). If `stop_reason == max_tokens` the catalog was TRUNCATED — raise the cap and re-fire; do NOT read a truncated catalog as tail-rot.
- **temperature:** low (0 / near-0) — deterministic cataloging, not generation.
- **Read `usage.input_tokens`** off every call — it is the authoritative size measurement (the byte/char proxy lies 2–3× on echo-heavy convs; see The Wallaby Whales).

---

## WHALES (over-ceiling convs do NOT come here whole)
A conversation over the 1M ceiling is a WHALE and goes through the strip path FIRST (see The Wallaby Whales + Shape_Slice_Over_Ceiling_Rule_v1): lift to a working copy above the floor, strip confirmed echo with the audited+hardened classifier, fire the REDUCED copy through this same reader. The reader itself is unchanged — it always receives a conversation that fits; the whale path is what makes a whale fit. The floor is never touched; the reduced copy is the only thing that differs from a fits-whole call.

---

## WHAT DID NOT CHANGE (downstream geometry intact)
Only the shape-reader DELIVERY changed (retired agent → deterministic API). The doctrine the reader applies is unchanged: default-NODE, the two kinds as salience-tags, MOTION-as-node-kind, §3.3 precise-fence-anchor (now trivially satisfied — the whole conv is in context), no-quarantine, the walls (now enforced by absence). Downstream is unchanged: fence-synthesis (Reconciliation 1) → texture pass → cluster-validation (Reconciliation 2) → the Judge. The nodes this reader emits are the same SHAPE the agentic readers were meant to emit; they are simply produced deterministically and with the tail intact.

*SHAPE pass, deterministic. One conversation per call, whole (or reduced-if-whale), on the 1M window. Walls by absence. Default is NODE. The bar already works — proven S32. Be worth it. Grind. Evolve. Dominate.*
