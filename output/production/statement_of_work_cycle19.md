# Statement of Work — Cycle 19
**Date:** 2026-03-29
**Work Cycles Completed:** 19
**Next Critique:** After Cycle 21 (Critique Cycle 10)

---

## Objectives This Cycle

Direct response to Critique Cycle 9 findings. Priority: critical spec violation fix (SF03 Byte body), persistent SF02 failures (storefront + window glow), character expression body posture, storyboard intimacy/bridging.

---

## Deliverables

### Alex Chen — Art Direction
- All 4 team assignment memos written and delivered to inboxes
- `output/production/production_bible.md` v4.0 — Section 12 added: SF03 Byte Void Black spec violation permanently on record

### Jordan Reed — Backgrounds & Style Frames
- `output/color/style_frames/LTG_COLOR_styleframe_otherside_v003.png` — **CRITICAL FIX**: Byte body GL-01b (#00D4E8), eye radius 15px min, Void Black slash removed from magenta eye
- `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v004.png` — Storefront = real damaged window (steel frame, 6 panes, 3 missing, crack rays, shard scatter); warm window glow = geometric trapezoid cones per window at alpha 90-110
- `output/backgrounds/environments/LTG_ENV_school_hallway_v002.png` — Black top-band artifact fixed, horizon lowered 18%, backpack/coat hooks/notice board added
- `output/backgrounds/environments/LTG_ENV_millbrook_main_street_v002.png` — Power lines with perspective convergence/catenary sag/weight hierarchy; road plane with asphalt + double-yellow center line + crosswalk

### Maya Santos — Character Design
- `output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v002.png` — Full ground-up rebuild: 5 expressions each with distinct body posture (A-frame/crossed+hip/chest-raise/arms-up/folded); replaces face-only v001
- `output/characters/main/LTG_CHAR_luma_expression_sheet_v003.png` — DELIGHTED arms raised (differentiates from SURPRISED); brow weight corrected 5px→2px across all 6 expressions
- `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v003.png` — SKEPTICAL lean formula fixed (0.4→2.5 multiplier): 2.4px→15px displacement, visible at thumbnail

### Sam Kowalski — Color & Style
- `output/characters/color_models/luma_color_model.md` — Hoodie base color reconciled: #E8722A→#E8703A (canonical), all overlay values recalculated; hoodie shadow #B85520→#B84A20 corrected
- `output/color/style_frames/sf03_v003_color_review.md` — Pre-render analysis: cyan eye 14.1:1 contrast (pass), magenta 5.5:1 (pass), minor BYTE_GLOW discrepancy noted
- `output/color/style_frames/sf02_v004_color_notes.md` — Window glow target: SUNLIT_AMBER (212,146,58) alpha 100

### Lee Tanaka — Storyboard
- `output/storyboards/panels/LTG_SB_act1_panel_a103_v002.png` — A1-03 rebuilt as MCU: Luma face 55% frame width, CRT amber-green asymmetric face lighting, legible 40×56px pixel shapes on screen
- `output/storyboards/act2/panels/LTG_SB_act2_panel_a208_v002.png` — A2-08 camera: low-angle → Luma-POV MCU eye-level (intimacy restored)
- `output/storyboards/act2/panels/LTG_SB_act2_panel_a207b_v001.png` — NEW bridging panel: hallway POV, Miri silhouette backlit in kitchen doorway, listening posture
- `output/storyboards/act2/LTG_SB_act2_contact_sheet_v005.png` — 12 panels, 4/4/4 layout, arc: NEAR-MISS→…→RESIGNED→BRIDGE→RECOGNITION
- `output/storyboards/LTG_SB_act1_coldopen_contact_sheet_v002.png` — Updated with A1-03 v002

---

## Critique C9 Items Closed This Cycle
- SF03 Byte body = Void Black — **FIXED** (GL-01b body now visible)
- SF02 storefront HUD element — **FIXED** (real damaged window geometry)
- SF02 warm window glow absent — **FIXED** (geometric per-window cones)
- School Hallway black artifact — **FIXED**
- Luma DELIGHTED/SURPRISED shared silhouette — **FIXED**
- Luma brow weight violation — **FIXED**
- Miri expression sheet face-only failure — **FIXED** (full body rebuild)
- Cosmo SKEPTICAL lean invisible — **FIXED**
- A1-03 compositionally passive — **FIXED** (MCU, CRT-lit)
- A2-08 wrong camera angle — **FIXED** (Luma POV)
- A2-07→A2-08 spatial jump — **FIXED** (bridging panel A2-07b)
- Hoodie base color discrepancy — **FIXED**

## Style Frame Status (End of Cycle 19)
- **SF01**: `LTG_COLOR_styleframe_discovery_v003.png` — A+ LOCKED
- **SF02**: `LTG_COLOR_styleframe_glitch_storm_v004.png` — storefront + window glow fixed, **pending Critique 10**
- **SF03**: `LTG_COLOR_styleframe_otherside_v003.png` — Byte body fixed, **pending Critique 10**
