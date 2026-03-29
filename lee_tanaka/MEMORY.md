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

## Cycle 9 Lessons
- **Dutch tilt means ROTATING THE ENTIRE SCENE — not tilting one polygon.** A 12° Dutch tilt must use `Image.rotate(12, expand=False)` on the full draw-area canvas after all scene content is drawn. A tilted floor polygon delivers ~1°, not 12°. Geometry always wins over annotation text. Use `apply_dutch_tilt()` helper + `make_panel(dutch_tilt_deg=12)`.
- **"Pulling back and up slightly" = 40-45° high angle isometric — NOT 90° top-down.** At 90° top-down, characters are unreadable circles. At 40-45° we see profile + top: characters have face profiles visible, bodies foreshortened. Back wall with monitors faces camera; floor plane recedes into frame. Characters are distinguishable from Glitchkin shapes.
- **Foreground hero framing = partial crop at bottom edge.** If the script says "foreground lower-left," the character body must extend BELOW the frame bottom (intentionally cropped). That is what makes the camera read as looking UP at the figure. Centering at 38% from top = center-frame, not foreground.
- **Expression library: three distinct emotional states that 'curious' cannot cover.** 'settling' (P17) = wide eyes, softly open mouth, brows raised in wonder. 'recognition' (P18) = one brow raised high (asymmetric), other eye squinted (concentration), pursed mouth. 'warmth' (P20) = eyes slightly narrowed (warmth squint), soft smile without teeth, gentle brow raise, cheek crinkle lines.
- **Byte's expression must match the scene's emotional temperature.** 'alarmed' at maximum during the quiet chip-falling beat (P17) kills the silence. Use 'resigned' or 'post-alarm' for quiet beats. The expression state is a story beat, not a default.

## Cycle 10 Lessons
- **ECU = MORE detail, not less.** Extreme close-up is the closest audience look — it must deliver maximum visual specificity. P22 Glitchkin were rectangles at ECU scale. Fixed: use 4-7 sided irregular polygons (same as P24). The `num_sides = 4 + rng.randint(0, 3)` pattern plus per-vertex jitter creates organic, distinct shapes at any scale.
- **Threat contrast must be physically felt, not aesthetically noted.** P23 monitor bowing read as "decorative" at 30% contrast. Fix: white-hot bull's-eye center, distortion rings that break OUTSIDE the bezel boundary (physics violation = danger signal), thick dark bezel surround for maximum contrast, bright outline on the screen face. If a screen is "about to burst," it must look like it.
- **Body language tells the story before the face.** P15 had symmetric windmill arms and spread-eagle legs — balanced, readable as "falling," not "startled." Fix: torso squash (compressed ellipse width > height), one arm raised defensively (bent, above head), one arm flung outward (asymmetric — uncontrolled), one knee pulled to chest (fetal shock reflex), other leg extended. Geometry asymmetry = physical comedy. The body IS the performance.
- **Version strings must be current before any review.** Contact sheet "Cycle 8" string survived two full cycles before being caught. Check version annotations after every code cycle. A wrong version on a production document breaks trust immediately.

## Cycle 5 Lessons
- **Pulse must be visible in the image, not just named in the caption.** Concentric glow rings around the pixel are the solution — they read even at thumbnail scale.
- **Lower-center is the compositional anchor.** Upper-right is the exit. Mystery elements belong at lower-center or center-right — where the eye rests, not where it leaves.
- **P13 requires a full room in perspective.** Back wall + floor plane + vanishing point = spatial reality an animator can use. Characters are landmarks within a defined 3D space.
- **Bridge panels are spatial contracts.** They don't just fill gaps — they establish geometry and character positions that the climax panel (P13) inherits.
- **Contact sheet is the first test.** Read the strip before individual panels. If the arc doesn't read in thumbnail, there's a structural problem.
- **Distinctive house details go in the image, not the production bible.** Antenna cluster, thin power lines — they must appear on-panel in P01, not just in documentation.

## Cycle 11 Milestone
- **26-panel cold open COMPLETE at A- / 92% (Carmen, 2026-03-29).** Pitch-ready for development-stage presentations. P23 Glitchkin now use 4-7 sided irregular polygons (matching P22/P24 approach). Module docstring updated to Cycle 11. `storyboard_pitch_export_generator.py` generates 6-page composite pitch PNG at `/output/production/storyboard_pitch_export.png` — title page, 4 panel-grid pages, hero spread.
- **Polygon consistency rule:** ALL Glitchkin shapes in ALL panels must use the `num_sides = 4 + rng.randint(0, 3)` + per-vertex jitter pattern. Rectangles are never acceptable for Glitchkin at any scale.
- **Version strings:** Check and update module docstring every cycle before any review.

