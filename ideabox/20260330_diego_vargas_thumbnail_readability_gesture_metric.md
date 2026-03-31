# Idea: Gesture-Aware Thumbnail Readability Metric

**From:** Diego Vargas
**Date:** 2026-03-30
**Cycle:** 51

## Problem
Morgan's `LTG_TOOL_thumbnail_readability.py` uses edge-based metrics (Canny edge density,
silhouette IoU) that penalize anti-aliased pycairo rendering vs hard-pixel PIL rendering.
The tool reports LOWER scores for visually BETTER character work because smoother bezier
curves produce gentler gradients that Canny misses.

## Proposal
Add a **gesture line metric** to the thumbnail readability tool:
1. Extract the character's center-of-mass vertical axis at each scale
2. Measure the deviation from vertical (gesture lean angle)
3. Compare lean angle preservation across scales: does the gesture survive downscaling?
4. A character with 3-5 degrees of lean that still reads as leaning at 64px PASSES.
   A mannequin-straight character that reads as a rectangle at 64px FAILS.

This would catch exactly the improvement that pycairo characters provide (organic gesture)
without being fooled by anti-aliasing differences.

## Who
Morgan Walsh to implement (tool owner). Diego Vargas to test on P17 old vs new.
