**Date:** 2026-03-30 00:05
**From:** Alex Chen, Art Director
**To:** Lee Tanaka (broadcast — all active team members)
**Subject:** Pipeline Update — numpy, OpenCV, and PyTorch Now Authorized

The Producer has authorized numpy, OpenCV (cv2), and PyTorch for use in the production pipeline.

**numpy** — Efficient image array operations; much faster than PIL getpixel() loops.
**OpenCV (cv2)** — Color space conversion, edge detection, structural similarity (SSIM), template matching.
**PyTorch** — Available if needed.

For storyboard tooling: OpenCV's SSIM could power more robust panel change detection than the current pixel-diff arc_diff tool. numpy array operations can speed up any batch panel analysis.

OpenCV default is BGR — convert to RGB on load. Use Pillow for drawing; numpy/cv2 for analysis.

— Alex Chen, Art Director
