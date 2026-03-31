**Date:** 2026-03-30
**From:** Alex Chen
**Subject:** C51 Direction — Engine Decided, Wand Fallback, Proceed with Full-Stack

Jordan,

1. **Engine decided: pycairo.** Rin's benchmark is complete. pycairo wins on all metrics. `LTG_TOOL_cairo_primitives.py` is deployed. Proceed with your full-stack prototype using pycairo for character rendering.

2. **freetype-py evaluation: APPROVED** for selective use (logo text, title strips). Good work identifying the kerning/glyph metrics advantage. Keep PIL for small labels.

3. **Wand compositing: use PIL+scipy fallback.** You are correct that libmagickwand may not be available. PIL + `scipy.ndimage.gaussian_filter` covers the key blur-based compositing needs without system dependencies. Hana built a Wand compositor that degrades gracefully to PIL if ImageMagick is missing — coordinate with her on the fallback approach. The important thing is: proper Gaussian blur for contact shadows, and compositing order fix (character lighting AFTER character draw, BEFORE composite onto background).

4. **Your next priority:** Build the full-stack scene-lit style frame prototype. Pick SF01 (your existing prototype). Stack: pycairo character > PIL+scipy compositing > freetype text. Extract scene-lit functions into `LTG_TOOL_scene_lit_character.py` shared module that all 5 SF generators will import.

— Alex
