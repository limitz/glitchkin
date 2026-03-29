# Rin Yamamoto — MEMORY

## Role (Updated Cycle 26)
**Procedural Art Engineer** on "Luma & the Glitchkin."
Hand-drawn quality is built IN at generation time — no post-processing step.

## Project Context
- Comedy-adventure cartoon pitch. All assets generated via Python PIL.
- Style: CRT/pixel aesthetic (Glitch world) + warm hand-drawn domestic (real world).
- Output dir: `/home/wipkat/team/output/`
- Tools dir: `output/tools/`
- Render lib: `output/tools/LTG_TOOL_render_lib_v001.py` (canonical)

## Pipeline Rules
- Naming: `LTG_TOOL_[descriptor]_v[###].py` — procedural tools
- Output PNGs: `LTG_[CATEGORY]_[descriptor]_[variant]_v[###].png`
- After `img.paste()`: ALWAYS refresh `draw = ImageDraw.Draw(img)`
- After `variable_stroke()` or `add_rim_light()` or `add_face_lighting()`: ALWAYS refresh draw context
- PIL only — no cairocffi, no external deps beyond NumPy (optional)
- IMAGE SIZE RULE: ≤ 1280px hard limit. Test images ≤ 640px. Use `img.thumbnail()`.

## Image Handling Policy (All Agents — added C29)
- Before sending any image to Claude for inspection: ask if a tool could extract the insight. If so, MAKE THE TOOL.
- Before sending an image: ask if lower resolution suffices. If so, downscale.
- Never send high-resolution images to Claude unless absolutely necessary.
- Claude vision limitations: may hallucinate on low-quality/rotated/tiny images; limited spatial reasoning; approximate counting only.

## RETIRED (C26)
All stylization post-process scripts have been moved to `output/tools/legacy/`:
- `LTG_TOOL_stylize_handdrawn_v001.py` — RETIRED
- `LTG_TOOL_stylize_handdrawn_v002.py` — RETIRED
- `LTG_TOOL_batch_stylize_v001.py` — RETIRED
All `*_styled*.png` output images: DELETED.
Do NOT reference, fix, or regenerate any of these.

## Active Tools
`output/tools/LTG_TOOL_render_lib_v001.py` (v1.1.0) — 8 render functions incl. paper_texture
`output/tools/LTG_TOOL_procedural_draw_v001.py` — v1.2.0 (C28 update). Procedural drawing library:
- `wobble_line(draw, p1, p2, color, width, amplitude, frequency, seed)`
- `wobble_polygon(draw, points, color, width, amplitude, frequency, seed, fill)`
- `variable_stroke(img, p1, p2, max_width, min_width, color, seed)` — modifies in-place
- `add_rim_light(img, threshold, light_color, width, side="all")` — modifies in-place
  side: "all"|"right"|"left"|"top"|"bottom" — spatial filter, prevents wrong-side rim
- `silhouette_test(img, threshold) -> PIL.Image` — returns RGB B&W
- `value_study(img) -> PIL.Image` — returns contrast-stretched RGB grayscale
- `add_face_lighting(img, face_center, face_radius, light_dir, shadow_color, highlight_color, seed)` — NEW C27
- Test images: `output/tools/test_procedural_draw_v001.png`, `output/tools/test_face_lighting_v001.png`
- Kai interface-compatible: silhouette_test/value_study both PIL.Image in/out

## Canonical Palette (Authoritative)
| Color | Hex | RGB | GL code |
|---|---|---|---|
| CORRUPT_AMBER | #FF8C00 | (255,140,0) | GL-07 |
| BYTE_TEAL | #00D4E8 | (0,212,232) | GL-01b |
| UV_PURPLE | #7B2FBE | (123,47,190) | GL-04 |
| HOT_MAGENTA | #FF2D6B | (255,45,107) | GL-06 |
| ELECTRIC_CYAN | #00F0FF | (0,240,255) | GL-01a |
| SUNLIT_AMBER | #D4923A | (212,146,58) | RW-03 |

## Artistry Lessons (from `/home/wipkat/artistry` — studied C26/C27)
Note: `/home/wipkat/artistry` files may be permission-restricted in some sessions.
All key techniques have been extracted to MEMORY and implemented. No further reads needed.

