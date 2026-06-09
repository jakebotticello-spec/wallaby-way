# The Wallaby Whales
*file: The_Wallaby_Whales_2026-06-03.md · v1 · apparatus S32 · 2026-06-03*
*authored by OC (S32, "Conductor"). The wall-delivery apparatus: how an over-ceiling conversation reaches the shape reader without breaking it, and without ever touching the floor.*
*subordinate to The Progenitor v5 (the law). Doctrine wins on any conflict.*
*This file CONFIRMS and DEPLOYS `Shape_Slice_Over_Ceiling_Rule_v1` (S29) in the deterministic-API / token-ceiling world S32 proved. The over-ceiling rule's STRUCTURE was right on paper; S32 ran it against four real whales and the live API and updated its NUMBERS and its MECHANISM. Append, supersede-don't-delete: the S29 rule stands as the origin; this file is the next link in its chain.*

---

## WHAT THIS IS (one paragraph)

A small number of conversations in the corpus are **whales** — single conversations whose serialized size exceeds the reader's context ceiling, so they cannot be sent whole. S29 predicted this ("the one case that can still compact a reader") and wrote the rule for handling it. S32 confirmed it for real: fired the corpus's largest conversations at the live API and found four that blow past the 1M-token ceiling, all for the same reason S29 characterized on the first whale — **massive `tool_result` echo** (the machine reading files out loud to itself). This file records the confirmation, fixes the measurement model S29 couldn't have known was off, and specifies the **dissection-table** mechanism: a whale is lifted to a working copy ABOVE the floor, the confirmed echo is stripped from the COPY by an audited classifier, and the reduced copy is what the reader mines. The floor is never touched. The atlas keeps its dead-language volumes on the shelf, untouched and immortal; we photograph the one living page and read the photograph.

---

## THE CONFIRMATION (S32 — the evidence this file is built on)

### The two-path reality
S32 fired real conversations at the deterministic Claude-API shape reader (Opus 4.8, 1M-token window, GA — no beta header). Two outcomes, now both proven:

- **FITS-WHOLE (the common path):** the conversation is sent whole, read in one deterministic pass, nodes emitted. **Proven clean to ~930k tokens** — `492e164b` (203 msgs, 930,752 input tokens) completed `end_turn`, 47 nodes, 0 drops, tail noded as richly as head. The fits-whole path is validated to within 70k of the ceiling.
- **OVER-CEILING (the whale path):** the conversation exceeds the 1M ceiling and cannot be sent whole no matter what. Must be REDUCED (echo-stripped) before sending. Four such whales measured (table below).

### The four whales (measured, S32)

```
rank   conv        msgs   actual tokens   ratio over est   result        disposition
1      cfc7a70a    101     4,400,000      2.2× over est    OVER (4.4×)   whale — strip path
2      83506215    173     3,000,000      3.3× over est    OVER (3.0×)   whale — strip path
3      55217328    303     2,200,000      3.2× over est    OVER (2.2×)   whale — strip path
4      d9d05961    441     1,200,000      1.6× over est    OVER (1.2×)   whale — strip path
—      492e164b    203       930,752      —                FITS ✓        fits-whole (validated ceiling)
—      d6e23963     56       485,766      0.78× of est     FITS ✓        fits-whole (first gate, clean)
```

(`cfc7a70a` is the same whale S29 characterized at 18.48 MB / 95.8% tool_result echo — now measured at 4.4M tokens, confirming it as the corpus's largest. It remains the canonical worst case and the right canary for the strip path.)

### The measurement correction (what S29 couldn't have known)
S29 sliced and ceilinged in **serialized BYTES** (10 MB target / 12 MB max). S32's first instinct — estimate tokens from a character count — was wrong by **2–3.3×** on every echo-heavy conv. Why: bash/tool stdout echo is **double-escaped JSON** (the stdout string is itself escaped JSON, sitting inside the message's escaped-JSON content field), and double-escaped text tokenizes far more densely than prose. A char-count proxy badly *under*-counts exactly the conversations most likely to be whales. **The ceiling axis is TOKENS, measured authoritatively, not bytes and not a char proxy.** (`d6e23963` is the tell in the other direction: it was the largest by JSON bytes but came in UNDER its char estimate, because it is genuine dense content with modest tool blocks — real content tokenizes *more* efficiently than echo. Bytes lie in both directions; tokens are the truth.)

