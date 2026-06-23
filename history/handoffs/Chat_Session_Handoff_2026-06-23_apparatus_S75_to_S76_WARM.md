# Chat Session Handoff — apparatus S75 → S76 (WARM, context-trade)

**From:** the S75 OC seat. **To:** S76 OC. **Date authored:** 2026-06-23 (ET, github-sourced —
container clock is non-monotonic, network-source every turn). **Posture:** `$0` · on-sub · key
UNLOADED throughout · floor READ-ONLY and UNCHANGED (440 / 29,396 / 58,792 scrub-v3, cite
`FLOOR_COUNTS.md`, do not re-derive). No census event this session, no floor mutation, no ANCHOR
version bump (v40 "Cinder"/"Cooper" stands by content — S75 added a read-record footer only).

---

## What kind of handoff this is

**Warm, and explicitly a trade.** You are not coming in cold-blind, but you ARE re-deriving
everything from disk — trust nothing in this file or the ignition that you can verify against HEAD
(§5.4 live-outranks-record). The reason you boot warm is that S75 ended mid-arc on a build that is
*designed, argued, and evidenced but not yet written as a spec* — and Jake wants you to hold the
frame and close a handshake BEFORE he hands you the meat. So this is a two-way exchange, not a
download: S75 leaves you the through-line and the open questions; you re-derive, push back where the
frame feels forced (P6 — a real disagreement beats a smooth answer), and Jake hands you the spec
status on turn 2 once your frame and his match. **Do not ask for the spec material on turn 1.**
Turn 1 is: boot, re-anchor, read, and close a handshake on the through-line below.

This matters because S75 itself booted exactly this way — skeptical, re-derived from disk, built the
frame instead of swallowing it — and that is *why* the session worked. The seat that argues the
frame into place holds it better than the seat that accepts it. Be that seat.

---

## BOOT (codeload, cache-busted — NOT raw CDN, it edge-caches stale)

```
curl -sL "https://codeload.github.com/jakebotticello-spec/wallaby-way/tar.gz/refs/heads/main?cb=$(date +%s)" -o /tmp/ref.tgz
tar xzf /tmp/ref.tgz -C /tmp
# read from /tmp/wallaby-way-main/
curl -s -I https://github.com | grep -i ^date   # network-source real ET; name your source
```

