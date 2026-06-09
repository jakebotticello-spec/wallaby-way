# scripts/reserve/ — held, not retired

Tools in here are PROVEN and INTACT but not on active duty. They are not dead (that's graveyard/);
they are between jobs. Do not delete them; do not wire them into the live pipeline without a deliberate decision.

## onsub_loop.js — Stage B on-sub reader loop
- STATUS: proven operational, passed its tests, locked on main (Stage A lock, v29).
- WHY IT'S HERE: it was Stage B's reader. The CORPUS read moved to the paid batch harness because the
  on-sub delivery path has a ~13K-char ceiling (181/219 corpus convs were over it). So this loop is
  SUPERSEDED *as the corpus mechanism*.
- POSSIBLE FUTURE USE: undetermined. It still works for bounded, small-conv reads, so it may be useful
  again for some future bounded task — but no specific role is assigned. Decide deliberately if/when that comes up.
- DO NOT: use it for full-corpus reads (it will hit the ceiling the project already paid to escape).
