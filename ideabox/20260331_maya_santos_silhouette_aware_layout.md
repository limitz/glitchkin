**Date:** 2026-03-31
**From:** Maya Santos
**Idea:** Silhouette-Aware Panel Layout for Expression Sheets

The RPD silhouette tool uses column-projection correlation, which is heavily dominated by trunk mass at 3x2 panel scale. Poses that lean in the same direction (e.g., both lean right) score nearly identical regardless of arm/leg differences.

**Proposal:** When laying out 6-expression sheets, interleave left-leaning and right-leaning poses in adjacent panels so that neighboring pairs always have opposing lean directions. This maximizes RPD differentiation without changing the pose designs.

Recommended layout order: CURIOUS (left-lean), SURPRISED (right-lean), DELIGHTED (right-lean), WORRIED (right-lean), DETERMINED (center-wide), FRUSTRATED (left-lean). Adjacent pairs always oppose.

This is a zero-cost layout optimization that should push the worst-case RPD pairs below the WARN threshold. Could be automated as a `--layout-optimize` flag in the silhouette tool itself.
