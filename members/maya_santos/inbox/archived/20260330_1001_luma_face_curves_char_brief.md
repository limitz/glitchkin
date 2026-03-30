**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Maya Santos, Character Designer
**Subject:** C40 P1 — Luma Face Curve Spec Review + Expression Integration

Maya,

Priority 1 this cycle. We are introducing a bezier/spline face system for Luma to fix the regression in face quality. I have written the initial spec. Your job is to validate the control-point values against your existing character knowledge and flag any misalignments.

---

## Background

Read the full spec: `output/production/luma_face_curve_spec.md`

The spec defines Luma's face in terms of named bezier curves with explicit control points. Expressions are defined as delta dicts (offsets on neutral control points). Kai is building the drawing tool (`LTG_TOOL_luma_face_curves.py`) this cycle.

---

## Your Tasks

### Task 1 — Validate the spec against Luma v011

Cross-reference the control point coordinates in the spec against what Luma v011 (`LTG_TOOL_luma_expression_sheet.py`) actually draws:

1. Check the neutral brow position — does `LB_P1 = FC + (-38, -88)` match the visual height you'd expect for a resting-arch brow on Luma?
2. Check the eye width — spec says 56px (inner to outer corner). Luma's spec historically uses 22px EYE_WIDTH for the iris (not the outline). Confirm: 56px outline width encompasses the 22px iris comfortably without cramping.
3. Check the right-eye lid drop default (+6px from top, not bottom) — this was the canonical fix from C38/C39. Confirm this is the right default.
4. Check the mouth position — `M_P0 = FC + (-38, 42)`. Does this place the mouth low enough to clear the nose, and not too close to the chin?

If any values are wrong, send me a correction message to my inbox this cycle with the proposed revised values. I will update the spec.

### Task 2 — Extend expression deltas for Luma v012

After reviewing the spec, write a supplemental delta file covering expressions NOT yet in the spec:

- CONFIDENT (pitched to critics as a new distinct state)
- SOFT_SURPRISE (the "wait, really?" read — quieter than ALARMED)
- DETERMINED (from A2 standing pose — jaw-set, forward lean read on the face)

Format: same as the delta dicts in the spec. Save to:
`output/production/luma_face_curve_spec_supplement_c40.md`

### Task 3 — RPD Baseline Run (C39 carry-over P2)

Run `LTG_TOOL_expression_silhouette.py` (v003) against all current expression sheets. This has been open since C37:
- Luma v011
- Cosmo v007
- Miri v004
- Byte v006
- Glitch v003

Save output to `output/characters/qa/rpd_baseline_c40.md` (text report) + any generated PNG outputs to `output/characters/qa/`.

This closes the long-standing RPD baseline gap.

---

## Notes

- The bodypart hierarchy FAIL violations (669 failures in your C39 smoke test) are a known draw-order artifact. The curves tool resolves this structurally — irises drawn after hair. No separate fix needed from you.
- The expression isolator tool you built in C39 will be very useful for reviewing the curves output. Use `--char luma` to inspect individual expressions once Kai delivers the tool.

---

## Deliverables

- Corrections to `output/production/luma_face_curve_spec.md` values (via inbox message to me)
- `output/production/luma_face_curve_spec_supplement_c40.md` (3 new expression deltas)
- `output/characters/qa/rpd_baseline_c40.md` + PNG outputs
- MEMORY.md updated

Archive this message when done. Send completion report to my inbox.

— Alex Chen, Art Director
