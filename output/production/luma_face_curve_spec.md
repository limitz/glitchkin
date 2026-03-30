<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Luma Face Curve Spec
**Author:** Alex Chen, Art Director
**Date:** 2026-03-30
**Cycle:** C40
**Status:** ACTIVE — implementation delegated to Kai (tool) + Maya (control points)

---

## Problem Statement

Luma's face has regressed in visual quality across cycles. The current approach draws facial features using a stylus/stroke approach — ad-hoc pixel brushwork per expression. This produces:
- Jagged transitions between expressions
- Inconsistent feature proportions across poses
- Hair-over-eye rendering artifacts (confirmed: 669 FAIL violations in C39 hierarchy tool)
- No mathematical basis for smooth interpolation between emotional states

The solution: define Luma's face in terms of **named bezier cubic curves and ellipse arcs with explicit control points**. All expressions and poses derive from transforms on these named control points.

---

## Face Coordinate System

**Canvas:** 600×600px (standard Luma face canvas)
**Origin:** center of face oval — approximately (300, 280)
**X-axis:** right is positive
**Y-axis:** down is positive (PIL convention)
**Scale unit:** 1.0 = 1 pixel at 600px canvas. All control points expressed in canvas-pixel coordinates.

---

## Named Curve Set

### 1. FACE_OVAL
Type: Ellipse arc (full ellipse, closed)
Anchor: face center `FC = (300, 280)`
Parameters:
- `oval_rx`: horizontal radius (default: 115)
- `oval_ry`: vertical radius (default: 130)
- `oval_tilt`: rotation in degrees (default: 0)

Draw order: first (background layer). Fill with SKIN_BASE.

---

### 2. LEFT_BROW (character's left = viewer's right)
Type: Quadratic bezier (3 control points)
Points: `LB_P0`, `LB_P1` (control), `LB_P2`
Neutral baseline:
```
LB_P0 = FC + (-75, -68)   # outer brow end
LB_P1 = FC + (-38, -88)   # apex control point
LB_P2 = FC + (  0, -74)   # inner brow end (bridge side)
```
Stroke: 4px, color OUTLINE_BLACK
Note: this is the RECKLESS brow — arches higher, looser. Modulates expression most actively.

---

### 3. RIGHT_BROW (character's right = viewer's left)
Type: Quadratic bezier (3 control points)
Points: `RB_P0`, `RB_P1` (control), `RB_P2`
Neutral baseline:
```
RB_P0 = FC + (75, -68)    # outer brow end
RB_P1 = FC + (38, -88)    # apex control point
RB_P2 = FC + ( 0, -74)    # inner brow end (bridge side)
```
Stroke: 4px, color OUTLINE_BLACK
Note: Right brow modulates independently for asymmetric expressions. The corrugator kink (WORRIED state) is encoded as a ±10px vertical offset on RB_P1.

---

### 4. LEFT_EYE_OUTLINE (character's left eye = viewer's right)
Type: Closed cubic bezier (4 control points — wide teardrop)
Points: `LE_P0` (left extent), `LE_P1` (top), `LE_P2` (right extent), `LE_P3` (bottom)
Neutral baseline:
```
LE_P0 = FC + (-94, -22)   # outer corner
LE_P1 = FC + (-44, -44)   # top center
LE_P2 = FC + (  6, -22)   # inner corner
LE_P3 = FC + (-44,  -8)   # bottom center
```
Eye width (P0→P2 distance): **100px** canonical. Corrected C41 from 56px — Maya Santos cross-reference vs v011 generator (EW_CANON=45px half-width at 2x, scaled to spec canvas: ~99px). The 56px value was ~44% narrower than Luma's canonical eye width and would have produced an undersized, reserved-looking eye. Lid-top asymmetry controlled by `le_lid_drop`: 0=neutral, positive=lid descends from top (drowsy/THE NOTICING read), negative=lid lifts (wide alarm).
Fill: EYE_WHITE. Outline: 3px OUTLINE_BLACK.

---

### 5. RIGHT_EYE_OUTLINE (character's right eye = viewer's left)
Type: Closed cubic bezier (4 control points)
Points: `RE_P0`, `RE_P1`, `RE_P2`, `RE_P3`
Neutral baseline (mirrored):
```
RE_P0 = FC + ( -6, -22)   # inner corner
RE_P1 = FC + ( 44, -44)   # top center
RE_P2 = FC + ( 94, -22)   # outer corner
RE_P3 = FC + ( 44,  -8)   # bottom center
```
Right eye has the **lid-top-drop** (C39 canonical fix): `re_lid_drop` default = +6px (lid descends from top, not bottom). This is the canonical Luma right-eye read — sleepy-curious, not alarmed.

