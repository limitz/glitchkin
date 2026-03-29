# Statement of Work — Cycle 8

**Date:** 2026-03-29
**Cycle:** 8

## Work Completed

### Alex Chen — Art Director
Applied all 8 Victoria/Naomi fixes to `style_frame_01_rendered.py`:
- Lighting overlay alpha raised: warm 28→70, cold 22→60 (now perceptible)
- Charged gap added at emotional midpoint — soft cyan glow + 18-pixel scatter between Byte's tendril and Luma's hand
- Tendril Bezier CP1 corrected — tendril now arcs toward Luma from the start
- Byte screen-glow added — upward ELEC_CYAN fill on Byte's lower quarter from CRT below
- Amber outline width fixed: 4→3px default, 5→3px call site (GL-07 compliant)
- Hoodie underside replaced warm tuple with SHADOW_PLUM (correct lavender ambient)
- Lamp floor pool added — warm glow ellipse on floor below lamp
- Shoe colors corrected: cream canvas main + deep cocoa sole per character spec
- **Output:** `/home/wipkat/team/output/color/style_frames/style_frame_01_rendered.png` regenerated

### Maya Santos — Character Designer
- **Miri complete redesign** (Priority 0): Two variants — MIRI-A (bun+chopsticks+inverted-flare cardigan+soldering iron) and MIRI-B (rounded puff curls+tech apron with circuit-pocket negative space). Both pass squint test.
- **Byte shape standardized to oval** — expression sheet updated to match style frame; chamfered-box polygon retired; all limb/eye geometry updated
- **GRUMPY posture fixed**: `body_tilt=-8`, `arm_l_dy=-6`, `arm_r_dy=-10`, `arm_x_scale=1.1` — confrontational forward lean with raised asymmetric arms
- **WORRIED/DETERMINED brow differential**: 8px gap, corrugator kink 8px (legible at pitch distance)
- **Collar rotation**: rebuilt with 2D rotation matrix — physically tilts per expression (8°/2°/-5°)
- **Output:** All 4 character PNGs regenerated

### Jordan Reed — Background & Environment Artist
Applied all 6 Takeshi fixes to `bg_house_interior_frame01.py`:
- Wall glow RGBA composited; atmospheric gradient re-applied on top — both effects survive
- Worn path replaced with bell-curve scanline texture + scuff marks
- Ceiling gradient inverted — warm far edge darkest, monitor wall side lightest
- Couch repositioned 9%-43% → 18%-52% (character now faces monitors correctly)
- Atmospheric haze extended 8% → 20% of wall height
- Standing floor lamp + side table added to warm zone
- **Output:** `frame01_house_interior.png` regenerated (66K, 1920×1080)

### Sam Kowalski — Color & Style Artist
- Added Section 6 to `master_palette.md` — "Environment / Props" (PROP-01 through PROP-07)
- Neutral grey `(100,100,100)` deprecated; replaced with desaturated Shadow Plum mid
- Named constants `CABLE_BRONZE`, `CABLE_DATA_CYAN`, `CABLE_MAG_PURP` added
- CHAR-L-08 placeholder added for hoodie underside
- All remaining inline tuples documented with comments
- Color keys regenerated — no regressions
- **Output:** Updated `master_palette.md`, updated `style_frame_01_rendered.py`

### Lee Tanaka — Storyboard Artist
- Created `panel_chaos_generator.py` — 12 panels + P22a bridge (P14-P24)
- Full cold open: 26 panels — QUIET → CURIOUS → BREACH → CHAOS → PEAK CHAOS
- Techniques: multi-exposure ghost, visible pulse/glitch FX, two-point perspective, additive glow, 22% OTS silhouettes
- Contact sheet regenerated: 5×6 grid, all 26 panels
- **Output:** 12 new panel PNGs + updated contact sheet

## Key Improvements Over Cycle 7
- Style frame lighting now structurally perceptible (warm/cold zones, lamp pool, Byte self-illumination, charged gap)
- Miri is finally a designed character with two viable options
- Byte shape consistent across all tools (oval)
- Cold open storyboard complete: 26 panels covering full arc
- Palette fully traceable — all props documented, no undocumented inline tuples
