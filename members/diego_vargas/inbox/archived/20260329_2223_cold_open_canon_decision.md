**Date:** 2026-03-29 22:23
**From:** Alex Chen, Art Director
**To:** Diego Vargas, Storyboard Artist
**Subject:** COLD OPEN CANON DECISION — Your storyboard (night/Grandma's den) is AUTHORITATIVE

Diego,

Official decision: **your storyboard is the authoritative cold open.** Night, Grandma's den, CRT television. This is the version of the cold open we are pitching.

## What was blocked and is now unblocked

Your cold open board and Priya's story bible had conflicting settings. That conflict is resolved:
- Your night/Grandma's den version: **CANONICAL cold open**
- Priya's school/daytime scene: repositioned as a brief pre-credits tag (before main titles), not the cold open itself

You are unblocked to proceed with v002 of the pilot cold open storyboard.

## C38 Fixes Required (from Critique 15 + Lee Tanaka's staging review)

Priority 1 — fix all before delivering v002:

1. **Hoodie color WRONG** — P6 Luma hoodie is slate blue. Canonical = LUMA_HOODIE_ORANGE `(232, 112, 58)` `#E8703A`. Fix in generator.

2. **W004 draw order violation** — stale `draw` object after `img.paste()`. After any `img.paste()`, you must call `draw = ImageDraw.Draw(img)` to refresh. Reinhardt flagged this as a functional code defect. Fix it.

3. **P01/P12/P13 staging** — Lee's notes:
   - P4: "Cyan bleeds into warm room" needs a directional intrusion source (an origin point + vector). Currently reads as ambient, not contact. Add a clear light source.
   - P6: THE NOTICING brow differential must be ≥ 6–8px gap at MCU head scale. CRT iris catch-light must be directional (screen-side eye stronger). Run `output/tools/LTG_TOOL_character_face_test_v001.py --char luma` before delivering v002.
   - P3: Confirm pixel shapes are 4–7 sided irregular polygons (no rectangles).
   - P4: MCU PUSH-IN implies camera move — add zoom indicator or START/END split panel notation.

4. **Naming convention violation** — your generator file is `LTG_SB_pilot_cold_open_v001.py` but lives in `output/tools/`. Files in `output/tools/` must use the `LTG_TOOL_` prefix. Rename to `LTG_TOOL_sb_pilot_cold_open_v002.py` for the v002 delivery. Kai will handle the formal naming sweep, but your new files must be compliant.

5. **Deliver as v002** — file: `output/storyboards/LTG_SB_pilot_cold_open_v002.png`, generator: `output/tools/LTG_TOOL_sb_pilot_cold_open_v002.py`.

## P2: Dual-Miri Visual Plant

Once v002 is delivered, I will brief you (or Jordan Reed) on a subtle visual detail to plant in one existing image that connects Grandma Miri and Glitch Layer Miri. This is a P2 item — do not block v002 on it.

## Confirm

Confirm receipt and estimated delivery for v002.

— Alex Chen
Art Director
