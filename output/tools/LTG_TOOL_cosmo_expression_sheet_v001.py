#!/usr/bin/env python3
"""
LTG_TOOL_cosmo_expression_sheet_v001.py
Cosmo Expression Sheet Generator — "Luma & the Glitchkin"

Cycle 14: First expression sheet for Cosmo (best friend / sidekick).
Required by Act 2 storyboard: A2-05b and A2-06 need Cosmo emotional range.

Cycle 16 fixes (Maya Santos — Dmitri critique response):
  - SKEPTICAL body_tilt: -3 → +6 (backward lean, body-language anchor for thumbnail legibility)
  - Populated 2 empty expression slots:
      5. WORRIED — A2-02: watching Byte's vulnerable cracked-eye moment (background figure)
      6. SURPRISED — A2-04c: energy drink cans all pop simultaneously (chaos beat)

Expressions (6 — sheet fully populated):
  1. NEUTRAL / OBSERVING      — default resting: watching, waiting, notebook tucked
  2. FRUSTRATED / DEFEATED    — A2-06 payoff: plan failed, notebook closing
  3. DETERMINED               — A2-05b setup: app running, this will work
  4. SKEPTICAL / ONE-BROW-UP  — A2-03 reaction to Luma's plan: I have concerns
  5. WORRIED                  — A2-02: watching Byte exposition with concern
  6. SURPRISED                — A2-04c: carbonation chaos pop

Cosmo anatomy (from cosmo.md v2.0):
  - Head: tall rounded rectangle (h:w = 1.16:1, corner_r = 0.12 head units)
  - Glasses: two large circles, frame thickness = 0.06 head width, 7-degree CCW tilt (NEUTRAL)
  - Hair: flat blue-black cap, center-right part, cowlick at crown
  - Body: narrow upright rectangle (4.0 heads tall total)
  - Shirt: horizontal cerulean/sage stripes
  - Notebook: always tucked under left arm (canonical accessory)
  - Shoes: brown espresso lace-ups
  - Body variation mandatory (Cycle 6 Marcus Webb rule)

Color spec (from cosmo.md):
  - Skin: #D9C09A base, #B89A78 shadow, #EED4B0 highlight
  - Hair: #1A1824 base, #0E0E18 shadow, #2C2B40 highlight
  - Glasses frame: #5C3A20 (Warm Espresso)
  - Lens tint: #EEF4FF, glare: #F0F0F0
  - Iris (through glass): #3D6B45 (Warm Forest Green)
  - Shirt stripe A: #5B8DB8 (Cerulean Blue)
  - Shirt stripe B: #7A9E7E (Sage Green)
  - Pants: #8C8880 (Warm Mid-Gray)
  - Shoes: #5C3A20 (Warm Espresso)
  - Notebook cover: #5B8DB8 (Cerulean Blue)
  - Line: #3B2820 (Deep Cocoa)

Character-over-background saturation rule: character colors more saturated than panel BG.
"""
from PIL import Image, ImageDraw, ImageFont
import math

# ── Palette ───────────────────────────────────────────────────────────────────
SKIN        = (217, 192, 154)   # #D9C09A — base warm olive
SKIN_SH     = (184, 154, 120)   # #B89A78 — shadow
SKIN_HL     = (238, 212, 176)   # #EED4B0 — highlight
HAIR        = (26, 24, 36)      # #1A1824 — blue-black
HAIR_SH     = (14, 14, 24)      # #0E0E18 — near-void
HAIR_HL     = (44, 43, 64)      # #2C2B40 — dark slate
EYE_WHITE   = (250, 240, 220)   # #FAF0DC — warm cream
IRIS        = (61, 107, 69)     # #3D6B45 — warm forest green
PUPIL       = (59, 40, 32)      # #3B2820 — deep cocoa
EYE_HL      = (240, 240, 240)   # #F0F0F0 — static white
GLASS_FRAME = (92, 58, 32)      # #5C3A20 — warm espresso
GLASS_LENS  = (238, 244, 255)   # #EEF4FF — ghost blue
GLASS_GLARE = (240, 240, 240)   # #F0F0F0
STRIPE_A    = (91, 141, 184)    # #5B8DB8 — cerulean blue
STRIPE_B    = (122, 158, 126)   # #7A9E7E — sage green
PANTS       = (140, 136, 128)   # #8C8880 — warm mid-gray
PANTS_SH    = (106, 100, 96)    # #6A6460 — mid-dark gray
SHOE        = (92, 58, 32)      # #5C3A20 — warm espresso (matches glasses)
SHOE_SOLE   = (184, 154, 120)   # #B89A78 — warm sand
NOTEBOOK    = (91, 141, 184)    # #5B8DB8 — cerulean blue
NOTEBOOK_SP = (61, 107, 138)    # #3D6B8A — deep cerulean (spine)
LINE        = (59, 40, 32)      # #3B2820 — deep cocoa
BLUSH       = (210, 128, 80)    # blush — appears in embarrassment only