### What this does NOT change
The fits-whole path is the rule and the whale path is the rare exception — exactly as S29's "keep fat / fences hide in tool_results" instinct intended. A whale is rare (4 measured across 325 convs). Echo-strip remains **last-resort, not pipeline-default** — it earns its place only on a conversation that has actually breached the ceiling. On a normal conversation it recovers almost nothing and must not run.

---

## THE DISSECTION TABLE (the mechanism — floor never touched)

The whale problem is "how do we read content trapped inside a conversation too big to send." The answer is NOT to mutate the floor, and NOT to send the floor's bytes through a stripper. It is:

1. **The floor IS the cold storage — already.** Every whale is preserved verbatim, immutable, append-only-enforced, on the floor. That is what the floor is for. A whale needs no "copy to preserve it" — it is already the most preserved artifact we own. Do not write copies INTO the floor; writing anything into the floor is the exact move the `floor_immutable_guard()` exists to refuse, and we never carve an exception into it. The shelf stays sealed.

2. **Lift a working copy ABOVE the floor.** A read-only SELECT pulls the whale off the floor and writes a verbatim working copy to a working directory (`pipeline/whales/`), never to the floor. This copy is the cadaver on the dissection table — the thing we are allowed to cut. The original on the floor is untouched and remains the record.

3. **Strip the COPY with an audited classifier (see below).** The strip removes only confirmed machine-echo, emits an audit manifest (the receipt), and produces a reduced copy that fits the ceiling.

4. **Mine the reduced copy.** The reduced copy is sent to the same deterministic shape reader as any fits-whole conversation. The nodes it produces anchor by `msg_uuid` back into the floor — so a future reader following a node lands on the WHOLE message on the immutable floor, echo and all. The strip affected only the reading pass; the record the nodes point at is complete.

**The floor is bedrock. The dissection happens on a table we carried into the room. Nothing bleeds on the carpet.**

---

## THE WHALE REGISTRY (the index card)

A plain file in the repo (NOT the floor): `pipeline/whales/whale_registry.md`. Lists every over-ceiling conversation — `conv_uuid`, slice, message count, actual token count, source path, disposition. This is the "these volumes are in the dead language; handle them via the strip path, not whole" index. It is built by measurement (fire/measure the candidates), appended-to as new whales surface (re-freezes, new exports, texture re-slices will find more), and version-controlled. The registry is authority for "is this conv a whale" so the pipeline never re-measures a known whale from scratch.

---

## THE AUDITED, HARDENED STRIP (the gate the stripper must pass before it cuts anything mined)

The strip is the one dangerous step in the whole apparatus: a classifier deciding per-block "this is junk echo, delete" vs "this is content, keep." Get it wrong and it deletes a real deliverable (a code-as-artifact block, a fence) silently — the worst failure mode, because nothing reports it. S29's over-ceiling rule §3 specified the content-aware shape; S31 specified four constraints; S32 read CC's measurement-stage classifier and found it sound in spirit but not yet safe to trust on anything we keep. The strip MUST satisfy ALL of the following before it runs on any conversation whose nodes enter the catalog:

1. **POSITIVE-SIGNATURE, not type-alone, not size-alone.** A block is stripped ONLY if it positively matches a machine-echo signature (bash stdout framing, long base64 run, file-cat dump, context-file serialization). Bare `type == tool_result` is NOT a strip trigger. A pure size gate is NOT a strip trigger — a size-only rule is exactly what eats the ~15.6% of tool_result blocks that carry floor-grade content (decisions, code-as-artifact). Default for any block is KEEP; strip is the exception requiring a positive hit.

