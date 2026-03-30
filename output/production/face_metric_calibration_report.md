# Face Metric Calibration Report

**Generated:** 2026-03-30 19:55
**Tool:** LTG_TOOL_face_metric_calibrate.py
**Cycle:** C49
**Author:** Kai Nakamura

---

## 1. Reference Data Sources

- **Face references:** `/home/wipkat/team/reference/drawing guides/face` (11 loadable images)
- **Body references:** `/home/wipkat/team/reference/drawing guides/body` (6 loadable images)
- **Total faces detected:** 52
- **Full detections (2+ eyes):** 5

**Detection method:** LTG_TOOL_face_landmark_detector (haar backend)

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
| `6c4cd96778a96c36aaad9b0f55841866.jpg` | 1 | 2 | Yes | Yes |
| `6c4cd96778a96c36aaad9b0f55841866.jpg` | 1 | 1 | Yes | No |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 1 | No | No |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 2 | Yes | Yes |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 2 | Yes | Yes |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 0 | No | No |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 0 | No | No |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 1 | No | No |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 0 | No | No |
| `ca1e4f8229c0d351bfddf787989e4260.jpg` | 1 | 0 | No | No |
| `istockphoto-984073990-612x612.jpg` | 1 | 1 | No | No |
| `istockphoto-984073990-612x612.jpg` | 1 | 0 | No | No |
| `kelyan-visage-expressions.jpg` | 1 | 0 | No | No |
| `kelyan-visage-expressions.jpg` | 1 | 0 | No | No |
| `kelyan-visage-expressions.jpg` | 1 | 0 | No | No |
| `kelyan-visage-expressions.jpg` | 1 | 2 | Yes | Yes |
| `kelyan-visage-expressions.jpg` | 1 | 2 | Yes | Yes |
| `kelyan-visage-expressions.jpg` | 1 | 1 | No | No |
| `kelyan-visage-expressions.jpg` | 1 | 0 | Yes | No |
| `kelyan-visage-expressions.jpg` | 1 | 0 | Yes | No |
| `kelyan-visage-expressions.jpg` | 1 | 1 | Yes | No |
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
| `irsorvbnrurc1.jpeg` | 1 | 0 | No | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | Yes | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | No | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | No | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | Yes | No |
| `irsorvbnrurc1.jpeg` | 1 | 0 | No | No |

## 3. Measured Ratio Statistics

| Ratio | Mean | Median | Std | Min | Max | N |
|---|---|---|---|---|---|---|
| `eye_r_frac` | 0.2629 | 0.2433 | 0.0532 | 0.2031 | 0.3435 | 5 |
| `eye_size_to_face_w` | 0.2629 | 0.2433 | 0.0532 | 0.2031 | 0.3435 | 5 |
| `eye_to_mouth_frac` | 0.7577 | 0.7600 | 0.0047 | 0.7483 | 0.7600 | 5 |
| `eye_to_nose_frac` | 0.4400 | 0.4400 | 0.0000 | 0.4400 | 0.4400 | 5 |
| `eye_y_frac` | -0.2770 | -0.2831 | 0.0198 | -0.2992 | -0.2449 | 5 |
| `inter_eye_distance` | 0.4045 | 0.3743 | 0.0819 | 0.3125 | 0.5285 | 5 |
| `mouth_w_to_face_w` | 0.3783 | 0.3278 | 0.0924 | 0.2812 | 0.5034 | 5 |
| `mouth_y_frac` | 0.4807 | 0.4769 | 0.0162 | 0.4608 | 0.5034 | 5 |
| `nose_to_mouth_frac` | 0.3177 | 0.3200 | 0.0047 | 0.3083 | 0.3200 | 5 |
| `nose_y_frac` | 0.1630 | 0.1569 | 0.0198 | 0.1408 | 0.1951 | 5 |

## 4. Threshold Comparison

Status key: **CALIBRATED** = within expected range, **REVIEW** = moderate deviation,
**ADJUST** = significant deviation — threshold update recommended.

### Inter-Eye Distance (frac of face width)

- **Status:** CALIBRATED (PASS)
- **Current threshold:** 0.38
- **Reference median:** 0.3743
- **Reference range:** 0.313 – 0.528
- **Deviation:** 1.5%
- **Samples:** 5
- **Note:** Reference median (0.374) is close to current threshold (0.380).

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
- **Reference median:** 0.2433
- **Reference range:** 0.203 – 0.343
- **Deviation:** 80.0%
- **Samples:** 5
- **Note:** 20% of reference eyes fall within current PASS range. Reference cartoon eyes tend to be stylistically larger than realistic proportions.

### Mouth Y Position (frac of head_r from center)

- **Status:** REVIEW (WARN)
- **Current threshold:** 0.38
- **Reference median:** 0.4769
- **Reference range:** 0.461 – 0.503
- **Deviation:** 25.5%
- **Samples:** 5
- **Note:** Reference mouth at 0.477 of head_r from center (current: 0.380). Positive = below center.

### Eye-to-Mouth Span (frac of head_r)

- **Status:** ADJUST (FAIL)
- **Current threshold:** 0.53
- **Reference median:** 0.7600
- **Reference range:** 0.748 – 0.760
- **Deviation:** 43.4%
- **Samples:** 5
- **Note:** Derived from eye_y_frac (-0.15) and mouth_y_frac (0.38).

### Eye-to-Nose Span (frac of head_r)

- **Status:** ADJUST (FAIL)
- **Current threshold:** 0.265
- **Reference median:** 0.4400
- **Reference range:** 0.440 – 0.440
- **Deviation:** 66.0%
- **Samples:** 5
- **Note:** Estimated from landmark detection. Nose cascades NOT available — using eye-mouth midpoint estimate.

### Nose-to-Mouth Span (frac of head_r)

- **Status:** CALIBRATED (PASS)
- **Current threshold:** 0.265
- **Reference median:** 0.3200
- **Reference range:** 0.308 – 0.320
- **Deviation:** 20.8%
- **Samples:** 5
- **Note:** Estimated from landmark detection. Nose cascades NOT available — using eye-mouth midpoint estimate.

## 5. Calibration Recommendations

**4 parameter(s) flagged for adjustment:**

- **Eye Y Position (frac of head_r from center)**: current=-0.15, recommended=-0.2831 (median of 5 samples)
- **Eye Radius (frac of head_r)**: current=0.130 – 0.217 (PASS range), recommended=0.2433 (median of 5 samples)
- **Eye-to-Mouth Span (frac of head_r)**: current=0.53, recommended=0.7600 (median of 5 samples)
- **Eye-to-Nose Span (frac of head_r)**: current=0.265, recommended=0.4400 (median of 5 samples)

**Action:** Update `LTG_TOOL_character_face_test.py` variant definitions to use
the recommended values above. Re-run face test gate on all character assets after update.

2 CALIBRATED / 1 REVIEW / 4 ADJUST

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
*Report generated by LTG_TOOL_face_metric_calibrate.py — C49*
