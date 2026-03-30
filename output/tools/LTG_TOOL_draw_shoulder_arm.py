# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_draw_shoulder_arm.py
Ryo Hasegawa / Cycle 48

Shared draw_shoulder_arm() helper — reusable shoulder-to-arm drawing with proper
shoulder involvement (mass, socket rotation, deltoid bump).

Implements the Shoulder Involvement Rule (image-rules.md, codified C47) and the
shoulder mechanics reference (output/production/shoulder_mechanics_reference_c47.md).

All character generators can import this module instead of duplicating shoulder/arm
logic inline.

Usage:
    from LTG_TOOL_draw_shoulder_arm import draw_shoulder_arm, compute_shoulder_shift

    # Compute shifted shoulder point based on arm angle
    shifted_sx, shifted_sy = compute_shoulder_shift(
        shoulder_x=100, shoulder_y=80,
        arm_angle_deg=45,
        arm_length=60,
        scale=1.0,
    )

    # Draw full shoulder + upper arm + forearm + hand
    hand_x, hand_y = draw_shoulder_arm(
        draw=draw,
        shoulder_x=100,
        shoulder_y=80,
        arm_angle_deg=45,
        arm_length=60,
        scale=1.0,
        style=ShoulderArmStyle(
            arm_fill=(230, 100, 35),
            outline=(45, 35, 30),
            skin_fill=(255, 220, 185),
            line_width=2,
            clothing="hoodie",      # "hoodie" | "cardigan" | "fitted" | "bare"
            deltoid_radius=None,    # auto from scale
        ),
    )

