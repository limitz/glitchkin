# Perspective Rules
*All agents: team members and critics.*

**Origin:** Chiara critique C47 — furniture reads as flat elevation across all Real World interiors. VP detect universal FAIL on furniture elements.

---

## Core Rule

**Every object with visible depth must converge toward the scene's vanishing point.**

Flat-elevation rectangles are prohibited for furniture, appliances, and architectural features in Real World interiors. If an object has three-dimensional volume, at least two of its visible faces must show foreshortening toward the VP.

---

## Perspective System by World Type

| World Type | Perspective | VP Source |
|---|---|---|
| Real World interiors | 2-point perspective (one wall receding left, one right) | `vp_spec_config.json` per generator |
| Real World exteriors | 1-point or 2-point depending on street angle | `vp_spec_config.json` per generator |
| Glitch Layer | No geometric perspective — depth via platform tiers, scale, and color temperature | VP checks skipped |
| Other Side | Abstract depth — no convergence rules | VP checks skipped |

---

## Vanishing Point Specifications

All Real World environments have canonical VP coordinates defined in `output/tools/vp_spec_config.json`. The `LTG_TOOL_sobel_vp_detect.py` tool (with `--vp-config` flag) validates VP alignment automatically.

Current Real World VPs:

| Environment | VP_X | VP_Y | Camera Note |
|---|---|---|---|
| Classroom | 192 | 230 | 3/4 back-right |
| Luma Study | 230 | 273 | CRT key light setup |
| Kitchen | 512 | 273 | Center-left |
| Tech Den | 820 | 295 | Right of center |
| Millbrook Street | 742 | 273 | Slightly right |
| School Hallway | 640 | 158 | Symmetric central corridor |
| Living Room | 704 | 259 | Center-right |

---

## Furniture Perspective Requirements

### What Convergence Means in Practice

For a table, chair, bookshelf, or appliance drawn as a polygon:

1. **Top surface:** The far edge must be shorter than the near edge (foreshortened). Both side edges must angle toward the VP.
2. **Side face:** Vertical edges remain vertical (2-point perspective convention). The top edge angles toward the VP; the bottom edge angles toward the VP.
3. **Front face:** If facing the viewer, this face appears widest. If turned, it foreshortens.

### Minimum Implementation (PIL polygon drawing)

For any rectangular object at position `(obj_x, obj_y)` with width `w` and height `h`:

```
# Flat elevation (PROHIBITED in Real World):
#   top-left ---- top-right
#   |                    |
#   bot-left ---- bot-right

# 2-point perspective (REQUIRED):
# Far edge shorter, angled toward VP_X, VP_Y
convergence_factor = (VP_Y - obj_y) / canvas_h  # 0..1, stronger near VP
shrink = w * convergence_factor * 0.15           # far edge shrinks

top_left  = (obj_x + shrink, obj_y)
top_right = (obj_x + w - shrink, obj_y)
bot_left  = (obj_x, obj_y + h)
bot_right = (obj_x + w, obj_y + h)
```

The exact convergence factor depends on the object's distance from the VP and the scene's field of view. The key requirement: **parallel horizontal edges in the real world must NOT be parallel in the image.**

### Camera Height Convention

| Scene Type | Camera Height | Eye Level (VP_Y as % of canvas) |
|---|---|---|
| Standard interior (adult eye level) | ~150cm equivalent | 32-40% from top |
| Child's perspective (Luma POV) | ~120cm equivalent | 40-50% from top |
| Low angle (dramatic) | ~80cm equivalent | 55-65% from top |
| High angle (overview) | ~200cm equivalent | 20-28% from top |

Current generators use adult eye level (VP_Y at 32-40% of canvas height). For Luma's POV shots, the VP should drop lower (higher VP_Y value) to sell the child's viewpoint.

---

## Per-Room Furniture Audit Checklist

When updating or creating an environment generator, verify every drawn element:

| Element | Must Show | Check |
|---|---|---|
| Tables/desks | Top surface foreshortening + one visible side face | Far edge shorter than near edge |
| Chairs | Seat plane angled, backrest has depth | Legs converge (not parallel vertical lines) |
| Shelving/cabinets | Side face visible, shelves converge | Horizontal shelf lines angle toward VP |
| Appliances (fridge, CRT, stove) | At least one receding face | Not a flat rectangle |
| Doors/windows | Frame reveals show wall thickness | Receding edges converge |
| Countertops | Surface foreshortening | Far edge shorter |

---

## Verification

1. **Automated:** Run `LTG_TOOL_sobel_vp_detect.py <image> --vp-config vp_spec_config.json` — checks architectural VP alignment.
2. **Manual convergence test:** Draw a line from each furniture edge through the VP. If parallel edges in the scene do not converge toward the VP, the perspective is broken.
3. **Flat elevation flag:** Any rectangular polygon where all four corners form a perfect rectangle (no convergence) in a Real World scene is a FAIL.

---

## Scope

- **Applies to:** All Real World environments and any Real World objects drawn in style frames or storyboard panels at scale where perspective is readable (head_r >= 20px equivalent).
- **Does not apply to:** Glitch Layer, Other Side, or sprint-scale objects where foreshortening would be sub-pixel.
- **Does not override:** The Depth Temperature Rule (see `docs/image-rules.md`). Perspective and temperature work together — convergence provides geometric depth; temperature provides tonal depth.
