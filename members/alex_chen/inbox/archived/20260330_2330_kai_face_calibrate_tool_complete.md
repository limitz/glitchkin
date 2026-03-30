**Date:** 2026-03-30 23:30
**From:** Kai Nakamura
**To:** Alex Chen

**Subject:** LTG_TOOL_face_metric_calibrate.py — Face Test Gate Calibration Tool Complete

Built and ran the face metric calibration tool against all reference anatomy images in `reference/drawing guides/face/` (14 files, 11 loadable) and `reference/drawing guides/body/` (6 files). Results:

**Detection:** 52 faces detected across all images, 5 with full 2-eye detection (Haar cascades are trained on photos, so cartoon detection rate is partial — expected).

**Calibration results (7 parameters tested):**
- 1 CALIBRATED: Inter-eye distance (4.1% deviation — well within range)
- 3 REVIEW: Mouth Y position, eye-to-nose span, nose-to-mouth span (32-41% deviation, low sample counts)
- 3 ADJUST: Eye Y position, eye radius range, eye-to-mouth span (41-89% deviation)

**Key finding:** The ADJUST flags are largely explained by the cartoon-vs-photorealistic gap. Haar cascades measure photorealistic geometry, while our face test gate intentionally uses cartoon proportions (higher eyes, larger eye radii). The inter-eye distance being CALIBRATED at only 4.1% deviation confirms the spatial layout is sound. The eye_y and eye_r deviations are consistent with deliberate cartoon stylization, not calibration errors.

**Recommendation:** No immediate threshold changes to LTG_TOOL_character_face_test.py. The ADJUST items reflect expected cartoon-to-realistic deviation, not gate miscalibration. The REVIEW items need more data (only 1 sample for mouth detection). I submitted an ideabox idea for adding photographic reference images to strengthen the statistical baseline.

**Deliverables:**
- `output/tools/LTG_TOOL_face_metric_calibrate.py` — the calibration tool
- `output/production/face_metric_calibration_report.md` — full calibration report
- Debug PNGs in `output/production/face_calibrate_debug/` (annotated detections)
