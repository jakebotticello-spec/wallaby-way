# Phase 11 — Severity Verification

All four P1 findings were verified against live evidence this phase: live
catalog queries against the running Supabase DB (FK, grants, triggers, RLS,
extensions) and direct reads of the scrub-v1 audit/verify files. No evidence
is inferred — every classification below cites the actual returned values.

---

## P1-A: Append-only enforcement missing

**Live evidence (this phase):**

*Grants* on `public.floor_conv_headers` and `public.floor_conv_messages`:
- `anon` → **TRUNCATE**
- `authenticated` → **TRUNCATE**
- `service_role` → **TRUNCATE**
- `postgres` → SELECT, INSERT, UPDATE, DELETE, TRUNCATE

So three non-owner roles (anon, authenticated, service_role) each hold
TRUNCATE on both floor tables, and postgres holds the full
UPDATE/DELETE/TRUNCATE set. Confirmed exactly as the panel asserted.

*Triggers* — `pg_trigger` (non-internal) returned 5 rows, **none on the
floor tables**: `update_objects_updated_at` (objects),
`enforce_bucket_name_length_trigger` (buckets), `protect_buckets_delete`
(buckets), `protect_objects_delete` (objects), `tr_check_filters`
(subscription). There is **no** BEFORE UPDATE/DELETE/TRUNCATE trigger on
`floor_conv_headers` or `floor_conv_messages`. (Note: Supabase's own
`storage` schema *does* ship `protect_*_delete` triggers — a working example
of the pattern the floor tables lack.)

*RLS* — both floor tables have `relrowsecurity = True`, `relforcerowsecurity
= False`. RLS is enabled, but TRUNCATE is a table-level operation that RLS
policies never filter, so RLS provides no protection against TRUNCATE, and
the standalone TRUNCATE grant to anon/authenticated/service_role is the
live exposure.

**Live-state discipline:** Based on **live catalog reads** of the running
DB (`role_table_grants`, `pg_trigger`, `pg_class.relrowsecurity`), the
strongest evidence class — not a static migration file.

**Classification: [EXISTING_DEFECT].** True of the database as it runs
today; does not wait on the locked schema. The append-only "immortal floor"
is currently a social convention with zero DB-level enforcement.

**Severity: P1 — CONFIRMED.** This is the load-bearing finding of the
review.

---

## P1-B: pgvector not installed; decision title says "+pgvector"

**Live evidence (this phase):** `pg_extension` →
`pg_stat_statements 1.11, pgcrypto 1.3, plpgsql 1.0, supabase_vault 0.3.1,
uuid-ossp 1.1`. **No `vector` row** — confirmed absent. `pg_available_extensions`
shows `vector` default_version `0.8.0`, installed_version `None` — i.e. it
is **installable on demand** via `CREATE EXTENSION vector;` but not
currently installed.

**Live-state discipline:** Live catalog read of `pg_extension` /
`pg_available_extensions`. Strong evidence class.

**Classification: [EXISTING_DEFECT]** in the narrow sense that the decision
title is inaccurate today — but the defect is a **title/scope mismatch**,
not a storage-correctness problem. pgvector is a future read-path concern;
it is not a prerequisite for the storage-only floor lock this decision
scopes, and it can be installed at any time (0.8.0 available).

**Severity: DOWNGRADE P1 → P2.** A missing extension that the locked scope
does not require is a naming inaccuracy, not a P1 risk to the floor.
Remediation is editorial: drop "+pgvector" from the title or annotate it as
"future — not part of this lock."

---

## P1-C: FK cascade action

**Query run (this phase):**
```sql
SELECT conname, confdeltype, confupdtype FROM pg_constraint WHERE conname = 'fk_header';
```
**Output:** `('fk_header', 'a', 'a')`

Decoded: `confdeltype = 'a'` = **NO ACTION**, `confupdtype = 'a'` = NO ACTION.
Broader scan confirms `fk_header` links child `floor_conv_messages` →
parent `floor_conv_headers` with NO ACTION on both delete and update. (For
contrast, Supabase's internal auth tables use `'c'`=CASCADE; the floor FK
deliberately does not.)

**Classification: NOT A DEFECT — RESOLVED.** The FK is **ON DELETE NO
ACTION**, the opposite of the feared CASCADE. It is **not** a third
append-only bypass. In fact it *protects*: a header with child messages
cannot be deleted (NO ACTION raises a FK violation if children exist). The
Phase 8 hypothesis is falsified by the actual catalog value.

**Severity: DOWNGRADE P1 → resolved / non-issue.** Two residual caveats
(neither P1): (1) NO ACTION does not protect *header-less* message rows or
the headers table itself from direct DELETE; (2) it does not stop TRUNCATE —
both of which remain covered by P1-A. P1-A is unaffected either way.

---

## P1-D: Thinking-block fidelity under "scrub-v1"

**Files read (this phase):** `scrub-audit.jsonl` (82,822 bytes — read first
50 + full programmatic aggregate of all 273 entries) and `verify.log` (233
bytes, full).

**What scrub-v1 actually did:** It is a **secrets/credential redactor**, not
a content rewriter. The audit contains **273 redaction entries** across four
`pattern_class` values: **RTSP 177** (→ `<RTSP_CRED_REDACTED>`), **postgres
76** (→ `<POSTGRES_CRED_REDACTED>`, connection-string creds),
**anthropic 10** (→ `<ANTHROPIC_KEY_REDACTED>`, original_length 108), and
**openai 10** (→ `<OPENAI_KEY_REDACTED>`, URLs/keys). Each entry records a
single regex-matched secret replaced by a fixed token, naming the exact JSON
path edited. verify.log additionally lists a `stripe` class with 0 hits.

