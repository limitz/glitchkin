<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Shoulder Involvement Rule — C47

**Author:** Maya Santos
**Date:** 2026-03-30
**Addresses:** Takeshi critique #3 (persistent since C15)

## Problem

Arms moved without shoulder involvement across all human characters. When arms raised, the torso top line remained flat — deltoids and trapezius did not shift.

## Rule

When a human character's arm raises, the shoulder on that side MUST visually respond:
- The deltoid bump at the torso-top corner rises proportionally to the arm raise.
- This is implemented as additional vertices in the torso top polygon.

## Implementation

### Per-Character Functions

| Character | Function | Rule |
|---|---|---|
| Cosmo | `_shoulder_dy()` in `LTG_TOOL_cosmo_expression_sheet.py` v008 | 25% of arm_dy, capped -8px. Fixed -6px for high-raise modes (head_grab, wide_startle, delighted). |
| Luma | `_luma_shoulder_dy()` in `LTG_TOOL_luma_expression_sheet.py` v014 | 8% of arm endpoint dy, capped -7px. Fixed values for custom-arm expressions (FRUSTRATED -3, WORRIED -4, ALARMED -6). |
| Miri | Inline in `draw_body_miri()` in `LTG_TOOL_grandma_miri_expression_sheet.py` v007 | 20% of arm_dy, capped -5px. Fixed -4px for extended/palms_out arm styles. |

### Geometry

The torso top polygon gains shoulder bump vertices:
```
Before: [left_top, right_top, right_bottom, left_bottom]
After:  [outer_left, left_deltoid_peak, inner_left, inner_right, right_deltoid_peak, outer_right, right_bottom, left_bottom]
```

The `sh_bump_w` (shoulder bump width) extends slightly beyond the torso edge. The deltoid peak vertex is displaced upward by the calculated `l_sh_dy` / `r_sh_dy`.

### Non-Human Characters

Byte and Glitch are non-human (floating robot, diamond sprite) — the shoulder rule does not apply to them.

## Future Work

- Style frame and storyboard panel generators should follow this rule when drawing human characters at sufficient scale.
- The lineup draws characters at small scale where shoulder displacement is sub-pixel — not applicable.
