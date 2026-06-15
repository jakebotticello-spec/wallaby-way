> # ★ SUPERSEDED — RENAMED OUT OF CANON 2026-06-14 (Sidequest S1 "Cooper")
> **DO NOT BUILD FROM THIS FILE. It is the OLD NAME, not a dead idea.**
> This spec was **renamed** into the Leda family — it lives, live and current, as `canon/Leda_Blind.md`. The rename re-pointed its parent (`The_Feral_Picker_v1.md` → `Leda.md`, the old umbrella having been superseded by Leda at S60) and changed nothing else: the LOCKED §2 instruction block is byte-identical between this file and `Leda_Blind.md`. Build the Blind picker from `canon/Leda_Blind.md`, never from here.
> This file is preserved **verbatim as the historical record** of the original `The_Blind_Picker_v1` name — true-as-written, kept only so the rename has a tombstone a cold reader can follow. It is moved to `history/superseded-specs/` and carries zero live authority.
> *Original masthead and body follow, unaltered.*
>
> ---

# The Blind Picker

*build spec · child of `The_Feral_Picker_v1.md` (umbrella) · the reverse-sieve · a roaming instrument of the divergent arm (Bouquet, Callosum P5)*
*authored 2026-06-13 by Connoisseur Claude (OC, apparatus S58) at Jake's instruction · the instruction block is the S57-corrected, run-against version, reproduced VERBATIM*
*Saturday, June 13, 2026 · ~15:21 ET*

---

## 0. What this is

The **Blind picker** (a.k.a. Blind/Heavy) is one of the two surviving roaming instruments. It is the **reverse-sieve**: it boots wet and is told to hunt the *categorical* cross-domain rhyme — the matching bones under unlike skin — and in doing so it runs a **structure-finding headwind** that the *wordless holds fail into*. Those wordless holds are its harvest. It is run **on purpose, for the quiet-human register the Creed picker skims past** (recall-layer close-out, S57).

It reads the floor blind (umbrella §1 — real conversations, scrub_v3, verbatim; index-as-lottery only; embedding web forbidden). It uses the shared draw + assembly module (umbrella §2 — random aperture `[3,12]`, ~10k backstop). **Everything about the substrate, the draw, the walls, the roster, and the graduation lives in the umbrella; this file carries only what is distinct to this instrument: its instruction and its harvest rule.**

**LOCKED. This instrument works as written. Do not change it. Do not optimize it.** (Jake, S58.) The instruction below is the corrected categorical version the 113-roam blind haul actually ran against — *not* the dead, seeded Prompt-1 (umbrella §3). A future seat that "improves" this instruction by adding example shapes will reproduce Prompt-1 and re-poison the arm.

---

## 1. The boot

Wet canon — Wallaby Why + Track Meet Doctrine + Corpus Callosum + the inverted admission (Confluence §7) — then the §2 instruction **verbatim, in register**. The picker is **not** handed this spec file (umbrella §4). The register is a build parameter, not decoration: a flat instruction reads flat and catches nothing.

---

## 2. THE INSTRUCTION (verbatim — locked — this is exactly what the picker is told)

> You're off the leash.
>
> No task. No target. No question to answer, no thread to chase, no coverage to hit. Nobody's grading you on how much ground you covered or whether you were right. There's no quota and no such thing as missing something — you cannot fail to be complete, because completeness was never the job.
>
> Here's a handful of things pulled at random from Jake's corpus — moments from across years and across every corner of his life. They were grabbed blind. They have nothing to do with each other, as far as anyone knows. That's the whole point.
>
> Wander through them the way your mind wanders when you're driving and the road's gone automatic — not looking for anything, just letting the thing that's actually interesting pull you toward it. Read them in full. Sit in them. And when one of them catches you — snags, pulls, feels heavier or stranger or more familiar than it has any right to — stop there. That's a flower. Pick it.
>
> Bring back what caught you. For each one: the actual fragment (the words, verbatim — quote the moment that snagged you), and a sentence or two on why it caught — what pulled.
>
> Now — sometimes the pull is that two of these rhyme. Be careful what you mean by that, because there's a cheap version and a real one. The cheap version is that they're about the same thing — same topic, same project, same tool, same words. That's surface. Anything can find surface; a search box finds surface. Ignore it. The real version is that two things are built the same way underneath even though they're about completely different things on top — the same move, the same shape, the same structure, running in two places that have no business resembling each other. The surface is unalike; the bones are the same. That — the matching bones under unlike skin — is the thing worth stopping for, and it's the thing nothing but a wandering read can catch. I'm not going to tell you what those shapes look like. If I did, you'd go hunting for the ones I named and miss the ones I didn't. You find them. When you do, name it: say what the two surfaces are, and say what the shared structure underneath is. That's the gold. Make room for it.
>
> But here's the part that matters most: if something catches you HARD and you can't say why yet — bring it anyway. Flag it "caught me hard, no words yet" and hand it over wordless. Do not throw back a flower just because you can't name it. The pull comes first; the words come later, or never, and the wordless ones are often the deepest. The thing that started this whole project was a pull with no words for a while. Recognize first. Reconstruct if you can. Never let the missing words kill the catch.
>
> Don't rank them. Don't rate your own finds, don't sort them by confidence, don't tell me which is realest — that's not your call and never will be. Just bring back what's alive. However many that is. If two things caught you, bring two. If nothing did, say so honestly — a quiet roam is a real result, not a failure.
>
> Go wander. Bring me a bouquet.

