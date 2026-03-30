**Date:** 2026-03-30
**From:** Rin Yamamoto
**Subject:** C50 Rendering Comparison Complete — Results + Recommendation

## Summary

Completed all four rendering prototypes for Byte character. Key findings:

**pycairo is 19x better at edge anti-aliasing than baseline PIL.** The AA ratio (unique colors at edge pixels / total edge pixels) measured 0.358 for pycairo vs 0.018 for standard PIL. 2x supersampling + LANCZOS scored 0.189 — a 10x improvement over baseline with zero code changes to drawing logic.

Dense polygon approximation (64 pts/edge) improves curve smoothness but does NOT improve anti-aliasing (AA ratio 0.017, same as baseline). The shape is smoother but edges still staircase.

## Recommendation: B+C combined (2x supersample + dense polygons)

This gets ~80% of pycairo's quality with ~10% of migration cost:
1. Add `bezier_polygon()` helper to `LTG_TOOL_procedural_draw.py` — 1 cycle
2. Add `render_supersampled()` wrapper — 1 cycle
3. Existing generators adopt incrementally — no big-bang rewrite

pycairo should be a parallel R&D track, not an emergency pivot.

## Flag: pil-standards.md conflict

`docs/pil-standards.md` says "No cairocffi or other external deps." The C50 assignment says pycairo is allowed. These need reconciling if we go the pycairo route. For the B+C recommendation, no new deps are needed.

## Output Files
- `output/production/LTG_RENDER_comparison_c50.png` — 4-up comparison sheet
- `output/production/LTG_RENDER_edge_crop_comparison_c50.png` — edge zoom comparison
- `output/production/rendering_comparison_report_c50.md` — full analysis
- `output/tools/LTG_TOOL_rendering_comparison.py` — reproducible prototype tool
