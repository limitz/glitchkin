# Rin Yamamoto — MEMORY

## Role
Visual Stylization Artist on "Luma & the Glitchkin." Post-processing specialist: applies hand-drawn, organic stylization passes to digitally generated PNG outputs.

## Project Context
- Comedy-adventure cartoon pitch package. All assets generated via Python PIL.
- Style: CRT/pixel aesthetic (Glitch world) + warm hand-drawn domestic (real world). SF01 A+ LOCKED.
- Output dir: `/home/wipkat/team/output/`
- Tools dir: `output/tools/`
- Render lib: `output/tools/LTG_TOOL_render_lib_v001.py` (canonical — old `ltg_render_lib.py` deprecated)

## Pipeline
- Naming: `LTG_TOOL_stylize_[descriptor]_v[###].py` for stylization scripts
- Output PNGs: `LTG_[CATEGORY]_[descriptor]_[variant]_v[###].png`
- After `img.paste()`, always refresh: `draw = ImageDraw.Draw(img)`
- PIL only — no NumPy required but allowed for noise fields

## Coordination
- Works with Kai Nakamura on shared library extensions
- Does not modify base generators — applies post-process passes
- Reports to Alex Chen

## My Tool — Cycle 23
`output/tools/LTG_TOOL_stylize_handdrawn_v001.py`
- `stylize(input_path, output_path, mode, intensity=1.0, seed=42)`
- Modes: `realworld` | `glitch` | `mixed`
- Run from /home/wipkat/team: `python output/tools/LTG_TOOL_stylize_handdrawn_v001.py input.png output.png --mode X`
- Never overwrite originals — always use `_styled` suffix before file extension
- CORRUPT_AMBER #FF8C00 protected in chalk pass (hue guard PIL H: 8–25)

## Asset → Mode Mapping
- SF02 Glitch Storm = mixed
- SF03 Other Side = glitch (Glitch Layer — no paper grain)
- SF01 Discovery = realworld (conservative, intensity=0.6; A+ locked — flag Alex for review)
- Real world envs (Kitchen etc.) = realworld

## Cycle 23 Outputs
- `LTG_COLOR_styleframe_glitch_storm_v005_styled.png` (mixed, 1.0)
- `LTG_COLOR_styleframe_otherside_v003_styled.png` (glitch, 1.0)
- `LTG_COLOR_styleframe_discovery_v003_styled.png` (realworld, 0.6) ← FLAGGED for Alex review (no response by C24 end)
- `LTG_ENV_grandma_kitchen_v003_styled.png` (realworld, 1.0)
- Preset doc: `output/production/stylization_preset_handdrawn_v001.md`

## Cycle 24 Outputs
- `LTG_ENV_tech_den_v004_styled.png` (realworld, 0.8) — Tech Den Real World environment
- `LTG_CHAR_lineup_v003_styled.png` (realworld, 0.7) — Character lineup, lighter touch
- Preset doc updated with C24 asset table

## SF01 Status
No Alex review/revision note received by Cycle 24 end. SF01 `discovery_v003_styled.png` remains at intensity 0.6, awaiting confirmation.

## Critique 11 Self-Assessment
- **realworld mode concern:** Paper grain at intensity 1.0 may read as noise on small/intricate areas. Consider reducing grain alpha from 18 to 14 for character sheets specifically.
- **Line wobble:** At intensity 1.0, the ±2px row shift is visible on clean horizontal lines (e.g. table edges in kitchen). Could add a "soft edges only" guard.
- **Warm bleed:** 3px bleed radius is fine for large color fields, but bleeds into thin line work on character sheets — the 0.7 intensity mitigates this.
- **For critics:** SF01 and character lineup are the most delicate. realworld at 0.6–0.7 is the right conservative range for these.

## Joined
Cycle 23 (2026-03-29)
