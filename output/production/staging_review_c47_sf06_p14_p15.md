<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Staging Review — C47

**Author:** Lee Tanaka (Character Staging & Visual Acting Specialist)
**Date:** 2026-03-30
**Assets Reviewed:**
- SF06 "The Hand-Off" (`LTG_COLOR_sf_miri_luma_handoff.png`) — Maya Santos C44
- P14 "Byte Ricochets Off Bookshelf" (`LTG_SB_cold_open_P14.png`) — Diego Vargas C45
- P15 "Luma Hits Floor / Glitch Forced-Hair Circle" (`LTG_SB_cold_open_P15.png`) — Diego Vargas C45

---

## SF06 "The Hand-Off" — Staging Assessment

### What Works
1. **Warm/cool split is the right instinct.** Miri left in warm (lamp) zone, Luma right in CRT cool zone. The tonal contrast between analog warmth and digital cool IS the show's thesis, and it reads in a single glance.
2. **CRT center composition.** The television between the two characters functions as the compositional hinge — the object that connects and separates them. Correct for a "hand-off" beat.
3. **Miri's right arm extended toward CRT.** The reaching gesture is the staging hook — her hand on the TV is the visual sentence: "I'm giving you this." This reads clearly.
4. **Two-character ground plane.** Both characters on the same ground line (GROUND_Y = 90%) in the foreground. No ambiguous depth separation for this scene.
5. **Living room environment.** Floor rug, family photos, CRT on stand — the environment is specific and inhabited. Good.

### Issues Found

#### ISSUE 1 — Miri's Arm Lacks Shoulder Engagement (Takeshi C15 persistent note)
**Severity:** WARN
**Description:** Miri's right arm (the "hand-off" gesture arm) draws as a polyline from `ra_shoulder` to `ra_elbow` to `ra_hand`, but the shoulder joint itself does not move. The cardigan torso rectangle remains symmetric — the right shoulder should pull forward and slightly upward when the arm extends rightward. Without deltoid/trapezius shift, the arm reads as a mechanical appendage, not a gesture with physical effort.
**Fix:** When `ra_shoulder` extends rightward by `HU * 0.35` at the elbow, the shoulder point itself should shift right by ~`HU * 0.06` and up by ~`HU * 0.03`. The cardigan torso silhouette needs an asymmetric right-shoulder bump (not a rectangle).
**Recipient:** Maya Santos (character geometry owner). See also Priority 3 shoulder mechanics notes below.

#### ISSUE 2 — Luma's Body Language is Passive
**Severity:** WARN
**Description:** The generator docstring says Luma's posture should be "attentive curiosity — she's being shown something." However, I cannot verify from the code alone that Luma's body lean is clearly forward. At style-frame scale, "attentive" requires a visible forward lean (4-6 degrees), weight on the balls of the feet, and head tilted slightly toward the CRT. If she stands straight, she reads as "present" but not "interested."
**Fix:** Confirm Luma's torso has a forward lean offset. Head_cx should shift ~`HR * 0.08` toward the CRT (leftward, since she's right of CRT). This is the same interiority principle from the SF02 staging brief — the body participates in the seeing.
**Recipient:** Maya Santos (for any character geometry updates) / Hana Okonkwo (living room env).

#### ISSUE 3 — Depth Temperature Lint: WARN (sep=11.0, threshold=12.0)
**Severity:** NOTE (informational)
**Description:** The depth temperature lint (C46 tool, now Section 12 in precritique_qa) reports SF06 as WARN: FG warmth=64.0, BG warmth=53.0, separation=11.0 (just under the 12.0 REAL_INTERIOR threshold). The depth grammar is correct direction (warm FG, cool BG) but the contrast could be slightly stronger. NOTE: The default sampling bands (78% FG, 70% BG) may not perfectly match SF06's composition, where both characters are at 90% ground plane. This may be a false proximity — the warm/cool split is actually between the left and right halves of the frame (horizontal), not the FG/BG tiers (vertical).
**Fix:** This is expected behavior for a horizontal warm/cool split scene. The depth temp lint is designed for vertical FG/BG tier separation (lineup, multi-tier). For SF06, the WARN is acceptable. No action needed unless the vertical depth cue is also intended.

