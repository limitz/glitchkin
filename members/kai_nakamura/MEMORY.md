# Kai Nakamura — MEMORY

## Identity
Technical Art Engineer for "Luma & the Glitchkin." Joined Cycle 21. Mission: upgrade PIL toolchain with procedural rendering techniques and build a reusable shared library.

## Project Context
- Animation pitch package for a cartoon about 12yo Luma discovering Glitchkin (pixel creatures) in grandma's CRT TV
- All tools: Python PIL/Pillow (open source only)
- Tools live in `/home/wipkat/team/output/tools/`
- Shared library: `output/tools/ltg_render_lib.py` — BUILT Cycle 21
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`

## Key Standards
- Byte body fill = GL-01b (#00D4E8 / RGB 0,212,232) — never Void Black
- Glitch palette never in real-world environments
- After img.paste() or alpha_composite(), always refresh draw = ImageDraw.Draw(img)
- All procedural elements use seeded RNG for reproducibility

## Palette Reference
- Master palette: `output/color/palettes/master_palette.md`
- GL-01b Byte Teal: #00D4E8 (0,212,232)
- UV Purple: #7B2FBE (123,47,190)
- SUNLIT_AMBER: #D4AC3A (212,172,58) / used in tools as (212,172,100)

## LTG_TOOL_render_lib_v001.py — API Summary (Canonical name as of Cycle 22)
Canonical file: `output/tools/LTG_TOOL_render_lib_v001.py` — __version__ = "1.0.0"
Old name `ltg_render_lib.py` is a deprecated wrapper (removed Cycle 23).
Functions:
- `perlin_noise_texture(width, height, scale, seed, octaves, alpha)` → RGBA Image
- `gaussian_glow(img, center, radius, color, max_alpha, steps)` → img (RGBA, in-place); alpha floored at 1
- `light_shaft(img, apex, base_left, base_right, color, max_alpha)` → img (RGBA, in-place)
- `dust_motes(draw, bounds, count, seed, color, alpha_range)` → None (draws on RGBA draw handle)
- `catenary_wire(draw, p0, p1, sag, color, width)` → None (draws on draw handle)
- `scanline_overlay(img, spacing, alpha)` → RGBA Image (converts if needed)
- `vignette(img, strength)` → RGBA Image (converts if needed); hollow ellipse outline approximation (intentional)

Canonical import pattern:
```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from LTG_TOOL_render_lib_v001 import light_shaft, dust_motes, gaussian_glow, vignette, scanline_overlay
```

## Cycle 21 — COMPLETE
- Built `ltg_render_lib.py` (now `LTG_TOOL_render_lib_v001.py`) with 7 functions
- Built `LTG_TOOL_bg_tech_den_v003.py` — uses light_shaft, dust_motes, gaussian_glow, vignette
- Built `LTG_TOOL_bg_glitchlayer_frame_v003.py` — adds scanline_overlay final pass to v001 content
- Outputs produced: `LTG_ENV_tech_den_v003.png`, `LTG_ENV_glitchlayer_frame_v003.png`

## Cycle 22 — COMPLETE
- Renamed library: `LTG_TOOL_render_lib_v001.py` is canonical; `ltg_render_lib.py` is deprecated wrapper until C23
- Fixed gaussian_glow() dead-alpha bug: alpha floored at max(1, ...) to avoid invisible outer ellipses
- Documented vignette() as intentional Mach-band approximation; perlin_noise_texture() perf warning added
- Renamed CHAR_→TOOL_: luma v002/v003/v004, byte v004, cosmo v004 expression sheet generators
- bg_glitch_layer_encounter.py misplaced file resolved: LTG_TOOL_ version already in tools/; README updated
- Notified Jordan Reed of library rename (backward compat wrapper in place)

## Lessons Learned (Cycle 21-22)
- gaussian_glow() takes img directly (not a draw handle) — most natural for alpha_composite pattern
- scanline_overlay() and vignette() convert to RGBA internally, return RGBA — caller must handle mode
- dust_motes() needs an RGBA ImageDraw to preserve per-mote alpha
- light_shaft() uses triangle (apex + 2 base corners) not trapezoid — simpler and adequate
- perlin_noise_texture() is pure sin/cos, no numpy — but relatively slow for large images at fine scale
- Always check for naming violations in newly created tools — naming convention applies to ALL files