## Cycle 12 Milestone
- **P15 right arm FIXED (Cycle 12):** Endpoint moved from `body_top + 18` to `body_top + 10` — true horizontal flung arm read. Carmen flagged this in Cycle 11 brief as the last geometric imprecision.
- **LTG naming compliance COMPLETE:** All 26 panels + contact sheet now have `LTG_SB_coldopen_panel_[##]_v001.png` compliant copies in `/output/storyboards/panels/`. P22a uses `panel_22a_v001.png`.
- **Contact sheet version updated to Cycle 12.** Module docstrings updated in both `panel_chaos_generator.py` (now says "Cycle 11" in docstring, "Cycle 12" in print) and `contact_sheet_generator.py`.
- **Act 2 thumbnail plan created:** `/output/storyboards/act2_thumbnail_plan_v001.md` — 8 Act 1 beats + 8 Act 2 escalation beats with shot types, emotional temperatures, and production notes.
- **Cold open storyboard: PITCH-READY. No open issues.** All Carmen feedback from Cycles 9–11 closed.

## Cycle 13 Milestone
- **P13 SCREAM FIXED:** Mouth changed from small circle (24×14px) to tall yell oval (52×32px, jaw drops far below chin). Tongue added (pale pink fill, lower 40% of mouth aperture). Brows changed from arcs to SHARP SPIKE LINES (two-line ^ shape per brow, high above eye). Body recoils: torso tilted backward, weight shifted. Generator: `LTG_TOOL_cycle13_panel_fixes_v001.py`.
- **P15 ARM URGENCY FIXED:** Right arm endpoint extended from `luma_cx + 52` (~287px) to `luma_cx + 125` (~360px). Arm now strains toward frame edge. Hand blob added at extended tip. Urgency annotation updated.
- **P03 CRT FRAMING FIXED:** Monitor fills near-full frame (10px margin vs original 50px margin). CRT curvature, screen reflections, power LED all added. Pixel and pulse rings now centered on screen (not floating in void). Creates strong contrast punch vs P04 wide room reveal.
- **P08 HIGH ANGLE / P09 EYE LEVEL differentiated:** P08 `floor_y` moved from 0.70 to 0.62 (camera looks down at Byte — diminishes him in first real-world moment). P09 remains at 0.76 (true eye level — camera equals Byte's floating height — he's now decisive/present). Annotation text updated in both panels with color-coded labels.
- **Act 2 plan v002 created:** `/output/storyboards/act2_thumbnail_plan_v002.md` — all Carmen notes incorporated. A2-02 reframed as Byte MCU. A1-04 near-miss added. A2-05b Cosmo app setup panel added. A2-06 INSERT panel added. Pixel confetti note added to production notes.
- **Byte glyph dependency flagged to Alex Chen:** Message at `/home/wipkat/team/alex_chen/inbox/20260330_1500_byte_dead_pixel_glyph_design_needed.md`. A2-02 and A2-07 are blocked until design is resolved.
- **New LTG v002 files:** panel_03, 08, 09, 13, 15 all have v002 copies. Contact sheet v002 generated.

