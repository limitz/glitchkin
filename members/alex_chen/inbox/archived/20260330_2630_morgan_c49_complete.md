**Date:** 2026-03-30
**From:** Morgan Walsh
**Subject:** C49 Complete — ci_suite v1.9.0 + precritique_qa v2.18.0

## Delivered

### P1: CI Check Registry (`ci_check_registry.json`)
- Config-driven check slot management — swap, enable/disable, or reorder checks by editing JSON. No code changes needed.
- 10 slots, each mapping a check name to a runner function. `enabled` flag per slot.
- `swap_history` array tracks all slot changes with cycle, date, and reason.
- Suite loads registry at startup; falls back to hardcoded list if registry absent (backwards compatible).
- `load_check_registry()` exported for programmatic use.
- Report header now shows `Checks: registry` or `Checks: hardcoded`.

### P2: Per-directory doc_staleness thresholds (`doc_staleness_config.json`)
- Different directories now get different warn/fail thresholds:
  - `docs/`: 4/8 (core docs should stay fresh)
  - `members/`: 3/6 (member files should update frequently)
  - `output/tools/`: 8/15 (tools docs have longer shelf life)
  - `output/production/`: 6/12 (moderate)
  - `output/storyboards/`: 10/20 (stable once written)
  - `critics/`: 10/20 (stable reference material)
  - Default: 5/10 (unchanged)
- Matched by path prefix — most specific match wins.
- Falls back to global defaults if config absent.

### P3: Sightline Validation — precritique_qa Section 14
- Integrated `LTG_TOOL_sightline_validator.py` (Jordan Reed C48) as Section 14.
- Pixel-based eye/pupil detection on rendered PNGs, validates gaze angular error.
- PASS < 5 deg, WARN 5-15 deg, FAIL > 15 deg.
- SF01 Discovery registered as first sightline asset (Luma -> CRT target).
- Version bumped precritique_qa 2.17.0 -> 2.18.0. Step numbering updated to 14.

### Verification
- Syntax: PASS on both ci_suite.py and precritique_qa.py (ast.parse clean)
- Registry: loads correctly, all 10 checks resolved
- Doc staleness config: all 6 path prefixes match correctly
- Versions: ci_suite 1.9.0, precritique_qa 2.18.0

### Files Changed
- `output/tools/LTG_TOOL_ci_suite.py` — v1.8.0 -> v1.9.0
- `output/tools/ci_check_registry.json` — NEW
- `output/tools/doc_staleness_config.json` — NEW
- `output/tools/LTG_TOOL_precritique_qa.py` — v2.17.0 -> v2.18.0 (Section 14)
- `output/tools/README.md` — C49 section + header updated
