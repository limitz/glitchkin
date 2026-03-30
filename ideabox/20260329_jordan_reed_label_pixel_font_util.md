**Author:** Jordan Reed
**Cycle:** 39
**Date:** 2026-03-29
**Idea:** Create a small shared pixel-font utility for drawing legible short text strings in PIL without font file dependencies. Right now drawing "MIRI" required hand-coding letter geometries as line segments — fragile, slow to author, and hard to verify visually. A reusable `draw_pixel_text(draw, x, y, text, color, scale=1)` function with a built-in 5x7 pixel bitmap for A-Z/0-9 would handle all future in-world prop text (labels, signs, notices, calendar headers) consistently and quickly. Register as `LTG_TOOL_pixel_font_v001.py`.
**Benefits:** Any team member drawing real-world signage, notices, or labels in PIL environments. Eliminates per-letter hand-coding, ensures uniform legible results, and supports scale parameter for varying prop distances.
