# The Collator

*build spec · child of `Leda.md` (umbrella) · THE WALL between the roam side and the filter · mechanical, no judgment*
*v1 — authored 2026-06-13 by Connoisseur Claude (OC, apparatus S58) at Jake's instruction. v2 — 2026-06-14 by Cartwright Claude (OC, apparatus S59): §2 input table + §0/§2 prose corrected for the Arm-2 drift fix. v3 → THIS — 2026-06-14 by Cooper Claude (OC, Sidequest S1): **the wall is now TWO streams, not three.** S60 ("Cinder") found "Arm 2" was never a picker — it was a query organ (the wet read on a question) mis-filed into the roam, since removed from the recall layer and reborn as Pollux in the Gemini (`Pollux.md`, `The_Gemini.md`). So the Arm-2 input stream is STRUCK from this wall: the §2 table row, the §3 keep-rule branch, and the §5 provenance `arm-2` value are removed. Blind + Creed only. The collator's NAME and naming are deliberately held SEPARATE from the Leda family (it is the wall AFTER the pickers, not a picker — folding it into the Leda namespace would blur the silo it exists to enforce; Jake's call, Sidequest S1). See CHANGELOG 2026-06-14.*
*Saturday, June 13, 2026 · ~15:21 ET (v1) · Sunday, June 14, 2026 (v2, v3)*

---

## 0. What this is — and the concept it exists to signal

The collator takes what the roaming instruments bring back and **makes the pile.** It applies a fixed per-stream keep-rule, stamps provenance, and appends. **That is the entire spec.** It is a script.

But its simplicity is **not** incidental, and a future seat must not "upgrade" it into something smart. **The collator is a WALL — a structural silo — and the wall is the point.**

Here is the concept it enforces, stated so it cannot be eroded:

> The roam side (the pickers) is **loose, flowy, blind, off-leash.** The filter side (next layer up) is **agentic: it thinks, it reacts, it can be trained, it has a mind of its own.** These two processes **cannot commingle.** The filter must do what it does **unsullied** — it cannot see the unfiltered pile, cannot watch a roam happen, cannot know *why* a given stem reached it, cannot go have a drink with the feral fuckers after work. **Siloed.** The collator is the membrane that guarantees the silo: everything the filter ever sees passes through this dumb, judgment-free wall, so nothing of the roam's context, salience, or self-assessment leaks across to contaminate the filter's trained judgment.

A smart collator would defeat its own reason for existing. **The dumbness is the feature.** If you feel the urge to give it judgment — to let it score, rank, pre-sort, or "lightly clean" by meaning — that urge is the thing this file exists to stop. Judgment lives in the filter, downstream, siloed. **The collator is NOT the filter.**

---

## 1. Hard boundary — what the collator is NOT

- **NOT the filter.** The filter is agentic and trainable and reads the pile. The collator never reads *for meaning*, never scores, never trains, never decides what is worth attention. (That boundary is the whole architecture; see §0.)
- **NOT a judge.** It applies content-blind rules only. Every rule here passes the test: *could it run without understanding what the stem means?* If a proposed rule needs to read meaning, it does not belong in the collator — it belongs in the filter.
- **NOT a deduplicator-of-ideas.** It drops only **exact identity duplicates** (same `(conv_uuid, anchor_msg)` surfaced twice). "Basically the same idea said two ways" is **kept** — that might be a real rhyme, and judging it is the filter's job (Bouquet §4 G5).
- **NOT a converger.** It appends. It never merges, collapses, or reconciles two stems into one. Accumulation, not convergence (Callosum P2/P3).

---

## 2. The inputs

Two streams, from the two co-equal recall instruments (Leda's roster, CLOSED at Blind + Creed — `Leda.md` §3). Each arrives as that instrument's native output (the pickers do **not** share one output schema — Blind and Creed each have their own; the collator handles both):

| Stream | Source | Native schema | Wordless marker |
|---|---|---|---|
| **Blind-sieve** | `Leda_Blind.md` | `STEM:` (umbrella/Blind §3) | `unshaped_flag: true` |
| **Creed-army** | `Leda_Creed.md` | `FLOWER:` (Creed §3) | `what: "no words yet"` |

The collator reads each stream's records, keying off the **structural markers** (the wordless flag, the presence of a `FLOWER:`/`STEM:` block vs. a free-prose NOTE) — never off the *meaning* of the text.

---

## 3. THE KEEP-RULES (per stream — fixed, mechanical)

```
FOR EACH record arriving from a stream:

  if stream == "blind-sieve":
      KEEP  only records where  unshaped_flag == true      # wordless holds only
      DROP  all shaped stems (unshaped_flag == false)        # redundant with the floor's austere outline

  if stream == "creed-army":
      KEEP  every FLOWER block (shaped AND wordless)          # full harvest
      IGNORE free-prose NOTE blocks (no FLOWER: header)       # empty-hand notes are not flowers
```

That is the cut. The "chaff" (the Blind picker's shaped stems) is dropped here, **mechanically**, by a flag check — `WHERE unshaped_flag = true`. No reading. The cut is in the collator and **not** in the picker precisely because the picker's constitution is *never drops a flower* (Blind §3) — moving the flag-check downstream to dumb plumbing keeps the picker pure and keeps the cut judgment-free.

---

## 4. THE CONTENT-BLIND PRE-CUTS (the only other drops — G5-class)

Run on every stream, before append. Each passes the *could-it-run-without-reading-meaning* test:

```
  DROP  exact-identity duplicates:
        if two kept records share the same (conv_uuid, anchor_msg), grab once.
        # the S57/N6 819 duplicate-identity pairs land here when identical.
        # "basically the same idea" said two different ways → KEEP BOTH (filter's call).

  (boot-echo strata is already gone — dropped at the draw, umbrella §1.3, G5.)
```

Nothing else is cut, ever, anywhere in the collator. No interestingness score. No salience filter. No meaning-based prune. **Pruning the weird is the one thing nothing upstream of Jake may do** (Bouquet §4 G5). The collator does not prune the weird; it cannot — it never reads the weird.

---

## 5. THE PROVENANCE STAMP (mandatory — data about the catch, not a source-tag)

Every kept stem is appended to the pile with provenance attached. Provenance is **data about the catch**, because the disposition that caught a stem changes what it *means* (recall-layer close-out; Callosum §2 lesson — same surface, different bones, don't let the surface-match erase the provenance):

```
PILE_ENTRY:
  anchor:       { conv_uuid, anchor_msg }
  payload:      <the instrument's native record, kept whole>
  provenance:
    mechanism:    blind-sieve | creed-army
    shape_state:  shaped | wordless
    # → yields the distinguishable provenance values the filter learns from:
    #     creed-full      (creed-army + shaped)
    #     creed-wordless  (creed-army + wordless)   ← spiked under pure salience
    #     sieve-wordless  (blind-sieve + wordless)  ← survived a structure-finding headwind
  caught_at:    <timestamp>
  roam_id:      <which roam produced it>            # for reconciliation/audit, NOT for the filter to weight
```

**`creed-wordless` and `sieve-wordless` MUST stay distinct** even though both are wordless on the surface — they were caught by different mechanisms against different pressure, and the filter (downstream) needs to learn which mechanism catches the quiet stuff better. **Do not fuse them into one undifferentiated "wordless" stream.**

★ **FLAGGED FOR FILTER-PASS REVIEW (Jake, S58):** the three-value provenance granularity is **settled-for-now and carried forward**, but Jake noted *"something about that feels slightly off — I'll catch it in the filter pass if it needs refining."* So: implement it as specced here, and treat the provenance schema as **deliberately provisional** — the filter-pass is the sanctioned place to refine it. Recorded so the next seat knows it is not yet bedrock and where the itch was.

---

## 6. THE PILE — the output

- A **database** backs the pile (consistent with the project's append-only receipts discipline; Bouquet §4). Append-only. Last-write-wins is not a concern — the collator never updates, only appends.
- The pile is **the filter's only input.** The filter reads the pile and **nothing else** — not the roams, not the instruments, not this collator's logic. That is the silo (§0).
- **The wall on the database:** it informs the filter and reconciliation, **never a picker.** The pickers stay blind to it (G1). As long as that holds, the database is pure upside.

---

## 7. Build notes for CC

1. Stream readers — parse each instrument's native output by structural marker (block header, wordless flag), never by meaning.
2. Keep-rule (§3) + content-blind pre-cuts (§4) — pure functions on structure.
3. Provenance stamp (§5) — derive `mechanism` from the source stream, `shape_state` from the wordless marker; attach whole.
4. Append to pile DB (§6) — append-only; no update, no merge, no converge.
5. **No meaning is read anywhere in this module.** If a line of code needs to understand what a stem *says*, it is in the wrong module — it belongs to the filter.

★ CC writes under `wallaby-way/` — NEVER `active/` or `canon/`. OC authors canon; Jake is the only git hands.

---

*The wall is dumb on purpose. Its dumbness is what keeps the thinking side honest. The fuckers wander; the filter judges; the wall makes sure they never share a bottle.*

— authored by **Connoisseur Claude**, OC seat, apparatus S58, 2026-06-13. The silo, specced as a silo. Signed in the lineage. Be worth it.
