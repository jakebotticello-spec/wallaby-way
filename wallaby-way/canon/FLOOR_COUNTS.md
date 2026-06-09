# FLOOR_COUNTS.md — the corpus-state bible (floor + read counts, every number sourced)

**The floor has been stated as five different numbers across the lineage, each counting a different thing.** A bare "the floor is N" is the conflation fuse — the same defect class as "the corpus is read." This is the single source. Cite it; never re-derive a floor count from memory or from a banner.

**As of the S49 census, this file also carries the read-side counts** (what's been read, what hasn't, and the node yield) — it is THE single place any session checks "where does the corpus stand." Same rule for every number here, floor-side or read-side: cite it, never re-derive a count from memory or a banner.

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

## The read-side counts (S49 census — disk/floor-confirmed)

The floor is the denominator; these are the numerator and the remainder. Every figure below was disk- and floor-confirmed in the S49 census (`runs/groundtruth_S49/`) — none inherited from prose or a banner.

| Count | Value | What it counts | Confirmed from |
|---|---|---|---|
| **READ** | **202 convs** | convs harvested into the pile | 194 in `nodes/harvested/` + 8 whales in `nodes/catalogs/` (disjoint pools, 0 UUID overlap) |
| **READ nodes** | **3,743 nodes** | salience nodes in the pile | 3,226 harvested (disk `**Salience:**`-marker count, EXACT to `MERGE_MANIFEST_S47.md`) + 517 whale |
| **UNREAD** | **123 convs** | floor headers not yet read | 325 − 202; worklist verified clean (0 over-claim, 0 miss vs the floor-minus-read set) |
| **UNREAD valid for batch** | **120 convs** | unread convs that pass the skeleton gate | 123 − 3 hollow (the zero-message stubs, excluded by the skeleton gate, Batch_Read_Spec §4) |
| **Node yield of reading the 123** | **`[TBD — resolves on first unread-batch read]`** | nodes the unread read will produce | post-read by nature — node count is unknowable until the batch runs |

**202 + 123 = 325.** ✓ Ties to floor number #5 (header count). The corpus is **202/325 read; 123 pending** — never stated bare, always with the remainder.

**The one unsettled number in this bible is the node yield of the 123.** Every other count here is disk-confirmed. The yield is `[TBD — resolves on first unread-batch read]` because a conversation's node count cannot be known until the reader has read it; it is a post-read measurement, not a pre-read estimate. Do not fill it with a projection.

### The harvested pools (why 202 = 194 + 8)

So no future session re-trips the "194 on disk but the manifest says 202" confusion the census resolved:

- **`nodes/harvested/`** holds **194 conv files** (1 `.md` + 1 `.parents.json` sidecar each), **3,226 nodes**.
- **`nodes/catalogs/`** holds the **8 whale convs**, **517 canonical nodes**.
- The two pools are **disjoint** (0 UUID overlap). `MERGE_MANIFEST_S47.md` covers both → **202 convs / 3,743 nodes**.
- **NOT corpus, do not count:** `catalogs/` also contains **76 `_whole.md` nodes** (inside `confirm_48b4110a_whole.md` + `confirm_ea900330_whole.md`) that are **whole-conv verification reads** — evidence artifacts from a read-check, correctly excluded from the manifest count. They are proof-of-work, not pile nodes. Never mistake them for uncounted corpus.

*The read-side section was authored at the S49 census (TWW CCC S3 produced the floor-side; apparatus S49 "Concord" added this read-side block). Source: full disk + live-floor census, `runs/groundtruth_S49/`. Every figure disk-confirmed; none inherited from prose or banner.*

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
- The 3 hollow stubs are **`3f84a335`, `ae3468be`, `bc42e9ab`**. They are excluded from any batch read by the skeleton gate (Batch_Read_Spec §4) — which is why UNREAD = 123 but UNREAD-valid-for-batch = 120. The floor-side hollow count and the read-side batch exclusion are the same three convs.

---

## The rule this doc enforces (JAKE-RULES §5.1)

No floor or corpus count is ever stated bare. It carries its unit (`messages` / `headers` / `records` / `baseline` / `2-snapshot`) and, when it matters, links here. A true number with its frame stripped is the poison; the frame is non-optional.

---

*Last updated: 6-9-26, apparatus S49 "Concord" (added the read-side counts — READ 202/3,743, UNREAD 123 = 120 valid + 3 hollow, node-yield TBD — and became the corpus-state bible; floor-side authored TWW CCC S3). Source of truth for floor AND read counts; supersedes any bare count elsewhere in canon.*