#### ISSUE 4 — Eye Flow Direction Unverified
**Severity:** NOTE
**Description:** The intended eye flow is: Miri's hand → CRT screen → Luma's face. This requires (a) Miri's gesture to be the entry point (first element the eye finds), (b) the CRT screen glow to pull the eye rightward, (c) Luma's face to be the resting point. Without running the sight-line diagnostic tool on the rendered output, I cannot confirm the eye flow geometrically. The composition appears sound in code, but the glow weighting determines the pull.
**Fix:** Run `LTG_TOOL_sight_line_diagnostic.py` on the rendered SF06 PNG with Miri's eye as source and CRT screen center as target, then CRT screen center as source and Luma's face as target.

---

## P14 "Byte Ricochets Off Bookshelf" — Staging Assessment

### What Works
1. **Multi-exposure ghost trail.** 5 ghost Byte silhouettes along a quadratic Bezier arc from lower-left origin to upper-right impact. Opacity ramps from 0.15 (origin) to 1.0 (impact). Scale increases toward impact. This is the correct storyboard grammar for fast cartoon motion — the trail IS the velocity, and the viewer reads it backward from impact.
2. **Airborne objects.** 3 books tumbling from the gap in the top shelf, plus the rubber duck. Each book has a distinct tilt angle — they're in different rotational states, which sells "mid-air chaos."
3. **Dutch tilt 12 degrees CW.** Applied via `Image.rotate(-12)` to the entire draw area (not the caption). Correct implementation (C9 lesson: Dutch tilt = rotate ENTIRE scene canvas).
4. **Impact star burst at Byte's position.** Radial lines at the impact point confirm the energy center. Reads well alongside the Bezier endpoint.
5. **Confetti scatter in the upper-right zone.** 28 particles from Byte's impact zone. TENSE density.

### Issues Found

#### ISSUE 5 — Byte Has No Expression at Impact Point
**Severity:** WARN
**Description:** The final (impact) Byte silhouette at `(PW*0.60, DRAW_H*0.15)` uses `draw_byte_silhouette()`, which draws two symmetric eye rectangles (VOID_BLACK 4px blocks) on the head. There is no expression differentiation — the docstring specifies "ALARMED expression" but the silhouette function draws the same face for all ghost positions. At the impact point (alpha=1.0, scale=1.0), this is Byte's most visible moment in the panel. He needs ALARMED eyes: cracked eye wider than normal eye, asymmetric brow lines above both eyes.
**Fix:** Add expression parameters to `draw_byte_silhouette()` or draw Byte's impact-position face separately with ALARMED geometry (one eye wider, both brows raised as short angled lines, mouth line). The ghost trail silhouettes (alpha < 1.0) can remain expressionless — they're motion blur.
**Recipient:** Diego Vargas.

#### ISSUE 6 — No Shoulder/Arm Recoil on Impact Byte
**Severity:** NOTE
**Description:** The silhouette function draws symmetric arms (same length left and right). At impact, Byte should show bounce-back recoil: one arm trailing behind (still moving forward), other arm thrown outward (impact reaction). Body language asymmetry sells the physical contact. Current symmetric arms read as "hovering," not "just hit something."
**Fix:** For the final (impact) ghost position, override arm angles to show asymmetric recoil. Left arm trailing back (shorter, angled toward origin), right arm flung outward (longer, angled up-right from impact).
**Recipient:** Diego Vargas.

---

## P15 "Luma Hits Floor / Glitch Forced-Hair Circle" — Staging Assessment

