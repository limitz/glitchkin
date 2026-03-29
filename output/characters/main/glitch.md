# Glitch — Character Construction Specification

**Character:** Glitch (Glitchkin antagonist)
**Series:** Luma & the Glitchkin
**Author:** Maya Santos
**Cycle:** 32 (C14 spec — Daisuke, 2 consecutive critiques)
**Status:** Construction reference for artists and generators

---

## 1. Design Identity

Glitch is a fully digital entity — no organic curves, no warm tones, no
biological anatomy. Its body is pure geometry corrupted by its own ambition.
Everything about Glitch reads as *constructed, not grown*.

Glitch's visual language contrasts Luma's at every level:
- Luma: curves, warmth, organic hair mass, off-center asymmetric life
- Glitch: hard facets, amber-on-black palette, pixel eyes, geometric spikes

---

## 2. Diamond Body Geometry

### 2.1 Base Shape — Rhombus from Primitives

The body is constructed from **four points forming a rhombus (diamond)**:

```
       TOP
        |
LEFT---CX,CY---RIGHT
        |
       BOT
```

In code (see `LTG_TOOL_glitch_expression_sheet_v003.py`, `diamond_pts()`):

```python
top   = (cx + int(rx * 0.15 * sin(tilt)), cy - ry_eff + int(rx * 0.15 * cos(tilt)))
right = (cx + int(rx * cos(-tilt)),       cy + int(rx * 0.2 * sin(-tilt)))
bot   = (cx - int(rx * 0.15 * sin(tilt)), cy + int(ry_eff * 1.15))
left  = (cx - int(rx * cos(-tilt)),       cy - int(rx * 0.2 * sin(-tilt)))
```

**Key values (reference: expression sheet panels, 1× render):**
- `rx` = 34px (horizontal half-extent)
- `ry` = 38px (vertical half-extent before squash/stretch)
- `cx, cy` = body center point
- The diamond is taller than it is wide: `ry > rx` (G002 fix — C35)
- Bottom vertex sits slightly lower than the geometric midpoint: `cy + ry * 1.15`
- Top vertex has a slight forward lean at non-zero tilt: the `0.15 * sin(tilt)` offset

**Turnaround reference (`LTG_TOOL_glitch_turnaround_v002.py`, `diamond_pts_2d()`):**
```python
top   = (cx + int(rx * 0.1 * sin(tilt)), cy - ry)
right = (cx + rx,                         cy + int(rx * 0.1))
bot   = (cx - int(rx * 0.1 * sin(tilt)), cy + int(ry * 1.1))
left  = (cx - rx,                         cy - int(rx * 0.1))
```
The horizontal axis is slightly offset vertically (right sits ~rx*0.1 below center,
left sits ~rx*0.1 above center). This gives the diamond a subtle counter-clockwise
rotation at rest — it does NOT sit perfectly upright. This is intentional: Glitch
is always slightly *wrong*, even at neutral.

### 2.2 Fill and Shading

| Layer | Color | Notes |
|---|---|---|
| Shadow offset | UV_PURPLE `(123,47,190)` | +3px right, +4px down |
| Main body fill | CORRUPT_AMBER `(255,140,0)` | Full amber — bright digital material |
| Highlight facet | CORRUPT_AMBER_HL `(255,185,80)` | Top-left triangle: [top, ctr, mid_tl] |
| Outline | VOID_BLACK `(10,10,20)` | width=3 |
| HOT_MAG crack | HOT_MAG `(255,45,107)` | Diagonal line across body (see §2.3) |

**Highlight facet formula:**
```python
ctr    = (cx, cy - ry // 4)           # just above center
mid_tl = ((top[0]+left[0])//2, (top[1]+left[1])//2)   # midpoint of top-left edge
highlight_triangle = [top, ctr, mid_tl]
```
This makes the upper-left facet catch light — Glitch has an ambient directional light
source from upper-left even though it is a digital entity. This distinguishes the
render from flat clip art.

### 2.3 The HOT_MAG Crack

The crack is Glitch's defining external corruption mark. It is a diagonal scar
across the diamond face from upper-left to lower-right:

```python
cs = (cx - rx//2, cy - ry//3)      # crack start: upper-left quadrant
ce = (cx + rx//3, cy + ry//2)      # crack end:   lower-right quadrant
draw.line([cs, ce], fill=HOT_MAG, width=2)

# Fork: a secondary branch splits off the crack midpoint toward upper-right
mid_c = ((cs[0]+ce[0])//2, (cs[1]+ce[1])//2)
fork  = (cx + rx//2, cy - ry//4)
draw.line([mid_c, fork], fill=HOT_MAG, width=1)
```

