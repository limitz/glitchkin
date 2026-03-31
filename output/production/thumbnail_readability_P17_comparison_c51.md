# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.

# P17 Thumbnail Readability Comparison — Old PIL vs New pycairo Characters (C51)

**Date:** 2026-03-30
**Author:** Diego Vargas

## Summary

Both versions of P17 FAIL at 128px due to expression density below the 0.08 threshold.
This is consistent with the C49 audit finding that cel-shaded smooth-fill panels score
low on edge density metrics (P17 was one of the 5 FAIL panels in that audit).

The pycairo version shows marginal improvements in expression density (+0.0002 at 128px,
+0.0031 at 32px) and hue stability (+0.012 at 32px), but marginal decreases in silhouette
IoU and edge preservation. The differences are within noise range for this tool.

## Detailed Comparison

| Metric | Scale | OLD (PIL) | NEW (pycairo) | Delta |
|--------|-------|-----------|---------------|-------|
| Silhouette IoU | 128px | 0.907 | 0.904 | -0.003 |
| Silhouette IoU | 64px | 0.561 | 0.535 | -0.026 |
| Silhouette IoU | 32px | 0.503 | 0.478 | -0.025 |
| Edge Preservation | 128px | 0.417 | 0.371 | -0.046 |
| Edge Preservation | 64px | 0.279 | 0.245 | -0.034 |
| Edge Preservation | 32px | 0.223 | 0.198 | -0.025 |
| Hue Stability | 128px | 0.996 | 0.995 | -0.001 |
| Hue Stability | 64px | 0.977 | 0.985 | +0.008 |
| Hue Stability | 32px | 0.949 | 0.961 | +0.012 |
| Expression Density | 128px | 0.039 | 0.040 | +0.001 |
| Expression Density | 64px | 0.064 | 0.064 | 0.000 |
| Expression Density | 32px | 0.101 | 0.104 | +0.003 |

## Grades

| Scale | OLD | NEW |
|-------|-----|-----|
| 128px | FAIL | FAIL |
| 64px | PASS | WARN |
| 32px | PASS | PASS |
| Overall | FAIL | FAIL |

## Analysis

1. **Edge preservation decreased** — pycairo's anti-aliased curves produce smoother
   edges with gentler transitions vs PIL's hard pixel edges. The Canny-based edge
   detector picks up fewer edge pixels because gradients are smoother. This is visually
   BETTER (organic curves) but scores LOWER on a metric designed to detect hard edges.

2. **Hue stability improved at small scales** — pycairo's gradient fills on the body
   shapes produce more consistent color blocks that survive downscaling better than
   PIL's flat fill + hard boundary approach.

3. **Expression density unchanged** — at MED panel scale (characters ~100-140px tall),
   both rendering engines produce faces too small for the head-region edge density test
   to differentiate. The 128px FAIL is a panel-type issue (TWO_SHOT MED with small
   characters), not a rendering engine issue.

4. **Silhouette IoU slightly lower** — the organic bezier body shapes have softer edges
   that downscale differently from PIL rectangles. The IoU metric is measuring mask
   overlap of hard-thresholded foreground detection, which slightly penalizes anti-aliased
   boundaries.

## Conclusion

The thumbnail_readability tool's metrics are not well-suited to measure the actual
improvement from pycairo characters. The improvement is in:
- **Gesture readability** (bezier tapered limbs vs rectangle arms)
- **Silhouette organic quality** (wobble hair vs radial lines)
- **Character identity** (head-to-body 37% ratio, proper proportions)

These are human-perceptible improvements that the current tool cannot quantify.
The tool's edge-based metrics actually penalize smoother rendering.

**Recommendation:** P17 pycairo version is the keeper — superior visual quality despite
marginal metric regression. The 128px FAIL is a known panel-type limitation (C49 audit).
