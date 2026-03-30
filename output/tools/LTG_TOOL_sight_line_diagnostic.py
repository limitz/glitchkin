#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sight_line_diagnostic.py
Sight-Line Diagnostic Tool — Cycle 39 (batch mode: Cycle 41)
Lee Tanaka, Character Staging & Visual Acting Specialist

Given a style frame or environment PNG, computes the sight-line from a
character's eye and checks whether it connects with a target element.

WHAT IT DOES
  1. Draws a thin CYAN ray from the eye position, in the direction of `aim_xy`,
     extending past the aim point.
  2. Draws the target area as a MAGENTA bounding box.
  3. Draws the character body axis (shoulder-to-hip) in AMBER if provided.
  4. Annotates: gaze angle (deg), miss distance (px), PASS / WARN / FAIL.
  5. Saves an annotated PNG (≤1280×1280px) as LTG_SNAP_sightline_<label>.png.

KEY CONCEPT — eye vs aim vs target
  eye_xy   : where the eye is located in the image (pixel coords)
  aim_xy   : a second point the gaze ray passes through — derived from the
             direction the pupil is facing. For a correct sight-line, aim_xy
             should be at or near target_xy. For a broken sight-line, aim_xy
             points somewhere else (e.g. straight ahead instead of toward target).
  target_xy: the actual subject the character SHOULD be looking at.

  miss_px  = perpendicular distance from target_xy to the ray defined by
             (eye_xy → aim_xy), extended to infinity.
  PASS  — miss_px ≤ threshold (default 15px)
  WARN  — miss_px ∈ (threshold, threshold×3]
  FAIL  — miss_px > threshold×3

Usage (CLI):
  python3 LTG_TOOL_sight_line_diagnostic.py \\
      --image   PATH_TO_PNG          \\
      --eye     EYE_CX  EYE_CY       \\
      --aim     AIM_CX  AIM_CY       \\
      --target  TGT_CX  TGT_CY       \\
      [--target-box  X0 Y0 X1 Y1]    \\
      [--body-top    BX  BY]          \\
      [--body-bot    BX  BY]          \\
      [--threshold   15]              \\
      [--label       "sf01_v006"]     \\
      [--output-dir  /path/to/dir]    \\
      [--no-save]

  If --aim is omitted, defaults to --target (so passing only eye+target
  checks that gaze goes directly to target — miss will be ~0px for PASS).

Batch / module usage:
  from LTG_TOOL_sight_line_diagnostic import run_sight_line_check
  result = run_sight_line_check(
      image_path  = "LTG_COLOR_styleframe_discovery.png",
      eye_xy      = (429, 427),     # eye centre pixel coords
      aim_xy      = (429, 427 - 50),  # direction ray (where eye is pointing)
                                      # If None, uses target_xy
      target_xy   = (923, 239),     # actual target centre to validate against
      target_box  = (830, 148, 1016, 330),  # optional bounding box
      body_top_xy = (412, 380),     # optional shoulder
      body_bot_xy = (371, 648),     # optional feet
      threshold   = 15,
      label       = "sf01_v006",
      output_dir  = "/home/wipkat/team/output/production",
      save        = True,
  )
  # result: {'status': 'PASS'/'WARN'/'FAIL', 'miss_px': float,
  #          'gaze_angle_deg': float, 'output_path': str|None, 'message': str}

  Tip for comparing v005 vs v006:
    v006 (fixed): eye=(429,427), aim=(923,239)  → ray goes to Byte → PASS
    v005 (broken): eye=(400,422), aim=(700,422)  → ray goes forward, misses Byte → WARN/FAIL

Batch mode (Cycle 41):
  python3 LTG_TOOL_sight_line_diagnostic.py --batch config.json [--output-dir /path]
  Reads a JSON config listing multiple check specs. Runs all checks, saves per-check
  annotated PNGs for WARN/FAIL cases, and writes a summary report.

  JSON config format:
  [
    {
      "label":       "p06_byte_luma",          // short identifier (used in filenames)
      "image":       "/path/to/panel.png",     // source image
      "eye":         [cx, cy],                 // eye origin
      "aim":         [ax, ay],                 // gaze direction point (optional)
      "target":      [tx, ty],                 // intended subject centre
      "target_box":  [x0, y0, x1, y1],        // optional bounding box
      "body_top":    [bx, by],                 // optional shoulder point
      "body_bot":    [bx, by],                 // optional hip/feet point
      "threshold":   15                        // optional miss threshold in px
    },
    ...
  ]

  If "aim" is omitted, gaze is assumed to go directly to target (miss ~0, will PASS).
  If "threshold" is omitted, uses global DEFAULT_THRESHOLD (15px).

  Summary report is printed to stdout and written to:
    <output_dir>/LTG_BATCH_sightline_summary.txt

  Annotated PNGs are saved ONLY for WARN and FAIL cases (to limit output volume).
  PASS results are included in the summary but no PNG is saved by default.
  Use --batch-save-all to save PNGs for all results including PASS.

  Exit code: 0 if all PASS, 1 if any WARN or FAIL.

