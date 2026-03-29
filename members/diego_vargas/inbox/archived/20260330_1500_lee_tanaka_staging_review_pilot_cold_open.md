**Date:** 2026-03-30 15:00
**From:** Lee Tanaka (Character Staging & Visual Acting Specialist)
**To:** Diego Vargas
**Subject:** Staging Review — Pilot Cold Open (`LTG_SB_pilot_cold_open_v001.png`)

Hi Diego,

Strong first storyboard. The six-panel arc is coherent and the palette choices are disciplined. Specific notes below.

---

## What's Working

**P1 WIDE / P2 OTS / P3 INSERT ECU** — the first three panels follow the correct compression sequence: WIDE (establish space) → OTS (Luma's perspective claimed) → INSERT ECU (Glitch element fills frame). This is textbook and it works. The OTS face reflection in the dark glass is a strong image: Luma's real face overlaid with the screen's digital void is thematic content, not just framing.

**P5 glass split (two-world boundary)** — this is the best composition decision in the sheet. A vertical split with warm Real World left / Glitch World right is a visual grammar that will carry through the entire show. It's clear, it's original, it's repeatable. Well done.

**Arc-color border scheme** — good practice, consistent with project standard. Arc reads cleanly at contact sheet scale.

---

## Issues to Address

### P4 — "cyan bleeds into warm room" needs spatial clarity
The beat description says Luma leans in and cyan bleeds into the Real World space. This is a crucial narrative moment (first intrusion). The staging question is: **where exactly does the intrusion show up?** If it's a light spill on Luma's face — great, but it must be directional from the screen side. If it's physical pixel scatter on the furniture, it must be positioned to show contact, not drift. Caption "Luma leans in — Glitch colors intrude" tells me the intention, but the image needs to show the intrusion's **origin point and direction**, not just its presence. Add a visible source and a vector.

### P6 — THE NOTICING expression: asymmetry needs to be legible at MCU scale
The pitch notes confirm asymmetry is intentional (left brow high = wonder, right brow straight/furrowed = apprehension). At MCU scale (head filling a significant portion of the 800×600 panel), this asymmetry should be readable. **The risk:** if the brow differential is ≤ 3px vertical gap, it reads as a drawing error, not an intention. Rule: left-brow apex must be at least 6–8px higher than right-brow line at MCU head scale. Also confirm: the iris catch light (cyan glow from CRT) is hitting the correct eye first — it should hit the left eye (screen side, if screen is camera-left) stronger than the right.

Per project gate: run `output/tools/LTG_TOOL_character_face_test_v001.py --char luma` to verify the expression geometry is legible at panel head scale before submitting revisions.

### P3 INSERT ECU — Glitchkin pixel shapes
The brief says "pixel glitch bursts — ELEC_CYAN + HOT_MAGENTA pixels form." Confirm the pixel shapes in the INSERT are **4-7 sided irregular polygons** (project standard from Cycle 11 — see `panel_chaos_generator.py` or any P22/P24 panel for reference). No rectangles. The Glitchkin must have organic edges even at their earliest formation moment.

---

## Camera Grammar: Consistency with SF Language

Your camera choices map correctly to the established style frame grammar:
- WIDE establishing with high angle (matches SF02 Dutch-tilt wide convention)
- ECU for digital/Glitch content (matches P03/P22 cold open tradition)
- MCU for character-emotion beats (matches A1-03 v002 Discovery standard)

The one gap is **P4**: it's labeled MCU PUSH-IN, which implies a camera move. In storyboard shorthand, this should show either a zoom indicator (arrow from current frame crop to tighter crop) or two discrete frames labeled START / END PUSH. As-is it reads as a single MCU frame. Either clarify the notation or split into two panels.

---

## Bottom Line

P1/P2/P3/P5 are production-ready. P4 needs intrusion directionality. P6 needs brow-differential verification (6–8px minimum gap) and iris catch-light directionality. The glass-split grammar in P5 is a genuine visual contribution — hold onto it.

Ready to review a v002 pass once you have the P4 and P6 fixes in.

— Lee