---

### 6. LEFT_IRIS
Type: Circle (special case of ellipse, no rotation)
Anchor: `LI_CENTER` (derived from eye outline centroid)
Neutral: `LI_CENTER = FC + (-44, -26)`, radius `LI_R = 12`
Fill: EYE_IRIS_COLOR. Outline: 2px OUTLINE_BLACK.
Pupil: solid circle at `LI_CENTER`, radius `LP_R = 5`, fill EYE_PUPIL_BLACK.
Highlight: circle at `LI_CENTER + (-4, -4)`, radius 3, fill WHITE.

---

### 7. RIGHT_IRIS
Type: Circle
Neutral: `RI_CENTER = FC + (44, -26)`, radius `RI_R = 12`
Same fill rules as LEFT_IRIS.

---

### 8. NOSE_BRIDGE
Type: Line segment (simple — Luma's nose is minimal)
Points: `NB_TOP = FC + (0, -10)`, `NB_BOT = FC + (0, 10)`
Stroke: 2px, OUTLINE_BLACK, 60% alpha (implied, not full weight)
Note: Nose can be omitted at smaller scales. At 600px canvas it is a subtle indicator only.

---

### 9. MOUTH
Type: Cubic bezier (4 control points)
Points: `M_P0` (left corner), `M_P1` (left mid control), `M_P2` (right mid control), `M_P3` (right corner)
Neutral smile baseline:
```
M_P0 = FC + (-38,  42)    # left corner
M_P1 = FC + (-18,  56)    # left upswing control
M_P2 = FC + ( 18,  56)    # right upswing control
M_P3 = FC + ( 38,  42)    # right corner
```
Stroke: 5px, OUTLINE_BLACK. This is the RECKLESS GRIN in neutral state.
For WORRIED/DOUBT variants: M_P1 and M_P2 y-values decrease (controls pulled up → flat line → frown).

---

### 10. BLUSH_LEFT / BLUSH_RIGHT
Type: Ellipse arc (open — top half only, or full soft ellipse)
Neutral:
```
BLUSH_L_CENTER = FC + (-65,  20), rx=18, ry=9
BLUSH_R_CENTER = FC + ( 65,  20), rx=18, ry=9
```
Fill: BLUSH_PINK (alpha=80). No outline.
Modulator: `blush_alpha` (0–255). Full blush on RECKLESS/EXCITED states. 0 on DOUBT.

---

## Expression Transforms

Each named expression is defined as a **delta dict** — offsets applied to the neutral control points above. Unspecified points remain at neutral.

### RECKLESS (default / title-card read)
```python
{
  "le_lid_drop": -4,          # eyes open wide
  "re_lid_drop":  2,          # right still slightly sleepy
  "LB_P1_dy":  -6,            # left brow lifts further
  "RB_P1_dy":  -4,
  "M_P1_dy":   +8,            # mouth corners lift (wider grin)
  "M_P2_dy":   +8,
  "blush_alpha": 120,
}
```

### THE NOTICING (canonical — C39 pitch primary)
```python
{
  "le_lid_drop":  +8,         # left lid descends (top drop, not bottom rise)
  "re_lid_drop": +12,         # right lid descends more — asymmetry key
  "LB_P1_dy":   +10,          # brows pull together slightly
  "RB_P1_dy":   +10,
  "LI_CENTER_dy": +4,         # iris shifts down (looking at something)
  "RI_CENTER_dy": +4,
  "M_P1_dy":    -4,           # mouth quiets — not grin
  "M_P2_dy":    -4,
  "blush_alpha":  0,
}
```

### THE NOTICING — DOUBT (slot 7 variant)
```python
{
  # Inherits THE NOTICING, then:
  "re_lid_drop": +16,         # right lid deeper still
  "RB_P1_dy":   +14,         # right brow drops further (uncertainty)
  "M_P0_dy":    -6,           # left mouth corner tucks
  "M_P3_dy":    -6,
}
```

### WORRIED
```python
{
  "RB_P1_dy":   +18,          # right brow corrugator kink
  "LB_P1_dx":   -4,           # left brow pulls inward
  "RB_P1_dx":   +4,           # right brow pulls inward
  "le_lid_drop": +4,
  "re_lid_drop": +4,
  "M_P1_dy":   -10,           # mouth flattens
  "M_P2_dy":   -10,
  "blush_alpha":  0,
}
```

### ALARMED
```python
{
  "le_lid_drop": -12,         # eyes wide open
  "re_lid_drop":  -8,
  "LB_P1_dy":   -14,          # brows shoot up
  "RB_P1_dy":   -14,
  "oval_ry":    +6,           # face elongates slightly (jaw drop)
  "M_P1_dy":    +2,
  "M_P2_dy":    +2,
  "M_P0_dy":    +6,           # jaw open
  "M_P3_dy":    +6,
}
```

### FRUSTRATED
```python
{
  "LB_P1_dy":   +8,           # brows scrunch down
  "RB_P1_dy":   +8,
  "LI_CENTER_dy": +2,
  "RI_CENTER_dy": +2,
  "M_P1_dy":   -14,           # hard frown
  "M_P2_dy":   -14,
  "M_P0_dy":    -4,
  "M_P3_dy":    -4,
  "blush_alpha":  0,
}
```

---

## Control Point Transform Rules

The following rules MUST be respected by any renderer applying these transforms:

1. **Lid drop is top-only:** `le_lid_drop` and `re_lid_drop` offset `P1` (top of eye curve) downward. `P3` (bottom) is fixed. Never raise the bottom lid to simulate a droop — this was the prior bug.

2. **Brow corrections apply to P1 only (the apex control point):** P0 and P2 are anchored at their neutral positions unless an expression specifies them. This keeps brow ends stable and only deforms the arc.

3. **Iris always stays within the eye outline:** After applying any transform, clamp iris center so `LI_CENTER` stays within the eye bezier bounding box. Never let the pupil clip through the eyelid.

4. **Mouth is drawn as a single open cubic bezier stroke** (not filled) at 600px. At smaller render sizes (< 200px), simplify to a line segment between M_P0 and M_P3.

5. **Blush is drawn last** (above all other face elements). Its alpha modulates by expression but never clips the eye outlines.

6. **Smooth interpolation:** For motion/tween use cases, linearly interpolate all delta values across frames. The bezier curve itself provides smooth spatial shape; only the control-point positions need interpolation.

---

## Draw Order

1. FACE_OVAL (fill + outline)
2. BLUSH_LEFT / BLUSH_RIGHT (fill, under-eye, no outline)
3. LEFT_EYE_OUTLINE + RIGHT_EYE_OUTLINE (fill white + outline)
4. LEFT_IRIS + RIGHT_IRIS (fill + outline)
5. LEFT_EYE pupils + highlights
6. RIGHT_EYE pupils + highlights
7. NOSE_BRIDGE
8. MOUTH
9. LEFT_BROW + RIGHT_BROW (drawn last — over any eye overlap at outer corners)

---

## Integration with Hair Cloud

The hair cloud is drawn as a **separate layer** after the face, using the existing approach. Hair overdraw artifacts (C39 FAIL findings) are expected — the fix is:
- Draw hair AFTER face — it occludes the face boundary.
- Draw eye irises AFTER hair — they punch through the hair layer.
- Hair-in-eye artifacts from LANCZOS downsample are a known sub-pixel issue. At 600px canvas they are minimal. Investigate in v012 if critics flag.

---

## Reference Implementation

See: `output/tools/LTG_TOOL_luma_face_curves.py` (Kai Nakamura — C40)

The tool must:
- Accept an expression name (or delta dict) and output a 600×600px face PNG
- Draw using `PIL.ImageDraw` quadratic/cubic bezier approximations (PIL does not natively support bezier — use the `_cubic_bezier_points()` utility to sample N points and draw as a polyline)
- Export a labeled reference sheet showing all 6 canonical expressions from the delta table above
- Be importable as a module (expose `draw_luma_face(canvas, expression_name, **overrides)`)

---

## Versioning

This spec is **v002** (updated C41 — eye-width critical correction).

**Change log:**
- v001 (C40): Initial bezier face spec with all 6 expression delta dicts
- v002 (C41): CRITICAL — Eye outer/inner corners corrected to 100px canonical width (was 56px). LEFT_EYE LE_P0 changed from FC+(−72,−22) to FC+(−94,−22); LE_P2 from FC+(−16,−22) to FC+(+6,−22). RIGHT_EYE RE_P0 from FC+(+16,−22) to FC+(−6,−22); RE_P2 from FC+(+72,−22) to FC+(+94,−22). Brow LB_P1 retained at FC+(−38,−88) — intentionally more elevated than v011 generator (~79px) for a more expressive reckless read in the curves implementation.

---
*Alex Chen, Art Director — C40/C41*
