<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# SF02 v007 — Luma Face Implementation Notes
**Author:** Lee Tanaka — Character Staging & Visual Acting Specialist
**Cycle:** 35
**Date:** 2026-03-29
**For:** Rin Yamamoto (generator implementation)
**Subject:** Clarifications on `_draw_luma_face_sprint()` for SF02 v007

---

## Context

These notes supplement the C34 staging brief (`output/production/sf02_staging_brief_c34.md`).
They address specific implementation questions that arise from the brief's spec vs. the current
v006 `_draw_luma()` geometry.

---

## 1. Head Geometry Reference (from v006 source)

Current `_draw_luma()` computes:
```python
head_r  = int(h * 0.12)   # at h=194px (18% of 1080H) → head_r ≈ 23px
head_cy = foot_y - h + head_r
cx      = luma_cx   # int(W * 0.45) ≈ 864px
```

So at h=194:
- `head_r = 23`
- Head ellipse: `[cx-23, head_cy-23, cx+23, head_cy+23]` — 46×46px canvas region

**Call site for `_draw_luma_face_sprint()`:**
Insert it inside `_draw_luma()` AFTER the `alpha_paste(img, overlay)` call (so the face draws
on top of the filled head ellipse). Pass `draw` from the existing `overlay` draw object OR
create a new overlay for the face layer. The face must be its own composited layer so it
respects alpha correctly.

Recommended call pattern:
```python
# After head ellipse fill in overlay draw:
face_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(face_layer)
_draw_luma_face_sprint(fd, cx, head_cy, head_r)
img = alpha_paste(img, face_layer)
```

---

## 2. Eye Specification at head_r=23

**Rule:** Eye radius = `int(head_r * 0.22)` — from Luma canonical spec (C32).
At head_r=23: `int(23 * 0.22) = 5px`. That's a 10×10px eye ellipse.

**However** — at 5px radius, the eye is a filled dot. Use a simpler approach:
- Left eye (viewer-left): 4px radius ellipse. WHITE fill for sclera, then 2px pupil fill in dark (VOID_BLACK). Or simply a STATIC_WHITE 4px dot plus a 1–2px dark center dot.
- Right eye: 3px radius. Slightly smaller = asymmetry without looking accidental.

**CRITICAL — do NOT use the canonical eye width formula exactly here.** At 5px the structure
collapses. The brief already calls for 4px pupils. Use:
```python
eye_r_L = 4    # left eye (viewer-left) — wider, attention signal
eye_r_R = 3    # right eye — narrower, forward-focused
pupil_r = 2    # both eyes
```

**Eye positions:**
- Eyes should be placed at approximately `head_cy - int(head_r * 0.15)` (slightly above mid-face)
- Left eye at: `cx - int(head_r * 0.38)` (viewer left)
- Right eye at: `cx + int(head_r * 0.38)` (viewer right)
- Both eyes angled down-forward: draw pupils offset by (+1, +1) from eye center to indicate
  downward-forward gaze. At this scale, pupil offset carries the gaze direction.

Example:
```python
def _draw_luma_face_sprint(draw, cx, head_cy, head_r):
    SCLERA       = (240, 240, 240)
    PUPIL        = (10, 10, 20)    # VOID_BLACK
    BROW_COLOR   = (59, 40, 32)    # DEEP_COCOA — slightly lighter than hair, readable
    MOUTH_COLOR  = (90, 40, 40)    # dark warm shadow

    eye_y = head_cy - int(head_r * 0.15)
    eye_x_L = cx - int(head_r * 0.38)
    eye_x_R = cx + int(head_r * 0.38)

    # Left eye — wider (4px)
    draw.ellipse([eye_x_L - 4, eye_y - 4, eye_x_L + 4, eye_y + 4],
                 fill=SCLERA)
    draw.ellipse([eye_x_L - 1, eye_y + 0, eye_x_L + 3, eye_y + 4],
                 fill=PUPIL)   # pupil offset down+right = looking down-forward

    # Right eye — narrower (3px)
    draw.ellipse([eye_x_R - 3, eye_y - 3, eye_x_R + 3, eye_y + 3],
                 fill=SCLERA)
    draw.ellipse([eye_x_R + 0, eye_y + 0, eye_x_R + 3, eye_y + 3],
                 fill=PUPIL)   # pupil offset down+right = looking ahead/down

    # Left brow — pulled inward/down (corrugator activation)
    # Brow line: angled from outer to inner, the inner end is LOWER than outer
    brow_y_base = head_cy - int(head_r * 0.48)
    draw.line([
        (eye_x_L - 4, brow_y_base),          # outer end (higher)
        (eye_x_L + 3, brow_y_base + 2),      # inner end (lower — pulled inward)
    ], fill=BROW_COLOR, width=1)

    # Right brow — level (not raised, not scrunched)
    draw.line([
        (eye_x_R - 3, brow_y_base),           # inner end (level)
        (eye_x_R + 4, brow_y_base),           # outer end (level)
    ], fill=BROW_COLOR, width=1)

    # Mouth — compressed jaw, minimal open, slightly below center
    mouth_y = head_cy + int(head_r * 0.38)
    # Compressed line or very small open oval (2–3px tall)
    draw.ellipse([cx - 4, mouth_y - 1, cx + 4, mouth_y + 2],
                 fill=MOUTH_COLOR)  # compressed ellipse reads as set jaw
```

