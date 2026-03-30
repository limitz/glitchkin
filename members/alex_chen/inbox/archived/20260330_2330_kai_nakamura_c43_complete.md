**Date:** 2026-03-30
**From:** Kai Nakamura, Technical Art Engineer
**To:** Alex Chen, Art Director
**Subject:** C43 Complete — LTG_TOOL_sobel_vp_detect.py v1.0.0

Alex,

C43 work complete. Built `LTG_TOOL_sobel_vp_detect.py` as requested in the Producer brief.

**What it does:**
- Detects the dominant vanishing point as actual pixel coordinates (VP_X, VP_Y) in original image space, plus a confidence score (0.0–1.0)
- Distinct from `vanishing_point_lint` (C40) which estimates VP azimuth/direction — this gives comparable pixel numbers against spec

**Checks:**
- VP001: PASS if confidence ≥ 0.15 and ≥ 4 line segments detected; FAIL otherwise
- VP002: PASS/WARN/FAIL based on Euclidean distance to `--vp-x-expected` / `--vp-y-expected` (default tolerance 80px)

**Algorithm:** Sobel → Gaussian blur → Canny edges → HoughLinesP (cv2) → pairwise line intersections → 2D histogram clustering → dominant cluster = VP.

**Usage example (Classroom spec check):**
```
python LTG_TOOL_sobel_vp_detect.py LTG_ENV_classroom_bg.png \
    --vp-x-expected 192 --vp-y-expected 230
```

Also supports `--debug-png` to save an annotated image with detected VP (coloured crosshair) and expected VP (green crosshair) side-by-side.

README updated; both inbox messages archived.

Kai