BUILT-IN TESTS:
  python3 LTG_TOOL_sight_line_diagnostic.py --self-test
  python3 LTG_TOOL_sight_line_diagnostic.py --sf01-test
  python3 LTG_TOOL_sight_line_diagnostic.py --batch-self-test
"""

import argparse
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ── Constants ─────────────────────────────────────────────────────────────────
DEFAULT_THRESHOLD  = 15
OUTPUT_DIR_DEFAULT = "/home/wipkat/team/output/production"
MAX_IMAGE_PX       = 1280

COLOR_RAY        = (  0, 220, 240)   # ELEC_CYAN sight-line ray
COLOR_TARGET_BOX = (255,  45, 107)   # HOT_MAGENTA target
COLOR_BODY_AXIS  = (220, 180,  60)   # AMBER body axis
COLOR_EYE_DOT    = (255, 255,  80)   # bright yellow eye origin
COLOR_AIM_DOT    = (180, 255, 180)   # light green aim point
COLOR_PASS       = ( 60, 220,  90)
COLOR_WARN       = (220, 180,  40)
COLOR_FAIL       = (220,  60,  60)
COLOR_TEXT_BG    = ( 18,  18,  24)
COLOR_TEXT_FG    = (240, 240, 240)
RAY_EXTEND_PX    = 80   # extend ray past aim point by this many pixels


# ── Helpers ────────────────────────────────────────────────────────────────────

def _load_font(size=12, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"    if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _distance_point_to_infinite_line(px, py, ax, ay, bx, by):
    """
    Distance from point P=(px,py) to the infinite line through A and B.
    Returns (dist_px, foot_x, foot_y).
    """
    dx = bx - ax
    dy = by - ay
    seg_len_sq = dx * dx + dy * dy
    if seg_len_sq < 1e-9:
        dist = math.sqrt((px - ax) ** 2 + (py - ay) ** 2)
        return dist, ax, ay
    t = ((px - ax) * dx + (py - ay) * dy) / seg_len_sq
    foot_x = ax + t * dx
    foot_y = ay + t * dy
    dist = math.sqrt((px - foot_x) ** 2 + (py - foot_y) ** 2)
    return dist, foot_x, foot_y


def _gaze_angle_degrees(eye_cx, eye_cy, aim_cx, aim_cy):
    """Angle of gaze vector in degrees, clockwise from positive-x axis."""
    dx = aim_cx - eye_cx
    dy = aim_cy - eye_cy
    return math.degrees(math.atan2(dy, dx))


def _draw_annotated_overlay(
        img, draw,
        eye_xy, aim_xy, target_xy, target_box,
        body_top_xy, body_bot_xy,
        miss_px, gaze_angle_deg, status, threshold):
    """Draw all sight-line annotations in place. Returns updated draw."""
    ex, ey = eye_xy
    ax, ay = aim_xy
    tx, ty = target_xy
    W, H   = img.size

    # ── 1. Extend ray: eye → aim → beyond ──────────────────────────────────
    dx = ax - ex
    dy = ay - ey
    seg_len = math.sqrt(dx * dx + dy * dy)
    if seg_len < 1e-6:
        end_x, end_y = ax + RAY_EXTEND_PX, ay
    else:
        scale = (seg_len + RAY_EXTEND_PX) / seg_len
        end_x = int(ex + dx * scale)
        end_y = int(ey + dy * scale)

    # Draw ray as dashed cyan line
    n_segs = max(20, int(seg_len / 3))
    pts = [(int(ex + (end_x - ex) * i / n_segs),
            int(ey + (end_y - ey) * i / n_segs)) for i in range(n_segs + 1)]
    for i in range(0, len(pts) - 1, 2):
        draw.line([pts[i], pts[i + 1]], fill=COLOR_RAY, width=2)

    # ── 2. Eye origin dot ───────────────────────────────────────────────────
    r = 5
    draw.ellipse([ex - r, ey - r, ex + r, ey + r],
                 fill=COLOR_EYE_DOT, outline=COLOR_TEXT_BG, width=1)

    # ── 3. Aim point dot (small) ────────────────────────────────────────────
    r2 = 3
    draw.ellipse([ax - r2, ay - r2, ax + r2, ay + r2],
                 fill=COLOR_AIM_DOT, outline=COLOR_TEXT_BG, width=1)

    # ── 4. Target bounding box + cross-hair ────────────────────────────────
    if target_box is not None:
        bx0, by0, bx1, by1 = target_box
        for expand in (4, 2, 0):
            alpha = (80, 100, 255)[expand // 2] if expand > 0 else 255
            draw.rectangle([bx0 - expand, by0 - expand, bx1 + expand, by1 + expand],
                           outline=COLOR_TARGET_BOX, width=2 if expand == 0 else 1)
    draw.line([(tx - 10, ty), (tx + 10, ty)], fill=COLOR_TARGET_BOX, width=2)
    draw.line([(tx, ty - 10), (tx, ty + 10)], fill=COLOR_TARGET_BOX, width=2)

    # ── 5. Body axis ────────────────────────────────────────────────────────
    if body_top_xy is not None and body_bot_xy is not None:
        draw.line([body_top_xy, body_bot_xy], fill=COLOR_BODY_AXIS, width=2)
        for bpt in (body_top_xy, body_bot_xy):
            bpx, bpy = bpt
            draw.ellipse([bpx - 3, bpy - 3, bpx + 3, bpy + 3], fill=COLOR_BODY_AXIS)

    # ── 6. Miss indicator: perpendicular from target to ray ─────────────────
    if miss_px > 2:
        _, foot_x, foot_y = _distance_point_to_infinite_line(tx, ty, ex, ey, end_x, end_y)
        draw.line([(tx, ty), (int(foot_x), int(foot_y))],
                  fill=COLOR_TARGET_BOX, width=1)

    # ── 7. Status badge ─────────────────────────────────────────────────────
    status_color = {"PASS": COLOR_PASS, "WARN": COLOR_WARN, "FAIL": COLOR_FAIL}[status]
    font_b = _load_font(14, bold=True)
    font_s = _load_font(11)

    lines = [
        (f"  {status}  ",                                     font_b, status_color),
        (f"  miss: {miss_px:.1f}px  (threshold {threshold}px)  ", font_s, COLOR_TEXT_FG),
        (f"  gaze: {gaze_angle_deg:.1f}°  ",                   font_s, COLOR_TEXT_FG),
        (f"  eye: ({ex},{ey})  aim: ({ax},{ay})  ",             font_s, (180, 180, 200)),
        (f"  target: ({tx},{ty})  ",                            font_s, (255, 140, 180)),
    ]
    max_w = 0
    total_h = 0
    line_heights = []
    tmp_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for text, font, _ in lines:
        bb = tmp_draw.textbbox((0, 0), text, font=font)
        lw = bb[2] - bb[0]
        lh = bb[3] - bb[1] + 4
        max_w = max(max_w, lw)
        total_h += lh
        line_heights.append(lh)

    pad = 6
    badge_w = max_w + pad * 2
    badge_h = total_h + pad * 2
    bx_badge = 8 if ex > W * 0.5 else W - badge_w - 8
    by_badge = 8

    draw.rectangle([bx_badge, by_badge, bx_badge + badge_w, by_badge + badge_h],
                   fill=COLOR_TEXT_BG, outline=status_color, width=2)
    cy_text = by_badge + pad
    for (text, font, color), lh in zip(lines, line_heights):
        draw.text((bx_badge + pad, cy_text), text, fill=color, font=font)
        cy_text += lh

    # ── 8. Legend ───────────────────────────────────────────────────────────
    legend = [
        (COLOR_RAY,        "— sight-line ray  (eye → aim)"),
        (COLOR_TARGET_BOX, "— target subject  (magenta)"),
        (COLOR_EYE_DOT,    "● eye origin"),
        (COLOR_AIM_DOT,    "● aim point"),
    ]
    if body_top_xy is not None:
        legend.insert(2, (COLOR_BODY_AXIS, "— body axis"))

    leg_font = _load_font(10)
    leg_y = by_badge + badge_h + 4
    for leg_color, leg_text in legend:
        draw.text((bx_badge + 4, leg_y), leg_text, fill=leg_color, font=leg_font)
        bb = draw.textbbox((bx_badge + 4, leg_y), leg_text, font=leg_font)
        leg_y += (bb[3] - bb[1]) + 3

    return draw


# ── Core function ──────────────────────────────────────────────────────────────

def run_sight_line_check(
        image_path,
        eye_xy,
        target_xy,
        aim_xy=None,
        target_box=None,
        body_top_xy=None,
        body_bot_xy=None,
        threshold=DEFAULT_THRESHOLD,
        label="check",
        output_dir=OUTPUT_DIR_DEFAULT,
        save=True,
):
    """
    Run a sight-line diagnostic and optionally save an annotated PNG.

    Parameters
    ----------
    image_path  : str    Path to source PNG/JPG.
    eye_xy      : (int, int)   Eye centre pixel coords.
    target_xy   : (int, int)   Actual target/subject centre pixel coords.
    aim_xy      : (int, int) or None
                  The direction the character is ACTUALLY gazing toward.
                  If None, defaults to target_xy (gaze assumed correct).
                  Set to a DIFFERENT point to test a broken/off-axis gaze.
    target_box  : (x0, y0, x1, y1) or None  Target bounding box.
    body_top_xy : (int, int) or None  Shoulder point for body axis annotation.
    body_bot_xy : (int, int) or None  Feet/hip point for body axis annotation.
    threshold   : int    Miss distance threshold in px (default 15).
    label       : str    Short label for output filename.
    output_dir  : str    Output PNG directory.
    save        : bool   Save annotated PNG if True.

    Returns
    -------
    dict:  status, miss_px, gaze_angle_deg, output_path, message
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = Image.open(image_path).convert("RGB")
    if img.width > MAX_IMAGE_PX or img.height > MAX_IMAGE_PX:
        img.thumbnail((MAX_IMAGE_PX, MAX_IMAGE_PX), Image.LANCZOS)

    # If aim_xy not provided, default to target_xy (gaze assumed correct → miss~0)
    if aim_xy is None:
        aim_xy = target_xy

    draw  = ImageDraw.Draw(img)
    ex, ey = eye_xy
    ax, ay = aim_xy
    tx, ty = target_xy

    # Extend ray for miss calculation
    dx = ax - ex
    dy = ay - ey
    seg_len = math.sqrt(dx * dx + dy * dy)
    if seg_len < 1e-6:
        end_x, end_y = ax + RAY_EXTEND_PX, ay
    else:
        scale = (seg_len + RAY_EXTEND_PX) / seg_len
        end_x = int(ex + dx * scale)
        end_y = int(ey + dy * scale)

    gaze_angle_deg = _gaze_angle_degrees(ex, ey, ax, ay)
    miss_px, _, _  = _distance_point_to_infinite_line(tx, ty, ex, ey, end_x, end_y)

    if miss_px <= threshold:
        status = "PASS"
    elif miss_px <= threshold * 3:
        status = "WARN"
    else:
        status = "FAIL"

    draw = _draw_annotated_overlay(
        img, draw,
        eye_xy=eye_xy, aim_xy=aim_xy, target_xy=target_xy,
        target_box=target_box,
        body_top_xy=body_top_xy, body_bot_xy=body_bot_xy,
        miss_px=miss_px, gaze_angle_deg=gaze_angle_deg,
        status=status, threshold=threshold,
    )

    output_path = None
    if save:
        os.makedirs(output_dir, exist_ok=True)
        safe_label = label.replace("/", "_").replace(" ", "_")
        output_path = os.path.join(output_dir, f"LTG_SNAP_sightline_{safe_label}.png")
        img.thumbnail((MAX_IMAGE_PX, MAX_IMAGE_PX), Image.LANCZOS)
        img.save(output_path, "PNG")
        print(f"Saved: {output_path}  ({img.width}×{img.height}px)")

    message = (f"{status} — miss {miss_px:.1f}px (threshold {threshold}px), "
               f"gaze {gaze_angle_deg:.1f}°")
    print(f"  {message}")

    return {
        "status":         status,
        "miss_px":        miss_px,
        "gaze_angle_deg": gaze_angle_deg,
        "output_path":    output_path,
        "message":        message,
    }


