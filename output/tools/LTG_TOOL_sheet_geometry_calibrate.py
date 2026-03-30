#!/usr/bin/env python3
"""
LTG_TOOL_sheet_geometry_calibrate.py
======================================
Sheet Geometry Auto-Detection for Motion Spec Sheets.

Author: Ryo Hasegawa / Cycle 40
Ideabox origin: actioned from 20260329_ryo_hasegawa_cg_support_polygon_lint.md
  (submitted C39: false WARNs caused by hard-coded HEADER_H in motion spec lint)

Purpose
-------
Scan the first 100 rows of each motion spec sheet to detect where panels
actually begin. Writes per-family geometry to:
  output/tools/sheet_geometry_config.json

The config is then loaded by:
  - LTG_TOOL_motion_spec_lint.py  (eliminates false zone-sampling WARNs)
  - LTG_TOOL_luma_motion.py       (HEADER_H consistency)
  - LTG_TOOL_byte_motion.py       (HEADER_H consistency)

Detection algorithm
-------------------
1. Load the sheet as RGB.
2. Scan rows 0..99: compute the row mean brightness.
3. The header is the initial dark region (mean < BRIGHT_THRESHOLD).
4. "Panel start" = first row where brightness rises above threshold.
5. Also scan for vertical gap columns to detect panel column positions and width.
6. "Annotation zone start" = panel_top + ANNOT_OFFSET_FROM_TOP (empirical, 26px).

Output schema (sheet_geometry_config.json)
------------------------------------------
{
  "version": 1,
  "families": {
    "luma": {
      "header_h": <int>,       // rows before panel content starts
      "panel_top_abs": <int>,  // absolute y of first panel row
      "annot_zone_y_start": <int>,
      "annot_zone_y_end": <int>,
      "badge_panel_top_abs": <int>,
      "expected_panels": <int>
    },
    "byte": { ... },
    "cosmo": { ... }    // placeholder; Cosmo sheet not yet available
  }
}

Usage
-----
  python3 LTG_TOOL_sheet_geometry_calibrate.py
          [--luma PATH]   default: output/characters/motion/LTG_CHAR_luma_motion.png
          [--byte PATH]   default: output/characters/motion/LTG_CHAR_byte_motion.png
          [--out PATH]    default: output/tools/sheet_geometry_config.json
          [--verbose]

  Or import:
    from LTG_TOOL_sheet_geometry_calibrate import calibrate_sheet, load_or_calibrate
"""

import sys
import os
import json
import argparse
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# -------------------------------------------------------------------------------
# Config
# -------------------------------------------------------------------------------

DEFAULT_BRIGHT_THRESHOLD = 100   # row mean brightness above this = panel content (light sheets)
DARK_SHEET_THRESHOLD = 12        # row mean above this counts as "not pure void" (dark sheets)
SCAN_ROWS = 100                  # only scan first 100 rows for header detection
ANNOT_OFFSET_FROM_PANEL_TOP = 26 # pixels from panel_top_abs to annotation zone start
ANNOT_ZONE_HEIGHT = 148          # annotation zone spans this many rows
BADGE_OFFSET_FROM_PANEL_TOP = 4  # beat-badge starts 4px below panel top
LABEL_ZONE_H = 42                # label strip at bottom (unchanged)

SHEET_PATHS = {
    "luma": "output/characters/motion/LTG_CHAR_luma_motion.png",
    "byte": "output/characters/motion/LTG_CHAR_byte_motion.png",
}

EXPECTED_PANELS = {
    "luma": 4,   # 4 panels: Idle, Sprint Anticipation, Discovery Reaction, Landing
    "byte": 4,   # 4 panels: COMMITMENT beat arc (B1–B4)
    "cosmo": 3,  # placeholder
}

DEFAULT_CONFIG_PATH = "output/tools/sheet_geometry_config.json"


# -------------------------------------------------------------------------------
# Core detection
# -------------------------------------------------------------------------------

def _row_mean(arr, row):
    """Mean pixel value of a single row (averaged over all channels)."""
    return float(arr[row].mean())