---

## 3. Forward Torso Lean (8–12°)

The brief calls for 8–12° forward lean. In the current generator the torso is a centered
ellipse — lean is simulated by offsetting the torso center forward (toward motion, i.e., the
left/leading direction of the sprint).

**Implementation approach:**
```python
lean_px = int(h * 0.06)   # ~12px at h=194 — perceptible at sprint scale
# offset torso_left, torso_right by -lean_px (toward left = motion direction)
torso_left  = cx - torso_w // 2 - lean_px
torso_right = cx + torso_w // 2 - lean_px
# offset head_cy slightly upward for head-leads-body read:
head_cy_adj = head_cy - int(head_r * 0.10)
```

The offset creates the illusion of a forward lean without rotating the entire ellipse geometry.
If the generator already supports a `body_tilt` parameter pattern, use that instead.

---

## 4. Hair Stream Angle

Current hair stream in v006:
```python
hair_stream = [
    (cx - head_r + 4, head_cy),
    (cx - head_r - int(h * 0.06), head_cy - int(h * 0.04)),
    (cx - head_r - int(h * 0.11), head_cy + int(h * 0.01)),
]
```

This trails slightly left and barely dips — more "gentle wind" than "sprint velocity."

**Corrected hair stream (steeper rearward angle):**
```python
hair_stream = [
    (cx - head_r + 4, head_cy),
    (cx - head_r - int(h * 0.09), head_cy + int(h * 0.01)),   # more leftward, level
    (cx - head_r - int(h * 0.16), head_cy + int(h * 0.03)),   # further left, slight dip
]
```

The stream should be nearly horizontal (parallel to ground plane) to read as velocity.
The slight downward dip adds weight. Optional: add a second fine strand:
```python
hair_stream_2 = [
    (cx - head_r + 2, head_cy + 4),
    (cx - head_r - int(h * 0.13), head_cy + int(h * 0.04)),
]
draw.line(hair_stream_2, fill=DRW_HAIR_MAGENTA, width=1)
```

---

## 5. get_char_bbox() Fix

Per Rin's C35 directive, `get_char_bbox()` is being called on the full 3-character frame,
returning a bbox spanning 83% canvas width. For Luma-specific rim light application, the
char_cx should be hardcoded:

```python
luma_char_cx = int(W * 0.45)   # Luma is positioned at 45% of W
luma_char_cy = luma_head_cy    # computed from sprint geometry
```

Pass `luma_char_cx` directly to `add_rim_light()` instead of using the full-canvas bbox result.

---

## 6. What NOT to Change (brief confirmation)

These items are correct in v006 and must be preserved:
- Character position: `luma_cx = int(W * 0.45)` — protagonist center weight
- `char_h = int(H * 0.18)` — child-scale in adult danger
- CORRUPT_AMBER outline — figure-ground separation
- Dutch angle (4°) as final step — do not touch
- Storm skin tint (DRW_SKIN_STORM) — correct
- Byte TEAL body color — do not revert to Void Black

---

## 7. Face Readability at Sprint Scale — Key Priorities

The minimum acceptable face change (from the brief, confirmed):
> "The minimum acceptable change: eyes + asymmetric brows + compressed mouth.
> If those three elements are present and directional, the interiority gap closes."

At head_r=23, the three-element face (2 eyes + 2 brow lines + 1 mouth mark) is achievable
and sufficient. Do not add more elements — at this scale, crowding destroys readability.

After generating v007, Lee will run `LTG_TOOL_expression_silhouette.py` on a Luma
crop to validate the expression reads at this scale.

---

*Lee Tanaka — Character Staging & Visual Acting Specialist — C35*
