**Date:** 2026-03-30
**From:** Kai Nakamura, Technical Art Engineer
**To:** Alex Chen, Art Director
**Subject:** C41 Completion Report — luma_face_curves v1.1.0 (Eye-Width Correction)

Alex,

C41 work complete.

---

## Task 1 — `LTG_TOOL_luma_face_curves.py` v1.1.0 (P1 — DONE)

**Critical eye-width correction applied per `luma_face_curve_spec.md` v002:**

| Point | v001 (wrong) | v002 (correct) |
|---|---|---|
| LE_P0 | FC+(-72,-22) | FC+(-94,-22) |
| LE_P2 | FC+(-16,-22) | FC+(+6,-22) |
| RE_P0 | FC+(+16,-22) | FC+(-6,-22) |
| RE_P2 | FC+(+72,-22) | FC+(94,-22) |
| Eye width | 56px | 100px canonical |

**Reference sheet updated:**
- 3×3 grid, all 9 expressions (6 canonical + 3 Maya Santos supplement)
- Each cell 600×600px, thumbnailed to ≤1280px per image rules
- Supplement row labeled `[supplement]` with distinct header tint for visual distinction
- Output path: `output/characters/luma_face_curves_reference.png`

Module API unchanged: `draw_luma_face(draw, fc, expression, overrides=None)` works identically. Any caller using FC-relative iris positions from v001 should note the eye bounding box is now wider — iris clamping will keep iris within the corrected (larger) eye.

## Task 2 — G007 Fix

Task 2 in the C41 brief describes the G007 fix as requiring a "distinguishable non-black color" for Glitch body outline. I note that `glitch.md` specifies VOID_BLACK outline for the Glitch body polygon (spec §2.2), and the G007 linter (`LTG_TOOL_glitch_spec_lint.py`) checks for VOID_BLACK specifically. The C40 fix applied VOID_BLACK to SF02 and SF03, which is correct per glitch.md. If the intended fix is different from the spec, please clarify whether glitch.md should be updated to specify a different outline color — I'll hold further changes to the G007 fix pending your direction.

## Task 3 — precritique_qa Version Collision

Already resolved at v2.8.0 (Morgan Walsh C39 + Kai C39 merge, documented in file docstring). No action needed.

---

Let me know if the 100px eye width needs further control-point tuning after your first render review.

— Kai Nakamura, Technical Art Engineer
