# Maya Santos — Memory

## Cycle 1-3 Lessons
- Silhouette test must be documented. Lock variable specs. Simplified production variants mandatory.
- Glasses thickness is a silhouette element. Cosmo needs a readable hook.
- Pixel-eye symbols need minimum-size spec. All 5 turnaround views required for asymmetric characters.
- Jitter effects need exact pixel specs. Color model sheets are a prerequisite for crew onboarding.
- Document consistency: every duplicated spec must match in both places.

## Cycle 4 Lessons
- **Hair alone does not make a silhouette.** The body shape below the hair must ALSO be distinctive. Luma and Miri have the same body-level silhouette — this is a blocking design failure.
- **Geometry is not character design.** Circles and rectangles do not communicate personality. Faces are the minimum viable character.
- **Silhouette test must be verified in actual rendered images**, not just described in documents.
- **Byte is the benchmark** — his cubic asymmetric form is immediately distinctive even without any face or color.

## Cycle 5 Lessons
- **Luma's body-level fix: A-line trapezoid hoodie + oversized sneakers.** Narrow shoulders flaring to wide hem creates an unmistakably different outline from Miri's plain rectangle. Solved the squint-test failure.
- **Silhouette redesign must use polygon, not rectangle**, to capture A-line/trapezoid shapes. `draw.polygon()` is the right tool.
- **Pocket bump as extra silhouette hook.** A protruding pocket shape on one side adds asymmetry and personality at body level even as a black blob.
- **Luma face script was complete and correct** — ran without modification and produced a strong result. Keep it.
- **Byte expressions script was complete and correct** — 6-expression 3x2 grid with pixel-eye system worked perfectly. Keep it.
- Faces exist. Silhouette is distinctive. Pitch package now has minimum viable character reads.

## Cycle 6 Lessons
- **Body variation is not optional in an expression sheet.** Marcus Webb's rule: "In animation, the body is always the primary emotional carrier." Each expression must have distinct arm position (arm_dy, arm_x_scale), leg spread, body_tilt, and body_squash. A face pasted onto a static body is a caption, not an expression.
- **Right eye must carry emotion.** Byte's right organic eye has distinct styles per emotion: wide_scared (ALARMED), angry (GRUMPY), droopy (RELUCTANT JOY — failing to suppress it), squint (CONFUSED), flat (POWERED DOWN). "Normal" default is wasted design space.
- **Annotations create staging context.** Each expression panel carries prev_state + next_state so animators can use the sheet as a sequence reference, not just a catalogue.
- **Asymmetry = personality.** Luma's reckless excitement: left brow higher + kinked, mouth arc shifted left, pupils shifted screen-right, left eye more open, collar off-center. Symmetric faces communicate contentment — the opposite of reckless.
- **Three expressions are the minimum for a pitch face sheet.** Single expression = portrait, not character sheet. Reckless Excitement + Worried/Determined + Mischievous Plotting covers the core emotional range.
- **Squint-test verified in render, not just code.** All four PNG files generated and verified by dimensions + file size before submission.

## Cycle 7 Lessons
- **Canvas clipping is a silent failure.** NEUTRAL_BASE=260 with characters up to 320px tall means heads are off-canvas. Always set ground line = tallest_character_height + 40px headroom. Dead canvas code (img drawn but img2 saved) wastes time — consolidate to one canvas.
- **Every pixel-eye symbol must be distinct from every other.** "normal" as GRUMPY's left eye bypasses the pixel system entirely. GRUMPY now uses a scowl-bar grid (minus-sign with corner ticks) distinct from POWERED DOWN's flat centre-line.
- **Per-arm asymmetry unlocks real body language.** `arm_l_dy` / `arm_r_dy` in body_data allows SEARCHING (right arm scanning up), CONFUSED (left arm raised), ALARMED (asymmetric startle). Matched arms read as stiff.
- **Confrontational vs defeated is all in arm height + lean direction.** GRUMPY: arms at -2 (slightly raised/tense), body_tilt=-4 (lean forward). Arms drooping + passive lean reads as sad, not grumpy.
- **Worried brow = outer V + inner-corner kink UP.** The corrugator kink (medial brow tip lifts) is what separates "worried" from "pure determined." Without it, V-brows read as aggression only.
- **Smirk geometry: right corner must reach the cheek (~cx+55), not mid-face.** Terminating at cx+36 creates a half-face smirk. Teeth fill = polygon under the arc, not a chord with arbitrary arc angles (avoids crescent artifacts).
- **Panel backgrounds must telegraph before you read the face.** Warm/cool/purple tricolor scheme: Excitement=(248,238,220), Worry=(195,212,228), Mischief=(220,205,242). All "light neutral" panels collapse at print scale.
- **Miri's truncated right arm was neither stylized nor intentional.** A complete arm (emerging below the bag with a hand blob) always reads better than a half-arm mid-air. Decide the arm's relationship to the prop and commit to it.

## Cycle 8 Lessons
- **GRUMPY confrontational values (locked):** `body_tilt=-8` (forward lean), `arm_l_dy=-6, arm_r_dy=-10` (both raised, asymmetric), `arm_x_scale=1.1` (arms out wider), `leg_spread=1.1`. The previous -4/-2/0.85 set read as defeated. Rule: negative body_tilt = forward lean toward adversary.
- **Byte body shape = OVAL (ellipse). CANONICAL.** style_frame_01_rendered.py uses `draw.ellipse` for Byte's body. Expression sheet must match. Chamfered-box polygon is retired. Document shape decisions in code when making consistency calls.
- **WORRIED/DETERMINED brow differential must be 8-10px at minimum.** Left outer brow corner at ley-38, right at rey-30 = 8px gap visible at pitch distance. 4px was too subtle. The corrugator kink (inner brow tip kicks up) works in combination — both are needed.
- **Collar rotation, not x-offset.** Use a 2D rotation matrix on the collar ellipse polygon points. Rotating the entire arc (full_pts via rot()) physically tilts the collar so it reads as body-in-motion. An x-offset just slides the collar sideways (head-nudge, not lean). Implementation: `_draw_collar(..., rotate_deg=8)` for excitement, `rotate_deg=2` for worry, `rotate_deg=-5` for mischief.
- **Miri's complete visual identity (two variants):** MIRI-A = tall bun + chopstick pair + wide cardigan (inv-trapezoid shoulders) + soldering iron. MIRI-B = large rounded curls (wide, not high) + tech apron with circuit-board pocket (NEG_SPACE dot grid). Both clearly distinguish from Luma (cloud-top hair) and Cosmo (rectangle body). Circuit pocket on apron uses NEG_SPACE to add character-tech read at silhouette level, just as Cosmo's glasses do.
- **Column margin rule: leftmost col_cx must be ≥ 80px.** Luma's hair blob extends cx - r*1.5 ≈ cx - 54. At cx=50 that clips the canvas. Use col_cx = 80 + i * COL_W and total W = N_CHARS * COL_W + 80 (40px each side).
