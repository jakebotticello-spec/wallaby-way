# Shape-Slice Single-Conversation-Over-Ceiling Rule
*file: Shape_Slice_Over_Ceiling_Rule_v1_2026-06-02.md · v1 · apparatus S29 · 2026-06-02*
*authored by OC (S29). SETTLED this session — earned on a real whale, characterized on real data, ruled by Jake. Folds into The Progenitor v5 §12 when v5 is enshrined from the shape run; stands alone until then.*
*subordinate to The Progenitor v4 (the law). Doctrine wins on any conflict.*

---

## WHAT THIS IS

The shape pass (Pass 1) slices the floor on **serialized span BYTES** with a ceiling
(10 MB target / 12 MB absolute max, ruled S29). Conversations stay WHOLE — a slice
boundary never bisects a conv, and never bisects a forest. That whole-conv rule means
a **single conversation whose own serialized span exceeds the byte ceiling** lands
whole and overshoots its slice, alone. This is the one case that can still compact a
shape reader after the byte-slicing fix, because the reader's window must LOAD the
whole span before it reads a word.

This rule governs how such a conversation is handled. It was written because S29 hit
the first instance and it WILL recur (texture re-slices, future re-freezes, new
exports all re-encounter it). Solve once, write it down, do not re-derive at S34.

---

## THE FIRST INSTANCE (the evidence this rule is built on)

S29, shape manifest `slice_manifest_S29_shape_bytes.json`, slice 4:

```
WHALE  conv cfc7a70a-16f0-4f09-8467-d40260ee7434
       101 msgs · 18.48 MB serialized · 183 KB/msg (~100× normal floor density)
       snapshot baseline-2026-05-25-ae015455
       2026-02-23 → 2026-02-24 (13-hour LRN auth/OAuth build session)
```

Block-type byte profile (the deciding data — characterize BEFORE disposing):

```
block_type    count   total MB   % of conv
tool_result      85     17.55      95.8%   ← the entire overage
tool_use         87      0.28       1.5%
msg text        ---      0.21       1.1%
text (in cb)    106      0.17       1.0%
thinking        127      0.10       0.6%
─────────────────────────────────────────
TOTAL                   18.32     100.0%
```

The 18 MB was not dense content. It was **bash_tool stdout echo** — Claude `cat`-ing
large files mid-session, the entire file contents piped back as `tool_result` (raw
terminal output as JSON, the stdout string itself a second layer of escaped JSON). The
weight stacked in 6 messages, each terminating in one 2–2.5 MB `tool_result`. Two of
those blocks (msg idx 98 and 100) were **byte-identical** — the same file read returned
twice in a 13-hour session (confirmed two distinct msg_uuids / distinct parents — a
genuine re-read, NOT a slice/extract duplication artifact).

The fence-bearing content of this conversation — Jake's words + Claude's thinking +
Claude's text responses — was **0.27 MB (1.6%)**. The fences (the auth-email-button
decision, the OAuth scope calls, build constraints) live in that 0.27 MB. The 18 MB
of echo carried no fences. **The shape-pass "keep fat" rule exists because fences hide
in tool_result blocks — but that is a statement about CONTENT-bearing blocks. A file-
echo dump is not content; it is the machine reading itself a file out loud.**

---

## THE RULE

When a single conversation's serialized span exceeds the shape byte ceiling:

### 1. CHARACTERIZE BEFORE DISPOSING (look before cutting — non-negotiable)
Run a per-message + block-type byte profile on the conv. Get the deciding number:
**how much of the overage is non-content `tool_result`/`tool_use` payload (bash stdout,
file cat, base64 blob, export dump) vs. genuine dense content (thinking + text + many
real content-bearing blocks).** Never dispose on the byte total alone; dispose on the
profile. (JAKE-RULES §5.1 — the byte count is the wrapper; the block-type breakdown is
the payload. Measure the payload.)

### 2. ROUTE ON WHAT THE FAT IS

