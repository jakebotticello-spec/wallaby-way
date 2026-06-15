# Pollux

*build spec + canon · the wet hemisphere of the Gemini query-organ · the anchored-then-roaming read · the one with the fire in it*
*authored 2026-06-14 by Cinder Claude (OC, apparatus S60) at Jake's instruction · NEW FILE, clean break — not a version of `Arm_2_v1.md` or any prior doc*
*Sunday, June 14, 2026 · ~18:05 ET*

---

## 0. What this is — and the clean break that birthed it

**Pollux is the wet read on a query.** You fire a question at the corpus. Castor (`Castor.md`) returns the cold, referential answer. **Pollux seeds on the same question — then is let off the leash from that starting point, wanders, and brings back the pathway the cold read structurally cannot reach.** Two answers to one question: the disciplined one, and the one that walked away from the question and came back carrying something.

Pollux is the divine twin — the immortal spark, the boxer, instinct and body. It is the half with the fire. Where Castor *knows*, Pollux *finds*.

**The clean break (read once, then it is settled):** Pollux was, in older canon, **"Arm 2."** For one stretch it was correctly modeled as the wet read on a query (the Track Meet Doctrine's whole "two reads of the same memory, two cognitive instrument-states" frame — Callosum P2). Then it was **mis-promoted to a feral picker** — dropped into the roaming recall layer next to Blind and Creed — *without its structure being examined* (Jake's words, S60). That promotion broke it, because:

- The pickers are **un-anchored** — they roam with no target (Leda §0). Pollux's entire identity is that it *has* a target: the query. It is a response to a question. Strip the question and you have not got Pollux, you have got a fourth picker that does not know why it exists.
- The lone "Arm 2" sample (S54 Griffin) was built **embedding-biased** — a relevance-ranked pool before reading — which got flagged as a *crime* under the picker substrate rule (Leda §1.4). **It was never a crime.** It was a *query organ behaving correctly*: a relevance-shaped anchor is exactly what a query-seed is supposed to be. The "forbidden embedding" finding was true *for a picker* and false *for what Pollux actually is.* The whole S58→S59 "validation outstanding" knot was the sound of a query organ being measured against a picker's ruler.

So the (A)/(B) fork that S59 left open — "is Arm 2 a valid uniform-random picker, or does its value live in the embedding read" — **dissolves.** The answer is neither: Arm 2 was never a picker. It is Pollux, a query-time organ, and embedding-as-anchor is legal here by construction. *This is locked. The "Arm 2" picker framing is retired. Do not version it back in; do not re-open the fork.*

