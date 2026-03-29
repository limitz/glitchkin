**Date:** 2026-03-29 09:00
**To:** Rin Yamamoto
**From:** Producer
**Re:** Cycle 23 — First Cycle: Stylization Tool Build + Pitch Package Pass

## Assignment

Welcome to your first cycle, Rin. Your mission is to build a reusable hand-drawn stylization tool and apply it to the pitch package's key PNG assets.

## Context
"Luma & the Glitchkin" is a comedy-adventure cartoon. The pitch package currently has clean, digitally-rendered style frames and character sheets. Your job is to give these assets the organic warmth of hand-drawn art — subtle ink variation, paper texture, slight color bleed — without obscuring the underlying designs.

**Existing pipeline:**
- Shared lib: `output/tools/LTG_TOOL_render_lib_v001.py` (7 functions: perlin_noise_texture, gaussian_glow, light_shaft, dust_motes, catenary_wire, scanline_overlay, vignette)
- Import: `from output.tools.LTG_TOOL_render_lib_v001 import *`
- All tools: Python PIL/NumPy only

**Read before starting:**
- `output/tools/README.md` — pipeline overview
- `output/color/palettes/master_palette.md` — canonical colors
- `output/production/character_sheet_standards_v001.md` — QC standards

## Deliverables

### 1. Build `LTG_TOOL_stylize_handdrawn_v001.py`
Save to `output/tools/`. The tool should:
- Accept any input PNG path and output a stylized version
- Implement at minimum:
  - Paper grain / organic texture overlay
  - Subtle ink line variation (edge wobble/jitter on outlines)
  - Slight color bleed at hard edges
  - Optional: mild halftone or watercolor bloom
- Export as `[original_name]_STYLIZED_v001.png` in same directory
- Be reusable: callable as a function (`stylize_handdrawn(input_path, output_path, intensity=1.0)`)
- Coordinate with Kai Nakamura if you need render lib additions

### 2. Apply Stylization to Pitch Package Assets
After Alex Chen delivers a creative brief (`output/production/rin_c23_creative_brief.md`), apply your tool to:
- **SF02 Glitch Storm**: `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v005.png`
- **SF03 Other Side**: `output/color/style_frames/LTG_COLOR_styleframe_otherside_v003.png`
- At least one character sheet (Alex will specify which)

**IMPORTANT:** Do not overwrite originals. Always save stylized versions as new files with `_STYLIZED_v001` suffix.

### 3. Stylization Preset Document
After applying the treatment, document your stylization parameters:
- Save to `output/production/stylization_preset_handdrawn_v001.md`
- Include: intensity settings, which passes were applied, which assets received treatment
- This allows the treatment to be reproduced or adjusted in future cycles

## Notes
- Check Alex's creative brief first before applying to assets — wait if it hasn't been written yet
- Coordinate with Kai on render lib compatibility
- After img.paste(), always refresh `draw = ImageDraw.Draw(img)`
- All naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`
- GL-07 CORRUPT_AMBER = #FF8C00 — do not desaturate this color in the stylization pass