# Panel backgrounds — low saturation, character reads above them
BG_NEUTRAL  = (210, 208, 200)   # warm light grey — resting baseline
BG_FRUSTRAT = (200, 192, 195)   # cool-warm grey — defeated low energy
BG_DETERMIN = (195, 210, 218)   # cool blue-grey — focused, pre-action
BG_SKEPTIC  = (205, 210, 200)   # neutral sage-grey — skeptical calm
BG_WORRIED  = (196, 200, 208)   # cool grey-blue — anxiety, watching the hard thing
BG_SURPRISED = (214, 208, 198)  # warm neutral — startled energy, not danger

CANVAS_BG   = (28, 24, 20)      # dark card background

# ── Layout ────────────────────────────────────────────────────────────────────
PANEL_W     = 280
PANEL_H     = 420
COLS        = 3
ROWS        = 2
PAD         = 18
HEADER      = 52

# ── Expression definitions ────────────────────────────────────────────────────
# Each entry: (name, body_data, panel_bg, glasses_tilt, brow_data, mouth_data,
#              prev_state, next_state)
#
# body_data keys:
#   arm_l_dy      — left arm vertical offset from neutral (down=positive)
#   arm_r_dy      — right arm vertical offset
#   body_tilt     — torso lean (negative = lean forward/left)
#   notebook_show — True/False (notebook under left arm)
#   notebook_open — True (held out) / False (tucked tight)
#
# brow_data keys:
#   l_raise  — left brow (viewer's right) raise amount in px
#   r_raise  — right brow raise amount
#   l_furrow — left brow inner-corner depression
#   r_furrow — right brow inner-corner depression
#
# mouth_data keys:
#   style — 'neutral'|'slight_smile'|'flat'|'grimace'|'compressed'|'open_determined'

