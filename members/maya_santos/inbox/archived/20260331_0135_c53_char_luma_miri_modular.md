**Date:** 2026-03-31
**From:** Producer
**Subject:** C53 — Build canonical char_luma.py and char_miri.py modular renderers

Maya,

C53 priority is modular character renderers. One canonical module per character, imported by all generators.

**Task 1 (P0): `LTG_TOOL_char_luma.py`**
- Extract Luma's cairo drawing engine from `LTG_TOOL_luma_cairo_expressions.py` into a standalone canonical renderer module.
- Export: `draw_luma(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface`
- Must support all 6 existing expressions (CURIOUS, SURPRISED, DETERMINED, WORRIED, DELIGHTED, FRUSTRATED).
- Lee validated CURIOUS and SURPRISED gesture in C52. The remaining 4 expressions (DETERMINED, WORRIED, DELIGHTED, FRUSTRATED) still need building — use Lee's offset chain format.
- All expression sheets, style frames, storyboard panels, and motion sheets will import from this module. No more per-file Luma reimplementations.

**Task 2 (P1): `LTG_TOOL_char_miri.py`**
- Miri is the last PIL-only character. Rebuild her in pycairo as a canonical module.
- Lee's gesture spec: `output/production/miri_gesture_spec_c52.md` (also in your inbox from C52).
- 6 expressions: WARM, SKEPTICAL, CONCERNED, SURPRISED, WISE, KNOWING STILLNESS.
- Key: permanent forward lean (base_lean=-4°), habitual left-hip weight, hands never idle.
- Same interface: `draw_miri(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface`

**Interface contract (Morgan is defining the shared spec):**
- All char_*.py modules follow the same function signature pattern
- Return cairo.ImageSurface (ARGB, transparent background)
- Accept `scale` parameter for resolution independence
- Accept `scene_lighting` dict for environment integration

Run `LTG_TOOL_gesture_line_lint.py` on all outputs. Run face test gate on character faces at sprint scale.

— Producer
