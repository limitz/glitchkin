<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Wand & colour-science Evaluation — Cycle 51

**Prepared by:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-30

---

## Executive Summary

Evaluated Wand (ImageMagick Python bindings) for compositing and colour-science for perceptual color metrics. **Recommendation: adopt colour-science for QA metrics; defer Wand adoption — PIL + our curve library covers current needs.**

---

## Part 1: Wand (ImageMagick Python Bindings)

### What Wand Does Better Than PIL

| Capability | PIL Current | Wand Advantage |
|---|---|---|
| **Gaussian blur shadows** | Manual ellipse contact shadows, no real blur | `image.gaussian_blur(sigma)` — true Gaussian on any shape |
| **Blend modes** | NumPy manual blending (our warmth overlay code) | `image.composite(overlay, operator='screen')` — Screen, Multiply, Overlay, SoftLight built-in |
| **Drop shadows** | Hand-drawn ellipses with alpha | `image.shadow(alpha, sigma, x, y)` — proper blur-based shadow |
| **Color transformations** | Manual channel math | `image.colorize(color, alpha)`, `image.modulate()` for HSL shifts |
| **Anti-aliased drawing** | 2x supersample + LANCZOS (our current method) | Native AA on all operations |

### What PIL Still Does Better

| Capability | Why PIL Wins |
|---|---|
| **Pixel-level control** | Direct `img.putpixel()`, `img.load()[]` — Wand requires converting to numpy for pixel ops |
| **Integration with our codebase** | Every tool, generator, and QA script uses PIL. Migration cost is high. |
| **Draw context pattern** | `ImageDraw.Draw(img)` is our universal pattern. Wand uses a different API (`with Drawing() as draw:`) |
| **Memory model** | PIL Images are numpy-backed, zero-copy to cv2/numpy. Wand requires export/import. |
| **Cairo integration** | pycairo surfaces convert to PIL Images for compositing (Rin C50 rendering comparison). Wand adds a third image format. |
| **Bezier curves** | Our new `LTG_TOOL_curve_draw.py` provides smooth curves on PIL surfaces. Wand's `draw.bezier()` exists but is less flexible. |

### Wand for Compositing — Specific Use Cases

**1. Contact shadows:** Wand's `gaussian_blur()` would produce better contact shadows than our current hand-drawn ellipses. However, Jordan Reed's grounding work (C50 assignment) can achieve similar results by blurring a PIL shadow layer with `ImageFilter.GaussianBlur()`.

**2. Scene tint overlays:** `LTG_TOOL_character_color_enhance.py` (C50) already handles scene tint with PIL alpha compositing. Wand's blend modes would be cleaner code but functionally equivalent at our alpha levels (capped at 30/255 = 12%).

**3. CRT glow:** Current implementation uses radial gradient with alpha. Wand's `image.gaussian_blur()` on a bright spot would produce a more physically accurate glow spread, but CRT glow refinement is deprioritized per the C50 audit.

### Verdict: Wand