2. **KEEP-BIASED by construction.** Small blocks kept unconditionally. No signature match → KEEP. The classifier's default return is "keep." (S32 confirmed CC's measurement classifier already inverts correctly here — small-keep floor, positive-match-to-strip. Good starting point.)

3. **THE kind-#4 HARDENING (the known bug to fix before any mined run).** The "large generic dump" rule — strip if `> threshold` AND "no conversational language" — is the one rule that can false-positive on a large CODE-DELIVERY block (Claude delivering a big file as a deliverable looks like "a dump with no prose" because code is not English sentences). This is precisely the 15.6%-floor-grade block the strip must NOT touch. BEFORE the strip runs on anything mined: harden kind-#4 so it cannot mistake a code-deliverable for echo — e.g. require the absence of a preceding code-write/deliverable `tool_use`, or raise its bar so it only catches the unambiguous MB-scale dumps. A classifier that cannot tell "cat dumped a file" from "Claude delivered code" is WRONG and is fixed, not adopted.

4. **AUDITABILITY IS MANDATORY (the receipt — the founding no-silent-discard invariant).** The strip MUST emit a per-block manifest: block id, kind matched, bytes/tokens dropped, host message uuid. A false-positive on a fence-bearing block must be CATCHABLE after the fact by reading the receipt. The measurement-stage classifier does NOT emit this — it counts and reports a total. That is fine for measuring; it is NOT fine for a mined run. No receipt → no trust → chunk the whale instead of stripping it.

5. **LAST-RESORT, LOW-BLAST-RADIUS.** The strip runs only on a registry-confirmed whale, only after fits-whole is impossible. It recovers ~0.6% on a normal conv and ~95%+ on an echo-whale — it is the whale-specific instrument, not a general pass. Because it is keep-biased + audited + rarely invoked, even a slightly-imperfect classifier has low blast radius — but the kind-#4 fix and the receipt are non-negotiable before it touches a conversation whose nodes enter the catalog.

**THE CANARY:** `cfc7a70a` (the 4.4M-token, ~95.8%-echo worst case) is the strip's proving ground. Strip it to a working copy, read the receipt, confirm it dropped ONLY echo and touched no content-bearing block. If the receipt comes back clean on the most extreme echo whale in the corpus, the strip is trustworthy. Then fire the reduced copy and confirm it nodes clean. Whale path proven → all four whales tractable.

---

## THE REFRAME S32 EARNED (for the canon)

S29's over-ceiling rule said the shape pass "forbids stripping because fences hide in tool_results" and treated the whale truncation as a careful exception. The ANCHOR's old do-not-relititate carried "strip is not the general fix (0.6% measured)" as if that closed the door on stripping. **Both halves are true and they are not in tension:** echo-strip is near-useless on a normal conversation (0.6%) AND it is the ONLY thing that makes a whale tractable (95%+). It was never a dead end — it is a precision instrument with exactly one indication. The error to retire is "stripping is not needed"; the truth to enshrine is "stripping is the whale-specific fix, hardened and audited, last-resort, floor-never-touched."

---

## OPEN / TUNABLE (folds forward)
- The fits-whole ceiling is validated to ~930k; the practical pipeline gate sits below 1M with output-token headroom (the reader must also EMIT a full node block). Pin the gate number against the authoritative token count at pipeline-build, informed by the 930k clean result.
- The strip's signature thresholds (the 256 KB block candidate floor from S29; the base64/escape-density numbers from CC's classifier) are build-tunable against what the four whales actually show when stripped. The STRUCTURE (positive-signature, keep-biased, kind-#4-hardened, audited, last-resort) is doctrine; the numbers are tunable.
- New whales will surface (re-freezes, new exports, texture re-slices). The registry is append-only-in-spirit; measure, record, route.

*Subordinate to The Progenitor v5. Confirms and deploys Shape_Slice_Over_Ceiling_Rule_v1. The floor is bedrock; the dissection table is ours. Look before cutting. Keep the receipt. Grind. Evolve. Dominate.*