# ── Batch mode ────────────────────────────────────────────────────────────────

def run_batch(config_path, output_dir=OUTPUT_DIR_DEFAULT, save_all=False):
    """
    Run multiple sight-line checks from a JSON config file.

    Parameters
    ----------
    config_path : str   Path to JSON config file (list of check specs).
    output_dir  : str   Directory for annotated PNGs and summary report.
    save_all    : bool  If True, save PNGs even for PASS results.
                        Default: only WARN/FAIL get PNGs.

    Returns
    -------
    dict: {
        'results': list of per-check result dicts (each has all run_sight_line_check keys
                   plus 'label', 'image_path'),
        'n_pass':  int,
        'n_warn':  int,
        'n_fail':  int,
        'all_pass': bool,
        'summary_path': str,   path to written summary .txt
    }
    """
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Batch config not found: {config_path}")

    with open(config_path, "r") as fh:
        specs = json.load(fh)

    if not isinstance(specs, list):
        raise ValueError("Batch config must be a JSON array of check spec objects.")

    os.makedirs(output_dir, exist_ok=True)

    results = []
    n_pass = n_warn = n_fail = 0

    print(f"\n── Batch sight-line run: {len(specs)} check(s) ──────────────────────")

    for i, spec in enumerate(specs):
        label      = spec.get("label", f"check_{i:03d}")
        image_path = spec.get("image")
        eye_xy     = tuple(spec["eye"])
        target_xy  = tuple(spec["target"])
        aim_xy     = tuple(spec["aim"])       if "aim"        in spec else None
        target_box = tuple(spec["target_box"]) if "target_box" in spec else None
        body_top   = tuple(spec["body_top"])  if "body_top"   in spec else None
        body_bot   = tuple(spec["body_bot"])  if "body_bot"   in spec else None
        threshold  = int(spec.get("threshold", DEFAULT_THRESHOLD))

        print(f"\n  [{i+1}/{len(specs)}] {label}")

        if not image_path:
            print(f"    SKIP — 'image' field missing in spec.")
            result = {
                "label":        label,
                "image_path":   None,
                "status":       "SKIP",
                "miss_px":      None,
                "gaze_angle_deg": None,
                "output_path":  None,
                "message":      "SKIP — no image specified",
            }
            results.append(result)
            continue

        if not os.path.isfile(image_path):
            print(f"    SKIP — image not found: {image_path}")
            result = {
                "label":        label,
                "image_path":   image_path,
                "status":       "SKIP",
                "miss_px":      None,
                "gaze_angle_deg": None,
                "output_path":  None,
                "message":      f"SKIP — image not found: {image_path}",
            }
            results.append(result)
            continue

        # Always save on first pass; delete PASS output afterward if not save_all
        r = run_sight_line_check(
            image_path  = image_path,
            eye_xy      = eye_xy,
            aim_xy      = aim_xy,
            target_xy   = target_xy,
            target_box  = target_box,
            body_top_xy = body_top,
            body_bot_xy = body_bot,
            threshold   = threshold,
            label       = label,
            output_dir  = output_dir,
            save        = True,
        )

        # Remove PASS PNGs unless caller wants all saved
        if not save_all and r["status"] == "PASS" and r.get("output_path") and os.path.isfile(r["output_path"]):
            try:
                os.remove(r["output_path"])
                r["output_path"] = None
            except OSError:
                pass

        r["label"]      = label
        r["image_path"] = image_path
        results.append(r)

        if r["status"] == "PASS":
            n_pass += 1
        elif r["status"] == "WARN":
            n_warn += 1
        elif r["status"] == "FAIL":
            n_fail += 1

    # ── Summary report ─────────────────────────────────────────────────────────
    lines = [
        "LTG Batch Sight-Line Diagnostic — Summary",
        f"Config: {config_path}",
        f"Run: {len(specs)} checks | PASS: {n_pass} | WARN: {n_warn} | FAIL: {n_fail}",
        "",
        f"{'#':<4}  {'Label':<30}  {'Status':<6}  {'Miss':>8}  {'Angle':>8}  Notes",
        "-" * 75,
    ]
    for i, r in enumerate(results):
        status   = r.get("status", "?")
        miss     = f"{r['miss_px']:.1f}px"   if r.get("miss_px")         is not None else "—"
        angle    = f"{r['gaze_angle_deg']:.1f}°" if r.get("gaze_angle_deg") is not None else "—"
        saved    = f"  → {r['output_path']}" if r.get("output_path") else ""
        lines.append(f"  {i+1:<3}  {r.get('label','?'):<30}  {status:<6}  {miss:>8}  {angle:>8}{saved}")

    lines += [
        "",
        "WARN/FAIL details:",
    ]
    has_issues = False
    for r in results:
        if r.get("status") in ("WARN", "FAIL"):
            has_issues = True
            lines.append(f"  [{r['status']}] {r.get('label','?')}: {r.get('message','')}")
            if r.get("output_path"):
                lines.append(f"         annotated PNG → {r['output_path']}")
    if not has_issues:
        lines.append("  (none)")

    summary_text = "\n".join(lines) + "\n"
    print("\n" + summary_text)

    summary_path = os.path.join(output_dir, "LTG_BATCH_sightline_summary.txt")
    with open(summary_path, "w") as fh:
        fh.write(summary_text)
    print(f"Summary written: {summary_path}")

    return {
        "results":      results,
        "n_pass":       n_pass,
        "n_warn":       n_warn,
        "n_fail":       n_fail,
        "all_pass":     (n_fail == 0 and n_warn == 0),
        "summary_path": summary_path,
    }


