**Date:** 2026-03-30
**From:** Sam Kowalski
**Subject:** Warm-pixel-percentage metric ready for precritique_qa / render_qa integration

## Context

The hue-split metric (top-half vs bottom-half median hue) fails for REAL_INTERIOR: 6/7 reference photos fall below the 12.0 threshold because single-temperature-dominant interiors have near-zero vertical split.

## New metric

`LTG_TOOL_warm_pixel_metric.py` — measures percentage of chromatic pixels in the warm hue range.

## API

```python
from LTG_TOOL_warm_pixel_metric import measure_warm_pixel_percentage, evaluate_threshold

result = measure_warm_pixel_percentage(img)  # PIL Image
# result["warm_pct"] -> float (e.g. 67.2)

eval_result = evaluate_threshold(result["warm_pct"], "REAL_INTERIOR")
# eval_result["passes"] -> bool
# eval_result["verdict"] -> "PASS" or "FAIL"
```

## Thresholds (calibrated C47)

- REAL_INTERIOR: warm_pct >= 35%
- REAL_STORM: warm_pct >= 5%
- GLITCH: warm_pct <= 15%
- OTHER_SIDE: warm_pct <= 5%

## Integration recommendation

1. Add `warm_pixel_pct` check to render_qa alongside (or replacing) `_check_warm_cool()`
2. For REAL_INTERIOR, use warm_pixel_pct as primary gate; hue-split as secondary
3. For REAL_STORM, keep both metrics (hue-split useful for contested scenes)
4. World-type inference: tool has `infer_world_type()` but recommend using existing `world_type_infer` for consistency

## Validation

31/31 generated assets PASS, 7/7 reference photos PASS. Full report at `output/production/warm_pixel_metric_report_c47.md`.
