"""
LTG_TOOL_render_qa_v001.py
===========================
Render Quality Assessment tool for "Luma & the Glitchkin."

Evaluates rendered PNGs against LTG rendering standards across five checks:
  A. Silhouette readability
  B. Value range
  C. Color fidelity (wraps LTG_TOOL_color_verify_v001)
  D. Warm/cool separation
  E. Line weight consistency

Author: Kai Nakamura (Technical Art Engineer)
Created: Cycle 26 — 2026-03-29
Version: 1.0.0

Coordinate note (Rin Inoue):
  silhouette_test(img) and value_study(img) are importable from this module.
  Both accept a PIL.Image and return a PIL.Image — compatible with
  LTG_TOOL_procedural_draw_v001.py interfaces.
"""

import os
import sys
import random
import statistics
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

# ---------------------------------------------------------------------------
# Import color verification from sibling tool
# ---------------------------------------------------------------------------
_TOOLS_DIR = Path(__file__).parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

from LTG_TOOL_color_verify_v001 import verify_canonical_colors, get_canonical_palette

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SILHOUETTE_THUMB_SIZE = (100, 100)
_MAX_OUTPUT_PX = 1280
_WARM_COOL_MIN_SEPARATION = 20.0   # PIL hue units (0–255 scale)
_VALUE_MIN_DARK = 30
_VALUE_MIN_BRIGHT = 225
_VALUE_MIN_RANGE = 150
_LINE_SAMPLE_COUNT = 20
random.seed(42)   # reproducible sampling


# ---------------------------------------------------------------------------
# A. Silhouette helpers
# ---------------------------------------------------------------------------

def silhouette_test(img: Image.Image) -> Image.Image:
    """
    Generate a B&W silhouette image from *img*.

    Converts to grayscale and applies a hard threshold at 128.
    If the image has an alpha channel the alpha is used as the shape mask;
    otherwise luminance is used. Output is resized to 100×100 for readability
    testing (thumbnail, preserving aspect ratio with padding).

    Parameters
    ----------
    img : PIL.Image
        Source image (any mode).

    Returns
    -------
    PIL.Image (mode "L", 100×100)
        White = shape pixels, Black = background.
        Compatible with LTG_TOOL_procedural_draw_v001.py silhouette_test().
    """
    if img.mode == "RGBA":
        # Use alpha channel as the silhouette mask
        alpha = img.split()[3]
        # Threshold: alpha > 128 → white (shape), else black (transparent)
        sil = alpha.point(lambda p: 255 if p > 128 else 0)
    else:
        gray = img.convert("L")
        # For opaque images threshold on darkness: dark pixels = shape
        sil = gray.point(lambda p: 255 if p < 128 else 0)

    # Thumbnail to 100×100 preserving aspect ratio, then paste on black canvas
    canvas = Image.new("L", SILHOUETTE_THUMB_SIZE, 0)
    sil.thumbnail(SILHOUETTE_THUMB_SIZE, Image.LANCZOS)
    offset_x = (SILHOUETTE_THUMB_SIZE[0] - sil.width) // 2
    offset_y = (SILHOUETTE_THUMB_SIZE[1] - sil.height) // 2
    canvas.paste(sil, (offset_x, offset_y))
    return canvas


def _score_silhouette(thumb: Image.Image) -> str:
    """
    Score a 100×100 B&W silhouette as 'distinct', 'ambiguous', or 'blob'.

    - 'distinct'  — clear shape with edges, not all-black or all-white
    - 'ambiguous' — present but edge count is low (unclear outline)
    - 'blob'      — nearly all-white or near-uniform (no readable shape)
    """
    pixels = list(thumb.getdata())
    total = len(pixels)
    white_count = sum(1 for p in pixels if p >= 128)
    black_count = total - white_count

    # All-black or all-white → blob
    if white_count < total * 0.02 or black_count < total * 0.02:
        return "blob"

    # Use edge detection to count edge pixels
    edges = thumb.filter(ImageFilter.FIND_EDGES)
    edge_pixels = list(edges.getdata())
    edge_count = sum(1 for p in edge_pixels if p > 20)
    edge_ratio = edge_count / total

    if edge_ratio >= 0.05:
        return "distinct"
    elif edge_ratio >= 0.015:
        return "ambiguous"
    else:
        return "blob"


# ---------------------------------------------------------------------------
# B. Value study helpers
# ---------------------------------------------------------------------------

