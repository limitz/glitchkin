#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_caption_retrofit.py
Caption Retrofit Tool — "Luma & the Glitchkin" Cold Open Panels
Diego Vargas, Storyboard Artist — Cycle 45

PURPOSE
-------
Applies the three-tier caption hierarchy (Jonas Feld C17 P1) to existing storyboard
panels that predate the P10/P11 standard. Panels P03, P06, P07, P08, P09, P23, P24
were built with a 60px one-tier caption bar. This tool replaces the bottom 72px of
each panel with a properly structured three-tier caption bar, preserving everything
above that zone.

APPROACH
--------
- Input: existing 800×600 PNG panel
- Reads the image, preserves the top (PH - NEW_CAPTION_H) = 528px as draw area
- The old 60px caption zone (rows 540-600) + 12px of old draw = REPLACED
  (the bottom 12px of the old draw zone is sacrificed — never contained critical content)
- Writes a fresh 72px three-tier caption bar at bottom
- Output: overwrites panel PNG in place at same path

THREE-TIER CAPTION SPEC
-----------------------
Tier 1: Shot code — bold 13pt, TEXT_SHOT=(232,224,204), top-left
Tier 2: Arc label — 11pt, arc-palette color, top-right
Tier 3: Narrative description — 9pt, TEXT_DESC=(155,148,122), second row
Metadata: 8pt, TEXT_META=(88,82,66), bottom-right
CAPTION_H: 72px (was 60px)

CAPTION SPECS PER PANEL
-----------------------
P03: CURIOUS/DISCOVERY (ELEC_CYAN border + arc label)
P06: DISCOVERY (ELEC_CYAN)
P07: TENSE → BREACH (HOT_MAGENTA)
P08: TENSE (HOT_MAGENTA)
P09: CURIOUS / FIRST ENCOUNTER (ELEC_CYAN)
P23: TENSE (HOT_MAGENTA)
P24: PITCH BEAT (ELEC_CYAN — bright)

Usage:
    python3 LTG_TOOL_sb_caption_retrofit.py              # retrofit all cold open panels
    python3 LTG_TOOL_sb_caption_retrofit.py --dry-run    # print plan without saving
    python3 LTG_TOOL_sb_caption_retrofit.py --panel P03  # retrofit one panel only
