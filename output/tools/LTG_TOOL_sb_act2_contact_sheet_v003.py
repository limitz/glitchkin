#!/usr/bin/env python3
"""
LTG_TOOL_sb_act2_contact_sheet_v003.py
Act 2 Contact Sheet v003 — Cycle 16
Lee Tanaka, Storyboard Artist

Changes from v002:
  - Includes new A2-06 MED panel (before the INSERT)
  - Uses A2-03 v002 (restaged with camera spec + whiteboard as character)
  - Uses A2-04 v002 (Byte as non-participant in second quadrant)
  - Uses A2-07 v002 (RESIGNED — unblocked)
  - Total: 9 panels (A1-04 + A2-02 through A2-07 MED + A2-06 INSERT + A2-07)
  - Arc updated to reflect new panel count and emotional arc
  - Version string: v003 / Cycle 16

Panel sequence (order):
  A1-04  — NEAR-MISS (classroom near-miss micro-beat)
  A2-02  — VULNERABLE (Byte MCU, cracked eye)
  A2-03  — SKEPTICAL (Cosmo doesn't believe — RESTAGED v002)
  A2-04  — INVESTIGATING + REFUSING (montage v002, Byte non-participant)
  A2-05b — DETERMINED (Cosmo with app, pre-failure)
  A2-06 MED — HOPEFUL (Cosmo+Luma two-shot, expectant)
  A2-06 INSERT — FAILURE (phone screen crash)
  A2-07  — RESIGNED (Byte chooses trust — ECU, most important Act 2 beat)

Emotional arc should now read:
  NEAR-MISS → VULNERABLE → SKEPTICAL → INVESTIGATING → DETERMINED → HOPEFUL → FAILURE → RESIGNED

Output:
  /home/wipkat/team/output/storyboards/act2/LTG_SB_act2_contact_sheet_v003.png
"""

from PIL import Image, ImageDraw, ImageFont
import os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
ACT2_DIR    = "/home/wipkat/team/output/storyboards/act2"
OUTPUT_PATH = os.path.join(ACT2_DIR, "LTG_SB_act2_contact_sheet_v003.png")

os.makedirs(ACT2_DIR, exist_ok=True)

# Panels in arc sequence — (filepath, short_label, arc_label)
PANEL_SEQUENCE = [
    (PANELS_DIR + "/LTG_SB_act2_panel_a104_v001.png",
     "A1-04\nnear-miss", "NEAR-MISS"),
    (PANELS_DIR + "/LTG_SB_act2_panel_a202_v001.png",
     "A2-02\nByte MCU", "VULNERABLE"),
    (PANELS_DIR + "/LTG_SB_act2_panel_a203_v002.png",
     "A2-03\nskeptic v2", "SKEPTICAL"),
    (PANELS_DIR + "/LTG_SB_act2_panel_a204_v002.png",
     "A2-04\nmontage v2", "INVESTIGATING"),
    (PANELS_DIR + "/LTG_SB_act2_panel_a205b_v001.png",
     "A2-05b\napp setup", "DETERMINED"),
    (PANELS_DIR + "/LTG_SB_act2_panel_a206_med_v001.png",
     "A2-06 MED\nhopeful", "HOPEFUL"),
    (PANELS_DIR + "/LTG_SB_act2_panel_a206_v001.png",
     "A2-06\nfailure", "FAILURE"),
    (PANELS_DIR + "/LTG_SB_act2_panel_a207_v002.png",
     "A2-07\nresigned", "RESIGNED"),
]

THUMB_W   = 156
THUMB_H   = 88
MARGIN    = 10
GUTTER    = 6
LABEL_H   = 24
HEADER_H  = 34
ROW1_N    = 4    # first row: 4 panels
ROW2_N    = 4    # second row: 4 panels


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
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


