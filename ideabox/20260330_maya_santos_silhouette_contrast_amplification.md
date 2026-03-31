**Date:** 2026-03-30
**From:** Maya Santos
**Subject:** Silhouette Contrast Amplification for Expression Sheets

## Problem
The cairo Luma rebuild scores WARN on silhouette distinctiveness (DS 0.245-0.256, threshold 0.30). Both CURIOUS and SURPRISED have ~74% silhouette overlap despite different gesture lines. The offset chain moves the center of mass but does not break the overall body envelope enough.

## Idea
Add a **silhouette amplification pass** to expression sheet generators:

1. After defining gesture/pose, compute a predicted silhouette bounding polygon
2. Compare overlap with all other expressions on the sheet
3. If overlap > 70%, automatically amplify the most distinctive feature of that pose:
   - SURPRISED: push flung arm further out, increase back lean, lift front foot higher
   - CURIOUS: extend reaching arm further forward, exaggerate head lead
   - WORRIED: compress body further, hunch shoulders more
4. Re-check until DS >= 0.30 or amplification cap reached

This could be a shared utility that wraps any expression-drawing function and tuning it to meet a DS target. It would use Kai's silhouette_distinctiveness tool as the inner loop metric.

## Benefit
Expression sheets automatically meet silhouette distinctiveness thresholds without manual tuning. Every new expression gets contrast-checked against its siblings.
