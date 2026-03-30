<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Luma Expression Sheet — Metadata

**File:** `luma_expression_sheet.png`
**Version:** v2.0 (Cycle 12)
**Generator:** `LTG_CHAR_luma_expression_sheet.py`
**Date:** 2026-03-29
**Designer:** Maya Santos

---

## Canvas Dimensions

| Property | Value |
|---|---|
| Total canvas | 1210 × 886 px |
| Panel size | 280 × 390 px per panel |
| Grid layout | 4 columns × 2 rows (8 panels) |
| Padding between panels | 18 px |
| Header height | 52 px |
| Outer padding | 18 px all sides |

## Head Unit Reference

| Scale level | Head unit value | Notes |
|---|---|---|
| Full render scale (intermediate canvas) | 1 head unit = 200 px | Head radius = 100 px. Used for all face draw functions before resize. |
| Panel scale (FACE_SCALE = 0.55) | 1 head unit ≈ 110 px | After LANCZOS resize into panel. |
| Body height unit (hu) | 140 px | Body proportion base; all body measurements derived as multiples of hu. |
| Sneaker width | hw = int(hu × 0.52) = 73 px | Canonical Cycle 11 normalized value. |

## Version History

| Version | Cycle | Change |
|---|---|---|
| v1.0 | Cycle 11 | Initial release. 3×2 grid, 6 expressions: Reckless Excitement, Worried/Determined, Mischievous Plotting, Settling/Wonder, Recognition, Warmth. |
| v2.0 | Cycle 12 | Expanded to 4×2 grid (8 panels). Added Neutral/Resting and At-Rest Curiosity expressions. Added sheet metadata line in header. Updated WARMTH prev_state from "← was: RECOGNITION" to "← was: ANY EARNED MOMENT" per Dmitri Volkov Cycle 11 feedback. |

## Expression Index

| # | Name | BG Color | Hoodie Color | Body language |
|---|---|---|---|---|
| 1 | Reckless Excitement | (240,200,150) warm amber | Orange | Right arm raised (-8 arm_r_dy), body_tilt=6 |
| 2 | Worried / Determined | (195,212,228) cool blue-grey | Dark | Arms level, no tilt |
| 3 | Mischievous Plotting | (220,205,242) warm lavender | Magenta-purple | Both arms raised asymmetric, body_tilt=-4 |
| 4 | Settling / Wonder | (180,215,205) soft teal-mint | Steel blue | Arms dropped (arm_dy=+8), no tilt |
| 5 | Recognition | (165,185,220) periwinkle | Deep blue | Left arm raised, slight forward lean |
| 6 | Warmth | (250,215,170) soft peach | Warm gold | Arms relaxed down, minimal tilt |
| 7 | Neutral / Resting *(new v2)* | (215,208,198) warm light grey | Warm tan | Arms hang level, no tilt — baseline anchor |
| 8 | At-Rest Curiosity *(new v2)* | (195,218,200) pale sage | Muted sage | Arms nearly neutral, right arm barely +2 |

## Notes

- Face draw functions render on a 400×440 px intermediate canvas, then resized to 220×242 px (FACE_SCALE=0.55) via PIL LANCZOS before compositing into the panel.
- Body draw function (`_draw_body`) renders directly on the main canvas at actual panel coordinates.
- New v2 expressions (slots 7 and 8) are tagged "[NEW]" in the rendered sheet label bar (soft green text).
