<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->

# Luma Gesture Validation Report — C52
## Lee Tanaka — Character Staging & Visual Acting Specialist
**Date:** 2026-03-30

---

## Summary

Maya's cairo-engine Luma expression sheet (C51, `LTG_TOOL_luma_cairo_expressions.py` v1.0.0) implements Lee's C50 gesture spec for 2 of 6 expressions: **CURIOUS** and **SURPRISED**. Both expressions PASS gesture line lint. The offset chain architecture works. Weight shift is readable. Counterpose produces visible silhouette differentiation.

**Verdict: GESTURE READS WELL.** Extend spec to Cosmo and Miri (done in this cycle — see companion documents).

---

## Gesture Line Lint Results

### Cairo Luma (C51) — `LTG_PROD_luma_cairo_expressions.png`

| Panel | Expression | Grade | Deviation | Notes |
|---|---|---|---|---|
| P3 | CURIOUS | **PASS** | 13.38px (scale 1.58) | Strong forward C-curve visible |
| P6 | SURPRISED | **PASS** | 24.59px (scale 1.60) | Dramatic backward lean, clear startle recoil |
| P1 | (label strip) | FAIL | 0.00px | False positive — narrow text strip, not character |
| P2, P4, P5, P7 | (margins/labels) | SKIP | — | Non-character regions |

**Grid detection note:** The lint tool's grid detector splits this 1280x720 sheet into 7 cells, some as narrow as 44px. The real character panels are P3 (CURIOUS, 369px wide) and P6 (SURPRISED, 455px wide). The P1 FAIL is a false positive on a narrow label/border strip. Recommend: when running lint on this sheet, use `--single` mode per half, or add label-area exclusion to the grid detector.

### Old PIL Luma (pre-C51) — `LTG_CHAR_luma_expression_sheet.png`

For comparison, the old PIL expression sheet:
- **13 FAIL** / 4 WARN / 5 PASS (across 28 detected cells)
- Every main expression pose FAILs with 0.00px deviation (confirmed straight vertical)
- The 5 PASSes come from small decorative/annotation elements, not character poses

**Improvement: from 0/6 PASS (old) to 2/2 PASS (new).** The offset chain works.

---

## Gesture Quality Assessment

### CURIOUS (P3) — PASS, 13.38px deviation
- **Offset chain visible:** Head leads forward (head_offset=-18), hips shift right (hip_shift=12), torso leans forward (torso_lean=-16). The three offsets create a readable C-curve.
- **Weight shift readable:** The 60/40 front weight is visible in the foot positions and body lean direction.
- **Counterpose present:** Shoulders compensate opposite to hips (shoulder_offset=-10).
- **Arms asymmetric:** Right arm in chin-touch (THE NOTICING callback), left arm reaching forward.
- **Pigeon-toed front foot:** front_foot_angle=-12 is visible.

### SURPRISED (P6) — PASS, 24.59px deviation
- **Most dramatic gesture line on the sheet** — 24.59px deviation vs CURIOUS's 13.38px. This is correct: SURPRISED should be the most extreme pose (backward C-curve, startle recoil).
- **Backward lean clear:** torso_lean=28, hip_shift=-26 (amplified values from Maya's implementation).
- **Front foot lifted:** front_foot_lift=14 is visible — foot leaves the ground in startle reflex.
- **Arm asymmetry:** Left arm defensive-high (near face), right arm flung back (counterbalance). Arms at completely different heights and distances from body.
- **Hip tilt dramatic:** -7.0 degrees toward back foot creates visible angular break.

---

## Remaining Luma Expressions (C50 Spec, Not Yet Built)

The following 4 expressions from the C50 spec are NOT yet implemented in the cairo engine. Maya should add these next:

| Expression | Gesture Shape | Key Visual Hook | Build Priority |
|---|---|---|---|
| DETERMINED | Backward power S | Widest stance, chin lifted | High |
| WORRIED | Inward compressed S | Narrowest silhouette, self-hold arms | High |
| DELIGHTED | Upward erupting S | Tallest (tiptoe), asymmetric Y-arms | Medium |
| FRUSTRATED | Aggressive diagonal | 80/20 weight, one arm flung | Medium |

**Recommended build order:** DETERMINED + WORRIED next (these create the maximum silhouette contrast with CURIOUS and SURPRISED already done — widest vs narrowest, forward vs backward). Then DELIGHTED + FRUSTRATED.

---

## Face Test Gate Status

Face test run at sprint scale (head_r=23): FOCUSED DET. = PASS, EYES ONLY = PASS, DETERMINED+ = PASS. Face legibility confirmed at production scale. The gesture line implementation has not broken face readability.

---

## Annotation Overlays

- `LTG_SNAP_gesture_lint_LTG_PROD_luma_cairo_expressions.png` — gesture line overlay on cairo sheet
- `LTG_SNAP_gesture_lint_LTG_CHAR_luma_expression_sheet.png` — gesture line overlay on old PIL sheet (for comparison)
