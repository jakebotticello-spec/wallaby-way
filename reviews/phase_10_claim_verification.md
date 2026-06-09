# Phase 10 — Claim Verification

Verifier: Claim Verifier (Phase 10). Every claim was independently re-checked against the **live Supabase DB** (`floor_conv_headers` / `floor_conv_messages`) and/or the **read-only source ndjson** (`apparatus-archive/snapshots/baseline-2026-05-25-ae015455/scrub-v1/records.ndjson`). DB access via psycopg3 (3.3.4), Python 3.13. Reviewer summaries were NOT accepted as evidence — every query was run and its raw output captured.

Classification legend:
- **VERIFIED** — claim matches the evidence.
- **INACCURATE** — claim is contradicted by the evidence.
- **MISATTRIBUTED** — fact is true but credited to the wrong source/measurement.
- **HALLUCINATED** — claim has no basis in the evidence.
- **UNVERIFIABLE** — evidence not obtainable.

---

## Verification Results (queries + raw outputs)

### Core counts (DB + source)
```
C1  SELECT count(*) FROM floor_conv_headers             -> 294
C2  SELECT count(*) FROM floor_conv_messages            -> 22801
C3  line-iteration of records.ndjson                    -> 23095   (file DOES end with a trailing newline; non-empty lines also = 23095)
    ndjson record split: floor_conv_header rows + floor_conv_message rows = 294 + 22801 = 23095 (matches DB exactly)
    NOTE: source records have NO 'type' discriminator key; record kind is inferred from columns
          (headers carry message_count/multi_root; messages carry msg_uuid/content_blocks).
C9  lines containing literal '\u' in records.ndjson     -> 1479
```

### Root / parent structure
```
C4  SELECT count(*) ... WHERE is_root=true                                            -> 304   (TOTAL roots)
    parent distribution for is_root=true rows:  '00000000-0000-4000-8000-000000000000' = 304
    => the sentinel is the UUIDv4-form all-zeros-except-version value
       '00000000-0000-4000-8000-000000000000', NOT the plain all-zeros UUID.
    WHERE is_root=true AND parent = '00000000-0000-4000-8000-000000000000' (actual sentinel) -> 304
    WHERE is_root=true AND parent = '00000000-0000-0000-0000-000000000000' (plain all-zeros)  -> 0
    WHERE is_root=true AND parent <> sentinel                                                  -> 0  (NO non-sentinel roots)
    WHERE parent = sentinel AND is_root=false                                                  -> 0  (sentinel used ONLY by roots)
    => exactly 304 roots, every one of which carries the sentinel. Clean 1:1.
C5  conversations with 2+ roots, GROUP BY conv_uuid                   HAVING >=2 -> 9
    conversations with 2+ roots, GROUP BY (snapshot_id, conv_uuid)    HAVING >=2 -> 9
    (consistent with 294 headers vs 304 roots: 10 extra root rows across 9 multi-root convs)
C17 SELECT count(*) ... WHERE parent_message_uuid IS NULL                        -> 0
```

### JSONB behavior (live)
```
C6  SELECT '{"z":1,"a":2,"m":3}'::jsonb::text  -> {"a": 2, "m": 3, "z": 1}   (keys SORTED, not insertion order)
C7  SELECT '{"a":1,"a":2}'::jsonb::text        -> {"a": 2}                    (last-wins, no error raised)
C8  content_blocks round-trip, 200 source samples (non-empty content_blocks) vs DB content_blocks::text,
    keyed precisely on the PK (snapshot_id, conv_uuid, msg_uuid):
        byte_identical = 0, reordered (same value, key order differs) = 200, value_mismatch = 0, notfound = 0, checked = 200
    => 200/200 round-trip with key reordering, ZERO byte-identical, ZERO value loss.
       (Panel asserted 198 reordered / 2 byte-identical. Clean PK-keyed comparison finds ALL 200
        differ only by key order; the 2 byte-identical records are not reproducible here.)
```

### Access control (live)
```
C10/C11 floor_conv_messages grants for anon / authenticated / service_role:
        each of the three roles has: REFERENCES, TRIGGER, TRUNCATE
        (NO SELECT, NO INSERT, NO UPDATE, NO DELETE for any of the three)
    floor_conv_headers grants for the three roles: IDENTICAL set -> REFERENCES, TRIGGER, TRUNCATE
        (the panel discussed messages; headers have the SAME exposure.)
C12 SELECT relname, relrowsecurity FROM pg_class:
        floor_conv_headers = true, floor_conv_messages = true   (RLS enabled on BOTH)
C13 SELECT ... FROM pg_policies WHERE tablename IN (...)  -> []  (0 policies on either table)
```