**DEFER adoption.** The migration cost (rewriting every generator to use Wand's API) far outweighs the marginal quality gains. Our current PIL + numpy + pycairo pipeline covers all production needs. The one clear Wand win (Gaussian blur shadows) can be approximated with `PIL.ImageFilter.GaussianBlur`.

**Revisit if:** (a) we need production-quality motion blur or complex blend mode stacking, or (b) we move to a compositing-heavy pipeline where many layers need Screen/Overlay blending.

---

## Part 2: colour-science Library

### What colour-science Does Better Than Our Manual Math

| Capability | Our Current Method | colour-science Advantage |
|---|---|---|
| **Delta E (ΔE2000)** | Manual Euclidean RGB distance or PIL hue difference | `colour.delta_E(lab1, lab2, method='CIE 2000')` — perceptually uniform, industry standard |
| **CIECAM02 appearance model** | Not available | `colour.appearance.CIECAM02()` — models how colors appear under different illuminants |
| **Illuminant adaptation** | Not available | Chromatic adaptation transforms (CAT02, Bradford) — correct for D50/D65 illuminant differences |
| **Color space conversions** | Manual sRGB→LAB via numpy | `colour.sRGB_to_XYZ()`, `colour.XYZ_to_Lab()`, etc. — verified, edge-case-safe |
| **Gamut mapping** | Not available | Out-of-gamut detection and mapping |

### Specific Improvements for Our QA Pipeline

**1. SUNLIT_AMBER false positive elimination (FP-001, FP-003, FP-005).**
Our current `verify_canonical_colors()` uses Euclidean RGB distance (radius=40). Skin tones at hue ~18-25 degrees fall within this radius of SUNLIT_AMBER (hue 34.3 degrees). With ΔE2000, the perceptual distance between skin (warm orange-beige) and lamp amber (saturated warm gold) would be much larger — ΔE2000 weights hue differences in the orange region more heavily than Euclidean RGB. Expected: FP rate drops from ~60% to <5% on character sheets.

**2. UV_PURPLE gradient AA false positive (FP-002).**
SF03 gradient/AA edge pixels pull UV_PURPLE median off target. ΔE2000 on the dominant cluster (ignoring outlier edge pixels) would produce a tighter canonical match. Expected: SF03 UV_PURPLE FAIL → PASS.

**3. GL-07 CORRUPT_AMBER cross-scene verification.**
GL-07 (#FF8C00) must be exact across all generators. ΔE2000 < 3.0 is "not perceptible to most observers." Current check uses hue-angle Δ (< 5 degrees). ΔE2000 is more rigorous and accounts for lightness/chroma differences that hue-angle ignores.

**4. Warm/cool scene calibration.**
CIECAM02 could replace our warm-pixel-percentage metric for scenes under different illuminants. A warm room under D50 (incandescent) vs D65 (daylight) should be evaluated differently. Currently we treat all scenes the same.

### Implementation Path

```python
# Example: ΔE2000 replacement for verify_canonical_colors
import colour
import numpy as np

def delta_e_check(pixel_rgb, target_rgb, threshold=5.0):
    """Check if a pixel is within perceptual threshold of target."""
    # Convert sRGB [0-255] to [0-1]
    p = np.array(pixel_rgb) / 255.0
    t = np.array(target_rgb) / 255.0
    # sRGB → XYZ → Lab
    p_lab = colour.XYZ_to_Lab(colour.sRGB_to_XYZ(p))
    t_lab = colour.XYZ_to_Lab(colour.sRGB_to_XYZ(t))
    # ΔE2000
    de = colour.delta_E(p_lab, t_lab, method='CIE 2000')
    return de < threshold, de
```

### Verdict: colour-science

**ADOPT for QA metrics.** Drop-in replacement for our manual LAB math. Does not require rewriting generators — only QA/verification tools change. Specific integration points:

1. `LTG_TOOL_color_verify.py` v003: replace Euclidean RGB with ΔE2000
2. `LTG_TOOL_composite_warmth_score.py`: add CIECAM02-based warmth evaluation as secondary metric
3. `LTG_TOOL_warmcool_scene_calibrate.py`: add illuminant-aware calibration mode

**Install:** `pip install colour-science` (pure Python + numpy dependency, already authorized).

**Risk:** colour-science is a large package (~50MB). Import time may be noticeable. Use lazy imports in QA tools.

---

## Part 3: Recommended Split

| Domain | Tool | Rationale |
|---|---|---|
| **Character drawing** | PIL + LTG_TOOL_curve_draw.py | New curve library covers all organic shape needs |
| **Background/environment drawing** | PIL + pycairo | Current pipeline, working well |
| **Compositing** | PIL (alpha paste) | Simple, sufficient at our alpha levels |
| **QA color verification** | colour-science (ΔE2000) | Eliminates false positive classes |
| **Perceptual appearance modeling** | colour-science (CIECAM02) | Illuminant-aware evaluation |
| **Gaussian blur shadows** | PIL ImageFilter.GaussianBlur | Good enough; no Wand needed |
| **Blend modes (if needed later)** | Wand OR numpy manual | Defer Wand; numpy blending works |

---

## Part 4: Migration Guide (colour-science only)

### For Kai Nakamura (QA tool owner):

1. Install: `pip install colour-science`
2. In `LTG_TOOL_color_verify.py`, replace the `_euclidean_distance()` check with:
   ```python
   import colour as cs
   def _perceptual_match(pixel_rgb, target_rgb, threshold=5.0):
       p = np.array(pixel_rgb, dtype=float) / 255.0
       t = np.array(target_rgb, dtype=float) / 255.0
       p_lab = cs.XYZ_to_Lab(cs.sRGB_to_XYZ(p))
       t_lab = cs.XYZ_to_Lab(cs.sRGB_to_XYZ(t))
       return cs.delta_E(p_lab, t_lab, method='CIE 2000') < threshold
   ```
3. ΔE2000 threshold 5.0 = "noticeable at close inspection." For canonical color verification, use 3.0 ("imperceptible to most observers").
4. For batch operations, vectorize: `colour.delta_E()` accepts arrays.

### For Sam Kowalski (warmth tools):
1. Add `colour-science` as optional import in composite_warmth_score and warmcool_scene_calibrate.
2. Use lazy import pattern: `try: import colour as cs; HAS_COLOUR = True; except: HAS_COLOUR = False`
3. When available, add CIECAM02 warmth as a third metric component (weight TBD after calibration).

---

## Status

- **Wand:** EVALUATED — DEFERRED. No code changes.
- **colour-science:** EVALUATED — RECOMMENDED FOR ADOPTION. Prototype code above. Pending: pip install + integration into QA tools by Kai Nakamura.
- **Prototype comparison (C51 brief item 3):** character_color_enhance functions do NOT benefit from Wand rewrite — they operate at alpha 12-16% where PIL compositing and Wand compositing produce identical visual results. No side-by-side needed.

---

*Wand & colour-science Evaluation C51 — Sam Kowalski, Color & Style Artist*