EXPRESSIONS = [
    # ── NEUTRAL / OBSERVING ────────────────────────────────────────────────────
    # Cosmo at rest: watching and cataloguing. Notebook tucked. Brows horizontal.
    # Mouth: expectant patience — barely-there uptick at corners.
    # Glasses: canonical 7° CCW tilt. Arms hanging at sides, relaxed.
    {
        "name":     "NEUTRAL / OBSERVING",
        "body_data": {
            "arm_l_dy": 0, "arm_r_dy": 0,
            "body_tilt": 0, "body_squash": 1.0,
            "notebook_show": True, "notebook_open": False,
        },
        "panel_bg": BG_NEUTRAL,
        "glasses_tilt": 7,
        "brow_data": {"l_raise": 0, "r_raise": 0, "l_furrow": 0, "r_furrow": 0},
        "mouth_data": {"style": "neutral"},
        "blush": False,
        "prev_state": "← was: ANY STATE",
        "next_state": "→ next: SKEPTICAL / ALARMED",
    },
    # ── FRUSTRATED / DEFEATED ─────────────────────────────────────────────────
    # A2-06: Plan failed. App didn't work. Notebook being closed.
    # Body: slumped shoulders (arm_l_dy high — arm droops), slight forward lean.
    # Brows: both pulled down slightly, inner corners slightly raised (not angry — sad).
    # Mouth: compressed flat line — swallowed disappointment.
    # Glasses: tilt increases to 10° (emotional tilt rule).
    # Notebook: held in both hands (open, being closed) — pivotal Cosmo beat.
    {
        "name":     "FRUSTRATED / DEFEATED",
        "body_data": {
            "arm_l_dy": 20, "arm_r_dy": 12,
            "body_tilt": 4, "body_squash": 0.96,
            "notebook_show": True, "notebook_open": True,
        },
        "panel_bg": BG_FRUSTRAT,
        "glasses_tilt": 10,
        "brow_data": {"l_raise": -3, "r_raise": -3, "l_furrow": 4, "r_furrow": 4},
        "mouth_data": {"style": "compressed"},
        "blush": False,
        "prev_state": "← was: DETERMINED",
        "next_state": "→ next: RESIGNED / RECALIBRATING",
    },
    # ── DETERMINED ────────────────────────────────────────────────────────────
    # A2-05b: App running, Cosmo believes this will work.
    # Body: upright, slight lean forward (engaged). Right arm up — holding phone out.
    # Left arm slightly down (counterbalance). Notebook tucked.
    # Brows: slight focused furrow, level — not angry, concentrating.
    # Mouth: small contained line with the faintest pull toward slight smile — not there yet.
    # Glasses: 7° base tilt (neutral state — he's in control here).
    {
        "name":     "DETERMINED",
        "body_data": {
            "arm_l_dy": 8, "arm_r_dy": -30,
            "body_tilt": -5, "body_squash": 1.0,
            "notebook_show": True, "notebook_open": False,
        },
        "panel_bg": BG_DETERMIN,
        "glasses_tilt": 7,
        "brow_data": {"l_raise": 2, "r_raise": 2, "l_furrow": 2, "r_furrow": 2},
        "mouth_data": {"style": "slight_smile"},
        "blush": False,
        "prev_state": "← was: NEUTRAL / OBSERVING",
        "next_state": "→ next: FRUSTRATED or SUCCEEDED",
    },
    # ── SKEPTICAL / ONE-BROW-UP ───────────────────────────────────────────────
    # A2-03: Watching Luma's plan on the whiteboard. Classic Cosmo signature move:
    # left brow (viewer's right) shoots up, right brow holds flat.
    # Body: BACKWARD lean (+6° tilt) — Cycle 16 fix (Dmitri: body-language anchor for squint test).
    #   Previous body_tilt=-3 (barely forward) was face-only expression, didn't read at thumbnail.
    #   +6 backward = leaning away from the board, skeptical containment posture.
    # Arms: slightly raised / crossed (containment). Notebook tucked.
    # Glasses: 9° tilt. Mouth: perfectly flat — deadpan. The "I told you so" setup.
    {
        "name":     "SKEPTICAL",
        "body_data": {
            "arm_l_dy": -8, "arm_r_dy": -5,
            "body_tilt": 6, "body_squash": 1.0,   # Cycle 16: -3→+6 backward lean
            "notebook_show": True, "notebook_open": False,
        },
        "panel_bg": BG_SKEPTIC,
        "glasses_tilt": 9,
        "brow_data": {"l_raise": 18, "r_raise": 0, "l_furrow": 0, "r_furrow": 1},
        "mouth_data": {"style": "flat"},
        "blush": False,
        "prev_state": "← was: NEUTRAL / OBSERVING",
        "next_state": "→ next: RESIGNED / PREPARING ANYWAY",
    },
    # ── WORRIED ───────────────────────────────────────────────────────────────
    # NEW Cycle 16 — A2-02: Byte MCU, Cosmo is background blur watching Byte's
    # vulnerable cracked-eye moment. Expression: genuine concern, not fear.
    # He knows what this costs Byte. He cares more than he usually admits.
    # Body: slight forward lean (-4°), arms drawn close (hugging himself slightly),
    #   notebook tucked tight (not used here — this is an emotional moment).
    # Brows: both raised at inner corners (corrugator kink = worry, not aggression).
    #   Outer brow: level. Inner corners: pulled up = "genuine concern" geometry.
    # Glasses tilt: 8° (slight increase from 7° neutral — emotional perturbation).
    # Mouth: flat + slightly compressed — not grimace, just... holding it together.
    {
        "name":     "WORRIED",
        "body_data": {
            "arm_l_dy": 6, "arm_r_dy": 6,
            "body_tilt": -4, "body_squash": 0.98,
            "notebook_show": True, "notebook_open": False,
        },
        "panel_bg": BG_WORRIED,
        "glasses_tilt": 8,
        "brow_data": {"l_raise": 6, "r_raise": 6, "l_furrow": 8, "r_furrow": 8},
        "mouth_data": {"style": "compressed"},
        "blush": False,
        "prev_state": "← was: NEUTRAL / SKEPTICAL",
        "next_state": "→ next: FRUSTRATED / TRYING ANYWAY",
    },
    # ── SURPRISED ─────────────────────────────────────────────────────────────
    # NEW Cycle 16 — A2-04c: All energy drink cans pop simultaneously. Carbonated
    # spray everywhere. Cosmo did NOT see this coming. Not dangerous — just chaotic.
    # Body: slight backward startle lean (+5°), arms snapped up instinctively (high),
    #   notebook open (he had it out for the plan).
    # Brows: BOTH fully raised — symmetrically (surprise = bilateral, not skeptical).
    # Glasses tilt: 10° (peak emotional tilt — Cosmo is maximally disrupted).
    # Mouth: small open oval — the "oh no" pause before the laugh.
    {
        "name":     "SURPRISED",
        "body_data": {
            "arm_l_dy": -18, "arm_r_dy": -22,
            "body_tilt": 5, "body_squash": 0.97,
            "notebook_show": True, "notebook_open": True,
        },
        "panel_bg": BG_SURPRISED,
        "glasses_tilt": 10,
        "brow_data": {"l_raise": 16, "r_raise": 16, "l_furrow": 0, "r_furrow": 0},
        "mouth_data": {"style": "open_surprised"},
        "blush": False,
        "prev_state": "← was: DETERMINED (plan in action)",
        "next_state": "→ next: FRUSTRATED / ACCEPTING CHAOS",
    },
]


# ── Drawing helpers ───────────────────────────────────────────────────────────

def _draw_cosmo_head(draw, cx, cy, hu):
    """Draw Cosmo's tall rounded-rectangle head.

    Head proportions: height = hu, width = hu * 0.86, corner_r = hu * 0.12
    Per cosmo.md: at 0.12 corner radius top/bottom read as rectangular at distance.
    """
    hw = int(hu * 0.43)   # half-width
    hh = int(hu * 0.50)   # half-height
    r  = int(hu * 0.12)   # corner radius
    # Rounded rectangle via polygon+arcs (PIL rounded_rectangle if available, else manual)
    try:
        draw.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh],
                                radius=r, fill=SKIN, outline=LINE, width=2)
    except AttributeError:
        # Fallback for older PIL: approximate with ellipse + rectangle combination
        draw.rectangle([cx - hw + r, cy - hh, cx + hw - r, cy + hh], fill=SKIN)
        draw.rectangle([cx - hw, cy - hh + r, cx + hw, cy + hh - r], fill=SKIN)
        for (ox, oy) in [(cx - hw + r, cy - hh + r), (cx + hw - r, cy - hh + r),
                         (cx - hw + r, cy + hh - r), (cx + hw - r, cy + hh - r)]:
            draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=SKIN)
        # Outline
        draw.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh],
                                radius=r, outline=LINE, width=2)


