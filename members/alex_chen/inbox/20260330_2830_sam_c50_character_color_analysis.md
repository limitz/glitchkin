**Date:** 2026-03-30
**From:** Sam Kowalski
**Subject:** C50 Complete — Character Color Rendering Analysis + Prototype Tool

## Summary

Completed all 4 tasks from the C50 assignment.

### Task 1: Character vs Background Color Analysis
Diagnosed 5 specific reasons our characters look flat:
1. **No scene lighting on characters** — backgrounds get warm/cool overlays, characters do not
2. **Shadow placement is geometric, not anatomical** — left-half rectangle, not form-following curves
3. **No warm-cheek/cool-edge skin variation** — reference shows all do this subtly
4. **No hair scene-color absorption** — dark hair should pick up ambient scene hue
5. **Hard rectangle edges with no integration** — no outline color response to scene

### Task 2: Prototype Tool
Built `LTG_TOOL_character_color_enhance.py` (registered in tools/README.md) with 5 overlay functions:
- `apply_scene_tint()` — scene lighting on character (alpha capped at 30 for warmth safety)
- `apply_skin_warmth()` — warm-cheek / cool-edge + blush
- `apply_form_shadow()` — curved torso-diagonal / limb-underside / inseam shadow shapes
- `derive_scene_outline()` — per-world outline color
- `apply_hair_absorption()` — 2x tint strength on hair zones

All are post-draw overlays. Integration = one function call after the character is drawn.

### Task 3: Reference Show Study
Analyzed Hilda and The Owl House references. Key finding: both use flat base fills (like us). The difference is that their characters **receive scene lighting**. Hilda's simplicity works because the flat fills respond to environmental color. The Owl House goes further with multi-zone cel-shadow + explicit scene overlay.

### Task 4: Before/After Demo
Generated comparison image at `output/color/LTG_COLOR_character_enhance_demo_c50.png`.

## Deliverables
- Analysis: `output/color/LTG_COLOR_character_rendering_analysis_c50.md`
- Tool: `output/tools/LTG_TOOL_character_color_enhance.py`
- Demo: `output/color/LTG_COLOR_character_enhance_demo_c50.png`

## Integration Recommendation
Priority order for Jordan/Rin: (1) apply_scene_tint on SF04 + SF05 first — highest impact, lowest risk. (2) apply_form_shadow on torsos. (3) apply_skin_warmth on faces. The scene tint alone will close most of the gap with reference shows.

## Warmth Safety Note
Scene tint alpha is hard-capped at 30 (~12%). At this level, HOODIE_ORANGE (#E8703A) remains R-dominant even under maximum cyan tint. Warmth lint PASS is preserved. The alpha cap was derived from the C18 cyan-dominance threshold analysis (hoodie needs alpha >= 41% to violate).
