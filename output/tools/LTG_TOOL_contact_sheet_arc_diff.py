#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_contact_sheet_arc_diff.py
Contact Sheet Arc-Diff Tool — Cycle 37
Lee Tanaka, Character Staging & Visual Acting Specialist

Compares two contact sheet PNGs (old version vs new version) and outputs a
side-by-side comparison PNG (≤ 800×600px) highlighting:
  - Panels where thumbnail content changed significantly (pixel diff > threshold)
  - Any new or removed panels (detected by panel count mismatch)
  - A summary legend with change status per slot

Usage:
  python3 LTG_TOOL_contact_sheet_arc_diff.py OLD.png NEW.png [OUTPUT.png]

  If OUTPUT.png is omitted, writes to:
    /home/wipkat/team/output/storyboards/LTG_TOOL_arc_diff_output.png

Arguments:
  OLD.png     Path to older contact sheet version
  NEW.png     Path to newer contact sheet version
  OUTPUT.png  Optional output path (default: storyboards root)

Exit codes:
  0 — success (diff generated)
  1 — usage error or missing input file

How it works:
  1. Load both contact sheets; resize to equal dimensions for comparison
  2. Split each sheet into a grid of per-panel thumbnails (auto-detect grid from
     image proportions using a common aspect-ratio heuristic — 480×270 panels
     in most LTG contact sheets)
  3. For each slot:
       - If only in OLD  → mark REMOVED (red border)
       - If only in NEW  → mark ADDED (green border)
       - Else compute mean absolute pixel difference between thumbnails:
           diff_score > CHANGED_THRESHOLD → mark CHANGED (yellow border)
           otherwise                       → mark SAME (grey border)
  4. Lay out OLD strip (left) and NEW strip (right) side-by-side, with colored
     borders indicating change status.  Summary count row at bottom.
  5. Thumbnail output to ≤ 800×600px (preserving aspect ratio).

Constants:
  CHANGED_THRESHOLD  = 12   (0–255 scale per-channel mean abs diff)
  PANEL_ASPECT_W     = 16   (panel aspect ratio width component)
  PANEL_ASPECT_H     =  9   (panel aspect ratio height component)
  MIN_PANEL_PX       = 40   (minimum panel short side in pixels to be valid)
  BORDER_PX          =  4   (border thickness in pixels around each thumbnail)

Programmatic API (for LTG_TOOL_precritique_qa integration — Morgan Walsh):
  from LTG_TOOL_contact_sheet_arc_diff import compare_contact_sheets
  result = compare_contact_sheets(old_path, new_path, output_path=None)
  # Returns dict: ok, error, n_old, n_new, same, changed, added, removed,
  #               changed_slots, added_slots, removed_slots, diff_output.
  # Does NOT call sys.exit() — safe to import.
  # If output_path provided, writes arc-diff PNG.  If None, skips PNG.

C39 review (Lee Tanaka): compare_contact_sheets() API confirmed correct for
  precritique_qa_v001.py Section 10 integration. No API changes needed.
  Docstring updated to advertise the programmatic API.
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont

# ── Constants ──────────────────────────────────────────────────────────────────
CHANGED_THRESHOLD = 12   # mean absolute per-channel diff that counts as changed
PANEL_ASPECT_W    = 16
PANEL_ASPECT_H    =  9
MIN_PANEL_PX      = 40
BORDER_PX         =  4
MAX_OUT_W         = 800
MAX_OUT_H         = 600

DEFAULT_OUTPUT = "/home/wipkat/team/output/storyboards/LTG_TOOL_arc_diff_output.png"

