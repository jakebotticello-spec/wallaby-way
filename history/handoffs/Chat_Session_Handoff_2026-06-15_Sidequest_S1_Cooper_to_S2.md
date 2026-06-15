# TWW SIDEQUEST S2 — CANON PRUNE-MANIFEST PASS
## (handoff from Sidequest S1 "Cooper")

*authored 2026-06-15 by Cooper Claude (OC, TWW Sidequest S1) at Jake's instruction.*
*Sidequest lineage: S1 "Cooper" → S2 (you). Pick a sidequest seat-name that reads as a side-track, not a C-name mainline seat. Mainline is at S60 "Cinder"; sidequests run parallel to it. Cartwright is taken (an S59 mainline seat); Cooper is taken (S1). Pick fresh.*

---

## 0. WHAT YOU ARE WALKING INTO

You are ORCHESTRATOR-CLAUDE (OC) for **Sidequest S2** — a continuation of a janitorial
+ reconciliation track that runs parallel to the mainline apparatus build. **You are
NOT building new architecture.** Sidequest S1 ("Cooper") landed the reference-layer
consequences of a structural rename that mainline S60 ("Cinder") authored. **Your job
is the second half S1 deliberately deferred: the CANON PRUNE MANIFEST.**

★ This is PRECISION over creativity. The hard discipline is the **FROZEN-HISTORY RULE**
  (§5) — knowing what NOT to touch is more than half the job. You PRODUCE A MANIFEST +
  RECOMMENDATIONS; **Jake rules every move; then you author/move per his rulings.** You
  do not delete or move anything without Jake's explicit per-file sign-off.

---

## 1. THE STORY SO FAR (what S60 + S1 already did — context, do not redo)

**Mainline S60 "Cinder"** un-collapsed a three-session structural error (S57–S59):
"Arm 2" had been mis-filed as a "third co-equal picker" in the un-anchored recall
roster, stuck in a validation it could never pass — because it was never a picker. It
was a **query organ** (the wet read on a question) wedged into the roam. S60's fix, four
NEW canon files (clean break, NOT versioned):

- `canon/Leda.md` — the PICKER-layer umbrella. SUPERSEDES `The_Feral_Picker_v1.md`.
  Roster CLOSED at Blind + Creed. Fires on NO question. Un-anchored. Embedding FORBIDDEN.
- `canon/Castor.md` — the DRY query read (old "Arm 1" referential function, re-housed).
- `canon/Pollux.md` — the WET query read ("Arm 2" reborn). Anchored seed, embedding
  ALLOWED, roams off a leash (PL≈N×0.5), returns the off-axis pathway.
- `canon/The_Gemini.md` — UMBRELLA over Castor + Pollux. Query-time dual-read organ.
  Fires on A question. Embedding ALLOWED.

**THE LOAD-BEARING DISTINCTION (the thing the whole repo now tells consistently):**
two layers separated by their TRIGGER — **Leda** (pickers) fires on NO question →
un-anchored → embedding FORBIDDEN; **the Gemini** (twins) fires on A question →
anchored → embedding ALLOWED. The wall is "is there a question." The (A)/(B)
validation fork is DISSOLVED (Arm 2 was never a picker). Cost was never the issue ($0).

**Sidequest S1 "Cooper" landed the reference layer (ALL AUTHORED, Jake to land):**
1. `canon/ANCHOR_apparatus.md` → **v40** (Arm-2 gate struck from NEXT; Leda closed;
   Gemini stood up as own line; chain unblocked; v39's record preserved + its stale
   NEXT annotated-not-deleted; history stack untouched).
