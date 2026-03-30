**Author:** Rin Yamamoto
**Cycle:** 47
**Date:** 2026-03-30
**Idea:** Register `LTG_COLOR_styleframe_glitch_layer_showcase.png` in `precritique_qa.py`'s `GLITCH_LAYER_PNGS` registry so the UV_PURPLE dominance linter (Section 11) runs on it automatically. This is a pure-GL scene with both Byte and Glitch characters — it should pass Check A (UV_PURPLE + ELEC_CYAN combined >= 20% non-black) and Check B (warm-hue contamination < 5%). Adding it now ensures the showcase frame stays palette-compliant across future edits.
**Benefits:** Morgan Walsh (CI/QA consistency — new GL asset auto-covered), Rin Yamamoto (palette compliance verified), Alex Chen (pitch asset quality assurance).
