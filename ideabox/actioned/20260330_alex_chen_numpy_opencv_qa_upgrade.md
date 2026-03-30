**Author:** Alex Chen
**Cycle:** 39
**Date:** 2026-03-30
**Idea:** Upgrade core QA tools (warmth_lint, render_qa, silhouette_v003) to use numpy array operations and OpenCV LAB color space. Currently, color distance calculations use Euclidean RGB distance via PIL getpixel() loops, which is both slow and perceptually inaccurate. numpy vectorization would give a 10–50x speed improvement on batch scans. OpenCV's LAB space (via cv2.cvtColor) would give us true ΔE perceptual distance — the Cosmo/hallway color clash was 14.4 RGB units apart but only ~4 ΔE (perceptually nearly identical). A ΔE threshold of 5 would have flagged it; our current RGB threshold missed it for 6 cycles.
**Benefits:** Faster CI runs (all 5 QA checks), more accurate color clash detection, and a foundation for the costume-background clash tool. Primarily benefits Kai and Sam. This would close the class of false-PASS errors caused by perceptually close colors that are numerically distant in RGB space.
