**Date:** 2026-03-29 19:40
**To:** Rin Yamamoto
**From:** Producer
**Re:** Cycle 29 — Apply procedural quality to SF01 Discovery

---

SF01 "Discovery" is the only style frame still at v003 with no procedural quality treatment. SF03/SF04 now use wobble outlines and variable stroke. SF01 should too.

## Task — SF01 v004 with procedural quality

Find the SF01 generator in `output/tools/` (search for "discovery" or "sf01").

Create `output/tools/LTG_TOOL_styleframe_discovery_v004.py` that generates:
`output/color/style_frames/LTG_COLOR_styleframe_discovery_v004.png`

Apply procedural techniques using `LTG_TOOL_procedural_draw_v001.py` v1.2.0:
- `wobble_polygon()` / `wobble_line()` on key outlines (Luma silhouette, furniture, CRT frame)
- `variable_stroke()` on Luma's head perimeter
- `add_rim_light(side="right")` on Luma — cool CRT light from the right (the CRT is the discovery source)
- `add_face_lighting()` — warm lamp light from upper-left in grandma's kitchen

Canonical constraints:
- SF01 is the warm domestic scene — no Glitch palette in the Real World zones
- Byte emerges from the CRT (the moment of discovery) — his teal glow is on the CRT side only
- Keep all palette values from v003

Image size rule: ≤ 1280px. Apply `img.thumbnail((1280, 1280), Image.LANCZOS)` before saving.

After `img.paste()` or `alpha_composite()`: always refresh `draw = ImageDraw.Draw(img)`.

Send completion report to `members/alex_chen/inbox/` when done.

— Producer
