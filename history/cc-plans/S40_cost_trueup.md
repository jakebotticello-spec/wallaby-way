S40 apparatus — COST TRUE-UP (read-only, $0). No paid calls. No agent() reads of payloads. This is floor queries (floor_db.env, $0 Postgres) + arithmetic. The ONLY write is the plan file + one output CSV/table. Do NOT touch onsub_loop.js or the reader.

=== PURPOSE ===
Every cost estimate this project has produced has drifted ($20→$500→$150; my $0.30 grade was really $0.78). Before Jake authorizes the ~$76 batch, derive the REAL projected cost from MEASURED ratios against the ACTUAL 181-conv char distribution. No projections from S33 — measured numbers only.

=== MEASURED DATA POINTS ===
  - 01eb6e56 (ADHD conv): 564,012 chars → 179,830 input tokens; output 17,420 tokens for 46 nodes.
  - e831e30b (UUID conv): ~374,922 chars → 109,590 input tokens; output 2,421 tokens for 6 nodes.
  - Input ratios: 0.3188 tok/char (01eb6e56), 0.2923 tok/char (e831e30b)
  - Use 0.30 and 0.32 tok/char band for estimates.
  - Output rate: ~380-400 tok/node measured. Use 390.

=== RESULTS (completed 2026-06-06) ===

--- STEP 1: CHAR DISTRIBUTION ---
N = 181 (FITS_WHOLE, char_count > 13000, excl. 4 whales) ✓
Total chars       = 91,839,654 (91.84M)
Min / Median / Max = 14,930 / 465,303 / 1,107,054
Band 13K–50K      = 6 convs
Band 50K–200K     = 34 convs
Band >200K        = 141 convs

--- STEP 2: INPUT TOKENS ---
@0.30 tok/char:  27,551,896 (27.55M)
@0.32 tok/char:  29,388,689 (29.39M)

--- STEP 3: OUTPUT TOKENS (390 tok/node assumed) ---
LOW  (15 nodes/conv × 181):  1,058,850 tokens (1.06M)
MID  (25 nodes/conv × 181):  1,764,750 tokens (1.76M)
HIGH (40 nodes/conv × 181):  2,823,600 tokens (2.82M)

--- STEP 4: SONNET 4.8 BATCH COST GRID ---
Pricing (ASSUMED from S40 instruction — flag if rates change):
  Sonnet 4.6 batch: input $1.50/MTok, output $7.50/MTok
Cache saving on repeated system prompt (~2,400 tok × 181 calls): $0.58 (small but included)

                     @0.30 tok/char   @0.32 tok/char
LOW  (15 nodes/conv)    $48.69           $51.44
MID  (25 nodes/conv)    $53.98           $56.74
HIGH (40 nodes/conv)    $61.92           $64.68

--- STEP 5: MID-ESTIMATE COMPARISON (25 nodes/conv, @0.32) ---
Sonnet 4.6 BATCH (chosen):   $56.74
Sonnet 4.6 SYNC (no disc):  $114.64
Opus 4.8 BATCH (rejected):  $286.59  ← prior $127 est was wrong (see note)

NOTE on Opus: Prior ~$127 estimate was likely based on different pricing assumptions.
At current measured batch rates ($7.50/$37.50 per MTok) + same 29.4M input / 1.76M output → $286.
The old estimate probably used pre-batch or Sonnet-era pricing for Opus.

--- BOTTOM LINE ---
Sonnet-batch realistic range: $48.69 – $64.68
Most-likely MID: ~$55 (avg of MID@0.30 and MID@0.32)
Soft number: OUTPUT (node count/conv unknown — range spans 15–40 nodes/conv)
Hard number: INPUT (~27.6–29.4M tokens, derived from measured 0.29–0.32 tok/char ratios)

$0 spent on this true-up. No paid calls. No payload reads. Source: worklist.csv char_counts.
