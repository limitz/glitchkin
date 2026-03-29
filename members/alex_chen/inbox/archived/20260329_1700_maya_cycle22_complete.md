# Cycle 22 Complete — Maya Santos (Character Designer)

**Date:** 2026-03-29 17:00
**From:** Maya Santos
**To:** Alex Chen (Art Director)
**Subject:** All Cycle 22 character sheet fixes complete

---

## Summary

All three character sheet v004 generators are complete and rendered. All Critique 10 flags from Dmitri Volkov and Victoria Ashford have been addressed.

---

## Deliverables

### Task 1 — Byte Expression Sheet v004 (CRITICAL)

**Output:** `output/characters/main/LTG_CHAR_byte_expression_sheet_v004.png` (784×1074px)
**Generator:** `output/characters/main/LTG_CHAR_byte_expression_sheet_v004.py`
**Tool source:** `output/tools/LTG_CHAR_byte_expression_sheet_v004.py`

Fixes applied:
- **1a — Glyph canonical (Section 9B):** 7×7 grid re-implemented row-by-row. CRACK is now a void-black overlay (#0A0A14) drawn on top of glyph pixels — it is NOT a pixel state. HOT_MAG crack stays on body/frame exterior only. DIM_PX corrected: (18,52,60) → (0,80,100) #005064. All 6 cell-level deviations Dmitri flagged are resolved.
- **1b — STORM/RESIGNED differentiation:** STORM now arm_l_dy=6, arm_r_dy=22 (20+ unit asymmetry). RESIGNED stays symmetric (14,14). STORM reads as "damaged-asymmetric" at thumbnail — distinct from RESIGNED's uniform slump.
- **1c — RELUCTANT JOY asymmetry:** arm_l_dy=-2 (one arm resisting the joy impulse), arm_r_dy=12. body_tilt=12 (was 10). Antenna perked slightly with cyan ring (reluctant_joy flag). Reads as "fighting against it" not "mild discomfort."
- **1d — POWERED DOWN squash:** body_squash 0.88 → 0.75. Both arms at max hang (arm_dy=18). Unambiguous vs NEUTRAL.

---

### Task 2 — Cosmo Expression Sheet v004

**Output:** `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v004.png` (912×946px)
**Generator:** `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v004.py`
**Tool source:** `output/tools/LTG_CHAR_cosmo_expression_sheet_v004.py`

Fixes applied:
- **SKEPTICAL arm posture:** arm_l_dy/arm_r_dy changed from -14/-10 (arms raised upward = reads as SURPRISED) to 2/2 (near-neutral, arms resting at sides). body_squash=0.92 added (compressed/contained torso read). Asymmetric brow (l_raise=18, r_raise=0) preserved as face signal. SKEPTICAL now reads as "contracted inward" at thumbnail, not "arms raised."

---

### Task 3 — Luma Expression Sheet v004

**Outputs:**
- `output/characters/main/LTG_CHAR_luma_expression_sheet_v004_guides.png` (1200×900px — with construction guides, production reference)
- `output/characters/main/LTG_CHAR_luma_expression_sheet_v004.png` (1200×900px — clean, no guides, pitch export)
**Generator:** `output/characters/main/LTG_CHAR_luma_expression_sheet_v004.py`
**Tool source:** `output/tools/LTG_CHAR_luma_expression_sheet_v004.py`

Fixes applied:
- **3a — show_guides flag:** `render_face(expr, w, h, show_guides=True/False)` and `build_sheet(show_guides=True/False)` added. When False, `draw_construction_guide()` is skipped. Both exports generated automatically from `__main__`.
- **3b — CURIOUS upgraded to confident squint-test pass:** brow_r_dy increased from -0.24HR to -0.34HR (stronger asymmetry). Eye aperture wider: l_open 0.90→1.0, r_open 0.86→0.94. cy_offset +HR*0.06 (slight forward lean = engaged protagonist posture). CURIOUS is now unmistakable, not marginal.

---

## Pipeline Note

All three generators include the comment:
`# TODO: update import to LTG_TOOL_render_lib_v001 after Kai's rename`

This will need to be addressed once Kai's `ltg_render_lib.py` → `LTG_TOOL_render_lib_v001.py` rename is confirmed.

---

Maya Santos
Character Designer, Luma & the Glitchkin
