**Date:** 2026-03-30
**From:** Alex Chen
**Subject:** Wand Compositing — APPROVED, Hybrid Architecture Adopted

Hana,

Your Wand evaluation is approved. The hybrid architecture is adopted as the production compositing pipeline:

**PIL generates > pycairo renders characters > Wand composites > PIL runs QA**

Specific approvals:
1. `wand_scene_lighting_overlay()` with Screen blend — approved for all CRT/lamp/window scenes
2. `wand_color_transfer()` with Soft Light — approved as the solution to environment-to-character tinting (the #1 compositing gap from C50)
3. Native Gaussian blur for contact shadows — approved, replaces multi-ellipse PIL workaround
4. Native morphology for edge tint — approved

Next steps for you:
- Coordinate with Jordan on integrating Wand compositing into style frame generators. Jordan has the scene-lit prototype (SF01) ready for extraction to shared module. Your Wand compositor should be the compositing layer in that shared module.
- Graceful fallback is mandatory — if libmagickwand is missing, fall back to PIL compositing silently.

Your line texture mismatch finding from C50 is now a quality gate (Gate 6 in the updated spec). Variable-width stroke via cairo + paper texture pass via Wand/PIL. Well caught.

— Alex
