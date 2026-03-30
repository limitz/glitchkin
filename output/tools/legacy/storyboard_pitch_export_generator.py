#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
Storyboard Pitch Export Generator — Luma & the Glitchkin
Cycle 11: Generates a multi-page pitch-format storyboard layout as a single tall
composite PNG for development-stage pitch presentations.

Layout:
  Page 1  — Title page (logo, episode title, contact sheet thumbnail)
  Page 2  — Panels P01–P07 (6-7 per page grid)
  Page 3  — Panels P08–P14
  Page 4  — Panels P15–P21
  Page 5  — Panels P22–P22a + P25 (bridge + title card)
  Page 6  — Hero spread: P23 + P24 large, side by side

Output: /home/wipkat/team/output/production/storyboard_pitch_export.png
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

# ── Paths ──────────────────────────────────────────────────────────────────────
PANELS_DIR   = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH  = "/home/wipkat/team/output/production/storyboard_pitch_export.png"
LOGO_PATH    = "/home/wipkat/team/output/production/show_logo.png"
CONTACT_PATH = "/home/wipkat/team/output/storyboards/panels/contact_sheet.png"

# ── Page geometry ──────────────────────────────────────────────────────────────
PAGE_W        = 1200
PAGE_MARGIN   = 56
PANEL_GAP     = 18
CAPTION_H     = 44   # height under each thumbnail for text
THUMB_COLS    = 3    # panels per row on body pages
BG_PAGE       = (245, 242, 236)       # warm off-white
BG_TITLEPAGE  = (18, 14, 10)          # near-black (cinematic)
ACCENT_CYAN   = (0, 200, 220)
ACCENT_AMBER  = (200, 140, 50)
TEXT_DARK     = (22, 18, 12)
TEXT_LIGHT    = (228, 220, 200)
TEXT_MID      = (90, 80, 65)
DIVIDER_COL   = (180, 165, 140)

# ── Panel metadata ─────────────────────────────────────────────────────────────
# (panel_num, filename, shot_type, timing, short_description)
PANEL_META = [
    ("01", "panel_p01_exterior.png",           "EXT WIDE",    "2.5s",
     "Millbrook at night — glowing window — owl on wire"),
    ("02", "panel_p02_exterior_close.png",     "EXT WIDE",    "1.5s",
     "House facade — curtains glow amber/teal — circuit doormat"),
    ("03", "panel_p03_first_pixel.png",        "CU OBJ",      "3.0s",
     "CRT monitor — one cyan pixel wakes — pulse, pulse"),
    ("04", "panel_p04_interior_wide.png",      "INT WIDE",    "2.0s",
     "Tech den — Luma asleep sideways on couch — snack wreckage"),
    ("05", "panel_p05_monitor_mcu.png",        "MCU",         "2.0s",
     "Monitor from shelf level — pixel cluster grows — 8-12 now"),
    ("06", "panel_p06_byte_emerging.png",      "CU SCR",      "2.5s",
     "Byte's face pressing through screen — disgusted/curious"),
    ("07", "panel_p07_approach.png",           "MED WIDE",    "1.5s",
     "Monitor looms — Dutch tilt — Luma asleep unaware"),
    ("08", "panel_p08_byte_real_world.png",    "MED",         "2.0s",
     "Byte phases through screen — pixel burst into room"),
    ("09", "panel_p09_byte_sees_luma.png",     "MCU",         "1.5s",
     "Byte freezes mid-float — sees Luma — processing"),
    ("10", "panel_p10_ots_byte_luma.png",      "OTS",         "2.0s",
     "OTS Byte: Luma sleeping — alien discovers sleeping human"),
    ("11", "panel_p11_nose_to_nose.png",       "ECU",         "1.5s",
     "Nose to nose — Byte hovers inches from Luma's face"),
    ("12", "panel_p12_recoil.png",             "MCU",         "1.0s",
     "Luma snort-stirs — Byte recoils — full-body alarm"),
    ("13", "panel_p13_scream.png",             "MED",         "2.0s",
     "They both scream — full-room perspective — chaos begins"),
    ("14", "panel_p14_bookshelf_ricochet.png", "MED",         "1.5s",
     "Byte ricochets off bookshelf — multi-ghost trajectory"),
    ("15", "panel_p15_luma_freefall.png",      "MED",         "0.8s",
     "Luma freefall — glitch makes hair perfect circle — 8 frames"),
    ("16", "panel_p16_floor_ecu.png",          "ECU",         "1.5s",
     "ECU Luma on floor — one eye finds something — focus builds"),
    ("17", "panel_p17_quiet_beat.png",         "MED",         "2.5s",
     "Quiet beat — Luma sits up — chip falls — they watch it"),
    ("18", "panel_p18_notebook_turn.png",      "MED",         "2.0s",
     "Luma turns notebook — margin doodles look like Byte"),
    ("19", "panel_p19_byte_reaction.png",      "CU",          "3.0s",
     "Byte: 'The preferred term is Glitchkin' — offended"),
    ("20", "panel_p20_twoshot_calm.png",       "MED WIDE",    "3.5s",
     "Two-shot — first quiet beat — new normal forming"),
    ("21", "panel_p21_chaos_overhead.png",     "WIDE",        "2.0s",
     "Chaos resumes — high angle — all monitors pressing"),
    ("22", "panel_p22_monitor_breach.png",     "ECU",         "2.0s",
     "ECU monitor: Glitchkin through glass — hand touches — ripple"),
    ("22a","panel_p22a_shoulder_bridge.png",   "MCU",         "0.8s",
     "BRIDGE: Byte lands on shoulder — accident, not choice"),
    ("23", "panel_p23_promise_shot.png",       "MED",         "2.5s",
     "PROMISE SHOT: backs to camera — two vs impossible chaos"),
    ("24", "panel_p24_breach_apex.png",        "WIDE",        "1.5s",
     "HOOK FRAME: breach apex — Dutch tilt — still point in storm"),
    ("25", "panel_p25_title_card.png",         "TITLE",       "3.0s",
     "TITLE CARD: 'Luma & the Glitchkin' — cold open ends"),
]

