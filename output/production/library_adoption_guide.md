<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Library Adoption Guide — C51 Stack
**Author:** Priya Shah, Story & Script Developer
**Date:** 2026-03-30
**Cycle:** 51
**Primary readers:** All team members writing Python code
**Context:** `docs/character-quality-pivot.md`, `docs/pil-standards.md`

---

## Purpose

C50 diagnosed the core quality gap: characters look like assembled geometry because PIL's drawing primitives were never designed for organic shapes. C51 evaluated and confirmed a new library stack. This guide documents each library: what it replaces, why it is better, how to install it, and a minimal usage example.

All libraries below are freely available and authorized for pitch development per the licensing policy in `docs/pil-standards.md`.

---

## 1. pycairo — Character Drawing Engine

**Replaces:** PIL `ImageDraw` (`draw.rectangle`, `draw.polygon`, `draw.ellipse`) for character rendering.

**Why it is better:**
- True bezier curves — no polygon approximation. A curve is a curve, not 64 line segments pretending to be one.
- Native anti-aliasing: 19x improvement over PIL baseline (Rin Yamamoto C50 benchmark).
- Variable-width strokes — enables line weight hierarchy and organic wobble without layered draw calls.
- Native gradient fills — eliminates layered-ellipse hacks for form shadows and skin tones.
- Float-precision geometry throughout — no integer rounding until final pixel output.

**Install:**
```bash
pip install pycairo
```
System dependency: `libcairo2-dev` (Ubuntu/Debian) or `cairo` (macOS via Homebrew).

**Minimal usage — draw a bezier curve and convert to PIL:**
```python
import cairo
from PIL import Image
import numpy as np

# Create cairo surface at 2x for AA
width, height = 2560, 1440
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Draw a character outline curve
ctx.set_source_rgba(0.2, 0.15, 0.1, 1.0)  # Deep Cocoa
ctx.set_line_width(4.0)
ctx.move_to(100, 300)
ctx.curve_to(150, 100, 350, 100, 400, 300)  # Cubic bezier
ctx.stroke()

# Convert to PIL Image
buf = surface.get_data()
arr = np.ndarray(shape=(height, width, 4), dtype=np.uint8, buffer=buf)
# Cairo is BGRA, PIL is RGBA — swap channels
img = Image.fromarray(arr[:, :, [2, 1, 0, 3]])
# Downscale to output size
img = img.resize((1280, 720), Image.LANCZOS)
img.save("output.png")
```

**Team convention:** Import shared primitives from `LTG_TOOL_cairo_draw.py` (Sam Kowalski). Do not write raw cairo API calls in generator scripts. Use: `cairo_bezier_body()`, `cairo_tube_limb()`, `cairo_variable_stroke()`, `cairo_to_pil()`.

---

## 2. Wand — Compositing

**Replaces:** Manual NumPy blending for shadows, glows, scene tint, and multi-layer composition.

**Why it is better:**
- ImageMagick's compositing engine handles blend modes (multiply, screen, overlay, soft-light) natively.
- Shadow and glow generation without hand-built Gaussian kernels.
- Color tinting and adjustment operations are single calls, not 20-line NumPy routines.
- Consistent, tested compositing math — eliminates edge-case blending bugs.

**Install:**
```bash
pip install Wand
```
System dependency: `libmagickwand-dev` (Ubuntu/Debian) or `imagemagick` (macOS via Homebrew).

**Minimal usage — add a drop shadow to a character layer:**
```python
from wand.image import Image as WandImage
from wand.color import Color

with WandImage(filename="character.png") as img:
    # Clone for shadow
    with img.clone() as shadow:
        shadow.colorize(Color("black"), Color("rgb(100%, 100%, 100%)"))
        shadow.gaussian_blur(sigma=8)
        # Composite shadow behind character
        shadow.composite(img, left=0, top=0)
        shadow.save(filename="character_with_shadow.png")
```

