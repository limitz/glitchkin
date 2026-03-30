# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_object_detect_qa.py
==============================
Object Detection QA Tool for "Luma & the Glitchkin."

Uses torchvision pretrained models (Faster R-CNN / FCOS) to detect objects in
output frames, validate that bounding boxes match intended subjects, and report
class labels with confidence scores.

This is the correct use of pretrained weights — QA on our output, not blocking
pretrained usage.

Workflow:
  1. Load a pretrained object detection model (Faster R-CNN ResNet50 FPN by default)
  2. Run inference on each target image
  3. Report detected objects: class labels, confidence scores, bounding boxes
  4. Optionally validate against an expected-subjects manifest
  5. Output results as structured dict or Markdown report

Author: Kai Nakamura (Technical Art Engineer)
Created: Cycle 48 — 2026-03-30
Version: 1.0.0

Usage:
  # Single image
  python3 LTG_TOOL_object_detect_qa.py path/to/image.png

  # Batch directory
  python3 LTG_TOOL_object_detect_qa.py --batch output/color/style_frames/

  # With expected subjects validation
  python3 LTG_TOOL_object_detect_qa.py path/to/image.png --expect person,tv

  # Save report
  python3 LTG_TOOL_object_detect_qa.py --batch output/ --report output/production/object_detect_qa.md

  # Adjust confidence threshold
  python3 LTG_TOOL_object_detect_qa.py path/to/image.png --threshold 0.3

Dependencies: PIL/Pillow, torch, torchvision (all authorized per pil-standards.md)

COCO-to-Glitchkin Class Mapping
--------------------------------
The COCO-trained model produces consistent misclassifications on our stylized
cartoon assets. These are *useful* — treat them as proxy detections:

  Glitch character    → "kite"        (angular diamond silhouette)
  CRT monitor/screen  → "tv", "laptop" (expected — these ARE screens)
  CRT with Glitchkin  → "microwave"   (boxy shape + internal figures)
  Circular UI / clocks in panels → "clock"
  Glitch confetti / particles → "stop sign", "traffic light" (bright geometric shapes)

When using --expect, use these proxy labels to validate character/prop presence
in stylized scenes. E.g.: `--expect tv,kite` for a panel with CRT + Glitch.
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# Lazy imports — torch/torchvision may not be installed in all environments
# ---------------------------------------------------------------------------
_TORCH_AVAILABLE = False
_TV_AVAILABLE = False
_PIL_AVAILABLE = False

try:
    from PIL import Image
    _PIL_AVAILABLE = True
except ImportError:
    pass

try:
    import torch
    _TORCH_AVAILABLE = True
except ImportError:
    pass

try:
    import torchvision
    from torchvision import transforms
    _TV_AVAILABLE = True
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# COCO class labels (91 classes, index 0 = __background__)
COCO_LABELS = [
    "__background__", "person", "bicycle", "car", "motorcycle", "airplane",
    "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
    "N/A", "stop sign", "parking meter", "bench", "bird", "cat", "dog",
    "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
    "N/A", "backpack", "umbrella", "N/A", "N/A", "handbag", "tie",
    "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "N/A", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "N/A", "dining table", "N/A", "N/A",
    "toilet", "N/A", "tv", "laptop", "mouse", "remote", "keyboard",
    "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
    "N/A", "book", "clock", "vase", "scissors", "teddy bear",
    "hair drier", "toothbrush",
]

# Default confidence threshold
DEFAULT_THRESHOLD = 0.25

# Supported image extensions
SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}

# Max image dimension for inference (downscale for speed; 1280 per image-rules.md)
MAX_DIM = 1280


# ---------------------------------------------------------------------------
# Model loading (cached singleton)
# ---------------------------------------------------------------------------

_model = None
_device = None


def _get_device() -> "torch.device":
    """Return the best available device (CUDA > CPU)."""
    global _device
    if _device is not None:
        return _device
    if _TORCH_AVAILABLE and torch.cuda.is_available():
        _device = torch.device("cuda")
    else:
        _device = torch.device("cpu")
    return _device


