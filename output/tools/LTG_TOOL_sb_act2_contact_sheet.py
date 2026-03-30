#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_act2_contact_sheet.py
Act 2 Contact Sheet v006 — Cycle 20
Lee Tanaka, Storyboard Artist

Changes from v005:
  - A2-02 updated to LTG_SB_act2_panel_a202.png (Maya Santos Cycle 18 rebuild)
  - Arc label for A2-02 updated to "VULNERABLE (RESIGNED-55%)"
  - Total: 12 panels (unchanged)
  - Layout: 3-row, 4/4/4 panels per row (unchanged)
  - Version string: v006 / Cycle 20

Panel sequence (arc order):
  A1-04  — NEAR-MISS (classroom near-miss micro-beat)
  A2-01  — ESTABLISHED (Tech Den wide, Act 2 opener)
  A2-02  — VULNERABLE (RESIGNED-55%) (Byte MCU v002 — rebuilt by Maya Santos)
  A2-03  — SKEPTICAL (Cosmo doesn't believe — v002)
  A2-04  — INVESTIGATING (montage v002, Byte non-participant)
  A2-05  — WALK+TALK (Millbrook exterior, Luma pitching)
  A2-05b — DETERMINED (Cosmo with app, pre-failure)
  A2-06 MED — HOPEFUL (Cosmo+Luma two-shot, expectant)
  A2-06 INSERT — FAILURE (phone screen crash)
  A2-07  — RESIGNED (Byte chooses trust — ECU)
  A2-07b — BRIDGE (Miri hears something)
  A2-08  — RECOGNITION (Grandma Miri returns — v002 Luma POV)

Emotional arc:
  NEAR-MISS → ESTABLISHED → VULNERABLE (RESIGNED-55%) → SKEPTICAL → INVESTIGATING →
  WALK+TALK → DETERMINED → HOPEFUL → FAILURE → RESIGNED → BRIDGE → RECOGNITION

Output:
  /home/wipkat/team/output/storyboards/act2/LTG_SB_act2_contact_sheet.png
"""

from PIL import Image, ImageDraw, ImageFont
import os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
ACT2_DIR    = "/home/wipkat/team/output/storyboards/act2"
ACT2_PANELS = os.path.join(ACT2_DIR, "panels")
OUTPUT_PATH = os.path.join(ACT2_DIR, "LTG_SB_act2_contact_sheet.png")

os.makedirs(ACT2_DIR, exist_ok=True)

# Panels in arc sequence — (filepath, short_label, arc_label, arc_color_rgb)
PANEL_SEQUENCE = [
    (PANELS_DIR + "/LTG_SB_act2_panel_a104.png",
     "A1-04\nnear-miss",    "NEAR-MISS",               (200, 160, 60)),
    (PANELS_DIR + "/LTG_SB_act2_panel_a201.png",
     "A2-01\nestablishing", "ESTABLISHED",             (200, 180, 120)),
    (ACT2_PANELS + "/LTG_SB_act2_panel_a202.png",
     "A2-02\nByte MCU v2",  "VULNERABLE (RESIGNED-55%)", (0, 200, 220)),
    (PANELS_DIR + "/LTG_SB_act2_panel_a203.png",
     "A2-03\nskeptic v2",   "SKEPTICAL",               (220, 160, 40)),
    (PANELS_DIR + "/LTG_SB_act2_panel_a204.png",
     "A2-04\nmontage v2",   "INVESTIGATING",            (120, 200, 120)),
    (PANELS_DIR + "/LTG_SB_act2_panel_a205.png",
     "A2-05\nwalk+talk",    "WALK+TALK",               (220, 200, 100)),
    (PANELS_DIR + "/LTG_SB_act2_panel_a205b.png",
     "A2-05b\napp setup",   "DETERMINED",              (180, 220, 80)),
    (PANELS_DIR + "/LTG_SB_act2_panel_a206_med.png",
     "A2-06 MED\nhopeful",  "HOPEFUL",                 (240, 220, 100)),
    (PANELS_DIR + "/LTG_SB_act2_panel_a206.png",
     "A2-06\nfailure",      "FAILURE",                 (220, 60, 60)),
    (PANELS_DIR + "/LTG_SB_act2_panel_a207.png",
     "A2-07\nresigned",     "RESIGNED",                (80, 140, 200)),
    (PANELS_DIR + "/LTG_SB_act2_panel_a207b.png",
     "A2-07b\nbridge",      "BRIDGE",                  (160, 140, 80)),
    (PANELS_DIR + "/LTG_SB_act2_panel_a208.png",
     "A2-08\nrecognition",  "RECOGNITION",             (200, 180, 240)),
]

# Layout: 3 rows — 4 / 4 / 4 panels per row (even)
ROW_LAYOUT = [4, 4, 4]

THUMB_W   = 160
THUMB_H   = 90
MARGIN    = 12
GUTTER    = 7
LABEL_H   = 28
HEADER_H  = 42
ARC_LBL_H = 18


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

    n_panels  = len(PANEL_SEQUENCE)
    max_cols  = max(ROW_LAYOUT)
    n_rows    = len(ROW_LAYOUT)

    # Sheet dimensions
    sheet_w = MARGIN * 2 + THUMB_W * max_cols + GUTTER * (max_cols - 1)
    row_h   = ARC_LBL_H + THUMB_H + LABEL_H
    sheet_h = HEADER_H + MARGIN + n_rows * row_h + GUTTER * (n_rows - 1) + MARGIN + 18

    sheet = Image.new('RGB', (sheet_w, sheet_h), (14, 11, 9))
    sd    = ImageDraw.Draw(sheet)

    # ── Header ────────────────────────────────────────────────────────────────
    sd.text((MARGIN, 6), "ACT 2 CONTACT SHEET — Luma & the Glitchkin",
            font=font_b, fill=(210, 200, 170))
    sd.text((sheet_w - 155, 6), "v006 — Cycle 20",
            font=font_ann, fill=(150, 140, 110))
    arc_text = ("ARC: NEAR-MISS → ESTABLISHED → VULNERABLE (RESIGNED-55%) → SKEPTICAL → "
                "INVESTIGATING → WALK+TALK → DETERMINED → HOPEFUL → "
                "FAILURE → RESIGNED → BRIDGE → RECOGNITION")
    sd.text((MARGIN, 20), arc_text, font=font_ann, fill=(120, 180, 140))
    sd.line([MARGIN, HEADER_H - 3, sheet_w - MARGIN, HEADER_H - 3],
            fill=(50, 44, 36), width=1)

    # ── Place panels row by row ───────────────────────────────────────────────
    panel_idx = 0
    for row_idx, row_count in enumerate(ROW_LAYOUT):
        y_base = (HEADER_H + MARGIN
                  + row_idx * (row_h + GUTTER))

        # Center the row if it has fewer panels than max_cols
        row_offset_x = (max_cols - row_count) * (THUMB_W + GUTTER) // 2

        for col in range(row_count):
            if panel_idx >= n_panels:
                break
            fpath, label, arc_lbl, arc_col = PANEL_SEQUENCE[panel_idx]

            x = MARGIN + row_offset_x + col * (THUMB_W + GUTTER)
            y = y_base + ARC_LBL_H   # thumbnail top (arc label sits above)

            # Arc label above thumbnail
            sd.text((x + 2, y - ARC_LBL_H + 2), arc_lbl,
                    font=font_ann, fill=arc_col)

            # Load and resize panel
            try:
                pimg = Image.open(fpath).resize((THUMB_W, THUMB_H), Image.LANCZOS)
            except Exception:
                pimg = Image.new('RGB', (THUMB_W, THUMB_H), (38, 28, 20))
                pd   = ImageDraw.Draw(pimg)
                pd.text((6, THUMB_H // 2 - 6), "PENDING",
                        font=font_cap, fill=(150, 130, 100))

            sheet.paste(pimg, (x, y))

            # Refresh draw after paste
            sd = ImageDraw.Draw(sheet)

            # Colored border (arc color)
            sd.rectangle([x - 2, y - 2, x + THUMB_W + 1, y + THUMB_H + 1],
                         outline=arc_col, width=2)

            # Label below
            lines = label.split('\n')
            sd.text((x + 2, y + THUMB_H + 3), lines[0],
                    font=font_ann, fill=(180, 170, 140))
            if len(lines) > 1:
                sd.text((x + 2, y + THUMB_H + 13), lines[1],
                        font=font_ann, fill=(120, 110, 88))

            # Sequence connector arrow within same row
            if col < row_count - 1:
                gap_cx = x + THUMB_W + 2
                gap_cy = y + THUMB_H // 2
                sd.line([gap_cx, gap_cy, gap_cx + GUTTER - 4, gap_cy],
                        fill=(70, 90, 70), width=2)
                sd.polygon([(gap_cx + GUTTER - 4, gap_cy - 3),
                             (gap_cx + GUTTER - 4, gap_cy + 3),
                             (gap_cx + GUTTER, gap_cy)],
                           fill=(70, 90, 70))

            panel_idx += 1

        # Row continuation arrow (down from end of row to start of next row)
        if row_idx < n_rows - 1:
            last_col  = row_count - 1
            lx = MARGIN + row_offset_x + last_col * (THUMB_W + GUTTER) + THUMB_W + 4
            ly = y_base + ARC_LBL_H + THUMB_H // 2
            ny = y_base + row_h + GUTTER + ARC_LBL_H + THUMB_H // 2
            next_row_count = ROW_LAYOUT[row_idx + 1]
            next_offset_x  = (max_cols - next_row_count) * (THUMB_W + GUTTER) // 2
            start_x = MARGIN + next_offset_x
            sd.line([lx, ly, lx, ny], fill=(70, 90, 70), width=2)
            sd.polygon([(lx - 3, ny - 4), (lx + 3, ny - 4), (lx, ny)],
                       fill=(70, 90, 70))
            sd.line([lx, ny, start_x, ny], fill=(70, 90, 70), width=2)
            sd.polygon([(start_x, ny - 3), (start_x, ny + 3), (start_x - 4, ny)],
                       fill=(70, 90, 70))

    # ── Footer ────────────────────────────────────────────────────────────────
    footer_y = sheet_h - 14
    sd.text((MARGIN, footer_y),
            "v006 | Cycle 20 | 12 panels | A2-02 v002 (Maya Santos rebuild) | arc label: VULNERABLE (RESIGNED-55%)",
            font=font_ann, fill=(100, 95, 80))

    sheet.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
    print("Act 2 contact sheet v006 generation complete (Cycle 20).")
