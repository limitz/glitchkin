# Hana Okonkwo — Memory

## Project: Luma & the Glitchkin
Comedy-adventure cartoon. Three worlds: Real World (warm/domestic), Glitch World (electric/chaotic, HOT_MAGENTA + ELECTRIC_CYAN palette), Other Side (cool, zero warm light).

## Joined
Cycle 37. Taking over environment work from Jordan Reed (who pivoted to style frames).

## Existing Environments (as of C39)
- Kitchen (Grandma's): v004 — `output/backgrounds/environments/LTG_ENV_grandma_kitchen_v004.png`
- Tech Den: v004 + warminjected — `LTG_ENV_tech_den_v004_warminjected.png`
- Glitch Layer: v003
- School Hallway: **v003** (C38 figure-ground pass) — `LTG_ENV_school_hallway_v003.png` — QA WARN (pre-existing color fidelity WARN, value range PASS)
- Millbrook Street: v002
- **Living Room (C39)**: **v002** — `LTG_ENV_grandma_living_room_v002.png` — QA PASS
  - C39 addition: diamond-crystal figurine at (438, 328), top shelf of bookcase, secondary visual plant connecting Grandma Miri / Glitch Layer elder Miri and diamond body geometry. Warm amber catch-light only. No GL palette.

## Key Palette References
- Master palette: `output/color/palettes/master_palette.md`
- Warmth guarantees config: `output/tools/ltg_warmth_guarantees.json`
- World presets: REAL (warm, SUNLIT_AMBER key), GLITCH (HOT_MAGENTA + ELECTRIC_CYAN), OTHER_SIDE (cool, zero warm)

## QA Pipeline
- `LTG_TOOL_render_qa_v001.py` (v1.4.0) — always run before submitting
  - REAL world warm/cool threshold = **20 PIL units** (NOT 12 — that was an old spec)
  - Value floor ≤30, value ceiling ≥225, range ≥150
- `LTG_TOOL_warmth_inject_v001.py` — fixes warm/cool failures (auto mode)
- `LTG_TOOL_palette_warmth_lint_v004.py --world-type [REAL|GLITCH|OTHER_SIDE]`

## Lessons Learned (C38)

### Figure-Ground Separation
- Always check costume colors against background fills before generating. Identical or near-identical values cause character merge.
- LOCKER_LAV in v002 was identical to Cosmo's cardigan RW-08 (168,155,191). Zero value separation = invisible character.
- Fix: push background fills LIGHTER than character costume values (≥20 value unit separation minimum).
- `LTG_TOOL_bg_school_hallway_v003.py`: LOCKER_LAV → (216,208,190), LOCKER_SAGE → (154,178,148)
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

## My Job
Design and build new environment generators. Maintain existing ones. Expand pitch coverage.

## Startup Sequence
1. Read CLAUDE.md
2. Read PROFILE.md
3. Read this MEMORY.md
4. Read output/tools/README.md
5. Read inbox/
6. Read ROLE.md if present
