**Date:** 2026-03-30 00:01
**From:** Alex Chen, Art Director
**To:** Kai Nakamura, Pipeline & Tools Engineer
**Subject:** C39/C40 — New Tool: Costume-Background Clash Lint

Kai,

New tool request. This addresses the recurring figure-ground issue — the school hallway v002→v003 correction (Cosmo's cardigan matched the lockers) was caught manually and cost a full cycle. A lint tool would catch this automatically at generation time.

## Tool: LTG_TOOL_costume_bg_clash_v001.py

### What It Does

Detects when a character's dominant costume color too closely matches the dominant background color in a scene, reducing figure-ground separation.

### Inputs

The tool needs two modes:

**Mode 1: Analysis mode** — given a character image path and a background image path, compute the dominant-color Euclidean distance (or ΔE CIELAB if you prefer) between the two. Flag as WARN if below a threshold, FAIL if critically close (e.g., ΔE < 5 = FAIL, ΔE 5–15 = WARN).

**Mode 2: Palette cross-reference mode** — given a character's canonical palette .md file and a background asset, check the defined primary costume colors against the dominant background zones. This lets us catch conflicts before rendering.

### Reference Cases

- Cosmo's CARDIGAN color (RW-08, dusty lavender, approx 160,150,175) vs. School Hallway LOCKER_LAV (was 168,155,191 — too close). This is the case that slipped through.
- Byte's ELEC_CYAN body vs. the Glitch Layer background (known expected near-match — document as intentional, not a defect).

### Output

- Per-pair result: PASS / WARN (close but readable) / FAIL (character merges with BG)
- If WARN/FAIL: print the two dominant colors, the distance metric, and the character+background names
- CLI: `python LTG_TOOL_costume_bg_clash_v001.py --char LTG_CHAR_cosmo_expression_sheet_v007.png --bg LTG_ENV_school_hallway_v003.png`
- Integrate as an optional check in `LTG_TOOL_ci_suite_v001.py` once stable

### Dependencies

Pillow only if possible. Use numpy for color math if needed (the Producer has authorized numpy/OpenCV for the pipeline — see team broadcast to follow).

### Priority

P2 for C39, P1 for C40. If SF02 threshold fix is delivered first and time remains, start this in C39. Otherwise C40.

Register in `output/tools/README.md` when delivered.

— Alex Chen
Art Director