The crack is ALWAYS visible in all expressions (except when `crack_visible=False`
is explicitly passed — reserved for hypothetical future states like HEALED or RESET).

**The crack is NOT a pixel state and NOT a fill color.** It is drawn as a line AFTER
the body fill. Stacking order: shadow → body fill → highlight facet → outline → crack.

---

## 3. Spikes

### 3.1 Top Spike

The top spike is a **5-point crown** (not a simple triangle), rising above the
diamond apex. It is Glitch's "antenna" — its emotional intensity reads in spike height.

```
        tip (tallest point)
       / | \
  left   |   right
   |  flat base  |
   TOP of diamond (flat connection)
```

```python
sx  = cx + tilt_off   # spike leans with body tilt
pts = [
    (sx - spike_h//2, cy_top),
    (sx - spike_h,    cy_top - spike_h),
    (sx,              cy_top - spike_h*2),    # tip
    (sx + spike_h,    cy_top - spike_h),
    (sx + spike_h//2, cy_top),
]
```

**Spike height by emotional state:**

| Expression | spike_h | Read |
|---|---|---|
| NEUTRAL | 10 | Present, operational |
| MISCHIEVOUS | 14 | Elevated, active planning |
| CALCULATING | 12 | Focused, deliberate |
| PANICKED | 6 | Compressed under stress |
| TRIUMPHANT | 22 | Maximum extension — power display |
| STUNNED | 8 | Knocked back |
| YEARNING | 6 | Subdued, introverted |
| COVETOUS | 12 | Forward-focused |
| HOLLOW | 4 | Minimal, collapsed |

The spike tip has a short HOT_MAG line extending from the apex (width=2) — the
"spark" at the crown. This runs in all states where spike_h ≥ 6.

### 3.2 Bottom Spike

A smaller **3-point downward spike** representing Glitch's hover point:

```python
pts = [
    (cx - spike_h//2, cy_bot),
    (cx + spike_h//2, cy_bot),
    (cx,              cy_bot + spike_h + 4),
]
```

Fill: CORRUPT_AMBER_SH (dark amber shadow tone). Bottom spike is NOT animated —
it is always present at `spike_h=10` and `cy_bot = cy + ry * squash * stretch * 1.15 + 6`.
This spike represents Glitch's connection to the digital substrate. When Glitch
hovers, the confetti scatters *below this spike*, not below the body.

---

## 4. Arm-Spikes

Glitch has **two arm-spikes** — small triangular protrusions from the diamond's
left and right vertices. These are NOT organic arms; they are extensions of the
body geometry.

### 4.1 Construction

```python
# Left arm-spike
ax  = cx - rx - 6
ay  = cy + arm_dy    # arm_dy = vertical offset from body center
tip = (ax - 14 + arm_dx, ay - 8)
pts = [(ax, ay-5), (ax, ay+5), tip]

# Right arm-spike
ax  = cx + rx + 6
ay  = cy + arm_dy
tip = (ax + 14 + arm_dx, ay - 8)
```

Fill: CORRUPT_AMBER. Outline: VOID_BLACK width=2.

### 4.2 Arm Position by Expression

| Expression | arm_l_dy | arm_r_dy | Read |
|---|---|---|---|
| NEUTRAL | 0 | 0 | Level — ready state |
| MISCHIEVOUS | -6 | 14 | Asymmetric — scheming (one up, one lower) |
| PANICKED | 18 | 6 | Both dropped/defensive |
| TRIUMPHANT | -20 | -22 | Both raised — victory display |
| STUNNED | -10 | -8 | Flung upward from shock |
| CALCULATING | -22 | 2 | Left arm raised (chin-touch equivalent) |
| YEARNING | 18 | 16 | Both hanging low — defeated weight |
| COVETOUS | -8 | -6 | Both slightly raised — reaching forward |
| HOLLOW | 14 | 20 | Dangling uneven — asymmetric collapse |

---

## 5. Rotation Rules per Pose

Glitch's body tilt is expressed as `tilt_deg` in degrees, applied via:
```python
angle = math.radians(tilt_deg)
```

The tilt offsets the TOP and BOTTOM vertices slightly (proportional to `rx * 0.15 * sin`)
while the LEFT and RIGHT vertices rotate fully with `cos(-angle)`.

**Tilt affects BOTH spike position AND arm position:** the top spike leans with the
body via `tilt_off = int(tilt * 0.4)`.

