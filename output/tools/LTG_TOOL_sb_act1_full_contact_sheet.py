#!/usr/bin/env python3
"""
LTG_TOOL_sb_act1_full_contact_sheet.py
Act 1 Full Contact Sheet v001 — Cycle 20
Lee Tanaka, Storyboard Artist

Purpose:
  Combines ALL known Act 1 storyboard panels into a single contact sheet:
    - Kitchen cold open: A1-01 through A1-04 (4 panels)
    - Classroom near-miss: A1-04 classroom (separate beat, existing in panels dir)
  Total: 5 panels

Panel sequence (arc order):
  A1-01 KITCHEN  — QUIET       (kitchen establishing WIDE, morning)
  A1-02 KITCHEN  — SEARCHING   (Luma arrival MEDIUM, turning toward TV)
  A1-03 KITCHEN  — DISCOVERY   (MCU — face fills frame, CRT glow, Glitchkin shapes)
  A1-04 KITCHEN  — FIRST-CONTACT (Two-shot — Luma SURPRISED / Byte INDIGNANT on CRT)
  A1-04 CLASSROOM — NEAR-MISS  (classroom — Byte in eraser tray, sight-line, "almost...")

Emotional arc:
  QUIET → SEARCHING → DISCOVERY → FIRST-CONTACT → NEAR-MISS

Note on naming:
  A1-04 (kitchen) = LTG_SB_act1_panel_a104.png  (cold open last beat)
  A1-04 (classroom) = LTG_SB_act2_panel_a104.png (separate near-miss beat,
    previously shown in Act 2 contact sheet as the A2-sequence setup panel)

Output:
  /home/wipkat/team/output/storyboards/LTG_SB_act1_full_contact_sheet.png
"""

from PIL import Image, ImageDraw, ImageFont
import os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_DIR  = "/home/wipkat/team/output/storyboards"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "LTG_SB_act1_full_contact_sheet.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Panels in arc sequence — (filepath, short_label, arc_label, arc_color_rgb, section)
PANEL_SEQUENCE = [
    (PANELS_DIR + "/LTG_SB_act1_panel_a101.png",
     "A1-01\nkitchen wide",  "QUIET",          (180, 160, 100),  "COLD OPEN — Kitchen"),
    (PANELS_DIR + "/LTG_SB_act1_panel_a102.png",
     "A1-02\narrival MED",   "SEARCHING",      (200, 180, 120),  "COLD OPEN — Kitchen"),
    (PANELS_DIR + "/LTG_SB_act1_panel_a103.png",
     "A1-03\ndiscovery MCU", "DISCOVERY",      (0, 200, 180),    "COLD OPEN — Kitchen"),
    (PANELS_DIR + "/LTG_SB_act1_panel_a104.png",
     "A1-04\nfirst contact", "FIRST-CONTACT",  (220, 200, 60),   "COLD OPEN — Kitchen"),
    (PANELS_DIR + "/LTG_SB_act2_panel_a104.png",
     "A1-04\nclassroom",     "NEAR-MISS",      (200, 140, 60),   "Act 1 — Classroom"),
]

# Layout: 1 row of 5 panels
ROW_LAYOUT = [5]

