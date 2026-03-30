# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_glitch_body_primitive_diagram_gen.py
Glitch Body Primitive Diagram — v001
"Luma & the Glitchkin" — Cycle 41 / Maya Santos

Generates output/characters/LTG_CHAR_glitch_body_primitive_diagram.png

Closes Alex Chen C41 P2: visual spec diagram for Glitch's diamond body primitive.
Addresses Daisuke Kobayashi C14 P8 / C16 P4 (4-cycle open item — verbal spec exists,
no diagram).

Layout: 2-column reference sheet
  Left panel:  Labeled anatomy diagram — proportions, vertices, construction notes
  Right panel: Expression silhouettes — NEUTRAL, MISCHIEVOUS, PANICKED, TRIUMPHANT
               showing tilt/squash/stretch range + Glitch vs Glitchkin visual distinction

Constants per glitch_body_diamond_spec.md:
  GLITCH_BODY_RX = 34px (1x scale)
  GLITCH_BODY_RY = 38px (1x scale)
  ry > rx — body TALLER than wide (never swap)
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

# ── Colors ─────────────────────────────────────────────────────────────────────
CORRUPT_AMBER    = (255, 140, 0)      # body fill
CORRUPT_AMBER_HL = (255, 185, 80)     # top-left highlight facet
CORRUPT_AMBER_SH = (168, 76, 0)       # shadow body (offset)
UV_PURPLE        = (123, 47, 190)     # UV shadow offset
HOT_MAG          = (255, 45, 107)     # crack scar + fork
VOID_BLACK       = (10, 10, 20)       # outline
ACID_GREEN       = (180, 255, 0)      # confetti (MISCHIEVOUS)
ELEC_CYAN        = (0, 240, 255)      # confetti (PANICKED/STUNNED)
SOFT_GOLD        = (255, 215, 80)     # confetti (TRIUMPHANT)
CANVAS_BG        = (22, 18, 32)       # dark background (Glitch Layer style)
LABEL_COLOR      = (200, 190, 210)    # label text
DIM_LABEL        = (130, 115, 150)    # secondary labels
MEASURE_LINE     = (80, 200, 255)     # measurement arrows
HIGHLIGHT_LINE   = (255, 240, 120)    # highlight annotations

# ── Layout ─────────────────────────────────────────────────────────────────────
TOTAL_W = 1280
TOTAL_H = 720
PANEL_W = (TOTAL_W - 60) // 2    # ~610px each
PAD     = 20
HEADER  = 48

# ── Font ───────────────────────────────────────────────────────────────────────
try:
    FONT_TITLE  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    FONT_HEAD   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
    FONT_LABEL  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    FONT_SMALL  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
except Exception:
    FONT_TITLE = FONT_HEAD = FONT_LABEL = FONT_SMALL = ImageFont.load_default()


# ── Geometry helpers ───────────────────────────────────────────────────────────
def diamond_pts(cx, cy, rx, ry, tilt_deg=0, squash=1.0, stretch=1.0):
    """Compute the 4 diamond vertex points per glitch_body_diamond_spec.md §2."""
    tilt  = math.radians(tilt_deg)
    ry_eff = int(ry * squash * stretch)
    top   = (cx + int(rx * 0.15 * math.sin(tilt)),
             cy - ry_eff + int(rx * 0.15 * math.cos(tilt)))
    right = (cx + int(rx * math.cos(-tilt)),
             cy + int(rx * 0.20 * math.sin(-tilt)))
    bot   = (cx - int(rx * 0.15 * math.sin(tilt)),
             cy + int(ry_eff * 1.15))
    left  = (cx - int(rx * math.cos(-tilt)),
             cy - int(rx * 0.20 * math.sin(-tilt)))
    return top, right, bot, left, ry_eff