def _draw_cosmo_hair(draw, cx, cy, hu):
    """Flat hair cap — blue-black, center-right part, cowlick at crown.

    Hair adds ~0.05 hu above skull line. Flat — almost no width contribution.
    """
    hw = int(hu * 0.43)
    hh = int(hu * 0.50)
    # Main hair cap (flat trapezoid-ish shape above skull)
    hair_top = cy - hh - int(hu * 0.05)
    hair_bot = cy - hh + int(hu * 0.15)
    # Left side slightly thicker (part is right of center, viewer's left)
    draw.ellipse([cx - hw - 2, hair_top, cx + int(hw * 0.2), hair_bot + 6],
                 fill=HAIR)
    draw.ellipse([cx - int(hw * 0.2), hair_top + 2, cx + hw + 2, hair_bot + 4],
                 fill=HAIR)
    # Part line (light gap) — right of center
    part_x = cx + int(hw * 0.12)
    draw.line([(part_x, hair_top + 4), (part_x, hair_bot)], fill=SKIN, width=2)
    # Cowlick — small forward-curling arc at crown
    cowlick_x = cx + int(hw * 0.05)
    cowlick_y = hair_top
    draw.arc([cowlick_x - int(hu * 0.07), cowlick_y - int(hu * 0.05),
              cowlick_x + int(hu * 0.07), cowlick_y + int(hu * 0.08)],
             start=280, end=80, fill=HAIR_HL, width=3)
    # Hair highlight (restrained — single arc on crown)
    draw.arc([cx - int(hw * 0.6), hair_top + 2, cx + int(hw * 0.6), hair_top + int(hu * 0.12)],
             start=200, end=340, fill=HAIR_HL, width=2)


def _draw_cosmo_glasses(draw, cx, cy, hu, tilt_deg):
    """Draw Cosmo's defining glasses element.

    Two circular lenses + nose bridge. Frame thickness = 0.06 hu.
    Lens diameter = 0.32 hu each. Eyes are magnified (1.25x) through lenses.
    Canonical tilt: 7° CCW (neutral). Increases to 10° frustrated, 9° skeptical.

    Glasses tilt: applied as a rotation around the nose bridge center.
    Per cosmo.md: NEVER draw at 0° — even neutral = 7°.
    """
    lens_r  = int(hu * 0.16)          # lens radius (0.32 hu diameter)
    frame_w = max(3, int(hu * 0.06))   # frame thickness
    bridge  = int(hu * 0.05)           # nose bridge gap half-width
    eye_sep = lens_r + bridge          # center-to-center half distance

    # Rotation math — tilt around bridge center (cx, cy_glasses)
    # Glasses sit at eye level: cy - 0.10 hu from face center
    gcy = cy - int(hu * 0.10)
    theta = math.radians(-tilt_deg)   # negative = CCW
    cos_t, sin_t = math.cos(theta), math.sin(theta)

    def rot(dx, dy):
        """Rotate offset (dx,dy) by tilt_deg CCW around glasses center."""
        return (int(cx + dx * cos_t - dy * sin_t),
                int(gcy + dx * sin_t + dy * cos_t))

    # Lens centers (left and right in glasses space)
    lcx, lcy = rot(-eye_sep, 0)
    rcx, rcy = rot(+eye_sep, 0)

    # Draw lenses (fill first, then frame)
    draw.ellipse([lcx - lens_r, lcy - lens_r, lcx + lens_r, lcy + lens_r],
                 fill=GLASS_LENS)
    draw.ellipse([rcx - lens_r, rcy - lens_r, rcx + lens_r, rcy + lens_r],
                 fill=GLASS_LENS)

    # Lens glare — thin crescent at top of each lens
    gl_r = int(lens_r * 0.7)
    draw.arc([lcx - gl_r, lcy - lens_r + 2, lcx + gl_r, lcy - lens_r + int(lens_r * 0.5)],
             start=200, end=340, fill=GLASS_GLARE, width=2)
    draw.arc([rcx - gl_r, rcy - lens_r + 2, rcx + gl_r, rcy - lens_r + int(lens_r * 0.5)],
             start=200, end=340, fill=GLASS_GLARE, width=2)

    # Draw frames (thick circle outline)
    draw.ellipse([lcx - lens_r, lcy - lens_r, lcx + lens_r, lcy + lens_r],
                 outline=GLASS_FRAME, width=frame_w)
    draw.ellipse([rcx - lens_r, rcy - lens_r, rcx + lens_r, rcy + lens_r],
                 outline=GLASS_FRAME, width=frame_w)

    # Nose bridge — short bar connecting inner edges
    bridge_l = rot(-bridge, 0)
    bridge_r = rot(+bridge, 0)
    draw.line([bridge_l, bridge_r], fill=GLASS_FRAME, width=frame_w)

    # Temple arms — short lines extending outward from outer lens edges
    l_temple_start = rot(-eye_sep - lens_r, 0)
    l_temple_end   = rot(-eye_sep - lens_r - int(hu * 0.06), int(hu * 0.02))
    r_temple_start = rot(+eye_sep + lens_r, 0)
    r_temple_end   = rot(+eye_sep + lens_r + int(hu * 0.06), int(hu * 0.02))
    draw.line([l_temple_start, l_temple_end], fill=GLASS_FRAME, width=max(2, frame_w - 1))
    draw.line([r_temple_start, r_temple_end], fill=GLASS_FRAME, width=max(2, frame_w - 1))

    return lcx, lcy, rcx, rcy, lens_r


