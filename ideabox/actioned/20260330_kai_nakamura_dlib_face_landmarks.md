**Author:** Kai Nakamura
**Cycle:** 48
**Date:** 2026-03-30
**Idea:** Replace Haar cascade detection in face_metric_calibrate with dlib's 68-point facial landmark detector. Haar cascades only produce bounding boxes (face, eye, smile regions) and yield just 5 full detections from 52 faces in our reference set. dlib's shape predictor gives precise landmark coordinates (eye corners, nose tip, mouth corners, jawline) per face, which would let us extract inter-eye distance, eye-to-nose, nose-to-mouth, and brow height as direct point-to-point measurements instead of bounding-box approximations. dlib is open source (Boost license) and the pretrained shape predictor is freely available.
**Benefits:** Face test gate calibration team (Kai, Jordan, Lee, Maya, Rin). Higher sample counts from the same reference images would produce statistically robust PASS/WARN/FAIL boundaries, reducing the REVIEW and ADJUST verdicts that currently dominate the calibration report.
