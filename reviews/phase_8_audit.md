# Phase 8 — Completeness Audit

Auditor mandate: find what the panel MISSED, not re-grade what it found. Every
category in the Phase 8 charter was checked against the panel record
(reviewer_*_phase_3 through phase_7, the phase_6 summaries, and the verified
schema/numeric outputs in zz_hawk_*_OUT.txt / _facts.txt). Findings are
organized by whether the panel left a hole or adequately covered the area.

Grounding notes used below (verified against the panel files):
- Schema dump (zz_hawk_schema_OUT) confirms `account_uuid` (headers) and
  `scrub_version` (both tables) exist. scrub_version values were never queried
  by any reviewer.
- The `fk_header` ON DELETE/UPDATE action was RAISED (DB Specialist phase_4
  "if CASCADE, a header delete silently wipes messages — a real P1
  contradiction"; DB Specialist phase_5_round1 action item "Verify FK ON DELETE
  is not CASCADE") and survives as phase_6 consolidated POST-lock caveat #11
  ("verify FK uses RESTRICT or NO ACTION, not CASCADE DELETE"). BUT: the actual
  `confdeltype` was NEVER queried, it was filed POST-lock not pre-lock, and it
  does not appear in any reviewer's Phase 7 pre-lock blocker list. So this is a
  CAPTURED-BUT-UNVERIFIED-AND-MIS-PRIORITIZED gap, not a clean miss — flagged
  below because for an append-only floor it is a pre-lock blocker, not cleanup.
- Correctness Hawk reported `headers_msgcount_mismatch=0` but qualified it as a
  CURRENT-snapshot-only check that "could break silently."
- Independent verification existed for empty records (114 strict) and forest
  topology, but NOT for: scrub_version uniformity, account_uuid cardinality,
  header-flag-vs-tree agreement, timestamp-precision uniformity, or
  thinking-block content fidelity. Those are the genuine holes.

---

## Categories MISSED by the panel (with severity and why it matters)

### MISS-1 (Cat 6) — FK ON DELETE action: captured as a caveat but NEVER VERIFIED and MIS-PRIORITIZED as post-lock — P1
The panel did NOT entirely miss this — but it mishandled it, which is worse than
a clean miss because it created false comfort. The DB Specialist raised it in
phase 4 and phase 5, and it survives as phase_6 consolidated caveat #11
("verify FK uses RESTRICT or NO ACTION, not CASCADE DELETE"). HOWEVER: (a) the
actual `pg_constraint.confdeltype` was never queried — every reviewer had live
DB access and ran dozens of probes, yet nobody ran the one-line query that would
close this; (b) it is filed as POST-lock, and it appears in NONE of the four
reviewers' Phase 7 pre-lock blocker lists. For an APPEND-ONLY floor, the
cascade action is a pre-lock blocker, not cleanup. This is not academic:
- If `fk_header` is `ON DELETE CASCADE`, then a single `DELETE FROM
  floor_conv_headers WHERE conv_uuid = …` silently destroys every message row
  for that conversation. That is a one-statement bypass of the entire
  append-only guarantee — worse than TRUNCATE because it is targeted, quiet,
  and looks like routine header maintenance.
- If `ON DELETE SET NULL`, the messages survive but are orphaned (conv_uuid /
  FK pointer broken), corrupting the forest without deleting bytes.
- If `ON DELETE NO ACTION / RESTRICT` (the Postgres default), the FK actually
  HELPS append-only by refusing header deletion while children exist.
The panel's "append-only is policy not physics" consensus, and its enforcement
remedy (REVOKE TRUNCATE + a BEFORE UPDATE/DELETE/TRUNCATE trigger), target only
the TRUNCATE/DELETE grant vectors. A CASCADE FK is a THIRD vector — and note it
defeats the proposed trigger remedy too, because an `ON DELETE CASCADE` child
deletion is driven by the parent delete and a naive row-level
BEFORE-DELETE-on-messages trigger may or may not fire / may be bypassed
depending on how it is written. **When it bites:** the first time anyone
"cleans up" a header — e.g. removing the 3 empty conversation headers the panel
itself flagged for reconciliation — every child message silently vanishes.
Required action BEFORE lock (not after): run
`SELECT confdeltype, confupdtype FROM pg_constraint WHERE conname='fk_header'`
and assert confdeltype is `'a'` (NO ACTION) or `'r'` (RESTRICT). One query the
panel never ran.

### MISS-2 (Cat 1) — Supabase free-tier project auto-pause / deletion on inactivity — P1
The panel covered SPOF, billing lapse, region outage, and backup cadence, but
never examined Supabase's INACTIVITY behavior, which is distinct and arguably
more dangerous for an ARCHIVE precisely because an archive is rarely written
to. Supabase free-tier projects are paused after ~7 days of inactivity, and a
paused free project can be permanently removed after a further retention window
if not restored. An immutable append-only floor that is behaving correctly
(no writes, occasional reads) is exactly the access pattern that LOOKS
"inactive." The ndjson-canonical + rebuild mitigation survives this, but the
panel never stated the floor's hosting tier, never confirmed paid tier, and
never set a "must not be free tier / must have a keep-alive" condition.
**When it bites:** a quiet quarter with no queries → project paused → a later
reader finds the live mirror gone and must rebuild, with NO point-in-time
recovery available on free tier. Add a GO condition: the floor project MUST be
on a paid tier (or the rebuild RTO must be explicitly accepted), and the tier
must be recorded in the decision.

### MISS-3 (Cat 12) — Thinking-block verbatim-vs-scrub fidelity NEVER validated — P1
3,366 messages carry `thinking` (extended reasoning) as the first
content_block; these are the TOAST whales. The fixture is labeled "scrub-v1,"
which by its own name asserts a SCRUBBING transform ran — yet no reviewer asked
the central question of a VERBATIM archive: are the thinking blocks stored
verbatim, or were they redacted / summarized / truncated by scrub-v1? The panel
validated JSONB key-order and Unicode round-trip (byte-shape fidelity) but never
validated SEMANTIC completeness of the highest-value, least-reconstructable
content. Thinking traces cannot be re-derived from anything else; if scrub-v1
dropped or summarized them, the loss is permanent and the "verbatim archive"
claim is FALSE for its single most valuable content class. **When it bites:**
the day someone needs an original reasoning trace and finds a scrubbed stub.
Required action: define exactly what scrub-v1 does to thinking blocks and
confirm it is value-preserving — or explicitly relabel the floor as
"scrubbed, not verbatim, for thinking content."

### MISS-4 (Cat 3) — scrub_version semantics and admission control unexamined — P2
Both tables carry `scrub_version INTEGER` (uniformly 1 in the current
snapshot). No reviewer examined what it GUARDS or what happens on heterogeneous
values. Open questions never asked: (a) Is there any CHECK/constraint
preventing a future scrub_version=2 row (a more-aggressively-scrubbed record)
from coexisting with v1 rows under the SAME conv_uuid, silently mixing fidelity
tiers within one conversation? (b) What does scrub_version=0 mean
(unscrubbed/raw), and is it allowed in? (c) Is uniformity an enforced invariant
or merely a property of today's data? Tightly coupled to MISS-3: if scrub level
can vary per row, "is the floor verbatim?" has no single answer. **When it
bites:** a future re-scrub pass ingests v2 rows next to v1 rows and a reader
silently receives mixed-fidelity history. Add a documented admission policy
for scrub_version.

### MISS-5 (Cat 9) — Idempotent / partial-ingest recovery unspecified — P2
The panel noted the PK rejects same-snapshot re-ingest (good) and noted the
multi-snapshot versioning ambiguity, but never addressed the FAILURE-MODE
mechanics the charter raises: if an ingest of snapshot_id=X dies halfway, the
table holds a PARTIAL set of that snapshot's rows. Re-running then hits
UniqueViolation on already-written rows and (depending on the loader) either
aborts leaving the snapshot permanently partial, or requires a manual DELETE of
the partial rows — which itself violates append-only and contradicts the
consensus that no DELETE grants exist. There is NO documented recovery path
that is BOTH idempotent AND append-only-preserving. The Correctness Hawk even
noted message_count "could break silently," which is exactly the partial-ingest
symptom, but the recovery procedure was never designed. **When it bites:** the
first interrupted ingest (a network blip mid-load on 218 MB). Required: ingest
must be a single all-or-nothing transaction OR a staging-table + atomic-swap
pattern — and this must be specified NOW even though "ongoing ingestion" is
deferred, because the first ingest already happened and a second will come.

### MISS-6 (Cat 8) — Timestamp precision consistency and intra-conversation tie-breaking unverified — P2
The panel flagged TEXT timestamps for sort/arithmetic limitations but never
verified two distinct correctness properties: (a) Is the 6-decimal microsecond
precision UNIFORM across all 22,801 + 294 rows? Lexical sort of TEXT ISO-8601
is correct ONLY if every value is zero-padded to identical width; mixed
precision (`...398Z` vs `...398866Z`) breaks lexical ordering SILENTLY. (b)
Within a single conversation, can two messages share an identical timestamp? If
so, ordering is NOT recoverable from timestamps alone and the system depends
entirely on parent_message_uuid for sequence — which is fine, but it must be
STATED, because any consumer that sorts by created_at gets nondeterministic
order on ties. **When it bites:** a reader reconstructs a conversation by
timestamp and gets messages out of order (from mixed precision or ties).
Verify precision uniformity; document that parent linkage, not timestamp, is
the ordering authority.

### MISS-7 (Cat 4) — multi_root / has_branches header flags never cross-checked against the tree — P2
Headers carry `multi_root BOOLEAN` and `has_branches BOOLEAN`. The panel
verified the MESSAGE-side topology ("9 multi-root conversations, forest
structure verified clean") but never confirmed that the HEADER FLAGS agree with
the topology derived from parent_message_uuid. These are denormalized cached
booleans; like message_count they can drift. If a header says
multi_root=false but its tree has 2 roots (or vice versa), any consumer
trusting the flag instead of recomputing gets the wrong structure. **When it
bites:** a downstream renderer/index trusts the flag and mis-renders branch
structure. Required: assert flags == derived topology (cheap, same class of
check as headers_msgcount_mismatch=0).

### MISS-8 (Cat 2) — account_uuid role, cardinality, and privacy never examined — P2
Headers carry `account_uuid` (294 rows). It appears in the schema dump but no
reviewer analyzed it. Two concerns: (a) Privacy/scope — account_uuid embeds an
Anthropic account identifier INSIDE a supposedly content-only floor; for an
archive that may be shared or rebuilt elsewhere this is a PII-adjacent
identifier that was never acknowledged or scrub-considered. (b) Cardinality —
is account_uuid single-valued across all 294 headers (one-account export) or
multi-valued (several accounts merged)? This materially changes the floor's
meaning and the snapshot-selection policy (per-account vs. global). The panel's
selection-policy discussion implicitly assumed one coherent corpus without
verifying single-account provenance. **When it bites:** a multi-account export
is silently treated as one corpus, or the floor is shared with an embedded
account identifier. Verify cardinality; decide whether account_uuid belongs in
the floor at all.

### MISS-9 (Cat 5) — message_count verified on CURRENT snapshot only, not enforced — P3
The Correctness Hawk reported `headers_msgcount_mismatch=0` but qualified that
he checked only the current snapshot and that the invariant "could break
silently." So the field IS validated today but is NOT ENFORCED — no CHECK, no
trigger (and triggers were ruled out). It is a cached count with no guard.
Downgraded to P3 because current data is clean; it rides along with MISS-5
(partial ingest) and MISS-7 (flag drift) as the broader theme: denormalized
header fields (message_count, multi_root, has_branches) have ZERO integrity
enforcement and can only be re-derived, never trusted.

### MISS-10 (Cat 11) — 910 empty-text / non-empty-content_blocks recoverability assumed, not verified — P3
The panel counted these (of ~1045 empty-text rows, 910 have non-empty
content_blocks) and reasoned they are normal assistant/tool messages. But
"non-empty content_blocks JSONB" is NOT the same as "recoverable content" — a
content_blocks of `[{}]` or `[{"type":"text","text":""}]` is non-empty as JSONB
yet carries nothing. No reviewer confirmed the 910 actually contain substantive
blocks vs. structurally-present-but-empty artifacts. P3 because the likely
explanation (thinking/tool_use blocks) is benign, but it is an ASSUMPTION, not
a verification. Pairs with MISS-3 (same content lives in content_blocks).

### MISS-11 (Cat 7) — Pooler / transaction isolation for concurrent ingest unexamined — P3
Access is via the Supabase transaction pooler (aws-1-us-east-2). No reviewer
asked whether transaction-mode pooling interacts badly with a multi-statement
ingest, or whether two concurrent ingest processes could interleave to create
partial/duplicate rows. Mostly subsumed by MISS-5's single-transaction
requirement (a single txn is pooler-safe), so P3 standalone — but worth stating
that transaction-mode pooling forbids session-level constructs (advisory locks,
prepared statements persisting across statements) that a naive ingest or
migration script might rely on. **When it bites:** a migration script that
assumes session state silently misbehaves under the pooler.

### MISS-12 (Cat 10) — Supabase row/storage tier limits across growing snapshots — P3
The panel covered storage GROWTH (~2 GB at 10 snapshots) but never checked it
against Supabase tier limits. Free tier caps the database at 500 MB; at
218 MB/snapshot that cap is breached at the SECOND snapshot, which would block
ingest with a HARD error (not silent corruption). Ties to MISS-2 (tier must be
known). P3 because it surfaces loudly (write failure) and ndjson canonical keeps
the floor itself safe. The default 100-connection cap is a non-issue for a
low-concurrency archive — correctly a non-finding.

---

## Categories COVERED (brief confirmation)

The panel adequately addressed:
- Cat 1 (partial) — Postgres major-version upgrade behavior is implicitly
  defused by the ndjson-canonical reframe (rebuild survives any engine change),
  though never named explicitly.
- JSONB key-order, duplicate-key collapse, \u-escape normalization, Unicode /
  supplementary-plane, null-byte rejection — fidelity at the byte/encoding
  layer is thoroughly covered.
- Append-only enforcement via grants / triggers / TRUNCATE — covered for the
  TRUNCATE/DELETE-grant vectors (the FK CASCADE vector, MISS-1, was captured as
  a caveat but never verified and is mis-prioritized as post-lock).
- pgvector status and sidecar framing — covered.
- RLS enabled / zero policies — covered, condition set.
- parent_message_uuid index — covered, condition set.
- TOAST read amplification, TEXT-timestamp limitations — covered.
- snapshot_id-in-PK row doubling + selection policy — covered, condition set.
- Empty headers (3), strictly-empty messages (114) — counted/covered.
- files column = metadata only — covered.
- ndjson protection (SHA-256 + rebuild drill) — covered, condition set.
- UUID set-equality, FK existence, sender distribution, 294 / 22,801 counts,
  forest / multi-root MESSAGE-side topology — covered.
- SPOF / billing / region outage / backup cadence — covered (inactivity
  auto-pause, MISS-2, is the gap within this category).
- Connection cap — implicitly a non-issue and correctly not over-weighted.

---

## Top 3 New Issues for the Judge

1. **FK cascade action: captured but never verified, and filed as post-lock
   when it is a pre-lock blocker (MISS-1, P1).** The panel listed "verify FK is
   not CASCADE" as consolidated caveat #11 but (a) never ran the one-line
   `pg_constraint.confdeltype` query despite having full live DB access, and (b)
   placed it post-lock — it appears in zero Phase 7 pre-lock blocker lists. If
   `fk_header` is `ON DELETE CASCADE`, deleting one header (e.g. the 3 empty
   headers the panel itself wants reconciled) silently deletes all its
   messages — a third append-only bypass that also evades the proposed
   REVOKE-TRUNCATE + trigger remedy. Must verify and treat as pre-lock.

2. **Thinking-block fidelity under "scrub-v1" was never validated (MISS-3, P1).**
   The 3,366 thinking traces are the highest-value, non-reconstructable
   content, and the fixture's own name asserts a scrub transform ran. Nobody
   checked whether thinking blocks are verbatim or redacted. The "verbatim
   archive" claim is UNPROVEN for its most precious content class.

3. **Free-tier auto-pause/limits + non-idempotent partial-ingest recovery
   (MISS-2 + MISS-5, P1/P2).** An archive's normal "no-write, rare-read"
   pattern looks inactive to Supabase free tier (pause → eventual delete;
   500 MB cap breached at snapshot #2), and there is NO recovery path that is
   both idempotent AND append-only-preserving for a partial ingest. Tier must be
   confirmed (paid) and ingest must be all-or-nothing (single txn or
   staging-swap).
