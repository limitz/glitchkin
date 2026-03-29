#!/usr/bin/env python3
"""
Contact Sheet Generator — Luma & the Glitchkin
Cycle 10: Combines ALL rendered panels in chronological order.
Updated to include P14–P24 (The Chaos Sequence). Version string fixed per Carmen's Cycle 9 critique.

Output: /home/wipkat/team/output/storyboards/panels/contact_sheet.png

MEMORY.md lesson: The contact sheet is the FIRST TEST.
Read the strip before individual panels. If the arc doesn't read in
thumbnail, there's a structural problem.

Panel sequence for cold open:
P01 → P02 → P03 → P04 → P05 → P06 → P07 →
P08 → P09 → P10 → P11 → P12 → P13 →
P14 → P15 → P16 → P17 → P18 → P19 → P20 →
P21 → P22 → P22a → P23 → P24 → P25
"""

from PIL import Image, ImageDraw, ImageFont
import os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "contact_sheet.png")

PW, PH = 480, 270   # individual panel dimensions

# All panels in chronological order
# Format: (panel_num_label, filename)
PANEL_ORDER = [
    ("P01",  "panel_p01_exterior.png"),
    ("P02",  "panel_p02_exterior_close.png"),
    ("P03",  "panel_p03_first_pixel.png"),
    ("P04",  "panel_p04_interior_wide.png"),
    ("P05",  "panel_p05_monitor_mcu.png"),
    ("P06",  "panel_p06_byte_emerging.png"),
    ("P07",  "panel_p07_approach.png"),
    ("P08",  "panel_p08_byte_real_world.png"),
    ("P09",  "panel_p09_byte_sees_luma.png"),
    ("P10",  "panel_p10_ots_byte_luma.png"),
    ("P11",  "panel_p11_nose_to_nose.png"),
    ("P12",  "panel_p12_recoil.png"),
    ("P13",  "panel_p13_scream.png"),
    # Cycle 10: The Chaos Sequence (P14–P24)
    ("P14",  "panel_p14_bookshelf_ricochet.png"),
    ("P15",  "panel_p15_luma_freefall.png"),
    ("P16",  "panel_p16_floor_ecu.png"),
    ("P17",  "panel_p17_quiet_beat.png"),
    ("P18",  "panel_p18_notebook_turn.png"),
    ("P19",  "panel_p19_byte_reaction.png"),
    ("P20",  "panel_p20_twoshot_calm.png"),
    ("P21",  "panel_p21_chaos_overhead.png"),
    ("P22",  "panel_p22_monitor_breach.png"),
    ("P22a", "panel_p22a_shoulder_bridge.png"),
    ("P23",  "panel_p23_promise_shot.png"),
    ("P24",  "panel_p24_breach_apex.png"),
    # Title card
    ("P25",  "panel_p25_title_card.png"),
]

COLS = 5         # panels per row
PAD  = 6         # padding between panels
HEADER_H = 60    # header row height
FOOTER_H = 28    # footer row height
LABEL_H  = 18    # label bar height under each panel in the sheet