def generate():
    font     = load_font(11)
    font_b   = load_font(11, bold=True)
    font_cap = load_font(10)
    font_ann = load_font(9)

    n_panels = len(PANEL_SEQUENCE)

    # Sheet dimensions: 4 columns × 2 rows
    sheet_w = MARGIN * 2 + THUMB_W * ROW1_N + GUTTER * (ROW1_N - 1)
    row_h   = THUMB_H + LABEL_H
    sheet_h = (HEADER_H + MARGIN
               + row_h + GUTTER + MARGIN
               + row_h + MARGIN)

    sheet = Image.new('RGB', (sheet_w, sheet_h), (15, 12, 10))
    sd    = ImageDraw.Draw(sheet)

    # ── Header ────────────────────────────────────────────────────────────────
    sd.text((MARGIN, 6), "ACT 2 CONTACT SHEET — Luma & the Glitchkin",
            font=font_b, fill=(210, 200, 170))
    sd.text((sheet_w - 150, 6), "v003 — Cycle 16",
            font=font_ann, fill=(150, 140, 110))
    # Arc summary line
    sd.text((MARGIN, 20),
            "ARC: NEAR-MISS → VULNERABLE → SKEPTICAL → INVESTIGATING → DETERMINED → HOPEFUL → FAILURE → RESIGNED",
            font=font_ann, fill=(120, 180, 140))
    sd.line([MARGIN, HEADER_H - 2, sheet_w - MARGIN, HEADER_H - 2],
            fill=(50, 44, 36), width=1)

    # ── Arc emotion color scale (cold → warm → cold) ─────────────────────────
    arc_colors = {
        "NEAR-MISS":    (200, 160, 60),
        "VULNERABLE":   (0, 200, 220),
        "SKEPTICAL":    (220, 160, 40),
        "INVESTIGATING":(120, 200, 120),
        "DETERMINED":   (180, 220, 80),
        "HOPEFUL":      (240, 220, 100),
        "FAILURE":      (220, 60, 60),
        "RESIGNED":     (80, 140, 200),
    }

    # ── Place panels in 2 rows of 4 ──────────────────────────────────────────
    for idx, (fpath, label, arc_lbl) in enumerate(PANEL_SEQUENCE):
        row = 0 if idx < ROW1_N else 1
        col = idx if row == 0 else idx - ROW1_N

        x = MARGIN + col * (THUMB_W + GUTTER)
        y = HEADER_H + MARGIN + row * (row_h + GUTTER + MARGIN)

        # Arc label (above thumbnail)
        arc_col = arc_colors.get(arc_lbl, (160, 160, 140))
        sd.text((x + 2, y - 14), arc_lbl, font=font_ann, fill=arc_col)

        # Load and resize panel
        try:
            pimg = Image.open(fpath).resize((THUMB_W, THUMB_H), Image.LANCZOS)
        except Exception:
            pimg = Image.new('RGB', (THUMB_W, THUMB_H), (38, 28, 20))
            pd   = ImageDraw.Draw(pimg)
            pd.text((6, THUMB_H // 2 - 6), "PENDING", font=font_cap,
                    fill=(150, 130, 100))

        sheet.paste(pimg, (x, y))

        # Border
        sd.rectangle([x - 1, y - 1, x + THUMB_W, y + THUMB_H],
                     outline=arc_col, width=1)

        # Label below thumbnail
        lines = label.split('\n')
        sd.text((x + 2, y + THUMB_H + 2), lines[0],
                font=font_ann, fill=(180, 170, 140))
        if len(lines) > 1:
            sd.text((x + 2, y + THUMB_H + 12), lines[1],
                    font=font_ann, fill=(130, 120, 95))

        # Sequence connector arrow (between thumbnails in same row)
        if col < (ROW1_N - 1):
            ax  = x + THUMB_W + GUTTER // 2
            ay  = y + THUMB_H // 2
            sd.line([ax - 3, ay, ax + 2, ay], fill=(80, 100, 80), width=2)
            sd.polygon([(ax + 2, ay - 3), (ax + 2, ay + 3), (ax + 6, ay)],
                       fill=(80, 100, 80))

    # Wrap arrow from row1 end to row2 start (↓ indicator)
    # Arrow from last panel row1 down-left to first panel row2
    r1_last_x = MARGIN + (ROW1_N - 1) * (THUMB_W + GUTTER) + THUMB_W
    r1_y      = HEADER_H + MARGIN + THUMB_H // 2
    r2_y      = HEADER_H + MARGIN + row_h + GUTTER + MARGIN + THUMB_H // 2
    # Down arrow at right edge
    sd.line([r1_last_x + 4, r1_y, r1_last_x + 4, r2_y], fill=(80, 100, 80), width=2)
    sd.polygon([(r1_last_x + 1, r2_y - 4),
                (r1_last_x + 7, r2_y - 4),
                (r1_last_x + 4, r2_y)],
               fill=(80, 100, 80))
    # Left arrow at bottom of right edge to row2 start
    r2_start_x = MARGIN + THUMB_W
    sd.line([r1_last_x + 4, r2_y, MARGIN + 2, r2_y], fill=(80, 100, 80), width=2)
    sd.polygon([(MARGIN + 2, r2_y - 3), (MARGIN + 2, r2_y + 3), (MARGIN - 2, r2_y)],
               fill=(80, 100, 80))

    # ── Footer note ───────────────────────────────────────────────────────────
    footer_y = sheet_h - 14
    sd.text((MARGIN, footer_y),
            "v003 | Cycle 16 | A2-03 restaged | A2-04 Byte added | A2-06 MED added | A2-07 UNBLOCKED",
            font=font_ann, fill=(100, 95, 80))

    sheet.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
    print("Act 2 contact sheet v003 generation complete (Cycle 16).")
