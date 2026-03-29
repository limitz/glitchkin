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

## Joined
Cycle 23 (2026-03-29)
