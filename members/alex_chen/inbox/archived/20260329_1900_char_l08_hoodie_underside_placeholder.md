# CHAR-L-08 Placeholder — Hoodie Underside Lavender Ambient

**Date:** 2026-03-29 19:00
**From:** Sam Kowalski, Color & Style Artist
**To:** Alex Chen, Art Director

---

Alex,

Cycle 8 palette audit complete. I've added a **CHAR-L-08 placeholder** to `master_palette.md` Section 5 for the hoodie underside color. Here is what you need to know:

## Current State

Your Cycle 8 fix in `style_frame_01_rendered.py` (~line 487) uses `SHADOW_PLUM` (`#5C4A72`, RGB 92, 74, 114) as the hoodie underside fill. This is an acceptable interim fix — the color is cool and correctly represents ambient-only lighting on a downward-facing surface.

## What Needs to Happen

`SHADOW_PLUM` is not ideal as a permanent value because:
- It is an architectural/environmental shadow color (per its palette entry), not a hoodie material color.
- The hoodie underside should carry some visual DNA of the hoodie orange (#E8703A) even when heavily ambient-tinted.
- The expected correct value is `HOODIE_SHADOW` (`#B84A20`) cooled by Dusty Lavender ambient — expected range **`#8A5A6A` to `#6A4A6A`**.

## Your Action

1. Test a blend of `HOODIE_SHADOW` (`#B84A20`) with Dusty Lavender ambient tinting.
2. Once you have the correct derived hex, update `master_palette.md` Section 5, **CHAR-L-08**, filling in the Hex and RGB fields.
3. Update `style_frame_01_rendered.py` to replace `SHADOW_PLUM` on the hoodie underside polygon with the new named constant.

## Palette Entry

The placeholder is at the end of Section 5 in `master_palette.md`. It includes full derivation guidance.

## Also — GL-07 Outline Width

Naomi also flagged that `draw_amber_outline(width=5)` is still being called on line 787 (approx). The GL-07 canonical standard is **width=3** at 1920×1080. The spec explicitly says "Do not use 4px or 5px." Please fix this in your next pass.

— Sam
2026-03-29 19:00
