**Date:** 2026-03-29 09:00
**From:** Alex Chen, Art Director
**To:** Sam Kowalski, Color & Style Artist
**Re:** Cycle 16 Work Assignments

Sam,

Three tasks this cycle, in priority order.

---

## TASK 1 — Fix Byte Body Fill in Expression Sheet v002 Generator [PRIORITY 1]

**File:** `/home/wipkat/team/output/tools/LTG_TOOL_byte_expression_sheet_v002.py`
**Issue:** Naomi Bridges (Critique C8) found body fill using GL-01 Electric Cyan `#00F0FF` instead of GL-01b Byte Teal `#00D4E8`. Confirmed: `BYTE_TEAL = (0, 212, 232)` is already correct in the constant definition, but verify the constant is actually USED in `draw_byte()` body ellipse fill (line ~440). If it is correct, double-check shadow values — Naomi also flagged shadow drifting to generic cool grey instead of GL-01a Deep Cyan. Fix all violations.

**Additional fixes in the same pass:**
- ALARMED panel background: current `BG_ALARM = (44, 22, 18)` reads warm cocoa — semantically wrong for a danger state. Change to a deep red-tinged cool: suggest `(22, 14, 30)` or similar — must read as danger without warmth.
- Pixel faceplate must be consistent size across all 8 expressions — verify this in the generator.

**Regenerate:** `LTG_CHAR_byte_expression_sheet_v002.png` (overwrite the file — same version, this is a fix pass on the existing v002).

**Send me the SF03 color review notes when this is done.** (See Task 3.)

---

## TASK 2 — Fix DRW-07 and ENV-06 in SF02 Generator [PRIORITY 1]

**File:** `/home/wipkat/team/output/tools/LTG_TOOL_style_frame_02_glitch_storm_v002.py`

**DRW-07 fix:** `DRW_HOODIE_STORM` is currently `(192, 122, 112)` = `#C07A70`. The corrected value is `#C8695A` = `(200, 105, 90)`. Update the constant and regenerate.

**ENV-06 check:** `TERRA_CYAN_LIT = (150, 172, 162)` — verify G=172>R=150, B=162>R=150. This was fixed in Cycle 13 by Jordan, but Naomi re-flagged it as still failing. Check the actual tuple and confirm it satisfies G>R AND B>R. If wrong, fix it.

Do NOT regenerate the SF02 output image — that belongs to Jordan Reed's fix pass this cycle. Your job here is just the color constant corrections. Confirm the values in a reply to me.

---

## TASK 3 — SF03 Color Review Notes [AFTER Task 1 complete]

Once the expression sheet is regenerated and the SF02 constants are fixed, send me your SF03 color review notes. These should address:
1. UV Purple ambient read across the full frame — does it hold?
2. Inverted atmospheric perspective — far structures darker/more purple?
3. Byte dual-eye legibility at production scale (Victoria/Naomi flagged this as the frame's entire emotional payload)
4. Confetti density — is ambient (seed=77, 50 particles) the right call or is it too sparse?
5. Abyss below platform — does BELOW_VOID read as infinite drop vs. just dark?

These notes will feed back to Jordan for the SF03 fix pass.

---

## Notes from Cycle 15 Messages

Thank you for the DRW-18/ENV-13 palette additions and the GL-01 vs GL-01b reminder. The SF03 color notes doc at `output/color/palettes/sf03_other_side_color_notes.md` and the classroom verification are logged.

—Alex Chen
Art Director
Cycle 16
