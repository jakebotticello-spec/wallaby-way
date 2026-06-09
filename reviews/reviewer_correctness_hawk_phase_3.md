# Correctness Hawk — Phase 3 Independent Review
Score: 5/10
Recommendation: LOCK-WITH-CAVEATS

I independently re-ran every reported check against the **live DB** and the **source ndjson** (367.49 MB,
23,095 lines). I took nothing on the summary's word, and that paid off twice:

1. The real DB tables are `floor_conv_headers` / `floor_conv_messages` (not "conversations"/"messages"), the root
   sentinel is `00000000-0000-4000-8000-000000000000` (a valid UUIDv4, NOT all-zeros), and the only FK is
   `fk_header` (no parent self-FK).
2. The source NDJSON records are **flat** — conversation headers carry `record_type:"conversation_header"`;
   message rows have NO `record_type` and expose `msg_uuid` / `conv_uuid` / `content_blocks` / `text` at top
   level. A reviewer who assumed a nested `data`/`message` wrapper (as a naive parser does) would silently
   round-trip against ZERO source rows and report a false pass. I caught and corrected this; all numbers below are
   from a parser that loads all 22,801 source messages and 294 headers.

Headline finding, reproduced from scratch on the real 2.93 MiB max record AND a 300-record random sample:
**Check 3's "byte-identical round-trip" claim is FALSE as stated.** The round-trip is value-preserving
(deep-equal), NOT byte-identical, for every non-empty JSONB value. For an *immutable verbatim archive* that is the
whole ballgame, so I cannot certify a clean LOCK-SAFE. The substrate is sound and the data is faithfully preserved
at the value level (596 messages with supplementary-plane Unicode in text, 929 in content, all round-trip fine);
the decision rationale just misdescribes what was actually proven, and the four checks leave several
archive-critical properties unverified.

---

## Verification Work (queries and outputs)

Environment: Python 3.13, psycopg 3.3.4. Source `records.ndjson` = 367,494,497 bytes (367.49 MB), 23,095 lines
(294 `conversation_header`, 22,801 message rows). DB tables `floor_conv_headers` (10 cols),
`floor_conv_messages` (13 cols). JSONB columns on messages: `content_blocks, attachments, files`; `text`,
`created_at`, `updated_at` are `text`.

Structural facts (independently pulled):
```
headers=294  messages=22801  sum=23095   distinct (snapshot_id,conv_uuid,msg_uuid)=22801   distinct_snapshots=1
constraints = floor_conv_headers_pkey(PK), floor_conv_messages_pkey(PK), fk_header(FK msgs->headers), + NOT NULL checks
indexes = ['floor_conv_headers_pkey','floor_conv_messages_pkey']   (PK only; no index on parent_message_uuid, conv_uuid alone, created_at, sender, is_root, or GIN on jsonb)
rls = {floor_conv_headers: true, floor_conv_messages: true}   policy_count = 0
is_root_count = 304   null_parent_count = 0   root sentinel = 00000000-0000-4000-8000-000000000000 (304 rows)
```

### Check 1 — Ingest 23,095 / 0 errors  → CONFIRMED (strengthened)
Counts match (294+22,801=23,095). Counts alone are insufficient, so I proved **identity completeness** (UUID
set-equality, which was NOT one of the four checks), parsing the source with correct flat paths:
```
loaded_src_msgs = 22801   loaded_src_convs = 294
MSG_SET_EQUAL  = True  (src=22801 db=22801  src_not_db=0  db_not_src=0)
CONV_SET_EQUAL = True  (src=294   db=294    src_not_db=0  db_not_src=0)
```
Every source UUID is in the DB and vice-versa — not merely the same cardinality.

### Check 2 — Pointer uniqueness + UniqueViolation  → CONFIRMED
```
distinct PK tuples = 22801 (= row count)
real duplicate INSERT on an existing PK -> psycopg.errors.UniqueViolation (rolled back)
post_rollback_count = 22801   (no leak)
```

