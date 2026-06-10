# APPEND BLOCK → `wallaby-way/tasks/lessons.md` — S51 "Continuance" entries
*Delivered by S51 REF-EDIT, 2026-06-10. The lessons file is not on HEAD (local/gitignored or not yet created) — Jake appends this block to the live local copy, or creates the file with it if none exists. Format per `wallaby-way/CLAUDE.md` §Per-project lessons.*

---

[NEEDS-JAKE: two S50 lessons from the handoff-correction record — that record is not on HEAD; insert the two queued S50 entries above these S51 entries if/when it surfaces.]

## 2026-06-10 — Rate constants, never re-derived
**What happened:** The batch discount got applied twice — twice in one session — producing gate lines at half the real rate.
**Root cause:** The effective batch rates ($1.50/$7.50 per MTok, discount already applied) were re-derived at gate time instead of cited, and the 50% discount was applied again.
**Pattern that prevents recurrence:** Gates print `$1.50/$7.50 per MTok` as NAMED CONSTANTS citing Batch_Read_Spec v1.2 §14 — never re-derived. Runner v1.6 bakes them in as code constants.

## 2026-06-10 — The wrong hand, ×2
**What happened:** Canon edits were routed through CC twice in S51 even though the text was OC-authored verbatim (S42 precedent existed).
**Root cause:** "OC authored it" was read as satisfying the role boundary; the boundary is about which HAND touches canon, not whose words.
**Pattern that prevents recurrence:** Any edit targeting `active/` or `wallaby-way/canon/` ships as an OC-authored FILE to Jake, who lands it. CC never edits those paths. (Now a hard rule in `wallaby-way/CLAUDE.md` — CANON HANDS.)

## 2026-06-10 — A pile count and a session-net count are different units
**What happened:** An expectation of 186 collided with an actual of 377/388 because one number counted the session's net additions and the other counted the pile.
**Root cause:** Two counts with different denominata compared as if same-unit — the floor-counts-carry-their-unit defect class, pointed at the pile.
**Pattern that prevents recurrence:** Every pile/read count states WHICH unit it counts (pile total vs session-net vs files vs convs) before it's compared to anything. Cite FLOOR_COUNTS; never compare bare numbers.

## 2026-06-10 — Run the one-line arithmetic against inherited canon numbers
**What happened:** A canon number (29,175 "convs" for the 6-8-26 export) survived TWO reconciliation sessions unchallenged. Measured truth: 424 convs / 28,836 msgs.
**Root cause:** Nobody ran one-line arithmetic against it — a convs-count that exceeds the floor's own message count should have screamed; the label "convs" was trusted because it was written down.
**Pattern that prevents recurrence:** Inherited canon numbers get a one-line sanity check (does the magnitude survive contact with adjacent known numbers?) at every reconciliation pass — reconcile-don't-inherit applies to ARITHMETIC, not just claims.

## 2026-06-10 — One task in two windows breaks the receipt chain
**What happened:** Two CC instances ran the same task; persists overwrote each other at 05:22:31 (the 176476ae double-fire) — data valid, receipts broken, spend doubled (~$1.71).
**Root cause:** One task in two windows is the dual of two tasks in one window — both destroy the one-task-one-receipt-chain invariant.
**Pattern that prevents recurrence:** One task = one window = one output dir; freshness-check the output dir (<1hr artifacts → HALT) before any paid fire. (Batch_Read_Spec v1.2 §16; `wallaby-way/CLAUDE.md` COLLISION rule.)

## 2026-06-10 — The corpus contains live ignition prompts; the reader obeys payload instructions
**What happened:** Conv f018b1f8 opens with an embedded session-ignition prompt (root human msg, 2,982 B); the reader executed it instead of cataloging — 2 junk fires. RESOLVED via the proven defang path: 1 block cut, end_turn, 17 nodes, $1.55, persisted + harvested (receipt `runs/defang_f018b1f8_S51/`).
**Root cause:** The reader is a model reading text; instructions IN the payload are instructions, and the corpus is full of Jake's real sessions — some of which begin with literal ignition blocks.
**Pattern that prevents recurrence:** Injection is a STANDING read hazard. The persist guard contains the blast radius to quarantine (junk never enters the pile); the remedy is defang-in-working-copy + testcall (Batch_Read_Spec v1.2 §13). Spot-check of 2–3 ignition-led already-piled convs is queued.

## 2026-06-10 — Narrative numbers vs clock-derived numbers
**What happened:** A number carried in narrative drifted from what the actual date arithmetic gives.
**Root cause:** When a date is known, deriving from prose instead of the date imports the prose's staleness.
**Pattern that prevents recurrence:** When a date is known, DERIVE FROM THE DATE — never from the narrative that mentions it. (Sibling of JAKE-RULES §5.2 verify-durations-against-timestamps.)

## 2026-06-10 — Prefix-twin UUIDs transpose, not just hallucinate
**What happened:** The injecting message in f018b1f8 was recorded as `019e64dc-6fbb-73a1-…` — actually the ASSISTANT reply that obeyed the prompt; the real injecting msg is the prefix-twin `019e64dc-6fbb-7fab-b7d7-4484d614fe98` (root human, 2,982 B). The defang HALT caught it before the blade moved.
**Root cause:** Same-millisecond UUIDs share a long prefix; a transposed twin passes every looks-right check that a hallucinated UUID would fail.
**Pattern that prevents recurrence:** Any UUID gating a cut gets role + byte-size verified against the rendered block before the cut executes (the defang HALT, working as built — Batch_Read_Spec v1.2 §13).

## 2026-06-10 — Tombstones name the class, never paraphrase the imperatives
**What happened:** A descriptive tombstone (it paraphrased what the removed ignition block instructed) made the reader half-follow the ghost of the instruction it replaced — mild residue in the f018b1f8 preamble, accepted + documented.
**Root cause:** A tombstone that restates an instruction's content IS that instruction at lower fidelity; the reader obeys text regardless of the frame around it.
**Pattern that prevents recurrence:** Tombstones name the CLASS of removed content ("session-ignition prompt, 2,982 B, cut") — never what it said to do. (Batch_Read_Spec v1.2 §13 tombstone rule; whale_registry class note.)