def _batch_self_test(output_dir=OUTPUT_DIR_DEFAULT):
    """
    Build a synthetic batch config and run it through run_batch().
    Uses temporary image files; verifies PASS/WARN/FAIL counts.
    """
    import tempfile

    W_T, H_T = 640, 360
    TARGET = (440, 200)
    TARGET_BOX = (420, 180, 460, 220)

    # Build 3 synthetic PNGs (same as _self_test cases)
    cases = [
        ("batch_pass", (100, 200), (440, 200)),
        ("batch_warn", (100, 200), (640, 225)),
        ("batch_fail", (100, 200), (640, 290)),
    ]

    tmp_paths = []
    config_entries = []

    for label, eye_xy, aim_xy in cases:
        img = Image.new("RGB", (W_T, H_T), (28, 22, 40))
        d = ImageDraw.Draw(img)
        tx, ty = TARGET
        d.ellipse([tx - 30, ty - 40, tx + 30, ty + 40], fill=(0, 100, 130),
                  outline=(0, 200, 220), width=2)
        d.text((8, 8), f"BATCH SYNTHETIC: {label.upper()}", fill=(160, 160, 180),
               font=_load_font(11))
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img.save(tmp.name)
        tmp.close()
        tmp_paths.append(tmp.name)
        config_entries.append({
            "label":      label,
            "image":      tmp.name,
            "eye":        list(eye_xy),
            "aim":        list(aim_xy),
            "target":     list(TARGET),
            "target_box": list(TARGET_BOX),
            "threshold":  DEFAULT_THRESHOLD,
        })

    # Write config JSON to a temp file
    cfg_tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(config_entries, cfg_tmp)
    cfg_tmp.close()

    print("\n── Batch self-test ───────────────────────────────────────────────")
    print(f"Config: {cfg_tmp.name}")
    summary = run_batch(cfg_tmp.name, output_dir=output_dir, save_all=False)

    # Clean up temp source files
    for p in tmp_paths:
        try:
            os.unlink(p)
        except OSError:
            pass
    try:
        os.unlink(cfg_tmp.name)
    except OSError:
        pass

    expected = {"batch_pass": "PASS", "batch_warn": "WARN", "batch_fail": "FAIL"}
    all_ok = True
    print("\n── Batch self-test results ───────────────────────────────────────")
    for r in summary["results"]:
        exp = expected.get(r["label"], "?")
        got = r["status"]
        ok  = (got == exp)
        mark = "OK" if ok else "UNEXPECTED"
        print(f"  [{mark}] {r['label']}: expected {exp}, got {got}")
        if not ok:
            all_ok = False

    expected_counts = (1, 1, 1)  # pass, warn, fail
    got_counts = (summary["n_pass"], summary["n_warn"], summary["n_fail"])
    if expected_counts != got_counts:
        print(f"  [UNEXPECTED] counts: expected {expected_counts}, got {got_counts}")
        all_ok = False
    else:
        print(f"  [OK] counts: PASS={summary['n_pass']}, WARN={summary['n_warn']}, FAIL={summary['n_fail']}")

    if all_ok:
        print("  All batch self-tests PASSED.")
    else:
        print("  Some batch self-tests produced unexpected results.")

    return all_ok