### Schema structure
```
C14 pg_indexes floor_conv_messages -> floor_conv_messages_pkey :
        CREATE UNIQUE INDEX ... USING btree (snapshot_id, conv_uuid, msg_uuid)
    pg_indexes floor_conv_headers  -> floor_conv_headers_pkey :
        CREATE UNIQUE INDEX ... USING btree (snapshot_id, conv_uuid)
    => ONLY the PK btree on each table. No secondary index on parent_message_uuid / conv_uuid-alone /
       sender / is_root / created_at.
C15 pg_constraint conname='fk_header':
        conrelid=floor_conv_messages, confrelid=floor_conv_headers,
        def = FOREIGN KEY (snapshot_id, conv_uuid) REFERENCES floor_conv_headers(snapshot_id, conv_uuid)
C16 pg_extension WHERE extname IN ('vector','pgvector') -> []  (NOT installed)
    installed extensions: pg_stat_statements, pgcrypto, plpgsql, supabase_vault, uuid-ossp
C20 EXPLAIN SELECT * FROM floor_conv_messages WHERE parent_message_uuid = $1:
        with actual sentinel:  "Seq Scan on floor_conv_messages (cost=0.00..2769.01 rows=304 width=838)"
                               "  Filter: (parent_message_uuid = '00000000-0000-4000-8000-000000000000'::uuid)"
        with random uuid:      "Seq Scan on floor_conv_messages (cost=0.00..2769.01 rows=1 width=838)"
        => Seq Scan in both cases (no index can serve this predicate).
```

### Data quality
```
C18 headers with zero matching messages, anti-join on (snapshot_id, conv_uuid) -> 3
    headers with zero matching messages, anti-join on conv_uuid only          -> 3
C19 strictly-empty messages: text='' AND content_blocks='[]'::jsonb
        AND attachments='[]'::jsonb AND files='[]'::jsonb                      -> 114
    (column types confirmed via information_schema: content_blocks/attachments/files = jsonb, text = text)
```

### Critical completeness-audit claim
```
C21 SELECT confdeltype FROM pg_constraint WHERE conname='fk_header' -> 'a'
    confdeltype 'a' = NO ACTION
    full row: confdeltype='a' (DELETE = NO ACTION), confupdtype='a' (UPDATE = NO ACTION)
    def     = FOREIGN KEY (snapshot_id, conv_uuid) REFERENCES floor_conv_headers(snapshot_id, conv_uuid)
    => fk_header has NO ON DELETE CASCADE. The default NO ACTION applies: an attempt to DELETE a header
       row that still has child messages will be REJECTED by the constraint (it cannot orphan or
       auto-delete messages).
```

---

## Claim-by-Claim Table

| Claim | Panel's assertion | Verified? | Classification | Evidence |
|-------|-------------------|-----------|----------------|----------|
| C1 | floor_conv_headers has 294 rows | YES | VERIFIED | count(*) = 294 |
| C2 | floor_conv_messages has 22,801 rows | YES | VERIFIED | count(*) = 22801 |
| C3 | Source ndjson has 23,095 lines | YES | VERIFIED | iterated lines = 23095; 294 headers + 22801 messages = 23095 |
| C4 | 304 messages have is_root=true AND parent = sentinel | YES | VERIFIED | is_root=true AND parent=sentinel = 304; is_root_total = 304; 0 non-sentinel roots. Caveat: the sentinel is `00000000-0000-4000-8000-000000000000` (UUIDv4 nil-with-version), NOT the plain all-zeros UUID — any reviewer who named the plain all-zeros value misidentified the literal |
| C5 | 9 conversations have 2+ roots | YES | VERIFIED | GROUP BY conv key HAVING count(is_root)>=2 = 9 (identical by conv_uuid and by (snapshot_id,conv_uuid)) |
| C6 | jsonb returns keys SORTED (not insertion order) | YES | VERIFIED | `'{"z":1,"a":2,"m":3}'::jsonb::text` = `{"a": 2, "m": 3, "z": 1}` |
| C7 | duplicate jsonb keys -> `{"a": 2}` (last-wins, no error) | YES | VERIFIED | `'{"a":1,"a":2}'::jsonb::text` = `{"a": 2}` |
| C8 | content_blocks round-trip: 198/200 key-reordered, 2 byte-identical (200-record sample) | PARTIAL | INACCURATE (in the exact split) | clean PK-keyed measure: reordered=200, byte_identical=0, value_mismatch=0, checked=200. The CORE finding (content_blocks survive as semantically-equal but key-reordered JSONB, zero value loss) is VERIFIED; the specific "198 reordered + 2 byte-identical" split is NOT reproducible — all 200 are reordered, none byte-identical |
| C9 | 1,479 source lines contain `\u`-escaped JSON | YES | VERIFIED | lines containing literal `\u` = 1479 |
| C10 | anon/authenticated/service_role have TRUNCATE on floor_conv_messages | YES | VERIFIED | all three have TRUNCATE (also REFERENCES, TRIGGER) |
| C11 | those roles do NOT have INSERT/UPDATE/DELETE | YES | VERIFIED | confirmed no INSERT/UPDATE/DELETE/SELECT. CAVEAT: they DO hold REFERENCES and TRIGGER, which the panel's "only TRUNCATE" framing omits; and floor_conv_headers carries the identical grant set |
| C12 | RLS enabled on both tables (relrowsecurity=TRUE) | YES | VERIFIED | floor_conv_headers=true, floor_conv_messages=true |
| C13 | pg_policies returns 0 rows for both tables | YES | VERIFIED | 0 policy rows |
| C14 | Only PK btree indexes exist (no secondary indexes) | YES | VERIFIED | only `*_pkey` btree on each; none on parent_message_uuid/sender/is_root/created_at/conv_uuid-alone |
| C15 | FK fk_header on floor_conv_messages -> floor_conv_headers (snapshot_id, conv_uuid) | YES | VERIFIED | constraint def matches exactly |
| C16 | pgvector/vector extension NOT installed | YES | VERIFIED | pg_extension has no vector/pgvector entry |
| C17 | 0 NULL values in parent_message_uuid | YES | VERIFIED | NULL count = 0 (column is NOT NULL in practice; sentinel used instead) |
| C18 | 3 conversation headers have zero matching messages | YES | VERIFIED | anti-join = 3 (both join-key variants) |
| C19 | 114 messages strictly empty (text='', content_blocks=[], attachments=[], files=[]) | YES | VERIFIED | strict-empty count = 114 |
| C20 | EXPLAIN for parent_message_uuid filter returns Seq Scan | YES | VERIFIED | top node = `Seq Scan on floor_conv_messages` with Filter on parent_message_uuid (confirmed with both the real sentinel and a random uuid) |
| C21 | (audit) confdeltype on fk_header | YES | VERIFIED | confdeltype = `'a'` = **NO ACTION** (no ON DELETE CASCADE; confupdtype also 'a' = NO ACTION) |

