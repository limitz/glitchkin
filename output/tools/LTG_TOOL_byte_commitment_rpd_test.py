# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_byte_commitment_rpd_test.py
Ryo Hasegawa / Cycle 39

Generates a 2-panel silhouette comparison contact sheet for RPD testing:
  Panel 1: RESIGNED (angled away, high, arms pinned)
  Panel 2: COMMITMENT (full frontal, eye-level, arms open)

Used as input to LTG_TOOL_expression_silhouette.py to verify
COMMITMENT vs RESIGNED RPD similarity ≤ 75%.

Output: output/characters/motion/LTG_CHAR_byte_commitment_rpd_input.png
"""

from PIL import Image, ImageDraw
import os
import math

BYTE_TEAL    = (  0, 212, 232)
LINE_COLOR   = ( 30,  50,  55)
VOID_BLACK   = ( 10,  10,  20)
SOFT_GOLD    = (232, 201,  90)
HOT_MAGENTA  = (255,  45, 107)
ELEC_CYAN    = (  0, 240, 255)
LABEL_TEXT   = (230, 245, 248)

W, H = 640, 320   # 2 panels, each 320x320
PANEL_W = W // 2
PANEL_H = H


def draw_limb(draw, p0, p1, body_col, lw):
    limb_w = max(5, lw * 3)
    draw.line([p0, p1], fill=body_col, width=limb_w)
    draw.line([p0, p1], fill=LINE_COLOR, width=lw)
    tip_r = lw * 2
    draw.ellipse([p1[0]-tip_r, p1[1]-tip_r, p1[0]+tip_r, p1[1]+tip_r],
                 fill=body_col, outline=LINE_COLOR, width=max(1, lw-1))


def draw_resigned_byte(draw, cx, cy, bw, bh):
    """RESIGNED: body angled 30° away, high float, arms pinned close, dim eye."""
    s = bw / 30
    lw = max(2, int(2.2 * s))
    tilt_deg = 25   # angled away
    tilt_rad = math.radians(tilt_deg)
    tx = int(math.sin(tilt_rad) * bh)

    # Body
    draw.ellipse([cx - bw + tx, cy - bh, cx + bw + tx, cy + bh],
                 fill=BYTE_TEAL, outline=LINE_COLOR, width=lw)

    # Crack scar (viewer right)
    crack_x = cx + int(bw * 0.55) + tx
    crack_y = cy - int(bh * 0.3)
    draw.line([(crack_x, crack_y),
               (crack_x - int(6*s), crack_y + int(8*s)),
               (crack_x - int(3*s), crack_y + int(14*s))],
              fill=HOT_MAGENTA, width=max(1, lw-1))

    # Arms PINNED (close to body)
    limb_len = int(20 * s)
    left_arm_base  = (cx - int(bw * 0.55) + tx, cy - int(bh * 0.2))
    left_arm_end   = (cx - int(bw * 0.65) + tx, cy - int(bh * 0.45))
    right_arm_base = (cx + int(bw * 0.55) + tx, cy - int(bh * 0.2))
    right_arm_end  = (cx + int(bw * 0.65) + tx, cy - int(bh * 0.45))
    draw_limb(draw, left_arm_base, left_arm_end, BYTE_TEAL, lw)
    draw_limb(draw, right_arm_base, right_arm_end, BYTE_TEAL, lw)

    # Legs
    leg_configs = [
        ((cx - int(bw*0.35)+tx, cy+int(bh*0.6)), (cx - int(bw*0.45)+tx, cy+int(bh*0.6)+limb_len)),
        ((cx + int(bw*0.35)+tx, cy+int(bh*0.6)), (cx + int(bw*0.45)+tx, cy+int(bh*0.6)+limb_len)),
    ]
    for p0, p1 in leg_configs:
        draw_limb(draw, p0, p1, BYTE_TEAL, lw)

    # Antenna lagging back
    ant_bx = cx + int(bw * 0.2) + tx
    ant_by = cy - bh
    ant_dx = int(math.sin(math.radians(-8)) * int(12*s))
    ant_ty = ant_by - int(12*s)
    draw.line([(ant_bx, ant_by), (ant_bx + ant_dx, ant_ty)],
              fill=LINE_COLOR, width=lw-1)

    # Eyes: dim/droopy left, heavy-lid right
    eye_gap = int(bw * 0.42)
    eye_y = cy - int(bh * 0.1)
    pixel_sz = max(2, int(4 * s))
    # Left eye dim
    draw.rectangle([cx - eye_gap + tx + pixel_sz,
                     eye_y + pixel_sz * 2,
                     cx - eye_gap + tx + pixel_sz * 2 - 1,
                     eye_y + pixel_sz * 3 - 1], fill=(130, 100, 40))
    # Right eye heavy lid
    for ey_off in range(3):
        for ex_off in range(3):
            col = LINE_COLOR if ey_off == 0 else (20, 40, 45)
            draw.rectangle([cx + eye_gap + tx + ex_off*pixel_sz - pixel_sz,
                             eye_y + ey_off*pixel_sz,
                             cx + eye_gap + tx + ex_off*pixel_sz,
                             eye_y + ey_off*pixel_sz + pixel_sz - 1], fill=col)

    # Mouth: flat line
    mouth_y = cy + int(bh * 0.35)
    mouth_w = int(bw * 0.5)
    draw.line([(cx - mouth_w + tx, mouth_y), (cx + mouth_w + tx, mouth_y)],
              fill=LINE_COLOR, width=lw-1)


def draw_commitment_byte(draw, cx, cy, bw, bh):
    """COMMITMENT: full frontal, slight -3° lean, arms open, eye-level."""
    s = bw / 30
    lw = max(2, int(2.2 * s))
    tilt_deg = -3  # slight forward lean
    tilt_rad = math.radians(tilt_deg)
    tx = int(math.sin(tilt_rad) * bh)

    # Body
    draw.ellipse([cx - bw + tx, cy - bh, cx + bw + tx, cy + bh],
                 fill=BYTE_TEAL, outline=LINE_COLOR, width=lw)

    # Crack scar (viewer right)
    crack_x = cx + int(bw * 0.55) + tx
    crack_y = cy - int(bh * 0.3)
    draw.line([(crack_x, crack_y),
               (crack_x - int(6*s), crack_y + int(8*s)),
               (crack_x - int(3*s), crack_y + int(14*s))],
              fill=HOT_MAGENTA, width=max(1, lw-1))

    # Arms OPEN (out, not reaching — wider than pinned)
    limb_len = int(20 * s)
    left_arm_base  = (cx - int(bw * 0.65) + tx, cy - int(bh * 0.2))
    left_arm_end   = (cx - int(bw * 1.05) + tx, cy - int(bh * 0.3))
    right_arm_base = (cx + int(bw * 0.65) + tx, cy - int(bh * 0.2))
    right_arm_end  = (cx + int(bw * 1.05) + tx, cy - int(bh * 0.3))
    draw_limb(draw, left_arm_base, left_arm_end, BYTE_TEAL, lw)
    draw_limb(draw, right_arm_base, right_arm_end, BYTE_TEAL, lw)

    # Legs
    leg_configs = [
        ((cx - int(bw*0.35)+tx, cy+int(bh*0.6)), (cx - int(bw*0.45)+tx, cy+int(bh*0.6)+limb_len)),
        ((cx + int(bw*0.35)+tx, cy+int(bh*0.6)), (cx + int(bw*0.45)+tx, cy+int(bh*0.6)+limb_len)),
    ]
    for p0, p1 in leg_configs:
        draw_limb(draw, p0, p1, BYTE_TEAL, lw)

    # Antenna slightly forward
    ant_bx = cx + int(bw * 0.2) + tx
    ant_by = cy - bh
    ant_dx = int(math.sin(math.radians(4)) * int(12*s))
    ant_ty = ant_by - int(12*s)
    draw.line([(ant_bx, ant_by), (ant_bx + ant_dx, ant_ty)],
              fill=LINE_COLOR, width=lw-1)

    # Eyes: SEARCHING left (pupil left), right eye open+level with crack
    eye_gap = int(bw * 0.42)
    eye_y = cy - int(bh * 0.1)
    pixel_sz = max(2, int(4 * s))
    # Left eye: pupil toward Luma (left)
    for ey_off in range(3):
        for ex_off in range(3):
            if ey_off == 1 and ex_off == 0:
                col = SOFT_GOLD
            else:
                col = (20, 40, 45)
            draw.rectangle([cx - eye_gap + tx + ex_off*pixel_sz,
                             eye_y + ey_off*pixel_sz,
                             cx - eye_gap + tx + ex_off*pixel_sz + pixel_sz - 1,
                             eye_y + ey_off*pixel_sz + pixel_sz - 1], fill=col)
    # Right eye: open, crack present
    for ey_off in range(3):
        for ex_off in range(3):
            if ey_off == 0 and ex_off == 2:
                col = HOT_MAGENTA
            else:
                col = ELEC_CYAN
            draw.rectangle([cx + eye_gap + tx + ex_off*pixel_sz - pixel_sz,
                             eye_y + ey_off*pixel_sz,
                             cx + eye_gap + tx + ex_off*pixel_sz,
                             eye_y + ey_off*pixel_sz + pixel_sz - 1], fill=col)

    # Mouth: subtle warmth arc
    mouth_y = cy + int(bh * 0.35)
    mouth_w = int(bw * 0.5)
    draw.arc([cx - mouth_w + tx, mouth_y - int(bh * 0.10),
              cx + mouth_w + tx, mouth_y + int(bh * 0.10)],
             start=200, end=340, fill=LINE_COLOR, width=lw-1)


def build_sheet():
    img = Image.new("RGB", (W, H), VOID_BLACK)
    draw = ImageDraw.Draw(img)

    # Panel 1: RESIGNED
    cx1, cy1 = PANEL_W // 2, PANEL_H // 2
    bw, bh = 40, 36

    # Draw panel bg (light for good silhouette contrast)
    draw.rectangle([0, 0, PANEL_W-1, PANEL_H-1], fill=(235, 238, 242))
    draw_resigned_byte(draw, cx1, cy1, bw, bh)
    draw.text((8, PANEL_H - 18), "RESIGNED", fill=(30, 50, 55))

    # Panel 2: COMMITMENT
    cx2, cy2 = PANEL_W + PANEL_W // 2, PANEL_H // 2
    draw.rectangle([PANEL_W, 0, W-1, PANEL_H-1], fill=(235, 238, 242))
    draw_commitment_byte(draw, cx2, cy2, bw, bh)
    draw.text((PANEL_W + 8, PANEL_H - 18), "COMMITMENT", fill=(30, 50, 55))

    # Divider
    draw.line([(PANEL_W, 0), (PANEL_W, H)], fill=VOID_BLACK, width=2)

    img.thumbnail((1280, 1280))
    assert img.width <= 1280 and img.height <= 1280
    return img


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "characters", "motion")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_byte_commitment_rpd_input.png")
    img = build_sheet()
    img.save(out_path)
    print(f"Saved: {out_path}  ({img.width}×{img.height})")


if __name__ == "__main__":
    main()
