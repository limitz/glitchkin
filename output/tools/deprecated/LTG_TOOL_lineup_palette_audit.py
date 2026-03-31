#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_lineup_palette_audit.py
Art Director: Alex Chen — Cycle 34

Scans the character lineup PNG and verifies each character's body colors
against the canonical values in master_palette.md.

Strategy: divide the lineup into per-character columns, collect all pixel
colors found in each column (excluding background), then for each audited
color check whether any pixel in that column is within TOLERANCE of the
canonical RGB. Also checks that WRONG legacy values are NOT present.

Output: PASS / FAIL per audited color, with hex diff details.

Usage:
    python3 LTG_TOOL_lineup_palette_audit.py [lineup.png] [--tolerance N]

Defaults:
    lineup.png  : output/characters/main/LTG_CHAR_character_lineup.png
    tolerance   : 18 (Euclidean distance in RGB space — within 18 = MATCH)
"""

from __future__ import annotations

import sys
import os
import argparse
import math
from typing import Tuple, List, Dict, Optional

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Canonical palette values (from master_palette.md)
# ---------------------------------------------------------------------------

# Each entry: (name, palette_id, canonical_rgb, legacy_wrong_rgb_or_None)
CHARACTER_COLORS: Dict[str, List[dict]] = {
    "byte": [
        {
            "name": "Byte Body Fill (GL-01b Byte Teal)",
            "palette_id": "GL-01b",
            "canonical": (0, 212, 232),   # #00D4E8
            "wrong": (0, 190, 210),        # older wrong value sometimes used
        },
        {
            "name": "Byte Shadow (GL-01a Deep Cyan)",
            "palette_id": "GL-01a",
            "canonical": (0, 168, 180),    # #00A8B4
            "wrong": (0, 144, 176),         # C33 bug — was #0090B0
        },
    ],
    "miri": [
        {
            "name": "Miri House Slippers (CHAR-M-11 Dusty Warm Apricot)",
            "palette_id": "CHAR-M-11",
            "canonical": (196, 144, 122),  # #C4907A
            "wrong": (90, 122, 90),         # C33 bug — was #5A7A5A cool sage
        },
        {
            "name": "Miri Skin Base (CHAR-M-01)",
            "palette_id": "CHAR-M-01",
            "canonical": (140, 84, 48),    # #8C5430
            "wrong": None,
        },
        {
            "name": "Miri Cardigan (CHAR-M-07 Warm Terracotta Rust)",
            "palette_id": "CHAR-M-07",
            "canonical": (184, 92, 56),    # #B85C38
            "wrong": None,
        },
    ],
    "luma": [
        {
            "name": "Luma Hoodie (RW-04 Pumpkin Orange)",
            "palette_id": "RW-04",
            "canonical": (232, 114, 42),   # generator LUMA_HOODIE
            "wrong": None,
        },
        {
            "name": "Luma Skin Base (RW-10 Warm Caramel)",
            "palette_id": "RW-10 / CHAR-L-01",
            "canonical": (200, 136, 90),   # generator LUMA_SKIN
            "wrong": None,
        },
    ],
    "cosmo": [
        {
            "name": "Cosmo Jacket (Dusty Lavender)",
            "palette_id": "RW-08",
            "canonical": (168, 155, 191),  # generator COSMO_JACKET
            "wrong": None,
        },
        {
            "name": "Cosmo Skin Base (CHAR-C-01)",
            "palette_id": "CHAR-C-01",
            "canonical": (217, 192, 154),  # #D9C09A generator COSMO_SKIN
            "wrong": None,
        },
    ],
    "glitch": [
        {
            "name": "Glitch Corrupt Amber (GL-07)",
            "palette_id": "GL-07",
            "canonical": (255, 140, 0),    # #FF8C00
            "wrong": None,
        },
        {
            "name": "Glitch UV Purple Shadow (GL-04)",
            "palette_id": "GL-04",
            "canonical": (123, 47, 190),   # #7B2FBE
            "wrong": None,
        },
        {
            "name": "Glitch Void Black Outline (GL-08)",
            "palette_id": "GL-08",
            "canonical": (10, 10, 20),     # #0A0A14
            "wrong": None,
        },
    ],
}

# Background color of the lineup canvas — skip pixels close to this
BACKGROUND_RGB = (250, 248, 244)
PANEL_BG_RGB   = (245, 241, 235)
BG_TOLERANCE   = 20  # pixels within this distance of BG are skipped


# ---------------------------------------------------------------------------
# Geometry: character column boundaries
# The lineup places characters in this order (left→right): Luma, Byte, Cosmo,
# Miri, Glitch. At 1280×508 the 5 characters divide roughly into 5 columns.
# We derive boundaries from image width dynamically.
# ---------------------------------------------------------------------------

CHARACTER_ORDER = ["luma", "byte", "cosmo", "miri", "glitch"]


def get_column_bounds(img_w: int, n: int = 5) -> List[Tuple[int, int]]:
    """Return (x_start, x_end) for each of n equal columns."""
    col_w = img_w // n
    return [(i * col_w, (i + 1) * col_w) for i in range(n)]


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def rgb_distance(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> float:
    """Euclidean distance in RGB space."""
    return math.sqrt(sum((ac - bc) ** 2 for ac, bc in zip(a, b)))


def is_background(px: Tuple[int, int, int]) -> bool:
    return (rgb_distance(px, BACKGROUND_RGB) < BG_TOLERANCE or
            rgb_distance(px, PANEL_BG_RGB) < BG_TOLERANCE)


def collect_pixels(pixels, x0: int, x1: int, img_h: int) -> List[Tuple[int, int, int]]:
    """Collect all non-background RGB pixels in a column slice."""
    result = []
    for y in range(img_h):
        for x in range(x0, x1):
            px = pixels[x, y]
            # Handle both RGB and RGBA
            if len(px) == 4:
                if px[3] < 128:
                    continue
                px = px[:3]
            if not is_background(px):
                result.append(px)
    return result


def nearest_canonical(
    px_list: List[Tuple[int, int, int]],
    canonical: Tuple[int, int, int],
    tolerance: float
) -> Optional[Tuple[int, int, int]]:
    """
    Find the pixel in px_list closest to canonical.
    Returns that pixel if within tolerance, else None.
    """
    best_px = None
    best_dist = float("inf")
    for px in px_list:
        d = rgb_distance(px, canonical)
        if d < best_dist:
            best_dist = d
            best_px = px
    if best_dist <= tolerance:
        return best_px
    return None


def check_wrong_present(
    px_list: List[Tuple[int, int, int]],
    wrong: Tuple[int, int, int],
    tolerance: float
) -> Optional[Tuple[int, int, int]]:
    """
    Check if any pixel is within tolerance of the wrong (legacy) value.
    Returns the offending pixel if found.
    """
    best_px = None
    best_dist = float("inf")
    for px in px_list:
        d = rgb_distance(px, wrong)
        if d < best_dist:
            best_dist = d
            best_px = px
    if best_dist <= tolerance:
        return best_px
    return None


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

def audit_lineup(lineup_path: str, tolerance: float = 18.0) -> dict:
    """
    Run the full palette audit.

    Returns a results dict:
      {
        "character": {
          "color_name": {
            "result": "PASS" | "FAIL" | "WRONG_PRESENT",
            "canonical": (r, g, b),
            "found":     (r, g, b) | None,
            "distance":  float | None,
            "message":   str,
          }
        }
      }
    """
    if not os.path.exists(lineup_path):
        raise FileNotFoundError(f"Lineup PNG not found: {lineup_path}")

    img = Image.open(lineup_path).convert("RGBA")
    img_w, img_h = img.size
    pixels = img.load()

    col_bounds = get_column_bounds(img_w, n=len(CHARACTER_ORDER))

    results: dict = {}

    for idx, char_name in enumerate(CHARACTER_ORDER):
        x0, x1 = col_bounds[idx]
        char_pixels = collect_pixels(pixels, x0, x1, img_h)
        char_results: dict = {}

        for color_entry in CHARACTER_COLORS.get(char_name, []):
            name       = color_entry["name"]
            canonical  = color_entry["canonical"]
            wrong      = color_entry.get("wrong")

            found_px = nearest_canonical(char_pixels, canonical, tolerance)

            if found_px is not None:
                dist = rgb_distance(found_px, canonical)
                entry = {
                    "result": "PASS",
                    "canonical": canonical,
                    "found": found_px,
                    "distance": round(dist, 1),
                    "message": (
                        f"PASS — found {rgb_to_hex(found_px)} "
                        f"(canonical {rgb_to_hex(canonical)}, dist={dist:.1f})"
                    ),
                }
            else:
                entry = {
                    "result": "FAIL",
                    "canonical": canonical,
                    "found": None,
                    "distance": None,
                    "message": (
                        f"FAIL — canonical {rgb_to_hex(canonical)} not found "
                        f"(tolerance={tolerance:.0f})"
                    ),
                }

            # Also check if the WRONG legacy value is present
            if wrong is not None:
                wrong_px = check_wrong_present(char_pixels, wrong, tolerance)
                if wrong_px is not None:
                    entry["result"] = "WRONG_PRESENT"
                    dist_w = rgb_distance(wrong_px, wrong)
                    entry["message"] += (
                        f" — LEGACY WRONG VALUE DETECTED: {rgb_to_hex(wrong_px)} "
                        f"(expected wrong {rgb_to_hex(wrong)}, dist={dist_w:.1f})"
                    )

            char_results[name] = entry

        results[char_name] = char_results

    return results


def format_report(results: dict, lineup_path: str) -> str:
    """Render audit results as a human-readable report."""
    lines = [
        "=" * 72,
        "LTG CHARACTER LINEUP PALETTE AUDIT",
        f"File : {lineup_path}",
        "=" * 72,
    ]

    total_pass = 0
    total_fail = 0
    total_wrong = 0

    for char_name in CHARACTER_ORDER:
        char_results = results.get(char_name, {})
        if not char_results:
            continue

        lines.append(f"\n[{char_name.upper()}]")
        for color_name, entry in char_results.items():
            result = entry["result"]
            if result == "PASS":
                marker = "  PASS"
                total_pass += 1
            elif result == "WRONG_PRESENT":
                marker = "  WRONG"
                total_wrong += 1
            else:
                marker = "  FAIL"
                total_fail += 1
            lines.append(f"{marker}  {color_name}")
            lines.append(f"        {entry['message']}")

    lines.append("\n" + "-" * 72)
    total = total_pass + total_fail + total_wrong
    lines.append(
        f"RESULT : {total_pass}/{total} PASS  |  "
        f"{total_fail} FAIL  |  {total_wrong} WRONG LEGACY VALUE"
    )
    if total_fail == 0 and total_wrong == 0:
        lines.append("STATUS : PASS — all canonical colors verified, no legacy values detected")
    else:
        lines.append("STATUS : FAIL — review errors above before next critique")
    lines.append("=" * 72)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit character lineup PNG against canonical palette values."
    )
    parser.add_argument(
        "lineup",
        nargs="?",
        default=os.path.join(
            os.path.dirname(__file__),
            "../characters/main/LTG_CHAR_character_lineup.png",
        ),
        help="Path to the lineup PNG (default: LTG_CHAR_character_lineup.png)",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=18.0,
        help="Euclidean RGB distance tolerance for color matching (default: 18)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON results dict",
    )
    args = parser.parse_args()

    lineup_path = os.path.abspath(args.lineup)

    try:
        results = audit_lineup(lineup_path, tolerance=args.tolerance)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 1

    if args.json:
        import json
        # Convert tuples to lists for JSON serialisation
        def serialise(obj):
            if isinstance(obj, tuple):
                return list(obj)
            raise TypeError(f"Not serialisable: {type(obj)}")
        print(json.dumps(results, default=serialise, indent=2))
    else:
        print(format_report(results, lineup_path))

    # Exit code: 0=all pass, 1=at least one fail or wrong
    total_fail = sum(
        1
        for char in results.values()
        for entry in char.values()
        if entry["result"] in ("FAIL", "WRONG_PRESENT")
    )
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
