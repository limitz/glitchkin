<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Character Lineup Staging Brief — v008
**Author:** Lee Tanaka, Character Staging & Visual Acting Specialist
**Date:** 2026-03-30
**For:** Maya Santos
**Cycle:** 42
**References:** Daisuke Kobayashi C16 critique — lineup staging P3 flag; Critique 15 P2 "Luma visually outperformed by Byte"

---

## Problem

The current lineup (v007) places all five characters on a flat common baseline. The read is: **an inventory of characters.** Every character's feet are at the same y coordinate. No one is closer or farther from the camera. No one leads the composition.

Daisuke's note: "the composition reads as an inventory, not a cast." A pitch-grade lineup communicates cast dynamics. The staging should tell us: who leads, who follows, who is adjacent, who is separate.

Additional context from C15 critique: Luma is currently losing visual power to Byte on screen. Zoe Park (audience): "Byte is the best thing in this pitch." The lineup is one of three places (with the expression sheet and the style frames) where Luma must claim protagonist presence.

---

## Proposed Staging: Half-Step Stagger + Forward Position

### Core Change: Two-Tier Ground Plane

Instead of a single flat baseline, introduce two ground levels:

**Foreground tier (y_ground_FG = canvas_h × 0.78):** Luma and Byte
**Background tier (y_ground_BG = canvas_h × 0.70):** Cosmo, Miri, Glitch

The foreground tier is visually lower (higher y value = closer to bottom of frame = closer to camera). Characters on FG tier read as slightly in front of BG tier characters. This creates depth without a full perspective environment.

Scale implication: FG characters can be 3–5% larger than BG characters to reinforce the depth read. At current lineup canvas (typically 1200–1400px wide), this difference is ~8–12px in height — enough to read clearly without distorting relative proportions.

### Character Positions (left to right)

| Position | Character | Tier | Notes |
|---|---|---|---|
| 1 (leftmost) | Cosmo | BG | Arms crossed (SKEPTICAL default posture) |
| 2 | Miri | BG | Warm open stance, facing slightly inward |
| 3 (center) | Luma | FG | 3–5% larger than BG chars — PROTAGONIST POSITION |
| 4 | Byte | FG | Next to Luma, slightly lower (his height is shorter) |
| 5 (rightmost) | Glitch | BG | Floating/hovering slightly above BG baseline |

### Luma's Positioning

Luma is the **single forward-center character.** Both feet on the FG baseline. She is the largest character in the lineup (by virtue of FG scale, not by changing her proportion constants). Her silhouette should break the center-horizontal slightly toward the left-center — not dead center (which reads as poster-formal) but decisively occupying the protagonist zone.

Body posture: Use THE NOTICING body posture from v013 (if available at time of v008 generation) — observational stillness + slight forward lean. This is her DEFINING expression in the pitch. If v013 is not yet available, use a neutral READY stance (weight evenly distributed, arms at sides, head slightly forward). Do NOT use RECKLESS (too energetic for a lineup) or WORRIED (wrong tone).

### Byte's Positioning

Byte stands NEXT TO Luma on the FG tier. His center is at Luma's right shoulder level (given his height). The juxtaposition of his tiny body next to Luma's 3.2-head figure IS the comedy and the dynamic. His FG position (same tier as Luma) communicates: these two are the core unit.

Expression: RELUCTANT JOY or COMMITTED WARMTH — the version of Byte that is not performing (no gold confetti, no star eye in a lineup). His cracked eye should be visible (the character's signature). Arms at mid-position.

### Cosmo and Miri (BG tier, flanking)

Cosmo on the left. His glasses tilt (7°) and arms-crossed default posture will naturally create a visual "wall" on the left margin — this is correct. He bookends the left side.

Miri on the right side of center (BG, between Luma/Byte and Glitch). Her open welcoming posture softens the composition. She should face slightly inward (toward Luma) — the grandmotherly character orienting toward the protagonist reads as story-relevant staging.

### Glitch (BG tier, rightmost, floating)

Glitch's baseline is the BG tier, but its floating hover means its body center is 20–30px ABOVE the BG baseline. It should read as hovering, not standing. This already differentiates it from the standing characters. The rightmost position is correct for the character who is narrative-antagonist-adjacent.

---

## Implementation Notes for Maya

### Ground Line Change
Replace the single flat baseline with two horizontal rules:
```python
FG_GROUND_Y = int(CANVAS_H * 0.78)  # Luma + Byte
BG_GROUND_Y = int(CANVAS_H * 0.70)  # Cosmo + Miri + Glitch
```
Draw a subtle shadow line at each ground level (e.g., alpha 40, 2px, warm gray for FG, cool gray for BG) so the depth reads without requiring a full environment.

### Scale Factor
```python
FG_SCALE = 1.03   # 3% larger for FG characters
BG_SCALE = 1.00   # baseline
```
Apply the scale factor to character height calculations only. Do NOT change head_r or proportion constants — the scale must be uniform and post-calculation. Multiply final character height by FG_SCALE / BG_SCALE.

### Background
Do NOT add a full environment. The lineup is a character reference sheet, not an illustration. Keep the background at the current soft-gradient approach. Adding a ground plane shadow is sufficient to communicate depth.

### Vertical Alignment
With two tiers, character feet are at different y values. The "lineup" read (characters side by side for height comparison) still works because:
- The height guide rules can run at the FG ground level (establishing Luma's 3.2 head unit as the reference)
- BG characters' feet being higher (smaller y) reads naturally as "slightly behind"
- Include a perspective note in the annotation bar: "FG tier / BG tier — scale +3% for FG characters"

---

## What This Communicates in 2 Seconds

1. **Luma is the protagonist.** She is in front. She is the largest. She is centered.
2. **Byte is her co-lead.** He is on her right on the same FG tier. They are the unit.
3. **The supporting cast support.** Cosmo, Miri, Glitch are behind — present, characterized, but behind.
4. **It's a cast, not an inventory.** The stagger is subtle enough to read as production polish, not cinematic over-design.

---

## When to Deliver

After Luma v013 body posture work is complete, generate lineup v008 with the FG/BG staging. Run `LTG_TOOL_expression_silhouette.py` on the lineup to verify Luma and Byte's silhouettes are distinguishable from each other at lineup scale. Send to Alex Chen and Lee Tanaka inboxes on completion.

---

Lee Tanaka
