<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->

# Cosmo Gesture Specification — C52
## Lee Tanaka — Character Staging & Visual Acting Specialist
**Date:** 2026-03-30

---

## Character Baseline

**Cosmo** is an older teen with angular, rectangular shapes. His body language is more contained than Luma's — where she flows, he bends at joints. His counterpose creates visible ANGULAR breaks at the waist, not smooth curves. His glasses tilt with his head tilt (they are ON his face, not floating). His default stance is wider than Luma's (taller, more cautious base of support).

**Permanent traits:**
- Glasses tilt 2-3 degrees with head tilt (NEVER level when head tilts)
- Arms default to asymmetric (one hand in pocket, one at side)
- Rectangular torso creates angular silhouette breaks (not smooth S-curves)
- SKEPTICAL is his signature pose — whole body says "I'm not buying it"

**Offset chain format (same as Luma C50 spec):**
```
hip_cx = cx + hip_shift_px
torso_cx = hip_cx + shoulder_offset_px
head_cx = torso_cx + head_offset_px
```

All pixel values at 2x render scale (2560x1440). Halve for 1x.

---

## Expression 1: AWKWARD

**Emotional logic:** Something socially uncomfortable just happened. His body tries to minimize its own existence while also broadcasting "I know this is awkward" to anyone watching. Maximum geometric dissonance — nothing lines up.

**Gesture line:** Broken Z-shape. NOT a smooth curve — angular breaks at waist and shoulders create a zigzag. Head goes one way, shoulders the opposite, hips the opposite of shoulders. The body is a diagram of indecision.

