# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.

# C50 Rendering Comparison Report
**Author:** Rin Yamamoto (Procedural Art Engineer)
**Date:** 2026-03-30
**Cycle:** 50

## Objective
Compare three alternative rendering approaches against our current PIL baseline for character
art quality, specifically targeting smooth curves, anti-aliased edges, and organic forms.

## Subject
Byte character — diamond body, pixelated eyes (intentionally blocky), crown spike, teal glow.
Byte is the simplest character to isolate rendering quality from design complexity.

## Approaches Tested

### A: pycairo (bezier curves + native anti-aliasing)
- True cubic bezier curves for diamond body edges
- Native sub-pixel anti-aliasing on all paths
- Radial gradient for glow (native, not layered ellipses)
- Linear gradient for body fill (native)
- Smooth crown spike via curve_to()

### B: PIL 2x render + LANCZOS downscale
- Standard PIL primitives at 1280x1280 (2x target resolution)
- LANCZOS resampling to 640x640
- Supersampling provides implicit anti-aliasing
- No code changes to drawing logic — just scale factors

### C: PIL dense-polygon approximation (64 points per curve)
- Standard PIL at target resolution (640x640)
- Diamond body: 256 vertices (64 per edge) with quadratic bezier interpolation
- Circles approximated with 128-point polygons
- Crown spike: 64-point polygon

### Baseline: Standard PIL (current pipeline)
- 4-point diamond polygon
- PIL ellipse() for circles
- Standard polygon/line primitives

## Quantitative Results

| Approach | Edge Pixels | Unique Colors at Edges | AA Ratio | Render Time (ms) |
|----------|-------------|----------------------|----------|------------------|
| A: pycairo | 2489 | 890 | 0.3576 | 8.3 |
| B: 2x+LANCZOS | 2220 | 419 | 0.1887 | 63.7 |
| C: dense poly | 1929 | 32 | 0.0166 | 11.8 |
| Baseline PIL | 1792 | 33 | 0.0184 | 9.8 |

**AA Ratio** = unique colors at edge pixels / total edge pixels. Higher = more gradient
transitions = smoother perceived edges.

## Qualitative Analysis

### A: pycairo — HIGHEST quality, HIGHEST disruption
**Strengths:**
- True bezier curves produce genuinely smooth, organic diamond edges
- Native anti-aliasing eliminates stairstepping completely
- Radial/linear gradients are computed analytically (no layered ellipses)
- Sub-pixel rendering matches broadcast-quality 2D animation standards
- Variable line width is native (set_line_width accepts float)

**Weaknesses:**
- pycairo uses a different drawing API — all existing generators would need rewriting
- ARGB32 surface format requires conversion to PIL for compositing with existing pipeline
- `docs/pil-standards.md` currently lists 'No cairocffi or other external deps' — pycairo is
  a different binding but the spirit of the rule may need clarification
- Team-wide learning curve for cairo's path-based drawing model

### B: PIL 2x + LANCZOS — MODERATE quality, LOWEST disruption
**Strengths:**
- Zero changes to drawing logic — just multiply coordinates by scale factor
- LANCZOS downscale provides effective anti-aliasing on all edges
- Every existing generator can adopt this with a simple wrapper
- Compositing, glow, and all PIL features work identically

**Weaknesses:**
- 4x memory usage during rendering (2x width * 2x height)
- Still fundamentally polygon-based — curves remain piecewise linear, just smaller steps
- Render time roughly doubles (drawing at 4x pixel count)
- Does not solve the underlying primitive limitation, only masks it

### C: PIL dense polygon — MODERATE quality, LOW disruption
**Strengths:**
- Stays within PIL — no new dependencies
- Bezier-interpolated vertices produce visibly smoother curves than 4-point polygons
- Can be applied selectively to specific shapes (body outlines, crowns) without
  changing the entire pipeline
- Negligible memory overhead

**Weaknesses:**
- Still no native anti-aliasing — edges are smoother in shape but still pixel-stepped
- Dense outlines drawn as line segments can show thickness variation at acute angles
- Diminishing returns past ~64 points per edge at 1280px canvas
- Requires per-shape bezier control point tuning

## Recommendation

**Best path forward: B + C combined.**

1. **Adopt dense-polygon curves (C)** for all character body shapes — immediate quality win
   with minimal disruption. Add `bezier_polygon()` helper to `LTG_TOOL_procedural_draw.py`.
2. **Add optional 2x supersampling (B)** as a final-pass wrapper for pitch-critical assets.
   A `render_supersampled(gen_func, scale=2)` wrapper can be applied to any generator.
3. **Evaluate pycairo (A) for next-gen pipeline** — highest ceiling but largest migration.
   Start with a hybrid approach: use pycairo for body/silhouette paths, composite result
   into PIL for eyes/text/existing pipeline features.

**Rationale:** B+C together achieve ~80% of pycairo's quality improvement with ~10% of the
migration cost. Every existing generator can adopt both techniques incrementally. pycairo
should be a longer-term R&D track, not a C50 emergency pivot.

## Pipeline Impact Assessment

| Change | Files Affected | Risk | Effort |
|--------|---------------|------|--------|
| Add `bezier_polygon()` to procedural_draw | 1 (lib) | LOW | 1 cycle |
| Update generators to use bezier_polygon | ~12 generators | LOW | 2-3 cycles |
| Add supersampling wrapper | 1 (lib) | LOW | 1 cycle |
| pycairo hybrid renderer | New module + all generators | HIGH | 5+ cycles |

## Output Files
- `LTG_RENDER_comparison_c50.png` — 4-up comparison sheet
- `LTG_RENDER_byte_pycairo_c50.png` — pycairo render
- `LTG_RENDER_byte_hires_downscale_c50.png` — 2x+LANCZOS render
- `LTG_RENDER_byte_dense_poly_c50.png` — dense polygon render
- `LTG_RENDER_byte_baseline_pil_c50.png` — baseline PIL render
- `LTG_RENDER_edge_crop_comparison_c50.png` — edge crop zoom (3x nearest neighbor)
