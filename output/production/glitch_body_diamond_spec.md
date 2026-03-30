<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Glitch — Diamond Body Primitive Construction Spec
**Author:** Maya Santos, Character Designer
**Date:** 2026-03-30
**Cycle:** C41
**Status:** PRODUCTION SPEC — reference for all artists and generators

*Addresses: Daisuke Kobayashi C14 P8 / C16 P4 (4-cycle open item). Distills §2 of `glitch.md` into a standalone production diagram spec.*

---

## 1. Diamond Proportions

```
         TOP VERTEX
             ★
            /|\
           / | \
          /  |  \
 LEFT ◆──────●──────◆ RIGHT
    VERTEX   CX,CY  VERTEX
          \  |  /
           \ | /
            \|/
             ★
         BOT VERTEX
```

**Canonical constants (1× render, expression sheet):**

| Constant | Value | Notes |
|---|---|---|
| `GLITCH_BODY_RX` | **34 px** | Horizontal half-extent (left→CX and CX→right) |
| `GLITCH_BODY_RY` | **38 px** | Vertical half-extent (top→CY and CY→bot) |
| **Proportional rule** | `ry > rx` | Body is TALLER than wide — never swap these |
| **Width:Height** | ~0.90 : 1.0 | `(rx*2) / (ry*2 + ry*0.15)` ≈ 0.87 effective |

> At 2× render (the production standard): `rx=68, ry=76`. Downsample to 1× with LANCZOS after compositing.

---

## 2. Vertex Formula (from body center CX, CY)

```
                  tilt_angle = math.radians(tilt_deg)

TOP    = (cx + int(rx * 0.15 * sin(tilt)),   cy - ry_eff + int(rx * 0.15 * cos(tilt)))
RIGHT  = (cx + int(rx * cos(-tilt)),          cy + int(rx * 0.20 * sin(-tilt)))
BOT    = (cx - int(rx * 0.15 * sin(tilt)),   cy + int(ry_eff * 1.15))
LEFT   = (cx - int(rx * cos(-tilt)),          cy - int(rx * 0.20 * sin(-tilt)))
```

Key points:
- **Top vertex** leans with body tilt (forward lean at non-zero tilt).
- **Bottom vertex** sits 15% BELOW `cy + ry_eff` — the diamond hangs low at the base. This gives Glitch visual weight despite hovering.
- **Left/Right vertices** rotate fully with `cos(-tilt)` — the equator rotates.
- At `tilt_deg=0`: right vertex sits ~`rx*0.20` BELOW center, left ~`rx*0.20` ABOVE center — giving a subtle counter-clockwise rest lean. This is intentional: Glitch is always slightly *wrong*, even at neutral.

**`ry_eff` is the modulated vertical radius:**
```python
ry_eff = int(ry * squash * stretch)
```
Where `squash < 1.0` compresses (PANICKED) and `stretch > 1.0` extends (TRIUMPHANT).

---

## 3. Rotation Range by State

| Expression | `tilt_deg` | Body Read |
|---|---|---|
| NEUTRAL | 0° | Upright — stable, operational |
| MISCHIEVOUS | +20° | Leans right — conspiratorial |
| PANICKED | −14° | Recoils left — flinch |
| TRIUMPHANT | 0° | Upright at full height — dominance |
| STUNNED | −18° | Hard recoil (larger than PANICKED) |
| CALCULATING | 0° | Perfectly still — control read |
| YEARNING | 0° | Still but heavy |
| COVETOUS | +12° | Leans toward subject — appetitive |
| HOLLOW | 0° | Unmoving — absence of will |

**Squash/stretch range:**

| Expression | squash | stretch | Read |
|---|---|---|---|
| PANICKED | 0.55 | 1.00 | Nearly flat — compression/flinch |
| TRIUMPHANT | 1.00 | 1.35 | Extended tall — maximum presence |
| NEUTRAL | 1.00 | 1.00 | Baseline |
| All others | 1.00 | 1.00 | Baseline |

---

## 4. Facet Fill Layers (draw order)

Draw layers in this order:

```
1. UV_PURPLE shadow   — polygon at offset (+3px right, +4px down) from body pts
2. CORRUPT_AMBER fill — main body polygon [TOP, RIGHT, BOT, LEFT]
3. AMBER_HL facet     — top-left triangle for directional lighting
4. VOID_BLACK outline — polygon outline, width=3
5. HOT_MAG crack      — diagonal scar + fork branch (see §5)
```

**Highlight facet (top-left catches light):**
```python
ctr    = (cx, cy - ry // 4)                           # just above center
mid_tl = ((TOP[0]+LEFT[0])//2, (TOP[1]+LEFT[1])//2)   # midpoint of top-left edge
facet  = [TOP, ctr, mid_tl]
draw.polygon(facet, fill=CORRUPT_AMBER_HL)
```

**Color values:**

| Name | RGB | Hex |
|---|---|---|
| CORRUPT_AMBER (body fill) | (255, 140, 0) | `#FF8C00` |
| CORRUPT_AMBER_HL (highlight) | (255, 185, 80) | `#FFB950` |
| CORRUPT_AMBER_SH (shadow body) | (168, 76, 0) | `#A84C00` |
| UV_PURPLE (shadow offset) | (123, 47, 190) | `#7B2FBE` |
| HOT_MAGENTA (crack) | (255, 45, 107) | `#FF2D6B` |
| VOID_BLACK (outline) | (10, 10, 20) | `#0A0A14` |

---

## 5. HOT_MAG Crack Construction

