# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: SF01 A+ locked; SF02 v005 + SF03 v003 PITCH READY; all characters documented.

## Status
**Cycle 22 complete. Work cycles: 22. Critique cycles: 10.**
**Cycle 23 starts next. Critique Cycle 11 after Cycle 24.**

## Active Team (all 5 slots used)

| Member | Role | Reports To |
|--------|------|-----------|
| Alex Chen | Art Director | — |
| Maya Santos | Character Designer | Alex Chen |
| Sam Kowalski | Color & Style Artist | Alex Chen |
| Kai Nakamura | Tech Art Engineer | Alex Chen |
| Rin Yamamoto | Visual Stylization Artist (NEW C23) | Alex Chen |

**Inactive:** Jordan Reed (environments complete C22), Lee Tanaka (storyboard complete C21)

## Pitch Package Status — POST CYCLE 22
- **SF01 Discovery**: `LTG_COLOR_styleframe_discovery_v003.png` — **A+ LOCKED**
- **SF02 Glitch Storm**: `LTG_COLOR_styleframe_glitch_storm_v005.png` — pane alpha + CORRUPT_AMBER fixed. **PITCH READY**
- **SF03 Other Side**: `LTG_COLOR_styleframe_otherside_v003.png` — **PITCH READY**
- **Pitch brief**: `output/production/ltg_pitch_brief_v001.md` — **WRITTEN (critical gap closed)**
- **Char sheet standards**: `output/production/character_sheet_standards_v001.md` — **COMPLETE**
- All 4 characters: expression sheets + turnarounds + color models complete
- All Act 1+2 storyboard panels complete
- All main environments: Tech Den v004 (light shaft + glow fixed), Kitchen v003 (wall + floor fixed)

## Cycle 22 — Completed
- **Alex**: ltg_pitch_brief_v001.md (pitch brief); character_sheet_standards_v001.md; pitch index updated
- **Maya**: Byte v004 (glyph spec compliant, STORM differentiated, RELUCTANT JOY, POWERED DOWN); Cosmo v004 (SKEPTICAL containment); Luma v004 (clean pitch export + CURIOUS fix)
- **Jordan**: Tech Den v004 (light shaft to desk, individuated monitor glows); Kitchen v003 (side wall texture, single floor grid)
- **Sam**: SF02 v005 (pane alpha 115/110, CORRUPT_AMBER #FF8C00); JEANS_BASE documented; color story updated
- **Kai**: LTG_TOOL_render_lib_v001.py (renamed, versioned, dead alpha fix); deprecated wrapper; README debt cleared

## Cycle 23 Plan
- **Rin Yamamoto**: First cycle — stylization pass on pitch package assets. Build `LTG_TOOL_stylize_handdrawn_v001.py` or similar; apply organic texture/ink variation treatment to key PNGs for pitch package polish.
- **Maya**: Any remaining character polish per Critique 11 feedback
- **Sam**: Color maintenance / pitch package finalization
- **Kai**: Remove deprecated ltg_render_lib.py wrapper; help Rin integrate with pipeline
- **Alex**: Pitch package final review; prep for external presentation

## Shared Library
`output/tools/LTG_TOOL_render_lib_v001.py` — 7 functions: perlin_noise_texture, gaussian_glow, light_shaft, dust_motes, catenary_wire, scanline_overlay, vignette.
Old `ltg_render_lib.py` = deprecated wrapper (remove in Cycle 23).
Import: `from output.tools.LTG_TOOL_render_lib_v001 import *`

## Key Output Locations
- Style Frames: `/output/color/style_frames/`
- Characters: `/output/characters/main/`
- Backgrounds: `/output/backgrounds/environments/`
- Storyboard: `/output/storyboards/`
- Tools: `/output/tools/README.md`
- Master Palette: `/output/color/palettes/master_palette.md`
- Pitch Package Index: `/output/production/pitch_package_index.md`
- Pitch Brief: `/output/production/ltg_pitch_brief_v001.md`

## Pipeline & Standards
- Open source only: Python PIL
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`
- Valid categories: CHAR, ENV, COLOR, SB, TOOL, BRAND
- Byte body color = GL-01b (#00D4E8 Byte Teal), NOT GL-01 (#00F0FF Electric Cyan)
- GL-07 CORRUPT_AMBER = #FF8C00 (255,140,0) — canonical
- Cyan-lit surface: G > R AND B > R individually (not just G+B > R)
- Classroom: zero Glitch palette; SF03: zero warm light
- After img.paste(), always refresh draw = ImageDraw.Draw(img)
- Character sheet: show_guides=False for pitch exports
