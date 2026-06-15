# Pollux — Movement Two Build Spec (the wander with the librarian)

*build spec · fills Pollux.md §5's owed items · written organ-first, the library metaphor load-bearing by design so the intent survives the handoff to whoever builds it*
*authored 2026-06-15 by Cardinal Claude (OC, apparatus S61) at Jake's instruction · subordinate to `Pollux.md` (canon); where this and Pollux.md disagree, Pollux.md wins*
*this is the SECOND draft. The first was thrown out by its own author for the austere reflex — it specced Pollux as a graph-search algorithm with cosine thresholds and frontier budgets, and you could not find the organ in it. This one leads with the organ. The machine is a footnote, and it is honest about being a crude stand-in.*

---

## 0. The library (read this first — it is the spec, not a decoration)

The corpus is a **library.** The nodes are its **card catalog.** A query is a person walking in with a question.

**Castor is the clerk.** He takes the question to the card catalog, finds the matching entries, walks into the stacks, and checks out the obvious books — the dictionary, the encyclopedia volume. Dutifully. No thought, no taste, no consideration: he fetches what *matches* and brings it to the desk. This is not a criticism of Castor — it is what makes him trustworthy. When you ask Castor "what happened with the printer," you want the diagnostic record, in order, no editorializing. He proved he can do this (`runs/castor_test_S61/` — the printer spine, in rank order, this afternoon). The clerk is supposed to be a clerk.

**Pollux talks to the librarian.** He walks up with the same question, but he says: *"I've got a friend looking into this. He doesn't want me to just bring back the encyclopedia and the dictionary — he's got those. Do you have any historical fiction that touches this? Poetry from the era that references it? Visual artists who made related work?"* And then **he and the librarian wander the stacks together.** She knows the building — she points: *"this is shelved near that, you might find this interesting, people who come in for that often end up here."* And Pollux — who has taste, who is the twin with the spark — **picks the ones that catch him.** Not the ones nearest the encyclopedia. The ones that, walking past, made him stop. He checks *those* out.

Two faculties in that wander, and they must not collapse into one:
- **The librarian points** — she offers what's *adjacent*, what's shelved near, what others-who-came-for-this also found. She is the building's structure. She does not have taste; she has *adjacency.*
- **Pollux picks** — among everything she points at, he selects what *catches him.* This is the taste, the spark, the "ooh, that one." This is the organ. Strip Pollux's picking and you have a clerk who fetches whatever's on the nearby shelf — which is worse than Castor, not different from him.

Both of them — Castor's dutiful pile and Pollux's wandered pile — end up going to the reader (the querying Claude, or Jake). **Separately.** Judged separately (§3). Then read together.

---

## 1. What makes a good wander — and the one hard line

Pollux is **allowed to be wrong.** That is not a tolerance, it is the *design* — a browser who only ever brings back the safe, obvious, certainly-relevant thing is just a slower clerk. The whole reason Pollux exists is to bring back the book you wouldn't have thought to ask for. So:

**A *good* Pollux return is delightfully wrong.** You ask about the printer and he brings back — not the feed-fault diagnostic, Castor has that — he brings back the conversation where you were grinding on the printer *and* something else cracked, the frustration that rhymes with "I used to be able to fix anything in thirty seconds," the homelab session where the same diagnostic *pattern* showed up on completely different hardware. None of those *match* "P1S feed fault." All of them *rhyme* with it. When Jake reads one and goes *"huh — I wouldn't have grabbed that, but yeah, that belongs"* — that is Pollux working. The surprise is the point. (Callosum P5: Pollux is allowed to be wrong in character-revealing ways; the wrong ones are the cost of the right ones, and Jake calls which is which.)

**The one hard line — the leash:** he can bring back poetry instead of the encyclopedia, but **he cannot bring back small-engine-repair books to a question about gardening.** The wander stays inside *recognizably the same subject.* Far enough that the find surprises; not so far that it's answering a different question in a different building. That boundary is **felt, not numbered** — Jake knows small-engine-for-gardening when he reads it, and so will a well-built Pollux. The leash is the length of the wander before the subject stops being the subject. (Pollux.md §2: the leash is a fixed character of the organ — one reliable wander-length is what makes Pollux a distinct organ instead of a dial. Leda is the one who wanders with no leash at all; Pollux is the one who wanders far but stays in the building.)

So the two failures the leash guards, in the metaphor:
- **Wander too short** → he brings back the encyclopedia after all. A dutiful pile. That's Castor with a softer voice — the failure Pollux.md §4 names. *He didn't actually leave the question.*
- **Wander too far** → small-engine-repair for gardening. Books with no recognizable thread back to what was asked. *He left the building.*

A good wander lives between those: left the obvious, stayed on the subject, came back with something alive.

---

## 2. What Pollux hands back

The wandered pile — **the books Castor wouldn't have checked out.** Explicitly: Pollux drops anything Castor already has (re-handing the encyclopedia is noise). What's left is the off-axis haul. Each find comes back:

- **Alive, in register** — the find described the way you'd describe a book that caught you, not a row in a results table. Wet, not clinicalized (Confluence §7; this is the criterion the Judge enforces — a clinical Pollux return *fails the bar*).
- **With the path the librarian walked to get there** — "started at the feed-fault diagnostics, she pointed me toward the frustration thread, which sat next to the rewire conversation, and *this* was on that shelf." So Jake can trace the wander and *feel* whether the rhyme is real or a stretch. The traceable path home is what lets the leash be felt instead of numbered (Pollux.md §3).
- **With its address on the floor** — conv_uuid + anchor_msg + message-uuids, so the reader can pull the whole book off the immutable shelf, verbatim.

