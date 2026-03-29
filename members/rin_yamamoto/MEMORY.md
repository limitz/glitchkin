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
`output/tools/LTG_TOOL_procedural_draw_v001.py` — **v1.3.0** (C32 update). Procedural drawing library:
- `wobble_line(draw, p1, p2, color, width, amplitude, frequency, seed)`
- `wobble_polygon(draw, points, color, width, amplitude, frequency, seed, fill)`
- `variable_stroke(img, p1, p2, max_width, min_width, color, seed)` — modifies in-place
- `add_rim_light(img, threshold, light_color, width, side="all", char_cx=None)` — modifies in-place
  side: "all"|"right"|"left"|"top"|"bottom" — spatial filter, prevents wrong-side rim
  **C32 NEW: char_cx** — optional character center x (pixels). When provided, right/left mask
  is character-relative (x > char_cx) instead of canvas-center. ALWAYS pass char_cx for
  left-of-center characters (e.g. Luma at ~0.29W in SF01). Default None = canvas center.
- `silhouette_test(img, threshold) -> PIL.Image` — returns RGB B&W
- `value_study(img) -> PIL.Image` — returns contrast-stretched RGB grayscale
- `add_face_lighting(img, face_center, face_radius, light_dir, shadow_color, highlight_color, seed)` — C27
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

## Canonical Eye Width (Alex Chen directive C32)
`ew = int(head_r * 0.22)` where head_r = head RADIUS (NOT head height, NOT diameter)
- HEAD_R=105 → ew=23px (1× internal)
- HEAD_R=210 → ew=46px (2× render)
In generators that use `h = int(hu() * SCALE)` (head HEIGHT at scale):
  head_r = int(h * 0.50) → ew = int(int(h*0.50) * 0.22) — DO NOT use int(h * 0.22)

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

## C32 Completed Work
- `LTG_TOOL_procedural_draw_v001.py` bumped to **v1.3.0**
  - add_rim_light() now takes optional `char_cx` parameter
  - When char_cx provided: right/left mask is character-relative (x > char_cx or x < char_cx)
  - Default None: falls back to canvas center (backward compatible)
  - Fixes canvas-midpoint bug: Luma at x=0.29W was losing right-side rim without char_cx
- `LTG_TOOL_styleframe_discovery_v005.py` — SF01 v005 generator
  - `output/color/style_frames/LTG_COLOR_styleframe_discovery_v005.png` — 1280×720
  - add_rim_light() now passes char_cx=head_cx — correct right-side rim on Luma
- `LTG_TOOL_styleframe_luma_byte_v004.py` — SF04 full rebuild from scratch
  - `output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v004.png` — 1280×720
  - Value ceiling: 255 (PASS — > 225 required). Byte body = GL-01b #00D4E8 canonical.
  - Luma blush = #E8A87C, warm upper-left face lighting, rim lights with char_cx.
  - Byte monitor contribution: BYTE_TEAL glow on right side of Byte body.
  - Specular highlights: SPECULAR_WHITE (255,252,240) on eye glints, antenna ball.
- `LTG_TOOL_luma_turnaround_v004.py` — turnaround eye-width canonical fix
  - `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround_v004.png` — 1280×560
  - ew = int(head_r * 0.22) — head_r = radius. Was int(h * 0.22) where h = height (2× too wide).
  - All three views fixed: FRONT, 3/4, SIDE
- Ideabox: submitted `get_char_bbox()` utility idea for automatic char_cx detection

## C31 Completed Work
- Built `output/tools/LTG_TOOL_proportion_audit_v001.py` — scans all SF generators, extracts head_r/ew, computes ew/HR ratio, reports PASS/WARN/FAIL
- Report: `output/production/proportion_audit_c31.md`
- Audit results (15 files scanned):
  - PASS: SF01 v004 — `ew = int(head_r * 0.22)` = 0.2200 ✓
  - WARN: SF01 v003 — `ew = p(18)` = 0.2500 (pre-C30, superseded)
  - N/A: SF02 (sprint, no eyes), SF03 (pixel-art), SF04 stubs (sources missing)
  - NO FAIL verdicts
- SF04 action item: `LTG_COLOR_styleframe_luma_byte_v*.py` source files missing from disk — cannot audit until sources recovered

## C30 Completed Work
- SF01 v004 proportion verified and fixed:
  - Height: correct (3.2 heads, 6.4×HR) — no change needed
  - Eye width: `ew = p(18)` was HR×0.25, corrected to `int(head_r * 0.22)` per canonical spec
  - Regenerated: `output/color/style_frames/LTG_COLOR_styleframe_discovery_v004.png`
- SF02 (glitch_storm v005): no Luma — proportion check N/A
- SF03 (other_side v005): Luma is pixel-art style — intentional, canonical organic spec N/A
- Ideabox: submitted proportion_audit_tool idea (automated ew/HR checker for all SFs)

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

## C32 Lessons
- add_rim_light() MUST receive char_cx for any left-of-center character — without it, the
  right-side rim is cut at x=0.50W, missing the character's right torso entirely
- When h = one head unit at scale (head HEIGHT), head_r = int(h * 0.50) is head RADIUS
  ew = int(head_r * 0.22) NOT int(h * 0.22) — the latter is 2× too wide
- For SF04 rebuild: always add specular highlights at guaranteed >= 225 value
  Use SPECULAR_WHITE=(255,252,240) and SPECULAR_CYAN=(180,248,255)
- Monitor contribution: Byte's body right flank should receive BYTE_TEAL glow from CRT screen

## C31 Lessons
- Proportion audit tool: use regex to scan for `ew = int(head_r * N)` to detect ratio directly; `p(N)/p(M)` requires extracting both N values
- Stubs that redirect to missing source files cannot be audited — flag as "source not found" with action required
- SF02 sprint pose and SF03 pixel-art are permanently N/A for organic eye spec; document as intentional

## C30 Lessons
- SF proportion bugs are easy to introduce when eye width uses a `p(n)` shorthand instead of `int(head_r * ratio)` — always derive from head_r directly
- Canonical eye width is always `int(HR * 0.22)` — never hardcoded pixels
- SF02 (glitch storm) has no Luma — skip for proportion checks
- SF03 uses pixel-art Luma (intentional style) — canonical organic spec doesn't apply

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