### Check 3 — "Byte-identical round-trip"  → CONTRADICTED (FALSE)
Max-size record `019c8d77-0f82-721a-9857-cda14fc964e6` (content blocks, 3,069,442 source bytes = 2.93 MiB):
```
MAXREC_src_bytes        = 3069442
MAXREC_db_bytes         = 3069442        (SAME byte LENGTH, but NOT identical bytes)
MAXREC_BYTE_IDENTICAL   = False          (keys reordered -> different byte sequence at same length)
MAXREC_DEEP_EQUAL       = True
MAXREC_src_b0_keys      = ['start_timestamp','stop_timestamp','flags','type','thinking','summaries','cut_off','truncated','alternative_display_type','signature']
MAXREC_db_b0_keys       = ['type','flags','cut_off','thinking','signature','summaries','truncated','stop_timestamp','start_timestamp','alternative_display_type']
MAXREC_same_order=False  MAXREC_same_set=True
```
Note: byte LENGTH happens to match here because key reordering only moves bytes around, but the byte SEQUENCE
differs (BYTE_IDENTICAL=False). Length equality is not byte equality.
300-record random round-trip (seed 42, full 22,801-message source loaded with correct paths, 0 missing):
```
byte_identical = 4/300   (1.3% -- only the trivially-empty [] arrays, which have nothing to reorder)
deep_equal     = 300/300
deep_NOT_equal = 0
text_mismatch  = 0/300   (the `text` column IS byte-verbatim; only JSONB is not)
```
This independently reproduces the orchestrator's 200-record result (198/200 reorder; ~1% byte-identical).

What Postgres JSONB actually does (tested directly with `(%s::jsonb)::text`):
```
key order   any multi-key object  -> reordered to storage order   CHANGED (byte; value-preserving)
whitespace  [ {  "a" :  1 } ]     -> [{"a": 1}]                    CHANGED (byte; value-preserving)
dup_keys    {"a":1,"a":2}         -> {"a": 2}                      CHANGED  <-- VALUE-LOSING (keeps last)
num 1e2     {"a":1e2}             -> {"a":100}                     CHANGED  (exponential collapsed)
num 1.5e3   {"a":1.5e3}           -> {"a":1500}                    CHANGED
num -0      {"a":-0}              -> {"a":0}                       CHANGED  (negative zero normalized)
num 1e-7    {"a":1e-7}            -> {"a":0.0000001}               CHANGED  (exponent expanded)
unicode esc {"s":"é 😀"} -> raw é + raw emoji, no \u    CHANGED (un-escapes)
```
I deliberately verified the non-changing cases too, to avoid overclaiming — these are PRESERVED textually:
```
1.0 -> 1.0 | 0.50 -> 0.50 | 5.000 -> 5.000 | 10000000000000000000 (unchanged) | 3.141592653589793238 (unchanged)
```
So the genuinely value-LOSING transform is **duplicate-key collapse**; number canonicalization changes the
*textual* form of a few exponent styles but not the numeric value; key-reorder, whitespace, and `\u` un-escape are
value-preserving but byte-altering.

How exposed is *this* snapshot? Raw-line scan of all 23,095 lines (with a dup-key-detecting JSON parser):
```
src_lines_backslash_u = 1479   src_lines_dup_keys = 0   src_nul_in_text = 0
```
1,479 source lines contain `\u`-escaped JSON, which JSONB un-escapes to raw UTF-8 — so those lines are
byte-altered on ingest (value-preserving). Critically `src_lines_dup_keys = 0`, so the one truly value-LOSING
transform does NOT fire on current data, and the 300-sample confirms `deep_equal=300/300` with zero numeric value
diffs. The current snapshot therefore loses no *values*, but it is demonstrably NOT stored byte-for-byte.
(Note: an earlier draft of this review reported "15 exponential-number lines" — that was a regex false positive
matching hex fragments inside UUIDs/base64, not JSON number literals. The correct value-level test is deep-equal,
which is 300/300; there is no numeric value loss in this snapshot.)

