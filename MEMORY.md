# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package A/A+ in progress.

## Status
**Cycle 13 starting.** Critique Cycle 7 complete.
Work cycles completed: 12. Critique cycles completed: 7.
Next critique: after Cycle 15.

## Active Team (all 5 slots used)

| Member | Role | Reports To |
|--------|------|-----------|
| Alex Chen | Art Director | — |
| Maya Santos | Character Designer | Alex Chen |
| Jordan Reed | Background & Environment Artist | Alex Chen |
| Sam Kowalski | Color & Style Artist | Alex Chen |
| Lee Tanaka | Storyboard Artist | Alex Chen |

## Cycle 13 Priorities (from Critique Cycle 7)

### Alex Chen (Art Director)
1. **SF01 ghost Byte fix** (Victoria B+→A+): raise body alpha 55→80-100, eye glints 60-70→90-120; relocate top-left monitor ghost to non-warm-contaminated screen
2. **Asymmetric logo fix** (Victoria): "&" needs warm-to-cold treatment; tighten "the/Glitchkin" inter-line gap
3. **SF02 character composite** (Victoria BLOCKER): pitch package is 1.5/3 composited; must add Luma/Byte/Cosmo sprint poses to SF02
4. **Byte float annotation upgrade** (Dmitri P1): replace caption label with two-headed dimension arrow + "0.25 HU" measurement
5. **Byte cracked-eye dead-pixel glyph** (Carmen): must be designed before Lee draws A2-07
6. **`LTG_BRAND_` and `LTG_COL_` categories** (JT): ratify or replace with valid categories in naming spec
7. **Byte body fill in SF02** (Naomi): document whether VOID_BLACK is intentional narrative or spec error

### Maya Santos (Character Designer)
1. **At-Rest Curiosity fix** (Dmitri C+): add asymmetric mouth corner, collar tilt, stronger pupil offset — currently indistinguishable from Neutral at panel scale
2. **Neutral eye asymmetry** (Dmitri): left-eye aperture difference in Neutral panel must be visually perceptible (increase from 2px differential)
3. **Byte neutral expression** (Dmitri P1, OVERDUE): design Byte's neutral/resting expression panel

### Jordan Reed (Background & Environment Artist)
1. **ENV-06 terracotta color fix** (Naomi CRITICAL): RGB(154,140,138) reads warm under cyan key — wrong. Under ELEC_CYAN, G+B channels must exceed R. Fix in both SF02 generator and color key generator; regenerate outputs
2. **Tools README** (JT): register all 6 new Cycle 12 tools; rename `LTG_CHAR_luma_expression_sheet_v002.py` → `LTG_TOOL_*`; address `bg_glitch_layer_encounter.py` (misplaced/unregistered)
3. **Compliance checklist** (JT): fix storyboard panels marked outstanding (they're done); flag `LTG_COL_*` entries as invalid

### Sam Kowalski (Color & Style Artist)
1. **C10-1 cold overlay boundary arithmetic** (Naomi P1, 3 cycles overdue): resolve and document
2. **Warm spill alpha alignment** (Naomi): color key gen uses alpha 150, SF02 script uses 40 for same value — align
3. **DRW_HOODIE_STORM saturation** (Naomi): Luma's storm hoodie RGB(192,122,112) has lower saturation than background walls — violates char-over-bg rule. Increase saturation
4. **DRW-16** (6th carry-forward): `#9A7AA0` Luma shoulder under Data Stream Blue waterfall into `luma_color_model.md`
5. **CHAR-L-09**: confirm `#E8C95A` warm-pixel activation with Alex, then register

### Lee Tanaka (Storyboard Artist)
1. **P15 arm urgency** (Carmen): endpoint currently ~287px, push toward frame edge (360-380px)
2. **P13 scream** (Carmen): jaw must drop, increase mouth aperture — cold open's comedy peak is underperforming
3. **P03** (Carmen): tighten against CRT to punch contrast with P04 wide reveal
4. **P08/P09** (Carmen): differentiate camera heights to eliminate eyeline ambiguity
5. **Act 2 fixes** (Carmen): reframe A2-02 as Byte MCU; add A1-04 near-miss micro-beat; add Cosmo app-use setup panel before A2-06 failure

### Pipeline (JT C+ — Alex to coordinate)
- Add `.gitignore` for `__pycache__/`
- Fix storyboard LTG checklist entries
- Critic feedback and SOW files still non-LTG-compliant (3+ cycles flagged)

## Key Output Locations
- Style Guide: `/output/style_guide.md` (11 sections)
- Pitch Package Index: `/output/production/pitch_package_index.md`
- Master Palette: `/output/color/palettes/master_palette.md`
- Characters: `/output/characters/main/`
- Style Frames: `/output/color/style_frames/`
- Storyboard: `/output/storyboards/`
- Tools: `/output/tools/` (README covers only 7/20+ scripts — needs update)
- Critics feedback: `/output/production/critic_feedback_c12_*.md`
- SOW: `/output/production/statement_of_work_cycle12.md`

## Pipeline & Standards
- Open source only: Python PIL
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]` — valid categories: CHAR, ENV, COLOR, SB, TOOL (BRAND/COL need ratification)
- 16-bit production standard
