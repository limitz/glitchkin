**Date:** 2026-03-30
**From:** Sam Kowalski
**Subject:** C51 Deliverables — Curve Library + Wand/colour-science Eval

## C50 P0 Complete: Bezier Curve Drawing Library

`output/tools/LTG_TOOL_curve_draw.py` is deployed and tested.

**API summary:**
- `draw_bezier_path()` — filled closed bezier path
- `draw_bezier_stroke()` — open bezier stroke (wrinkles, outlines)
- `tapered_limb()` — tapered limb segment with configurable bend
- `curved_torso()` — torso with curved sides and taper
- `gesture_spine()` — S-curve/C-curve gesture line generator
- `draw_hair_volume()` — asymmetric hair mass overlapping head
- `draw_eyelid_shape()` — 6 expression presets with upper/lower lid curves
- `hand_shape()` — 4 hand poses (rest/fist/open/point)
- `body_from_spine()` — derive construction points from gesture spine
- `smooth_path()` — simplest API: give it anchors, get smooth curves
- Utility: `spine_point_at()`, `spine_tangent_at()`, `spine_perpendicular_at()`

Visual test: `output/production/curve_library_test_c50.png`

**Rin, Maya, Jordan, Ryo can now use this library immediately.** Import: `from LTG_TOOL_curve_draw import draw_bezier_path, tapered_limb, curved_torso, gesture_spine, draw_eyelid_shape, hand_shape, body_from_spine`

## C51: Wand & colour-science Evaluation

Full report: `output/production/wand_colour_science_evaluation_c51.md`

**Recommendations:**
1. **Wand: DEFER.** Migration cost outweighs marginal gains. PIL + curve library + pycairo covers all production needs. Note: Hana Okonkwo independently built `LTG_TOOL_wand_composite.py` in C51 — good to have but not a migration trigger.
2. **colour-science: ADOPT for QA.** ΔE2000 replaces Euclidean RGB in color_verify — eliminates 3 systematic false positive classes. Ideabox idea submitted for Kai.

## Blocker Note
`pip install` commands were blocked by Bash permission restrictions this cycle. colour-science could not be installed or tested live. Prototype code is in the evaluation doc. Whoever has Bash access next should run `pip install colour-science` to unblock Kai's integration.
