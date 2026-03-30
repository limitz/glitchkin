#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_bodypart_hierarchy.py
Body-Part Color-Index Hierarchy Tool — v002
"Luma & the Glitchkin" — Cycle 39–40 / Maya Santos

PURPOSE:
  Assigns a color-index ID to each character body part in a character sprite
  or expression panel. Scans each horizontal and vertical scan line and lists
  the color-index transitions. Detects hierarchy violations (e.g., an eye pixel
  appearing inside/under a hair polygon = "eye inside hair").

  Key use case: catching "eye inside hair" rendering issues in Luma expressions
  where the hair cloud is drawn OVER the eye area but the eye circle's overdraw
  misses some pixels.

COLOR INDEX SCHEME (Luma-focused, adaptable):
  Each body part is identified by its canonical color(s) with a per-channel
  tolerance. Parts with multiple colors are collapsed to the same index.

  Index 0  — BACKGROUND (panel BG, detected automatically by corner sampling)
  Index 1  — OUTLINE / LINE (dark brown-black: ~(59,40,32))
  Index 2  — SKIN (warm mid-brown: ~(200,136,90))
  Index 3  — SKIN_SHADOW (darker warm: ~(160,104,64))
  Index 4  — SKIN_HIGHLIGHT (lighter warm: ~(223,160,112))
  Index 5  — HAIR (near-black warm: ~(26,15,10))
  Index 6  — HAIR_HIGHLIGHT (~(61,31,15))
  Index 7  — EYE_WHITE (~(250,240,220))
  Index 8  — EYE_IRIS (~(200,125,62))
  Index 9  — EYE_PUPIL (~(59,40,32)) — often same as LINE
  Index 10 — EYE_HIGHLIGHT (~(240,240,240))
  Index 11 — BLUSH (~(232,148,100))
  Index 12 — HOODIE (orange family: ~(232,112,42))
  Index 13 — HOODIE_SHADOW (~(184,74,32))
  Index 14 — HOODIE_HIGHLIGHT (~(245,144,80))
  Index 15 — PANTS (dark indigo: ~(42,40,80))
  Index 16 — SHOE (~(245,232,208))
  Index 17 — SHOE_SOLE (~(199,91,57))
  Index 18 — PIXEL_ACCENT (cyan/magenta hoodie pixels: cyan=(0,240,255), magenta=(255,45,107))
  Index 99 — UNKNOWN (does not match any registered part)

HIERARCHY RULES:
  Hair (5,6) must NOT appear inside the bounding box of Eye (7,8,9,10).
  Eye (7,8,9,10) must NOT appear inside a pure Hair (5,6) horizontal run.
  Any UNKNOWN pixel inside the head bounding box → flag for review.

  A "bounding box" violation: if any eye-index pixel has a hair-index pixel
  directly above it in the same column within the head region, that's an
  "eye under hair" violation (hair is drawn on top of eye).

  A "scan-line run violation": if on any horizontal scan line, the transition
  sequence within the head region is:
    ... HAIR ... EYE ... HAIR ...
  that means the eye is punched through hair, which is fine —
  BUT if the sequence is:
    ... EYE ... HAIR ... EYE ...
  or there is a single stray hair pixel embedded inside a contiguous eye run,
  that is a rendering artifact.