---

## Summary

- **Total claims checked: 21 / 21.**
- **VERIFIED: 20.**
- **INACCURATE (in detail only): 1 -> C8.** The C8 *finding* (content_blocks round-trip with key-reordered JSONB and zero value loss) is correct, but the precise quantitative split "198 reordered / 2 byte-identical out of 200" is NOT reproducible. A clean PK-keyed re-measure of the same 200-record sample yields **200 reordered / 0 byte-identical / 0 value-mismatch**. The 2 "byte-identical" records claimed by the panel do not appear; every sampled content_blocks differs from source by key order only. This is a measurement-precision error, not a substantive one — the conclusion (no data loss, only canonical JSONB key reordering) stands.
- **HALLUCINATED / MISATTRIBUTED: 0.** No claim was invented or credited to the wrong source.

### C21 — fk_header cascade action (the requested new finding)
`confdeltype = 'a'` = **NO ACTION** (and `confupdtype = 'a'` = NO ACTION). The `fk_header` foreign key does **NOT** cascade. Deleting a `floor_conv_headers` row that still has child `floor_conv_messages` will be **rejected** by the constraint — it cannot orphan messages or auto-delete them. Relevant to the lock/teardown design: a header delete is safe (constraint-blocked), not a silent cascade.

### Accuracy footnotes (claims VERIFIED but with caveats the panel should record — NOT reclassified)
- **C4 — sentinel literal:** The 304 figure is exact and the structure is clean (304 roots, all sentinel-parented, zero non-sentinel roots, sentinel never used by non-roots). BUT the sentinel value is `00000000-0000-4000-8000-000000000000` (a nil-UUID with the v4 version/variant nibbles set), **not** the plain all-zeros `00000000-0000-0000-0000-000000000000`. A query against the plain all-zeros value returns 0 rows. Any reviewer statement that named the plain all-zeros UUID as the sentinel is describing the wrong literal even though the count is right.
- **C10/C11 — grant completeness:** Verified true as stated, but the panel's "only TRUNCATE" framing is incomplete: anon/authenticated/service_role also hold **REFERENCES** and **TRIGGER** on both tables, and **floor_conv_headers** carries the identical grant set (the discussion centered on messages). DML (INSERT/UPDATE/DELETE) and SELECT remain correctly absent.
- **C3 — trailing newline / type key:** ndjson does end with a trailing newline (line-iteration and non-empty counts both = 23095, so no off-by-one). Records have no `type`/`_type` discriminator; record kind is inferred from columns. Count reconciliation (294 + 22801 = 23095) is exact.
- **C8 — exact split not reproducible:** The 2 "byte-identical" content_blocks the panel reported could not be reproduced under a clean PK-keyed comparison (all 200 sampled records reorder keys). This may stem from a different sampling order, a join that matched on a non-unique key, or comparing pre-canonicalized text on the panel's side. The substantive claim (semantic equality, zero data loss, JSONB key reordering) is sound; only the headline 198/2 split is off.