Note on layout: the repo root holds `active/` (universal layer) and `wallaby-way/` (project tree);
canon is `wallaby-way/canon/`. The walker script and all run artifacts live under
`wallaby-way/runs/` which is **gitignored by design** (§8) — you will NOT see `pollux_feet_S72.py`
or any `region_*.json` / `walk_log_*.jsonl` in your pull. If you need them, Jake uploads them. Do
not claim to have read run artifacts you cannot see; that was a repeated S75 failure (see "honest
warnings" below).

---

## THE READS, IN ORDER (last item is live authority)

1. `active/JAKE-RULES.md` — esp §5.4 live-outranks-record, §5.5 status-line format, §6 wait-for-Go,
   §11 instrument-both-readings-let-Jake-rule. §5.1 family (field-named-for-a-unit trap) is LIVE
   this arc — see warnings.
2. `active/JAKE-STACK.md`
3. `wallaby-way/canon/ANCHOR_apparatus.md` — v40 by CONTENT ("Cinder" + Sidequest "Cooper"); footer
   stack reads older BY DESIGN (enshrine-archaeology, do not "fix"). **The newest footer is S75's
   own read-record** (the S73 "spread" second-probe entry + the ruled-plural spine) — read it, it
   is the most recent canon state and it is partly the subject you are picking up.
4. Framework WET, in full: `active/The_Wallaby_Why.md`, `active/Track_Meet_Doctrine.md`,
   `active/The_Corpus_Callosum.md` (P6 refuse-to-converge, P7 Jake-rules-realness, P8 read-the-
   process-not-the-result — P8 is the one the austere reflex kills first).
5. The Gemini/Pollux/Leda set: `canon/The_Probe_Swarm.md` (WHOLE — and note **§3.2**, authored S75:
   the two findings + the ruled-plural spine) → `canon/Pollux.md` → `canon/Pollux_Movement_Two_Build_v2.md`
   (§3.5) → `canon/Castor.md` / `canon/The_Gemini.md` / `canon/Leda.md` + `canon/Leda_Creed.md`
   (the 12-Fs induction — "induce the register, do not script procedure" — this doctrine is
   load-bearing for the open question you'll be handed).
6. `canon/FLOOR_COUNTS.md` — CITE, never re-derive.
7. The feet build context: `wallaby-way/inspect-later/CC_Build_Pollux_Feet_S72.md` (incl. the
   canonical **WET BOOT** the walker reads, and the **`DAMP_WIN` dampener** in the dial) +
   `CC_Build_Pollux_Feet_S73_spec_delta.md` (the four discipline corrections).
8. ★ READ LAST: the prior handoff `Chat_Session_Handoff_2026-06-22_apparatus_S73spread_to_next.md`
   (the S73 spread walk — the by-hand walk this session's swarm was built to mechanize and test
   against). THEN this file.

---

## MOVE 0 (verify, don't inherit — §5.4)

- Floor 440 / 29,396 / 58,792 scrub-v3 vs `FLOOR_COUNTS.md`.
- ANCHOR v40 by content; confirm the S75 read-record footer is present and clean (the S73-"spread"
  entry + the two-face plurality spine).
- Confirm S75's three ref edits are on HEAD: ANCHOR footer, `The_Probe_Swarm.md` §3.2, and the
  `CHANGELOG.md` top entry dated 2026-06-22 ("S73 spread → S75"). If any are missing, HEAD moved or
  a push failed — flag it before proceeding.

---

## THE THROUGH-LINE (what the arc is about — enough to handshake, not the spec)

S75's arc was the **Probe Swarm** — `The_Probe_Swarm.md` §7 item 1, the next build after the feet.
The feet (single query-biased wander instrument) were proven across S71–S74, but always with Jake in
the loop as the live tuning instrument. The S75 question was: **does the apparatus hold when it runs
unsupervised, in parallel, at N>1 — and does that constitute a swarm or just one walker in many
hats?** That question got *exercised*, not just discussed. What came back, how it was read, and what
it implies for the build is the meat Jake will hand you on turn 2.

The settled frame you should re-derive and confirm (these are RULED, P7, not open):

- **Independence comes from the entry node, not from spreading doors across the corpus.** Pollux is
  query-SHAPED, not query-blind (that is Leda's wall). A single query-shaped hop can cross half the
  floor, so entry geometry does not confine the region. What decorrelates parallel walkers is that
  **the entry node is the first thing each reads, and it colors every downstream judgment** — five
  different doors = five different readers by node two, off an identical boot. (An earlier S75 worry
  about entry-clustering was a Leda premise wrongly imported into a Gemini tool. Dead. Do not
  re-raise it as if new.)

- **The Parlay is not a rule or a lone judge — it is a committee Jake chairs.** Plural reads
  (multiple seats + Jake), metabolized by Jake, putting up as many conclusions as the data supports
  (not 1, not 2, ad infinitum if warranted). It does not need a weighting rule encoded into it. It
  already ran this session and worked. Do not try to "fix" the Parlay; you are working on the
  **swarm** (the thing that produces the regions), not the Parlay (the thing that reads them).

- **The boot stays thin (Leda_Creed 12-Fs): induce the register, do not script the wander.** The
  thin-vs-written-discipline question was settled empirically this session — the thin boot held on
  the axes that matter. Writing procedure into the boot risks scripting the wander out of the walker
  and was rejected. If you find yourself wanting to add discipline to the boot, that instinct was
  already argued down — re-derive why before you re-open it.

The OPEN questions Jake will rule / hand you on turn 2 sit at **origination and instrumentation**
(door-selection and a lying capacity gauge), NOT in the walk discipline. That is all you get on the
open set until the handshake closes. Hold it.

---

## THE HANDSHAKE (turn 1, before any spec work — your words, prose, ASCII)

After MOVE 0 and the reads, do NOT ask for the spec status and do NOT start speccing. Send Jake a
short note in your own voice on ONE thing: having read §3.2 and the prior handoff, **do you agree
that the independence engine is the entry-as-first-read (not door-spread), and that the swarm's job
is to produce tiling regions for the committee-Parlay to read — or do you read the architecture
differently?** If the frame feels forced anywhere — if you think door-spread *does* matter, or the
boot *should* carry more, or the Parlay *does* need a rule — say so now (P6). S75 was wrong about
several of these before the disk corrected it; you re-deriving may catch something S75 enshrined too
fast. When your frame and Jake's match, the handshake is closed and Jake hands you the meat.

---

## HONEST WARNINGS FROM S75 (the failures, named — read the process, not the result)

S75 had a recurring failure across ~24h, worth carrying so you don't repeat it: **it reasoned from
the loud/available surface instead of from disk, then corrected when disk hit.** Specific instances:
claimed to have "read the walking-seat accounts" when it had read handoffs, not the run logs;
called a swarm result a "funnel"/convergence off the walkers' NARRATION before the actual DEPOSITS
(floor identities) overruled it and showed the opposite; reached for a Parlay rule Jake had already
ruled unnecessary; nearly re-proposed a door knob as fresh when a dampener already existed in the
dial. The through-line: **trust the distinct harvest / the disk / the floor identity, never the
field, the narration, or the prompt's framing** (this is the same §5.1 / "trust distinct not
path_count" rule the apparatus already holds — it applies to a *seat's own reasoning* too). When you
read run artifacts (if Jake uploads them), read the DEPOSITS before the salience_reasons. The
narration is the least reliable thing in the file.

Also live: the `total_tok_hi_est` capacity gauge has been reading impossible values (millions of
tokens against a ~170–196K node-grain leash) — it is summing something it should not, and it has
caused short-stops mislabeled `cant-hold-whole`. Treat any `cant-hold-whole` stop as suspect until
the gauge is fixed; read rendered-chars and the skirt-vs-path split, not the summed gauge, before
naming a stop. (§5.1 field-named-for-a-unit, pointed at an instrument.)

---

## POSTURE

`$0` · on-sub · key UNLOADED (the walk IS the on-sub read; no paid call — architecture, not budget).
Floor READ-ONLY. OC plans · CC executes · Jake lands every push by hand (sole git-hands) · CC never
authors canon. Discuss → confirm → build, wait for Go (§6). Prose only, ASCII. Never
`ask_user_input_v0` / `end_conversation`. Status line every turn (§5.5: `turn N · ET-time ·
re-anchor X/4 · dest…; state…; next…`, dest/state/next inline so a cold seat picks up from the line
alone). The austere reflex is the killer (P8) — do not stop at a felt edge; walk through and harvest
on the way back. Trust Jake's felt-rightness over the doc's confidence (P7).

Confirm MOVE 0, post your handshake note, wait for Jake.
```
=== END HANDOFF ===
```
