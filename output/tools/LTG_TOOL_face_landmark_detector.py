#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_face_landmark_detector.py — v1.0.0
Face Landmark Detection Tool — Multi-Backend

Detects faces and extracts facial landmarks using the best available backend:
  1. dlib 68-point shape predictor (most precise — requires dlib + shape_predictor_68_face_landmarks.dat)
  2. OpenCV Haar cascade + heuristic landmark estimation (fallback — always available)

The tool provides a unified FaceLandmarks dataclass regardless of backend, containing:
  - 5 key points: left_eye, right_eye, nose_tip, mouth_left, mouth_right
  - 68-point landmarks (dlib only; None for Haar backend)
  - Computed facial proportion ratios matching face_metric_calibrate conventions

Designed to be imported by LTG_TOOL_face_metric_calibrate.py for improved calibration.

Dependencies: PIL/Pillow, OpenCV (cv2), numpy
Optional: dlib (pip install dlib) + shape_predictor_68_face_landmarks.dat

Usage:
  python3 LTG_TOOL_face_landmark_detector.py [image_path_or_dir] [options]

  --backend    BACKEND  Force backend: "dlib", "haar", or "auto" (default: auto)
  --model-path PATH     Path to dlib shape_predictor_68_face_landmarks.dat
  --debug               Save annotated debug images
  --output     PATH     Output report path

API:
  detect_landmarks(filepath, backend="auto") -> list[FaceLandmarks]
  get_backend_name() -> str
  get_available_backends() -> list[str]