def draw_diamond_body(draw, cx, cy, rx, ry, tilt_deg=0, squash=1.0, stretch=1.0,
                      spike_h=10, arm_l_dy=0, arm_r_dy=0):
    """Draw Glitch's full diamond body per spec §4–§8."""
    top, right, bot, left, ry_eff = diamond_pts(cx, cy, rx, ry, tilt_deg, squash, stretch)

    # 1. UV shadow (offset +3, +4)
    shadow_pts = [(p[0]+3, p[1]+4) for p in [top, right, bot, left]]
    draw.polygon(shadow_pts, fill=UV_PURPLE)

    # 2. Main body fill
    body_pts = [top, right, bot, left]
    draw.polygon(body_pts, fill=CORRUPT_AMBER)

    # 3. Highlight facet (top-left triangle)
    ctr     = (cx, cy - ry // 4)
    mid_tl  = ((top[0]+left[0])//2, (top[1]+left[1])//2)
    draw.polygon([top, ctr, mid_tl], fill=CORRUPT_AMBER_HL)

    # 4. Outline
    draw.polygon(body_pts, outline=VOID_BLACK, width=3)

    # 5. HOT_MAG crack + fork
    cs  = (cx - rx//2, cy - ry//3)
    ce  = (cx + rx//3, cy + ry//2)
    draw.line([cs, ce], fill=HOT_MAG, width=2)
    mid_c = ((cs[0]+ce[0])//2, (cs[1]+ce[1])//2)
    fork  = (cx + rx//2, cy - ry//4)
    draw.line([mid_c, fork], fill=HOT_MAG, width=1)

    # 6. Bottom spike (3-point)
    bot_spike_tip = (bot[0], bot[1] + spike_h)
    bot_spike_pts = [(bot[0] - rx//5, bot[1]),
                     bot_spike_tip,
                     (bot[0] + rx//5, bot[1])]
    draw.polygon(bot_spike_pts, fill=CORRUPT_AMBER, outline=VOID_BLACK, width=2)

    # 7. Arm spikes (from LEFT and RIGHT vertices)
    arm_spike_len = int(rx * 0.65)
    arm_spike_w   = int(rx * 0.22)
    # Left arm-spike
    lax = left[0] - arm_spike_len
    lay = left[1] + arm_l_dy
    draw.polygon([(left[0], left[1] - arm_spike_w),
                  (lax, lay),
                  (left[0], left[1] + arm_spike_w)],
                 fill=CORRUPT_AMBER, outline=VOID_BLACK, width=2)
    # Right arm-spike
    rax = right[0] + arm_spike_len
    ray = right[1] + arm_r_dy
    draw.polygon([(right[0], right[1] - arm_spike_w),
                  (rax, ray),
                  (right[0], right[1] + arm_spike_w)],
                 fill=CORRUPT_AMBER, outline=VOID_BLACK, width=2)

    # 8. Top spike crown (5 points)
    # Simplified 3-pt spike for diagram clarity
    top_spike_pts = [(top[0] - rx//6, top[1]),
                     (top[0], top[1] - spike_h),
                     (top[0] + rx//6, top[1])]
    draw.polygon(top_spike_pts, fill=CORRUPT_AMBER, outline=VOID_BLACK, width=2)

    return top, right, bot, left, ry_eff


def arrow_h(draw, x1, y, x2, color, font, label, above=True):
    """Draw horizontal measurement arrow."""
    draw.line([(x1, y), (x2, y)], fill=color, width=1)
    draw.line([(x1, y-4), (x1, y+4)], fill=color, width=1)
    draw.line([(x2, y-4), (x2, y+4)], fill=color, width=1)
    mx = (x1 + x2) // 2
    ty = y - 14 if above else y + 4
    draw.text((mx, ty), label, fill=color, font=font, anchor="mm")


def arrow_v(draw, x, y1, y2, color, font, label, right_side=True):
    """Draw vertical measurement arrow."""
    draw.line([(x, y1), (x, y2)], fill=color, width=1)
    draw.line([(x-4, y1), (x+4, y1)], fill=color, width=1)
    draw.line([(x-4, y2), (x+4, y2)], fill=color, width=1)
    my = (y1 + y2) // 2
    tx = x + 8 if right_side else x - 8
    anchor = "lm" if right_side else "rm"
    draw.text((tx, my), label, fill=color, font=font, anchor=anchor)


# ── Panel 1: Anatomy Diagram ───────────────────────────────────────────────────
def draw_anatomy_panel(draw, px, py, pw, ph):
    """Left panel: labeled anatomy of the diamond body."""
    # Panel background
    draw.rectangle([px, py, px+pw, py+ph], fill=(28, 22, 40))
    draw.rectangle([px, py, px+pw, py+ph], outline=(60, 50, 80), width=1)

    draw.text((px + pw//2, py + 14), "ANATOMY — Diamond Body Primitive",
              fill=HIGHLIGHT_LINE, font=FONT_HEAD, anchor="mm")

    # Draw at 2x scale for diagram (rx=68, ry=76)
    SCALE = 2
    rx = 34 * SCALE   # 68
    ry = 38 * SCALE   # 76
    cx = px + pw // 2 - 20
    cy = py + ph // 2 + 10

    top, right, bot, left, ry_eff = draw_diamond_body(draw, cx, cy, rx, ry,
                                                       tilt_deg=0, spike_h=10*SCALE)

    # === Labels ===
    # Center dot
    draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=MEASURE_LINE)

    # Vertex labels
    draw.text((top[0], top[1] - 22), "TOP VERTEX",
              fill=LABEL_COLOR, font=FONT_SMALL, anchor="mm")
    draw.text((bot[0], bot[1] + 28), "BOT VERTEX",
              fill=LABEL_COLOR, font=FONT_SMALL, anchor="mm")
    draw.text((left[0] - 52, left[1]), "LEFT",
              fill=LABEL_COLOR, font=FONT_SMALL, anchor="rm")
    draw.text((right[0] + 8, right[1]), "RIGHT",
              fill=LABEL_COLOR, font=FONT_SMALL, anchor="lm")

    # rx measurement
    arrow_h(draw, cx, cy + 8, right[0], MEASURE_LINE, FONT_SMALL,
            "rx=34px (1x)\nrx=68px (2x)", above=False)
    draw.text((cx + (right[0]-cx)//2, cy + 22), "rx=34px (1x) / 68px (2x)",
              fill=MEASURE_LINE, font=FONT_SMALL, anchor="mm")

    # ry measurement (from cy to top)
    arrow_v(draw, cx - rx - 22, top[1] + (ry_eff - (top[1] - (cy - ry_eff))),
            cy, MEASURE_LINE, FONT_SMALL, "")
    # Simpler: just draw the arrow from top.y to cy
    x_arr = px + 36
    draw.line([(x_arr, top[1]), (x_arr, cy)], fill=MEASURE_LINE, width=1)
    draw.line([(x_arr-4, top[1]), (x_arr+4, top[1])], fill=MEASURE_LINE, width=1)
    draw.line([(x_arr-4, cy), (x_arr+4, cy)], fill=MEASURE_LINE, width=1)
    draw.text((x_arr - 6, (top[1]+cy)//2), "ry=38\n(1x)",
              fill=MEASURE_LINE, font=FONT_SMALL, anchor="rm")

    # Width annotation
    draw.line([(left[0], cy + ry + 28), (right[0], cy + ry + 28)], fill=MEASURE_LINE, width=1)
    draw.line([(left[0], cy+ry+22), (left[0], cy+ry+34)], fill=MEASURE_LINE, width=1)
    draw.line([(right[0], cy+ry+22), (right[0], cy+ry+34)], fill=MEASURE_LINE, width=1)
    draw.text(((left[0]+right[0])//2, cy+ry+38), "rx*2=68px (1x) / 136px (2x)",
              fill=MEASURE_LINE, font=FONT_SMALL, anchor="mm")

    # Proportional rule label
    rule_x = px + pw - 10
    rule_y = py + 42
    draw.text((rule_x, rule_y), "ry > rx — body TALLER than wide",
              fill=HIGHLIGHT_LINE, font=FONT_SMALL, anchor="rm")
    draw.text((rule_x, rule_y + 14), "NEVER swap rx/ry",
              fill=HOT_MAG, font=FONT_SMALL, anchor="rm")

    # Facet label
    facet_label_x = cx + rx // 2
    facet_label_y = cy - ry // 2
    draw.line([(facet_label_x, facet_label_y), (facet_label_x + 40, facet_label_y - 18)],
              fill=CORRUPT_AMBER_HL, width=1)
    draw.text((facet_label_x + 42, facet_label_y - 18), "AMBER_HL\nfacet",
              fill=CORRUPT_AMBER_HL, font=FONT_SMALL, anchor="lm")

    # Crack label
    crack_mid_x = cx
    crack_mid_y = cy + ry // 6
    draw.line([(crack_mid_x, crack_mid_y), (crack_mid_x - 42, crack_mid_y + 25)],
              fill=HOT_MAG, width=1)
    draw.text((crack_mid_x - 44, crack_mid_y + 25), "HOT_MAG\ncrack+fork",
              fill=HOT_MAG, font=FONT_SMALL, anchor="rm")

    # UV shadow label (top-right)
    draw.text((cx + rx + 12, cy - ry//2), "UV_PURPLE\nshadow (+3,+4)",
              fill=UV_PURPLE, font=FONT_SMALL, anchor="lm")

    # Arm-spike label
    arm_label_x = left[0] - 34 * SCALE
    draw.text((arm_label_x - 4, left[1] + 12), "arm-spike\n(LEFT vtx)",
              fill=LABEL_COLOR, font=FONT_SMALL, anchor="rm")

    # Bottom spike label
    draw.text((bot[0], bot[1] + 10*SCALE + 16), "spike_h\n3-pt",
              fill=LABEL_COLOR, font=FONT_SMALL, anchor="mm")

    # Counter-clockwise neutral rest label
    draw.text((px + pw//2, py + ph - 8),
              "tilt_deg=0: right vtx ~rx×0.20 BELOW center (intentional off-balance)",
              fill=DIM_LABEL, font=FONT_SMALL, anchor="mb")


# ── Panel 2: Expression Silhouettes ───────────────────────────────────────────
def draw_expression_panel(draw, px, py, pw, ph):
    """Right panel: expression silhouettes (4 states + Glitch vs Glitchkin note)."""
    draw.rectangle([px, py, px+pw, py+ph], fill=(22, 16, 34))
    draw.rectangle([px, py, px+pw, py+ph], outline=(60, 50, 80), width=1)

    draw.text((px + pw//2, py + 14), "EXPRESSION SILHOUETTES — tilt / squash / stretch range",
              fill=HIGHLIGHT_LINE, font=FONT_HEAD, anchor="mm")

    # 4 expressions side by side in 2x2 grid
    expressions = [
        ("NEUTRAL",      0,   1.00, 1.00, 10, 0,  0,   [], "tilt=0"),
        ("MISCHIEVOUS", +20,  1.00, 1.00, 10, -4, -2,
         [(0, ACID_GREEN), (0, HOT_MAG)], "tilt=+20°"),
        ("PANICKED",    -14,  0.55, 1.00, 10, 0,  0,
         [(0, HOT_MAG), (0, ELEC_CYAN), (0, ELEC_CYAN)], "squash=0.55"),
        ("TRIUMPHANT",   0,   1.00, 1.35, 14, -8, -8,
         [(0, CORRUPT_AMBER), (0, SOFT_GOLD)], "stretch=1.35"),
    ]

    cell_w = pw // 2 - PAD
    cell_h = (ph - 50) // 2 - PAD

    import random
    rng = random.Random(42)

    for idx, (name, tilt, squash, stretch, spike_h, arm_l_dy, arm_r_dy, confetti_hint, note) \
            in enumerate(expressions):
        col = idx % 2
        row = idx // 2
        cx = px + PAD + col * (cell_w + PAD) + cell_w // 2
        cy = py + 42 + PAD + row * (cell_h + PAD) + cell_h // 2

        # Confetti hint (simplified dots)
        if confetti_hint:
            bot_ref = cy + int(38 * 1.0 * stretch * 1.15) + spike_h + 4
            for (_, color) in confetti_hint:
                dx = rng.randint(-18, 18)
                dy = rng.randint(-4, 8)
                draw.rectangle([cx + dx, bot_ref + dy,
                                 cx + dx + 4, bot_ref + dy + 4], fill=color)

        top, right, bot, left, ry_eff = draw_diamond_body(
            draw, cx, cy, 34, 38,
            tilt_deg=tilt, squash=squash, stretch=stretch,
            spike_h=spike_h, arm_l_dy=arm_l_dy, arm_r_dy=arm_r_dy)

        # Expression label
        label_y = cy + int(38 * stretch * 1.15) + spike_h + 16
        draw.text((cx, label_y), name,
                  fill=CORRUPT_AMBER_HL, font=FONT_LABEL, anchor="mt")
        draw.text((cx, label_y + 15), note,
                  fill=DIM_LABEL, font=FONT_SMALL, anchor="mt")

    # Glitch vs Glitchkin distinction note
    note_y = py + ph - 52
    draw.rectangle([px + PAD, note_y - 4, px + pw - PAD, note_y + 48],
                   fill=(38, 28, 55), outline=(80, 60, 110), width=1)
    draw.text((px + pw//2, note_y + 4), "GLITCH vs GENERIC GLITCHKIN",
              fill=HIGHLIGHT_LINE, font=FONT_LABEL, anchor="mm")
    draw.text((px + pw//2, note_y + 20),
              "Glitch = THE consumed-character: DIAMOND body (rx=34, ry=38) + HOT_MAG crack",
              fill=LABEL_COLOR, font=FONT_SMALL, anchor="mm")
    draw.text((px + pw//2, note_y + 34),
              "Glitchkin = generic entity: TRIANGLE body (no crack, smaller scale, no arm-spikes)",
              fill=DIM_LABEL, font=FONT_SMALL, anchor="mm")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    img  = Image.new("RGB", (TOTAL_W, TOTAL_H), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, TOTAL_W, HEADER], fill=(16, 12, 24))
    draw.text((TOTAL_W//2, 14),
              "GLITCH — Diamond Body Primitive Spec  |  Luma & the Glitchkin  |  "
              "per glitch_body_diamond_spec.md (Maya Santos, C41)",
              fill=HIGHLIGHT_LINE, font=FONT_TITLE, anchor="mm")
    draw.text((TOTAL_W//2, 34),
              "rx=34px (1x) / 68px (2x)   ry=38px (1x) / 76px (2x)   ry > rx (ALWAYS taller than wide)",
              fill=DIM_LABEL, font=FONT_SMALL, anchor="mm")

    # Left panel: anatomy
    draw_anatomy_panel(draw, PAD, HEADER + PAD,
                       PANEL_W, TOTAL_H - HEADER - PAD * 2)

    # Right panel: expressions
    draw_expression_panel(draw, PAD + PANEL_W + PAD, HEADER + PAD,
                          PANEL_W, TOTAL_H - HEADER - PAD * 2)

    # Image size rule: ≤1280px
    img.thumbnail((1280, 1280), Image.LANCZOS)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "characters")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_glitch_body_primitive_diagram.png")
    img.save(out_path)
    w, h = img.size
    print(f"Saved: {os.path.abspath(out_path)}  ({w}×{h}px)")
    print("Glitch diamond body primitive diagram — anatomy + expression silhouettes")
    print("Closes Daisuke Kobayashi C14 P8 / C16 P4 (no visual diagram existed)")


if __name__ == "__main__":
    main()