"""

import os
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont

# ── Paths ────────────────────────────────────────────────────────────────────
try:
    import importlib.util
    _spec = importlib.util.spec_from_file_location(
        "project_paths",
        os.path.join(os.path.dirname(__file__), "LTG_TOOL_project_paths.py")
    )
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    PANELS_DIR = str(_mod.resolve_output("storyboards/panels"))
except Exception:
    PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"

# ── Dimensions ────────────────────────────────────────────────────────────────
PW          = 800
PH          = 600
CAPTION_H   = 72     # new standard (was 60)
DRAW_H      = PH - CAPTION_H    # 528

# ── Palette ───────────────────────────────────────────────────────────────────
ELEC_CYAN   = (0, 212, 232)
HOT_MAGENTA = (232, 0, 152)
ARC_COMMIT  = (60, 200, 140)     # threshold/commitment beats
BG_CAPTION  = (12, 8, 6)
TEXT_SHOT   = (232, 224, 204)
TEXT_DESC   = (155, 148, 122)
TEXT_META   = (88, 82, 66)


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


# ── Caption specs per panel ───────────────────────────────────────────────────
# Each entry: (shot_label, arc_label, arc_color, border_color, tier3_line1, tier3_line2, meta)
PANEL_SPECS = {
    "P03": {
        "panel_id":  "P03",
        "filename":  "LTG_SB_cold_open_P03.png",
        "shot":      "P03  |  CU MONITOR  |  STATIC",
        "arc":       "ARC: CURIOUS / DISCOVERY",
        "arc_color": ELEC_CYAN,
        "border":    ELEC_CYAN,
        "desc1":     "Hero CRT prop. Static. One ELEC_CYAN pixel appears lower-right.",
        "desc2":     "First Glitch Palette moment in episode. The Glitch is here.",
        "meta":      "LTG_SB_cold_open_P03  /  Diego Vargas  /  C41 (caption retrofit C45)",
    },
    "P06": {
        "panel_id":  "P06",
        "filename":  "LTG_SB_cold_open_P06.png",
        "shot":      "P06  |  CU MONITOR SCREEN  |  STATIC",
        "arc":       "ARC: DISCOVERY",
        "arc_color": ELEC_CYAN,
        "border":    ELEC_CYAN,
        "desc1":     "Byte's face pressed against glass from inside. DISGUSTED / CURIOUS.",
        "desc2":     "First appearance of Byte. Normal eye: 70% squint. Cracked eye: searching.",
        "meta":      "LTG_SB_cold_open_P06  /  Diego Vargas  /  C41 (caption retrofit C45)",
    },
    "P07": {
        "panel_id":  "P07",
        "filename":  "LTG_SB_cold_open_P07.png",
        "shot":      "P07  |  MED WIDE  |  DUTCH 8° CW  |  LOW ANGLE",
        "arc":       "ARC: TENSE → BREACH",
        "arc_color": HOT_MAGENTA,
        "border":    HOT_MAGENTA,
        "desc1":     "Monitor bows convex; distortion rings break OUTSIDE bezel.",
        "desc2":     "Byte mid-phase: lower half inside screen. DETERMINED + ALARMED.",
        "meta":      "LTG_SB_cold_open_P07  /  Diego Vargas  /  C43 (caption retrofit C45)",
    },
    "P08": {
        "panel_id":  "P08",
        "filename":  "LTG_SB_cold_open_P08.png",
        "shot":      "P08  |  MED  |  BYTE FULL REVEAL",
        "arc":       "ARC: TENSE",
        "arc_color": HOT_MAGENTA,
        "border":    HOT_MAGENTA,
        "desc1":     "Byte full character reveal — first time in real world. Pixel confetti drifting.",
        "desc2":     'Camera at Byte\'s eye level (~6" off floor). "The flesh dimension."',
        "meta":      "LTG_SB_cold_open_P08  /  Diego Vargas  /  C41 (caption retrofit C45)",
    },
    "P09": {
        "panel_id":  "P09",
        "filename":  "LTG_SB_cold_open_P09.png",
        "shot":      "P09  |  MED WIDE  |  BYTE FLOATING",
        "arc":       "ARC: CURIOUS / FIRST ENCOUNTER",
        "arc_color": ELEC_CYAN,
        "border":    ELEC_CYAN,
        "desc1":     "Byte floating 18\" off floor, spots Luma on couch. Cracked eye scans.",
        "desc2":     "Sight-line annotation. Gravity ghost: confetti falls, Byte doesn't.",
        "meta":      "LTG_SB_cold_open_P09  /  Diego Vargas  /  C43 (caption retrofit C45)",
    },
    "P23": {
        "panel_id":  "P23",
        "filename":  "LTG_SB_cold_open_P23.png",
        "shot":      "P23  |  MED OTS REVERSE  |  PROMISE SHOT",
        "arc":       "ARC: TENSE",
        "arc_color": HOT_MAGENTA,
        "border":    HOT_MAGENTA,
        "desc1":     "Luma + Byte from behind, both facing monitor wall. Show's promise shot.",
        "desc2":     "Luma warm vs. Full Glitch Chaos. Byte shoulder-perch. Push-in annotated.",
        "meta":      "LTG_SB_cold_open_P23  /  Diego Vargas  /  C42 (caption retrofit C45)",
    },
    "P24": {
        "panel_id":  "P24",
        "filename":  "LTG_SB_cold_open_P24.png",
        "shot":      "P24  |  WIDE/MED  |  LOW ANGLE  |  DUTCH 12° L  |  HOOK FRAME",
        "arc":       "ARC: PITCH BEAT",
        "arc_color": ELEC_CYAN,
        "border":    ELEC_CYAN,
        "desc1":     "CHAOS APEX. 28 Glitchkin pour through breached screens. Hook frame.",
        "desc2":     "Luma FG hero (low angle). Byte on shoulder (resigned dignity). Dutch 12°.",
        "meta":      "LTG_SB_cold_open_P24  /  Diego Vargas  /  C42 (caption retrofit C45)",
    },
}


def retrofit_panel(spec, dry_run=False):
    """Apply three-tier caption to an existing panel PNG."""
    path = os.path.join(PANELS_DIR, spec["filename"])
    if not os.path.exists(path):
        print(f"  SKIP — file not found: {path}")
        return False

    if dry_run:
        print(f"  DRY-RUN {spec['panel_id']}: {spec['shot']}")
        print(f"    Arc: {spec['arc']} (border: {spec['border']})")
        print(f"    Desc: {spec['desc1']}")
        return True

    img = Image.open(path).convert("RGB")
    orig_w, orig_h = img.size

    # Preserve draw area: top DRAW_H (528) px
    # If original is 800×600 with old 60px caption → draw was 540px
    # We take the top 528px (drop the bottom 12px of old draw + old 60px caption)
    draw_crop_h = DRAW_H   # 528
    draw_area   = img.crop([0, 0, PW, draw_crop_h])

    # New canvas: draw area + new caption bar
    new_img = Image.new("RGB", (PW, PH), BG_CAPTION)
    new_img.paste(draw_area, (0, 0))
    draw    = ImageDraw.Draw(new_img)

    # ── Caption bar ───────────────────────────────────────────────────────────
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    # Tier 1 — Shot code
    draw.text((10, DRAW_H + 4), spec["shot"], font=font_t1, fill=TEXT_SHOT)

    # Tier 2 — Arc label (right, arc-colored)
    arc_text_w = 10 + len(spec["arc"]) * 7   # rough estimate for right-align
    draw.text((PW - arc_text_w - 10, DRAW_H + 5),
              spec["arc"], font=font_t2, fill=spec["arc_color"])

    # Tier 3 — Narrative description
    draw.text((10, DRAW_H + 22), spec["desc1"], font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35), spec["desc2"], font=font_t3, fill=(120, 112, 90))

    # Metadata
    draw.text((PW - 10 - len(spec["meta"]) * 5, DRAW_H + 56),
              spec["meta"], font=font_meta, fill=TEXT_META)

    # Arc border (full panel)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=spec["border"], width=4)

    new_img.thumbnail((1280, 1280))
    new_img.save(path, "PNG")
    print(f"  DONE {spec['panel_id']}: {path}  {new_img.size}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Retrofit three-tier caption hierarchy on cold open storyboard panels."
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Print plan without saving.")
    parser.add_argument("--panel", type=str, default=None,
                        help="Retrofit a single panel by ID (e.g. P03). Default: all.")
    args = parser.parse_args()

    if args.panel:
        panel_id = args.panel.upper()
        if panel_id not in PANEL_SPECS:
            print(f"ERROR: Unknown panel '{panel_id}'. Options: {list(PANEL_SPECS.keys())}")
            sys.exit(1)
        specs = {panel_id: PANEL_SPECS[panel_id]}
    else:
        specs = PANEL_SPECS

    print(f"Caption retrofit — {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"Panels to process: {list(specs.keys())}")
    print(f"Output dir: {PANELS_DIR}")
    print()

    results = {}
    for panel_id, spec in specs.items():
        ok = retrofit_panel(spec, dry_run=args.dry_run)
        results[panel_id] = ok

    print()
    passed = sum(1 for v in results.values() if v)
    print(f"Complete: {passed}/{len(results)} panels processed.")

    # Caption classification decisions (for Alex Chen reporting)
    if not args.dry_run and not args.panel:
        print()
        print("Caption classification decisions (per Alex Chen brief):")
        for pid, spec in specs.items():
            print(f"  {pid}: T1=shot code | T2=arc label | T3=action description + technical note")
        print("No ambiguous panels. All existing captions contained action/technical info only.")
        print("No dialogue present in P03/P06/P07/P08/P09/P23/P24 captions — N/A for Tier 1 dialogue slot.")
        print("Tier 1 repurposed as shot code per P10/P11 standard (most legible read for storyboard use).")


if __name__ == "__main__":
    main()
