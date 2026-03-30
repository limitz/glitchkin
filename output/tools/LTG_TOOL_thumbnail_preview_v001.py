# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_thumbnail_preview_v001.py
Thumbnail Visibility Preview Tool — Hana Okonkwo / C39

Shows a side-by-side comparison:
  Left panel:  full 1280×720 view of the input image
  Right panel: 120×68 thumbnail simulation shown at 8× zoom (960×544)

If a pixel region is specified (x1, y1, x2, y2 in input-image coordinates),
a colored bounding box is drawn on both panels so the region can be visually
tracked across scales.

Usage:
  python LTG_TOOL_thumbnail_preview_v001.py <input.png> [--region x1 y1 x2 y2]

Output:
  <input_stem>_thumbnail_preview.png  (saved next to the input file)
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

# ── constants ──────────────────────────────────────────────────────────────
FULL_W, FULL_H = 1280, 720          # left panel size
THUMB_W, THUMB_H = 120, 68          # thumbnail simulation size
ZOOM = 8                             # zoom factor for thumb panel
THUMB_ZOOM_W = THUMB_W * ZOOM       # 960
THUMB_ZOOM_H = THUMB_H * ZOOM       # 544

PANEL_PAD = 20                       # padding between panels and around sheet
LABEL_H = 28                         # height of the label bar below each panel

BOX_COLOR = (255, 80, 0)             # orange bounding-box outline
BOX_WIDTH = 3                        # outline thickness on full panel (px)
THUMB_BOX_WIDTH = 2                  # outline thickness on zoom panel (px)

SHEET_BG = (30, 30, 30)             # dark sheet background
LABEL_BG = (20, 20, 20)             # label bar background
LABEL_FG = (220, 220, 220)          # label text colour


def load_and_fit(path: Path, target_w: int, target_h: int) -> Image.Image:
    """Load an image and resize (LANCZOS) to fit inside target_w × target_h,
    then centre-paste onto a solid-black canvas of exactly that size."""
    img = Image.open(path).convert("RGBA")
    img.thumbnail((target_w, target_h), Image.LANCZOS)
    canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 255))
    ox = (target_w - img.width) // 2
    oy = (target_h - img.height) // 2
    canvas.paste(img, (ox, oy))
    return canvas, ox, oy, img.width, img.height


def draw_box(img: Image.Image, box: tuple, color, width: int):
    """Draw a rectangle outline on img (mutates img)."""
    draw = ImageDraw.Draw(img)
    x1, y1, x2, y2 = box
    for i in range(width):
        draw.rectangle([x1 + i, y1 + i, x2 - i, y2 - i], outline=color)
    return img


