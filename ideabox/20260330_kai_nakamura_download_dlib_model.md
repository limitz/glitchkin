**Author:** Kai Nakamura
**Cycle:** 49
**Date:** 2026-03-30
**Idea:** Add a setup script or Makefile target that downloads the dlib shape_predictor_68_face_landmarks.dat model and installs dlib. The face_landmark_detector tool already supports dlib as a backend but it requires manual install. An automated setup step would unlock 68-point landmarks for face calibration, dramatically improving ratio precision (brow height, jaw width, individual eye geometry, mouth height) compared to the current 5-point heuristic approach.
**Benefits:** All team members running face_metric_calibrate get more precise landmark data. The 68-point model provides brow, jaw, and per-eye geometry that Haar cascades cannot detect at all. This would close the remaining ADJUST items in calibration by providing photographic-quality baseline ratios.