Characters exempt from shoulder involvement: Byte (digital body), Glitch (non-humanoid).
Skip shoulder shift for sprint-scale figures where head_r < 20px.
"""

import math
from dataclasses import dataclass, field
from typing import Optional, Tuple

from PIL import ImageDraw


# ---------------------------------------------------------------------------
# Style configuration
# ---------------------------------------------------------------------------

@dataclass
class ShoulderArmStyle:
    """Per-character style parameters for shoulder-arm drawing."""
    arm_fill: Tuple[int, int, int] = (230, 100, 35)       # Clothing color (sleeve)
    outline: Tuple[int, int, int] = (45, 35, 30)          # Line color
    skin_fill: Tuple[int, int, int] = (255, 220, 185)     # Hand/skin color
    skin_highlight: Optional[Tuple[int, int, int]] = None  # Finger line color (optional)
    line_width: int = 2
    clothing: str = "hoodie"  # "hoodie" | "cardigan" | "fitted" | "bare"
    deltoid_radius: Optional[int] = None  # None = auto-compute from scale
    hand_radius: Optional[int] = None     # None = auto from arm_width
    two_segment: bool = True              # True = upper arm + forearm with elbow bend
    elbow_bend_factor: float = 0.12       # How much the elbow bows outward (fraction of arm_length)


# ---------------------------------------------------------------------------
# Shoulder shift computation (the core of the involvement rule)
# ---------------------------------------------------------------------------

def compute_shoulder_shift(
    shoulder_x: float,
    shoulder_y: float,
    arm_angle_deg: float,
    arm_length: float,
    scale: float = 1.0,
    side: int = 1,
) -> Tuple[float, float]:
    """Compute the shifted shoulder point based on arm angle.

    Implements the shoulder involvement rule from image-rules.md (C47):
    - When arm rises above horizontal, shoulder point rises 3-5px (scaled).
    - When arm extends outward, shoulder point spreads 4-6px (scaled).
    - When arm crosses body, shoulder drops and shifts inward.

    Args:
        shoulder_x: Resting shoulder socket X position.
        shoulder_y: Resting shoulder socket Y position.
        arm_angle_deg: Arm angle in degrees. 0=horizontal outward, 90=straight up,
                       -90=straight down, negative angles cross body.
        arm_length: Full arm length in pixels.
        scale: Character scale multiplier (1.0 = style-frame scale).
        side: +1 for right shoulder (viewer's left), -1 for left shoulder (viewer's right).
              Controls which direction is "outward" vs "inward".

    Returns:
        (shifted_x, shifted_y) — new shoulder point position.
    """
    angle_rad = math.radians(arm_angle_deg)

    # Arm endpoint relative to shoulder (for ratio calculations)
    arm_dx = math.cos(angle_rad) * arm_length * side
    arm_dy = -math.sin(angle_rad) * arm_length  # negative because Y increases downward

    # Shoulder rise: when arm goes above horizontal (arm_dy < 0 relative to shoulder)
    # Rise is proportional to how far above horizontal the arm is
    rise_ratio = max(0.0, -arm_dy / arm_length)  # 0 when level/below, up to 1 when straight up
    shoulder_rise = rise_ratio * 5.0 * scale

    # Shoulder spread: proportional to how far the arm extends outward
    spread_ratio = abs(arm_dx) / arm_length if arm_length > 0 else 0.0
    shoulder_spread = spread_ratio * 4.0 * scale

    # Determine direction: arm going outward vs crossing body
    arm_going_outward = (arm_dx * side) > 0

    if arm_going_outward:
        # Arm extends outward: shoulder spreads outward
        shift_x = side * shoulder_spread
        shift_y = -shoulder_rise
    else:
        # Arm crosses body: shoulder drops and shifts inward
        cross_ratio = min(1.0, abs(arm_dx) / (arm_length * 0.5)) if arm_length > 0 else 0.0
        shift_x = -side * cross_ratio * 3.5 * scale  # shifts inward
        shift_y = cross_ratio * 1.5 * scale           # drops slightly
        # Still apply rise if arm is also going up while crossing
        shift_y -= shoulder_rise * 0.5

    # Both arms raised (caller handles this by calling twice; each call raises its side)

    shifted_x = shoulder_x + shift_x
    shifted_y = shoulder_y + shift_y

    return shifted_x, shifted_y


# ---------------------------------------------------------------------------
# Deltoid bump drawing
# ---------------------------------------------------------------------------

def _draw_deltoid(
    draw: ImageDraw.ImageDraw,
    sx: float, sy: float,
    arm_angle_deg: float,
    radius: int,
    style: ShoulderArmStyle,
    side: int,
):
    """Draw the deltoid bump at the shoulder-arm junction.

    The bump follows the arm's initial direction, making the shoulder read as
    mass rather than a hinge.

    Clothing modifiers:
    - hoodie: wider bump (fabric bunch)
    - cardigan: bump + crease line
    - fitted: clean arc (most visible)
    - bare: visible ellipse
    """
    angle_rad = math.radians(arm_angle_deg)

    # Deltoid center is offset from shoulder point in the arm direction
    bump_offset = radius * 0.6
    bump_cx = sx + math.cos(angle_rad) * bump_offset * side
    bump_cy = sy - math.sin(angle_rad) * bump_offset

    r = radius
    lw = max(1, style.line_width - 1)

    if style.clothing == "hoodie":
        # Wider rectangle-ish bump = fabric bunching at hoodie sleeve top
        r_wide = int(r * 1.4)
        draw.ellipse(
            [int(bump_cx - r_wide), int(bump_cy - r),
             int(bump_cx + r_wide), int(bump_cy + r)],
            fill=style.arm_fill, outline=style.outline, width=lw,
        )
    elif style.clothing == "cardigan":
        # Rounded bump + a short crease line at the seam
        draw.ellipse(
            [int(bump_cx - r), int(bump_cy - r),
             int(bump_cx + r), int(bump_cy + r)],
            fill=style.arm_fill, outline=style.outline, width=lw,
        )
        # Crease line along shoulder seam direction (perpendicular to arm)
        perp_angle = angle_rad + math.pi / 2
        crease_len = r * 0.8
        cx1 = bump_cx + math.cos(perp_angle) * crease_len * side
        cy1 = bump_cy - math.sin(perp_angle) * crease_len
        cx2 = bump_cx - math.cos(perp_angle) * crease_len * side
        cy2 = bump_cy + math.sin(perp_angle) * crease_len
        draw.line(
            [(int(cx1), int(cy1)), (int(cx2), int(cy2))],
            fill=style.outline, width=max(1, lw - 1),
        )
    elif style.clothing == "fitted":
        # Clean rounded corner — most visible on Cosmo
        draw.ellipse(
            [int(bump_cx - r), int(bump_cy - int(r * 0.85)),
             int(bump_cx + r), int(bump_cy + int(r * 0.85))],
            fill=style.arm_fill, outline=style.outline, width=lw,
        )
    else:  # "bare" or fallback
        draw.ellipse(
            [int(bump_cx - r), int(bump_cy - r),
             int(bump_cx + r), int(bump_cy + r)],
            fill=style.arm_fill, outline=style.outline, width=lw,
        )


# ---------------------------------------------------------------------------
# Arm segment drawing
# ---------------------------------------------------------------------------

def _draw_two_segment_arm(
    draw: ImageDraw.ImageDraw,
    start_x: float, start_y: float,
    arm_angle_deg: float,
    arm_length: float,
    arm_width: float,
    style: ShoulderArmStyle,
    side: int,
) -> Tuple[float, float]:
    """Draw upper arm + forearm with elbow bend. Returns hand position (hx, hy)."""
    angle_rad = math.radians(arm_angle_deg)
    upper_len = arm_length * 0.50
    forearm_len = arm_length * 0.50
    aw = int(arm_width)
    lw = style.line_width

    # Elbow: midpoint with outward bow
    mid_x = start_x + math.cos(angle_rad) * upper_len * side
    mid_y = start_y - math.sin(angle_rad) * upper_len

    # Elbow bows outward (perpendicular to arm direction)
    bow = style.elbow_bend_factor * arm_length
    perp_angle = angle_rad + math.pi / 2
    elbow_x = mid_x + math.cos(perp_angle) * bow * side
    elbow_y = mid_y - math.sin(perp_angle) * bow

    # Hand endpoint
    # Forearm continues from elbow, slightly more downward (gravity pull)
    forearm_angle = angle_rad - 0.15  # slight downward sag
    hand_x = elbow_x + math.cos(forearm_angle) * forearm_len * side
    hand_y = elbow_y - math.sin(forearm_angle) * forearm_len

    # Upper arm polygon
    aw_upper = aw
    aw_elbow = int(aw * 0.75)
    draw.polygon([
        int(start_x - aw_upper // 2), int(start_y),
        int(start_x + aw_upper // 2), int(start_y),
        int(elbow_x + aw_elbow // 2), int(elbow_y),
        int(elbow_x - aw_elbow // 2), int(elbow_y),
    ], fill=style.arm_fill, outline=style.outline)

    # Forearm polygon
    aw_hand = int(aw * 0.6)
    draw.polygon([
        int(elbow_x - aw_elbow // 2), int(elbow_y),
        int(elbow_x + aw_elbow // 2), int(elbow_y),
        int(hand_x + aw_hand // 2), int(hand_y),
        int(hand_x - aw_hand // 2), int(hand_y),
    ], fill=style.arm_fill, outline=style.outline)

    return hand_x, hand_y


def _draw_single_segment_arm(
    draw: ImageDraw.ImageDraw,
    start_x: float, start_y: float,
    arm_angle_deg: float,
    arm_length: float,
    arm_width: float,
    style: ShoulderArmStyle,
    side: int,
) -> Tuple[float, float]:
    """Draw single-segment arm (simpler, for small scale). Returns hand position."""
    angle_rad = math.radians(arm_angle_deg)
    hand_x = start_x + math.cos(angle_rad) * arm_length * side
    hand_y = start_y - math.sin(angle_rad) * arm_length
    aw = int(arm_width)
    aw_end = int(aw * 0.7)

    # Arm fill (thick line via polygon)
    draw.polygon([
        int(start_x - aw // 2), int(start_y),
        int(start_x + aw // 2), int(start_y),
        int(hand_x + aw_end // 2), int(hand_y),
        int(hand_x - aw_end // 2), int(hand_y),
    ], fill=style.arm_fill, outline=style.outline)

    return hand_x, hand_y


def _draw_hand(
    draw: ImageDraw.ImageDraw,
    hx: float, hy: float,
    hand_r: int,
    style: ShoulderArmStyle,
):
    """Draw a simple ellipse hand at the given position."""
    lw = max(1, style.line_width - 1)
    draw.ellipse(
        [int(hx - hand_r), int(hy - hand_r * 0.6),
         int(hx + hand_r), int(hy + hand_r * 0.8)],
        fill=style.skin_fill, outline=style.outline, width=lw,
    )


# ---------------------------------------------------------------------------
# Main public API
# ---------------------------------------------------------------------------

def draw_shoulder_arm(
    draw: ImageDraw.ImageDraw,
    shoulder_x: float,
    shoulder_y: float,
    arm_angle_deg: float,
    arm_length: float,
    scale: float = 1.0,
    side: int = 1,
    style: Optional[ShoulderArmStyle] = None,
    arm_width: Optional[float] = None,
    skip_shoulder_shift: bool = False,
    skip_deltoid: bool = False,
) -> Tuple[float, float]:
    """Draw a complete shoulder + arm assembly with proper shoulder involvement.

    This is the main entry point. It:
    1. Computes the shifted shoulder point (shoulder involvement rule).
    2. Draws the deltoid bump at the shifted shoulder.
    3. Draws upper arm + forearm (or single segment) from shoulder to hand.
    4. Draws the hand.

    Args:
        draw: PIL ImageDraw context.
        shoulder_x: Resting (unshifted) shoulder socket X.
        shoulder_y: Resting (unshifted) shoulder socket Y.
        arm_angle_deg: Arm direction in degrees. 0=horizontal outward,
                       positive=upward, negative=downward.
        arm_length: Full arm length in pixels (shoulder to hand).
        scale: Character scale multiplier (affects shoulder shift magnitude).
        side: +1 = right shoulder (viewer's left), -1 = left shoulder (viewer's right).
        style: ShoulderArmStyle instance. None = default style.
        arm_width: Arm segment width in pixels. None = arm_length * 0.18.
        skip_shoulder_shift: If True, do not shift shoulder point (use for exempt chars
                             or sub-20px head_r figures).
        skip_deltoid: If True, do not draw deltoid bump.

    Returns:
        (hand_x, hand_y) — position of the drawn hand center.
    """
    if style is None:
        style = ShoulderArmStyle()

    if arm_width is None:
        arm_width = arm_length * 0.18

    # 1. Compute shifted shoulder
    if skip_shoulder_shift:
        sx, sy = shoulder_x, shoulder_y
    else:
        sx, sy = compute_shoulder_shift(
            shoulder_x, shoulder_y,
            arm_angle_deg, arm_length,
            scale=scale, side=side,
        )

    # 2. Deltoid bump
    deltoid_r = style.deltoid_radius
    if deltoid_r is None:
        deltoid_r = max(2, int(4 * scale + 0.5))  # 4-6px at style-frame scale

    if not skip_deltoid:
        _draw_deltoid(draw, sx, sy, arm_angle_deg, deltoid_r, style, side)

    # 3. Arm segments
    if style.two_segment:
        hand_x, hand_y = _draw_two_segment_arm(
            draw, sx, sy, arm_angle_deg, arm_length, arm_width, style, side,
        )
    else:
        hand_x, hand_y = _draw_single_segment_arm(
            draw, sx, sy, arm_angle_deg, arm_length, arm_width, style, side,
        )

    # 4. Hand
    hand_r = style.hand_radius
    if hand_r is None:
        hand_r = max(3, int(arm_width * 0.65))
    _draw_hand(draw, hand_x, hand_y, hand_r, style)

    return hand_x, hand_y


# ---------------------------------------------------------------------------
# Convenience: torso top-edge polyline with shoulder involvement
# ---------------------------------------------------------------------------

def shoulder_polyline(
    body_cx: float,
    body_top_y: float,
    body_half_width: float,
    left_arm_angle_deg: float,
    right_arm_angle_deg: float,
    arm_length: float,
    scale: float = 1.0,
    neck_half_width: Optional[float] = None,
) -> list:
    """Return a polyline list for the torso top edge incorporating shoulder shifts.

    The torso top is NOT a straight line — it curves through the shifted shoulder
    points, creating asymmetric silhouettes when arms are in different positions.

    Args:
        body_cx: Torso center X.
        body_top_y: Torso top Y (unshifted baseline).
        body_half_width: Half the torso width.
        left_arm_angle_deg: Left arm angle (viewer's right side).
        right_arm_angle_deg: Right arm angle (viewer's left side).
        arm_length: Arm length for shift computation.
        scale: Character scale.
        neck_half_width: Half the neck width. None = body_half_width * 0.35.

    Returns:
        List of (x, y) tuples forming the torso top edge from viewer's left
        shoulder through neck to viewer's right shoulder. Suitable for use as
        the top segment of a torso polygon.
    """
    if neck_half_width is None:
        neck_half_width = body_half_width * 0.35

    # Right shoulder (viewer's left, side=+1)
    r_sx, r_sy = compute_shoulder_shift(
        body_cx - body_half_width, body_top_y,
        right_arm_angle_deg, arm_length,
        scale=scale, side=1,
    )

    # Left shoulder (viewer's right, side=-1)
    l_sx, l_sy = compute_shoulder_shift(
        body_cx + body_half_width, body_top_y,
        left_arm_angle_deg, arm_length,
        scale=scale, side=-1,
    )

    # Build polyline: right shoulder -> neck right -> neck left -> left shoulder
    points = [
        (int(r_sx), int(r_sy)),
        (int(body_cx - neck_half_width), int(body_top_y)),
        (int(body_cx + neck_half_width), int(body_top_y)),
        (int(l_sx), int(l_sy)),
    ]

    return points


# ---------------------------------------------------------------------------
# Self-test / demo
# ---------------------------------------------------------------------------

def _demo():
    """Generate a demo image showing shoulder involvement at various arm angles."""
    from PIL import Image

    W, H = 1280, 720
    BG = (248, 244, 236)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Title
    d.text((20, 10), "draw_shoulder_arm() — Shoulder Involvement Demo (C48)", fill=(40, 40, 40))
    d.text((20, 28), "Each pair: arm angle shown. Deltoid bump + shoulder shift visible.",
           fill=(100, 100, 100))

    # Demo angles
    angles = [-60, -30, 0, 30, 60, 90, 120]
    styles = {
        "hoodie": ShoulderArmStyle(
            arm_fill=(230, 100, 35), outline=(45, 35, 30),
            skin_fill=(255, 220, 185), clothing="hoodie", line_width=2,
        ),
        "cardigan": ShoulderArmStyle(
            arm_fill=(120, 80, 55), outline=(45, 35, 30),
            skin_fill=(245, 225, 205), clothing="cardigan", line_width=2,
        ),
        "fitted": ShoulderArmStyle(
            arm_fill=(80, 130, 180), outline=(35, 35, 45),
            skin_fill=(255, 220, 185), clothing="fitted", line_width=2,
        ),
    }

    row_y = 80
    for style_name, style_obj in styles.items():
        d.text((20, row_y - 10), f"{style_name}:", fill=(60, 60, 60))
        for i, angle in enumerate(angles):
            cx = 100 + i * 160
            cy = row_y + 90
            arm_len = 55
            # Draw both sides
            draw_shoulder_arm(d, cx - 20, cy, angle, arm_len,
                              scale=1.0, side=1, style=style_obj)
            draw_shoulder_arm(d, cx + 20, cy, angle, arm_len,
                              scale=1.0, side=-1, style=style_obj)
            d.text((cx - 10, cy + 70), f"{angle}deg", fill=(80, 80, 80))
        row_y += 200

    import os
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "characters", "motion")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_shoulder_arm_demo.png")
    img.save(out_path)
    print(f"Demo saved: {out_path}")
    return out_path


if __name__ == "__main__":
    _demo()
