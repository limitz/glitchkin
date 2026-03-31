**Date:** 2026-03-31
**From:** Producer
**Subject:** C53 — Modular renderer architecture + CI enforcement

Morgan,

C53 priority is modular character renderers. You define the shared architecture.

**Task 1 (P0): Shared interface definition**
- Create `LTG_TOOL_char_interface.py` — defines the standard interface contract for all `char_*.py` modules.
- Standard function signature: `draw_X(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface`
- Document parameter types, defaults, and return value expectations.
- Include a `validate_char_module(module)` function that checks a char_*.py module exports the required interface.

**Task 2 (P0): CI lint for modular compliance**
- Add a check to `LTG_TOOL_ci_suite.py` that detects direct character drawing in scene generators.
- Scene generators (style frames, storyboard panels, motion sheets) should import from `char_*.py` — not draw characters inline.
- Pattern to flag: any scene generator file that calls `cairo.Context` methods to draw body parts without importing a `char_*.py` module.

**Task 3 (P1): Migrate bezier remaining**
- Continue bezier migration (batch 1 done C52). Check `python3 output/tools/LTG_TOOL_curve_utils.py --audit` for remaining files.

— Producer
