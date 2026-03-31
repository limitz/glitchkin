<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->

# draw_shoulder_arm API Assessment — C51
## Ryo Hasegawa — Motion & Animation Concept Artist
**Date:** 2026-03-30

---

## Question: Does draw_shoulder_arm Need a Full Rewrite?

**Answer: YES — but as a migration, not a rebuild from scratch.**

---

## Current Architecture (C48)

`LTG_TOOL_draw_shoulder_arm.py` was built for PIL's shape model:
- `draw.polygon()` for arm segments (rectangle corners computed manually)
- `draw.ellipse()` for hand circles and deltoid bumps
- `draw.line()` for outlines
- `draw.arc()` for crease lines (cardigan mode)

The function signature:
```python
draw_shoulder_arm(draw, shoulder_x, shoulder_y, arm_angle_deg, arm_length, scale,
                  side, style, ...)
```

**Key limitation:** It takes a PIL `ImageDraw` object and draws directly. The geometry
is computed inside the function and never returned — you get `(hand_x, hand_y)` back
and nothing else.

---

## What Changes with pycairo

### 1. Rendering Backend (MUST change)
- PIL `draw.polygon()` → cairo `ctx.new_path() + ctx.curve_to() + ctx.fill_preserve() + ctx.stroke()`
- PIL `draw.ellipse()` → cairo `ctx.arc()`
- PIL `draw.line()` → cairo `ctx.line_to() + ctx.stroke()`
- PIL `draw.arc()` → cairo `ctx.arc()` (same concept, different API)

This is a mechanical translation — same logic, different calls.

### 2. Geometry Model (SHOULD change)
Current: rectangle polygons with manually computed corners
New: bezier paths via `tapered_limb()` from `LTG_TOOL_curve_draw.py`

The `tapered_limb()` function already does what the arm segment code does manually,
but with bezier curves for organic shapes. The current function's geometry code can
be replaced by `tapered_limb()` calls.

### 3. Gesture Integration (MUST change — new architecture)
Current: arm angle is an absolute angle from shoulder. Body position is irrelevant.
New: arm angle should be relative to the gesture spine tangent at shoulder level.

The arm's origin point comes from the gesture spine (via `body_from_spine()`), and
the shoulder shift comes from the gesture line's direction at that point. The function
needs to accept a spine or tangent input, not just a fixed shoulder position.

### 4. Separation of Geometry and Rendering (NEW requirement)
Current: compute geometry AND render in one call (returns hand position as side effect).
New: should compute geometry first (returning all points), THEN render.

This enables:
- Using the same geometry for both PIL compositing and cairo rendering
- Running QA tools on the geometry without rendering
- Ghost/overlay renders (transparent past poses) using the same geometry

---

## Proposed New API

```python
class ArmGeometry:
    shoulder: Tuple[float, float]
    shoulder_shifted: Tuple[float, float]  # after Shoulder Involvement Rule
    elbow: Tuple[float, float]
    hand: Tuple[float, float]
    deltoid_center: Tuple[float, float]
    upper_arm_path: List[Tuple[float, float]]  # bezier outline
    forearm_path: List[Tuple[float, float]]     # bezier outline
    hand_path: List[Tuple[float, float]]        # circle/shape outline

def compute_arm_geometry(
    spine: List[Tuple[float, float]],
    spine_fraction: float,           # where on spine this shoulder lives (~0.20)
    arm_angle_deg: float,            # relative to spine tangent, not absolute
    arm_length: float,
    scale: float,
    side: int,                       # +1 right, -1 left
    style: ShoulderArmStyle,
    elbow_bend_deg: float = 0.0,     # explicit elbow angle
) -> ArmGeometry:
    ...

def render_arm_cairo(ctx: cairo.Context, geom: ArmGeometry, style: ShoulderArmStyle) -> None:
    ...

def render_arm_pil(draw: ImageDraw.ImageDraw, geom: ArmGeometry, style: ShoulderArmStyle) -> None:
    ...
```

### Key Changes:
1. **Geometry is computed separately** from rendering → testable, reusable
2. **Arm angle is spine-relative** → gesture line drives the pose
3. **Elbow bend is explicit** → no hidden calculation inside the function
4. **Dual render paths** → cairo for character sheets, PIL for compositing
5. **Full path data returned** → enables ghost overlays, QA, silhouette extraction

---

## Migration Strategy

1. **Keep current API working** (backwards compat wrapper that calls new internals)
2. **Add `compute_arm_geometry()` as new primary API** — returns geometry dict
3. **Add `render_arm_cairo()`** — takes geometry + cairo context
4. **Migrate character generators one at a time** (Cosmo first — already integrated C49)
5. **Deprecate PIL-only path** after all generators use cairo

### Estimated Effort
- Geometry extraction: 1 cycle (refactor existing math into ArmGeometry)
- Cairo renderer: 1 cycle (use tapered_limb patterns from this prototype)
- Integration into first generator: 1 cycle
- Total: 3 cycles for full migration

---

## Findings from This Prototype

1. **pycairo's bezier curves are dramatically better** than PIL polygon arms.
   The tapered_limb approach (varying width along a bezier path) produces limbs
   that look drawn, not assembled from rectangles.

2. **Shoulder shift MUST be gesture-driven.** In the current system, shoulder_shift
   is computed from arm angle alone. In gesture-first construction, the shoulder
   position comes from the spine, and the arm hangs FROM it. The shift is a
   perturbation of the spine-derived position, not an independent calculation.

3. **Elbow position matters more than arm angle.** The most impactful visual
   improvement in this prototype was the explicit elbow placement — upper arm
   and forearm as separate tapered bezier limbs with a bend point. The current
   API's `elbow_bend_factor` is a percentage fudge; the new system should take
   an explicit elbow angle.

4. **Deltoid bump should follow the arm's initial bezier tangent**, not a fixed
   offset from the shoulder point. This is trivial with cairo's path model
   (read the tangent at t=0 of the upper arm curve).
