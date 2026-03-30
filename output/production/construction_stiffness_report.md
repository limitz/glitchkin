# Construction Stiffness Report

**Backend:** OpenCV (cv2)

| File | Outline px | Straight % | Longest Run | Stiffness | Verdict |
|------|-----------|------------|-------------|-----------|---------|
| LTG_CHAR_luma_turnaround.png | 25147 | 64.1% | 1117px | 0.4026 | FAIL |
| LTG_CHAR_cosmo_turnaround.png | 16219 | 48.2% | 91px | 0.2914 | WARN |
| LTG_CHAR_miri_turnaround.png | 20787 | 47.1% | 783px | 0.2978 | WARN |
| LTG_CHAR_byte_turnaround.png | 13888 | 65.6% | 1437px | 0.4350 | FAIL |
| LTG_CHAR_glitch_turnaround.png | 4081 | 27.2% | 36px | 0.1667 | PASS |

## Metric Definitions
- **Straight %**: Fraction of outline pixels in straight runs (min run length, max deviation threshold).
- **Longest Run**: Longest single straight segment in pixels.
- **Stiffness Score**: 0.6 * Straight% + 0.4 * (LongestRun / TotalOutline). Higher = stiffer.
- **Thresholds**: FAIL > 0.4, WARN > 0.25, PASS <= 0.25
- Organic cartoon characters should have low stiffness. Red = straight runs (bad), Green = curves (good).