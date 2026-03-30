# Face Landmark Detector — Validation Report

**Generated:** 2026-03-30 19:55
**Tool:** LTG_TOOL_face_landmark_detector.py v1.0.0
**Cycle:** C49
**Author:** Kai Nakamura

**Backend(s):** haar
**Reference directory:** `/home/wipkat/team/reference/drawing guides/face/`
**dlib available:** No

---

## 1. Detection Summary

| Metric | Count |
|---|---|
| Total faces detected | 39 |
| Full detection (2 eyes) | 5 |
| Five-point landmarks | 5 |
| 68-point landmarks | 0 |

## 2. Per-Image Results

| Image | Backend | Face Size | Eyes | Nose | Mouth | 68pt |
|---|---|---|---|---|---|---|
| `0e7259e1dc6b99fddedebce574829dcc.jp` | haar | 54x54 | 0 | N | N | N |
| `0e7259e1dc6b99fddedebce574829dcc.jp` | haar | 61x61 | 0 | N | N | N |
| `0e7259e1dc6b99fddedebce574829dcc.jp` | haar | 53x53 | 0 | N | N | N |
| `0e7259e1dc6b99fddedebce574829dcc.jp` | haar | 56x56 | 0 | N | N | N |
| `0e7259e1dc6b99fddedebce574829dcc.jp` | haar | 64x64 | 0 | N | N | N |
| `12e9af895b19adc6a4864818a6baaf71.jp` | haar | 45x45 | 0 | N | N | N |
| `68643b9889b5783dd8572a3adbf9bf27.jp` | haar | 131x131 | 0 | N | Y | N |
| `6c4cd96778a96c36aaad9b0f55841866.jp` | haar | 149x149 | 1 | N | Y | N |
| `6c4cd96778a96c36aaad9b0f55841866.jp` | haar | 151x151 | 2 | Y | Y | N |
| `ca1e4f8229c0d351bfddf787989e4260.jp` | haar | 141x141 | 0 | N | N | N |
| `ca1e4f8229c0d351bfddf787989e4260.jp` | haar | 129x129 | 1 | N | N | N |
| `ca1e4f8229c0d351bfddf787989e4260.jp` | haar | 132x132 | 2 | Y | Y | N |
| `ca1e4f8229c0d351bfddf787989e4260.jp` | haar | 156x156 | 1 | N | N | N |
| `ca1e4f8229c0d351bfddf787989e4260.jp` | haar | 136x136 | 2 | Y | Y | N |
| `ca1e4f8229c0d351bfddf787989e4260.jp` | haar | 125x125 | 0 | N | N | N |
| `ca1e4f8229c0d351bfddf787989e4260.jp` | haar | 147x147 | 0 | N | N | N |
| `ca1e4f8229c0d351bfddf787989e4260.jp` | haar | 140x140 | 0 | N | N | N |
| `istockphoto-984073990-612x612.jpg` | haar | 100x100 | 1 | N | N | N |
| `istockphoto-984073990-612x612.jpg` | haar | 89x89 | 0 | N | N | N |
| `kelyan-visage-expressions.jpg` | haar | 47x47 | 0 | N | N | N |
| `kelyan-visage-expressions.jpg` | haar | 51x51 | 0 | N | N | N |
| `kelyan-visage-expressions.jpg` | haar | 54x54 | 0 | N | N | N |
| `kelyan-visage-expressions.jpg` | haar | 172x172 | 1 | N | Y | N |
| `kelyan-visage-expressions.jpg` | haar | 147x147 | 2 | Y | Y | N |
| `kelyan-visage-expressions.jpg` | haar | 151x151 | 1 | N | N | N |
| `kelyan-visage-expressions.jpg` | haar | 179x179 | 0 | N | Y | N |
| `kelyan-visage-expressions.jpg` | haar | 152x152 | 0 | N | Y | N |
| `kelyan-visage-expressions.jpg` | haar | 123x123 | 2 | Y | Y | N |
| `young-boy-character-various-facial-` | haar | 48x48 | 0 | N | N | N |
| `young-boy-character-various-facial-` | haar | 51x51 | 0 | N | N | N |
| `young-boy-character-various-facial-` | haar | 51x51 | 0 | N | N | N |
| `young-boy-character-various-facial-` | haar | 49x49 | 0 | N | N | N |
| `young-boy-character-various-facial-` | haar | 49x49 | 0 | N | N | N |
| `young-boy-character-various-facial-` | haar | 48x48 | 0 | N | N | N |
| `young-boy-character-various-facial-` | haar | 49x49 | 0 | N | N | N |
| `young-boy-character-various-facial-` | haar | 46x46 | 0 | N | N | N |
| `young-boy-character-various-facial-` | haar | 52x52 | 0 | N | N | N |
| `young-boy-character-various-facial-` | haar | 51x51 | 0 | N | N | N |
| `young-boy-character-various-facial-` | haar | 49x49 | 0 | N | N | N |

## 3. Facial Ratio Statistics

*Computed from full detections (2+ eyes) only.*

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

## 4. Comparison with C48 Baseline

C48 baseline (Haar-only): 52 faces detected, 5 full detections (2+ eyes).

This run: 39 faces detected, 5 full detections, 5 five-point, 0 with 68-point landmarks.

**Parity:** Same full detection count as C48 baseline.

## 5. Recommendations

- **Install dlib** for 68-point landmark detection: `pip install dlib`
- **Download shape predictor model:** http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
- Place model at: `/home/wipkat/team/output/tools/models/shape_predictor_68_face_landmarks.dat`
- dlib is licensed under Boost Software License 1.0 (open source, compatible)

- Haar backend provides heuristic 5-point landmarks (nose + mouth estimated)
- dlib backend provides precise 68-point landmarks with sub-feature geometry
- For cartoon face calibration, dlib on photographic references would give the most accurate baseline proportions

---
*Report generated by LTG_TOOL_face_landmark_detector.py v1.0.0 — C49*
