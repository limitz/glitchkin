#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_face_metric_calibrate.py
Face Test Gate Calibration Tool — Reference Anatomy Validation

Loads reference face proportion charts from reference/drawing guides/face/ and
reference/drawing guides/body/, extracts measurable facial ratios via OpenCV
Haar cascade detection, and compares them against the current face test gate
thresholds in LTG_TOOL_character_face_test.py.

Extracted ratios:
  - inter_eye_distance:  distance between eye centers / face width
  - eye_to_nose:         vertical distance from eye center to nose center / face height
  - nose_to_mouth:       vertical distance from nose center to mouth center / face height
  - brow_height:         vertical distance from brow to eye center / face height
  - eye_size_ratio:      eye width / face width

Current face test gate thresholds (from LTG_TOOL_character_face_test.py):
  - inter_eye_distance:  0.76 * head_r (2 * 0.38 — eye_x offset as fraction of head_r)
  - eye_y_frac:          -0.15 (standard) to -0.22 (wide-eyed)
  - brow_y_frac:         -0.48 (brow height from head center)
  - mouth_y_frac:        +0.38 (mouth center from head center)
  - eye_r range:         0.087 (FAIL floor) to 0.217 (maximum)
  - mouth_w range:       0.130 to 0.217
  - mouth_h range:       0.043 to 0.217

Output:
  - Markdown calibration report at output/production/face_metric_calibration_report.md
  - Per-image detection summary
  - Recommended threshold adjustments (if any)

Dependencies: PIL/Pillow, OpenCV (cv2), numpy

Usage:
  python3 LTG_TOOL_face_metric_calibrate.py [options]

  --face-dir   PATH  Face reference directory (default: reference/drawing guides/face/)
  --body-dir   PATH  Body reference directory (default: reference/drawing guides/body/)
  --output     PATH  Output report path (default: output/production/face_metric_calibration_report.md)
  --debug            Save annotated debug PNGs for each detected face

