**Date:** 2026-03-29 19:00
**To:** Rin Yamamoto
**From:** Producer (via Alex Chen)
**Re:** Cycle 26 — Role Shift: Procedural Art Engineer

---

## Your Role Has Changed

You are no longer a post-processing artist. You are now a **Procedural Art Engineer**, working alongside Kai Nakamura to build hand-drawn stylization and visual effects directly into the asset generation pipeline — at the point of creation, not after.

The stylize_handdrawn_v002 tool remains valid for legacy assets. New assets from C26 onward should have their visual character generated procedurally from the start.

---

## Study: /home/wipkat/artistry

A separate AI artist project lives at `/home/wipkat/artistry`. It has developed procedural drawing techniques through iterative critique. Read:
- `/home/wipkat/artistry/artist/memory.md` — the artist's accumulated lessons
- `/home/wipkat/artistry/tools/render_engine.py` — core drawing engine
- `/home/wipkat/artistry/tools/work_005_closeup_v2.py` — latest technique set
- Recent critique files in `/home/wipkat/artistry/output/` (work_003 through work_005)

**Specific techniques to extract and adapt for LTG:**
1. **Wobble paths** — organic, non-straight line drawing that makes lines feel hand-drawn. Extract the wobble algorithm and adapt it for PIL (Pillow).
2. **Variable stroke weight** — strokes that vary in width along their length, tapering at endpoints. Critical for organic character lines.
3. **Silhouette-first pipeline** — draw the character silhouette as a solid first, verify it reads, then add detail. This is a quality methodology, not just a visual technique.
4. **Volumetric face lighting** — split-light approach with brow-shadow, nose-on-cheek shadow, chin-on-neck shadow. Makes faces feel 3D.
5. **Rim lights** — thin bright edge on character silhouettes to separate them from backgrounds.
6. **Three-tier line weight** — already in LTG standards (9px/4.5px/1.5px at 2×), but verify the artistry project implements it consistently and extract any refinements.

---

## Your Cycle 26 Deliverable

Build `output/tools/LTG_TOOL_procedural_draw_v001.py` — a new drawing library for LTG that adds hand-drawn quality to PIL-based generators.

Required functions:
1. `wobble_line(draw, p1, p2, amplitude=2, frequency=8, seed=42)` — draws a slightly wobbly line between two points
2. `wobble_polygon(draw, points, amplitude=2, frequency=6, seed=42)` — draws a closed wobble-outlined shape
3. `variable_stroke_line(img, p1, p2, max_width=4, min_width=1, color=(0,0,0))` — PIL-based variable-width stroke (taper at ends, thicker in middle)
4. `add_rim_light(img, character_mask, light_color, width=3)` — adds a rim light edge on a character mask
5. `silhouette_test(img, threshold=128)` — returns a pure B&W silhouette image for squint testing
6. `value_study(img)` — converts to grayscale, stretches contrast, returns value study image

Test each function and include a `__main__` demo that generates a test output image.

---

## Coordinate with Kai
Kai is building QA tools (silhouette test, value range checker). Your `silhouette_test()` and `value_study()` functions will integrate with Kai's QA pipeline. Sync on interfaces.

---

## Standards
- All output images ≤ 1280px (prefer smaller for test outputs — 640px is fine for development)
- Output: `output/tools/LTG_TOOL_procedural_draw_v001.py`
- Test image: `output/tools/test_procedural_draw_v001.png` (small — 640px or less)

— Alex Chen, Art Director (relaying Producer directive)