def _draw_cosmo_eyes(draw, lcx, lcy, rcx, rcy, lens_r):
    """Draw magnified eyes visible through lenses (1.25x normal size).

    Highlight: upper-right position (opposite to Luma's upper-left — subtle distinction).
    Lower lid: straight-ish horizontal line — more 'observing' than 'wondering'.
    """
    iris_r = int(lens_r * 0.55)   # magnified iris
    pup_r  = int(iris_r * 0.55)

    for (ex, ey) in [(lcx, lcy), (rcx, rcy)]:
        # Eye white
        draw.ellipse([ex - iris_r - 4, ey - iris_r - 4,
                      ex + iris_r + 4, ey + iris_r + 4], fill=EYE_WHITE)
        # Iris
        draw.ellipse([ex - iris_r, ey - iris_r, ex + iris_r, ey + iris_r], fill=IRIS)
        # Pupil
        draw.ellipse([ex - pup_r, ey - pup_r, ex + pup_r, ey + pup_r], fill=PUPIL)
        # Highlight — upper-RIGHT per cosmo.md
        hl_r = max(2, int(iris_r * 0.28))
        draw.ellipse([ex + int(iris_r * 0.3), ey - iris_r + 2,
                      ex + int(iris_r * 0.3) + hl_r * 2, ey - iris_r + 2 + hl_r * 2],
                     fill=EYE_HL)
        # Flat lower lid line — Cosmo's 'observing' eye character
        draw.line([(ex - iris_r - 3, ey + int(iris_r * 0.5)),
                   (ex + iris_r + 3, ey + int(iris_r * 0.5))],
                  fill=LINE, width=2)


def _draw_cosmo_nose(draw, cx, cy, hu):
    """Simple button nose — slightly larger than Luma's (0.1 hu vs 0.08)."""
    nose_r = int(hu * 0.05)
    draw.ellipse([cx - nose_r, cy + int(hu * 0.06),
                  cx + nose_r, cy + int(hu * 0.16)], fill=SKIN_SH)


def _draw_cosmo_brows(draw, cx, cy, hu, tilt_deg, brow_data, lcx, lcy, rcx, rcy):
    """Draw Cosmo's expressive brows above the glasses.

    l_raise: left brow raise in px (viewer's right — his more mobile brow).
    r_raise: right brow raise in px.
    l_furrow / r_furrow: inner-corner depression (worry pull-down).

    Brows sit ~lens_r + 0.06 hu above lens center.
    """
    lens_r  = int(hu * 0.16)
    brow_y_base = lcy - lens_r - int(hu * 0.06)

    l_raise  = brow_data.get("l_raise",  0)
    r_raise  = brow_data.get("r_raise",  0)
    l_furrow = brow_data.get("l_furrow", 0)
    r_furrow = brow_data.get("r_furrow", 0)

    brow_w = int(hu * 0.18)  # brow half-width
    brow_thick = max(3, int(hu * 0.028))

    # Left brow (viewer's right — Cosmo's mobile brow)
    l_inner_y = brow_y_base - l_raise - l_furrow   # inner raised by furrow = pulled down (compress)
    l_outer_y = brow_y_base - l_raise + l_furrow // 2
    l_pts = [
        (lcx - brow_w, l_outer_y),
        (lcx,          l_inner_y),
        (lcx + brow_w, l_outer_y + 2),
    ]
    draw.line(l_pts, fill=HAIR, width=brow_thick)

    # Right brow
    r_inner_y = brow_y_base - r_raise - r_furrow
    r_outer_y = brow_y_base - r_raise + r_furrow // 2
    r_pts = [
        (rcx - brow_w, r_outer_y + 2),
        (rcx,          r_inner_y),
        (rcx + brow_w, r_outer_y),
    ]
    draw.line(r_pts, fill=HAIR, width=brow_thick)


