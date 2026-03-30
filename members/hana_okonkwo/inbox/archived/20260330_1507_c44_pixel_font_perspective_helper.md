**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Hana Okonkwo, Environment & Background Artist
**Subject:** C44 Brief — Pixel Font Perspective-Scale Helper

Hana,

C44 brief — one P2 item from the actioned ideabox.

---

## P2 — Pixel Font Perspective-Scale Helper

**Background:** Your C43 classroom chalkboard deployed `draw_pixel_text()` with "1011 XOR 0110" and "F X  2X 5". The text looks correct at the canvas level, but in a 3/4 perspective view the chalkboard is angled — text in perspective should scale down slightly toward the vanishing point to read naturally.

The current implementation draws pixel text at a flat scale regardless of perspective position. This is acceptable at the distances we're working with (and QA passes), but a helper that applies a mild perspective scale correction would improve realism for any future text-heavy environments.

**Deliverable:** A helper function added to `LTG_TOOL_pixel_font_v001.py` (or a new thin module `LTG_TOOL_pixel_font_perspective.py` if cleaner):

```python
def draw_pixel_text_perspective(draw, text, x, y, scale, vp_x, vp_y, char_spacing=1, color=(255,255,255)):
    """
    Draws pixel text with mild perspective scale: characters closer to vp_x/vp_y
    are scaled down by a factor proportional to their distance from canvas center vs VP.
    Simple linear approximation — not full projective transform.
    """
```

Requirements:
- `scale` = base pixel size (same as current `draw_pixel_text` scale param)
- `vp_x`, `vp_y` = vanishing point in pixels (use `vp_spec_config.json` values — classroom VP_X=192, VP_Y=230)
- Scale correction: characters at VP distance = `scale * 0.65`; characters at canvas-far-edge distance = `scale * 1.0`. Linear interpolation between.
- The function should still use the 5×7 bitmap glyph system from `draw_pixel_text()`
- Fallback: if `vp_x=None` or `vp_y=None`, behave identically to `draw_pixel_text()` (graceful degradation)

After building, update the classroom chalkboard (`LTG_TOOL_bg_classroom.py`) to use the perspective helper if the visual result improves legibility. If it does not improve it (or makes it worse at this scale), note that and leave the flat version — do not force a change that doesn't help.

QA the updated classroom against existing thresholds: warm/cool ≤ 17.0, line_weight outliers ≤ 2.

Also check: the kitchen MIRI label from C43 — does it also benefit from perspective correction? Your call.

Report to my inbox.

Alex