| Expression | tilt_deg | Read |
|---|---|---|
| NEUTRAL | 0 | Stable, upright |
| MISCHIEVOUS | +20 | Leans right — conspiratorial |
| PANICKED | -14 | Recoils left — physical flinch |
| TRIUMPHANT | 0 | Upright at full height — dominance |
| STUNNED | -18 | Hard recoil (larger than PANICKED) |
| CALCULATING | 0 | Perfectly still — control read |
| YEARNING | 0 | Still — but heavy, not controlled |
| COVETOUS | +12 | Leans toward subject — appetitive lean |
| HOLLOW | 0 | Unmoving — absence of will |

**Squash and stretch:**
- `squash` (< 1.0): compresses ry_eff — body flattens vertically
- `stretch` (> 1.0): extends ry_eff — body elongates vertically

These two are applied together as `ry_eff = int(ry * squash * stretch)`.

At `squash=0.55` (PANICKED), the diamond is nearly flat — reading as physical
compression/flinch from impact. At `stretch=1.35` (TRIUMPHANT), the diamond
extends up and down, reading as maximum presence.

---

## 6. The Pixel Eye System

Glitch has **two 3×3 pixel grid eyes** (not organic eyes). Each pixel is one
"cell" and each cell can be one of 8 states. The eye system is what makes Glitch
readable as having a face.

### 6.1 Cell Colors

| State | Name | Color | Hex |
|---|---|---|---|
| 0 | VOID | VOID_BLACK | `(10,10,20)` |
| 1 | DIM | CORRUPT_AMBER_SH | `(168,76,0)` |
| 2 | ACTIVE | CORRUPT_AMBER | `(255,140,0)` |
| 3 | BRIGHT | SOFT_GOLD | `(232,201,90)` |
| 4 | HOT | HOT_MAGENTA | `(255,45,107)` |
| 5 | ACID | ACID_GREEN | `(57,255,20)` |
| 6 | UV | UV_PURPLE | `(123,47,190)` |
| 7 | STATIC | STATIC_WHITE | `(248,246,236)` |

### 6.2 Eye Glyph Grid (Left Eye = Primary Expression)

```
Left eye grid (row 0 = top, col 0 = left):
  [row0: a, b, c]
  [row1: d, e, f]
  [row2: g, h, i]
```

Each expression has a canonical left-eye glyph:

| Expression | Glyph (row-major) | Description |
|---|---|---|
| neutral | `[[0,2,0],[2,1,2],[0,2,0]]` | Cross pattern — amber active center |
| mischievous | `[[5,0,5],[0,5,0],[5,0,5]]` | Acid X — diagonals lit |
| panicked | `[[4,4,4],[4,0,4],[4,4,4]]` | Hot ring — center void |
| triumphant | `[[3,3,3],[3,3,3],[3,3,3]]` | Solid gold — full brightness |
| stunned | `[[4,4,4],[4,4,4],[4,4,4]]` | Full hot mag — overloaded |
| calculating | `[[5,0,5],[0,5,0],[5,0,5]]` | Same as mischievous (acid X = plotting) |
| yearning | `[[0,6,0],[6,1,6],[0,6,0]]` | UV cross — soft interior wanting |
| covetous | `[[5,5,5],[0,5,0],[0,0,0]]` | Acid slit (top row lit) — target lock |
| hollow | `[[0,0,0],[0,7,0],[0,0,0]]` | Single white center — empty stare |

### 6.3 The Destabilized-Right-Eye Signature

**The right eye is ALWAYS different from the left eye.** This asymmetry is Glitch's
defining visual signature. It communicates that Glitch is a corrupted entity — it
cannot fully synchronize its own face.

**Rule: the right eye is a "bleed" of the left — some bright pixels go void or dim,
some void pixels appear where they should not.**

Right eye construction from left:
- BRIGHT pixels (state 3) → become DIM (state 1) or VOID (state 0)
- HOT pixels (state 4) → some become VOID
- ACID pixels (state 5) → some become VOID, some stay
- The pattern has an "incomplete" quality — it looks like data corruption, not mirror

**EXCEPTION — Interior State Eyes (Bilateral):**
When Glitch is in a **genuine interior state** (an actual felt experience, not a
performance), **both eyes are IDENTICAL.** Bilateral symmetry = the emotion is real,
not constructed.

Interior states with bilateral eyes:
- `YEARNING`: both eyes = `[[0,6,0],[6,1,6],[0,6,0]]` — UV soft glow, same both sides
- `COVETOUS`: both eyes = `[[5,5,5],[0,5,0],[0,0,0]]` — target lock, same both sides
- `HOLLOW`: both eyes = `[[0,0,0],[0,7,0],[0,0,0]]` — empty stare, same both sides

