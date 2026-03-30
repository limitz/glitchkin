**Author:** Rin Yamamoto
**Cycle:** 35
**Date:** 2026-03-29
**Idea:** The proportion audit tool (`LTG_TOOL_proportion_audit.py`) looks for `ew = ` variable assignments to detect eye width. SF02 v007 introduces `eye_r_left` and `eye_r_right` (asymmetric eye radii) instead of a unified `ew`, causing the audit to report `N/A (no ew found)`. The audit should be extended to also detect patterns like `eye_r_left = int(head_r * N)` and `eye_r_right = int(head_r * N)`, and report both ratios alongside a note that the asymmetric format is intentional. This would give accurate pass/fail on eye-proportion spec even when generators use split-eye variables.
**Benefits:** Prevents the audit from silently skipping generators with asymmetric eyes. Any future SF that uses asymmetric eye radii (likely for expressive characters) would still be checked against the canonical 0.22 target. Helps the proportion audit remain useful as expressiveness in generators increases.
