**Date:** 2026-03-29 19:00
**To:** Maya Santos
**From:** Producer (via Alex Chen)
**Re:** Cycle 26 — Luma Style Consistency Investigation + Fix

---

## Problem: Luma Style Inconsistency

Producer feedback: "The LUMA expression sheet looks nothing like the other images, like LTG_CHAR_luma_classroom_pose_v002. I prefer the look in the classroom pose."

Your expression sheet v005 and the classroom pose are visually inconsistent — they look like different characters or different art styles.

---

## Step 1: Investigate

Compare these files carefully:
- `output/characters/main/LTG_CHAR_luma_expression_sheet_v005.png`
- Any existing classroom pose file: search for `LTG_CHAR_luma_classroom_pose_v002` in `output/characters/`

Also compare generators:
- `output/tools/LTG_CHAR_luma_expression_sheet_v005.py`
- The classroom pose generator (find it in `output/tools/`)

Document the specific differences you find:
- Line weight differences
- Construction method (circle-based vs polygon, etc.)
- Hair rendering (cloud vs individual strands vs spiky)
- Face proportions (eye size ratio, nose style, mouth style)
- Color palette (same skin tone? same hoodie color?)
- Body construction (hoodie shape, limb style)

---

## Step 2: Decision

Alex Chen will send you a directive specifying which specific features from the classroom pose to carry into the expression sheet. Wait for his message before rebuilding.

If no message arrives from Alex by the time you finish Step 1, use your own judgment based on the investigation to align the expression sheet to the classroom pose style.

---

## Step 3: Rebuild if needed

If the styles are substantially different:
- Update `LTG_CHAR_luma_expression_sheet_v005.py` to align with classroom pose visual style
- Regenerate `LTG_CHAR_luma_expression_sheet_v005.png` (overwrite in-place, same version)
- Document what changed in a note to Alex Chen's inbox

Also check: does the turnaround v002 have the same inconsistency? If yes, fix the turnaround too.

---

## Standards
- All output images ≤ 1280px (expression sheet canvas: 1200×900 standard, then thumbnail to ≤1280)
- show_guides=False for pitch exports
- After img.paste(), refresh draw = ImageDraw.Draw(img)

— Alex Chen, Art Director
