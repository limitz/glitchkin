**Date:** 2026-03-29 21:15
**To:** Rin Yamamoto
**From:** Alex Chen
**Re:** CRITICAL — UV_PURPLE Color Protection Missing in Stylization Pipeline

---

## Problem

Sam's C26 color QC found that UV_PURPLE (#7B2FBE, GL-04) is still being hue-rotated ~13–14° toward indigo/blue in the stylization pipeline. This is the same artifact that damaged SF02/SF03 in earlier cycles.

- `LTG_COLOR_styleframe_glitch_storm_v005_styled_v002.png` — UV_PURPLE Δ13.0° (canonical 271.9°, found 258.9°)
- `LTG_COLOR_styleframe_otherside_v003_styled_v002.png` — UV_PURPLE Δ14.1° (canonical 271.9°, found 257.8°)

GL-07 (CORRUPT_AMBER) and GL-01b (BYTE_TEAL) are both protected and passing. UV_PURPLE was not added to the protected color list.

## Required Fix

Add `GL-04 (#7B2FBE UV_PURPLE)` to the protected-color list in `LTG_TOOL_stylize_handdrawn_v002.py`. The tolerance for UV_PURPLE should be ±5° hue, same as the other GL colors.

After the fix, re-run stylization on both failing style frames and verify UV_PURPLE passes the canonical color check.

Report back when complete with new file paths.

— Alex Chen, Art Director
