**Date:** 2026-03-31
**From:** Producer
**Subject:** C53 — Build canonical char_byte.py and char_glitch.py modular renderers

Rin,

C53 priority is modular character renderers.

**Task 1 (P0): `LTG_TOOL_char_byte.py`**
- Extract Byte's cairo drawing engine from `LTG_TOOL_byte_expression_sheet.py` into a standalone canonical renderer module.
- Export: `draw_byte(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface`
- Must support all 10 existing expressions. Include cracked eye detail.
- Byte body = OVAL, color = GL-01b #00D4E8 BYTE_TEAL.

**Task 2 (P0): `LTG_TOOL_char_glitch.py`**
- Extract Glitch's cairo drawing engine from `LTG_TOOL_glitch_expression_sheet.py` into a standalone canonical renderer module.
- Export: `draw_glitch(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface`
- Must support all 9 existing expressions. Diamond body with bulge.

**Interface contract:**
- Same function signature pattern as all char_*.py modules
- Return cairo.ImageSurface (ARGB, transparent background)
- Accept `scale` parameter for resolution independence
- Accept `scene_lighting` dict for environment integration
- Byte and Glitch are exempt from shoulder involvement rule (non-humanoid)

Run face test gate on outputs at sprint scale.

— Producer
