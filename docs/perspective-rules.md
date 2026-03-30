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
| Real World interiors (rooms) | 2-point perspective (one wall receding left, one right) | `vp_spec_config.json` per generator |
| Real World interiors (corridors/hallways) | 1-point perspective (central vanishing point, symmetric convergence) | `vp_spec_config.json` per generator |
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
| Ceiling tiles/panels | Tile edges converge toward VP | Especially critical in hallways — major depth cue |
| Light fixtures (ceiling) | Spacing compresses toward VP | Receding row of pendants/fluorescents must foreshorten |

### Hallway Ceiling Convergence (1-Point)

School hallways are 1-point perspective scenes. The ceiling is the **highest-impact depth cue** after the floor — its convergence lines are long, unbroken, and visible from any angle. Missing ceiling convergence collapses the hallway to a flat backdrop.

**Required elements for hallway ceiling:**

1. **Ceiling edge lines** — left and right ceiling-wall junctions converge toward `VP_X, VP_Y`. These are the two strongest perspective lines in the scene.
2. **Tile/panel grid** — if ceiling tiles are drawn, both X and Y tile edges must converge toward VP. Tiles farther from camera are smaller in both dimensions.
3. **Fluorescent light fixtures** — draw as rectangular strips parallel to the hallway axis. Spacing between fixtures compresses toward VP (closer spacing = farther away). Width of each fixture narrows toward VP.
4. **Minimum implementation** — even without tiles or fixtures, the ceiling-wall junction lines are mandatory. Two converging lines from top-left and top-right corners toward VP provide immediate depth.

**Hallway VP_Y spec (School Hallway):** VP_Y = 158 (28.9% of canvas). This is an adult-height establishing shot looking down the corridor. The low VP_Y means the ceiling occupies a smaller fraction of the frame — make the convergence lines prominent (2-3px stroke) so they read at pitch-deck scale.

**PIL implementation sketch:**
```
# Ceiling-wall junction lines (left and right)
draw.line([(0, ceiling_y_near), (VP_X, VP_Y)], fill=WALL_SHADOW, width=3)
draw.line([(W, ceiling_y_near), (VP_X, VP_Y)], fill=WALL_SHADOW, width=3)

# Fluorescent fixtures — spacing compresses toward VP
for i, frac in enumerate([0.15, 0.35, 0.55, 0.72, 0.85, 0.93]):
    fx = int(lerp(fixture_near_x, VP_X, frac))
    fy = int(lerp(fixture_near_y, VP_Y, frac))
    fw = int(lerp(fixture_near_w, 2, frac))  # narrows toward VP
    draw.rectangle([(fx - fw//2, fy - 1), (fx + fw//2, fy + 1)], fill=FIXTURE_COLOR)
```

---

## Verification

1. **Automated:** Run `LTG_TOOL_sobel_vp_detect.py <image> --vp-config vp_spec_config.json` — checks architectural VP alignment.
2. **Manual convergence test:** Draw a line from each furniture edge through the VP. If parallel edges in the scene do not converge toward the VP, the perspective is broken.
3. **Flat elevation flag:** Any rectangular polygon where all four corners form a perfect rectangle (no convergence) in a Real World scene is a FAIL.

---

## Camera Height Cross-Check

VP_Y values in `vp_spec_config.json` should be consistent with the Camera Height Convention table above. Quick validation (assuming 546px canvas height):

| Environment | VP_Y | VP_Y as % | Expected Range | Status |
|---|---|---|---|---|
| Classroom | 230 | 42.1% | 32-40% (adult) or 40-50% (child) | Borderline — reads child POV |
| Kitchen | 273 | 50.0% | 32-40% (adult) | LOW — reads child POV. Intentional if Luma's perspective; flag if Miri's kitchen |
| Living Room | 259 | 47.4% | 32-40% (adult) | LOW — reads child POV |
| School Hallway | 158 | 28.9% | 32-40% (adult) | HIGH — reads high angle/overview |

**Action:** Verify whether each environment's camera height is intentional. If the scene is meant to be from Luma's POV, the lower VP is correct. If from a neutral/adult camera, VP_Y should be raised (lower percentage). The hallway VP at 28.9% reads as an adult looking down a long corridor, which is appropriate for an establishing shot.

---

## Scope

- **Applies to:** All Real World environments and any Real World objects drawn in style frames or storyboard panels at scale where perspective is readable (head_r >= 20px equivalent).
- **Does not apply to:** Glitch Layer, Other Side, or sprint-scale objects where foreshortening would be sub-pixel.
- **Does not override:** The Depth Temperature Rule (see `docs/image-rules.md`). Perspective and temperature work together — convergence provides geometric depth; temperature provides tonal depth.
