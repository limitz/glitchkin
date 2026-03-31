**Date:** 2026-03-31
**From:** Producer
**Subject:** C53 — Build canonical char_cosmo.py modular renderer

Sam,

C53 priority is modular character renderers.

**Task (P0): `LTG_TOOL_char_cosmo.py`**
- Extract Cosmo's cairo drawing engine from `LTG_TOOL_cosmo_expression_sheet.py` into a standalone canonical renderer module.
- Export: `draw_cosmo(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface`
- Lee's gesture spec in your inbox and at `output/production/cosmo_gesture_spec_c52.md`.
- 6 expressions: AWKWARD, WORRIED, SURPRISED, SKEPTICAL, DETERMINED, FRUSTRATED.
- Key: angular body language (joint breaks, not smooth curves), glasses tilt = head_tilt * 0.4, signature pose SKEPTICAL.
- Recommended build order: SKEPTICAL + SURPRISED first to validate angular-break approach.
- Apply your color enhancement pass (`LTG_TOOL_character_color_enhance.py`) as an optional post-draw parameter.

**Interface contract:**
- Same function signature as Maya's char_luma.py
- Return cairo.ImageSurface (ARGB, transparent background)
- Accept `scale` parameter for resolution independence
- Accept `scene_lighting` dict for environment integration

Run `LTG_TOOL_gesture_line_lint.py` on all 6 expressions — all must PASS.

— Producer
