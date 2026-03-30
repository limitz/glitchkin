# Stylization Preset — Hand-Drawn v001 / v002
**Tools:**
- `output/tools/LTG_TOOL_stylize_handdrawn.py` — Cycle 23 (RETIRED — do not use on new assets)
- `output/tools/LTG_TOOL_stylize_handdrawn.py` — Cycle 25 (CURRENT — use for all new assets)

**Author:** Rin Yamamoto / Cycle 23 / 2026-03-29
**v002 Update:** Rin Yamamoto / Cycle 25 / 2026-03-29

---

## Assets Treated (Cycle 23)

| Asset | Mode | Intensity | Seed | Output |
|-------|------|-----------|------|--------|
| `LTG_COLOR_styleframe_glitch_storm.png` | mixed | 1.0 | 42 | `LTG_COLOR_styleframe_glitch_storm_v005_styled.png` |
| `LTG_COLOR_styleframe_otherside.png` | glitch | 1.0 | 42 | `LTG_COLOR_styleframe_otherside_v003_styled.png` |
| `LTG_COLOR_styleframe_discovery.png` | realworld | 0.6 | 42 | `LTG_COLOR_styleframe_discovery_v003_styled.png` |
| `LTG_ENV_grandma_kitchen.png` | realworld | 1.0 | 42 | `LTG_ENV_grandma_kitchen_styled.png` |

## Assets Treated (Cycle 25) — v002 Tool

| Asset | Mode | Intensity | Seed | Output | Notes |
|-------|------|-----------|------|--------|-------|
| `LTG_COLOR_styleframe_glitch_storm.png` | mixed | 1.0 | 42 | `LTG_COLOR_styleframe_glitch_storm_v005_styled_v002.png` | SF02 — rebuilt with Fix 4 cross-dissolve; HOT_MAGENTA crack elements verified readable |
| `LTG_COLOR_styleframe_otherside.png` | glitch | 1.0 | 42 | `LTG_COLOR_styleframe_otherside_v003_styled_v002.png` | SF03 — Byte teal GL-01b protected; zero warm light confirmed |

**SF01 Discovery:** LOCKED — v001 output (`discovery_v003_styled.png`) approved by Alex Chen. Not reprocessed with v002.

---

## Assets Treated (Cycle 24)

| Asset | Mode | Intensity | Seed | Output | Notes |
|-------|------|-----------|------|--------|-------|
| `LTG_ENV_tech_den.png` | realworld | 0.8 | 42 | `LTG_ENV_tech_den_styled.png` | Tech Den is Real World room; intensity 0.8 preserves tech/screen detail |
| `LTG_CHAR_lineup.png` | realworld | 0.7 | 42 | `LTG_CHAR_lineup_v003_styled.png` | Character sheets need lighter touch; intensity 0.7 preserves line clarity |

---

---

## v002 Changes (Cycle 25) — Critical Fixes

### Fix 1 — Full Canonical Color Protection
All canonical palette colors are now protected across all color-modifying passes (chalk highlights, color bleed).

**PROTECTED_HUES table** (PIL HSV hue, 0–255 range):

| Color | Hex | PIL Hue Center | Tolerance |
|-------|-----|---------------|-----------|
| CORRUPT_AMBER | #FF8C00 | ~23.3 | ±12 |
| BYTE_TEAL | #00D4E8 | ~131.2 | ±12 |
| UV_PURPLE | #6A0DAD | ~194.7 | ±12 |
| HOT_MAGENTA | #FF0080 | ~233.7 | ±12 |
| ELECTRIC_CYAN | #00F0FF | ~130.0 | ±12 |
| SUNLIT_AMBER | #D4923A | ~24.3 | ±12 |

Any pixel whose PIL hue falls within any range above is skipped entirely in color-modifying passes.

### Fix 2 — Chalk Pass Exclusions
The chalk pass (`_pass_chalk_highlights`) now additionally skips:
- **(a) Cyan-family pixels**: PIL H 100–160. Protects CRT screen glow, Byte teal, Electric Cyan specular pops.
- **(b) Light source pixels**: V > 216 AND S > 100 in non-protected hues. Protects warm cream ceilings, sunlit wall values, CRT glow (which are saturated light sources, not material surfaces that should look chalky).

### Fix 3 — Warm Bleed Zone Boundary Gate
`_pass_color_bleed()` now checks the source pixel's PIL hue before including it in the warm detection mask.
- **Gate**: if source pixel PIL H is 100–160 (cyan family), it is excluded from the warm bleed source mask.
- Prevents SUNLIT_AMBER from bleeding into cyan-lit skin regions (Luma face split, Glitch Layer boundaries).

### Fix 4 — Mixed Mode Cross-Dissolve Compositing
`_apply_mixed_treatment()` (mixed mode, SF02) now uses per-pixel weighted-average blend in the transition zone.
- Formula: `blended = (1 - blend_weight) * realworld_pixel + blend_weight * glitch_pixel`
- `blend_weight` is a smooth-step spatial gradient (0.0=realworld, 1.0=glitch) across the ~200px transition zone.
- Replaces the previous `alpha_composite` approach which produced double-edge ghost artifacts.
- Pure zones (above and below transition) still copy pixel rows directly for performance.

### Verification Step
After every `stylize()` call, `verify_canonical_colors()` runs automatically and prints:
- OK message if all canonical colors within 5° (≈3.5 PIL hue units) of canonical.
- WARNING per color if drift detected. Batch-safe — does NOT abort.
- TODO: Replace inline implementation with Kai Nakamura's `LTG_TOOL_color_verify.py` import once available.

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

**Status (Cycle 24):** No revision request received from Alex Chen. SF01 styled output remains as-is pending Alex's confirmation.
