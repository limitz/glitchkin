**Author:** Sam Kowalski
**Cycle:** 48
**Date:** 2026-03-30
**Idea:** Integrate the composite warmth score into render_qa as the primary warm/cool check, replacing the hue-split-only metric. The composite score (70% warm-pixel-pct + 30% hue-split) correctly classifies all 19 tested assets with zero false positives, while the hue-split metric alone produces systematic false positives for single-temperature-dominant scenes (FP-006/FP-007). Kai Nakamura could import `compute_composite_warmth_score()` from `LTG_TOOL_composite_warmth_score.py` and use the per-world-type composite thresholds (REAL_INTERIOR >= 0.25, REAL_STORM >= 0.04, GLITCH <= 0.12, OTHER_SIDE <= 0.04) to replace the current `_check_warm_cool()` logic.
**Benefits:** Kai Nakamura (render_qa maintainer) — eliminates the warm/cool WARN false-positive class that has persisted since C35. All team members running QA checks — fewer false alarms to investigate. Critics — cleaner QA reports with no documented-FP noise.