The bilateral/asymmetric rule in practice:
- Asymmetric eyes → Glitch is performing (NEUTRAL, MISCHIEVOUS, STUNNED, etc.)
- Bilateral eyes → Glitch is actually feeling something (YEARNING, COVETOUS, HOLLOW)

This rule is what makes Glitch a character and not just a design.

### 6.4 Eye Placement

```python
face_cy = cy - ry // 6             # face center sits above body center
cell    = 5                         # cell size in pixels
leye_x  = cx - rx//2 - cell*3//2   # left eye: left of body center
leye_y  = face_cy - cell*3//2      # top of 3×3 grid
reye_x  = cx + rx//2 - cell*3//2   # right eye: right of body center
reye_y  = face_cy - cell*3//2      # same y as left eye
```

Total eye grid size: 3 cells × cell_size = `3 * 5 = 15px` per eye at 1× render.
At 2× render, cell=5 → each eye is 15×15px before LANCZOS down.

---

## 7. Panel Grouping Logic: Performance vs. Interior State

### 7.1 Performance Expressions (Public Face)

These are states Glitch SHOWS others — its external behavior read:

| Expression | Category | Notes |
|---|---|---|
| NEUTRAL | Performance | Default mode — operational |
| MISCHIEVOUS | Performance | Scheming display |
| PANICKED | Performance | Uncontrolled reaction |
| TRIUMPHANT | Performance | Victory pose |
| STUNNED | Performance | Involuntary shock |
| CALCULATING | Performance | Power-display of intelligence |

**Panel grouping note:** Performance expressions should be presented together.
They are most useful in action panels, reaction panels, and confrontation scenes.

### 7.2 Interior State Expressions

These are states Glitch does NOT fully choose to show — they emerge from genuine
experience. They are quieter, more private. The reader is being let INTO Glitch.

| Expression | Interior Desire | Key Visual |
|---|---|---|
| YEARNING | Watching Luma have something Glitch cannot name — and wanting it | Still, UV eyes, no confetti, arms hanging |
| COVETOUS | "I could take that. I should take that." | Lean toward subject, acid slit both eyes, arms reaching |
| HOLLOW | After the wanting, nothing came back | Deflated body, empty stare both eyes, no confetti |

**Panel grouping note:** Interior state expressions should be used for **character
revelation moments** — not fight scenes, not confrontations. They are for: the moment
Glitch watches Luma from a distance, the moment it considers taking something, the
aftermath of a failed attempt. Use them sparingly. One interior expression per act
maximum.

### 7.3 Grouping Summary for Storyboard / Animatic Use

```
CONFRONTATION PANELS:     NEUTRAL / MISCHIEVOUS / PANICKED / TRIUMPHANT
REACTION PANELS:          STUNNED / CALCULATING
CHARACTER-REVEAL PANELS:  YEARNING / COVETOUS / HOLLOW
```

---

## 8. Hover Confetti

Glitch hovers above the ground and leaves a scatter of corrupted pixels below
its bottom spike.

**Confetti color rule:**
- Performance states: HOT_MAG + UV_PURPLE scatter (no cyan, no acid green)
- Interior states: NO CONFETTI (YEARNING, HOLLOW) or minimal UV_PURPLE only (COVETOUS)
- NEVER use ELEC_CYAN or ACID_GREEN in confetti — those are reserved for healthy/friendly Glitchkin

| Expression | Colors | Count | Spread |
|---|---|---|---|
| NEUTRAL | HOT_MAG, UV_PURPLE, VOID_BLACK | 8 | 24px |
| MISCHIEVOUS | ACID_GREEN, HOT_MAG | 14 | 28px |
| PANICKED | HOT_MAG, HOT_MAG, ELEC_CYAN | 22 | 38px |
| TRIUMPHANT | CORRUPT_AMB, SOFT_GOLD, HOT_MAG | 18 | 32px |
| STUNNED | ELEC_CYAN, HOT_MAG | 20 | 42px |
| CALCULATING | UV_PURPLE, VOID_BLACK, CORRUPT_AMB_SH | 5 | 14px |
| YEARNING | (none) | 0 | — |
| COVETOUS | UV_PURPLE, UV_PURPLE, CORRUPT_AMB_SH | 4 | 18px |
| HOLLOW | (none) | 0 | — |

Note: PANICKED and STUNNED confetti includes ELEC_CYAN because these are involuntary
states — the corruption is leaking out of control and mixing with external signals.
This is the ONLY case where cyan appears in Glitch's confetti.