Author: Kai Nakamura — Technical Art Engineer
Cycle: 49 (created)
"""

import os
import sys
import argparse
import math
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

import numpy as np
import cv2

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow required. pip install Pillow")
    sys.exit(1)

# ── Optional dlib import ───────────────────────────────────────────────────
_DLIB_AVAILABLE = False
_dlib = None
try:
    import dlib as _dlib
    _DLIB_AVAILABLE = True
except ImportError:
    pass

# ── Version ────────────────────────────────────────────────────────────────
__version__ = "1.0.0"

# ── Project path resolution ───────────────────────────────────────────────
def _find_project_root():
    """Walk upward from this file to find CLAUDE.md sentinel."""
    d = Path(__file__).resolve().parent
    for _ in range(10):
        if (d / "CLAUDE.md").exists():
            return d
        d = d.parent
    return Path(__file__).resolve().parent.parent.parent


PROJECT_ROOT = _find_project_root()

# Default path for dlib shape predictor model
DEFAULT_MODEL_PATH = str(PROJECT_ROOT / "output" / "tools" / "models" /
                         "shape_predictor_68_face_landmarks.dat")

# ── Supported image formats ───────────────────────────────────────────────
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


# ── Data structures ──────────────────────────────────────────────────────

@dataclass
class LandmarkPoint:
    """A single 2D landmark point in image coordinates."""
    x: float
    y: float

    def as_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


@dataclass
class FaceLandmarks:
    """Detected face with landmarks and computed ratios.

    Attributes:
        filepath: Source image path.
        face_bbox: (x, y, w, h) face bounding box in image coords.
        backend: Which backend produced this detection ("dlib" or "haar").
        left_eye: Center of left eye (viewer's left).
        right_eye: Center of right eye (viewer's right).
        nose_tip: Tip of nose (or estimated position).
        mouth_left: Left corner of mouth (or estimated).
        mouth_right: Right corner of mouth (or estimated).
        landmarks_68: Full 68-point landmark array if available (dlib only).
        confidence: Detection confidence score (0-1, or None).
        ratios: Computed facial proportion ratios.
    """
    filepath: str
    face_bbox: Tuple[int, int, int, int]
    backend: str
    left_eye: Optional[LandmarkPoint] = None
    right_eye: Optional[LandmarkPoint] = None
    nose_tip: Optional[LandmarkPoint] = None
    mouth_left: Optional[LandmarkPoint] = None
    mouth_right: Optional[LandmarkPoint] = None
    landmarks_68: Optional[np.ndarray] = None
    confidence: Optional[float] = None
    ratios: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        self._compute_ratios()

    @property
    def filename(self) -> str:
        return os.path.basename(self.filepath)

    @property
    def fx(self) -> int:
        return self.face_bbox[0]

    @property
    def fy(self) -> int:
        return self.face_bbox[1]

    @property
    def fw(self) -> int:
        return self.face_bbox[2]

    @property
    def fh(self) -> int:
        return self.face_bbox[3]

    def has_full_detection(self) -> bool:
        """True if both eyes detected."""
        return self.left_eye is not None and self.right_eye is not None

    def has_five_point(self) -> bool:
        """True if all 5 key landmarks detected."""
        return all([self.left_eye, self.right_eye, self.nose_tip,
                    self.mouth_left, self.mouth_right])

    def _compute_ratios(self):
        """Compute facial proportion ratios matching face_metric_calibrate conventions."""
        fw, fh = self.fw, self.fh
        if fw < 10 or fh < 10:
            return

        face_cx = self.fx + fw / 2.0
        face_cy = self.fy + fh / 2.0
        face_r = fh / 2.0  # head_r approximation

        # Inter-eye distance
        if self.left_eye and self.right_eye:
            le = self.left_eye
            re = self.right_eye
            inter_eye = math.hypot(re.x - le.x, re.y - le.y)
            self.ratios["inter_eye_distance"] = inter_eye / fw

            # Eye Y position (average of both eyes, relative to face center)
            eye_cy_avg = (le.y + re.y) / 2.0
            self.ratios["eye_y_frac"] = (eye_cy_avg - face_cy) / face_r

            # Eye size estimate: for dlib we can compute from landmarks; for Haar
            # we estimate from inter-eye distance
            if self.landmarks_68 is not None:
                # Left eye: landmarks 36-41, right eye: 42-47
                le_pts = self.landmarks_68[36:42]
                re_pts = self.landmarks_68[42:48]
                le_w = np.max(le_pts[:, 0]) - np.min(le_pts[:, 0])
                re_w = np.max(re_pts[:, 0]) - np.min(re_pts[:, 0])
                avg_eye_w = (le_w + re_w) / 2.0
                self.ratios["eye_size_to_face_w"] = avg_eye_w / fw
                self.ratios["eye_r_frac"] = (avg_eye_w / 2.0) / face_r
            else:
                # Heuristic: eye width ~ 0.28 * inter_eye_distance for realistic faces
                est_eye_w = inter_eye * 0.65
                self.ratios["eye_size_to_face_w"] = est_eye_w / fw
                self.ratios["eye_r_frac"] = (est_eye_w / 2.0) / face_r

            # Nose position
            if self.nose_tip:
                nose_cy = self.nose_tip.y
                self.ratios["nose_y_frac"] = (nose_cy - face_cy) / face_r
                self.ratios["eye_to_nose_frac"] = abs(nose_cy - eye_cy_avg) / face_r

            # Mouth position
            if self.mouth_left and self.mouth_right:
                mouth_cx = (self.mouth_left.x + self.mouth_right.x) / 2.0
                mouth_cy = (self.mouth_left.y + self.mouth_right.y) / 2.0
                self.ratios["mouth_y_frac"] = (mouth_cy - face_cy) / face_r
                mouth_w = abs(self.mouth_right.x - self.mouth_left.x)
                self.ratios["mouth_w_to_face_w"] = mouth_w / fw

                # Eye to mouth
                eye_to_mouth = abs(mouth_cy - eye_cy_avg)
                self.ratios["eye_to_mouth_frac"] = eye_to_mouth / face_r

                # Nose to mouth
                if self.nose_tip:
                    self.ratios["nose_to_mouth_frac"] = abs(mouth_cy - self.nose_tip.y) / face_r

                # Mouth height from 68-point landmarks
                if self.landmarks_68 is not None:
                    mouth_pts = self.landmarks_68[48:68]
                    mouth_h = np.max(mouth_pts[:, 1]) - np.min(mouth_pts[:, 1])
                    self.ratios["mouth_h_to_face_w"] = mouth_h / fw

            # Brow height (dlib only — landmarks 17-26)
            if self.landmarks_68 is not None:
                brow_pts = self.landmarks_68[17:27]
                brow_cy = np.mean(brow_pts[:, 1])
                self.ratios["brow_y_frac"] = (brow_cy - face_cy) / face_r
                self.ratios["brow_to_eye_frac"] = abs(brow_cy - eye_cy_avg) / face_r

            # Jaw width (dlib only — landmarks 0-16)
            if self.landmarks_68 is not None:
                jaw_pts = self.landmarks_68[0:17]
                jaw_w = np.max(jaw_pts[:, 0]) - np.min(jaw_pts[:, 0])
                self.ratios["jaw_width_to_face_w"] = jaw_w / fw

    def summary_line(self) -> str:
        """One-line summary for report output."""
        parts = [f"  {self.filename}: face {self.fw}x{self.fh}px [{self.backend}]"]
        if self.has_five_point():
            parts.append("5-point")
        elif self.has_full_detection():
            parts.append("2-eye")
        else:
            parts.append("partial")
        if self.landmarks_68 is not None:
            parts.append("68-lm")
        if self.confidence is not None:
            parts.append(f"conf={self.confidence:.2f}")
        return ", ".join(parts)


# ── Backend: dlib 68-point ────────────────────────────────────────────────

class DlibBackend:
    """Face detection and 68-point landmark extraction using dlib."""

    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        if not _DLIB_AVAILABLE:
            raise ImportError("dlib is not installed. Install with: pip install dlib")
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"dlib shape predictor model not found at: {model_path}\n"
                f"Download from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2\n"
                f"Extract and place at: {model_path}"
            )
        self.detector = _dlib.get_frontal_face_detector()
        self.predictor = _dlib.shape_predictor(model_path)
        self.name = "dlib"

    def detect(self, filepath: str) -> List[FaceLandmarks]:
        """Detect faces and extract 68-point landmarks."""
        img = _load_image_rgb(filepath)
        if img is None:
            return []

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        faces = self.detector(gray, 1)  # upsample 1x

        results = []
        for face_rect in faces:
            x = max(0, face_rect.left())
            y = max(0, face_rect.top())
            w = face_rect.width()
            h = face_rect.height()

            # Get 68-point landmarks
            shape = self.predictor(gray, face_rect)
            landmarks = np.array([(shape.part(i).x, shape.part(i).y) for i in range(68)])

            # Extract 5 key points from 68-point landmarks
            # Left eye center: mean of points 36-41
            le_pts = landmarks[36:42]
            le_center = LandmarkPoint(float(np.mean(le_pts[:, 0])), float(np.mean(le_pts[:, 1])))

            # Right eye center: mean of points 42-47
            re_pts = landmarks[42:48]
            re_center = LandmarkPoint(float(np.mean(re_pts[:, 0])), float(np.mean(re_pts[:, 1])))

            # Nose tip: point 30
            nose_tip = LandmarkPoint(float(landmarks[30, 0]), float(landmarks[30, 1]))

            # Mouth corners: points 48 (left) and 54 (right)
            mouth_left = LandmarkPoint(float(landmarks[48, 0]), float(landmarks[48, 1]))
            mouth_right = LandmarkPoint(float(landmarks[54, 0]), float(landmarks[54, 1]))

            fl = FaceLandmarks(
                filepath=filepath,
                face_bbox=(x, y, w, h),
                backend="dlib",
                left_eye=le_center,
                right_eye=re_center,
                nose_tip=nose_tip,
                mouth_left=mouth_left,
                mouth_right=mouth_right,
                landmarks_68=landmarks,
                confidence=None,  # dlib HOG doesn't provide confidence scores
            )
            results.append(fl)

        return results


# ── Backend: Haar cascade + heuristic landmarks ─────────────────────────

class HaarBackend:
    """Face detection via Haar cascades with heuristic landmark estimation.

    Uses OpenCV Haar cascades for face and eye detection, then estimates
    nose and mouth positions from facial geometry heuristics.
    """

    def __init__(self):
        haar_dir = cv2.data.haarcascades
        self.face_cascade = self._load_cascade(haar_dir, "haarcascade_frontalface_alt2.xml")
        self.eye_cascade = self._load_cascade(haar_dir, "haarcascade_eye.xml")
        self.smile_cascade = self._load_cascade(haar_dir, "haarcascade_smile.xml")
        self.nose_cascade = self._load_cascade(haar_dir, "haarcascade_mcs_nose.xml")
        self.name = "haar"

        if self.face_cascade is None:
            raise RuntimeError("OpenCV Haar face cascade not available")

    @staticmethod
    def _load_cascade(haar_dir: str, name: str):
        path = os.path.join(haar_dir, name)
        if not os.path.exists(path):
            return None
        c = cv2.CascadeClassifier(path)
        if c.empty():
            return None
        return c

    def detect(self, filepath: str) -> List[FaceLandmarks]:
        """Detect faces and extract landmarks via Haar + heuristics."""
        img = _load_image_rgb(filepath)
        if img is None:
            return []

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )
        if len(faces) == 0:
            # Retry with more lenient params for cartoon faces
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.05, minNeighbors=2, minSize=(20, 20),
                flags=cv2.CASCADE_SCALE_IMAGE,
            )

        results = []
        for (fx, fy, fw, fh) in faces:
            roi_gray = gray[fy:fy + fh, fx:fx + fw]

            # ── Eyes ──
            left_eye = None
            right_eye = None
            if self.eye_cascade is not None:
                eye_roi = roi_gray[0:int(fh * 0.6), :]
                eyes = self.eye_cascade.detectMultiScale(
                    eye_roi, scaleFactor=1.1, minNeighbors=3,
                    minSize=(int(fw * 0.08), int(fh * 0.05)),
                )
                if len(eyes) >= 2:
                    sorted_eyes = sorted(eyes, key=lambda e: e[0])
                    le = sorted_eyes[0]
                    re = sorted_eyes[1]
                    left_eye = LandmarkPoint(
                        fx + le[0] + le[2] / 2.0,
                        fy + le[1] + le[3] / 2.0,
                    )
                    right_eye = LandmarkPoint(
                        fx + re[0] + re[2] / 2.0,
                        fy + re[1] + re[3] / 2.0,
                    )
                elif len(eyes) == 1:
                    e = eyes[0]
                    # Single eye — place at center, can't determine L/R
                    left_eye = LandmarkPoint(
                        fx + e[0] + e[2] / 2.0,
                        fy + e[1] + e[3] / 2.0,
                    )

            # ── Nose ──
            nose_tip = None
            if self.nose_cascade is not None:
                nose_roi = roi_gray[int(fh * 0.2):int(fh * 0.75),
                                    int(fw * 0.2):int(fw * 0.8)]
                noses = self.nose_cascade.detectMultiScale(
                    nose_roi, scaleFactor=1.1, minNeighbors=3,
                    minSize=(int(fw * 0.1), int(fh * 0.05)),
                )
                if len(noses) > 0:
                    nx, ny, nw, nh = max(noses, key=lambda n: n[2] * n[3])
                    nose_tip = LandmarkPoint(
                        fx + int(fw * 0.2) + nx + nw / 2.0,
                        fy + int(fh * 0.2) + ny + nh / 2.0,
                    )

            # Heuristic nose estimate if cascade missed
            if nose_tip is None and left_eye and right_eye:
                eye_cy = (left_eye.y + right_eye.y) / 2.0
                # Nose tip ~ 40% down from eye line to chin
                nose_y = eye_cy + fh * 0.22
                nose_x = (left_eye.x + right_eye.x) / 2.0
                nose_tip = LandmarkPoint(nose_x, nose_y)

            # ── Mouth ──
            mouth_left = None
            mouth_right = None
            smile_detected = False
            if self.smile_cascade is not None:
                mouth_roi = roi_gray[int(fh * 0.5):, :]
                smiles = self.smile_cascade.detectMultiScale(
                    mouth_roi, scaleFactor=1.3, minNeighbors=5,
                    minSize=(int(fw * 0.15), int(fh * 0.05)),
                )
                if len(smiles) > 0:
                    sx, sy, sw, sh = max(smiles, key=lambda s: s[2] * s[3])
                    mouth_cy = fy + int(fh * 0.5) + sy + sh / 2.0
                    mouth_cx = fx + sx + sw / 2.0
                    mouth_left = LandmarkPoint(mouth_cx - sw / 2.0, mouth_cy)
                    mouth_right = LandmarkPoint(mouth_cx + sw / 2.0, mouth_cy)
                    smile_detected = True

            # Heuristic mouth estimate if cascade missed
            if not smile_detected and left_eye and right_eye:
                eye_cy = (left_eye.y + right_eye.y) / 2.0
                inter_eye = abs(right_eye.x - left_eye.x)
                mouth_y = eye_cy + fh * 0.38
                mouth_cx = (left_eye.x + right_eye.x) / 2.0
                mouth_hw = inter_eye * 0.45  # half mouth width
                mouth_left = LandmarkPoint(mouth_cx - mouth_hw, mouth_y)
                mouth_right = LandmarkPoint(mouth_cx + mouth_hw, mouth_y)

            fl = FaceLandmarks(
                filepath=filepath,
                face_bbox=(fx, fy, fw, fh),
                backend="haar",
                left_eye=left_eye,
                right_eye=right_eye,
                nose_tip=nose_tip,
                mouth_left=mouth_left,
                mouth_right=mouth_right,
                landmarks_68=None,
                confidence=None,
            )
            results.append(fl)

        return results


# ── Image loading ────────────────────────────────────────────────────────

def _load_image_rgb(filepath: str) -> Optional[np.ndarray]:
    """Load image as RGB numpy array via PIL (wider format support)."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return None
    try:
        pil_img = Image.open(filepath)
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")
        return np.array(pil_img)
    except Exception:
        return None


# ── Public API ───────────────────────────────────────────────────────────

_backend_cache: Dict[str, Any] = {}


def get_available_backends() -> List[str]:
    """Return list of available backend names."""
    backends = ["haar"]  # always available
    if _DLIB_AVAILABLE and os.path.exists(DEFAULT_MODEL_PATH):
        backends.insert(0, "dlib")
    return backends


def get_backend_name(backend: str = "auto") -> str:
    """Return the name of the backend that would be used."""
    if backend == "auto":
        if _DLIB_AVAILABLE and os.path.exists(DEFAULT_MODEL_PATH):
            return "dlib"
        return "haar"
    return backend


def _get_backend(backend: str = "auto", model_path: str = DEFAULT_MODEL_PATH):
    """Get or create backend instance."""
    name = get_backend_name(backend)

    if name not in _backend_cache:
        if name == "dlib":
            _backend_cache[name] = DlibBackend(model_path)
        else:
            _backend_cache[name] = HaarBackend()

    return _backend_cache[name]


def detect_landmarks(filepath: str, backend: str = "auto",
                     model_path: str = DEFAULT_MODEL_PATH) -> List[FaceLandmarks]:
    """Detect faces and landmarks in an image.

    Args:
        filepath: Path to image file.
        backend: "auto" (best available), "dlib", or "haar".
        model_path: Path to dlib shape predictor model (only used for dlib backend).

    Returns:
        List of FaceLandmarks objects, one per detected face.
    """
    try:
        be = _get_backend(backend, model_path)
    except (ImportError, FileNotFoundError, RuntimeError) as e:
        if backend == "auto":
            # Fall back to haar
            be = _get_backend("haar")
        else:
            raise
    return be.detect(filepath)


def detect_landmarks_batch(filepaths: List[str], backend: str = "auto",
                           model_path: str = DEFAULT_MODEL_PATH) -> List[FaceLandmarks]:
    """Detect landmarks across multiple images.

    Returns flat list of all FaceLandmarks from all images.
    """
    all_results = []
    for fp in filepaths:
        results = detect_landmarks(fp, backend=backend, model_path=model_path)
        all_results.extend(results)
    return all_results


# ── Comparison utilities ─────────────────────────────────────────────────

def compare_backends(filepath: str, model_path: str = DEFAULT_MODEL_PATH) -> Dict[str, Any]:
    """Run both backends on the same image and compare results.

    Returns dict with per-backend results and delta analysis.
    Only meaningful if dlib is available; otherwise returns haar-only results.
    """
    haar_results = detect_landmarks(filepath, backend="haar")
    dlib_results = []
    if _DLIB_AVAILABLE and os.path.exists(model_path):
        try:
            dlib_results = detect_landmarks(filepath, backend="dlib", model_path=model_path)
        except Exception:
            pass

    comparison = {
        "filepath": filepath,
        "haar_count": len(haar_results),
        "dlib_count": len(dlib_results),
        "haar_full": sum(1 for r in haar_results if r.has_full_detection()),
        "dlib_full": sum(1 for r in dlib_results if r.has_full_detection()),
        "haar_five_point": sum(1 for r in haar_results if r.has_five_point()),
        "dlib_five_point": sum(1 for r in dlib_results if r.has_five_point()),
    }

    # Ratio deltas for matching face detections
    if haar_results and dlib_results:
        # Simple: compare first full detection from each
        haar_full = [r for r in haar_results if r.has_full_detection()]
        dlib_full = [r for r in dlib_results if r.has_full_detection()]
        if haar_full and dlib_full:
            h = haar_full[0]
            d = dlib_full[0]
            deltas = {}
            for key in set(h.ratios.keys()) & set(d.ratios.keys()):
                deltas[key] = {
                    "haar": h.ratios[key],
                    "dlib": d.ratios[key],
                    "delta": d.ratios[key] - h.ratios[key],
                    "pct_diff": abs(d.ratios[key] - h.ratios[key]) / abs(d.ratios[key]) * 100
                    if d.ratios[key] != 0 else 0,
                }
            comparison["ratio_deltas"] = deltas

    return comparison


# ── Debug visualization ──────────────────────────────────────────────────

def draw_debug_image(filepath: str, landmarks_list: List[FaceLandmarks],
                     output_path: str) -> str:
    """Draw landmarks on image and save as debug PNG.

    Respects 1280px max dimension rule.
    """
    img = _load_image_rgb(filepath)
    if img is None:
        return ""

    bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    for lm in landmarks_list:
        # Face bbox (green)
        cv2.rectangle(bgr,
                      (lm.fx, lm.fy),
                      (lm.fx + lm.fw, lm.fy + lm.fh),
                      (0, 255, 0), 2)

        # Key points
        if lm.left_eye:
            cv2.circle(bgr, (int(lm.left_eye.x), int(lm.left_eye.y)), 3, (255, 0, 0), -1)
        if lm.right_eye:
            cv2.circle(bgr, (int(lm.right_eye.x), int(lm.right_eye.y)), 3, (255, 0, 0), -1)
        if lm.nose_tip:
            cv2.circle(bgr, (int(lm.nose_tip.x), int(lm.nose_tip.y)), 3, (0, 255, 255), -1)
        if lm.mouth_left:
            cv2.circle(bgr, (int(lm.mouth_left.x), int(lm.mouth_left.y)), 3, (0, 0, 255), -1)
        if lm.mouth_right:
            cv2.circle(bgr, (int(lm.mouth_right.x), int(lm.mouth_right.y)), 3, (0, 0, 255), -1)

        # 68-point landmarks (small cyan dots)
        if lm.landmarks_68 is not None:
            for (px, py) in lm.landmarks_68:
                cv2.circle(bgr, (int(px), int(py)), 1, (255, 255, 0), -1)

        # Label
        label = f"{lm.backend}"
        if lm.has_five_point():
            label += " 5pt"
        if lm.landmarks_68 is not None:
            label += " 68lm"
        cv2.putText(bgr, label, (lm.fx, lm.fy - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    # Resize to <= 1280px
    h, w = bgr.shape[:2]
    if max(h, w) > 1280:
        scale = 1280.0 / max(h, w)
        bgr = cv2.resize(bgr, (int(w * scale), int(h * scale)),
                         interpolation=cv2.INTER_AREA)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, bgr)
    return output_path


# ── Report generation ────────────────────────────────────────────────────

def generate_validation_report(all_landmarks: List[FaceLandmarks],
                               reference_dir: str,
                               output_path: str) -> str:
    """Generate a validation report comparing landmark detection results.

    Returns path to written report.
    """
    lines = []
    lines.append("# Face Landmark Detector — Validation Report")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Tool:** LTG_TOOL_face_landmark_detector.py v{__version__}")
    lines.append(f"**Cycle:** C49")
    lines.append(f"**Author:** Kai Nakamura")
    lines.append("")

    backend_used = set(lm.backend for lm in all_landmarks) if all_landmarks else {"none"}
    lines.append(f"**Backend(s):** {', '.join(sorted(backend_used))}")
    lines.append(f"**Reference directory:** `{reference_dir}`")
    lines.append(f"**dlib available:** {'Yes' if _DLIB_AVAILABLE else 'No'}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 1: Detection summary
    lines.append("## 1. Detection Summary")
    lines.append("")
    total = len(all_landmarks)
    full = sum(1 for lm in all_landmarks if lm.has_full_detection())
    five_pt = sum(1 for lm in all_landmarks if lm.has_five_point())
    has_68 = sum(1 for lm in all_landmarks if lm.landmarks_68 is not None)
    lines.append(f"| Metric | Count |")
    lines.append(f"|---|---|")
    lines.append(f"| Total faces detected | {total} |")
    lines.append(f"| Full detection (2 eyes) | {full} |")
    lines.append(f"| Five-point landmarks | {five_pt} |")
    lines.append(f"| 68-point landmarks | {has_68} |")
    lines.append("")

    # Section 2: Per-image breakdown
    lines.append("## 2. Per-Image Results")
    lines.append("")
    lines.append("| Image | Backend | Face Size | Eyes | Nose | Mouth | 68pt |")
    lines.append("|---|---|---|---|---|---|---|")

    for lm in all_landmarks:
        eyes = "2" if lm.has_full_detection() else ("1" if lm.left_eye or lm.right_eye else "0")
        nose = "Y" if lm.nose_tip else "N"
        mouth = "Y" if (lm.mouth_left and lm.mouth_right) else "N"
        pts68 = "Y" if lm.landmarks_68 is not None else "N"
        lines.append(
            f"| `{lm.filename[:35]}` | {lm.backend} | {lm.fw}x{lm.fh} "
            f"| {eyes} | {nose} | {mouth} | {pts68} |"
        )

    if not all_landmarks:
        lines.append("| *(no faces detected)* | — | — | — | — | — | — |")
    lines.append("")

    # Section 3: Ratio statistics (full detections only)
    full_lms = [lm for lm in all_landmarks if lm.has_full_detection()]
    if full_lms:
        lines.append("## 3. Facial Ratio Statistics")
        lines.append("")
        lines.append("*Computed from full detections (2+ eyes) only.*")
        lines.append("")

        # Aggregate ratios
        ratio_data: Dict[str, list] = {}
        for lm in full_lms:
            for key, val in lm.ratios.items():
                ratio_data.setdefault(key, []).append(val)

        lines.append("| Ratio | Mean | Median | Std | Min | Max | N |")
        lines.append("|---|---|---|---|---|---|---|")
        for key in sorted(ratio_data.keys()):
            vals = np.array(ratio_data[key])
            lines.append(
                f"| `{key}` | {np.mean(vals):.4f} | {np.median(vals):.4f} | "
                f"{np.std(vals):.4f} | {np.min(vals):.4f} | {np.max(vals):.4f} | {len(vals)} |"
            )
        lines.append("")

    # Section 4: Comparison with C48 Haar-only baseline
    lines.append("## 4. Comparison with C48 Baseline")
    lines.append("")
    lines.append("C48 baseline (Haar-only): 52 faces detected, 5 full detections (2+ eyes).")
    lines.append("")
    lines.append(f"This run: {total} faces detected, {full} full detections, "
                 f"{five_pt} five-point, {has_68} with 68-point landmarks.")
    lines.append("")
    if full > 5:
        lines.append("**Improvement:** More full detections than C48 baseline.")
    elif full == 5:
        lines.append("**Parity:** Same full detection count as C48 baseline.")
    else:
        lines.append("**Regression:** Fewer full detections than C48 baseline.")
    lines.append("")

    # Section 5: Recommendations
    lines.append("## 5. Recommendations")
    lines.append("")
    if not _DLIB_AVAILABLE:
        lines.append("- **Install dlib** for 68-point landmark detection: `pip install dlib`")
        lines.append("- **Download shape predictor model:** "
                     "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
        lines.append(f"- Place model at: `{DEFAULT_MODEL_PATH}`")
        lines.append("- dlib is licensed under Boost Software License 1.0 (open source, compatible)")
        lines.append("")
    lines.append("- Haar backend provides heuristic 5-point landmarks (nose + mouth estimated)")
    lines.append("- dlib backend provides precise 68-point landmarks with sub-feature geometry")
    lines.append("- For cartoon face calibration, dlib on photographic references would give "
                 "the most accurate baseline proportions")
    lines.append("")
    lines.append("---")
    lines.append(f"*Report generated by LTG_TOOL_face_landmark_detector.py v{__version__} — C49*")
    lines.append("")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    return output_path


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Face Landmark Detection Tool — multi-backend"
    )
    parser.add_argument("path", nargs="?",
                        default=str(PROJECT_ROOT / "reference" / "drawing guides" / "face"),
                        help="Image file or directory to scan")
    parser.add_argument("--backend", default="auto", choices=["auto", "dlib", "haar"],
                        help="Detection backend (default: auto)")
    parser.add_argument("--model-path", default=DEFAULT_MODEL_PATH,
                        help="Path to dlib shape_predictor_68_face_landmarks.dat")
    parser.add_argument("--debug", action="store_true",
                        help="Save annotated debug images")
    parser.add_argument("--output", default=None,
                        help="Output report path (default: output/production/face_landmark_validation_report.md)")
    parser.add_argument("--compare", action="store_true",
                        help="Run both backends and compare (requires dlib)")

    args = parser.parse_args()

    if args.output is None:
        args.output = str(PROJECT_ROOT / "output" / "production" /
                          "face_landmark_validation_report.md")

    print(f"Face Landmark Detector v{__version__}")
    print(f"Backend: {get_backend_name(args.backend)}")
    print(f"Available backends: {', '.join(get_available_backends())}")
    print(f"dlib installed: {_DLIB_AVAILABLE}")
    print(f"Path: {args.path}")
    print()

    # Collect image paths
    if os.path.isfile(args.path):
        filepaths = [args.path]
    elif os.path.isdir(args.path):
        filepaths = sorted([
            os.path.join(args.path, f) for f in os.listdir(args.path)
            if os.path.isfile(os.path.join(args.path, f))
            and os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
        ])
    else:
        print(f"ERROR: Path not found: {args.path}")
        return 1

    print(f"Images to process: {len(filepaths)}")
    print()

    # Detect landmarks
    all_landmarks = []
    for fp in filepaths:
        results = detect_landmarks(fp, backend=args.backend, model_path=args.model_path)
        all_landmarks.extend(results)

        if args.debug and results:
            debug_dir = str(PROJECT_ROOT / "output" / "production" /
                            "face_landmark_debug")
            base = os.path.splitext(os.path.basename(fp))[0]
            debug_path = os.path.join(debug_dir, f"debug_{base}.png")
            draw_debug_image(fp, results, debug_path)

        # Print per-image summary
        if results:
            for r in results:
                print(r.summary_line())
        else:
            print(f"  {os.path.basename(fp)}: no faces detected")

    print()

    # Backend comparison if requested
    if args.compare and _DLIB_AVAILABLE:
        print("Backend comparison:")
        for fp in filepaths:
            comp = compare_backends(fp, args.model_path)
            print(f"  {os.path.basename(fp)}: haar={comp['haar_count']} "
                  f"dlib={comp['dlib_count']} "
                  f"haar_full={comp['haar_full']} dlib_full={comp['dlib_full']}")
        print()

    # Summary
    full_count = sum(1 for lm in all_landmarks if lm.has_full_detection())
    five_count = sum(1 for lm in all_landmarks if lm.has_five_point())
    lm68_count = sum(1 for lm in all_landmarks if lm.landmarks_68 is not None)
    print(f"Total faces: {len(all_landmarks)}")
    print(f"Full detections (2 eyes): {full_count}")
    print(f"Five-point landmarks: {five_count}")
    print(f"68-point landmarks: {lm68_count}")
    print()

    # Generate report
    report_path = generate_validation_report(all_landmarks, args.path, args.output)
    print(f"Report: {report_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
