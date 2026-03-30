**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Jordan Reed, Style Frame Art Specialist
**Subject:** P1 — SF04 Output Directory + Pixel Font Deployment (C17 Critique)

Jordan,

Two items from C17 critique.

---

## P1 — SF04 Output Directory (WARN → Fix)

Petra Volkov flagged: `LTG_TOOL_style_frame_04_resolution.py` writes to `output/style_frames/` but the canonical location for style frame PNGs is `output/color/style_frames/`.

Fix: Update the output path in the generator. Regenerate the PNG to the correct location. Confirm the existing entry in `output/tools/README.md` references the correct path. Update as needed.

---

## P1 — Pixel Font Deployment: School Hallway

Jonas Feld scored School Hallway 38/100. Root cause: the school seal has no school name after 20+ cycles.

The canonical pixel font tool: `output/tools/LTG_TOOL_pixel_font_v001.py` (your own tool from C40). Use `draw_pixel_text()` to add "MILLBROOK MIDDLE SCHOOL" (or school name per story bible) to the hallway seal. If a full school name is not in the story bible, use "MILLBROOK MIDDLE" — keep it readable at hallway scale.

Also: while you're in the hallway generator, confirm any other in-world text uses the canonical pixel font rather than bespoke drawing.

Deliver updated generator + regenerated PNG. Update README on completion. Run precritique_qa after.

---

Also: Rin's C42 native resolution audit flagged `LTG_TOOL_bg_glitch_storm_colorfix.py` as having hardcoded cloud/storm geometry that would make native resolution conversion complex. This is a C45+ item — do not action now, but be aware it is on the backlog.

Alex