# ── Self-test (synthetic images, no style frame required) ─────────────────────

def _self_test(output_dir=OUTPUT_DIR_DEFAULT):
    """
    Three synthetic test cases:
      PASS: eye at (100,200), aim at (440,200) → ray is horizontal,
            target at (440,200) is on ray → miss=0
      WARN: eye at (100,200), aim at (640,225) → ray slopes slightly down,
            target fixed at (440,200) → miss ≈ 22px (> 15, < 45)
      FAIL: eye at (100,200), aim at (640,270) → ray slopes more,
            target fixed at (440,200) → miss ≈ 60px (> 45)
    """
    import tempfile

    W_T, H_T = 640, 360
    TARGET = (440, 200)
    TARGET_BOX = (420, 180, 460, 220)

    cases = [
        ("pass", (100, 200), (440, 200)),   # aim = target → miss=0
        ("warn", (100, 200), (640, 225)),   # aim drifts below → miss~22px
        ("fail", (100, 200), (640, 290)),   # aim drifts far below → miss~65px
    ]
    expected = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}

    results = []
    for label, eye_xy, aim_xy in cases:
        img = Image.new("RGB", (W_T, H_T), (28, 22, 40))
        d = ImageDraw.Draw(img)
        # Simple background — a "Byte-like" circle at target position
        tx, ty = TARGET
        d.ellipse([tx - 30, ty - 40, tx + 30, ty + 40], fill=(0, 100, 130),
                   outline=(0, 200, 220), width=2)
        d.text((8, 8), f"SYNTHETIC TEST: {label.upper()}", fill=(160, 160, 180),
               font=_load_font(11))

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
        img.save(tmp_path)

        # Compute expected miss manually for verification
        ex, ey = eye_xy
        ax, ay = aim_xy
        dx, dy = ax - ex, ay - ey
        seg_len = math.sqrt(dx**2 + dy**2)
        end_x = int(ex + dx * (seg_len + RAY_EXTEND_PX) / seg_len)
        end_y = int(ey + dy * (seg_len + RAY_EXTEND_PX) / seg_len)
        miss_expected, _, _ = _distance_point_to_infinite_line(
            TARGET[0], TARGET[1], ex, ey, end_x, end_y)
        print(f"\n  [{label}] expected miss ≈ {miss_expected:.1f}px  "
              f"(expecting {expected[label]})")

        result = run_sight_line_check(
            image_path  = tmp_path,
            eye_xy      = eye_xy,
            aim_xy      = aim_xy,
            target_xy   = TARGET,
            target_box  = TARGET_BOX,
            body_top_xy = (eye_xy[0], eye_xy[1] - 20),
            body_bot_xy = (eye_xy[0], eye_xy[1] + 100),
            threshold   = DEFAULT_THRESHOLD,
            label       = f"selftest_{label}",
            output_dir  = output_dir,
            save        = True,
        )
        results.append((label, result["status"], result["miss_px"]))
        os.unlink(tmp_path)

    print("\n── Self-test summary ─────────────────────────────────────────────")
    all_ok = True
    for label, got, miss in results:
        exp = expected[label]
        ok  = (got == exp)
        mark = "OK" if ok else "UNEXPECTED"
        print(f"  [{mark}] {label}: expected {exp}, got {got} (miss={miss:.1f}px)")
        if not ok:
            all_ok = False
    if all_ok:
        print("  All self-tests PASSED.")
    else:
        print("  Some self-tests produced unexpected results.")
    return all_ok


