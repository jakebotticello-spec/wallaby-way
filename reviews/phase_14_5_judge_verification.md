# Phase 14.5 — Post-Judge Verification

Purpose: classify every P0/P1 finding in the Phase 14 judge ruling as
**[PANEL-RAISED]** (already verified in Phase 11 — skip) or **[JUDGE-INTRODUCED]**
(verify here with a ground-truth check). For every [JUDGE-INTRODUCED] P0/P1,
issue [JUDGE-CONFIRMED], [JUDGE-HALLUCINATED], or [JUDGE-PARTIAL].

Inputs read: `phase_14_judge_ruling.md`, `phase_11_severity_verification.md`.

---

## P0/P1 extraction from the judge ruling

The judge's Severity Rulings table (ruling lines 85-100) grades exactly **one**
finding at P0/P1, and the ruling states it explicitly: *"The only P1 is P1-A"*
(line 100). There are **zero P0 findings**. Everything else the judge rules on
is P2 or P3 and is therefore out of scope for this P0/P1 verifier.

| # | Finding in judge ruling | Judge severity | In P0/P1 scope? |
|---|---|---|---|
| 1 | P1-A Append-only enforcement absent (TRUNCATE held by 4 roles, no triggers, RLS doesn't gate TRUNCATE, both tables) | **P1 (confirmed)** | YES |
| — | FK cascade (feared third bypass) | Non-issue / resolved | no |
| — | "Verbatim" claim accuracy | P2 (labeling) | no |
| — | scrub-v1 thinking-block fidelity | P2 (labeling) | no |
| — | pgvector absent vs "+pgvector" title | P2 (editorial/scope) | no |
| — | Multi-snapshot mixed-version query | P2 (pre-snapshot-2) | no |
| — | Partial-ingest idempotency vs append-only | P2 (pre-snapshot-2) | no |
| — | Supabase free-tier auto-pause / 500 MB cap | P2 (pre-lock empirical) | no |
| — | account_uuid PII-adjacent in content floor | P2 (acknowledge) | no |
| — | No secondary indexes | P3 | no |
| — | Denormalized header fields unenforced | P3 | no |
| — | TOAST / timestamp-as-TEXT / empty-content | P3 | no |

So the only finding requiring classification here is **P1-A**.

Note on the judge's "hard pre-lock blockers": the ruling promotes caveats 1-4
to blockers (lines 64, 108-122, 132). Caveat 1 *is* the remediation for P1-A
(panel-raised). Caveats 2-4 (record ndjson SHA-256; demonstrate
rebuild-from-ndjson; relabel "verbatim") are process/operationalization
requirements and labeling fixes, not P0/P1 *defect findings* — the judge grades
the underlying items at P2 (labeling) or treats them as conditions on the
reframe, never assigning them P0/P1 severity. They are therefore not in the
P0/P1 set this phase must verify. The one substantive *new factual claim* the
judge attaches at the P1's evidentiary weight is the grant-scope expansion in
ruling line 27 (REFERENCES/TRIGGER also held; headers table identical), handled
as a sub-item below.

---

## Classification of P1-A

**[PANEL-RAISED].** P1-A is the panel's load-bearing finding throughout. It was
raised by the panel in Phases 3-7, examined by the Phase 8 auditor, and
**already live-verified in Phase 11** (the entire "P1-A: Append-only enforcement
missing" section of `phase_11_severity_verification.md`, lines 10-48, with live
reads of `role_table_grants`, `pg_trigger`, and `pg_class.relrowsecurity`). The
judge's disposition (ruling line 20: "ACCEPT. This is the load-bearing finding")
adopts the Phase 11 result verbatim and adds no new severity.

Per the Phase 14.5 mandate, [PANEL-RAISED] findings are skipped here because
they were verified in Phase 11. **No re-verification required for the P1-A core.**

### Sub-item: judge's grant-scope expansion (ruling line 27)

The judge states the exposure is "broader than the panel's 'only TRUNCATE'
shorthand — the three non-owner roles also hold REFERENCES and TRIGGER, and the
*headers* table carries the identical grant set." Phase 11's P1-A section
itemized only TRUNCATE, so on a Phase-11-only reading this looked
judge-introduced. **Ground-truth check resolves it as already panel-verified.**

**Ground-truth check: read of `phase_10_claim_verification.md` (the Phase 10
Claim Verifier's live DB results).** Phase 10 C10/C11 (lines 59-61) records the
live grant query:

> "floor_conv_messages grants for anon / authenticated / service_role: each of
> the three roles has: REFERENCES, TRIGGER, TRUNCATE (NO SELECT, NO INSERT, NO
> UPDATE, NO DELETE) ... floor_conv_headers grants for the three roles:
> IDENTICAL set -> REFERENCES, TRIGGER, TRUNCATE."

Phase 10's claim table (line 124) and accuracy footnote (line 150) repeat it
verbatim: the three roles "DO hold REFERENCES and TRIGGER, which the panel's
'only TRUNCATE' framing omits; and floor_conv_headers carries the identical
grant set." This is a **live catalog read** (psycopg3 against the running DB),
the strongest evidence class.

**Disposition: [JUDGE-CONFIRMED] — and reclassified [PANEL-RAISED].** Both halves
of the judge's line-27 claim are exactly what the Phase 10 Claim Verifier
already established by live query: (a) anon/authenticated/service_role hold
REFERENCES + TRIGGER in addition to TRUNCATE, and (b) the headers table carries
the identical grant set. The judge did not introduce a new fact; he surfaced a
Phase 10 verification result that the Phase 11 P1-A write-up had compressed into
"TRUNCATE." Because it was verified in Phase 10 (within the verification phase
band this verifier is told to treat as authoritative), it is **[PANEL-RAISED] /
already-verified**, not judge-introduced. It correctly widens caveat 1's REVOKE
scope (REFERENCES/TRIGGER), and the caveat's own test step re-checks grants, so
there is no open verification item. No severity or verdict impact.

---

## Verification table

| Finding | Source | Classification | Ground-truth check |
|---|---|---|---|
| P1-A Append-only enforcement absent (TRUNCATE on both floor tables for anon/authenticated/service_role; no guard triggers; RLS enabled but doesn't gate TRUNCATE) | Panel (Phase 3-7) → Phase 8 audit → **live-verified Phase 11** | **[PANEL-RAISED]** — skip (already verified Phase 11) | Not re-run here by design. Phase 11 = [LIVE-VERIFIED] via `role_table_grants`, `pg_trigger`, `pg_class.relrowsecurity`. Judge disposition merely ACCEPTs the Phase 11 result. |
| P1-A sub-claim: non-owner roles also hold REFERENCES + TRIGGER, and headers table has identical grant set (ruling line 27) | Phase 10 Claim Verifier (live DB) — surfaced by judge | **[PANEL-RAISED] / [JUDGE-CONFIRMED]** | Read `phase_10_claim_verification.md` C10/C11 (lines 59-61, 124, 150): live query shows anon/authenticated/service_role each hold `REFERENCES, TRIGGER, TRUNCATE` on `floor_conv_messages` AND headers carries the IDENTICAL set. Both halves of the judge's claim are an existing Phase 10 live-verified result, not a new judge fact. Phase 11's P1-A write-up had compressed it to "TRUNCATE." Widens caveat 1 REVOKE scope; caveat's own test re-checks grants. No severity/verdict impact. |

---

## Summary

- **P0 findings in judge ruling:** 0.
- **P1 findings in judge ruling:** 1 (P1-A only; judge: "The only P1 is P1-A").
- **[PANEL-RAISED] (skipped — verified in Phases 10/11):** P1-A core
  (live-verified Phase 11), and its grant-scope detail (REFERENCES/TRIGGER on
  both tables; headers parity — live-verified Phase 10 C10/C11).
- **[JUDGE-INTRODUCED] genuinely new P0/P1 findings:** 0. The one claim that
  read as new on a Phase-11-only basis (the line-27 grant-scope expansion) was
  found, on ground-truth check, to be an already-recorded Phase 10 live-query
  result → **[JUDGE-CONFIRMED]**, reclassified [PANEL-RAISED].
- **No [JUDGE-HALLUCINATED] findings.** The judge fabricated no P0/P1 defect and
  inflated nothing above its evidence floor (he in fact *downgraded* the panel's
  other P1s to P2/non-issue, consistent with Phase 11).

**Net: every P0/P1 in the judge ruling traces to a panel finding already
verified in Phase 10 or Phase 11. There are no judge-introduced P0/P1 findings
requiring independent verification, and none were hallucinated.**

### Note on tooling

Initial Bash/Grep calls in this phase returned errors/empty output transiently;
once recovered, the ground-truth check was completed by reading
`phase_10_claim_verification.md`, which contains the live `role_table_grants`
result that resolves the only contested sub-claim. No live DB re-query was
required — the Phase 10 artifact already holds the catalog read.