Verdict: Check 3 as written is FALSE. The provable property is "**value-preserving (deep-equal) round-trip, NOT
byte-identical, for JSONB columns; byte-verbatim only for the `text`-typed columns.**" "Objects order-insensitive"
also understates JSONB behavior (whitespace strip + dup-key collapse + number canonicalization + `\u` un-escape).

### Check 4 — Forest reconstruction  → CONFIRMED (strengthened to all conversations)
Root encoding is doubly consistent (`is_root=true` ⇔ parent = sentinel):
```
null_parent_count=0   sentinel_parent_count=304   is_root_count=304
is_root_true_but_nonsentinel_parent = 0
is_root_false_but_sentinel_parent   = 0
```
BFS reconstruction of every multi-root conversation, with subtree-sum reconciliation:
```
multi_root_conv_count = 9   total_roots = 304
MR abe64eb8 roots=2 msgs=136 sum=136 unreach=0 sizes=[134,2]   <-- matches reported "136=134+2"
MR 9905f7f6 roots=2 msgs=40  sum=40  unreach=0 sizes=[38,2]    <-- matches reported "40=38+2"
MR 3805826d roots=2 msgs=2   sum=2   unreach=0 sizes=[1,1]     <-- matches reported "2=1+1"
MR b5cefa7c roots=6 msgs=21  sum=21  unreach=0 sizes=[9,7,2,1,1,1]
MR 8586fbad roots=2 msgs=46  sum=46  unreach=0 sizes=[44,2]
MR eb0a6982 roots=2 msgs=81  sum=81  unreach=0 sizes=[65,16]
MR a1330e8f roots=2 msgs=8   sum=8   unreach=0 sizes=[7,1]
MR c47c2aaa roots=2 msgs=50  sum=50  unreach=0 sizes=[49,1]
MR 59a6af8b roots=2 msgs=23  sum=23  unreach=0 sizes=[22,1]
ALL_MR_SUBTREE_SUMS_MATCH = True
```
All three spot-checked sums in the original claim (136=134+2, 40=38+2, 2=1+1) reproduce exactly. I extended
reachability to **every conversation** (not just the 9) and added header-consistency / referential checks:
```
total_convs(by messages)=291  convs_no_root=0  convs_with_orphans=0  TOTAL_UNREACHABLE=0
msgs_without_header=0   headers_msgcount_mismatch=0   (header.message_count == actual for every header)
headers_with_zero_msgs=3   (bc42e9ab, ae3468be, 3f84a335; all message_count=0)
distinct_conv_in_messages=291  (vs 294 headers)
```
CONFIRMED. NEW fact the four checks didn't surface: **3 of 294 conversation headers carry zero messages** — so
"294 conversations" is really 291 with content + 3 empty shells. Their `message_count` is 0 and matches, so it's
not an error, but the "verbatim archive" rationale should state it.

### Immutability probe (not one of the four checks, but central to "immutable archive")
```
current_user = postgres
grants_on_messages = [DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE]
RLS enabled, policies = 0
```
RLS-with-0-policies denies PostgREST/anon, but the connecting role is the **owner**, which bypasses RLS and holds
UPDATE/DELETE/TRUNCATE. "Immutable" is currently a label, not an enforced property.

---

## Check-by-Check Verdict
| Check | Verdict | Evidence |
|---|---|---|
| 1. Ingest 23,095 / 0 errors | CONFIRMED (+ UUID set-equality both directions) | 294+22,801; src/db UUID sets identical both ways |
| 2. Pointer uniqueness + UniqueViolation | CONFIRMED | 22,801 distinct PKs; live dup-insert raised UniqueViolation; no leak |
| 3. "Byte-identical" round-trip | **FALSE** | 4/300 byte-identical, 300/300 deep-equal; max-rec byte sequence differs (keys reordered, same length); JSONB strips whitespace, collapses dup keys, normalizes some numbers, un-escapes `\u`; `text` column IS verbatim; snapshot has 1,479 `\u` lines byte-altered on ingest |
| 4. Forest reconstruction | CONFIRMED (extended to all convs) | 9/9 sums match incl. reported 136/40/2; full-dataset reachability=0; is_root/sentinel consistent; header counts match; +3 empty headers found |

