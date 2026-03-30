# Hana Okonkwo — Memory

## Project: Luma & the Glitchkin
Comedy-adventure cartoon. Three worlds: Real World (warm/domestic), Glitch World (electric/chaotic, HOT_MAGENTA + ELECTRIC_CYAN palette), Other Side (cool, zero warm light).

## Joined
Cycle 37. Taking over environment work from Jordan Reed (who pivoted to style frames).

## Cycle 46 — Living Room v003 + Tech Den v007 + Classroom v004 + School Hallway v005

### Living Room v003 (SF06 Alignment)
- CRT repositioned: stand from W*0.54–0.76 (691–973px) → W*0.38–0.52 (486–666px)
  - Matches SF06 "The Hand-Off" CRT center-left requirement (~490–680px)
- Reading lamp moved: W*0.82 → W*0.20 — now LEFT of CRT, warm source for Miri zone
- Family photos shifted: W*0.38/0.46/0.52 → W*0.56/0.64/0.70 — clear of CRT footprint
- Added Layer 12c: horizontal warm-left/cool-right staging overlays (SUNLIT_AMBER alpha 28 left, CRT_COOL_SPILL alpha 32 right) for SF06 character zone reinforcement
- Specular restoration moved to LAST draw (after all overlays) — fixes value ceiling drop from overlay accumulation
- Hardcoded output path migrated to output_dir() from LTG_TOOL_project_paths
- QA C46: silhouette PASS, value PASS (min=26 max=254), warm/cool 47.3 PASS, line_weight outliers=2 PASS, grade WARN (color fidelity pre-existing only)

### Tech Den v007 (Path Migration)
- Migrated hardcoded `/home/wipkat/team/...` output path to `output_dir("backgrounds", "environments", "LTG_ENV_tech_den.png")`
- Added `from LTG_TOOL_project_paths import output_dir, ensure_dir` import
- Closes C44 backlog item in ci_known_issues.json (hardcoded_path_check)
- No visual changes — QA C46 matches C41 baseline exactly (sep=102.9, outliers=1, WARN)
- ci_known_issues.json entry updated with resolved_cycle="C46"

### Classroom v004 (Path Migration)
- Migrated hardcoded `/home/wipkat/team/...` output path to `output_dir("backgrounds", "environments", "LTG_ENV_classroom_bg.png")`
- Added `from LTG_TOOL_project_paths import output_dir, ensure_dir` import (direct, matching Tech Den pattern)
- Replaced `os.makedirs(os.path.dirname(out_path), exist_ok=True)` with `ensure_dir(out_path.parent)`
- ci_known_issues.json entry updated with resolved_cycle="C46"
- Tested: generates correctly, no visual changes