def make_label_bar(w: int, h: int, text: str) -> Image.Image:
    """Create a dark bar with centred text label."""
    bar = Image.new("RGBA", (w, h), LABEL_BG)
    draw = ImageDraw.Draw(bar)
    # Use default bitmap font — no external font deps
    draw.text((w // 2, h // 2), text, fill=LABEL_FG, anchor="mm")
    return bar


def build_preview(input_path: Path, region=None) -> Image.Image:
    """
    Build the side-by-side preview sheet.

    region — optional (x1, y1, x2, y2) in original input-image pixels.
    """
    # ── 1. Load original image dimensions ────────────────────────────────
    orig = Image.open(input_path)
    orig_w, orig_h = orig.size
    orig.close()

    # ── 2. Build full panel (left) ────────────────────────────────────────
    full_panel, fx_off, fy_off, fw, fh = load_and_fit(input_path, FULL_W, FULL_H)

    if region:
        rx1, ry1, rx2, ry2 = region
        # Scale region from original coords → full-panel display coords
        scale_x = fw / orig_w
        scale_y = fh / orig_h
        bx1 = int(fx_off + rx1 * scale_x)
        by1 = int(fy_off + ry1 * scale_y)
        bx2 = int(fx_off + rx2 * scale_x)
        by2 = int(fy_off + ry2 * scale_y)
        draw_box(full_panel, (bx1, by1, bx2, by2), BOX_COLOR, BOX_WIDTH)

    # ── 3. Build thumbnail simulation (right) ─────────────────────────────
    # Downscale to 120×68
    thumb_raw = Image.open(input_path).convert("RGBA")
    thumb_raw.thumbnail((THUMB_W, THUMB_H), Image.LANCZOS)
    # Centre onto exact 120×68 canvas
    thumb_canvas = Image.new("RGBA", (THUMB_W, THUMB_H), (0, 0, 0, 255))
    tx_off = (THUMB_W - thumb_raw.width) // 2
    ty_off = (THUMB_H - thumb_raw.height) // 2
    thumb_canvas.paste(thumb_raw, (tx_off, ty_off))

    # Draw box on thumbnail canvas before zoom
    if region:
        scale_x = thumb_raw.width / orig_w
        scale_y = thumb_raw.height / orig_h
        tbx1 = int(tx_off + rx1 * scale_x)
        tby1 = int(ty_off + ry1 * scale_y)
        tbx2 = int(tx_off + rx2 * scale_x)
        tby2 = int(ty_off + ry2 * scale_y)
        draw_box(thumb_canvas, (tbx1, tby1, tbx2, tby2), BOX_COLOR, 1)

    # Zoom by 8× using NEAREST to preserve pixelated thumbnail feel
    thumb_zoomed = thumb_canvas.resize(
        (THUMB_ZOOM_W, THUMB_ZOOM_H), Image.NEAREST
    )

    # ── 4. Compose sheet ──────────────────────────────────────────────────
    sheet_w = PANEL_PAD + FULL_W + PANEL_PAD + THUMB_ZOOM_W + PANEL_PAD
    sheet_h = PANEL_PAD + max(FULL_H, THUMB_ZOOM_H) + LABEL_H + PANEL_PAD

    sheet = Image.new("RGBA", (sheet_w, sheet_h), SHEET_BG)
    draw = ImageDraw.Draw(sheet)

    # Paste full panel
    full_x = PANEL_PAD
    full_y = PANEL_PAD
    sheet.paste(full_panel, (full_x, full_y))

    # Paste zoomed thumb panel
    thumb_x = PANEL_PAD + FULL_W + PANEL_PAD
    thumb_y = PANEL_PAD + (max(FULL_H, THUMB_ZOOM_H) - THUMB_ZOOM_H) // 2
    sheet.paste(thumb_zoomed, (thumb_x, thumb_y))

    # Label bars
    full_label = make_label_bar(FULL_W, LABEL_H, "Full 1280×720")
    sheet.paste(full_label, (full_x, full_y + FULL_H))

    thumb_label = make_label_bar(
        THUMB_ZOOM_W, LABEL_H, f"Thumbnail 120×68  (×{ZOOM} zoom)"
    )
    sheet.paste(thumb_label, (thumb_x, PANEL_PAD + max(FULL_H, THUMB_ZOOM_H)))

    # ── 5. Enforce ≤1280px hard limit ─────────────────────────────────────
    sheet = sheet.convert("RGB")
    sheet.thumbnail((1280, 1280), Image.LANCZOS)

    return sheet


def main():
    parser = argparse.ArgumentParser(
        description="LTG Thumbnail Visibility Preview Tool"
    )
    parser.add_argument("input", help="Path to input PNG")
    parser.add_argument(
        "--region",
        nargs=4,
        type=int,
        metavar=("X1", "Y1", "X2", "Y2"),
        help="Pixel region in input-image coordinates to highlight",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    region = tuple(args.region) if args.region else None
    preview = build_preview(input_path, region=region)

    out_path = input_path.parent / (input_path.stem + "_thumbnail_preview.png")
    preview.save(str(out_path))
    print(f"Saved: {out_path}")
    print(f"Sheet size: {preview.size[0]}×{preview.size[1]}px")


if __name__ == "__main__":
    main()
