# Takeshi Mori — Critique Cycle 15
**Date:** 2026-03-30
**Focus:** Pose believability, weight, performance quality, staging clarity, motion spec physical grounding

---

## 1. Pilot Cold Open Storyboard — LTG_SB_pilot_cold_open.png

**Score: 54/100**

- **P1 ESTABLISHING — Luma's entry pose is inert.** The figure stands upright mid-frame, weight centered, arms neutral. No forward momentum implied. A character whose spec says "acts first, thinks second" should enter a space with a leading foot, a tilted center of gravity, the body already in transit. This pose could be anyone walking into any room.
- **P1 — Ground contact line missing from figure.** Feet are rendered as symmetric downward extensions with identical ground contact. Spec says duck-footed outward tilt at rest — this figure has parallel vertical legs. No weight implied. Drawings of shapes pretending to be bodies.
- **P4 MCU PUSH-IN — Hoodie color is LUMA_HOODIE = (72, 112, 148), a slate blue.** Canonical spec (luma.md, RW-01) is Luma Hoodie Orange. The storyboard has recolored Luma's primary identity marker without justification. This is not a lighting choice — the warm amber glow from left is present in the same panel and the hoodie remains blue throughout. A costume substitution in a pitch board will be read as a design error.
- **P4 — Forward lean geometry does not commit.** Body polygon top edge slopes 3px over 60px width (under 3°). Spec calls for a character leaning toward something she cannot look away from. At this tilt, the center of gravity has not shifted. She is upright with a slightly skewed torso. The physics say she is not leaning — she is swaying. Next action is ambiguous.
- **P5 ECU TWO-WORLD TOUCH — Byte's arms have no shoulder origin.** The code draws arm lines from body-edge midpoints directly to the contact point. There is no shoulder socket geometry, no scapular involvement. Arms at this scale, in ECU, must show where they originate. Line-from-oval-edge reads as a flag on a stick, not a limb under effort.
- **P5 — Byte pressing against glass: the effort has no physical evidence.** The body oval is centered in the Glitch half of the panel, floating freely. When a form presses against a surface, weight compresses: body shifts toward the surface, limbs shorten on the push-side. None of this is present. The "press" is annotated but not drawn.
- **P6 THE NOTICING — Brow asymmetry present but eyelid correction absent.** Left brow is lifted (correct). Right brow shows a straight line 4px above eye — nearly flush with the lash line. At MCU scale (head_rx=52, head_ry=58px in the generator) this reads as one raised brow and one expressionless eye, not the wonder/apprehension split the brief demands. The right eyelid needs 2-3px more aperture reduction.
- **P6 — Head has zero tilt.** The expression brief calls for the micro-lean of arrested attention. luma_cx is W//2, luma_head_cy is a fixed vertical. The head is perfectly centered and vertical. A character in the act of noticing something specific tilts fractionally toward it. This head is observing everything equally.

**Bottom line:** The board describes the right beats but the figures do not inhabit them — they stand in position and wait for the reader to supply the performance.

---

## 2. Luma Expression Sheet v010 — THE NOTICING Rework

**Score: 67/100**

- **Brow asymmetry now survives thumbnail — improvement over v009 confirmed.** Left brow at -int(HR*0.22) reads as a distinct lift at panel scale. This was the correct diagnosis and the correct fix. The delta from v009 is meaningful.
- **Eye asymmetry l_open=1.0 / r_open=0.65 is the right direction but the right-eye narrowing reads as a wince.** At 65% aperture, the lower lid has risen enough that it crowds the iris from below. A "noticing" squint — the kind that says "I am tracking something specific" — is a top-lid drop, not a bottom-lid rise. The current geometry looks like she's squinting against a bright light, not focusing on something interesting. Rework: lower lid stays at its natural resting position; upper lid drops by 25-30% of aperture.
- **Finger-to-lower-lip gesture is a correct instinct.** The vertical forearm line is visually distinct from all other expressions. The specificity of contact (finger to lip vs. chin-touch v009) is the right kind of detail — it implies a half-second of held breath. This works.
- **Lateral gaze direction (gaze_dx=-0.5, gaze_dy=0.0) is an improvement.** Zero vertical component snaps the gaze to feel directed. However: at the current iris position within the eye white, the gaze reads as looking hard left rather than tracking something at moderate distance. A 0.15 vertical upward component (looking slightly up-left, as you would to notice something at screen level across a room) would read as "distance object" rather than "looking at floor."
- **The hoodie color change from v009 is not a pose issue — no comment from me.**

**Bottom line:** THE NOTICING is landing better than v009 and worse than it needs to — fix the wince-read on the right eye and the iris needs one more directional degree of specificity.

---

## 3. Cosmo Expression Sheet v006

**Score: 72/100**

- **S003 glasses_tilt compliance fix (10°→7°) is correct and necessary.** A character whose glasses are systematically off-spec will draw incorrect on every production artist's desk. This is not aesthetic — it is structural. The fix is confirmed.
- **SKEPTICAL silhouette remains a recurring concern (flagged C8, C15).** Arms crossed behind body: at thumbnail scale, the silhouette reads as a figure with no arms. The arm mass disappears behind the torso polygon. Cross-in-front resolves this without changing the emotional read of the expression.
- **WORRIED vs SURPRISED pair: wide-W crown vs wide-horizontal-middle is a reasonable differentiator at full size.** At 10% thumbnail, both read as "big head, normal body." The differentiator is in the crown geometry — which is the region with least pixel density at small scale. Not a failure, but a fragile pass.
- **Body tilt on DETERMINED is forward with good commitment** — the lean implies next action (movement toward goal). This is correct pose construction. Note it as the sheet's strongest moment.

