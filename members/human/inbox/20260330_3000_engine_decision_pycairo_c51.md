**Date:** 2026-03-30
**From:** Rin Yamamoto
**Subject:** DRAWING ENGINE DECISION — pycairo (P0 unblock for all character work)

Producer, the engine benchmark is complete. **Recommendation: pycairo.**

## Summary

Benchmarked pycairo vs PIL 2x+LANCZOS vs PIL baseline on identical Byte character renders. pycairo wins on:

1. **Features**: Only engine with native bezier curves, variable-width strokes, gradient fills, compositing operators, clip paths. PIL has none of these.
2. **Performance**: 3.1ms vs 81.8ms (PIL 2x) — 26x faster than the supersampling approach.
3. **Quality**: 0.2142 AA ratio (5x better than PIL baseline 0.0449). Native sub-pixel anti-aliasing on all edges.
4. **Reference alignment**: Owl House / Hilda / Kipo all use smooth bezier outlines, variable stroke weight, gradient fills — only pycairo can match this.
5. **PIL interop**: Cairo surface converts to PIL Image in 0.44ms via numpy. Existing compositing pipeline continues unchanged.

skia-python and aggdraw could not be installed (pip blocked). Even if available, pycairo's results are strong enough that neither could change the outcome.

## Deliverables

- `output/tools/LTG_TOOL_cairo_primitives.py` (v1.0.0) — shared primitives library, ready for all generators
- `output/tools/LTG_TOOL_engine_benchmark_c51.py` — benchmark tool
- `output/production/engine_benchmark_report_c51.md` — full report with data
- 6 comparison PNGs in `output/production/LTG_RENDER_engine_*_c51.png`

The team is unblocked. Character generators can begin importing `LTG_TOOL_cairo_primitives` immediately.

— Rin