USAGE:
  python3 LTG_TOOL_bodypart_hierarchy.py <image.png>
          [--palette luma|byte|cosmo|custom]
          [--tolerance 25]
          [--panel N]
          [--grid COLSxROWS]
          [--head-region x0,y0,x1,y1]
          [--output-annotated annotated.png]
          [--output-csv transitions.csv]
          [--verbose]
          [--chain --char NAME --expr EXPR]

  <image.png>             Character panel or expression sheet panel PNG.
                          Ignored when using --chain (source image derived from
                          expression_isolator output).
  --palette               Use named character palette (default: luma)
  --tolerance             Per-channel tolerance for color matching (default: 25)
  --panel N               Auto-crop to panel index N (0-based, left-to-right,
                          top-to-bottom) before running analysis. Eliminates
                          UNKNOWN_IN_HEAD inflation from label text and panel
                          borders on full expression sheets.
                          Use --grid to specify sheet dimensions (default: 3x3).
  --grid COLSxROWS        Grid layout when using --panel N (default: 3x3).
                          Example: --grid 4x3 for a 4-column, 3-row sheet.
  --head-region           Optional: restrict analysis to a pixel region (x0,y0,x1,y1)
                          If not specified: auto-detect head bounding box from
                          HAIR + SKIN + EYE pixels in upper 50% of image
  --output-annotated      Save annotated image with colored body-part overlay
  --output-csv            Save scan-line transition CSV
  --verbose               Print full transition table to stdout
  --chain                 Pipeline mode: run expression_isolator first to extract
                          the expression at 800x800px, then run hierarchy on that
                          output. Use with --char and --expr.
  --char NAME             Character name for --chain mode (luma|byte|cosmo)
  --expr EXPR             Expression name for --chain mode (e.g. "THE NOTICING")

OUTPUT:
  PASS/WARN/FAIL with pixel coordinates of any violations.
  FAIL: eye pixels embedded in hair (rendering defect — fix immediately)
  WARN: unknown pixels inside head region (check manually)
  PASS: hierarchy clean

