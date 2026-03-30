#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P14.py
Cold Open Panel P14 — MED — Byte Ricochets Off Bookshelf
Diego Vargas, Storyboard Artist — Cycle 45

Beat: Comedic escalation. Byte has launched himself (or been launched) across
      Grandma Miri's den and impacts the bookshelf. The ricochet arc is shown as
      a multi-exposure PIXEL TRAIL — the storyboard grammar for fast cartoon motion.
      Books and a rubber duck become airborne. The scene goes briefly chaotic.

This panel is pure comedy timing. The staging must read:
  1. WHERE Byte came from (trail arc shows it)
  2. WHERE Byte is NOW (impact point at bookshelf, high right)
  3. WHAT got hit (books + rubber duck dislodged, in mid-air)
  4. DUTCH TILT — fixed camera 5ft, Dutch 12° CW = energy and instability

Camera: Fixed, 5ft height — medium camera. Dutch tilt 12° CW applied to draw area only.
        Annotation: "FIXED CAM — 5ft  DUTCH 12° CW"

Key staging:
  - Bookshelf occupies upper-right quadrant — tall shelves, books jammed tight
  - Byte impact point: upper-right, slight bounce-back pose (ALARMED expression)
  - Multi-exposure pixel trail: arc from lower-left → upper-right (ricochet trajectory)
    4-5 ghost Byte silhouettes at decreasing opacity along arc = motion grammar
  - Airborne objects: 3 books (tumbling) + rubber duck (airborne upper-center)
  - Confetti from Byte's presence drifts in chaotic scatter (TENSE density)
  - Warm den ambient vs ELEC_CYAN from Byte presence

Annotations:
  - "RICOCHET ARC →" with trajectory arrow
  - "DUTCH 12° CW — fixed cam"
  - "BOOKS AIRBORNE" label on falling book cluster
  - "RUBBER DUCK (BG detail)" label

Arc: TENSE (HOT_MAGENTA border)
Image size rule: ≤ 1280px in both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P14.png
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P14.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H   # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM   = (250, 240, 220)
SUNLIT_AMB   = (212, 146, 58)
VOID_BLACK   = (10, 10, 20)
DEEP_SPACE   = (6, 4, 14)
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM= (0, 120, 140)
HOT_MAGENTA  = (232, 0, 152)
LUMA_HOODIE  = (232, 112, 58)   # canonical orange — not used in this panel but noted
BYTE_TEAL    = (0, 212, 232)
BYTE_BODY    = (0, 180, 200)
SHELF_WOOD   = (148, 98, 52)
SHELF_SHADOW = (98, 60, 28)
BOOK_COLORS  = [
    (200, 60, 40),   # red
    (60, 120, 200),  # blue
    (80, 160, 80),   # green
    (200, 180, 40),  # yellow
    (140, 60, 160),  # purple
    (210, 120, 50),  # amber
]
RUBBER_DUCK  = (240, 210, 40)   # classic yellow duck
RUBBER_BEAK  = (230, 140, 20)
WALL_WARM    = (190, 170, 138)
FLOOR_WARM   = (160, 132, 96)
PIXEL_TRAIL  = (0, 200, 220)    # ghost trail color
# Caption
BG_CAPTION   = (12, 8, 6)
TEXT_SHOT    = (232, 224, 204)
TEXT_ARC     = HOT_MAGENTA
TEXT_DESC    = (155, 148, 122)
TEXT_META    = (88, 82, 66)
ARC_COLOR    = HOT_MAGENTA
ANN_COLOR    = (220, 200, 80)

