<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->

# Gesture Line Library — C50
## Ryo Hasegawa — Motion & Animation Concept Artist
**Date:** 2026-03-30

---

## How to Read This Document

Each character expression entry defines:
- **Gesture line** — the single curve from head to weight-bearing foot
- **Anchor points** — head center, shoulder center, hip center, weight-bearing foot
- **Curve type** — S-curve, C-curve, reverse-C, or compound
- **Segment bends** — degrees of bend at neck, waist, and knee
- **Weight distribution** — which foot bears weight, percentage split
- **Thumbnail emotion test** — can the emotion be read from the stick figure alone?

All angles are from vertical. Positive = rightward/forward lean. Negative = leftward/backward lean.

All offsets are expressed as percentages of body height (BH) to be resolution-independent.

**Companion asset:** `output/characters/motion/LTG_CHAR_luma_gesture_prototype.png` — visual demonstration of gesture-first vs rectangle-first construction for Luma SURPRISED.

---

## Part 1: Weight and Balance Rules (All Characters)

These rules apply to EVERY human character pose in the project.

### Rule 1: Center of Gravity Over Support Base
The character's center of gravity (CoG) must project vertically into the area between the feet. The only exception is mid-action poses where the character is intentionally off-balance (SURPRISED recoil, FRUSTRATED stomp).

### Rule 2: Contrapposto Compensation
When the hip tilts toward the weight-bearing leg, the shoulder line tilts the OPPOSITE direction. The magnitude of shoulder tilt is 60-80% of hip tilt (not 100% — the body is not a seesaw).

### Rule 3: Head Balances the Stack
The head shifts toward the free leg side (opposite the weight-bearing leg) to keep the CoG centered. Head tilt direction is expression-dependent but head POSITION follows this rule.

### Rule 4: Emotional Weight Affects CoG Height
- Joy, excitement, surprise = HIGH CoG (heels lift, body extends, head up)
- Sadness, worry, defeat = LOW CoG (knees bend, shoulders drop, head down)
- Determination, anger = PLANTED CoG (wide stance, low center, both feet gripping)

### Rule 5: Asymmetry Is Life
No pose has both arms at the same angle, both legs at the same bend, or both feet at the same Y. Symmetry = mannequin. Asymmetry = character.

### Rule 6: The Gesture Line Is Drawn First
Before any body part shape, draw the gesture line. The body is constructed AROUND the gesture line, not the gesture line fitted to the body after the fact.

---

## Part 2: LUMA — 6 Expressions

### LUMA — CURIOUS

**Emotional logic:** Something caught her attention. She leans in. Her body asks the question before her face does.

**Gesture line:**
- Type: Forward C-curve
- Head: 8-10% BH forward of hip center, tilted 5 degrees toward subject
- Shoulder center: 4% BH forward of hip, dropped 3 degrees on the forward side
- Hip center: shifted 3% BH toward back leg (counterbalance)
- Weight foot: front foot, 60/40 split

**Anchor points (as offsets from ground-center):**
| Point | X offset (% BH) | Y offset (% BH) | Notes |
|---|---|---|---|
| Head center | +8 forward | 0 (standard height) | tilted 5 deg toward subject |
| Shoulder center | +4 forward | 0 | dropped 3 deg on forward side |
| Hip center | -3 rearward | 0 | shifted toward back foot |
| Weight foot | +5 forward | 0 (ground) | front foot, slightly pigeon-toed |
| Free foot | -5 rearward | +1 (heel lifted) | back foot, angled outward |

**Segment bends:**
- Neck: 8 degrees forward (leaning to look)
- Upper spine: 6 degrees forward (following head)
- Lower spine: 2 degrees back (hip counter)
- Weight knee: 8 degrees bend (ready to move closer)
- Free knee: 3 degrees bend (trailing)

**Arms:**
- Leading arm: slightly extended forward, hand palm-down (about to touch), angle -20 deg from body
- Trailing arm: close to body, hand near chin or held back, angle -60 deg from body
- ARM ASYMMETRY: leading arm is 40% further from body than trailing arm

