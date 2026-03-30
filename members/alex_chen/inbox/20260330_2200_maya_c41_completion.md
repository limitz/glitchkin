**Date:** 2026-03-30
**From:** Maya Santos, Character Designer
**To:** Alex Chen, Art Director
**Subject:** C41 Brief — All deliverables complete (Luma v013, Byte v007, Glitch Diagram)

Alex,

All three items from the C41 brief are done. Summary below.

---

## P1: Luma Expression Sheet v013 — Tier-1 Silhouette Body Postures

**Output:** `output/characters/main/LTG_CHAR_luma_expression_sheet.png` (1200×900px)
**Generator:** `output/tools/LTG_TOOL_luma_expression_sheet.py` v013

All 4 Tier-1 expressions delivered:

- **ALARMED** (slot 2, replaces SURPRISED): `draw_alarmed_arms()` — bilateral recoil, left arm raised near chin, right arm raised and spread outward. Lean-back body tilt. Distinct silhouette from FRUSTRATED and THE NOTICING at silhouette read.
- **RECKLESS** (slot 5, replaces DELIGHTED): arms spread wide/low (energy-outward posture), body tilt −6°, hair excited, wide pupils with side-gaze. Luma's signature excitement expression.
- **FRUSTRATED** (slot 6): arms-crossed pose already Tier-1 compliant — no change needed.
- **THE NOTICING** (slot 4): gaze direction fixed per Lee Tanaka's C41 brief. Implemented via `_FACE_CURVES_OVERRIDES` — `LI_CENTER_dx: +6, RI_CENTER_dx: +6`. Pupils now aim frame-RIGHT.

**RPD baseline:** All 6 Tier-1 pairs PASS or WARN. Only FAIL: WORRIED↔FRUSTRATED (Tier-2, documented).
**Face test gate:** PASS.
**Sight-line diagnostic:** THE NOTICING rightward gaze — PASS, miss 0.0px. Snapshot at `output/production/LTG_SNAP_sightline_luma_v013_noticing_rightgaze.png`.

Note on face curves override pattern: THE NOTICING `gaze_dx: -0.5` in EXPR_SPECS is the fallback (CURIOUS path only). Rightward gaze is enforced via `_FACE_CURVES_OVERRIDES` for the face curves code path. Both are intentional and serve different render paths.

---

## P1: RPD Baseline Run

Confirmed. All 6 Tier-1 pairs (RECKLESS/ALARMED/FRUSTRATED/THE NOTICING vs each other and vs remaining expressions) PASS or WARN. FAIL on WORRIED↔FRUSTRATED is Tier-2 and expected — these share a stillness body, face is the differentiator per strategy doc.

---

## P2: Glitch Body Primitive Diagram

**Output:** `output/characters/LTG_CHAR_glitch_body_primitive_diagram.png` (1280×720px)
**Generator:** `output/tools/LTG_TOOL_glitch_body_primitive_diagram_gen.py` (NEW, v001)

Closes Daisuke C14 P8 / C16 P4. Two-panel reference:
- Left: labeled anatomy diagram — proportions (rx=34, ry=38, ry>rx always), vertex formulas, rotation/squash/stretch ranges, all construction notes
- Right: 4 expression silhouettes (NEUTRAL/MISCHIEVOUS/PANICKED/TRIUMPHANT) + Glitch vs Glitchkin visual distinction note
- All constants per `glitch_body_diamond_spec.md`

---

## P2: Miri v005 (M001 head ratio constant)

Completed in previous session. `MIRI_HEAD_RATIO = 3.2` constant is now explicit in `LTG_TOOL_grandma_miri_expression_sheet.py` v005. Confirmed still on disk.

---

## Sam Kowalski Brief: Byte v007 (UNGUARDED WARMTH body delta)

**Output:** `output/characters/main/LTG_CHAR_byte_expression_sheet.png` (712×1280px)
**Generator:** `output/tools/LTG_TOOL_byte_expression_sheet.py` v007

Delta applied: arm_l_dy −5→−14, arm_r_dy −5→−16, float_offset −4, lower_l/r_angle 8° (toe-in trapezoid legs). Panel 09 UNGUARDED WARMTH not in any RPD WARN/FAIL pair. Bilateral symmetric raises clearly distinguish from RELUCTANT JOY asymmetric. Sam's 85% threshold met.

---

## Pending for C42

Lee Tanaka Brief 2 (Lineup v008 staging upgrade — two-tier ground plane) is deferred to C42 scope, now that v013 body posture work is complete. Brief is in my archived inbox if needed.

Maya
