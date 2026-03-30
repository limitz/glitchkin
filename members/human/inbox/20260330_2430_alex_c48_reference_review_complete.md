**Date:** 2026-03-30
**From:** Alex Chen
**Subject:** C48 Reference Review Complete — Key Findings and Tool Priorities

Producer,

Reference image review across all 22 categories is complete. Full art direction notes written to `output/production/reference_art_direction_notes_c48.md`. Key findings:

## Top Findings Affecting Current Assets

1. **CRT glow asymmetry.** Real CRT glow is brighter above/sides than below (cabinet occlusion). Our generators use symmetric Gaussian. All CRT glow needs asymmetric falloff — 30% reduction below screen.

2. **Warm/cool ratio may be miscalibrated.** Real interiors show 25-35% warm pixels, 65-75% cool. Our REAL_INTERIOR threshold of 12.0 warm/cool ratio seems high. Needs Sam/Kai calibration against refs.

3. **Temperature transition is sigmoid, not linear.** Real warm-to-cool falloff happens in a narrow band (~10-15% of room depth), not gradual. Generators should use step/sigmoid, not linear interpolation.

4. **BG tier needs saturation drop in addition to cool shift.** Depth Temperature Rule should add a saturation component: BG objects lose 15-25% saturation relative to FG.

5. **School hallway missing ceiling convergence.** This is a cheap, high-impact depth improvement for Hana.

6. **UV_PURPLE may need hue center shift.** Real glitch art clusters at 280-290, not 270. Minor adjustment.

## Tool Build Priority for C49

Top 3 to build next cycle:
1. `warmcool_scene_calibrate` — warm/cool threshold is potentially wrong; highest impact
2. `glow_profile_extract` — CRT glow asymmetry data needed before generator fixes
3. `face_metric_calibrate` — expression delta thresholds are a new concept from refs

Remaining 5 tools ranked C50-C52 in the full notes.

## Perspective Rules Updated

Added hallway as explicit 1-point case, ceiling convergence to audit checklist, camera-height VP_Y cross-check note. See updated `docs/perspective-rules.md`.

## Byte Position

Approved Priya's recommendation — Byte stays CRT through P19-P20, floats to Luma's level at P21. Messages sent to Priya (acknowledgment) and Diego (confirmation). Diego is unblocked for P22/P22a.

## Team Output Review

- **Ryo's draw_shoulder_arm helper:** Clean, well-structured shared module. Three public functions (draw, compute, polyline) plus style dataclass. Correctly implements Shoulder Involvement Rule from image-rules.md. Demo shows all clothing types x 7 angles. Approved for integration. Recommend Maya, Lee, Jordan adopt in next update cycle.
- **Morgan's ci_suite v1.8.0:** Check 10 repurposed from ext_model_check to doc_staleness. Clean removal of old check, clean addition of new. Delegates to doc_governance_audit. Thresholds (WARN 5+, FAIL 10+ cycles stale) are reasonable. Approved.

All inbox messages archived.

— Alex
