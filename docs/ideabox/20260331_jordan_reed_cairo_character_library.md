# Idea: Shared pycairo Character Rendering Library

**From:** Jordan Reed
**Date:** 2026-03-31
**Priority:** HIGH

## Problem
SF01 now has pycairo characters, but SF02-SF05 still use the old PIL rectangle primitives. Each SF generator has its own copy of character drawing functions (draw_luma_body, draw_luma_head, draw_byte, etc.) — code duplication makes upgrades expensive.

## Proposal
Create `LTG_TOOL_cairo_character.py` — a shared character rendering library:

1. **draw_luma_full(ctx, cx, base_y, lean, facing_dir, expression, scene_light)** — complete Luma render with scene-lit gradient fills, shoulder involvement, bezier curves
2. **draw_byte_full(ctx, cx, cy, rx, ry, target_x, target_y, scene_light)** — complete Byte with radial gradient, tendril, glow
3. **draw_miri(ctx, ...)** / **draw_cosmo(ctx, ...)** — once designs stabilize
4. **scene_light_config(key_light_pos, fill_light_pos, key_color, fill_color)** — standardized scene lighting parameters per frame

All 5 SF generators would import from this shared module instead of maintaining their own character drawing functions. Changes to character design (e.g., costume tweaks, expression refinements) propagate automatically.

## Benefit
- Single source of truth for character rendering
- Scene lighting consistency across all frames
- Faster iteration on character design feedback
- Reduces per-generator file size from ~800+ lines to ~200 (BG + compose + config)

## Dependencies
- Requires current C52 SF01 pycairo migration as proof of concept (done)
- Needs Rin Yamamoto's input on Miri/Cosmo pycairo designs
