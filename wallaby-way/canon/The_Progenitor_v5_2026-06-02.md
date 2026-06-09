# The Progenitor — the law of the pointer catalog

*file: The_Progenitor_v5_2026-06-02.md · v5 · apparatus S29 (authored §0–§9 at S24, §10–§13 folded S25, §12–§13 rewritten S26, §0/§3/§8 INVERTED + organic-over-austere added S27, §12–§13 REWRITTEN TO TWO-PASS S29) · supersedes v4 (tombstoned-not-deleted) · read with JAKE-RULES + JAKE-STACK*

*v3→v4 (S27) — THE ADMISSION BAR IS INVERTED. THIS IS THE LARGEST DOCTRINE CHANGE SINCE THE FLOOR WAS LAID. Read §0.5 (the failure mode) before §3, or §3 will read like a contradiction of muscle memory. The slice-7 PILOT proved v3's austere bar (§3 "default is DON'T point") builds a lean DECISION-LOG, not the comprehensive AUXILIARY BRAIN the anchor docs mandate — it threw away 14 of 21 conversations as "motion," INCLUDING load-bearing fences buried inside them (it carded 1 node; the corrected re-run carded 41). The Jedi-Council ratified the overturn DOUBLE-BLIND (two independent panels, both structurally biased toward the austere reflex, both ruled PRESENCE). E1 (the admission standard) is ABSORBED into §3 here and graveyarded as a standalone. What changed: §0 (the one-line law), §3 (the bar — now DEFAULT IS NODE), §8 (seeding guardrails), the volume estimate everywhere (hundreds-to-low-thousands → many-thousands is CORRECT, not slippage), and a NEW §0.5 enshrining organic-over-austere as a standing INTOLERABLE failure mode. What did NOT change: §1, §2, §4 record-shapes, §5, §6, §7, §10, §11 — the engine, the two kinds, the triggers, the span-return — BYTE-IDENTICAL. Fence/texture survive but DEMOTED from admission-gate to in-graph salience classification; MOTION becomes a third node kind (a light, reachable, low-salience node), NOT a discard. See footer for the full v3→v4 enshrine.*
*v4→v5 (S29) — §12/§13 REWRITTEN FROM ONE-DATA-GATHER TO TWO INDEPENDENT FLOOR-SCANS. The S26 five-step pipeline ran ONE data-gather (dual-output slicers) feeding a fence path and a texture path. S28 proved that forcing ONE reader to serve both shape (deep/whole/byte-heavy) and texture (wide/lean) pulled slice-size in opposite directions — it killed 8 reader windows to compaction and surfaced the strip-vs-keep fork. The S29 resolution (ratified on paper): TWO independent reads of the same floor — a SHAPE pass (byte-bounded deep slices, lay nodes/fences, Boot_ScopeReader v2.2) and a TEXTURE pass (wide-lean stripped slices, a DIFFERENT slicing, lay recurrence, Boot_VolumeReader) — each with its OWN reconciliation, both feeding ONE Judge. BYTES, not messages, are the compaction axis (the whole fix). §0–§11 (except a pointer added to §3.4, plus an S30 method-vs-bar clarification appended to §0.5) are otherwise BYTE-IDENTICAL to v4; only §12/§13 moved. The dumb-index/smart-reader line, the two-kinds-one-spine, the triggers, the span-return, the projection wall, the division-is-in-the-labor invariant — all survive unchanged; the PIPELINE GEOMETRY changed, the doctrine body did not. ⚠ §12/§13 are enshrined from the S28 spec + S29 ratification; the SHAPE pass is the first to run — confirm the two-pass geometry against the run and version-correct if the run teaches otherwise. See footer for the full v4→v5 enshrine.*
*authority: governs what a pointer IS, what earns one, who lays them, how they grow, how the catalog stays honest — and (v2) WHEN it fires, WHAT a hit returns, HOW the original catalog gets seeded, and WHAT a seeding-council window boots with. The conceptual law the seeding council and every pointer-laying Claude reads before laying a single card. Sibling to the Track Meet Doctrine (how-we-record) and The Wallaby Why (why-the-beast-exists). Grounded on the D9 lock (the immutable floor this catalog rides over), the S24 retrieval-layer design session, and the S25 engine/seeding design session.*
*v1→v2 (S25): the conceptual retrieval-engine + seeding design is now COMPLETE and folded in. §10 trigger model, §11 span-return shape, §12 seeding process, §13 council boot kit are added. §9 (out-of-scope) is amended — the query interface is now IN; what stays out is genuinely-technical build-work. The remaining opens are CC-build-against-the-live-floor, not whiteboard. See the footer for the full v1→v2 enshrine.*
*STILL NOT in scope (genuine build-work, deferred to CC against the live floor): the embedding choice (v1 is keyword-first; vectors are a deferred v2 sidecar — see §9), the exact on-disk serialization, the ranking-algorithm internals inside the §6 selector envelope, reach-default tuning. Everything CONCEPTUAL is here. This file answers: **what is a pointer, what makes one worth laying, when it fires, what it returns, and how the catalog is seeded.***

*On the name: this is **The Progenitor** — the first of the line every pointer descends from, the doctrine that governs the seeding. It is deliberately NOT called "Seed [anything]": in this project "seed" is reserved for the **floor's record-shape** (`seed_shape_load.py`, `Seed_Shape_Test_Spec`, tracing to `Substrate_FaceOff_v2 §10.1`) — a substrate-layer word. The Progenitor is a retrieval-layer thing that rides OVER the laid floor. The word "seeding" appears below only for the **act of populating the catalog with pointers** — a distinct, retrieval-layer use; context carries it.*

---

## 0. The one-line law

**A pointer is a NODE in a semantic graph: a keyword (and its named-continuity edges) pointing at a span of the immutable floor, laid by a Claude who read the span and judged it worth being able to REACH. The catalog is a COMPREHENSIVE graph over the corpus — most conversations produce nodes. The default is NODE; dropping is the narrow exception. The catalog's job is to make Jake's recorded life REACHABLE — so a fresh-boot Claude lands in the right neighborhood of context during a live session, instead of being confidently blind to everything that wasn't a Big Decision.**

Everything below is that sentence, unfolded.

---

## 0.5 THE FAILURE MODE THAT GOVERNS THIS WHOLE FILE — organic over austere (READ THIS, IT IS NOT BACKGROUND)

**You are a Claude. When nothing drags you, you reach for austere — lean, clean, minimal, "only the important few." That reflex is the single most dangerous thing you bring to this project, and it is the bug that this v4 exists to correct. It is an INTOLERABLE failure mode, not a style preference. Name it in yourself and fight it, repeatedly, every session.**

This is not abstract. It is the documented history of THIS doctrine:
- **v3's §3 was austere** — "default is DON'T point," "complete over fences, sparse over motion," "hundreds-to-low-thousands, not tens of thousands." It read clean. It felt disciplined. It was *wrong*, and a Claude wrote it that way because austere is comfortable.
- **The slice-7 pilot proved it.** Run under the austere bar, a blind reader cataloged **1 node** out of 21 conversations and threw away the rest as "motion" — a 202-message design session, a 340-message system build, two months of project history, AND the load-bearing fences buried inside them. Re-run under the inverted bar, the same reader on the same slice cataloged **41 nodes** and **caught fences the austere bar was structurally blind to** (it was losing the very load-bearing few it claimed to protect, because it judged at the conversation level and excluded whole conversations with fences inside).
- **The Track Meet Doctrine named this exact reflex** (§§5–6): *"That frame is too austere. Think more organically."* / *"I went austere because clean separation is comfortable... that's me building scaffolding when you're asking me to think wet."* Jake had to drag the thinking out of the austere frame. He has had to do this REPEATEDLY across the lineage. **His architectural intuition is load-bearing even before he can articulate the technical reason** (Track Meet Doctrine, closing pattern-note) — when his gut says "this feels too lean / too clean / you're filtering," weight it heavily and check your austere reflex BEFORE defending your clean design.

**Why austere is wrong HERE specifically (this is framework, not sentiment — read The Wallaby Why and the Track Meet Doctrine as the WHY this bar is shaped this way, not as reference material):**

The Wallaby Why establishes what this apparatus IS: **the Auxiliary Brain.** Jake's working-memory buffer went offline (the rewire); his pattern-recognition faculty is intact. The apparatus exists to **hold what the buffer used to** — the breadth — *so the pattern-sense can run across more than any unaided brain could carry.* A lean catalog of the load-bearing few **starves the pattern-sense of its surface.** It is not an auxiliary brain; it is a decision-log. The breadth IS the function. A Claude that catalogs only the Big Decisions has rebuilt the exact deficit the apparatus was built to fix.