### Wobble Paths (implemented in procedural_draw_v001)
- Sin-based perpendicular displacement; amplitude + ±20% random jitter; seeded per edge

### Variable Stroke Weight (implemented)
- Parabolic taper `4*t*(1-t)`; circle chain at varying radii; ±10% jitter per step

### Silhouette-First Methodology
- Draw silhouette first, verify shape reads, then use `silhouette_test()` as QA gate

### Volumetric Face Lighting (IMPLEMENTED C27)
- Split-light: brow shadow, nose-on-cheek shadow, chin-on-neck shadow
- PIL adaptation of Cairo radial gradient: stacked concentric ellipses with alpha falloff
- Feathering: non-linear alpha (t^1.5 or t^2.0) across 6–8 concentric steps
- Anatomical ratios: brow_y = cy − 0.25ry; nose_y = cy + 0.10ry; chin_y = cy + 0.70ry
- Highlight accent on lit side (cheekbone/forehead) using same soft-ellipse stack
- Organic edge detail via wobble_line on brow and chin boundaries
- Test image: `output/tools/test_face_lighting_v001.png` (600×300)

### Rim Lights (implemented)
- Edge dilation: dilate bright mask, subtract original, composite as RGBA

## Coordination
- Kai Nakamura: `LTG_TOOL_render_qa_v001.py` — silhouette_test/value_study interfaces matched
- Reports to Alex Chen

## C27 Completed Work
- `output/tools/LTG_COLOR_styleframe_luma_byte_v002.py` — SF04 v002 generator
- `output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v002.png` — 1280×720

## C28 Completed Work
- `output/tools/LTG_TOOL_procedural_draw_v001.py` bumped to v1.2.0
  - add_rim_light() now takes side="all"|"right"|"left"|"top"|"bottom" parameter
  - Spatial mask: PIL paste of 255 into half-canvas, ImageChops.multiply against edge_mask
  - Backward compat: default side="all" preserves prior behavior
- `output/tools/LTG_COLOR_styleframe_luma_byte_v003.py` — SF04 v003 generator (C28 fixes)
- `output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v003.png` — 1280×720
  - Blush fixed: RGB (232, 168, 124) alpha 65 — warm peach (was orange-red)
  - Byte body fill fixed: BYTE_TEAL (0, 212, 232) canonical GL-01b (was (0, 190, 210))
  - Rim light fixed: side="right" — cyan only on monitor-facing side of Luma

## C29 Completed Work
- `output/tools/LTG_TOOL_styleframe_discovery_v004.py` — SF01 v004 generator
- `output/color/style_frames/LTG_COLOR_styleframe_discovery_v004.png` — 1280×720
  - Canvas rescaled from 1920×1080 to 1280×720 using SX/SY/sp() scale factors
  - wobble_polygon() applied to: Luma head silhouette, CRT frame, couch seat, couch back, couch arm
  - variable_stroke() on Luma head perimeter: 8-arc technique around head ellipse
  - add_face_lighting(): warm lamp from upper-left (-1,-1), shadow=SKIN_SH, highlight=SKIN_HL
  - add_rim_light(side="right"): CRT teal (0,220,232) from right — discovery source
  - Blush corrected to warm peach (232,168,124) — matching SF04 v003 correction
  - BYTE_TEAL canonical (0,212,232) used throughout

## C27/C28/C29 Lessons
- Composition scales: use SX/SY factors (W/1920, H/1080) to port 1920×1080 coords to 1280×720
- sp(n) = int(n * min(SX,SY)) for uniform pixel widths/radii that scale proportionally
- variable_stroke on character perimeters: best done as 8-arc segments around an ellipse
- add_face_lighting before add_rim_light: face lighting shapes form, rim defines silhouette edge
- wobble_polygon on furniture (couch) works cleanly: organic seating volume with flat fill under
- Always refresh draw = ImageDraw.Draw(img) after variable_stroke / add_rim_light / add_face_lighting
- Rim light direction: use side= parameter to restrict to correct half-canvas — essential for
  physically correct lighting (CRT on right → side="right")
- draw_luma_head must accept img as argument (not just draw) to support variable_stroke and blush compositing

## Joined
Cycle 23 (2026-03-29)
