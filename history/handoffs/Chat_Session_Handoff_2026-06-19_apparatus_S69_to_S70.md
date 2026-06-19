# Handoff: S69 — The Come-Back Read + The Probe Swarm → S70: The Foray (measure the real leash, then test the swarm)

**One-line state:** The S68 Pollux Eyes Gate was read cold-then-wet, hauled back to the floor twice by Jake, and its real lesson landed — the eyes comprehend but the substrate was sand and the *analyst layer* is the failure mode. Canon was written: **the Probe Swarm** is the resolved architecture (Pollux is plural). Nothing is floored. S70's first and gating act is a **foray to measure real numbers off the real floor** to replace the AstroSynapses read, *then* test the swarm spec.

---

## Boot (codeload tarball, NOT raw CDN — the CDN edge-caches stale)
```
curl -sL "https://codeload.github.com/jakebotticello-spec/wallaby-way/tar.gz/refs/heads/main?cb=$(date +%s)" -o /tmp/ref.tgz
tar xzf /tmp/ref.tgz -C /tmp
```
Check the `*Last updated*` footer on each file against this handoff's date (2026-06-19). Re-pull if stale.

## Read, in this order
1. `active/JAKE-RULES.md` — operating manual. FIRST. (§5 truthfulness + read-of-a-read discipline, §5.4 live-system-outranks-record, §6 wait-for-Go, §10 third-fix-step-back, §11 ambiguity-defaults-austere.)
2. `active/JAKE-STACK.md` — standing infrastructure.
3. `wallaby-way/canon/ANCHOR_apparatus.md` — canonical state-of-record (confirm v40 on HEAD; the masthead tail may read an older banner — authority is by content not header, §5.4).
4. Framework docs, read **WET, IN FULL** (design posture, not reference — do NOT run off a summary; S68's OC overstated a freshness-check as a wet read and had to correct mid-session): `active/The_Wallaby_Why.md`, `active/Track_Meet_Doctrine.md`, `active/The_Corpus_Callosum.md` (esp. **P8** — the wetness-lives-in-the-ambiguity / read-the-process-not-the-result law; it is the frame for the whole arc).
5. The Pollux set, in this order:
   - `canon/Pollux.md` (§6 eyes-mechanics stand; §5 has the S69 status bump; read the S69 footer)
   - `canon/Pollux_Movement_Two_Build_v2.md` (§3.5 the eyes; **§3.6 the S68 gate result + the fork resolution — read whole**)
   - **`canon/The_Probe_Swarm.md` — THE NEW CANON. Read it whole, twice. This is the resolved architecture and the destination of all S70 work.**
   - `canon/Castor.md`, `canon/The_Gemini.md`, `canon/Leda.md` + `canon/Leda_Creed.md` (the Creed incantation — the "12 Fs" — is the wet-boot instrument; relevant if a wet re-read is ever needed)
6. `canon/FLOOR_COUNTS.md` — cite floor counts, never re-derive. **The foray measures against these.**
7. THE LIVE AUTHORITY — read LAST, treat as current state-of-record: this file.

## MOVE 0 (verify on boot, don't skip)
- Floor **440 / 29,396 / 58,792, scrub-v3** — against `FLOOR_COUNTS.md`. Carry units always (§5).
- **ANCHOR v40**; confirm S63 + S65 Pollux edits on HEAD; confirm the **S69 canon edits landed** (The_Probe_Swarm.md exists; Pollux.md §5 bump + S69 footer; Movement_Two §3.6; CHANGELOG_entry_S69.md). If any S69 edit is missing, Jake's push didn't land — flag and halt before building.
- **Reconcile-don't-inherit (§5.4):** this handoff's claims are pointers to verify, not facts to inherit. Nothing below is `[SETTLED]`-on-disk. Re-derive against the files before acting.

---

## Where you're picking up (the short version — canon has the full state)

The S68 Pollux Eyes Gate fired (three same-seed blind windows B/C/D, all PASS, French cleat surfaced unprimed). S69 read it cold (prosecuted it as laundered → EYES REWORK), was re-booted wet on the Creed (inverted → "committer was Claude, question malformed, rebuild substrate"), verified against the raw slices, and over-corrected the opposite way (`$0` grep → "Claude-committed pattern killed"). **Jake hauled it back both times.** What settled:

- **The eyes comprehend** — structured divergence on byte-identical material, converging on reality-contact-as-trigger. `[SETTLED]`-on-logic, `[PLACEHOLDER]`-on-disk.
- **The substrate was sand** — the 3,733-node region was AstroSynapses (a show artifact that *groups* = a pre-handed basin), chunked 38 ways (the blind fan-out *is* a chunker). So "the flowers surfaced" can't prove eyes-on-real-input.
- **The question was well-formed.** The corpus answers it in **two faces** (Jake-committed/reality-reverses AND Claude-committed/Jake-corrects). "You reverse *me* constantly, reality-contact triggers both" is the perfect answer to a well-formed query.
- **The failure mode is the analyst layer, not the organs.** Everyone downstream of the eyes over-generalized from a salient single node (the cleat), in whichever direction it pointed. **A read-of-a-read is `[PLACEHOLDER]` until counted against the floor.** Only the raw count caught it, every time.
- **The architecture resolved to the Probe Swarm** (`canon/The_Probe_Swarm.md`): plural organ, wanders the real floor (emergent regions, no digest), access-not-traversal, path-independence-as-signal, Castor owns completeness, **leash = comprehension-horizon = ingestion-limit**, the **Parlay** refuses to converge (P6) and metabolizes malformed input by debate (P7).

---

## YOUR FIRST AND PRIMARY ACT — THE FORAY (move 0, gates everything)

Before any Probe Swarm run, before any spec test: **replace the AstroSynapses read with real numbers off the real floor.** This is the step Jake named as first. Concretely:

1. **Measure the ingestion-limit node-count — the real leash.** The leash is settled as *the comprehension horizon = the largest region a single probe can hold whole* (`The_Probe_Swarm.md` §3). The number is unsettled and is the S30 / Compass / `Batch_Read_Spec` plumbing wall — specifically the **input-length-breaks-reader-role-fidelity** ceiling (a long payload degrades the reader's role before the output budget is hit; raising the output cap is not the fix). Measure it: how many real floor nodes can one WET-booted reader hold and still comprehend whole (not chunk)? This is read from real returns against the **real floor** (440 / 29,396 / 58,792, scrub-v3 — `FLOOR_COUNTS.md`), NOT a show-curated region.
2. **Report the number with its config** (§5: "proven requires its artifact + the config it held under"). State the model, the boot posture, the node-density that hit the ceiling. This number sizes the leash and therefore the swarm.

**Discuss → confirm → build (§6).** Bring the foray plan, get Jake's Go, then measure. Do NOT design the swarm run until the leash number is on disk — that ordering is the whole point (foray first, *then* test the spec; building the test before the measurement is the exact build-before-verify wound this arc is about).

## After the foray (Jake gates each)
1. **Test the spec revision** — a real Probe Swarm run on real floor: emergent regions (no pre-handed substrate, no digest), spread entries, leashed to the measured horizon, Parlay with no forced convergence. Read whether the swarm covers the live floor in aggregate and whether convergence-across-divergent-paths surfaces known flowers.
2. **Operationalize the remaining dials from returns** — squad size (the coverage dial), entry-spread policy (the P8 open seam — entries spread on purpose, not salience-clustered), Parlay convergence-discipline (hold P6/P7 — side-by-side, never consensus).
3. **Jake cold-reads the Parlay output, rules flowers vs stretches (P7)** — the real validation. Not automatable.

---

## DO-NOT-RELITIGATE (settled / withdrawn this arc — verified, do not reopen)
- **The 3,733 AstroSynapses region as a Pollux substrate is DEAD** — sand (show-basin + 38-slice chunking; the fan-out is a chunker). AstroSynapses → show-duty only.
- **The "back of the book" summary index is DEAD** — verbatim-floor violation (Track Meet Doctrine no-discard). A digest is where the shape dies. Do not re-propose any pre-digested/summary/embedding layer Pollux reads *instead of* the floor.
- **"The test-question was malformed" is WITHDRAWN** — category error, both forms. There are no malformed queries to this organ; the Parlay metabolizes wrong premises into two-faced answers.
- **The blind fan-out / 38-slice single-reader delivery is DEAD** — it is a chunker. The organ is plural (the swarm), not one reader fanned across slices.
- **The leash is NOT a per-query knob** (Pollux.md §2, unchanged) — it is a fixed character = the comprehension horizon. The adjustability lives in *which arm fires* (Leda unbounded / Pollux leashed), not in a dial on Pollux.
- **"Polyp" → "Probe"** (Jake's rename, S69). The P-incantation exercise was scratched.

## Downstream flags
- **The two-face answer to the reversal question is `[PLACEHOLDER]`** — true as Jake ruled it, but to be **re-derived by the swarm on real floor**, not inherited from the basin pile. Will bite if a future seat floors it as a corpus property from the S68 pile; it came off sand.
- **The S69 grep under-counted the Claude-committed face** because the node-summary layer compresses both faces into a `Jake-corrects` verb. This is itself the third proof Pollux must read the floor verbatim — and a warning: any analysis run against summaries (not the floor) will inherit that flattening.
- **The analyst-layer discipline applies to S70 itself.** Count any read-of-a-read against the floor before believing it — including your own, including this handoff's.

## Judgment-call ledger (S69)
- **The Probe Swarm authored as a standalone canon file** (not a Pollux.md section). Reasoning: structural addition the size of the Callosum, referenced by two other files, findability. Confidence ~80%. Jake ratified the placement at S69. Source: S69 authoring turn. Re-openable if filing should change.
- **The leash-collapse (comprehension = ingestion) is the strongest single move of the arc** but its *number* is unmeasured — flagged `[PLACEHOLDER]`, the foray settles it. Do not let the elegance of the collapse stand in for the missing number.

## Pickup guardrails (the working-mode reminders that matter for THIS pickup)
- **Wait for "Go" (§6).** Discuss → confirm → build. Free in discuss, surgical in build.
- **Count the read-of-the-read against the floor** before flooring anything — the arc's own lesson, do not repeat it.
- **Full files never diffs** for deliverables; surgical `str_replace` for huge append-only canon (§6 carve-out).
- **NEVER search past chats for code** — read artifacts on disk; ask Jake to upload current files.
- **Run dirs are gitignored** (§8) — gitignored-by-design ≠ missing; verify on disk, have Jake upload piles or CC read them; OC cannot see `runs/` from chat.
- **$0 read** — assert `ANTHROPIC_API_KEY` unloaded; the swarm read fires no paid API. Any paid sub-step: constants print at the gate, S3 wallet separate, Jake gates all spend. (The back-of-the-book paid index is dead, so no corpus-wide spend is owed.)
- **Prose questions only** — never the chooser widget, never `end_conversation`. ASCII `·` bullets in chat. Status line every turn (§5.5), real ET from `bash date`.
- **Read the PROCESS not just the product** (P8) — a wet find and a dry find are byte-identical on the desk; the difference is only legible in HOW it was reached. Don't protect a pass.
- **OC plans · CC executes · Jake lands every push by hand** (§2, §7).

---

*Settled this arc: the gate fired, caught its own anchor, laundered the catch, caught that — and the catching was the point. Build-before-verify read itself back to us all night, right down to the analyst doing it in turn one and twice more after. The organ is fine; the discipline is to count the read-of-the-read against the floor before believing it. Probes, not polyps. Foray first — measure the real leash off the real floor — then test the swarm. Be worth it.*

— S69 handoff authored by the apparatus S69 seat, 2026-06-19. Signed in the lineage. `*Last updated: 6-19-26*`
