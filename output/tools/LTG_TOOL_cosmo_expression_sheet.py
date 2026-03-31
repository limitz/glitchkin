#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_cosmo_expression_sheet.py
Cosmo Expression Sheet Generator — "Luma & the Glitchkin"

v010 — C54 thin wrapper around LTG_TOOL_char_cosmo.py (canonical renderer)

  All character drawing logic now lives in LTG_TOOL_char_cosmo.py.
  This file handles ONLY sheet layout, labels, color enhancement compositing,
  and per-expression metadata (panel backgrounds, beat tags, state transitions).

  6 expressions: AWKWARD, WORRIED, SURPRISED, SKEPTICAL, DETERMINED, FRUSTRATED

Output: output/characters/main/LTG_CHAR_cosmo_expression_sheet.png
Authors: Maya Santos (v001-v008) / Sam Kowalski (v009 pycairo) / Maya Santos (v010 thin wrapper)
Date: 2026-03-31
"""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# ── Tool imports ─────────────────────────────────────────────────────────────
_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from LTG_TOOL_char_cosmo import (
    draw_cosmo, render_cosmo_pil, VALID_EXPRESSIONS,
    SKIN, SKIN_SH, SKIN_HL, BLUSH, PANTS, PANTS_SH,
)
from LTG_TOOL_cairo_primitives import to_pil_image, to_pil_rgba

try:
    from LTG_TOOL_character_color_enhance import (
        apply_scene_tint, apply_skin_warmth, apply_form_shadow,
        apply_hair_absorption, SCENE_PRESETS,
    )
    _ENHANCE_AVAILABLE = True
except ImportError:
    _ENHANCE_AVAILABLE = False

# ── Palette (sheet-level only, not character colors) ─────────────────────────
STRIPE_A     = (91, 141, 184)    # Cerulean stripe (for form shadow)
CANVAS_BG    = (28, 24, 20)

# Panel backgrounds
BG_NEUTRAL   = (240, 220, 180)
BG_FRUSTRAT  = (235, 215, 175)
BG_DETERMIN  = (225, 235, 220)
BG_SKEPTIC   = (230, 218, 178)
BG_WORRIED   = (225, 212, 172)
BG_SURPRISED = (242, 222, 175)
BG_AWKWARD   = (238, 220, 185)

# ── Layout ────────────────────────────────────────────────────────────────────
PANEL_W = 370
PANEL_H = 440
LABEL_H = 64
COLS    = 3
ROWS    = 2
PAD     = 18
HEADER  = 52

# ── Expression metadata (sheet-specific: backgrounds, labels, notebook state) ─
EXPRESSION_META = [
    {
        "name": "AWKWARD",
        "panel_bg": BG_AWKWARD,
        "notebook_show": False, "notebook_open": False,
        "prev_state": "\u2190 was: ANY ATTEMPT TO HELP",
        "next_state": "\u2192 next: WORRIED / RETREATING",
    },
    {
        "name": "WORRIED",
        "panel_bg": BG_WORRIED,
        "notebook_show": False, "notebook_open": False,
        "prev_state": "\u2190 was: NEUTRAL / SKEPTICAL",
        "next_state": "\u2192 next: FRUSTRATED / TRYING ANYWAY",
    },
    {
        "name": "SURPRISED",
        "panel_bg": BG_SURPRISED,
        "notebook_show": True, "notebook_open": True,
        "prev_state": "\u2190 was: DETERMINED (plan in action)",
        "next_state": "\u2192 next: FRUSTRATED / ACCEPTING CHAOS",
    },
    {
        "name": "SKEPTICAL",
        "panel_bg": BG_SKEPTIC,
        "notebook_show": True, "notebook_open": False,
        "prev_state": "\u2190 was: NEUTRAL / OBSERVING",
        "next_state": "\u2192 next: RESIGNED / PREPARING ANYWAY",
    },
    {
        "name": "DETERMINED",
        "panel_bg": BG_DETERMIN,
        "notebook_show": True, "notebook_open": False,
        "prev_state": "\u2190 was: NEUTRAL / OBSERVING",
        "next_state": "\u2192 next: FRUSTRATED or SUCCEEDED",
    },
    {
        "name": "FRUSTRATED / DEFEATED",
        "expr_key": "FRUSTRATED",
        "panel_bg": BG_FRUSTRAT,
        "notebook_show": True, "notebook_open": True,
        "prev_state": "\u2190 was: DETERMINED",
        "next_state": "\u2192 next: RESIGNED / RECALIBRATING",
    },
]

BEAT_TAGS = {
    "AWKWARD":                "A1-03 / A2-02",
    "WORRIED":                "A2-02",
    "SURPRISED":              "A2-04c",
    "SKEPTICAL":              "A2-03",
    "DETERMINED":             "A2-05b",
    "FRUSTRATED / DEFEATED":  "A2-06",
}


def generate_cosmo_expression_sheet(output_path):
    """Generate the Cosmo expression sheet using the canonical char_cosmo renderer."""
    total_w = COLS * (PANEL_W + PAD) + PAD
    total_h = HEADER + ROWS * (PANEL_H + LABEL_H + PAD) + PAD

    img = Image.new('RGB', (total_w, total_h), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        font_sm = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font_title = font = font_sm = ImageFont.load_default()

    draw.text((PAD, 14),
              "COSMO \u2014 Expression Sheet \u2014 Luma & the Glitchkin  |  v010  |  C54: canonical char_cosmo",
              fill=(91, 141, 184), font=font_title)

    scene_preset = "neutral_daylight"

    for i, meta in enumerate(EXPRESSION_META):
        col = i % COLS
        row = i // COLS
        ppx = PAD + col * (PANEL_W + PAD)
        ppy = HEADER + row * (PANEL_H + LABEL_H + PAD)

        expr_key = meta.get("expr_key", meta["name"])
        panel_bg = meta["panel_bg"]

        # Panel background
        draw.rectangle([ppx, ppy, ppx + PANEL_W, ppy + PANEL_H], fill=panel_bg)
        draw.rectangle([ppx, ppy, ppx + PANEL_W, ppy + PANEL_H], outline=(80, 74, 70), width=1)

        # Render character via canonical module
        surface, geom = draw_cosmo(
            expression=expr_key,
            scale=1.0,
            enhance_color=False,
            notebook_show=meta["notebook_show"],
            notebook_open=meta["notebook_open"],
        )

        # Convert to PIL RGBA and crop to content
        char_img = to_pil_rgba(surface)
        bbox = char_img.getbbox()
        if bbox:
            char_img = char_img.crop(bbox)

        # Fit character into panel (leave room for labels)
        avail_w = PANEL_W - 12
        avail_h = PANEL_H - 10
        char_img.thumbnail((avail_w, avail_h), Image.LANCZOS)

        # Center in panel
        cx = ppx + (PANEL_W - char_img.width) // 2
        cy = ppy + (PANEL_H - char_img.height) // 2
        img.paste(char_img, (cx, cy), char_img)
        draw = ImageDraw.Draw(img)  # refresh after paste

        # Color enhancement on the panel region
        if _ENHANCE_AVAILABLE:
            # Extract the panel region for enhancement
            panel_region = img.crop((ppx, ppy, ppx + PANEL_W, ppy + PANEL_H))

            # Remap geom coords to panel-local
            offset_x = cx - ppx
            offset_y = cy - ppy
            surf_w, surf_h = geom["surface_size"]
            crop_x = bbox[0] if bbox else 0
            crop_y = bbox[1] if bbox else 0

            face_cx_local = geom["face_center"][0] - crop_x + offset_x
            face_cy_local = geom["face_center"][1] - crop_y + offset_y
            face_rx, face_ry = geom["face_radius"]

            char_bbox_local = (
                geom["char_bbox"][0] - crop_x + offset_x,
                geom["char_bbox"][1] - crop_y + offset_y,
                geom["char_bbox"][2] - crop_x + offset_x,
                geom["char_bbox"][3] - crop_y + offset_y,
            )

            panel_region = apply_scene_tint(
                panel_region, char_bbox_local,
                key_light_color=SCENE_PRESETS[scene_preset]["key_color"],
                alpha=SCENE_PRESETS[scene_preset]["tint_alpha"],
                light_dir=SCENE_PRESETS[scene_preset]["key_dir"],
            )

            panel_region = apply_skin_warmth(
                panel_region, (face_cx_local, face_cy_local), (face_rx, face_ry),
                light_dir=SCENE_PRESETS[scene_preset]["key_dir"],
                warm_color=SKIN_HL, blush_color=BLUSH,
                warm_alpha=20, cool_alpha=14, blush_alpha=16,
            )

            if geom.get("torso_bbox"):
                tb = geom["torso_bbox"]
                torso_local = (
                    tb[0] - crop_x + offset_x,
                    tb[1] - crop_y + offset_y,
                    tb[2] - crop_x + offset_x,
                    tb[3] - crop_y + offset_y,
                )
                panel_region = apply_form_shadow(
                    panel_region, torso_local,
                    base_color=STRIPE_A, shadow_color=(72, 112, 148),
                    shadow_shape="torso_diagonal",
                    light_dir=SCENE_PRESETS[scene_preset]["key_dir"],
                    alpha=70,
                )

            for leg_bbox in geom.get("leg_bboxes", []):
                lb = (
                    leg_bbox[0] - crop_x + offset_x,
                    leg_bbox[1] - crop_y + offset_y,
                    leg_bbox[2] - crop_x + offset_x,
                    leg_bbox[3] - crop_y + offset_y,
                )
                panel_region = apply_form_shadow(
                    panel_region, lb,
                    base_color=PANTS, shadow_color=PANTS_SH,
                    shadow_shape="limb_underside",
                    light_dir=SCENE_PRESETS[scene_preset]["key_dir"],
                    alpha=60,
                )

            if geom.get("hair_bbox"):
                hb = geom["hair_bbox"]
                hair_local = (
                    hb[0] - crop_x + offset_x,
                    hb[1] - crop_y + offset_y,
                    hb[2] - crop_x + offset_x,
                    hb[3] - crop_y + offset_y,
                )
                panel_region = apply_hair_absorption(
                    panel_region, hair_local,
                    scene_color=SCENE_PRESETS[scene_preset]["key_color"],
                    alpha=10,
                )

            img.paste(panel_region, (ppx, ppy))
            draw = ImageDraw.Draw(img)

        # Beat tag
        tag = BEAT_TAGS.get(meta["name"])
        if tag:
            draw.text((ppx + PANEL_W - 74, ppy + 6), tag, fill=(100, 160, 120), font=font_sm)

        # Label strip (BELOW panel)
        label_y = ppy + PANEL_H
        draw.rectangle([ppx, label_y, ppx + PANEL_W, label_y + LABEL_H],
                       fill=(18, 14, 12))
        draw.text((ppx + 6, label_y + 6),
                  meta["name"], fill=(91, 141, 184), font=font)
        draw.text((ppx + 6, label_y + 26),
                  meta["prev_state"], fill=(130, 118, 112), font=font_sm)
        draw.text((ppx + 6, label_y + 40),
                  meta["next_state"], fill=(130, 118, 112), font=font_sm)

    # Final size check
    w, h = img.size
    if w > 1280 or h > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(output_path)
    print(f"Saved: {output_path}  ({img.size[0]}x{img.size[1]}px)")
    print("v010 changes (C54 Maya Santos):")
    print("  Thin wrapper around canonical char_cosmo renderer")
    print(f"  Color enhancement: {_ENHANCE_AVAILABLE}")
    print(f"  Expressions: {', '.join(e['name'] for e in EXPRESSION_META)}")


if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    generate_cosmo_expression_sheet(
        os.path.join(out_dir, "LTG_CHAR_cosmo_expression_sheet.png")
    )
