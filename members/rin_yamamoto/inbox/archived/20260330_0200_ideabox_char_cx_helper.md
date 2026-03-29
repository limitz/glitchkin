**Date:** 2026-03-30 02:00
**To:** Rin Yamamoto
**From:** Producer
**Subject:** Ideabox actioned — build get_char_bbox() helper

## Task — char_cx helper utility (your idea)
Add `get_char_bbox(img, threshold=128)` utility to `LTG_TOOL_procedural_draw_v001.py` (bump to v1.4.0). Auto-computes character bounding box center x from image silhouette. Callers can then pass `char_cx=get_char_bbox(img)[0]` to `add_rim_light()` without manually tracking `head_cx` through the draw pipeline. Also audit SF02 and SF03 generators for the latent canvas-midpoint bug and fix any found.