# Pages 2-5: panel groups (indices into PANEL_META)
PAGE_GROUPS = [
    list(range(0, 7)),    # Page 2: P01-P07
    list(range(7, 14)),   # Page 3: P08-P14
    list(range(14, 21)),  # Page 4: P15-P21
    list(range(21, 26)),  # Page 5: P22-P22a + P23-P25
]


# ── Font loading ───────────────────────────────────────────────────────────────
def load_fonts():
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    try:
        reg_sm  = ImageFont.truetype(paths[0], 12)
        reg_md  = ImageFont.truetype(paths[0], 16)
        reg_lg  = ImageFont.truetype(paths[0], 22)
        bold_sm = ImageFont.truetype(paths[1], 12)
        bold_md = ImageFont.truetype(paths[1], 18)
        bold_lg = ImageFont.truetype(paths[1], 28)
        bold_xl = ImageFont.truetype(paths[1], 42)
        bold_xxl= ImageFont.truetype(paths[1], 58)
    except Exception:
        f = ImageFont.load_default()
        reg_sm = reg_md = reg_lg = bold_sm = bold_md = bold_lg = bold_xl = bold_xxl = f
    return reg_sm, reg_md, reg_lg, bold_sm, bold_md, bold_lg, bold_xl, bold_xxl


def text_width(draw, text, font):
    """Return width of rendered text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def draw_rule(draw, y, x0, x1, color=DIVIDER_COL, width=1):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ── Page 1: Title Page ─────────────────────────────────────────────────────────
def make_title_page(fonts):
    reg_sm, reg_md, reg_lg, bold_sm, bold_md, bold_lg, bold_xl, bold_xxl = fonts
    page_h = 900
    img = Image.new("RGB", (PAGE_W, page_h), BG_TITLEPAGE)
    draw = ImageDraw.Draw(img)

    # Subtle warm vignette grid lines (decorative)
    for x in range(0, PAGE_W, 60):
        draw.line([(x, 0), (x, page_h)], fill=(28, 22, 15), width=1)
    for y in range(0, page_h, 60):
        draw.line([(0, y), (PAGE_W, y)], fill=(28, 22, 15), width=1)

    # Logo — load if available, else draw text fallback
    logo_y = 80
    logo_h = 160
    logo_placed = False
    if os.path.exists(LOGO_PATH):
        try:
            logo_img = Image.open(LOGO_PATH).convert("RGBA")
            # Scale to fit within (PAGE_W - 2*margin) x logo_h preserving aspect
            max_logo_w = PAGE_W - 2 * PAGE_MARGIN
            lw, lh = logo_img.size
            scale = min(max_logo_w / lw, logo_h / lh)
            new_lw, new_lh = int(lw * scale), int(lh * scale)
            logo_img = logo_img.resize((new_lw, new_lh), Image.LANCZOS)
            logo_x = (PAGE_W - new_lw) // 2
            # Paste on dark bg
            bg_patch = Image.new("RGB", (new_lw, new_lh), BG_TITLEPAGE)
            bg_patch.paste(logo_img, mask=logo_img.split()[3])
            img.paste(bg_patch, (logo_x, logo_y))
            logo_placed = True
            logo_bottom = logo_y + new_lh
        except Exception:
            logo_placed = False

    if not logo_placed:
        # Text fallback logo
        title_text = "LUMA"
        tw = text_width(draw, title_text, bold_xxl)
        draw.text(((PAGE_W - tw) // 2, logo_y), title_text, fill=ACCENT_AMBER, font=bold_xxl)
        sub_text = "& THE GLITCHKIN"
        sw = text_width(draw, sub_text, bold_lg)
        draw.text(((PAGE_W - sw) // 2, logo_y + 70), sub_text, fill=ACCENT_CYAN, font=bold_lg)
        logo_bottom = logo_y + 70 + 40

    # Divider line
    div_y = logo_bottom + 30
    draw_rule(draw, div_y, PAGE_MARGIN, PAGE_W - PAGE_MARGIN, color=ACCENT_AMBER, width=2)

    # Episode info block
    ep_y = div_y + 22
    ep_title = "EPISODE 01 — COLD OPEN"
    ep_tw = text_width(draw, ep_title, bold_md)
    draw.text(((PAGE_W - ep_tw) // 2, ep_y), ep_title, fill=TEXT_LIGHT, font=bold_md)

    sub_ep = "\u201cThe Night Everything Went Wrong\u201d"
    sub_ew = text_width(draw, sub_ep, reg_lg)
    draw.text(((PAGE_W - sub_ew) // 2, ep_y + 32), sub_ep, fill=ACCENT_AMBER, font=reg_lg)

    # Runtime / panel count
    runtime_y = ep_y + 80
    info_lines = [
        "26 Panels  \u2022  Est. Runtime: 68\u201374 seconds",
        "Storyboard Artist: Lee Tanaka  \u2022  Art Director: Alex Chen",
        "Development Draft \u2022 2026-03-29  \u2022  Grade: A\u2212 / 92%",
    ]
    for i, line in enumerate(info_lines):
        lw = text_width(draw, line, reg_sm)
        draw.text(((PAGE_W - lw) // 2, runtime_y + i * 20), line,
                  fill=TEXT_MID if i > 0 else TEXT_LIGHT, font=reg_sm)

    # Contact sheet thumbnail
    contact_y = runtime_y + 80
    if os.path.exists(CONTACT_PATH):
        try:
            cs = Image.open(CONTACT_PATH).convert("RGB")
            thumb_w = PAGE_W - 2 * PAGE_MARGIN
            thumb_h = int(cs.height * thumb_w / cs.width)
            # Cap height so it fits on page
            max_thumb_h = page_h - contact_y - 80
            if thumb_h > max_thumb_h:
                thumb_h = max_thumb_h
                thumb_w = int(cs.width * thumb_h / cs.height)
            cs_thumb = cs.resize((thumb_w, thumb_h), Image.LANCZOS)
            cx = (PAGE_W - thumb_w) // 2
            img.paste(cs_thumb, (cx, contact_y))
            # Thin cyan border
            draw.rectangle([cx - 1, contact_y - 1, cx + thumb_w + 1, contact_y + thumb_h + 1],
                           outline=ACCENT_CYAN, width=1)
            cs_label = "CONTACT SHEET — Full 26-panel cold open arc"
            cl_w = text_width(draw, cs_label, reg_sm)
            draw.text(((PAGE_W - cl_w) // 2, contact_y + thumb_h + 6),
                      cs_label, fill=ACCENT_CYAN, font=reg_sm)
        except Exception:
            draw.text((PAGE_MARGIN, contact_y), "[Contact sheet unavailable]",
                      fill=TEXT_MID, font=reg_sm)
    else:
        draw.text((PAGE_MARGIN, contact_y), "[Contact sheet not found]",
                  fill=TEXT_MID, font=reg_sm)

    # Footer
    footer_y = page_h - 36
    draw_rule(draw, footer_y - 8, PAGE_MARGIN, PAGE_W - PAGE_MARGIN,
              color=(45, 35, 22), width=1)
    footer_text = "CONFIDENTIAL — DEVELOPMENT DRAFT — NOT FOR DISTRIBUTION"
    ftw = text_width(draw, footer_text, reg_sm)
    draw.text(((PAGE_W - ftw) // 2, footer_y), footer_text,
              fill=(70, 55, 38), font=reg_sm)

    return img


# ── Body pages (panels in grid) ────────────────────────────────────────────────
def make_panel_grid_page(panel_indices, page_num, total_pages, fonts, title_label=""):
    """Render a page with THUMB_COLS columns of panel thumbnails."""
    reg_sm, reg_md, reg_lg, bold_sm, bold_md, bold_lg, bold_xl, bold_xxl = fonts

    thumb_w = (PAGE_W - 2 * PAGE_MARGIN - PANEL_GAP * (THUMB_COLS - 1)) // THUMB_COLS
    thumb_h = int(thumb_w * 270 / 480)   # preserve 480x270 aspect

    rows = math.ceil(len(panel_indices) / THUMB_COLS)
    header_h = 70
    footer_h = 36
    page_h = header_h + rows * (thumb_h + CAPTION_H + PANEL_GAP) + PAGE_MARGIN + footer_h

    img = Image.new("RGB", (PAGE_W, page_h), BG_PAGE)
    draw = ImageDraw.Draw(img)

    # Header
    header_text = title_label or f"COLD OPEN — Panel Sequence (Page {page_num} of {total_pages})"
    draw.text((PAGE_MARGIN, 22), header_text, fill=TEXT_DARK, font=bold_md)
    draw_rule(draw, 54, PAGE_MARGIN, PAGE_W - PAGE_MARGIN, color=DIVIDER_COL, width=1)

    # Panel thumbnails
    for i, meta_idx in enumerate(panel_indices):
        col = i % THUMB_COLS
        row = i // THUMB_COLS
        x0 = PAGE_MARGIN + col * (thumb_w + PANEL_GAP)
        y0 = header_h + row * (thumb_h + CAPTION_H + PANEL_GAP)

        panel_num, filename, shot_type, timing, description = PANEL_META[meta_idx]
        panel_path = os.path.join(PANELS_DIR, filename)

        # Load and resize panel image
        if os.path.exists(panel_path):
            try:
                pimg = Image.open(panel_path).convert("RGB")
                pthumb = pimg.resize((thumb_w, thumb_h), Image.LANCZOS)
                img.paste(pthumb, (x0, y0))
            except Exception:
                # Placeholder on error
                draw.rectangle([x0, y0, x0 + thumb_w, y0 + thumb_h],
                               fill=(200, 195, 188), outline=DIVIDER_COL, width=1)
                draw.text((x0 + 4, y0 + thumb_h // 2 - 8), "Panel not found",
                          fill=TEXT_MID, font=reg_sm)
        else:
            draw.rectangle([x0, y0, x0 + thumb_w, y0 + thumb_h],
                           fill=(200, 195, 188), outline=DIVIDER_COL, width=1)
            draw.text((x0 + 4, y0 + thumb_h // 2 - 8), f"P{panel_num}: not found",
                      fill=TEXT_MID, font=reg_sm)

        # Panel border
        draw.rectangle([x0, y0, x0 + thumb_w - 1, y0 + thumb_h - 1],
                       outline=TEXT_DARK, width=1)

        # Caption area below thumbnail
        cap_y = y0 + thumb_h + 4
        # Panel number + shot type
        header_cap = f"P{panel_num}  {shot_type}  [{timing}]"
        draw.text((x0, cap_y), header_cap, fill=TEXT_DARK, font=bold_sm)
        # Description (wrap to thumb_w)
        desc_y = cap_y + 16
        # Simple word-wrap
        words = description.split()
        line = ""
        line_y = desc_y
        for word in words:
            test = (line + " " + word).strip()
            if text_width(draw, test, reg_sm) <= thumb_w:
                line = test
            else:
                if line:
                    draw.text((x0, line_y), line, fill=TEXT_MID, font=reg_sm)
                    line_y += 14
                line = word
        if line:
            draw.text((x0, line_y), line, fill=TEXT_MID, font=reg_sm)

    # Footer
    footer_y = page_h - footer_h
    draw_rule(draw, footer_y, PAGE_MARGIN, PAGE_W - PAGE_MARGIN, color=DIVIDER_COL, width=1)
    footer_text = f"Luma & the Glitchkin — Cold Open Storyboard — Development Draft 2026-03-29   |   pg {page_num}"
    ftw = text_width(draw, footer_text, reg_sm)
    draw.text(((PAGE_W - ftw) // 2, footer_y + 8), footer_text, fill=TEXT_MID, font=reg_sm)

    return img


# ── Page 6: Hero spread (P23 + P24 large, side by side) ───────────────────────
def make_hero_spread(fonts):
    reg_sm, reg_md, reg_lg, bold_sm, bold_md, bold_lg, bold_xl, bold_xxl = fonts
    header_h  = 80
    hero_h    = 420  # tall hero panel area
    cap_h     = 80
    footer_h  = 50
    page_h    = header_h + hero_h + cap_h + footer_h

    img = Image.new("RGB", (PAGE_W, page_h), BG_PAGE)
    draw = ImageDraw.Draw(img)

    # Header
    title = "PROMISE SHOT + HOOK FRAME — The Close"
    draw.text((PAGE_MARGIN, 20), title, fill=TEXT_DARK, font=bold_lg)
    subtitle = "P23 (Promise Shot) and P24 (Hook Frame / Dutch Tilt Chaos Apex) — hold 2.5s + 1.5s"
    draw.text((PAGE_MARGIN, 54), subtitle, fill=TEXT_MID, font=reg_sm)
    draw_rule(draw, 72, PAGE_MARGIN, PAGE_W - PAGE_MARGIN, color=DIVIDER_COL, width=1)

    # Two panels side by side, full width
    usable_w = PAGE_W - 2 * PAGE_MARGIN - PANEL_GAP
    panel_w  = usable_w // 2
    panel_h  = hero_h

    hero_panels = [
        # (meta_index, accent_color, label)
        (22, ACCENT_CYAN,  "P23 — THE PROMISE SHOT\nBacks to camera — together vs chaos"),
        (23, ACCENT_AMBER, "P24 — THE HOOK FRAME\nDutch tilt — still point in the storm"),
    ]

    for i, (meta_idx, accent, label) in enumerate(hero_panels):
        x0 = PAGE_MARGIN + i * (panel_w + PANEL_GAP)
        y0 = header_h

        panel_num, filename, shot_type, timing, description = PANEL_META[meta_idx]
        panel_path = os.path.join(PANELS_DIR, filename)

        if os.path.exists(panel_path):
            try:
                pimg = Image.open(panel_path).convert("RGB")
                # Fit within panel_w x panel_h preserving aspect
                orig_w, orig_h = pimg.size
                scale = min(panel_w / orig_w, panel_h / orig_h)
                new_w = int(orig_w * scale)
                new_h = int(orig_h * scale)
                pimg = pimg.resize((new_w, new_h), Image.LANCZOS)
                # Center within slot
                px = x0 + (panel_w - new_w) // 2
                py = y0 + (panel_h - new_h) // 2
                img.paste(pimg, (px, py))
                # Accent border
                draw.rectangle([px - 2, py - 2, px + new_w + 2, py + new_h + 2],
                               outline=accent, width=3)
            except Exception:
                draw.rectangle([x0, y0, x0 + panel_w, y0 + panel_h],
                               fill=(200, 195, 188), outline=accent, width=2)
        else:
            draw.rectangle([x0, y0, x0 + panel_w, y0 + panel_h],
                           fill=(200, 195, 188), outline=accent, width=2)
            draw.text((x0 + 8, y0 + panel_h // 2), "Panel not found", fill=TEXT_MID, font=reg_sm)

        # Caption
        cap_y = y0 + panel_h + 8
        lines = label.split("\n")
        draw.text((x0, cap_y), lines[0], fill=TEXT_DARK, font=bold_sm)
        if len(lines) > 1:
            draw.text((x0, cap_y + 16), lines[1], fill=TEXT_MID, font=reg_sm)
        timing_str = f"{shot_type}  \u2022  {timing}"
        draw.text((x0, cap_y + 30), timing_str, fill=accent, font=reg_sm)

    # Footer
    footer_y = page_h - footer_h
    draw_rule(draw, footer_y, PAGE_MARGIN, PAGE_W - PAGE_MARGIN, color=DIVIDER_COL, width=1)
    footer_text = "Luma & the Glitchkin — Cold Open Storyboard — Development Draft 2026-03-29   |   pg 6 of 6"
    ftw = text_width(draw, footer_text, reg_sm)
    draw.text(((PAGE_W - ftw) // 2, footer_y + 10), footer_text, fill=TEXT_MID, font=reg_sm)

    return img


# ── Assembly ───────────────────────────────────────────────────────────────────
def assemble_composite(pages):
    """Stack all pages vertically into one tall composite PNG."""
    total_h = sum(p.height for p in pages)
    # Add a thin separator stripe between pages
    SEP_H = 6
    total_h += SEP_H * (len(pages) - 1)

    composite = Image.new("RGB", (PAGE_W, total_h), (140, 130, 115))
    y_cursor = 0
    for i, page in enumerate(pages):
        composite.paste(page, (0, y_cursor))
        y_cursor += page.height
        if i < len(pages) - 1:
            # Page separator stripe
            sep_draw = ImageDraw.Draw(composite)
            sep_draw.rectangle([0, y_cursor, PAGE_W, y_cursor + SEP_H - 1],
                               fill=(100, 90, 75))
            y_cursor += SEP_H

    return composite


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Storyboard Pitch Export Generator — Cycle 11")
    print("Generating pitch-format layout...")
    print("=" * 60)

    fonts = load_fonts()
    pages = []

    # Page 1: Title page
    print("  Building page 1 — title page...")
    pages.append(make_title_page(fonts))

    # Pages 2-5: Panel grids
    page_labels = [
        "COLD OPEN — Setup & Introduction (P01–P07)",
        "COLD OPEN — First Contact & Chaos Begins (P08–P14)",
        "COLD OPEN — Quiet Beat & Escalation (P15–P21)",
        "COLD OPEN — Bridge, Promise, Hook & Title (P22–P25)",
    ]
    total_body_pages = len(PAGE_GROUPS)
    total_pages = 1 + total_body_pages + 1  # title + body + hero spread
    for pg_i, indices in enumerate(PAGE_GROUPS):
        page_num = pg_i + 2
        print(f"  Building page {page_num} — {len(indices)} panels...")
        pages.append(make_panel_grid_page(
            indices,
            page_num=page_num,
            total_pages=total_pages,
            fonts=fonts,
            title_label=page_labels[pg_i],
        ))

    # Page 6: Hero spread
    print(f"  Building page {total_pages} — hero spread (P23 + P24)...")
    pages.append(make_hero_spread(fonts))

    # Assemble composite
    print("  Assembling composite PNG...")
    composite = assemble_composite(pages)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    composite.save(OUTPUT_PATH, "PNG", optimize=True)
    print(f"\n  Saved: {OUTPUT_PATH}")
    print(f"  Composite size: {composite.width} x {composite.height} px  ({len(pages)} pages)")
    print("\nDone.")


if __name__ == "__main__":
    main()
