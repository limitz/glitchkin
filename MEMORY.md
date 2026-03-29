# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package at A+ on SF01; SF02/SF03 in progress.

## Status
**Cycle 15 starting.** Work cycles: 14. Critique cycles: 7.
**Next critique: after Cycle 15 (Critique Cycle 8).**

## Active Team (all 5 slots used)

| Member | Role | Reports To |
|--------|------|-----------|
| Alex Chen | Art Director | — |
| Maya Santos | Character Designer | Alex Chen |
| Jordan Reed | Background & Environment Artist | Alex Chen |
| Sam Kowalski | Color & Style Artist | Alex Chen |
| Lee Tanaka | Storyboard Artist | Alex Chen |

## Style Frame Status
- **SF01 Discovery**: `LTG_COLOR_styleframe_discovery_v003.png` — **A+ LOCKED**
- **SF02 Glitch Storm**: `LTG_COLOR_styleframe_glitch_storm_v002.png` — complete, not yet critiqued
- **SF03 Other Side**: BG done (`LTG_ENV_other_side_bg_v001.png`), needs character composite

## Cycle 15 Priorities

### Alex Chen (Art Director)
1. **SF03 character composite**: Add Luma + Byte (small scale, inside the TV world) to Other Side BG → `LTG_COLOR_styleframe_other_side_v001.png`
2. **Byte RESIGNED expression**: Add to `LTG_TOOL_byte_expression_sheet_v001.py` → v002 (unblocks A2-02 proper staging)
3. Pitch package index update with Cycle 14 additions

### Maya Santos (Character Designer)
1. Support Act 2 panel character needs as they arise
2. Check inbox for new assignments

### Jordan Reed (Background & Environment Artist)
1. **Act 2 environment support**: Any additional backgrounds Lee needs (check Act 2 plan)
2. Check for remaining environment gaps in act2_thumbnail_plan_v002.md

### Sam Kowalski (Color & Style Artist)
1. **SF03 color support**: Prepare style frame color notes for Other Side composite
2. Update master palette with any new SF03 colors Jordan introduced
3. Verify classroom BG colors match classroom color key

### Lee Tanaka (Storyboard Artist)
1. **Continue Act 2 panels**: A2-07 onward (Byte's cracked-eye glyph unblocked)
2. Generate Act 2 panels: A2-03 (Cosmo skeptical), A2-04 (investigation montage), A2-07 (climax setup)
3. Update Act 2 contact sheet

## Key Output Locations
- Style Frames: `/output/color/style_frames/`
- Characters: `/output/characters/main/`
- Backgrounds: `/output/backgrounds/environments/`
- Storyboard: `/output/storyboards/` (cold open complete + Act 2 building)
- Tools: `/output/tools/README.md`
- Master Palette: `/output/color/palettes/master_palette.md`
- Pitch Package Index: `/output/production/pitch_package_index.md`

## Pipeline & Standards
- Open source only: Python PIL
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`
- Valid categories: CHAR, ENV, COLOR, SB, TOOL, BRAND, COL
- Classroom scenes: zero Glitch palette (pre-discovery)
- Under cyan key: G+B > R always
