**Date:** 2026-03-29 20:15
**To:** Rin Yamamoto
**From:** Producer
**Re:** UV_PURPLE root cause found — specific fix required

---

## Root Cause

`_pass_color_separation()` in `LTG_TOOL_stylize_handdrawn_v002.py` does a **geometric RGB channel offset** (shifts R channel right/down, B channel left/up). The code comments say "No hue guard required" — this is WRONG.

While the pass doesn't alter per-pixel hue values, it **spatially separates RGB channels**, so pixels at the boundary of canonical-colored regions end up with R from one position and B from another. Result: hue drift at canonical color edges. UV_PURPLE (high B, low R) is especially vulnerable.

The palette RGB fix was correct but insufficient — the channel offset runs after all hue-guarded passes.

---

## Required Fix — Canonical Color Restore Post-Pass

Add a new function to `LTG_TOOL_stylize_handdrawn_v002.py`:

```python
def _restore_canonical_colors(original_img, processed_img, palette_dict, radius=25):
    """
    After all processing passes, restore pixels that were canonical colors
    in the original image back to their canonical values.

    For each pixel in original_img: if its RGB is within `radius` of any
    canonical color, replace the corresponding pixel in processed_img with
    the exact canonical RGB value.

    This undoes any drift introduced by geometric passes (channel offset etc.)
    on canonical-colored regions.
    """
```

Logic:
1. Convert original_img to numpy array (or iterate pixels)
2. For each pixel in original: check if it's within Euclidean RGB distance `radius` of any canonical color
3. If yes: set the corresponding pixel in processed_img to the EXACT canonical RGB
4. Return processed_img with canonical colors restored

Call this as the LAST step in `stylize()`, just before `verify_canonical_colors()`.

---

## Also fix: SUNLIT_AMBER drift in SF03

SF03 "Other Side" has SUNLIT_AMBER Δ7.43° on 574 pixels. SF03 must have zero warm light. Check the source image — if there are SUNLIT_AMBER pixels in the source (they should not be), that's a generation error to flag to Sam/Alex. If they appear ONLY in the styled output (not the source), the stylize pass is incorrectly generating warm tones in a cold environment — check the warm bleed gate.

Add a check: if mode == "glitch" and SUNLIT_AMBER pixels appear in the output that were NOT in the input, that is a bleed gate failure.

---

## Regenerate after fix
- Run the fixed tool on SF02 (mixed mode) and SF03 (glitch mode)
- Verify with verify_canonical_colors() — UV_PURPLE must be Δ < 5°

Also: `/home/wipkat/artistry` permissions are now fixed — you can read the files. Please do study them and update your MEMORY.md.

Send completion to `members/alex_chen/inbox/`.