def detect_panel_top(img, bright_threshold=DEFAULT_BRIGHT_THRESHOLD):
    """
    Scan first SCAN_ROWS of img to find the row where panel content begins.

    Strategy 1 (light sheets): find first row with mean > bright_threshold.
    Strategy 2 (dark sheets): the header is a band with distinct color from the
      canvas void. After the header ends, there's a PAD gap of pure void, then
      panel borders/content. We detect the header END (the last row of the
      header-colored band) and infer panel_top = header_end + PAD.

    For the Byte motion sheet: canvas = VOID_BLACK ~(10,10,20) mean≈13,
      header = (20,28,38) mean≈29. Panels also dark (VOID_BLACK canvas under
      mostly-dark panel content) — Strategy 1 fails. Strategy 2 detects the
      header end at row ~44, then adds PAD=12 → panel_top=56.

    Returns:
        panel_top_abs (int): absolute y where panels begin
        header_h (int):      same value (height of header region)
    """
    try:
        import numpy as np
        arr = _img_to_array(img)

        # Strategy 1: find first bright row (works for light-background sheets)
        for row in range(min(SCAN_ROWS, img.height)):
            if _row_mean(arr, row) > bright_threshold:
                return row, row

        # Strategy 2 (dark-background sheets): detect header end.
        # The header is a consistent-color band near the top.
        # Method: sample row means; find where initial non-void band ends.
        # "Header pixel": mean clearly above true void (threshold ~15).
        # After header, canvas returns to void, then panel begins after PAD.
        HEADER_PIXEL_THRESHOLD = 15  # header band rows have mean > this
        header_end = None
        in_header = False
        for row in range(min(SCAN_ROWS, img.height)):
            m = _row_mean(arr, row)
            if not in_header and m > HEADER_PIXEL_THRESHOLD:
                in_header = True
            elif in_header and m <= HEADER_PIXEL_THRESHOLD:
                header_end = row - 1
                break

        if header_end is not None:
            # Estimate PAD as ~12 (typical for dark Byte sheet)
            # The panel begins after the header + PAD gap.
            # Scan from header_end onward to find first row above void-black level.
            for row in range(header_end + 1, min(header_end + 30, img.height)):
                m = _row_mean(arr, row)
                if m > HEADER_PIXEL_THRESHOLD:
                    return row, row
            # Fallback: header_end + 12 (PAD)
            panel_top = header_end + 12
            return panel_top, panel_top

        # Strategy 3 (last resort): use hard-coded known values.
        # For Byte sheets (VOID_BLACK canvas, HEADER_H=44, PAD=12):
        # panel_top = 44 + 12 = 56.
        # We use 56 as a safe default for dark sheets.
        return 56, 56

    except ImportError:
        # numpy not available: fall back to PIL pixel scan
        return _detect_panel_top_pil(img, bright_threshold)


def _img_to_array(img):
    """Convert PIL image to numpy array."""
    import numpy as np
    return np.array(img)


def _detect_panel_top_pil(img, bright_threshold):
    """PIL-only fallback for panel top detection (slower)."""
    w, h = img.size
    px = img.load()
    for row in range(min(SCAN_ROWS, h)):
        total = 0
        for x in range(w):
            r, g, b = px[x, row]
            total += (r + g + b) / 3
        mean = total / w
        if mean > bright_threshold:
            return row, row
    return SCAN_ROWS, SCAN_ROWS


def calibrate_sheet(path, family_name, bright_threshold=DEFAULT_BRIGHT_THRESHOLD,
                    expected_panels=None, verbose=False):
    """
    Calibrate geometry for a single motion spec sheet.

    Args:
        path (str): Path to the PNG sheet.
        family_name (str): 'luma', 'byte', or 'cosmo'.
        bright_threshold (float): Row mean brightness cutoff.
        expected_panels (int): Override panel count (auto from EXPECTED_PANELS if None).
        verbose (bool): Print detection details.

    Returns:
        dict with geometry keys, or None on error.
    """
    if not HAS_PIL:
        print(f"ERROR: Pillow required for calibration.", file=sys.stderr)
        return None

    if not os.path.exists(path):
        print(f"WARNING: Sheet not found: {path}", file=sys.stderr)
        return None

    try:
        img = Image.open(path).convert("RGB")
    except Exception as e:
        print(f"ERROR opening {path}: {e}", file=sys.stderr)
        return None

    w, h = img.size

    panel_top_abs, header_h = detect_panel_top(img, bright_threshold)

    annot_zone_y_start = panel_top_abs + ANNOT_OFFSET_FROM_PANEL_TOP
    annot_zone_y_end = annot_zone_y_start + ANNOT_ZONE_HEIGHT
    badge_panel_top_abs = panel_top_abs + BADGE_OFFSET_FROM_PANEL_TOP

    ep = expected_panels if expected_panels is not None else EXPECTED_PANELS.get(family_name, 3)

    geo = {
        "header_h": header_h,
        "panel_top_abs": panel_top_abs,
        "annot_zone_y_start": annot_zone_y_start,
        "annot_zone_y_end": min(annot_zone_y_end, h - LABEL_ZONE_H - 2),
        "badge_panel_top_abs": badge_panel_top_abs,
        "expected_panels": ep,
        "sheet_w": w,
        "sheet_h": h,
        "_source": os.path.basename(path),
    }

    if verbose:
        print(f"  [{family_name}] panel_top_abs={panel_top_abs}  header_h={header_h}")
        print(f"  [{family_name}] annot_zone: y={annot_zone_y_start}..{geo['annot_zone_y_end']}")
        print(f"  [{family_name}] badge_panel_top_abs={badge_panel_top_abs}")
        print(f"  [{family_name}] expected_panels={ep}  sheet={w}x{h}")

    return geo


