# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
Panel Chaos Generator — Luma & the Glitchkin
Cycle 11: Generates panels P14–P24 (The Chaos Sequence).
Emotional arc section: CHAOS (escalating from first-contact glitch cascade
through peak mayhem — Byte ricocheting, Luma falling, mutual discovery,
other Glitchkin breaching, and the show's promise shot).

MEMORY.md principles applied:
- Lower-center = anchor/mystery. Upper-right = exit.
- Pulse/glitch FX must be VISIBLE in image, not just named in caption.
- Bridge panels are spatial contracts (P22a is the Byte-lands-on-shoulder bridge).
- OTS shots: whose shoulder, camera height, direction, distance — all explicit.
- Character introduction shots need scale — Byte at 80-100px minimum.
- Two-point perspective for three-quarter interior views.
- Glow effects ADD light (alpha_composite, not dark overlay).
- Contact sheet is the first test. Arc must read in thumbnail.

Output: /home/wipkat/team/output/storyboards/panels/
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random

PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
PW, PH = 480, 270
CAPTION_H = 48
DRAW_H = PH - CAPTION_H
BORDER = 2

# Color palette
BG_DRAW       = (242, 240, 235)
BG_CAPTION    = (25, 20, 18)
BORDER_COL    = (20, 15, 12)
TEXT_CAPTION  = (235, 228, 210)
TEXT_PANEL    = (20, 15, 12)

# Scene colors
WARM_DARK     = (22, 16, 10)
WARM_AMBER    = (55, 38, 24)
WARM_WALL     = (45, 30, 18)
LUMA_SKIN     = (200, 136, 90)
LUMA_HAIR     = (22, 14, 8)
LUMA_PJ       = (160, 200, 180)   # mint PJ top
BYTE_CYAN     = (0, 212, 232)
BYTE_DARK     = (8, 8, 18)
GLITCH_CYAN   = (0, 240, 255)
GLITCH_MAG    = (255, 0, 200)
GLITCH_ACID   = (180, 255, 40)
FLOOR_DARK    = (16, 12, 8)
SHELF_WARM    = (48, 32, 18)


# ── Utilities ─────────────────────────────────────────────────────────────────

def load_fonts():
    try:
        font       = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        font_bold  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_cap   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        font_ann   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except Exception:
        font = font_bold = font_cap = font_ann = ImageFont.load_default()
    return font, font_bold, font_cap, font_ann


def apply_dutch_tilt(img, degrees, bg_color=(8, 4, 14)):
    """Rotate the drawing area portion of an image by degrees (Dutch tilt).
    Draws scene content on a temp canvas, rotates entire scene, then pastes back.
    This delivers TRUE geometric tilt — not just a tilted floor line.
    Per Carmen's Cycle 8 critique: geometry always wins over annotation text.
    """
    # Crop the draw area (not the caption bar)
    draw_area = img.crop((0, 0, PW, DRAW_H))
    # Rotate with expand=False so it stays the same size, fill bg_color for margins
    rotated = draw_area.rotate(degrees, resample=Image.BICUBIC, expand=False,
                               fillcolor=bg_color)
    img.paste(rotated, (0, 0))


def make_panel(panel_num, shot_type, caption, draw_fn, filename,
               dutch_tilt_deg=0, dutch_bg=(8, 4, 14)):
    img  = Image.new('RGB', (PW, PH), BG_DRAW)
    draw = ImageDraw.Draw(img)
    font, font_bold, font_cap, font_ann = load_fonts()

    # Drawing area
    draw.rectangle([0, 0, PW, DRAW_H], fill=WARM_DARK)

    # Scene content
    draw_fn(draw, img, font, font_bold, font_ann)

    # Apply Dutch tilt AFTER scene is drawn — rotates ENTIRE scene contents
    if dutch_tilt_deg != 0:
        apply_dutch_tilt(img, dutch_tilt_deg, bg_color=dutch_bg)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.text((8, DRAW_H + 5), caption[:80], fill=TEXT_CAPTION, font=font_cap)

    # Border
    draw.rectangle([0, 0, PW-1, PH-1], outline=BORDER_COL, width=BORDER)

    # Panel number badge (top-left)
    draw.rectangle([0, 0, 42, 20], fill=(20, 15, 12))
    draw.text((4, 3), f"P{panel_num}", fill=(235, 228, 210), font=font_bold)

    # Shot type badge (top-right)
    sw = min(len(shot_type) * 7 + 8, 120)
    draw.rectangle([PW - sw, 0, PW, 20], fill=(20, 15, 12))
    draw.text((PW - sw + 4, 3), shot_type, fill=(235, 228, 210), font=font_bold)

    out = f"{PANELS_DIR}/{filename}"
    img.save(out)
    print(f"  Saved: {out}")
    return img


def add_pixel_confetti(draw, x_range, y_range, count, seed, alpha=200,
                       colors=None):
    """Scatter pixel confetti — visible glitch FX, not decoration.
    Trail direction and density carry spatial/temporal meaning."""
    if colors is None:
        colors = [GLITCH_CYAN, GLITCH_MAG, (255, 255, 180)]
    rng = random.Random(seed)
    for _ in range(count):
        px = rng.randint(x_range[0], x_range[1])
        py = rng.randint(y_range[0], y_range[1])
        sz = rng.randint(1, 4)
        col = rng.choice(colors)
        draw.rectangle([px, py, px + sz, py + sz], fill=col)


def add_glitch_glow(img, cx, cy, r_max, color_rgb, max_alpha=80):
    """Additive glow composite — light adds, never darkens.
    Uses alpha_composite per MEMORY.md Cycle 7 lesson."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for r in range(r_max, 4, -4):
        a = int(max_alpha * (1 - r / r_max) * 0.7)
        od.ellipse([cx - r, cy - r, cx + r, cy + r],
                   fill=(*color_rgb, a))
    img_rgba = img.convert('RGBA')
    img_rgba.alpha_composite(overlay)
    result = img_rgba.convert('RGB')
    # copy pixels back
    img.paste(result)


def draw_byte_body(draw, bx, by, size=42, expression='alarmed',
                   lean_deg=0, trail=True):
    """
    Draw Byte's body at (bx, by) center.
    expression: 'alarmed' | 'processing' | 'offended' | 'resigned' | 'disgusted'
    lean_deg: body tilt in degrees (positive = right lean)
    size: body square size in pixels — minimum 80 for debut shots, 42 for small/background.
    Four expression components (MEMORY.md Cycle 6):
      1. Normal eye aperture
      2. Cracked-eye pixel state
      3. Mouth shape
      4. Body lean direction
    """
    hs = size // 2
    c  = max(2, size // 8)   # chamfer

    # Pixel trail BEFORE body (shows movement history)
    if trail:
        for t in range(1, 4):
            tx = bx - t * (size // 2)
            alpha_dec = t * 60
            trail_col = (0, max(0, 212 - alpha_dec), max(0, 232 - alpha_dec))
            draw.rectangle([tx - size // 3, by - size // 3,
                            tx + size // 3, by + size // 3],
                           outline=trail_col, width=1)

    # Lean offset (simple shear)
    lean_px = int(hs * math.tan(math.radians(lean_deg)) * 0.5)

    # Hover glow below (additive look via layered ellipses)
    for gr in [18, 12, 7]:
        gc = max(0, 80 - gr * 4)
        draw.ellipse([bx - gr * 2, by + hs - 4 + gr // 2,
                      bx + gr * 2, by + hs + 4 + gr // 2],
                     fill=(0, gc, gc + 10))

    # Body chamfered rectangle
    body_pts = [
        (bx - hs + c + lean_px, by - hs),
        (bx + hs - c + lean_px, by - hs),
        (bx + hs + lean_px, by - hs + c),
        (bx + hs + lean_px, by + hs - c),
        (bx + hs - c + lean_px, by + hs),
        (bx - hs + c + lean_px, by + hs),
        (bx - hs + lean_px, by + hs - c),
        (bx - hs + lean_px, by - hs + c),
    ]
    draw.polygon(body_pts, fill=BYTE_CYAN, outline=BYTE_DARK, width=2)

    # Spike on top (character landmark)
    spike_base = size // 5
    draw.polygon([
        (bx - spike_base // 2 + lean_px, by - hs),
        (bx + spike_base // 2 + lean_px, by - hs),
        (bx + lean_px, by - hs - spike_base),
    ], fill=BYTE_CYAN, outline=BYTE_DARK, width=1)

    # ── Stubby limbs ───────────────────────────────────────────
    limb_w = max(3, size // 8)
    # Arm-left
    draw.rectangle([bx - hs - limb_w + lean_px, by - size // 6,
                    bx - hs + lean_px, by + size // 6], fill=BYTE_CYAN, outline=BYTE_DARK, width=1)
    # Arm-right
    draw.rectangle([bx + hs + lean_px, by - size // 6,
                    bx + hs + limb_w + lean_px, by + size // 6], fill=BYTE_CYAN, outline=BYTE_DARK, width=1)
    # Leg-left
    draw.rectangle([bx - size // 4 + lean_px, by + hs,
                    bx - size // 8 + lean_px, by + hs + limb_w * 2], fill=BYTE_CYAN, outline=BYTE_DARK, width=1)
    # Leg-right
    draw.rectangle([bx + size // 8 + lean_px, by + hs,
                    bx + size // 4 + lean_px, by + hs + limb_w * 2], fill=BYTE_CYAN, outline=BYTE_DARK, width=1)

    # ── Eyes ───────────────────────────────────────────────────
    eye_y_off = -size // 8
    # Normal eye (left of Byte, viewer's right)
    ne_x = bx + size // 6 + lean_px
    ne_y = by + eye_y_off
    ew = max(4, size // 5)
    eh = max(3, size // 6)

    if expression == 'alarmed':
        # Wide-open (max aperture), warning triangle in cracked eye
        aperture = 1.0
    elif expression == 'processing':
        aperture = 0.7
    elif expression in ('offended', 'disgusted'):
        aperture = 0.65
    else:  # resigned / other
        aperture = 0.55

    draw.ellipse([ne_x - ew // 2, ne_y - int(eh * aperture),
                  ne_x + ew // 2, ne_y + int(eh * aperture)],
                 fill=(255, 255, 255), outline=BYTE_DARK, width=1)
    draw.ellipse([ne_x - ew // 4, ne_y - int(eh * aperture * 0.5),
                  ne_x + ew // 4, ne_y + int(eh * aperture * 0.5)],
                 fill=BYTE_DARK)

    # Cracked eye (right of Byte, viewer's left)
    ce_x = bx - size // 6 + lean_px
    ce_y = by + eye_y_off
    draw.ellipse([ce_x - ew // 2, ce_y - int(eh * aperture),
                  ce_x + ew // 2, ce_y + int(eh * aperture)],
                 fill=(220, 255, 255), outline=BYTE_DARK, width=1)
    # Crack lines
    draw.line([(ce_x - ew // 3, ce_y - int(eh * aperture * 0.8)),
               (ce_x + ew // 3, ce_y + int(eh * aperture * 0.8))],
              fill=BYTE_DARK, width=1)
    draw.line([(ce_x, ce_y - int(eh * aperture)),
               (ce_x - ew // 4, ce_y + int(eh * aperture * 0.5))],
              fill=BYTE_DARK, width=1)

    # Pixel display in cracked eye
    if expression == 'alarmed':
        # Warning triangle ⚠ in Acid Green
        cx_e, cy_e = ce_x, ce_y
        t_sz = max(3, size // 10)
        draw.polygon([
            (cx_e, cy_e - t_sz),
            (cx_e - t_sz, cy_e + t_sz // 2),
            (cx_e + t_sz, cy_e + t_sz // 2),
        ], fill=GLITCH_ACID)
        draw.rectangle([cx_e - 1, cy_e - t_sz // 3,
                        cx_e + 1, cy_e + t_sz // 2 - 2], fill=BYTE_DARK)
        draw.rectangle([cx_e - 1, cy_e + t_sz // 2 - 1,
                        cx_e + 1, cy_e + t_sz // 2], fill=BYTE_DARK)
    elif expression == 'processing':
        # Three rotating dots (cyan/magenta alternating)
        for di, (ddx, ddy) in enumerate([(-3, -2), (0, 3), (3, -2)]):
            dc = GLITCH_CYAN if di % 2 == 0 else GLITCH_MAG
            draw.rectangle([ce_x + ddx - 1, ce_y + ddy - 1,
                            ce_x + ddx + 1, ce_y + ddy + 1], fill=dc)
    elif expression == 'offended':
        # Exclamation mark
        draw.rectangle([ce_x - 1, ce_y - int(eh * 0.6),
                        ce_x + 1, ce_y + int(eh * 0.1)], fill=GLITCH_CYAN)
        draw.rectangle([ce_x - 1, ce_y + int(eh * 0.3),
                        ce_x + 1, ce_y + int(eh * 0.5)], fill=GLITCH_CYAN)
    else:
        # Resigned: flat line
        draw.line([(ce_x - ew // 3, ce_y), (ce_x + ew // 3, ce_y)],
                  fill=GLITCH_CYAN, width=1)

    # ── Mouth ──────────────────────────────────────────────────
    m_y = by + size // 6
    m_w = max(5, size // 4)
    if expression == 'alarmed':
        # Rectangle open — pixel teeth visible
        draw.rectangle([bx - m_w + lean_px, m_y - 2,
                        bx + m_w + lean_px, m_y + max(3, size // 8)],
                       fill=BYTE_DARK, outline=BYTE_DARK, width=1)
        # Pixel teeth
        for ti in range(3):
            tx = bx - m_w + 2 + ti * (m_w * 2 // 3) + lean_px
            draw.rectangle([tx, m_y - 1, tx + max(2, size // 12), m_y + 2],
                           fill=(220, 255, 255))
    elif expression in ('offended', 'disgusted'):
        # Flat grimace — horizontal, compressed
        draw.arc([bx - m_w + lean_px, m_y - 4,
                  bx + m_w + lean_px, m_y + 4],
                 start=0, end=180, fill=BYTE_DARK, width=2)
    else:
        # Neutral/resigned slight frown
        draw.arc([bx - m_w + lean_px, m_y - 3,
                  bx + m_w + lean_px, m_y + 6],
                 start=10, end=170, fill=BYTE_DARK, width=2)


def draw_luma_face(draw, cx, cy, size=80, expression='curious',
                   hair_state='normal'):
    """
    Draw Luma's face.
    expression: 'panic' | 'curious' | 'excited' | 'floor-impact' | 'reckless'
              | 'settling' | 'recognition' | 'warmth'
    hair_state: 'normal' | 'glitch-circle' | 'max-volume'
    Face placement carries emotional info (MEMORY.md Cycle 7):
      centered = neutral, lower-center = urgency/discovery
    CYCLE 9: Added 'settling' (P17), 'recognition' (P18), 'warmth' (P20)
      per Carmen's critique — three distinct emotional states need distinct faces.
    """
    r = size // 2
    # Face
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 fill=LUMA_SKIN, outline=(50, 30, 15), width=2)

    # Hair
    if hair_state == 'glitch-circle':
        # Glitch-forced PERFECT circle — deeply wrong, rendered clean
        draw.ellipse([cx - int(r * 1.5), cy - int(r * 1.5),
                      cx + int(r * 1.5), cy + int(r * 1.5)],
                     fill=LUMA_HAIR, outline=(0, 240, 255), width=2)
        # Pixel flash at transition
        for px_off in range(-6, 6, 2):
            draw.rectangle([cx + px_off, cy - int(r * 1.5) - 2,
                            cx + px_off + 2, cy - int(r * 1.5) + 2],
                           fill=GLITCH_CYAN)
    elif hair_state == 'max-volume':
        # Maximum poof — 40% extra volume, flyaways
        draw.ellipse([cx - int(r * 1.9), cy - int(r * 2.0),
                      cx + int(r * 1.9), cy + int(r * 0.4)],
                     fill=LUMA_HAIR)
        # Flyaway strands
        for fx, fy in [(-int(r * 1.9), -int(r * 0.8)),
                       (int(r * 1.7), -int(r * 0.6)),
                       (-int(r * 1.4), -int(r * 1.8)),
                       (int(r * 1.2), -int(r * 1.9))]:
            draw.ellipse([cx + fx - 6, cy + fy - 6,
                          cx + fx + 6, cy + fy + 6], fill=LUMA_HAIR)
    else:  # normal — slightly asymmetric, right-biased volume
        draw.ellipse([cx - int(r * 1.55), cy - int(r * 1.7),
                      cx + int(r * 1.7), cy + int(r * 0.3)],
                     fill=LUMA_HAIR)
        # Escaped forehead curl
        draw.ellipse([cx - int(r * 0.2) - 5, cy - r - 4,
                      cx - int(r * 0.2) + 5, cy - r + 4], fill=LUMA_HAIR)

    # Eyes
    ew, eh = max(8, r // 3), max(6, r // 4)
    eye_y = cy - r // 6

    if expression == 'panic':
        # Pupils shrunk to dots, full whites
        for ex in [cx - r // 3, cx + r // 3]:
            draw.ellipse([ex - ew // 2, eye_y - eh,
                          ex + ew // 2, eye_y + eh], fill=(255, 255, 245))
            draw.ellipse([ex - 2, eye_y - 2, ex + 2, eye_y + 2], fill=(20, 12, 8))
        # Eyebrows shot up to hairline
        draw.arc([cx - r // 2, eye_y - eh - 16,
                  cx - r // 8, eye_y - eh - 4],
                 start=200, end=340, fill=(22, 14, 8), width=3)
        draw.arc([cx + r // 8, eye_y - eh - 16,
                  cx + r // 2, eye_y - eh - 4],
                 start=200, end=340, fill=(22, 14, 8), width=3)
        # Mouth: max aperture rectangle scream
        draw.rectangle([cx - r // 3, eye_y + eh + 6,
                        cx + r // 3, eye_y + eh + 6 + r // 2],
                       fill=(25, 10, 6))

    elif expression == 'curious':
        # Squint of assessment — one eye more open
        draw.ellipse([cx - r // 3 - ew // 2, eye_y - int(eh * 0.8),
                      cx - r // 3 + ew // 2, eye_y + int(eh * 0.8)],
                     fill=(255, 255, 245))
        draw.ellipse([cx + r // 3 - ew // 2, eye_y - int(eh * 0.6),
                      cx + r // 3 + ew // 2, eye_y + int(eh * 0.6)],
                     fill=(255, 255, 245))
        draw.ellipse([cx - r // 3 - 3, eye_y - 3,
                      cx - r // 3 + 3, eye_y + 3], fill=(20, 12, 8))
        draw.ellipse([cx + r // 3 - 3, eye_y - 3,
                      cx + r // 3 + 3, eye_y + 3], fill=(20, 12, 8))
        # Focused brow
        draw.arc([cx - r // 2, eye_y - eh - 12,
                  cx - r // 8, eye_y - eh - 3],
                 start=200, end=340, fill=(22, 14, 8), width=3)
        draw.arc([cx + r // 8, eye_y - eh - 10,
                  cx + r // 2, eye_y - eh - 2],
                 start=200, end=340, fill=(22, 14, 8), width=3)
        # Slight smile — not fear, pure curiosity
        draw.arc([cx - r // 3, eye_y + eh + 5,
                  cx + r // 3, eye_y + eh + 14],
                 start=20, end=160, fill=(50, 30, 15), width=2)

    elif expression == 'reckless':
        # Maximum reckless excitement — wide grin, bright eyes
        for ex in [cx - r // 3, cx + r // 3]:
            draw.ellipse([ex - ew // 2, eye_y - int(eh * 1.1),
                          ex + ew // 2, eye_y + int(eh * 1.1)], fill=(255, 255, 245))
            # Star-shaped pupils (excitement)
            draw.ellipse([ex - 4, eye_y - 4, ex + 4, eye_y + 4], fill=(20, 12, 8))
            draw.line([(ex, eye_y - 5), (ex, eye_y + 5)], fill=(20, 12, 8), width=1)
            draw.line([(ex - 5, eye_y), (ex + 5, eye_y)], fill=(20, 12, 8), width=1)
        # Brows in extreme arc (thrilled)
        draw.arc([cx - r // 2, eye_y - eh - 18,
                  cx - r // 8, eye_y - eh - 5],
                 start=200, end=340, fill=(22, 14, 8), width=3)
        draw.arc([cx + r // 8, eye_y - eh - 18,
                  cx + r // 2, eye_y - eh - 5],
                 start=200, end=340, fill=(22, 14, 8), width=3)
        # Huge grin showing teeth
        draw.arc([cx - r // 2, eye_y + eh + 4,
                  cx + r // 2, eye_y + eh + r // 2 + 4],
                 start=15, end=165, fill=(50, 30, 15), width=3)
        draw.rectangle([cx - r // 3, eye_y + eh + 8,
                        cx + r // 3, eye_y + eh + 14], fill=(240, 235, 225))

    elif expression == 'floor-impact':
        # One eye visible (face sideways on floor), slight daze → focus
        # Only right eye visible
        ex = cx + r // 6
        draw.ellipse([ex - ew // 2, eye_y - eh,
                      ex + ew // 2, eye_y + eh], fill=(255, 255, 245))
        draw.ellipse([ex - 3, eye_y - 3, ex + 3, eye_y + 3], fill=(20, 12, 8))
        # Brow furrowing — not fear, FOCUS
        draw.arc([cx, eye_y - eh - 10, cx + r // 2, eye_y - eh - 2],
                 start=200, end=340, fill=(22, 14, 8), width=3)

    elif expression == 'excited':
        # Mid-grin — disoriented but stoked (Luma's default awakening state)
        for ex in [cx - r // 3, cx + r // 3]:
            draw.ellipse([ex - ew // 2, eye_y - int(eh * 0.9),
                          ex + ew // 2, eye_y + int(eh * 0.9)], fill=(255, 255, 245))
            draw.ellipse([ex - 3, eye_y - 3, ex + 3, eye_y + 3], fill=(20, 12, 8))
        draw.arc([cx - r // 3, eye_y + eh + 4,
                  cx + r // 3, eye_y + eh + r // 3 + 4],
                 start=20, end=160, fill=(50, 30, 15), width=2)
        # Slightly disheveled brow
        draw.arc([cx - r // 2, eye_y - eh - 12, cx - r // 8, eye_y - eh - 3],
                 start=200, end=340, fill=(22, 14, 8), width=3)
        draw.arc([cx + r // 8, eye_y - eh - 10, cx + r // 2, eye_y - eh - 2],
                 start=200, end=340, fill=(22, 14, 8), width=3)

    elif expression == 'settling':
        # P17: After the excitement high — settling into wonder looking at Byte.
        # Open mouth softly (not screaming, not closed — mid-open wonder).
        # Wide eyes. Brows raised but not alarmed — genuine wonder/awe.
        # Carmen: "the comma before the next exclamation" — soft, open, attentive.
        for ex in [cx - r // 3, cx + r // 3]:
            draw.ellipse([ex - ew // 2, eye_y - int(eh * 1.0),
                          ex + ew // 2, eye_y + int(eh * 1.0)], fill=(255, 255, 245))
            # Pupil — centered, slightly dilated (wonder)
            draw.ellipse([ex - 4, eye_y - 4, ex + 4, eye_y + 4], fill=(20, 12, 8))
        # Brows raised gently — not alarmed, not furrowed — open curiosity
        draw.arc([cx - r // 2, eye_y - eh - 16,
                  cx - r // 8, eye_y - eh - 5],
                 start=200, end=340, fill=(22, 14, 8), width=3)
        draw.arc([cx + r // 8, eye_y - eh - 14,
                  cx + r // 2, eye_y - eh - 4],
                 start=200, end=340, fill=(22, 14, 8), width=3)
        # Mouth: softly open — wonder breath, not scream rectangle
        mouth_y = eye_y + eh + 6
        draw.arc([cx - r // 4, mouth_y, cx + r // 4, mouth_y + r // 4],
                 start=20, end=160, fill=(50, 30, 15), width=2)
        # Soft open gap — small oval, not a rectangle
        draw.ellipse([cx - r // 6, mouth_y + 2, cx + r // 6, mouth_y + r // 5],
                     fill=(30, 15, 8))

    elif expression == 'recognition':
        # P18: Luma connecting what the notebook says to Byte.
        # ONE brow raised (asymmetric — the "aha" brow).
        # Eyes narrowed in CONCENTRATION — not wide, not closed.
        # Slight head-tilt implied by asymmetric brow position.
        # Left eye normal aperture, right eye slightly squinted.
        # Carmen: "recognition, not curiosity" — this is cognitive connection.
        # Left eye (viewer right) — more open (the raised-brow side)
        draw.ellipse([cx - r // 3 - ew // 2, eye_y - int(eh * 0.9),
                      cx - r // 3 + ew // 2, eye_y + int(eh * 0.9)],
                     fill=(255, 255, 245))
        draw.ellipse([cx - r // 3 - 3, eye_y - 3,
                      cx - r // 3 + 3, eye_y + 3], fill=(20, 12, 8))
        # Right eye (viewer left) — narrowed (concentration squint)
        draw.ellipse([cx + r // 3 - ew // 2, eye_y - int(eh * 0.55),
                      cx + r // 3 + ew // 2, eye_y + int(eh * 0.55)],
                     fill=(255, 255, 245))
        draw.ellipse([cx + r // 3 - 3, eye_y - 2,
                      cx + r // 3 + 3, eye_y + 2], fill=(20, 12, 8))
        # ASYMMETRIC brows: left brow raised high (the "aha!" brow)
        draw.arc([cx - r // 2, eye_y - eh - 18,
                  cx - r // 8, eye_y - eh - 6],
                 start=200, end=340, fill=(22, 14, 8), width=3)
        # Right brow lower, slightly furrowed inward (concentration)
        draw.arc([cx + r // 8, eye_y - eh - 10,
                  cx + r // 2, eye_y - eh - 4],
                 start=210, end=340, fill=(22, 14, 8), width=3)
        # Mouth: slight pursed — thinking, not smiling or open
        draw.arc([cx - r // 4, eye_y + eh + 6,
                  cx + r // 4, eye_y + eh + 12],
                 start=15, end=165, fill=(50, 30, 15), width=2)

    elif expression == 'warmth':
        # P20: First feeling of connection with Byte — choosing warmth deliberately.
        # Soft smile — genuine, not excited grin. Eyes slightly narrowed in warmth.
        # Brows gently raised — not alarmed, not furrowed — open and present.
        # Carmen: "She is choosing warmth deliberately" — this is emotional intent.
        for ex in [cx - r // 3, cx + r // 3]:
            # Eyes slightly narrowed (warmth squint — happiness closes eyes a little)
            draw.ellipse([ex - ew // 2, eye_y - int(eh * 0.7),
                          ex + ew // 2, eye_y + int(eh * 0.7)], fill=(255, 255, 245))
            draw.ellipse([ex - 3, eye_y - 3, ex + 3, eye_y + 3], fill=(20, 12, 8))
        # Brows gently raised — peaceful, not tense
        draw.arc([cx - r // 2, eye_y - eh - 13,
                  cx - r // 8, eye_y - eh - 4],
                 start=200, end=330, fill=(22, 14, 8), width=2)
        draw.arc([cx + r // 8, eye_y - eh - 12,
                  cx + r // 2, eye_y - eh - 3],
                 start=210, end=340, fill=(22, 14, 8), width=2)
        # Soft smile — NOT a grin. Gentle curve, no teeth, corners lifted.
        draw.arc([cx - r // 3, eye_y + eh + 6,
                  cx + r // 3, eye_y + eh + r // 3 + 2],
                 start=15, end=165, fill=(50, 30, 15), width=3)
        # Slight cheek lift lines (warmth crinkle)
        draw.line([(cx - r // 3 - 2, eye_y + eh - 2),
                   (cx - r // 2 - 4, eye_y + eh + 8)],
                  fill=(180, 110, 70), width=1)
        draw.line([(cx + r // 3 + 2, eye_y + eh - 2),
                   (cx + r // 2 + 4, eye_y + eh + 8)],
                  fill=(180, 110, 70), width=1)

    # Chip crumb on cheek (character detail from script)
    draw.rectangle([cx + int(r * 0.55) - 2, cy + int(r * 0.25) - 2,
                    cx + int(r * 0.55) + 2, cy + int(r * 0.25) + 2],
                   fill=(255, 140, 20))


# ── Panel drawing functions ────────────────────────────────────────────────────

def draw_p14(draw, img, font, font_bold, font_ann):
    """P14: Byte ricocheting off bookshelf. Multi-exposure trajectory.
    Fixed camera at 5ft, Dutch 12° CW, bookshelf fills right half.
    Three ghost positions: approach (cyan), impact (magenta), exit (white-cyan).
    CYCLE 9 FIX: Dutch tilt now applied as true canvas rotation (12°) via
    apply_dutch_tilt() in make_panel — not a sloped floor polygon.
    Per Carmen: geometry must deliver the angle the annotation states."""
    # Room — warm dark, glitch light strobing from off-frame monitors
    draw.rectangle([0, 0, PW, DRAW_H], fill=(20, 14, 8))

    # Floor (FLAT — the 12° tilt is applied at canvas level after draw)
    floor_y = int(DRAW_H * 0.74)
    draw.polygon([
        (0, floor_y), (PW, floor_y),
        (PW, DRAW_H), (0, DRAW_H)
    ], fill=FLOOR_DARK)
    draw.line([(0, floor_y), (PW, floor_y)], fill=(35, 24, 14), width=1)

    # Glitch light (off-frame monitors, left side) — warm chaotic strobing
    for i in range(5):
        intensity = max(0, 45 - i * 8)
        draw.polygon([(0, 0), (i * 22 + 30, 0), (i * 10, DRAW_H), (0, DRAW_H)],
                     fill=(0, intensity, intensity + 15))

    # --- BOOKSHELF (right half — starts at 43% to properly fill right half of frame) ---
    shelf_x = int(PW * 0.43)
    shelf_top = int(DRAW_H * 0.05)
    shelf_bot = floor_y - 2
    draw.rectangle([shelf_x, shelf_top, PW - 5, shelf_bot], fill=SHELF_WARM,
                   outline=(60, 42, 24), width=2)
    # Shelf planks (3 levels)
    for level in [0.30, 0.55, 0.78]:
        sy = shelf_top + int((shelf_bot - shelf_top) * level)
        draw.rectangle([shelf_x, sy - 3, PW - 5, sy], fill=(60, 40, 20))
    # Books on shelves
    book_colors = [(140, 60, 30), (60, 100, 80), (180, 120, 40),
                   (80, 60, 120), (160, 80, 50)]
    for bi, bc in enumerate(book_colors):
        bx_b = shelf_x + 8 + bi * 18
        b_shelf_y = shelf_top + int((shelf_bot - shelf_top) * 0.55) - 22
        draw.rectangle([bx_b, b_shelf_y, bx_b + 14, b_shelf_y + 22], fill=bc)
    # "DO NOT RECORD OVER" VHS on middle shelf
    vhs_x = shelf_x + 10
    vhs_y = shelf_top + int((shelf_bot - shelf_top) * 0.30) - 16
    draw.rectangle([vhs_x, vhs_y, vhs_x + 55, vhs_y + 12], fill=(25, 20, 15),
                   outline=(50, 40, 30), width=1)
    draw.text((vhs_x + 2, vhs_y + 2), "DO NOT RECORD", fill=(180, 160, 120), font=font_ann)

    # Ceiling fan (upper left, partially visible, spinning backward)
    fan_cx, fan_cy = int(PW * 0.22), int(DRAW_H * 0.08)
    draw.ellipse([fan_cx - 10, fan_cy - 4, fan_cx + 10, fan_cy + 4],
                 fill=(45, 35, 22), outline=(60, 48, 30), width=1)
    for fan_angle in [0, 90, 180, 270]:
        rad = math.radians(fan_angle + 15)  # +15° = wrong direction (backward spin)
        blade_len = 28
        fx = fan_cx + int(blade_len * math.cos(rad))
        fy = fan_cy + int(blade_len * math.sin(rad))
        draw.line([(fan_cx, fan_cy), (fx, fy)], fill=(55, 42, 26), width=5)
        # Backward-spin smear (MEMORY.md: glitch FX visible, not just described)
        draw.line([(fan_cx, fan_cy), (fx - 4, fy + 4)],
                  fill=(0, 180, 200), width=1)

    # --- BYTE MULTI-EXPOSURE TRAJECTORY ---
    # Entry (approach from lower-left): cyan
    entry_bx, entry_by = int(PW * 0.18), int(DRAW_H * 0.65)
    impact_bx, impact_by = int(PW * 0.66), int(DRAW_H * 0.44)
    exit_bx,  exit_by   = int(PW * 0.30), int(DRAW_H * 0.20)

    # PIXEL TRAIL — trajectory path (thickens toward impact per velocity profile)
    # Entry smear (cyan, thin)
    for t in range(8):
        tx = entry_bx + t * (impact_bx - entry_bx) // 9
        ty = entry_by + t * (impact_by - entry_by) // 9
        draw.ellipse([tx - 5, ty - 3, tx + 5, ty + 3],
                     fill=(0, max(0, 240 - t * 10), max(0, 255 - t * 8)))
    # Impact starburst (magenta — energy spike)
    for star_r in range(18, 4, -4):
        draw.ellipse([impact_bx - star_r, impact_by - star_r,
                      impact_bx + star_r, impact_by + star_r],
                     outline=GLITCH_MAG, width=1)
    # Exit smear (white-cyan, thicker — 20% acceleration post-impact)
    for t in range(9):
        tx = impact_bx + t * (exit_bx - impact_bx) // 10
        ty = impact_by + t * (exit_by - impact_by) // 10
        smear_w = 7 + t  # trail thickens (acceleration visible)
        draw.ellipse([tx - smear_w, ty - smear_w // 2,
                      tx + smear_w, ty + smear_w // 2],
                     fill=(min(255, 100 + t * 20), 255, 255))

    # Ghost 1: mid-approach (CYAN body, limbs forward)
    draw_byte_body(draw, entry_bx + 20, entry_by,
                   size=32, expression='alarmed', lean_deg=-15, trail=False)
    # Ghost 2: at impact (MAGENTA tint, body compressed — squash)
    draw.rectangle([impact_bx - 22, impact_by - 10,
                    impact_bx + 22, impact_by + 10],
                   fill=GLITCH_MAG, outline=(180, 0, 140), width=2)
    # Ghost 3: bouncing off (white-cyan, limbs behind)
    draw_byte_body(draw, exit_bx - 10, exit_by + 12,
                   size=32, expression='alarmed', lean_deg=20, trail=False)

    # Airborne books (3, from impact point)
    for bi, (boffx, boffy, bc) in enumerate([
        (30, -20, (140, 60, 30)),
        (48, -12, (60, 100, 80)),
        (62, -28, (180, 120, 40)),
    ]):
        bxb = impact_bx + boffx
        byb = impact_by + boffy
        # Tumbling book (rotated rectangle via polygon)
        angle = 20 + bi * 35
        rad = math.radians(angle)
        bw, bh = 12, 18
        corners = [(bxb + bw * math.cos(rad) - bh * math.sin(rad),
                    byb + bw * math.sin(rad) + bh * math.cos(rad)),
                   (bxb - bw * math.cos(rad) - bh * math.sin(rad),
                    byb - bw * math.sin(rad) + bh * math.cos(rad)),
                   (bxb - bw * math.cos(rad) + bh * math.sin(rad),
                    byb - bw * math.sin(rad) - bh * math.cos(rad)),
                   (bxb + bw * math.cos(rad) + bh * math.sin(rad),
                    byb + bw * math.sin(rad) - bh * math.cos(rad))]
        draw.polygon(corners, fill=bc, outline=(20, 12, 6), width=1)

    # Rubber duck (mid-flight, upper center)
    duck_x, duck_y = int(PW * 0.42), int(DRAW_H * 0.28)
    draw.ellipse([duck_x - 10, duck_y - 8, duck_x + 10, duck_y + 8],
                 fill=(255, 200, 30), outline=(200, 140, 10), width=2)
    draw.ellipse([duck_x + 4, duck_y - 12, duck_x + 16, duck_y - 4],
                 fill=(255, 200, 30), outline=(200, 140, 10), width=1)
    # Bill
    draw.polygon([(duck_x + 14, duck_y - 9), (duck_x + 20, duck_y - 7),
                  (duck_x + 14, duck_y - 5)], fill=(255, 160, 0))

    # Pixel confetti at impact and exit (visible FX per MEMORY.md)
    add_pixel_confetti(draw, (impact_bx - 25, impact_bx + 40),
                       (impact_by - 30, impact_by + 20), 30, seed=14)
    add_pixel_confetti(draw, (0, PW // 3), (0, int(DRAW_H * 0.6)), 20, seed=141)

    # Camera angle annotation (tilt applied via canvas rotation — geometry delivers 12°)
    draw.text((4, DRAW_H - 14), "DUTCH 12° CW — canvas rotated — fixed camera",
              fill=(120, 110, 90), font=font_ann)


def draw_p15(draw, img, font, font_bold, font_ann):
    """P15: Luma in freefall from couch. GLITCH-FORCED HAIR SYMMETRY (8-frame gag).
    Floor-level camera, downward-looming impact shot. Notebook spiraling.
    KEY VISUAL: Hair has been corrected to a PERFECT CIRCLE — deeply wrong, cleanly rendered."""
    draw.rectangle([0, 0, PW, DRAW_H], fill=(18, 12, 8))

    # Floor — close up (we're at floor level looking UP)
    floor_y = int(DRAW_H * 0.82)
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(14, 10, 6))
    draw.line([(0, floor_y), (PW, floor_y)], fill=(30, 20, 12), width=1)

    # Pixel confetti ring on floor — excited about the incoming collision
    # (Compositional anchor: lower-center)
    ring_cx, ring_cy = PW // 2, floor_y + 4
    for r in range(55, 5, -10):
        intensity = max(0, 60 - r)
        draw.ellipse([ring_cx - r * 2, ring_cy - r // 2,
                      ring_cx + r * 2, ring_cy + r // 2],
                     outline=(0, intensity + 100, intensity + 140), width=1)
    add_pixel_confetti(draw, (ring_cx - 55, ring_cx + 55),
                       (floor_y - 10, floor_y + 8), 35, seed=15)

    # Background: monitor glow + chaos (she's falling through the peak glitch field)
    for i in range(4):
        gx = i * (PW // 4) + PW // 8
        for gr in [28, 18, 10]:
            a_col = max(0, 60 - gr * 2)
            draw.ellipse([gx - gr * 2, 0, gx + gr * 2, gr * 2],
                         fill=(0, a_col, a_col + 10))

    # Luma in freefall — PHYSICAL SURPRISE read before you see the face
    # CYCLE 10 FIX (Carmen): Body language tells the story.
    # - Torso SQUASH: compressed height (impact anticipation physics)
    # - Head tilted BACK (startled — chin up, neck extended)
    # - LEFT arm raised DEFENSIVELY (high — elbow up, wrist above head level)
    # - RIGHT arm lower, angled out (asymmetry = uncontrolled reaction)
    # - RIGHT leg pulled up, KNEE TO CHEST (fetal reflex, physical shock)
    # - LEFT leg extends downward (asymmetric — one grounded reflex, one tuck)
    luma_cx = PW // 2 - 5
    luma_cy = int(DRAW_H * 0.36)

    # Body — SQUASHED: tall compressed to wide. Torso squash = height ~60% of normal.
    # Wide + short ellipse communicates impact compression instantly.
    body_top = luma_cy - 12   # compressed — less vertical height than normal
    body_bot = luma_cy + 26   # compressed bottom — total height ~38px vs normal 46px
    draw.ellipse([luma_cx - 34, body_top, luma_cx + 34, body_bot],
                 fill=LUMA_PJ, outline=(100, 150, 120), width=2)
    # Squash annotation
    draw.line([(luma_cx + 36, body_top), (luma_cx + 46, body_top)],
              fill=(0, 180, 200), width=1)
    draw.line([(luma_cx + 36, body_bot), (luma_cx + 46, body_bot)],
              fill=(0, 180, 200), width=1)
    draw.line([(luma_cx + 41, body_top), (luma_cx + 41, body_bot)],
              fill=(0, 180, 200), width=1)
    draw.text((luma_cx + 48, luma_cy - 6), "SQUASH",
              fill=(0, 180, 200), font=font_ann)

    # LEFT ARM — raised DEFENSIVELY HIGH (elbow up, wrist above head)
    # Bent arm: shoulder → elbow goes up-left, elbow → wrist curls toward face
    draw.line([(luma_cx - 12, body_top + 8), (luma_cx - 42, body_top - 28)],
              fill=LUMA_SKIN, width=6)   # upper arm: angled up-left steeply
    draw.line([(luma_cx - 42, body_top - 28), (luma_cx - 28, body_top - 42)],
              fill=LUMA_SKIN, width=6)   # forearm: curls inward (defensive guard)

    # RIGHT ARM — lower, flung outward (uncontrolled, asymmetric)
    # CYCLE 12 FIX (Carmen Cycle 11 brief): endpoint moved from body_top+18 to body_top+10
    # for true horizontal read. 8px elevation drop over ~42px horizontal = ~11° below H.
    # Bringing endpoint UP 8px achieves near-perfect horizontal exit trajectory.
    draw.line([(luma_cx + 10, body_top + 10), (luma_cx + 52, body_top + 10)],
              fill=LUMA_SKIN, width=6)

    # RIGHT LEG — KNEE TO CHEST (fetal/shock reflex — pulled tight)
    # Thigh goes up-right, shin folds back under
    draw.line([(luma_cx + 8, body_bot), (luma_cx + 32, body_bot - 18)],
              fill=LUMA_SKIN, width=6)   # thigh pulled up
    draw.line([(luma_cx + 32, body_bot - 18), (luma_cx + 18, body_bot + 8)],
              fill=LUMA_SKIN, width=6)   # shin folded back (knee to chest geometry)

    # LEFT LEG — extends downward (asymmetric — other leg kicks out)
    draw.line([(luma_cx - 8, body_bot), (luma_cx - 32, body_bot + 36)],
              fill=LUMA_SKIN, width=6)

    # Face — head TILTED BACK (startled — chin up, neck visible below face)
    # Shift face slightly up and back to show head-tilt, neck exposed
    draw_luma_face(draw, luma_cx - 4, body_top - 30, size=46,
                   expression='panic', hair_state='glitch-circle')
    # Tilt annotation
    draw.text((luma_cx - 62, body_top - 38), "HEAD BACK",
              fill=(0, 200, 220), font=font_ann)

    # GLITCH-FORCED HAIR SYMMETRY annotation (storyboard note — the visual gag)
    # The perfect circle is already drawn by draw_luma_face with hair_state='glitch-circle'
    # Annotation arrow
    ann_x, ann_y = luma_cx + 58, body_top - 42
    draw.line([(ann_x, ann_y), (luma_cx + 26, body_top - 48)],
              fill=(0, 200, 220), width=1)
    draw.text((ann_x + 2, ann_y - 10), "GLITCH OVERRIDES",
              fill=(0, 200, 220), font=font_ann)
    draw.text((ann_x + 2, ann_y), "HAIR — 8 FRAMES",
              fill=(0, 200, 220), font=font_ann)

    # Airborne couch cushion (falling parallel to Luma)
    draw.rectangle([int(PW * 0.08), int(DRAW_H * 0.38),
                    int(PW * 0.24), int(DRAW_H * 0.54)],
                   fill=(130, 90, 55), outline=(90, 60, 35), width=2)

    # Notebook spiraling (pages fluttering)
    nb_x, nb_y = int(PW * 0.70), int(DRAW_H * 0.42)
    # Rotated notebook via polygon
    for page in range(3):
        ang = math.radians(30 + page * 20)
        pts = [(nb_x + 25 * math.cos(ang + t * math.pi / 2),
                nb_y + 18 * math.sin(ang + t * math.pi / 2)) for t in range(4)]
        draw.polygon(pts, fill=(235, 225, 190) if page < 2 else (200, 190, 150),
                     outline=(80, 70, 50), width=1)
    draw.text((nb_x - 12, nb_y - 6), "HISTORY", fill=(80, 70, 50), font=font_ann)
    draw.text((nb_x - 12, nb_y + 2), "OF THE", fill=(80, 70, 50), font=font_ann)

    # Pixel confetti through whole frame (she's in peak glitch zone)
    add_pixel_confetti(draw, (0, PW), (0, int(DRAW_H * 0.75)), 40, seed=15,
                       colors=[GLITCH_CYAN, GLITCH_MAG, (255, 220, 60)])

    # Camera angle note
    draw.text((4, DRAW_H - 14), "FLOOR LEVEL — looking up — impact incoming",
              fill=(120, 110, 90), font=font_ann)


def draw_p16(draw, img, font, font_bold, font_ann):
    """P16: ECU — Luma's face pressed against floor, one eye visible.
    Camera at floor level, perfectly horizontal. Eye begins to TRACK — then FOCUS.
    Expression shifts: daze → not fear → FOCUS. Caption quote: '...WHAT.'"""
    draw.rectangle([0, 0, PW, DRAW_H], fill=(10, 7, 4))

    # Floor surface (fills lower half — she's flat on it)
    floor_y = DRAW_H // 2
    # Textured floor — warm grain
    for gy in range(floor_y, DRAW_H, 3):
        noise = random.Random(gy + 16).randint(0, 8)
        draw.rectangle([0, gy, PW, gy + 2], fill=(14 + noise, 10 + noise // 2, 6 + noise // 3))

    # Chip crumb fallen to floor (small, dry, loud — the FIRST SOUND)
    chip_x, chip_y = PW // 2 + 30, floor_y + 8
    draw.rectangle([chip_x - 4, chip_y - 4, chip_x + 4, chip_y + 4],
                   fill=(255, 140, 20), outline=(200, 100, 10), width=1)
    draw.text((chip_x + 6, chip_y - 6), "tik", fill=(120, 110, 90), font=font_ann)

    # Background: chaos still happening (defocused — Byte trails, falling books)
    # Soft glow smears in upper half (blurry background activity)
    for smear_x, smear_col in [
        (PW // 5, GLITCH_CYAN), (PW * 2 // 5, GLITCH_MAG),
        (PW * 3 // 4, GLITCH_CYAN)
    ]:
        for sr in range(30, 5, -6):
            alpha_v = max(0, 50 - sr * 2)
            draw.ellipse([smear_x - sr * 2, 8, smear_x + sr * 2, floor_y - 8],
                         fill=(smear_col[0] * alpha_v // 100,
                               smear_col[1] * alpha_v // 100,
                               smear_col[2] * alpha_v // 100))

    # Luma's face pressed flat on floor — profile/partial, face horizontal
    # Only the RIGHT EYE is fully visible (huge — fills lower portion of frame)
    # Lower-center is the compositional anchor
    face_cx = PW // 2 - 30
    face_cy = floor_y - 20

    # Face surface (cheek flat against floor)
    draw.ellipse([face_cx - 65, face_cy - 25,
                  face_cx + 65, face_cy + 25], fill=LUMA_SKIN)

    # Hair spilling across floor (dark mass, left side)
    draw.ellipse([face_cx - 130, face_cy - 30,
                  face_cx - 10, face_cy + 20], fill=LUMA_HAIR)

    # THE EYE — enormous, lower-center frame anchor, FOCUS building
    eye_cx = face_cx + 20
    eye_cy = face_cy - 5
    eye_rx, eye_ry = 44, 28
    # White sclera
    draw.ellipse([eye_cx - eye_rx, eye_cy - eye_ry,
                  eye_cx + eye_rx, eye_cy + eye_ry],
                 fill=(250, 248, 240), outline=(50, 30, 15), width=2)
    # Iris (warm amber-brown — Luma's eye color)
    draw.ellipse([eye_cx - eye_rx // 2, eye_cy - eye_ry // 2,
                  eye_cx + eye_rx // 2, eye_cy + eye_ry // 2],
                 fill=(120, 72, 30))
    # Pupil
    draw.ellipse([eye_cx - eye_rx // 5, eye_cy - eye_ry // 4,
                  eye_cx + eye_rx // 5, eye_cy + eye_ry // 4],
                 fill=(15, 8, 4))
    # Eye reflection — cyan glitch light from the chaos above
    draw.ellipse([eye_cx + 8, eye_cy - eye_ry // 3,
                  eye_cx + 18, eye_cy - eye_ry // 6],
                 fill=(200, 245, 255))

    # FOCUS LINE from pupil (gaze direction arrow — the eye has found something)
    focus_end_x = PW - 20
    focus_end_y = int(floor_y * 0.35)
    draw.line([(eye_cx + eye_rx, eye_cy),
               (focus_end_x, focus_end_y)],
              fill=(180, 165, 130), width=1)
    draw.ellipse([focus_end_x - 4, focus_end_y - 4,
                  focus_end_x + 4, focus_end_y + 4],
                 fill=(180, 165, 130))

    # Brow (just above eye, barely visible — furrowing toward FOCUS not fear)
    draw.arc([eye_cx - eye_rx + 5, eye_cy - eye_ry - 18,
              eye_cx + eye_rx - 5, eye_cy - eye_ry - 4],
             start=200, end=340, fill=(22, 14, 8), width=4)

    # Chip crumb on cheek (character detail — still there)
    draw.rectangle([face_cx + 35, face_cy + 2,
                    face_cx + 41, face_cy + 8], fill=(255, 140, 20))

    # Pixel confetti above (background chaos, fading down)
    add_pixel_confetti(draw, (0, PW), (0, floor_y - 15), 25, seed=16)

    # Camera annotation
    draw.text((4, DRAW_H - 14), "ECU FLOOR — camera perfectly horizontal",
              fill=(120, 110, 90), font=font_ann)


def draw_p17(draw, img, font, font_bold, font_ann):
    """P17: MED two-shot — Luma sitting up, Byte hovering. THE QUIET BEAT.
    Chaos has paused. Notebook in Luma's lap. A chip falls between them.
    Both watching it fall. This is the comma before the next exclamation.
    Camera: eye level, clean room space, monitors all showing glitch in background."""
    draw.rectangle([0, 0, PW, DRAW_H], fill=(22, 16, 10))

    # Room: two-point perspective (MEMORY.md: non-negotiable for 3/4 interior)
    # Left VP approx at (-200, DRAW_H//2), right VP at (680, DRAW_H//3)
    floor_y = int(DRAW_H * 0.74)
    # Back wall
    back_wall_y = int(DRAW_H * 0.22)
    draw.rectangle([0, back_wall_y, PW, floor_y], fill=(28, 20, 12))
    draw.line([(0, back_wall_y), (PW, back_wall_y)], fill=(42, 28, 16), width=1)

    # Room corner (left VP side) — perspective line
    corner_x = int(PW * 0.32)
    draw.line([(corner_x, back_wall_y), (0, floor_y)], fill=(38, 26, 14), width=1)
    draw.rectangle([0, back_wall_y, corner_x, floor_y], fill=(25, 17, 10))

    # Floor
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=FLOOR_DARK)
    draw.line([(0, floor_y), (PW, floor_y)], fill=(32, 22, 12), width=1)

    # MONITORS ON BACK WALL — all showing glitch imagery (chaos continues)
    monitor_configs = [
        (55, back_wall_y + 5, 80, 50, (0, 30, 40)),    # Byte tiled face
        (185, back_wall_y + 8, 90, 55, (30, 0, 30)),    # white static overload
        (330, back_wall_y + 6, 75, 48, (0, 20, 35)),    # raw scrolling code
    ]
    for mx, my, mw, mh, glitch_fill in monitor_configs:
        draw.rectangle([mx, my, mx + mw, my + mh], fill=(12, 10, 18),
                       outline=(35, 28, 45), width=2)
        draw.rectangle([mx + 3, my + 3, mx + mw - 3, my + mh - 3], fill=glitch_fill)
        # Scan line pattern (glitch texture, visible not just described)
        for sl in range(my + 4, my + mh - 4, 4):
            draw.line([(mx + 3, sl), (mx + mw - 3, sl)],
                      fill=(0, min(255, glitch_fill[1] + 40),
                            min(255, glitch_fill[2] + 60)), width=1)

    # Scattered books/chips on floor
    for ox, oy, oc in [(40, floor_y - 8, (80, 55, 35)),
                       (90, floor_y - 5, (60, 90, 70)),
                       (350, floor_y - 6, (140, 55, 25))]:
        draw.rectangle([ox, oy, ox + 14, oy + 4], fill=oc)

    # LUMA — sitting cross-legged on floor, left of center
    # Lower-center = anchor (MEMORY.md lesson: urgency/discovery)
    luma_cx = int(PW * 0.32)
    luma_cy = int(DRAW_H * 0.58)

    # Cross-legged body (simplified)
    # Torso
    draw.rectangle([luma_cx - 20, luma_cy - 35, luma_cx + 20, luma_cy + 5],
                   fill=LUMA_PJ, outline=(100, 150, 120), width=1)
    # Crossed legs (X shape)
    draw.polygon([(luma_cx - 35, luma_cy + 5), (luma_cx, luma_cy + 5),
                  (luma_cx + 10, floor_y - 2), (luma_cx - 45, floor_y - 2)],
                 fill=(100, 68, 45))
    draw.polygon([(luma_cx + 35, luma_cy + 5), (luma_cx, luma_cy + 5),
                  (luma_cx - 10, floor_y - 2), (luma_cx + 45, floor_y - 2)],
                 fill=(100, 68, 45))

    # Notebook in lap
    draw.rectangle([luma_cx - 28, luma_cy + 2, luma_cx + 28, luma_cy + 16],
                   fill=(235, 225, 195), outline=(80, 70, 50), width=1)
    draw.text((luma_cx - 26, luma_cy + 4), "HISTORY OF THE INTERNET",
              fill=(80, 70, 50), font=font_ann)

    # Face — SETTLING expression (not curious — she has settled from panic into wonder)
    # P17: After the excitement high. She's looking at Byte with open-mouthed wonder.
    # Carmen: wide eyes, brows raised, mouth softly open — the comma before the exclamation.
    draw_luma_face(draw, luma_cx + 2, luma_cy - 62, size=44,
                   expression='settling', hair_state='normal')

    # BYTE — floating at chest height to Luma, center of room
    # CYCLE 9 FIX: Expression 'resigned' not 'alarmed' — quiet beat, not alarm beat.
    # Carmen: 'alarmed' at maximum during chip-landing undercuts the silence.
    byte_cx = int(PW * 0.60)
    byte_cy = int(DRAW_H * 0.44)
    draw_byte_body(draw, byte_cx, byte_cy, size=48,
                   expression='resigned', lean_deg=0, trail=False)
    # "Breathing" chest indicator — does he breathe? chest going up/down
    draw.arc([byte_cx - 12, byte_cy - 10, byte_cx + 12, byte_cy + 6],
             start=0, end=180, fill=(0, 180, 200), width=2)

    # THE CHIP — falling between them (lower-center, the one quiet sound)
    chip_x = int(PW * 0.48)
    chip_y = int(DRAW_H * 0.62)
    draw.rectangle([chip_x - 4, chip_y - 4, chip_x + 4, chip_y + 4],
                   fill=(255, 140, 20), outline=(200, 100, 10), width=1)
    # Motion line — chip descending slowly
    draw.line([(chip_x, chip_y - 12), (chip_x, chip_y - 5)],
              fill=(180, 160, 120), width=1)

    # Pixel confetti drifting slowly (settling, not erupting)
    add_pixel_confetti(draw, (0, PW), (back_wall_y, floor_y), 25, seed=17)

    # Camera annotation
    draw.text((4, DRAW_H - 14), "MED — eye level — quiet beat — chaos paused",
              fill=(120, 110, 90), font=font_ann)


def draw_p18(draw, img, font, font_bold, font_ann):
    """P18: MED — Luma's curiosity fully activates. Notebook turn.
    She taps her HISTORY OF THE INTERNET page — shows Byte the doodles.
    Her margin drawings look suspiciously like him. Something is clicking in her brain.
    MCU, slight low angle, empowered framing."""
    draw.rectangle([0, 0, PW, DRAW_H], fill=(22, 16, 10))

    # Room (simplified — focus is on Luma and notebook)
    floor_y = int(DRAW_H * 0.78)
    draw.rectangle([0, int(DRAW_H * 0.20), PW, floor_y], fill=(26, 18, 11))
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=FLOOR_DARK)
    draw.line([(0, floor_y), (PW, floor_y)], fill=(32, 22, 12), width=1)

    # Monitor glow (background, all still blazing)
    for mg_x in [60, 210, 370]:
        for gr in [22, 15, 8]:
            draw.ellipse([mg_x - gr * 3, int(DRAW_H * 0.20),
                          mg_x + gr * 3, int(DRAW_H * 0.20) + gr * 2],
                         fill=(0, max(0, 35 - gr), max(0, 50 - gr)))

    # LUMA — sitting, MCU, slight low angle — lower-center placement (urgency)
    # The face is the story; notebook being turned is the action
    luma_cx = int(PW * 0.38)
    luma_cy = int(DRAW_H * 0.55)

    # Torso (just lower portion visible in MCU)
    draw.rectangle([luma_cx - 22, luma_cy + 5, luma_cx + 22, floor_y - 2],
                   fill=LUMA_PJ, outline=(100, 150, 120), width=1)

    # Arm — gesturing (pointing at notebook, then at Byte off-frame right)
    # Left arm pointing down at notebook
    draw.line([(luma_cx - 10, luma_cy + 8), (luma_cx - 30, luma_cy + 35)],
              fill=LUMA_SKIN, width=6)
    # Right arm pointing right (toward Byte)
    draw.line([(luma_cx + 10, luma_cy + 8), (luma_cx + 65, luma_cy + 15)],
              fill=LUMA_SKIN, width=6)

    # Notebook held up / turned toward Byte
    nb_cx = luma_cx - 8
    nb_cy = luma_cy + 42
    draw.rectangle([nb_cx - 35, nb_cy - 22, nb_cx + 35, nb_cy + 22],
                   fill=(235, 225, 195), outline=(80, 70, 50), width=2)

    # Title text on notebook page
    try:
        font_nb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 7)
    except Exception:
        font_nb = font_ann
    draw.text((nb_cx - 33, nb_cy - 20), "HISTORY OF THE INTERNET", fill=(60, 50, 35), font=font_nb)
    draw.text((nb_cx - 33, nb_cy - 14), "MRS. OKAFOR — DUE FRIDAY", fill=(60, 50, 35), font=font_nb)

    # MARGIN DOODLES — small Byte-like glitch creatures (character insight)
    # These look suspiciously like Byte
    for doodle_x, doodle_y in [(nb_cx - 28, nb_cy - 6),
                                (nb_cx - 20, nb_cy + 6),
                                (nb_cx + 18, nb_cy - 8)]:
        # Tiny glitchkin shape in margin
        draw.rectangle([doodle_x - 4, doodle_y - 5, doodle_x + 4, doodle_y + 5],
                       fill=(0, 200, 220), outline=(0, 140, 160), width=1)
        draw.rectangle([doodle_x - 2, doodle_y - 3, doodle_x, doodle_y],
                       fill=(255, 255, 200))  # tiny eye

    # "what if a computer had feelings???" label
    draw.text((nb_cx - 30, nb_cy + 10), "what if a computer", fill=(80, 65, 45), font=font_nb)
    draw.text((nb_cx - 30, nb_cy + 17), "had FEELINGS???", fill=(80, 65, 45), font=font_nb)

    # Face — RECOGNITION expression (not curious — she is connecting notebook to Byte)
    # P18: Luma realizes she has been drawing Glitchkin in her margins.
    # Carmen: "recognition, not curiosity" — cognitive connection. One brow raised,
    # eyes narrowed in concentration, asymmetric aha-moment expression.
    draw_luma_face(draw, luma_cx + 2, luma_cy - 55, size=48,
                   expression='recognition', hair_state='normal')

    # Byte (off-frame right, just barely visible as sliver — his POV implied)
    draw.rectangle([PW - 8, int(DRAW_H * 0.32), PW - 2, int(DRAW_H * 0.56)],
                   fill=BYTE_CYAN, outline=BYTE_DARK, width=1)

    # Pixel confetti (settling, sparse)
    add_pixel_confetti(draw, (0, PW), (0, floor_y - 10), 18, seed=18)

    # Camera annotation
    draw.text((4, DRAW_H - 14), "MED — slight low angle — curiosity activates",
              fill=(120, 110, 90), font=font_ann)


def draw_p19(draw, img, font, font_bold, font_ann):
    """P19: CU — Byte's face. CHARACTER MOMENT.
    Reaction to being called 'a dead pixel.' Expression cascade:
    indignation → grudging acknowledgment → indignation → resignation.
    Caption: 'The preferred term is Glitchkin.'"""
    draw.rectangle([0, 0, PW, DRAW_H], fill=(14, 10, 18))

    # Background — abstract scan-lines (we're in Byte's space)
    for sl in range(0, DRAW_H, 5):
        brightness = 12 + (sl % 10) * 2
        draw.line([(0, sl), (PW, sl)], fill=(0, brightness, brightness + 8), width=2)

    # Pixel confetti stabilized to slow drift (chaos settling)
    add_pixel_confetti(draw, (0, PW), (0, DRAW_H), 22, seed=19,
                       colors=[(0, 180, 200), (180, 0, 160), (200, 240, 200)])

    # BYTE — large, center-frame, character owns the shot
    # Per MEMORY.md Cycle 7: character must OWN frame on CU. Size 90px.
    byte_cx = PW // 2 - 5
    byte_cy = int(DRAW_H * 0.47)
    byte_size = 90

    # Background glow (Byte radiates) — additive, not dark overlay
    for gr in range(60, 8, -10):
        gc = max(0, 80 - gr)
        draw.ellipse([byte_cx - gr * 2, byte_cy - gr,
                      byte_cx + gr * 2, byte_cy + gr],
                     fill=(0, gc, gc + 8))

    draw_byte_body(draw, byte_cx, byte_cy, size=byte_size,
                   expression='offended', lean_deg=0, trail=False)

    # Tiny arms CROSSING (he's crossed his arms — injured dignity)
    arm_y = byte_cy + byte_size // 8
    # Cross-arm lines over body
    draw.line([(byte_cx - byte_size // 2, arm_y),
               (byte_cx + byte_size // 4, arm_y + 8)],
              fill=BYTE_DARK, width=3)
    draw.line([(byte_cx + byte_size // 2, arm_y),
               (byte_cx - byte_size // 4, arm_y + 8)],
              fill=BYTE_DARK, width=3)

    # One finger raised (about to make a point, then puts it down)
    finger_x = byte_cx + byte_size // 2 + 12
    finger_y = byte_cy - byte_size // 4
    draw.line([(byte_cx + byte_size // 2, arm_y),
               (finger_x, finger_y)], fill=BYTE_CYAN, width=5)
    draw.ellipse([finger_x - 4, finger_y - 6, finger_x + 4, finger_y + 2],
                 fill=BYTE_CYAN, outline=BYTE_DARK, width=1)

    # Expression annotation (expression cascade labels)
    draw.text((8, 24), "EXPRESSION CASCADE:", fill=(180, 160, 120), font=font_ann)
    for i, label in enumerate(["1. INDIGNANT", "2. GRUDGING", "3. RESIGNED"]):
        draw.text((8, 36 + i * 12), label, fill=(140, 125, 100), font=font_ann)

    # Character moment annotation
    draw.text((PW - 105, 24), "CHARACTER MOMENT",
              fill=(0, 200, 220), font=font_ann)
    draw.text((PW - 95, 36), "CU — owns frame",
              fill=(0, 180, 200), font=font_ann)

    # Camera annotation
    draw.text((4, DRAW_H - 14), "CU BYTE — eye level — slight low angle",
              fill=(120, 110, 90), font=font_ann)


def draw_p20(draw, img, font, font_bold, font_ann):
    """P20: MED WIDE — Two-shot establishing their relationship.
    Rule of thirds: Luma left, Byte right. First QUIET BEAT.
    The new normal beginning to form. They look at each other.
    Room around them: warm analogue + glitch coexisting — the show's visual thesis."""
    draw.rectangle([0, 0, PW, DRAW_H], fill=(24, 16, 10))

    # Room (3/4 two-point perspective per MEMORY.md)
    floor_y = int(DRAW_H * 0.72)
    back_wall_y = int(DRAW_H * 0.24)
    corner_x = int(PW * 0.38)

    # Left wall (warm amber)
    draw.rectangle([0, back_wall_y, corner_x, floor_y], fill=(30, 20, 12))
    draw.line([(corner_x, back_wall_y), (0, floor_y)], fill=(40, 28, 16), width=1)
    # Back wall
    draw.rectangle([corner_x, back_wall_y, PW, floor_y], fill=(28, 18, 11))
    draw.line([(0, back_wall_y), (PW, back_wall_y)], fill=(42, 28, 16), width=1)
    # Floor
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=FLOOR_DARK)
    draw.line([(0, floor_y), (PW, floor_y)], fill=(32, 22, 12), width=1)

    # MONITORS BACK WALL — all still blazing (coexistence of warm world + glitch)
    for mx, mw in [(corner_x + 20, 75), (corner_x + 130, 82), (corner_x + 248, 70)]:
        my = back_wall_y + 6
        mh = 44
        draw.rectangle([mx, my, mx + mw, my + mh], fill=(10, 8, 16),
                       outline=(30, 25, 42), width=2)
        # Each monitor: different glitch pattern (warm/cool coexistence)
        for scan in range(my + 3, my + mh - 3, 3):
            sc = 20 + (scan - my) * 2
            draw.line([(mx + 2, scan), (mx + mw - 2, scan)],
                      fill=(0, min(sc, 80), min(sc + 20, 100)), width=1)

    # Room details: books on floor, chips, scattered props
    for ox, oy, oc in [(50, floor_y - 6, (70, 50, 30)),
                       (120, floor_y - 4, (55, 88, 65)),
                       (PW - 80, floor_y - 5, (130, 50, 22))]:
        draw.rectangle([ox, oy, ox + 12, oy + 3], fill=oc)

    # Ceiling fan visible (upper area, still spinning slightly wrong)
    fan_cx = int(PW * 0.85)
    fan_cy = int(DRAW_H * 0.12)
    for fa in [0, 90, 180, 270]:
        rad = math.radians(fa + 8)
        fx = fan_cx + int(25 * math.cos(rad))
        fy = fan_cy + int(22 * math.sin(rad))
        draw.line([(fan_cx, fan_cy), (fx, fy)], fill=(48, 36, 22), width=4)

    # LUMA — sitting on floor, rule-of-thirds left
    luma_cx = int(PW * 0.28)
    luma_cy = int(DRAW_H * 0.60)
    # Torso
    draw.rectangle([luma_cx - 18, luma_cy - 28, luma_cx + 18, luma_cy + 8],
                   fill=LUMA_PJ, outline=(100, 150, 120), width=1)
    # Cross-legged
    draw.polygon([(luma_cx - 30, luma_cy + 8), (luma_cx + 5, luma_cy + 8),
                  (luma_cx + 10, floor_y - 2), (luma_cx - 38, floor_y - 2)],
                 fill=(95, 62, 40))
    draw.polygon([(luma_cx + 30, luma_cy + 8), (luma_cx - 5, luma_cy + 8),
                  (luma_cx - 10, floor_y - 2), (luma_cx + 38, floor_y - 2)],
                 fill=(95, 62, 40))
    # Face — WARMTH expression (not curious — she is choosing connection with Byte)
    # P20: The name exchange. First feeling of genuine connection.
    # Carmen: "She is choosing warmth deliberately." Soft smile, eyes narrowed in warmth,
    # brows gently raised — emotional intent, not assessment.
    draw_luma_face(draw, luma_cx + 2, luma_cy - 52, size=42,
                   expression='warmth', hair_state='normal')
    # Notebook (still in lap)
    draw.rectangle([luma_cx - 22, luma_cy + 4, luma_cx + 22, luma_cy + 14],
                   fill=(235, 225, 195), outline=(80, 70, 50), width=1)

    # Open space between them (COMPOSITIONAL INVITATION — relationship will fill it)
    # Pixel confetti drifts in the gap space
    add_pixel_confetti(draw, (int(PW * 0.38), int(PW * 0.62)),
                       (int(DRAW_H * 0.30), floor_y), 22, seed=20)

    # BYTE — floating at Luma's eye level, rule-of-thirds right
    byte_cx = int(PW * 0.68)
    byte_cy = luma_cy - 48
    draw_byte_body(draw, byte_cx, byte_cy, size=46,
                   expression='resigned', lean_deg=0, trail=False)

    # Camera annotation
    draw.text((4, DRAW_H - 14), "MED WIDE — eye level — first quiet beat",
              fill=(120, 110, 90), font=font_ann)


