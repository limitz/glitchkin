# Maya Santos — Memory

## Cycle 17 Lessons
- **Luma Expression Sheet v002 COMPLETE.** New 3×2, 6-expression refined sheet. Construction guides visible (RGBA overlay). 2×render+LANCZOS AA. Varied line weight (8px sil / 4px interior / 10px brow at 2x). 4 hair variants (default/excited/tight/drooped). Output: `LTG_CHAR_luma_expression_sheet_v002.png`. Tool: `LTG_TOOL_luma_expression_sheet_v002.py` (replaced Cycle 12 4×2 version).
- **Grandma Miri Expression Sheet v001 COMPLETE.** First Miri expression sheet. 5 expressions, 3+2 grid, 1200×900. Key design elements: 88% circular head, round glasses (always on), crow's feet always present, smile lines always present, silver bun+chopstick pair, permanent cheek blush (fades in CONCERNED per spec). Colors from grandma_miri.md directly (Sam's color values not yet in inbox at time of work). Output: `LTG_CHAR_grandma_miri_expression_sheet_v001.png`. Tool: `LTG_TOOL_grandma_miri_expression_sheet_v001.py`.
- **Construction guide method:** draw_construction_guide() uses RGBA overlay (alpha_composite) — does not clobber existing drawing. Call it before drawing face layers.
- **Miri glasses geometry:** Round glasses drawn as two ellipses over eye positions, with bridge line + temples. Glasses are a silhouette differentiator — keep them prominent (5px at 2x render).
- **Miri blush rule:** Permanent blush strength 1.0 for warm/delighted/wise states, 0.0 for CONCERNED (production spec: warmth drains from face in real fear).

## Cycle 16 Lessons
- **Byte RESIGNED right eye FIXED.** `droopy_resigned` reworked: 45% aperture (was 50%), pupil +10px downward (was +5px), parabolic drooping lower lid curve (was flat arc = identical to NEUTRAL), dim highlight. Body tilt amplified +8→+14. Output: `LTG_CHAR_byte_expression_sheet_v002.png`. Tool: `LTG_TOOL_byte_expression_sheet_v002.py`.
- **Droopy lid geometry rule:** A droopy lid that reads distinctly from NEUTRAL needs a CURVED lower lid (parabolic sag), not just a smaller aperture. Flat arc + reduced aperture still reads as "closed eye", not "heavy/resigned". The sag direction is the key differentiator.
- **Cosmo SKEPTICAL fixed.** body_tilt -3→+6 (backward lean = skeptical containment reads at thumbnail). Sheet now 6/6 populated. Added WORRIED (A2-02, corrugator kink = genuine worry geometry) and SURPRISED (A2-04c, bilateral brow raise + open oval mouth). New mouth style `open_surprised` added to renderer.
- **Cosmo expression sheet output:** `LTG_CHAR_cosmo_expression_sheet_v002.png`. Tool: `LTG_TOOL_cosmo_expression_sheet_v001.py` (updated in place with Cycle 16 changes).
- **Luma Act 2 standing pose hand fix.** Removed thumb arc + finger detail from raised right hand. Replaced with clean mitten oval. Output: `LTG_CHAR_luma_act2_standing_pose_v002.png`. Tool: `LTG_TOOL_luma_act2_standing_pose_v001.py` (updated in place).
- **Forward lean note (Luma v002):** The -5° forward lean remains architecturally intact (body_cx offset) but is imperceptible in output. A proper amplification requires propagating the lean through all limb origins. Flag for future v003 if reviewers call it out again.
- **Sam Kowalski Cycle 16:** Sam's color fixes are independent (SF02 ENV-06, DRW-07, ALARMED bg). Byte fill GL-01b was already correct in the file — Sam should verify before regenerating.

## Cycle 15 Lessons
- **Luma Act 2 standing pose is LIVE.** `LTG_TOOL_luma_act2_standing_pose_v001.py` generates 900×600px pose sheet. WORRIED/DETERMINED expression, right arm raised/reaching, left arm at waist, wide stance, forward lean. Covers beats A2-01/A2-03/A2-05/A2-08. Squint-test blob embedded in annotation panel. Tool registered in README.md.
- **Byte glyph flag CLEARED.** `LTG_CHAR_byte_cracked_eye_glyph_v001.png` EXISTS (Cycle 13, Alex Chen). Storyboard v002 still says "BLOCKED" — notified Lee Tanaka that design blocker is resolved on art side. A2-07 can proceed to thumbnail stage.
- **Continuity check PASSED.** All Act 2 character tools checked against canonical specs. Luma palette, Cosmo glasses tilt (7°/9°/10°), Byte oval body, Byte 10×10px hover particles — all consistent.