def value_study(img: Image.Image) -> Image.Image:
    """
    Return a grayscale image with contrast stretched to the full 0–255 range.

    Parameters
    ----------
    img : PIL.Image
        Source image (any mode).

    Returns
    -------
    PIL.Image (mode "L")
        Grayscale with auto-levels applied. ≤ 1280px.
        Compatible with LTG_TOOL_procedural_draw_v001.py value_study().
    """
    gray = img.convert("L")
    # Auto-levels stretch
    stretched = ImageOps.autocontrast(gray, cutoff=0)
    stretched.thumbnail((_MAX_OUTPUT_PX, _MAX_OUTPUT_PX), Image.LANCZOS)
    return stretched


def _check_value_range(img: Image.Image) -> dict:
    """
    Check that the image uses the full value range.

    Returns
    -------
    dict
        {
          "min": int,       # darkest pixel value (0–255)
          "max": int,       # brightest pixel value (0–255)
          "range": int,     # max - min
          "has_dark": bool, # min <= VALUE_MIN_DARK (30)
          "has_bright": bool, # max >= VALUE_MIN_BRIGHT (225)
          "pass": bool,
          "notes": list[str]
        }
    """
    gray = img.convert("L")
    pixels = list(gray.getdata())
    min_val = min(pixels)
    max_val = max(pixels)
    val_range = max_val - min_val

    has_dark = min_val <= _VALUE_MIN_DARK
    has_bright = max_val >= _VALUE_MIN_BRIGHT
    range_ok = val_range >= _VALUE_MIN_RANGE

    notes = []
    if not has_dark:
        notes.append(f"No deep darks — darkest pixel is {min_val} (threshold ≤ {_VALUE_MIN_DARK})")
    if not has_bright:
        notes.append(f"No bright highlights — brightest pixel is {max_val} (threshold ≥ {_VALUE_MIN_BRIGHT})")
    if not range_ok:
        notes.append(f"Value compression — range is {val_range} (minimum {_VALUE_MIN_RANGE} required)")

    passed = has_dark and has_bright and range_ok

    return {
        "min": min_val,
        "max": max_val,
        "range": val_range,
        "has_dark": has_dark,
        "has_bright": has_bright,
        "pass": passed,
        "notes": notes,
    }


# ---------------------------------------------------------------------------
# D. Warm / cool separation
# ---------------------------------------------------------------------------

def _rgb_to_pil_hue(r: int, g: int, b: int) -> float:
    """
    Convert (R,G,B) 0–255 to PIL HSV hue (0–255 scale). Returns -1 if achromatic.
    """
    import colorsys
    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    h, s, v = colorsys.rgb_to_hsv(rf, gf, bf)
    if s < 0.05:
        return -1.0
    return h * 255.0