**Did it touch thinking blocks?** **Yes — but only to redact secrets inside
them, in exactly 8 of the 273 entries** (`thinking`-path entries: RTSP 6,
anthropic 1, postgres 1). Those 8 are leaked API keys / RTSP / postgres
credentials that appeared *inside* a `content[N].thinking` block and were
replaced with a redaction token. The other 265 redactions are in non-thinking
paths (`text`, `content[N].text`, `content[N].input.file_text`,
`content[N].display_content.json_block`, `attachments[].extracted_content`,
nested `content[N].content[M].*`). **No transform reformats, normalizes, or
rewrites thinking-block prose** — the only modification to any thinking block
is substituting a matched secret string with a fixed token (8 substitutions
total across all 3,366 thinking blocks).

**verify.log:** `{"passed": true, "scrub_version": 1, "scanned_bytes":
331359194, "scanned_strings": 673871, "regex_hits_per_class": {RTSP:0,
postgres:0, openai:0, anthropic:0, stripe:0}}` — a post-scrub re-scan of
~331 MB / 673,871 strings found **zero** remaining secret hits across all
five classes. The scrub is complete (no leaked secrets survive) and its only
footprint is token substitution at audited paths.

**Classification: [EXISTING_DEFECT] — but minor and quantifiable, NOT the
catastrophic "thinking blocks silently modified" feared in Phase 8.** The
3,366 thinking blocks are **verbatim except where a thinking block literally
contained a secret**, in which case that secret (and only that secret) was
replaced by a fixed-length token. This is the correct, desirable behavior
for an archive (you do not want live API keys immortalized), but it does
mean the baseline is **not byte-for-byte identical to the raw export** at
the redacted offsets — the "verbatim" claim must be qualified as
"verbatim-modulo-secrets."

**Severity: DOWNGRADE P1 → P2 (documentation/labeling).** The remediation is
to label the floor as "verbatim except secret-redacted (scrub-v1)" and to
retain `scrub-audit.jsonl` as the immutable record of exactly which bytes
were redacted (it already exists and is precise to the JSON path). Fidelity
of reasoning *content* is preserved; only secret strings were altered.

---

## P2: Supabase free-tier auto-pause risk  — [STATIC-INFERENCE]

**Tag: [STATIC-INFERENCE].** The claim (no-write/rare-read archive looks
inactive → free-tier auto-pause, eventual delete, 500 MB cap) is an
inference about Supabase platform *policy*, not a property readable from the
DB catalog. DB queries cannot confirm tier or quota. (Sizing note from this
phase: the scrubbed snapshot is ~365 MB JSON / ~367 MB ndjson on disk; if
loaded verbatim plus indexes this is plausibly near or over a 500 MB free
cap — which raises, not lowers, the relevance of the tier check.)

**Falsification test:** Open the Supabase project dashboard →
Settings/Billing → confirm (1) project tier (Free vs Pro), (2) the
auto-pause-after-inactivity policy and window, (3) the storage cap / current
usage vs 500 MB. If the project is Pro, or auto-pause is disabled, or usage
is comfortably under cap with backups enabled, the finding is falsified.
Severity remains P2 pending dashboard check.

---

## Summary Severity Table

| Finding | Panel Severity | Adjusted | Classification | Evidence |
|---|---|---|---|---|
| P1-A Append-only / TRUNCATE / no triggers | P1 | **P1 (confirmed)** | [EXISTING_DEFECT] | Live: anon+authenticated+service_role+postgres hold TRUNCATE on both floor tables; 5 non-internal triggers, none on floor tables; RLS on but doesn't gate TRUNCATE |
| P1-B pgvector absent vs title | P1 | **P2 (downgrade)** | [EXISTING_DEFECT] — doc/scope mismatch | Live `pg_extension`: no `vector`; `pg_available_extensions`: vector 0.8.0 installable; not required by storage-only lock |
| P1-C FK `fk_header` cascade | P1 | **Resolved / non-issue (downgrade)** | NOT A DEFECT | Live query: `('fk_header','a','a')` = ON DELETE **NO ACTION** — protects, does not cascade |
| P1-D scrub-v1 thinking-block fidelity | P1 | **P2 (downgrade)** | [EXISTING_DEFECT] — minor/labeling | scrub-audit: 273 secret-only redactions (RTSP 177/postgres 76/anthropic 10/openai 10); only 8 touch a `content[*].thinking` path; verify.log `passed:true`, 0 residual hits over 331 MB. Thinking blocks verbatim-modulo-8-secret-tokens |
| P2 Supabase free-tier auto-pause | P2 | **P2** | [STATIC-INFERENCE] | Not catalog-verifiable; ~365 MB snapshot near 500 MB cap; dashboard falsification test supplied |

### Net severity changes this phase
- **P1-A confirmed P1** on live grant + trigger + RLS evidence (the one
  load-bearing defect).
- **P1-B downgraded P1 → P2** (missing extension not required by the
  storage-only lock; installable on demand; title-accuracy issue).
- **P1-C resolved to non-issue** — FK is ON DELETE NO ACTION, not CASCADE;
  the feared third bypass does not exist.
- **P1-D downgraded P1 → P2** — scrub-v1 is a secrets redactor; thinking
  blocks are verbatim except where they contained a secret; verify.log
  confirms a clean post-scrub scan. Labeling fix, not a fidelity failure.
- **Only P1-A survives at P1.** P1-B and P1-D drop to P2; P1-C dissolves.