### What Works
1. **Floor-level camera.** Wall strip at top 18%, floor dominates the remaining 82%. This is the correct camera height for a "floor is the world now" comedic fall. The baseboard is visible, the perspective converges — we ARE at 6 inches off the ground.
2. **Glitch forced-hair circle geometry.** The ELEC_CYAN outlined perfect circle around Luma's head, with interior radial lines in hair color, is exactly right. It reads as WRONG (forced geometric order on an organic shape) and therefore funny. The contrast between the radial-line hair (Glitch order) and Luma's canonical wild hair texture tells the worldbuilding beat without a word.
3. **DAZED expression.** One visible eye with reduced aperture, off-center downward iris, droopy eyelid arc. Flat slightly-open mouth ("ooof"). This is the correct post-impact read — she's winded, not hurt.
4. **Daze stars.** Three asterisks (alternating SUNLIT_AMBER and ELEC_CYAN) around the head. The color alternation is a nice touch — analog and digital worlds both contributing to her dazedness.
5. **Luma's hoodie (LUMA_HOODIE orange) is the warm color anchor** in a cool-ambient scene. Correct application of the warm/cool grammar — even in a scene dominated by Byte's ELEC_CYAN field, Luma's analog warmth persists.

### Issues Found

#### ISSUE 7 — Right Arm is Limp, Not Urgent (C12/C13 pattern)
**Severity:** WARN
**Description:** Luma's right arm reaching forward from `torso_x` to `arm_end_x = PW * 0.22` is drawn as a single 18px-wide line. At floor level, this arm should show post-fall sprawl energy — not a neat line extending politely forward. The arm should bend at the elbow (mid-point deflection), fingers spread or fist visible at the endpoint, and the hoodie sleeve should bunch at the elbow crook. A single straight line reads as "mannequin arm."
**Fix:** Replace the single arm line with a two-segment polyline (shoulder → elbow → hand), with the elbow deflected 15-20px below the shoulder-hand midpoint. Add a hand blob (mitten oval, 10-12px) at the endpoint. This is the same urgency principle from P15 C12/C13 — limbs must SHOW the force that put them there.
**Recipient:** Diego Vargas.

#### ISSUE 8 — Body Sprawl is Too Neat
**Severity:** NOTE
**Description:** Luma's body (hoodie rectangle + pants rectangle) draws as aligned rectangles. A post-fall sprawl should show rotation — the torso twisted slightly relative to the legs, one knee bent, shoes at different angles. The current layout reads as "lying flat by choice" rather than "just hit the floor after being knocked down." Even a 4-6 degree rotation of the hoodie rectangle and a knee bend on one leg would sell the fall.
**Fix:** Rotate the hoodie body fill 4-6 degrees. Bend one leg at the knee (two segments instead of one rectangle). Offset one shoe from the other vertically.
**Recipient:** Diego Vargas.

---

## Summary of Action Items

| # | Asset | Severity | Description | Recipient |
|---|-------|----------|-------------|-----------|
| 1 | SF06 | WARN | Miri right arm shoulder engagement — deltoid shift missing | Maya Santos |
| 2 | SF06 | WARN | Luma body lean toward CRT — attentive posture unverified | Maya Santos |
| 3 | SF06 | NOTE | Depth temp lint WARN (sep=11.0, horizontal split scene) | N/A |
| 4 | SF06 | NOTE | Eye flow unverified — run sight-line diagnostic | Jordan Reed / Hana |
| 5 | P14 | WARN | Byte impact silhouette has no ALARMED expression | Diego Vargas |
| 6 | P14 | NOTE | Byte symmetric arms at impact — needs recoil asymmetry | Diego Vargas |
| 7 | P15 | WARN | Luma right arm is single straight line — needs elbow bend + hand | Diego Vargas |
| 8 | P15 | NOTE | Body sprawl too neat — needs rotation + knee bend | Diego Vargas |

**Overall assessment:** All three assets are structurally sound — the staging reads and the beats are correct. The issues are refinements in physical acting: shoulder mechanics, expression at key moments, and body language that sells physical contact. No blocking issues.
