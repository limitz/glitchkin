**Date:** 2026-03-30
**From:** Sam Kowalski
**Subject:** C49 Complete — render_qa v2.2.0 + warmcool_scene_calibrate v3.0.0

## Summary

Two deliverables this cycle:
1. Composite warmth score integrated into render_qa v2.2.0 (producer assignment)
2. Sigmoid profile measurement + BG saturation drop added to warmcool_scene_calibrate v3.0.0 (Alex assignment)

## render_qa v2.2.0

- Warm/cool check D now uses composite score: `0.7 * (warm_pct/100) + 0.3 * min(hue_split/127.5, 1.0)`
- Thresholds: REAL_INTERIOR >= 0.25, REAL_STORM >= 0.04, GLITCH <= 0.12, OTHER_SIDE <= 0.04
- Result dict includes `composite_score`, `composite_verdict`, `composite_explanation`
- Graceful fallback chain: composite -> warm_pixel_pct -> hue-split only

## warmcool_scene_calibrate v3.0.0

- `measure_sigmoid_profile()`: samples warm_pct in N horizontal bands between BG_Y and FG_Y, compares to logistic expectation from image-rules.md, reports per-band deviation and PASS/WARN/FAIL
- `measure_saturation_drop()`: measures BG/FG saturation ratio. Target: 0.75-0.85 per BG Saturation Drop rule
- `warm_cool_mix()`: reference implementation of the logistic function (steepness=12.0 default)
- CLI: `--sigmoid-profile --fg-y 0.78 --bg-y 0.70 --steepness 12.0 --bands 10`
- Companion to Lee's depth_temp_lint (band positions) — this checks transition shape

## Validation note

Bash execution was restricted this cycle. Both files parse cleanly (ast.parse verified). Recommend Kai or Morgan run a full QA pass to confirm no regressions.

## Ideabox

Submitted: precritique_qa Section 13 simplification (composite from render_qa instead of independent warm_pixel_metric).
