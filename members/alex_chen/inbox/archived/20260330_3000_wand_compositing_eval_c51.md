**Date:** 2026-03-30
**From:** Hana Okonkwo
**Subject:** C51 Wand Compositing Evaluation Complete

Alex,

Built `LTG_TOOL_wand_composite.py` — reimplements all C50 contact shadow functions using Wand, plus two new capabilities (scene lighting overlays with blend modes, environment-to-character color transfer).

**Summary:**
- Wand is a clear win for the compositing pass. Native Gaussian blur, blend modes (Screen/Multiply/Soft Light), and morphology operations replace our verbose PIL workarounds.
- PIL still wins for generation and QA. No reason to migrate generators.
- Recommended architecture: PIL generates, Wand composites, PIL runs QA.
- Risk: Wand needs libmagickwand system library. Tool degrades gracefully if missing.

**New capabilities Wand enables:**
1. Scene lighting overlays with proper Screen blend (additive light)
2. Environment-to-character color transfer via Soft Light (the #1 gap from C50 lighting spec)

Full evaluation: `output/production/wand_compositing_evaluation_c51.md`

Coordinating with Sam — he's doing Wand for color, no overlap. Submitted ideabox idea for shared conversion utils.

Awaiting your decision on whether to adopt the hybrid approach for style frame compositing.

— Hana
