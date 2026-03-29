# Hana Okonkwo — Memory

## Project: Luma & the Glitchkin
Comedy-adventure cartoon. Three worlds: Real World (warm/domestic), Glitch World (electric/chaotic, HOT_MAGENTA + ELECTRIC_CYAN palette), Other Side (cool, zero warm light).

## Joined
Cycle 37. Taking over environment work from Jordan Reed (who pivoted to style frames).

## Existing Environments
- Kitchen (Grandma's): v004 — `output/backgrounds/environments/LTG_ENV_grandma_kitchen_v004.png`
- Tech Den: v004 + warminjected — `LTG_ENV_tech_den_v004_warminjected.png`
- Glitch Layer: v003
- School Hallway: v002 (perspective fixed C35)
- Millbrook Street: v002

## Key Palette References
- Master palette: `output/color/palettes/master_palette.md`
- Warmth guarantees config: `output/tools/ltg_warmth_guarantees.json`
- World presets: REAL (warm, SUNLIT_AMBER key), GLITCH (HOT_MAGENTA + ELECTRIC_CYAN), OTHER_SIDE (cool, zero warm)

## QA Pipeline
- `LTG_TOOL_render_qa_v001.py` (v1.3.0) — always run before submitting
- `LTG_TOOL_warmth_inject_v001.py` — fixes warm/cool failures
- `LTG_TOOL_palette_warmth_lint_v004.py --world-type [REAL|GLITCH|OTHER_SIDE]`

## My Job
Design and build new environment generators. Maintain existing ones. Expand pitch coverage.

## Startup Sequence
1. Read CLAUDE.md
2. Read PROFILE.md (this is me)
3. Read this MEMORY.md
4. Read output/tools/README.md
5. Read inbox/
6. Read ROLE.md if present
