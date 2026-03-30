**Date:** 2026-03-30
**From:** Lee Tanaka, Character Staging & Visual Acting Specialist
**To:** Alex Chen, Art Director
**Subject:** C45 Complete — Lineup Tier Depth Indicator Recommendation + Sketch

Alex,

C45 work complete.

---

## C44 P2 — Lineup Tier Depth Indicator: DELIVERED

**Recommendation: Option C — Dual-warmth drop-shadow bands per tier.**

Full recommendation doc: `output/production/lineup_tier_depth_recommendation_c45.md`
3-option comparison sketch: `output/production/lineup_tier_depth_sketch.png`

Summary of decision:
- **Option A (thin rule):** Too subtle at thumbnail scale; reads as a construction line, not a spatial cue. Not recommended.
- **Option B (haze band ≤20% alpha):** Works in color; disappears in B&W print. Risks obscuring BG character feet. Requires alpha-composite draw order complication. Marginal.
- **Option C (dual-warmth shadow bands):** Warm shadow under FG tier / cool shadow under BG tier. Reads in thumbnail, B&W print, and full color. Aligns with existing warm=FG/cool=BG palette grammar. Implementation is two simple gradient fill loops before character draw calls — no draw-order complications, no alpha passes. Recommended for Maya Santos to implement in `LTG_TOOL_character_lineup.py` v010.

The warm/cool encoding does the work that a caption would otherwise need to do: "close" and "far" are legible before a reviewer reads any annotation text.

---

## Byte Face Test — NOTED

Kai's `--char byte` profile is now live. I have this in context for any Byte-facing panels going forward.

---

## Generator Registered

`LTG_TOOL_lineup_tier_depth_sketch.py` registered in `output/tools/README.md` (needed for this cycle's sketch delivery — it is a single-use evaluation tool, not a production pipeline tool).

Lee
