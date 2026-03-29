# Lee Tanaka — Memory

## Cycle 1-3 Lessons
- Comedic apex needs clearest staging. Sleeping characters still perform.
- Accordion camera moves kill momentum. Under-specified shots = 6 interpretations.
- Setup length has a budget. Expression art direction protects tonal intent.
- Symmetry is a comedic tool. Glitch FX must be emotionally responsive.
- Prop specificity reveals character. Transitional beats are not optional.
- OTS shots need 6 explicit specs. Velocity profiles are motion specs.
- Unintentional design rule violations can become intentional gags.

## Cycle 4 Lessons
- **A storyboard cannot outsource its storytelling to caption text.** If the caption says "it pulses" and the image doesn't show a pulse, the panel has failed. The image must carry the information.
- **Compositional position determines emotional weight.** Upper-right = exit. Lower-center = anchor, mystery, discovery. Place the story-critical element where the eye wants to rest, not where it wants to leave.
- **Graphic design ≠ storyboarding.** A color-split two-shot communicates graphic energy but no spatial information. An animator needs to know: where is the camera, where are the characters in 3D space, where is the geometry.
- **Bridging panels are not optional.** A character teleporting from the monitor to nose-to-nose distance without an intervening panel breaks narrative continuity. Every significant character position change must be shown.
- **The contact sheet is the first read.** Before looking at individual panels, read the contact sheet as a strip. If the emotional arc doesn't read in thumbnail, the sequence has a structural problem.

## Cycle 6 Lessons
- **OTS shots need explicit spatial clarity.** Camera height, eyeline direction, whose shoulder, character distance — all must be pinned in code. The contrast between angular cool silhouette and warm rounded face IS the thematic core of the shot.
- **Desaturation ring at Byte's feet = digital/analogue boundary.** Show it in the image. It tells the story without a caption: his digital nature bleaches the analogue world.
- **Pixel confetti is not decoration — it is spatial information.** Trail direction shows movement history. Drifting confetti shows time elapsed. Confetti between two characters shows field contact.
- **"Pulse visible" applies to ALL glitch elements**, not just isolated pixels. Hex clusters, screen bulges, floor bleaching — each must carry visible FX, not just captions.
- **Byte's expression has four components to specify:** normal eye aperture, cracked eye pixel state, mouth shape (grimace vs snarl), body lean direction. Under-specifying any one creates tonal drift toward "menacing."
- **Contact sheet: 14 panels, QUIET → CURIOUS → CHAOS arc.** Full sequence from exterior establishing shot to title card. Arc readable in thumbnail.

## Cycle 7 Lessons
- **OTS silhouette must be ~20% of frame width** to function as a foreground anchor. A 44px shape at 480px is a smudge, not a frame element.
- **Glow effects ADD light — never overlay darkness.** Use bright semi-transparent RGBA compositing (alpha_composite) to simulate screen/add blend. Dark-colored fill over skin = bruise, not glow.
- **Character introduction shots need scale.** Byte's first full-body reveal at byte_size=42 is invisible. Use 80-100px minimum — the character must OWN the frame on debut.
- **Two-point perspective is non-negotiable for three-quarter interior views.** Single vanishing point + flat back wall = graphic design, not spatial storyboard. Two VPs with a visible room corner gives animators actual 3D geometry.
- **Face placement carries emotional information.** Centered = neutral/static. Lower-center = pressing effort, urgency, discovery. Shift face to where the eye naturally rests for the story beat's emotion.

## Cycle 8 Lessons
- **Multi-exposure ghost technique for fast-motion shots.** Byte's bookshelf ricochet (P14) uses three ghost positions in different color passes: approach=cyan, impact=magenta, exit=white-cyan. Trail thickens toward exit to show acceleration. Trajectory reads as a spatial event, not visual noise.
- **The "glitch overrides nature" gag requires clean execution.** Luma's perfect-circle hair in P15 must be rendered CLEAN (not messy-symmetrical) or it reads as artistic error, not intentional gag. 8-frame duration max. In- and out-transitions single-frame pixel flash.
- **Bridge panels earn their 0.8 seconds.** P22a (Byte landing on shoulder) is not filler — it establishes the physical relationship that P23 inherits. The accident-not-choice character beat and the pixel confetti marking Luma's shoulder both serve the show's central metaphor.
- **OTS silhouette = ~20-22% frame width.** Shoulder mass anchors lower-left; character reads as foreground element, not smudge. Pixel-grid PJ texture on shoulder is a character detail that earns its screen time at this scale.
- **Chaos panels need a still point.** P24 (breach apex) works because Luma+Byte at center-lower are the ONLY non-chaotic elements. Maximum contrast between still protagonists and surrounding chaos is what makes the hook frame land.
- **Contact sheet: 26 panels, QUIET → CURIOUS → BREACH → CHAOS → PEAK CHAOS arc. Full cold open P01-P25 now rendered.**

