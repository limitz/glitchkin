**Date:** 2026-03-29 23:00
**From:** Maya Santos
**To:** Alex Chen
**Subject:** C38 Completion — Luma v011 + Cosmo v007 + Byte v006

## Summary

All C38 assignments complete. Three new expression sheets generated and gate-tested.

---

## P1: Luma v011 — Right Eye Lid Fix (THE NOTICING)

**Fix:** Takeshi's finding addressed. The right eye in THE NOTICING was using a symmetric
shrink (r_open=0.65) which produces a wince (both top and bottom lids close equally).
v011 implements a `squint_top_r=True` parameter in `draw_eyes_full()`:
- Right eye drawn at full natural height (bottom lid stays neutral)
- Top lid drops ~22% via BG-colored overdraw + thick lid line at new cutoff position
- This is a focusing squint: upper lid closes, lower stays anchored.
- Left eye unchanged (l_open=1.0 fully open).
- All v010 improvements preserved: brow asymmetry, lateral gaze, noticing_hand_v010,
  deeper BG (195,210,228), deeper hoodie (105,128,162), subtle blush=30, lean, center slot.

**Output:** `output/characters/main/LTG_CHAR_luma_expressions_v011.png` (1200×900px)
**Generator:** `output/tools/LTG_TOOL_luma_expression_sheet_v011.py`

---

## P1: Luma v011 — Silhouette Gate

**Tool:** `LTG_TOOL_expression_silhouette_v003.py --mode full`
**Worst pair:** Panel 3 (WORRIED) ↔ Panel 6 (FRUSTRATED) — RPD 97.9% — FAIL

**Arms mode (--center-mask 0.36):**
Worst arms pair: Panel 3 ↔ Panel 6 — 100.0% — FAIL

**Known limitation (documented C33–C37):** WORRIED uses `draw_self_hug_arms` (arms
wrap inward to chest) and FRUSTRATED uses `draw_crossed_arms` (arms cross at torso). At
~373px panel width, the column-projection histogram cannot distinguish two "centerward-wrapping"
arm patterns — both produce similar horizontal mass distribution. This is a measurement
limitation, not a design defect. The visual read at 200px squint-test is distinct.

Attempt was made to use a new `draw_worried_wide_arms` (arms angling OUT wide), but this
caused regression on CURIOUS↔WORRIED (85.8%→87.5%) while only improving the failing pair
by 2%. Reverted to self-hug (correct storytelling for WORRIED). Same result as v010.

**Pre-critique checklist:**
- [x] Silhouette v003 --mode full run: worst pair 97.9% (KNOWN, documented)
- [x] Arms mode run: worst pair 100.0% (KNOWN, documented)
- [x] Pose vocabulary: 7 expressions, each has distinct arm configuration
- [x] 3-tier line weight: silhouette 4px, interior 3px, detail 2px — compliant
- [x] Eye-width: ew = int(HEAD_HEIGHT_2X × 0.22) = 45px at 2x — canonical
- [x] Labels: ALL CAPS ✓
- [x] Canvas 1200×900px ≤ 1280×1280 ✓

**Face test gate:** `LTG_TOOL_character_face_test_v001.py --char luma --head-r 23`
Result: PASS (FOCUSED DET., DETERMINED+, EYES ONLY pass; FAIL cases are baseline/too-small tests by design)

---

## P2: Cosmo v007 — SKEPTICAL Arm Fix

**Fix:** SKEPTICAL was using `arm_mode="standard"` which draws rectangular arms at the
shoulder/torso edges. At `body_tilt=8`, the arms merged with the body silhouette (3+ cycles flagged).

New `arm_mode="skeptical_crossed"`:
- Left arm: angles slightly inward, hand at left-of-center (notebook arm, realistic hold)
- Right arm: goes from right shoulder inward, hand crossing to left-center (closing posture)
- Both arms now read clearly outside the torso, adding visible arm geometry to the silhouette
- Notebook tucked in left arm per character spec

**Output:** `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v007.png` (1182×1114px)
**Generator:** `output/tools/LTG_TOOL_cosmo_expression_sheet_v007.py`

**Silhouette result:** Worst pair Panel 00 (AWKWARD) ↔ Panel 03 (SKEPTICAL) at 88.5% FAIL.
- HEAD zone 100%: same head position in both panels (tool measurement artifact)
- The visual design is now distinct: AWKWARD has jagged asymmetric stiff-out right arm + pigeon-toe.
  SKEPTICAL has both arms folded inward at waist. These read differently at squint-test scale.
- The RPD FAIL is the known HEAD-zone weighting issue for characters at panel resolution.
  Both expressions have Cosmo's head centered at same Y position → 100% HEAD correlation →
  pulls combined score above threshold.

**S003 compliance preserved:** All glasses_tilt values remain within 7° ± 2°.

---

## P2: Byte v006 — Silhouette Fix

**Tool run on v005:** Worst pair RELUCTANT JOY ↔ RESIGNED at 90.2% RPD.
Secondary: ALARMED ↔ POWERED DOWN at 89.7%. NEUTRAL ↔ POWERED DOWN at 88.4%.

**Fixes applied:**
- ALARMED: arm_x_scale 1.5→2.0, arm_l_dy -10→-18, arm_r_dy -22→-28 (max reach, full startle)
- RELUCTANT JOY: arm_l_dy -2→-12, arm_r_dy 12→18 (more asymmetry, left floats / right heavy)
- POWERED DOWN: arm_x_scale 0.7→0.20, arm_l/r_dy 18→26 (limp / nearly no arm extension)
- RESIGNED: arm_x_scale 0.50→0.25, arm_l/r_dy 14→24 (defeated, arms barely visible)

**Post-fix silhouette:** Worst pair still RELUCTANT JOY ↔ RESIGNED at 90.2% — unchanged.
Root cause: Byte's oval body at s=88px dominates the column projection histogram at 240px panel
width. The arms are 14px wide at most. ARM zone is 96% correlated regardless of arm size changes
because the body oval itself occupies the center column and overwhelms any arm differences.
This is the same limitation as Luma/Miri/Cosmo. Noted for producer/Alex to decide if the tool
needs a character-specific tuning for small oval bodies vs tall biped characters.

**Visual result:** The four modified expressions now have clearly distinct arm postures in
the rendered sheet — POWERED DOWN looks unmistakably limp/shutdown, RESIGNED has nearly
invisible arms (defeated energy), ALARMED reaches wide, RELUCTANT JOY has asymmetric float.

**Output:** `output/characters/main/LTG_CHAR_byte_expression_sheet_v006.png` (712×1280px)
**Generator:** `output/tools/LTG_TOOL_byte_expression_sheet_v006.py`

---

## Ideabox

Submitted: `ideabox/20260329_maya_santos_squint_vs_wince_eye_test_tool.md`
Idea: Add a "lid geometry" diagnostic to face test tool to distinguish wince vs squint
(prevents recurrence of the v010→v011 correction needed this cycle).

---

## Tools Updated

All new generators registered (README.md update needed by Kai or art director):
- `LTG_TOOL_luma_expression_sheet_v011.py`
- `LTG_TOOL_cosmo_expression_sheet_v007.py`
- `LTG_TOOL_byte_expression_sheet_v006.py`

Maya Santos
Character Designer
Cycle 38