def _check_warm_cool(img: Image.Image) -> dict:
    """
    Check warm/cool separation by comparing median hue of top half vs bottom half.

    Returns
    -------
    dict
        {
          "zone_a_hue": float,   # median hue of first zone (PIL 0–255 scale)
          "zone_b_hue": float,   # median hue of second zone
          "separation": float,   # angular distance (PIL scale)
          "pass": bool,
          "notes": list[str]
        }
    """
    rgb = img.convert("RGB")
    w, h = rgb.size

    # Split top / bottom halves
    top_half = rgb.crop((0, 0, w, h // 2))
    bot_half = rgb.crop((0, h // 2, w, h))

    def median_hue(region: Image.Image) -> float:
        hues = []
        for (r, g, b) in region.getdata():
            hue = _rgb_to_pil_hue(r, g, b)
            if hue >= 0:
                hues.append(hue)
        if not hues:
            return -1.0
        hues.sort()
        return hues[len(hues) // 2]

    hue_a = median_hue(top_half)
    hue_b = median_hue(bot_half)

    notes = []
    if hue_a < 0 or hue_b < 0:
        notes.append("One or both zones are achromatic — warm/cool check skipped")
        return {
            "zone_a_hue": hue_a,
            "zone_b_hue": hue_b,
            "separation": 0.0,
            "pass": True,   # skip, don't penalise achromatic images
            "notes": notes,
        }

    # Circular distance on 0–255 scale
    delta = abs(hue_a - hue_b)
    if delta > 127.5:
        delta = 255.0 - delta
    separation = delta

    passed = separation >= _WARM_COOL_MIN_SEPARATION
    if not passed:
        notes.append(
            f"Flat palette — warm/cool separation is {separation:.1f} PIL units "
            f"(minimum {_WARM_COOL_MIN_SEPARATION} required)"
        )

    return {
        "zone_a_hue": round(hue_a, 2),
        "zone_b_hue": round(hue_b, 2),
        "separation": round(separation, 2),
        "pass": passed,
        "notes": notes,
    }


# ---------------------------------------------------------------------------
# E. Line weight consistency
# ---------------------------------------------------------------------------

def _check_line_weight(img: Image.Image, n_samples: int = _LINE_SAMPLE_COUNT) -> dict:
    """
    Detect edges and estimate line widths at random sample points.

    Strategy: apply FIND_EDGES, pick *n_samples* random edge pixels, for each
    measure the run-length of the bright edge line in the horizontal direction.
    Cluster widths into thin / mid / thick tiers and flag outliers.

    Returns
    -------
    dict
        {
          "sampled_widths": list[int],
          "mean_width": float,
          "std_width": float,
          "outlier_count": int,
          "pass": bool,
          "notes": list[str]
        }
    """
    gray = img.convert("L")
    edge_img = gray.filter(ImageFilter.FIND_EDGES)
    edge_data = list(edge_img.getdata())
    w, h = edge_img.size

    # Find candidate edge pixels (bright in edge map)
    edge_pixels = [(i % w, i // w) for i, v in enumerate(edge_data) if v > 40]

    notes = []
    if len(edge_pixels) < n_samples:
        notes.append(
            f"Insufficient edge pixels found ({len(edge_pixels)}) — "
            "line weight check skipped (possibly a flat/colorfield image)"
        )
        return {
            "sampled_widths": [],
            "mean_width": 0.0,
            "std_width": 0.0,
            "outlier_count": 0,
            "pass": True,  # skip, don't penalise images with no lines
            "notes": notes,
        }

    random.seed(42)
    sample_pts = random.sample(edge_pixels, min(n_samples, len(edge_pixels)))
    edge_array = list(edge_img.getdata())

    widths = []
    for (px, py) in sample_pts:
        # Measure horizontal run length of the bright edge line
        run = 1
        # Extend right
        x = px + 1
        while x < w and edge_array[py * w + x] > 40:
            run += 1
            x += 1
        # Extend left
        x = px - 1
        while x >= 0 and edge_array[py * w + x] > 40:
            run += 1
            x -= 1
        widths.append(run)

    mean_w = statistics.mean(widths)
    std_w = statistics.stdev(widths) if len(widths) > 1 else 0.0

    # Flag outliers: width > mean + 2*std or < mean - 2*std
    outliers = [w for w in widths if abs(w - mean_w) > 2 * std_w and std_w > 0]
    outlier_count = len(outliers)

    passed = outlier_count <= 2
    if not passed:
        notes.append(
            f"Line weight inconsistency — {outlier_count} outlier widths detected "
            f"(mean={mean_w:.1f}px, std={std_w:.1f}px)"
        )

    return {
        "sampled_widths": widths,
        "mean_width": round(mean_w, 2),
        "std_width": round(std_w, 2),
        "outlier_count": outlier_count,
        "pass": passed,
        "notes": notes,
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def qa_report(img_path: str) -> dict:
    """
    Run all QA checks on a single image. Returns results dict.

    Checks:
      A. Silhouette readability — threshold image, check shape at 100×100
      B. Value range — darkest pixel ≤ 30, brightest ≥ 225; flag if range < 150
      C. Color fidelity — wrap verify_canonical_colors() from LTG_TOOL_color_verify_v001
      D. Warm/cool separation — sample hues in two zones, check separation ≥ 20 PIL units
      E. Line weight consistency — edge detect, sample 20 points, check cluster spread

    Parameters
    ----------
    img_path : str
        Path to the PNG file to evaluate.

    Returns
    -------
    dict
        {
          "file": str,
          "silhouette": {
              "score": "distinct|ambiguous|blob",
              "thumbnail": PIL.Image (100×100 B&W)
          },
          "value_range": {
              "min": int, "max": int, "range": int,
              "has_dark": bool, "has_bright": bool, "pass": bool,
              "notes": list[str]
          },
          "color_fidelity": { ...dict from verify_canonical_colors()... },
          "warm_cool": {
              "zone_a_hue": float, "zone_b_hue": float,
              "separation": float, "pass": bool, "notes": list[str]
          },
          "line_weight": {
              "sampled_widths": list, "mean_width": float,
              "std_width": float, "outlier_count": int,
              "pass": bool, "notes": list[str]
          },
          "overall_grade": "PASS|WARN|FAIL"
        }
    """
    img = Image.open(img_path)
    img.load()

    # A — Silhouette
    sil_thumb = silhouette_test(img)
    sil_score = _score_silhouette(sil_thumb)

    # B — Value range
    value_result = _check_value_range(img)

    # C — Color fidelity
    palette = get_canonical_palette()
    color_result = verify_canonical_colors(img, palette, max_delta_hue=5)

    # D — Warm/cool separation
    warm_cool_result = _check_warm_cool(img)

    # E — Line weight consistency
    line_weight_result = _check_line_weight(img)

    # --- Grading logic ---
    # FAIL: silhouette=blob, value range completely fails (no dark AND no bright)
    # WARN: any single check fails (silhouette ambiguous, minor value issue, color drift, flat palette)
    # PASS: all checks pass

    fail_conditions = []
    warn_conditions = []

    # Silhouette
    if sil_score == "blob":
        fail_conditions.append("silhouette=blob")
    elif sil_score == "ambiguous":
        warn_conditions.append("silhouette=ambiguous")

    # Value range
    if not value_result["has_dark"] and not value_result["has_bright"]:
        fail_conditions.append("value_range: no darks AND no brights")
    elif not value_result["pass"]:
        warn_conditions.append("value_range: compressed or missing extreme")

    # Color fidelity
    if not color_result.get("overall_pass", True):
        warn_conditions.append("color_fidelity: hue drift detected")

    # Warm/cool
    if not warm_cool_result["pass"]:
        warn_conditions.append("warm_cool: insufficient separation")

    # Line weight
    if not line_weight_result["pass"]:
        warn_conditions.append("line_weight: inconsistent widths")

    if fail_conditions:
        overall_grade = "FAIL"
    elif warn_conditions:
        overall_grade = "WARN"
    else:
        overall_grade = "PASS"

    return {
        "file": str(img_path),
        "silhouette": {
            "score": sil_score,
            "thumbnail": sil_thumb,
        },
        "value_range": value_result,
        "color_fidelity": color_result,
        "warm_cool": warm_cool_result,
        "line_weight": line_weight_result,
        "overall_grade": overall_grade,
        "_fail_conditions": fail_conditions,
        "_warn_conditions": warn_conditions,
    }


def qa_batch(directory: str) -> list:
    """
    Run qa_report on all PNGs in *directory*. Returns list of result dicts.

    Parameters
    ----------
    directory : str
        Path to directory containing PNG files.

    Returns
    -------
    list[dict]
        One result dict per PNG found (sorted by filename).
    """
    dir_path = Path(directory)
    png_files = sorted(dir_path.glob("*.png"))
    results = []
    for png in png_files:
        try:
            result = qa_report(str(png))
        except Exception as exc:
            result = {
                "file": str(png),
                "error": str(exc),
                "overall_grade": "FAIL",
            }
        results.append(result)
    return results


def qa_summary_report(results: list, output_path: str):
    """
    Write a Markdown QA summary to *output_path*.

    Parameters
    ----------
    results : list[dict]
        List of result dicts from qa_report() or qa_batch().
    output_path : str
        Destination file path for the Markdown report.
    """
    lines = []
    lines.append("# LTG Render QA Report — Cycle 26")
    lines.append("")
    lines.append(f"**Generated:** 2026-03-29  ")
    lines.append(f"**Tool:** LTG_TOOL_render_qa_v001.py  ")
    lines.append(f"**Total assets evaluated:** {len(results)}")
    lines.append("")

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| File | Silhouette | Value Range | Color Fidelity | Warm/Cool | Line Weight | Grade |")
    lines.append("|------|-----------|-------------|----------------|-----------|-------------|-------|")

    for r in results:
        fname = Path(r["file"]).name
        if "error" in r:
            lines.append(f"| {fname} | ERROR | — | — | — | — | **FAIL** |")
            continue

        sil = r["silhouette"]["score"]
        vr = "PASS" if r["value_range"]["pass"] else "WARN"
        cf = "PASS" if r["color_fidelity"].get("overall_pass", True) else "WARN"
        wc = "PASS" if r["warm_cool"]["pass"] else "WARN"
        lw = "PASS" if r["line_weight"]["pass"] else "WARN"
        grade = r["overall_grade"]
        grade_fmt = f"**{grade}**" if grade in ("FAIL", "WARN") else grade
        lines.append(f"| {fname} | {sil} | {vr} | {cf} | {wc} | {lw} | {grade_fmt} |")

    lines.append("")

    # Grade counts
    pass_count = sum(1 for r in results if r.get("overall_grade") == "PASS")
    warn_count = sum(1 for r in results if r.get("overall_grade") == "WARN")
    fail_count = sum(1 for r in results if r.get("overall_grade") == "FAIL")
    lines.append(f"**Results:** {pass_count} PASS / {warn_count} WARN / {fail_count} FAIL")
    lines.append("")

    # Detailed section per file
    lines.append("---")
    lines.append("")
    lines.append("## Detailed Results")
    lines.append("")

    for r in results:
        fname = Path(r["file"]).name
        lines.append(f"### {fname}")
        lines.append("")

        if "error" in r:
            lines.append(f"**ERROR:** {r['error']}")
            lines.append("")
            continue

        grade = r["overall_grade"]
        lines.append(f"**Overall Grade:** {grade}")
        lines.append("")

        # Fail / warn conditions
        if r.get("_fail_conditions"):
            lines.append("**FAIL conditions:**")
            for c in r["_fail_conditions"]:
                lines.append(f"- {c}")
            lines.append("")
        if r.get("_warn_conditions"):
            lines.append("**WARN conditions:**")
            for c in r["_warn_conditions"]:
                lines.append(f"- {c}")
            lines.append("")

        # A — Silhouette
        sil = r["silhouette"]
        lines.append(f"**A. Silhouette:** `{sil['score']}`")
        lines.append("")

        # B — Value range
        vr = r["value_range"]
        vr_status = "PASS" if vr["pass"] else "WARN"
        lines.append(
            f"**B. Value Range:** {vr_status} — "
            f"min={vr['min']}, max={vr['max']}, range={vr['range']}"
        )
        if vr["notes"]:
            for note in vr["notes"]:
                lines.append(f"  - {note}")
        lines.append("")

        # C — Color fidelity
        cf = r["color_fidelity"]
        cf_status = "PASS" if cf.get("overall_pass", True) else "WARN"
        lines.append(f"**C. Color Fidelity:** {cf_status}")
        for color_name, data in cf.items():
            if color_name == "overall_pass":
                continue
            if isinstance(data, dict):
                status = data.get("status", "")
                if status in ("not_found", "achromatic_target"):
                    lines.append(f"  - {color_name}: {status}")
                else:
                    flag = "PASS" if data.get("pass", True) else "FAIL"
                    lines.append(
                        f"  - {color_name}: target={data.get('target_hue', '?'):.1f}° "
                        f"found={data.get('found_hue', '?'):.1f}° "
                        f"delta={data.get('delta', '?'):.1f}° [{flag}]"
                    )
        lines.append("")

        # D — Warm/cool
        wc = r["warm_cool"]
        wc_status = "PASS" if wc["pass"] else "WARN"
        lines.append(
            f"**D. Warm/Cool Separation:** {wc_status} — "
            f"zone_a={wc['zone_a_hue']}, zone_b={wc['zone_b_hue']}, "
            f"separation={wc['separation']}"
        )
        if wc["notes"]:
            for note in wc["notes"]:
                lines.append(f"  - {note}")
        lines.append("")

        # E — Line weight
        lw = r["line_weight"]
        lw_status = "PASS" if lw["pass"] else "WARN"
        lines.append(
            f"**E. Line Weight:** {lw_status} — "
            f"mean={lw['mean_width']}px, std={lw['std_width']}px, "
            f"outliers={lw['outlier_count']}"
        )
        if lw["notes"]:
            for note in lw["notes"]:
                lines.append(f"  - {note}")
        lines.append("")
        lines.append("---")
        lines.append("")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[QA] Summary report written to: {output_path}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python LTG_TOOL_render_qa_v001.py <image.png>          # single file")
        print("  python LTG_TOOL_render_qa_v001.py --batch <directory>  # batch mode")
        sys.exit(0)

    if sys.argv[1] == "--batch" and len(sys.argv) >= 3:
        directory = sys.argv[2]
        output_md = sys.argv[3] if len(sys.argv) >= 4 else "qa_report.md"
        print(f"[QA] Batch mode: {directory}")
        results = qa_batch(directory)
        for r in results:
            grade = r.get("overall_grade", "?")
            fname = Path(r["file"]).name
            print(f"  {grade:4s}  {fname}")
        qa_summary_report(results, output_md)
    else:
        img_path = sys.argv[1]
        print(f"[QA] Checking: {img_path}")
        result = qa_report(img_path)
        print(f"  Silhouette:    {result['silhouette']['score']}")
        vr = result["value_range"]
        print(f"  Value range:   min={vr['min']} max={vr['max']} range={vr['range']} pass={vr['pass']}")
        wc = result["warm_cool"]
        print(f"  Warm/cool:     separation={wc['separation']:.1f} pass={wc['pass']}")
        lw = result["line_weight"]
        print(f"  Line weight:   mean={lw['mean_width']}px outliers={lw['outlier_count']} pass={lw['pass']}")
        cf_pass = result["color_fidelity"].get("overall_pass", True)
        print(f"  Color fidelity: overall_pass={cf_pass}")
        print(f"  GRADE:         {result['overall_grade']}")
