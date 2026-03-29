**Date:** 2026-03-30 02:00
**To:** Kai Nakamura
**From:** Producer
**Subject:** Ideabox actioned — build stub linter + Glitch spec linter

## Task 1 — Stub integrity linter (your idea)
Build `LTG_TOOL_stub_linter_v001.py`. Scans all files in `output/tools/` for broken imports — specifically any `from LTG_CHAR_* import` or `from LTG_COLOR_* import` referencing deleted originals. Output: which stubs are broken, what they import, whether a canonical `LTG_TOOL_*` replacement exists. Consider integrating as a pre-commit check.

## Task 2 — Glitch spec linter (Alex's idea)
Build `LTG_TOOL_glitch_spec_lint_v001.py`. Validates Glitchkin generator code against the spec in `output/characters/main/glitch.md`. Check: faceplate width within spec range, body mass ratio, at least 2 unique Glitchkin in multi-Glitchkin frames. Fast automated gate before any Glitch asset goes to critique.
