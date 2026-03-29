# Statement of Work — Cycle 9

**Date:** 2026-03-29
**Cycle:** 9

## Work Completed

### Alex Chen — Art Director
- **Couch scale fixed (P0, 4 cycles)**: span reduced 768px→422px (~22% of frame, 4.8:1 ratio with character)
- **Screen-glow/submerge draw order fixed**: submerge fade now executes before screen-glow; glow visible
- **Overlay draw order fixed**: `draw_lighting_overlay()` moved before character draw calls
- **HOODIE_AMBIENT finalized**: `#B06040` (70% HOODIE_SHADOW + 30% DUSTY_LAVENDER); replaces SHADOW_PLUM
- **False arm-span comment corrected**: 21% → 28%
- **Byte design document updated**: `byte.md` v3.0 reflects oval body; chamfered-box retired with historical note
- **MIRI-A locked**: formal message sent to Maya Santos
- **Output:** `style_frame_01_rendered.png` regenerated

### Maya Santos — Character Designer
- **Character turnarounds created**: `character_turnaround_generator.py` — 4-view strips (front/3/4/side/back) for Luma and Byte at 200px height. Note: Byte turnaround still uses chamfered-cube description — needs oval update.
- **MIRI-A locked**: MIRI-B removed from silhouette generator; `grandma_miri.md` updated
- **Byte action pose redesigned**: mid-flight leap with diagonal body, asymmetric arms, trailing kick leg, hover particles implying trajectory
- **Excitement background**: `(248,238,220)` → `(240,200,150)` — committed warm amber
- **Output:** All character PNGs regenerated; new `luma_turnaround.png`, `byte_turnaround.png`

### Jordan Reed — Background & Environment Artist
- **Glitch Layer 1920×1080 created**: `bg_glitch_layer_frame.py` — void black base, 3-tier platforms (near ELEC_CYAN / mid DATA_BLUE / far near-void), aurora with 4 sinusoidal bands, pixel flora, ghost platforms, pixel trails
- **Naming convention compliance**: LTG-format copies created for key output files; compliance report sent to Alex
- **Output:** `glitch_layer_frame.png` + `LTG_ENV_glitchlayer_frame_v001.png`, `LTG_ENV_lumashome_study_interior_v001.png`

### Sam Kowalski — Color & Style Artist
- **Section 7 — Skin Color System added**: resolves Fiona's discrepancy — `#C4A882` is canonical neutral, `#C8885A` is lamp-lit derivation; CHAR-C-01 (Cosmo `#D9C09A`) formally registered; warm/cool skin tables added
- **CHAR-L-08 finalized**: `#B06040` HOODIE_AMBIENT with full derivation; SHADOW_PLUM interim removed
- **CHAR-L-09/10 added**: shoe canvas (RW-01) and shoe sole (RW-12) formally documented
- **PROP-07 finalized**: `CABLE_NEUTRAL_PLUM #504064` with named constant
- **SHOE_CANVAS/SHOE_SOLE aliases removed**: direct references to WARM_CREAM/DEEP_COCOA
- **Naming convention compliance checklist created**: `naming_convention_compliance_checklist.md`
- **Output:** Updated `master_palette.md`, updated `style_frame_01_rendered.py`, color keys regenerated

### Lee Tanaka — Storyboard Artist
- **Dutch tilt fixed** (P14, P24): `apply_dutch_tilt()` helper rotates entire panel canvas ±12° — geometry now delivers the stated angle
- **P21 redesigned to 40-45° isometric** overhead: back wall visible, floor plane receding, characters foreshortened with visible faces (not anonymous top-of-head circles)
- **P24 hero framing fixed**: Luma in lower-left third, cropped at frame bottom (camera looks up), Glitchkin chaos fills right/upper
- **Expression library expanded**: 'settling' (P17), 'recognition' (P18), 'warmth' (P20) added to `draw_luma_face()`
- **Output:** All 12 chaos panels regenerated + contact sheet

## Key Improvements Over Cycle 8
- Couch scale finally correct — spatial logic of style frame restored
- Screen-glow on Byte now visible (draw order fixed)
- Full 26-panel cold open with geometrically correct Dutch tilts and isometric overhead
- Miri locked as MIRI-A — character design package complete for 4 characters
- Skin color system documented and reconciled
- Palette at ~85% production-ready (CHAR-L-08 finalized)
- Naming convention compliance checklist available for team
- Glitch Layer production background available for compositing