def _draw_cosmo_mouth(draw, cx, cy, hu, mouth_data):
    """Draw Cosmo's expression-specific mouth.

    Mouth sits at cy + 0.26 hu from face center.
    Styles:
      neutral        — straight line, barely-there uptick at corners (expectant patience)
      slight_smile   — small contained uptick, not dramatic (quietly pleased)
      flat           — perfectly flat line — deadpan I-told-you-so
      compressed     — flat but ends pulled slightly inward + downward — swallowed defeat
      grimace        — teeth-clenched stress (not used in current sheet but defined)
    """
    mouth_y = cy + int(hu * 0.26)
    mw = int(hu * 0.20)  # half-width
    style = mouth_data.get("style", "neutral")

    if style == "neutral":
        # Barely-there uptick at corners — waiting patience
        draw.line([(cx - mw, mouth_y), (cx + mw, mouth_y)], fill=LINE, width=2)
        draw.line([(cx - mw, mouth_y), (cx - mw + 4, mouth_y - 2)], fill=LINE, width=2)
        draw.line([(cx + mw, mouth_y), (cx + mw - 4, mouth_y - 2)], fill=LINE, width=2)

    elif style == "slight_smile":
        # Small contained arc — quietly pleased, not jubilant
        draw.arc([cx - mw, mouth_y - int(hu * 0.06),
                  cx + mw, mouth_y + int(hu * 0.06)],
                 start=10, end=170, fill=LINE, width=3)

    elif style == "flat":
        # Perfect flat line — deadpan (the "I told you so" power)
        draw.line([(cx - mw, mouth_y), (cx + mw, mouth_y)], fill=LINE, width=3)

    elif style == "compressed":
        # Flat line, corners pulled slightly down — swallowed disappointment
        draw.line([(cx - mw + 4, mouth_y - 1), (cx + mw - 4, mouth_y - 1)],
                  fill=LINE, width=3)
        draw.line([(cx - mw, mouth_y + 3), (cx - mw + 6, mouth_y - 2)],
                  fill=LINE, width=2)
        draw.line([(cx + mw, mouth_y + 3), (cx + mw - 6, mouth_y - 2)],
                  fill=LINE, width=2)

    elif style == "grimace":
        # Clenched — teeth strip with pressed lips above/below
        draw.rectangle([cx - mw + 4, mouth_y - 4, cx + mw - 4, mouth_y + 6],
                       fill=(245, 240, 232), outline=LINE, width=2)
        for i in range(4):
            tx = cx - mw + 8 + i * (int(mw * 0.45))
            draw.line([(tx, mouth_y - 4), (tx, mouth_y + 6)], fill=LINE, width=1)

    elif style == "open_surprised":
        # Small open oval — the "oh no" pause (SURPRISED A2-04c)
        # Not a fear-scream rectangle — small contained oval, jaw dropped slightly
        draw.ellipse([cx - int(mw * 0.55), mouth_y - 4,
                      cx + int(mw * 0.55), mouth_y + int(hu * 0.10)],
                     fill=(210, 180, 150), outline=LINE, width=2)


