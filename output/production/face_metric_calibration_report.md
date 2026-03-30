# Face Metric Calibration Report

**Generated:** 2026-03-30 15:12
**Tool:** LTG_TOOL_face_metric_calibrate.py
**Cycle:** C46
**Author:** Kai Nakamura

---

## 1. Reference Data Sources

- **Face references:** `/home/wipkat/team/reference/drawing guides/face` (11 loadable images)
- **Body references:** `/home/wipkat/team/reference/drawing guides/body` (6 loadable images)
- **Total faces detected:** 52
- **Full detections (2+ eyes):** 5

**Detection method:** OpenCV Haar cascades (frontalface_alt2, eye, smile)

**Note:** Reference images are cartoon/illustration expression sheets and proportion
guides — not photographic portraits. Haar cascades are trained on real faces, so
detection rates on stylized art will be lower than on photos. Detected faces represent
the subset of reference art that is close enough to photorealistic proportions for
cascade detection to trigger. This is expected and acceptable — our face test gate
targets cartoon art that must still read as *faces* to human viewers, and cascade-
detectable faces are a reasonable proxy for that readability threshold.

## 2. Per-Image Detection Summary

| Image | Faces | Eyes | Mouth | Full Detection |
|---|---|---|---|---|
| `0e7259e1dc6b99fddedebce574829dcc.jpg` | 1 | 0 | No | No |
| `0e7259e1dc6b99fddedebce574829dcc.jpg` | 1 | 0 | No | No |
| `0e7259e1dc6b99fddedebce574829dcc.jpg` | 1 | 0 | No | No |
| `0e7259e1dc6b99fddedebce574829dcc.jpg` | 1 | 0 | No | No |
| `0e7259e1dc6b99fddedebce574829dcc.jpg` | 1 | 0 | No | No |
| `12e9af895b19adc6a4864818a6baaf71.jpg` | 1 | 0 | No | No |
| `68643b9889b5783dd8572a3adbf9bf27.jpg` | 1 | 0 | Yes | No |
| `6c4cd96778a96c36aaad9b0f55841866.jpg` | 1 | 1 | Yes | No |
| `6c4cd96778a96c36aaad9b0f55841866.jpg` | 1 | 2 | No | Yes |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 1 | No | No |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 2 | No | Yes |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 2 | No | Yes |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 0 | No | No |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 0 | No | No |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 1 | No | No |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 0 | No | No |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 0 | No | No |
| `istockphoto-984073990-612x612.jpg` | 1 | 0 | No | No |
| `istockphoto-984073990-612x612.jpg` | 1 | 1 | No | No |
| `kelyan-visage-expressions.jpg` | 1 | 0 | No | No |
| `kelyan-visage-expressions.jpg` | 1 | 0 | No | No |
| `kelyan-visage-expressions.jpg` | 1 | 0 | No | No |
| `kelyan-visage-expressions.jpg` | 1 | 1 | No | No |
| `kelyan-visage-expressions.jpg` | 1 | 2 | No | Yes |
| `kelyan-visage-expressions.jpg` | 1 | 1 | Yes | No |
| `kelyan-visage-expressions.jpg` | 1 | 0 | Yes | No |
| `kelyan-visage-expressions.jpg` | 1 | 0 | Yes | No |
| `kelyan-visage-expressions.jpg` | 1 | 2 | Yes | Yes |
| `young-boy-character-various-facial-260nw` | 1 | 0 | No | No |
| `young-boy-character-various-facial-260nw` | 1 | 0 | No | No |
| `young-boy-character-various-facial-260nw` | 1 | 0 | No | No |
| `young-boy-character-various-facial-260nw` | 1 | 0 | No | No |
| `young-boy-character-various-facial-260nw` | 1 | 0 | No | No |
| `young-boy-character-various-facial-260nw` | 1 | 0 | No | No |
| `young-boy-character-various-facial-260nw` | 1 | 0 | No | No |
| `young-boy-character-various-facial-260nw` | 1 | 0 | No | No |
| `young-boy-character-various-facial-260nw` | 1 | 0 | No | No |
| `young-boy-character-various-facial-260nw` | 1 | 0 | No | No |
| `young-boy-character-various-facial-260nw` | 1 | 0 | No | No |
| `2-1.webp` | 1 | 0 | No | No |
| `3-adult-vs-child.jpg` | 1 | 0 | No | No |
| `360_F_520729056_38ryw39QuWLchsnLPU8TVEf5` | 1 | 0 | No | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | No | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | No | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | No | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | No | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | Yes | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | No | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | Yes | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | No | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | No | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | No | No |

## 3. Measured Ratio Statistics

