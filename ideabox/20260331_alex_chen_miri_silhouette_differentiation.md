# Idea: Miri Silhouette Differentiation Priority

**Submitted by:** Alex Chen
**Date:** 2026-03-31

## Problem
Luma/Miri silhouette distinctiveness score is DS=0.01 (WPC=1.000) — they are visually interchangeable at silhouette scale. This is the single worst metric in the entire QA pipeline.

## Proposal
Make Miri's pycairo rebuild the top priority for next cycle. The rebuild should:
1. Exaggerate Miri's unique silhouette features: forward lean (-4deg permanent), wider cardigan shoulder line, bun+hairpin crown, tea cup prop
2. Use Lee's Miri gesture spec (permanent base_lean, hands-never-idle rule) to ensure every expression has a distinct pose
3. Run silhouette distinctiveness tool against Luma after rebuild — target DS > 0.15

This is not just a rendering quality improvement like the other pycairo rebuilds — it's a fundamental design differentiation issue that affects pitch readability.

## Impact
- Fixes the worst QA metric in the pipeline
- Unblocks SF05 and SF06 (both require Miri with distinctive body language)
- Lineup v013 can then be fully pycairo (5/5 characters)
