# pipeline/scrub_output.py  S42
# Output-surface credential scrub — text-in / text-out, no side effects.
# Extends the authoritative S12 PATTERNS ruleset with Supabase credential formats.
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from apparatus_freeze_pipeline import PATTERNS  # noqa: E402

SUPABASE_PATTERNS = [
    ('supabase_secret',      r'sb_secret_[A-Za-z0-9_-]{20,}',        '<SUPABASE_SECRET_REDACTED>'),
    ('supabase_publishable', r'sb_publishable_[A-Za-z0-9_-]{20,}',   '<SUPABASE_PUBLISHABLE_REDACTED>'),
    ('supabase_ref_url',     r'https://[a-z0-9]{16,}\.supabase\.co', '<SUPABASE_REF_URL_REDACTED>'),
]
PATTERNS_OUTPUT = PATTERNS + SUPABASE_PATTERNS


def scrub_text(s: str) -> str:
    """Apply all PATTERNS_OUTPUT in order. Idempotent: redaction tokens match no pattern."""
    for _, pattern, token in PATTERNS_OUTPUT:
        s = re.sub(pattern, token, s)
    return s


def scrub_file(path) -> str:
    """Read a UTF-8 file and return its scrubbed text. Does NOT write."""
    return scrub_text(Path(path).read_text(encoding='utf-8'))