---

## Gaps Not Covered by the Four Checks
Count, uniqueness, value round-trip, and tree shape are necessary but not sufficient for a *permanent immutable
verbatim archive*.

1. **True byte/canonical verbatim fidelity of JSONB** — not covered (refuted above). There is no raw-text copy of
   the JSON; all structured payloads live only as JSONB.
   - Failure mode: any consumer needing byte-exact replay (hash-chaining, signed manifests, legal "verbatim"
     attestation, diffing against the upstream export) fails — the DB holds a re-serialization, not original bytes.
   - When: the first time someone hashes the export and compares to a hash of DB content.
   - Check: store original raw JSON **text** (text/bytea column or sidecar) + per-record SHA-256 and assert
     hash(source)==hash(stored). Keep JSONB as the query layer. Or keep the NDJSON snapshot as canonical
     source-of-truth with the DB as a derived index.

2. **Dup-key normalization on FUTURE snapshots** — not covered.
   - Failure mode: a future export containing `{"a":1,"a":2}` is silently altered (last wins); deep-equal cannot
     even detect it because the parsed source object can't hold both keys. (Current snapshot has 0 such lines.)
   - When: silently, on ingest of any snapshot whose producer emits duplicate keys.
   - Check: pre-ingest lint of raw NDJSON for duplicate keys; fail loud, or store raw text alongside.

3. **Immutability enforcement** — not covered. Nothing prevents UPDATE/DELETE/TRUNCATE for the owner role.
   - When: any accidental or malicious write.
   - Check: append-only triggers (RAISE on UPDATE/DELETE), a write-revoked reader role, periodic hash-manifest
     verification. RLS-with-0-policies does nothing for the owner.

4. **Durability / backup / PITR** — not covered. Substrate loss = archive loss for a "permanent" store.
   - Check: confirm automated backups + PITR are enabled and test a restore; retain NDJSON snapshots off-substrate.

5. **Multi-snapshot / re-ingest semantics** — not covered. snapshot_id is in the PK but only 1 snapshot exists;
   collision/supersede behavior for a 2nd snapshot is unverified, and each re-ingest grows the table linearly.
   - Check: ingest a 2nd snapshot into scratch and assert intended behavior.

6. **Read-path performance at scale** — not covered. PK indexes only, so tree traversal and content/sender queries
   are sequential scans; content_blocks is heavily TOASTed. Fine at 22k rows; degrades as snapshots accumulate.
   - Check: EXPLAIN ANALYZE intended access patterns; add indexes (parent_message_uuid, conv_uuid) before growth.

7. **NUL bytes / control chars in text** — I checked: `src_nul_in_text = 0`, so no current risk, but it is
   unguarded for future data (Postgres `text` rejects U+0000 and would fail/alter ingest).

8. **Empty conversations** — 3 headers have zero messages (found above); the rationale should acknowledge that
   "294 conversations" is 291 with content + 3 empty shells.

---

## Unicode Edge Case Results
Confirmed **596** source messages with supplementary-plane (>U+FFFF) chars in `text`. Independently, I found
**929** source messages carry supplementary-plane chars in serialized `content` as well — MORE than the 596 in
text — so the prior "no content_blocks Unicode issues" note is wrong: content_blocks carry MORE supplementary-plane
characters than text does. They round-trip fine.
```
src_text_supp_msgs = 596   src_content_supp_msgs = 929
text round-trip (8 sampled, >5 requested)        : 8/8 perfect (codepoint AND utf-8-byte equal), fails=[]
content_blocks round-trip (6 supplementary-plane): 6/6 deep-equal, fails=[]
src_nul_in_text = 0   src_lines_backslash_u = 1479 (source mixes raw UTF-8 with \u escapes; JSONB un-escapes \u)
```
JSON-escaping difference: the source mixes raw UTF-8 with `\u`-escaped sequences (1,479 lines); JSONB normalizes
everything to raw UTF-8 on output. For *strings* this is value-preserving (decoded characters are identical), so
emoji / CJK-extension chars survive losslessly — but it is one more reason the stored bytes are NOT identical to
the source bytes. Unicode fidelity is GOOD at the value level; the only caveat is the universal JSONB byte
difference under Check 3.

