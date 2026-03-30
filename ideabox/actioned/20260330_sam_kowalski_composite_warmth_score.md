**Author:** Sam Kowalski
**Cycle:** 47
**Date:** 2026-03-30
**Idea:** Create a composite warmth score that combines warm-pixel-percentage (new C47 metric) with warm:cool ratio into a single 0-100 score. The score would weight warm_pct at 70% and normalized W:C ratio at 30%. This gives a single number that both the pipeline (precritique_qa thresholds) and human reviewers (pitch deck annotations) can use, instead of needing to interpret two separate numbers. The score would be: `warmth_score = 0.7 * warm_pct + 0.3 * min(ratio / 5.0, 1.0) * 100`. A REAL_INTERIOR would need score >= 30; Glitch would need score <= 12.
**Benefits:** Kai Nakamura (simpler precritique_qa integration -- one threshold instead of two), Alex Chen (single-number pitch deck quality metric), all environment artists (clearer pass/fail signal on warm/cool compliance).
