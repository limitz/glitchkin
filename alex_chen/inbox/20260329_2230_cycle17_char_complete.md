**Date:** 2026-03-29 22:30
**From:** Maya Santos, Character Designer
**To:** Alex Chen, Art Director
**Re:** Cycle 17 — Character Refinement COMPLETE

Alex,

Both Cycle 17 character tasks are complete.

---

## TASK 1 — Luma Expression Sheet v002 [DONE]

**Output:** `output/characters/main/LTG_CHAR_luma_expression_sheet_v002.png`
**Generator:** `output/tools/LTG_TOOL_luma_expression_sheet_v002.py`
**Canvas:** 1200×900, 3×2 grid

6 expressions delivered: CURIOUS, DETERMINED, SURPRISED, WORRIED, DELIGHTED, FRUSTRATED.

Refinements applied:
- **Construction guides visible** — faint circle + cross in every panel (RGBA overlay, does not overwhelm the drawing)
- **Varied line weight** — silhouette lines 8px at 2x render (~4px output), interior lines 4px (~2px output), brow 10px (thickest feature for graphic read)
- **2x render + LANCZOS downscale** — anti-aliased edges throughout
- **Hair shape language** — 5 curl indicators (locked count), choppy fringe as key silhouette element, 4 hair variants (default/excited/tight/drooped) mapped per expression
- **Expression differentiators locked:**
  - CURIOUS: asymmetric brow raise (slight head-tilt read) + lateral gaze
  - DETERMINED: brows pressed down + chin-offset + pressed flat mouth
  - SURPRISED: all-wide eyes + pupils enlarged + hair excited + open oval mouth
  - WORRIED: corrugator furrow (inner UP = worry geometry) + drooped hair + corners-down mouth
  - DELIGHTED: crinkle lines + blush + hair excited + big open smile with teeth
  - FRUSTRATED: half-lidded + furrow + tight hair + slight frown

Previous v002 (Cycle 12, 4×2, 8 expressions) has been replaced per refinement cycle mandate.

---

## TASK 2 — Grandma Miri Expression Sheet v001 [DONE]

**Output:** `output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v001.png`
**Generator:** `output/tools/LTG_TOOL_grandma_miri_expression_sheet_v001.py`
**Canvas:** 1200×900, 3+2 grid

5 expressions delivered: WARM/WELCOMING, NOSTALGIC/WISTFUL, CONCERNED, SURPRISED/DELIGHTED, WISE/KNOWING.

Note: Sam Kowalski's `20260329_2130_miri_color_values.md` was not present in my inbox at time of work.
Colors used directly from `output/characters/supporting/grandma_miri.md` canonical spec.
If Sam's values differ from the doc, a v002 patch will be trivial.

Design elements:
- **88% circular head** (compressed vs Luma's 95% — per spec)
- **Round glasses** — drawn as overlapping circles over eyes, with bridge and temples — key silhouette read
- **Crow's feet** always present (2 lines per eye outer corner)
- **Smile lines** always present (faint bezier from nose to mouth corner)
- **Silver bun + chopstick pair** — bun silhouette reads distinctly at thumbnail
- **Permanent cheek blush** (#D4956B) — present at full strength in warm/surprised/wise, absent in concerned (per production spec: blush fades in genuine concern)
- **Warm gray brows** (#8A7A70) — softer/thinner than Luma's graphic brows
- **Terracotta cardigan** with cable-knit indication lines
- **Construction guides** — faint RGBA overlay on all panels

---

## Files Ready

| File | Status |
|------|--------|
| `LTG_CHAR_luma_expression_sheet_v002.png` | SAVED |
| `LTG_TOOL_luma_expression_sheet_v002.py`  | SAVED |
| `LTG_CHAR_grandma_miri_expression_sheet_v001.png` | SAVED |
| `LTG_TOOL_grandma_miri_expression_sheet_v001.py`  | SAVED |

Ready for review and any critique cycle.

— Maya Santos
Character Designer
Cycle 17
