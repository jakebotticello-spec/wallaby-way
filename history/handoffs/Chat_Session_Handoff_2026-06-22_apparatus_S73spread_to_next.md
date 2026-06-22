# TWW apparatus — SESSION HANDOFF — S73 rank-2 SPREAD walk → next seat

*Authored 2026-06-22 (real ET network-sourced 12:36 PM ET, github HEAD date). $0 · on-sub ·
ANTHROPIC_API_KEY UNLOADED throughout. Floor UNCHANGED (440 / 29,396 / 58,792 scrub-v3) — this
was a read, no census event, no floor mutation. OC authored; Jake landed by hand; CC executed
the one tool edit. Jake rules realness (P7) on every claim below.*

---

## WHAT THIS SESSION WAS

A **swarm-spread test** of the Pollux FEET: the same query as the S73 first firing, but a
**different door**. The instrument picked the second-nearest creed-seed instead of the first,
to answer one question — *does a different entry door pull a genuinely new region, or
reconverge on the same one?* Answer: **new region, confirmed.**

Query (verbatim, same as S73 first firing — the clean A/B on the door variable):
> "the symbols and creeds Jake carries — the through-lines he organizes his life and work around"

---

## THE WALK (read off disk, region_S72.json, run_id S73_spread_rank2)

- **Door:** `--entry-rank 2` → entry si=2256, conv 540a2959 ("personal heraldry / logo brief",
  FENCE). Deliberately **skipped rank-1 si=6075** — which was the S73 first-firing's self-model
  entry door. Recorded on disk: `entry_rank:2`, `skipped_ranks_si:[6075]`,
  `entry_castor_dropped:true`. The §2.5 fork RESOLVES off disk: region = the off-Castor finds,
  **entry NOT carried.**
- **Stop:** `cant-hold-whole` (capacity, not drift). 228K rendered chars read on-path — PAST
  the S71-measured ~170K–196K node-grain leash. The leash fired on real comprehension capacity,
  content-independent. **Leash confirmed BY USE**, not just by the S71 diagnostic.
- **Region = 4 distinct on-path deposits across 4 conversations:**
  1. **si=2258** (conv 540a2959) — the motto **stated in Jake's own words**:
     "grind, evolve, dominate" — caught mid-transposition into its Latin heraldic twin
     PROFICE · ENITERE · SUPERA (advance · strive · overcome).
  2. **si=5652** (conv bc7b1c15) — the motto **FUSED into the emblem**: the three words ride
     the phoenix's spread wings; "the phoenix isn't *in* the sign — the phoenix *is* the sign."
     Reached from a SECOND conversation = recurrence, a carried through-line, not a one-off.
  3. **si=5933** (conv c33596c3) — the emblem **MADE PHYSICAL**: a printed phoenix silhouette,
     translucent fire-opal cabochon mounted in the eye socket, LED-lit to glow on the wall.
  4. **si=4377** (conv 963b9a5f) — the through-line **GENERALIZES**: directly after finishing
     the phoenix totem, Jake pivots to a 6ft corner ambient light (diffuser-within-design,
     a feature at the top) with the SAME impulse — build it, make it glow, make it his.