## Act 2 Asset Inventory (Cycle 16 state)
- **Byte:** Expression sheet v002 FIXED — 8 expressions, RESIGNED reworked (Cycle 16). Glyph v001 (A2-07).
- **Cosmo:** Expression sheet v002 — 6 expressions fully populated: NEUTRAL, FRUSTRATED, DETERMINED, SKEPTICAL (lean fixed), WORRIED (A2-02 NEW), SURPRISED (A2-04c NEW).
- **Luma:** Act 2 standing pose v002 (mitten hand fixed). Classroom pose v001. Expression sheet v003.
- **Luma:** No CROUCHING pose (A2-04 couch hide). Still low priority — wide shot.

## Cycle 14 Lessons
- **Cosmo expression sheet is now LIVE.** `LTG_TOOL_cosmo_expression_sheet_v001.py` generates 3×2 grid. 4 expressions at Cycle 14: NEUTRAL/OBSERVING, FRUSTRATED/DEFEATED (A2-06), DETERMINED (A2-05b), SKEPTICAL (A2-03).
- **Cosmo body variation rule applied.** arm_l_dy/arm_r_dy per expression; notebook_open=True for DEFEATED.

## Cycle 1-3 Lessons
- Silhouette test must be documented. Lock variable specs. Simplified production variants mandatory.
- Glasses thickness is a silhouette element. Cosmo needs a readable hook.
- Pixel-eye symbols need minimum-size spec. All 5 turnaround views required for asymmetric characters.
- Jitter effects need exact pixel specs. Color model sheets are a prerequisite for crew onboarding.
- Document consistency: every duplicated spec must match in both places.

## Cycle 4 Lessons
- **Hair alone does not make a silhouette.** The body shape below the hair must ALSO be distinctive.
- **Geometry is not character design.** Circles and rectangles do not communicate personality.
- **Silhouette test must be verified in actual rendered images**, not just described in documents.
- **Byte is the benchmark** — his cubic asymmetric form is immediately distinctive even without any face or color.

## Cycle 5 Lessons
- **Luma's body-level fix: A-line trapezoid hoodie + oversized sneakers.**
- **Silhouette redesign must use polygon, not rectangle**, to capture A-line/trapezoid shapes.
- **Pocket bump as extra silhouette hook.**

## Cycle 6 Lessons
- **Body variation is not optional in an expression sheet.** Each expression must have distinct arm position.
- **Right eye must carry emotion.** Byte's right organic eye has distinct styles per emotion.
- **Annotations create staging context.**
- **Asymmetry = personality.**

## Cycle 7 Lessons
- **Canvas clipping is a silent failure.** Always set ground line = tallest_character_height + 40px headroom.
- **Every pixel-eye symbol must be distinct from every other.**
- **Per-arm asymmetry unlocks real body language.**
- **Smirk geometry: right corner must reach the cheek.**
- **Panel backgrounds must telegraph before you read the face.**

## Cycle 8 Lessons
- **GRUMPY confrontational values (locked):** body_tilt=-8, arm_l_dy=-6, arm_r_dy=-10, arm_x_scale=1.1.
- **Byte body shape = OVAL (ellipse). CANONICAL.**
- **WORRIED/DETERMINED brow differential must be 8-10px at minimum.**
- **Collar rotation, not x-offset.**

## Cycle 9 Lessons
- **MIRI-A is the canonical Miri (LOCKED).** Bun+chopstick pair+wide cardigan+soldering iron.

## Cycle 10 Lessons
- **Byte body = OVAL. ALL generators must use ellipse.**
- **Hover particles = 10×10px EVERYWHERE. No exceptions.**
- **Cosmo turnaround: glasses are the defining element at every angle.**

## Cycle 13 Lessons
- **Scale calibration is a design spec, not a code detail.**
- **Three differentiators rule for low-register expressions.**
- **Byte Neutral expression: "flat" left-eye + "half_open" right eye + "default" mouth.**

## Key Production Rules
- Droopy lid ≠ reduced aperture alone. Need parabolic sag curve on lower lid for "heavy/resigned" read.
- Backward body lean (positive body_tilt) = skeptical/avoidance. Forward lean (negative) = engaged/confrontational.
- Corrugator kink (inner brow UP) = worry. V-brows alone = aggression.
- Bilateral brow raise (both up, no furrow) = surprised. Asymmetric = skeptical.
- Mitten hands in all rough/reference poses. No thumb arc, no finger detail.