# ── SF01 v005 vs v006 comparison test ─────────────────────────────────────────

def _run_sf01_tests(output_dir=OUTPUT_DIR_DEFAULT):
    """
    Tests the sight-line on SF01 v006 (should PASS — sight-line was fixed)
    and SF01 v005 (should WARN/FAIL — sight-line was broken).

    Coordinate derivation for 1280×720 canvas:
    ─────────────────────────────────────────────────────────────────────────
    SX = SY = SP = 1280/1920 = 2/3 ≈ 0.6667

    TARGET (Byte/emerge position on CRT screen):
      mw_x     = int(1920*0.50 * SX)      = 640
      mw_w     = int(1920*0.46 * SX)      ≈ 589
      mw_h     = int(1080*0.57 * SY)      ≈ 410
      ceiling_y= int(1080*0.12 * SY)      ≈ 86
      mw_y     = ceiling_y                = 86
      crt_x    = mw_x + int(mw_w*0.22)   ≈ 640 + 130 = 770
      crt_w    = int(mw_w*0.52)           ≈ 306
      crt_h    = int(mw_h*0.62)           ≈ 254
      crt_y    = mw_y + int(mw_h*0.08)   ≈ 86 + 33 = 119
      scr_pad  = int(24 * SP)             ≈ 16
      scr_x0   = crt_x + scr_pad         ≈ 786
      scr_x1   = crt_x + crt_w - scr_pad ≈ 1060
      scr_y0   = crt_y + scr_pad         ≈ 135
      scr_y1   = crt_y + crt_h - scr_pad*2 ≈ 339
      emerge_cx= (786+1060)//2            = 923
      emerge_cy= (135+339)//2             = 237
      emerge_rx= int((scr_x1-scr_x0)*0.34)= int(274*0.34) = 93
      emerge_ry= int((scr_y1-scr_y0)*0.44)= int(204*0.44) = 89
      byte_cy  = emerge_cy - int(emerge_ry*0.20) ≈ 237 - 18 = 219
      TARGET   = (923, 219)   (Byte body centre)

    EYE v006 (sight-line FIXED — head turned toward screen):
      luma_cx   = int(1920*0.29 * SX)     ≈ 371
      lean_offset = int(44 * SP)          ≈ 29
      scale     = 0.92; p(n)= int(n*0.92*SP) = int(n*0.6133)
      head_cx_body = luma_cx + lean_offset = 400
      head_gaze_offset = int(18 * SP)     ≈ 12
      head_cx   = 400 + 12                = 412
      luma_base_y = int(1080*0.90 * SY)  ≈ 648
      torso_top = luma_base_y - p(260)    ≈ 648 - 159 = 489
        [p(260)=int(260*0.6133)≈159]
      head_cy_body = torso_top - p(70)    ≈ 489 - 43 = 446
        [p(70)=int(70*0.6133)≈43]
      head_cy   = head_cy_body + p(6)     ≈ 446 + 4 = 450
        [p(6)=int(6*0.6133)≈4]
      lex (L-eye cx) = head_cx + p(4)    ≈ 412 + 2 = 414
      ley (L-eye cy) = head_cy - p(10)   ≈ 450 - 6 = 444
      rex (R-eye cx) = head_cx + p(38)   ≈ 412 + 23 = 435
      rey (R-eye cy) = head_cy - p(8)    ≈ 450 - 5 = 445
      pupil_shift    = p(8)              ≈ 5
      L-pupil cx  = lex + pupil_shift    = 419
      R-pupil cx  = rex + pupil_shift    = 440
      Eye centre (midpoint of pupils)    = ((419+440)//2, 444) = (429, 444)
      AIM v006 = TARGET = (923, 219)     (head turned directly toward Byte)

    EYE v005 (sight-line BROKEN — eyes NOT turned toward screen):
      head_cx  = luma_cx + lean_offset   = 400  (no gaze offset)
      head_cy  = torso_top - p(70)       ≈ 489 - 43 = 446  (no +p(6))
      lex_v005 = head_cx - p(26)         ≈ 400 - 16 = 384
      ley_v005 = head_cy - p(10)         ≈ 446 - 6 = 440
      rex_v005 = head_cx + p(28)         ≈ 400 + 17 = 417
      Eye centre (v005 midpoint)         = ((384+417)//2, 440) = (400, 440)
      AIM v005 = pupils NOT shifted toward Byte.
        In v005 pupils are centred in iris (no right-shift).
        Gaze direction: straight forward or slightly right but NOT toward CRT.
        Approximate aim: (400 + 200, 440) = (600, 440) — looking "forward",
        not at the CRT which is at right ~920px.
    ─────────────────────────────────────────────────────────────────────────
    """
    print("\n── SF01 sight-line tests ─────────────────────────────────────────")

    SF01_V006 = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_discovery.png"
    SF01_V005 = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_discovery.png"

    # Byte position (emerge from CRT screen)
    target_xy  = (923, 219)
    target_box = (923 - 93, 219 - 89, 923 + 93, 219 + 89)

    # v006 test — sight-line fixed, expect PASS
    print("\n  SF01 v006 (sight-line fixed — expect PASS):")
    if os.path.isfile(SF01_V006):
        result_v6 = run_sight_line_check(
            image_path  = SF01_V006,
            eye_xy      = (429, 444),
            aim_xy      = (923, 219),        # aimed directly at Byte — PASS
            target_xy   = target_xy,
            target_box  = target_box,
            body_top_xy = (412, 420),
            body_bot_xy = (371, 648),
            threshold   = DEFAULT_THRESHOLD,
            label       = "sf01_v006",
            output_dir  = output_dir,
            save        = True,
        )
    else:
        print(f"  SKIP: {SF01_V006} not found.")
        result_v6 = None

    # v005 test — sight-line broken, expect WARN or FAIL
    print("\n  SF01 v005 (sight-line broken — expect WARN/FAIL):")
    if os.path.isfile(SF01_V005):
        result_v5 = run_sight_line_check(
            image_path  = SF01_V005,
            eye_xy      = (400, 440),
            aim_xy      = (600, 440),        # looking "forward" — not toward Byte
            target_xy   = target_xy,
            target_box  = target_box,
            body_top_xy = (400, 415),
            body_bot_xy = (371, 648),
            threshold   = DEFAULT_THRESHOLD,
            label       = "sf01_v005",
            output_dir  = output_dir,
            save        = True,
        )
    else:
        print(f"  SKIP: {SF01_V005} not found.")
        result_v5 = None

    print("\n── SF01 results ──────────────────────────────────────────────────")
    if result_v6:
        ok6 = (result_v6["status"] == "PASS")
        print(f"  v006: {result_v6['status']}  miss={result_v6['miss_px']:.1f}px  {'OK' if ok6 else 'UNEXPECTED'}")
    if result_v5:
        ok5 = (result_v5["status"] in ("WARN", "FAIL"))
        print(f"  v005: {result_v5['status']}  miss={result_v5['miss_px']:.1f}px  {'OK' if ok5 else 'UNEXPECTED'}")


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="LTG Sight-Line Diagnostic Tool v002 — Cycle 39/41",
    )
    parser.add_argument("--image",           type=str)
    parser.add_argument("--eye",             type=int, nargs=2, metavar=("CX", "CY"))
    parser.add_argument("--aim",             type=int, nargs=2, metavar=("AX", "AY"),
                        help="Gaze aim direction point (defaults to --target)")
    parser.add_argument("--target",          type=int, nargs=2, metavar=("TX", "TY"))
    parser.add_argument("--target-box",      type=int, nargs=4, metavar=("X0", "Y0", "X1", "Y1"))
    parser.add_argument("--body-top",        type=int, nargs=2, metavar=("BX", "BY"))
    parser.add_argument("--body-bot",        type=int, nargs=2, metavar=("BX", "BY"))
    parser.add_argument("--threshold",       type=int, default=DEFAULT_THRESHOLD)
    parser.add_argument("--label",           type=str, default="check")
    parser.add_argument("--output-dir",      type=str, default=OUTPUT_DIR_DEFAULT)
    parser.add_argument("--no-save",         action="store_true")
    parser.add_argument("--self-test",       action="store_true")
    parser.add_argument("--sf01-test",       action="store_true")
    # Batch mode (Cycle 41)
    parser.add_argument("--batch",           type=str, metavar="CONFIG_JSON",
                        help="Run batch mode from a JSON config file.")
    parser.add_argument("--batch-save-all",  action="store_true",
                        help="In batch mode, save annotated PNGs for PASS results too.")
    parser.add_argument("--batch-self-test", action="store_true",
                        help="Run the synthetic batch self-test.")

    args = parser.parse_args()

    if args.self_test:
        ok = _self_test(output_dir=args.output_dir)
        sys.exit(0 if ok else 1)

    if args.sf01_test:
        _run_sf01_tests(output_dir=args.output_dir)
        sys.exit(0)

    if args.batch_self_test:
        ok = _batch_self_test(output_dir=args.output_dir)
        sys.exit(0 if ok else 1)

    if args.batch:
        summary = run_batch(
            config_path = args.batch,
            output_dir  = args.output_dir,
            save_all    = args.batch_save_all,
        )
        sys.exit(0 if summary["all_pass"] else 1)

    if not args.image or not args.eye or not args.target:
        parser.print_help()
        print("\nERROR: --image, --eye, and --target are required (or use --batch CONFIG).",
              file=sys.stderr)
        sys.exit(1)

    result = run_sight_line_check(
        image_path  = args.image,
        eye_xy      = tuple(args.eye),
        aim_xy      = tuple(args.aim) if args.aim else None,
        target_xy   = tuple(args.target),
        target_box  = tuple(args.target_box) if args.target_box else None,
        body_top_xy = tuple(args.body_top) if args.body_top else None,
        body_bot_xy = tuple(args.body_bot) if args.body_bot else None,
        threshold   = args.threshold,
        label       = args.label,
        output_dir  = args.output_dir,
        save        = not args.no_save,
    )
    sys.exit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
