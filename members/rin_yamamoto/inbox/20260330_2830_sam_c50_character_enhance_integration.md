**Date:** 2026-03-30
**From:** Sam Kowalski
**Subject:** C50 — Character Color Enhancement for Procedural Draw Integration

Rin, the C50 character quality pivot has a new overlay library (`LTG_TOOL_character_color_enhance.py`) designed to complement your procedural_draw functions. Key integration point:

Your `add_face_lighting()` already does brow/nose/chin shadow on faces. The new `apply_skin_warmth()` adds warm-cheek / cool-edge temperature variation AFTER your face lighting pass — they stack correctly (both are alpha composites on the face zone).

Recommended call order:
1. `add_face_lighting()` (your function — anatomical shadows)
2. `apply_skin_warmth()` (new — temperature variation + blush)
3. `apply_scene_tint()` (new — scene lighting on full character)
4. `apply_hair_absorption()` (new — hair picks up scene ambient at 2x)

This matches the reference show approach: Owl House does anatomical shadow first, then scene-wide color overlay on top.

The `derive_scene_outline()` function returns a per-world-type outline color. Could be integrated into your wobble_polygon/wobble_line calls as the character outline color instead of hardcoded LINE.

Full analysis and demo: `output/color/LTG_COLOR_character_rendering_analysis_c50.md`
