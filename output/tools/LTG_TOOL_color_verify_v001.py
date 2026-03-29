"""
LTG_TOOL_color_verify_v001.py
==============================
Canonical color verification utility for "Luma & the Glitchkin."

Verifies that canonical palette colors in a rendered image have not drifted
beyond an acceptable hue tolerance. Intended as a gating function: call after
stylize() or any processing pass that could shift hues.

Author: Kai Nakamura (Technical Art Engineer)
Created: Cycle 25 — 2026-03-29
Version: 1.0.0
"""

import colorsys


# ---------------------------------------------------------------------------
# Canonical Palette
# ---------------------------------------------------------------------------

# Verified against output/color/palettes/master_palette.md (Cycle 25)
_CANONICAL_PALETTE = {
    "CORRUPT_AMBER":   (255, 140, 0),    # #FF8C00 — GL-07 bridge/warning color
    "BYTE_TEAL":       (0, 212, 232),    # #00D4E8 — GL-01b Byte body fill
    "UV_PURPLE":       (123, 47, 190),   # #7B2FBE — GL-04 deep digital void
    "HOT_MAGENTA":     (255, 45, 107),   # #FF2D6B — GL-02 danger/error signal
    "ELECTRIC_CYAN":   (0, 240, 255),    # #00F0FF — GL-01 primary glitch energy
    "SUNLIT_AMBER":    (212, 146, 58),   # #D4923A — RW-03 real-world warm light
}


def get_canonical_palette():
    """
    Returns the standard LTG canonical palette dict for verification.

    Returns
    -------
    dict
        Mapping of {"COLOR_NAME": (R, G, B), ...} with all six canonical
        LTG colors that must be verified on processed outputs.

    Notes
    -----
    Values are sourced from output/color/palettes/master_palette.md.
    Update both this function and _CANONICAL_PALETTE if the master palette
    is revised.
    """
    return dict(_CANONICAL_PALETTE)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _rgb_to_hue(r, g, b):
    """
    Convert an (R, G, B) triple (0–255 each) to hue in degrees [0, 360).

    Returns -1 if the color is achromatic (no hue).
    """
    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    h, s, v = colorsys.rgb_to_hsv(rf, gf, bf)
    if s < 0.05:  # achromatic — no meaningful hue
        return -1.0
    return h * 360.0


def _hue_delta(hue_a, hue_b):
    """
    Shortest angular distance between two hues (both in degrees).
    Returns a value in [0, 180].
    """
    delta = abs(hue_a - hue_b) % 360.0
    if delta > 180.0:
        delta = 360.0 - delta
    return delta


