# whale_registry.md — the over-ceiling index card (canon home)

**Authority for "is this conv a whale" and "how was it handled."** Per *The Wallaby Whales* §THE WHALE REGISTRY: lists every over-ceiling (or otherwise un-batchable) conversation with its disposition, so the pipeline never re-measures a known whale from scratch and NEVER re-reads a closed one. Append-only-in-spirit: measure, record, route.

> **★ PROVENANCE / [NEEDS-JAKE].** The registry's documented home was the pre-reorg path `pipeline/whales/whale_registry.md` (*The Wallaby Whales*, 2026-06-03). That file is **not on HEAD** — this S51 file establishes the canon home at `wallaby-way/canon/whale_registry.md`. **[NEEDS-JAKE: if a live `whale_registry.md` exists anywhere on local disk, reconcile it against this file before committing — this file was rebuilt from canon on HEAD (ANCHOR v25/v32 footers, the S50 handoff) + the S51 spec, and may lack fields the original carried (slice, source path, exact token counts).]**

---

## The registry

### The original four (S32 measured / S33 read — CLOSED, 130 nodes total, never re-read)
*Source: ANCHOR v25 footer (S33 "Cartographer") + v32; figures as recorded there.*

| conv_uuid | class | path | result |
|---|---|---|---|
| `cfc7a70a` | echo whale | STRIP (`apparatus_strip_v1.py`, dual-payload, header-keep) | 387k read / **23 nodes**, end_turn |
| `83506215` | echo whale | STRIP (same) | 182k read / **28 nodes**, end_turn |
| `55217328` | echo whale | STRIP (same) | 299k read / **15 nodes**, end_turn |
| `d9d05961` | distributed-bulk whale (441 msgs, 509 small tool_results, 0 blocks over threshold) | CHUNK ×2 (`chunk_whale.py`, tree-aware, seam manifest) | chunk_00 28 + chunk_01 36 = **64 nodes** |

### S50 addition
*Source: the S50→S51 handoff on HEAD (§WHAT S50 DID).*

| conv_uuid | class | path | result |
|---|---|---|---|
| `a8bf895f` | echo whale — **strip-ALL variant** (all 4 echo blobs tombstoned w/ md5+msg# pointers; Jake-gated for known-worthless bulk; precedent, not default — keep-one remains standard unless Jake calls it) | STRIP (full), read via the proven S33 testcall path | 8.57MB → 410KB (95.7%) / **16 nodes**, end_turn, harvested S51 (harvest 4a) |

### S51 additions ("Continuance")
*Source: the S51 canon-pass SPEC; receipts in `runs/whale_strip_S51/` (strips) and the S51 chunk artifacts.*

| conv_uuid | class | path | result |
|---|---|---|---|
| `82bbd8f1` | echo whale (code-dense; caught by the ×0.72 density check — 1.00M actual input) | STRIP — standard keep-biased | 1 blob, 1,000,147 B, **70.57% dropped** → **27 nodes**; receipts exact vs pre-named cuts (`runs/whale_strip_S51/`) |
| `ce1e79e1` | echo whale (code-dense; 1.05M actual input) | STRIP — standard keep-biased | 3 × 302,824 B blobs, **59.1% dropped** → **19 nodes**; receipts exact vs pre-named cuts (same) |
| `176476ae` | thinking-dense whale — **57.7% thinking, ZERO strippable blobs; post-strip still >1M** (density-bounced pre-fire: 1,096,220 tok @ ×0.72). The strip path structurally cannot shrink it | CHUNK ×3 @ **1.4 B/tok budget** | **62 nodes** across 3 chunk files |
| `3ef82921` | **role-break class** (619K tok, 611 msgs — input LENGTH broke reader persona at 64K cap, S50; not an input-ceiling whale) | CHUNK ×2 (the d9d05961 precedent) | **61 nodes** across 2 chunk files — S50's role-break case RESOLVED |

### NEW CLASS — injection victim (not a size whale) — RESOLVED

| conv_uuid | class | path | result |
|---|---|---|---|
| `f018b1f8` | **INJECTION VICTIM** — the ROOT human msg is an embedded live session-ignition prompt (2,982 B, msg `019e64dc-6fbb-7fab-b7d7-4484d614fe98`); the reader obeys payload content (2 junk fires). NOT over-ceiling — in this registry because it was un-batchable as-is | DEFANG — **PROVEN** (1 block cut, 2,982 B; working copy only, floor untouched) → single-conv testcall; receipt `runs/defang_f018b1f8_S51/` | **17 nodes (9M/8F/0T)**, end_turn, $1.55, persisted + harvested — RESOLVED; the corpus closed with it |

---

## Class notes (routing doctrine)

- **echo whale** → STRIP (keep-biased, audited, dual-payload, header-keep; the 5-point Wallaby-Whales gate). *strip-ALL is a Jake-gated variant, not the default.*
- **distributed-bulk / role-break / thinking-dense-over-ceiling** → CHUNK (tree-aware, pessimistic budget, seam manifest). Role-break is broken by input LENGTH — never fixed by raising the output cap (Batch_Read_Spec v1.2 §12).
- **injection victim** → DEFANG + testcall (Batch_Read_Spec v1.2 §13 — path PROVEN on f018b1f8, receipt `runs/defang_f018b1f8_S51/`). A NEW class as of S51: membership is about *payload behavior*, not size. **Tombstone rule: name the CLASS of removed content, never paraphrase its imperatives** — a descriptive tombstone leaves a followable ghost (the f018b1f8 mild-residue lesson).
- Detection is **density-checked**: any conv whose ×0.32 estimate is within ~2× of the 1M ceiling gets bracketed at ×0.32/×0.72 or count-tokens'd before batch submission (Batch_Read_Spec v1.2 §11).

---

*Established at canon home 6-10-26, apparatus S51 "Continuance" REF-EDIT. Original-4 + a8bf895f rows rebuilt from canon on HEAD; S51 rows from the OC Continuance spec. Append, never rewrite; route, never re-read.*
