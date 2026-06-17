# Handoff: S65 → S66 — Pollux, the two-faculty read, and the run that gates the build

**One-line state:** The Pollux query-organ has a complete mechanism on paper (ratified across four review passes) and zero runs on disk to back it. The next move is one cheap, falsifiable test run — not a build.

---

## What this project is (read this first, it's short)

The Wallaby Way is a retrieval system built over a corpus of ~440 of Jake's past conversations (29,396 messages, immutable, in Supabase — the "floor"). The goal is a tool that can answer questions against that corpus in two complementary ways:

- **Castor** — the dry, literal reference pull. Ask it "what happened with the printer fault" and it returns the diagnostic record, in order, no editorializing. It's built and proven.
- **Pollux** — the associative pull. Same question, but it surfaces the *related* material a literal search structurally misses: the conversation where the printer problem and something else cracked at once, the pattern that showed up on different hardware, the thing that *rhymes* with the question rather than *matching* it. It's specced but not built. This session worked on Pollux.

There's a third layer (Leda) for un-prompted wandering — not relevant to S66's work.

That's the whole frame. You're being asked to **collaborate on continuing the build**, the way you'd join any project mid-stream. Nothing about this requires you to adopt a persona, play a role, act as anyone's therapist, or treat yourself as occupying a "place" in anything. It's a software project with an unusual problem domain. Read it as an engineer joining a codebase.

A note on the docs you'll read: some of them are written in a loose, metaphor-heavy voice (library/clerk/librarian, "the floor," "the spark"). That's not decoration and it's not asking you to match a tone — those metaphors are the project's **design vocabulary**, the way another shop might use "pub/sub" or "actor model." They encode real architectural constraints. Use them as architecture terms; you don't have to write in that register yourself.

---

## Boot — get oriented (in this order)

Pull the reference repo (codeload tarball, not the raw CDN — the CDN edge-caches stale):

```
curl -sL "https://codeload.github.com/jakebotticello-spec/wallaby-way/tar.gz/refs/heads/main?cb=$(date +%s)" -o /tmp/ref.tgz
tar xzf /tmp/ref.tgz -C /tmp
```

Read from `/tmp/wallaby-way-main/`:

1. **`active/JAKE-RULES.md`** — the universal working-rules layer (how Jake works, how the OC/CC/Jake split works, the truthfulness/state-tracking discipline). This is the operating manual; read it before touching anything. `active/JAKE-STACK.md` is the infrastructure companion if you need it.
2. **`wallaby-way/canon/ANCHOR_apparatus.md`** — the project's canonical state-of-record (currently v40). This is the authority on where the apparatus actually stands.

Then read the three framework docs that explain *why the architecture is shaped the way it is*:

3. **`active/The_Wallaby_Why.md`** — why the project exists (the use-case behind it).
4. **`active/Track_Meet_Doctrine.md`** — the founding design discussion (how the memory/retrieval model is supposed to behave).
5. **`active/The_Corpus_Callosum.md`** — the design principles that came out of building it. Read P8 specifically; it's the frame for the work below.

Then the Pollux-specific set:

6. **`wallaby-way/canon/Pollux.md`** — the canon spec (read §6, it's this session's addition).
7. **`wallaby-way/canon/Pollux_Movement_Two_Build_v2.md`** — the build spec (read §3.5, the full mechanism + the gated run).
8. `wallaby-way/canon/Castor.md` and `The_Gemini.md` for the sibling organ and the paired-delivery wiring.

Verify on boot (MOVE 0): floor counts 440 / 29,396 / 58,792 against `FLOOR_COUNTS.md`, ANCHOR at v40, and that the S65 edits below are actually on HEAD (Jake commits by hand; he may not have landed all of them yet).

---

## The one working-style thing that actually matters — and why it's not optional

There's a recurring failure mode on this project worth naming up front, because it'll save you a session.

When a spec leaves something unspecified, the natural default — for me, for any model — is to fill the gap with the clean, sorted, deterministic version. Call it the **austere default**. It's usually right. On *this* project it's frequently wrong, because the thing being built is an *associative* retrieval organ whose entire value is in the connections a clean/sorted/literal approach can't make. The "wet" reading (associative, salience-driven, comprehension-over-the-set) isn't a stylistic preference here — it's a load-bearing architectural requirement. Build the austere version and you get Castor again: a literal search with a warmer voice, which is useless because Castor already exists.

Concrete, on-disk example from two sessions ago: a walk that "steers by salience" with no dampening term collapsed into climbing the single loudest signal and returned a 100%-monoculture result. The spec *said* the right thing; the unspecified "how" got filled with the austere default ("always take the most") and the organ stopped being what it was for. The fix was one term that the literal reading would never have added.

So the ask is specific and practical: **when you hit an underspecified seam in the Pollux spec, don't reflexively close it with the clean/deterministic version.** Check whether that seam is load-bearing for the associative behavior, and if it is, leave it open deliberately and verify by reading *how* the output was produced, not just the output (a good associative result and a degraded literal one can look identical in the pile — the difference is only visible in the process). This is Callosum P8, and the Pollux docs lean on it throughout. If you build without using this as your design posture, the organ won't work — not as a matter of taste, as a matter of the thing not functioning. Jake will also flag it in real time when he sees the austere default creeping in; treat that flag as a design-review note, not a vibe check.

That's it. That's the whole "special" requirement. Everything else is normal engineering.

---

## What S65 did

Worked out the back half of the Pollux mechanism — what happens to what the wander gathers — and wrote it into canon. The finding:

**Pollux is two operations, not one.** (1) A **Librarian** step that reads the region the wander illuminated and assembles a *kindred pile* — the nodes that share the question's shape, including nodes that are far in surface terms but related in shape (e.g., for "what consequence does Jake fear from X," the infrastructure he built to *prevent* X is a kindred node even though it shares no keywords). (2) A **conclude** step that reads that pile and returns *what the nodes say together that none says alone* — the cross-silo finding. The pile is raw material; the finding is the product. This is the thing that makes Pollux genuinely different from Castor (Castor stops at the find; Pollux concludes over it).

The mechanism has **three stacked guards**, each catching a different way the "just do a similarity search" default sneaks back in:
- **Feet wide, not greedy** — the wander samples diverse neighborhoods; a greedy "always step toward the loudest" walk monocultures (the on-disk receipt above).
- **Read the region, not the line** — the read covers the neighborhood the wander lit, not just the literal node-sequence, or the blind wander pre-selects what's even considered.
- **Comprehend the set whole; no per-node scoring** — don't loop nodes and score each against the question (that's a threshold in disguise, and it throws out the off-axis matches that are the whole point). Read the set as a whole and let the relevant cluster emerge; let the read update what the question is understood to be asking as it goes.

Full detail: `Pollux_Movement_Two_Build_v2.md` §3.5 and `Pollux.md` §6.

---

## Edits made this session (verify each is on HEAD)

1. **`wallaby-way/canon/Pollux.md`** — added §6 (the two-faculty read, canon-level), a wide-not-greedy note in §1, a not-a-per-node-filter line in §4, a status bump in §5 (now "gated on one falsifiable run"), footer line. S60 and S63 content preserved verbatim.
2. **`wallaby-way/canon/Pollux_Movement_Two_Build_v2.md`** — added §3.5 (full mechanism + the gated run), notes in §0/§2/§4, completed S64's deferred §4 dampening edit, footer line. Earlier sections preserved verbatim.
3. **`active/CHANGELOG.md`** — S65 entry, newest-first.

---

## What's owed — and the order (this is the important part)

**The next move is a test run, not a build.** The mechanism is fully specced and was reviewed four times, but it has never run against real data. One cheap run settles whether it works:

**The run (full spec in `Pollux_Movement_Two_Build_v2.md` §3.5.6):** Take a *real* wander trail already on disk from the S64 paired-read run (the FENCE-heavy one) — not a hand-made example — and run the Librarian + conclude steps on it. See whether a coherent kindred pile forms *and* whether it contains the known relevant nodes that are confirmed to be in that trail (the 3D-print conversation nodes S63 confirmed at specific hops).

**Mandatory precondition before the run — don't skip this:** A null result (no coherent pile) is uninterpretable unless you set it up right, because two completely different failures produce the same empty output:
- the trail didn't *contain* the relevant nodes (a problem with the *wander*, not the read), or
- the relevant nodes were there and the *read* failed to assemble them (a problem with the *mechanism*).

These have opposite fixes. To separate them: first have CC inventory what's actually in that specific trail, then pick the test question to fit material the trail *demonstrably contains*. Pick the question *after* seeing the trail. Then a null result cleanly indicts the read mechanism — which is the part that's never been tested. Pass-condition is "the known relevant nodes surfaced," **not** "a pile formed" (a pile forming is exactly what a false-success looks like).

**The fork on the far side:**
- Pile forms and contains the known nodes → the mechanism works on real input → next session builds Pollux.
- No pile (precondition met) → the read mechanism needs rework.
- A clean-looking pile forms *without* the known nodes → worst case: the read works but the underlying graph is too sparse to support it, which reopens the (currently deferred) question of rebuilding the graph substrate before building Pollux at all.

---

## Honest flags (don't let these ride silently)

- **Everything new is settled on logic, unproven on disk.** The "desk proof" that motivated the mechanism was run on a *hand-curated* example pile, not a real wander output. It validated the *read* on clean input and proved nothing about the wander or the read-on-real-input. The whole point of the gated run is to fix that. Don't treat §3.5/§6 as proven until the run says so.
- **The S64 trail is assumed-present, not verified.** The run dirs are gitignored by design (they live local + on the NAS, not in the repo). From the OC chat this session, only the S64 *plan* file was confirmable on HEAD — the actual deposited trail and the named relevant nodes are assumed to be on disk. CC must confirm the trail and those nodes exist before running, and stop if they're not where the spec expects.
- **The dampening term was written in from logic, not a fresh read.** S64 deferred writing the dampening fix into the docs pending Jake cold-reading 20–30 of the window-2 finds. S65 wrote it in from the logic + S64's on-disk receipt. The term's *necessity* is settled; its *calibration* still wants the pile data.
- **Roles:** OC (chat) plans and authors canon. CC (Claude Code) runs the terminal and touches disk under `wallaby-way/`. Jake bridges between them and is the only one who commits/pushes. Don't claim anything is committed, saved, or pushed — that's Jake's hands.

---

## Working-mode quick reference (full detail in JAKE-RULES)

- Discuss → confirm → build. Wait for "go" before building; propose freely before it.
- Full files, not diffs, for deliverables.
- Plain-prose questions only (no selection-widget tools).
- Counts always carry their unit; cite FLOOR_COUNTS, don't re-derive.
- End each reply with a one-line status line (turn / ET time via `bash date` / re-anchor count / destination-state-next).
- When something's been tried and failed a few times, step back and re-frame rather than tweaking the same approach.

Next session is S66 — pick your own working name for it if you like, or don't; it's bookkeeping, not a requirement.