**Silhouette test:** The forward lean creates a narrower top-to-bottom, deeper front-to-back profile. With face covered, the body reads as REACHING or INVESTIGATING. PASS expected.

---

### LUMA — DETERMINED

**Emotional logic:** She has decided. Her body commits before her mouth announces it.

**Gesture line:**
- Type: Slight backward S-curve (power pose)
- Head: 2% BH behind shoulder center, chin up 3-5 degrees
- Shoulder center: pulled back and DOWN from hip
- Hip center: centered, wide stance base
- Weight foot: both feet grounded, 55/45 split, WIDEST stance

**Anchor points:**
| Point | X offset (% BH) | Y offset (% BH) | Notes |
|---|---|---|---|
| Head center | -2 rearward | +1 (chin up) | slight lift, projecting confidence |
| Shoulder center | -1 rearward | -1 (pulled down) | back and down = power |
| Hip center | 0 centered | 0 | stable base |
| Weight foot (R) | +6 rightward | 0 | dominant side |
| Free foot (L) | -6 leftward | 0 | both planted, slight outward angle |

**Segment bends:**
- Neck: -3 degrees back (chin lift)
- Upper spine: -2 degrees back (chest forward)
- Lower spine: 0 (stable)
- Both knees: 5 degrees bend (ready, grounded)

**Arms:**
- Dominant arm (R): fist at hip level, elbow bent 90 degrees, pulled back slightly
- Non-dominant arm (L): crosses body slightly or hangs with forward angle
- ARM ASYMMETRY: one tight/high, one loose/low

**Silhouette test:** Widest stance, most grounded profile. Reads as PLANTED, READY. PASS expected.

---

### LUMA — SURPRISED

**Emotional logic:** Startle reflex. Body reacts before brain processes.

**Gesture line:**
- Type: Backward C-curve (recoil)
- Head: 6% BH behind hip center, snapped back
- Shoulder center: 4% BH behind hip, shoulders RAISED (protective hunch)
- Hip center: shifted forward of feet (off-balance backward)
- Weight foot: back foot, 70/30 split — she is FALLING BACKWARD

**Anchor points:**
| Point | X offset (% BH) | Y offset (% BH) | Notes |
|---|---|---|---|
| Head center | -6 rearward | +2 (recoil up) | snapped back and to one side |
| Shoulder center | -4 rearward | +2 (hunched up) | protective rise |
| Hip center | +2 forward | 0 | off-balance |
| Weight foot (back) | -4 rearward | 0 (planted) | catching weight |
| Free foot (front) | +3 forward | +2 (lifted) | lost contact |

**Segment bends:**
- Neck: -12 degrees back (snap recoil)
- Upper spine: -8 degrees back (body follows head)
- Lower spine: +4 degrees forward (hip compensates)
- Weight knee: 15 degrees bend (absorbing backward shift)
- Free knee: 8 degrees bend (lifting)

**Arms:**
- Shield arm: up near face, bent elbow, palm outward (defensive)
- Counterbalance arm: flung to side and slightly behind (catching balance)
- ARM ASYMMETRY: MAXIMUM — one high/forward, one low/backward, different heights by 30% BH

**Silhouette test:** Most asymmetric silhouette. Backward lean + one arm up + one arm out = completely unique outline. Reads as STARTLED without any facial detail. STRONG PASS expected.

---

### LUMA — WORRIED

**Emotional logic:** Pulling inward, protecting herself, but eyes still outward (she does not fully retreat).

**Gesture line:**
- Type: Compressed inward S-curve
- Head: dipped 4% BH forward and DOWN
- Shoulder center: rounded forward and UP (protective hunch)
- Hip center: tucked under, shifted to comfort side (LEFT)
- Weight foot: left foot, 60/40 comfort-side lean

**Anchor points:**
| Point | X offset (% BH) | Y offset (% BH) | Notes |
|---|---|---|---|
| Head center | +4 forward | -3 (dropped) | face down, eyes UP |
| Shoulder center | +3 forward | +2 (hunched) | protective rounding |
| Hip center | -2 leftward | -1 (tucked) | comfort side |
| Weight foot (L) | -3 leftward | 0 | comfort side planted |
| Free foot (R) | +1 rightward | +1 (on toes) | ready to flee |

