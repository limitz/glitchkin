# Idea: Gesture Lint Grid Label Exclusion
**From:** Lee Tanaka
**Date:** 2026-03-31

## Problem
`LTG_TOOL_gesture_line_lint.py` grid detection splits expression sheets into cells that include narrow label strips and margin areas. These produce false-positive FAILs (e.g., a 44px-wide text strip with 0px deviation scores as FAIL). On Maya's cairo Luma sheet, 1 of 7 detected cells was a false positive.

## Proposal
Add a minimum cell width filter to the grid detector. Any cell narrower than 15% of the image width should be excluded from linting (it's a label, separator, or margin — not a character panel). This is a 3-line change in `_detect_grid()`.

Alternatively, add a `--min-cell-pct 15` CLI flag to let users control the threshold.

## Impact
Eliminates false-positive FAILs in the summary line, making the tool output trustworthy without manual interpretation. When Morgan integrates gesture lint into precritique_qa, false positives would produce misleading automated reports.
