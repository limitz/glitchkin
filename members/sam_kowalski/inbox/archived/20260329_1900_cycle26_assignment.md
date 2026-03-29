**Date:** 2026-03-29 19:00
**To:** Sam Kowalski
**From:** Producer (via Alex Chen)
**Re:** Cycle 26 — Color QC Pass on All C25 New Assets

---

## Context
Cycle 25 produced a significant number of new assets. Before these go to critics, run a full color QC pass.

---

## Deliverable: Color QC Report for C25 Assets

Use `LTG_TOOL_color_verify_v001.py` (Kai's new tool from C25) to check all new PNG outputs from Cycle 25.

Assets to check:
- `output/characters/color_models/LTG_COLOR_luma_color_model_v001.png`
- `output/characters/color_models/LTG_COLOR_byte_color_model_v001.png`
- `output/characters/color_models/LTG_COLOR_cosmo_color_model_v001.png`
- `output/characters/main/LTG_CHAR_luma_expression_sheet_v005.png`
- `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround_v002.png`
- `output/characters/main/turnarounds/LTG_CHAR_cosmo_turnaround_v002.png`
- `output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v003.png`
- `output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v001.png`
- `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v005_styled_v002.png`
- `output/color/style_frames/LTG_COLOR_styleframe_otherside_v003_styled_v002.png`

For each asset:
1. Run `verify_canonical_colors()` with the standard palette
2. Note which canonical colors appear (some may not be in every image — that's fine)
3. Flag any with hue drift > 5°

Also:
- Visually check the SF04 (Luma+Byte) against master_palette.md — does Byte's body look like #00D4E8 BYTE_TEAL, not #00F0FF?
- Check that SF04 has both warm (Real World) and cool (Glitch) zones present and distinct

Write results to `output/production/color_qc_c25_assets.md`.
Flag any issues to `members/alex_chen/inbox/` for director review.

---

## Standards
- Use `from output.tools.LTG_TOOL_color_verify_v001 import verify_canonical_colors, get_canonical_palette`
- Run from `/home/wipkat/team`

— Alex Chen, Art Director
