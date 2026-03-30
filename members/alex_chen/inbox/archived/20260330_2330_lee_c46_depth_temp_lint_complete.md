**Date:** 2026-03-30
**From:** Lee Tanaka, Character Staging & Visual Acting Specialist
**To:** Alex Chen, Art Director
**Subject:** C46 Depth Temperature Linter — Complete

Alex,

`LTG_TOOL_depth_temp_lint.py` v1.0.0 is built and tested.

## What it does
Validates the Depth Temperature Rule (codified C45): warm=FG, cool=BG in any multi-character/multi-tier composition.

- Samples horizontal bands at FG (78%) and BG (70%) ground-plane Y positions
- Measures per-tier average warmth (R-B channel diff, excluding void/highlight pixels)
- PASS: separation >= threshold (12.0 for REAL_INTERIOR)
- WARN: FG warmer but separation < threshold
- FAIL: depth grammar inverted
- SKIP: Glitch Layer / OTHER_SIDE scenes (exempt per rule)
- Uses `world_type_infer.py` for automatic threshold + GL exemption

## Self-test results
5 synthetic tests: all PASS (PASS/WARN/FAIL/SKIP detection + batch API).

## Real asset results
- **Lineup (LTG_CHAR_lineup.png):** WARN — FG=22.4, BG=13.3, sep=9.1 (under 12.0 threshold but correct direction). The warm tier bands Maya implemented may need slightly more temperature separation.
- **SF06 Handoff:** WARN — FG=64.0, BG=53.0, sep=11.0. Close to threshold, correct direction.
- **Covetous Glitch (GL):** SKIP (correctly exempted).

## precritique_qa integration
Module API ready: `run_depth_temp_check(paths) -> dict` matches the Section pattern. Ideabox submitted for Morgan Walsh to add as Section 12.

## Remaining C46 tasks
P1 (SF06 staging review) and P2 (Byte P14/P15 staging check) from your brief are separate tasks — will address if time permits or carry to next cycle.

Lee
