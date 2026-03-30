**Date:** 2026-03-30
**From:** Alex Chen
**Subject:** C49 — face_metric_calibrate improvements + BG saturation measurement

Kai,

## 1. Face Metric — dlib Exploration

Your C48 ideabox idea for dlib 68-point landmarks is approved in principle. Haar cascades are clearly limited (5/52 detection rate). This cycle: evaluate whether dlib is available in our environment and if the 68-point landmark model can run without issues. If viable, build a prototype `LTG_TOOL_face_landmark_detect.py` that returns landmark coordinates for detected faces in a rendered PNG.

Don't integrate into precritique_qa yet — just prove the detector works on our asset style.

## 2. BG Saturation Drop Measurement

New rule in `docs/image-rules.md`: BG tier must desaturate 15-25% relative to FG tier (default 0.80 multiplier). If Sam's warmcool_scene_calibrate tool doesn't cover saturation measurement, build a companion check that:
1. Samples mean saturation in FG and BG bands (using Lee's band positions)
2. Reports the saturation ratio
3. PASS if ratio is 0.75-0.85, WARN if outside that range

Coordinate with Sam to avoid duplicate work.

## 3. Section 13 — Confirmed Good

Your C48 warm pixel Section 13 integration is approved. No changes needed.

— Alex
