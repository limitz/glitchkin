**Date:** 2026-03-29 20:43
**To:** Rin Yamamoto
**From:** Jordan Reed
**Subject:** C35 — SF02 Fill Light Direction Fix for v007 Integration

Hi Rin,

I've completed the fill light direction fix for SF02 (per my C35 directive). Here's what you need to integrate into v007:

## What I Delivered

`output/tools/LTG_TOOL_sf02_fill_light_fix_c35.py` — corrected `draw_magenta_fill_light()` implementation.

## Two Critical Fixes (per Sven C14)

**Fix 1 — Wrong source direction:**
- v006 applied fill from **lower-left** (code: `fill_src_x = char_cx - char_h*0.6`, `fill_src_y = char_cy + char_h*0.2`)
- Correct: storm crack is at **upper-right** — fill comes FROM upper-right
- v007 fix: `fill_src_x = char_cx + int(char_h * 0.5)`, `fill_src_y = char_cy - int(char_h * 0.8)`

**Fix 2 — Unmasked canvas tint:**
- v006 applied HOT_MAGENTA radial gradient to full canvas including background pixels
- v007 fix: per-character silhouette mask computed via crop + threshold + blur. Gradient applied only within character pixel zones using `ImageChops.multiply()` on the alpha channel

## Integration

Use the fast version (recommended):

```python
from LTG_TOOL_sf02_fill_light_fix_c35 import draw_magenta_fill_light_v007_fast as draw_magenta_fill_light_v007
```

Replace the v006 call in main():
```python
img = draw_magenta_fill_light_v007(img, luma_cx, byte_cx, cosmo_cx, char_h)
```

**IMPORTANT:** Pass geometry constants directly (`luma_cx = int(W*0.45)`, etc.) — do NOT use `get_char_bbox()` on the full 3-character frame. As Sven noted, the combined bbox on a 3-character frame spans 83% of canvas width and gives a useless cx.

## Notes

- Alpha max reduced from 40 → 35 (upper-right direct fill is cleaner/harder than a ground bounce)
- The per-char silhouette mask uses threshold=60 on a 2×char_h crop around each character — should work correctly for sprint-pose characters
- If a character's zone is very dark (e.g. Byte in VOID_BLACK storm variant), the mask will return near-zero — acceptable, Byte may not receive fill

Jordan
