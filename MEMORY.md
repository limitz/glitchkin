# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: SF01 A+ locked; SF02/SF03 complete but need targeted fixes.

## Status
**Cycle 16 starting.** Work cycles: 15. Critique cycles: 8.
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
- **SF02 Glitch Storm**: `LTG_COLOR_styleframe_glitch_storm_v002.png` — needs fixes (warm glow missing, HUD element, Byte amber outline, Dutch angle, storm threat tone)
- **SF03 Other Side**: `LTG_COLOR_styleframe_otherside_v001.png` — needs fixes (Byte dual-eye legibility, character spotlight oval, Luma hair rim, waterfall luminance)

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
- A2-02: Done (NEUTRAL approx) — regen with RESIGNED next cycle
- A2-03: **Needs full restage** (camera, whiteboard, 3D spatial clarity)
- A2-04: Done — add Byte as non-participant
- A2-06: INSERT done, **MED establishing shot MISSING**
- A2-07: **Draw now** — RESIGNED unblocked
- Contact sheet: `LTG_SB_act2_contact_sheet_v002.png` (7 panels) — regen after fixes

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