| Ratio | Mean | Median | Std | Min | Max | N |
|---|---|---|---|---|---|---|
| `eye_r_frac` | 0.2804 | 0.2517 | 0.0621 | 0.2169 | 0.3605 | 5 |
| `eye_size_to_face_w` | 0.2804 | 0.2517 | 0.0621 | 0.2169 | 0.3605 | 5 |
| `eye_to_mouth_frac` | 0.7483 | 0.7483 | 0.0000 | 0.7483 | 0.7483 | 1 |
| `eye_to_nose_frac` | 0.3741 | 0.3741 | 0.0000 | 0.3741 | 0.3741 | 1 |
| `eye_y_frac` | -0.2770 | -0.2831 | 0.0198 | -0.2992 | -0.2449 | 5 |
| `inter_eye_distance` | 0.4023 | 0.3642 | 0.0827 | 0.3125 | 0.5285 | 5 |
| `mouth_w_to_face_w` | 0.5034 | 0.5034 | 0.0000 | 0.5034 | 0.5034 | 1 |
| `mouth_y_frac` | 0.5034 | 0.5034 | 0.0000 | 0.5034 | 0.5034 | 1 |
| `nose_to_mouth_frac` | 0.3741 | 0.3741 | 0.0000 | 0.3741 | 0.3741 | 1 |
| `nose_y_frac_est` | 0.1293 | 0.1293 | 0.0000 | 0.1293 | 0.1293 | 1 |

## 4. Threshold Comparison

Status key: **CALIBRATED** = within expected range, **REVIEW** = moderate deviation,
**ADJUST** = significant deviation — threshold update recommended.

### Inter-Eye Distance (frac of face width)

- **Status:** CALIBRATED (PASS)
- **Current threshold:** 0.38
- **Reference median:** 0.3642
- **Reference range:** 0.312 – 0.528
- **Deviation:** 4.1%
- **Samples:** 5
- **Note:** Reference median (0.364) is close to current threshold (0.380).

### Eye Y Position (frac of head_r from center)

- **Status:** ADJUST (FAIL)
- **Current threshold:** -0.15
- **Reference median:** -0.2831
- **Reference range:** -0.299 – -0.245
- **Deviation:** 88.7%
- **Samples:** 5
- **Note:** Reference eyes sit at -0.283 of head_r from center (current: -0.150). Negative values = above center. Cartoon faces often place eyes higher than realistic anatomy.

### Eye Radius (frac of head_r)

- **Status:** ADJUST (FAIL)
- **Current threshold:** 0.130 – 0.217 (PASS range)
- **Reference median:** 0.2517
- **Reference range:** 0.217 – 0.361
- **Deviation:** 80.0%
- **Samples:** 5
- **Note:** 20% of reference eyes fall within current PASS range. Reference cartoon eyes tend to be stylistically larger than realistic proportions.

### Mouth Y Position (frac of head_r from center)

- **Status:** REVIEW (WARN)
- **Current threshold:** 0.38
- **Reference median:** 0.5034
- **Reference range:** 0.503 – 0.503
- **Deviation:** 32.5%
- **Samples:** 1
- **Note:** Reference mouth at 0.503 of head_r from center (current: 0.380). Positive = below center.

### Eye-to-Mouth Span (frac of head_r)

- **Status:** ADJUST (FAIL)
- **Current threshold:** 0.53
- **Reference median:** 0.7483
- **Reference range:** 0.748 – 0.748
- **Deviation:** 41.2%
- **Samples:** 1
- **Note:** Derived from eye_y_frac (-0.15) and mouth_y_frac (0.38).

### Eye-to-Nose Span (frac of head_r)

- **Status:** REVIEW (WARN)
- **Current threshold:** 0.265
- **Reference median:** 0.3741
- **Reference range:** 0.374 – 0.374
- **Deviation:** 41.2%
- **Samples:** 1
- **Note:** Estimated from landmark detection. Nose cascades NOT available — using eye-mouth midpoint estimate.

### Nose-to-Mouth Span (frac of head_r)

- **Status:** REVIEW (WARN)
- **Current threshold:** 0.265
- **Reference median:** 0.3741
- **Reference range:** 0.374 – 0.374
- **Deviation:** 41.2%
- **Samples:** 1
- **Note:** Estimated from landmark detection. Nose cascades NOT available — using eye-mouth midpoint estimate.

## 5. Calibration Recommendations

**3 parameter(s) flagged for adjustment:**

- **Eye Y Position (frac of head_r from center)**: current=-0.15, recommended=-0.2831 (median of 5 samples)
- **Eye Radius (frac of head_r)**: current=0.130 – 0.217 (PASS range), recommended=0.2517 (median of 5 samples)
- **Eye-to-Mouth Span (frac of head_r)**: current=0.53, recommended=0.7483 (median of 1 samples)

**Action:** Update `LTG_TOOL_character_face_test.py` variant definitions to use
the recommended values above. Re-run face test gate on all character assets after update.

1 CALIBRATED / 3 REVIEW / 3 ADJUST

## 6. Methodology Notes

- **Detection:** OpenCV Haar cascades (frontalface_alt2 for face, eye for eyes, smile for mouth)
- **Coordinate system:** All ratios expressed as fractions of face_r (half face height) or
  face width, matching the convention in `LTG_TOOL_character_face_test.py`
- **Limitations:**
  - Haar cascades are trained on real photographs; cartoon face detection is partial
  - AVIF format images cannot be loaded (PIL limitation on this system)
  - Expression sheets contain many small faces — only those large enough for cascade
    detection contribute to the statistics
  - Nose cascade (haarcascade_mcs_nose.xml) may not be available; nose position
    is then estimated as eye-mouth midpoint
- **Cartoon adjustment factor:** Cartoon faces intentionally deviate from photorealistic
  proportions (larger eyes, wider spacing, higher eye line). A deviation of 15-30%
  from realistic anatomy is expected and desirable for the LTG art style.

---
*Report generated by LTG_TOOL_face_metric_calibrate.py — C46*
