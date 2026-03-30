# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_sb_act1_contact_sheet.py
Act 1 Cold Open Contact Sheet v002 — Cycle 19
Lee Tanaka, Storyboard Artist

Changes from v001:
  - Uses A1-03 v002 (MCU rebuild per Critique Cycle 9 — face fills 50%+ frame,
    CRT off-frame lower-left, amber-green left cheek glow, asymmetric eyes)
  - Version string updated to Cycle 19 / v002

Panel sequence (arc order):
  A1-01 — ESTABLISHING  (QUIET — kitchen, morning, CRT glow visible)
  A1-02 — ARRIVAL       (CURIOUS — Luma enters, spots TV)
  A1-03 — DISCOVERY     (CURIOUS/SURPRISED — MCU v002 — she SEES them)
  A1-04 — FIRST CONTACT (SURPRISED — Byte appears, reaction)

Arc colors (border):
  QUIET       → warm amber:        (200, 170, 80)
  CURIOUS     → cyan-teal:         (0,  200, 210)
  SURPRISED   → bright cyan:       (0,  240, 255)

Layout: 2×2 grid
Output:
  /home/wipkat/team/output/storyboards/LTG_SB_act1_coldopen_contact_sheet.png
"""

from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_DIR  = "/home/wipkat/team/output/storyboards"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "LTG_SB_act1_coldopen_contact_sheet.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Panel sequence: (filepath, beat_label, arc_label, arc_color_rgb)
PANEL_SEQUENCE = [
    (PANELS_DIR + "/LTG_SB_act1_panel_a101.png",
     "A1-01\nestablishing", "ESTABLISHING", (200, 170, 80)),
    (PANELS_DIR + "/LTG_SB_act1_panel_a102.png",
     "A1-02\narrival",      "ARRIVAL",      (0,  200, 210)),
    (PANELS_DIR + "/LTG_SB_act1_panel_a103.png",     # v002 — MCU rebuild
     "A1-03\ndiscovery v2", "DISCOVERY",    (0,  210, 220)),
    (PANELS_DIR + "/LTG_SB_act1_panel_a104.png",
     "A1-04\nfirst contact","FIRST CONTACT",(0,  240, 255)),
]

# Layout: 2x2
COLS = 2
ROWS = 2

THUMB_W  = 300
THUMB_H  = 168
MARGIN   = 20
GUTTER   = 12
LABEL_H  = 32
HEADER_H = 52
FOOTER_H = 28
BORDER_W = 5

TOTAL_W = MARGIN * 2 + COLS * THUMB_W + (COLS - 1) * GUTTER + BORDER_W * 2 * COLS
TOTAL_H = HEADER_H + MARGIN + ROWS * (THUMB_H + LABEL_H) + (ROWS - 1) * GUTTER + MARGIN + FOOTER_H

BG_COLOR     = (18, 14, 10)
HEADER_COLOR = (28, 22, 16)
TEXT_HEADER  = (240, 225, 180)
TEXT_LABEL   = (220, 210, 175)
TEXT_ARC     = (200, 195, 160)
TEXT_FOOTER  = (130, 120, 95)
DIVIDER_COL  = (45, 38, 28)


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()


def ensure_panels_exist():
    """Run each panel generator if its output doesn't exist."""
    generators = [
        "/home/wipkat/team/output/tools/LTG_TOOL_sb_panel_a101.py",
        "/home/wipkat/team/output/tools/LTG_TOOL_sb_panel_a102.py",
        "/home/wipkat/team/output/tools/LTG_TOOL_sb_panel_a103.py",   # v002
        "/home/wipkat/team/output/tools/LTG_TOOL_sb_panel_a104_kitchen.py",
    ]
    outputs = [
        PANELS_DIR + "/LTG_SB_act1_panel_a101.png",
        PANELS_DIR + "/LTG_SB_act1_panel_a102.png",
        PANELS_DIR + "/LTG_SB_act1_panel_a103.png",
        PANELS_DIR + "/LTG_SB_act1_panel_a104.png",
    ]
    for gen, out in zip(generators, outputs):
        if not os.path.exists(out):
            print(f"Generating: {out}")
            result = subprocess.run(["python3", gen], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"  ERROR: {result.stderr}")
            else:
                print(f"  OK: {result.stdout.strip()}")
        else:
            print(f"  Exists: {out}")


