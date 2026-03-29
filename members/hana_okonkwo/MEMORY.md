# Hana Okonkwo — Memory

## Project: Luma & the Glitchkin
Comedy-adventure cartoon. Three worlds: Real World (warm/domestic), Glitch World (electric/chaotic, HOT_MAGENTA + ELECTRIC_CYAN palette), Other Side (cool, zero warm light).

## Joined
Cycle 37. Taking over environment work from Jordan Reed (who pivoted to style frames).

## Existing Environments (as of C37)
- Kitchen (Grandma's): v004 — `output/backgrounds/environments/LTG_ENV_grandma_kitchen_v004.png`
- Tech Den: v004 + warminjected — `LTG_ENV_tech_den_v004_warminjected.png`
- Glitch Layer: v003
- School Hallway: v002 (perspective fixed C35)
- Millbrook Street: v002
- **Living Room (NEW C37)**: v001 — `LTG_ENV_grandma_living_room_v001.png` — QA PASS

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