def draw_p21(draw, img, font, font_bold, font_ann):
    """P21: WIDE HIGH ANGLE — Full room chaos resuming. Inverse of opening push-in.
    CYCLE 9 FIX: Camera is 40-45° high angle isometric (NOT straight-down 90°).
    'Pulling back and up slightly' per script. Characters have PROFILE visible —
    not just top-of-head circles. Room walls implied. Floor plane at angle.
    Back wall monitors BLAZING, pixel confetti fills room like snow globe.
    Multiple Glitchkin pressing monitor insides. Byte URGENT. Luma pointing.
    They see: Byte is NOT alone."""
    draw.rectangle([0, 0, PW, DRAW_H], fill=(16, 10, 8))

    # ── ISOMETRIC / 40-45° HIGH ANGLE LAYOUT ──
    # Back wall occupies upper portion, floor angles down into foreground
    # Visible perspective: we see both the wall face AND floor receding
    back_wall_top = 0
    back_wall_bot = int(DRAW_H * 0.38)   # wall-floor junction line
    floor_bot = DRAW_H                    # floor extends to bottom of frame

    # BACK WALL (upper portion, facing camera)
    draw.rectangle([0, back_wall_top, PW, back_wall_bot], fill=(22, 14, 10))

    # FLOOR receding away (isometric — floor plane visible)
    # Perspective lines converging toward horizon at back_wall_bot
    draw.polygon([
        (0, back_wall_bot), (PW, back_wall_bot),
        (PW, floor_bot), (0, floor_bot)
    ], fill=(18, 12, 8))

    # Floor perspective grid (isometric lines receding to back wall)
    # Vertical lines (left-right spacing)
    for gx in range(0, PW + 1, 60):
        draw.line([(gx, back_wall_bot), (gx, floor_bot)], fill=(24, 16, 10), width=1)
    # Horizontal lines (depth bands receding)
    for depth in range(5):
        gy = back_wall_bot + int((floor_bot - back_wall_bot) * (depth / 5))
        # Slight perspective narrowing of horizontal bands
        draw.line([(0, gy), (PW, gy)], fill=(24, 16, 10), width=1)

    # Side walls implied (left and right wall meeting back wall)
    # Left wall edge
    draw.line([(0, back_wall_bot), (0, floor_bot)], fill=(30, 20, 12), width=2)
    # Right wall edge
    draw.line([(PW, back_wall_bot), (PW, floor_bot)], fill=(30, 20, 12), width=2)
    # Ceiling implied as dark edge at very top
    draw.rectangle([0, 0, PW, 6], fill=(12, 8, 6))

    # MONITORS ON BACK WALL — ALL BLAZING at maximum intensity
    # Glitchkin shapes pressing against insides of each monitor
    monitor_cols = [(0, 55, 70), (40, 0, 35), (0, 40, 60), (50, 20, 0)]
    mon_configs = [
        (15, 8, 88, back_wall_bot - 14, monitor_cols[0]),
        (130, 5, 92, back_wall_bot - 10, monitor_cols[1]),
        (255, 7, 84, back_wall_bot - 12, monitor_cols[2]),
        (368, 6, 90, back_wall_bot - 11, monitor_cols[3]),
    ]
    for mi, (mx, my, mw, mh, mc) in enumerate(mon_configs):
        # Monitor casing
        draw.rectangle([mx, my, mx + mw, my + mh], fill=(10, 8, 14),
                       outline=(30, 22, 40), width=2)
        # Screen — overlit, straining
        draw.rectangle([mx + 3, my + 3, mx + mw - 3, my + mh - 3], fill=mc)
        # Scan lines (texture)
        for sl in range(my + 4, my + mh - 4, 4):
            draw.line([(mx + 3, sl), (mx + mw - 3, sl)],
                      fill=(0, min(255, mc[1] + 40), min(255, mc[2] + 60)), width=1)
        # GLITCHKIN pressing from inside
        rng_m = random.Random(mi * 7 + 21)
        for gk in range(3 + mi % 2):
            gkx = mx + rng_m.randint(10, mw - 18)
            gky = my + rng_m.randint(6, mh - 10)
            gks = rng_m.randint(6, 12)
            draw.rectangle([gkx - gks // 2, gky - gks // 2,
                            gkx + gks // 2, gky + gks // 2],
                           fill=GLITCH_CYAN, outline=(0, 180, 200), width=1)
            draw.ellipse([gkx - 2, gky - 3, gkx + 2, gky + 1], fill=(255, 255, 255))

    # PIXEL CONFETTI filling room (snow globe — floor-to-ceiling)
    add_pixel_confetti(draw, (0, PW), (back_wall_bot, floor_bot), 70, seed=21,
                       colors=[GLITCH_CYAN, GLITCH_MAG, (255, 240, 100), (200, 255, 200)])
    add_pixel_confetti(draw, (0, PW), (back_wall_top, back_wall_bot), 30, seed=212,
                       colors=[GLITCH_CYAN, GLITCH_MAG])

    # ── LUMA — 40-45° high angle: PROFILE VISIBLE, not just top-of-head ──
    # She is standing on the floor plane (midground), pointing at monitors
    # At 40° angle we see her from above-and-in-front — profile + top
    luma_cx = int(PW * 0.32)
    luma_cy = int(DRAW_H * 0.60)   # mid-floor-plane = mid-frame vertically

    # Body from high angle: torso foreshortened, still readable as upright figure
    # Shoulders as ellipse (high-angle foreshortening)
    draw.ellipse([luma_cx - 18, luma_cy - 8, luma_cx + 18, luma_cy + 8],
                 fill=LUMA_PJ, outline=(90, 135, 110), width=2)
    # Head and partial face (40° angle: we see top + some profile — NOT pure silhouette)
    draw.ellipse([luma_cx - 14, luma_cy - 28, luma_cx + 14, luma_cy - 4],
                 fill=LUMA_HAIR)
    # Partial face profile (visible at 40-45° — not just a hair circle)
    draw.ellipse([luma_cx - 10, luma_cy - 24, luma_cx + 12, luma_cy - 8],
                 fill=LUMA_SKIN)
    # Visible eye (one, partial profile)
    draw.ellipse([luma_cx + 2, luma_cy - 20, luma_cx + 8, luma_cy - 14],
                 fill=(255, 245, 230))
    draw.ellipse([luma_cx + 4, luma_cy - 19, luma_cx + 7, luma_cy - 15],
                 fill=(20, 12, 8))

    # Arm pointing at monitors (from high angle — arm foreshortened toward back wall)
    arm_end_x = luma_cx + int(40 * math.cos(math.radians(-50)))
    arm_end_y = luma_cy + int(40 * math.sin(math.radians(-50)))
    draw.line([(luma_cx + 14, luma_cy - 4), (arm_end_x, arm_end_y)],
              fill=LUMA_SKIN, width=5)
    # Pointing finger tip
    draw.ellipse([arm_end_x - 4, arm_end_y - 4, arm_end_x + 4, arm_end_y + 4],
                 fill=LUMA_SKIN)

    # Legs (foreshortened — just visible below shoulder mass)
    draw.line([(luma_cx - 8, luma_cy + 6), (luma_cx - 12, luma_cy + 22)],
              fill=(95, 62, 40), width=6)
    draw.line([(luma_cx + 8, luma_cy + 6), (luma_cx + 12, luma_cy + 22)],
              fill=(95, 62, 40), width=6)

    # Shadow on floor (depth cue for floating vs standing)
    draw.ellipse([luma_cx - 16, luma_cy + 20, luma_cx + 16, luma_cy + 28],
                 fill=(10, 7, 4))

    # ── BYTE — 40-45° high angle: profile + top visible (NOT pure cube top) ──
    byte_cx = int(PW * 0.60)
    byte_cy = int(DRAW_H * 0.52)
    byte_sz = 26  # wide-shot scale

    # Byte body from high-ish angle: we see top + front face of cube
    # Top face (foreshortened — flat ellipse above)
    draw.ellipse([byte_cx - byte_sz // 2, byte_cy - byte_sz - 6,
                  byte_cx + byte_sz // 2, byte_cy - byte_sz + 6],
                 fill=BYTE_CYAN, outline=BYTE_DARK, width=1)
    # Front face of cube (profile visible — not just dot)
    draw.rectangle([byte_cx - byte_sz // 2, byte_cy - byte_sz,
                    byte_cx + byte_sz // 2, byte_cy + byte_sz // 3],
                   fill=BYTE_CYAN, outline=BYTE_DARK, width=1)
    # Spike on top (from above angle — spike visible as a point)
    draw.polygon([
        (byte_cx - 4, byte_cy - byte_sz),
        (byte_cx + 4, byte_cy - byte_sz),
        (byte_cx, byte_cy - byte_sz - 10),
    ], fill=BYTE_CYAN, outline=BYTE_DARK, width=1)
    # Visible eye on front face
    draw.ellipse([byte_cx - 5, byte_cy - byte_sz + 4,
                  byte_cx + 5, byte_cy - byte_sz + 12],
                 fill=(255, 255, 255), outline=BYTE_DARK, width=1)
    draw.ellipse([byte_cx - 2, byte_cy - byte_sz + 6,
                  byte_cx + 2, byte_cy - byte_sz + 10],
                 fill=BYTE_DARK)
    # Urgency: arms raised / gesturing (visible from high angle)
    draw.line([(byte_cx - byte_sz // 2, byte_cy - byte_sz // 2),
               (byte_cx - byte_sz, byte_cy - byte_sz)],
              fill=BYTE_CYAN, width=3)
    draw.line([(byte_cx + byte_sz // 2, byte_cy - byte_sz // 2),
               (byte_cx + byte_sz, byte_cy - byte_sz)],
              fill=BYTE_CYAN, width=3)
    # Glow pool on floor beneath him
    draw.ellipse([byte_cx - 20, byte_cy + byte_sz // 3 - 4,
                  byte_cx + 20, byte_cy + byte_sz // 3 + 4],
                 fill=(0, 40, 50))

    # Pixel trails from Byte (urgency)
    add_pixel_confetti(draw, (byte_cx - 30, byte_cx + 60),
                       (byte_cy - 20, byte_cy + 40), 18, seed=211)

    # Camera direction annotation
    draw.text((4, 4), "HIGH ANGLE 40-45° — not straight down — profiles visible",
              fill=(0, 200, 220), font=font_ann)
    draw.text((4, DRAW_H - 14), "INVERSE of opening push-in — camera retreating UP",
              fill=(120, 110, 90), font=font_ann)


def draw_p22(draw, img, font, font_bold, font_ann):
    """P22: ECU — Single monitor screen, multiple Glitchkin pressing through.
    Screen FILLS frame completely. Multiple Glitchkin jostling inside,
    one hand TOUCHING GLASS from inside — glass ripples like liquid.
    Screen bowing outward. Pixel confetti streaming from corners.
    VISIBLE FX: bulge, ripple ring, confetti eruption at corners."""
    draw.rectangle([0, 0, PW, DRAW_H], fill=(8, 5, 14))

    # Monitor bezel (very thin edge — ECU, screen fills almost everything)
    bezel_inset = 12
    draw.rectangle([0, 0, PW, DRAW_H],
                   fill=(12, 8, 18), outline=(25, 18, 35), width=bezel_inset)

    # SCREEN fills inner area
    screen_x1, screen_y1 = bezel_inset, bezel_inset
    screen_x2, screen_y2 = PW - bezel_inset, DRAW_H - bezel_inset
    screen_w = screen_x2 - screen_x1
    screen_h = screen_y2 - screen_y1

    # Screen fill — overlit, almost white-cyan
    draw.rectangle([screen_x1, screen_y1, screen_x2, screen_y2],
                   fill=(0, 80, 100))

    # Scan lines (analog texture)
    for sl in range(screen_y1, screen_y2, 3):
        brightness = 40 + (sl % 12) * 8
        draw.line([(screen_x1, sl), (screen_x2, sl)],
                  fill=(0, min(255, brightness + 60), min(255, brightness + 90)), width=1)

    # GLITCHKIN pressing from inside — multiple, jostling, chaotic
    # CYCLE 10 FIX (Carmen): ECU must show MORE detail, not less. Each Glitchkin
    # uses varied polygon shapes (4-7 sides, different sizes) — same approach as P24.
    # No two shapes identical — visually distinct, organically menacing.
    rng_22 = random.Random(22)
    for gk in range(8):
        gx = rng_22.randint(screen_x1 + 15, screen_x2 - 15)
        gy = rng_22.randint(screen_y1 + 10, screen_y2 - 10)
        gs = rng_22.randint(18, 42)  # wider size range for variety
        num_sides = 4 + rng_22.randint(0, 3)  # 4, 5, 6, or 7 sides
        # Glitchkin body — irregular polygon, each shape unique
        # Pressing-flat distortion: x-axis squash (wider than tall) at glass surface
        pts = []
        for side in range(num_sides):
            ang = side * (2 * math.pi / num_sides) + rng_22.uniform(-0.3, 0.3)
            jitter_x = rng_22.randint(-gs // 4, gs // 4)
            jitter_y = rng_22.randint(-gs // 4, gs // 4)
            # Slight x-stretch: pressed against glass = wider shape
            pts.append((gx + int((gs // 2 + jitter_x) * 1.2 * math.cos(ang)),
                        gy + int((gs // 2 + jitter_y) * 0.8 * math.sin(ang))))
        if len(pts) >= 3:
            body_col = rng_22.choice([(0, 180, 200), (0, 160, 185), (0, 195, 215), (20, 200, 210)])
            draw.polygon(pts, fill=body_col, outline=(0, 120, 150), width=2)
        # Smushed-face highlight — ellipse showing face pressed against glass
        draw.ellipse([gx - gs // 3, gy - gs // 4,
                      gx + gs // 3, gy + gs // 4],
                     fill=(0, 220, 240), outline=(0, 150, 180), width=1)
        # Eye pixels (two white squares — the giveaway that these are faces)
        draw.rectangle([gx - 4, gy - 3, gx - 1, gy], fill=(255, 255, 255))
        draw.rectangle([gx + 1, gy - 3, gx + 4, gy], fill=(255, 255, 255))

    # THE HAND TOUCHING GLASS — center-frame, low-center compositional anchor
    # (MEMORY.md: lower-center is the anchor. Eye rests here.)
    hand_cx = PW // 2
    hand_cy = int(DRAW_H * 0.62)
    hand_size = 28
    # Hand shape (angular glitch finger)
    draw.polygon([
        (hand_cx - hand_size // 3, hand_cy),
        (hand_cx + hand_size // 3, hand_cy),
        (hand_cx + hand_size // 4, hand_cy + hand_size),
        (hand_cx, hand_cy + hand_size + 6),
        (hand_cx - hand_size // 4, hand_cy + hand_size),
    ], fill=BYTE_CYAN, outline=BYTE_DARK, width=2)
    # Individual pixel fingers
    for fi, fx in enumerate([hand_cx - 12, hand_cx - 4, hand_cx + 4, hand_cx + 12]):
        draw.rectangle([fx - 3, hand_cy - 18 + fi * 2,
                        fx + 3, hand_cy], fill=BYTE_CYAN, outline=BYTE_DARK, width=1)

    # GLASS RIPPLE from hand-touch — visible FX, concentric ellipses
    for rr in range(6, 50, 8):
        ripple_alpha = max(0, 200 - rr * 4)
        draw.ellipse([hand_cx - rr * 2, hand_cy - rr,
                      hand_cx + rr * 2, hand_cy + rr],
                     outline=(min(255, 80 + rr * 3), 255, 255), width=2)

    # Screen BOWING OUTWARD at hand contact point (cartoon physics bulge)
    # Simulated with increasingly bright/white center
    for br in range(25, 4, -5):
        bv = max(0, 220 - br * 6)
        draw.ellipse([hand_cx - br * 3, hand_cy - br * 2 - 30,
                      hand_cx + br * 3, hand_cy + br * 2 - 30],
                     fill=(bv, 255, 255))

    # PIXEL CONFETTI streaming from corners (escape points)
    for corner_x, corner_y in [(screen_x1, screen_y1),
                                (screen_x2, screen_y1),
                                (screen_x1, screen_y2),
                                (screen_x2, screen_y2)]:
        for ci in range(8):
            rng_c = random.Random(ci + corner_x)
            px = corner_x + rng_c.randint(-20, 20)
            py = corner_y + rng_c.randint(-16, 16)
            sz = rng_c.randint(2, 5)
            col = rng_c.choice([GLITCH_CYAN, GLITCH_MAG, (255, 255, 100)])
            draw.rectangle([px - sz // 2, py - sz // 2,
                            px + sz // 2, py + sz // 2], fill=col)

    # Building WHINE annotation
    draw.text((screen_x1 + 4, screen_y1 + 4), "DIGITAL WHINE BUILDING",
              fill=(0, 220, 240), font=font_ann)
    draw.text((screen_x1 + 4, screen_y1 + 14), "MULTIPLIED — all screens",
              fill=(0, 200, 220), font=font_ann)

    # Camera annotation
    draw.text((4, DRAW_H - 14), "ECU MONITOR — dead flat — screen fills frame",
              fill=(120, 110, 90), font=font_ann)


def draw_p22a(draw, img, font, font_bold, font_ann):
    """P22a: MCU — Byte accidentally landing on Luma's shoulder. BRIDGE PANEL.
    Camera: eye level to shoulder (3.5ft off floor). OTS from slightly behind-right.
    Byte caught MID-ACCIDENT — one leg on shoulder, one dangling, gripping her PJ fabric.
    His expression: ALARMED (warning triangle cracked eye). 0.8 second insert panel.
    Pixel confetti sparking at contact point — digital nature marks her shoulder.
    Luma's profile only: jaw, hair, curve of shoulder — she hasn't noticed yet.
    MEMORY.md: Bridge panels are spatial contracts. OTS needs 6 explicit specs."""
    draw.rectangle([0, 0, PW, DRAW_H], fill=(20, 14, 8))

    # Room in background (defocused — chaos continuing off-frame)
    for blur_x in [80, 200, 340]:
        for gr in range(22, 6, -4):
            draw.ellipse([blur_x - gr * 3, 0, blur_x + gr * 3, gr * 2],
                         fill=(0, max(0, 40 - gr), max(0, 55 - gr)))

    # --- OTS SHOT SPECS (6-spec per MEMORY.md) ---
    # 1. Whose shoulder: Luma's RIGHT shoulder (viewer's left side of frame)
    # 2. Camera height: 3.5 feet off floor (Luma's shoulder height)
    # 3. Direction: slightly behind and to her right — looking over shoulder toward monitors
    # 4. Byte distance from Luma: 0 inches — he's ON her shoulder
    # 5. Background: monitors blazing (defocused), chaos continuing
    # 6. Luma silhouette: jaw, hair, shoulder visible — NO competing sharp elements

    # LUMA'S SHOULDER MASS — occupies lower-left anchor position
    # Per MEMORY.md: OTS silhouette ~20% of frame width
    shoulder_w = int(PW * 0.22)  # exactly 22% frame width
    shoulder_h = int(DRAW_H * 0.35)
    shoulder_x = 0
    shoulder_y = DRAW_H - shoulder_h

    # Shoulder/torso (PJ fabric — mint with pixel-grid texture)
    draw.rectangle([shoulder_x, shoulder_y, shoulder_x + shoulder_w, DRAW_H],
                   fill=LUMA_PJ, outline=(90, 135, 110), width=2)

    # Pixel-grid PJ texture (character detail)
    for pg in range(shoulder_y, DRAW_H, 8):
        draw.line([(shoulder_x, pg), (shoulder_x + shoulder_w, pg)],
                  fill=(140, 180, 155), width=1)
    for pg in range(shoulder_x, shoulder_x + shoulder_w, 8):
        draw.line([(pg, shoulder_y), (pg, DRAW_H)],
                  fill=(140, 180, 155), width=1)

    # Luma's jaw/neck visible above shoulder
    draw.ellipse([shoulder_x + 5, shoulder_y - 40,
                  shoulder_x + shoulder_w + 12, shoulder_y + 8],
                 fill=LUMA_SKIN, outline=(50, 30, 15), width=1)

    # Hair (dark mass above shoulder and jaw)
    draw.ellipse([shoulder_x - 10, shoulder_y - 80,
                  shoulder_x + shoulder_w + 20, shoulder_y - 15],
                 fill=LUMA_HAIR)

    # CONTACT POINT — where Byte has landed (mid-shoulder top)
    contact_x = shoulder_x + shoulder_w // 2 + 15
    contact_y = shoulder_y

    # PIXEL CONFETTI AT CONTACT POINT — digital nature marks her
    # "tiny sparks" — cyan fading to brief Soft Gold per script
    for ci in range(12):
        rng_c = random.Random(ci + 22)
        px = contact_x + rng_c.randint(-22, 22)
        py = contact_y + rng_c.randint(-18, 12)
        sz = rng_c.randint(2, 4)
        # Warm gold on first few (the "belonging" warmth per script)
        col = (230, 200, 80) if ci < 3 else (rng_c.choice([GLITCH_CYAN, GLITCH_MAG]))
        draw.rectangle([px - sz // 2, py - sz // 2,
                        px + sz // 2, py + sz // 2], fill=col)

    # Corona of cyan/magenta sparks at contact (visible FX per MEMORY.md)
    for cr in range(16, 4, -4):
        draw.ellipse([contact_x - cr, contact_y - cr // 2,
                      contact_x + cr, contact_y + cr // 2],
                     outline=(0, 200, 230), width=1)

    # BYTE — on the shoulder, awkward landing
    # One leg ON shoulder surface, one dangling off far side
    # Body tilted 20° sideways — overcorrecting
    byte_cx = contact_x + 8
    byte_cy = contact_y - 28
    byte_size = 52  # large enough to read clearly

    # Byte's ambient glow (his digital presence)
    for gr in range(25, 5, -6):
        draw.ellipse([byte_cx - gr * 2, byte_cy - gr,
                      byte_cx + gr * 2, byte_cy + gr],
                     fill=(0, max(0, 50 - gr * 3), max(0, 65 - gr * 3)))

    draw_byte_body(draw, byte_cx, byte_cy, size=byte_size,
                   expression='alarmed', lean_deg=20, trail=False)

    # Leg ON shoulder (one limb flat against PJ fabric)
    leg_on_x = byte_cx - byte_size // 4
    draw.rectangle([leg_on_x, contact_y - 8, leg_on_x + 10, contact_y + 4],
                   fill=BYTE_CYAN, outline=BYTE_DARK, width=1)

    # Leg DANGLING (other limb off far side)
    draw.rectangle([byte_cx + byte_size // 4, contact_y - 4,
                    byte_cx + byte_size // 4 + 8, contact_y + 16],
                   fill=BYTE_CYAN, outline=BYTE_DARK, width=1)

    # Hands GRIPPING PJ fabric (both arm-tips on her hoodie)
    for grip_x in [byte_cx - byte_size // 2 - 4, byte_cx + byte_size // 2 + 4]:
        draw.ellipse([grip_x - 4, contact_y - 6, grip_x + 4, contact_y + 2],
                     fill=BYTE_CYAN, outline=BYTE_DARK, width=1)

    # Look direction: monitors ahead (he's already scoping the threat)
    gaze_x = PW - 20
    gaze_y = int(DRAW_H * 0.28)
    draw.line([(byte_cx + byte_size // 3, byte_cy - byte_size // 6),
               (gaze_x, gaze_y)],
              fill=(0, 180, 200), width=1)
    draw.ellipse([gaze_x - 4, gaze_y - 4, gaze_x + 4, gaze_y + 4],
                 fill=(0, 180, 200))

    # Monitor blaze background (defocused chaos)
    for bx_m in [PW // 2, int(PW * 0.72), PW - 40]:
        for gr in range(20, 4, -4):
            draw.ellipse([bx_m - gr * 2, int(DRAW_H * 0.18),
                          bx_m + gr * 2, int(DRAW_H * 0.18) + gr * 2],
                         fill=(0, max(0, 55 - gr), max(0, 72 - gr)))

    # OTS spec annotation
    draw.text((shoulder_x + shoulder_w + 4, shoulder_y + 4),
              "OTS: ~22% frame", fill=(0, 180, 200), font=font_ann)
    draw.text((shoulder_x + shoulder_w + 4, shoulder_y + 14),
              "Luma's R shoulder", fill=(0, 160, 180), font=font_ann)
    draw.text((shoulder_x + shoulder_w + 4, shoulder_y + 24),
              "3.5ft camera height", fill=(0, 140, 160), font=font_ann)

    # "tktktk" sound annotation (confetti on fabric)
    draw.text((contact_x + 20, contact_y - 42), "tktktk",
              fill=(160, 145, 120), font=font_ann)

    # Camera annotation
    draw.text((4, DRAW_H - 14), "MCU — shoulder height — BRIDGE: Byte lands by accident",
              fill=(120, 110, 90), font=font_ann)


def draw_p23(draw, img, font, font_bold, font_ann):
    """P23: MED — Luma and Byte, BACKS TO CAMERA. The SHOW'S PROMISE SHOT.
    Facing wall of monitors together. Camera behind them at their eye levels.
    Luma: shoulders square, chin up, hands ready. Byte: on shoulder, grumpy but present.
    Room: FULL GLITCH CHAOS palette — warm world nearly gone.
    Multiple monitors beginning to breach simultaneously — screens bowing forward.
    This is the handshake with the audience: these two, facing impossible chaos, together."""
    draw.rectangle([0, 0, PW, DRAW_H], fill=(10, 6, 12))

    # Floor (they're standing)
    floor_y = int(DRAW_H * 0.80)
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(8, 5, 10))
    draw.line([(0, floor_y), (PW, floor_y)], fill=(20, 12, 18), width=1)

    # FULL GLITCH CHAOS PALETTE — warm world nearly gone, cool cyan/magenta dominates
    # Background: monitor wall completely blazing
    back_wall_y = int(DRAW_H * 0.10)
    draw.rectangle([0, back_wall_y, PW, floor_y], fill=(12, 8, 16))

    # MONITOR WALL (filling back of frame, all bowing forward)
    # CYCLE 10 FIX (Carmen): Increase contrast dramatically. Monitors must read as
    # "about to break through" — hot white-cyan center, high-contrast dark bezels,
    # aggressive distortion rings breaking outside the bezel edge, bright outline glow.
    monitors_bowing = [
        (20, back_wall_y + 4, 80, 48),
        (120, back_wall_y + 2, 90, 52),
        (230, back_wall_y + 5, 78, 46),
        (330, back_wall_y + 3, 85, 50),
        (430, back_wall_y + 4, 45, 44),
    ]
    for mx, my, mw, mh in monitors_bowing:
        cx_m = mx + mw // 2
        cy_m = my + mh // 2
        # Screen fill — overloaded, nearly white-hot at center
        draw.rectangle([mx, my, mx + mw, my + mh], fill=(0, 180, 220))
        # AGGRESSIVE distortion rings OUTSIDE bezel (breaking through physical boundary)
        for rr in range(mh // 2 + 20, 3, -5):
            ring_intensity = max(0, 255 - rr * 7)
            ring_col = (0, min(255, ring_intensity + 100), min(255, ring_intensity + 130))
            draw.ellipse([cx_m - rr * 2, cy_m - rr,
                          cx_m + rr * 2, cy_m + rr],
                         outline=ring_col, width=2)
        # Hot-center radial gradient — near-white at bull's-eye
        for gr in range(mh // 2, 1, -3):
            heat = min(255, 255 - gr * 5)
            draw.ellipse([cx_m - gr * 2, cy_m - gr,
                          cx_m + gr * 2, cy_m + gr],
                         fill=(heat // 5, min(255, heat + 40), 255))
        # Hottest point — pure white punch at center
        hw = max(5, mw // 8)
        draw.ellipse([cx_m - hw, cy_m - hw // 2,
                      cx_m + hw, cy_m + hw // 2],
                     fill=(220, 255, 255))
        # BEZEL — thick, high-contrast dark frame (threat needs a dark surround)
        draw.rectangle([mx, my, mx + mw, my + mh], fill=None,
                       outline=(200, 255, 255), width=3)
        draw.rectangle([mx - 3, my - 3, mx + mw + 3, my + mh + 3], fill=None,
                       outline=(5, 3, 10), width=4)
        # Pixel confetti erupting from monitor (breach starting)
        add_pixel_confetti(draw,
                           (mx - 10, mx + mw + 10),
                           (my - 6, my + mh + 6),
                           16, seed=mx + 23)

    # Glitchkin shapes pressing from all monitor insides
    # CYCLE 11 FIX (Carmen): Use same 4-7 sided polygon approach as P22 and P24.
    # Rectangles at this scale are generic — polygons with per-vertex jitter create
    # organic, distinct shapes that read as individual creatures, not uniform blocks.
    rng_23 = random.Random(23)
    for _ in range(14):
        gx = rng_23.randint(20, PW - 20)
        gy = rng_23.randint(back_wall_y + 4, back_wall_y + 48)
        gs = rng_23.randint(8, 18)
        num_sides = 4 + rng_23.randint(0, 3)  # 4, 5, 6, or 7 sides
        pts = []
        for side in range(num_sides):
            ang = side * (2 * math.pi / num_sides) + rng_23.uniform(-0.3, 0.3)
            jitter_x = rng_23.randint(-gs // 4, gs // 4)
            jitter_y = rng_23.randint(-gs // 4, gs // 4)
            pts.append((gx + int((gs // 2 + jitter_x) * math.cos(ang)),
                        gy + int((gs // 2 + jitter_y) * math.sin(ang))))
        if len(pts) >= 3:
            body_col = (0, rng_23.randint(160, 240), rng_23.randint(180, 255))
            draw.polygon(pts, fill=body_col, outline=(0, 140, 180), width=1)
        # Pixel eye — gives each Glitchkin a face even at small scale
        draw.rectangle([gx - 1, gy - 1, gx + 1, gy + 1], fill=(255, 255, 255))

    # PIXEL CONFETTI filling the room (floor to ceiling — snow globe)
    add_pixel_confetti(draw, (0, PW), (back_wall_y, floor_y), 65, seed=23,
                       colors=[GLITCH_CYAN, GLITCH_MAG, (255, 240, 80), (200, 255, 200)])

    # Room cables on floor (warm world's last remnants)
    for cy_c in [floor_y - 3, floor_y - 1]:
        draw.line([(0, cy_c), (PW, cy_c)], fill=(30, 20, 12), width=1)

    # LUMA — back to camera, center-left, shoulders square, chin up (implied)
    luma_cx = int(PW * 0.40)
    luma_body_top = int(DRAW_H * 0.32)

    # Back view: hair mass visible (large, organic, the chaos-proof constant)
    draw.ellipse([luma_cx - int(PW * 0.12), luma_body_top - 28,
                  luma_cx + int(PW * 0.12), luma_body_top + 24],
                 fill=LUMA_HAIR)
    # Shoulders (PJ top from back)
    draw.rectangle([luma_cx - 32, luma_body_top + 18,
                    luma_cx + 32, floor_y - 2], fill=LUMA_PJ,
                   outline=(90, 135, 110), width=1)
    # Arms at sides (about to move)
    draw.line([(luma_cx - 24, luma_body_top + 30),
               (luma_cx - 38, floor_y - 30)], fill=LUMA_SKIN, width=6)
    draw.line([(luma_cx + 24, luma_body_top + 30),
               (luma_cx + 38, floor_y - 30)], fill=LUMA_SKIN, width=6)
    # Legs
    draw.line([(luma_cx - 12, floor_y - 2), (luma_cx - 14, floor_y)],
              fill=(95, 62, 40), width=10)
    draw.line([(luma_cx + 12, floor_y - 2), (luma_cx + 14, floor_y)],
              fill=(95, 62, 40), width=10)

    # BYTE — on her shoulder (having committed to the perch)
    byte_cx = luma_cx + 28
    byte_cy = luma_body_top + 10
    byte_size = 32  # smaller from behind, but clear silhouette
    # Byte back-of-head (cube spike visible from behind)
    draw.rectangle([byte_cx - byte_size // 2, byte_cy - byte_size // 2,
                    byte_cx + byte_size // 2, byte_cy + byte_size // 2],
                   fill=BYTE_CYAN, outline=BYTE_DARK, width=2)
    # Spike
    draw.polygon([
        (byte_cx - byte_size // 5, byte_cy - byte_size // 2),
        (byte_cx + byte_size // 5, byte_cy - byte_size // 2),
        (byte_cx, byte_cy - byte_size // 2 - byte_size // 3),
    ], fill=BYTE_CYAN, outline=BYTE_DARK, width=1)
    # Small glow emanating from Byte
    for gr in range(14, 4, -4):
        draw.ellipse([byte_cx - gr, byte_cy - gr, byte_cx + gr, byte_cy + gr],
                     outline=(0, max(0, 80 - gr * 6), max(0, 100 - gr * 6)), width=1)

    # CAMERA PUSH line annotation (slight push-in happening)
    draw.line([(PW // 2, DRAW_H - 5), (PW // 2, DRAW_H - 14)],
              fill=(150, 135, 110), width=1)
    draw.text((PW // 2 + 4, DRAW_H - 14), "PUSH IN",
              fill=(150, 135, 110), font=font_ann)

    # "The show's promise shot" annotation
    draw.text((4, 4), "PROMISE SHOT: two + impossible chaos = together",
              fill=(0, 180, 200), font=font_ann)

    # Camera annotation
    draw.text((4, DRAW_H - 14), "MED — behind them — backs to camera — OTS/reverse",
              fill=(120, 110, 90), font=font_ann)


def draw_p24(draw, img, font, font_bold, font_ann):
    """P24: WIDE — Chaos apex: THE BREACH. Multiple Glitchkin POURING out.
    Dutch tilt 12° LEFT — applied as TRUE canvas rotation via make_panel().
    CYCLE 9 FIX: Luma moved to LOWER-LEFT THIRD. Partially cropped at bottom
    (foreground figure). Camera reads as looking UP at her.
    Luma foreground: low-angle chin-up, jaw SET, eyes WIDE. Reckless excitement.
    Byte on shoulder: resigned dignity, absolutely furious, absolutely staying.
    Background chaos fills right + upper portions. Glitchkin everywhere except
    the still point where Luma+Byte stand.
    This is THE HOOK FRAME. Hold 1.5s. Everything at maximum except the two leads."""
    draw.rectangle([0, 0, PW, DRAW_H], fill=(8, 4, 14))

    # Floor — FLAT (12° Dutch tilt applied via canvas rotation after draw)
    floor_y = int(DRAW_H * 0.76)
    draw.polygon([(0, floor_y), (PW, floor_y),
                  (PW, DRAW_H), (0, DRAW_H)], fill=(6, 3, 10))
    draw.line([(0, floor_y), (PW, floor_y)], fill=(16, 10, 20), width=1)

    # Background: monitors ALL BREACHED — Glitchkin pouring out
    # Back wall, total chaos palette — warm world GONE
    draw.rectangle([0, 0, PW, floor_y], fill=(10, 5, 18))

    # BREACHED MONITORS across back wall
    breach_monitors = [
        (10, 15, 70, 42), (95, 10, 80, 46), (195, 14, 72, 44),
        (285, 11, 78, 42), (378, 13, 68, 40), (458, 16, 18, 38),
    ]
    for mx, my, mw, mh in breach_monitors:
        # Monitor casing (dark, secondary to chaos)
        draw.rectangle([mx, my, mx + mw, my + mh], fill=(5, 3, 10),
                       outline=(18, 12, 28), width=2)
        # Screen: white-out at breach point
        draw.rectangle([mx + 2, my + 2, mx + mw - 2, my + mh - 2],
                       fill=(20, 15, 30))
        # Breach hole (multiple points of max cyan light)
        draw.ellipse([mx + mw // 2 - 8, my + mh // 2 - 5,
                      mx + mw // 2 + 8, my + mh // 2 + 5],
                     fill=(180, 255, 255))

    # GLITCHKIN POURING OUT — wall to wall, ceiling to floor
    # All shapes, all sizes, all chaotic angles
    rng_24 = random.Random(24)
    for gk in range(35):
        gx = rng_24.randint(10, PW - 10)
        gy = rng_24.randint(8, int(floor_y * 0.88))
        gs = rng_24.randint(10, 32)
        # Each Glitchkin: random jagged body + pixel eye
        pts = []
        for side in range(4 + rng_24.randint(0, 3)):
            ang = side * (2 * math.pi / (4 + rng_24.randint(0, 3)))
            jitter = rng_24.randint(-gs // 4, gs // 4)
            pts.append((gx + int((gs // 2 + jitter) * math.cos(ang)),
                        gy + int((gs // 3 + jitter) * math.sin(ang))))
        if len(pts) >= 3:
            col = rng_24.choice([(0, 200, 220), (0, 180, 200), (0, 160, 185)])
            draw.polygon(pts, fill=col, outline=(0, 130, 155), width=1)
        # Pixel eye
        draw.rectangle([gx - 2, gy - 2, gx + 2, gy + 2], fill=(255, 255, 255))

    # Pixel trails from each monitor breach point
    for mx_b, my_b, mw_b, mh_b in breach_monitors:
        cx_b = mx_b + mw_b // 2
        cy_b = my_b + mh_b // 2
        add_pixel_confetti(draw, (cx_b - 20, cx_b + 20),
                           (cy_b - 10, floor_y),
                           10, seed=mx_b + 241)

    # PIXEL CONFETTI — maximum saturation, room full
    add_pixel_confetti(draw, (0, PW), (0, floor_y), 80, seed=24,
                       colors=[GLITCH_CYAN, GLITCH_MAG,
                                (255, 240, 60), (100, 255, 200), (255, 100, 255)])

    # LUMA — FOREGROUND, LOWER-LEFT THIRD — partially cropped at bottom
    # CYCLE 9 FIX: Camera reads as looking UP at her — she fills lower-left.
    # Figure is LARGE, cropped at bottom edge (foreground hero placement).
    # Background chaos + Glitchkin fill right half and upper portions.
    luma_cx = int(PW * 0.22)    # Left third of frame (not center)
    luma_cy = int(DRAW_H * 0.72)  # Low — figure extends below frame bottom (cropped)

    # Body — large foreground figure (low angle = she looms into frame)
    # Body extends below DRAW_H — partially cropped at bottom (foreground!)
    body_top = luma_cy - 55
    body_bot = DRAW_H + 20      # INTENTIONALLY below frame bottom = cropped
    draw.rectangle([luma_cx - 36, body_top, luma_cx + 36, body_bot],
                   fill=LUMA_PJ, outline=(90, 135, 110), width=3)
    # Arms at sides, slightly out — ready-to-move pose (large scale)
    draw.line([(luma_cx - 28, body_top + 20), (luma_cx - 65, body_top + 55)],
              fill=LUMA_SKIN, width=9)
    draw.line([(luma_cx + 28, body_top + 20), (luma_cx + 62, body_top + 52)],
              fill=LUMA_SKIN, width=9)
    # Legs (low-angle foreshortening — barely visible, cropped)
    draw.rectangle([luma_cx - 28, floor_y - 10,
                    luma_cx - 10, floor_y + 8], fill=(95, 62, 40))
    draw.rectangle([luma_cx + 10, floor_y - 8,
                    luma_cx + 28, floor_y + 8], fill=(95, 62, 40))

    # Face — MAXIMUM RECKLESS EXCITEMENT (the show's signature Luma expression)
    # Chin up, eyes wide, jaw set — adrenaline overriding sense
    # Face is at mid-frame vertically (low angle: body goes DOWN below frame)
    draw_luma_face(draw, luma_cx + 2, luma_cy - 100, size=62,
                   expression='reckless', hair_state='max-volume')

    # BYTE — on her shoulder, resigned dignity, upper-left area near Luma
    byte_cx = luma_cx + 44
    byte_cy = body_top - 10
    draw_byte_body(draw, byte_cx, byte_cy, size=40,
                   expression='resigned', lean_deg=-5, trail=False)

    # Byte's pixel confetti corona (his presence marks her)
    for cr in range(14, 3, -3):
        draw.ellipse([byte_cx - cr, byte_cy - cr, byte_cx + cr, byte_cy + cr],
                     outline=(0, max(0, 120 - cr * 8), max(0, 150 - cr * 8)), width=1)

    # STILL POINT annotation (lower-left two vs the chaos filling rest of frame)
    draw.text((PW // 2 + 20, 4), "THE HOOK FRAME — still point in the storm",
              fill=(0, 200, 220), font=font_ann)
    draw.text((PW // 2 + 20, 14), "Hold 1.5s — Luma lower-left, chaos fills frame",
              fill=(0, 180, 200), font=font_ann)

    # Dutch tilt annotation (canvas rotation delivers true 12° — not polygon tilt)
    draw.text((4, DRAW_H - 14), "WIDE — DUTCH 12° canvas rotate — low angle hero",
              fill=(120, 110, 90), font=font_ann)


# ── Main ──────────────────────────────────────────────────────────────────────

PANELS = [
    # (panel_num, shot_type, caption_text, draw_fn, output_filename, dutch_tilt_deg, dutch_bg)
    (
        "14", "MED",
        "Byte ricochets off bookshelf — multi-exposure trajectory — pinball physics",
        draw_p14,
        "panel_p14_bookshelf_ricochet.png",
        12, (20, 14, 8)   # TRUE 12° Dutch tilt CW — canvas rotation
    ),
    (
        "15", "MED",
        "Luma in freefall — glitch forces hair into PERFECT CIRCLE — 8 frames",
        draw_p15,
        "panel_p15_luma_freefall.png"
    ),
    (
        "16", "ECU",
        "ECU: Luma's face on floor — one eye finds something — FOCUS building",
        draw_p16,
        "panel_p16_floor_ecu.png"
    ),
    (
        "17", "MED",
        "Quiet beat — Luma sitting up, Byte hovering — chip falls — they watch",
        draw_p17,
        "panel_p17_quiet_beat.png"
    ),
    (
        "18", "MED",
        "Curiosity activates — Luma turns notebook — doodles look like Byte",
        draw_p18,
        "panel_p18_notebook_turn.png"
    ),
    (
        "19", "CU",
        "Byte's character moment — 'The preferred term is Glitchkin' — offended",
        draw_p19,
        "panel_p19_byte_reaction.png"
    ),
    (
        "20", "MED WIDE",
        "Two-shot: Luma left, Byte right — first quiet beat — new normal forming",
        draw_p20,
        "panel_p20_twoshot_calm.png"
    ),
    (
        "21", "WIDE",
        "Chaos resumes — high angle — other Glitchkin pressing ALL monitors",
        draw_p21,
        "panel_p21_chaos_overhead.png"
    ),
    (
        "22", "ECU",
        "ECU monitor: multiple Glitchkin pressing through — hand touches glass — ripple",
        draw_p22,
        "panel_p22_monitor_breach.png"
    ),
    (
        "22a", "MCU",
        "BRIDGE: Byte ACCIDENTALLY lands on Luma's shoulder — pixel sparks on fabric",
        draw_p22a,
        "panel_p22a_shoulder_bridge.png"
    ),
    (
        "23", "MED",
        "PROMISE SHOT: backs to camera — Luma+Byte facing chaos — together",
        draw_p23,
        "panel_p23_promise_shot.png"
    ),
    (
        "24", "WIDE",
        "THE BREACH: Glitchkin pouring out — Luma hero shot — Byte on shoulder — HOOK",
        draw_p24,
        "panel_p24_breach_apex.png",
        -12, (8, 4, 14)   # TRUE 12° Dutch tilt LEFT (negative = CCW) — canvas rotation
    ),
]


def main():
    print("=" * 60)
    print("Panel Chaos Generator — Cycle 12")
    print("Generating P14–P24 (The Chaos Sequence)")
    print("=" * 60)

    import os
    os.makedirs(PANELS_DIR, exist_ok=True)

    for entry in PANELS:
        panel_num, shot_type, caption, draw_fn, filename = entry[:5]
        dutch_deg = entry[5] if len(entry) > 5 else 0
        dutch_bg  = entry[6] if len(entry) > 6 else (8, 4, 14)
        make_panel(panel_num, shot_type, caption, draw_fn, filename,
                   dutch_tilt_deg=dutch_deg, dutch_bg=dutch_bg)

    print(f"\nDone. {len(PANELS)} panels generated.")
    print(f"Output: {PANELS_DIR}/")


if __name__ == "__main__":
    main()