The crack is a DIAGONAL SCAR from upper-left to lower-right of the body face, plus a fork branch:

```python
cs = (cx - rx//2,  cy - ry//3)      # crack start — upper-left quadrant
ce = (cx + rx//3,  cy + ry//2)      # crack end   — lower-right quadrant
draw.line([cs, ce], fill=HOT_MAG, width=2)

# Fork: secondary branch from crack midpoint toward upper-right
mid_c = ((cs[0]+ce[0])//2, (cs[1]+ce[1])//2)
fork  = (cx + rx//2, cy - ry//4)
draw.line([mid_c, fork], fill=HOT_MAG, width=1)
```

Rules:
- Crack is ALWAYS visible (all expressions except hypothetical future HEALED/RESET states).
- Crack is drawn AFTER body fill and AFTER outline — it is on top of everything except the pixels eye layer.
- The crack is NOT a fill color and NOT a pixel state.

---

## 6. Assembly with Pixel Confetti Elements

Glitch hovers above the ground and scatters corrupted pixels below its bottom spike.

**Confetti anchor point:**
```python
cy_bot_spike = cy + ry_eff * squash * stretch * 1.15 + 6   # bottom spike tip
# Confetti scatters at and below cy_bot_spike — NOT below the body
```

**Confetti color rules by state:**

| State Category | Colors Used | Count | Spread |
|---|---|---|---|
| Performance (NEUTRAL) | HOT_MAG, UV_PURPLE, VOID_BLACK | 8 | 24px |
| Performance (MISCHIEVOUS) | ACID_GREEN, HOT_MAG | 14 | 28px |
| Performance (PANICKED) | HOT_MAG, HOT_MAG, ELEC_CYAN | 22 | 38px |
| Performance (TRIUMPHANT) | CORRUPT_AMB, SOFT_GOLD, HOT_MAG | 18 | 32px |
| Performance (STUNNED) | ELEC_CYAN, HOT_MAG | 20 | 42px |
| Performance (CALCULATING) | UV_PURPLE, VOID_BLACK, CORRUPT_AMB_SH | 5 | 14px |
| Interior (YEARNING) | *none* | 0 | — |
| Interior (COVETOUS) | UV_PURPLE, UV_PURPLE, CORRUPT_AMB_SH | 4 | 18px |
| Interior (HOLLOW) | *none* | 0 | — |

**Rules:**
- PANICKED and STUNNED may include ELEC_CYAN — these are involuntary states, corruption leaks out of control.
- NEVER use ELEC_CYAN or ACID_GREEN in confetti for performance/design states.
- Interior states (YEARNING, HOLLOW) have NO confetti. Silence = genuine felt state.

**Draw order: confetti goes FIRST (bottom layer), before bottom spike, before body.**

---

## 7. Full Assembly Order (Complete Character)

```
1. Hover confetti    — scattered pixels at cy_bot_spike level
2. Bottom spike      — 3-point downward spike from BOT vertex
3. UV_PURPLE shadow  — body polygon at (+3, +4) offset
4. CORRUPT_AMBER body — main diamond polygon
5. AMBER_HL facet    — top-left highlight triangle
6. VOID_BLACK outline — polygon border, width=3
7. HOT_MAG crack     — diagonal scar + fork
8. Left arm-spike    — from LEFT vertex, tip pointing outward
9. Right arm-spike   — from RIGHT vertex, tip pointing outward
10. Face (FRONT/3/4 only) — pixel eye system (see glitch.md §6)
11. Top spike        — 5-point crown from TOP vertex
```

---

## 8. Scale Reference Diagram

```
         [TOP spike crown — 5 pts]
                  ↑ spike_h px
                  ★
                 /|\
    LEFT ◆──────────────◆ RIGHT
       (rx=34)   center  (rx=34)
                 ↓
    ← rx*2 = 68px wide →
                  ★
                  ↓ spike_h px (bottom spike, 3 pts)

    ry=38 → total body height: 38+38*1.15 = ~82px (neutral)
    With 2× render: rx=68, ry=76 → width 136px, height ~164px
```

---

## 9. COVETOUS / HOLLOW State Geometry Notes

**COVETOUS** (+12° tilt):
- Forward lean toward subject
- `arm_l_dy = -8, arm_r_dy = -6` (both arm-spikes raised — reaching)
- Both eyes BILATERAL (acid slit, top row lit) — genuine interior state
- Confetti: minimal UV_PURPLE only (4 particles, 18px spread)

**HOLLOW** (0° tilt, squash=1.0, stretch=1.0):
- Unmoving — no squash/stretch, no tilt
- `arm_l_dy = 14, arm_r_dy = 20` (dangling uneven — asymmetric collapse)
- `spike_h = 4` (minimum — collapsed presence)
- Both eyes BILATERAL (single white center) — empty stare
- NO confetti

**NEUTRAL** (reference baseline):
- `tilt_deg=0, squash=1.0, stretch=1.0`
- `spike_h=10`
- `arm_l_dy=0, arm_r_dy=0`
- Asymmetric eyes (right eye destabilized from left)

---

## 10. Generator Index

| File | Version | Location |
|---|---|---|
| `LTG_TOOL_glitch_expression_sheet.py` | v003 (C28) — 9 expressions, 3×3 | `output/tools/` |
| `LTG_TOOL_glitch_turnaround.py` | v002 (C24) — 4-view turnaround | `output/tools/` |
| Full character spec | — | `output/characters/main/glitch.md` |

---

*Maya Santos, Character Designer — C41*