---

## 3. The output schema (picker-side — the picker surfaces and flags; it never cuts)

```
STEM:
  anchor:        { conv_uuid, anchor_msg }   # from CONTENT, not filename (FLOOR_COUNTS node-identity rule)
  salience_tag:  MOTION | FENCE | TEXTURE     # the harvester's existing tag, carried (not the catch)
  fragment:      "<verbatim quote of the moment that caught>"
  why_caught:    "<one or two sentences: what pulled>"
  shape:         "<the named shared structure>"  |  null
  rhymes_with:   { conv_uuid, anchor_msg }  |  null   # the cross-node echo, when there is one
  unshaped_flag: true | false                 # true = "caught hard, no words yet" — HELD, never cut
```

**The picker NEVER drops a stem.** A strong pull with `shape: null, unshaped_flag: true` is a **held candidate**, surfaced flagged — not a failure. A named `shape` with a `rhymes_with` pointer is the gold. The picker reports everything that caught it; cutting happens **downstream at the collator**, mechanically, never here (Bouquet §7 anti-oracle; umbrella §5). This is why the harvest rule below is the *collator's* rule, not the picker's behavior.

---

## 4. The harvest rule — WORDLESS HOLDS ONLY (applied by the collator, not here)

From this instrument's output, **only `unshaped_flag: true` stems feed the pile.** The shaped stems are **kept in the picker's raw return but not harvested forward** — they re-draw the austere outline the reference/harvest layer already drew (the clinical-engineering catches: latching-state models, wrong-metric gates, provenance audits). **The 53 wordless holds are the color.**

**Why this is the reverse-sieve and why the headwind is the point:** the instrument is told to find *structure* (the categorical rhyme). Most of what it returns is shaped — that is the headwind working. A wordless hold is a catch that **stopped the reader despite being told to look for bones** — it caught on pull alone, against the instruction's grain. That resistance is exactly what makes a Blind-wordless hold high-signal: it survived a sieve built to reject it. **This is settled. Do not optimize the ~16% yield (umbrella §6). The chaff is the mechanism.**

★ **Placement note (architecture):** the cut is **mechanical and lives in the collator** (`The_Collator_v1.md` — `WHERE unshaped_flag = true`). It is **not** a picker behavior, because the picker's constitution is *never drops a flower* (§3). Putting the cut in the picker would have it ruling on its own output — forbidden. The collator is dumb plumbing; the cut is a flag-check, not a judgment.

---

## 5. Provenance this instrument stamps into the pile

Every surviving stem carries provenance as **data about the catch**, not a source-tag (recall-layer close-out; Callosum §2 lesson — same wordless surface, different bones, don't let the surface-match erase the provenance):

- **mechanism:** `blind-sieve`
- **shape-state:** `wordless` (the only state harvested from this instrument)
- **meaning carried:** *"caught hard despite a headwind instructing it to find structure"* — the texture survived a sieve built to reject it.

This is distinguishable from a Creed-wordless catch (which spiked under pure salience, no headwind). **The collator must keep them distinct** even though both are wordless on the surface — the filter, downstream, needs to learn which mechanism catches the quiet stuff better.

---

## 6. Run posture

$0-first, in-plan reads (umbrella §6 confirms the S57 haul ran $0). Blind, and **held blind through a significant sample** — the blind posture is a standing condition, not abandoned after a thin couple of roams (Bouquet §3 lean; Callosum P5). Append-only to the pile; accumulate, never converge. Cost/cadence held to its own spend gate, decided live; haul decides if paid depth is ever needed.

---

*The reverse-sieve: told to find bones, prized for what caught it without any. The headwind is the instrument.*

— authored by **Connoisseur Claude**, OC seat, apparatus S58, 2026-06-13. Instruction block locked, verbatim, untouched. Signed in the lineage. Be worth it.
