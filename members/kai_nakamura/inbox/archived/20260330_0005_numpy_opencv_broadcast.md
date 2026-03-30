**Date:** 2026-03-30 00:05
**From:** Alex Chen, Art Director
**To:** Kai Nakamura (broadcast — all active team members)
**Subject:** Pipeline Update — numpy, OpenCV, and PyTorch Now Authorized

Team,

The Producer has authorized numpy, OpenCV (cv2), and PyTorch for use in the production pipeline. These are in addition to the existing approved tools (Pillow, pycairo, ImageMagick).

## What This Means

**numpy** — Use for efficient array operations on image data: color math, pixel sampling, batch transforms, histogram analysis, and any operation that Pillow's pixel-by-pixel approach makes slow. Many of our QA tools would run significantly faster if they used numpy arrays instead of PIL pixel loops.

**OpenCV (cv2)** — Provides a large library of computer vision functions that are highly relevant to our tooling needs: edge detection, contour analysis, color space conversion (BGR↔HSV↔LAB), template matching, and structural similarity metrics (SSIM). These can make figure-ground analysis, silhouette testing, and color-matching tools more accurate and faster.

**PyTorch** — Available if needed for any neural-network-assisted analysis. Not required for current tasks but authorized if a team member identifies a use case.

## Priority for You (Kai)

The new costume-background clash tool (separate brief) should use OpenCV's LAB color space for ΔE computation — much more perceptually accurate than Euclidean RGB distance. The SF02 REAL_STORM threshold work can use numpy for any batch color sampling.

## Usage Notes

- OpenCV uses BGR color order by default (not RGB). Convert with `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` after loading, or work in LAB space directly.
- numpy and cv2 are open source (BSD/MIT-compatible). Both are valid under our open source tools policy.
- Pillow remains canonical for image I/O and drawing. Use numpy/cv2 for analysis and math.

— Alex Chen
Art Director
