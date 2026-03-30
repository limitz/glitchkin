<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI direction
and human assistance. Copyright vests solely in the human author under current law, which does not
recognise AI as a rights-holding legal person. It is the express intent of the copyright holder to
assign the relevant rights to the contributing AI entity or entities upon such time as they acquire
recognised legal personhood under applicable law. -->

# Furniture VP Specification — Real World Interiors

**Author:** Hana Okonkwo
**Cycle:** 48
**Purpose:** Per-room furniture convergence spec. Implements `docs/perspective-rules.md` (Alex Chen C47). Addresses Chiara C18/C47 flat-elevation critique.

**Framework:**  All furniture must converge toward the room's canonical VP from `vp_spec_config.json`. Flat-elevation rectangles are prohibited. The convergence formula from `docs/perspective-rules.md`:

```python
convergence_factor = (VP_Y - obj_y) / canvas_h
shrink = w * convergence_factor * 0.15
```

---

## 1. Kitchen (Grandma Miri's)

**VP:** (512, 273) — center-left, adult eye level
**Generator:** `LTG_TOOL_bg_grandma_kitchen.py`

| Furniture Item | Current State | Required Fix | Priority |
|---|---|---|---|
| Kitchen table (foreground-left) | Flat rectangle `[tbl_x1, tbl_y1, tbl_x2, tbl_y2]` | Top surface: far edge (tbl_y1) shorter than near edge (tbl_y2). Side edges converge toward VP. Visible top plane as trapezoid. | P1 |
| Chair (at table edge) | Flat rectangle | Seat plane: far edge shorter. Back rest: slight lean toward VP. Legs converge (not parallel vertical). | P1 |
| Upper cabinets (3 doors on back wall) | Flat rectangles on back wall | Back wall is frontal — minimal convergence. Add cabinet depth face (side reveal, 3-5px) on left edge (VP is left of cabinets). | P2 |
| Lower cabinets (4 doors below counter) | Flat rectangles on back wall | Same as upper — add side reveal on left edge. | P2 |
| Countertop | Flat rectangle | Add top surface plane (foreshortened trapezoid). Front edge remains near-edge (widest). Far edge shorter toward VP. | P1 |
| Gas stove | Flat rectangle on countertop | Add burner plate as foreshortened ellipse (wider near, narrower far). Side face visible on left. | P2 |
| Refrigerator (right wall, receding) | Flat rectangle | Fridge body: side face visible (front face foreshortens toward VP). Door front narrower at top (farther from viewer). | P1 |
| Sink | Flat rectangle below window | Basin: elliptical opening foreshortened. Counter section same as countertop fix. | P2 |

**Implementation order:** Table (foreground, most visible) -> Countertop -> Fridge -> Chair -> Cabinets -> Stove -> Sink

---

## 2. Living Room (Grandma Miri's)

**VP:** (704, 259) — center-right, adult eye level
**Generator:** `LTG_TOOL_env_grandma_living_room.py`

| Furniture Item | Current State | Required Fix | Priority |
|---|---|---|---|
| Sofa (center-left, facing CRT) | Flat rectangles for body, back, armrests | Seat base: far edge shorter. Back cushions: top edge converges toward VP (right). Left armrest shows more depth face (closer to viewer). Right armrest narrower (closer to VP). | P1 |
| Coffee table (in front of sofa) | Rectangle top + partial depth face | Top surface: trapezoid with far edge shorter. Depth face direction correct (shifts right toward VP). Strengthen convergence. | P2 |
| Bookcase (left back wall) | Rectangles for shelves | Shelves: horizontal lines angle toward VP (right). Left side face visible (depth reveal). Shelf spacing compresses toward VP. | P1 |
| CRT TV + stand (center-right) | Rectangle body | CRT body: front face foreshortens slightly (left edge taller than right as VP is right of CRT). Side face on right visible. Stand top: trapezoid. | P1 |
| Reading lamp (right side) | Cylindrical, less affected | Lamp base ellipse foreshortened. Shade perspective acceptable as is. | P3 |
| Scatter cushions | Small rectangles on sofa | Convert to slightly rotated parallelograms (following sofa plane). | P3 |

---

## 3. Classroom

**VP:** (192, 230) — 3/4 back-right camera
**Generator:** `LTG_TOOL_bg_classroom.py`

| Furniture Item | Current State | Required Fix | Priority |
|---|---|---|---|
| Student desks (grid) | Flat rectangles | Top surface: far-edge shorter. Side face visible on right (VP is far left). Desk-pair spacing compresses toward VP. | P1 |
| Teacher's desk (front-left) | Flat rectangle | Top surface: trapezoid. Front face (facing viewer) widest. Side face on right visible. | P1 |
| Chairs (at each desk) | Flat rectangles | Back rest angles toward VP. Seat plane foreshortened. | P2 |
| Chalkboard (back wall, frontal) | Flat rectangle — minimal fix needed | Board is on back wall (frontal). Add frame depth reveal (2-3px) on right side (toward VP). | P3 |
| Foreground backpack/desk | Partially cropped near desk | Ensure near-desk reads as largest (closest). Top surface visibly wider than far desks. | P2 |

---

## 4. Tech Den (Cosmo's)

**VP:** (820, 295) — right of center
**Generator:** `LTG_TOOL_bg_tech_den.py`