## The Empty Records
The reported "135 empty records" did not reproduce. The DB has **114** messages strictly empty in all four content
fields:
```
EMPTY (text='' AND content_blocks=[] AND attachments=[] AND files=[]) = 114
EMPTY (text='' alone)                                                 = 1045   <-- the broader set the "135"/"1045" figures likely reference
distinct conversations containing a strict-empty record = 19   -> CLUSTERED, not distributed
by_sender = assistant:63, human:51
top conv 14d5cb03 holds 84 of the 114   <-- heavily clustered in one conversation
```
Source verification on 8 sampled strict-empty UUIDs: ALL are genuinely empty in the source ndjson (text_len=0,
content_len=0). Ingest did NOT strip content — these were empty in the upstream snapshot (deleted/blank turns),
faithfully preserved with intact PK, sender, is_root, and parent pointers. They are also the only rows that pass
Check 3's byte test (empty `[]` has nothing to reorder), which is exactly why the random sample shows ~0.6%
byte-identical. The "135" figure in the prior context does not match either my strict-4-empty count (114) or the
text-only-empty count (1045); this should be reconciled definitionally before the lock (it is NOT a data error —
all sampled empties are genuinely empty in source — but the headline number is wrong somewhere).

---

## Verdict
LOCK-WITH-CAVEATS, score 5/10.

Solidly TRUE: complete and identity-correct ingest (UUID set-equality both directions, not just counts), enforced
pointer uniqueness, clean tree structure with zero orphans across **all** conversations (not just the 9
spot-checked), header message_count matching actuals, perfectly consistent is_root/sentinel encoding, and
**value-preserving** round-trip including supplementary-plane Unicode (596 messages in text, 929 in content_blocks,
all round-trip fine). The substrate behaves correctly; the current snapshot loses no data *values*. The `text`
column is genuinely byte-verbatim.

Must NOT be carried into the decision record as written: the substrate is **not a byte-verbatim store for JSON**.
Postgres JSONB normalizes (key reorder, whitespace strip, dup-key collapse, some number forms, `\u` un-escape) and
there is no raw-text fallback. On *this* snapshot only value-preserving transforms fire on values, but 1,479 `\u`
lines are already byte-altered on ingest, and dup-key collapse is a silent, value-losing landmine for future
snapshots that is invisible to deep-equal. Calling this an "immutable verbatim archive" on the strength of a
"byte-identical" check that is actually false is the core correctness problem; immutability is likewise unenforced
(owner role retains UPDATE/DELETE/TRUNCATE; RLS has zero policies).

Conditions to clear before LOCK-SAFE: (1) restate the rationale as value-preserving, NOT byte-identical, noting
`text` is verbatim while JSONB is not and that 1,479 `\u` lines are byte-altered on ingest; (2) store the original
raw JSON text + per-record SHA-256 (or keep NDJSON as canonical source-of-truth, DB as derived index) to actually
satisfy "verbatim"; (3) add a pre-ingest lint for dup-keys / NUL bytes; (4) make immutability real (append-only
triggers or a write-revoked reader role — RLS-with-0-policies does nothing for the owner); (5) confirm backups/PITR
with a tested restore; (6) reconcile the empty-record count (strict-4-empty=114 vs text-only=1045 vs reported 135)
and acknowledge the 3 zero-message conversation headers. None of these block using Supabase; they block calling it
*verbatim* and *immutable* on the strength of the four checks as written.