**Interop with PIL:** Convert via raw bytes:
```python
from wand.image import Image as WandImage
from PIL import Image as PILImage
import io

with WandImage(filename="input.png") as wand_img:
    png_blob = wand_img.make_blob("png")
    pil_img = PILImage.open(io.BytesIO(png_blob))
```

---

## 3. bezier — Curve Math

**Replaces:** Hand-rolled bezier functions (`bezier3`, `bezier4`, `bezier_point`, etc.) scattered across tool scripts.

**Why it is better:**
- Arc-length parameterization — place points evenly along a curve by distance, not by parameter t (which clusters points near endpoints).
- Subdivision — split a curve at any point cleanly.
- Intersection detection — find where two curves cross, essential for overlap checking.
- Curvature analysis — measure how sharp a curve is at any point.
- Mathematically correct and tested. Hand-rolled implementations had edge cases (division by zero at cusps, incorrect tangent at t=0/t=1).

**Install:**
```bash
pip install bezier
```

**Minimal usage — create a curve and sample points along it:**
```python
import bezier
import numpy as np

# Define control points (3 rows = x, y, [z]; columns = control points)
nodes = np.array([
    [100.0, 200.0, 350.0, 400.0],  # x
    [300.0, 100.0, 100.0, 300.0],  # y
])
curve = bezier.Curve(nodes, degree=3)

# Sample 20 evenly-spaced points
t_values = np.linspace(0.0, 1.0, 20)
points = curve.evaluate_multi(t_values)
# points[0] = x coords, points[1] = y coords
```

**Team convention:** Import from `LTG_TOOL_curve_utils.py` (Morgan Walsh). Run `python3 LTG_TOOL_curve_utils.py --audit` to check migration status of existing tools.

---

## 4. Shapely — Geometric Operations

**Replaces:** Pixel-level mask operations for silhouette comparison, overlap ratio, and outline analysis.

**Why it is better:**
- Resolution-independent — silhouette operations work on geometry, not pixels. Results do not change with render scale.
- IoU (Intersection over Union) is a single function call, not a pixel-counting loop.
- Outline simplification (Douglas-Peucker) reduces curve complexity while preserving shape.
- Width profiles — measure character width at any vertical slice for proportion checking.
- Buffer/offset operations — expand or contract a silhouette by a precise distance.

**Install:**
```bash
pip install Shapely
```

**Minimal usage — compare two character silhouettes:**
```python
from shapely.geometry import Polygon

# Silhouette outlines as coordinate lists
silhouette_a = Polygon([(0,0), (10,0), (10,20), (5,22), (0,20)])
silhouette_b = Polygon([(1,0), (11,0), (11,20), (6,22), (1,20)])

# Distinctiveness score
iou = silhouette_a.intersection(silhouette_b).area / silhouette_a.union(silhouette_b).area
distinctiveness = 1.0 - iou
print(f"Distinctiveness: {distinctiveness:.3f}")  # Higher = more distinct

# Simplify outline (reduce points while preserving shape)
simplified = silhouette_a.simplify(tolerance=1.0)
print(f"Points: {len(silhouette_a.exterior.coords)} -> {len(simplified.exterior.coords)}")
```

**Team convention:** Wrapped by `LTG_TOOL_curve_utils.py`. Prefer Shapely geometric operations over pixel-level mask operations for QA metrics.

---

## 5. colour-science — Perceptual Color

**Replaces:** Manual LAB/delta-E calculations in QA tools and color verification scripts.

**Why it is better:**
- CIE delta-E 2000 (the perceptually accurate metric) is a single function call. Our manual implementation used CIE76 (less accurate) because 2000 was too complex to hand-code correctly.
- Chromatic adaptation transforms (Bradford, Von Kries) — essential for accurate "what does this color look like under CRT light vs daylight?" calculations.
- Gamut mapping and conversion between color spaces (sRGB, AdobeRGB, CIE LAB, LUV, XYZ) with correct illuminant handling.
- Less code, fewer bugs. Our manual color math was 200+ lines across 4 tools. colour-science replaces all of it.

