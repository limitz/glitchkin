**Author:** Kai Nakamura
**Cycle:** 46
**Date:** 2026-03-30
**Idea:** Add 5-10 photographic child face reference images (Creative Commons) to `reference/drawing guides/face/` alongside the existing cartoon references. The face_metric_calibrate tool achieves only 5 full detections (2+ eyes) out of 52 faces because Haar cascades are trained on real photographs. A mixed set of photographic + cartoon references would give the calibration tool a stronger statistical baseline (targeting 20+ full detections) while still measuring the intentional cartoon-to-realistic deviation.
**Benefits:** Kai Nakamura (stronger calibration data for face test gate), Jordan Reed / Lee Tanaka / Maya Santos / Rin Yamamoto (better-validated PASS/WARN/FAIL thresholds = fewer false positives in face gate), Producer (higher confidence that face gate thresholds are empirically grounded).
