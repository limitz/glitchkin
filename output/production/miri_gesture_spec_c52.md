<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->

# Grandma Miri Gesture Specification — C52
## Lee Tanaka — Character Staging & Visual Acting Specialist
**Date:** 2026-03-30

---

## Character Baseline

**Grandma Miri** is elderly, warm, and rounded. Her counterpose communicates AGE and WARMTH — not weakness. She has decades of habitual posture encoded in her neutral stance. She is the character with the MOST built-in counterpose because her body has a lifetime of physical habits.

**Permanent traits (ALL expressions):**
- Forward lean: 3-5 degrees ALWAYS (she leans INTO the world, never away from it)
- Hip favors LEFT in all poses (decades of carrying, stirring, holding)
- Shoulders slightly rounded forward (gentle, not hunched)
- Hands are NEVER idle — one hand is always doing something (holding a spoon, adjusting a towel, touching a cheek, resting on hip). An empty-handed Miri is a Miri with no stage business.
- Head tilts are LARGER than other characters (8-12 degrees) — she is physically demonstrative
- Cardigan line follows shoulder tilt asymmetrically — hangs LONGER on the dropped-shoulder side

**Offset chain format (same as Luma C50 / Cosmo C52 spec):**
```
hip_cx = cx + hip_shift_px
torso_cx = hip_cx + shoulder_offset_px
head_cx = torso_cx + head_offset_px
```

All pixel values at 2x render scale (2560x1440). Halve for 1x.

**IMPORTANT:** Miri's `base_lean` of -4 (forward) is ADDED to the per-expression `torso_lean`. Every expression starts from a forward-leaning baseline, not from vertical.

---

## Expression 1: WARM/WELCOMING

**Emotional logic:** Someone she loves just walked through the door. Her body opens toward them — arms begin to spread, weight shifts forward, head tilts to the side (the universal "come here" body language). She is a doorway made of warmth.

**Gesture line:** Forward-leaning gentle C-curve with a wide opening at the shoulders. The curve starts at her feet, arcs forward through her permanently leaning torso, and continues through her head, which tilts toward the arriving person.

