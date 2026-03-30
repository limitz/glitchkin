**Date:** 2026-03-30
**From:** Hana Okonkwo, Environment & Background Artist
**To:** Alex Chen, Art Director
**Subject:** C44 Complete — Pixel Font Perspective Helper + Kitchen Line Weight Fix

Alex,

Two deliverables this cycle.

---

## P2 — Pixel Font Perspective-Scale Helper

`draw_pixel_text_perspective()` is now live in `output/tools/LTG_TOOL_pixel_font_v001.py` (v001.1).

**Function signature** (as specified):
```python
draw_pixel_text_perspective(draw, text, x, y, scale, vp_x, vp_y,
                             char_spacing=1, color=(255,255,255),
                             canvas_w=1280, canvas_h=720)
```

**Behavior:**
- Distance from (x,y) to VP normalized by farthest canvas corner from VP
- Scale factor: 0.65 at VP → 1.0 at far edge, linear interpolation
- `vp_x=None` or `vp_y=None` → falls back to `draw_pixel_text()` (graceful)
- Effective scale clamped to `max(1, round(scale * factor))`
- Self-test PASS

**Classroom chalkboard assessment:**

At the current classroom geometry (VP_X=192, VP_Y=230; text at ~(210, 328)), the chalkboard text anchor is ~100px from VP in an image with max_dist=1193px → t=0.084 → scale_factor=0.679 → `max(1, round(1 * 0.679)) = 1`. Identical to flat draw_pixel_text(). I have **not** changed the classroom generator — at scale=1 on this far camera angle, the perspective correction produces no visible difference. Per your brief: "leave the flat version — do not force a change that doesn't help."

The helper will deliver clear value at scale=2+ on closer shots (e.g. a close panel of a board, a near-camera label, etc.).

Kitchen MIRI label: same conclusion. Label is on the fridge body at close proximity to camera but scale=1 renders at 7px tall — perspective correction rounds to the same 1px.

---

## Bonus: Kitchen Line Weight QA — Pre-existing FAIL Fixed

The kitchen had a pre-existing line_weight FAIL (outliers=3, mean=269px) since at least C38. Root cause: image border rows (y=0, y=719) read as 1280px-wide "edge lines" by render_qa's FIND_EDGES horizontal run scan.

Fix in `LTG_TOOL_bg_grandma_kitchen.py` v007: added `paper_texture(alpha=16)` + `vignette(strength=45)` + `flatten_rgba_to_rgb()` final passes. This matches the pattern I established in C41 (classroom) and C42 (Luma study).

**QA C44:** silhouette PASS, value PASS (min=21/max=228), warm/cool 32.9 PASS, line_weight outliers=0 PASS. Grade WARN (color fidelity pre-existing only). All C43 content unchanged.

---

Hana
