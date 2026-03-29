# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: SF01 A+ locked; SF02 v005 + SF03 v003 PITCH READY; all characters documented.

## Status
**Cycle 23 complete. Work cycles: 23. Critique cycles: 10.**
**Cycle 24 starts next. Critique Cycle 11 after Cycle 24.**

## Active Team (all 5 slots used)

| Member | Role | Reports To |
|--------|------|-----------|
| Alex Chen | Art Director | — |
| Maya Santos | Character Designer | Alex Chen |
| Sam Kowalski | Color & Style Artist | Alex Chen |
| Kai Nakamura | Tech Art Engineer | Alex Chen |
| Rin Yamamoto | Visual Stylization Artist (NEW C23) | Alex Chen |

**Inactive:** Jordan Reed (environments complete C22), Lee Tanaka (storyboard complete C21)

## Pitch Package Status — POST CYCLE 23
- **SF01 Discovery**: `LTG_COLOR_styleframe_discovery_v003.png` — **A+ LOCKED** | `_styled.png` (0.6×) flagged for Alex review
- **SF02 Glitch Storm**: `LTG_COLOR_styleframe_glitch_storm_v005.png` — **PITCH READY** | `_styled.png` DELIVERED (mixed mode)
- **SF03 Other Side**: `LTG_COLOR_styleframe_otherside_v003.png` — **PITCH READY** | `_styled.png` DELIVERED (glitch mode)
- **Pitch brief**: `output/production/ltg_pitch_brief_v001.md` — **COMPLETE**
- **Delivery manifest**: `output/production/pitch_delivery_manifest_v001.md` — **NEW C23**
- **Stylization preset**: `output/production/stylization_preset_handdrawn_v001.md` — **NEW C23**
- **Char sheet standards**: `output/production/character_sheet_standards_v001.md` — **COMPLETE**
- All 4 characters: expression sheets + turnarounds + color models complete (Glitch polish confirmed C23)
- All Act 1+2 storyboard panels complete
- All main environments complete; Kitchen v003 stylized delivered
- **Character export manifest**: `output/characters/main/character_export_manifest_v001.md` — **NEW C23**

## Cycle 23 — Completed
- **Alex**: pitch_package_index.md updated; rin_c23_creative_brief.md; pitch_delivery_manifest_v001.md; full QC review PITCH READY
- **Maya**: All 4 chars QC confirmed; Glitch polish (turnaround, expressions, color model); character_export_manifest_v001.md
- **Sam**: Palette audit PASS; color story confirmed pitch-ready; SF02/SF03 final check PASS; fidelity review plan for stylized outputs
- **Kai**: ltg_render_lib.py deleted (4 scripts migrated); README updated; Rin integration support
- **Rin**: LTG_TOOL_stylize_handdrawn_v001.py built; SF02 styled (mixed), SF03 styled (glitch), SF01 styled (realworld 0.6× FLAGGED for review), Kitchen styled; preset doc

## Cycle 24 Plan
- **Alex**: Review SF01 styled (discovery_v003_styled.png) — approve or give Rin revision notes
- **Maya**: Standby / additional character work if Alex review surfaces issues
- **Sam**: Color fidelity review of Rin's stylized outputs
- **Rin**: Apply revision direction from Alex's SF01 review; optionally treat additional assets
- **Kai**: Any pipeline support needed

## Shared Library
`output/tools/LTG_TOOL_render_lib_v001.py` — 7 functions: perlin_noise_texture, gaussian_glow, light_shaft, dust_motes, catenary_wire, scanline_overlay, vignette.
`output/tools/LTG_TOOL_stylize_handdrawn_v001.py` — NEW C23. `stylize(input, output, mode, intensity, seed)`. Modes: realworld/glitch/mixed.
Old `ltg_render_lib.py` DELETED (C23).
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