def make_contact_sheet():
    font_title = load_font(22, bold=True)
    font_arc   = load_font(14, bold=True)
    font_label = load_font(12)
    font_sub   = load_font(11)
    font_foot  = load_font(10)

    img  = Image.new('RGB', (TOTAL_W, TOTAL_H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # ── Header ────────────────────────────────────────────────────────────────
    draw.rectangle([0, 0, TOTAL_W, HEADER_H], fill=HEADER_COLOR)
    draw.line([0, HEADER_H, TOTAL_W, HEADER_H], fill=DIVIDER_COL, width=2)

    draw.text((MARGIN, 10), "Act 1 — Cold Open", font=font_title, fill=TEXT_HEADER)
    draw.text((MARGIN, 34),
              '"Luma & the Glitchkin"  |  Kitchen Cold Open  |  Cycle 19  |  Lee Tanaka',
              font=font_sub, fill=TEXT_ARC)

    arc_text = "QUIET  →  CURIOUS  →  SURPRISED"
    draw.text((TOTAL_W - 310, 18), arc_text, font=font_sub, fill=(200, 190, 140))

    # ── Panels ────────────────────────────────────────────────────────────────
    panel_idx = 0
    for row in range(ROWS):
        for col in range(COLS):
            if panel_idx >= len(PANEL_SEQUENCE):
                break

            filepath, short_label, arc_label, arc_color = PANEL_SEQUENCE[panel_idx]

            cell_x = MARGIN + col * (THUMB_W + GUTTER + BORDER_W * 2)
            cell_y = HEADER_H + MARGIN + row * (THUMB_H + LABEL_H + GUTTER + BORDER_W * 2)

            thumb_x = cell_x + BORDER_W
            thumb_y = cell_y + BORDER_W

            # Arc-colored border
            draw.rectangle([cell_x, cell_y,
                             cell_x + THUMB_W + BORDER_W * 2,
                             cell_y + THUMB_H + BORDER_W * 2 + LABEL_H],
                            outline=arc_color, width=BORDER_W)

            # Load and paste thumbnail
            if os.path.exists(filepath):
                try:
                    panel_img = Image.open(filepath).convert('RGB')
                    thumb = panel_img.resize((THUMB_W, THUMB_H), Image.LANCZOS)
                    img.paste(thumb, (thumb_x, thumb_y))
                except Exception as e:
                    draw.rectangle([thumb_x, thumb_y,
                                    thumb_x + THUMB_W, thumb_y + THUMB_H],
                                   fill=(45, 35, 25))
                    draw.text((thumb_x + 10, thumb_y + THUMB_H // 2 - 10),
                              f"ERROR: {e}", font=font_sub, fill=(200, 80, 80))
            else:
                draw.rectangle([thumb_x, thumb_y,
                                 thumb_x + THUMB_W, thumb_y + THUMB_H],
                                fill=(38, 30, 20))
                draw.text((thumb_x + 8, thumb_y + THUMB_H // 2 - 18),
                           "MISSING PANEL", font=font_label, fill=(180, 80, 60))
                draw.text((thumb_x + 8, thumb_y + THUMB_H // 2),
                           os.path.basename(filepath), font=font_sub, fill=(150, 100, 80))

            # Refresh draw after paste
            draw = ImageDraw.Draw(img)

            # Label area below thumbnail
            label_y = thumb_y + THUMB_H + 2

            # Arc label
            draw.text((thumb_x + 6, label_y + 2), arc_label,
                      font=font_arc, fill=arc_color)

            # Short label
            label_lines = short_label.split('\n')
            for li, ll in enumerate(label_lines):
                draw.text((thumb_x + THUMB_W - 95, label_y + 2 + li * 11),
                          ll, font=font_label, fill=TEXT_LABEL)

            panel_idx += 1

    # ── Arc flow connector lines ──────────────────────────────────────────────
    # Row 1: A1-01 → A1-02
    r1_arrow_x = MARGIN + THUMB_W + BORDER_W * 2
    r1_arrow_y = HEADER_H + MARGIN + THUMB_H // 2 + BORDER_W
    draw.line([(r1_arrow_x + 2, r1_arrow_y),
               (r1_arrow_x + GUTTER - 2, r1_arrow_y)],
              fill=(200, 190, 140), width=2)
    draw.polygon([(r1_arrow_x + GUTTER - 2, r1_arrow_y),
                  (r1_arrow_x + GUTTER - 8, r1_arrow_y - 4),
                  (r1_arrow_x + GUTTER - 8, r1_arrow_y + 4)],
                 fill=(200, 190, 140))

    # Vertical connector row 1 → row 2
    row_gap_x = MARGIN + THUMB_W + BORDER_W * 2 + GUTTER // 2
    row1_bot  = HEADER_H + MARGIN + THUMB_H + LABEL_H + BORDER_W * 2
    row2_top  = HEADER_H + MARGIN + (THUMB_H + LABEL_H + GUTTER + BORDER_W * 2)
    draw.line([(row_gap_x, row1_bot), (row_gap_x, row2_top)],
              fill=(160, 150, 110), width=1)

    # Row 2: A1-03 → A1-04
    r2_arrow_x = MARGIN + THUMB_W + BORDER_W * 2
    r2_arrow_y = HEADER_H + MARGIN + (THUMB_H + LABEL_H + GUTTER + BORDER_W * 2) + THUMB_H // 2 + BORDER_W
    draw.line([(r2_arrow_x + 2, r2_arrow_y),
               (r2_arrow_x + GUTTER - 2, r2_arrow_y)],
              fill=(0, 220, 240), width=2)
    draw.polygon([(r2_arrow_x + GUTTER - 2, r2_arrow_y),
                  (r2_arrow_x + GUTTER - 8, r2_arrow_y - 4),
                  (r2_arrow_x + GUTTER - 8, r2_arrow_y + 4)],
                 fill=(0, 220, 240))

    # ── Footer ────────────────────────────────────────────────────────────────
    foot_y = TOTAL_H - FOOTER_H
    draw.line([0, foot_y, TOTAL_W, foot_y], fill=DIVIDER_COL, width=1)
    draw.text((MARGIN, foot_y + 8),
              'Act 1 Cold Open — 4 panels — QUIET → CURIOUS → SURPRISED  |  A1-03 MCU rebuild (v002)',
              font=font_foot, fill=TEXT_FOOTER)
    draw.text((TOTAL_W - 300, foot_y + 8),
              "LTG_SB_act1_coldopen_contact_sheet_v002  |  Cycle 19",
              font=font_foot, fill=(110, 100, 78))

    draw.rectangle([0, 0, TOTAL_W - 1, TOTAL_H - 1], outline=DIVIDER_COL, width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    ensure_panels_exist()
    make_contact_sheet()
    print("Act 1 cold open contact sheet v002 generation complete (Cycle 19).")