def _collect_near_color_pixels(img_rgb, target_rgb, radius=40):
    """
    Sample pixels from *img_rgb* that are within *radius* in Euclidean RGB
    space of *target_rgb*.

    Parameters
    ----------
    img_rgb : PIL.Image (mode "RGB" or "RGBA")
    target_rgb : (R, G, B) int tuple
    radius : int — Euclidean RGB distance threshold for sampling

    Returns
    -------
    list of (R, G, B) int tuples
    """
    tr, tg, tb = target_rgb
    radius_sq = radius * radius

    # Convert to RGB if RGBA
    if img_rgb.mode == "RGBA":
        work = img_rgb.convert("RGB")
    elif img_rgb.mode != "RGB":
        work = img_rgb.convert("RGB")
    else:
        work = img_rgb

    pixels = list(work.getdata())
    matched = []
    for (r, g, b) in pixels:
        dr, dg, db = r - tr, g - tg, b - tb
        if dr * dr + dg * dg + db * db <= radius_sq:
            matched.append((r, g, b))
    return matched


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def verify_canonical_colors(img, palette_dict, max_delta_hue=5):
    """
    Sample canonical colors from *img* and check for hue drift.

    For each entry in *palette_dict*, pixels near that color's RGB value are
    sampled. The median hue of sampled pixels is compared to the target hue.
    If the drift exceeds *max_delta_hue* degrees the color fails.

    Colors whose target is achromatic (no hue) are skipped with a note.
    Colors for which no matching pixels are found are marked "not_found" —
    this is **not** a fail, since the color may simply not appear in this
    frame.

    Parameters
    ----------
    img : PIL.Image
        The image to verify (any mode; converted internally as needed).
    palette_dict : dict
        Mapping of {"COLOR_NAME": (R, G, B), ...}.
        Use :func:`get_canonical_palette` for the standard LTG palette.
    max_delta_hue : float
        Maximum acceptable hue drift in degrees. Default: 5.

    Returns
    -------
    dict
        Per-color results keyed by color name, plus an "overall_pass" key.

        Each per-color entry is one of:

        Pass / Fail::

            {
                "target_rgb": (R, G, B),
                "target_hue": float,       # degrees
                "found_hue": float,        # median hue of sampled pixels
                "delta": float,            # absolute hue drift in degrees
                "pass": bool,
                "sample_count": int,
            }

        Not found (not a fail)::

            {
                "target_rgb": (R, G, B),
                "status": "not_found",
                "pass": True,
            }

        Achromatic target (skipped)::

            {
                "target_rgb": (R, G, B),
                "status": "achromatic_target",
                "pass": True,
            }

        overall_pass::

            "overall_pass": bool   # True only if ALL present colors pass
    """
    results = {}
    all_pass = True

    for color_name, target_rgb in palette_dict.items():
        tr, tg, tb = target_rgb
        target_hue = _rgb_to_hue(tr, tg, tb)

        # Achromatic target — cannot do a meaningful hue check
        if target_hue < 0:
            results[color_name] = {
                "target_rgb": target_rgb,
                "status": "achromatic_target",
                "pass": True,
            }
            continue

        # Collect nearby pixels
        matched = _collect_near_color_pixels(img, target_rgb, radius=40)

        if not matched:
            results[color_name] = {
                "target_rgb": target_rgb,
                "status": "not_found",
                "pass": True,
            }
            continue

        # Compute hue for each matched pixel; ignore achromatic ones
        hues = []
        for (r, g, b) in matched:
            h = _rgb_to_hue(r, g, b)
            if h >= 0:
                hues.append(h)

        if not hues:
            # All sampled pixels were achromatic — treat as not_found
            results[color_name] = {
                "target_rgb": target_rgb,
                "status": "not_found",
                "pass": True,
            }
            continue

        # Use median hue (robust to a few outliers at the edge of the sample radius)
        hues.sort()
        median_hue = hues[len(hues) // 2]
        delta = _hue_delta(target_hue, median_hue)
        color_pass = delta <= max_delta_hue

        if not color_pass:
            all_pass = False

        results[color_name] = {
            "target_rgb": target_rgb,
            "target_hue": round(target_hue, 2),
            "found_hue": round(median_hue, 2),
            "delta": round(delta, 2),
            "pass": color_pass,
            "sample_count": len(matched),
        }

    results["overall_pass"] = all_pass
    return results


# ---------------------------------------------------------------------------
# CLI / unit tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    from PIL import Image, ImageDraw

    print("=" * 60)
    print("LTG_TOOL_color_verify_v001 — self-test")
    print("=" * 60)

    palette = get_canonical_palette()
    print("\nCanonical palette loaded:")
    for name, rgb in palette.items():
        h = _rgb_to_hue(*rgb)
        print(f"  {name:20s}  RGB{rgb}  hue={h:.1f}°")

    # --- Test 1: image containing exactly the canonical colors ---
    print("\n--- Test 1: clean image (no drift expected) ---")
    img_clean = Image.new("RGB", (240, 40), (20, 20, 20))
    draw = ImageDraw.Draw(img_clean)
    for i, (name, rgb) in enumerate(palette.items()):
        x0 = i * 40
        draw.rectangle([x0, 0, x0 + 39, 39], fill=rgb)

    results = verify_canonical_colors(img_clean, palette, max_delta_hue=5)
    for k, v in results.items():
        if k == "overall_pass":
            print(f"\n  overall_pass: {v}")
        else:
            status = v.get("status", "checked")
            if status in ("not_found", "achromatic_target"):
                print(f"  {k:20s}  status={status}")
            else:
                flag = "PASS" if v["pass"] else "FAIL"
                print(f"  {k:20s}  target={v['target_hue']:.1f}°  "
                      f"found={v['found_hue']:.1f}°  "
                      f"delta={v['delta']:.1f}°  [{flag}]")

    assert results["overall_pass"], "Test 1 FAILED: expected overall_pass=True on clean image"
    print("  [Test 1 PASSED]")

    # --- Test 2: hue drift detection via internal helper ---
    # Electric Cyan (#00F0FF) target hue ~183.5°.
    # Simulate a color that was cyan but has drifted 30° toward green.
    # The verify function samples pixels within radius=40 of the target RGB.
    # A color shifted significantly in hue may or may not fall in that radius;
    # this test validates _hue_delta() and the detection math directly.
    print("\n--- Test 2: hue drift detection (internal helpers) ---")
    target_hue = _rgb_to_hue(0, 240, 255)   # ~183.5°
    drifted_hue = _rgb_to_hue(0, 255, 180)  # ~160.0° — visibly green-cyan
    delta = _hue_delta(target_hue, drifted_hue)
    print(f"  target_hue={target_hue:.1f}°  drifted_hue={drifted_hue:.1f}°  delta={delta:.1f}°")
    assert delta > 5, f"Expected delta > 5°, got {delta:.1f}°"
    # Now build an image that contains the drifted color AND is close enough in RGB
    # to be sampled (within radius=40). (0,255,220) vs (0,240,255): dist=sqrt(225+1225)=38 < 40
    near_drifted = (0, 255, 220)  # dist=38 from (0,240,255), hue ~168° — delta ~15.5°
    img_drifted = Image.new("RGB", (100, 100), near_drifted)
    results2 = verify_canonical_colors(img_drifted, {"ELECTRIC_CYAN": (0, 240, 255)}, max_delta_hue=5)
    ec = results2.get("ELECTRIC_CYAN", {})
    status = ec.get("status", "checked")
    if status in ("not_found", "achromatic_target"):
        print(f"  ELECTRIC_CYAN  status={status}")
    else:
        flag = "PASS" if ec["pass"] else "FAIL"
        print(f"  ELECTRIC_CYAN  target={ec['target_hue']:.1f}°  "
              f"found={ec['found_hue']:.1f}°  delta={ec['delta']:.1f}°  [{flag}]")
        assert not results2["overall_pass"], "Test 2 FAILED: expected overall_pass=False on drifted image"
    print("  [Test 2 PASSED — drift detection verified]")

    # --- Test 3: empty image (no canonical colors present) ---
    print("\n--- Test 3: blank image (not_found expected, not a failure) ---")
    img_blank = Image.new("RGB", (100, 100), (50, 50, 50))
    results3 = verify_canonical_colors(img_blank, palette, max_delta_hue=5)
    for k, v in results3.items():
        if k == "overall_pass":
            print(f"\n  overall_pass: {v}")
        else:
            print(f"  {k:20s}  status={v.get('status', 'unknown')}")
    assert results3["overall_pass"], "Test 3 FAILED: not_found should not fail"
    print("  [Test 3 PASSED — not_found is not a failure]")

    # --- Test 4: programmatic usage example ---
    print("\n--- Test 4: usage example with a file path ---")
    print("  (Demonstrates how stylize() would call this as a gating function)")
    print()
    print("  from PIL import Image")
    print("  from LTG_TOOL_color_verify_v001 import verify_canonical_colors, get_canonical_palette")
    print()
    print("  img = Image.open('output_frame.png')")
    print("  palette = get_canonical_palette()")
    print("  report = verify_canonical_colors(img, palette, max_delta_hue=5)")
    print("  if not report['overall_pass']:")
    print("      failed = [k for k, v in report.items() if k != 'overall_pass'")
    print("                and isinstance(v, dict) and not v.get('pass', True)]")
    print("      raise ValueError(f'Color drift detected in: {failed}')")
    print()

    print("=" * 60)
    print("All self-tests PASSED.")
    print("=" * 60)