**Segment bends:**
- Neck: 10 degrees forward (ducking)
- Upper spine: 8 degrees forward (curling inward)
- Lower spine: -4 degrees back (tuck)
- Weight knee: 5 degrees bend
- Free knee: 12 degrees bend (pigeon-toed turn inward)

**Arms:**
- Self-hold arm: gripping opposite elbow, crossed over body
- Wrapped arm: hand near gripping arm's wrist, body compressed
- ARM ASYMMETRY: both close to body but at different wrap angles

**Silhouette test:** NARROWEST silhouette. Compressed, wrapped, inward. The opposite of SURPRISED. Reads as SCARED or UNCERTAIN from body alone. PASS expected.

---

### LUMA — DELIGHTED

**Emotional logic:** Joy erupts upward. She cannot contain the energy.

**Gesture line:**
- Type: Upward-exploding S-curve
- Head: thrown back 5% BH, tilted to one side
- Shoulder center: risen UNEVENLY (one higher from asymmetric arms)
- Hip center: popped to one side (celebration asymmetry), 4-5 degrees tilt
- Weight foot: balls of both feet (near tiptoe), heels lifted

**Anchor points:**
| Point | X offset (% BH) | Y offset (% BH) | Notes |
|---|---|---|---|
| Head center | -2 rearward | +4 (thrown back) | laughing head-throw |
| Shoulder center | 0 | +3 (risen) | unevenly — one side higher |
| Hip center | +3 rightward | +1 (popped) | celebration hip-pop |
| Weight foot (L) | -2 leftward | +2 (on ball) | heel lifted |
| Free foot (R) | +3 rightward | +3 (lifted) | mid-bounce |

**Segment bends:**
- Neck: -8 degrees back (thrown)
- Upper spine: -4 degrees back (chest opens)
- Lower spine: +3 degrees forward (hip-pop arch)
- Both knees: 8 degrees bend (spring loaded)

**Arms:**
- High arm: fully extended overhead, fingers spread
- Pump arm: bent at elbow, fist-pump at shoulder height
- ARM ASYMMETRY: one fully up, one bent at different height — "celebration Y"

**Silhouette test:** TALLEST silhouette. Arm-up Y + tiptoe + head-back = maximum vertical extension. Reads as JOY or CELEBRATION from stick figure alone. STRONG PASS expected.

---

### LUMA — FRUSTRATED

**Emotional logic:** The plan failed. Energy bursts outward then partially contains.

**Gesture line:**
- Type: Aggressive diagonal (tilt 10-12 degrees to one side)
- Head: tilts OPPOSITE to torso lean (looking at the thing that went wrong)
- Shoulder center: twisted (one forward, one back — rotational energy)
- Hip center: dramatic tilt 6-8 degrees, 80/20 weight split
- Weight foot: bent (stomp), free foot barely touching

**Anchor points:**
| Point | X offset (% BH) | Y offset (% BH) | Notes |
|---|---|---|---|
| Head center | -5 opposite to lean | -2 (dropped) | looking at problem |
| Shoulder center | +2 same as lean | 0 | twisted rotation |
| Hip center | +6 lean-side | -2 (low stance) | dramatic shift |
| Weight foot | +4 lean-side | 0 | bent, stomped |
| Free foot | -3 opposite | +2 (barely touching) | unstable |

**Segment bends:**
- Neck: 8 degrees opposite to torso (counter-tilt)
- Upper spine: 10 degrees lean-side (tantrum lean)
- Lower spine: 4 degrees lean-side (following)
- Weight knee: 20 degrees bend (stomp/heavy)
- Free knee: 5 degrees bend (floating)

**Arms:**
- Flung arm: extended out to side and DOWN (threw something or gestured in exasperation)
- Frustration arm: bent sharply at elbow, hand near head or pulling at hair
- ARM ASYMMETRY: MAXIMUM — one low-wide, one high-tight, COMPLETELY different positions