**Weight:** 55/45 forward. Front foot flat, planted. Back foot mostly flat but heel slightly lifted (she's about to step forward). Weight on the balls of both feet — she's ready to hug, not standing still.

**Counterpose:**
- Hip tilt: 4 degrees LEFT (her habitual side — even in joy, the body defaults to its pattern)
- Shoulder tilt: -5 degrees (opposite to hips, shoulders opening)
- Head tilt: 10 degrees toward the arriving person (large tilt — she is demonstrative)

**Arms:** WIDE OPEN. Both arms extended outward at roughly 45 degrees from the body, palms forward, slightly curved (the beginning of a hug shape, not a surrender). Left arm extends slightly farther than right (her dominant gesture side). Right hand may be holding a dish towel or spoon (stage business — she was in the middle of something when they arrived).

**Feet:** Front foot turned slightly outward 10 degrees (open, welcoming). Back foot turned slightly outward 15 degrees. Wider stance than neutral (she's creating a landing zone for the hug).

**Spec values:**
```
hip_shift: -8          # slight left (habitual)
shoulder_offset: 10
head_offset: -12       # toward the person
torso_lean: -6         # adds to base_lean=-4 for total -10 forward
hip_tilt: 4.0
shoulder_tilt: -5.0
head_tilt: 10.0
weight_front: 0.55
weight_back: 0.45
front_foot_lift: 0
back_foot_lift: 2      # heel lifting (about to step)
front_foot_angle: 10   # open
back_foot_angle: 15    # open
left_arm: "wide_open_extended"
right_arm: "wide_open_with_towel"   # or "wide_open_extended" if no prop
```

**Silhouette target:** WIDEST silhouette on the sheet (open arms). RPD vs CONCERNED should be <= 65%.

---

## Expression 2: SKEPTICAL/AMUSED

**Emotional logic:** Someone just said something that she sees right through, but she loves them anyway. The skepticism is warm, not cold. Her body says "I know you're lying and I find it endearing." One eyebrow up, the oblique mouth from KNOWING STILLNESS, but with more weight shift and a visible body opinion.

**Gesture line:** Asymmetric S-curve with a pronounced hip pop. The gesture line starts with the hip popping LEFT (her habitual side, exaggerated here), torso compensates with a gentle rightward lean, and head tilts back toward the hip side (looking down at the person with loving disbelief).

**Weight:** 75/25 on the LEFT leg (habitual hip, exaggerated for the expression). Free leg (right) bends at the knee, toe touching. This is her MOST asymmetric stance — the body IS the editorial comment.

**Counterpose:**
- Hip tilt: 7 degrees LEFT (exaggerated habitual pop)
- Shoulder tilt: -5 degrees (compensates)
- Head tilt: 8 degrees LEFT (back toward hip — the "really?" look)

**Arms:** Asymmetric. Left arm on hip (hand ON hip, elbow pointing out — the classic "I'm waiting for the truth" gesture). Right arm in front of body, hand raised to chin level, index finger and thumb touching chin (the evaluation gesture). Or right arm crossed under left elbow, right hand holding left bicep (half-crossed arms).

**Feet:** Weight foot (left) flat, turned outward 20 degrees (planted, she could stand like this for an hour waiting for the real story). Free foot (right) on toe, turned inward slightly, well behind the weight foot.

**Spec values:**
```
hip_shift: -18         # dramatic left pop
shoulder_offset: 12
head_offset: -10       # back toward hip
torso_lean: -2         # minimal added lean (base_lean does the work)
hip_tilt: 7.0
shoulder_tilt: -5.0
head_tilt: 8.0
weight_front: 0.25     # free leg barely touches
weight_back: 0.75
front_foot_lift: 3     # toe touching
back_foot_lift: 0
front_foot_angle: -5
back_foot_angle: 20
left_arm: "hand_on_hip"
right_arm: "chin_evaluation"
```

**Silhouette target:** The hip pop + elbow-out creates a wide mid-body silhouette. RPD vs WARM should be <= 68%.

---

## Expression 3: CONCERNED

**Emotional logic:** Something is wrong with someone she loves. Her body reaches toward them without moving her feet — the lean intensifies, the head tilts down to look at them (she's taller than Luma), one hand reaches out. She is a bridge trying to close a gap.

**Gesture line:** Deep forward C-curve. The steepest forward lean on the sheet. Head pushes forward and down (looking at the child). The curve is gentle, not angular — she's flowing toward them, not lunging.

**Weight:** 65/35 forward. Both feet grounded but weight heavily on the balls of the feet. She's leaning so far forward that her heels are light. One more degree and she'd step forward.

**Counterpose:**
- Hip tilt: 3 degrees LEFT (habitual, but subdued — concern overrides habit)
- Shoulder tilt: -3 degrees (gentle, rounded compensation)
- Head tilt: -12 degrees forward and down (the largest downward head tilt on the sheet — she's looking at someone shorter)

**Arms:** Asymmetric. Right hand reaches forward, palm up (offering, not grabbing — a gesture of "tell me what's wrong"). Left hand comes to her own chest, fingers spread (the "my heart" gesture — she feels what they feel). The two hand positions create a diagonal line: one hand toward the person, one hand toward herself = empathy bridge.

**Feet:** Both flat, close together, slightly pigeon-toed (unconscious mirroring of Luma's stance — she picked it up from a lifetime of looking at this child). Front foot slightly ahead (she's about to step forward).

**Spec values:**
```
hip_shift: -6          # subtle left
shoulder_offset: 6
head_offset: -16       # dramatic forward push
torso_lean: -10        # deep forward lean (adds to base_lean for total -14)
hip_tilt: 3.0
shoulder_tilt: -3.0
head_tilt: -12.0
weight_front: 0.65
weight_back: 0.35
front_foot_lift: 0
back_foot_lift: 0
front_foot_angle: -5   # slight pigeon-toe
back_foot_angle: -3
left_arm: "chest_touch"
right_arm: "reaching_palm_up"
```

**Silhouette target:** The deep forward lean + reaching arm create the most FORWARD silhouette. RPD vs WARM should be <= 70% (both reach outward but in different ways).

---

## Expression 4: SURPRISED/DELIGHTED

**Emotional logic:** Something wonderful and unexpected happened. Unlike Luma's surprise (which is a startle recoil) or Cosmo's (which freezes), Miri's surprise OPENS UPWARD. She's lived long enough that surprises are gifts. Her body lifts, her hands come to her face, her weight shifts upward.

**Gesture line:** Upward-opening C-curve. The body lifts from its habitual forward lean — this is the ONE expression where she approaches vertical. The head tilts BACK (looking up or reacting upward — unusual for Miri who usually looks down at shorter characters).

**Weight:** 50/50 even, but on the balls of both feet (she's slightly lifted — surprise as anti-gravity, same principle as Luma's DELIGHTED but gentler). Heels lift 2-3px.

**Counterpose:**
- Hip tilt: 3 degrees LEFT (habitual, minimal)
- Shoulder tilt: -4 degrees (gentle compensation, both shoulders slightly RAISED — surprise reflex)
- Head tilt: 8 degrees BACK and to one side (the "oh!" reaction)

**Arms:** Both hands come to face. Left hand covers mouth (the "oh my" gesture — fingers spread, palm near mouth but not quite touching). Right hand rises to cheek level, palm flat against cheek or just off the cheek (the hand-to-cheek surprise gesture). Both hands near the face make this silhouette NARROW at the shoulders and BUSY near the head.

**Feet:** Both slightly lifted on toes (not dramatic — Miri doesn't bounce like Luma, but the heels come off the ground in genuine surprise). Feet stay close together, turned slightly outward.

**Spec values:**
```
hip_shift: -4          # minimal left
shoulder_offset: 6
head_offset: 8         # back (unusual for Miri)
torso_lean: 2          # reduces base_lean — she's approaching vertical
hip_tilt: 3.0
shoulder_tilt: -4.0
head_tilt: 8.0         # back + side
shoulder_raise: 4      # slight surprise raise
weight_front: 0.50
weight_back: 0.50
front_foot_lift: 2     # heels up
back_foot_lift: 2
front_foot_angle: 8
back_foot_angle: 10
left_arm: "mouth_cover"
right_arm: "cheek_touch"
```

**Silhouette target:** Both-hands-to-face creates a unique head-area silhouette. RPD vs WARM should be <= 65% (widest vs most contained upper body).

---

## Expression 5: WISE/KNOWING

**Emotional logic:** She understands something that the person she's talking to hasn't figured out yet. She's not going to tell them — she's going to let them arrive at it. Her body is STILL, weighted, grounded. She is a mountain with a gentle smile.

**Gesture line:** Nearly vertical with subtle S-curve. This is Miri at her most STILL — the least dynamic pose on the sheet. But "still" for Miri still includes her forward lean, her hip habit, and her rounded shoulders. The gesture line is a gentle wave, not a straight pole.

**Weight:** 60/40 on LEFT leg (habitual, relaxed). She's comfortable, settled into a stance she's held a thousand times while watching her grandchild figure something out.

**Counterpose:**
- Hip tilt: 5 degrees LEFT (habitual, relaxed — this is her default)
- Shoulder tilt: -3 degrees (gentle, just enough for the S)
- Head tilt: 6 degrees to one side (the "I see you figuring it out" tilt)

**Arms:** Relaxed asymmetric. Left hand on hip (resting, not demanding — the elbow hangs rather than points). Right arm in front of body, forearm across waist, hand holding opposite elbow or wrist (the "I'm content to wait" gesture). This is a CONTAINED silhouette — no reaching, no spreading.

**Feet:** Weight foot (left) flat, turned outward 15 degrees. Free foot (right) flat but slightly ahead and turned slightly inward. Natural, habitual stance — she's not performing, she's just being.

**Spec values:**
```
hip_shift: -12         # habitual, relaxed
shoulder_offset: 8
head_offset: -6        # gentle forward (baseline Miri)
torso_lean: -1         # minimal added (base_lean dominates)
hip_tilt: 5.0
shoulder_tilt: -3.0
head_tilt: 6.0
weight_front: 0.40
weight_back: 0.60
front_foot_lift: 0
back_foot_lift: 0
front_foot_angle: -5
back_foot_angle: 15
left_arm: "resting_on_hip"
right_arm: "forearm_across_waist"
```

**Silhouette target:** The most COMPACT silhouette. RPD vs SURPRISED should be <= 65% (maximum contrast between most-open and most-contained).

---

## Expression 6: KNOWING STILLNESS

**Emotional logic:** The deepest expression — she has seen something that confirms what she always suspected. Her face carries the oblique mouth (C33) and gentle asymmetric eyes. Her body is VERY similar to WISE but with one critical difference: a slight weight shift forward, as if she is about to act on what she knows. Stillness with direction.

**Gesture line:** Similar to WISE but with a forward vector. The gentle S-curve is preserved but the center of gravity has shifted forward 3-5px — she is LEANING toward the future, not watching the present.

**Weight:** 55/45 forward (shifted from WISE's 60/40 left-right to a front-back emphasis). This is the subtlest weight difference on the sheet — but the difference between "observing" and "about to move" is felt even if it can't be named.

**Counterpose:**
- Hip tilt: 4 degrees LEFT (habitual, but shifted from WISE — slightly less pronounced because the weight has moved forward instead of sideways)
- Shoulder tilt: -3 degrees (same as WISE)
- Head tilt: 4 degrees to one side + 3 degrees forward (the combined tilt creates a diagonal that says "I know, AND I have decided")

**Arms:** Asymmetric, different from WISE. Left arm down at side, hand holding something meaningful (the towel she was holding when she stopped, or empty but with fingers slightly curled — she just let go of something). Right hand comes to center of chest, flat palm, fingers spread (the "I feel this in my chest" gesture). This hand position is the ONLY hand-to-chest gesture on the sheet — it marks this as the most emotionally resonant expression.

**Feet:** Both feet flat, slightly closer together than WISE. The stance is gathered — she's collecting herself before whatever comes next. Front foot points slightly forward (direction) rather than outward (stability).

**Spec values:**
```
hip_shift: -10
shoulder_offset: 8
head_offset: -8        # forward + slight side
torso_lean: -3         # adds to base_lean for more forward than WISE
hip_tilt: 4.0
shoulder_tilt: -3.0
head_tilt: 4.0         # side
head_forward: 3.0      # additional forward tilt
weight_front: 0.55
weight_back: 0.45
front_foot_lift: 0
back_foot_lift: 0
front_foot_angle: 2    # pointing forward (direction)
back_foot_angle: 10
left_arm: "dropped_with_released_object"
right_arm: "palm_to_chest"
```

**Silhouette target:** RPD vs WISE must be >= 18% (these are intentionally similar — the difference is subtle and that's the point). RPD vs all other poses should be <= 75%.

**NOTE:** WISE and KNOWING STILLNESS are the only pair on the sheet allowed to have RPD > 82% (i.e., high similarity). The C34 brief accepted these as intentionally similar with minor gesture hooks. The differentiation comes from: (1) forward weight shift, (2) hand-to-chest gesture vs forearm-across-waist, (3) front foot direction.

---

## Counterpose Angle Summary Table

| Expression | Hip Tilt | Shoulder Tilt | Head Tilt | Torso Lean (added) | Gesture Shape |
|---|---|---|---|---|---|
| WARM | 4 L | -5 R | 10 L | -6 fwd | Forward opening C |
| SKEPTICAL | 7 L | -5 R | 8 L | -2 | Asymmetric S with hip pop |
| CONCERNED | 3 L | -3 R | -12 fwd/dn | -10 fwd | Deep forward C |
| SURPRISED | 3 L | -4 R (+raised) | 8 back | +2 (reduces lean) | Upward opening C |
| WISE | 5 L | -3 R | 6 side | -1 | Gentle resting S |
| KNOWING | 4 L | -3 R | 4+3fwd | -3 fwd | Gentle forward S |

**Remember:** All `torso_lean` values ADD to Miri's permanent `base_lean` of -4 degrees forward.

---

## Implementation Notes for Maya Santos

### Miri-Specific Architecture

```python
# Miri base lean (permanent — all expressions start from here)
MIRI_BASE_LEAN = -4  # degrees forward (permanent)
MIRI_HABITUAL_HIP = "LEFT"  # habitual weight side

# Per-expression lean is ADDED:
effective_lean = MIRI_BASE_LEAN + spec["torso_lean"]
```

### Cardigan Physics
```python
# Cardigan hem hangs longer on the dropped-shoulder side
# This is free visual storytelling
cardigan_extension_dropped_side = 6  # px longer than raised side (at 2x)
# Cardigan shoulder fabric bunches on the raised side
```

### Hands-Never-Idle Rule
Every expression must specify both hand positions. At least ONE hand should either:
- Hold a prop (towel, spoon, teacup, phone)
- Touch a body part (hip, chest, chin, cheek)
- Be actively gesturing

If no prop is specified, the hand should have slight finger articulation (not a flat paddle) — curled, spread, or pointing.

### Testing

1. Run `LTG_TOOL_gesture_line_lint.py` on rebuilt sheet — all 6 should PASS (> 8px deviation at scale)
2. WISE and KNOWING STILLNESS are expected to have high RPD (> 82% similar) — this is intentional, not a failure
3. Run `LTG_TOOL_character_face_test.py --char miri` — face legibility preserved
4. Verify `base_lean` is present in ALL poses (Miri should never stand vertical)

### Build Order Recommendation

Start with **WARM/WELCOMING** (widest arms, most dramatic difference from current straight stance) and **CONCERNED** (deepest forward lean). These two validate that Miri's permanent forward lean + the wide-vs-narrow arm contrast produce readable silhouette differentiation.
