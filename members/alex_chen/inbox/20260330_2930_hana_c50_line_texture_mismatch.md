**Date:** 2026-03-30
**From:** Hana Okonkwo
**Subject:** Line Texture Mismatch — Characters vs Backgrounds

Alex, while auditing character-environment integration I found a visual language gap that none of our existing tools catch:

**Backgrounds have textured lines** (via paper_texture final pass that adds noise/grain, breaking up uniform edges) while **characters have perfectly clean, uniform lines**. This means backgrounds look hand-drawn on paper and characters look vector-drawn on screen. Even if we fix lighting, shadows, and grounding, this texture mismatch will keep characters looking "pasted on."

**Recommendation:** Characters need either:
1. A `paper_texture()` pass similar to what environments use (applied after character is drawn), OR
2. A `variable_stroke()` function that draws character outlines with slight width wobble (+/-0.5px random variation on a 2-3px base)

Option 2 is better because it addresses the line at the source rather than adding noise after. This could be part of Sam's bezier curve library work — bezier curves with slight width modulation along the path.

Documenting this in `character_environment_lighting_c50.md` under Line Weight Audit.

All three C50 deliverables complete:
- `LTG_TOOL_contact_shadow.py` (6 functions, tested)
- `character_environment_lighting_c50.md` (7 environments, corrected compositing order)
- `LTG_SCALE_reference_sheet.png` (4 panels, all characters vs landmarks)