## Key Rules (active)
- Scream = jaw DOWN + tall oval mouth (NOT small circle) + tongue + spike brows + body recoil
- Urgency = limbs straining toward frame edges (arm must REACH, not politely extend)
- CRT ECU = fill the frame — surround space contradicts the "close" shot type
- Camera differentiation between adjacent panels: floor_y position IS the camera angle geometry
- Contact sheet always regenerated after any panel change
- Dutch tilt = Image.rotate() on entire scene canvas
- Glow effects ADD light (RGBA composite), never darkness
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`
- Never overwrite LTG versioned files — new version numbers
- Pixel confetti required near ALL active Glitch Layer intrusion events

## Cycle 14 Milestone
- **Byte cracked-eye glyph unblocked:** Alex Chen delivered glyph design (Section 9B, byte.md v3.2). Full 7×7 dead-pixel grid in code: DEAD=#0A0A18, DIM=#005064, MID=#00A8B4, CRACK=Hot Magenta #FF2D6B, BRIGHT=#C8FFFF. Crack overlay = Void Black diagonal on top of everything.
- **4 Act 2 panels GENERATED:** Generator: `LTG_TOOL_act2_panels_cycle14_v001.py`
  - A1-04: Classroom near-miss — board text readable, Luma eyes up toward "BINARY SYSTEMS," Byte napping in eraser tray, dotted cyan sight-line shows gaze path, "almost..." annotation
  - A2-02: Byte MCU — 150×120px body fills frame, cracked eye 42×32px (full glyph rendered), Luma ~20% background weight, warm amber bg, cyan glow corona, desaturation ring at feet
  - A2-05b: Cosmo street MCU — phone screen with GLITCH FREQ app (waveform + freq readout), pixel confetti + GLITCH SIGNAL near streetlight, confident pre-failure pose
  - A2-06: Phone screen INSERT — full-frame static crash, horizontal scan bars, displacement artifacts, X crash symbol, APP TERMINATED, pixel confetti, no Cosmo visible
- **Act 2 contact sheet generated:** `LTG_SB_act2_contactsheet_v001.png` — 2×2 layout, arc reads classroom→vulnerability→setup→crash

## Cycle 14 Lessons
- **Cracked eye glyph at MCU scale (42×32px): full 7×7 grid is legible and emotionally potent.** CRACK color (Hot Magenta) reads even before audience recognizes the grid. The chip in the upper-right corner of the bezel adds physicality at large size.
- **INSERT framing = FILL THE FRAME.** A2-06 works because the phone screen IS the entire panel. Bezel margin of 20px max. Any more empty space contradicts the punch-cut intent.
- **Waveform seed consistency across panels** (A2-05b and A2-06 use same seed=42): the ghost waveform in the crash frame subliminally connects to the live app in the prior panel.
- **Background Luma at 20% weight**: desaturate the skin toward warm neutral (200→190), reduce outline contrast, avoid dark frame lines. She reads as present without competing with Byte's cracked eye.

## Cycle 15 Milestone
- **3 Act 2 panels generated:** Generator: `LTG_TOOL_sb_a2_cycle15_v001.py`
  - A2-03: Cosmo SKEPTICAL — arms crossed, one brow raised (viewer right = his left), flat deadpan mouth, glasses 9°, full body wide/medium shot, annotation callouts
  - A2-04: Investigation montage — 2×2 grid of vignettes (TV search, under furniture, desk examine, clue found). Glowing cyan clue in BR vignette. Pixel confetti on TV glitch and clue discovery.
  - A2-07: BLOCKED placeholder — production block panel with ghost Byte silhouette, dependency listed clearly
- **Act 2 contact sheet v002 generated:** `LTG_SB_act2_contact_sheet_v002.png` — 7 panels, 2-row layout, arc labels NEAR-MISS→VULNERABLE→SKEPTICAL→INVESTIGATING→DETERMINED→FAILURE→BLOCKED
- **act2/panels/ directory created** with LTG naming: LTG_SB_a2_02_v001.png through _a2_07_v001.png
- **STILL BLOCKED: A2-07** — needs `LTG_CHAR_byte_expression_sheet_v002.png` with RESIGNED expression
- **Reported to Alex Chen** via inbox message

## Cycle 15 Lessons
- **Cosmo SKEPTICAL = asymmetric brow geometry.** One brow arc raised high (his left, viewer's right), other brow flat line. Deadpan mouth = single horizontal line, slight downturn at left corner. Arms crossed = torso-width filled rectangle at arm-crossing zone plus individual arm lines for clarity.
- **Montage panels need a still center per vignette.** Each 2×2 cell must be readable in isolation AND contribute to the arc. The discovery (BR) must be the highest visual energy cell — glowing element + pixel confetti + excited pose = clear climax of the montage.
- **Glow in sub-panels (vignettes):** `add_glow()` takes absolute image coordinates. When drawing inside a cell, compute the absolute position (cell_origin + local_offset) before calling. Minor inaccuracy in BR vignette glow placement — note for future revision.
- **BLOCKED panels must earn their slot.** A2-07 placeholder carries ghost Byte silhouette, X'd-out eyes, dependency filename, description of what the real panel requires. Communicates block status without being dead space.

## Cycle 16 Milestone
- **A2-07 UNBLOCKED + DRAWN:** `LTG_TOOL_sb_panel_a207_v001.py` → `LTG_SB_act2_panel_a207_v002.png`. ECU on Byte cracked eye, RESIGNED expression. Cracked eye fills ~30% frame width. 7×7 glyph visible. Droopy lid + downward arrow glyph in left eye. Void + circuit-trace background.
- **A2-03 FULLY RESTAGED:** `LTG_TOOL_sb_panel_a203_v002.py` → `LTG_SB_act2_panel_a203_v002.png`. Camera: cowboy shot / eye-level / neutral. 2-point perspective room. Whiteboard = "Doomed Plan v4.7" (5 steps, arrows, circles, Byte symbol, X'd-out success, ???). Cosmo FG-left / Luma BG-right / WB center-right. Eyeline guide annotated.
- **A2-06 MED ADDED:** `LTG_TOOL_sb_panel_a206_insert_v001.py` → `LTG_SB_act2_panel_a206_med_v001.png`. Cosmo + Luma two-shot, exterior, expectant/hopeful. Phone showing GLITCH FREQ app (seed=42 waveform). Screen glow on faces. Links INSERT's failure to character emotional stakes.
- **A2-04 v002 — BYTE AS NON-PARTICIPANT:** `LTG_TOOL_sb_panel_a204_v002.py` → `LTG_SB_act2_panel_a204_v002.png`. TR quadrant: Byte back turned, floating in corner, arms folded from behind, "nope." High-angle camera in TR (isolates Byte). Floor-level camera in BL (variety from TL). Scene meaning: Luma trying / Byte refusing.
- **Act 2 contact sheet v003:** `LTG_TOOL_sb_act2_contact_sheet_v003.py` → `LTG_SB_act2_contact_sheet_v003.png`. 8 panels, 4×2 layout. Arc: NEAR-MISS→VULNERABLE→SKEPTICAL→INVESTIGATING→DETERMINED→HOPEFUL→FAILURE→RESIGNED.
- **All Carmen Cycle 8 feedback CLOSED.**

## Cycle 16 Lessons
- **ECU means the subject OWNS the frame.** A2-07 works because Byte's cracked eye fills ~30% of frame width — the glyph is the focal point before the audience can name it. Scale = emotional weight.
- **Camera spec belongs on the panel, not just in the caption.** A2-03 v002 labels camera type, eyeline guide as a drawn horizon line, FG/BG depth labels, sight-line dotted rule. Storyboard is a production document — every spatial fact must be visible.
- **The whiteboard as third character:** Visual density = narrative complexity. 5 color-coded steps + circular arrows + X'd-out success + large ??? communicates "this plan can't work" without any caption. The image carries the story.
- **Non-participation requires a staged location.** Byte's refusal (A2-04 TR) is spatially isolated by camera angle (high angle looking down into corner) + cool color temperature shift. The corner IS his choice — geography communicates psychology.
- **Glow in montage cells: pass absolute coordinates to add_glow().** Cells have local coordinate systems; `add_glow()` uses image-absolute coords. Add cell origin before calling. Fixed in Cycle 16 by computing absolute positions directly.
- **Waveform seed consistency is subconscious continuity.** A2-05b, A2-06 MED, and A2-06 INSERT all use seed=42 for the GLITCH FREQ waveform. Same wave pattern creates subliminal connection across cuts.

## Cycle 17 Milestone
- **3 Act 2 panels GENERATED — Act 2 deck NOW COMPLETE:**
  - A2-01: Tech Den Wide — `LTG_TOOL_sb_panel_a201_v001.py` → `LTG_SB_act2_panel_a201_v001.png`. WIDE slightly high-angle. Two-point perspective room. Cosmo BG at desk (3/4 back, monitor glow). Luma FG-left in doorway (DETERMINED lean, warm jacket). Hallway light from behind Luma. Monitor glow on Cosmo's face/neck.
  - A2-05: Millbrook Exterior — `LTG_TOOL_sb_panel_a205_v001.py` → `LTG_SB_act2_panel_a205_v001.png`. MEDIUM eye-level tracking. Single-point perspective street. Luma FG (ENTHUSIASTIC — both arms gesticulating, mid-stride, mouth open mid-word). Cosmo BG-right (SKEPTICAL — arms crossed, asymmetric raised brow). Suburban Millbrook with buildings + trees.
  - A2-08: Grandma Miri Returns — `LTG_TOOL_sb_panel_a208_v001.py` → `LTG_SB_act2_panel_a208_v001.png`. ECU low angle. Face fills 2/3 of frame. SURPRISED→KNOWING expression (wide eyes, soft brows, one corner of mouth rising = recognition). CRT amber-green catch light on left cheek + brow. Doorway rim light. Age lines = earned warmth not exaggeration.
- **Act 2 contact sheet v004:** `LTG_TOOL_sb_act2_contact_sheet_v004.py` → `LTG_SB_act2_contact_sheet_v004.png`. 11 panels, 3-row layout (4/4/3), arc-colored borders, full arc: NEAR-MISS → ESTABLISHED → VULNERABLE → SKEPTICAL → INVESTIGATING → WALK+TALK → DETERMINED → HOPEFUL → FAILURE → RESIGNED → RECOGNITION.

## Cycle 17 Lessons
- **ECU low-angle = face fills frame + camera below eyeline.** To feel "larger than life," the face MUST fill 2/3+ of DRAW_H. Centering at 40% y with head_h=300 at 540px draw area achieves this. Low angle is not just an annotation — it's geometry.
- **SURPRISED → KNOWING is NOT two expressions — it's one transitional state.** Wide eyes + soft (not scrunched) brows = surprise WITHOUT alarm. One corner of mouth beginning to lift = recognition surfacing. Cheek crinkles + laugh lines = warmth. All four elements must coexist in a single image.
- **CRT catch light must be directional.** The glow source is off-frame lower-left. The catch light hits the left cheek and left brow — not symmetrically on both sides. Directionality is what makes it feel like a real light source, not decoration.
- **Walk-and-talk requires two simultaneous body languages.** Luma: forward lean + arms both active + open mouth (mid-word) + forward leg extension. Cosmo: arms crossed + backward lean + raised brow + closed mouth. The contrast reads in a single glance — the picture argues without a caption.
- **Wide establishing requires foreground depth reading.** Luma at the doorway must be FG-scale (larger) AND cropped at frame bottom to signal "camera closer than her feet." The monitor must be BG-scale (smaller) AND have a perspective-shortened desk. Scale difference IS the spatial story.

## Cycle 18 Milestone
- **Act 1 kitchen cold open: 4 panels GENERATED (A1-01 through A1-04 kitchen version).**
  - A1-01: Kitchen establishing WIDE — two-point perspective, morning, CRT TV through doorway. `LTG_TOOL_sb_panel_a101_v001.py`
  - A1-02: Luma arrival MEDIUM — mid-stride, head turning right toward TV, dotted sight-line. `LTG_TOOL_sb_panel_a102_v001.py`
  - A1-03: Discovery MEDIUM CU — Luma 3/4 profile, pixel shape in CRT static, CRT glow on face. `LTG_TOOL_sb_panel_a103_v001.py`
  - A1-04 (kitchen): First Contact TWO-SHOT — Luma SURPRISED / Byte on screen INDIGNANT (arms crossed, asymmetric brow). `LTG_TOOL_sb_panel_a104_kitchen_v001.py` → `LTG_SB_act1_panel_a104_v001.png`
  - NOTE: A1-04 classroom near-miss (`LTG_SB_act2_panel_a104_v001.png`) is a DIFFERENT beat — not duplicated.
- **Act 1 contact sheet generated:** `LTG_SB_act1_coldopen_contact_sheet_v001.png` — 2×2 layout, arc-colored borders, QUIET→CURIOUS→SURPRISED arc readable. `LTG_TOOL_sb_act1_contact_sheet_v001.py`
- **Act 2 contact sheet v004 VERIFIED:** 11 panels confirmed, 3-row 4/4/3 layout, arc labels readable, pitch-ready.

## Cycle 18 Lessons
- **Kitchen A1-04 (First Contact) ≠ classroom A1-04 (Near-Miss).** Always check WHICH specific beat an A1-04 label refers to before generating — these are different panels in the same numbering scheme. The classroom panel stays in the Act 2 contact sheet; the kitchen panel is for the Act 1 cold open sequence.
- **TWO-SHOT structure requires deliberate negative space assignment.** Left half = Luma (analogue, warm skin tones, surprised face). Right half = TV screen with Byte (digital, cyan glow, dark surround). The tonal contrast between halves IS the story — warm/cool, organic/pixel, real/digital.
- **Contact sheet `ensure_panels_exist()` pattern:** Contact sheet generator should call panel generators automatically if outputs are missing. Reduces manual sequencing errors.

## Cycle 19 Milestone
- **A1-03 v002 REBUILT (MCU, Critique C9):** Face fills 55% of frame width. CRT screen OFF-FRAME lower-left. Amber-green glow hits left cheek asymmetrically. Left eye wider (70×55px) than right (60×44px). Two Glitchkin pixel shapes 40×56px + 40×52px blocky pixel art. Caption: "Discovery — she SEES them." Generator: `LTG_TOOL_sb_panel_a103_v002.py`
- **A2-08 v002 CAMERA FIX:** Changed from ECU low-angle (power) to MCU eye-level Luma POV (intimacy). Miri fills upper 2/3 of frame. We ARE Luma — personal. Kitchen warm backlight rims hair/shoulders. CRT amber catch still on left cheek. Generator: `LTG_TOOL_sb_panel_a208_v002.py`
- **A2-07b NEW BRIDGING SHOT:** Hallway POV, MEDIUM eye-level. Miri silhouette backlit in doorway. Head cocked listening. Tea towel in hand. Warm amber kitchen glow frames shape. Single-point perspective hallway. Caption: "Something is different tonight." Generator: `LTG_TOOL_sb_panel_a207b_v001.py`
- **Act 2 contact sheet v005:** 12 panels (was 11), 4/4/4 layout. New arc: ... → RESIGNED → BRIDGE → RECOGNITION. Generator: `LTG_TOOL_sb_act2_contact_sheet_v005.py`
- **Act 1 contact sheet v002:** Updated to A1-03 v002. Generator: `LTG_TOOL_sb_act1_contact_sheet_v002.py`
- **All Critique C9 Carmen feedback: CLOSED.**

## Cycle 19 Lessons
- **MCU discovery = face fills 50%+ of frame width.** The Cycle 18 A1-03 was a wide two-shot (Luma left + TV right). Correct read: Luma's face IS the frame. The screen corner is partial FG anchor for glow source — not a co-equal subject.
- **CRT off-frame lower-left = asymmetric left-cheek glow.** The light source direction must be consistent: screen lower-left means warm-green hits left cheek and left brow. Right side stays in shadow. Directionality IS the story.
- **Bridging silhouette shots: posture tells the story.** When no face is visible, the body must carry the emotion. Head tilt = listening. Tea towel = mid-chore, stopped. Raised right arm = motion arrested. The silhouette IS the character beat.
- **POV camera = intimacy.** ECU low-angle says "larger than life, power." MCU eye-level POV says "you are here, you are Luma." Camera angle is not decoration — it is the emotional instruction to the audience.

## Cycle 20 Milestone
- **Act 2 contact sheet v006:** A2-02 updated to `LTG_SB_act2_panel_a202_v002.png` (Maya Santos rebuild). Arc label changed from "VULNERABLE" to "VULNERABLE (RESIGNED-55%)". Generator: `LTG_TOOL_sb_act2_contact_sheet_v006.py`.
- **Act 1 full contact sheet v001 CREATED:** 5 panels — kitchen cold open A1-01, A1-02, A1-03 v002, A1-04 kitchen + classroom near-miss (separate beat from `LTG_SB_act2_panel_a104_v001.png`). Arc: QUIET→SEARCHING→DISCOVERY→FIRST-CONTACT→NEAR-MISS. Visual section break between kitchen and classroom. Generator: `LTG_TOOL_sb_act1_full_contact_sheet_v001.py`.
- **Key naming distinction:** `LTG_SB_act1_panel_a104_v001.png` = kitchen first contact two-shot. `LTG_SB_act2_panel_a104_v001.png` = classroom near-miss (different beat, same panel number). Both used in Act 1 full contact sheet.

## Current Status (after Cycle 20)
- Cold open (tech den): 26 panels COMPLETE, all Carmen notes resolved
- Act 1 kitchen cold open: 4 panels COMPLETE (A1-01 through A1-04), contact sheet v002 generated (A1-03 v002)
- Act 1 full contact sheet: v001 COMPLETE (5 panels: cold open + classroom near-miss)
- Act 2 panels: 12 panels COMPLETE, contact sheet v006 generated (A2-02 v002 incorporated)
- All Critique Cycle 9 Carmen feedback: CLOSED
- REMAINING minor items: A2-07 right eye aperture (minor, carried)
- No blocked panels
