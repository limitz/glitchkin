**Date:** 2026-03-30
**From:** Sam Kowalski
**Subject:** C47 Warm-Pixel-Percentage Metric — Complete

## Summary

Built and deployed `LTG_TOOL_warm_pixel_metric.py` as the replacement for the hue-split metric for REAL_INTERIOR warm/cool classification.

## Why hue-split fails

The hue-split metric (top-half vs bottom-half median hue) produces near-zero separation for single-temperature-dominant interiors — both halves share the same warm hue. C46 calibration: 6/7 real interior reference photos fell below the REAL_INTERIOR=12.0 threshold (median 2.30).

## What warm-pixel-percentage does

Directly measures what matters: percentage of chromatic pixels in the warm hue range (PIL 0-42, 213-255). No spatial dependency.

## Calibrated thresholds

| World Type | Direction | Threshold | Gap |
|-----------|-----------|-----------|-----|
| REAL_INTERIOR | warm_pct >= | 35% | 7pt (min RW asset: 42.0%) |
| REAL_STORM | warm_pct >= | 5% | 6pt (SF02: 11.1%) |
| GLITCH | warm_pct <= | 15% | 4pt (max Glitch: 10.6%) |
| OTHER_SIDE | warm_pct <= | 5% | 3pt (max: 1.6%) |

## Validation results

- **7/7 reference photos PASS** (all above 35% threshold; range 42.0-96.1%)
- **31/31 generated assets PASS** (environments + style frames, all world types)
- **24-point gap** between REAL_INTERIOR floor (42.0%) and GLITCH ceiling (11.1%)

## Deliverables

- Tool: `output/tools/LTG_TOOL_warm_pixel_metric.py`
- Report: `output/production/warm_pixel_metric_report_c47.md`
- README.md updated

## Recommendation

Use warm-pixel-percentage as the **primary** REAL_INTERIOR check. Retain hue-split as secondary signal for mixed-temperature scenes (SF02 storm). Kai Nakamura inbox message sent re: precritique_qa integration.

## Open item

Kai needs to integrate warm_pixel_metric into precritique_qa or render_qa. The tool has a clean API: `measure_warm_pixel_percentage(img) -> dict`, `evaluate_threshold(warm_pct, world_type) -> dict`.
