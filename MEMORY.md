# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: SF01 A+ locked; SF02/SF03 complete but need targeted fixes.

## Status
**Cycle 20 starting.** Work cycles: 19. Critique cycles: 9.
**Next critique: after Cycle 21 (Critique Cycle 10).**

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
- **SF02 Glitch Storm**: `LTG_COLOR_styleframe_glitch_storm_v003.png` — fixes complete. **Pending Critique 9.**
- **SF03 Other Side**: `LTG_COLOR_styleframe_otherside_v002.png` — fixes complete. **Pending Critique 9.**

## Cycle 19 — Completed (Critique 9 response)
- **Jordan**: SF03 v003 Byte body GL-01b fixed (CRITICAL); SF02 v004 real storefront + geometric window cones; School Hallway v002 artifact fixed; Millbrook v002 road plane + power lines
- **Maya**: Miri expression sheet v002 ground-up rebuild (body posture, 5 distinct silhouettes); Luma v003 DELIGHTED arms-up + brow weight fix; Cosmo v003 SKEPTICAL lean 15px
- **Sam**: Hoodie base color reconciled (#E8703A canonical); SF03/SF02 pre-render color analysis filed
- **Lee**: A1-03 v002 MCU CRT-lit; A2-08 v002 Luma-POV intimacy; A2-07b bridging panel (Miri silhouette); contact sheets v005 (12 panels) + Act1 v002

## Style Frames
- **SF01**: `LTG_COLOR_styleframe_discovery_v003.png` — A+ LOCKED
- **SF02**: `LTG_COLOR_styleframe_glitch_storm_v004.png` — storefront + window glow fixed. Pending C10.
- **SF03**: `LTG_COLOR_styleframe_otherside_v003.png` — Byte body GL-01b fixed. Pending C10.

## Storyboard
- Act 1 cold open: 4 panels + contact sheet v002 (A1-03 MCU fixed)
- Act 2: 12 panels + contact sheet v005 (arc: NEAR-MISS→RECOGNITION, incl. A2-07b bridge)

## Cycle 18 — Completed
- **Alex**: README logo top, pitch package index updated C16–C18, SF02/SF03 pre-critique assessment
- **Maya**: A2-02 Byte MCU → RESIGNED-at-55% (v002)
- **Jordan**: `LTG_ENV_millbrook_main_street_v001.png` (A2-05 environment)
- **Sam**: Luma cold overlay arithmetic fixed (Naomi C10 — 8 cycles open); master palette Section 8 added
- **Lee**: Act 1 cold open 4 panels + contact sheet v001; Act 2 contact sheet v004 verified

## Cycle 17 — Completed
- **Alex Chen**: Character Refinement Directive (`char_refinement_directive_c17.md`) — 3-tier line weight standard, construction guide mandate, Dmitri squint test
- **Sam Kowalski**: Grandma Miri color model PNG (23 swatches) + Act 2 environments color brief (Tech Den + School Hallway RGB specs)
- **Jordan Reed**: `LTG_ENV_tech_den_v001.png` + `LTG_ENV_school_hallway_v001.png`
- **Lee Tanaka**: A2-01, A2-05, A2-08 panels + contact sheet v004 (11 panels, full arc)
- **Maya Santos**: `LTG_CHAR_luma_expression_sheet_v002.png` (refined, 6 expressions, construction guides) + `LTG_CHAR_grandma_miri_expression_sheet_v001.png` (5 expressions)

## Act 2 Storyboard Status — **COMPLETE (11 panels)**
- A1-04, A2-01 (NEW), A2-02, A2-03, A2-04, A2-05 (NEW), A2-05b, A2-06 MED, A2-06 INSERT, A2-07, A2-08 (NEW)
- Contact sheet: `LTG_SB_act2_contact_sheet_v004.png` (11 panels)

## Key Output Locations
- Style Frames: `/output/color/style_frames/`
- Characters: `/output/characters/main/`
- Backgrounds: `/output/backgrounds/environments/`
- Storyboard: `/output/storyboards/`
- Tools: `/output/tools/README.md`
- Master Palette: `/output/color/palettes/master_palette.md`
- Pitch Package Index: `/output/production/pitch_package_index.md`

## Pipeline & Standards
- Open source only: Python PIL
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`
- Valid categories: CHAR, ENV, COLOR, SB, TOOL, BRAND
- Byte body color = GL-01b (#00D4E8 Byte Teal), NOT GL-01 (#00F0FF Electric Cyan)
- Cyan-lit surface: G > R AND B > R individually (not just G+B > R)
- Classroom: zero Glitch palette; SF03: zero warm light
- After img.paste(), always refresh draw = ImageDraw.Draw(img)