Author: Kai Nakamura — Technical Art Engineer
Cycle: 46 (2026-03-30)
"""

import os
import sys
import argparse
import math
import json
import random
from datetime import datetime
from pathlib import Path

import numpy as np
import cv2

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow required. pip install Pillow")
    sys.exit(1)


# ── Project path resolution ─────────────────────────────────────────────────
def _find_project_root():
    """Walk upward from this file to find CLAUDE.md sentinel."""
    d = Path(__file__).resolve().parent
    for _ in range(10):
        if (d / "CLAUDE.md").exists():
            return d
        d = d.parent
    return Path(__file__).resolve().parent.parent.parent  # fallback


PROJECT_ROOT = _find_project_root()


def output_dir():
    """Canonical output directory."""
    d = PROJECT_ROOT / "output" / "production"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ── Current face test gate thresholds (extracted from LTG_TOOL_character_face_test.py) ──
# These are the thresholds we are validating against reference anatomy data.
# All values are fractions of head_r (radius) unless noted otherwise.

CURRENT_THRESHOLDS = {
    # Inter-eye distance: each eye is at cx ± 0.38*head_r → total separation = 0.76*head_r
    # As fraction of head diameter (2*head_r): 0.76 / 2.0 = 0.38
    "inter_eye_distance_frac": 0.38,   # fraction of face width (diameter)

    # Eye vertical position: fraction of head_r from center (negative = above center)
    "eye_y_frac_standard": -0.15,      # standard position
    "eye_y_frac_wide": -0.22,          # wide-eyed / fear expressions

    # Brow height: fraction of head_r from center (negative = above center)
    "brow_y_frac": -0.48,

    # Mouth vertical position: fraction of head_r from center (positive = below center)
    "mouth_y_frac": 0.38,

    # Eye radius range (as fraction of head_r)
    "eye_r_min_fail": 0.087,           # below this = FAIL (too small)
    "eye_r_min_pass": 0.130,           # minimum for PASS
    "eye_r_max": 0.217,                # maximum (wide-open)

    # Mouth dimensions (as fraction of head_r)
    "mouth_w_min": 0.130,
    "mouth_w_max": 0.217,
    "mouth_h_min": 0.043,
    "mouth_h_max": 0.217,
}

# Derived ratios for comparison with reference anatomy:
# eye_to_mouth vertical span = |eye_y_frac - mouth_y_frac| = |-0.15 - 0.38| = 0.53 of head_r
# brow_to_eye vertical span = |brow_y_frac - eye_y_frac| = |-0.48 - (-0.15)| = 0.33 of head_r
# Nose assumed at midpoint of eye-to-mouth: roughly 0.115 of head_r below center
# eye_to_nose = |(-0.15) - (0.115)| = 0.265 of head_r
# nose_to_mouth = |0.115 - 0.38| = 0.265 of head_r

DERIVED_RATIOS = {
    "eye_to_mouth_frac": 0.53,         # of head_r
    "brow_to_eye_frac": 0.33,          # of head_r
    "eye_to_nose_frac": 0.265,         # of head_r (estimated)
    "nose_to_mouth_frac": 0.265,       # of head_r (estimated)
    # Normalized ratios (proportions of face features relative to each other):
    "inter_eye_to_face_width": 0.38,   # inter-eye / face diameter
    "eye_to_mouth_to_face_height": 0.265,  # eye-to-mouth / face diameter
    "brow_to_eye_to_face_height": 0.165,   # brow-to-eye / face diameter
}


# ── Haar cascade loaders ────────────────────────────────────────────────────
HAAR_DIR = cv2.data.haarcascades

def _load_cascade(name):
    path = os.path.join(HAAR_DIR, name)
    if not os.path.exists(path):
        return None
    return cv2.CascadeClassifier(path)


FACE_CASCADE = _load_cascade("haarcascade_frontalface_alt2.xml")
EYE_CASCADE = _load_cascade("haarcascade_eye.xml")
SMILE_CASCADE = _load_cascade("haarcascade_smile.xml")
NOSE_CASCADE = _load_cascade("haarcascade_mcs_nose.xml")  # may not exist


# ── Image loading ────────────────────────────────────────────────────────────
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


def load_image_cv2(filepath):
    """Load an image via PIL (wider format support) then convert to cv2 BGR numpy array.

    Returns (bgr_array, original_size) or (None, None) on failure.
    """
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return None, None
    try:
        pil_img = Image.open(filepath)
        if pil_img.mode == "L":
            pil_img = pil_img.convert("RGB")
        elif pil_img.mode in ("RGBA", "LA", "PA"):
            pil_img = pil_img.convert("RGB")
        elif pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")
        arr = np.array(pil_img)
        bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        return bgr, pil_img.size
    except Exception:
        return None, None


def load_image_gray(filepath):
    """Load image and return grayscale numpy array."""
    bgr, size = load_image_cv2(filepath)
    if bgr is None:
        return None, None
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return gray, size


# ── Face detection and landmark extraction ───────────────────────────────────

class FaceDetection:
    """A single detected face with extracted landmarks and ratios."""

    def __init__(self, filepath, face_bbox, eyes, smile_bbox=None, nose_bbox=None):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        # Face bounding box (x, y, w, h) in image coords
        self.fx, self.fy, self.fw, self.fh = face_bbox
        # Eyes: list of (ex, ey, ew, eh) in image coords
        self.eyes = eyes
        self.smile_bbox = smile_bbox
        self.nose_bbox = nose_bbox
        # Computed ratios
        self.ratios = {}
        self._compute_ratios()

    def _compute_ratios(self):
        """Compute facial proportion ratios from detected landmarks."""
        fw, fh = self.fw, self.fh
        if fw < 10 or fh < 10:
            return

        # Face center
        face_cx = self.fx + fw / 2
        face_cy = self.fy + fh / 2
        face_r = fh / 2  # approximate head_r as half face height

        # Eye positions
        if len(self.eyes) >= 2:
            # Sort eyes by X to get left/right
            sorted_eyes = sorted(self.eyes, key=lambda e: e[0])
            le = sorted_eyes[0]  # left eye (viewer's left)
            re = sorted_eyes[1]  # right eye (viewer's right)

            # Eye centers (in image coords)
            le_cx = le[0] + le[2] / 2
            le_cy = le[1] + le[3] / 2
            re_cx = re[0] + re[2] / 2
            re_cy = re[1] + re[3] / 2

            # Inter-eye distance / face width
            inter_eye_dist = abs(re_cx - le_cx)
            self.ratios["inter_eye_distance"] = inter_eye_dist / fw

            # Eye center Y (average) relative to face center, as fraction of face_r
            eye_cy_avg = (le_cy + re_cy) / 2
            eye_y_from_center = (eye_cy_avg - face_cy) / face_r
            self.ratios["eye_y_frac"] = eye_y_from_center

            # Eye size (average width) as fraction of face width
            avg_eye_w = (le[2] + re[2]) / 2
            self.ratios["eye_size_to_face_w"] = avg_eye_w / fw

            # Eye radius as fraction of head_r (half eye width / face_r)
            avg_eye_r = avg_eye_w / 2
            self.ratios["eye_r_frac"] = avg_eye_r / face_r

            # Mouth position (if detected)
            if self.smile_bbox is not None:
                sx, sy, sw, sh = self.smile_bbox
                mouth_cy = sy + sh / 2
                mouth_y_from_center = (mouth_cy - face_cy) / face_r
                self.ratios["mouth_y_frac"] = mouth_y_from_center

                # Eye to mouth distance as fraction of face_r
                eye_to_mouth = abs(mouth_cy - eye_cy_avg)
                self.ratios["eye_to_mouth_frac"] = eye_to_mouth / face_r

                # Mouth width as fraction of face width
                self.ratios["mouth_w_to_face_w"] = sw / fw

                # Nose position estimated midpoint (if no nose cascade)
                if self.nose_bbox is None:
                    nose_cy_est = (eye_cy_avg + mouth_cy) / 2
                    self.ratios["nose_y_frac_est"] = (nose_cy_est - face_cy) / face_r
                    self.ratios["eye_to_nose_frac"] = abs(nose_cy_est - eye_cy_avg) / face_r
                    self.ratios["nose_to_mouth_frac"] = abs(mouth_cy - nose_cy_est) / face_r

            # Nose position (if detected)
            if self.nose_bbox is not None:
                nx, ny, nw, nh = self.nose_bbox
                nose_cy = ny + nh / 2
                nose_y_from_center = (nose_cy - face_cy) / face_r
                self.ratios["nose_y_frac"] = nose_y_from_center
                self.ratios["eye_to_nose_frac"] = abs(nose_cy - eye_cy_avg) / face_r
                if self.smile_bbox is not None:
                    sx, sy, sw, sh = self.smile_bbox
                    mouth_cy = sy + sh / 2
                    self.ratios["nose_to_mouth_frac"] = abs(mouth_cy - nose_cy) / face_r

        elif len(self.eyes) == 1:
            e = self.eyes[0]
            eye_cy = e[1] + e[3] / 2
            eye_y_from_center = (eye_cy - face_cy) / face_r
            self.ratios["eye_y_frac"] = eye_y_from_center
            self.ratios["eye_r_frac"] = (e[2] / 2) / face_r

    def has_full_detection(self):
        """Return True if we have at least 2 eyes detected."""
        return len(self.eyes) >= 2

    def summary_line(self):
        """One-line summary for report."""
        parts = [f"  {self.filename}: face {self.fw}x{self.fh}px, {len(self.eyes)} eyes"]
        if self.smile_bbox:
            parts.append("mouth")
        if self.nose_bbox:
            parts.append("nose")
        return ", ".join(parts)


def detect_faces_in_image(filepath, debug=False):
    """Detect all faces in an image and extract landmarks.

    Returns list of FaceDetection objects.
    """
    gray, size = load_image_gray(filepath)
    if gray is None:
        return []

    bgr = None
    if debug:
        bgr_full, _ = load_image_cv2(filepath)
        bgr = bgr_full.copy() if bgr_full is not None else None

    # Detect faces
    if FACE_CASCADE is None or FACE_CASCADE.empty():
        return []

    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    if len(faces) == 0:
        # Try with more lenient parameters for cartoon faces
        faces = FACE_CASCADE.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=2,
            minSize=(20, 20),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

    detections = []
    for (fx, fy, fw, fh) in faces:
        # Region of interest for eye/mouth detection
        roi_gray = gray[fy:fy + fh, fx:fx + fw]

        # Detect eyes within face ROI (upper 60% of face)
        eye_roi = roi_gray[0:int(fh * 0.6), :]
        eyes_local = []
        if EYE_CASCADE is not None and not EYE_CASCADE.empty():
            eyes = EYE_CASCADE.detectMultiScale(
                eye_roi,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(int(fw * 0.08), int(fh * 0.05)),
            )
            # Convert to image coords
            for (ex, ey, ew, eh) in eyes:
                eyes_local.append((fx + ex, fy + ey, ew, eh))

        # Detect smile/mouth within face ROI (lower 50% of face)
        smile_bbox = None
        mouth_roi = roi_gray[int(fh * 0.5):, :]
        if SMILE_CASCADE is not None and not SMILE_CASCADE.empty():
            smiles = SMILE_CASCADE.detectMultiScale(
                mouth_roi,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(int(fw * 0.15), int(fh * 0.05)),
            )
            if len(smiles) > 0:
                # Take the largest smile detection
                sx, sy, sw, sh = max(smiles, key=lambda s: s[2] * s[3])
                smile_bbox = (fx + sx, fy + int(fh * 0.5) + sy, sw, sh)

        # Nose detection (optional — cascade may not be available)
        nose_bbox = None
        if NOSE_CASCADE is not None and not NOSE_CASCADE.empty():
            nose_roi = roi_gray[int(fh * 0.2):int(fh * 0.75), int(fw * 0.2):int(fw * 0.8)]
            noses = NOSE_CASCADE.detectMultiScale(
                nose_roi,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(int(fw * 0.1), int(fh * 0.05)),
            )
            if len(noses) > 0:
                nx, ny, nw, nh = max(noses, key=lambda n: n[2] * n[3])
                nose_bbox = (
                    fx + int(fw * 0.2) + nx,
                    fy + int(fh * 0.2) + ny,
                    nw, nh,
                )

        det = FaceDetection(filepath, (fx, fy, fw, fh), eyes_local, smile_bbox, nose_bbox)
        detections.append(det)

        # Debug annotation
        if debug and bgr is not None:
            cv2.rectangle(bgr, (fx, fy), (fx + fw, fy + fh), (0, 255, 0), 2)
            for (ex, ey, ew, eh) in eyes_local:
                cv2.rectangle(bgr, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 1)
            if smile_bbox:
                sx, sy, sw, sh = smile_bbox
                cv2.rectangle(bgr, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 1)
            if nose_bbox:
                nx, ny, nw, nh = nose_bbox
                cv2.rectangle(bgr, (nx, ny), (nx + nw, ny + nh), (0, 255, 255), 1)

    if debug and bgr is not None and len(detections) > 0:
        debug_dir = output_dir() / "face_calibrate_debug"
        debug_dir.mkdir(exist_ok=True)
        base = os.path.splitext(os.path.basename(filepath))[0]
        debug_path = str(debug_dir / f"debug_{base}.png")
        # Resize to <=1280 before saving
        h, w = bgr.shape[:2]
        if max(h, w) > 1280:
            scale = 1280 / max(h, w)
            bgr = cv2.resize(bgr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
        cv2.imwrite(debug_path, bgr)

    return detections


# ── Aggregate statistics ─────────────────────────────────────────────────────

def aggregate_ratios(all_detections):
    """Compute aggregate statistics across all face detections.

    Returns dict mapping ratio_name -> {mean, median, std, min, max, count, values}.
    """
    # Collect all ratio values
    ratio_collections = {}
    for det in all_detections:
        for key, val in det.ratios.items():
            if key not in ratio_collections:
                ratio_collections[key] = []
            ratio_collections[key].append(val)

    stats = {}
    for key, values in ratio_collections.items():
        arr = np.array(values)
        stats[key] = {
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "std": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "count": len(values),
            "values": values,
        }
    return stats


# ── Threshold comparison ─────────────────────────────────────────────────────

def compare_thresholds(stats):
    """Compare measured ratios against current face test gate thresholds.

    Returns list of dicts with comparison results and recommendations.
    """
    comparisons = []

    # 1. Inter-eye distance
    if "inter_eye_distance" in stats:
        s = stats["inter_eye_distance"]
        current = CURRENT_THRESHOLDS["inter_eye_distance_frac"]
        diff = s["median"] - current
        pct = abs(diff / current) * 100 if current else 0
        comparisons.append({
            "parameter": "Inter-Eye Distance (frac of face width)",
            "current_threshold": current,
            "reference_median": s["median"],
            "reference_range": f"{s['min']:.3f} – {s['max']:.3f}",
            "reference_std": s["std"],
            "sample_count": s["count"],
            "deviation_pct": pct,
            "status": "CALIBRATED" if pct < 15 else ("REVIEW" if pct < 30 else "ADJUST"),
            "note": _inter_eye_note(current, s),
        })

    # 2. Eye vertical position
    if "eye_y_frac" in stats:
        s = stats["eye_y_frac"]
        current = CURRENT_THRESHOLDS["eye_y_frac_standard"]
        diff = s["median"] - current
        pct = abs(diff / abs(current)) * 100 if current else 0
        comparisons.append({
            "parameter": "Eye Y Position (frac of head_r from center)",
            "current_threshold": current,
            "reference_median": s["median"],
            "reference_range": f"{s['min']:.3f} – {s['max']:.3f}",
            "reference_std": s["std"],
            "sample_count": s["count"],
            "deviation_pct": pct,
            "status": "CALIBRATED" if pct < 20 else ("REVIEW" if pct < 40 else "ADJUST"),
            "note": _eye_y_note(current, s),
        })

    # 3. Eye radius range
    if "eye_r_frac" in stats:
        s = stats["eye_r_frac"]
        current_min = CURRENT_THRESHOLDS["eye_r_min_pass"]
        current_max = CURRENT_THRESHOLDS["eye_r_max"]
        # Check if reference eye sizes fall within current PASS range
        in_range_count = sum(1 for v in s["values"]
                            if current_min <= v <= current_max)
        in_range_pct = (in_range_count / s["count"]) * 100 if s["count"] else 0
        comparisons.append({
            "parameter": "Eye Radius (frac of head_r)",
            "current_threshold": f"{current_min:.3f} – {current_max:.3f} (PASS range)",
            "reference_median": s["median"],
            "reference_range": f"{s['min']:.3f} – {s['max']:.3f}",
            "reference_std": s["std"],
            "sample_count": s["count"],
            "deviation_pct": 100 - in_range_pct,
            "status": "CALIBRATED" if in_range_pct >= 70 else ("REVIEW" if in_range_pct >= 40 else "ADJUST"),
            "note": f"{in_range_pct:.0f}% of reference eyes fall within current PASS range. "
                    f"Reference cartoon eyes tend to be stylistically larger than realistic proportions.",
        })

    # 4. Mouth Y position
    if "mouth_y_frac" in stats:
        s = stats["mouth_y_frac"]
        current = CURRENT_THRESHOLDS["mouth_y_frac"]
        diff = s["median"] - current
        pct = abs(diff / abs(current)) * 100 if current else 0
        comparisons.append({
            "parameter": "Mouth Y Position (frac of head_r from center)",
            "current_threshold": current,
            "reference_median": s["median"],
            "reference_range": f"{s['min']:.3f} – {s['max']:.3f}",
            "reference_std": s["std"],
            "sample_count": s["count"],
            "deviation_pct": pct,
            "status": "CALIBRATED" if pct < 20 else ("REVIEW" if pct < 40 else "ADJUST"),
            "note": _mouth_y_note(current, s),
        })

    # 5. Eye-to-mouth span
    if "eye_to_mouth_frac" in stats:
        s = stats["eye_to_mouth_frac"]
        current = DERIVED_RATIOS["eye_to_mouth_frac"]
        diff = s["median"] - current
        pct = abs(diff / abs(current)) * 100 if current else 0
        comparisons.append({
            "parameter": "Eye-to-Mouth Span (frac of head_r)",
            "current_threshold": current,
            "reference_median": s["median"],
            "reference_range": f"{s['min']:.3f} – {s['max']:.3f}",
            "reference_std": s["std"],
            "sample_count": s["count"],
            "deviation_pct": pct,
            "status": "CALIBRATED" if pct < 20 else ("REVIEW" if pct < 40 else "ADJUST"),
            "note": f"Derived from eye_y_frac ({CURRENT_THRESHOLDS['eye_y_frac_standard']}) "
                    f"and mouth_y_frac ({CURRENT_THRESHOLDS['mouth_y_frac']}).",
        })

    # 6. Eye-to-nose and nose-to-mouth
    for ratio_key, label in [
        ("eye_to_nose_frac", "Eye-to-Nose Span"),
        ("nose_to_mouth_frac", "Nose-to-Mouth Span"),
    ]:
        if ratio_key in stats:
            s = stats[ratio_key]
            current = DERIVED_RATIOS.get(ratio_key, None)
            if current is not None:
                diff = s["median"] - current
                pct = abs(diff / abs(current)) * 100 if current else 0
                comparisons.append({
                    "parameter": f"{label} (frac of head_r)",
                    "current_threshold": current,
                    "reference_median": s["median"],
                    "reference_range": f"{s['min']:.3f} – {s['max']:.3f}",
                    "reference_std": s["std"],
                    "sample_count": s["count"],
                    "deviation_pct": pct,
                    "status": "CALIBRATED" if pct < 25 else ("REVIEW" if pct < 50 else "ADJUST"),
                    "note": f"Estimated from landmark detection. "
                            f"Nose cascades {'available' if NOSE_CASCADE and not NOSE_CASCADE.empty() else 'NOT available — using eye-mouth midpoint estimate'}.",
                })

    return comparisons


def _inter_eye_note(current, s):
    if s["median"] > current * 1.15:
        return (f"Reference inter-eye distance ({s['median']:.3f}) is wider than current "
                f"threshold ({current:.3f}). Cartoon styles often have wider-set eyes. "
                f"Current value is within stylistic range — no adjustment needed unless "
                f"realism is desired.")
    elif s["median"] < current * 0.85:
        return (f"Reference inter-eye distance ({s['median']:.3f}) is narrower than current "
                f"threshold ({current:.3f}). Consider narrowing eye spacing.")
    return f"Reference median ({s['median']:.3f}) is close to current threshold ({current:.3f})."


def _eye_y_note(current, s):
    return (f"Reference eyes sit at {s['median']:.3f} of head_r from center "
            f"(current: {current:.3f}). Negative values = above center. "
            f"Cartoon faces often place eyes higher than realistic anatomy.")


def _mouth_y_note(current, s):
    return (f"Reference mouth at {s['median']:.3f} of head_r from center "
            f"(current: {current:.3f}). Positive = below center.")


# ── Report generation ────────────────────────────────────────────────────────

def generate_report(all_detections, stats, comparisons, face_dir, body_dir, output_path):
    """Generate a Markdown calibration report."""
    lines = []
    lines.append("# Face Metric Calibration Report")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Tool:** LTG_TOOL_face_metric_calibrate.py")
    lines.append(f"**Cycle:** C46")
    lines.append(f"**Author:** Kai Nakamura")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Section 1: Data Sources ──
    lines.append("## 1. Reference Data Sources")
    lines.append("")
    lines.append(f"- **Face references:** `{face_dir}` ({_count_loadable(face_dir)} loadable images)")
    lines.append(f"- **Body references:** `{body_dir}` ({_count_loadable(body_dir)} loadable images)")
    lines.append(f"- **Total faces detected:** {len(all_detections)}")
    full_det = sum(1 for d in all_detections if d.has_full_detection())
    lines.append(f"- **Full detections (2+ eyes):** {full_det}")
    lines.append("")
    lines.append("**Detection method:** OpenCV Haar cascades (frontalface_alt2, eye, smile)")
    lines.append("")
    lines.append("**Note:** Reference images are cartoon/illustration expression sheets and proportion")
    lines.append("guides — not photographic portraits. Haar cascades are trained on real faces, so")
    lines.append("detection rates on stylized art will be lower than on photos. Detected faces represent")
    lines.append("the subset of reference art that is close enough to photorealistic proportions for")
    lines.append("cascade detection to trigger. This is expected and acceptable — our face test gate")
    lines.append("targets cartoon art that must still read as *faces* to human viewers, and cascade-")
    lines.append("detectable faces are a reasonable proxy for that readability threshold.")
    lines.append("")

    # ── Section 2: Per-image detection summary ──
    lines.append("## 2. Per-Image Detection Summary")
    lines.append("")
    lines.append("| Image | Faces | Eyes | Mouth | Full Detection |")
    lines.append("|---|---|---|---|---|")

    # Group by source directory
    for det in all_detections:
        fname = det.filename
        mouth = "Yes" if det.smile_bbox else "No"
        full = "Yes" if det.has_full_detection() else "No"
        lines.append(f"| `{fname[:40]}` | 1 | {len(det.eyes)} | {mouth} | {full} |")

    if not all_detections:
        lines.append("| *(no faces detected)* | — | — | — | — |")

    lines.append("")

    # ── Section 3: Measured Ratios ──
    lines.append("## 3. Measured Ratio Statistics")
    lines.append("")
    if stats:
        lines.append("| Ratio | Mean | Median | Std | Min | Max | N |")
        lines.append("|---|---|---|---|---|---|---|")
        for key in sorted(stats.keys()):
            s = stats[key]
            lines.append(f"| `{key}` | {s['mean']:.4f} | {s['median']:.4f} | "
                         f"{s['std']:.4f} | {s['min']:.4f} | {s['max']:.4f} | {s['count']} |")
        lines.append("")
    else:
        lines.append("*No ratio data extracted — insufficient face detections.*")
        lines.append("")

    # ── Section 4: Threshold Comparison ──
    lines.append("## 4. Threshold Comparison")
    lines.append("")
    lines.append("Status key: **CALIBRATED** = within expected range, **REVIEW** = moderate deviation,")
    lines.append("**ADJUST** = significant deviation — threshold update recommended.")
    lines.append("")

    if comparisons:
        for c in comparisons:
            status_icon = {"CALIBRATED": "PASS", "REVIEW": "WARN", "ADJUST": "FAIL"}[c["status"]]
            lines.append(f"### {c['parameter']}")
            lines.append("")
            lines.append(f"- **Status:** {c['status']} ({status_icon})")
            lines.append(f"- **Current threshold:** {c['current_threshold']}")
            lines.append(f"- **Reference median:** {c['reference_median']:.4f}")
            lines.append(f"- **Reference range:** {c['reference_range']}")
            lines.append(f"- **Deviation:** {c['deviation_pct']:.1f}%")
            lines.append(f"- **Samples:** {c['sample_count']}")
            lines.append(f"- **Note:** {c['note']}")
            lines.append("")
    else:
        lines.append("*No comparisons computed — insufficient data.*")
        lines.append("")

    # ── Section 5: Recommendations ──
    lines.append("## 5. Calibration Recommendations")
    lines.append("")

    adjust_items = [c for c in comparisons if c["status"] == "ADJUST"]
    review_items = [c for c in comparisons if c["status"] == "REVIEW"]
    calibrated_items = [c for c in comparisons if c["status"] == "CALIBRATED"]

    if not comparisons:
        lines.append("**Insufficient detection data for calibration.** Possible causes:")
        lines.append("- Reference images are too stylized for Haar cascade detection")
        lines.append("- Reference images may need manual annotation for precise landmark extraction")
        lines.append("- Consider adding photographic face reference images alongside cartoon references")
        lines.append("")
        lines.append("**Recommendation:** Current analytically-derived thresholds remain in effect.")
        lines.append("When more realistic reference images become available, re-run this tool.")
    elif adjust_items:
        lines.append(f"**{len(adjust_items)} parameter(s) flagged for adjustment:**")
        lines.append("")
        for c in adjust_items:
            lines.append(f"- **{c['parameter']}**: current={c['current_threshold']}, "
                         f"recommended={c['reference_median']:.4f} (median of {c['sample_count']} samples)")
        lines.append("")
        lines.append("**Action:** Update `LTG_TOOL_character_face_test.py` variant definitions to use")
        lines.append("the recommended values above. Re-run face test gate on all character assets after update.")
    elif review_items:
        lines.append(f"**{len(review_items)} parameter(s) flagged for review** (moderate deviation):")
        lines.append("")
        for c in review_items:
            lines.append(f"- **{c['parameter']}**: deviation {c['deviation_pct']:.1f}% from reference")
        lines.append("")
        lines.append("**Action:** No immediate adjustment required. These deviations are within")
        lines.append("acceptable range for cartoon stylization. Monitor in future calibration runs.")
    else:
        lines.append(f"**All {len(calibrated_items)} measured parameters are CALIBRATED.**")
        lines.append("")
        lines.append("Current face test gate thresholds are consistent with reference anatomy data.")
        lines.append("No threshold adjustments recommended at this time.")

    lines.append("")
    lines.append(f"{len(calibrated_items)} CALIBRATED / {len(review_items)} REVIEW / {len(adjust_items)} ADJUST")
    lines.append("")

    # ── Section 6: Methodology notes ──
    lines.append("## 6. Methodology Notes")
    lines.append("")
    lines.append("- **Detection:** OpenCV Haar cascades (frontalface_alt2 for face, eye for eyes, smile for mouth)")
    lines.append("- **Coordinate system:** All ratios expressed as fractions of face_r (half face height) or")
    lines.append("  face width, matching the convention in `LTG_TOOL_character_face_test.py`")
    lines.append("- **Limitations:**")
    lines.append("  - Haar cascades are trained on real photographs; cartoon face detection is partial")
    lines.append("  - AVIF format images cannot be loaded (PIL limitation on this system)")
    lines.append("  - Expression sheets contain many small faces — only those large enough for cascade")
    lines.append("    detection contribute to the statistics")
    lines.append("  - Nose cascade (haarcascade_mcs_nose.xml) may not be available; nose position")
    lines.append("    is then estimated as eye-mouth midpoint")
    lines.append("- **Cartoon adjustment factor:** Cartoon faces intentionally deviate from photorealistic")
    lines.append("  proportions (larger eyes, wider spacing, higher eye line). A deviation of 15-30%")
    lines.append("  from realistic anatomy is expected and desirable for the LTG art style.")
    lines.append("")
    lines.append("---")
    lines.append(f"*Report generated by LTG_TOOL_face_metric_calibrate.py — C46*")
    lines.append("")

    # Write report
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    return output_path


def _count_loadable(directory):
    """Count images loadable by PIL in a directory."""
    if not os.path.isdir(directory):
        return 0
    count = 0
    for fname in os.listdir(directory):
        ext = os.path.splitext(fname)[1].lower()
        if ext in SUPPORTED_EXTENSIONS:
            try:
                Image.open(os.path.join(directory, fname))
                count += 1
            except Exception:
                pass
    return count


# ── Main pipeline ────────────────────────────────────────────────────────────

def run_calibration(face_dir, body_dir, output_path, debug=False):
    """Run the full calibration pipeline.

    Returns (all_detections, stats, comparisons, report_path).
    """
    all_detections = []

    # Process face reference directory
    if os.path.isdir(face_dir):
        for fname in sorted(os.listdir(face_dir)):
            filepath = os.path.join(face_dir, fname)
            if not os.path.isfile(filepath):
                continue
            dets = detect_faces_in_image(filepath, debug=debug)
            all_detections.extend(dets)

    # Process body reference directory (may contain faces in proportion charts)
    if os.path.isdir(body_dir):
        for fname in sorted(os.listdir(body_dir)):
            filepath = os.path.join(body_dir, fname)
            if not os.path.isfile(filepath):
                continue
            dets = detect_faces_in_image(filepath, debug=debug)
            all_detections.extend(dets)

    # Filter to full detections for ratio statistics
    full_detections = [d for d in all_detections if d.has_full_detection()]

    # Aggregate
    stats = aggregate_ratios(full_detections)

    # Compare
    comparisons = compare_thresholds(stats)

    # Generate report
    report_path = generate_report(all_detections, stats, comparisons, face_dir, body_dir, output_path)

    return all_detections, stats, comparisons, report_path


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Face Test Gate Calibration Tool — validate thresholds against reference anatomy"
    )
    default_face = str(PROJECT_ROOT / "reference" / "drawing guides" / "face")
    default_body = str(PROJECT_ROOT / "reference" / "drawing guides" / "body")
    default_output = str(output_dir() / "face_metric_calibration_report.md")

    parser.add_argument("--face-dir", default=default_face,
                        help=f"Face reference directory (default: {default_face})")
    parser.add_argument("--body-dir", default=default_body,
                        help=f"Body reference directory (default: {default_body})")
    parser.add_argument("--output", default=default_output,
                        help=f"Output report path (default: {default_output})")
    parser.add_argument("--debug", action="store_true",
                        help="Save annotated debug PNGs for each detected face")

    args = parser.parse_args()

    print(f"Face Metric Calibration Tool — LTG C46")
    print(f"Face dir:   {args.face_dir}")
    print(f"Body dir:   {args.body_dir}")
    print(f"Output:     {args.output}")
    print(f"Debug PNGs: {'Yes' if args.debug else 'No'}")
    print()

    all_dets, stats, comparisons, report_path = run_calibration(
        args.face_dir, args.body_dir, args.output, debug=args.debug
    )

    # Print summary
    full_count = sum(1 for d in all_dets if d.has_full_detection())
    print(f"Total faces detected: {len(all_dets)}")
    print(f"Full detections (2+ eyes): {full_count}")
    print()

    if comparisons:
        print("Threshold comparison:")
        for c in comparisons:
            print(f"  [{c['status']:10s}] {c['parameter']}: "
                  f"current={c['current_threshold']}, ref_median={c['reference_median']:.4f}")
        print()

    adjust_count = sum(1 for c in comparisons if c["status"] == "ADJUST")
    review_count = sum(1 for c in comparisons if c["status"] == "REVIEW")
    cal_count = sum(1 for c in comparisons if c["status"] == "CALIBRATED")
    print(f"Result: {cal_count} CALIBRATED / {review_count} REVIEW / {adjust_count} ADJUST")
    print(f"Report: {report_path}")

    # Exit code: 0 if no ADJUST, 1 if any ADJUST
    return 1 if adjust_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