# Change status colours (RGB)
COLOR_SAME    = (140, 140, 140)   # grey
COLOR_CHANGED = (220, 200,  40)   # yellow
COLOR_ADDED   = ( 60, 200,  80)   # green
COLOR_REMOVED = (220,  60,  60)   # red
COLOR_BG      = ( 24,  24,  30)   # dark background
COLOR_TEXT    = (240, 240, 240)
COLOR_HEADER  = ( 50,  50,  60)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _detect_panel_grid(sheet_w: int, sheet_h: int):
    """
    Auto-detect how many columns and rows of panels are in a contact sheet,
    returning (cols, rows, panel_w, panel_h).

    Strategy: try candidate column counts 2..8 and pick the one whose implied
    panel dimensions are closest to a 16:9 aspect ratio.  Rows are derived from
    the total panel count implied by the closest integer row fit.
    """
    best_cols = 1
    best_rows = 1
    best_score = float("inf")
    best_pw = sheet_w
    best_ph = sheet_h

    for cols in range(2, 9):
        pw = sheet_w / cols
        for rows in range(1, 9):
            ph = sheet_h / rows
            if pw < MIN_PANEL_PX or ph < MIN_PANEL_PX:
                continue
            # Score = deviation from target aspect ratio
            aspect_ratio = pw / ph
            target = PANEL_ASPECT_W / PANEL_ASPECT_H
            score = abs(aspect_ratio - target)
            if score < best_score:
                best_score = score
                best_cols = cols
                best_rows = rows
                best_pw = int(pw)
                best_ph = int(ph)

    return best_cols, best_rows, best_pw, best_ph


def _extract_panel_thumbs(sheet, cols: int, rows: int,
                           panel_w: int, panel_h: int):
    """
    Extract panel thumbnails from a contact sheet by slicing into a grid.
    Returns a flat list, row-major order (left-to-right, top-to-bottom).
    """
    thumbs = []
    for row in range(rows):
        for col in range(cols):
            x0 = col * panel_w
            y0 = row * panel_h
            x1 = x0 + panel_w
            y1 = y0 + panel_h
            crop = sheet.crop((x0, y0, x1, y1))
            thumbs.append(crop)
    return thumbs


def _mean_abs_diff(img_a: Image.Image, img_b: Image.Image) -> float:
    """
    Compute mean absolute per-channel pixel difference between two images.
    Resizes both to a common small size (64×36) for speed.
    """
    compare_size = (64, 36)
    a = img_a.convert("RGB").resize(compare_size, Image.LANCZOS)
    b = img_b.convert("RGB").resize(compare_size, Image.LANCZOS)
    import struct

    total = 0.0
    pixels = compare_size[0] * compare_size[1]
    a_data = list(a.getdata())
    b_data = list(b.getdata())
    for (ar, ag, ab_), (br, bg, bb_) in zip(a_data, b_data):
        total += abs(ar - br) + abs(ag - bg) + abs(ab_ - bb_)
    return total / (pixels * 3)


def _add_border(thumb: Image.Image, color: tuple, border_px: int) -> Image.Image:
    """Add a solid color border around a thumbnail."""
    w, h = thumb.size
    bordered = Image.new("RGB", (w + border_px * 2, h + border_px * 2), color)
    bordered.paste(thumb, (border_px, border_px))
    return bordered