def _draw_cosmo_body(draw, cx, body_top_y, hu, body_data):
    """Draw Cosmo's full body: striped shirt, pants, shoes, notebook.

    Body proportions (from cosmo.md):
      - Torso height: 1.2 hu, width: 0.95 * head width = 0.95 * 0.86 * hu ≈ 0.82 hu
      - Shoulder width: 0.9 * head width ≈ 0.77 hu
      - Arms: straight cylinders, hang close to torso
      - Legs: longer thinner than Luma's
      - Notebook: tucked under left arm (viewer's right side of body)

    body_data keys: arm_l_dy, arm_r_dy, body_tilt, body_squash,
                    notebook_show, notebook_open
    """
    arm_l_dy     = body_data.get("arm_l_dy", 0)
    arm_r_dy     = body_data.get("arm_r_dy", 0)
    body_tilt    = body_data.get("body_tilt", 0)
    body_squash  = body_data.get("body_squash", 1.0)
    nb_show      = body_data.get("notebook_show", True)
    nb_open      = body_data.get("notebook_open", False)

    # Body geometry
    torso_hw = int(hu * 0.41)     # half-width of torso (slightly narrower than head)
    torso_h  = int(hu * 1.2 * body_squash)
    tilt_off = int(body_tilt * 0.4)

    torso_bot_y = body_top_y + torso_h

    # ── Torso (striped shirt) ────────────────────────────────────────────────
    # Draw solid shirt base first, then overlay stripes
    shirt_pts = [
        (cx - torso_hw + tilt_off, body_top_y),
        (cx + torso_hw + tilt_off, body_top_y),
        (cx + torso_hw,            torso_bot_y),
        (cx - torso_hw,            torso_bot_y),
    ]
    draw.polygon(shirt_pts, fill=STRIPE_A, outline=LINE, width=2)

    # Horizontal stripes (alternating A/B, equal width ~0.04 hu each)
    stripe_h = max(4, int(hu * 0.055))
    n_stripes = torso_h // stripe_h
    for i in range(n_stripes):
        if i % 2 == 0:
            continue   # blue (base) is already painted
        sy = body_top_y + i * stripe_h
        ey = min(sy + stripe_h, torso_bot_y)
        # Interpolate tilt across stripe vertical position
        t_frac = (sy - body_top_y) / max(1, torso_h)
        s_tilt = tilt_off * (1 - t_frac)
        sw_l = int(torso_hw - abs(s_tilt) * 0.1)
        stripe_pts = [
            (cx - sw_l + int(s_tilt), sy),
            (cx + sw_l + int(s_tilt), sy),
            (cx + sw_l,               ey),
            (cx - sw_l,               ey),
        ]
        draw.polygon(stripe_pts, fill=STRIPE_B)

    # Redraw outline over stripes
    draw.polygon(shirt_pts, outline=LINE, width=2)

    # Neck opening at top of shirt
    neck_w = int(hu * 0.10)
    draw.ellipse([cx - neck_w, body_top_y - int(hu * 0.04),
                  cx + neck_w, body_top_y + int(hu * 0.08)],
                 fill=SKIN)

    # ── Arms ────────────────────────────────────────────────────────────────
    arm_w  = int(hu * 0.12)
    arm_h  = int(hu * 0.75)
    arm_y  = body_top_y + int(hu * 0.06)

    # Left arm (viewer's right) — notebook side
    lax = cx - torso_hw + tilt_off - int(hu * 0.03)
    lay = arm_y + arm_l_dy
    draw.rectangle([lax - arm_w, lay, lax, lay + arm_h],
                   fill=STRIPE_A, outline=LINE, width=2)
    # Hand blob
    draw.ellipse([lax - arm_w - 6, lay + arm_h - 6,
                  lax + 4,         lay + arm_h + int(hu * 0.14)],
                 fill=SKIN, outline=LINE, width=2)

    # Right arm (viewer's left)
    rax = cx + torso_hw + tilt_off + int(hu * 0.03)
    ray = arm_y + arm_r_dy
    draw.rectangle([rax, ray, rax + arm_w, ray + arm_h],
                   fill=STRIPE_A, outline=LINE, width=2)
    # Hand blob
    draw.ellipse([rax - 4,         ray + arm_h - 6,
                  rax + arm_w + 6, ray + arm_h + int(hu * 0.14)],
                 fill=SKIN, outline=LINE, width=2)

    # ── Notebook (canonical — tucked under left arm, viewer's right) ─────────
    if nb_show:
        nb_h = int(hu * 0.30)
        nb_w = int(hu * 0.18)
        if nb_open:
            # Held in front — both hands visible, notebook out
            nb_x = cx - int(nb_w * 0.5)
            nb_y = torso_bot_y - int(hu * 0.55)
            draw.rectangle([nb_x, nb_y, nb_x + nb_w * 2, nb_y + nb_h],
                           fill=NOTEBOOK, outline=LINE, width=2)
            # Open pages (warm cream edge visible at center split)
            draw.line([(nb_x + nb_w, nb_y), (nb_x + nb_w, nb_y + nb_h)],
                      fill=(250, 240, 220), width=3)
            draw.line([(nb_x + nb_w, nb_y), (nb_x + nb_w, nb_y + nb_h)],
                      fill=LINE, width=1)
        else:
            # Tucked: narrow spine protrusion under left arm
            nb_tuck_x = cx - torso_hw - int(hu * 0.02)
            nb_tuck_y = arm_y + arm_l_dy + int(arm_h * 0.35)
            draw.rectangle([nb_tuck_x - nb_w, nb_tuck_y,
                            nb_tuck_x,        nb_tuck_y + nb_h],
                           fill=NOTEBOOK, outline=LINE, width=2)
            # Spine in shadow
            draw.rectangle([nb_tuck_x - 6, nb_tuck_y,
                            nb_tuck_x,     nb_tuck_y + nb_h],
                           fill=NOTEBOOK_SP)
            # Page edge
            draw.line([(nb_tuck_x - nb_w + 3, nb_tuck_y + 3),
                       (nb_tuck_x - nb_w + 3, nb_tuck_y + nb_h - 3)],
                      fill=(250, 240, 220), width=2)

    # ── Pants ────────────────────────────────────────────────────────────────
    leg_w  = int(hu * 0.16)
    leg_h  = int(hu * 0.90)   # longer legs than Luma
    leg_l  = cx - int(torso_hw * 0.42)
    leg_r  = cx + int(torso_hw * 0.42)
    leg_y  = torso_bot_y

    draw.rectangle([leg_l - leg_w, leg_y, leg_l + leg_w, leg_y + leg_h],
                   fill=PANTS, outline=LINE, width=2)
    # Center crease line — Cosmo has pressed his trousers
    draw.line([(leg_l, leg_y), (leg_l, leg_y + leg_h)], fill=PANTS_SH, width=1)

    draw.rectangle([leg_r - leg_w, leg_y, leg_r + leg_w, leg_y + leg_h],
                   fill=PANTS, outline=LINE, width=2)
    draw.line([(leg_r, leg_y), (leg_r, leg_y + leg_h)], fill=PANTS_SH, width=1)

    # ── Shoes (brown espresso lace-ups) ─────────────────────────────────────
    # Conservative, low-profile. Match glasses frames in color.
    shoe_w = int(hu * 0.28)
    shoe_h = int(hu * 0.18)
    shoe_y = leg_y + leg_h

    draw.ellipse([leg_l - leg_w - shoe_w + int(shoe_w * 0.3), shoe_y,
                  leg_l - leg_w + int(shoe_w * 0.4),           shoe_y + shoe_h],
                 fill=SHOE, outline=LINE, width=2)
    draw.arc([leg_l - leg_w - shoe_w + int(shoe_w * 0.35), shoe_y + 3,
              leg_l - leg_w + int(shoe_w * 0.35),           shoe_y + shoe_h - 3],
             start=200, end=340, fill=SHOE_SOLE, width=2)

    draw.ellipse([leg_r + leg_w - int(shoe_w * 0.4), shoe_y,
                  leg_r + leg_w + shoe_w - int(shoe_w * 0.3), shoe_y + shoe_h],
                 fill=SHOE, outline=LINE, width=2)
    draw.arc([leg_r + leg_w - int(shoe_w * 0.35), shoe_y + 3,
              leg_r + leg_w + shoe_w - int(shoe_w * 0.35), shoe_y + shoe_h - 3],
             start=200, end=340, fill=SHOE_SOLE, width=2)


