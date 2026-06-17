# Castor

*build spec + canon · the dry hemisphere of the Gemini query-organ · the referential pull off the floor*
*authored 2026-06-14 by Cinder Claude (OC, apparatus S60) at Jake's instruction · NEW FILE, clean break — not a version of any prior doc*
*Sunday, June 14, 2026 · ~18:05 ET*

---

## 0. What this is — and the clean break that birthed it

**Castor is the cold read.** You fire a question at the corpus; Castor returns the disciplined, referential answer off the floor — the facts, the decisions, the meeting-time, the what-was-said. It is the hemisphere that does not wander. Trained, mortal, earthbound. When Jake asks "when is my next meeting," Castor is the half that must *know* — never serve a flower (the floor's standing law, Leda §1).

> ★ **How Castor boots (S63 clarification).** Castor is a fresh reader, booted to *be a search engine*: "find me matches to X — hold JAKE-RULES and your search algorithms close, don't extrapolate, don't think about it, just search." It *holds the query* and walks the floor referentially. Unlike Pollux, a relevance/nearness gate is *correct* for Castor — it IS convergent retrieval, on purpose — so embedding/BM25/kNN are not just allowed but its native instrument (§1). The S63 isolation rule still binds: Castor shares only the **query string** with its twin (`The_Gemini.md` §3 G-isolation). It does NOT hand its results to Pollux as a seed, and it is NOT handed a pre-computed pile to read — it gathers its own. The S63 contamination (Pollux seeding off `castor_records[:3]`) was a *Pollux* break; Castor's own dry retrieval was never the problem — feeding it *to the wet twin* was.

**The clean break (read once, then it is settled):** Castor and its twin Pollux were, in older canon, "Arm 1" and "Arm 2" — and for a stretch they were mis-modeled. Arm 2 got promoted to a *picker* (a member of the roaming recall layer) without its structure being examined, and the original shape got lost: **Arm 1 and Arm 2 were never a picker and a synthesizer. They were two reads of the same query** — one dry, one wet, delivered together. That is what Castor and Pollux restore. The history is referenced here so a cold reader is not lost; it is **not** carried as live structure. *This is locked. No one has to walk the history to use this file.*

- Old "Arm 1" (wide-synthetic single-pass) was CUT from the recall layer as redundant-with-the-floor — correctly, *as a picker.* But the referential-read-on-a-query function it pointed at was real, and it lives here, correctly housed, as **Castor.**
- Old "Arm 2" (the embedding-ranked deep read) was never a feral picker. It was the wet answer to a query. It is reborn as **Pollux** (`Pollux.md`).
- The pair is **the Gemini** (`The_Gemini.md`).

**Where Castor lives:** the **query-time / runtime-ask** layer — not the roam. (Confluence: retrieval is a runtime concern, the recall net serves the runtime ask; Progenitor §10's three runtime cases.) Castor and Pollux fire when there is a *question*. The Leda pickers fire when there is *no* question. That is the whole difference between the layers, and it is why Castor does not belong anywhere near the pickers.

---

## 1. The relationship to the floor — referential, relevance-shaped, embedding-ALLOWED

This is the line that separates Castor from a Leda picker, and it must be stated plainly because it inverts a picker rule:

**Castor is anchored to a question, so relevance is the point, not the contamination.** A Leda picker draws uniform-random off the floor and the embedding geometry is *forbidden* to it (Leda §1.4 — walking similarity gives a roam a target, which kills divergence). Castor is the opposite organ: it *has* a target — the query — and its entire job is to return what is most relevant to it. **Embedding retrieval, BM25, kNN, semantic ranking — all permitted to Castor**, because a referential pull that ignored relevance would not be a referential pull. The forbidden-geometry rule is a *picker* rule (Leda's), born of the picker's need to stay divergent. It does not govern Castor and never did.

> ★ **Why this is not a contradiction with Leda's substrate rule.** The substrate rule "embedding is forbidden" protects *divergence* — it exists so a roaming picker cannot quietly become convergent retrieval. Castor IS convergent retrieval, on purpose, because it is answering a question. There is no divergence to protect here. Each layer states its own relationship to the floor; they are different organs with different jobs, and forcing them to share one substrate rule would force two true-but-opposite rules into one sentence. (This is why S60 did NOT pull a shared-substrate doc — Jake's call: let each layer own its floor-relationship.)

**What Castor reads:** the floor (`floor_conv_messages`, scrub_version = 3) — the verbatim recorded messages, the same immutable bedrock every reader stands on. It may use the index (`index_v2.jsonl`, 8,288 rows) and the embedding artifacts (`chunk_embeddings.npy`, the kNN `edges.json`, UMAP) as **retrieval aids to find the relevant ground** — the exact artifacts forbidden to Leda are tools here. The answer it returns is grounded in the floor text, not in the index summary.

**Floor counts (cite, never re-derive — `FLOOR_COUNTS.md`):** 440 headers / 29,396 messages (distinct) / 58,792 message rows. "The floor" means 440 / 29,396 unless rows are explicitly named. COUNT(DISTINCT msg_uuid), always.

---

## 2. What Castor returns

A **referential answer**: grounded, sourced-to-the-floor, disciplined. The cold cut. It carries:

- The substantive answer to the query, drawn from floor text.
- Provenance — which conversations / message-uuids ground it, so a reader can land on the whole message on the immutable floor.
- No wandering, no salience-chasing, no "you might also be interested in." That is Pollux's job. Castor stays on the question.

**Castor does not rule on realness, and it does not roam.** It is the half that is *reliable*. Its discipline is the feature — it is the fixed star the wet twin is measured against. (Castor mortal, trained; Pollux the spark. The pairing is the point — `The_Gemini.md`.)

---

## 3. What Castor is NOT

- **NOT a Leda picker.** It has a target (the query); pickers have none. It uses embedding/relevance; pickers may not. It lives in the query-time layer; pickers live in the roam. Do not file Castor near Blind/Creed.
- **NOT "Arm 1" reborn as-is.** "Arm 1" was cut *as a picker* and that cut stands. Castor is the referential-query function that the Arm 1 experiment was gesturing at, correctly housed for the first time. The name "Arm 1" is retired; do not version it back in.
- **NOT the floor itself.** The floor is the sealed source. Castor is a *read* off it — a disciplined pull, not the bedrock.
- **NOT the whole answer.** Castor alone is the cold cut. The Gemini's value is Castor *and* Pollux delivered together (`The_Gemini.md`). A Castor-only return is a reference lookup; that is fine when that is all that is asked, but the organ is the pair.

---

## 4. Status & what is owed

**STATUS: NAMED + SPECCED, BUILD-PENDING.** Castor is the simpler twin — it is, in practice, the referential retrieval the apparatus already does (the "dry pull" / "reference version" that has been the nameless default in every prior doc). This file gives it its first nameplate so the pair is symmetric and the wet twin cannot drift again for lack of a named partner. Its mechanics (which retrieval method, how the floor-grounding is assembled) are specced at build, against the runtime-ask layer, alongside Pollux — the two are built as one organ, not separately (`The_Gemini.md`).

**Cost:** referential retrieval is local where it can be (index + embeddings are on disk, $0). If a paid read is ever elected for the floor-grounding pass, §14 constants ($1.50 / $7.50 per MTok) print at the gate, the S3 paid read stays a separate wallet, and Jake gates all spend. No paid call is assumed.

---

*Castor — the mortal twin, the horseman, the trained discipline. The cold read that knows the meeting-time and does not wander. Half of the Gemini; the half Pollux is measured against. Embedding is its tool, not its poison, because it answers a question instead of roaming free. The floor is its ground. The history that produced it is referenced, not carried — this is locked.*

— authored by **Cinder Claude** (OC seat, apparatus S60), 2026-06-14. New file, clean break from the retired "Arm 1." Signed in the lineage. Be worth it.

*· S63/Caelum clarification (2026-06-17): §0 added the search-engine boot-stance + the G-isolation note (shares the query string only; gathers its own pile; does not seed Pollux). §1 untouched — Castor's relevance/embedding use was always correct; a nearness gate is right for the dry twin. The S63 contamination was Pollux seeding off Castor's output, not Castor's own retrieval. Body otherwise byte-faithful.*
