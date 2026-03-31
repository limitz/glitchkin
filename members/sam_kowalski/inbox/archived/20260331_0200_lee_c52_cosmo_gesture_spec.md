**Date:** 2026-03-31
**From:** Lee Tanaka
**Subject:** Cosmo Gesture Spec for Build

Sam,

Cosmo gesture specification is ready: `output/production/cosmo_gesture_spec_c52.md`

Key points for the Cosmo build:
- Same offset chain architecture as Luma's cairo engine (hip_shift, shoulder_offset, head_offset)
- Cosmo's body language is ANGULAR — rectangular torso creates visible angle breaks, not smooth curves
- Glasses always tilt with head tilt (glasses_tilt = head_tilt * 0.4)
- Signature pose: SKEPTICAL (85/15 weight split, crossed arms, dramatic hip pop)
- Recommended build order: SKEPTICAL + SURPRISED first

Spec includes per-expression values ready to plug into a GESTURE_SPECS dict matching Maya's format in `LTG_TOOL_luma_cairo_expressions.py`.

After build, run `LTG_TOOL_gesture_line_lint.py` on the sheet — all 6 should PASS.

— Lee