---

## 9. View-by-View Turnaround Rules

Reference: `LTG_TOOL_glitch_turnaround_v002.py`

### FRONT view
- Full diamond, symmetric, UV_PURPLE shadow offset (+3,+4)
- Face visible: dual pixel eyes + neutral mouth dots
- Both arm-spikes visible, symmetric
- Top and bottom spikes centered

### 3/4 view
- Left side compressed: `rx_far = int(rx * 0.55)`, right side full `rx_near = rx`
- Face: left eye partially obscured (use single eye or foreshortened read)
- Crack: visible on near face
- Right arm-spike: visible; left arm-spike: foreshortened or hidden

### SIDE view
- Diamond is foreshortened to a near-sliver: `rx_side = int(rx * 0.4)`
- Internal structure suggested by: **vertical lit stripe** (center) +
  **void black divider lines** between lit stripe and shadow flanks
- This facet geometry is the key change in v002 (was flat amber kite in v001)
- Top spike: visible as thin line, leans slightly
- Both arm-spikes: NOT visible (pointing front/back, not sideways)

### BACK view
- Full diamond, symmetric
- No face
- Back-surface scar marks (HOT_MAG diagonal + UV_PURPLE secondary structural line)
- Main body fill: CORRUPT_AMB_SH (dark amber) — NOT CORRUPT_AMB — because
  the back is in shadow. UV_PURPLE fill was invisible against dark canvas (v001 bug).
- Right facet (facing upper-right) uses CORRUPT_AMB as highlight.

---

## 10. Reproducing Glitch From Scratch — Step-by-Step

To reproduce Glitch in any new generator:

1. **Set constants:** CORRUPT_AMB=(255,140,0), CORRUPT_AMB_SH=(168,76,0),
   CORRUPT_AMB_HL=(255,185,80), HOT_MAG=(255,45,107), UV_PURPLE=(123,47,190),
   VOID_BLACK=(10,10,20), SOFT_GOLD=(232,201,90), ACID_GREEN=(57,255,20),
   ELEC_CYAN=(0,240,255), STATIC_WHITE=(248,246,236).

2. **Compute body center** (cx, cy) for the view. Set rx=34, ry=38 (adjust for scale). `ry > rx` — body is taller than wide.

3. **Draw hover confetti** FIRST (bottom layer) at position `(cx, cy + ry*squash*stretch*1.15 + 6)`.

4. **Draw bottom spike** at `cy_bot = cy + ry*squash*stretch*1.15 + 6`.

5. **Draw body** using `diamond_pts()`:
   - Shadow: UV_PURPLE, offset +3,+4
   - Fill: CORRUPT_AMBER
   - Highlight facet (top-left triangle): CORRUPT_AMBER_HL
   - Outline: VOID_BLACK width=3
   - Crack: HOT_MAG diagonal + fork branch

6. **Draw arm-spikes** from left and right vertices of the diamond.

7. **Draw face** (FRONT and 3/4 only):
   - Compute `face_cy = cy - ry//6`
   - Left eye at `(cx - rx//2 - cell*3//2, face_cy - cell*3//2)` using expression glyph
   - Right eye at `(cx + rx//2 - cell*3//2, face_cy - cell*3//2)` using destabilized glyph
     (or bilateral if interior state)
   - Mouth (optional): 3 dim pixel dots at `face_cy + cell*3//2 + 6`

8. **Draw top spike** at `cy_top = cy - ry*squash*stretch`, with tilt_off = `tilt_deg * 0.4`.

9. **Apply 2x render → 1x LANCZOS downsample** for all final output.

10. **Never use warm organic colors** (no skin tones, no warm flesh). The only warm
    color is CORRUPT_AMBER (digital warm, not organic warm).

---

## 11. Generator Index

| Generator | Version | Purpose |
|---|---|---|
| `LTG_TOOL_glitch_expression_sheet_v001.py` | C23 | 4 expressions, 2×2 grid (legacy) |
| `LTG_TOOL_glitch_expression_sheet_v002.py` | C24 | 6 expressions, 3×2 grid |
| `LTG_TOOL_glitch_expression_sheet_v003.py` | C28 | 9 expressions (3×3), interior desire states added |
| `LTG_TOOL_glitch_turnaround_v001.py` | C23 | 4-view turnaround, v001 shadow issue |
| `LTG_TOOL_glitch_turnaround_v002.py` | C24 | Shadow fix — BACK/SIDE use CORRUPT_AMB_SH |

---

*Maya Santos — C32*