def generate():
    # Load available panels (skip missing files gracefully)
    loaded = []
    for label, fname in PANEL_ORDER:
        path = os.path.join(PANELS_DIR, fname)
        if os.path.exists(path):
            img = Image.open(path)
            loaded.append((label, img))
        else:
            print(f"  [SKIP] {fname} — not found")

    if not loaded:
        print("No panels found. Exiting.")
        return

    n      = len(loaded)
    rows   = (n + COLS - 1) // COLS

    # Thumbnail size (slightly smaller than full panel — fit more per row)
    THUMB_W = PW // 2      # 240
    THUMB_H = PH // 2      # 135

    cs_w = PAD + COLS * (THUMB_W + PAD)
    cs_h = HEADER_H + rows * (THUMB_H + LABEL_H + PAD) + FOOTER_H

    cs = Image.new('RGB', (cs_w, cs_h), (14, 10, 8))
    d  = ImageDraw.Draw(cs)

    # ── Load fonts ─────────────────────────────────────────────────────────
    try:
        font_hdr   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_sub   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
        font_foot  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except Exception:
        fb = ImageFont.load_default()
        font_hdr = font_sub = font_label = font_foot = fb

    # ── Header bar ─────────────────────────────────────────────────────────
    d.rectangle([0, 0, cs_w, HEADER_H], fill=(20, 14, 10))
    d.rectangle([0, HEADER_H - 1, cs_w, HEADER_H], fill=(0, 180, 200))  # teal rule

    d.text((PAD, 8), "LUMA & THE GLITCHKIN", fill=(0, 240, 255), font=font_hdr)
    d.text((PAD, 30), "Ep.01 Cold Open — Cycle 10 Contact Sheet (P01–P25 complete)", fill=(200, 190, 165), font=font_sub)
    d.text((cs_w - 160, 8),  f"{n} panels rendered", fill=(140, 130, 110), font=font_sub)
    d.text((cs_w - 160, 24), "2026-03-29 Cycle 10", fill=(120, 110, 90), font=font_foot)

    # ── Place panels in grid ────────────────────────────────────────────────
    for i, (label, img) in enumerate(loaded):
        col = i % COLS
        row = i // COLS

        x = PAD + col * (THUMB_W + PAD)
        y = HEADER_H + PAD + row * (THUMB_H + LABEL_H + PAD)

        # Resize to thumbnail
        thumb = img.resize((THUMB_W, THUMB_H), Image.LANCZOS)
        cs.paste(thumb, (x, y))

        # Thin border around thumbnail
        d.rectangle([x - 1, y - 1, x + THUMB_W, y + THUMB_H], outline=(40, 30, 20), width=1)

        # Label bar below thumbnail
        label_y = y + THUMB_H
        d.rectangle([x, label_y, x + THUMB_W, label_y + LABEL_H], fill=(20, 14, 10))
        d.text((x + 4, label_y + 4), label, fill=(0, 200, 220), font=font_label)

    # ── Emotional arc annotation bar ───────────────────────────────────────
    # Minimal beat markers under each row of panels — helps read arc at a glance
    arc_labels = [
        ("QUIET →",        0),        # P01-P05: setup / quiet warmth
        ("CURIOUS →",      COLS),     # P06-P10: Byte enters / investigates
        ("BREACH →",       COLS * 2), # P11-P13: discovery / scream
        ("CHAOS →",        COLS * 3), # P14-P19: ricochet / floor / discovery
        ("PEAK CHAOS →",   COLS * 4), # P20-P24: Glitchkin breach / promise shot
    ]
    arc_y = HEADER_H + PAD + rows * (THUMB_H + LABEL_H + PAD) + 4
    for arc_text, panel_start_idx in arc_labels:
        if panel_start_idx < n:
            arc_col_x = PAD + (panel_start_idx % COLS) * (THUMB_W + PAD)
            arc_row_y = HEADER_H + PAD + (panel_start_idx // COLS) * (THUMB_H + LABEL_H + PAD)
            # Small arc marker above the row
            d.text((arc_col_x, arc_row_y - 12), arc_text, fill=(120, 100, 70), font=font_foot)

    # ── Footer ─────────────────────────────────────────────────────────────
    footer_y = cs_h - FOOTER_H
    d.rectangle([0, footer_y, cs_w, cs_h], fill=(16, 11, 8))
    d.rectangle([0, footer_y, cs_w, footer_y + 1], fill=(50, 38, 22))  # warm rule
    d.text((PAD, footer_y + 8),
           "Storyboard: Lee Tanaka  |  Art Dir: Alex Chen  |  'Luma & the Glitchkin' Ep.01",
           fill=(100, 90, 70), font=font_foot)
    d.text((PAD, footer_y + 18),
           "Color: warm amber/terracotta (house) vs cold CRT teal (Byte/glitch intruder)",
           fill=(80, 72, 58), font=font_foot)

    cs.save(OUTPUT_PATH)
    print(f"Saved contact sheet: {OUTPUT_PATH}")
    print(f"  Size: {cs_w}x{cs_h}  |  Panels: {n}  |  Grid: {COLS}x{rows}")


if __name__ == '__main__':
    generate()