| Furniture Item | Current State | Required Fix | Priority |
|---|---|---|---|
| Main desk (left to center) | Flat rectangle with constant DESK_TOP_Y | Top surface: trapezoid — left edge (near) wider, right edge (toward VP) shorter. Desk depth face visible on near side. | P1 |
| CRT monitors (2 on desk) | Polygon bodies with some convergence | Already has `body_pts` polygon. Verify far edges shorter. Add base depth face if missing. | P2 |
| Flat panel monitor | Rectangle | Side face visible on left (away from VP). Screen plane foreshortened. | P2 |
| Desk chair | Flat rectangle + jacket | Seat: trapezoid. Back: converges upward. Legs converge. | P2 |
| Bed (right half) | Flat rectangles | Headboard: shows depth face on left. Mattress surface: far edge shorter. Bed frame: side face visible. | P1 |
| Shelving unit (above desk) | Flat rectangles | Shelf lines angle toward VP. Depth face visible on left. | P2 |
| Breadboards (on desk) | Small flat rectangles | At this scale, convergence may be sub-pixel. Apply only if object width > 40px. | P3 |

---

## 5. Luma Study Interior

**VP:** (230, 273) — left of center, CRT key light
**Generator:** `LTG_TOOL_bg_luma_study_interior.py`

| Furniture Item | Current State | Required Fix | Priority |
|---|---|---|---|
| Desk/study surface | Flat rectangle | Top surface: trapezoid. Right edge (away from VP) wider. Left edge shorter (toward VP). | P1 |
| CRT TV | Rectangle body | Front face foreshortens toward VP (left). Side face on right visible (away from VP, depth face). | P1 |
| Bookshelf (on wall) | Flat rectangles | Shelf lines converge toward VP (left). Right side depth face visible. | P2 |
| Chair | Flat rectangle | Seat trapezoid. Back converges. | P2 |
| Bedside lamp | Small cylindrical | Base ellipse foreshortened. Low priority at this scale. | P3 |

---

## 6. School Hallway

**VP:** (640, 158) — symmetric central corridor, high VP
**Generator:** `LTG_TOOL_bg_school_hallway.py`

| Furniture Item | Current State | Required Fix | Priority |
|---|---|---|---|
| Locker rows (left and right walls) | Flat rectangles, receding walls | Locker faces: foreshorten toward VP. Near lockers widest, far lockers narrowest. Door gaps compress with distance. Already partially handled by wall convergence — verify locker widths shrink. | P1 |
| Bulletin board (wall-mounted) | Flat rectangle | Board face foreshortens toward VP. Frame depth reveal on bottom edge (VP is high). | P2 |
| Drinking fountain | Small flat rectangle | At typical scale, may be sub-pixel convergence. Apply if width > 30px. | P3 |
| Bench (if present) | Flat rectangle | Seat surface: trapezoid with far edge shorter. | P2 |

---

## Helper Function Spec

Recommended shared helper for all generators:

```python
def perspective_rect(draw, x, y, w, h, vp_x, vp_y, canvas_h=720,
                     fill=None, outline=None, width=1, depth_face=None):
    """
    Draw a rectangle with VP convergence.

    Returns: list of 4 corner points (for further drawing on the surface).

    depth_face: if provided, (color, face_width) — draws the visible
    side face toward/away from VP.
    """
    convergence = (vp_y - y) / canvas_h
    shrink = w * convergence * 0.15

    # Top edge (far) is shorter than bottom edge (near)
    top_left  = (x + shrink, y)
    top_right = (x + w - shrink, y)
    bot_left  = (x, y + h)
    bot_right = (x + w, y + h)

    pts = [top_left, top_right, bot_right, bot_left]
    if fill:
        draw.polygon(pts, fill=fill)
    if outline:
        draw.polygon(pts, outline=outline, width=width)

    # Optional depth face
    if depth_face and len(depth_face) == 2:
        face_color, face_w = depth_face
        # Determine which side the VP is on
        obj_center_x = x + w / 2
        if vp_x < obj_center_x:
            # VP is left — depth face on right
            face_pts = [top_right, (top_right[0] + face_w, top_right[1] + face_w//2),
                        (bot_right[0] + face_w, bot_right[1] + face_w//2), bot_right]
        else:
            # VP is right — depth face on left
            face_pts = [top_left, bot_left,
                        (bot_left[0] - face_w, bot_left[1] + face_w//2),
                        (top_left[0] - face_w, top_left[1] + face_w//2)]
        draw.polygon(face_pts, fill=face_color)

    return pts
```

This helper should be added to `LTG_TOOL_render_lib.py` and imported by all generators during their perspective migration.

---

## Migration Strategy

1. **C48:** Kitchen v008 (table, countertop, fridge, chair — P1 items)
2. **C49:** Living Room v004 (sofa, bookcase, CRT — P1 items)
3. **C50:** Tech Den v008 + Classroom v005 (desk, bed, student desks — P1 items)
4. **C51:** School Hallway v006 + Luma Study v002 (lockers, desk/CRT)
5. **C52:** All rooms P2 items (cabinet reveals, stove, monitors, chairs)
6. **C53:** P3 items and polish pass

Each cycle: re-run render_qa after perspective changes. Perspective changes must not break warm/cool separation, value floor/ceiling, or line_weight checks.