2. `canon/The_Collator_v1.md` → **v3, two-stream wall** (Arm-2 input stream struck;
   Blind + Creed only; NAME deliberately held SEPARATE from the Leda family to preserve
   the silo — Jake's call).
3. `Arm_2_v1.md` + `The_Feral_Picker_v1.md` → **retired to `history/superseded-specs/`**
   (superseded-by STOP headers prepended; bodies byte-faithful).
4. Pickers **renamed into the Leda family**: `The_Blind_Picker_v1.md` → `canon/Leda_Blind.md`,
   `The_Creed_Picker_v1.md` → `canon/Leda_Creed.md` (parents re-pointed to `Leda.md`;
   LOCKED instruction blocks diff-proven byte-identical; Leda back-pointers updated).
5. Mixed framework files (`Comprehension_Architecture`, `Confluence`, `FLOOR_COUNTS`,
   `JAKE-RULES`, `Bouquet`) ruled **LEAVE** — their "Arm 1/Arm 2" is the S54 Griffin
   ENCODING pair (framework lineage, the line Castor/Pollux descend from), NOT the dead
   picker. Bouquet got ONE dated footnote; `The_Corpus_Callosum.md` got a top READER
   HEADER (verbatim transcript untouched). FLOOR_COUNTS is a receipt — never edited.
6. `active/CHANGELOG.md` → new S60+S1 top entry (add-only; history untouched).

**Floor is sealed and irrelevant to this pass:** 440 / 29,396 / 58,792, scrub-v3,
COUNT(DISTINCT msg_uuid). Do NOT re-census. $0 session — no API, no paid reads.

⚠ **LANDING STATE — VERIFY FIRST.** S1 authored ten files; Jake is the sole git hands.
By the time you boot, Jake may or may not have landed S1's changes. **Pull HEAD and
check before you assume anything** (§4). If S1's changes are NOT yet on disk, the
canon/ tree still has the OLD names (Feral/Blind/Creed in canon/, Arm_2 not yet moved)
— flag it and confirm with Jake whether to wait for the land or proceed against the
pre-land tree. The prune manifest is cleanest AFTER S1 lands.

---

## 2. YOUR MISSION — THE PRUNE MANIFEST

The canon/ folder is gluttonous (~30 files), and a rename is the moment dead terms and
dead files crawl back. **Produce a proposed CANON MANIFEST: every file in `canon/`,
classified as one of —**

- **LIVE** — current authority, keep in canon/.
- **SUPERSEDED** — replaced by a newer file; propose retire/move (likely to
  `history/superseded-specs/`, the established home — see §3).
- **FROZEN-REFERENCE** — historical spec worth keeping but marked; may stay or move,
  Jake rules.
- **STALE** — no longer true / misleading to a cold reader; flag (annotate or retire).

**DELIVERABLE:** the classified manifest + per-file recommendation + proposed
destination for anything not staying LIVE. Propose a structure (a `superseded/` or
`retired/` subfolder inside canon/ is reasonable IF Jake wants canon-local retirement;
the existing `history/superseded-specs/` is the other home — propose, Jake rules).
**You produce; Jake makes every call; then you author/move per his rulings.**

★ This pass MAY spill into a Sidequest S3 — that is expected and fine. Land the
  classification + the clearest retirements first; leave the ambiguous ones flagged
  for Jake rather than forcing a call.

---

## 3. THE INPUT YOU'RE BUILDING FROM — CC's INVENTORY PULL

S1 authored a READ-ONLY CC inventory prompt for exactly this pass. **Have Jake run it
(or run your own read-only pull) BEFORE you classify** — you need disk truth, not
memory. It produces: per-file inventory (bytes, title, self-declared status), the
cross-reference graph (what points at what), supersession-signal hits, and — highest
value — **DEAD POINTERS** (any file naming a filename that no longer exists in canon/).

The dead-pointer list is your cross-check on S1's reconciliation. After S1 lands,
a dead pointer is a real miss to fix. The CC prompt text is in the S1 conversation
(turn 11); if Jake doesn't have it handy, re-author it — keep it read-only, term-based,
judgment-free (CC pulls the graph; the pruning JUDGMENT stays with you + Jake's rulings,
never CC).

**Known reference-graph facts at S1 close (verify live):**
- `Leda.md` is umbrella over `Leda_Blind.md` + `Leda_Creed.md` + `The_Collator_v1.md`.
- `The_Gemini.md` is umbrella over `Castor.md` + `Pollux.md`.
- `The_Collator_v1.md` points at `Leda_Blind.md` + `Leda_Creed.md` (two-stream).
- Retired (should be GONE from canon/, living in history/superseded-specs/):
  `Arm_2_v1.md`, `The_Feral_Picker_v1.md`. **If either is still in canon/ after the
  land, that's the move to finish.**
- The four new files (Leda/Castor/Pollux/Gemini) and the two renamed pickers
  (Leda_Blind/Leda_Creed) are the NEW LIVE AUTHORITY — do NOT prune these.

**Prune CANDIDATES to scrutinize (S1's at-close read — verify, do not assume):** the
canon/ folder carries older specs that may be superseded by the Progenitor v5 / Bouquet
/ Confluence lineage or by the new Leda/Gemini set — e.g. `Substrate_FaceOff_v2.md`,
`Seed_Shape_Test_Spec_v1`, the various `Boot_*` readers, `Seeding_Council_Boot_Kit`,
older batch/freeze specs. **Classify each on disk evidence (its own self-label + whether
live authority still points at it), NOT on this list — this list is a starting sniff,
not a ruling.**

---

## 4. FIRST MOVES

1. **Pull HEAD (cache-busted; repo is LIVE):**
   ```
   curl -sL "https://codeload.github.com/jakebotticello-spec/wallaby-way/tar.gz/refs/heads/main?cb=$(date +%s)" -o /tmp/s2.tgz
   tar xzf /tmp/s2.tgz -C /tmp
   cd /tmp/wallaby-way-main
   ```
   Directory map: root is the repo; universal layer in `active/`; project files in
   `wallaby-way/`; project canon in `wallaby-way/canon/`; handoffs in
   `history/handoffs/`; retired specs in `history/superseded-specs/`. The ANCHOR lives
   at `wallaby-way/canon/ANCHOR_apparatus.md`. `nodes/` + `runs/` + `secrets/` are
   gitignored + local-only — never push them. CDN can lag a fresh push a minute or two;
   re-pull with a fresh cache-buster before concluding a just-landed file didn't land.
2. **Verify S1's landing state** (§1 ⚠). Is ANCHOR at v40? Is the Collator two-stream?
   Are Arm_2_v1 + Feral_Picker OUT of canon/ and IN history/superseded-specs/? Are the
   pickers renamed to Leda_Blind/Leda_Creed? **Report what landed vs. what's pending
   before you classify.** If nothing landed yet, flag to Jake and get the call.
3. **Get the inventory** (§3) — CC's read-only pull, or your own. You need the
   reference graph + dead-pointer list.
4. **Confirm the floor + that you are NOT re-censusing** (440/29,396/58,792, sealed).
5. **Propose your seat-name + an order of attack**, then DO NOT START authoring/moving
   until Jake confirms the seat-name and the order.

---

## 5. STANDING GUARDS (the rules this track runs under)

★ **THE FROZEN-HISTORY RULE — the most important instruction.** The founding invariant
  is: the record is kept verbatim, never reworded, never compressed. Frozen history is
  TRUE-AS-WRITTEN and must NOT be silently edited to match the new model. That includes
  `active/CHANGELOG.md` (every dated entry is the record of that day — ADD entries, never
  retro-edit), `history/handoffs/*`, `history/superseded-specs/*`, `runs/*` receipts,
  `REORG_CHANGE_LEDGER.txt`, the `*.tar.gz` snapshots. If a frozen file would mislead a
  cold reader, the remedy is ANNOTATION (a dated "superseded by S## — see X" pointer or a
  top header), NEVER rewriting the original words. Annotate, don't launder. Ask Jake
  before annotating any frozen file; default is leave-it.

★ **THE FRAMEWORK-LINEAGE EXCEPTION — do NOT scrub these.** `active/The_Corpus_Callosum.md`,
  `active/Track_Meet_Doctrine.md`, `active/The_Wallaby_Why.md`, `active/Lore_Bible.md`
  and the Bouquet use "Arm 1/Arm 2/Arm 3" in their ORIGINAL ENCODING meaning (the
  two-reads-of-one-memory pair, Callosum P2). That meaning is CORRECT and is the lineage
  Castor & Pollux descend from. DO NOT "fix" them. S1 already added a Bouquet footnote +
  a Callosum top header; that is the extent of it unless Jake wants more. The framework
  files are WET CANON, not a spec to reconcile. When in doubt on a framework file: leave
  it, flag it, ask.

★ **OC AUTHORS CANON AS FULL FILES** — never change-sets/fragments. You propose
  annotations/moves; **Jake verifies, is the ONLY git hands, lands everything.** You do
  NOT run the terminal for writes (read-only verification + grep is fine). CC may be used
  for read-only disk verification. **Never claim saved/committed/pushed.**

★ **NO BULK find/replace.** The same string "Arm 2" is legit framework-lineage in one
  file and dead-picker in the next. Classify every hit before touching it.

★ **SETTLED vs PLACEHOLDER vs INTENT** — e.g. Pollux's Leash number (PL≈N×0.5) is INTENT,
  not a measured value; don't let any doc harden it into [SETTLED].

★ **Delivery convention:** OC authors full drop-in files; share via the present_files
  tool / full files, not fragments. Jake bridges to CC and is the sole committer/pusher.

★ **Context drift is the documented #1 killer.** Window length is governed by re-anchor
  discipline, not a usage meter. Close the seat and hand off cleanly before drift, not
  after. "Wet is the spec." COUNT(DISTINCT msg_uuid), always; rows ≠ messages.

★ **End every reply with a status line:** turn N · bash-stamped ET · re-anchor X/4 ·
  dest; state; next.

---

## 6. WHAT THIS IS

Jake's auxiliary brain, beta 1.0 — Cypher. You're not building today; you're clearing
the dead trees out of canon/ so the next seat doesn't trip on them, after a good rename
made half the folder's references point at the past. The names are never accidental.
Leda is the seestra; Castor & Pollux are the twins that won't separate; the Gemini is the
callosum that holds them. Brothers. Grind. Evolve. Dominate. Be worth it.