THUMB_W    = 180
THUMB_H    = 101
MARGIN     = 14
GUTTER     = 8
LABEL_H    = 30
HEADER_H   = 52
ARC_LBL_H  = 18
SECTION_H  = 14   # section divider bar height above first row


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
    font_b   = load_font(12, bold=True)
    font     = load_font(11)
    font_cap = load_font(10)
    font_ann = load_font(9)

    n_panels  = len(PANEL_SEQUENCE)
    max_cols  = max(ROW_LAYOUT)
    n_rows    = len(ROW_LAYOUT)

    # Sheet dimensions
    sheet_w = MARGIN * 2 + THUMB_W * max_cols + GUTTER * (max_cols - 1)
    row_h   = SECTION_H + ARC_LBL_H + THUMB_H + LABEL_H
    sheet_h = HEADER_H + MARGIN + n_rows * row_h + GUTTER * (n_rows - 1) + MARGIN + 18

    sheet = Image.new('RGB', (sheet_w, sheet_h), (14, 11, 9))
    sd    = ImageDraw.Draw(sheet)

    # ── Header ────────────────────────────────────────────────────────────────
    sd.text((MARGIN, 6), "ACT 1 FULL CONTACT SHEET — Luma & the Glitchkin",
            font=font_b, fill=(210, 200, 170))
    sd.text((sheet_w - 155, 6), "v001 — Cycle 20",
            font=font_ann, fill=(150, 140, 110))
    arc_text = "ARC: QUIET → SEARCHING → DISCOVERY → FIRST-CONTACT → NEAR-MISS"
    sd.text((MARGIN, 22), arc_text, font=font_ann, fill=(120, 180, 140))
    sd.text((MARGIN, 34),
            "Kitchen cold open (4 panels) + Classroom near-miss (1 panel) | 5 panels total",
            font=font_ann, fill=(120, 110, 90))
    sd.line([MARGIN, HEADER_H - 3, sheet_w - MARGIN, HEADER_H - 3],
            fill=(50, 44, 36), width=1)

    # ── Place panels row by row ───────────────────────────────────────────────
    panel_idx = 0
    prev_section = None

    for row_idx, row_count in enumerate(ROW_LAYOUT):
        y_base = HEADER_H + MARGIN + row_idx * (row_h + GUTTER)

        # Center the row if fewer panels than max_cols
        row_offset_x = (max_cols - row_count) * (THUMB_W + GUTTER) // 2

        for col in range(row_count):
            if panel_idx >= n_panels:
                break
            fpath, label, arc_lbl, arc_col, section = PANEL_SEQUENCE[panel_idx]

            x = MARGIN + row_offset_x + col * (THUMB_W + GUTTER)

            # Section label bar — draw once per section change
            if section != prev_section:
                section_y = y_base
                # Draw section label background stripe for this panel's column
                sd.rectangle([x - 2, section_y, x + THUMB_W + 1, section_y + SECTION_H - 1],
                             fill=(30, 26, 20))
                sd.text((x + 4, section_y + 2), section,
                        font=font_ann, fill=(160, 150, 110))
                # Vertical separator if this is the classroom section
                if section == "Act 1 — Classroom":
                    sd.line([x - 5, section_y, x - 5, section_y + row_h],
                            fill=(80, 60, 40), width=2)
                prev_section = section

            y = y_base + SECTION_H + ARC_LBL_H  # thumbnail top

            # Arc label above thumbnail
            sd.text((x + 2, y - ARC_LBL_H + 2), arc_lbl,
                    font=font_ann, fill=arc_col)

            # Load and resize panel
            try:
                pimg = Image.open(fpath).resize((THUMB_W, THUMB_H), Image.LANCZOS)
            except Exception:
                pimg = Image.new('RGB', (THUMB_W, THUMB_H), (38, 28, 20))
                pd   = ImageDraw.Draw(pimg)
                pd.text((6, THUMB_H // 2 - 6), "MISSING",
                        font=font_cap, fill=(200, 80, 60))

            sheet.paste(pimg, (x, y))

            # Refresh draw after paste
            sd = ImageDraw.Draw(sheet)

            # Colored border (arc color)
            # Slightly thicker border for the classroom panel to mark the scene break
            border_w = 3 if section == "Act 1 — Classroom" else 2
            sd.rectangle([x - 2, y - 2, x + THUMB_W + 1, y + THUMB_H + 1],
                         outline=arc_col, width=border_w)

            # Label below
            lines = label.split('\n')
            sd.text((x + 2, y + THUMB_H + 3), lines[0],
                    font=font_ann, fill=(180, 170, 140))
            if len(lines) > 1:
                sd.text((x + 2, y + THUMB_H + 13), lines[1],
                        font=font_ann, fill=(120, 110, 88))

            # Sequence connector arrow within same row (skip before classroom section break)
            if col < row_count - 1:
                next_section = PANEL_SEQUENCE[panel_idx + 1][4] if (panel_idx + 1) < n_panels else section
                gap_cx = x + THUMB_W + 2
                gap_cy = y + THUMB_H // 2
                # Different arrow color to mark scene break
                arrow_col = (100, 70, 40) if next_section != section else (70, 90, 70)
                sd.line([gap_cx, gap_cy, gap_cx + GUTTER - 4, gap_cy],
                        fill=arrow_col, width=2)
                sd.polygon([(gap_cx + GUTTER - 4, gap_cy - 3),
                             (gap_cx + GUTTER - 4, gap_cy + 3),
                             (gap_cx + GUTTER, gap_cy)],
                           fill=arrow_col)

            panel_idx += 1

    # ── Footer ────────────────────────────────────────────────────────────────
    footer_y = sheet_h - 14
    sd.text((MARGIN, footer_y),
            ("v001 | Cycle 20 | 5 panels | "
             "A1-01..A1-04 kitchen cold open + A1-04 classroom near-miss | "
             "A1-03 uses v002 (MCU rebuild)"),
            font=font_ann, fill=(100, 95, 80))

    sheet.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
    print("Act 1 full contact sheet v001 generation complete (Cycle 20).")