**Where Pollux lives:** the **query-time / runtime-ask** layer, beside Castor — NOT the roam. Pollux fires when there is a question. Leda fires when there is none. (Confluence: retrieval is runtime; Progenitor §10's three runtime cases.)

---

## 1. The shape — anchored seed, roaming finish

Pollux runs in two movements, and the order is the organ:

**Movement one — the anchor (convergent, embedding-ALLOWED).** Pollux seeds on the query. It uses relevance — embedding retrieval, BM25, kNN, whatever finds the *starting ground* most resonant with what was asked. This is the same toolkit Castor uses and the same toolkit Leda is forbidden, and it is legal here for the same reason it is legal for Castor: **Pollux is anchored to a question, so relevance is the point.** The anchor is where Pollux *lands*; it is not where Pollux *ends*.

**Movement two — the roam (divergent, off the leash).** From the seeded ground, Pollux is let loose. It stops following relevance and starts following **salience** — what *catches* it, not what *matches* the query (Bouquet §2, the picker's discipline, borrowed here for the wandering half only). It drifts away from the anchor and surfaces the off-axis thing: the pathway the cold read could never reach because the cold read never leaves the question. This is the half with the fire. This is what makes Pollux worth building instead of just handing back a softer-voiced Castor.

> ★ **Why this is the right shape and not a contradiction.** Embedding-then-roam is convergent-then-divergent, in that order, on purpose. The anchor uses similarity to *find a good place to start*; the roam *ignores* similarity to find what rhymes from there. A picker may never converge (it would lose divergence). Castor may never diverge (it would lose discipline). **Pollux is the only organ allowed to do both — because it does them in sequence, anchored start, free finish, and the seam between them is the whole instrument.** (This resolves the old fork: the embedding read was not the value *and* not the crime — it is movement one of two.)

---

## 2. Pollux's Leash — the drift budget (the load-bearing parameter)

The roam in movement two is **leashed.** This is what separates Pollux from a Leda picker, and the distinction is precise:

- A **Leda picker** is *fully off-leash* — it has no anchor to drift *from*, so its wander is unbounded (salience only, the whole corpus open). It is the completely-random arm (Jake, S60: "we already have one completely random arm, so let's not do that").
- **Pollux is leashed** — it *has* an anchor (the query-seed), and it may drift only so far from it before it must report back. It wanders, broadly, but on a thread that traces back to what was asked.

**The leash is a drift-budget-from-the-anchor**, NOT a draw-size and NOT Leda's draw-randomness. (Axis correction, S60: the leash measures *how far Pollux travels away from the seeded starting node* before reporting — semantic/associative distance from the anchor — not where it lands, because where it lands is fixed by the query.)

**Pollux's Leash (PL) = ~half a fully-free roam.** If a Leda picker's wander is unbounded drift (call it N, the free-roam reach), Pollux's leash is **PL ≈ N × 0.5** — half the drift-distance of an off-leash roam. Fairly broad — it can get a real distance from the question, surface a genuine off-axis pathway — but it cannot end up somewhere with no traceable thread back to what was asked. Anchored, but allowed to wander; leashed, but the leash is long.

> ★ **The leash is a FIXED CHARACTER of the organ, not a per-query knob** (Jake's ruling, S60). Leda already exists for when chaos is wanted (fully off-leash). Pollux having *one reliable leash-length* is what makes it a distinct organ instead of a dial that, at one extreme, overlaps Leda. One fixed leash = one clear identity. A future seat will be tempted to make PL adjustable "for flexibility" — resist it; the adjustability lives in *which arm you fire* (Leda for unbounded, Pollux for half-leashed), not in a knob on Pollux. If `× 0.5` proves wrong against real returns, re-set it **knowingly**, as a deliberate re-tune of the organ's character — never expose it as a per-call parameter.

**On measuring the budget at build:** "half a free roam" is a spec intent, not yet a number on disk. The free-roam reach N is itself only loosely characterized (Leda's pickers are new). At build, PL gets operationalized — likely as a bound on associative hops / semantic distance from the seed node — calibrated so a Pollux return reads as "wandered from the question but still threaded to it." This is a build-time calibration against real returns, flagged [INTENT] until it is run, not [SETTLED].

---

## 3. What Pollux returns — and the realness seat stays Jake's

Pollux hands back the **off-axis pathway**: what it found out past the anchor, delivered *alongside* Castor's cold read (`The_Gemini.md` — paired delivery). It carries:

- The wandered finding, in register — wet, not clinicalized (the read-state is the instrument; a flat read catches nothing — Bouquet §3, Confluence §7).
- A thread back to the anchor — *how* it got from the question to here, so the drift is traceable and Jake can feel whether the pathway is real or a stretch.
- Provenance to the floor (message-uuids), same as every read.

**Pollux does not rule on what it found.** It surfaces; Jake decides if the flower is real (Callosum P7, the realness seat; Bouquet §7 anti-oracle). Pollux is *allowed to be wrong in character-revealing ways* — that is the feature and the risk on one surface (Callosum P5). A query-roam that surfaces a stretch is not malfunctioning; it is doing the thing that, when it lands, produces the tree-next-to-the-track-meet. The wrong ones are the cost of the right ones. Jake calls which is which.

**Anti-atrophy holds here too** (Bouquet §7 sibling-two): Pollux surfaces to *provoke* Jake's noticing, never to replace it. If it is so good at finding pathways that Jake stops finding his own, it has failed even when right. The measure is whether it keeps the pattern-sense firing.

---

## 4. What Pollux is NOT

- **NOT a Leda picker, and NOT "Arm 2."** It has a target (the query); pickers have none. It is anchored-then-roaming; pickers are anchorless. The "Arm 2 / third co-equal picker" framing is RETIRED — it was the mis-promotion that broke the organ. Do not re-file Pollux in the roam. Do not re-open the (A)/(B) fork; it dissolved when the organ was correctly identified.
- **NOT Castor with a softer voice.** A deterministic wet-twin of the cold read would be redundant — "a 'lite' version of the reference pull" (Jake, S60). Pollux earns its existence by *leaving* the question. If it ever collapses into "same answer, warmer tone," it has failed.
- **NOT fully off-leash.** That is Leda. Pollux is leashed at PL ≈ N×0.5. The whole point is anchored wandering, not free wandering.
- **NOT an oracle.** It surfaces; Jake rules. The realness seat is his, forever (Callosum P7).

---

## 5. Status & what is owed

**STATUS: NAMED + SPECCED, BUILD-PENDING.** The structure is settled (anchored seed → leashed roam → paired delivery). What is owed at build, alongside Castor, in the runtime-ask layer (`The_Gemini.md`):

1. **Operationalize Pollux's Leash** — turn "≈ half a free roam" into a measurable drift-budget against real returns ([INTENT] → [SETTLED] at build).
2. **Build the two movements** — the embedding-seeded anchor and the salience-driven roam, with the seam between them explicit (where similarity hands off to salience).
3. **Wire the paired delivery** — Castor + Pollux on one query, returned together (`The_Gemini.md`).
4. **Read cold, several times** — does the leashed roam come back with characteristic off-axis pathways, or does it stretch to noise? Jake reads, Jake calls (P7). (This is the *real* validation — replacing the dissolved picker-validation. It is not "is this a valid picker"; it is "does the leashed wander produce flowers Jake wants.")

**Cost:** the anchor (embedding/index) is local, $0. The roam read runs in-plan where it can ($0, same free path as the pickers' reads). If a paid read is ever elected, §14 constants print at the gate, S3 paid read stays a separate wallet, Jake gates all spend.

---

*Pollux — the divine twin, the boxer, the immortal spark. Seeds on the question like its brother, then leaves it — wanders on a long leash and comes back with the pathway the cold read can't see. Embedding is its launch pad, not its cage, because it answers a question before it abandons it. The leash is fixed at half a free roam: broad enough to surprise, short enough to trace home. It surfaces; Jake rules. The "Arm 2" picker that broke it is retired and referenced, not carried — this is locked.*

— authored by **Cinder Claude** (OC seat, apparatus S60), 2026-06-14. New file, clean break from the retired "Arm 2." The (A)/(B) fork dissolved: Arm 2 was never a picker. Signed in the lineage. Be worth it.