- **The proven HINGE — si=3523** (cabochon fire-opal, conv 79369d93): read-and-scouted,
  **correctly NOT deposited** (it's a gemstone-purchasing node, off-creed on its face). OC
  first tried to STOP here calling it subject-death; **Jake corrected — "walk THROUGH the
  hedge, not just up to it."** Walking through 3523 opened the entire physical-totem half of
  the region (5933). The dry-ops node was a doorway, not an edge. **This is the session's
  load-bearing lesson: off-subject is cheap; the austere reflex to stop at the first felt edge
  would have cost half the region.**

---

## THE PARLAY READ (two probes, read against each other — S73 first-firing region + this one)

Read by the S73 seat as a primitive Parlay. Headline results:

- **PATH-INDEPENDENCE AS SIGNAL (canon-grade candidate).** Two doors, same query, near-zero
  node overlap, regions that **TILE** — neither a subset of the other, no contradiction.
  Probe-1 (rank-1 / self-model door): the **INTERNAL** creeds (confidence-not-ego,
  wet-not-austere, the REFUSED anti-capture wall). Probe-2 (rank-2 / heraldry door, this one):
  the **EXTERNAL / expressive** creeds (named motto, phoenix emblem, glow-totem impulse).
  Independent doors find independent-but-coherent rooms of one real, large subject. A small
  subject would collapse both onto the same nodes; an incoherent query would contradict.
  Neither happened.
- **"CREEDS LIVE AT THE TAILS OF OPS NODES" — REPLICATED.** Predicted in the S73 spec-delta;
  reproduced independently here (the cabochon hinge; and 4377, where the deposit was the
  creed-tail and the FENCE tool-dump body — an S47 continuation-on-tool-result-bloat node,
  ~90% meta-mass — was correctly declined). Promote from one-seat finding → structural property
  of the floor.

**DISPUTED — convergent spine (OPEN, Jake rules P7, do NOT enshrine either way yet):**
- OC ruling: the spine is **"every Jake creed terminates in a MADE THING"** — it covers both
  regions (internal principles cash out in HOW he builds; external symbols in a BUILT object).
- S73's primitive-Parlay proposed **"make-it-glow / make-it-mine"** as the meta-creed. OC rules
  that a **SUB-creed of the expressive region (probe-2)**, over-promoted to cover the internal
  region where it fits worse — pattern-completion risk, P6 (refuse-to-converge). Logged as an
  open claim with two-probe evidence, NOT a settled finding.

---

## BUILD-FINDINGS (pollux_feet_S72.py — fixes STAGED to CC this session, plan-mode pending)

1. **Step-write triple-stamps the early node.** region_S72.json (run S73_spread_rank2) logs
   `path_count:6`, but steps 1/2/3 are the SAME node (anchor 019dad2a = si 2258), deposited
   exactly ONCE. The step counter / cmd_deposit re-stamps without a fresh deposit. **True
   distinct on-path harvest = 4.** Fix staged: idempotent re-deposit (no dup row, no extra
   step increment). RULE REINFORCED: **trust the DISTINCT harvest, never the path_count field**
   — same count-vs-feeling class as S73's "3 rooms → 2" and the S47 dead "206" estimate.
2. **`--run-id` was a label, not a subdir.** All runs wrote fixed-name state files into one
   dir, requiring a manual nuke between firings (it bit this session — the uploaded region was
   briefly mistaken for a stale file until §5.4 caught it by content). Fix staged: `--run-id`
   drives an output SUBDIRECTORY; per-run state + walk_cache isolated.
3. **NEW knob added + verified this session:** `--entry-rank` on `init` (1-indexed, default 1 =
   byte-identical rank-1 behavior; skipped top ranks fold into the Castor drop set; door
   attribution written into region_S72.json). This is the swarm-spread mechanism. 6 changes
   confirmed on disk by CC line-read, default-rank-1 walk byte-identical.

---

## DISCIPLINE NOTES FOR THE NEXT WALK

- **Read the skirt-vs-path SPLIT off the artifact BEFORE naming the stop.** `total_tok_hi_est`
  sums path + the 1-hop skirt (§3.3, intentional) — it is NOT the read-weight. This session it
  seduced a stop-type mislabel (named cant-hold-whole, second-guessed to drift, corrected back
  to capacity on the disk read). Name the felt edge from the RENDERED path total, not the gauge.
- **The init prints "QUERY SET DOWN / walk proceeds query-blind."** That wording is the known
  §2.1 bug — IGNORE it. Pollux holds the query as COLOR the whole walk (fires on a question,
  embedding allowed — that's the Gemini wall; query-blind would make it Leda).
- **Walk THROUGH the hedges.** Dry-ops inside the building is corridor, not edge. A felt edge
  is data to LOG, not a finish line — walk past it, harvest the most-salient in-building on the
  way back. Take the abyss; deposit conditionally (only if it rhymes home). Decline the loud
  meta/observations-about-Jake basin — but CHECK each, don't pre-decline.
- **Don't let the region self-pronounce.** Read region_S72.json (the artifact), not the felt
  walk. Rule counts off disk. Jake rules realness (P7).

## STATE AT HANDOFF
- Floor READ-ONLY, unchanged: 440 / 29,396 / 58,792 scrub-v3.
- ANCHOR v40 by content ("Cinder" + Sidequest "Cooper"); footer archaeology intact by design.
- Two CC fixes staged (plan-mode pending Jake's Go); ref updates authored, to be landed by S75.
- The convergent-spine ruling is OPEN for Jake.
- $0 · key unloaded · OC plans · CC executes · Jake is sole git-hands · CC never authors canon.