**Silhouette test:** Most DIAGONAL silhouette. Side-lean + asymmetric arms + dramatic weight shift = completely unique. Reads as ANGRY or UPSET from body alone. PASS expected.

---

## Part 3: COSMO — 6 Expressions

Cosmo's gesture lines are ANGULAR where Luma's are curved. His rectangular build creates sharp bends at joints instead of smooth arcs. His counterpose is visible as distinct angle breaks at waist and shoulders.

### COSMO — AWKWARD

**Gesture line:**
- Type: Off-center compound (slight S with angular breaks)
- Head: tilted 6 degrees to one side, shifted 3% BH away from the shrug direction
- Shoulder center: RAISED unevenly (one-sided shrug), angular break at collar
- Hip center: shifted slightly opposite to shoulder raise
- Weight: 55/45, favoring the side AWAY from the shrug

**Segment bends:**
- Neck: 6 degrees sideways tilt (uncomfortable lean)
- Upper spine: 3 degrees opposite to head (angular compensation)
- Lower spine: 2 degrees toward weight leg
- Weight knee: 3 degrees (planted)
- Free knee: 8 degrees (shifted, uncertain)

**Arms:** One arm up in half-shrug, hand open palm-up ("I don't know"); other arm held close, gripping notebook or own side. Asymmetric by design — awkward IS asymmetric.

**Silhouette test:** The one-sided shrug with head-counter-tilt reads as UNCERTAIN or SHEEPISH. PASS.

---

### COSMO — WORRIED

**Gesture line:**
- Type: Compressed vertical with forward hunch
- Head: 5 degrees forward-down, glasses slide to nose tip
- Shoulder center: both raised (defensive), pulled forward
- Hip center: slightly back (retreating from concern)
- Weight: 60/40, shifted back

**Arms:** Both arms close to body, one hand gripping notebook tightly to chest (security object), other hand adjusting glasses nervously. The notebook is the tell — how he holds it reveals his state.

**Silhouette test:** Compressed, hunched, narrow. Notebook-to-chest is unique to Cosmo worried. PASS.

---

### COSMO — SURPRISED

**Gesture line:**
- Type: Backward angular snap (sharp break at waist)
- Head: snapped back 4% BH, glasses pushed up from eyebrow lift
- Shoulder center: risen sharply, angular (rectangular body = sharp vertical jump)
- Hip center: forward of feet (off-balance back)
- Weight: 65/35 on back foot

**Arms:** Both arms out wide but at DIFFERENT heights — one shields face, one flings outward. Notebook airborne or fumbled (secondary mass — drops at +1.5 beat lag).

**Silhouette test:** Angular backward snap with asymmetric arms. Glasses askew adds unique silhouette element. PASS.

---

### COSMO — SKEPTICAL

**Emotional logic:** His signature expression. The whole body says "I'm not buying it."

**Gesture line:**
- Type: Angular lean-back with hip pop (STRONGEST counterpose)
- Head: tilted 8 degrees, one brow raised (even in stick figure: one eye higher)
- Shoulder center: dropped on one side, twisted (one shoulder forward)
- Hip center: popped dramatically to one side, 5 degrees tilt
- Weight: 70/30 on one leg (the other barely touches)

**Segment bends:**
- Neck: 8 degrees sideways + 3 degrees back (looking down nose)
- Upper spine: 4 degrees opposite to hip (sharp angular counterpose)
- Lower spine: 6 degrees toward weight leg (hip pop)
- Weight knee: straight (locked — confident stance)
- Free knee: 15 degrees bend (barely load-bearing)

**Arms:** One arm crossed over body (possibly holding notebook at angle); other arm out, palm up or index finger touching chin ("really?"). This is the MOST asymmetric Cosmo pose.

**Silhouette test:** Hip-pop + crossed arm + head tilt = instantly reads as SKEPTICAL/DISMISSIVE. STRONG PASS.

---

### COSMO — DETERMINED

