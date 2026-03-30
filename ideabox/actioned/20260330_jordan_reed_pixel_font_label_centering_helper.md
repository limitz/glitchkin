**Author:** Jordan Reed
**Cycle:** 40
**Date:** 2026-03-30
**Idea:** Add a `draw_centered_label(draw, cx, cy, text, color, scale=1, bg_color=None, padding=2)` helper to `LTG_TOOL_pixel_font_v001.py`. It would use `measure_pixel_text()` to compute text width, draw an optional filled background rectangle (with padding), then render the text centered on `(cx, cy)`. This removes the per-caller centering math that already appeared twice in the kitchen generator (paper scrap + pip pip). Any future prop label — magnets, name tags, sticky notes — would need the same centering pattern.
**Benefits:** Saves every caller the 3-line measure + offset calc. Reduces risk of off-center labels. Particularly useful for Diego (storyboard callout boxes) and Hana (ENV prop signage) where centered text on small patches is common.