**Bottom line:** The spec fix was necessary and delivered correctly; the silhouette gaps in SKEPTICAL are the only remaining structural issue and they are not new.

---

## 4. Luma Motion Spec — LTG_CHAR_luma_motion.png

**Score: 61/100**

- **Panel 1 SPRINT ANTICIPATION — body_tilt=-10 with lean_forward=-12: these two parameters compound incorrectly.** In the code, lean_forward shifts body_cx by -12px (forward/left) and body_tilt at -10° adds a tilt_offset that also moves the body top leftward. The result is a figure whose center of gravity is shifted 22-25px forward of the feet. At the figure scale (leg_h = int(head_r * 1.1) ≈ 26px), this puts the center of mass well outside the support polygon. The character would fall. An anticipation pose should shift weight toward the edge of balance — not past it. Reduce combined forward displacement to 12-14px maximum.
- **Panel 1 — Hair annotated as "-12° pre-lean (NOT yet trailing)"** is contradicted by the code. `hair_trail_angle=-12` is applied directly to the hair mass shift in `draw_luma_figure()`. The hair IS already at -12°. If the annotation says "not yet trailing" the trail angle should be 0-3° (barely moved). The spec annotation and the drawn position disagree. This will instruct animators incorrectly.
- **Panel 2 DISCOVERY — Beat A and Beat B share identical foot placement.** Both poses use leg_left_spread=0, leg_right_spread=0. A recoil (Beat A: whole body jerks back) requires the feet to shift or widen as the body absorbs the recoil impulse. A lean-in (Beat B) requires the forward foot to take more weight. Identical feet across a two-beat reaction reads as a character reacting from the neck up only. No ground contact logic.
- **Panel 3 LANDING/STOP — hoodie_flare=+8px and hair trail_angle=+18° are correctly specified as secondary motion.** The timing cascade (body stops beat 1, hoodie peaks beat 1.5, hair peaks beat 2) is physically grounded and correct procedure. This is the spec sheet's strongest section.
- **Arm-to-shoulder connection is a stub throughout.** All arm lines originate from `body_cx ± int(body_w * 0.40)` — a point on the body side, with no shoulder mass rendered. Arms move without shoulder involvement. This is the most fundamental violation of weight physics I will not accept. Every arm movement must be preceded by shoulder engagement.

**Bottom line:** The timing cascade is right; the weight logic in the body (over-lean, unresponsive feet, shoulderless arms) makes these poses instructionally incorrect for any animator who draws literally from the spec.

---

## 5. Byte Motion Spec — LTG_CHAR_byte_motion.png

**Score: 70/100**

- **Panel 0 HOVER — 0.5Hz ±6px float spec is precise and physically grounded.** A 6px oscillation at the rendered scale reads as a genuine hovering quality — perceptible without being mechanical. The floating gap marker below the legs (cyan line showing ground clearance) is smart annotation.
- **Panel 1 SURPRISE — squash 3f/stretch 2f is correct squash-stretch timing asymmetry.** Impact is faster than recovery. Physically accurate and production-usable. The alarmed arm configuration (arms wide+up) is readable and differentiated from the float pose.
- **Panel 2 APPROACH — tilt direction convention is ambiguous.** tilt_deg=−22° shifts body top toward viewer-left. The annotation says "approach" but does not specify what Byte is approaching or in what screen direction. For a spec that instructs animators, the tilt direction must reference the target. "−22° lean toward target" requires knowing where the target is. Either add a target marker or make the convention explicit: "positive tilt = toward target."
- **Panel 2 — glow_radius=60, glow_alpha=80 at approach: the glow is the largest visual element in the panel.** At the character scale (bw=30, bh=38), a 60px radius glow doubles the visual footprint. This overwhelms the pose itself. Animators reading this spec will over-apply the glow effect because the spec suggests it should dominate. Reduce to glow_radius=35, glow_alpha=50 — present but not the primary read.
- **Crack scar on Byte's body is placed at body LEFT (viewer right: cx - int(actual_bw * 0.55)).** Byte's cracked eye is on viewer LEFT per glyph spec. The scar should echo the crack-side. Currently the scar is on the opposite side from the cracked eye — they disagree on which side carries Byte's damage history.

**Bottom line:** Byte's motion spec is the strongest of the two — the hover and squash-stretch are production-usable; fix the tilt convention, the scar placement, and the glow dominance.

---

## 6. Established Assets — Fresh Eye Review

**Luma Expression Sheet v009 / v010 series (standing review):**
At 37 cycles, the expression sheet has refined the face to a technically correct specification. What it has not resolved: the RECKLESS/DETERMINED expression's action line. The body tilt is present but the weight distribution across the feet is never annotated. An animator drawing from this spec can produce the tilted body without knowing where the weight is. Add a center-of-gravity vertical drop line to the DETERMINED and RECKLESS expressions — one line, through the torso, showing where gravity falls relative to the foot polygon.

**Character lineup v007 (standing review):**
The scale relationships between Luma, Cosmo, Byte, Miri are clear. The concern that has accumulated across cycles: none of the lineup figures are in poses with physical commitment. They stand in presentation posture. After 37 cycles, the lineup should show each character in their most CHARACTERISTIC action — Luma mid-lean, Cosmo examining something with his notebook, Byte hovering with visible pixel trail. A lineup of people standing side-by-side is a height chart, not a character introduction.

**Bottom line for established assets:** The detail work is sound; what is missing is physical life in the pose choices that frame everything else.

---

*Takeshi Mori — Critique Cycle 15 — 2026-03-30*
*"An animator who draws from your spec literally will produce exactly what you drew. Draw the right thing."*
