# Rin Yamamoto — MEMORY

## Role
Visual Stylization Artist on "Luma & the Glitchkin." Post-processing specialist: applies hand-drawn, organic stylization passes to digitally generated PNG outputs.

## Project Context
- Comedy-adventure cartoon pitch package. All assets generated via Python PIL.
- Style: CRT/pixel aesthetic (Glitch world) + warm hand-drawn domestic (real world).
- Output dir: `/home/wipkat/team/output/`
- Tools dir: `output/tools/`
- Render lib: `output/tools/LTG_TOOL_render_lib_v001.py` (canonical)

## Pipeline
- Naming: `LTG_TOOL_stylize_[descriptor]_v[###].py` for stylization scripts
- Output PNGs: `LTG_[CATEGORY]_[descriptor]_[variant]_v[###].png`
- After `img.paste()`, always refresh: `draw = ImageDraw.Draw(img)`
- PIL only — no NumPy required but allowed for noise fields
- **IMAGE SIZE RULE: prefer smallest resolution appropriate for the task. Hard limit ≤ 1280px in both dimensions.** Use `img.thumbnail((1280, 1280), Image.LANCZOS)` before saving. Preserve aspect ratio. Only use large sizes when detail inspection requires it. Detail crops also ≤ 1280×1280px.

## Current Tool
`output/tools/LTG_TOOL_stylize_handdrawn_v002.py` — CURRENT (v001 RETIRED)
- `stylize(input_path, output_path, mode, intensity=1.0, seed=42)`
- Modes: `realworld` | `glitch` | `mixed`
- Run from /home/wipkat/team: `python output/tools/LTG_TOOL_stylize_handdrawn_v002.py input.png output.png --mode X`
- Never overwrite originals — always use `_styled_v002` suffix for new outputs
- All canonical colors protected via PROTECTED_HUES (6 colors, ±12 PIL hue tolerance)
- verify_canonical_colors() runs post-process — batch-safe warnings, no abort

## Cycle 25 Fixes in v002
1. **Full hue protection** — ALL 6 canonical colors protected on every modifying pass (not just CORRUPT_AMBER)
2. **Chalk pass exclusions** — skips cyan-family (H 100–160) and light-source pixels (V>216, S>100)
3. **Warm bleed gate** — _pass_color_bleed() skips cyan-family source pixels (no amber bleed into cyan zones)
4. **Mixed mode cross-dissolve** — per-pixel weighted average in transition zone (no alpha_composite ghosting)

## Asset → Mode Mapping
- SF02 Glitch Storm = mixed (1.0)
- SF03 Other Side = glitch (1.0) — Glitch Layer, no paper grain
- SF01 Discovery = LOCKED (v001 output, Alex approved). DO NOT reprocess.
- Real world envs (Kitchen, Tech Den etc.) = realworld

## Cycle 25 Outputs
- `LTG_COLOR_styleframe_glitch_storm_v005_styled_v002.png` (mixed, 1.0)
- `LTG_COLOR_styleframe_otherside_v003_styled_v002.png` (glitch, 1.0)
- Preset doc updated: `output/production/stylization_preset_handdrawn_v001.md`

## Previous Outputs (still valid)
- `LTG_COLOR_styleframe_discovery_v003_styled.png` — LOCKED (Alex approved C24)
- `LTG_ENV_grandma_kitchen_v003_styled.png` (realworld, 1.0)
- `LTG_ENV_tech_den_v004_styled.png` (realworld, 0.8)
- `LTG_CHAR_lineup_v003_styled.png` (realworld, 0.7)

## Coordination
- Kai Nakamura: building LTG_TOOL_color_verify_v001.py — TODO refactor verify_canonical_colors() import when ready
- Reports to Alex Chen

## Verify Warning Note (Cycle 25)
SF02/SF03 verify runs report hue drift warnings on cyan/purple pixels. This is expected: RGB channel separation in glitch mode creates edge-level hue deviation that the sampler picks up. The actual canonical color areas are protected from desaturation/bleed — the drift is from the geometric channel-offset pass, which is intentional glitch aesthetic. Worth noting for critics.

## Joined
Cycle 23 (2026-03-29)