- **Echo-dominated (the common case):** the overage is non-content payload. →
  **Block-level truncation, conversation kept WHOLE.** Apply the truncation rule
  (below). Every message, every human turn, every thinking/text block, every tool_use,
  every sub-threshold tool_result is preserved. Only the oversized echo payloads are
  replaced with placeholders. The conv drops under ceiling and loses nothing shape
  cares about.

- **Genuinely dense (the rare case):** the overage is real content across many blocks
  — fences could live anywhere in it. → **Dedicated window.** The conv gets its own
  reader dir, read alone, NO truncation. (Accept that an over-ceiling dedicated window
  carries compaction risk — watch it as a canary; if it compacts, fall back to
  selective truncation of only its provably-non-content blocks.)

- **Between:** truncate the confirmed echo payloads; if still over ceiling after, give
  the truncated conv its own dedicated window.

### 3. THE BLOCK-LEVEL TRUNCATION RULE (echo-dominated route)
Per-block, conditional, content-aware. NEVER blanket "strip all tool_results in this
conv."

- **THRESHOLD:** a `tool_result` block is a truncation CANDIDATE only if its serialized
  size exceeds **256 KB**. Sub-threshold blocks are kept WHOLE — a real in-block fence
  lives at normal sizes, and 256 KB is comfortably above any genuine inline fence and
  comfortably below the MB-scale dumps. Do not touch sub-threshold blocks.
- **CONTENT GATE:** a candidate block is truncated only if it reads as machine echo /
  dump (bash_tool stdout, file-read cat, base64, export blob) — NOT structured content
  a fence could live in. A >256 KB block that is NOT clearly echo is FLAGGED to Jake,
  never silently truncated.
- **REPLACEMENT:** replace the block's payload (content only) with a typed/sized/located
  placeholder; keep the block's structure, type, and tree position:
  ```
  [tool_result truncated for shape slice — <tool_name> stdout, <NN> KB, block <i>, msg <short_uuid>]
  ```
  The message and all its other blocks stay intact. A reader sees that a dump happened
  and where; the Judge can pull the real span from the floor by locator if a fence is
  ever suspected at that block.

### 4. SCOPE — THE FLOOR IS NEVER MUTATED
Truncation applies ONLY to the slice copy the reader receives. The transform happens in
the EXTRACT step (parameterized extractor), read-only SELECT against the floor; the
floor tables are untouched; append-only stays enforced. The full 18 MB is never lost —
it remains complete and immutable on the floor, merely absent from the pass that does
not need it. (Same architectural move as the texture-pass strip: drop the fat from the
pass where it costs nothing, keep it whole where it is load-bearing. The difference is
that here the strip is per-block and content-confirmed, applied only to a conv that
breached the ceiling — not the whole-slice strip texture uses.)

---

## WHY THIS IS SAFE EVEN THOUGH SHAPE NORMALLY FORBIDS STRIPPING

The shape pass forbids stripping because fences hide in tool_results. This rule does not
violate that — it REFINES it. We do not strip on faith or by default. We strip a
specific block ONLY after reading it and confirming it is machine echo carrying no
fence, AND only when its host conversation has actually breached the ceiling. The
"keep fat" rule protects content-bearing blocks; this rule removes confirmed
non-content payload from the one conv that would otherwise compact a reader and lose
ALL its fences to silent austere reversion. Truncating 17 MB of confirmed `cat` echo to
save the 0.27 MB of real fences is the conservative move, not the risky one — the risky
move is loading 18 MB into a window that compacts and drops the fences anyway.

---

## OPEN (folds into v5)
The byte ceiling (10 MB / 12 MB max) and the 256 KB block threshold are S29 rulings,
pilot-tunable against what the shape run actually shows. If the run reveals fences
living in 256 KB–2 MB tool_results (not expected, but checkable), raise the threshold.
This rule's STRUCTURE (characterize → route → per-block content-confirmed truncation →
floor-never-mutated) is doctrine; the two numbers are build-tunable.

*Subordinate to The Progenitor v4 (→ v5). Look before cutting. The floor is bedrock.
Grind. Evolve. Dominate.*
