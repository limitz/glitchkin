# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_color_verify.py
==============================
Canonical color verification utility for "Luma & the Glitchkin."
Version 3.0.0 — adds CORRUPT_AMBER fringe detection mode.

All v001/v002 API is preserved unchanged. New function
:func:`detect_corrupt_amber` validates that GL-07 (#FF8C00) pixels in a
Real World scene are sanctioned fringe (low composited intensity, within
CRT bounding box) vs accidental full-opacity GL palette leaks.

Author: Kai Nakamura (Technical Art Engineer)
Created: Cycle 25 — 2026-03-29  (v001)
Updated: Cycle 31 — 2026-03-29  (v002 — histogram mode)
Updated: Cycle 47 — 2026-03-30  (v003 — CORRUPT_AMBER detection mode, Jordan Reed)
Version: 3.0.0

CHANGELOG
---------
v3.0.0  C47 — Add ``detect_corrupt_amber()`` function. Given a composited RGB image
               and CRT bounding box, finds GL-07 hue pixels, validates they are
               spatially contained and have composited intensity consistent with
               alpha <= 38/255 (15%). Flags full-opacity GL-07 as violations.
               Reference: output/production/corrupt_amber_fringe_spec.md (C46).
v2.0.0  C31 — Add ``histogram=True`` parameter to verify_canonical_colors().
               Per-color result gains optional ``hue_histogram`` (list of dicts),
               ``histogram_bucket_deg`` (int), ``canonical_bucket_index`` (int).
               All other API unchanged.
v1.0.0  C25 — Initial release.
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
# Histogram helpers (v002 addition)
# ---------------------------------------------------------------------------

_DEFAULT_BUCKET_DEG = 5  # 360 / 5 = 72 buckets


def _build_hue_histogram(hues, bucket_deg=_DEFAULT_BUCKET_DEG, canonical_hue=None):
    """
    Build a hue distribution histogram from a list of hue values (degrees).

    Parameters
    ----------
    hues : list of float — hue values in [0, 360), achromatic pixels excluded
    bucket_deg : int — width of each hue band in degrees (default: 5)
    canonical_hue : float | None — if given, marks the bucket containing this hue

    Returns
    -------
    tuple (histogram, canonical_bucket_index)

    histogram : list of dicts, one per bucket, ordered by hue range:
        {
            "hue_start":  float,  # lower bound of bucket (degrees)
            "hue_end":    float,  # upper bound of bucket (degrees)
            "count":      int,    # number of pixels in this band
            "is_canonical": bool, # True if canonical hue falls in this bucket
        }

    canonical_bucket_index : int | None — index into histogram of the canonical bucket,
        or None if canonical_hue is None or achromatic.
    """
    n_buckets = 360 // bucket_deg
    counts = [0] * n_buckets

    for h in hues:
        idx = int(h // bucket_deg) % n_buckets
        counts[idx] += 1

    canonical_idx = None
    if canonical_hue is not None and canonical_hue >= 0:
        canonical_idx = int(canonical_hue // bucket_deg) % n_buckets

    histogram = []
    for i, cnt in enumerate(counts):
        histogram.append({
            "hue_start": float(i * bucket_deg),
            "hue_end": float((i + 1) * bucket_deg),
            "count": cnt,
            "is_canonical": (i == canonical_idx),
        })

    return histogram, canonical_idx


def format_histogram(histogram, canonical_bucket_index=None, width=40):
    """
    Format a hue histogram as a multi-line ASCII string for human inspection.

    Parameters
    ----------
    histogram : list of dicts (output of _build_hue_histogram)
    canonical_bucket_index : int | None
    width : int — max bar width in characters

    Returns
    -------
    str
    """
    max_count = max((b["count"] for b in histogram), default=1) or 1
    lines = []
    for i, bucket in enumerate(histogram):
        if bucket["count"] == 0 and not bucket["is_canonical"]:
            continue  # skip empty non-canonical buckets for brevity
        bar_len = int(bucket["count"] / max_count * width)
        bar = "#" * bar_len
        marker = " <-- CANONICAL" if bucket["is_canonical"] else ""
        lines.append(
            f"  {bucket['hue_start']:5.1f}–{bucket['hue_end']:5.1f}°  "
            f"|{bar:<{width}}|  {bucket['count']:5d}{marker}"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def verify_canonical_colors(img, palette_dict, max_delta_hue=5, histogram=False):
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
    histogram : bool
        When True, each per-color result that has sampled pixels also includes:
          - ``hue_histogram``          — list of dicts (see below)
          - ``histogram_bucket_deg``   — int, bucket width in degrees (5)
          - ``canonical_bucket_index`` — int | None, index of canonical hue bucket

        Each histogram entry:
            {
                "hue_start":    float,  # bucket lower bound (degrees)
                "hue_end":      float,  # bucket upper bound (degrees)
                "count":        int,    # pixels in this band
                "is_canonical": bool,   # True for the canonical hue's bucket
            }

        Default: False (histogram data omitted — existing behavior unchanged).

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
                # --- if histogram=True ---
                "hue_histogram":          list[dict],
                "histogram_bucket_deg":   int,
                "canonical_bucket_index": int | None,
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

        entry = {
            "target_rgb": target_rgb,
            "target_hue": round(target_hue, 2),
            "found_hue": round(median_hue, 2),
            "delta": round(delta, 2),
            "pass": color_pass,
            "sample_count": len(matched),
        }

        # --- v002: histogram mode ---
        if histogram:
            hist, canonical_idx = _build_hue_histogram(
                hues,
                bucket_deg=_DEFAULT_BUCKET_DEG,
                canonical_hue=target_hue,
            )
            entry["hue_histogram"] = hist
            entry["histogram_bucket_deg"] = _DEFAULT_BUCKET_DEG
            entry["canonical_bucket_index"] = canonical_idx

        results[color_name] = entry

    results["overall_pass"] = all_pass
    return results


# ---------------------------------------------------------------------------
# CORRUPT_AMBER Detection Mode (v003 — C47)
# ---------------------------------------------------------------------------

# GL-07 / CORRUPT_AMBER canonical RGB
_CORRUPT_AMBER_RGB = (255, 140, 0)
# Maximum composited brightness (Value in HSV) for alpha-38 fringe.
# At alpha=38/255 (~15%) over black, peak V = 255*0.149 = 0.149.
# Over a mid-dark bg (V~0.15), composited V ~ 0.15 + 0.85*0.15 = 0.28.
# We use V <= 0.45 as ceiling to allow some bg brightness tolerance.
_CORRUPT_AMBER_MAX_VALUE = 0.45
# Spatial margin around CRT box — fringe may extend a few pixels past box edge
_CRT_BOX_MARGIN_PX = 12


def detect_corrupt_amber(img, crt_box=None, rgb_radius=30,
                         max_value=_CORRUPT_AMBER_MAX_VALUE,
                         box_margin=_CRT_BOX_MARGIN_PX):
    """
    Detect CORRUPT_AMBER (GL-07, #FF8C00) pixels in a composited RGB image
    and classify them as sanctioned fringe or palette violations.

    A pixel is flagged as CORRUPT_AMBER if it is within *rgb_radius* Euclidean
    distance of the canonical GL-07 RGB value (255, 140, 0). This tight radius
    excludes SUNLIT_AMBER (212, 146, 58) which is ~50 RGB distance away.

    A flagged pixel is classified as:
      - **sanctioned**: composited value (HSV V) <= *max_value* AND within
        *crt_box* (expanded by *box_margin*). Consistent with alpha <= 38/255.
      - **violation**: composited value > *max_value* OR outside the CRT box.
        Indicates full-opacity or near-full-opacity GL-07 in a Real World scene.

    If *crt_box* is None, spatial containment is not checked (all flagged pixels
    are classified by intensity only).

    Parameters
    ----------
    img : PIL.Image
        Composited RGB image (the final rendered PNG).
    crt_box : tuple (x0, y0, x1, y1) or None
        CRT glow bounding box in pixel coordinates. If provided, flagged pixels
        outside this box (plus margin) are violations regardless of intensity.
    rgb_radius : int
        Euclidean RGB distance threshold for matching GL-07 (default 30).
        SUNLIT_AMBER is ~50 away — radius 30 cleanly excludes it.
    max_value : float
        Maximum HSV Value for sanctioned fringe (default 0.45).
    box_margin : int
        Spatial margin (px) around crt_box (default 12).

    Returns
    -------
    dict
        {
            "total_amber_pixels": int,     # total pixels matching GL-07
            "sanctioned": int,             # within box + low intensity
            "violations": int,             # outside box or high intensity
            "violation_pixels": list,      # [(x, y, r, g, b, hsv_v), ...] (up to 50)
            "pass": bool,                  # True if violations == 0
            "max_violation_value": float,  # highest V among violations (0 if none)
            "message": str,
        }
    """
    if img.mode != "RGB":
        work = img.convert("RGB")
    else:
        work = img

    w, h = work.size
    pixels = list(work.getdata())
    tr, tg, tb = _CORRUPT_AMBER_RGB
    radius_sq = rgb_radius * rgb_radius

    # Expand CRT box by margin
    if crt_box is not None:
        bx0 = crt_box[0] - box_margin
        by0 = crt_box[1] - box_margin
        bx1 = crt_box[2] + box_margin
        by1 = crt_box[3] + box_margin
    else:
        bx0, by0, bx1, by1 = 0, 0, w, h  # no spatial filter

    total_amber = 0
    sanctioned = 0
    violations = 0
    violation_list = []
    max_viol_v = 0.0

    for idx, (r, g, b) in enumerate(pixels):
        dr, dg, db = r - tr, g - tg, b - tb
        if dr * dr + dg * dg + db * db > radius_sq:
            continue

        rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
        _, s, v = colorsys.rgb_to_hsv(rf, gf, bf)

        total_amber += 1
        x = idx % w
        y = idx // w
        in_box = (bx0 <= x <= bx1 and by0 <= y <= by1)
        low_intensity = (v <= max_value)

        if in_box and low_intensity:
            sanctioned += 1
        else:
            violations += 1
            if v > max_viol_v:
                max_viol_v = v
            if len(violation_list) < 50:
                violation_list.append((x, y, r, g, b, round(v, 3)))

    is_pass = violations == 0

    if total_amber == 0:
        msg = "No CORRUPT_AMBER pixels detected (no pixels within RGB radius of GL-07)."
    elif is_pass:
        msg = (f"PASS — {total_amber} CORRUPT_AMBER pixels, all sanctioned "
               f"(within CRT box, V <= {max_value:.2f}).")
    else:
        msg = (f"FAIL — {violations}/{total_amber} CORRUPT_AMBER pixel(s) are violations "
               f"(max V={max_viol_v:.3f}, threshold {max_value:.2f}).")

    return {
        "total_amber_pixels": total_amber,
        "sanctioned": sanctioned,
        "violations": violations,
        "violation_pixels": violation_list,
        "pass": is_pass,
        "max_violation_value": round(max_viol_v, 4),
        "message": msg,
    }


# ---------------------------------------------------------------------------
# CLI / unit tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import argparse
    from PIL import Image, ImageDraw

    parser = argparse.ArgumentParser(
        description="LTG color verification utility — v3.0.0",
    )
    parser.add_argument(
        "image", nargs="?", default=None,
        help="Path to image file to verify (optional — runs self-tests if omitted)",
    )
    parser.add_argument(
        "--histogram", action="store_true",
        help="Show hue distribution histogram for each sampled color",
    )
    parser.add_argument(
        "--corrupt-amber", action="store_true",
        help="Run CORRUPT_AMBER fringe detection (v003). Reports sanctioned vs violation pixels.",
    )
    parser.add_argument(
        "--crt-box", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"),
        help="CRT glow bounding box for CORRUPT_AMBER spatial containment check",
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # If an image path is given, verify it and exit
    # ------------------------------------------------------------------
    if args.image:
        img_in = Image.open(args.image)
        palette = get_canonical_palette()
        report = verify_canonical_colors(img_in, palette, max_delta_hue=5, histogram=args.histogram)
        print(f"\nColor verification: {args.image}")
        print("=" * 60)
        for k, v in report.items():
            if k == "overall_pass":
                print(f"\noverall_pass: {v}")
                continue
            status = v.get("status", "checked")
            if status in ("not_found", "achromatic_target"):
                print(f"  {k:20s}  status={status}")
            else:
                flag = "PASS" if v["pass"] else "FAIL"
                print(f"  {k:20s}  target={v['target_hue']:.1f}°  "
                      f"found={v['found_hue']:.1f}°  "
                      f"delta={v['delta']:.1f}°  [{flag}]  n={v['sample_count']}")
                if args.histogram and "hue_histogram" in v:
                    print(f"    Hue histogram ({v['histogram_bucket_deg']}° buckets):")
                    print(format_histogram(v["hue_histogram"], v["canonical_bucket_index"]))

        overall = report["overall_pass"]

        # CORRUPT_AMBER detection (v003)
        if args.corrupt_amber:
            crt_box = tuple(args.crt_box) if args.crt_box else None
            ca_report = detect_corrupt_amber(img_in, crt_box=crt_box)
            print(f"\nCORRUPT_AMBER detection:")
            print(f"  {ca_report['message']}")
            print(f"  Total amber pixels: {ca_report['total_amber_pixels']}")
            print(f"  Sanctioned: {ca_report['sanctioned']}")
            print(f"  Violations: {ca_report['violations']}")
            if ca_report['violations'] > 0:
                print(f"  Max violation V: {ca_report['max_violation_value']:.3f}")
                for vp in ca_report['violation_pixels'][:10]:
                    print(f"    ({vp[0]},{vp[1]}) RGB=({vp[2]},{vp[3]},{vp[4]}) V={vp[5]}")
            overall = overall and ca_report["pass"]

        sys.exit(0 if overall else 1)

    # ------------------------------------------------------------------
    # Self-tests (no image argument)
    # ------------------------------------------------------------------
    print("=" * 60)
    print("LTG_TOOL_color_verify — self-test")
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
    print("\n--- Test 2: hue drift detection (internal helpers) ---")
    target_hue = _rgb_to_hue(0, 240, 255)   # ~183.5°
    drifted_hue = _rgb_to_hue(0, 255, 180)  # ~160.0° — visibly green-cyan
    delta = _hue_delta(target_hue, drifted_hue)
    print(f"  target_hue={target_hue:.1f}°  drifted_hue={drifted_hue:.1f}°  delta={delta:.1f}°")
    assert delta > 5, f"Expected delta > 5°, got {delta:.1f}°"
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

    # --- Test 4: histogram mode (v002 new feature) ---
    print("\n--- Test 4: histogram mode (v002) ---")
    results4 = verify_canonical_colors(img_clean, palette, max_delta_hue=5, histogram=True)
    for k, v in results4.items():
        if k == "overall_pass":
            continue
        status = v.get("status", "checked")
        if status in ("not_found", "achromatic_target"):
            print(f"  {k:20s}  status={status}  (no histogram)")
            continue
        # Verify histogram keys are present
        assert "hue_histogram" in v, f"Missing hue_histogram for {k}"
        assert "histogram_bucket_deg" in v, f"Missing histogram_bucket_deg for {k}"
        assert "canonical_bucket_index" in v, f"Missing canonical_bucket_index for {k}"
        hist = v["hue_histogram"]
        bucket_deg = v["histogram_bucket_deg"]
        canonical_idx = v["canonical_bucket_index"]
        assert len(hist) == 360 // bucket_deg, f"Expected {360//bucket_deg} buckets, got {len(hist)}"
        # Canonical bucket must be marked
        assert canonical_idx is not None, f"canonical_bucket_index is None for {k}"
        assert hist[canonical_idx]["is_canonical"], f"Canonical bucket not marked for {k}"
        # Total count must equal len(hues) — all sampled chromatic pixels
        total_hist_pixels = sum(b["count"] for b in hist)
        print(f"  {k:20s}  histogram OK  buckets={len(hist)}  "
              f"canonical_bucket={canonical_idx}  "
              f"canonical_hue={v['target_hue']:.1f}°  "
              f"total_pixels_in_hist={total_hist_pixels}")
        # Show the histogram for this one color as demonstration
        if k == "ELECTRIC_CYAN":
            print(f"    Sample histogram for ELECTRIC_CYAN ({bucket_deg}° buckets):")
            print(format_histogram(hist, canonical_idx))

    assert results4["overall_pass"], "Test 4 FAILED: expected overall_pass=True"
    print("  [Test 4 PASSED — histogram mode verified]")

    # --- Test 5: histogram on drifted image shows spread across buckets ---
    print("\n--- Test 5: histogram on drifted image shows canonical bucket NOT peak ---")
    img_drift2 = Image.new("RGB", (200, 200), (0, 255, 220))  # hue ~168°, canonical ELEC_CYAN ~183°
    results5 = verify_canonical_colors(
        img_drift2,
        {"ELECTRIC_CYAN": (0, 240, 255)},
        max_delta_hue=5,
        histogram=True,
    )
    ec5 = results5.get("ELECTRIC_CYAN", {})
    if "hue_histogram" in ec5:
        hist5 = ec5["hue_histogram"]
        canonical_idx5 = ec5["canonical_bucket_index"]
        peak_idx = max(range(len(hist5)), key=lambda i: hist5[i]["count"])
        print(f"  Peak bucket index: {peak_idx} ({hist5[peak_idx]['hue_start']:.0f}–{hist5[peak_idx]['hue_end']:.0f}°, "
              f"count={hist5[peak_idx]['count']})")
        print(f"  Canonical bucket index: {canonical_idx5} "
              f"({hist5[canonical_idx5]['hue_start']:.0f}–{hist5[canonical_idx5]['hue_end']:.0f}°, "
              f"count={hist5[canonical_idx5]['count']})")
        assert peak_idx != canonical_idx5 or hist5[canonical_idx5]["count"] == 0, \
            "Test 5 WARN: peak is at canonical bucket — drift may not be obvious in histogram"
        print("  [Test 5 PASSED — histogram shows drift: peak ≠ canonical bucket]")
    else:
        print(f"  ELECTRIC_CYAN status={ec5.get('status', 'unknown')} — no histogram (not found)")

    # --- Test 6: backward compatibility — histogram=False (default) ---
    print("\n--- Test 6: backward compatibility (histogram=False) ---")
    results6 = verify_canonical_colors(img_clean, palette, max_delta_hue=5)
    for k, v in results6.items():
        if k == "overall_pass":
            continue
        assert "hue_histogram" not in v, f"hue_histogram should NOT be present when histogram=False for {k}"
    print("  [Test 6 PASSED — no histogram keys when histogram=False]")

    print("\n" + "=" * 60)
    print("All self-tests PASSED.")
    print("=" * 60)