RNG = random.Random(1414)


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


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=50):
    """Additive alpha composite glow — never darkens."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_irregular_poly(draw, cx, cy, r, sides, color, rng, seed_offset=0):
    """Draw an irregular polygon (4–7 sided) for Glitchkin pixel artifacts."""
    pts = []
    for k in range(sides):
        angle = (2 * math.pi * k / sides) + rng.uniform(-0.3, 0.3)
        rad   = r * rng.uniform(0.65, 1.15)
        pts.append((cx + rad * math.cos(angle), cy + rad * math.sin(angle)))
    draw.polygon(pts, fill=color)


def draw_byte_silhouette(draw, cx, cy, scale=1.0, alpha_factor=1.0, img=None):
    """
    Draw a simplified Byte silhouette (body + head) for multi-exposure ghost trail.
    alpha_factor 0.0–1.0: opacity control for ghost trail.
    Uses RGBA overlay when img is provided.
    """
    body_h = int(42 * scale)
    body_w = int(28 * scale)
    head_r = int(16 * scale)
    arm_w  = int(6 * scale)
    arm_l  = int(14 * scale)
    leg_h  = int(12 * scale)

    alpha  = int(255 * alpha_factor)
    color  = (*BYTE_TEAL, alpha)

    if img is None:
        # Direct draw — no alpha
        c = BYTE_TEAL
        # Body
        draw.ellipse([cx - body_w // 2, cy - body_h // 2,
                      cx + body_w // 2, cy + body_h // 2], fill=c)
        # Head
        draw.ellipse([cx - head_r, cy - body_h // 2 - head_r,
                      cx + head_r, cy - body_h // 2 + head_r], fill=c)
        # Eyes (pixel blocks)
        ey = cy - body_h // 2
        for ex_off in [-6, 5]:
            draw.rectangle([cx + ex_off * int(scale), ey - 3,
                             cx + ex_off * int(scale) + 4, ey + 2],
                            fill=VOID_BLACK)
        # Arms
        draw.rectangle([cx - body_w // 2 - arm_l, cy - arm_w // 2,
                         cx - body_w // 2,        cy + arm_w // 2], fill=c)
        draw.rectangle([cx + body_w // 2,         cy - arm_w // 2,
                         cx + body_w // 2 + arm_l, cy + arm_w // 2], fill=c)
        # Legs
        for lx_off in [-8, 6]:
            draw.rectangle([cx + lx_off * int(scale), cy + body_h // 2,
                             cx + lx_off * int(scale) + 5, cy + body_h // 2 + leg_h],
                            fill=c)
    else:
        # RGBA overlay for transparency
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        ld    = ImageDraw.Draw(layer)
        bw2   = body_w // 2
        bh2   = body_h // 2
        ld.ellipse([cx - bw2, cy - bh2, cx + bw2, cy + bh2], fill=color)
        ld.ellipse([cx - head_r, cy - bh2 - head_r,
                    cx + head_r, cy - bh2 + head_r], fill=color)
        ld.rectangle([cx - bw2 - arm_l, cy - arm_w // 2,
                       cx - bw2,        cy + arm_w // 2], fill=color)
        ld.rectangle([cx + bw2,         cy - arm_w // 2,
                       cx + bw2 + arm_l, cy + arm_w // 2], fill=color)
        # pixel eyes — darker
        ey   = cy - bh2
        eye_c = (0, 0, 0, alpha)
        for ex_off in [-6, 5]:
            ld.rectangle([cx + ex_off, ey - 3, cx + ex_off + 4, ey + 2], fill=eye_c)
        img.paste(Image.alpha_composite(img.convert('RGBA'), layer).convert('RGB'))


def draw_book(draw, cx, cy, w, h, color, tilt_deg=0):
    """Draw a tilted book rectangle (closed, solid color)."""
    half_w = w // 2
    half_h = h // 2
    angle  = math.radians(tilt_deg)
    cos_a  = math.cos(angle)
    sin_a  = math.sin(angle)
    corners_local = [
        (-half_w, -half_h),
        ( half_w, -half_h),
        ( half_w,  half_h),
        (-half_w,  half_h),
    ]
    pts = [(int(cx + lx * cos_a - ly * sin_a),
            int(cy + lx * sin_a + ly * cos_a))
           for (lx, ly) in corners_local]
    draw.polygon(pts, fill=color)
    # Spine line (dark)
    spine_local = [(-half_w + 4, -half_h), (-half_w + 4, half_h)]
    spine_pts   = [(int(cx + lx * cos_a - ly * sin_a),
                    int(cy + lx * sin_a + ly * cos_a))
                   for (lx, ly) in spine_local]
    draw.line(spine_pts, fill=(max(0, color[0]-40), max(0, color[1]-40),
                                max(0, color[2]-40)), width=2)


def draw_rubber_duck(draw, cx, cy, scale=1.0):
    """Simple rubber duck silhouette: body + head + beak."""
    bw = int(24 * scale)
    bh = int(18 * scale)
    hr = int(11 * scale)
    # Body (ellipse)
    draw.ellipse([cx - bw, cy - bh // 2, cx + bw, cy + bh // 2],
                 fill=RUBBER_DUCK)
    # Head (smaller ellipse, offset up-right)
    hx = cx + int(bw * 0.55)
    hy = cy - bh // 2 - int(hr * 0.4)
    draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=RUBBER_DUCK)
    # Beak
    beak_pts = [
        (hx + hr - 2, hy),
        (hx + hr + int(9 * scale), hy - int(4 * scale)),
        (hx + hr + int(9 * scale), hy + int(4 * scale)),
    ]
    draw.polygon(beak_pts, fill=RUBBER_BEAK)
    # Eye dot
    draw.ellipse([hx + 2, hy - 3, hx + 6, hy + 1], fill=VOID_BLACK)


def draw_panel():
    # ── Base canvas ───────────────────────────────────────────────────────────
    img  = Image.new('RGB', (PW, PH), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # ── Background: warm den wall + floor ─────────────────────────────────────
    horizon_y = int(DRAW_H * 0.62)

    # Wall fill
    draw.rectangle([0, 0, PW, horizon_y], fill=WALL_WARM)
    # Floor fill
    draw.rectangle([0, horizon_y, PW, DRAW_H], fill=FLOOR_WARM)

    # Floor planks (horizontal lines)
    for py in range(horizon_y + 6, DRAW_H, 18):
        draw.line([(0, py), (PW, py)],
                  fill=(max(0, FLOOR_WARM[0] - 20), max(0, FLOOR_WARM[1] - 22),
                         max(0, FLOOR_WARM[2] - 16)), width=1)

    # Warm ambient from upper-left (desk lamp source)
    add_glow(img, int(PW * 0.05), int(DRAW_H * 0.10), int(PW * 0.6),
             SUNLIT_AMB, steps=10, max_alpha=24)
    draw = ImageDraw.Draw(img)

    # ── Bookshelf — upper-right ───────────────────────────────────────────────
    # Shelf frame: 3 shelves visible, right side of frame
    shelf_x0  = int(PW * 0.52)
    shelf_x1  = int(PW * 0.98)
    shelf_top = int(DRAW_H * 0.04)
    shelf_bot = int(DRAW_H * 0.72)
    shelf_w   = 10

    # Back wall of shelf (slightly darker)
    draw.rectangle([shelf_x0 + shelf_w, shelf_top, shelf_x1 - shelf_w, shelf_bot],
                   fill=(168, 148, 116))

    # 3 shelf boards
    shelf_ys = [
        int(DRAW_H * 0.22),
        int(DRAW_H * 0.44),
        int(DRAW_H * 0.66),
    ]
    for sy in shelf_ys:
        draw.rectangle([shelf_x0, sy, shelf_x1, sy + shelf_w], fill=SHELF_WOOD)
        draw.line([(shelf_x0, sy + shelf_w), (shelf_x1, sy + shelf_w)],
                  fill=SHELF_SHADOW, width=2)

    # Vertical sides of shelf
    draw.rectangle([shelf_x0, shelf_top, shelf_x0 + shelf_w, shelf_bot],
                   fill=SHELF_WOOD)
    draw.rectangle([shelf_x1 - shelf_w, shelf_top, shelf_x1, shelf_bot],
                   fill=SHELF_WOOD)

    # Books packed on shelves (intact rows — some displaced by impact)
    # Top shelf: some books still standing, 2 gaps where books were
    def pack_shelf_row(shelf_surface_y, row_height, x_start, x_end, omit_slots=None):
        """Fill a shelf row with books sitting ON shelf_surface_y.
        row_height: vertical space above the shelf board available for books.
        Books sit with bottom at shelf_surface_y, top at shelf_surface_y - book_h."""
        omit_slots = omit_slots or []
        slot_w     = 22
        x          = x_start + 4
        slot_idx   = 0
        while x + slot_w <= x_end - 4:
            if slot_idx not in omit_slots:
                color = BOOK_COLORS[slot_idx % len(BOOK_COLORS)]
                bw = slot_w - RNG.randint(0, 4)
                # Book height: 60–90% of available row height
                bh = max(8, int(row_height * RNG.uniform(0.65, 0.90)))
                by_bottom = shelf_surface_y      # sits on shelf
                by_top    = by_bottom - bh
                draw.rectangle([x, by_top, x + bw, by_bottom], fill=color)
                draw.line([(x, by_top), (x + bw, by_top)],
                          fill=(max(0, color[0]-20), max(0, color[1]-20),
                                max(0, color[2]-20)), width=2)
            x        += slot_w + 1
            slot_idx += 1

    # Row heights: distance between shelf boards
    row0_h = shelf_ys[0] - shelf_top - shelf_w   # top-shelf row height
    row1_h = shelf_ys[1] - shelf_ys[0] - shelf_w
    row2_h = shelf_ys[2] - shelf_ys[1] - shelf_w

    # Top shelf: 3 books missing (impact zone) — gaps at slots 3, 4, 5
    pack_shelf_row(shelf_ys[0], row0_h,
                   shelf_x0 + shelf_w, shelf_x1 - shelf_w,
                   omit_slots=[3, 4, 5])
    # Middle shelf: full
    pack_shelf_row(shelf_ys[1], row1_h,
                   shelf_x0 + shelf_w, shelf_x1 - shelf_w)
    # Bottom shelf: full
    pack_shelf_row(shelf_ys[2], row2_h,
                   shelf_x0 + shelf_w, shelf_x1 - shelf_w)

    # ── AIRBORNE books (the 3 displaced) ─────────────────────────────────────
    # Launched from the gap on top shelf — tumbling into frame center / left
    airborne_books = [
        # (cx, cy, w, h, color, tilt)
        (int(PW * 0.44), int(DRAW_H * 0.16), 20, 32, BOOK_COLORS[3], -38),
        (int(PW * 0.34), int(DRAW_H * 0.22), 22, 30, BOOK_COLORS[0], 55),
        (int(PW * 0.40), int(DRAW_H * 0.30), 18, 28, BOOK_COLORS[4], -20),
    ]
    for (bx, by, bw, bh, bcol, btilt) in airborne_books:
        draw_book(draw, bx, by, bw, bh, bcol, tilt_deg=btilt)
    draw = ImageDraw.Draw(img)

    # ── RUBBER DUCK (airborne, upper-center) ─────────────────────────────────
    duck_cx = int(PW * 0.31)
    duck_cy = int(DRAW_H * 0.12)
    draw_rubber_duck(draw, duck_cx, duck_cy, scale=1.1)
    draw = ImageDraw.Draw(img)

    # ── Multi-exposure Byte PIXEL TRAIL (ricochet arc) ────────────────────────
    # Arc: from lower-left origin → upper-right impact point (top of bookshelf)
    # 5 ghost silhouettes along the arc at decreasing opacity (motion blur grammar)
    impact_cx = int(PW * 0.60)
    impact_cy = int(DRAW_H * 0.15)
    origin_cx = int(PW * 0.08)
    origin_cy = int(DRAW_H * 0.68)

    # Bezier arc control point (high arc)
    ctrl_x = int(PW * 0.25)
    ctrl_y = int(DRAW_H * -0.08)   # above frame — high arc

    num_ghosts = 5
    for gi in range(num_ghosts):
        t = gi / (num_ghosts - 1)   # 0.0 = origin, 1.0 = impact
        # Quadratic Bezier position
        gx = int((1-t)**2 * origin_cx + 2*(1-t)*t * ctrl_x + t**2 * impact_cx)
        gy = int((1-t)**2 * origin_cy + 2*(1-t)*t * ctrl_y + t**2 * impact_cy)
        # Alpha: fades from nearly invisible at origin → solid at impact
        alpha_f = 0.15 + 0.85 * t
        scale   = 0.7 + 0.3 * t    # gets larger as it gets closer (TENSE energy)

        draw_byte_silhouette(draw, gx, gy, scale=scale,
                              alpha_factor=alpha_f, img=img)
        draw = ImageDraw.Draw(img)

    # Draw arc arrow line (trajectory guide — storyboard annotation)
    arc_pts = []
    for step in range(20):
        t  = step / 19
        ax = int((1-t)**2 * origin_cx + 2*(1-t)*t * ctrl_x + t**2 * impact_cx)
        ay = int((1-t)**2 * origin_cy + 2*(1-t)*t * ctrl_y + t**2 * impact_cy)
        arc_pts.append((ax, ay))
    for i in range(len(arc_pts) - 1):
        draw.line([arc_pts[i], arc_pts[i+1]], fill=(*ELEC_CYAN_DIM, ), width=1)

    # Arrow head at impact
    draw.polygon([
        (impact_cx - 6, impact_cy + 12),
        (impact_cx + 6, impact_cy + 12),
        (impact_cx, impact_cy + 2),
    ], fill=ELEC_CYAN_DIM)

    # ── Confetti from impact — scattered, chaotic (TENSE density) ─────────────
    for _ in range(28):
        px = RNG.randint(int(PW * 0.35), int(PW * 0.85))
        py = RNG.randint(int(DRAW_H * 0.04), int(DRAW_H * 0.55))
        sz = RNG.choice([2, 4, 4, 8])
        draw.rectangle([px, py, px + sz, py + sz], fill=ELEC_CYAN)

    # ── Glow from Byte at impact point ────────────────────────────────────────
    add_glow(img, impact_cx, impact_cy, 80, ELEC_CYAN, steps=8, max_alpha=38)
    draw = ImageDraw.Draw(img)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann = load_font(9)
    font_sm  = load_font(8)

    # Camera note
    draw.text((8, 8), "FIXED CAM — 5ft  |  DUTCH 12° CW",
              font=font_ann, fill=ANN_COLOR)

    # Ricochet arc label
    draw.text((int(PW * 0.12), int(DRAW_H * 0.35)),
              "RICOCHET ARC →", font=font_ann, fill=ELEC_CYAN_DIM)
    draw.text((int(PW * 0.12), int(DRAW_H * 0.35) + 11),
              "multi-exposure trail", font=font_sm, fill=(80, 130, 140))

    # Airborne books label
    draw.text((int(PW * 0.22), int(DRAW_H * 0.27)),
              "BOOKS AIRBORNE", font=font_ann, fill=ANN_COLOR)
    draw.line([(int(PW * 0.30), int(DRAW_H * 0.25)),
               (int(PW * 0.42), int(DRAW_H * 0.22))],
              fill=ANN_COLOR, width=1)

    # Rubber duck label
    draw.text((duck_cx + 30, duck_cy - 12),
              "RUBBER DUCK", font=font_sm, fill=(190, 160, 60))

    # Impact star burst (simple radial lines from impact)
    for ang_deg in range(0, 360, 45):
        ang = math.radians(ang_deg)
        x0  = impact_cx + int(22 * math.cos(ang))
        y0  = impact_cy + int(22 * math.sin(ang))
        x1  = impact_cx + int(36 * math.cos(ang))
        y1  = impact_cy + int(36 * math.sin(ang))
        draw.line([(x0, y0), (x1, y1)], fill=ELEC_CYAN, width=2)

    # ── Apply Dutch tilt to draw area only (caption stays horizontal) ─────────
    draw_crop = img.crop([0, 0, PW, DRAW_H])
    draw_crop  = draw_crop.rotate(-12, expand=False, fillcolor=DEEP_SPACE)
    img.paste(draw_crop, (0, 0))
    draw = ImageDraw.Draw(img)

    # ── Three-tier caption bar ────────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    # Tier 1 — Shot code
    draw.text((10, DRAW_H + 4),
              "P14  |  MED  |  FIXED CAM  |  DUTCH 12° CW",
              font=font_t1, fill=TEXT_SHOT)

    # Tier 2 — Arc label
    draw.text((PW - 188, DRAW_H + 5),
              "ARC: TENSE", font=font_t2, fill=TEXT_ARC)

    # Tier 3 — Narrative description
    draw.text((10, DRAW_H + 22),
              "Byte ricochets off bookshelf. Multi-exposure pixel trail shows full arc.",
              font=font_t3, fill=TEXT_DESC)

    draw.text((10, DRAW_H + 35),
              "Books + rubber duck airborne. Dutch 12° CW. Chaos escalation.",
              font=font_t3, fill=(120, 112, 90))

    # Metadata
    draw.text((PW - 276, DRAW_H + 56),
              "LTG_SB_cold_open_P14  /  Diego Vargas  /  C45",
              font=font_meta, fill=TEXT_META)

    # Arc border — HOT_MAGENTA (TENSE)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    draw_panel()
    print("P14 standalone panel generation complete.")
    print("Beat: Byte ricochets off bookshelf — multi-exposure trail, books airborne.")
    print("Dutch tilt 12° CW applied to draw area only; caption horizontal.")