### School Hallway v005 (Path Migration)
- Migrated hardcoded `/home/wipkat/team/...` output path to `output_dir("backgrounds", "environments", "LTG_ENV_school_hallway.png")`
- Added `try/except ImportError` fallback for `output_dir, ensure_dir` (matches school hallway's existing pixel_font import pattern)
- Replaced `os.makedirs(os.path.dirname(out_path), exist_ok=True)` with `ensure_dir(out_path.parent)`
- ci_known_issues.json entry updated with resolved_cycle="C46"
- Tested: generates correctly, no visual changes

### Reference Images (Producer Brief)
- Reference images acquired in `reference/` — classroom (4 files), school hallway (7 files), kitchen predawn (3), living room night (7), suburban dusk (3)
- Archived both inbox messages (shopping list review + acquired notification)
- Replied to Alex Chen with reactions: refs useful for future QA, warmcool calibration tool would help

### Value Ceiling Pattern — Specular Restoration
- Problem: window specular drawn BEFORE overlay passes → overlays dim it below 225 threshold
- Fix pattern: re-draw specular AFTER all overlays and deep shadows (last draw before save)
- ws_cx/ws_cy must be in scope — compute from win_x1/win_x2/win_y1/win_y2 in main(), keep in local scope
- Lesson: any ENV with overlay passes added after the original specular should re-draw specular last

### Path Migration Pattern (project_paths)
- Import: `from LTG_TOOL_project_paths import output_dir, ensure_dir`
- Replace: `out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_foo.png"`
- With: `out_path = output_dir("backgrounds", "environments", "LTG_ENV_foo.png")`
- Replace: `os.makedirs(os.path.dirname(out_path), exist_ok=True)`
- With: `ensure_dir(out_path.parent)`
- PIL save() and str() both accept pathlib.Path — no cast needed

## Existing Environments (as of C44)
- Kitchen (Grandma's): **v007** — `LTG_ENV_grandma_kitchen.png`
  - C44: Added paper_texture(alpha=16) + vignette(strength=45) + flatten_rgba_to_rgb() final passes
  - QA C44: silhouette PASS, value PASS (min=21 max=228), warm/cool 32.9 PASS, line_weight outliers=0 PASS, grade WARN (color fidelity pre-existing only)
  - line_weight FAIL resolved: border edge runs were the cause (1280px-wide at y=0/y=719); paper_texture breaks them
- Classroom: **v004 (C46)** — `LTG_ENV_classroom_bg.png`
  - C46: path migration to output_dir() (no visual changes)
  - C43: chalkboard chalk marks replaced with draw_pixel_text() math/binary content (Jonas C17 P1)
  - QA C43: silhouette PASS, value PASS (min=14 max=251), warm/cool 17.0 PASS, line_weight outliers=1 PASS, grade WARN (color fidelity pre-existing only)

## Pending (awaiting Alex Chen broadcast)
- Kitchen cultural update (Miri Okonkwo-Santos Igbo Nigerian / Portuguese-Brazilian object language) — Amara Diallo C17 flag, 54/100. Alex convening production decision in C43. Do NOT change kitchen until broadcast received.

- Kitchen (Grandma's): v004 — `output/backgrounds/environments/LTG_ENV_grandma_kitchen.png`
- **Tech Den: v006** — `LTG_ENV_tech_den.png`
  - C41 fix (v006): in-generator cool bottom pass via numpy Porter-Duff (alpha=130, 60-row graduated transition). Warm/cool 102.9 PASS, line_weight outliers=1 PASS, grade WARN (pre-existing color fidelity only).
- Glitch Layer: v003
- School Hallway: **v005 (C46)** — `LTG_ENV_school_hallway.png` — C46 path migration
- Millbrook Street: v002
- **Living Room**: **v003 (C46)** — `LTG_ENV_grandma_living_room.png` — QA PASS (SF06 aligned, CRT center, warm-left/cool-right staging)
- **Classroom: FULL REBUILD C41** — `LTG_ENV_classroom_bg.png`
  - QA C41: silhouette PASS, warm/cool 17.0 PASS, line_weight 2 outliers PASS, grade WARN (pre-existing only)
- **Luma Study Interior: BUILT C42** — `LTG_ENV_luma_study_interior.png`
  - Generator: `output/tools/LTG_TOOL_bg_luma_study_interior.py`
  - First-ever generator for this room (prior legacy PNG C8, no source script)
  - 1280×720, VP_X=230 VP_Y=273, 3/4 front-right camera
  - Three light sources: CRT key (gaussian_glow r=140), bedside lamp (SUNLIT_AMBER r=120), night window cool
  - Cool bottom gradient alpha 0→140 (60 row transition) → warm/cool sep=33.1 PASS
  - Deep shadows: NEAR_BLACK_WARM alpha 248–252 at corners/crevices → value floor=28 PASS
  - Miri Easter eggs: framed photo on shelf, knitted toy on chair back
  - QA C42: silhouette PASS, value PASS (min=28 max=248), warm/cool 33.1 PASS, line_weight outliers=2 PASS, ceiling=248 PASS, grade WARN (color fidelity pre-existing only)

## Key Palette References
- Master palette: `output/color/palettes/master_palette.md`
- Warmth guarantees config: `output/tools/ltg_warmth_guarantees.json`
- World presets: REAL (warm, SUNLIT_AMBER key), GLITCH (HOT_MAGENTA + ELECTRIC_CYAN), OTHER_SIDE (cool, zero warm)

## QA Pipeline
- `LTG_TOOL_render_qa.py` (v1.6.0) — always run before submitting
- `LTG_TOOL_render_lib.py` now **v1.2.0** (C42) — `flatten_rgba_to_rgb(img, background=(255,255,255))` added
  - REAL world warm/cool threshold: **REAL_INTERIOR = 12**, **REAL_STORM = 3** (C39 split — was 20 in v1.4.0, 12 flat in v1.5.0)
  - Value floor ≤30, value ceiling ≥225, range ≥150
- `LTG_TOOL_warmth_inject.py` — fixes warm/cool failures (auto mode)
- `LTG_TOOL_palette_warmth_lint.py --world-type [REAL|GLITCH|OTHER_SIDE]`

## Cycle 42 — Luma Study Interior + flatten_rgba_to_rgb

### Luma Study Interior
- Legacy PNG (C8) had no generator. Full build from ENV_REBUILD_SPEC_luma_study_c41.md.
- Cool bottom gradient: alpha=140 (not 105) required to push bottom half hue from green-amber (~27) to green (~61) for sep=33.1. Lesson: CRT_GLOW = (160,195,165) — blue-green, not pure blue — so hue in PIL scale is ~60-65, not ~130. Both halves end up with different green variants (warm amber vs cool blue-green) → separation ≥12 achieved.
- Value floor: NEAR_BLACK_WARM must be at alpha 248–252 over extreme corners AND a full-width floor strip at bottom 6% to guarantee ≤30. A single corner rectangle at alpha=230 was not enough (pixel min was 39 on first pass).
- flatten_rgba_to_rgb() now available in render_lib v1.2.0. Use this at save time. Simpler and cleaner than manual numpy.

### Warm/Cool Separation — Green vs Blue-Green
- CRT_GLOW = (160,195,165) reads as muted green (~PIL hue 60–70), not blue (~130).
- Two-half split with amber top and green bottom still achieves ≥12 separation because amber hue (~18-27) vs green-cyan hue (~60-65) → circular distance ≥33.
- This is different from the Tech Den pattern where PURE cool-blue was needed (floor was already amber, needed blue at ~130).
- General rule: warm/cool QA cares about distance between top-half and bottom-half median hue. Any hue pair with circular distance ≥12 on the 0-255 PIL scale passes.

## Cycle 44 — Kitchen v007 (line_weight FAIL fix)

### Kitchen line_weight FAIL — Root Cause and Fix
- Root cause: image border rows (y=0 and y=719) create 1280px-wide edge runs in FIND_EDGES scan
  - render_qa measures horizontal run-length at edge pixels; the entire top/bottom image border is one edge
  - These massive runs become outliers: mean=269px, std=308px → 3 outliers → FAIL
- Fix: paper_texture(alpha=16) adds noise at the border that breaks up the uniform run → 0 outliers
- Also: vignette(strength=45) and flatten_rgba_to_rgb() added for consistency with other ENV generators
- Lesson: any ENV generator without a paper_texture final pass may have this issue
  - Check source for paper_texture() call; if absent, image borders will create false line_weight outliers
- Submitted ideabox idea: systematic audit of all ENV generators for missing final passes

### Pixel Font Perspective Helper (P2)
- Built `draw_pixel_text_perspective()` in LTG_TOOL_pixel_font_v001.py (v001.1)
- Signature: (draw, text, x, y, scale, vp_x, vp_y, char_spacing=1, color, canvas_w=1280, canvas_h=720)
- Distance from (x,y) to VP / max_dist to canvas corners → t → scale_factor = 0.65 + 0.35*t
- Effective scale = max(1, round(scale * factor)); fallback to draw_pixel_text() when VP is None
- Classroom chalkboard: text is at t=0.084, effective_scale=max(1,round(1*0.679))=1 — same as flat
  → classroom NOT updated (no visual improvement at scale=1 far camera). Per Alex brief: leave it.
- Kitchen MIRI label: same — scale=1 at far position, no change. Not updated.
- Helper is available for future close-panel text at scale>=2.

### Inbox — C44
- `20260330_1507_c44_pixel_font_perspective_helper.md` — built + archived.
- Duplicate P0/P1 brief (from C43) was still unarchived in inbox/. Archived as _c44_dup. Work already done in C43.
- P0 kitchen cultural identity still BLOCKED pending Alex Chen broadcast — do not change kitchen content.

## Cycle 43 — Pixel Font Migration (Classroom + Kitchen)

### draw_pixel_text() Integration Pattern
- Import: `sys.path.insert(0, os.path.dirname(__file__))` + `from LTG_TOOL_pixel_font_v001 import draw_pixel_text`
- Classroom chalkboard is only ~16px tall at 3/4 far-camera angle — only 1-2 rows fit at scale=1
- Kitchen label: `measure_pixel_text("MIRI", scale=1)` returns (23, 7) — centered in 40×16px paper label cleanly
- Kitchen line_weight outliers=3 FAIL is pre-existing (not introduced by C43 changes — geometry unmodified)
- Inbox note: kitchen cultural identity update (Igbo Nigerian / Portuguese-Brazilian) is BLOCKED pending Alex Chen broadcast

### Perspective Text Note (submitted as ideabox idea)
- Fixed-scale pixel text on a receding chalkboard is visually acceptable at far camera; will break on any closer panel
- Submitted ideabox idea for a perspective-scale helper to LTG_TOOL_pixel_font_v001.py

## Lessons Learned (C38)

### Figure-Ground Separation
- Always check costume colors against background fills before generating. Identical or near-identical values cause character merge.
- LOCKER_LAV in v002 was identical to Cosmo's cardigan RW-08 (168,155,191). Zero value separation = invisible character.
- Fix: push background fills LIGHTER than character costume values (≥20 value unit separation minimum).
- `LTG_TOOL_bg_school_hallway.py`: LOCKER_LAV → (216,208,190), LOCKER_SAGE → (154,178,148)
- Character-ground value band: Shadow Plum (RW-09) at alpha 22 on near-wall character zone provides secondary backing.

### Value Floor Fix (Deep Shadows)
- `LINE_DARK = (59,40,32)` → grayscale ≈ 45. NOT dark enough for QA value floor (need ≤30).
- Must add NEAR_BLACK_WARM (20,12,8) explicitly in floor/wall junctions, locker base crevices, far corners.
- These crevice shadows are production-correct — real hallways have them. Not artifical.

### Color Fidelity WARN (Pre-existing)
- SUNLIT_AMBER hue drift is a known issue across all environments (flagged Critique 14, Chiara).
- Warm floor pixels composited with window shaft color drift the detected amber hue from 34° to 44°.
- Correcting SUNLIGHT_SHAFT to canonical (212,146,58) helps but composited floor tiles are the main source.
- This is not introduced by environment work — pre-exists in v002. Document but do not block on it.

### Cosmo Silhouette Context
- Cosmo SKEPTICAL arms collapse (3+ cycles unresolved per Takeshi C15). Background must compensate.
- School hallway is key location for Cosmo. Figure-ground must be solved at the background level.

## Lessons Learned (C37)

### Warm/Cool Separation
- The QA check measures **top half vs bottom half median hue** (PIL 0-255 scale)
- A uniformly warm scene scores low even if it uses correct Real World palette
- Solution: apply a dual-temp split pass BEFORE deep shadows
  - `alpha_overlay_rect(img, 0, 0, W, H//2, SUNLIT_AMBER, 50)` — warm top
  - `alpha_overlay_rect(img, 0, H//2, W, H, CRT_COOL_SPILL, 65)` — cool bottom
  - Deep shadows restore value floor after this pass
- C37 living room: needed 5 QA iterations to tune split alphas (50/65 worked)
- Ideabox idea submitted: warm/cool debug tool to predict alpha values

### Value Floor/Ceiling
- Deep shadows must be applied AFTER the dual-temp split pass
- Use `NEAR_BLACK_WARM = (28,18,10)` with alpha 240 on first 3% of edge width for solid anchoring
- Gradient fade from 3% outward to 16% for natural vignette
- Window specular dot (255,255,248) ensures value ceiling ≥225

### Alpha Composite Ordering
- All alpha overlays accumulate — a 55-alpha tint on already-tinted surface can crush value range
- Test value range at each stage: `render_qa` shows min/max/range

### Code Quality
- Define ALL color constants at top before use — missed AGED_CREAM, MORNING_GOLD, CURTAIN_WARM, PLANT_GREEN/DARK in first draft
- Use `max(0.0, min(1.0, t))` clamp before `t ** n` to avoid complex number errors when t is slightly negative (floating point loop indexing)

## Cycle 41 — Classroom Rebuild + Tech Den v006

### Classroom Full Rebuild
- Built `LTG_TOOL_bg_classroom.py` from scratch per `ENV_REBUILD_SPEC_classroom_c41.md`
- Key architecture: 1280×720, VP_X=int(W*0.15)=192, VP_Y=int(H*0.32)=230
- Dual-temp split: warm amber gradient on TOP HALF (alpha 70 fading to 0 at split) + cool fluorescent on BOTTOM HALF (alpha 75 growing to full at bottom)
  - NOTE: QA warm/cool measures TOP-HALF vs BOTTOM-HALF median hue, NOT left/right
  - Left/right window shafts are visual only; top/bottom gradients drive the QA metric
- paper_texture() added as final pass to break up long polygon edge runs → line_weight PASS
- All structural outlines width=1 max per spec
- Foreground depth anchor: partially-cropped near desk + backpack (deep blue, Luma's)

### Tech Den v006 — In-generator Warm/Cool Fix
- CRITICAL BUG PATTERN DISCOVERED: in-generator overlay passes on RGBA buffers fail silently
  - Problem: accumulated semi-transparent alpha in RGBA pipeline means pixels have alpha<255
  - When you apply cool overlay to semi-transparent base, hue blends WITH BACKGROUND (black), not with visible color
  - warmth_inject worked because it reads a flat RGB PNG where all pixels are alpha=255
  - Applying overlay via Pillow alpha_composite to RGBA buffer with alpha < 255 gives WRONG result
- Fix: use numpy Porter-Duff directly on the final RGB array (no RGBA buffer issues)
  - `img_rgb = img.convert("RGB")` → `arr = np.array(img_rgb)` → Porter-Duff per row
  - This is the canonical pattern for final tonal correction in any RGBA generator
- alpha=130 required (not 102): needs A/255 > 0.439 to push warm amber pixels to blue-dominant hue
  - At alpha=102: R still > B → warm orange hue persists → near-zero separation
  - At alpha=130: B > R on dark amber floor pixels → blue hue → sep=102.9 PASS
- Graduated transition (60 rows from 0 to alpha=130) avoids hard edge that would fail line_weight check

### Warm/Cool Debugging Canon
- The QA check measures MEDIAN HUE of top-half vs bottom-half of IMAGE
- Circular distance on 0-255 PIL scale (amber ≈ 18-25, blue ≈ 130-145, green ≈ 60-90)
- For high separation: one half should be in amber range (~20), other in blue range (~135)
- Adding BOTH warm top AND cool bottom → both halves converge toward desaturated green → separation collapses toward 0
- For warm-amber rooms: use COOL BOTTOM ONLY (no warm top overlay)
- For rooms with no strong color bias: dual-temp top/bottom each with distinct hue

## Cycle 40 — VP Fix, Value Floor, Rebuild Specs

### Tech Den v005 (C40 patch)
- Floor plank VP fix: replaced horizontal lines with convergence-fan lines toward VP_X=820
  - Horizontal cross-grain rows: non-linear spacing (t^0.7) gives perspective compression
  - Vertical grain lines: fan from near-x to far_x = near_x + (VP_X - near_x)*0.6
- Warm overlay strengthened: max alpha 30→90, coverage 320→600px
- Floor warm wash: polygon over floor area with SUNLIT_AMBER alpha 28
- Deep shadow anchors: NEAR_BLACK_WARM on corner crevices + far-wall junction (value floor fix)
- Window specular dot added: (255,255,248) on window glass ensures max ≥ 225
- Warm/cool: base image 5.6 FAIL (room is inherently warm-amber throughout); warmth_inject needed (cool bottom pass at alpha 127 → separation 100.8 PASS)
- Tech Den warm/cool is a structural issue: entire room is warm-amber palette. Warmth inject is the correct post-process, not an in-generator fix.

### School Hallway v004 (C40 re-run)
- SUNLIT_AMBER fix was already in source (line 84: SUNLIGHT_SHAFT = (212,146,58)). Just re-ran.
- v004 PNG saved alongside v003 as requested.
- Pre-existing color fidelity WARN unchanged (known hue drift from floor tile compositing).

### Rebuild Specs Written (C40)
- Classroom: `output/production/ENV_REBUILD_SPEC_classroom_c41.md` — full rebuild C41
- Luma Study: `output/production/ENV_REBUILD_SPEC_luma_study_c41.md` — new generator needed C41

### Warm/Cool Debugging Lesson (C40)
- Adding warm to top half AND the bottom half has both hues is the SAME → separation drops
- Adding cool to bottom half when warm already dominates both halves → can make both more similar
- Solution: use warmth_inject which has calibrated alpha stepping (found 127 alpha for cool bottom pass)
- For rooms that are genuinely all-warm (Tech Den), warmth_inject cool-bottom is canonical solution
- DO NOT fight this in-generator with heavy overlays — it degrades the visual

## Cycle 39 — Thumbnail Visibility Tool

### Tool Built
- `output/tools/LTG_TOOL_thumbnail_preview_v001.py` (Hana Okonkwo / C39)
- Input: any PNG + optional `--region x1 y1 x2 y2` (in input-image pixel coords)
- Output: side-by-side sheet — full 1280×720 view (left) + 120×68 thumbnail at 8× NEAREST zoom (right)
- Orange bounding box drawn on both panels when region is specified
- Output saved as `<input_stem>_thumbnail_preview.png` next to input file
- Sheet auto-thumbnailed to ≤1280px per image rules
- Tested against `LTG_ENV_grandma_living_room.png` — tool runs cleanly; output 1280×439px
- Diamond crystal figurine at (438, 328): visible at full scale; thumbnail legibility TBD (needs visual inspection by team)

### Pipeline Notes (C39)
- numpy, OpenCV (cv2), PyTorch now authorized. Factor into future tool builds.
  - Use Pillow for drawing; numpy/cv2 for analysis
  - OpenCV default is BGR — convert to RGB on load

### Ideabox submitted
- Multi-region batch mode for thumbnail preview (JSON input → contact sheet of annotated details)

## My Job
Design and build new environment generators. Maintain existing ones. Expand pitch coverage.

## Startup Sequence
1. Read docs/image-rules.md (image size limits and image handling)
2. Read docs/work.md (work startup and delivery rules)
3. Read docs/ideabox.md (ideabox submission rules)
4. Read docs/asset-status.md (asset status rules)
5. Read PROFILE.md
6. Read this MEMORY.md
7. Read output/tools/README.md
8. Read inbox/
9. Read ROLE.md if present