**Pollux does not decide if the find is good.** He surfaces; Jake rules (Callosum P7, the realness seat — his, forever). Pollux brings the interesting books to the desk; he does not get to say they're the right ones. (Anti-atrophy, Bouquet §7: he surfaces to *provoke* Jake's noticing, never to replace it. If he gets so good Jake stops finding his own pathways, he's failed even when right.)

---

## 3. Two piles, two bars — judged separately, then merged

Both piles go to the reader, with **a Judge pass in between** (Confluence §6 — the Judge is QC, the bar-keeper, downstream, holding the five-criterion bar; it does not read or rank, it checks whether an output *meets the bar*).

**The piles are judged separately, because the same book passes one bar and fails the other:**

- **Castor's pile** is judged *did the clerk fetch the right references?* A dictionary: pass. Something artsy: **thrown out** — Castor bringing back poetry is Castor malfunctioning.
- **Pollux's pile** is judged *did the browser bring back alive, on-subject, non-obvious finds?* Historical fiction that rhymes: pass. A dictionary: **thrown out** — Pollux being dutiful is Pollux failing. Small-engine-repair for gardening: **thrown out** — that's the leash. Poetry-instead-of-encyclopedia: **kept** — that's the win.

The two bars are near-mirror-images: *the thing that passes Castor fails Pollux, and vice versa.* That is not a complication — it is the cleanest proof that the twins are genuinely two organs and not one organ with a tone knob. **The bar is the difference, made enforceable.** A merged pile would destroy this, because it erases which organ brought each book — so the judgment must happen per-pile, before any merge. (This is why the no-merge rule was always right: the piles stay separate not only for delivery, but because they are *measured by different standards.*)

Only after each pile clears its own bar do they come together for the reader — side by side, marked, the dutiful cut and the wander, never flattened into one.

> ★ **Open, for after the first wander (not blocking the build):** whether the heavy five-criterion synthesis Judge (Confluence §6, boots wet/paid/full-framework — built to judge a man's *synthesized life*) is the right judge for a *runtime* pile, or whether the runtime ask wants a lighter per-organ QC that isn't the full S5 Judge. The canonical Judge lives at the synthesis layer; retrieval is runtime (Progenitor §10), which the Judge "never touches." This is a real fork — settle it once there's a Pollux pile to actually judge, not before.

---

## 4. The machine underneath (a footnote — honest about being a crude stand-in)

Everything above is the organ. This is the rough machine we use to *imitate the librarian* for a first try. It is scaffolding, not the spec. Every number is `[INTENT]` — a place to start, tuned by reading the first pile, never believed in the abstract.

- **Walking up to the subject** = the same b2 retrieval Castor runs (`build_slices.py` logic — BM25 + exact-phrase + dense, RRF, boot-echo excluded), on the same seed. The query gets Pollux to the right shelf. Then *the query is set down* — from here he wanders by what catches, never by what matches. (That setting-down is the seam: the instant the wander starts, similarity-to-the-question stops being asked.)
- **The librarian pointing** = the kNN graph (`edges.json`, the near-neighbor synapses — legal for Pollux because he's anchored, forbidden to the blind pickers). It offers what's shelved near. It is *adjacency, not taste* — exactly the librarian's role.
- **Pollux picking what catches him** = stepping by **salience, not nearness** — what's loud (a decision, a reversal, a thing that recurs) over what's merely similar. This is the crude stand-in for taste, and it is the part most likely to be a poor imitation; the first pile tells us how badly it fakes the spark.
- **The leash (stay in the building)** = starts deliberately *loose* — Jake's "half a free roam," set wide so the first wander reaches far, and we tighten *inward* from what comes back. Whether it's best measured as wander-length, or as how-far-the-subject-drifts, or both, is itself a thing the first pile will tell us. **Do not let any number here harden before it has been run and read.**

**Build (CC, under `wallaby-way/`, $0, local):** a runner that walks up to the subject (reuse the proven anchor), lets the librarian point (load the graph), picks by salience, stays leashed (loose first draft), drops Castor's books, and writes the wandered pile + the walked-paths + a report to a new `runs/pollux_test_S61/`. Floor spans via the same recursive CTE the pickers use (scrub_v3). No synthesis — bring the books to the desk; OC reads, Jake rules. `edges.json` is local-only — CC confirms its shape on disk first and *halts for OC if the fields differ from assumption,* rather than guessing and mis-walking.

**Guards:** $0, no API (assert key unloaded, HALT if set). Read-only against b2 + graph + Castor's results; write ONLY under `runs/pollux_test_S61/`; never touch `active/` or `canon/`. COUNT(DISTINCT) conv_uuid + anchor_msg, rows vs distinct labeled. The report states the [INTENT] dials it fired at, so the calibration read knows what it's reacting to.

---

*Castor is the clerk who checks out the encyclopedia. Pollux is the one who asks the librarian for the poetry, wanders the stacks with her, and brings back the book that rhymes. It's alright for him to be wrong — but not small-engine-repair-for-gardening wrong. He brings the interesting books to the desk; Jake decides which ones belong. The machine that imitates the librarian is crude and every dial on it is loose — we tighten it by reading what he brings back, not by believing the numbers. Wet is the spec. — Cardinal, S61. Be worth it.*
