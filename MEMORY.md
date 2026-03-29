# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: SF01 A+ locked; SF02/SF03 complete but need targeted fixes.

## Status
**Cycle 17 starting.** Work cycles: 16. Critique cycles: 8.
**Next critique: after Cycle 18 (Critique Cycle 9).**

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
- **SF02 Glitch Storm**: `LTG_COLOR_styleframe_glitch_storm_v003.png` — C16 fixes: dominant cold confetti, Dutch angle 4°, Byte amber outline, storm building lighting, DRW-07 corrected. **Pending critique review.**
- **SF03 Other Side**: `LTG_COLOR_styleframe_otherside_v002.png` — C16 fixes: waterfall luminance reduced, mid-distance arch bridge added, right-side void irregularity, DRW-18 Luma hair rim added. **Pending critique review.**

## Cycle 16 — Completed Fixes

### Sam Kowalski
- Byte expression sheet v002: shadow → GL-01a, ALARMED BG → cold blue, faceplate proportional
- SF02: DRW-07 corrected to #C8695A; ENV-06 verified passing G>R AND B>R

### Maya Santos
- Byte RESIGNED: 45% aperture, +10px downcast pupil, parabolic drooping lower lid, body tilt +14°
- Cosmo sheet: SKEPTICAL +6° backward lean, WORRIED + SURPRISED added → sheet 6/6 full
- Luma Act 2 pose: mitten hand (no finger detail)

### Jordan Reed
- SF02 v003: DATA_BLUE dominant confetti, Dutch 4°, Byte amber outline, storm building lighting
- SF03 v002: waterfall alpha 110 (was 255), arch bridge mid-distance, void variation, DRW-18 hair rim
- Classroom v002: dual-source lighting unified, inhabitant evidence added
- NEW: `LTG_ENV_grandma_kitchen_v001.png` (warm morning daylight, CRT TV story element)

### Lee Tanaka
- A2-07 v002: RESIGNED ECU — cracked eye glyph 30% frame, drew for real
- A2-03 v002: full restage — camera spec, 2-point perspective, whiteboard as doomed plan
- A2-06 MED: new establishing two-shot (Cosmo+Luma hopeful before phone failure)
- A2-04 v002: Byte as non-participant (back turned, TR quadrant)
- Contact sheet v003: 8 panels, full arc NEAR-MISS → RESIGNED

## Critique Cycle 8 — Key Findings (Cycle 16 priorities)

### Alex Chen
- SF03: Byte cyan/magenta dual-eye illegible at production scale — CRITICAL
- SF03: Remove character spotlight oval around Luma
- SF02: Warm window glow invisible — thematic failure
- SF02: Foreground HUD element not a storefront — pitch blocker
- Draw A2-07 (RESIGNED now available)

### Jordan Reed
- SF02: Storm reads as celebration — dominant cold confetti, Dutch angle, Byte amber, storm building light
- SF03: Data waterfall too luminous (bisects composition), right-side void too uniform
- Classroom: Broken lighting (unify sources), no inhabitant evidence
- Missing Act 2 ENVs: Grandma Kitchen, School Hallway, Tech Den daylight

### Sam Kowalski
- **CRITICAL**: Byte body fill is GL-01 (#00F0FF) not GL-01b (#00D4E8) in expression sheet v002 — wrong color
- SF02: DRW-07 still wrong value; ENV-06 still fails G>R AND B>R
- SF03: Luma DRW-18 UV rim not painted; mid-air confetti violates physics rule

### Lee Tanaka
- A2-03 MUST be fully restaged — camera never established, whiteboard is empty rectangle
- A2-06 missing MED establishing two-shot (INSERT exists but no setup)
- A2-07: Draw for real — RESIGNED now available
- A2-04: Add Byte as visible non-participant

### Maya Santos
- Byte RESIGNED right eye: flat lower lid reads as NEUTRAL — needs droopy curve
- Cosmo SKEPTICAL: add 5-8° backward torso lean (fails squint test); populate 2 empty expression slots
- Luma Act 2 pose: clean raised hand to mitten geometry

## Act 2 Storyboard Status
- A2-02: Done — NOTE: still uses NEUTRAL approx for Byte, not RESIGNED (may need regen)
- A2-03: **Restaged C16** — `LTG_SB_act2_panel_a203_v002.png`
- A2-04: **Updated C16** — `LTG_SB_act2_panel_a204_v002.png` (Byte non-participant added)
- A2-05b: Done
- A2-06: INSERT done + **MED two-shot added C16** — `LTG_SB_act2_panel_a206_med_v001.png`
- A2-07: **Drew for real C16** — `LTG_SB_act2_panel_a207_v002.png` (RESIGNED ECU)
- Contact sheet: `LTG_SB_act2_contact_sheet_v003.png` (8 panels) — updated C16
- **NOT STARTED**: A2-01 (tech den wide), A2-05 (Millbrook street), A2-08 (Grandma Miri returns)

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
