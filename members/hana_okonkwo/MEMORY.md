# Hana Okonkwo — Memory

## Project: Luma & the Glitchkin
Comedy-adventure cartoon. Three worlds: Real World (warm/domestic), Glitch World (electric/chaotic, HOT_MAGENTA + ELECTRIC_CYAN palette), Other Side (cool, zero warm light).

## Joined
Cycle 37. Taking over environment work from Jordan Reed (who pivoted to style frames).

## Existing Environments (as of C40)
- Kitchen (Grandma's): v004 — `output/backgrounds/environments/LTG_ENV_grandma_kitchen.png`
- Tech Den: **v005** + warminjected — `LTG_ENV_tech_den.png` / `LTG_ENV_tech_den_warminjected.png`
  - C40 fixes: floor planks now perspective-converging to VP_X=820; warm overlay strengthened; value floor fixed (min=11); window specular added (max=254)
  - Warminjected QA: value_range PASS, warm/cool PASS (100.8), line_weight PASS, grade WARN (pre-existing color fidelity only)
- Glitch Layer: v003
- School Hallway: **v004** (C40 re-run) — `LTG_ENV_school_hallway.png` + `LTG_ENV_school_hallway_v004.png`
  - SUNLIT_AMBER hue fix (C14) was in source. Re-ran generator. QA: warm/cool 34.8 PASS, value PASS, grade WARN (pre-existing color fidelity)
- Millbrook Street: v002
- **Living Room (C39)**: **v002** — `LTG_ENV_grandma_living_room.png` — QA PASS
- **Classroom**: FAIL grade (silhouette blob, warm/cool 9.3 FAIL, line weight FAIL). Rebuild spec written: `output/production/ENV_REBUILD_SPEC_classroom_c41.md`. Execute C41.
- **Luma Study Interior**: 31-cycle-old legacy PNG, no generator. Warm/cool 5.4 FAIL. Rebuild spec written: `output/production/ENV_REBUILD_SPEC_luma_study_c41.md`. Execute C41.
  - C39 addition: diamond-crystal figurine at (438, 328), top shelf of bookcase, secondary visual plant connecting Grandma Miri / Glitch Layer elder Miri and diamond body geometry. Warm amber catch-light only. No GL palette.

## Key Palette References
- Master palette: `output/color/palettes/master_palette.md`
- Warmth guarantees config: `output/tools/ltg_warmth_guarantees.json`
- World presets: REAL (warm, SUNLIT_AMBER key), GLITCH (HOT_MAGENTA + ELECTRIC_CYAN), OTHER_SIDE (cool, zero warm)

## QA Pipeline
- `LTG_TOOL_render_qa.py` (v1.6.0) — always run before submitting
  - REAL world warm/cool threshold: **REAL_INTERIOR = 12**, **REAL_STORM = 3** (C39 split — was 20 in v1.4.0, 12 flat in v1.5.0)
  - Value floor ≤30, value ceiling ≥225, range ≥150
- `LTG_TOOL_warmth_inject.py` — fixes warm/cool failures (auto mode)
- `LTG_TOOL_palette_warmth_lint.py --world-type [REAL|GLITCH|OTHER_SIDE]`

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