def load_model(model_name: str = "fasterrcnn_resnet50_fpn"):
    """
    Load a pretrained object detection model from torchvision.

    Parameters
    ----------
    model_name : str
        Model name. Supported: "fasterrcnn_resnet50_fpn", "fcos_resnet50_fpn".

    Returns
    -------
    torch.nn.Module
        The detection model in eval mode.
    """
    global _model

    if not _TORCH_AVAILABLE or not _TV_AVAILABLE:
        raise RuntimeError(
            "torch and torchvision are required for object detection QA. "
            "Install with: pip install torch torchvision"
        )

    if _model is not None:
        return _model

    device = _get_device()

    if model_name == "fasterrcnn_resnet50_fpn":
        weights = torchvision.models.detection.FasterRCNN_ResNet50_FPN_Weights.DEFAULT
        _model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=weights)
    elif model_name == "fcos_resnet50_fpn":
        weights = torchvision.models.detection.FCOS_ResNet50_FPN_Weights.DEFAULT
        _model = torchvision.models.detection.fcos_resnet50_fpn(weights=weights)
    else:
        raise ValueError(f"Unknown model: {model_name}. Use 'fasterrcnn_resnet50_fpn' or 'fcos_resnet50_fpn'.")

    _model.to(device)
    _model.eval()
    return _model


# ---------------------------------------------------------------------------
# Core detection
# ---------------------------------------------------------------------------

def detect_objects(
    img_path: str,
    threshold: float = DEFAULT_THRESHOLD,
    model_name: str = "fasterrcnn_resnet50_fpn",
) -> Dict:
    """
    Run object detection on a single image.

    Parameters
    ----------
    img_path : str
        Path to the image file.
    threshold : float
        Minimum confidence score to include a detection.
    model_name : str
        Torchvision model to use.

    Returns
    -------
    dict
        {
            "file": str,
            "status": "OK" | "NO_DETECTIONS" | "ERROR" | "SKIP",
            "detections": list[dict],  # each: {label, score, bbox}
            "unique_labels": list[str],
            "image_size": (width, height),
            "error": str or None,
        }
    """
    path = Path(img_path)
    ext = path.suffix.lower()

    if ext not in SUPPORTED_EXTS:
        return {
            "file": str(path),
            "status": "SKIP",
            "detections": [],
            "unique_labels": [],
            "image_size": (0, 0),
            "error": f"unsupported extension: {ext}",
        }

    if not path.is_file():
        return {
            "file": str(path),
            "status": "ERROR",
            "detections": [],
            "unique_labels": [],
            "image_size": (0, 0),
            "error": "file not found",
        }

    if not _PIL_AVAILABLE:
        return {
            "file": str(path),
            "status": "ERROR",
            "detections": [],
            "unique_labels": [],
            "image_size": (0, 0),
            "error": "PIL/Pillow not available",
        }

    try:
        img = Image.open(str(path)).convert("RGB")
    except Exception as e:
        return {
            "file": str(path),
            "status": "ERROR",
            "detections": [],
            "unique_labels": [],
            "image_size": (0, 0),
            "error": f"failed to open image: {e}",
        }

    # Downscale per image-rules.md
    img.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
    w, h = img.size

    if not _TORCH_AVAILABLE or not _TV_AVAILABLE:
        return {
            "file": str(path),
            "status": "ERROR",
            "detections": [],
            "unique_labels": [],
            "image_size": (w, h),
            "error": "torch/torchvision not available",
        }

    try:
        model = load_model(model_name)
    except Exception as e:
        return {
            "file": str(path),
            "status": "ERROR",
            "detections": [],
            "unique_labels": [],
            "image_size": (w, h),
            "error": f"model load failed: {e}",
        }

    device = _get_device()

    # Transform to tensor
    to_tensor = transforms.ToTensor()
    img_tensor = to_tensor(img).unsqueeze(0).to(device)

    with torch.no_grad():
        predictions = model(img_tensor)

    pred = predictions[0]
    boxes = pred["boxes"].cpu()
    labels = pred["labels"].cpu()
    scores = pred["scores"].cpu()

    detections = []
    for i in range(len(scores)):
        score = float(scores[i])
        if score < threshold:
            continue
        label_idx = int(labels[i])
        label_str = COCO_LABELS[label_idx] if label_idx < len(COCO_LABELS) else f"class_{label_idx}"
        bbox = [round(float(c), 1) for c in boxes[i]]
        detections.append({
            "label": label_str,
            "score": round(score, 4),
            "bbox": bbox,  # [x1, y1, x2, y2]
            "bbox_area_pct": round(
                ((bbox[2] - bbox[0]) * (bbox[3] - bbox[1])) / (w * h) * 100, 2
            ),
        })

    # Sort by score descending
    detections.sort(key=lambda d: d["score"], reverse=True)

    unique_labels = sorted(set(d["label"] for d in detections))

    status = "OK" if detections else "NO_DETECTIONS"
    return {
        "file": str(path),
        "status": status,
        "detections": detections,
        "unique_labels": unique_labels,
        "image_size": (w, h),
        "error": None,
    }


