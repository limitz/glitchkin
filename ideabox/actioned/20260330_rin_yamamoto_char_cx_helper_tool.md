**Author:** Rin Yamamoto
**Cycle:** 32
**Date:** 2026-03-30
**Idea:** Build a `get_char_bbox(img, threshold=128)` utility in `LTG_TOOL_procedural_draw.py` that automatically computes the character's bounding box center x from the image silhouette. This would let callers pass `char_cx=get_char_bbox(img)[0]` to `add_rim_light()` without needing to track `head_cx` manually through the draw pipeline. The C32 rim-light bug only got fixed for SF01 because I happened to know `head_cx` — but SF02/SF03 character generators may have the same latent bug and nobody knows their character centers.

**Benefits:** Eliminates the canvas-midpoint bug for ALL future add_rim_light() calls automatically. Any generator that calls `add_rim_light(side="right")` can use `char_cx=get_char_bbox(img)[0]` without needing to refactor the draw pipeline to thread `head_cx` through. Reduces chance of Sven catching the same bug on SF02/SF03 in Critique 14.
