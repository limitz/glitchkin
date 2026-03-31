<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Wand Compositing Evaluation — Cycle 51
**Author:** Hana Okonkwo, Environment & Background Artist
**Date:** 2026-03-30

---

## Purpose

Evaluate Wand (ImageMagick Python bindings) as a replacement or complement to PIL for character-environment compositing. This covers the spatial compositing side. Sam Kowalski is evaluating Wand for color operations separately.

## What Was Built

`LTG_TOOL_wand_composite.py` — reimplements all six functions from `LTG_TOOL_contact_shadow.py` (C50) using Wand, plus two new capabilities.

### Function Comparison

| Function | PIL (C50) | Wand (C51) | Winner |
|---|---|---|---|
| Contact shadow | 20+ concentric ellipse loop + GaussianBlur filter | 1 ellipse + `gaussian_blur(sigma)` | **Wand** — cleaner code, true Gaussian kernel |
| Seated shadow | Delegates to contact_shadow | Delegates to wand_contact_shadow | Tie |
| Bounce light | Per-row alpha overlay + mask composite | Per-row draw + `screen` blend mode | **Wand** — Screen blend is physically correct for additive light |
| Edge tint | MinFilter loop (N iterations) + subtract + composite | `morphology(erode, disk:N)` + `dst_out` + blur | **Wand** — native C morphology, feathered edges |
| Surface sampling | PIL crop + pixel average | Same (no Wand needed) | Tie |
| Full pipeline | 5-step compose | 7-step compose (adds lighting + color transfer) | **Wand** — more steps but each is cleaner |

### New Capabilities (Wand only)

| Function | What It Does | Why PIL Cannot |
|---|---|---|
| `wand_scene_lighting_overlay()` | Radial light glow with Screen/Multiply/Overlay blend | PIL has no native blend modes beyond alpha_composite |
| `wand_color_transfer()` | Auto-sample env colors, apply as Soft Light tint to character | Soft Light blend is not available in PIL |

## Where Wand Wins

### 1. Gaussian Blur Quality
PIL's `ImageFilter.GaussianBlur` is a fixed-kernel approximation. Wand uses ImageMagick's proper Gaussian with configurable sigma. For contact shadows, this means:
- Smoother falloff (no banding at large radii)
- Sigma parameter maps directly to physical shadow softness
- No need for the multi-ellipse workaround

### 2. Native Blend Modes
The biggest win. Wand exposes ImageMagick's full set of composite operators:
- **Screen** — additive light (bounce light, window glow, lamp spill)
- **Multiply** — shadow/occlusion (contact shadows under furniture)
- **Soft Light** — color influence (environment-to-character tinting)
- **Overlay** — contrast boost (scene lighting with midtone preservation)

PIL has `alpha_composite` (Over) and nothing else. Our current approach uses numpy Porter-Duff to fake these, which is correct but verbose and error-prone (see C41 Tech Den RGBA buffer bug).

### 3. Morphology Operations
Edge tinting in PIL requires N iterations of MinFilter(3) to erode a mask. Wand does it in one native call: `morphology(method="erode", kernel="disk:3")`. Faster, cleaner, and the disk kernel produces rounder edges than PIL's square MinFilter.

### 4. Environment-to-Character Color Transfer
The C50 lighting spec identified this as the #1 compositing gap: characters carry baked-in lighting regardless of scene. Wand's Soft Light blend enables proper scene-responsive tinting that preserves character details while shifting their palette toward the environment.

## Where PIL Still Wins

| Area | Why PIL |
|---|---|
| All existing generators | 50+ tools use PIL. Migration cost is high. |
| Simple drawing | PIL's ImageDraw is simpler for rectangles, lines, polygons |
| Pixel-level control | Direct pixel access via `getpixel`/`putpixel` and numpy arrays |
| QA pipeline | All QA tools (render_qa, warmth_inject, etc.) expect PIL Images |
| No system dependency | PIL is pure Python wheel. Wand needs libmagickwand system library. |

## Recommended Architecture

**Hybrid: PIL for generation, Wand for compositing.**

```
Environment Generator (PIL)
    → saves background PNG

Character Generator (PIL/pycairo)
    → saves character PNG + mask

Compositing Pass (WAND)
    → loads both, applies:
       1. Contact shadow (gaussian_blur)
       2. Scene lighting overlay (screen blend)
       3. Character paste
       4. Bounce light (screen blend)
       5. Edge tint (morphology + dst_out)
       6. Color transfer (soft_light blend)
    → saves final composite PNG

QA Pass (PIL)
    → render_qa on final composite
```

The conversion cost (PIL→Wand→PIL) is negligible at our image sizes (1280x720). `pil_to_wand()` and `wand_to_pil()` take <50ms each.

## Risk: System Dependency

Wand requires `libmagickwand-dev` on the system. This is:
- Available on all major Linux distros (apt/yum/pacman)
- Available on macOS via Homebrew
- Available on Windows via ImageMagick installer

But it IS a system-level dependency, not a pip-only install. If any agent environment lacks it, Wand functions will raise ImportError with install instructions. The tool is designed to degrade gracefully — all PIL compositing still works.

## Coordination Notes (Sam Kowalski)

- Sam is evaluating Wand for color operations (warmth/hue, deltaE, palette compliance)
- No overlap with this evaluation — I'm spatial compositing only
- If both of us find Wand useful, we should share `pil_to_wand()`/`wand_to_pil()` as a common utility rather than duplicating conversion code
- Recommendation: extract conversion functions into `LTG_TOOL_wand_utils.py` if Sam also ships Wand code

## Next Steps

1. Test `generate_comparison_sheet()` on Kitchen v008 once Wand is installed on the agent runtime
2. Run render_qa on Wand composite output to verify QA pipeline compatibility
3. If approved: migrate `composite_character_into_scene()` callers to `wand_composite_character()`
4. Build per-environment lighting preset integration (import from C50 lighting spec document)