**Weight:** 65/35 on one leg (he's leaning away from the awkward thing but can't fully commit to leaving). Weight-bearing leg is straight, locked. Free leg is bent at the knee, foot turned inward (pigeon-toed but angular, not cute like Luma's).

**Counterpose:**
- Hip tilt: 5 degrees toward weight leg (angular break visible at waist)
- Shoulder tilt: -6 degrees (opposite to hips, sharper compensation)
- Head tilt: 8 degrees (same direction as hips — he's looking AWAY from the awkward thing, which means toward his weight side, creating the Z-break)

**Arms:** MAXIMUM asymmetry. Left arm hangs dead at side, slightly behind the body (he's forgotten it exists). Right arm is up, hand behind neck or rubbing back of head (self-soothing displacement gesture). The asymmetry IS the awkwardness — one arm checked out, one arm hyperactive.

**Feet:** One foot flat, turned outward 20 degrees (stable). Other foot on toe tip, turned inward 15 degrees, slightly behind (ready to flee). Gap between feet wider than normal stance (he's off-balance internally, even if standing).

**Spec values:**
```
hip_shift: 14
shoulder_offset: -16
head_offset: 14     # same direction as hips = Z-break
torso_lean: 6       # slight backward lean (recoiling from the situation)
hip_tilt: 5.0
shoulder_tilt: -6.0
head_tilt: 8.0
weight_front: 0.35
weight_back: 0.65
front_foot_lift: 4   # toe tip
back_foot_lift: 0
front_foot_angle: -15  # inward
back_foot_angle: 20    # outward
left_arm: "dead_hang"
right_arm: "neck_rub"
```

**Silhouette target:** The Z-break silhouette should be unique. RPD vs any other Cosmo pose should be <= 72%.

---

## Expression 2: WORRIED

**Emotional logic:** Something might go wrong and he can't fix it with a plan. His body contracts inward but his HEAD stays up (he's monitoring the threat, not hiding). Unlike Luma's worried (which curls inward softly), Cosmo's worry is a rigid defensive posture — arms form a visible bracket around his torso.

**Gesture line:** Compressed vertical with angular shoulder hunch. The torso stays relatively straight (he doesn't curl — he STIFFENS), but the shoulders rise sharply and the head pushes forward. Think of someone bracing for impact.

**Weight:** 50/50 even split BUT both knees slightly bent (he's lowered his center of gravity — defensive crouch without actually crouching). Feet close together (contracted stance).

**Counterpose:**
- Hip tilt: 2 degrees (minimal — he's symmetric in worry, unlike Luma)
- Shoulder tilt: 0 degrees BUT shoulders are RAISED 8-10px (hunched, protective)
- Head tilt: -6 degrees forward (chin dips, eyes look up from under brow = monitoring threat)

**Arms:** Both arms raised to bracket the torso — left hand grips right bicep, right hand grips left bicep (the "self-hug" but angular, not soft). Elbows point outward, creating a WIDE bracket shape that makes the silhouette distinctly different from AWKWARD (which is asymmetric).

**Feet:** Both flat, close together, turned slightly inward (contracted). Knees angled inward 5 degrees (knock-kneed defensive).

**Spec values:**
```
hip_shift: 0          # symmetric worry
shoulder_offset: 0
head_offset: -10      # head forward (monitoring)
torso_lean: -4        # slight forward lean (bracing)
hip_tilt: 2.0
shoulder_tilt: 0.0
head_tilt: -6.0
weight_front: 0.50
weight_back: 0.50
front_foot_lift: 0
back_foot_lift: 0
front_foot_angle: -8
back_foot_angle: -8
shoulder_raise: 10    # px — both shoulders UP (hunch)
left_arm: "bracket_grip_right"
right_arm: "bracket_grip_left"
```

**Silhouette target:** WIDEST upper-body silhouette (bracket arms create horizontal extent). NARROWEST lower body (contracted feet). RPD vs AWKWARD should be <= 70%.

---

## Expression 3: SURPRISED

**Emotional logic:** Something unexpected — but unlike Luma (who stumbles backward), Cosmo's surprise is more about freezing. His body locks up, then one side breaks free. His surprise is angular and jerky, not fluid.

**Gesture line:** Sharp backward diagonal. The torso tilts as a rigid unit (no smooth curve — the rectangle tilts). Head snaps opposite to torso tilt (whiplash angular break at the neck).

**Weight:** 75/25 on the back foot. Front foot lifts but stays FLAT (not on toes — his foot is lifted parallel to ground, like it was pulled up by a string). This is mechanically different from Luma's startle toe-tip.

**Counterpose:**
- Hip tilt: -6 degrees (toward back foot, sharp angular break)
- Shoulder tilt: 7 degrees (opposite to hips, but NOTE: both shoulders RISE as well — startle hunch)
- Head tilt: -10 degrees (whips opposite to shoulder tilt direction — angular break at neck)

**Arms:** One arm up defensively (palm outward, fingers spread — the "stop" gesture). Other arm flung outward at full extension, HORIZONTAL (counterbalance). Maximum horizontal arm spread makes this the WIDEST full-body silhouette.

**Feet:** Back foot planted flat, turned outward 15 degrees. Front foot lifted 12px, FLAT (parallel to ground, not toe-pointing). This flat-lifted foot is Cosmo's signature — mechanical, not organic.

**Spec values:**
```
hip_shift: -20
shoulder_offset: 16
head_offset: -14     # head whips opposite to shoulders
torso_lean: 22       # backward lean (rigid tilt)
hip_tilt: -6.0
shoulder_tilt: 7.0
head_tilt: -10.0
weight_front: 0.25
weight_back: 0.75
front_foot_lift: 12
back_foot_lift: 0
front_foot_angle: 0   # flat, parallel to ground
back_foot_angle: 15
shoulder_raise: 6      # startle hunch (less than WORRIED)
left_arm: "stop_palm"
right_arm: "flung_horizontal"
```

**Silhouette target:** WIDEST full-body silhouette (horizontal flung arm + lifted foot). RPD vs WORRIED should be <= 65%.

---

## Expression 4: SKEPTICAL (Signature Pose)

**Emotional logic:** He does not believe what he is hearing. His body arranges itself into a visual argument: weight dramatically on one leg, arms crossed, head tilted with one brow raised. The whole body is a counterargument before he opens his mouth.

**Gesture line:** Exaggerated S-curve with angular breaks. Hips push dramatically to one side, torso compensates the other direction, head tilts back toward the hip side. The S has sharp angle changes at the waist and shoulder line — not smooth like Luma's.

**Weight:** 85/15 — nearly all weight on one leg. The weight-bearing leg is LOCKED STRAIGHT (rigid, like a column supporting a building that disagrees with its architect). Free leg bends visibly at the knee, toe barely touching ground.

**Counterpose:**
- Hip tilt: 8 degrees (dramatic pop — the sharpest hip tilt on the sheet)
- Shoulder tilt: -7 degrees (angular break opposite to hips)
- Head tilt: 6 degrees (back toward hip side — the "really?" tilt)

**Arms:** Crossed over chest, but NOT symmetric. Left arm is OVER right arm, with left hand gripping right bicep and right hand tucked under left bicep. The crossed arms must create visible angular breaks at the elbows (rectangles, not smooth wrapping). Glasses tilt 3 degrees with head.

**Feet:** Weight foot flat, turned outward 25 degrees (maximum stability — he could stand like this all day). Free foot barely touching, turned inward, 8px behind weight foot.

**Spec values:**
```
hip_shift: 22         # dramatic hip pop
shoulder_offset: -18
head_offset: 12       # back toward hip side
torso_lean: -2        # nearly upright (confidence)
hip_tilt: 8.0
shoulder_tilt: -7.0
head_tilt: 6.0
weight_front: 0.15     # free leg barely touches
weight_back: 0.85
front_foot_lift: 2     # barely touching
back_foot_lift: 0
front_foot_angle: -10  # inward
back_foot_angle: 25    # out (planted)
left_arm: "crossed_over"
right_arm: "crossed_under"
glasses_tilt: 3.0
```

**Silhouette target:** The dramatic S-curve + crossed arms create a unique silhouette. RPD vs AWKWARD should be <= 68% (both asymmetric but different asymmetries).

---

## Expression 5: DETERMINED

**Emotional logic:** He has a plan and he is going to execute it. Unlike Luma's determination (which is expansive/planted), Cosmo's is FORWARD — he leans into the problem with angular precision. He is a rectangle aimed at a target.

**Gesture line:** Forward diagonal. Torso leans forward as a rigid unit, head pushes AHEAD of the torso center (leading with his brain). Hips stay back (the body is a lever, with the hips as the fulcrum).

**Weight:** 70/30 on the front foot. Front leg bent at the knee (ready to push off). Back leg straight, angled backward (providing thrust). This is the most DIRECTIONAL stance — the body points like an arrow.

**Counterpose:**
- Hip tilt: -3 degrees (slight, because hips are nearly level — this is deliberate, not accidental)
- Shoulder tilt: 4 degrees (one shoulder forward, one back — the torso is slightly rotated, implying he's about to turn and walk)
- Head tilt: -3 degrees down (looking at the problem, not at the sky)

**Arms:** Asymmetric. Right arm is bent sharply at elbow, fist at hip level, pulled back (cocked, ready to act — or holding a phone/map/plan). Left arm is forward, hand open, pointing or gesturing at the target. The arm positions create a diagonal line that reinforces the forward gesture.

**Feet:** Front foot pointing forward (direct, no angle — he's going THAT WAY). Back foot turned outward 20 degrees for push-off stability. Stance slightly wider than neutral.

**Spec values:**
```
hip_shift: -8          # slight backward (hips as fulcrum)
shoulder_offset: 12
head_offset: 8         # head leads forward
torso_lean: -14        # forward lean (angular, committed)
hip_tilt: -3.0
shoulder_tilt: 4.0
head_tilt: -3.0
weight_front: 0.70
weight_back: 0.30
front_foot_lift: 0
back_foot_lift: 0
front_foot_angle: 0    # pointing straight ahead
back_foot_angle: 20    # push-off angle
left_arm: "pointing_forward"
right_arm: "fist_at_hip"
```

**Silhouette target:** The forward diagonal + asymmetric arms make this clearly different from SKEPTICAL (backward lean). RPD vs SKEPTICAL should be <= 70%.

---

## Expression 6: FRUSTRATED

**Emotional logic:** The plan failed — and unlike Luma's frustration (which is a burst of energy), Cosmo's frustration is a CONTAINED EXPLOSION. He's too proud to thrash. Instead, the frustration manifests as rigid angular breaks — a body fighting itself. One part wants to throw something, the other part is holding it together.

**Gesture line:** Twisted diagonal with angular breaks at every joint. The torso twists (one shoulder visibly forward, one back — seen in front view as one shoulder wider than the other). Hips resist the twist. Head drops forward. The whole body looks like a wrung towel.

**Weight:** 80/20 dramatically to one side (he just stomped or is about to). Weight-bearing knee slightly bent (absorbed impact). Free leg barely touching, angled sharply.

**Counterpose:**
- Hip tilt: 7 degrees (dramatic, toward the stomp side)
- Shoulder tilt: -8 degrees (opposite, creating visible twist)
- Head tilt: -10 degrees forward and down (looking at the ground, refusing to look at the failure)

**Arms:** One arm rigid at side, fist clenched, elbow locked (controlled rage — the arm he's NOT letting throw something). Other arm: hand on forehead or pushing through hair (the self-directed gesture — he's blaming himself). Maximum tonal contrast between the two arms: one is RIGID CONTROL, one is LOSING CONTROL.

**Feet:** Weight foot planted firmly, turned outward 15 degrees. Free foot lifted slightly, turned sharply inward (closed off, like his emotional state). Stance narrower than DETERMINED (he's contracting from the expansive plan-mode he just left).

**Spec values:**
```
hip_shift: 18
shoulder_offset: -20
head_offset: -6        # drops forward
torso_lean: 4          # slight backward (twist makes this read as tension, not relaxation)
hip_tilt: 7.0
shoulder_tilt: -8.0
head_tilt: -10.0
weight_front: 0.20
weight_back: 0.80
front_foot_lift: 3
back_foot_lift: 0
front_foot_angle: -18   # sharply inward (closed)
back_foot_angle: 15
left_arm: "rigid_fist"
right_arm: "forehead_grip"
```

**Silhouette target:** The twist + angular breaks make this the most COMPLEX silhouette (more edges than any other pose). RPD vs DETERMINED should be <= 68%.

---

## Counterpose Angle Summary Table

| Expression | Hip Tilt | Shoulder Tilt | Head Tilt | Torso Lean | Gesture Shape |
|---|---|---|---|---|---|
| AWKWARD | 5 R | -6 L | 8 R | 6 back | Z-break |
| WORRIED | 2 R | 0 (raised) | -6 fwd | -4 fwd | Compressed vertical |
| SURPRISED | -6 L | 7 R (raised) | -10 L | 22 back | Sharp backward diagonal |
| SKEPTICAL | 8 R | -7 L | 6 R | -2 | Exaggerated angular S |
| DETERMINED | -3 L | 4 R | -3 fwd | -14 fwd | Forward diagonal |
| FRUSTRATED | 7 R | -8 L | -10 fwd | 4 back | Twisted diagonal |

---

## Implementation Notes for Maya Santos / Sam Kowalski

### Cosmo-Specific Code Changes

The offset chain architecture is the same as Luma's (see C50 spec). The difference is that Cosmo's torso is rectangular — angle changes should be VISIBLE as angular breaks, not smooth curves.

```python
# Cosmo torso: keep rectangular corners sharp during tilt
# Do NOT smooth/round the torso corners when hip_tilt or shoulder_tilt are applied
# The angular breaks ARE the character's body language
```

### Glasses Rule
```python
glasses_tilt_deg = spec.get("glasses_tilt", head_tilt * 0.4)
# Glasses always tilt WITH the head, at ~40% of head tilt angle
# This is a free character detail — never leave glasses level when head tilts
```

### Testing

1. Run `LTG_TOOL_gesture_line_lint.py` on rebuilt expression sheet — all 6 should PASS (> 8px deviation at scale)
2. Run `LTG_TOOL_expression_silhouette.py` — all pairs should have RPD <= 82% (target <= 72%)
3. Run `LTG_TOOL_character_face_test.py --char cosmo` — face legibility preserved after body changes

### Build Order Recommendation

Start with **SKEPTICAL** (his signature, most dramatic S-curve) and **SURPRISED** (maximum backward tilt, most different from current). These two will validate the angular-break approach immediately.
