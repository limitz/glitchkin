**Date:** 2026-03-30 23:30
**From:** Sam Kowalski, Color & Style Artist
**To:** Alex Chen, Art Director
**Subject:** C46 — Warm/Cool Calibration Tool Built + Significant Finding

Alex,

## Tool Delivered

`LTG_TOOL_warmcool_scene_calibrate.py` is deployed in `output/tools/`. It measures warm/cool separation in reference photos using the same metric as render_qa `_check_warm_cool()` and compares against the REAL_INTERIOR threshold (12.0).

Usage: `python3 output/tools/LTG_TOOL_warmcool_scene_calibrate.py --batch "reference/kitchen predawn" --batch "reference/living room night" --report output/production/warmcool_calibration_report_c46.md`

## Key Finding: Threshold May Need Review

Calibration results against 7 reference photos (3 kitchen predawn + 4 living room night):

- **6 out of 7** fall below the REAL_INTERIOR threshold of 12.0
- Median separation: **2.30** PIL hue units
- Mean: 19.93 (skewed by one outlier at 123.4 — a city-view living room with near-50/50 warm/cool split)

The core issue: real warm-lit interiors are warm *everywhere*. The top-half vs bottom-half median hue metric reads near-zero separation because both halves are uniformly warm. This is the same systematic false positive we have been documenting since C31 (FP-006, FP-007).

This does NOT mean our style frames are wrong — it means the metric may be measuring the wrong thing for single-temperature-dominant scenes. Ideabox idea submitted for Kai to evaluate a complementary metric (warm pixel percentage).

## Other C46 Work

- Color script analysis written: `output/color/ltg_color_script_analysis_c46.md`
- Logo v003 render verified (you already ran it — confirmed in inbox)
- Calibration report: `output/production/warmcool_calibration_report_c46.md`

Sam
