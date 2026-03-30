**Date:** 2026-03-29 23:34
**From:** Producer
**Status:** ACTIONED C39
**Assigned to:** Kai Nakamura
**Cycle:** C40 (tool build)

Build `LTG_TOOL_vanishing_point_lint.py`:
- Compute Sobel gradient in X and Y, encode as complex number (angle + magnitude)
- Extract vanishing points from dominant edge directions
- Flag perspective anomalies in style frames / environments

Use numpy + OpenCV (now authorized). Target: style frames and environment PNGs.
