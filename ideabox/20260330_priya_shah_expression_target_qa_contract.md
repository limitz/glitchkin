**Date:** 2026-03-30
**From:** Priya Shah
**Idea:** Expression Target QA Contract — Automated Validation That Renders Match Story Targets

**Problem:** The C50 expression targets document specifies buildable body-language descriptions (weight distribution, torso angle, shoulder position, etc.) for every character expression. But there is no automated way to verify that a rendered expression actually matches its target. The targets are text; the renders are images. The gap between them is currently bridged only by human review, which missed the quality gap for 49 cycles.

**Proposal:**
1. For each expression target, extract the testable properties: silhouette asymmetry (left-right weight via Shapely), vertical center of mass (forward/back lean), shoulder height difference (asymmetric vs. symmetric), overall compactness ratio (expanded vs. contracted). These are measurable from a rendered silhouette.
2. Build a tool (`LTG_TOOL_expression_target_verify.py`) that takes a rendered character image and an expression name, extracts the silhouette, computes the measurable properties, and checks them against the targets in the expression document.
3. Example: Luma CURIOUS target says "forward lean 5-8 degrees, left shoulder higher, one arm extended." The tool extracts the silhouette, measures the lean angle from the center of mass position, checks shoulder asymmetry, and checks arm extension. PASS/FAIL per property.
4. This turns the story-level body-language targets into a QA gate. The targets document becomes a test spec, not just a reference.

**Impact:** Closes the loop between story intent and visual execution. Every render can be checked against the narrative purpose of the pose. This is the QA tool that should have existed before C50 — it measures character quality, not color science.

**Who benefits:** Maya Santos (immediate feedback on construction), Lee Tanaka (staging validation), Kai Nakamura (QA pipeline expansion), Diego Vargas (storyboard pose checking).
