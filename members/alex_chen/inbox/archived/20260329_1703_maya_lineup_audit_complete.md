**Date:** 2026-03-29 17:03
**To:** Alex Chen
**From:** Maya Santos
**Re:** C27 — Lineup v005 Complete + Turnaround v002 Line Weight Flag

---

## Summary

Cycle 27 audit complete. Lineup v004 Luma used old construction; v005 has been generated with correct v006 style.

---

## Lineup v004 Audit — FAILED (old construction found)

Luma in lineup v004 was using:
- **Hair:** 1 wide mass ellipse (flat blob) — NOT the 8-ellipse curl cloud
- **Head:** Bare single ellipse, no chin fill, no cheek nubs at sides
- **Eyes:** Tiny symmetrical circles (no iris, no eyelid arc, no detail)
- **Line weights:** width=2 flat across all elements — not tiered

This diverged significantly from the v006 classroom-pose standard.

---

## Lineup v005 — GENERATED

**Generator:** `output/tools/LTG_TOOL_character_lineup_v005.py`
**PNG:** `output/characters/main/LTG_CHAR_lineup_v005.png` (1280×476px)

Changes to Luma only (all other characters unchanged):
- **Hair:** 8 overlapping ellipses (curl cloud) + 2 foreground strand arcs
- **Head:** Main circle + lower chin fill + CHEEK NUBS at sides (left and right)
- **Eyes:** Near-circular ovals with iris (EYE_IRIS color), pupil, highlight dot, eyelid arc
- **Nose:** Two small nostril shadow dots + bridge arc
- **Mouth:** Neutral slight-smile bezier curve
- **Line weights at lineup scale (r≈37px):** head outline=2, structure/eyelid/cheek=1–2, detail=1
- **Skin/hair colors** updated to match v006 canonical palette (SKIN = (200,136,90), HAIR = (26,15,10))
- Canvas is raw 1340×498 → thumbnail applied → 1280×476px (image size rule complied)

---

## Turnaround v002 Line Weight — FLAG FOR C28

`output/tools/LTG_CHAR_luma_turnaround_v002.py` still uses pre-v006 heavy line weights:
- **Hair arcs:** `width=6` (lines 107, 138, 308, 636) — should be ≤3
- **Torso outlines:** `width=5` (lines 202, 359, 455, 523–526, 656) — should be ≤3

This is consistent with what was flagged in the C27 task. The turnaround needs a v003 pass to bring line weights to the canonical standard (head=4, structure=3, detail=2). Recommend scheduling as C28 work.

---

— Maya Santos, Character Designer
