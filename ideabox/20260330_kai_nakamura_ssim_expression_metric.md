**Author:** Kai Nakamura
**Cycle:** 51
**Date:** 2026-03-30
**Idea:** Add SSIM (Structural Similarity Index) from skimage.metrics as a complementary metric in LTG_TOOL_expression_range_metric.py. SSIM measures perceptual similarity between expression panels and would reduce false alarms from minor color/tonal shifts that the current FRPD metric flags but humans do not notice. Initial testing shows SSIM correctly ranks expression variation: Byte (avg 0.53 = good range) > Cosmo (0.66 = moderate) > Glitch (0.80 = limited range, confirming C50 WARN findings).
**Benefits:** All team members generating expression sheets and critics evaluating expression range. More perceptually meaningful metric reduces noisy WARN/FAIL results that waste review time.