Author: Maya Santos
Cycle: 39
Date: 2026-03-29
"""

import argparse
import csv
import os
import sys
from collections import defaultdict
from PIL import Image, ImageDraw

# ── Color index registry ───────────────────────────────────────────────────────

# Format: index → (name, list_of_rgb_tuples)
# Pixels are classified to the nearest registered color within tolerance.

LUMA_PALETTE = {
    0:  ("BACKGROUND",       []),                              # auto-detected
    1:  ("OUTLINE",          [(59, 40, 32)]),
    2:  ("SKIN",             [(200, 136, 90)]),
    3:  ("SKIN_SHADOW",      [(160, 104, 64)]),
    4:  ("SKIN_HIGHLIGHT",   [(223, 160, 112)]),
    5:  ("HAIR",             [(26, 15, 10)]),
    6:  ("HAIR_HIGHLIGHT",   [(61, 31, 15)]),
    7:  ("EYE_WHITE",        [(250, 240, 220)]),
    8:  ("EYE_IRIS",         [(200, 125, 62)]),
    9:  ("EYE_PUPIL",        [(59, 40, 32)]),    # overlaps OUTLINE
    10: ("EYE_HIGHLIGHT",    [(240, 240, 240)]),
    11: ("BLUSH",            [(232, 148, 100)]),
    12: ("HOODIE",           [(232, 112, 42), (150, 175, 200), (155, 85, 45),
                               (80, 100, 140), (135, 75, 65), (105, 128, 162),
                               (112, 124, 152)]),
    13: ("HOODIE_SHADOW",    [(184, 74, 32)]),
    14: ("HOODIE_HIGHLIGHT", [(245, 144, 80)]),
    15: ("PANTS",            [(42, 40, 80), (26, 24, 48)]),
    16: ("SHOE",             [(245, 232, 208)]),
    17: ("SHOE_SOLE",        [(199, 91, 57)]),
    18: ("PIXEL_ACCENT",     [(0, 240, 255), (255, 45, 107), (255, 45, 120)]),
    99: ("UNKNOWN",          []),
}

# Visualization colors for annotated output (index → display RGB)
INDEX_DISPLAY_COLORS = {
    0:  (230, 225, 215),    # BG — pale
    1:  (80,  60,  40),     # OUTLINE — dark brown
    2:  (200, 136, 90),     # SKIN
    3:  (160, 104, 64),     # SKIN_SHADOW
    4:  (223, 160, 112),    # SKIN_HIGHLIGHT
    5:  (26,  15,  10),     # HAIR — very dark
    6:  (80,  50,  25),     # HAIR_HIGHLIGHT
    7:  (220, 210, 180),    # EYE_WHITE
    8:  (180, 100, 40),     # EYE_IRIS
    9:  (80,  60,  40),     # EYE_PUPIL
    10: (255, 255, 240),    # EYE_HIGHLIGHT
    11: (232, 148, 100),    # BLUSH
    12: (232, 112, 42),     # HOODIE
    13: (184, 74,  32),     # HOODIE_SHADOW
    14: (245, 144, 80),     # HOODIE_HIGHLIGHT
    15: (60,  58,  100),    # PANTS
    16: (210, 200, 170),    # SHOE
    17: (199, 91,  57),     # SHOE_SOLE
    18: (0,   220, 255),    # PIXEL_ACCENT
    99: (255, 0,   255),    # UNKNOWN — magenta flag
}

# Hierarchy group definitions (used in violation detection)
HAIR_INDICES  = {5, 6}
EYE_INDICES   = {7, 8, 9, 10}
SKIN_INDICES  = {2, 3, 4, 11}
HEAD_INDICES  = HAIR_INDICES | EYE_INDICES | SKIN_INDICES | {1}  # everything head-related


def _color_distance(p: tuple, ref: tuple) -> float:
    """Per-channel L1 distance."""
    return max(abs(int(p[c]) - int(ref[c])) for c in range(3))


def classify_pixel(p: tuple, palette: dict, tolerance: int, bg_color: tuple) -> int:
    """
    Classify a pixel tuple (r,g,b) to a palette index.
    Returns index of best match within tolerance, or 99 (UNKNOWN).
    Returns 0 (BACKGROUND) if within tolerance of bg_color.
    """
    if _color_distance(p, bg_color) <= tolerance:
        return 0

    best_idx  = 99
    best_dist = tolerance + 1

    for idx, (name, colors) in palette.items():
        if idx in (0, 99):
            continue
        for ref in colors:
            d = _color_distance(p, ref)
            if d < best_dist:
                best_dist = d
                best_idx  = idx

    return best_idx if best_dist <= tolerance else 99


def sample_bg_color(img: Image.Image, sample_size: int = 8) -> tuple:
    """Sample corner pixels to detect panel background color."""
    arr = img.load()
    w, h = img.size
    s = sample_size
    samples = []
    for cx, cy in [(0, 0), (w - s, 0), (0, h - s), (w - s, h - s)]:
        for dx in range(s):
            for dy in range(s):
                x = min(cx + dx, w - 1)
                y = min(cy + dy, h - 1)
                px = arr[x, y]
                samples.append(px[:3])
    r_vals = sorted(p[0] for p in samples)
    g_vals = sorted(p[1] for p in samples)
    b_vals = sorted(p[2] for p in samples)
    mid = len(r_vals) // 2
    return (r_vals[mid], g_vals[mid], b_vals[mid])


def build_index_map(img: Image.Image, palette: dict, tolerance: int, bg_color: tuple):
    """
    Build a 2D list of palette indices for every pixel in the image.
    Returns (index_map, width, height).
    """
    rgb = img.convert("RGB")
    w, h = rgb.size
    arr  = rgb.load()
    idx_map = [[0] * w for _ in range(h)]

    for y in range(h):
        for x in range(w):
            p = arr[x, y][:3]
            idx_map[y][x] = classify_pixel(p, palette, tolerance, bg_color)

    return idx_map, w, h


def detect_head_region(idx_map, w, h):
    """
    Auto-detect head bounding box from HAIR + EYE + SKIN pixels
    in the upper 55% of the image.
    Returns (x0, y0, x1, y1) or None if insufficient pixels found.
    """
    head_y_limit = int(h * 0.55)
    xs = []
    ys = []
    for y in range(head_y_limit):
        for x in range(w):
            if idx_map[y][x] in HEAD_INDICES:
                xs.append(x)
                ys.append(y)

    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def scan_transitions(idx_map, w, h, palette, x0=0, y0=0, x1=None, y1=None):
    """
    Scan horizontal and vertical lines within the region [x0,y0,x1,y1].
    Returns:
      h_transitions: dict of y → list of (x, from_idx, to_idx) transitions
      v_transitions: dict of x → list of (y, from_idx, to_idx) transitions
    """
    if x1 is None: x1 = w
    if y1 is None: y1 = h

    x0 = max(0, x0); y0 = max(0, y0)
    x1 = min(w, x1); y1 = min(h, y1)

    h_trans = {}
    for y in range(y0, y1):
        row = idx_map[y][x0:x1]
        trans = []
        prev = row[0] if row else 0
        for dx, cur in enumerate(row[1:], start=1):
            if cur != prev:
                trans.append((x0 + dx, prev, cur))
                prev = cur
        if trans:
            h_trans[y] = trans

    v_trans = {}
    for x in range(x0, x1):
        col = [idx_map[y][x] for y in range(y0, y1)]
        trans = []
        prev = col[0] if col else 0
        for dy, cur in enumerate(col[1:], start=1):
            if cur != prev:
                trans.append((y0 + dy, prev, cur))
                prev = cur
        if trans:
            v_trans[x] = trans

    return h_trans, v_trans


def detect_violations(idx_map, w, h, head_region):
    """
    Detect hierarchy violations within the head region.

    Rules checked:
      1. EYE-UNDER-HAIR (column check): In any column within the head region,
         if we see: ... HAIR row ... EYE row ... (hair above eye in same column)
         AND that eye pixel has no skin/outline pixels separating it from the hair,
         it is a potential "eye covered by hair" artifact.

      2. HAIR-INSIDE-EYE-RUN (scanline check): In any row, if within a contiguous
         run of EYE index pixels there is a HAIR index pixel, that is a stray pixel.

      3. UNKNOWN-IN-HEAD: Any pixel classified as UNKNOWN (99) within the head bbox.

    Returns list of violation dicts:
      { "type": str, "x": int, "y": int, "description": str, "severity": "FAIL"|"WARN" }
    """
    if head_region is None:
        return []

    hx0, hy0, hx1, hy1 = head_region
    violations = []

    # Rule 1: EYE-UNDER-HAIR — column scan
    for x in range(hx0, hx1 + 1):
        last_hair_y = None
        for y in range(hy0, hy1 + 1):
            idx = idx_map[y][x]
            if idx in HAIR_INDICES:
                last_hair_y = y
            elif idx in EYE_INDICES:
                if last_hair_y is not None:
                    # Check if there's only non-separating pixels between last hair and this eye
                    gap_start = last_hair_y + 1
                    gap_pixels = [idx_map[gy][x] for gy in range(gap_start, y)]
                    # If gap contains only outline or more hair (no skin/bg in between),
                    # this is a likely "eye inside hair" rendering defect
                    non_separator = all(
                        gp in HAIR_INDICES | {1}   # hair or outline only — no skin gap
                        for gp in gap_pixels
                    )
                    if non_separator and len(gap_pixels) < 8:
                        violations.append({
                            "type":        "EYE_UNDER_HAIR",
                            "x":           x,
                            "y":           y,
                            "description": (
                                f"Eye pixel ({idx}) at ({x},{y}) appears directly below "
                                f"hair pixel ({last_hair_y}) in column {x} — possible "
                                f"'eye inside hair' rendering defect. "
                                f"Gap={len(gap_pixels)}px (hair/outline only, no skin separator)."
                            ),
                            "severity":    "FAIL",
                        })
                    last_hair_y = None   # reset after seeing eye

    # Rule 2: HAIR-INSIDE-EYE-RUN — horizontal scanline
    for y in range(hy0, hy1 + 1):
        row = idx_map[y][hx0:hx1 + 1]
        in_eye_run   = False
        eye_run_start = None
        for dx, idx in enumerate(row):
            x = hx0 + dx
            if idx in EYE_INDICES:
                if not in_eye_run:
                    in_eye_run    = True
                    eye_run_start = x
            else:
                if in_eye_run and idx in HAIR_INDICES:
                    violations.append({
                        "type":        "HAIR_IN_EYE_RUN",
                        "x":           x,
                        "y":           y,
                        "description": (
                            f"Hair pixel ({idx}) at ({x},{y}) embedded in eye run "
                            f"(eye run started at x={eye_run_start}) — "
                            f"stray hair pixel inside eye region."
                        ),
                        "severity":    "FAIL",
                    })
                elif not in_eye_run or idx not in EYE_INDICES | {1}:
                    in_eye_run    = False
                    eye_run_start = None

    # Rule 3: UNKNOWN in head region
    for y in range(hy0, hy1 + 1):
        for x in range(hx0, hx1 + 1):
            if idx_map[y][x] == 99:
                violations.append({
                    "type":        "UNKNOWN_IN_HEAD",
                    "x":           x,
                    "y":           y,
                    "description": (
                        f"Pixel at ({x},{y}) is UNKNOWN (no palette match within tolerance) "
                        f"inside the head bounding box. Check for off-spec color."
                    ),
                    "severity":    "WARN",
                })

    return violations


def build_annotated_image(img: Image.Image, idx_map, w, h,
                           violations: list,
                           head_region=None) -> Image.Image:
    """
    Build an annotated version of the image showing:
    - Per-pixel body-part color overlay (semi-blended with original)
    - Violation pixels highlighted in bright magenta (FAIL) or yellow (WARN)
    - Head region bounding box drawn in green
    """
    original = img.convert("RGB")
    overlay  = Image.new("RGB", (w, h), (0, 0, 0))
    ov_arr   = overlay.load()

    for y in range(h):
        for x in range(w):
            idx = idx_map[y][x]
            col = INDEX_DISPLAY_COLORS.get(idx, (128, 0, 128))
            ov_arr[x, y] = col

    # Blend: 40% overlay, 60% original
    orig_arr = original.load()
    out      = Image.new("RGB", (w, h))
    out_arr  = out.load()
    for y in range(h):
        for x in range(w):
            oc = orig_arr[x, y]
            vx = ov_arr[x, y]
            out_arr[x, y] = (
                int(oc[0] * 0.6 + vx[0] * 0.4),
                int(oc[1] * 0.6 + vx[1] * 0.4),
                int(oc[2] * 0.6 + vx[2] * 0.4),
            )

    # Highlight violations
    for v in violations:
        vx = v["x"]
        vy = v["y"]
        if v["severity"] == "FAIL":
            vc = (255, 0, 200)    # bright magenta
        else:
            vc = (255, 220, 0)    # yellow
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = vx + dx, vy + dy
                if 0 <= nx < w and 0 <= ny < h:
                    out_arr[nx, ny] = vc

    draw = ImageDraw.Draw(out)

    # Draw head region box
    if head_region:
        hx0, hy0, hx1, hy1 = head_region
        draw.rectangle([hx0, hy0, hx1, hy1], outline=(0, 200, 60), width=2)

    # Legend strip
    try:
        from PIL import ImageFont
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)
    except Exception:
        from PIL import ImageFont
        font = ImageFont.load_default()

    legend_items = [
        (2,  "SKIN"),
        (5,  "HAIR"),
        (7,  "EYE_W"),
        (8,  "EYE_I"),
        (12, "HOODIE"),
        (15, "PANTS"),
        (99, "UNKN"),
    ]
    lx = 4
    ly = max(4, h - 24)
    for (lidx, lname) in legend_items:
        col = INDEX_DISPLAY_COLORS.get(lidx, (128, 0, 128))
        draw.rectangle([lx, ly, lx + 10, ly + 10], fill=col, outline=(0, 0, 0), width=1)
        draw.text((lx + 12, ly), lname, fill=(0, 0, 0), font=font)
        lx += 48

    # Mark violations with a cross
    for v in violations:
        vx = v["x"]
        vy = v["y"]
        fc = (255, 0, 200) if v["severity"] == "FAIL" else (255, 220, 0)
        draw.line([vx - 4, vy, vx + 4, vy], fill=fc, width=1)
        draw.line([vx, vy - 4, vx, vy + 4], fill=fc, width=1)

    out.thumbnail((1280, 1280), Image.LANCZOS)
    return out


def crop_panel(img: "Image.Image", panel_index: int, cols: int, rows: int) -> "Image.Image":
    """
    Crop a single panel (0-based, left-to-right, top-to-bottom) from an
    expression sheet laid out in a cols×rows grid.

    The crop is computed by dividing the full image width by cols and height by
    rows. No padding compensation is applied — the crop includes any inter-panel
    border pixels, but those will be classified as BACKGROUND by the hierarchy
    tool since they match the sheet BG colour.

    Returns the cropped PIL Image.
    """
    w, h = img.size
    if panel_index < 0 or panel_index >= cols * rows:
        print(f"ERROR: --panel {panel_index} out of range for {cols}x{rows} grid "
              f"(valid: 0–{cols * rows - 1})")
        sys.exit(1)

    col = panel_index % cols
    row = panel_index // cols
    panel_w = w // cols
    panel_h = h // rows
    x0 = col * panel_w
    y0 = row * panel_h
    x1 = x0 + panel_w
    y1 = y0 + panel_h
    print(f"Panel {panel_index} → grid ({col},{row}) → crop ({x0},{y0})–({x1},{y1})  "
          f"({panel_w}×{panel_h}px)")
    return img.crop((x0, y0, x1, y1))


def run_chain(char: str, expr: str, palette_name: str, tolerance: int,
              output_annotated: str, output_csv: str, verbose: bool) -> None:
    """
    Pipeline mode: run expression_isolator to extract the named expression at
    800×800px, then run the hierarchy check on that output.

    Requires LTG_TOOL_expression_isolator.py to be in the same directory.
    """
    import subprocess
    import tempfile

    script_dir = os.path.dirname(os.path.abspath(__file__))
    isolator   = os.path.join(script_dir, "LTG_TOOL_expression_isolator.py")

    if not os.path.exists(isolator):
        print(f"ERROR: --chain requires LTG_TOOL_expression_isolator.py in {script_dir}")
        sys.exit(1)

    # Run expression_isolator to produce a single-expression PNG
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name

    iso_cmd = [
        sys.executable, isolator,
        "--char", char,
        "--expr", expr,
        "--output", tmp_path,
    ]
    print(f"[chain] Running expression_isolator: {' '.join(iso_cmd[2:])}")
    result = subprocess.run(iso_cmd, capture_output=True, text=True)
    if result.returncode not in (0, 1):     # isolator exits 0=PASS, 1=WARN, 2=FAIL
        print(f"ERROR: expression_isolator failed:\n{result.stderr}")
        os.unlink(tmp_path)
        sys.exit(1)
    print(result.stdout.strip())

    # Now run hierarchy on the isolated expression image
    hier_cmd = [
        sys.executable, __file__,
        tmp_path,
        "--palette", palette_name,
        "--tolerance", str(tolerance),
    ]
    if output_annotated:
        hier_cmd += ["--output-annotated", output_annotated]
    if output_csv:
        hier_cmd += ["--output-csv", output_csv]
    if verbose:
        hier_cmd += ["--verbose"]

    print(f"[chain] Running hierarchy on isolated expression...")
    result2 = subprocess.run(hier_cmd, capture_output=True, text=True)
    print(result2.stdout)
    if result2.stderr:
        print(result2.stderr)

    os.unlink(tmp_path)
    sys.exit(result2.returncode)


def main():
    parser = argparse.ArgumentParser(
        description="LTG Body-Part Hierarchy Tool v002 — detects eye-inside-hair and other rendering violations."
    )
    parser.add_argument("image",               nargs="?", default=None,
                        help="Character panel or expression sheet PNG (omit when using --chain)")
    parser.add_argument("--palette",           default="luma",
                        choices=["luma", "byte", "cosmo"],
                        help="Character palette to use (default: luma)")
    parser.add_argument("--tolerance",         type=int, default=25,
                        help="Per-channel color tolerance for palette matching (default: 25)")
    parser.add_argument("--panel",             type=int, default=None,
                        help="Crop to panel index N (0-based, L→R, T→B) before analysis")
    parser.add_argument("--grid",              default="3x3",
                        help="Grid layout for --panel (default: 3x3, e.g. 4x3)")
    parser.add_argument("--head-region",       default=None,
                        help="Restrict analysis to region: x0,y0,x1,y1 (pixels)")
    parser.add_argument("--output-annotated",  default=None,
                        help="Save annotated body-part overlay PNG")
    parser.add_argument("--output-csv",        default=None,
                        help="Save scan-line transition CSV")
    parser.add_argument("--verbose",           action="store_true",
                        help="Print full transition table to stdout")
    parser.add_argument("--chain",             action="store_true",
                        help="Pipeline: run expression_isolator then hierarchy (requires --char and --expr)")
    parser.add_argument("--char",              default=None,
                        help="Character name for --chain mode (luma|byte|cosmo)")
    parser.add_argument("--expr",              default=None,
                        help="Expression name for --chain mode (e.g. 'THE NOTICING')")
    args = parser.parse_args()

    # ── Chain mode ──────────────────────────────────────────────────────────────
    if args.chain:
        if not args.char or not args.expr:
            print("ERROR: --chain requires --char and --expr")
            sys.exit(1)
        run_chain(
            char=args.char,
            expr=args.expr,
            palette_name=args.palette,
            tolerance=args.tolerance,
            output_annotated=args.output_annotated,
            output_csv=args.output_csv,
            verbose=args.verbose,
        )
        return   # run_chain calls sys.exit() internally; this is a safety return

    # ── Normal mode ─────────────────────────────────────────────────────────────
    if args.image is None:
        print("ERROR: <image> is required unless --chain is used.")
        sys.exit(1)

    if not os.path.exists(args.image):
        print(f"ERROR: Image not found: {args.image}")
        sys.exit(1)

    # Select palette
    if args.palette == "luma":
        palette = LUMA_PALETTE
    elif args.palette == "byte":
        # Byte uses a simplified palette (teal body, dark BG)
        palette = {
            0:  ("BACKGROUND",  []),
            1:  ("OUTLINE",     [(10, 10, 20)]),
            2:  ("BYTE_TEAL",   [(0, 212, 232)]),
            3:  ("BYTE_HL",     [(0, 240, 255)]),
            4:  ("BYTE_SH",     [(0, 168, 192)]),
            5:  ("HOT_MAG",     [(255, 45, 120), (255, 45, 107)]),
            6:  ("UV_PURPLE",   [(123, 47, 190)]),
            7:  ("EYE_WHITE",   [(240, 240, 245)]),
            8:  ("SOFT_GOLD",   [(232, 201, 90)]),
            99: ("UNKNOWN",     []),
        }
    else:
        palette = LUMA_PALETTE  # Cosmo uses similar skin/hair palette for now

    img = Image.open(args.image).convert("RGB")
    w, h = img.size
    print(f"Image: {args.image}  ({w}×{h}px)")
    print(f"Palette: {args.palette}  |  Tolerance: {args.tolerance}px per channel")

    # ── Panel crop (--panel N) ──────────────────────────────────────────────────
    if args.panel is not None:
        try:
            grid_parts = args.grid.lower().split("x")
            if len(grid_parts) != 2:
                raise ValueError
            grid_cols = int(grid_parts[0])
            grid_rows = int(grid_parts[1])
        except (ValueError, IndexError):
            print(f"ERROR: --grid must be in COLSxROWS format (e.g. 3x3, 4x3). Got: {args.grid!r}")
            sys.exit(1)
        img = crop_panel(img, args.panel, grid_cols, grid_rows)
        w, h = img.size
        print(f"Panel crop applied. Working image: {w}×{h}px")

    bg_color = sample_bg_color(img)
    print(f"BG color (auto): RGB{bg_color}")

    print("Building index map... ", end="", flush=True)
    idx_map, w, h = build_index_map(img, palette, args.tolerance, bg_color)
    print("done.")

    # Head region
    if args.head_region:
        try:
            coords = [int(v.strip()) for v in args.head_region.split(",")]
            if len(coords) != 4:
                raise ValueError("Expected 4 comma-separated integers")
            head_region = tuple(coords)
            print(f"Head region (manual): {head_region}")
        except ValueError as e:
            print(f"ERROR: --head-region must be x0,y0,x1,y1 integers: {e}")
            sys.exit(1)
    else:
        head_region = detect_head_region(idx_map, w, h)
        if head_region:
            print(f"Head region (auto):   {head_region}")
        else:
            print("WARNING: Could not detect head region. Hierarchy check skipped.")

    # Scan transitions
    print("Scanning transitions...")
    hx0, hy0, hx1, hy1 = head_region if head_region else (0, 0, w, h)
    h_trans, v_trans = scan_transitions(idx_map, w, h, palette, hx0, hy0, hx1, hy1)

    if args.verbose:
        print(f"\nHorizontal scan transitions in head region ({len(h_trans)} rows with transitions):")
        for y in sorted(h_trans.keys())[:30]:
            trans = h_trans[y]
            trans_str = " → ".join(
                f"[{palette.get(fi, ('?', []))[0]}→{palette.get(ti, ('?', []))[0]}]@x={x}"
                for (x, fi, ti) in trans
            )
            print(f"  y={y:4d}: {trans_str}")
        if len(h_trans) > 30:
            print(f"  ... ({len(h_trans) - 30} more rows not shown, use --output-csv for full data)")

    # Detect violations
    print("\nDetecting hierarchy violations...")
    violations = detect_violations(idx_map, w, h, head_region)

    fail_v = [v for v in violations if v["severity"] == "FAIL"]
    warn_v = [v for v in violations if v["severity"] == "WARN"]

    if fail_v:
        overall = "FAIL"
    elif warn_v:
        overall = "WARN"
    else:
        overall = "PASS"

    print("=" * 65)
    print(f"BODY-PART HIERARCHY CHECK  |  {os.path.basename(args.image)}")
    print(f"Palette: {args.palette}  |  Head region: {head_region}")
    print("-" * 65)
    print(f"Violations: {len(fail_v)} FAIL  |  {len(warn_v)} WARN")
    print("-" * 65)

    # Group violations by type for compact output
    by_type = defaultdict(list)
    for v in violations:
        by_type[v["type"]].append(v)

    for vtype, vlist in sorted(by_type.items()):
        sev = vlist[0]["severity"]
        print(f"  [{sev}]  {vtype}: {len(vlist)} instance(s)")
        # Show up to 5 examples per type
        for v in vlist[:5]:
            print(f"         ({v['x']},{v['y']})  {v['description'][:90]}")
        if len(vlist) > 5:
            print(f"         ... ({len(vlist) - 5} more — see annotated output for full map)")

    if not violations:
        print("  No violations detected. Hierarchy clean.")

    print("-" * 65)
    print(f"OVERALL: {overall}")
    print("=" * 65)

    # Save CSV
    if args.output_csv:
        with open(args.output_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["direction", "fixed_axis", "pos_axis", "from_name", "from_idx", "to_name", "to_idx"])
            for y, trans in sorted(h_trans.items()):
                for (x, fi, ti) in trans:
                    fn = palette.get(fi, ("?", []))[0]
                    tn = palette.get(ti, ("?", []))[0]
                    writer.writerow(["H", y, x, fn, fi, tn, ti])
            for x, trans in sorted(v_trans.items()):
                for (y, fi, ti) in trans:
                    fn = palette.get(fi, ("?", []))[0]
                    tn = palette.get(ti, ("?", []))[0]
                    writer.writerow(["V", x, y, fn, fi, tn, ti])
        print(f"Transitions CSV: {args.output_csv}")

    # Save annotated image
    if args.output_annotated:
        ann = build_annotated_image(img, idx_map, w, h, violations, head_region)
        ann.save(args.output_annotated)
        print(f"Annotated image: {args.output_annotated}")

    # Exit code
    if overall == "FAIL":
        sys.exit(2)
    elif overall == "WARN":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
