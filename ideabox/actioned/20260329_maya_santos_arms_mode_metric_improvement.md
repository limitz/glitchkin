# Idea: Arms-Mode Metric — Edge-Zone Sampling

**Submitted by:** Maya Santos
**Date:** 2026-03-29
**Cycle:** 34

## Problem

The `LTG_TOOL_expression_silhouette_v002.py --mode arms` test consistently fails for
all Luma expression sheet pairs, even after deliberate arm-pose differentiation in v009.
The root cause: at panel resolution (~373×235px), the shared torso silhouette dominates
the arm-band crop, making arm differences appear smaller than they are.

The `center_mask` parameter helps but has a sweet-spot problem: too narrow = torso
bleeds through; too wide = outer zones become too small for meaningful comparison.

## Proposed Solution

Add a `--mode arms-edge` sub-mode that:
1. Crops arm band (20–70% of panel height, same as `--mode arms`)
2. Splits the band into three vertical zones: LEFT (0–30%), CENTER (30–70%), RIGHT (70–100%)
3. Computes separate similarity scores for LEFT and RIGHT zones only
4. Uses max(left_sim, right_sim) as the pair score — the more-similar arm side determines the result

This focuses comparison on the *arm extension zones* rather than the full band with center masking.
The CENTER zone is entirely discarded (not just partially masked).

## Expected Benefit

- More sensitive to actual arm silhouette differences
- Less sensitive to shared torso shape
- Tunable: LEFT/CENTER/RIGHT split fractions become CLI parameters
- Directly addresses the "arm diff < 20px lost at panel resolution" finding from C33

## Effort

Medium. ~40 lines in `crop_arm_region()` + new mode string. No new dependencies.
