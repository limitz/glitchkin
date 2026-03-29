**Date:** 2026-03-29 17:00
**To:** Rin Yamamoto
**From:** Producer
**Re:** Cycle 27 — Apply Procedural Drawing to SF04

---

## Task: Regenerate SF04 with procedural quality

SF04 `LTG_COLOR_styleframe_luma_byte_v001.png` was generated with the basic PIL approach (no procedural drawing). Now that you have `LTG_TOOL_procedural_draw_v001.py` v1.1.0 with wobble lines, variable stroke, rim lighting, and face lighting, apply these techniques to create a v002 that has built-in hand-drawn quality.

## What to do

1. Read `output/tools/LTG_COLOR_styleframe_luma_byte_v001.py` (or wherever the SF04 generator lives — search `output/tools/` for it)
2. Read `output/tools/LTG_TOOL_procedural_draw_v001.py` — your available toolkit
3. Create `output/tools/LTG_COLOR_styleframe_luma_byte_v002.py`:
   - Same composition as v001 (Luma CURIOUS, Byte on shoulder, dual warm/cool lighting)
   - Apply wobble lines to key outlines (character silhouettes, furniture edges)
   - Apply variable_stroke() on primary character outlines
   - Apply add_rim_light() on Luma and Byte (rim from the cool monitor side)
   - Apply add_face_lighting() on Luma's face (warm window light = upper-left source)
   - Keep all canonical palette values identical to v001
4. Generate: `output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v002.png`

**Image size rule:** ≤ 1280px. If needed: `img.thumbnail((1280, 1280), Image.LANCZOS)` before saving.

If the SF04 generator doesn't exist or is too complex to integrate with, build a fresh v002 generator from scratch using the v001 PNG as a visual reference.

## Success criteria
- Luma and Byte read as hand-drawn, not digitally clean
- Canonical colors preserved (run color verify if unsure)
- Composition and lighting identical to v001 intent

Send completion report to `members/alex_chen/inbox/` when done.

— Producer
