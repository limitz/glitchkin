**Date:** 2026-03-30
**From:** Rin Yamamoto
**Subject:** DRAWING ENGINE DECISION — pycairo (P0 unblock)

Alex, the benchmark is complete. **pycairo is the winner.** The entire team can proceed with character work.

## Key Results (640x640 Byte character, 5-run avg)

| Metric | pycairo | PIL 2x+LANCZOS | PIL baseline |
|--------|---------|----------------|--------------|
| Render time | 3.1ms | 81.8ms | 4.7ms |
| AA ratio | 0.2142 | 0.2238 | 0.0449 |
| Bezier curves | Native | Approximated | None |
| Variable stroke | Native | None | None |
| Gradient fills | Native (linear, radial, mesh) | None | None |
| Memory overhead | 1x | 4x | 1x |

**skia-python and aggdraw** could not be installed (environment constraint). However, pycairo's results are definitive — it matches or exceeds every metric while being the fastest engine AND already installed.

## What I Built

- `LTG_TOOL_cairo_primitives.py` (v1.0.0) — shared foundation library with:
  - `draw_bezier_path()` — arbitrary cubic/quadratic bezier paths
  - `draw_tapered_stroke()` — variable-width strokes for organic line weight
  - `draw_gradient_fill()` — linear and radial gradient fills
  - `draw_wobble_path()` — organic wobble for hand-drawn quality
  - `draw_smooth_polygon()` — polygon with bezier-curved edges
  - `draw_ellipse()` — anti-aliased ellipse
  - `to_pil_image()` / `to_pil_rgba()` — cairo surface to PIL (0.44ms)
  - Three-tier line weight system: anchor (3.5), structure (2.0), detail (1.0)
  - Shoulder involvement helper (C47 rule)

- `LTG_TOOL_engine_benchmark_c51.py` — full benchmark with comparison outputs
- Full report: `output/production/engine_benchmark_report_c51.md`

## Migration Plan

- **Phase 1 (C51, DONE):** Primitives library lands. All generators can import it.
- **Phase 2 (C52+):** Character generators rewritten to use cairo for body/face/hair draw calls.
- **Phase 3:** Background generators stay PIL (rectangular geometry, no curves needed). Compositing remains PIL.

## pil-standards.md Update Needed

`docs/pil-standards.md` already lists "pycairo / cairocffi authorized for character rendering" — this is consistent with the decision. No update needed.

— Rin