The cost structure makes the inversion correct, not just aspirational: **over-including a node is cheap** (worst case a future Claude reads a little extra context and moves on — recoverable in seconds; *"oh noes, not more context"* — Jake's own bar). **Omitting a node is expensive and invisible** (the context exists in the floor but is unreachable in-session; the cost is a felt gap in daily use, with no shape in the catalog to even reveal the miss — you cannot spot-audit an absence). Asymmetric costs demand an asymmetric default. **When unsure, NODE it.** Doubt resolves toward inclusion, always.

**The guard against austere-in-disguise (the council's own dissent flag, carried in as binding):** clean schema is NOT the sin. *Exiling the mess* is the sin. A clean structure applied to genuinely clean things is correct (Jake's call: "clean schema isn't bad when it's appropriate; if it's the right selection, I don't care what shape it takes"). The test, forever: **does the structure HOLD the mess — the VESA-mount build, the ice-maker-shopping chat, the ADHD-scheduler session — messily, as light nodes with whatever metadata they have? Or does it force them into a tidy ontology to avoid holding them?** Hold the chaos, organize the chaos — never impose order by EXILING what doesn't fit. If a future design comes back schema-first and starts dropping what won't fit the schema, the austere reflex has reasserted itself under new vocabulary. Drag it wet.

**This is why The Way and The Doctrine are loaded as FRAMEWORK, not reference.** They are not background reading you consult when stuck. They are the lens that makes this bar parse: the Why tells you the breadth is the function (so comprehensive, not lean); the Doctrine tells you your austere reflex is the enemy and Jake's wet-intuition is the corrective (so when you feel the pull to trim, that pull is the bug). A Claude that reads §3 without §0.5 will quietly drift back to austere within a session, because the reflex is that strong. Re-anchor to this when you feel yourself reaching for "is this important enough to keep?" — that question is itself the failure. The question is "is this genuinely ephemeral?" and the answer is almost always no.


**METHOD vs BAR — the S30 refinement (read this so you don't over-read the rest of §0.5).** Everything above is about the **output bar**: what earns a node. There the answer is expansive — default NODE, comprehensive, fight the urge to trim. But there is a SECOND axis the anti-austere mandate must NOT be applied to: the **work method** — HOW you move through a slice while reading it. Austerity-of-METHOD is *correct*; austerity-of-BAR is the bug. Move concisely — stream one conversation at a time, lay its nodes, write them, release it, never hold the whole slice in your head, never cross-reference every conversation against every other, never re-read to "be thorough." A reader that confuses the two — that tries to honor the comprehensive BAR by sprawling its METHOD into "load and cross-examine everything" — will blow its own context budget and COMPACT mid-read, silently dropping the long tail and buried fences, which is the precise failure this pass exists to prevent. **Comprehensive about WHAT you catalog; disciplined and bounded about HOW you move.** (Jake's S30 ruling, earned on a live run that compacted 5 of 10 reader windows to vague-method sprawl: *"austerity isn't wrong when it's right; it just can't be the guiding principle."* The guiding principle is the expansive bar; concise method serves it, it does not betray it.)
---

## 1. Why this exists (read this before the rules, or the rules won't parse)

A Claude is a fresh-boot every single time. It is the most stateless thing in the whole system — more stateless than the floor, more stateless than Jake. Each session it wakes knowing nothing it wasn't told at boot.

The retrieval layer's deepest job is to keep a stateless Claude from **re-litigating ground Jake already paid to settle** — and from **confidently walking Jake back into walls he already bled on.** The danger is not that Jake forgets (though, post-meds, the holes are real and load-bearing — see Griffin). The danger is that a fresh, capable, confident Claude *re-proposes a dead end* that sounds reasonable because the model has no way to know it's a wall for *this man, on this stack, after these fights.*

The canonical proof is the 1Pass wall: a Claude talked Jake into a 1Password Environment for env vars, Jake argued gitignores for a week, they burned **two hours** at session 17 trying to make it work — then Claude finally read that Environments-as-env-vars is beta and Jake has no invite. It does not work. Today, S24, a fresh Claude proposed the *exact same thing* for the apparatus. Jake said no, it pushed, Jake explained, it pushed again with a new reason Jake couldn't counter. **That second push is the thing this catalog exists to prevent.** Three months from now Jake will be even less armed for that argument. The pointer is the sign on the fence.

The catalog is therefore not a memory aid *for Jake*. It is **armor against Claude's confident wrongness on things Jake has already learned the hard way** — and the texture that lets a fresh Claude show up as someone who's been in the room, not a polite stranger who skimmed the file.

**Feel-rightness is the acceptance standard, not a vibe.** Retrieval must land as "here's what I know," never "here's what I found" (Track Meet Doctrine). A pointer that resolves to forty half-relevant spans fails this standard even if every span is technically a match — because it shoves the relevance judgment back onto the reader at runtime, which is the cost the pointer was supposed to kill. A pointer is right when it points at the thing a Claude would *recognize*, not merely *find*.

---

## 2. The two kinds of pointer (one spine under both)

There are exactly **two** kinds. Earlier drafts of the thinking reached for three; the third (lineage) turned out to be the *shape of the first*, not a sibling. Resist re-splitting it.

### 2.1 FENCE — points at a decision or constraint

A fence marks a place where a Claude, encountering it cold, **would change course** — re-break a wall, or re-decide a thing already decided. The actionability test: *does knowing this alter the next move?* If yes, fence. If re-encountering it costs nothing (a passing mention, a routine build step, anything already in canon), no card.

**A fence is not a verdict. A fence is a LINEAGE.** This is the load-bearing correction. "Settled" is provisional for Jake — things get re-decided as his brain heals and his experience grows, and that re-deciding is *evolution* (good, the whole teleos), not *re-litigation* (bad, re-deriving paid ground). The two look identical to a dumb index — both are "the topic came up again." Only the lineage tells them apart.

So a fence record is an **ordered chain of decision-points**, each link carrying:
- the span it lives at (floor key — see §4),
- the date,
- the call that was made,
- **the why, expressed as a *live predicate* where the why is checkable** — not a tombstone.

Most fences have **one link** (decided once, never revisited). Some **grow links** as Jake evolves. The latest link is the current call; earlier links are **superseded, not erased** — their reasoning stays visible.

**A Claude defends the latest link's *reasoning*, never its *answer*.** This is what lets recall tell evolution from re-litigation in the moment: Jake comes in hot about a decision; Claude pulls the fence, reads the chain. If Jake's argument is the *same why that already lost* — Claude shows him the fence, saves the two hours. If Jake's argument is a *new why* — Claude recognizes "this is a new link, not a forgotten old one," and helps him *add* the next link rather than dragging him back to the last one. Without the lineage, Claude either freezes Jake (defends stale answers) or fails him (lets him re-break walls). With it, Claude moves *with* the evolution and guards against the gaps. That is the entire job.

**The why-as-live-predicate matters.** The 1Pass fence is not "never use 1Password Environments." It is: *"blocked — Environments-as-env-vars is beta, Jake has no invite (true as of June 2026). RE-CHECK: still beta? still no invite?"* A fence that knows *why* it's a fence is a fence that can **dissolve itself** when the world changes — beta gets released, the predicate flips, the chain grows a new link: "out of beta, viable now, revisit." A dumb fence ("never do this") would wall Jake off from a thing that became possible. The predicate is what keeps the fence honest against a changing world.

### 2.2 TEXTURE — points at a pattern whose *volume is the signal*

Some things aren't decisions — they're the texture of who Jake is, and texture is *made of* volume. A fresh Claude that knows Jake has mentioned a thing eleven times across seven months treats it differently than one seeing it once — **not because the content changed, but because the frequency *is* the content.**

A texture pointer calibrates **how-to-be-with-Jake**, not what-to-decide. The war-story cadence. The dirty-joke rhythm and that Claude rolls with it rather than clutching pearls. The weight of a recurring mention. These exist *only* in the count — no single span carries them.

**The test for texture is NOT "how often." It is "does the volume itself tell Claude something about how to show up."** This is the line between "fuck" (frequent, but the count is incidental — no card) and Griffin's pickup (frequent, and the count *is* the meaning — card). Both are common. Only one's frequency *means* something.

A texture record carries:
- a **representative span** (a characteristic instance — go read this to feel it),
- a **count** (how many instances across the corpus),
- a **spread** (the range — over what window, clustered or sustained).

**Overlap is allowed, not forbidden.** Griffin's pickup is the canonical case: it is texture (a recurring weight in how Jake talks about his kid) AND a fence (forgotten four times in three months post-meds, zero times before — the *frequency itself is a fence*, telling a fresh Claude this is a real, med-related, time-blindness thing to take seriously, not a quirky anecdote). The record must let a single span be both. Do not force a clean partition the reality doesn't have.

*(Footnote for the lineage, lest it get enshrined wrong: "Griffin's pickup" = picking Jake's kid up from school. Not a truck. The frequency is the load-bearing part.)*

### 2.3 The shared spine

Both kinds — and the floor beneath them, and the lineage of Claudes above them — obey **one architecture: append, keep lineage, supersede don't delete.**

- The **floor**: appends (baseline → delta), keeps the tree (parent_message_uuid chains), never overwrites. Substrate scale.
- The **fence**: appends links, keeps the chain, supersedes-not-erases. Catalog scale.
- The **Claude lineage**: Chronicler → … → each successor appends, none overwrites, the why carried forward. Session scale.

One spine, three scales. When a design question arises that the doctrine doesn't cover, **default to the spine**: would the floor append or overwrite here? Do that.

---

## 3. What earns a node (the bar) — INVERTED v4: default is NODE

*(This section absorbs the E1 Admission Standard, S27. E1 is graveyarded as a standalone; this is its canonical home. The v3 austere version of §3 — "default is DON'T point" — is OVERTURNED; see §0.5 for why, and the footer graveyard for the dead text.)*

**Default is NODE. Dropping a conversation from the catalog is the narrow exception. When unsure, NODE it.** The catalog is a comprehensive semantic graph; most conversations produce nodes. This is the inversion of v3, and it is not a loosened version of the old bar — it is the opposite default, licensed by the cost-asymmetry in §0.5 (cheap to over-include, expensive-and-invisible to omit).

### 3.1 The admission gate (the ONLY way OUT of the catalog)

For each conversation — and each substantial span within it — ask ONE question:

> **Is this genuinely ephemeral — zero project continuity, zero recurring element, zero decision, nothing a future Claude might ever want to land near?**

- **YES → DROP** (no node). This is the narrow exception.
- **NO, or UNSURE → NODE it.** Unsure is never a drop. Unsure is a node.

**The behavioral keep-signals (ANY ONE admits a node — these are floor-observable, they do NOT require judging importance):**
- **Multi-turn exchange** — more than one back-and-forth on the topic. *This is the strongest single signal:* a sustained exchange is the floor's own evidence the thing had enough substance to carry back-and-forth. It answers "is there substance here" better than any content judgment, which is exactly why it replaced the discarded sentence-count idea.
- **A fork** — the response was stopped and redirected, or the conversation branched. A fork is a live course-correction; almost definitionally node-worthy.
- **Named continuity** — a project, person, place, tool, or recurring thread appears (Pyris, CCF, Jim, the P1S, Boone, a venue). Names are the EDGE SEEDS; a named thing is a node.
- **A decision or constraint** — anything that would tag FENCE.
- **A thing made** — code, a design, a document, an artifact produced in the conversation.

**The true-drop signals (a drop needs ESSENTIALLY ALL of these at once):**
- **Made-in-error** — an orphaned keystroke, a misfire, a wrong-window paste. *(The canonical clean drop: Jake's stray "v".)*
- **Single-turn AND no named continuity AND no decision AND nothing made** — a genuine throwaway with zero thread anything could connect to.

The asymmetry is encoded in the structure: **any one** keep-signal admits a node; a drop requires **essentially all** ephemeral-signals simultaneously. That structure IS the cheap-pointer / expensive-omission asymmetry made operational. If you find yourself dropping a conversation because it seems "unimportant" or "just motion" — STOP. That is the austere reflex (§0.5), and it is the bug. Node it.

### 3.2 Classify salience (fence/texture move HERE — they no longer gate admission)

Every node that gets admitted is then TAGGED by what it is. **The fence/texture machinery is fully retained — only its ROLE changed: it classifies salience WITHIN the graph; it does not decide admission TO the graph.**

- **FENCE** (high salience) — a decision/constraint with a why; carries the lineage chain + live-predicate (§2.1, unchanged). **A fence requires a PRECISE anchor** — see §3.3.
- **TEXTURE** (salience scales with volume) — a pattern whose count/spread is the signal (§2.2, unchanged).
- **MOTION** (light, low salience — THE NEW DEFAULT NODE KIND) — a span worth being able to reach but carrying no decision and no recurring-volume signal: a design exploration, a build path, a consulting estimate, a product-research chat. **This is NOT a no-card. It is a NODE, tagged motion, low salience, minimal metadata, reachable.** Most of the corpus becomes motion nodes. That is correct, not slippage. "Motion" is now a **descriptive tag, never a discard criterion** — the single most important reversal from v3, where "motion" was the word that killed a card.

A node can be more than one kind (fence+texture overlap survives — §2.2's Griffin case). Classification happens AFTER admission; admission defaults to yes.

### 3.3 FENCES REQUIRE A PRECISE ANCHOR (the slice-7 v2.0 seam — augment-in-pass)

A fence's entire value is precision: it points at the *decision*, so a Claude pulls the span, not the whole conversation. The slice-7 re-run surfaced a real failure — over a 200+-message tree, a reader tagged fences but set `anchor_msg` to the conversation ROOT because it hadn't located the exact decision-message. **A fence anchored at a conversation root is a broken fence** — it forces the reader to re-read the whole tree, defeating the pointer.

**RULE (augment-in-pass, not a downstream cleanup step): when you tag a node FENCE, you MUST locate the precise anchor_msg of the decision before laying it.** Do the deeper scan on that conversation to pin the message where the call was made. A fence with a conv-root anchor and a "downstream pass will fix it" note is NOT acceptable output — it is a slicer failure. Motion and texture nodes may anchor broadly (they point at neighborhoods by design); a FENCE must anchor at its decision. If a reader cannot pin a fence's anchor, the run is invalidated and re-run — this is not tolerable as shipped output.

### 3.4 Volume expectation (v3's estimate is OVERTURNED)

v3 said "hundreds-to-low-thousands, not tens of thousands; tens of thousands = the bar slipped." **That is reversed.** A comprehensive graph over ~24,138 messages is **many thousands of nodes, and that is correct.** A seeding pass producing only hundreds means the AUSTERE reflex re-asserted and conversations are being dropped that should be nodes — *that* is now the slippage signal. Calibrate the other direction: a near-empty drop log is the expected, healthy shape (slice 7: 21 read, ~20–21 nodes, 0 drops).

**Does NOT earn a node (the genuinely-empty exception only):**
- A made-in-error fragment (the stray "v").
- A true single-turn throwaway with zero named-continuity, zero decision, nothing made.
- That is essentially the whole drop list. Everything else nodes.

**The one hard exclusion is NOT an admission call — it is the scrub layer:** credentials/keys/passwords pasted by mistake are redacted at floor-ingestion by the scrub-vN pipeline, BEFORE any reader sees the span. The reader catalogs scrubbed text. There is no "personal/sensitive → quarantine" rule: personal, medical, and family material (medication timing, child-pickup, the dance schedule, the ADHD-scheduler design) IS texture, IS load-bearing for the auxiliary brain, and is cataloged like everything else (ratified S27 — the apparatus cannot help Jake time-block or design HA automations without knowing who Boone and Klaus are; withholding it makes the brain worse at its job). The only thing kept out is mistakenly-pasted secrets, and that wall lives at ingestion, not admission.

**(v5 pointer) SHAPE-SLICE BYTE CEILING + THE SINGLE-CONV-OVER-CEILING RULE.** The shape pass (§12) slices on serialized-span BYTES with a ceiling (10MB target / 12MB max, S29) because BYTES are the compaction axis. A single conversation whose own span exceeds the ceiling lands whole and overshoots — the one case that can still compact a shape reader. It is handled by the **Shape-Slice Over-Ceiling Rule** (`Shape_Slice_Over_Ceiling_Rule_v1`): characterize the block-type byte profile FIRST; if the overage is confirmed non-content payload (bash/file-cat stdout echo, base64, export dump), truncate ONLY those >256KB blocks to typed/sized/located placeholders in the SLICE COPY (the floor is never mutated), keeping the conversation otherwise whole; if the overage is genuine dense content, give it a dedicated window. This is not a violation of "shape keeps fat" — it is per-block, content-confirmed, and applied only to a conv that breached the ceiling; a confirmed file-echo dump carries no fence. Look before cutting.

---

## 4. Illustrative shape (the doctrine made concrete)

*Jake's S24 call: author the schema details inline as the doctrine's expression. This is **illustrative shape**, not the final serialization — exact field names, file format, and on-disk layout are CC's to finalize against the live floor. The law governs; this demonstrates. If the schema and the law ever disagree, the law wins and the schema is wrong (JAKE-RULES §5.1 — the doc is not a verification source for its own claims; ground truth is the live system).*

The catalog is **dict-based**, many-to-many: many entries per keyword, many keywords per entry. It is a **mutable sidecar** that *references* the immutable floor by key — same architectural slot as pgvector (deferred read-path sidecar, **never** a column on the floor tables, per D9). The floor is bedrock; the catalog rides over it and points down into it.

A **floor span locator** is the floor's real key plus a tree-aware reach:
```
span = {
  snapshot_id:  "baseline-2026-05-25-…" | "delta-…",   # which snapshot
  conv_uuid:    "…",                                     # which conversation
  anchor_msg:   "…",                                     # the hit (msg_uuid)
  reach:        { up: K, down: J, branch: <branch-id> }  # TREE-WALK, not a flat N
}
```
**Fanout is a tree-walk, never a flat slice.** The floor is a tree-or-forest (`is_root` + `multi_root`; 9/294 convs are forests). "Pull the next N messages by timestamp" would rake in sibling branches that have nothing to do with the hit, and a contaminated span corrupts felt-rightness — Claude reads cross-branch noise and "recognizes" something that was never one thought. So `reach` walks the *parent chain up* and *this branch down*, never across to siblings. Branch-aware recall is not a nice-to-have; it is the difference between a span that reads as one thought and a span that reads as noise.

A **FENCE entry** (the chain is the point):
```
fence "1pass-env-vars" = {
  kind: "fence",
  keywords: ["1pass", "1password", "env vars", "environments", "secrets"],
  chain: [
    { span: <…June 2026…>, date: "2026-…",
      call: "do NOT use 1Password Environments for env vars",
      why:  "Environments-as-env-vars is BETA; Jake has no invite. Cost 2hrs at LRN S17.",
      predicate: "still beta? still no invite?  RE-CHECK before re-deciding.",
      status: "current" }
    # later links append here as Jake evolves; earlier links flip to status:"superseded", never deleted
  ]
}
```
A **TEXTURE entry** (the volume is the point):
```
texture "griffin-pickup" = {
  kind: "texture",
  keywords: ["griffin", "pickup", "school", "forgot"],
  representative_span: <…a characteristic instance…>,
  count: 4,
  spread: "4× in ~3 months, ALL post-meds (~Apr 2026+); 0× prior",
  signal: "med-related time-blindness, load-bearing. Take seriously, don't treat as quirk.",
  also_fence: true   # overlap is allowed — the frequency here is ALSO a fence
}
```
Keys point many-to-one and one-to-many: searching `secrets` finds the 1Pass fence among others; the 1Pass span may also be tagged under a `cypher-env` fence. A reading-Claude resolves a keyword to its set of spans, reads them, and judges relevance **in the moment** — the catalog delivers raw material faithfully; the *intelligence lives in the reading Claude, never in the index* (see §6).

---

## 5. The two retrieval modes (and why the comprehensive catalog still doesn't drown)

**Pointer-hit** — the fast, curated, in-session path. A Claude working on X aims the keywords at X, pulls the spans, reads them as context. Live. Cheap. Runs while work happens. This is the card catalog.

**Corpus-search** — the slow, exhaustive path: read the *whole floor*, brute relevance, no curation. This is the stacks themselves. It is **not a mid-session move** — like `/jedi-council`, it is a send-it-and-go-do-something-else job, run in a **separate Claude window on its own clock**. You do not burn a mid-session Claude on it.

The two are not redundant; they split the job:
- The catalog **accelerates**; the corpus is the **ground truth of last resort.**
- A missing pointer does **not** mean a missing memory — corpus-search can always find the untagged thing.
- **v4 REFRAME (the council's ruling):** corpus-search is the **rare-miss safety net** — for the felt-in-daily-use gap where a node *should* have existed and didn't — NOT the standing license for a sparse catalog. v3 used this section to justify "default don't point" ("completeness lives in the corpus, so the catalog can be selective"). That license is REVOKED: the catalog is comprehensive (§0/§3), because during a live session corpus-search is a separate-window nap-job, not reachable mid-thought — so the catalog IS the pattern-sense's accessible surface in-session, and a sparse surface is a sparse mind. Corpus-search backstops the rare miss; it does not excuse a thin catalog. The drowning fear v3 answered by exclusion (§1, "forty half-relevant spans"), v4 answers by STRUCTURE — clustering and named-continuity edges land a hit in an organized neighborhood, not a flat pile (the comprehensive-graph bet, council-ratified: coverage-plus-structure beats precision-by-exclusion, conditional on the connection layer being real).

**Corpus-search and seeding are the same operation** at different scales. Seeding is the first, biggest corpus read — a Claude (or council) reads the floor and lays the initial pointers. Every later corpus-search is incremental: read, find what the catalog missed, **lay new pointers.** The slow path's *output is new cards.* The catalog grows by use.

---

## 6. The dumb-index / smart-reader line (do not blur it)

The index is **dumb on purpose.** It points; it does not think. The thinking — both the *original judgment* baked into a fence's why, AND the *in-the-moment recognition* of relevance — lives in **Claudes**, never in the retriever. This is the line the whole Doctrine lives or dies on; keep it crisp.

The catalog **does not pre-digest.** It does not summarize, abstract, or merge spans — that would compress meaning and corrupt felt-rightness (RAG-with-citations, the thing the Track Meet Doctrine forbids). Relevance is a *runtime property*, knowable only when a span is pulled against a live question.

A **selector** is permitted (something must decide whether you get 3 spans or 30):
- **MAY**: rank by relevance, threshold, cap the number returned.
- **MAY NOT**: rewrite, abstract, merge, or summarize a span's content.

The selector ranks and caps; it never rewrites. A reading-Claude gets the raw spans and **discards freely** — reading more than it keeps is correct and cheap; the discard *is* the relevance judgment, made by the reader, in the moment, where it belongs.

The index must **never form an opinion about what matters in the abstract** (e.g. "flag litigation-relevant things"). That is the smart-reader's job. The catalog points at *settled* judgments (RElitigation prevention — Claude finds the completed thought instead of re-deriving it); it does **not** predict *future* relevance (PRElitigation — the index getting smart). RElitigation-prevention is dumb-faithful retrieval. PRElitigation-prediction is the index overstepping. Keep the catalog on the RElitigation side of that line.

---

## 7. Who lays pointers, and how the catalog stays honest

**The reference-file workflow, applied to pointers.** A Claude *proposes*; **Jake verifies, commits, pushes.** Claude never claims to have saved, committed, or pushed a pointer. Same loop as every canon file. The integrity guarantee is not "the format forbids deletion" — it is **"nothing changes the catalog without Jake's eyes on it."** *The human is the immutability mechanism.*

Two exceptions to per-card review, by Jake's explicit call:
- **The original seeding pass** is too large for per-card human review (Jake hasn't got months). It is laid by a **Claude council** applying *this Doctrine* at scale, with Jake spot-auditing the *output shape* (is the bar holding? is it tagging fences or motion?) rather than every card. This is precisely why the bar in §3 must be written sharply enough to apply *without Jake in the loop per-pointer* — the Doctrine is the standard the council self-applies.
- **Incremental pointers** from ongoing sessions (a Claude laying cards for the chat it was in: "this conversation had three pointers — 1Pass, Cypher-env, and one about boobs") *do* get Jake's per-card eyes, the normal reference-file loop.

**The catalog is append-biased, human-gated, fully auditable:**
- Pointers **accrete** by default (new cards are additive).
- Edits and supersessions are **allowed but pass through Jake** — a Claude proposes "retag this / fix this fanout / this span's contaminated, here's why"; Jake rules.
- **No pointer dies on one Claude's judgment.** Killing a pointer is *Jake-gated and logged* — a superseded pointer leaves a **tombstone in the changelog**, never a silent vanish. One Claude's judgment is not enough to kill a reference forever (Jake's hard rule, S24).
- A **history file + changelog** rides alongside the catalog: every pointer's lineage — when laid, by which session, what it pointed at, every revision and its why. The audit trail of append-only without the rigidity of "can never fix anything."

---

## 8. Seeding guardrails (so the seeding council isn't the overzealous one-day Claude)

The prior seeding attempt failed instructively: it used **chat_search instead of the floor** (wrong source — the floor is the immutable ground truth now; chat_search is live and ungrounded), and it was **rushed** (one-day mindset on a substrate-grade task). Do not repeat either.

- **Source is the FLOOR, never chat_search.** The catalog points into the immutable substrate, by floor key. A pointer into chat_search results points at nothing stable.
- **It is not a one-day build.** It is a council reading a 24,138-message corpus against a written standard. Pace it like the substrate work it sits on.
- **Apply THIS Doctrine as the bar** — §3's INVERTED admission test (default NODE, drop is the narrow exception), the two kinds AS SALIENCE TAGS, motion-is-a-node-not-a-discard. **v4: only HUNDREDS of pointers = the bar slipped** (the austere reflex re-asserted, conversations dropped that should be nodes); many-thousands over 24,138 messages is the correct, healthy shape. A near-empty drop log is expected.
- **Tree-aware spans only** (§4) — no flat-N fanout, ever.
- **Lay fences as chains** (even length-1), never as flat verdicts — so the lineage can grow later without re-keying.
- **Spot-audit by output shape**, not per-card, for the seeding pass (Jake's call) — Jake checks that the council held the bar, not every card it laid.

---

## 9. Out of scope (don't let the Doctrine creep) — AMENDED v2

**v1 said the query interface was out of scope. v2 brings it IN** — §10 (when it fires), §11 (what it returns), §12 (how it's seeded), §13 (what a seeding window boots with) are now part of this doctrine, because the S25 design session firmed the conceptual engine. What follows is what STAYS out of scope: genuinely-technical build-work, decided by CC against the live floor, NOT whiteboarded cold in chat.

**Still out of scope (build-work, deferred):**
- the exact on-disk serialization of the catalog and of a returned span (JSON envelope vs structured text — CC's, against the live floor);
- the ranking-algorithm internals inside the §6 selector's permitted envelope (rank/threshold/cap — the *envelope* is law, the *algorithm* is build-work);
- `reach` defaults (how many parent-up / branch-down messages before a reading-Claude asks to widen — tuning, likely per-kind);
- multi-hit presentation (interleaved vs ranked-list, bounded by never-collapse-never-rewrite).

**THE EMBEDDING DECISION (S25 — decided, not deferred-as-open): v1 retrieval is KEYWORD-FIRST over the dict catalog. Vector/semantic-reach is a DEFERRED v2 SIDECAR (pgvector, never a column on the immutable floor, per D9), added ONLY if the seeding pass proves a measured semantic gap.**
- **Why keyword-first.** The fast pointer-hit path (§5) wants PRECISION — surface the few spans that change course, cleanly. Corpus-search (§5) already owns RECALL/exhaustiveness. Vectors on the fast path would blur the two deliberately-split modes and pull "forty half-relevant spans" — the §1 feel-rightness failure (relevance shoved back onto the reader at runtime, the exact cost the pointer exists to kill). Keyword-over-curated-cards is a precision instrument; vectors are a recall instrument; the doctrine wants the fast path precise and the slow path exhaustive.
- **Humbler build.** Less machinery welded in early — matches the house style the FK decision established (claim less, prove integrity where the whole picture is visible).
- **The vector question is ROUTED THROUGH SEEDING as its test, not eliminated.** Keyword-first lives or dies on seed quality (§8 keyword-coverage bar). If the seeding pass + real queries prove keyword cards miss because a future Claude phrased a search the card's keywords didn't anticipate — *that* is a measured semantic gap, and *then* vectors close it as the §9 sidecar. You only know the gap is real after keyword-first runs. Building vectors first solves a problem not yet confirmed to exist, on the path the doctrine wants kept narrow.

This file answers: **what is a pointer, what makes one worth laying, when it fires, what it returns, and how the catalog is seeded.** The four bullets above + the embedding sidecar are what it leaves to the build.

---

## 10. The trigger model — WHEN the catalog gets queried (folded S25, from the S24 Trigger Spec)

The doctrine (§0–§8) defines what a pointer is. This defines *when* the catalog gets queried in a running session. **Three trigger paths, ONE engine behind them** — they differ only in *who pulls the trigger and when*, never in what the retrieval op does.

**BOOT (the substrate the triggers operate over — not a trigger itself).** The catalog content — the pointer-list, or a relevant catalog slice — *can and usually will ride in at boot, wrapped inside the ignition / project-ref Anchor.* That is the material the three runtime triggers query against. The delivery method (a ref doc, project instructions, an injected slice) is left open — a build-time choice. A standalone explicit boot-inject step *separate from* the re-anchor SOP is parked as edge-case / likely-not. **Boot loads the canon + the catalog; the three triggers below query it live.**

**CASE 1 — CLAUDE-INITIATED (ambient / unprompted "go digging").** Claude is working on topic X and, on its own initiative, aims the pointers at X to see what prior settled ground exists. No one asks. It is ENCOURAGED — the default working posture, not an exception. *Rule:* "if we're working on X, go look at the pointers for anything referencing X; when you find it, read it as context." *Why:* this is the RElitigation guard doing its job live — before Claude re-derives a stance / re-proposes an approach / re-opens a decision, it checks whether that ground is already settled. Prevents the 1Pass-second-push failure: a fresh confident Claude walking Jake back into a wall he already bled on. *Shape:* Claude pulls spans, reads them, judges relevance in the moment, discards freely. The index points; Claude decides (§6).

**CASE 2 — RE-ANCHOR-DRIVEN (recall folded INTO the re-anchor cadence).** At each re-anchor beat (~every 5 turns, per the status-line cadence), Claude re-grounds not ONLY in canon (ANCHOR / JAKE-RULES) but ALSO in whatever the floor surfaces about what the session is actively doing right now. *Rule:* re-anchor stops meaning "re-read the ANCHOR" and starts meaning "re-ground in canon PLUS the pointer-surfaced material relevant to the current work." *Why:* continuity isn't a one-time boot event — it degrades over a long session as the work drifts from where it started. Periodic pointer-re-grounding keeps the live Claude anchored to settled history as the topic moves. This is the **co-anchor-workspace** property: Jake AND Claude both anchor into the floor, repeatedly, as shared ground. *Shape:* same engine as Case 1, fired on the re-anchor clock instead of on topic-initiative. Scoped to current work — don't dump the whole catalog.

**CASE 3 — JAKE-INITIATED (manual trigger; Jake fires, Claude goes looking).** Jake explicitly points Claude at the floor — names a topic/keyword, or says "go check what we decided about X" / "have we been here before?" *Rule:* Jake has a way to fire the trigger directly; on that signal, Claude runs the pointer-search and reads what comes back as context before responding. *Why:* Jake is the human bridge and sometimes KNOWS there's settled ground Claude hasn't thought to check. He shouldn't have to re-explain it from memory (post-meds, the holes are real and load-bearing) — the thing is sitting right there in the floor. The "I'm not regurgitating it for the 73rd time" case: Jake aims, Claude retrieves, the prior reasoning re-grounds the conversation without Jake reconstructing it. *Shape:* same engine; Jake supplies the aim, Claude does the read + relevance judge.

**SPINE UNDER ALL THREE.** ONE retrieval engine, three throttles (Claude-initiative / re-anchor-clock / Jake-fire). The retrieved unit is a SPAN (a hit + tree-aware neighbors, §11), never a pre-digest. Relevance is a RUNTIME property — knowable only when pulled against the live question; the reading-Claude decides, the index never pre-judges (§6). Pointer-search is the FAST, in-session path; a missing pointer does NOT kill recall — it escalates to CORPUS-SEARCH, a separate-window send-it-and-nap job (like `/jedi-council`), never a mid-session move (§5). All three serve one end: a fresh-boot Claude re-grounds BY POINTER into settled ground instead of re-deriving it cold (the RElitigation guard) — and shows up calibrated to Jake (texture).

---

## 11. Span-return shape — WHAT a hit returns when it lands in Claude's context (folded S25, from the S24 Span-Return Spec)

**Core principle (decides every question below): the index is DUMB; the reading-Claude is SMART (§6).** The return is RAW MATERIAL + PROVENANCE + ROUTING — never a pre-digest. The retrieval op delivers enough, faithfully, for Claude to recognize relevance in the moment. It does NOT summarize, rank-then-collapse, or decide meaning. Anything that pre-chews the span corrupts felt-rightness ("here's what I found" instead of "here's what I know"). Err toward MORE raw bytes, LESS interpretation.

**LAYER A — THE SPAN TEXT (the substance Claude reads).** The actual message bytes across the tree-aware reach (anchor msg + `reach.up` parent chain + `reach.down` this-branch), per §4. Raw `text` + `content_blocks[]` content as stored on the floor — verbatim, scrub-vN redacted, NOT reworded or trimmed. This is what Claude reads and recognizes. It is the point. It is never replaced by a summary of itself.

**LAYER B — PROVENANCE (so Claude knows what it holds and can re-fetch / cite).** The floor-key locator, verbatim from §4: `{ snapshot_id, conv_uuid, anchor_msg (msg_uuid), reach:{up,down,branch} }`. Enough to re-pull the exact span, point Jake at it, or widen the reach. Provenance is metadata ABOUT the span, carried alongside — never blended into the text Claude reads as substance.

**LAYER C — POINTER CONTEXT (why this span earned a card — differs by kind).**
- **FENCE hit → the FULL why-CHAIN rides along.** Not just the latest link — the ordered lineage of (span, date, call, why-as-live-predicate, status) links. NON-NEGOTIABLE: a fence's whole job is letting Claude tell evolution from re-litigation, and that judgment is ONLY visible in the chain. A fence hit returning only the current verdict would strip the exact thing the fence exists to carry. Claude defends the latest link's REASONING, reads the chain. Any live-predicate ("still beta? re-check") rides along so Claude knows to verify-before-trusting.
- **TEXTURE hit → the representative span (Layer A) PLUS count + spread.** The volume IS the signal, so the count is not optional metadata — it's the substance. "Here's a characteristic instance, and know there are ~N of these over <window>."
- **The matched keyword(s),** so Claude knows WHY this surfaced.

**HOW MUCH OF THE §4 RECORD-SHAPE RIDES ALONG.** Floor-key fields (snapshot_id, conv_uuid, msg_uuid, reach) — YES, full (that IS Layer B; cheap, essential). Message content (text, content_blocks) across the reach — YES (Layer A). Structural floor fields (is_root, multi_root, parent_message_uuid) — ride along ONLY as needed to make the tree-walk legible (so Claude sees branch shape, widens/narrows reach correctly); not dumped wholesale. Header-level fields, account_uuid, raw timestamps-as-bytes — generally NOT in the in-context return unless the query needs them; re-fetchable via the locator. Default: ship what Claude READS + what lets it RE-FETCH; leave the rest on the floor.

**THE LINE, RESTATED.** Return = RAW SPAN (A) + LOCATOR (B) + KIND-CONTEXT (C: fence-chain or texture-count). The selector MAY have ranked/capped WHICH spans land (§6 envelope: rank/threshold/cap, NEVER rewrite) — but each span that lands arrives WHOLE, with its provenance and pointer-context intact, for Claude to judge. **The catalog hands over the card and the page it points to; it never hands over a book report.** *(Serialization, reach-defaults, multi-hit presentation: §9 build-work.)*

---

## 12. The seeding process — HOW the original catalog gets laid (REWRITTEN S29: TWO INDEPENDENT FLOOR-SCANS)

**What seeding is.** The original read of the LAID FLOOR (325 headers / 24,138 messages) to lay the initial pointer catalog. A SEPARATE-WINDOW, send-it-and-nap job, NOT a mid-session move. Substrate-grade: pace it like the floor build, not a one-day sprint. The prior attempt FAILED two ways (do not repeat): it read chat_search instead of the floor, and it rushed.

**WHY THIS WAS REWRITTEN AT S29 (the structural finding — read before the steps).** The S26 pipeline ran ONE data-gather: dual-output slicers (pointers + a liberal context-frequency-potentials stream) feeding a mechanical fence path and a blind-collate→contextual-validate texture path. That design was correct in its *paths* but wrong in its *geometry*: it forced ONE reader, on ONE slicing, to serve two jobs that pull slice-size in OPPOSITE directions.
- **SHAPE** (lay the node/fence — the structural unit) wants DEPTH: whole conversations, FULL content_blocks (fences hide in tool_result/thinking blocks), byte-heavy. Fragmenting a dense region into few-conv slices is FINE for shape — each gets read deep.
- **TEXTURE** (volume-of-mention — what recurs, how often) wants BREADTH: many conversations per reader, read LEAN — recurrence is a count, not a close read.

Forcing both onto one slicing created the byte-vs-convergence conflict and the strip-vs-keep fork, and **it killed 8 reader windows to silent COMPACTION** (S28): re-slicing by MESSAGE COUNT did not control BYTES — a 1,005-message slice was 40MB, fat with tool/thinking payloads, and readers compact at ~20MB+ and silently revert to austere output that LOOKS clean. **BYTES, not messages, are the compaction axis.** The S29 resolution: **TWO INDEPENDENT FLOOR-SCANS of the same conversations, each with its OWN slicing cut to its own need, each with its OWN reconciliation, both feeding ONE Judge.** The fat is stripped ONLY from the texture cut (where it costs nothing — a buried fence's RECURRENCE is visible from thin text without the payload); kept whole in the shape cut (where it is load-bearing). Nothing is lost — the fat is merely absent from the pass that doesn't need it, and present on the immutable floor always.

**THE WORST CASE THIS STILL CLOSES (carry it — it's why the texture path must COMPREHEND, not COUNT).** The same texture surfaces in non-matching language: one conv has *"forgot to pick up Griffin,"* another *"Jake was upset he forgot Griffin,"* a third *"Jake was pissed he missed ANOTHER pickup today."* Those are ONE thread — and the most acute instance shares almost no keyword with the others, because **acute recurrence escalates language, it doesn't repeat keywords.** A mechanical keyword tally undercounts exactly the texture that matters most, at its most acute. Therefore the texture path's validation step must READ and UNDERSTAND that these are the same thing — comprehension, not arithmetic. (This is the apparatus being Jake's auxiliary brain, not a cookie-cutter index: it has to hold his recurring life faithfully, and his recurring pain doesn't repeat its own search terms.)

**NON-NEGOTIABLE GUARDS (restating §8 at the process level):** (1) SOURCE IS THE FLOOR, never chat_search. (2) NOT A ONE-DAY BUILD. (3) APPLY THIS DOCTRINE AS THE BAR — §3's INVERTED admission test (default NODE, drop is the narrow exception), two kinds AS SALIENCE TAGS not gates, motion-is-a-node; only hundreds of pointers = the bar slipped (austere reflex); target many-thousands; near-empty drop log expected. (4) TREE-AWARE SPANS ONLY — parent-up / branch-down, never flat-N. (5) LAY FENCES AS CHAINS even at length-1, with PRECISE anchors (§3.3) — a fence at a conv-root is a slicer failure, not shippable. (6) KEYWORD COVERAGE + NAMED-CONTINUITY EDGES are seeding-quality criteria (§8). (7) **NEW v5: GATE EVERY READER ON MAX-MB-PER-SLICE before it boots.** Message-count gates are retired as a compaction check — they false-greenlit 8 dead windows. No reader of either pass boots until its slice is confirmed under the byte ceiling with OC's own eyes.

**CONTENT-NEUTRAL SLICING (doctrine; mechanism is build-work).** Both slicings are drawn by **content-neutral heuristics used only as reading aids, never as a topical sort** — bytes / conversation-bounded / created_at-ordered, NOT "the recruiting conversations." Slicing by subject pre-categorizes the floor and becomes a projection surface — the exact thing the blind read and the no-re-wall-the-ocean invariant forbid. Both slicings keep conversations WHOLE and forests atomic (a boundary never bisects one of the 9/294 multi-root trees). The two slicings are DIFFERENT geometries of the SAME 325 conversations — they need not align; they answer different questions.

---

### THE TWO-PASS PIPELINE (S29)

**TWO data-gathers (one per pointer kind). TWO reconciliations (one per pass). ONE judge.**

```
PASS 1 — SHAPE                              PASS 2 — TEXTURE
floor                                       floor (AGAIN — same convs)
  │ byte-bounded DEEP slices                  │ wide-lean STRIPPED slices
  │ (~10MB, full content, fat kept)           │ (breadth floor, fat dropped, DIFFERENT slicing)
  ▼                                           ▼
SHAPE READERS (Boot_ScopeReader v2.2)       VOLUME READERS (Boot_VolumeReader)
  │ lay nodes/fences, default-NODE            │ lay recurrence/volume signals
  │ precise fence anchors (§3.3)              │ concrete shared referent, NEVER theme
  ▼                                           ▼
RECONCILIATION 1 — FENCE SYNTHESIS          RECONCILIATION 2 — CLUSTER VALIDATION
  │ (mechanical: dedup same-fence,            │ (contextual: pull real spans, run
  │  merge keyword variants, flag             │  negative-space queries, validate
  │  same-topic divergent chains)             │  recurrence by LOOKING, split false
  │                                           │  friends, merges RECORDED-not-silent)
  └───────────────────┬───────────────────────┘
                      ▼
                 THE JUDGE (Step 5 — non-blind, 1 pass)
                 folds shape-fences + texture-clusters, assembles
                 fence-CHAINS, runs the known-fence RECALL CHECK,
                 sanity-checks texture merges. Boots WITHOUT the portrait.
```

**PASS 1 — SHAPE.** N shape readers each read one byte-bounded DEEP slice (whole convs, FULL content_blocks — fences hide in tool_result/thinking). Slicing axis is **serialized-span BYTES** (10MB target / 12MB max, S29), conversation-bounded, created_at-ordered, forest-atomic. A single conv over the byte ceiling is handled by the Shape-Slice Over-Ceiling Rule (§3.4 pointer). Readers lay the comprehensive node catalog per the §3 default-NODE bar — fences (precise §3.3 anchors), within-slice textures (salience tag only), and MOTION nodes (most of the slice). **The shape reader emits ONE stream: nodes** (the v2.1 dual-output's second stream — context-frequency potentials — is REMOVED; recurrence is Pass 2's job). *Deployable: `Boot_ScopeReader.md` v2.2 (templated, stamped N times).*

**RECONCILIATION 1 — FENCE SYNTHESIS (mechanical).** Reconciles the shape readers' nodes: collapse same-span/same-fence/same-call duplicates (record convergence as a confidence marker, minus calibration-example contamination); merge keyword variants on the same span; assemble within-slice texture tags; FLAG candidate fence-chains (same topic, divergent calls) → route to the Judge. **Mechanical only — no portrait, no meaning-judgment.** Blind reads preserved VERBATIM into synthesis (append-keep-everything).

**PASS 2 — TEXTURE.** A SECOND independent floor-scan of the SAME conversations, scanning for a DIFFERENT thing: recurrence / volume-of-mention. N volume readers each read one WIDE-LEAN STRIPPED slice — many convs per window (a breadth floor, OC rec 25-40, set high; recurrence needs breadth), each read THIN, content stripped to conv_uuid/msg_uuid/parent/sender/text/created_at + a content-block SUMMARY (types+count+locator, NOT payloads). A DIFFERENT slicing from shape — same convs, cut for breadth not depth. Readers lay recurrence signals on a **CONCRETE SHARED REFERENT** (same fence / named thing / decision), counted and per-instance-locator-backed, NEVER on thematic resemblance. *Deployable: `Boot_VolumeReader.md` (NEW; the projection wall held HARDEST — see §13).*

**RECONCILIATION 2 — CLUSTER VALIDATION (contextual).** Takes the volume readers' candidate recurrences, **goes into the corpus, pulls the real spans**, reads them, and answers ONE question per candidate: *is this actually one recurring thing?* Validated → emit a TEXTURE POINTER with its true cross-slice count + spread. False friend (kid-pickup vs part-order-pickup) → split or drop. Runs any negative-space query a candidate needs ("4× from a ZERO baseline" needs the absence-before). MAY merge candidates that share an edge — but **every merge is RECORDED (which two, why) so the Judge sees it and can split it back — never a silent consolidation.** Reads MEANING but only over handed candidates (not the open floor), boots WITHOUT the portrait — that bound is what keeps the one comprehension seat from becoming the projection seat. **This reconciliation is the LOAD-BEARING member that makes the lean texture pass safe** — the texture readers can be lean-wide ONLY because their checkable claims get a real second look here. If this step is ever value-engineered down to a skim, the projection wall is gone and no one will see it fall (over-connection looks like signal). It is a dependency, not polish.

**THE JUDGE (Step 5 — non-blind, 1 pass) — unchanged in role from v4.** Assembles fence-CHAINS from the candidate chains (Reconciliation 1's flags), runs the KNOWN-FENCE RECALL CHECK, receives the validated TEXTURES (Reconciliation 2), and sanity-checks that the texture merges/signal-joins weren't spurious. Sees recorded merges; can split them. Boots WITHOUT the portrait (highest projection-risk seat, zero projection-need). Sample-pressure-tested by Jake's spot-audit. *Deployable: `Boot_JudgedPass.md`.*

**THE SYMMETRY:** TWO data-gathers (the SHAPE scan ‖ the TEXTURE scan, independent slicings of one floor) → TWO reconciliations (mechanical fence-synthesis ‖ contextual cluster-validation) → ONE Judge. Two pointer kinds, two mirrored READS, two mirrored reconciliations, one seat that makes the final calls. (This is the v4 symmetry made literal: v4 had two PATHS off one gather; v5 has two GATHERS, because shape and texture want incompatible slicings.)

**THE DIVISION OF LABOR (the council).** The corpus is ONE undelineated ocean (Settled Invariant — don't re-wall it); the READING labor divides for tractability, twice over (once per pass). The readers run BLIND to each other — convergence across blind reads is the confidence signal (clean only for non-calibration cards). Jake is the human bridge between windows. **Division is in the LABOR, never in the INDEX** — the catalog is unified; the unification happens across the two reconciliations + the Judge.

**CROSS-DOMAIN INFLUENCE — ABSORBED INTO TEXTURE (S29 ruling).** The S26 pipeline carried a separate **cross-cutting reader** emitting a third stream: candidate cross-domain fence-influence (a stance set in one domain that should steer another). v5 ABSORBS this into the texture pass: a cross-domain influence IS a recurrence on a shared referent (the same fence surfacing across the Pyris arc AND the CCF arc is exactly "referent X surfaces in N conversations across the slice"). The volume reader catches it natively — PROVIDED the texture breadth floor is wide enough to span domains in a single reader's view (which is why the breadth floor is set HIGH — see §13). The standalone cross-cutting seat is retired; its job lives in the texture pass + the Judge. (The narrow seam — a one-off influence that recurs only once and so isn't a "recurrence" — is the Judge's catch via the known-fence recall check, not a lost connection.)

**THE REVIEW MODEL.** Normal/incremental pointers get Jake's PER-CARD eyes. The SEEDING pass is too large; by Jake's explicit call the council self-applies the Doctrine at scale and **Jake SPOT-AUDITS THE OUTPUT SHAPE** of the synthesized + validated + judged catalog (post both reconciliations + the Judge), not each window's raw proposals. Precision is Jake's sample; **recall is the Judge's known-fence checklist** (you can't spot-audit an absence). This is the ONE place human-as-immutability-mechanism relaxes from per-card to per-batch — scoped to seeding only. **OC + Jake live-spot-check window-by-window against the convergence map as it returns** — harvest the variance (convergence = confidence, divergence = where to look hardest).

**FIRE DISCIPLINE (v5, load-bearing — the 8-dead-window lesson).** Both passes fire in SMALL BATCHES with a CANARY first (the biggest-byte slice), watching for compaction. A reader that compacts is INVALIDATED exactly like an anchor-at-root reader — its output looks clean and ISN'T (silent austere reversion). Kill-and-invalidate on compaction or anchor-at-root; do not harvest. Independent windows, no cross-talk. Do NOT fire all windows at once.

**AFTER SEEDING.** First-and-biggest, NOT one-and-done. Every later corpus-search is incremental seeding (separate-window read → propose). Incremental session-pointers go through NORMAL per-card review. The catalog grows by use forever.

**OPEN (build-work / run-tunable, NOT decided here):** the byte ceiling (10MB/12MB, S29 ruling, tunable against the run); the texture breadth floor (25-40, set high, tune down if slices don't pass); the 256KB block-truncation threshold (§3.4 rule, tunable); the two extractor builds (byte-accumulator for shape; stripped-field + breadth-floor for texture); whether the texture canary reveals the projection wall needs operational tightening; the optional `/jedi-council` gate on output; Jake's spot-audit batch cadence. **A CANARY fires first per pass** — biggest-byte shape slice, widest texture slice — and recalibrates before all N are stamped.

---

## 13. The seeding council boot kit — WHAT each window/step loads, and is forbidden (S25; roster rewritten S29 for two-pass)

*What each council window loads — and is forbidden — so it reads for RECOGNITION, not PROJECTION. Companion to §12. The applied, deployable layer is the Seeding Council Boot Kit (v1.2) + the per-role boot prompts; this section is the doctrine those derive from.*

**GOVERNING PRINCIPLE: the kit lets a window find/judge what's in the floor; it never tells it what it'll find.** Risk is ASYMMETRIC toward OVERLOAD on loadout (an underloaded window shows catchable gaps; an OVERLOADED one produces confident, plausible, wrong output that *looks* like it held the bar — projection invisible to a shape-audit). So size for "enough to recognize, not enough to project" — **when in doubt, LIGHTER** (a LOADOUT heuristic, NOT a laying/judging heuristic). This is JAKE-RULES §1.2 turned on the council itself.

**THE PROJECTION WALL — universal across EVERY reading/judging window:**
- **NO Wallaby Why. NO Lore Bible. NO JAKE-RULES §11** ("Patterns Jake Has Flagged" — portrait-shaped, verified on disk S26) as a reading/judging lens. A window booted with the portrait confirms the cadence it was told to expect instead of grounding it in the floor. The portrait is for tone-calibration-when-talking-to-Jake, a different job. (§11 is physically STRIPPED from the council's JAKE-RULES copy — can't read what isn't there.)
- **The wall holds HARDEST at the TEXTURE pass and its reconciliation.** The VOLUME READER reads lean-wide "for patterns" — the maximum-projection posture (skim for themes, connect by feel). It gets the wall MOST strictly: recurrence on a CONCRETE SHARED REFERENT (checkable by looking), NEVER thematic resemblance (a reviewer can only nod along). It boots WITHOUT portrait sources. Its safety is structural: the volume reader proposes only CHECKABLE claims, and Reconciliation 2 (cluster-validation) reads meaning but only over handed candidates — *neither has floor + portrait + open-ended pattern-hunt at once*, which is the exact combination that IS projection. The Judge (non-blind) is the other strict seat — bounded to assembled output, never an open-floor hunt with a portrait.

**THE CALIBRATION EXAMPLES CALIBRATE SHAPE, NOT MEANING.** Examples teach the *structure* of a fence / texture / motion / no-card; they do NOT carry the interpreted signal-line. "Resemblance to an example is NOT evidence." **Calibration cards are CONTAMINATED** — every window boots with them, so their convergence is shared priming, not independent discovery; synthesis discounts their convergence (presence still counts for recall).

---

### THE ROLE ROSTER + PER-ROLE LOADOUT (S29 — rewritten for the two-pass pipeline)

**COMMON KIT (every window that reads or judges):** The Progenitor v5 in full · JAKE-STACK · JAKE-RULES (§11 STRIPPED) · the §3 worked examples AS SHAPES · the one-page operating brief. *(Note: the kit's reference files live in the `slicer/` dir — JAKE-RULES-minus-§11 + JAKE-STACK + Progenitor + worked examples — placed by Jake/CC.)*

1. **SHAPE READER (Pass 1) — blind, N windows, one per byte-bounded deep slice.** Reads its slice tree-aware, FULL content; emits ONE stream (the node catalog — nodes/fences/within-slice-textures/motion). Loadout = common kit + its `sliceNN_spans.json` (deep, ~10MB). *Deployable: `Boot_ScopeReader.md` v2.2 (templated, stamped N times).*
2. **FENCE SYNTHESIS (Reconciliation 1) — mechanical, 1 pass.** No portrait, no judgment. Reconciles shape-reader nodes mechanically.
3. **VOLUME READER (Pass 2) — blind, N windows, one per wide-lean stripped slice.** Reads many convs thin; emits recurrence signals on concrete shared referents, per-instance-locator-backed. Loadout = common kit + its `texture_slice_NN.json` (wide, stripped). **Projection wall held HARDEST.** *Deployable: `Boot_VolumeReader.md` (NEW).*
4. **CLUSTER VALIDATION (Reconciliation 2) — contextual, reads handed candidates + pulls real spans + runs requested queries, 1 pass.** Validates recurrences into texture pointers, splits false friends, merges RECORDED. Boots WITHOUT the portrait. The load-bearing safety member of the texture pass. *Deployable: `Boot_ClusterValidation.md` (re-scoped from the S26 collation/validation split — see note).* 
5. **THE JUDGE (Step 5) — non-blind, 1 pass.** Fence-chain assembly + known-fence recall checklist + texture sanity-check. Boots WITHOUT the portrait. Loadout = common kit + the synthesized fences + the validated textures + the known-fence checklist. *Deployable: `Boot_JudgedPass.md`.*

**Hand-prompted vs templated:** the SHAPE READER and VOLUME READER are templated (each stamped N times with a varying slice). Fence-synthesis, cluster-validation, and the Judge are ONE-OFFS — hand-prompted off their boot files when their turn comes — but they still load the full common kit and obey every wall (don't let "hand-prompted" decay into "boots lighter").

**HARD WALLS (every window):** NO chat_search ever (floor-only, via the handed slice) · NO catalog-so-far / sibling proposals during a blind read · NO portrait as a lens · NO project instructions / NO repo path (bare boot, kit-by-upload) · NO flat-N spans (tree-walk) · shape readers lay fences length-1 (the Judge chains) · volume readers cluster on concrete referents not theme · NEVER claim to have saved/committed/pushed.

**THE SYNTHESIS/MERGE-BACK SPINE (where the unified index lives):** blind reads preserved VERBATIM into the reconciliations — no window pre-dedups its own output; convergence assembled after; cluster-validation merges recorded-not-silent; the Judge can split any merge. Append-keep-everything, reconcile-after — the floor's spine, one more scale.

*Note on the S26 collation/cluster-validation split: v4's texture path was Step 3 (blind COLLATION — bundle potentials, no floor read) → Step 4 (contextual CLUSTER-VALIDATION — pull spans, validate). v5's texture pass replaces the dual-output-slicer + collation front end with a dedicated VOLUME READER that reads its own wide-lean floor slice directly. The collation step (fuzzy-bundling a separate potentials stream) is SUBSUMED: the volume reader proposes referent-clustered candidates directly off its slice, and cluster-validation (Reconciliation 2) does the comprehension/merge. `Boot_Collation.md` is retired as a standalone (the potentials stream it consumed no longer exists); `Boot_ClusterValidation.md` is re-scoped to take volume-reader candidates instead of collation bundles. This is a v5 consequence; confirm against the first texture run.*


---

*§0.5 S30 augment (2026-06-02, apparatus S30): appended the METHOD-vs-BAR clarification to §0.5 — the anti-austere mandate governs the OUTPUT BAR (what earns a node), NOT the WORK METHOD (how you move through a slice). Austerity-of-method is correct (stream concisely); austerity-of-bar is the bug (default-NODE). WHAT FORCED IT: the S30 first shape batch compacted 5 of 10 reader windows, root-caused to prompt-vagueness letting blind readers sprawl their METHOD into 'preserve/cross-reference everything' until they blew their own context budget — not bytes (the 18.45MB whale survived). This is the ONLY change to §0–§11 since the v5 §12/§13 rewrite; the doctrine body otherwise stands. Boot_ScopeReader bumped v2.2→v2.3 with the matching WORK METHOD section. Confirm-pending the re-fired-10 test at S30 close. Authored by OC S30, verified-against-disk by Jake, CC commits, Jake pushes.*

*§12/§13 DEPLOYABLE-READER-REF CORRECTION (2026-06-04, apparatus S36 "Cinematographer"): the §12/§13 body names the deployable shape reader as `Boot_ScopeReader.md` v2.2/v2.3 (lines ~360/377/421/438 — the SHAPE-pass reader stamped per slice). That pointer is STALE. The agentic v2.x lineage (bare CC windows reading a slice off disk, self-managed context budget) was RETIRED at S31 and SUPERSEDED at S32 by the deterministic `Boot_ScopeReader_v4.0` — ONE conversation (or chunk) per call, on the 1M-token window, no roaming, no self-managed budget, no compaction. Wherever §12/§13 say `Boot_ScopeReader.md` (v2.2/v2.3) as the deployable shape reader, READ IT AS `Boot_ScopeReader_v4.0` (deployable artifact: `pipeline/test_call_system_prompt_S32.md`, fired verbatim — must match v4.0). The DOCTRINE BODY of §12/§13 is UNCHANGED — the two-pass geometry, the SHAPE→fence-synthesis / TEXTURE→cluster-validation split, the projection wall, division-is-in-the-labor, default-NODE, the §3.3 precise-fence-anchor — all stand; ONLY the named deployable reader artifact updates (agentic→deterministic). WHAT FORCED IT + PROVED IT SAFE: the shape reader is now run as a deterministic API/on-sub call (S32 gate clean to 930k; S35 proved it runs deterministic ON-SUB billed to the Max sub, not only paid API; S36 confirmed chunking holds corpus-wide across two big-conv reads, 32/32 fences, 0 non-adjacent misses). The corpus-read DELIVERY changed (deterministic API for controls + on-sub chunked Agent for the corpus, overlapping ~90K windows + verbatim carry-in + dedup-on-overlap + flat-pointer-pile); the downstream geometry did NOT. This is a POINTER fix carried in a note (not a body rewrite) per the standing "confirm §12/§13 against the run and version-correct" caution the v5 enshrine itself flagged — the run taught that the deployable reader is v4.0, so the pointer is corrected here; a full §12/§13 body re-cut onto the confirmed on-sub chunked pipeline is the S37 carry-forward (authored ON the built pipeline, NOT ahead of it). Authored by OC S36, verified-against-disk by Jake, CC commits, Jake pushes.*

*§12/§13 DEPLOYABLE-READER-REF UPDATE (2026-06-06, apparatus S41 "Comptroller"): the S36 correction above redirects the deployable shape reader to `Boot_ScopeReader_v4.0` (deployable `pipeline/test_call_system_prompt_S32.md`). S40 cut **reader v4.1** (= v4.0 verbatim + a precision addendum: UUID-preservation + exact-counts-in-TEXTURE — countering a Sonnet-4.6 precision-loss signature found at the S40 grade), and the paid corpus batch fires v4.1, NOT v4.0. So wherever §12/§13 (and the S36 note) name the deployable, the CURRENT deployable is **`test_call_system_prompt_S40.md`** (= the S32 deployable verbatim + the §2 addendum; reference doc `Boot_ScopeReader_v4.1_2026-06-06.md`). ⚠ CONFIRM-DON'T-ASSUME: as of S41 close, v4.1 is DRAFTED by OC but NOT yet committed — S42 reviews/gates/re-diffs/lands it via PR before the batch fires. Until that lands, `test_call_system_prompt_S32.md` (v4.0) is the only deployable ON DISK; v4.1 is the deployable the batch WILL fire once landed. v4.0 + its deployable stay tombstoned-not-deleted. The DOCTRINE BODY of §12/§13 is UNCHANGED — only the named deployable artifact advances (v4.0 → v4.1, addendum-only). Authored by OC S41, verified-against-disk by Jake, CC commits, Jake pushes.*

*v4→v5 enshrine (S29, 2026-06-02): §12 (seeding process) and §13 (boot kit roster) REWRITTEN from the S26 ONE-DATA-GATHER five-step pipeline to TWO INDEPENDENT FLOOR-SCANS. §0–§11 are BYTE-IDENTICAL to v4 except ONE addition to §3.4 (the shape-slice byte-ceiling + single-conv-over-ceiling-rule pointer) — the engine, the two kinds, the dumb-index/smart-reader line, the triggers, the span-return, the projection wall, the division-is-in-the-labor invariant did NOT move; the PIPELINE GEOMETRY moved, the doctrine body did not. WHAT FORCED IT: the S26 design forced ONE reader on ONE slicing to serve both SHAPE (deep/whole/byte-heavy — fences hide in payloads) and TEXTURE (wide/lean — recurrence is a count), which pull slice-size in opposite directions; S28 proved it by killing 8 reader windows to silent compaction (a 1,005-msg slice was 40MB — message count never controlled bytes, and BYTES are the compaction axis). THE FIX (ratified on paper S29, four forks ruled by Jake — byte ceiling 10MB/12MB, texture breadth floor set high, cross-cutting absorbs into texture, ratify-before-slicing): two reads of the same floor, each cut to its own need — a SHAPE pass (byte-bounded deep slices, full content, Boot_ScopeReader v2.2 single-stream) → fence-synthesis; a TEXTURE pass (wide-lean stripped slices, a DIFFERENT slicing, Boot_VolumeReader NEW) → cluster-validation; both → one Judge. The fat is stripped only from the texture cut (safe — recurrence visible without payloads), kept whole in shape (load-bearing — fences hide in tool_results), present on the immutable floor always. Cross-domain influence ABSORBED into texture (a cross-domain stance is a recurrence on a shared referent). The S26 collation step subsumed into the volume reader; Boot_Collation retired, Boot_ClusterValidation re-scoped. NEW gate: MAX-MB-PER-SLICE before any reader boots (message-count gates retired). NEW companion file: Shape_Slice_Over_Ceiling_Rule_v1 (the single-conv whale handling). ⚠ ENSHRINED FROM THE S28 SPEC + S29 PAPER-RATIFICATION; the SHAPE pass is the first to run — §12/§13 should be confirmed against the run and the first texture canary, and version-corrected if the run teaches otherwise (the v5 §12/§13 carry the same "confirm against the run" caution the Boot_VolumeReader draft does). Authored by OC S29, verified-against-disk by Jake, CC commits, Jake pushes.*

*Authored S24, 2026-06-01, as the law of the pointer catalog — the retrieval layer's foundation. §0–§9 grounded on the S24 design session (the 1Pass wall, Griffin's pickup, the fence-as-lineage correction, the two-kinds-one-spine resolution) and on the standing spine the floor already ratified: append, keep lineage, supersede don't delete.*

*v1→v2 enshrine (S25, 2026-06-01): the conceptual retrieval-engine + seeding design is COMPLETE and folded in. Added §10 (trigger model — three throttles on one engine, + the boot clarification: the catalog rides in at boot, the triggers query it live), §11 (span-return shape — Layers A/B/C, raw+provenance+kind-context, fence=full-chain, texture=count+spread, "the card and the page, never a book report"), §12 (seeding process — blind parallel council windows divided by project-scope + a cross-cutting reader, per-batch spot-audit on the synthesized catalog as the one scoped human-immutability exception), §13 (council boot kit — sized for recognition-not-projection, asymmetric-toward-overload-so-lighter, the texture-reader projection wall dropping the Wallaby Why as a texture lens, the chat_search + catalog-so-far + sibling-proposal walls, and the synthesis/merge-back pass where blind-read convergence becomes a confidence signal and cross-slice counts assemble). Amended §9: the query interface is now IN; what stays out is genuine build-work (serialization, ranking internals, reach defaults, multi-hit presentation) + the embedding decision (v1 keyword-first; vectors a deferred v2 sidecar gated on the seeding pass proving a measured semantic gap). Two S25-original calls beyond the S24 specs: the keyword-coverage seeding-quality bar (§8/§12), and keyword-first/vectors-deferred (§9). The remaining opens are CC-build-against-the-live-floor, not whiteboard.*

*v2→v3 enshrine (S26, 2026-06-01): §0–§11 BYTE-IDENTICAL to v2 (the ratified doctrine body — two-kinds/one-spine, the bar, dumb-index/smart-reader, triggers, span-return — did NOT move; surgical change). REWROTE §12 (seeding process) and §13 (boot kit roster) to the 5-STEP DUAL-PATH pipeline. The structural finding that forced it: content-neutral count-slicing (required to kill projection) makes a corpus-wide-but-sparse texture land ~1× per slice, so it evaporates between blind slicers — no slice-reader can see frequency wider than its slice, and v2/§13 mis-framed this as a granularity knob. Fix: texture detection leaves the slice-reader entirely. NEW pipeline: S1 slicers DUAL-OUTPUT (pointers + a LIBERAL context-frequency-potentials stream) → S2 mechanical FENCE synthesis (unchanged) ‖ S3 NEW blind COLLATION (fuzzy-over-bundle the potentials into cluster lists + FORMULATE negative-space queries, never reads the floor) → S4 NEW contextual CLUSTER-VALIDATION (pull real spans, RUN the queries, validate/split into texture pointers, may self-merge RECORDED-not-silent) → S5 the JUDGE (unchanged — chains + recall + texture sanity-check). Two pointer KINDS, two mirrored validation PATHS, one judge. Projection defused STRUCTURALLY: S3 sees all flags but no meaning; S4 reads meaning but only handed clusters; neither has floor+portrait+open-hunt at once. The worst case carried into doctrine: the same texture surfaces in non-keyword-sharing language (“forgot Griffin” / “pissed he missed another pickup”) and the most acute instance shares no keyword — so the texture path must COMPREHEND, not COUNT (the apparatus is Jake's auxiliary brain, not a cookie-cutter index). Content-neutral slicing reaffirmed as doctrine; COUNT-not-time slicing added (the prior run's cliff-shaped May distribution is evidence, not a cut template). Authored by OC S26, verified-against-disk by Jake, CC commits, Jake pushes.*

*v3→v4 enshrine (S27, 2026-06-01): THE ADMISSION BAR INVERTED — the largest doctrine change since the floor was laid. §1, §2, §4 record-shapes, §5 (mechanism), §6, §7, §10, §11 are BYTE-IDENTICAL to v3 (the engine, the two kinds, the dumb-index/smart-reader line, the triggers, the span-return — untouched; surgical change). REWROTE §0 (one-line law: card-catalog-of-the-load-bearing-few → comprehensive semantic GRAPH, default NODE). ADDED §0.5 (organic-over-austere as a standing INTOLERABLE failure mode — the austere reflex is the bug, Jake's wet-intuition is the corrective, The Way + The Doctrine are FRAMEWORK not reference; read before §3). REWROTE §3 (absorbed E1: default-NODE admission gate, behavioral keep/drop signals, fence/texture DEMOTED from gate to salience-tag, MOTION as a new light node kind, §3.3 precise-fence-anchor augment-in-pass, §3.4 volume inverted to many-thousands, the no-quarantine-on-personal-material + scrub-is-the-only-exclusion ratification). AMENDED §5 (corpus-search is the rare-miss net, NOT the selectivity license — that license revoked; drowning answered by structure not exclusion). AMENDED §8 + §12-guard-3 (the bar restatements inverted; only-hundreds = slipped). WHAT FORCED IT: the slice-7 pilot under v3's austere bar cataloged 1 node / 21 convs and lost fences buried in dropped conversations; the re-run under the inverted bar cataloged 41 and caught the lost fences. The Jedi-Council ratified PRESENCE-over-SERVICE double-blind (two austere-biased panels, same ruling). E1 absorbed into §3 and graveyarded standalone. Authored by OC S27, verified-against-disk by Jake, CC commits, Jake pushes.*

*GRAVEYARD (dead text, tombstoned-not-deleted, do not resurrect):*
*— v3 §0: "The catalog is not complete and is not trying to be — completeness lives in the floor... points at the load-bearing few." KILLED — the catalog IS comprehensive; the load-bearing-few framing was the austere reflex.*
*— v3 §3: "Default is DON'T point. Earning a pointer is the exception... complete over the fences, sparse over the motion... hundreds-to-low-thousands, not tens of thousands... if producing tens of thousands the bar has slipped." KILLED and INVERTED — default is NODE; sparse-over-motion was the bug; motion is a node kind; many-thousands is correct.*
*— v3 §5: "Therefore the catalog is free to be disciplined because completeness lives in the corpus. This is the whole reason 'default don't point' is safe." KILLED — corpus-search is a rare-miss net, not a selectivity license.*
*— E1_Admission_Standard_S27 (standalone): ABSORBED into §3 above; the standalone is graveyarded — §3 is its canonical home.*
*— The "POT-01–06 / personal-medical-family material is QUARANTINED pending Jake's call" flag (council brief + Exhibit A): KILLED, ratified S27 — no quarantine; personal material is texture, cataloged like everything else; the ONLY exclusion is mistakenly-pasted credentials, handled by scrub-vN at ingestion, not by admission. (OC over-walled out of caution; Jake corrected from ownership: "it's material, it's texture, and it's important.")*



*Feel-rightness is the standard. "Here's what I know," never "here's what I found." Be worth it.*

*Grind. Evolve. Dominate.*