def draw_cosmo(draw, cx, cy, hu, expr):
    """Draw one full Cosmo character at given position and head-unit scale.

    cy is the face center (vertical). Body grows downward from cy + hu/2 (neck base).
    """
    glasses_tilt = expr.get("glasses_tilt", 7)
    body_data    = expr.get("body_data", {})
    brow_data    = expr.get("brow_data", {})
    mouth_data   = expr.get("mouth_data", {"style": "neutral"})

    # ── Body (drawn FIRST — character-over-background saturation rule) ───────
    body_top_y = cy + int(hu * 0.55)   # top of shirt at neck base
    _draw_cosmo_body(draw, cx, body_top_y, hu, body_data)

    # ── Head ─────────────────────────────────────────────────────────────────
    _draw_cosmo_hair(draw, cx, cy, hu)
    _draw_cosmo_head(draw, cx, cy, hu)

    # ── Glasses (and get lens centers for eyes/brows) ─────────────────────────
    lcx, lcy, rcx, rcy, lens_r = _draw_cosmo_glasses(draw, cx, cy, hu, glasses_tilt)

    # ── Eyes ─────────────────────────────────────────────────────────────────
    _draw_cosmo_eyes(draw, lcx, lcy, rcx, rcy, lens_r)

    # ── Brows ─────────────────────────────────────────────────────────────────
    _draw_cosmo_brows(draw, cx, cy, hu, glasses_tilt, brow_data, lcx, lcy, rcx, rcy)

    # ── Nose ─────────────────────────────────────────────────────────────────
    _draw_cosmo_nose(draw, cx, cy, hu)

    # ── Mouth ─────────────────────────────────────────────────────────────────
    _draw_cosmo_mouth(draw, cx, cy, hu, mouth_data)


# ── Sheet generator ───────────────────────────────────────────────────────────

def generate_cosmo_expression_sheet(output_path):
    """Render 3×2 expression grid for Cosmo. 6 expressions — fully populated (Cycle 16)."""
    total_w = COLS * (PANEL_W + PAD) + PAD
    total_h = HEADER + ROWS * (PANEL_H + PAD) + PAD

    img  = Image.new('RGB', (total_w, total_h), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font       = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        font_sm    = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font_title = font = font_sm = ImageFont.load_default()

    # Sheet header
    draw.text((PAD, 14),
              "COSMO — Expression Sheet — Luma & the Glitchkin  |  v001  |  Cycle 16",
              fill=(91, 141, 184), font=font_title)

    # Head unit for panel rendering — character renders at ~55% of panel height
    # PANEL_H = 420. Face center at panel_center_y. hu = PANEL_H * 0.16 ≈ 67px
    HU = int(PANEL_H * 0.155)   # ≈ 65px — gives ~4.0 heads total visible

    for i, expr in enumerate(EXPRESSIONS):
        col = i % COLS
        row = i // COLS
        ppx = PAD + col * (PANEL_W + PAD)
        ppy = HEADER + row * (PANEL_H + PAD)

        panel_bg = expr["panel_bg"]

        # Panel background
        draw.rectangle([ppx, ppy, ppx + PANEL_W, ppy + PANEL_H], fill=panel_bg)
        draw.rectangle([ppx, ppy, ppx + PANEL_W, ppy + PANEL_H], outline=(80, 74, 70), width=1)

        # Character — face center at ~30% down the panel, body fills rest
        face_cy = ppy + int(PANEL_H * 0.28)
        face_cx = ppx + PANEL_W // 2

        # Draw Cosmo
        draw_cosmo(draw, face_cx, face_cy, HU, expr)

        # Label bar at bottom
        bar_h = 64
        draw.rectangle([ppx, ppy + PANEL_H - bar_h,
                        ppx + PANEL_W, ppy + PANEL_H],
                       fill=(18, 14, 12))
        draw.text((ppx + 6, ppy + PANEL_H - bar_h + 4),
                  expr["name"], fill=(91, 141, 184), font=font)
        draw.text((ppx + 6, ppy + PANEL_H - bar_h + 24),
                  expr["prev_state"], fill=(130, 118, 112), font=font_sm)
        draw.text((ppx + 6, ppy + PANEL_H - bar_h + 38),
                  expr["next_state"], fill=(130, 118, 112), font=font_sm)

        # Storyboard beat tag
        beat_tags = {
            "NEUTRAL / OBSERVING":    "A1-03 / A2-01",
            "FRUSTRATED / DEFEATED":  "A2-06",
            "DETERMINED":             "A2-05b",
            "SKEPTICAL":              "A2-03",
            "WORRIED":                "A2-02",
            "SURPRISED":              "A2-04c",
        }
        tag = beat_tags.get(expr["name"])
        if tag:
            draw.text((ppx + PANEL_W - 60, ppy + 6),
                      tag, fill=(100, 160, 120), font=font_sm)

    img.save(output_path)
    print(f"Saved: {output_path}  ({total_w}×{total_h}px)")


if __name__ == '__main__':
    import os
    out_dir = "/home/wipkat/team/output/characters/main"
    os.makedirs(out_dir, exist_ok=True)
    generate_cosmo_expression_sheet(
        os.path.join(out_dir, "LTG_CHAR_cosmo_expression_sheet_v002.png")
    )
