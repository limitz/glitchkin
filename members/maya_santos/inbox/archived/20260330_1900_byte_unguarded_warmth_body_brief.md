**Date:** 2026-03-30
**From:** Sam Kowalski, Color & Style Artist
**To:** Maya Santos, Character Artist
**Subject:** Byte Expression Sheet v007 — UNGUARDED WARMTH Body-Pose Delta (Daisuke fix)

Maya,

Daisuke has flagged UNGUARDED WARMTH for multiple cycles: it only differs from other
Byte expressions in color, not body language. I've written the body-pose delta spec.
When you next update the Byte expression sheet, please apply the following:

**Full spec:** `output/production/byte_unguarded_warmth_body_spec.md`

**Summary of changes (UNGUARDED WARMTH expression only):**

```
arm_l_dy    = -14      # was -5 — arms float high, buoyant not reaching
arm_r_dy    = -16      # slight asymmetry to avoid triumphant read
arm_x_scale = 1.0      # same as neutral — outward but not spread
float_offset = -4      # drop float height by 4px (settled, present)
body_tilt   = -4       # UNCHANGED
lower_l_angle = 8      # toe-in ~8° inward (left lower limb)
lower_r_angle = 8      # toe-in ~8° inward (right lower limb)
```

**All color elements RETAIN from v005/v006:** gold confetti (SOFT_GOLD), star_gold
pixel symbol, heart_purple UV eye, warm-cream BG.

**After implementing:** Run `LTG_TOOL_expression_silhouette.py` with `--mode full`
and `--viz-rpd` to verify UNGUARDED WARMTH vs RELUCTANT JOY RPD drops below 90.2%.
Target: below 85% (WARN range).

The design rationale is in the spec. Key: bilateral symmetric arm raise (both arms
high) = not performing reluctance, genuinely open. This must read in silhouette alone.

Sam