def _make_label_block(text: str, w: int, h: int, color: tuple) -> Image.Image:
    """Create a small colored label block with text."""
    block = Image.new("RGB", (w, h), color)
    draw = ImageDraw.Draw(block)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)
    except Exception:
        font = ImageFont.load_default()

    # Center text
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = max(0, (w - tw) // 2)
    ty = max(0, (h - th) // 2)
    draw.text((tx, ty), text, fill=COLOR_TEXT, font=font)
    return block


def _build_strip(thumbs, statuses,
                 thumb_target_w: int, thumb_target_h: int,
                 label_h: int):
    """
    Build a horizontal or wrapped strip of bordered thumbnails.
    Returns an RGBA image of the strip.
    """
    n = len(thumbs)
    if n == 0:
        return Image.new("RGB", (thumb_target_w, thumb_target_h + label_h + BORDER_PX * 2), COLOR_BG)

    status_color_map = {
        "SAME":    COLOR_SAME,
        "CHANGED": COLOR_CHANGED,
        "ADDED":   COLOR_ADDED,
        "REMOVED": COLOR_REMOVED,
    }

    cell_w = thumb_target_w + BORDER_PX * 2
    cell_h = thumb_target_h + BORDER_PX * 2 + label_h

    # Lay out in a single row (strip); caller wraps if needed
    strip_w = cell_w * n
    strip_h = cell_h
    strip = Image.new("RGB", (strip_w, strip_h), COLOR_BG)
    draw = ImageDraw.Draw(strip)

    for i, (thumb, status) in enumerate(zip(thumbs, statuses)):
        color = status_color_map.get(status, COLOR_SAME)
        thumb_r = thumb.convert("RGB").resize(
            (thumb_target_w, thumb_target_h), Image.LANCZOS)
        bordered = _add_border(thumb_r, color, BORDER_PX)
        x0 = i * cell_w
        y0 = 0
        strip.paste(bordered, (x0, y0))

        # Status label below
        label = _make_label_block(status, cell_w, label_h, color)
        strip.paste(label, (x0, y0 + BORDER_PX * 2 + thumb_target_h))

    return strip


# ── Main ───────────────────────────────────────────────────────────────────────

def build_arc_diff(old_path: str, new_path: str, output_path: str) -> None:
    """Core logic: load, compare, and output the arc-diff PNG."""

    if not os.path.isfile(old_path):
        print(f"ERROR: OLD file not found: {old_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(new_path):
        print(f"ERROR: NEW file not found: {new_path}", file=sys.stderr)
        sys.exit(1)

    old_sheet = Image.open(old_path).convert("RGB")
    new_sheet = Image.open(new_path).convert("RGB")

    # ── Detect grids ──────────────────────────────────────────────────────────
    old_cols, old_rows, old_pw, old_ph = _detect_panel_grid(*old_sheet.size)
    new_cols, new_rows, new_pw, new_ph = _detect_panel_grid(*new_sheet.size)

    old_thumbs = _extract_panel_thumbs(old_sheet, old_cols, old_rows, old_pw, old_ph)
    new_thumbs = _extract_panel_thumbs(new_sheet, new_cols, new_rows, new_pw, new_ph)

    n_old = len(old_thumbs)
    n_new = len(new_thumbs)
    n_max = max(n_old, n_new)

    # ── Per-slot comparison ───────────────────────────────────────────────────
    old_statuses = []
    new_statuses = []

    for i in range(n_max):
        has_old = i < n_old
        has_new = i < n_new

        if has_old and not has_new:
            old_statuses.append("REMOVED")
        elif has_new and not has_old:
            new_statuses.append("ADDED")
        else:
            diff = _mean_abs_diff(old_thumbs[i], new_thumbs[i])
            status = "CHANGED" if diff > CHANGED_THRESHOLD else "SAME"
            old_statuses.append(status)
            new_statuses.append(status)

    # Pad shorter list with ADDED / REMOVED placeholders
    while len(new_thumbs) < n_max:
        placeholder = Image.new("RGB", (old_pw, old_ph), (30, 30, 40))
        new_thumbs.append(placeholder)
        new_statuses.append("ADDED")
    while len(old_thumbs) < n_max:
        placeholder = Image.new("RGB", (new_pw, new_ph), (30, 30, 40))
        old_thumbs.append(placeholder)
        old_statuses.append("REMOVED")

    # ── Layout sizing ─────────────────────────────────────────────────────────
    # Target: fit within MAX_OUT_W × MAX_OUT_H
    # Layout: two rows of thumbnails (OLD on top row, NEW on bottom row)
    # Each thumbnail target: fit n_max thumbs across MAX_OUT_W / 2 width

    HEADER_H = 20    # space for "OLD" / "NEW" column headers
    LABEL_H  = 14    # status label height below each thumbnail
    GAP_H    = 6     # gap between OLD and NEW rows
    FOOTER_H = 22    # summary stats footer

    available_w = MAX_OUT_W
    available_h = MAX_OUT_H - HEADER_H * 2 - LABEL_H * 2 - GAP_H - FOOTER_H

    # Thumbnail width from available width
    thumb_w = max(20, available_w // n_max - BORDER_PX * 2)
    thumb_h = max(12, int(thumb_w * PANEL_ASPECT_H / PANEL_ASPECT_W))

    # If combined height exceeds budget, shrink
    combined_h = (thumb_h + BORDER_PX * 2 + LABEL_H) * 2 + GAP_H
    if combined_h > available_h:
        scale = available_h / combined_h
        thumb_h = max(12, int(thumb_h * scale))
        thumb_w = max(20, int(thumb_w * scale))

    strip_w = (thumb_w + BORDER_PX * 2) * n_max

    old_strip = _build_strip(old_thumbs, old_statuses, thumb_w, thumb_h, LABEL_H)
    new_strip = _build_strip(new_thumbs, new_statuses, thumb_w, thumb_h, LABEL_H)

    # ── Compose output image ──────────────────────────────────────────────────
    out_w = max(strip_w, 300)
    row_h = thumb_h + BORDER_PX * 2 + LABEL_H
    out_h = HEADER_H + row_h + GAP_H + HEADER_H + row_h + FOOTER_H

    out = Image.new("RGB", (out_w, out_h), COLOR_BG)
    draw = ImageDraw.Draw(out)

    try:
        font_sm = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
        font_xs = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except Exception:
        font_sm = ImageFont.load_default()
        font_xs = font_sm

    def draw_header(y: int, label: str, path: str) -> None:
        draw.rectangle([(0, y), (out_w, y + HEADER_H - 1)], fill=COLOR_HEADER)
        display_path = os.path.basename(path)
        draw.text((4, y + 2), f"{label}: {display_path}", fill=COLOR_TEXT, font=font_sm)

    # OLD row
    y_old_header = 0
    y_old_strip  = y_old_header + HEADER_H
    draw_header(y_old_header, "OLD", old_path)
    out.paste(old_strip, (0, y_old_strip))

    # NEW row
    y_new_header = y_old_strip + row_h + GAP_H
    y_new_strip  = y_new_header + HEADER_H
    draw_header(y_new_header, "NEW", new_path)
    out.paste(new_strip, (0, y_new_strip))

    # Footer summary
    n_changed = old_statuses.count("CHANGED")
    n_added   = new_statuses.count("ADDED")
    n_removed = old_statuses.count("REMOVED")
    n_same    = old_statuses.count("SAME")

    y_footer = y_new_strip + row_h
    draw.rectangle([(0, y_footer), (out_w, out_h)], fill=(18, 18, 24))

    summary_parts = [
        (f"  SAME: {n_same}",    COLOR_SAME),
        (f"  CHANGED: {n_changed}", COLOR_CHANGED),
        (f"  ADDED: {n_added}",   COLOR_ADDED),
        (f"  REMOVED: {n_removed}", COLOR_REMOVED),
        (f"  OLD panels: {n_old}  NEW panels: {n_new}", COLOR_TEXT),
    ]
    sx = 4
    for text, color in summary_parts:
        draw.text((sx, y_footer + 5), text, fill=color, font=font_xs)
        bbox = draw.textbbox((sx, y_footer + 5), text, font=font_xs)
        sx = bbox[2] + 6

    # ── Size cap ──────────────────────────────────────────────────────────────
    out.thumbnail((MAX_OUT_W, MAX_OUT_H), Image.LANCZOS)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    out.save(output_path)
    print(f"Arc-diff written: {output_path}  ({out.size[0]}×{out.size[1]}px)")
    print(f"  OLD panels: {n_old}  NEW panels: {n_new}")
    print(f"  SAME: {n_same}  CHANGED: {n_changed}  ADDED: {n_added}  REMOVED: {n_removed}")


def compare_contact_sheets(old_path: str, new_path: str, output_path: str = None) -> dict:
    """
    Programmatic API: compare two contact sheet PNGs and return a result dict.

    Does NOT call sys.exit() — safe to import and call from other tools.
    If output_path is provided, writes the visual arc-diff PNG to that path.
    If output_path is None, skips writing the output image.

    Parameters
    ----------
    old_path    : str — path to the older contact sheet PNG
    new_path    : str — path to the newer contact sheet PNG
    output_path : str | None — path to write arc-diff comparison PNG (optional)

    Returns
    -------
    dict with keys:
        ok          : bool  — True if both files were found and compared
        error       : str | None — error message if ok=False
        n_old       : int  — panel count in old sheet
        n_new       : int  — panel count in new sheet
        same        : int  — panels unchanged
        changed     : int  — panels changed (diff > CHANGED_THRESHOLD)
        added       : int  — panels present in new, not in old
        removed     : int  — panels present in old, not in new
        changed_slots : list of int — 0-based slot indices that changed
        added_slots   : list of int — 0-based slot indices that were added
        removed_slots : list of int — 0-based slot indices that were removed
        diff_output : str | None — output_path used (or None if not saved)
    """
    if not os.path.isfile(old_path):
        return {"ok": False, "error": f"OLD file not found: {old_path}",
                "n_old": 0, "n_new": 0, "same": 0, "changed": 0,
                "added": 0, "removed": 0, "changed_slots": [],
                "added_slots": [], "removed_slots": [], "diff_output": None}
    if not os.path.isfile(new_path):
        return {"ok": False, "error": f"NEW file not found: {new_path}",
                "n_old": 0, "n_new": 0, "same": 0, "changed": 0,
                "added": 0, "removed": 0, "changed_slots": [],
                "added_slots": [], "removed_slots": [], "diff_output": None}

    old_sheet = Image.open(old_path).convert("RGB")
    new_sheet = Image.open(new_path).convert("RGB")

    old_cols, old_rows, old_pw, old_ph = _detect_panel_grid(*old_sheet.size)
    new_cols, new_rows, new_pw, new_ph = _detect_panel_grid(*new_sheet.size)

    old_thumbs = _extract_panel_thumbs(old_sheet, old_cols, old_rows, old_pw, old_ph)
    new_thumbs = _extract_panel_thumbs(new_sheet, new_cols, new_rows, new_pw, new_ph)

    n_old = len(old_thumbs)
    n_new = len(new_thumbs)
    n_max = max(n_old, n_new)

    old_statuses = []
    new_statuses = []
    changed_slots = []
    added_slots   = []
    removed_slots = []

    for i in range(n_max):
        has_old = i < n_old
        has_new = i < n_new
        if has_old and not has_new:
            old_statuses.append("REMOVED")
            removed_slots.append(i)
        elif has_new and not has_old:
            new_statuses.append("ADDED")
            added_slots.append(i)
        else:
            diff = _mean_abs_diff(old_thumbs[i], new_thumbs[i])
            status = "CHANGED" if diff > CHANGED_THRESHOLD else "SAME"
            old_statuses.append(status)
            new_statuses.append(status)
            if status == "CHANGED":
                changed_slots.append(i)

    n_changed = old_statuses.count("CHANGED")
    n_added   = len(added_slots)
    n_removed = len(removed_slots)
    n_same    = old_statuses.count("SAME")

    saved_path = None
    if output_path is not None:
        try:
            build_arc_diff(old_path, new_path, output_path)
            saved_path = output_path
        except Exception:
            pass  # Non-fatal; result dict is complete regardless

    return {
        "ok": True,
        "error": None,
        "n_old": n_old,
        "n_new": n_new,
        "same": n_same,
        "changed": n_changed,
        "added": n_added,
        "removed": n_removed,
        "changed_slots": changed_slots,
        "added_slots": added_slots,
        "removed_slots": removed_slots,
        "diff_output": saved_path,
    }


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: LTG_TOOL_contact_sheet_arc_diff.py OLD.png NEW.png [OUTPUT.png]",
              file=sys.stderr)
        sys.exit(1)

    old_path    = sys.argv[1]
    new_path    = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) >= 4 else DEFAULT_OUTPUT

    build_arc_diff(old_path, new_path, output_path)


if __name__ == "__main__":
    main()
