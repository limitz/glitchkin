**Author:** Lee Tanaka
**Cycle:** 47
**Date:** 2026-03-30
**Idea:** Add per-asset band position overrides to the depth_temp_lint Section 12 integration. The C47 run showed SF04 and SF05 FAIL at default band positions (78% FG, 70% BG) which are calibrated for lineup tier geometry. Style frames have different character ground planes. A JSON config (like arc_diff_config.json) could map each asset to its actual FG/BG band Y positions, reducing false FAILs without weakening the rule.
**Benefits:** Reduces false positives in the depth temp lint for non-lineup multi-character scenes. Morgan Walsh or any pipeline member could implement this as a config file alongside the existing DEPTH_TEMP_PNGS registry. Would make the Section 12 results more actionable for artists.