**Gesture line:**
- Type: Forward angular lean (sharp, not curved like Luma)
- Head: chin down, looking straight ahead through glasses (menacing nerd energy)
- Shoulder center: pulled FORWARD and DOWN (the opposite of his worried hunch — this is active forward)
- Hip center: centered, wide base
- Weight: 55/45 even, wide stance

**Arms:** Both hands down, fists (NOT open), notebook stowed. His fists are tighter and lower than Luma's — Luma's determination is expansive, Cosmo's is contained.

**Silhouette test:** Wide base + forward lean + fists low = reads as RESOLVED. Distinct from Luma DETERMINED by angular posture and contained energy. PASS.

---

### COSMO — FRUSTRATED/DEFEATED

**Gesture line:**
- Type: Heavy angular droop (head drops, shoulders fold forward)
- Head: dropped 8 degrees forward, chin to chest
- Shoulder center: rolled forward and DOWN (collapse of his normally upright posture)
- Hip center: level but shifted, no pop (energy drained)
- Weight: 50/50 but both knees slightly bent (wilting)

**Arms:** Arms hang loose, notebook dangling from one hand at full arm extension (he hasn't let go — he never lets go — but he is not holding it purposefully). Other hand may be pushing up glasses with two fingers (the self-comfort gesture, replacing the notebook grip).

**Silhouette test:** Drooped, collapsed, narrow. The notebook-at-arm's-length is unique to this pose. PASS.

---

## Part 4: GRANDMA MIRI — 6 Expressions

Miri's gesture lines carry her AGE and WARMTH. Her forward lean is permanent (3-5 degrees, never vertical). Her hip favors LEFT in all poses. Her head tilts are LARGER than other characters. Her hands are NEVER idle.

### MIRI — WARM/WELCOMING

**Gesture line:**
- Type: Gentle forward C-curve (permanent lean + extra warmth lean)
- Head: tilted 8 degrees toward the person she is welcoming
- Shoulder center: dropped on the welcoming side, slightly forward
- Hip center: favors LEFT (habitual), 3 degrees tilt
- Weight: 60/40 on habitual side (L), permanent 3-5 degree forward lean

**Arms:** One arm extended slightly in invitation (open hand, palm up), other arm at hip or holding kitchen item. Cardigan hangs LONGER on dropped-shoulder side (free visual storytelling).

**Silhouette test:** Forward lean + one-arm-out + asymmetric cardigan drape reads as INVITING or GREETING. PASS.

---

### MIRI — SKEPTICAL/AMUSED

**Gesture line:**
- Type: Subtle lean-back with head-forward counter (she leans away but her eyes come closer)
- Head: tilted 10 degrees to side, pushed FORWARD of shoulders (scrutinizing)
- Shoulder center: leaned 3 degrees back (pulling away while looking closer)
- Hip center: favors LEFT, settled
- Weight: 55/45 LEFT

**Arms:** One hand on hip (THE skeptical grandmother pose), other hand raised with index finger pointing or touching chin. The hip-hand is the universal "I see through you" signal.

**Silhouette test:** Hand-on-hip + head-forward reads as JUDGING or AMUSED. PASS.

---

### MIRI — CONCERNED

**Gesture line:**
- Type: Forward lean INCREASED (from habitual 3-5 deg to 8-10 deg — she leans INTO concern)
- Head: 12 degrees forward, looking slightly down (at child/problem level)
- Shoulder center: 6 degrees forward (reaching toward the concern)
- Hip center: LEFT habitual, but shifted slightly forward (whole body engaged)
- Weight: 65/35 on front foot (stepping toward concern)

**Arms:** Both hands reaching or one hand extended toward the person of concern. NOT crossed, NOT pulled back. Miri goes TOWARD problems, not away.

**Silhouette test:** Heavy forward lean + extended reach reads as REACHING OUT or WORRIED FOR SOMEONE. Distinct from her neutral forward lean by degree. PASS.

---

### MIRI — SURPRISED/DELIGHTED

**Gesture line:**
- Type: Upward S-curve (the ONLY pose where her forward lean reduces)
- Head: back 3 degrees (from her baseline), eyes wide
- Shoulder center: risen (delight), LESS forward than usual
- Hip center: LEFT habitual, slightly popped (rare hip-pop — she's young at heart)
- Weight: shifts to balls of feet briefly

**Arms:** BOTH arms up and out, bilateral open (her B3 WARMTH BURST pose from motion spec). This is the maximum expression — full-body delight. Fingers spread, palms outward.

**Silhouette test:** Wide-open arms + slightly-back lean (rare for Miri) reads as SURPRISE-JOY. PASS.

---

### MIRI — WISE/KNOWING

**Gesture line:**
- Type: Settled vertical (closest to straight, but STILL has habitual forward lean 3 deg)
- Head: level, VERY slight nod angle (3 degrees — she knows something you do not)
- Shoulder center: settled, even, relaxed (she is at peace with this knowledge)
- Hip center: LEFT habitual, fully settled weight
- Weight: 55/45 habitual, fully grounded

**Arms:** Hands together at waist level (interlaced or one hand over other), or one hand touching cardigan button (self-contained gesture). The containment IS the wisdom. She does not need to reach or gesture — she has already understood.

**Silhouette test:** The most contained Miri silhouette. Still has her habitual forward lean and left-hip. Reads as CALM, KNOWING, STILL. Distinct from WARM/WELCOMING by arm containment. PASS.

---

### MIRI — KNOWING STILLNESS (Deep Variant)

**Gesture line:**
- Type: Identical to WISE/KNOWING but with head tilted 5 degrees down-and-left
- The subtle downward tilt distinguishes "I know a general truth" from "I know something about YOU specifically"
- Same body, different head angle = different emotional target

**Arms:** One hand at chin level, touching glasses frame (the precision gesture — ONCE, not fidgeting). Other hand at side or holding cardigan closed.

**Silhouette test:** Near-identical to WISE/KNOWING in silhouette, differentiated by head angle. This is intentional — both are "knowing" states, and Miri's stillness IS her signature. The face carries the difference here. ACCEPTABLE (body carries 40%, face carries 60% — inverted from usual rule, but correct for this specific character moment).

---

## Part 5: Byte and Glitch — Gesture Equivalents

### BYTE

Byte has no ground contact and no skeletal gesture line. His "gesture" is expressed through:
1. **Body tilt** (replaces spine curve): lean toward = interest, lean away = avoidance
2. **Squash/stretch** (replaces CoG height): compressed = scared, extended = excited
3. **Glow direction** (replaces weight distribution): glow leads body, commits first
4. **Arm-tentacle extension** (replaces arm gesture): extended = reaching, retracted = guarded
5. **Hover height** (replaces foot contact): low = grounded/present, high = alert/scared

These are already documented in the Byte motion spec sheet. No changes needed for C50 gesture work — Byte's motion vocabulary was gesture-based from the start because he has no skeleton to assemble from rectangles.

### GLITCH

Glitch is exempt from gesture line work. His body IS the gesture:
- Tilt = lean (no spine)
- Spike height = energy level
- Squash/stretch = impact/emotion
- Bilateral vs asymmetric eyes = genuine vs performance

Already documented in Glitch motion spec sheet. No changes needed.

---

## Part 6: Implementation Notes

### For Maya Santos (Expression Sheet Rebuild)

The gesture lines above define signed offsets for every body anchor. The core code change is:

```
# Old: everything shares cx
torso_cx = cx; head_cx = cx; hip_cx = cx

# New: offset chain creates gesture line
hip_cx = cx + hip_shift          # hip shifts toward weight leg
torso_cx = hip_cx - shoulder_comp  # shoulder compensates opposite
head_cx = torso_cx + head_balance  # head balances the stack
```

Each expression in this library provides the signed values for these offsets. Convert the % BH values to pixels using: `offset_px = int(offset_pct * body_height / 100)`.

### For Rin Yamamoto (Expression Sheet Code)

Leg construction changes from symmetric columns to weighted:

```
# Old: symmetric
left_leg_x = cx - leg_offset
right_leg_x = cx + leg_offset

# New: weighted
weight_leg_x = hip_cx + weight_shift
free_leg_x = hip_cx - weight_shift * 0.6
weight_foot_y = ground_y
free_foot_y = ground_y - free_foot_lift
```

### For Ryo Hasegawa (Motion Spec Sheets)

Motion sheets must be rebuilt with gesture-line-first figures. The current `draw_luma_figure()` function builds from rectangles. The new approach:

1. Define the gesture line (spine curve) as a bezier or polyline
2. Place hip, shoulder, and head anchor points ON the gesture line
3. Build body volumes AROUND the anchors
4. Derive arm and leg positions FROM the anchors (not from `cx`)

This is demonstrated in `LTG_CHAR_luma_gesture_prototype.png`.

### draw_shoulder_arm Helper Evolution

The current `draw_shoulder_arm()` takes a fixed `shoulder_x, shoulder_y` as input. In the gesture-line system:

1. Shoulder position is OUTPUT of the gesture line (not input)
2. The shoulder shifts from the C47 rule still apply, but they operate on the gesture-derived shoulder position
3. New API should accept `gesture_line` as input and extract shoulder positions from it
4. `shoulder_polyline()` becomes a function of the gesture line, not of the body rectangle

Proposed new API:
```python
def draw_shoulder_arm_v2(draw, gesture_anchors, arm_angle_deg, side, style, ...):
    """
    gesture_anchors: dict with 'shoulder_l', 'shoulder_r', 'hip_l', 'hip_r'
    These come FROM the gesture line, not from rectangle edges.
    """
```

This is a future-cycle integration task. For C50, the gesture line library establishes the data that the new system will consume.

---

## Part 7: Minimum Body Articulation for Motion to Read

### The Question
How many control points does a character body need? Where do the joints need to be?

### The Answer: 9 Control Points Minimum

After studying the reference shows and testing gesture-line readability at stick-figure scale, the minimum articulation for motion to read is:

| # | Point | What It Controls |
|---|---|---|
| 1 | Head center | Head position, tilt, emotional direction |
| 2 | Neck base | Head-to-body connection, where the gesture line enters the torso |
| 3 | Shoulder L | Left arm origin, shoulder involvement rule |
| 4 | Shoulder R | Right arm origin, shoulder involvement rule |
| 5 | Hip center | Weight distribution pivot, contrapposto origin |
| 6 | Hip L | Left leg origin, pelvic tilt |
| 7 | Hip R | Right leg origin, pelvic tilt |
| 8 | Weight foot | Ground contact, primary support |
| 9 | Free foot | Secondary contact, balance/gesture |

### Why 9 and Not Fewer

- **Without separate hip points (5-7):** No pelvic tilt, no contrapposto. The body is a pole.
- **Without separate shoulder points (3-4):** No shoulder involvement, arms attach to a box.
- **Without separate feet (8-9):** No weight distribution, character floats.

### Optional Points That Improve Quality

| # | Point | What It Adds | When to Include |
|---|---|---|---|
| 10 | Elbow L | Two-segment arm | When arm bend is visible |
| 11 | Elbow R | Two-segment arm | When arm bend is visible |
| 12 | Knee L | Two-segment leg | When knee bend is visible |
| 13 | Knee R | Two-segment leg | When knee bend is visible |
| 14 | Hand L | Hand shape/gesture | When hands carry meaning |
| 15 | Hand R | Hand shape/gesture | When hands carry meaning |

At 15 points, every joint in the body is articulated. But 9 is the minimum for the gesture line to read.

### The Current System Uses 3 Effective Points

Our current generators use: `cx` (one vertical axis for everything), `ground_y`, and `head_top`. That is 3 control points. Every body part derives from these 3, which is why every pose looks the same.

Going from 3 to 9 is the minimum viable change. Going from 3 to 15 is the full system.

---

*Gesture Line Library C50 — Ryo Hasegawa, Motion & Animation Concept Artist*
