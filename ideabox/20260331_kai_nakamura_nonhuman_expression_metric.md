**Date:** 2026-03-31
**From:** Kai Nakamura
**Idea:** Non-Humanoid Expression Metric Mode

**Problem:** The expression_range_metric relies on face region pixel delta (top 40% of bounding box) which works well for humanoid characters but poorly for non-humanoid ones like Glitch. Glitch's diamond body and non-standard face region mean the metric consistently reports WARN even when expression variation exists in different parts of the body (glow patterns, shape distortion, color shifts).

**Proposal:** Add an alternate analysis mode to LTG_TOOL_expression_range_metric.py for non-humanoid characters that:
1. Uses full-body pixel delta instead of head-zone-only
2. Adds a color histogram divergence metric (captures glow/color expression changes)
3. Uses skimage SSIM as a complementary metric (already evaluated in C51: lower SSIM = more expression variation)
4. Per-character config allows specifying which mode to use

**Benefit:** Eliminates persistent false WARNs for Glitch. Provides more accurate expression variation data for non-humanoid characters. The SSIM evaluation data from C51 already shows the approach works.

**Effort:** Medium (1 cycle)