def detect_batch(
    directory: str,
    threshold: float = DEFAULT_THRESHOLD,
    model_name: str = "fasterrcnn_resnet50_fpn",
    recursive: bool = False,
) -> List[Dict]:
    """
    Run object detection on all images in a directory.

    Parameters
    ----------
    directory : str
        Path to directory.
    threshold : float
        Minimum confidence score.
    model_name : str
        Model name.
    recursive : bool
        Whether to search subdirectories.

    Returns
    -------
    list[dict]
        One result per image file.
    """
    dirpath = Path(directory)
    if not dirpath.is_dir():
        return [{
            "file": str(dirpath),
            "status": "ERROR",
            "detections": [],
            "unique_labels": [],
            "image_size": (0, 0),
            "error": "not a directory",
        }]

    results = []
    pattern = "**/*" if recursive else "*"
    for fpath in sorted(dirpath.glob(pattern)):
        if not fpath.is_file():
            continue
        if fpath.suffix.lower() not in SUPPORTED_EXTS:
            continue
        results.append(detect_objects(str(fpath), threshold=threshold, model_name=model_name))

    return results


# ---------------------------------------------------------------------------
# Validation against expected subjects
# ---------------------------------------------------------------------------

def validate_expected(
    result: Dict,
    expected_labels: Set[str],
) -> Dict:
    """
    Validate that detected labels include all expected subjects.

    Parameters
    ----------
    result : dict
        Output from detect_objects().
    expected_labels : set[str]
        Set of COCO class labels expected in the image.

    Returns
    -------
    dict
        {
            "file": str,
            "verdict": "PASS" | "WARN" | "FAIL",
            "found": list[str],
            "missing": list[str],
            "unexpected": list[str],
            "explanation": str,
        }
    """
    detected = set(result.get("unique_labels", []))
    found = sorted(expected_labels & detected)
    missing = sorted(expected_labels - detected)
    unexpected = sorted(detected - expected_labels)

    if not missing:
        verdict = "PASS"
        explanation = f"All expected subjects found: {', '.join(found)}"
    elif len(missing) == len(expected_labels):
        verdict = "FAIL"
        explanation = f"None of the expected subjects found. Missing: {', '.join(missing)}"
    else:
        verdict = "WARN"
        explanation = f"Some expected subjects missing: {', '.join(missing)}"

    if unexpected:
        explanation += f". Additional objects: {', '.join(unexpected)}"

    return {
        "file": result.get("file", ""),
        "verdict": verdict,
        "found": found,
        "missing": missing,
        "unexpected": unexpected,
        "explanation": explanation,
    }


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def format_report(
    results: List[Dict],
    validations: Optional[List[Dict]] = None,
    include_empty: bool = False,
) -> str:
    """
    Format detection results as a Markdown report.

    Parameters
    ----------
    results : list[dict]
        Output from detect_objects() or detect_batch().
    validations : list[dict] or None
        Output from validate_expected() per image.
    include_empty : bool
        Include images with no detections.

    Returns
    -------
    str
        Markdown report text.
    """
    lines = [
        "# Object Detection QA Report",
        "",
        f"**Tool:** LTG_TOOL_object_detect_qa.py v1.0.0",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Threshold:** {DEFAULT_THRESHOLD}",
        "",
        "---",
        "",
    ]

    total = len(results)
    ok_count = sum(1 for r in results if r["status"] == "OK")
    no_det = sum(1 for r in results if r["status"] == "NO_DETECTIONS")
    err_count = sum(1 for r in results if r["status"] == "ERROR")
    skip_count = sum(1 for r in results if r["status"] == "SKIP")

    lines.append(f"**Images scanned:** {total}")
    lines.append(f"**With detections:** {ok_count}  |  **No detections:** {no_det}  |  **Errors:** {err_count}  |  **Skipped:** {skip_count}")
    lines.append("")

    # Validation summary
    if validations:
        v_pass = sum(1 for v in validations if v["verdict"] == "PASS")
        v_warn = sum(1 for v in validations if v["verdict"] == "WARN")
        v_fail = sum(1 for v in validations if v["verdict"] == "FAIL")
        lines.append(f"**Validation:** PASS: {v_pass}  WARN: {v_warn}  FAIL: {v_fail}")
        lines.append("")

    lines.append("---")
    lines.append("")

    val_map = {}
    if validations:
        for v in validations:
            val_map[v["file"]] = v

    for r in results:
        if r["status"] == "NO_DETECTIONS" and not include_empty:
            continue
        if r["status"] == "SKIP":
            continue

        fname = Path(r["file"]).name
        lines.append(f"## {fname}")
        lines.append("")

        if r["status"] == "ERROR":
            lines.append(f"  - **ERROR:** {r.get('error', 'unknown')}")
            lines.append("")
            continue

        w, h = r.get("image_size", (0, 0))
        lines.append(f"  - Size: {w}x{h}  |  Status: {r['status']}")

        if r["unique_labels"]:
            lines.append(f"  - Objects found: {', '.join(r['unique_labels'])}")

        # Validation result
        val = val_map.get(r["file"])
        if val:
            lines.append(f"  - **Validation: {val['verdict']}** — {val['explanation']}")

        lines.append("")

        # Detail table for detections
        if r["detections"]:
            lines.append("| Label | Score | BBox | Area % |")
            lines.append("|-------|-------|------|--------|")
            for d in r["detections"][:20]:  # Cap at 20 detections per image
                bbox_str = f"[{d['bbox'][0]:.0f}, {d['bbox'][1]:.0f}, {d['bbox'][2]:.0f}, {d['bbox'][3]:.0f}]"
                lines.append(
                    f"| {d['label']} | {d['score']:.3f} | {bbox_str} | {d['bbox_area_pct']:.1f}% |"
                )
            if len(r["detections"]) > 20:
                lines.append(f"| ... | _({len(r['detections']) - 20} more)_ | | |")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Generated by LTG_TOOL_object_detect_qa.py v1.0.0 (Kai Nakamura, C48)*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Object Detection QA — detect objects in output frames using torchvision pretrained models."
    )
    parser.add_argument(
        "image", nargs="?", default=None,
        help="Image file to analyze"
    )
    parser.add_argument(
        "--batch", default=None,
        help="Directory of images to analyze"
    )
    parser.add_argument(
        "--expect", default=None,
        help="Comma-separated expected COCO class labels (e.g. 'person,tv')"
    )
    parser.add_argument(
        "--threshold", type=float, default=DEFAULT_THRESHOLD,
        help=f"Minimum confidence threshold (default: {DEFAULT_THRESHOLD})"
    )
    parser.add_argument(
        "--model", default="fasterrcnn_resnet50_fpn",
        help="Model name (default: fasterrcnn_resnet50_fpn)"
    )
    parser.add_argument(
        "--report", default=None,
        help="Save Markdown report to file"
    )
    parser.add_argument(
        "--include-empty", action="store_true",
        help="Include images with no detections in report"
    )
    parser.add_argument(
        "--recursive", action="store_true",
        help="Search subdirectories when using --batch"
    )

    args = parser.parse_args()

    if not _TORCH_AVAILABLE or not _TV_AVAILABLE:
        print("ERROR: torch and torchvision are required.")
        print("Install with: pip install torch torchvision")
        sys.exit(2)

    threshold = args.threshold

    expected = None
    if args.expect:
        expected = set(l.strip() for l in args.expect.split(",") if l.strip())

    results = []
    if args.batch:
        print(f"[object_detect_qa] Scanning directory: {args.batch}")
        results = detect_batch(args.batch, threshold=threshold,
                              model_name=args.model, recursive=args.recursive)
    elif args.image:
        print(f"[object_detect_qa] Analyzing: {args.image}")
        results = [detect_objects(args.image, threshold=threshold,
                                 model_name=args.model)]
    else:
        parser.print_help()
        sys.exit(1)

    # Validate if expected labels provided
    validations = None
    if expected:
        validations = [validate_expected(r, expected) for r in results]

    # Print summary
    for r in results:
        fname = Path(r["file"]).name
        n_det = len(r["detections"])
        labels = ", ".join(r["unique_labels"][:5])
        print(f"  {fname}: {r['status']} ({n_det} detections) [{labels}]")

    if validations:
        print("\nValidation:")
        for v in validations:
            fname = Path(v["file"]).name
            print(f"  {fname}: {v['verdict']} — {v['explanation']}")

    # Generate report
    if args.report:
        report = format_report(results, validations=validations,
                               include_empty=args.include_empty)
        rpath = Path(args.report)
        rpath.parent.mkdir(parents=True, exist_ok=True)
        rpath.write_text(report, encoding="utf-8")
        print(f"\n[object_detect_qa] Report saved to: {args.report}")

    # Exit code
    if validations:
        fails = sum(1 for v in validations if v["verdict"] == "FAIL")
        if fails:
            sys.exit(2)
        warns = sum(1 for v in validations if v["verdict"] == "WARN")
        if warns:
            sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