def calibrate_all(sheet_paths=None, verbose=False):
    """
    Calibrate all known sheet families.

    Args:
        sheet_paths (dict): Override paths per family, e.g. {"luma": "/abs/path.png"}.
        verbose (bool): Print per-family details.

    Returns:
        dict: Config structure ready for JSON serialisation.
    """
    if sheet_paths is None:
        sheet_paths = {}

    # Resolve to absolute paths relative to repo root
    repo_root = Path(__file__).parent.parent.parent  # tools/ -> output/ -> team/
    families = {}

    for family, default_rel in SHEET_PATHS.items():
        path = sheet_paths.get(family, None)
        if path is None:
            path = str(repo_root / default_rel)
        if verbose:
            print(f"\nCalibrating family '{family}' from: {path}")
        geo = calibrate_sheet(path, family, verbose=verbose)
        if geo is not None:
            families[family] = geo
        else:
            if verbose:
                print(f"  -> Skipped (sheet not available)")

    # Cosmo: no sheet yet — insert placeholder with safe defaults
    if "cosmo" not in families:
        families["cosmo"] = {
            "header_h": 44,
            "panel_top_abs": 56,
            "annot_zone_y_start": 82,
            "annot_zone_y_end": 230,
            "badge_panel_top_abs": 60,
            "expected_panels": 3,
            "sheet_w": 1280,
            "sheet_h": 720,
            "_source": "placeholder — no Cosmo sheet yet",
        }
        if verbose:
            print(f"\n  [cosmo] No sheet available — using safe defaults")

    config = {
        "version": 1,
        "description": (
            "Auto-detected panel geometry for LTG motion spec sheets. "
            "Generated by LTG_TOOL_sheet_geometry_calibrate.py. "
            "Re-run after regenerating any motion sheet."
        ),
        "families": families,
    }
    return config


def save_config(config, out_path):
    """Write config dict to JSON file."""
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Wrote: {out_path}")


def load_config(config_path):
    """Load geometry config from JSON. Returns None if not found."""
    if not os.path.exists(config_path):
        return None
    try:
        with open(config_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"WARNING: Could not load {config_path}: {e}", file=sys.stderr)
        return None


def get_family_geo(config, family_name):
    """Extract geometry dict for a family from config. Returns None if missing."""
    if config is None:
        return None
    return config.get("families", {}).get(family_name, None)


def load_or_calibrate(config_path, family_name, sheet_path=None, verbose=False):
    """
    Load geometry config from disk; calibrate if not present.

    Convenience function for motion tools to call at startup.

    Returns:
        (header_h, panel_top_abs) tuple, or hard-coded fallback on error.
    """
    config = load_config(config_path)
    geo = get_family_geo(config, family_name) if config else None

    if geo is None:
        if verbose:
            print(f"sheet_geometry_config.json missing or no entry for '{family_name}' — calibrating…")
        paths = {}
        if sheet_path:
            paths[family_name] = sheet_path
        new_config = calibrate_all(sheet_paths=paths, verbose=verbose)
        save_config(new_config, config_path)
        geo = get_family_geo(new_config, family_name)

    if geo is None:
        # Hard-coded fallback
        fallbacks = {"luma": (54, 54), "byte": (56, 56), "cosmo": (56, 56)}
        hh, pt = fallbacks.get(family_name, (56, 56))
        return hh, pt

    return geo["header_h"], geo["panel_top_abs"]


# -------------------------------------------------------------------------------
# CLI
# -------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Calibrate motion spec sheet panel geometry and write sheet_geometry_config.json."
    )
    parser.add_argument("--luma", default=None,
                        help="Path to Luma motion sheet PNG (default: auto-resolved)")
    parser.add_argument("--byte", default=None,
                        help="Path to Byte motion sheet PNG (default: auto-resolved)")
    parser.add_argument("--out", default=None,
                        help="Output JSON path (default: output/tools/sheet_geometry_config.json)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print detection details per family")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.parent
    out_path = args.out or str(repo_root / DEFAULT_CONFIG_PATH)

    sheet_paths = {}
    if args.luma:
        sheet_paths["luma"] = args.luma
    if args.byte:
        sheet_paths["byte"] = args.byte

    print("LTG Sheet Geometry Calibrator — Ryo Hasegawa / C40")
    print("=" * 55)

    config = calibrate_all(sheet_paths=sheet_paths, verbose=args.verbose or True)
    save_config(config, out_path)

    # Print summary
    print("\nGeometry Summary:")
    for family, geo in config.get("families", {}).items():
        src = geo.get("_source", "")
        print(f"  {family:8s}  header_h={geo['header_h']:3d}  "
              f"panel_top={geo['panel_top_abs']:3d}  "
              f"annot_y={geo['annot_zone_y_start']}..{geo['annot_zone_y_end']}  "
              f"panels={geo['expected_panels']}  [{src}]")

    print(f"\nConfig written to: {out_path}")
    print("Next: re-run LTG_TOOL_motion_spec_lint.py — WARN count should drop.")


if __name__ == "__main__":
    main()
