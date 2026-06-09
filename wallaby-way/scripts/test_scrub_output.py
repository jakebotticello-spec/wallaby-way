# pipeline/test_scrub_output.py  S43
# Fixture for pipeline/scrub_output.py.
# Positive (creds removed) + negative (clean node byte-identical) + idempotency.
# No real secrets — all cred values are synthetic fakes.
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent   # pipeline/
sys.path.insert(0, str(_HERE))

from scrub_output import scrub_text, PATTERNS_OUTPUT  # noqa: E402

failures = []

def ok(label, cond):
    status = 'PASS' if cond else 'FAIL'
    print(f'  [{status}] {label}')
    if not cond:
        failures.append(label)
    return cond

print(f'scrub_output loaded: {len(PATTERNS_OUTPUT)} patterns active')
print()

# ── synthetic fakes — NOT real values ─────────────────────────────────────────
FAKE_SB_SECRET      = 'sb_secret_' + 'A' * 25             # 25 chars > {20,} floor
FAKE_SB_PUBLISHABLE = 'sb_publishable_' + 'B' * 25
FAKE_SB_REF_URL     = 'https://abcdefghijklmnop.supabase.co'  # 16 lowercase = {16,} floor
FAKE_ANTHROPIC      = 'sk-ant-' + 'C' * 25
FAKE_POSTGRES       = 'postgresql://testuser:testpassword12345@db.example.com/testdb'

POSITIVE_INPUT = (
    'Node output surface — cred-bearing string:\n'
    f'  sb_key={FAKE_SB_SECRET}\n'
    f'  pub_key={FAKE_SB_PUBLISHABLE}\n'
    f'  endpoint={FAKE_SB_REF_URL}\n'
    f'  api_key={FAKE_ANTHROPIC}\n'
    f'  db_url={FAKE_POSTGRES}\n'
)

# ── POSITIVE ──────────────────────────────────────────────────────────────────
print('=== POSITIVE (all cred classes are scrubbed) ===')
scrubbed_pos = scrub_text(POSITIVE_INPUT)

ok('sb_secret_ full key removed',
   FAKE_SB_SECRET not in scrubbed_pos)
ok('sb_publishable_ full key removed',
   FAKE_SB_PUBLISHABLE not in scrubbed_pos)
ok('supabase project-ref URL removed',
   FAKE_SB_REF_URL not in scrubbed_pos)
ok('anthropic full key removed',
   FAKE_ANTHROPIC not in scrubbed_pos)
ok('postgres password body removed',
   'testpassword12345' not in scrubbed_pos)
ok('<SUPABASE_SECRET_REDACTED> token present',
   '<SUPABASE_SECRET_REDACTED>' in scrubbed_pos)
ok('<SUPABASE_PUBLISHABLE_REDACTED> token present',
   '<SUPABASE_PUBLISHABLE_REDACTED>' in scrubbed_pos)
ok('<SUPABASE_REF_URL_REDACTED> token present',
   '<SUPABASE_REF_URL_REDACTED>' in scrubbed_pos)
ok('<ANTHROPIC_KEY_REDACTED> token present',
   '<ANTHROPIC_KEY_REDACTED>' in scrubbed_pos)
ok('<POSTGRES_CRED_REDACTED> token present',
   '<POSTGRES_CRED_REDACTED>' in scrubbed_pos)

# ── NEGATIVE ──────────────────────────────────────────────────────────────────
print()
print('=== NEGATIVE (clean node catalog — output must be byte-identical to input) ===')

CLEAN_NODE = """\
## Node 1: batch-pipeline-decision

**Type:** MOTION
**Salience:** MOTION
**Keywords:** batch, apparatus, S42, paid-arm

**Summary:** Jake established the batch pipeline build order for S42,
routing the 181 over-ceiling convs to the paid API arm (Batch_Read_Spec §8).

**Span:**
- anchor_msg: "019c7fd0-b828-7658-b340-2dc9cf17a4ee"
- session: S42

--- DONE: 1 node ---
"""

scrubbed_neg = scrub_text(CLEAN_NODE)

ok('clean node output == input (no mutation)',
   scrubbed_neg == CLEAN_NODE)
ok('UUID 019c7fd0-b828-7658-b340-2dc9cf17a4ee survived intact',
   '019c7fd0-b828-7658-b340-2dc9cf17a4ee' in scrubbed_neg)
ok('anchor_msg line survived intact',
   '- anchor_msg: "019c7fd0-b828-7658-b340-2dc9cf17a4ee"' in scrubbed_neg)

# ── IDEMPOTENCY ───────────────────────────────────────────────────────────────
print()
print('=== IDEMPOTENCY (scrub_text(scrub_text(x)) == scrub_text(x)) ===')

ok('idempotent on scrubbed positive input',
   scrub_text(scrubbed_pos) == scrubbed_pos)
ok('idempotent on clean node input',
   scrub_text(scrubbed_neg) == scrubbed_neg)

# ── summary ───────────────────────────────────────────────────────────────────
print()
total = 15
if not failures:
    print(f'ALL {total} ASSERTIONS PASSED')
else:
    print(f'FAILED {len(failures)}/{total}:')
    for f in failures:
        print(f'  - {f}')
    sys.exit(1)
