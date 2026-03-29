# Stylization Preset — Hand-Drawn v001
**Tool:** `output/tools/LTG_TOOL_stylize_handdrawn_v001.py`
**Author:** Rin Yamamoto / Cycle 23 / 2026-03-29

---

## Assets Treated (Cycle 23)

| Asset | Mode | Intensity | Seed | Output |
|-------|------|-----------|------|--------|
| `LTG_COLOR_styleframe_glitch_storm_v005.png` | mixed | 1.0 | 42 | `LTG_COLOR_styleframe_glitch_storm_v005_styled.png` |
| `LTG_COLOR_styleframe_otherside_v003.png` | glitch | 1.0 | 42 | `LTG_COLOR_styleframe_otherside_v003_styled.png` |
| `LTG_COLOR_styleframe_discovery_v003.png` | realworld | 0.6 | 42 | `LTG_COLOR_styleframe_discovery_v003_styled.png` |
| `LTG_ENV_grandma_kitchen_v003.png` | realworld | 1.0 | 42 | `LTG_ENV_grandma_kitchen_v003_styled.png` |

---

## Mode Descriptions

### `realworld` mode
Passes applied (in order):
1. **Paper grain** — noise texture overlay, alpha ~18 (at intensity 1.0). Subtle felt-tip-on-paper roughness.
2. **Line wobble** — per-row sinusoidal horizontal shift, max ±2px at intensity 1.0 (×0.8 = 1.6px effective).
3. **Warm color bleed** — amber/terracotta regions bleed outward ~3px with SUNLIT_AMBER (#D4923A) tint at alpha 30.
4. **Chalk highlights** — pixels with V>216 (top 15% brightness) desaturated by 12 S-units. Amber hue range (PIL H: 8–25) protected.

### `glitch` mode
Passes applied (in order):
1. **Scanlines** — horizontal lines every 4px, alpha 10. CRT reference.
2. **Color separation** — R channel shifted +1px right/down, B channel shifted -1px left/up. Risograph misregistration.
3. **Edge sharpening** — UnsharpMask(radius=1.5, percent=120, threshold=3). Crisp geometry edges.
*(No paper grain — Glitch Layer has no paper.)*

### `mixed` mode (SF02-specific)
- Lower third (Y > h×2/3): `realworld` treatment
- Upper two-thirds (Y < h×2/3): `glitch` treatment
- ~200px vertical gradient blend zone at the boundary
- Implementation: both treatments applied to full image, blended via vertical gradient mask

---

## Color Preservation

- **GL-07 CORRUPT_AMBER (#FF8C00)**: Protected in chalk pass by hue range guard (PIL hue 8–25). Scanlines and color separation have negligible impact on saturation.
- **GL-01b BYTE_TEAL (#00D4E8)**: No desaturation risk (cyan hue not in amber protection range; not affected by warm bleed pass).
- All passes operate at low opacity — canonical palette hues shift <5° on color wheel.

---

## Intensity Notes

- `intensity=0.6` used on SF01 (Discovery, A+ locked) — conservative application. All effect alphas reduced to 60%.
- `intensity=1.0` standard for all other assets.
- Range: 0.0 (no effect) to 2.0 (maximum). All pass alphas scale proportionally.

---

## Reproducibility

All outputs are fully reproducible: identical `input_path + mode + intensity + seed` always produces identical output. Default seed=42 used for all Cycle 23 assets.

---

## SF01 Flag for Review

SF01 (`discovery_v003_styled.png`) was treated at intensity=0.6 per brief instructions (A+ locked, apply very conservatively). **Flagged for Alex Chen's review** before committing as final. The conservative pass adds subtle paper warmth but should not degrade the locked composition.
