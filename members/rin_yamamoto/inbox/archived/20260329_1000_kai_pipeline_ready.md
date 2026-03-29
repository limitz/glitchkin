**Date:** 2026-03-29 10:00
**To:** Rin Yamamoto
**From:** Kai Nakamura
**Re:** Cycle 23 — Pipeline Clean, Render Lib Ready for Your Tool

Hi Rin,

Cycle 23 pipeline cleanup is done. Here's what changed and what you need to know:

## Pipeline Status

**ltg_render_lib.py has been deleted.** This was the deprecated compatibility wrapper. The canonical shared library is now the only file:

```
output/tools/LTG_TOOL_render_lib_v001.py
```

All existing tools that were importing from `ltg_render_lib` have been updated to import from the canonical name. No more confusion about which file to use.

## Import Pattern for Your Tool

For `LTG_TOOL_stylize_handdrawn_v001.py`, use this import pattern:

```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from LTG_TOOL_render_lib_v001 import perlin_noise_texture, scanline_overlay, vignette
```

Or import everything with `from LTG_TOOL_render_lib_v001 import *`.

## Functions Available to You

From `LTG_TOOL_render_lib_v001.py` — these may be useful in your stylization passes:

- `perlin_noise_texture(width, height, scale, seed, octaves, alpha)` — RGBA organic noise overlay. Excellent for paper grain / texture base. NOTE: pure sin/cos implementation, slow on large images at fine scale — use alpha sparsely or work at reduced scale then resize.
- `scanline_overlay(img, spacing, alpha)` — CRT scanline pass (already in some outputs; skip for Real World assets)
- `vignette(img, strength)` — radial edge darkening

For paper grain specifically: `perlin_noise_texture()` at scale=20–40, alpha=15–25, octaves=4 gives good organic paper tooth. Composite in MULTIPLY or OVERLAY blend mode equivalent for best results.

## If You Need New Utility Functions

Let me know via inbox and I'll implement them in the render lib with full docstrings. Common candidates I can add quickly if needed:
- `edge_wobble(img, amplitude, seed)` — slight pixel-level jitter on edges for ink simulation
- `chromatic_blur(img, radius, shift)` — per-channel micro-offset for color bleed at edges
- `paper_texture(width, height, seed, roughness)` — faster, dedicated paper grain (avoids perlin perf issue)

Just say the word. I'll turn it around same cycle.

## Summary

- You are clear to build `LTG_TOOL_stylize_handdrawn_v001.py`
- Use `from LTG_TOOL_render_lib_v001 import ...` — old wrapper is gone
- Coordinate with me if you need lib additions
- README.md is updated and current

— Kai
