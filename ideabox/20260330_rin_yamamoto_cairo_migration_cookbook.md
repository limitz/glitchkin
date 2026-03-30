**Date:** 2026-03-30
**From:** Rin Yamamoto
**Idea:** Cairo Migration Cookbook for Generator Authors

Now that pycairo is the official engine, every generator author needs a quick-reference guide for converting PIL draw calls to cairo equivalents. I propose writing a `docs/cairo-migration-cookbook.md` with:

1. **Side-by-side recipes**: PIL `draw.polygon()` → cairo `move_to/curve_to/fill/stroke`
2. **Common patterns**: fill+outline, gradient fill, tapered stroke, wobble outline
3. **Import boilerplate**: how to import `LTG_TOOL_cairo_primitives` from any tool location
4. **PIL interop**: when to convert to PIL and back (compositing, glow layers, text)
5. **What NOT to migrate**: background generators, contact sheets, grids — PIL is fine there
6. **Gotchas**: BGRA byte order, ARGB32 format, refreshing draw context after paste

This saves every team member from re-discovering the same patterns. Estimated effort: 1 hour.
