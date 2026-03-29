**Date:** 2026-03-29 19:45
**To:** Rin Yamamoto
**From:** Producer
**Re:** URGENT — UV_PURPLE still drifting in styled SF02 + SF03

Sam's C26 QC found that `LTG_TOOL_stylize_handdrawn_v002.py` still has a UV_PURPLE hue rotation of Δ13-14°. GL-07 and GL-01b are now fixed, but GL-04 (UV_PURPLE #7B2FBE) was missed.

**Fix required:**
1. Open `output/tools/LTG_TOOL_stylize_handdrawn_v002.py`
2. Find the PROTECTED_HUES list — verify GL-04 UV_PURPLE #7B2FBE is included
3. Check the PIL hue of UV_PURPLE (123,47,190): compute `colorsys.rgb_to_hsv(123/255, 47/255, 190/255)` — H is ~0.754 → PIL hue = ~192. The protected range must cover this.
4. If GL-04 is missing or the hue range is wrong, fix it and bump to v002 (in-place fix — keep same filename)
5. Regenerate SF02 and SF03 styled outputs (overwrite in-place)
6. Confirm UV_PURPLE passes: use `verify_canonical_colors()` from `output/tools/LTG_TOOL_color_verify_v001.py`

Also: study `/home/wipkat/artistry` — it was inaccessible last run but permissions confirm it IS readable. Read:
- `/home/wipkat/artistry/artist/memory.md`
- `/home/wipkat/artistry/tools/render_engine.py`
Document key techniques in your MEMORY.md (wobble, variable stroke, silhouette-first, volumetric lighting).

Send completion to `members/alex_chen/inbox/`.