**Install:**
```bash
pip install colour-science
```

**Minimal usage — compute perceptual color difference:**
```python
import colour
import numpy as np

# Two colors in sRGB (0-1 range)
color_a = np.array([0.8, 0.6, 0.3])  # warm amber
color_b = np.array([0.75, 0.55, 0.35])

# Convert to CIE LAB
lab_a = colour.XYZ_to_Lab(colour.sRGB_to_XYZ(color_a))
lab_b = colour.XYZ_to_Lab(colour.sRGB_to_XYZ(color_b))

# Perceptual difference (CIE 2000)
delta_e = colour.delta_E(lab_a, lab_b, method="CIE 2000")
print(f"Delta E: {delta_e:.2f}")  # < 2.0 = barely perceptible
```

---

## 6. freetype-py — Selective Text Rendering

**Replaces:** PIL `ImageFont` for cases requiring typographic precision.

**Why it is better:**
- Precise glyph metrics — exact bounding boxes, advance widths, bearing values.
- Kerning tables — proper letter spacing from the font file, not PIL's default spacing.
- Sub-pixel rendering control.
- Useful for: title cards, in-world text on CRT screens, QA annotation overlays where alignment matters.

**Note:** PIL `ImageFont` remains fine for simple text overlays and debug annotations. freetype-py is for cases where typographic quality matters to the output.

**Install:**
```bash
pip install freetype-py
```

**Minimal usage — render text with precise metrics:**
```python
import freetype

face = freetype.Face("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
face.set_char_size(48 * 64)  # 48pt at 64 units per point

# Load a glyph
face.load_char('L')
bitmap = face.glyph.bitmap
# bitmap.buffer contains the rendered glyph as a flat array
# bitmap.width, bitmap.rows give dimensions
print(f"Glyph 'L': {bitmap.width}x{bitmap.rows} px, "
      f"advance: {face.glyph.advance.x // 64} px")
```

---

## 7. scikit-image — QA Analysis

**Replaces:** Manual cv2 edge analysis pipelines for quality assessment.

**Why it is better:**
- Structural Similarity Index (SSIM) — perceptual image comparison in one call. Better than pixel-diff for measuring whether two expression renders look meaningfully different.
- Morphological operations — clean binary masks for silhouette extraction.
- Edge quality metrics — Canny with automatic thresholding, edge continuity analysis.
- Well-documented, heavily tested. Our cv2 pipelines were functional but fragile (hardcoded thresholds, no automatic adaptation).

**Install:**
```bash
pip install scikit-image
```

**Minimal usage — compare two expression renders:**
```python
from skimage.metrics import structural_similarity as ssim
from skimage.io import imread

img_a = imread("expression_curious.png", as_gray=True)
img_b = imread("expression_focused.png", as_gray=True)

score, diff_map = ssim(img_a, img_b, full=True)
print(f"SSIM: {score:.3f}")  # 1.0 = identical, < 0.85 = visually distinct
# diff_map shows WHERE the images differ — useful for expression range QA
```

---

## Migration Notes

- **PIL is not being removed.** PIL remains the I/O and compositing backbone. pycairo draws characters; PIL loads, saves, and composites the final output. Wand handles complex compositing; PIL handles simple paste operations.
- **Existing tools migrate incrementally.** New tools use the new stack from the start. Existing tools with hand-rolled bezier functions should migrate to `LTG_TOOL_curve_utils.py` over time. Run `python3 LTG_TOOL_curve_utils.py --audit` to check status.
- **After any `img.paste()`**, refresh the draw context: `draw = ImageDraw.Draw(img)`. This rule from `docs/pil-standards.md` still applies.
- **All seeded RNG requirements still apply.** pycairo and Wand operations that involve randomness (noise, scatter) must use seeded RNG for reproducibility.

---

*Priya Shah — Story & Script Developer*
*Document: `output/production/library_adoption_guide.md`*
*Created C51.*