## Cycle 12 Milestone
- **P15 right arm FIXED (Cycle 12):** Endpoint moved from `body_top + 18` to `body_top + 10` — true horizontal flung arm read. Carmen flagged this in Cycle 11 brief as the last geometric imprecision.
- **LTG naming compliance COMPLETE:** All 26 panels + contact sheet now have `LTG_SB_coldopen_panel_[##]_v001.png` compliant copies in `/output/storyboards/panels/`. P22a uses `panel_22a_v001.png`.
- **Contact sheet version updated to Cycle 12.** Module docstrings updated in both `panel_chaos_generator.py` (now says "Cycle 11" in docstring, "Cycle 12" in print) and `contact_sheet_generator.py`.
- **Act 2 thumbnail plan created:** `/output/storyboards/act2_thumbnail_plan_v001.md` — 8 Act 1 beats + 8 Act 2 escalation beats with shot types, emotional temperatures, and production notes.
- **Cold open storyboard: PITCH-READY. No open issues.** All Carmen feedback from Cycles 9–11 closed.

## Cycle 11 Milestone
- **26-panel cold open COMPLETE at A- / 92% (Carmen, 2026-03-29).** Pitch-ready for development-stage presentations. P23 Glitchkin now use 4-7 sided irregular polygons (matching P22/P24 approach). Module docstring updated to Cycle 11. `storyboard_pitch_export_generator.py` generates 6-page composite pitch PNG at `/output/production/storyboard_pitch_export.png` — title page, 4 panel-grid pages, hero spread.
- **Polygon consistency rule:** ALL Glitchkin shapes in ALL panels must use the `num_sides = 4 + rng.randint(0, 3)` + per-vertex jitter pattern. Rectangles are never acceptable for Glitchkin at any scale.
- **Version strings:** Check and update module docstring every cycle before any review.

## Cycle 10 Lessons
- **ECU = MORE detail, not less.** Extreme close-up is the closest audience look — it must deliver maximum visual specificity. P22 Glitchkin were rectangles at ECU scale. Fixed: use 4-7 sided irregular polygons (same as P24). The `num_sides = 4 + rng.randint(0, 3)` pattern plus per-vertex jitter creates organic, distinct shapes at any scale.
- **Threat contrast must be physically felt, not aesthetically noted.** P23 monitor bowing read as "decorative" at 30% contrast. Fix: white-hot bull's-eye center, distortion rings that break OUTSIDE the bezel boundary (physics violation = danger signal), thick dark bezel surround for maximum contrast, bright outline on the screen face. If a screen is "about to burst," it must look like it.
- **Body language tells the story before the face.** P15 had symmetric windmill arms and spread-eagle legs — balanced, readable as "falling," not "startled." Fix: torso squash (compressed ellipse width > height), one arm raised defensively (bent, above head), one arm flung outward (asymmetric — uncontrolled), one knee pulled to chest (fetal shock reflex), other leg extended. Geometry asymmetry = physical comedy. The body IS the performance.
- **Version strings must be current before any review.** Contact sheet "Cycle 8" string survived two full cycles before being caught. Check version annotations after every code cycle. A wrong version on a production document breaks trust immediately.

## Cycle 9 Lessons
- **Dutch tilt means ROTATING THE ENTIRE SCENE — not tilting one polygon.** A 12° Dutch tilt must use `Image.rotate(12, expand=False)` on the full draw-area canvas after all scene content is drawn. A tilted floor polygon delivers ~1°, not 12°. Geometry always wins over annotation text. Use `apply_dutch_tilt()` helper + `make_panel(dutch_tilt_deg=12)`.
- **"Pulling back and up slightly" = 40-45° high angle isometric — NOT 90° top-down.** At 90° top-down, characters are unreadable circles. At 40-45° we see profile + top: characters have face profiles visible, bodies foreshortened. Back wall with monitors faces camera; floor plane recedes into frame. Characters are distinguishable from Glitchkin shapes.
- **Foreground hero framing = partial crop at bottom edge.** If the script says "foreground lower-left," the character body must extend BELOW the frame bottom (intentionally cropped). That is what makes the camera read as looking UP at the figure. Centering at 38% from top = center-frame, not foreground.
- **Expression library: three distinct emotional states that 'curious' cannot cover.** 'settling' (P17) = wide eyes, softly open mouth, brows raised in wonder. 'recognition' (P18) = one brow raised high (asymmetric), other eye squinted (concentration), pursed mouth. 'warmth' (P20) = eyes slightly narrowed (warmth squint), soft smile without teeth, gentle brow raise, cheek crinkle lines.
- **Byte's expression must match the scene's emotional temperature.** 'alarmed' at maximum during the quiet chip-falling beat (P17) kills the silence. Use 'resigned' or 'post-alarm' for quiet beats. The expression state is a story beat, not a default.

## Cycle 5 Lessons
- **Pulse must be visible in the image, not just named in the caption.** Concentric glow rings around the pixel are the solution — they read even at thumbnail scale.
- **Lower-center is the compositional anchor.** Upper-right is the exit. Mystery elements belong at lower-center or center-right — where the eye rests, not where it leaves.
- **P13 requires a full room in perspective.** Back wall + floor plane + vanishing point = spatial reality an animator can use. Characters are landmarks within a defined 3D space.
- **Bridge panels are spatial contracts.** They don't just fill gaps — they establish geometry and character positions that the climax panel (P13) inherits.
- **Contact sheet is the first test.** Read the strip before individual panels. If the arc doesn't read in thumbnail, there's a structural problem.
- **Distinctive house details go in the image, not the production bible.** Antenna cluster, thin power lines — they must appear on-panel in P01, not just in documentation.
