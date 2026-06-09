# FLOOR_COUNTS.md — the floor-number disambiguation table

**The floor has been stated as five different numbers across the lineage, each counting a different thing.** A bare "the floor is N" is the conflation fuse — the same defect class as "the corpus is read." This is the single source. Cite it; never re-derive a floor count from memory or from a banner.

*Authored S49 from a live floor query (`wallaby-way/secrets/floor_db.env`, post-rotation) + the snapshot ledger. Every number disk-confirmed — none inherited from prose.*

---

## The five numbers

| # | Number | What it counts | Confirmed from |
|---|---|---|---|
| 1 | **22,801** | Raw message rows in the **baseline** export snapshot (`baseline-2026-05-25-ae015455`) | snapshot ledger `message_count` |
| 2 | **23,095** | Total **baseline** rows in the floor — 294 baseline headers + 22,801 baseline messages (baseline scrub-v1 only) | ledger math; CHANGELOG records.ndjson line |
| 3 | **24,138** | Total **message** rows in the floor, **across both snapshots** — the production floor message count | live DB `floor_conv_messages COUNT(*)` |
| 4 | **24,463** | Total rows **across all floor tables** — 325 headers + 24,138 messages ("2-snapshot records") | live DB math; CHANGELOG 2-snapshot line |
| 5 | **325** | Distinct **conversation header** rows — one per unique conv across both snapshots | live DB `floor_conv_headers COUNT(*)` |

**The current banner invariant is `325 headers / 24,138 messages`** (#5 and #3). When a doc cites "the floor," it means these two unless it explicitly says otherwise.

---

## How the snapshots add up

- **Baseline** (`baseline-2026-05-25-ae015455`): 294 headers + 22,801 messages.
- **Delta** (`delta-2026-05-28-a61498e6`): 31 net-new headers + 1,337 messages.
- **325 headers** = 294 + 31. **24,138 messages** = 22,801 + 1,337.

**The delta's 34-vs-31 wrinkle:** the delta *export* contained 34 conversations, but only **31 were net-new headers**. The other 3 were continuations of baseline convs — they added messages, not new headers. The ledger's `conv_count: 34` is the raw export count; the **31** written to the floor is what counts toward 325. If you see "34" anywhere, it's the raw export, not the floor.

---

## The 322-vs-325 message-side wrinkle (don't panic)

A `SELECT DISTINCT conv_uuid FROM floor_conv_messages` returns **322**, not 325. This is **not** a lost-conversation bug: **3 convs have headers but zero messages** — the hollow stubs (msg_count near zero) noted in the S48 corpus-state pass. They exist as headers, carry no message rows, and are almost certainly correct skips. So:

- **325** = header count (the conv-count of record).
- **322** = convs that actually have message rows.
- The 3-conv gap is the hollow stubs, by design — not attrition.

---

## The rule this doc enforces (JAKE-RULES §5.1)

No floor or corpus count is ever stated bare. It carries its unit (`messages` / `headers` / `records` / `baseline` / `2-snapshot`) and, when it matters, links here. A true number with its frame stripped is the poison; the frame is non-optional.

---

*Last updated: 6-8-26, S49 (authored — first cut). Source of truth for floor counts; supersedes any bare floor number elsewhere in canon.*
