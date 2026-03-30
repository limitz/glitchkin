# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
Byte Expression Sheet Generator — "Luma & the Glitchkin"
Cycle 6: body varies per expression, right eye carries emotion,
annotations added with prev/next state context.
"""
from PIL import Image, ImageDraw, ImageFont
import math

BYTE_TEAL  = (0, 212, 232)   # #00D4E8 — body fill
BYTE_HL    = (0, 240, 255)   # #00F0FF — highlights only
BYTE_SH    = (0, 144, 176)   # #0090B0 — shadow
SCAR_MAG   = (255, 45, 107)  # #FF2D6B
LINE       = (10, 10, 20)    # #0A0A14 void black
EYE_W      = (240, 240, 245)
BG         = (20, 18, 28)

# Each expression: (name, left_eye_symbol, emotion,
#                   body_data, right_eye_data, prev_state, next_state)
# body_data keys: arm_dy (arm vertical offset from neutral),
#                 arm_x_scale (how far arms extend),
#                 leg_spread (leg x offset multiplier),
#                 body_tilt (horizontal skew of body top),
#                 body_squash (vertical scale 1.0 = normal)
# right_eye_data: style key ('wide', 'narrow', 'angry', 'normal', 'flat', 'wide_scared', 'droopy')

EXPRESSIONS = [
    (
        "GRUMPY",
        "grumpy", "disgust",
        # CONFRONTATIONAL posture (Cycle 8 fix — Dmitri + Marcus mandates):
        # body_tilt=-8: negative = forward lean TOWARD adversary (aggressive, not defeated).
        # arm_l_dy=-6, arm_r_dy=-10: both arms raised but asymmetric (ready to refuse/block).
        # arm_x_scale=1.1: arms extend OUT slightly (wider stance reads as defensive-aggressive).
        # leg_spread=1.1: planted, squared-up feet.
        # Previous values (body_tilt=-4, arm_dy=-2, arm_x_scale=0.85) read as defeated/passive.
        {"arm_dy": -8, "arm_x_scale": 1.1, "leg_spread": 1.1, "body_tilt": -8, "body_squash": 1.0,
         "arm_l_dy": -6, "arm_r_dy": -10},
        "angry",
        "← was: SEARCHING",
        "→ next: REFUSING"
    ),
    (
        "SEARCHING",
        "loading", "curious",
        {"arm_dy": -4, "arm_x_scale": 1.1, "leg_spread": 1.2, "body_tilt": -8, "body_squash": 1.0,
         "arm_l_dy": 4, "arm_r_dy": -18},   # right arm extended/raised (scanning), left relaxed
        "wide",
        "← was: IDLE",
        "→ next: ALARMED/FOUND"
    ),
    (
        "ALARMED",
        "!", "fear",
        {"arm_dy": -16, "arm_x_scale": 1.5, "leg_spread": 1.6, "body_tilt": 0, "body_squash": 0.92,
         "arm_l_dy": -10, "arm_r_dy": -22},  # asymmetric startle: one arm higher
        "wide_scared",
        "← was: SEARCHING",
        "→ next: FLEEING/FROZEN"
    ),
    (
        "RELUCTANT JOY",
        "♥", "happy",
        {"arm_dy": 8, "arm_x_scale": 0.6, "leg_spread": 0.8, "body_tilt": 10, "body_squash": 1.0,
         "arm_l_dy": 8, "arm_r_dy": 8},
        "droopy",
        "← was: GRUMPY",
        "→ next: DENYING IT"
    ),
    (
        "CONFUSED",
        "?", "confused",
        {"arm_dy": -6, "arm_x_scale": 1.0, "leg_spread": 1.1, "body_tilt": -18, "body_squash": 1.0,
         "arm_l_dy": -14, "arm_r_dy": 2},  # one arm raised (questioning gesture), one low
        "squint",
        "← was: ANY STATE",
        "→ next: SEARCHING"
    ),
    (
        "POWERED DOWN",
        "flat", "neutral",
        {"arm_dy": 18, "arm_x_scale": 0.7, "leg_spread": 0.6, "body_tilt": 0, "body_squash": 0.88,
         "arm_l_dy": 18, "arm_r_dy": 18},
        "flat",
        "← was: ANY STATE",
        "→ next: BOOTING UP"
    ),
]

PANEL_W, PANEL_H = 240, 320
COLS = 3
ROWS = 2
PAD = 16
HEADER = 50


def draw_pixel_symbol(draw, cx, cy, size, symbol):
    """Draw a pixel-eye symbol using a 5x5 grid at given position and size."""
    cell = size // 5
    if cell < 2:
        cell = 2
    ox = cx - (5*cell)//2
    oy = cy - (5*cell)//2

    PIXEL_CYAN = (0, 240, 255)
    PIXEL_MAG  = (255, 45, 107)
    OFF        = (20, 18, 28)

    grids = {
        "!": [
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0],
            [0,0,1,0,0],
        ],
        "?": [
            [0,1,1,1,0],
            [0,0,0,1,0],
            [0,0,1,1,0],
            [0,0,0,0,0],
            [0,0,1,0,0],
        ],
        "♥": [
            [0,1,0,1,0],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [0,1,1,1,0],
            [0,0,1,0,0],
        ],
        "loading": [
            [1,0,1,0,1],
            [0,0,0,0,0],
            [1,0,0,0,1],
            [0,0,0,0,0],
            [1,0,1,0,1],
        ],
        "flat": [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [1,1,1,1,1],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ],
        # GRUMPY: minus-sign (flat bar) with downward corner ticks — distinct from POWERED DOWN flat
        # flat is centred; grumpy has corner ticks making it read as a scowl line.
        "grumpy": [
            [0,0,0,0,0],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,1],
            [0,0,0,0,0],
        ],
        "normal": None,  # normal eye
    }

    grid = grids.get(symbol)
    if grid is None:
        # Draw a normal eye (iris + pupil)
        draw.ellipse([cx-cell*2, cy-cell*2, cx+cell*2, cy+cell*2], fill=EYE_W)
        draw.ellipse([cx-cell, cy-cell, cx+cell, cy+cell], fill=(60,38,20))
        draw.ellipse([cx-cell//2, cy-cell//2, cx+cell//2, cy+cell//2], fill=LINE)
        draw.ellipse([cx+cell//2, cy-cell, cx+cell*2-2, cy-cell//2], fill=(255,252,245))
        return

    # Pixel eye background
    draw.rectangle([ox-2, oy-2, ox+5*cell+2, oy+5*cell+2], fill=(255,255,255))
    draw.rectangle([ox-2, oy-2, ox+5*cell+2, oy+5*cell+2], outline=LINE, width=1)

    for row in range(5):
        for col in range(5):
            v = grid[row][col]
            px = ox + col*cell
            py = oy + row*cell
            color = PIXEL_CYAN if v == 1 else PIXEL_MAG if v == 2 else OFF
            draw.rectangle([px+1, py+1, px+cell-1, py+cell-1], fill=color)


def draw_right_eye(draw, cx, cy, size, style):
    """Draw Byte's right (organic) eye with emotion-specific expression."""
    cell = size // 5
    if cell < 2:
        cell = 2

    if style == "flat":
        # Powered down: flat line matching left eye
        draw_pixel_symbol(draw, cx, cy, size, "flat")
        return

    # Base white sclera for all organic styles
    ew = cell * 2
    eh = cell * 2

    if style == "wide":
        # SEARCHING — wide open, slightly wandering
        draw.ellipse([cx-ew, cy-eh, cx+ew, cy+eh], fill=EYE_W)
        draw.ellipse([cx-cell+2, cy-cell+2, cx+cell+2, cy+cell+2], fill=(60,38,20))
        draw.ellipse([cx-cell//2+2, cy-cell//2+2, cx+cell//2+2, cy+cell//2+2], fill=LINE)
        draw.ellipse([cx+cell, cy-eh+2, cx+ew-2, cy-cell], fill=(255,252,245))

    elif style == "wide_scared":
        # ALARMED — whites showing all around, pupil centered (deer-in-headlights)
        draw.ellipse([cx-ew-2, cy-eh-3, cx+ew+2, cy+eh+3], fill=EYE_W, outline=LINE, width=2)
        # Pupil small and centered
        draw.ellipse([cx-cell+1, cy-cell+1, cx+cell-1, cy+cell-1], fill=(60,38,20))
        draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=LINE)
        # Extra upper highlight suggesting dilated terror
        draw.ellipse([cx+cell-2, cy-eh+2, cx+ew-2, cy-cell+2], fill=(255,252,245))
        # Extra bottom white visible (shows whites below iris)
        draw.arc([cx-ew-2, cy-eh-3, cx+ew+2, cy+eh+3], start=200, end=340, fill=(220,220,230), width=2)

    elif style == "angry":
        # GRUMPY — heavy upper lid pressing down, pupil shifted down-inward
        draw.ellipse([cx-ew, cy-eh+4, cx+ew, cy+eh], fill=EYE_W)
        # Pupil shifted down and inward (glare)
        draw.ellipse([cx-cell-2, cy, cx+cell-2, cy+cell*2-2], fill=(60,38,20))
        draw.ellipse([cx-4-2, cy+4, cx+4-2, cy+4+8], fill=LINE)
        draw.ellipse([cx+2, cy+2, cx+cell+2, cy+cell-2], fill=(255,252,245))
        # Heavy upper eyelid line (scowl)
        draw.arc([cx-ew, cy-eh+4, cx+ew, cy+eh], start=195, end=345, fill=LINE, width=5)
        draw.line([(cx-ew, cy-eh//2+4), (cx+ew, cy-eh//2)], fill=LINE, width=3)

    elif style == "droopy":
        # RELUCTANT JOY — heavy-lidded, trying NOT to smile, lid drooping
        draw.ellipse([cx-ew, cy-eh+6, cx+ew, cy+eh+2], fill=EYE_W)
        draw.ellipse([cx-cell+1, cy-cell+4, cx+cell+1, cy+cell+4], fill=(60,38,20))
        draw.ellipse([cx-4+1, cy+1, cx+4+1, cy+8], fill=LINE)
        draw.ellipse([cx+cell, cy-3, cx+ew-2, cy+3], fill=(255,252,245))
        # Droopy upper lid (half-closed, suppressing emotion)
        draw.arc([cx-ew, cy-eh+6, cx+ew, cy+eh+2], start=195, end=345, fill=LINE, width=6)
        # Slight upturn at corner — he's failing to suppress it
        draw.line([(cx-ew, cy+5), (cx-ew+4, cy+2)], fill=LINE, width=2)

    elif style == "squint":
        # CONFUSED — one eye slightly squinted/tilted (tilted head matches)
        draw.ellipse([cx-ew, cy-eh+4, cx+ew, cy+eh+2], fill=EYE_W)
        # Pupil shifted slightly up (confused upward glance)
        draw.ellipse([cx-cell, cy-cell-2, cx+cell, cy+cell-2], fill=(60,38,20))
        draw.ellipse([cx-4, cy-8, cx+4, cy], fill=LINE)
        draw.ellipse([cx+cell-2, cy-eh+4, cx+ew-4, cy-cell], fill=(255,252,245))
        # Furrowed brow suggestion — angled lid
        draw.line([(cx-ew, cy-eh//2+4), (cx+ew, cy-eh//2+2)], fill=LINE, width=3)

    else:
        # Default normal
        draw.ellipse([cx-ew, cy-eh, cx+ew, cy+eh], fill=EYE_W)
        draw.ellipse([cx-cell, cy-cell, cx+cell, cy+cell], fill=(60,38,20))
        draw.ellipse([cx-cell//2, cy-cell//2, cx+cell//2, cy+cell//2], fill=LINE)
        draw.ellipse([cx+cell//2, cy-cell, cx+cell*2-2, cy-cell//2], fill=(255,252,245))


def draw_byte(draw, cx, cy, size, expression_name, cracked_symbol, emotion, body_data, right_eye_style):
    """Draw Byte with per-expression body variation.

    BODY SHAPE DECISION (Cycle 8): OVAL (ellipse), matching style_frame_01_rendered.py.
    style_frame_01_rendered.py draws Byte's body with draw.ellipse (oval/ellipse).
    Expression sheet now uses the same shape for consistency across all production assets.
    The chamfered-box polygon from earlier cycles is RETIRED.
    """
    s = size

    arm_dy      = body_data.get("arm_dy", 0)
    arm_x_scale = body_data.get("arm_x_scale", 1.0)
    leg_spread  = body_data.get("leg_spread", 1.0)
    body_tilt   = body_data.get("body_tilt", 0)
    body_squash = body_data.get("body_squash", 1.0)
    # Per-arm vertical offset (falls back to shared arm_dy if not specified)
    arm_l_dy    = body_data.get("arm_l_dy", arm_dy)
    arm_r_dy    = body_data.get("arm_r_dy", arm_dy)

    # OVAL body — rx/ry derived from size + squash.
    # body_tilt shifts the oval center horizontally (forward lean).
    body_rx = s // 2
    body_ry = int(s * 0.55 * body_squash)   # slightly taller than wide, squash applies
    bcx = cx + body_tilt                      # tilt offsets the whole oval laterally
    bcy = cy

    # Main oval fill
    draw.ellipse([bcx - body_rx, bcy - body_ry,
                  bcx + body_rx, bcy + body_ry],
                 fill=BYTE_TEAL, outline=LINE, width=3)

    # Shadow side — right half filled ellipse (darker teal), same tilt
    # Use a clipped rectangle overlay to approximate right-half shadow
    shadow_pts = [
        (bcx,                  bcy - body_ry),
        (bcx + body_rx,        bcy - body_ry + 4),
        (bcx + body_rx,        bcy + body_ry - 4),
        (bcx,                  bcy + body_ry),
        (bcx + body_rx // 2,   bcy + body_ry),
        (bcx + body_rx,        bcy + body_ry // 2),
        (bcx + body_rx,        bcy),
    ]
    draw.polygon(shadow_pts, fill=BYTE_SH)

    # Highlight arc — top-left of oval (GL spec)
    draw.arc([bcx - body_rx, bcy - body_ry, bcx + body_rx, bcy + body_ry],
             start=200, end=310, fill=BYTE_HL, width=3)

    sh = body_ry * 2  # use ry*2 as effective height for legacy references below

    # Magenta scar markings — referenced to oval center + body_ry
    crack_x = bcx - s//4
    draw.line([(crack_x, bcy - body_ry//2), (crack_x + s//8, bcy - body_ry//6)], fill=SCAR_MAG, width=2)
    draw.line([(crack_x + s//8, bcy - body_ry//6), (crack_x - s//10, bcy + body_ry//6)], fill=SCAR_MAG, width=2)

    # Damage notch on right side of oval
    notch_pts = [
        (bcx + body_rx - 4,           bcy - body_ry//4),
        (bcx + body_rx + s//12,        bcy - body_ry//6),
        (bcx + body_rx - 4,            bcy + body_ry//6),
    ]
    draw.polygon(notch_pts, fill=BG, outline=LINE, width=1)

    # EYES — positioned relative to oval center
    eye_y = bcy - body_ry//5
    eye_size = s // 4

    # Left eye = cracked pixel display
    lx = bcx - s//5
    crack_frame_size = eye_size + 4
    draw.rectangle([lx - crack_frame_size//2, eye_y - crack_frame_size//2,
                    lx + crack_frame_size//2, eye_y + crack_frame_size//2],
                   fill=(255,255,255), outline=LINE, width=2)
    draw.line([(lx + 2, eye_y - crack_frame_size//2),
               (lx - 4, eye_y + crack_frame_size//2)], fill=LINE, width=2)
    draw_pixel_symbol(draw, lx, eye_y, eye_size, cracked_symbol)

    # Right eye — carries emotion via style
    rx = bcx + s//5
    draw_right_eye(draw, rx, eye_y, eye_size, right_eye_style)

    # MOUTH — varies by emotion, placed in lower half of oval
    mouth_y = bcy + body_ry // 3
    mw = s // 3
    if emotion == "disgust":
        draw.arc([bcx-mw, mouth_y-8, bcx+mw, mouth_y+16], start=200, end=340, fill=LINE, width=3)
    elif emotion == "curious":
        draw.ellipse([bcx-8, mouth_y-8, bcx+8, mouth_y+4], outline=LINE, width=2)
    elif emotion == "fear":
        draw.arc([bcx-mw+4, mouth_y-10, bcx+mw-4, mouth_y+22], start=10, end=170, fill=LINE, width=3)
        draw.chord([bcx-mw+8, mouth_y-8, bcx+mw-8, mouth_y+18], start=10, end=170, fill=(180,160,150))
    elif emotion == "happy":
        draw.arc([bcx-mw//2, mouth_y-6, bcx+mw//2, mouth_y+12], start=20, end=160, fill=LINE, width=3)
    elif emotion == "confused":
        for i in range(4):
            x1 = bcx - mw + i*(mw//2)
            y1 = mouth_y + (4 if i%2==0 else -4)
            x2 = x1 + mw//2
            y2 = mouth_y + (-4 if i%2==0 else 4)
            draw.line([(x1,y1),(x2,y2)], fill=LINE, width=2)
    elif emotion == "neutral":
        pass  # powered down
    else:
        draw.line([(bcx-mw//2, mouth_y), (bcx+mw//2, mouth_y)], fill=LINE, width=2)

    # LIMBS — attach at oval edge (body_rx wide, body_ry tall)
    lw = s//6
    lh = s//5
    arm_extend = int(lw * arm_x_scale)
    arm_base_y = bcy - body_ry//5   # neutral arm attachment point (upper body area)

    # Left arm — independent vertical offset
    left_arm_y = arm_base_y + arm_l_dy
    draw.rectangle([bcx - body_rx - arm_extend, left_arm_y,
                    bcx - body_rx,              left_arm_y + lh],
                   fill=BYTE_TEAL, outline=LINE, width=2)
    # Right arm — independent vertical offset
    right_arm_y = arm_base_y + arm_r_dy
    draw.rectangle([bcx + body_rx,              right_arm_y,
                    bcx + body_rx + arm_extend, right_arm_y + lh],
                   fill=BYTE_TEAL, outline=LINE, width=2)

    # LEGS — attach at bottom of oval
    leg_offset = int(s//4 * leg_spread)
    leg_h = lh
    leg_w = int(lw * 0.9)
    draw.rectangle([bcx - leg_offset - leg_w//2, bcy + body_ry,
                    bcx - leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE, width=2)
    draw.rectangle([bcx + leg_offset - leg_w//2, bcy + body_ry,
                    bcx + leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE, width=2)

    # Hover particle confetti — 10x10px (canonical spec, matches turnaround generator)
    for (px, py, pc) in [
        (bcx-20, bcy + body_ry + leg_h + 5,  BYTE_HL),
        (bcx+5,  bcy + body_ry + leg_h + 8,  SCAR_MAG),
        (bcx+25, bcy + body_ry + leg_h + 3,  BYTE_HL),
        (bcx-35, bcy + body_ry + leg_h + 10, (0,200,180)),
    ]:
        draw.rectangle([px, py, px+10, py+10], fill=pc)


def generate_byte_expressions(output_path):
    total_w = COLS * (PANEL_W + PAD) + PAD
    total_h = HEADER + ROWS * (PANEL_H + PAD) + PAD

    img = Image.new('RGB', (total_w, total_h), BG)
    draw = ImageDraw.Draw(img)

    try:
        font       = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        font_sm    = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except:
        font = font_sm = font_title = ImageFont.load_default()

    draw.text((PAD, 12), "BYTE — Expression Sheet — Luma & the Glitchkin",
              fill=(0,240,255), font=font_title)

    for i, (name, symbol, emotion, body_data, right_eye_style, prev_st, next_st) in enumerate(EXPRESSIONS):
        col = i % COLS
        row = i // COLS
        px = PAD + col * (PANEL_W + PAD)
        py = HEADER + row * (PANEL_H + PAD)

        # Panel background
        draw.rectangle([px, py, px+PANEL_W, py+PANEL_H], fill=(16,14,24))
        draw.rectangle([px, py, px+PANEL_W, py+PANEL_H], outline=(40,35,55), width=1)

        # Draw Byte — slightly higher to leave room for annotation bar
        byte_size = 88
        bcx = px + PANEL_W // 2
        bcy = py + PANEL_H // 2 - 20
        draw_byte(draw, bcx, bcy, byte_size, name, symbol, emotion, body_data, right_eye_style)

        # Label bar at bottom
        bar_h = 58
        draw.rectangle([px, py+PANEL_H-bar_h, px+PANEL_W, py+PANEL_H], fill=(10,8,18))
        draw.text((px+6, py+PANEL_H-bar_h+4), name, fill=(0,240,255), font=font)
        # Prev/next state annotations (motion context)
        draw.text((px+6, py+PANEL_H-bar_h+22), prev_st, fill=(120,110,140), font=font_sm)
        draw.text((px+6, py+PANEL_H-bar_h+36), next_st, fill=(120,110,140), font=font_sm)

    img.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == '__main__':
    generate_byte_expressions("/home/wipkat/team/output/characters/main/byte_expressions.png")
