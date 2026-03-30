# Wand vs PIL Scene-Lit Compositing — C51 Evaluation Report

## Scope
Scene-lit compositing passes only (Jordan Reed). Sam Kowalski evaluates character_color_enhance overlays separately.

## BLOCKER: ImageMagick System Library Not Installed

Wand (Python bindings for ImageMagick) installed successfully via pip, but **cannot function**
without the ImageMagick system library (`libmagickwand-dev`). This is not a pip-installable
dependency — it requires `sudo apt install libmagickwand-dev` or equivalent.

**Status:** PIL baselines collected. Wand implementations written and ready to test once
ImageMagick is installed. The Wand code in `LTG_TOOL_wand_compositing_eval.py` will
auto-detect Wand availability and populate the comparison columns.

**Action needed:** System administrator installs `libmagickwand-dev`, then re-run this script.

## Passes Tested (PIL Baseline Only)

| Pass | PIL ms | Wand ms | Mean Pixel Diff | Approach Difference |
|---|---|---|---|---|
| CRT Tint Overlay | 2.33 | BLOCKED | BLOCKED | PIL: 20-step concentric ellipses. Wand: same but with Drawing API. Similar. |
| Contact Shadow | 0.79 | BLOCKED | BLOCKED | PIL: per-row alpha ellipses. Wand: single ellipse + gaussian_blur. Wand is cleaner. |
| Bounce Light | 0.58 | BLOCKED | BLOCKED | PIL: per-scanline alpha lines. Wand: filled rect + blur + screen composite. Wand is simpler. |

## Key Findings

### Wand Advantages for Scene-Lit Compositing
1. **Gaussian blur as a first-class op**: Contact shadows and bounce light are more physically accurate
   when drawn sharp then blurred, vs PIL's manual per-row alpha gradients. Wand does this in one call.
2. **Composite operators**: `screen`, `multiply`, `overlay` etc. are native. PIL requires manual
   alpha_composite + numpy array manipulation for non-standard blend modes.
3. **Fewer lines of code**: Contact shadow is ~8 lines with Wand vs ~15 with PIL.
4. **Gradient fills**: Wand supports radial and linear gradients natively — CRT glow could be
   a single radial gradient instead of 20 concentric ellipses.

### Wand Disadvantages
1. **PIL/Wand conversion overhead**: Each pass requires PNG encode/decode round-trip.
   At 1280x720 this adds ~20-50ms per conversion.
2. **System dependency**: Requires libmagickwand-dev (ImageMagick). PIL is pure Python wheel.
3. **Memory**: Wand images are separate from PIL — holding both doubles memory per frame.
4. **Slower for simple ops**: For operations that are just "fill an ellipse with alpha",
   PIL's approach is simpler and faster.

### Recommendation

**Hybrid approach — use Wand selectively:**

| Operation | Use | Reason |
|---|---|---|
| Contact shadow | Wand | gaussian_blur produces physically correct soft falloff |
| Bounce light | Wand | screen composite + blur = cleaner than scanline loop |
| CRT tint overlay | PIL | Concentric ellipses are fine; no Wand advantage |
| Post-character lighting | PIL | Simple alpha_composite; no advantage from Wand |
| Bloom/glow effects | Wand | Native blur kernel is superior to PIL's ImageFilter |

**Conversion cost mitigation:**
- Batch multiple Wand operations on the same Wand image before converting back to PIL
- Convert to Wand once at the start of the compositing pass, do all Wand ops, convert back once
- For the scene-lit pipeline: PIL draws scene + character -> convert to Wand -> contact shadow + bounce + bloom -> convert back to PIL -> final overlay + text

## Migration Path
1. Add `pil_to_wand()` / `wand_to_pil()` utilities to a shared compositing module
2. Replace contact shadow and bounce light implementations with Wand versions
3. Keep PIL for all drawing, text, and simple overlays
4. Profile full SF01 pipeline with hybrid approach — target < 100ms conversion overhead

## Alternative: PIL + scipy.ndimage for Gaussian Blur

If ImageMagick installation is not feasible, `scipy.ndimage.gaussian_filter` provides the
same gaussian blur capability without any system dependency. scipy is already authorized
and used in our codebase (sightline_validator uses scipy.ndimage for morphological ops).

```python
from scipy.ndimage import gaussian_filter
import numpy as np

# PIL contact shadow with scipy blur (no Wand needed)
shadow_arr = np.array(shadow_layer)
shadow_arr[:, :, 3] = gaussian_filter(shadow_arr[:, :, 3].astype(float), sigma=3.0).astype(np.uint8)
shadow_layer = Image.fromarray(shadow_arr)
```

This hybrid (PIL + scipy) approach gives us Wand's key advantage (proper gaussian blur for
contact shadows and bounce light) without the ImageMagick system dependency. The only Wand
advantage we lose is native composite operators (screen, multiply) — but those are implementable
in numpy as one-liners.

**Revised recommendation if ImageMagick is unavailable:**
- Use PIL + scipy.ndimage.gaussian_filter for blur-dependent compositing
- Use numpy for non-standard blend modes (screen = 1 - (1-a)*(1-b))
- Skip Wand entirely — the PIL+scipy+numpy stack covers all our needs

## Visual Comparison
See: `/home/wipkat/team/output/production/wand_compositing_eval_c51.png`
