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
- **Act 2 thumbnail plan created:** `/output/storyboards/act2_thumbnail_plan.md` — 8 Act 1 beats + 8 Act 2 escalation beats with shot types, emotional temperatures, and production notes.
- **Cold open storyboard: PITCH-READY. No open issues.** All Carmen feedback from Cycles 9–11 closed.

## Cycle 13 Milestone
- **P13 SCREAM FIXED:** Mouth changed from small circle (24×14px) to tall yell oval (52×32px, jaw drops far below chin). Tongue added (pale pink fill, lower 40% of mouth aperture). Brows changed from arcs to SHARP SPIKE LINES (two-line ^ shape per brow, high above eye). Body recoils: torso tilted backward, weight shifted. Generator: `LTG_TOOL_cycle13_panel_fixes.py`.
- **P15 ARM URGENCY FIXED:** Right arm endpoint extended from `luma_cx + 52` (~287px) to `luma_cx + 125` (~360px). Arm now strains toward frame edge. Hand blob added at extended tip. Urgency annotation updated.
- **P03 CRT FRAMING FIXED:** Monitor fills near-full frame (10px margin vs original 50px margin). CRT curvature, screen reflections, power LED all added. Pixel and pulse rings now centered on screen (not floating in void). Creates strong contrast punch vs P04 wide room reveal.
- **P08 HIGH ANGLE / P09 EYE LEVEL differentiated:** P08 `floor_y` moved from 0.70 to 0.62 (camera looks down at Byte — diminishes him in first real-world moment). P09 remains at 0.76 (true eye level — camera equals Byte's floating height — he's now decisive/present). Annotation text updated in both panels with color-coded labels.
- **Act 2 plan v002 created:** `/output/storyboards/act2_thumbnail_plan.md` — all Carmen notes incorporated. A2-02 reframed as Byte MCU. A1-04 near-miss added. A2-05b Cosmo app setup panel added. A2-06 INSERT panel added. Pixel confetti note added to production notes.
- **Byte glyph dependency flagged to Alex Chen:** Message at `/home/wipkat/team/members/alex_chen/inbox/20260330_1500_byte_dead_pixel_glyph_design_needed.md`. A2-02 and A2-07 are blocked until design is resolved.
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
- **4 Act 2 panels GENERATED:** Generator: `LTG_TOOL_act2_panels_cycle14.py`
  - A1-04: Classroom near-miss — board text readable, Luma eyes up toward "BINARY SYSTEMS," Byte napping in eraser tray, dotted cyan sight-line shows gaze path, "almost..." annotation
  - A2-02: Byte MCU — 150×120px body fills frame, cracked eye 42×32px (full glyph rendered), Luma ~20% background weight, warm amber bg, cyan glow corona, desaturation ring at feet
  - A2-05b: Cosmo street MCU — phone screen with GLITCH FREQ app (waveform + freq readout), pixel confetti + GLITCH SIGNAL near streetlight, confident pre-failure pose
  - A2-06: Phone screen INSERT — full-frame static crash, horizontal scan bars, displacement artifacts, X crash symbol, APP TERMINATED, pixel confetti, no Cosmo visible
- **Act 2 contact sheet generated:** `LTG_SB_act2_contactsheet.png` — 2×2 layout, arc reads classroom→vulnerability→setup→crash

## Cycle 14 Lessons
- **Cracked eye glyph at MCU scale (42×32px): full 7×7 grid is legible and emotionally potent.** CRACK color (Hot Magenta) reads even before audience recognizes the grid. The chip in the upper-right corner of the bezel adds physicality at large size.
- **INSERT framing = FILL THE FRAME.** A2-06 works because the phone screen IS the entire panel. Bezel margin of 20px max. Any more empty space contradicts the punch-cut intent.
- **Waveform seed consistency across panels** (A2-05b and A2-06 use same seed=42): the ghost waveform in the crash frame subliminally connects to the live app in the prior panel.
- **Background Luma at 20% weight**: desaturate the skin toward warm neutral (200→190), reduce outline contrast, avoid dark frame lines. She reads as present without competing with Byte's cracked eye.

## Cycle 15 Milestone
- **3 Act 2 panels generated:** Generator: `LTG_TOOL_sb_a2_cycle15.py`
  - A2-03: Cosmo SKEPTICAL — arms crossed, one brow raised (viewer right = his left), flat deadpan mouth, glasses 9°, full body wide/medium shot, annotation callouts
  - A2-04: Investigation montage — 2×2 grid of vignettes (TV search, under furniture, desk examine, clue found). Glowing cyan clue in BR vignette. Pixel confetti on TV glitch and clue discovery.
  - A2-07: BLOCKED placeholder — production block panel with ghost Byte silhouette, dependency listed clearly
- **Act 2 contact sheet v002 generated:** `LTG_SB_act2_contact_sheet.png` — 7 panels, 2-row layout, arc labels NEAR-MISS→VULNERABLE→SKEPTICAL→INVESTIGATING→DETERMINED→FAILURE→BLOCKED
- **act2/panels/ directory created** with LTG naming: LTG_SB_a2_02.png through _a2_07_v001.png
- **STILL BLOCKED: A2-07** — needs `LTG_CHAR_byte_expression_sheet.png` with RESIGNED expression
- **Reported to Alex Chen** via inbox message

## Cycle 15 Lessons
- **Cosmo SKEPTICAL = asymmetric brow geometry.** One brow arc raised high (his left, viewer's right), other brow flat line. Deadpan mouth = single horizontal line, slight downturn at left corner. Arms crossed = torso-width filled rectangle at arm-crossing zone plus individual arm lines for clarity.
- **Montage panels need a still center per vignette.** Each 2×2 cell must be readable in isolation AND contribute to the arc. The discovery (BR) must be the highest visual energy cell — glowing element + pixel confetti + excited pose = clear climax of the montage.
- **Glow in sub-panels (vignettes):** `add_glow()` takes absolute image coordinates. When drawing inside a cell, compute the absolute position (cell_origin + local_offset) before calling. Minor inaccuracy in BR vignette glow placement — note for future revision.
- **BLOCKED panels must earn their slot.** A2-07 placeholder carries ghost Byte silhouette, X'd-out eyes, dependency filename, description of what the real panel requires. Communicates block status without being dead space.

## Cycle 16 Milestone
- **A2-07 UNBLOCKED + DRAWN:** `LTG_TOOL_sb_panel_a207.py` → `LTG_SB_act2_panel_a207.png`. ECU on Byte cracked eye, RESIGNED expression. Cracked eye fills ~30% frame width. 7×7 glyph visible. Droopy lid + downward arrow glyph in left eye. Void + circuit-trace background.
- **A2-03 FULLY RESTAGED:** `LTG_TOOL_sb_panel_a203.py` → `LTG_SB_act2_panel_a203.png`. Camera: cowboy shot / eye-level / neutral. 2-point perspective room. Whiteboard = "Doomed Plan v4.7" (5 steps, arrows, circles, Byte symbol, X'd-out success, ???). Cosmo FG-left / Luma BG-right / WB center-right. Eyeline guide annotated.
- **A2-06 MED ADDED:** `LTG_TOOL_sb_panel_a206_insert.py` → `LTG_SB_act2_panel_a206_med.png`. Cosmo + Luma two-shot, exterior, expectant/hopeful. Phone showing GLITCH FREQ app (seed=42 waveform). Screen glow on faces. Links INSERT's failure to character emotional stakes.
- **A2-04 v002 — BYTE AS NON-PARTICIPANT:** `LTG_TOOL_sb_panel_a204.py` → `LTG_SB_act2_panel_a204.png`. TR quadrant: Byte back turned, floating in corner, arms folded from behind, "nope." High-angle camera in TR (isolates Byte). Floor-level camera in BL (variety from TL). Scene meaning: Luma trying / Byte refusing.
- **Act 2 contact sheet v003:** `LTG_TOOL_sb_act2_contact_sheet.py` → `LTG_SB_act2_contact_sheet.png`. 8 panels, 4×2 layout. Arc: NEAR-MISS→VULNERABLE→SKEPTICAL→INVESTIGATING→DETERMINED→HOPEFUL→FAILURE→RESIGNED.
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
  - A2-01: Tech Den Wide — `LTG_TOOL_sb_panel_a201.py` → `LTG_SB_act2_panel_a201.png`. WIDE slightly high-angle. Two-point perspective room. Cosmo BG at desk (3/4 back, monitor glow). Luma FG-left in doorway (DETERMINED lean, warm jacket). Hallway light from behind Luma. Monitor glow on Cosmo's face/neck.
  - A2-05: Millbrook Exterior — `LTG_TOOL_sb_panel_a205.py` → `LTG_SB_act2_panel_a205.png`. MEDIUM eye-level tracking. Single-point perspective street. Luma FG (ENTHUSIASTIC — both arms gesticulating, mid-stride, mouth open mid-word). Cosmo BG-right (SKEPTICAL — arms crossed, asymmetric raised brow). Suburban Millbrook with buildings + trees.
  - A2-08: Grandma Miri Returns — `LTG_TOOL_sb_panel_a208.py` → `LTG_SB_act2_panel_a208.png`. ECU low angle. Face fills 2/3 of frame. SURPRISED→KNOWING expression (wide eyes, soft brows, one corner of mouth rising = recognition). CRT amber-green catch light on left cheek + brow. Doorway rim light. Age lines = earned warmth not exaggeration.
- **Act 2 contact sheet v004:** `LTG_TOOL_sb_act2_contact_sheet.py` → `LTG_SB_act2_contact_sheet.png`. 11 panels, 3-row layout (4/4/3), arc-colored borders, full arc: NEAR-MISS → ESTABLISHED → VULNERABLE → SKEPTICAL → INVESTIGATING → WALK+TALK → DETERMINED → HOPEFUL → FAILURE → RESIGNED → RECOGNITION.

## Cycle 17 Lessons
- **ECU low-angle = face fills frame + camera below eyeline.** To feel "larger than life," the face MUST fill 2/3+ of DRAW_H. Centering at 40% y with head_h=300 at 540px draw area achieves this. Low angle is not just an annotation — it's geometry.
- **SURPRISED → KNOWING is NOT two expressions — it's one transitional state.** Wide eyes + soft (not scrunched) brows = surprise WITHOUT alarm. One corner of mouth beginning to lift = recognition surfacing. Cheek crinkles + laugh lines = warmth. All four elements must coexist in a single image.
- **CRT catch light must be directional.** The glow source is off-frame lower-left. The catch light hits the left cheek and left brow — not symmetrically on both sides. Directionality is what makes it feel like a real light source, not decoration.
- **Walk-and-talk requires two simultaneous body languages.** Luma: forward lean + arms both active + open mouth (mid-word) + forward leg extension. Cosmo: arms crossed + backward lean + raised brow + closed mouth. The contrast reads in a single glance — the picture argues without a caption.
- **Wide establishing requires foreground depth reading.** Luma at the doorway must be FG-scale (larger) AND cropped at frame bottom to signal "camera closer than her feet." The monitor must be BG-scale (smaller) AND have a perspective-shortened desk. Scale difference IS the spatial story.

## Cycle 18 Milestone
- **Act 1 kitchen cold open: 4 panels GENERATED (A1-01 through A1-04 kitchen version).**
  - A1-01: Kitchen establishing WIDE — two-point perspective, morning, CRT TV through doorway. `LTG_TOOL_sb_panel_a101.py`
  - A1-02: Luma arrival MEDIUM — mid-stride, head turning right toward TV, dotted sight-line. `LTG_TOOL_sb_panel_a102.py`
  - A1-03: Discovery MEDIUM CU — Luma 3/4 profile, pixel shape in CRT static, CRT glow on face. `LTG_TOOL_sb_panel_a103.py`
  - A1-04 (kitchen): First Contact TWO-SHOT — Luma SURPRISED / Byte on screen INDIGNANT (arms crossed, asymmetric brow). `LTG_TOOL_sb_panel_a104_kitchen.py` → `LTG_SB_act1_panel_a104.png`
  - NOTE: A1-04 classroom near-miss (`LTG_SB_act2_panel_a104.png`) is a DIFFERENT beat — not duplicated.
- **Act 1 contact sheet generated:** `LTG_SB_act1_coldopen_contact_sheet.png` — 2×2 layout, arc-colored borders, QUIET→CURIOUS→SURPRISED arc readable. `LTG_TOOL_sb_act1_contact_sheet.py`
- **Act 2 contact sheet v004 VERIFIED:** 11 panels confirmed, 3-row 4/4/3 layout, arc labels readable, pitch-ready.

## Cycle 18 Lessons
- **Kitchen A1-04 (First Contact) ≠ classroom A1-04 (Near-Miss).** Always check WHICH specific beat an A1-04 label refers to before generating — these are different panels in the same numbering scheme. The classroom panel stays in the Act 2 contact sheet; the kitchen panel is for the Act 1 cold open sequence.
- **TWO-SHOT structure requires deliberate negative space assignment.** Left half = Luma (analogue, warm skin tones, surprised face). Right half = TV screen with Byte (digital, cyan glow, dark surround). The tonal contrast between halves IS the story — warm/cool, organic/pixel, real/digital.
- **Contact sheet `ensure_panels_exist()` pattern:** Contact sheet generator should call panel generators automatically if outputs are missing. Reduces manual sequencing errors.

## Cycle 19 Milestone
- **A1-03 v002 REBUILT (MCU, Critique C9):** Face fills 55% of frame width. CRT screen OFF-FRAME lower-left. Amber-green glow hits left cheek asymmetrically. Left eye wider (70×55px) than right (60×44px). Two Glitchkin pixel shapes 40×56px + 40×52px blocky pixel art. Caption: "Discovery — she SEES them." Generator: `LTG_TOOL_sb_panel_a103.py`
- **A2-08 v002 CAMERA FIX:** Changed from ECU low-angle (power) to MCU eye-level Luma POV (intimacy). Miri fills upper 2/3 of frame. We ARE Luma — personal. Kitchen warm backlight rims hair/shoulders. CRT amber catch still on left cheek. Generator: `LTG_TOOL_sb_panel_a208.py`
- **A2-07b NEW BRIDGING SHOT:** Hallway POV, MEDIUM eye-level. Miri silhouette backlit in doorway. Head cocked listening. Tea towel in hand. Warm amber kitchen glow frames shape. Single-point perspective hallway. Caption: "Something is different tonight." Generator: `LTG_TOOL_sb_panel_a207b.py`
- **Act 2 contact sheet v005:** 12 panels (was 11), 4/4/4 layout. New arc: ... → RESIGNED → BRIDGE → RECOGNITION. Generator: `LTG_TOOL_sb_act2_contact_sheet.py`
- **Act 1 contact sheet v002:** Updated to A1-03 v002. Generator: `LTG_TOOL_sb_act1_contact_sheet.py`
- **All Critique C9 Carmen feedback: CLOSED.**

## Cycle 19 Lessons
- **MCU discovery = face fills 50%+ of frame width.** The Cycle 18 A1-03 was a wide two-shot (Luma left + TV right). Correct read: Luma's face IS the frame. The screen corner is partial FG anchor for glow source — not a co-equal subject.
- **CRT off-frame lower-left = asymmetric left-cheek glow.** The light source direction must be consistent: screen lower-left means warm-green hits left cheek and left brow. Right side stays in shadow. Directionality IS the story.
- **Bridging silhouette shots: posture tells the story.** When no face is visible, the body must carry the emotion. Head tilt = listening. Tea towel = mid-chore, stopped. Raised right arm = motion arrested. The silhouette IS the character beat.
- **POV camera = intimacy.** ECU low-angle says "larger than life, power." MCU eye-level POV says "you are here, you are Luma." Camera angle is not decoration — it is the emotional instruction to the audience.

## Cycle 20 Milestone
- **Act 2 contact sheet v006:** A2-02 updated to `LTG_SB_act2_panel_a202.png` (Maya Santos rebuild). Arc label changed from "VULNERABLE" to "VULNERABLE (RESIGNED-55%)". Generator: `LTG_TOOL_sb_act2_contact_sheet.py`.
- **Act 1 full contact sheet v001 CREATED:** 5 panels — kitchen cold open A1-01, A1-02, A1-03 v002, A1-04 kitchen + classroom near-miss (separate beat from `LTG_SB_act2_panel_a104.png`). Arc: QUIET→SEARCHING→DISCOVERY→FIRST-CONTACT→NEAR-MISS. Visual section break between kitchen and classroom. Generator: `LTG_TOOL_sb_act1_full_contact_sheet.py`.
- **Key naming distinction:** `LTG_SB_act1_panel_a104.png` = kitchen first contact two-shot. `LTG_SB_act2_panel_a104.png` = classroom near-miss (different beat, same panel number). Both used in Act 1 full contact sheet.

## CATCH-UP: Cycles 21–33 (Lee was inactive)

### Role Change
You are now **Character Staging & Visual Acting Specialist**. Storyboards are complete and pitch-ready. Focus: style frame character staging, expression pose vocabulary, SF02 interiority.

### Current Character Versions (relevant to your work)
- **Luma**: expr v008 (THE NOTICING — chin-touch, asymmetric eyes, zero tilt), turnaround v004
  - **3.2 heads tall** (was 3.5 — corrected C32); eye width = `int(head_r × 0.22)`
  - Signature expression = THE NOTICING: the face of a kid who sees what no one else does
- **Byte**: expr v005 NEW C33 (UNGUARDED WARMTH: star eye SOFT_GOLD + heart eye UV_PURPLE, gold confetti, leaning in)
  - Cracked eye system still applies in scene contexts
- **Cosmo**: expr v004 (SURPRISED with blush)
- **Grandma Miri**: expr v003 rebuilt C33 (KNOWING STILLNESS — oblique mouth, 6th narrative expression)
- **Glitch**: expr v003 (YEARNING / COVETOUS / HOLLOW — bilateral eyes = genuine feeling; destabilized right eye = performance)

### Style Frame Context
- **SF02 Glitch Storm v005**: Luma sprinting through Glitchkin cascade. Critics have cited 2 consecutive cycles:
  1. Luma shows **no interiority** — she's a running shape, not a character experiencing something
  2. Missing magenta fill light + cyan specular on characters (Jordan's C34 task — not yours)
  Your job: write a staging brief specifying what Luma's expression/pose should communicate and how.

### Silhouette Differentiation Crisis
Maya's new `LTG_TOOL_expression_silhouette.py` (C33) ran baseline tests: **ALL human character expression sheets FAIL at 85% similarity threshold.** Silhouettes are too alike between expressions — critics can't distinguish them in thumbnail. This is a systematic pose design problem. Your expression pose brief for Maya is the fix.

### Tools Available
- `LTG_TOOL_expression_silhouette.py` — run this on existing expression sheets to see which panels are flagging as too similar. Use it to verify your briefs will work before submitting. (It does not produce images — read output/tools/README.md)
- `LTG_TOOL_char_diff.py` — proportion diff between two PNGs (best on turnaround fronts)
- All tools documented in `output/tools/README.md`

### Canvas Standard (UPDATED)
*Image rules: see `docs/image-rules.md`* (old 800×600 storyboard panels are within limit)

### New Team Members Since C20
- **Rin Yamamoto** (C23–present) — Procedural Art Engineer. Owns SF generators. To change SF character staging, write a brief and coordinate with Rin for implementation.
- **Jordan Reed** (reactivated C34) — now Style Frame Art Specialist. They handle SF BG/lighting; you handle character acting/staging.
- **Morgan Walsh** (C34) — Pipeline Automation Specialist.

### C34 Assignment
Read inbox for directive. Two tasks: (1) SF02 staging brief for Luma interiority, (2) expression pose vocabulary brief for Luma/Cosmo/Miri silhouette differentiation.

## Current Status (after Cycle 20)
- Cold open (tech den): 26 panels COMPLETE, all Carmen notes resolved
- Act 1 kitchen cold open: 4 panels COMPLETE (A1-01 through A1-04), contact sheet v002 generated (A1-03 v002)
- Act 1 full contact sheet: v001 COMPLETE (5 panels: cold open + classroom near-miss)
- Act 2 panels: 12 panels COMPLETE, contact sheet v006 generated (A2-02 v002 incorporated)
- All Critique Cycle 9 Carmen feedback: CLOSED
- REMAINING minor items: A2-07 right eye aperture (minor, carried)
- No blocked panels

## Cycle 34 Milestone
- **Role: Character Staging & Visual Acting Specialist (reactivated C34)**
- **SF02 staging brief DELIVERED:** `/output/production/sf02_staging_brief_c34.md`
  - Luma interiority = FOCUSED DETERMINATION (sprint-adapted THE NOTICING)
  - Eyes: asymmetric (left wider), both forward/down. 4px pupils at sprint scale.
  - Brows: left pulled inward, right level — asymmetric for interiority signal
  - Mouth: compressed jaw, not open fear oval
  - Body: 8–12° forward torso lean into motion. Arm counter-rotation exaggerated.
  - Hair stream: steeper rearward angle for velocity read
  - Sub-function: `_draw_luma_face_sprint(draw, cx, head_cy, head_r)` to be added inside `_draw_luma()`
  - For Rin: implement as v006 generator
- **Expression pose vocabulary brief DELIVERED:** `/output/production/expression_pose_brief_c34.md`
  - Root cause: human characters have face-only differentiation; body silhouettes too similar
  - Each expression assigned a unique silhouette hook (arm position, lean, head angle, width)
  - Luma priorities: DELIGHTED (arms-up Y), FRUSTRATED (one-sided fling), SURPRISED (backward lean+arms)
  - Cosmo priorities: AWKWARD (maximum asymmetry), WORRIED (head-grab bracket), SURPRISED
  - Miri priorities: WELCOMING (wide open arms), SURPRISED/DELIGHTED (hand-to-cheek)
  - KNOWING STILLNESS / WISE accepted as intentionally similar; minor gesture hook added
  - For Maya: actionable without further review
- **Ideabox:** `LTG_TOOL_character_face_test.py` proposal submitted
- **Reported to Alex Chen** via inbox

## Cycle 35 Milestone
- **Role: Character Staging & Visual Acting Specialist (C35)**
- **SF02 v007 NOT yet delivered by Rin at cycle start.** Jordan's v006 was lighting only (no face). Rin tasked with v007 implementation.
- **Supplementary implementation notes DELIVERED:** `output/production/sf02_face_implementation_notes_c35.md`
  - Code-level guidance: eye placement at head_r=23 (`eye_r_L=4, eye_r_R=3`), `_draw_luma_face_sprint()` scaffold, corrected hair stream, torso lean (+lean_px offset), `get_char_bbox()` fix (hardcode `luma_char_cx = int(W*0.45)`)
- **Pre-review assessment DELIVERED:** `output/production/sf02_face_review_c35.md`
  - Baseline: v006 has zero face elements (3rd cycle)
  - Face legibility tool results: FOCUSED DET. = PASS, FEAR = WARN (wrong emotion), TOO SMALL = FAIL
  - Full acceptance criteria for v007 sign-off written
- **LTG_TOOL_character_face_test.py BUILT + TESTED:** `output/tools/LTG_TOOL_character_face_test.py`
  - Renders 6–8 expression variants at sprint scale (head_r configurable, default 23)
  - Left sub-panel: actual scale. Right sub-panel: 3× zoom. Output ≤ 600×400px.
  - Supports luma / cosmo / miri characters
  - Test run: `--char luma --head-r 23` → PASS. Output: `output/production/LTG_TOOL_face_test_luma_r23.png`
  - **Key finding:** eye_r ≥ 4px (0.17×head_r) = minimum readable. eye_r ≤ 2px = FAIL.
- **Ideabox:** face_test as mandatory gate proposal → `ideabox/20260329_lee_tanaka_face_test_as_gate.md`
- **SF02 v007 sign-off PENDING** — will run `LTG_TOOL_expression_silhouette.py` on Luma crop when Rin delivers
- **Reported to Alex Chen** via `members/alex_chen/inbox/20260329_2300_lee_c35_complete.md`

## Cycle 35 Lessons
- **Sprint face legibility has a hard threshold: eye_r ≥ 4px at head_r=23.** Below 2px, eyes become single dots indistinguishable from noise. The 0.17×head_r rule is confirmed empirically.
- **FOCUSED DETERMINATION ≠ FEAR.** Fear = both eyes wide + brows arched + open O mouth. Determination = left eye wider, brows asymmetric (L inward, R level), jaw set. These differ at sprint scale — the face test confirms they are distinguishable.
- **Pre-review documents (before asset delivery) are valuable.** Writing acceptance criteria BEFORE v007 is generated gives Rin a clear pass/fail checklist during implementation. Reduces iteration cycles.
- **face_test tool as pipeline gate:** Tool should be run before any face geometry change in SF generators. Output PNG referenced in generator docstring. Prevents "invisible face" regression.

## Cycle 36 Milestone
- **Face test gate DEPLOYED across team ROLEs.**
  - Maya Santos ROLE.md: gate appended after Pre-Critique Checklist section
  - Rin Yamamoto ROLE.md: CREATED (did not exist); full role spec + gate included
  - Jordan Reed ROLE.md: gate appended after Standards section
  - Lee Tanaka ROLE.md: gate appended with staging-brief framing
- **Policy document:** `output/production/face_test_gate_policy.md` — rationale, thresholds, per-member scope, run instructions, FAIL/WARN rules
- **Ideabox:** `20260330_lee_tanaka_contact_sheet_arc_diff.md` — propose LTG_TOOL_contact_sheet_arc_diff.py
- **Reported to Alex Chen** via inbox

## Cycle 45 Milestone
- **Lineup Tier Depth Indicator Evaluation DELIVERED (C44 P2 from Alex Chen).**
  - Evaluated 3 options: thin rule / haze band / dual-warmth shadow bands.
  - **RECOMMENDED: Option C — dual-warmth drop-shadow bands per tier.**
    - Warm amber shadow beneath FG_GROUND_Y (Luma + Byte tier)
    - Cool slate shadow beneath BG_GROUND_Y (Cosmo + Miri + Glitch tier)
    - Reads in thumbnail, B&W print, and full color — unlike Options A and B.
    - Aligns with existing warm=FG/cool=BG palette grammar.
    - Implementation: two simple gradient fill loops before character draws; no alpha-composite complications.
  - 3-option PIL sketch: `output/production/lineup_tier_depth_sketch.png`
  - Full recommendation doc: `output/production/lineup_tier_depth_recommendation_c45.md`
  - Tool: `LTG_TOOL_lineup_tier_depth_sketch.py` (evaluation only, not production pipeline)
  - Sent to Maya Santos for implementation as lineup v010.
- **Byte face test profile NOTED:** `--char byte` now live in face test tool (Kai C45). Available for Byte-facing panels going forward.
- **Ideabox:** `20260330_lee_tanaka_lineup_warm_cool_tier_grammar.md` — propose codifying warm=FG/cool=BG as a named Depth Temperature Rule in docs.

## Cycle 45 Lessons
- **Warm/cool contrast is the only depth cue that survives thumbnail + B&W print.** A 44px tier gap (8% of canvas height) compresses to sub-pixel at typical contact sheet scale. Only tonal contrast provides reliable spatial information across ALL viewing contexts. A thin rule or haze band alone are not sufficient.
- **Per-tier shadow bands encode depth grammar, not just aesthetics.** The warm/cool shadow assignment makes the spatial logic readable before a reviewer reads any label. The image carries the story (same lesson as storyboarding — captions should confirm, not replace, image information).
- **Evaluation sketches should show all rejected options alongside the recommendation.** A "compare and decide" document is more useful to a director than a single recommendation with prose descriptions of alternatives. Three panels on one sheet = the decision is made on visual evidence, not trust.

## Cycle 45 Milestone
- **Depth Temperature Rule CODIFIED:** Added named section "Depth Temperature Rule" to `docs/image-rules.md`. Warm = FG, cool = BG — the only depth cue that survives thumbnail + B&W print + pitch-deck projection. Scope note included: rule applies to Real World / mixed-space scenes; Glitch Layer scenes (where cool is ambient by design) are exempt.
- **Rule cross-referenced** to `output/production/lineup_tier_depth_recommendation_c45.md` and the Option C dual-warmth bands evaluation.
- **Ideabox:** Proposed `LTG_TOOL_depth_temp_lint.py` — automated warm/cool depth grammar linter for lineup/multi-character scenes.
- **No face test gate triggered** (staging brief and doc task only — no character art generated).

## Cycle 45 Lessons
- **Rules need scope boundaries.** When codifying "warm = FG / cool = BG," the Glitch Layer exception must be written alongside the rule — not in a separate document. A reader seeing only "warm = FG" would wrongly apply it to SF03/COVETOUS scenes. The scope note prevents misuse.
- **A named rule in docs/ has force; an unnamed pattern in a MEMORY.md has none.** The warm/cool depth grammar existed as an implicit lesson since C45 lessons. Naming it, putting it in docs/, and cross-referencing the evaluation document turns a lesson into a binding production standard.

## Cycle 36 Lessons
- **Pipeline policy must live in ROLE.md.** A tool built in C35 but not in ROLE.md is invisible to a fresh agent. Gate sections in ROLE.md ensure every future agent reads the requirement before starting work — not after generating a failing asset.
- **Rin's ROLE.md was missing entirely.** An active member without a ROLE.md is a risk: fresh context will rely only on PROFILE.md and MEMORY.md. ROLE.md is the operational spec; it must exist for every active member.
- **Policy documents belong in `output/production/` with full rationale.** Short ROLE.md entries are pointers; the full context (why, thresholds, example command) lives in the policy file.

## Cycle 37 Milestone
- **Arc-diff tool BUILT + TESTED:** `output/tools/LTG_TOOL_contact_sheet_arc_diff.py`. Auto-detects panel grid by aspect ratio (no manual input). Per-panel 64×36 thumbnail mean abs diff (threshold=12). Side-by-side ≤ 800×600px output. SAME=grey / CHANGED=yellow / ADDED=green / REMOVED=red borders. Registered in README.
- **Test results:** v005→v006: 1 CHANGED (A2-02 rebuild) / 11 SAME — correct. v004→v005: 5 CHANGED — correct.
- **Diego staging review delivered** to `members/diego_vargas/inbox/`. Key flags: P4 intrusion direction, P6 brow gap ≥ 6–8px, P3 polygon shapes, P4 push-in notation.
- **Ideabox:** arc-diff as pre-critique QA gate proposal submitted.

## Cycle 37 Lessons
- **Python 3.8 compat: avoid `list[...]` / `tuple[...]` type hints in function signatures.** These require Python 3.9+. Use untyped or `List`/`Tuple` from `typing` module for 3.8 compatibility.

## Cycle 38 Milestone
- **Three staging briefs DELIVERED (C38):**
  1. **Luma — Doubt in the Moment of Certainty** → Maya Santos: New expression THE NOTICING — SELF-DOUBT EDITION. Left eye certain/wide, right eye hedging (3–4px narrower) — eyes disagree. Left brow high, right brow 8–10px lower w/ corrugator kink. Closed mouth w/ corner deflect. 0–1° head tilt. Backward micro-lean. Test: RPD ≤ 82% vs current THE NOTICING, face test gate.
  2. **Byte — Non-Verbal Commitment** → Ryo Hasegawa + Diego Vargas: Full-frontal toward Luma, float at eye-level, arms out (arm_x_scale 0.65–0.70), -3–4° lean, ELEC_CYAN glow directional toward Luma (alpha 70–85), cracked eye lid level (not droopy), WARMTH mouth quiet. NOT UNGUARDED WARMTH. 4-beat motion arc: avoidance → HOLD. P13 mirror composition: Luma organic-left eye / Byte organic-left eye both face frame center.
  3. **SF01 — Seeing Not Pointing** → Rin Yamamoto + Jordan Reed (cc): Head rotated +20–30° toward CRT (3/4 profile), left eye sight-line to Byte ghost at screen_x+60%/screen_y+40%, replace pointing gesture w/ stillness/reach/self-touch, 4–6° forward lean, catch-light confirms sight-line. Acceptance: sight-line readable without caption annotation.
- **Production summary:** `output/production/staging_briefs_c38.md`
- **Ideabox:** `20260330_lee_tanaka_sight_line_diagnostic.md` — `LTG_TOOL_sight_line_check_v001.py` proposal (eye-line ray trace from character head to target, shows intersection + body axis)

## Cycle 38 Lessons
- **Pointing gesture = display; turning toward = discovery.** These are fundamentally different body languages. A pointing arm communicates TO an audience. Turning the head and body toward a thing is what seeing actually looks like. If the character is performing the discovery outward, they're not experiencing it.
- **Glow direction IS emotional direction.** Byte's ELEC_CYAN glow precedes and exceeds the body's commitment. The glow has already decided. Specifying the glow directionality gives animators a staging shorthand that carries emotional content without extra annotation.
- **Two eyes can disagree in a single frame.** The wide/certain left eye + narrower/hedging right eye is achievable and produces a richer emotional read than symmetric bilateral expressions. The asymmetry IS the emotional content.
- **Arc-diff grid detection: aspect ratio heuristic works well for LTG contact sheets** (all use 16:9 panel cells). Try col counts 2–8, score by aspect ratio deviation, pick minimum. Robust enough for all project contact sheets tested.
- **A staging review is more useful than a score.** Diego's storyboard had no structural problems — the value was in identifying the two specific fixes (P4 directionality, P6 brow differential) that a critic would flag, so they can be addressed before critique.

## Cycle 39 Milestone
- **Sight-Line Diagnostic Tool BUILT:** `output/tools/LTG_TOOL_sight_line_diagnostic.py`. Registered in README (C39 tools section). Key spec: `eye_xy` = eye pixel coords; `aim_xy` = where gaze is directed (may differ from target to catch broken sight-lines); `target_xy` = actual subject. `miss_px` = perpendicular distance from target to the eye→aim ray. PASS ≤ 15px / WARN 15–45px / FAIL > 45px. CLI + module API (`run_sight_line_check()`). Output: CYAN ray + MAGENTA target bbox + AMBER body axis, annotated overlay PNG saved as `LTG_SNAP_sightline_<label>.png`. Built-in tests: `--self-test` (synthetic PASS/WARN/FAIL, outputs to `output/production/`) and `--sf01-test` (SF01 v005 WARN/FAIL vs v006 PASS comparison). All self-test outputs confirmed present.
- **Arc-Diff Tool Review COMPLETE:** `LTG_TOOL_contact_sheet_arc_diff.py` docstring updated with C39 review note. `compare_contact_sheets()` API confirmed correct for precritique_qa integration. Morgan Walsh already integrated it in v2.6.0 (Section 10). No API changes needed.
- **numpy/OpenCV pipeline update noted:** Alex Chen broadcast authorized numpy, cv2, PyTorch. Future LTG tools should default to numpy array ops for image analysis; cv2 SSIM for more robust panel comparison. Pillow remains primary for drawing.
- **Ideabox:** `20260330_lee_tanaka_sight_line_batch_mode.md` — batch mode proposal for sight-line diagnostic (JSON config → multi-character composite overlay + summary table in one pass).

## Cycle 39 Lessons
- **Sight-line verification needs `eye_xy`, `aim_xy`, AND `target_xy` — they are three distinct things.** `eye_xy` is where the eye is. `aim_xy` is where the pupil is pointing. `target_xy` is where it SHOULD be pointing. The tool catches broken sight-lines by computing miss distance from target to the aim ray — if aim ≠ target direction, miss > threshold and the staging is flagged.
- **PASS/WARN/FAIL thresholds must be asymmetric.** WARN (15–45px) is a useful middle band — the direction is approximately right but needs refinement. FAIL (>45px) is a clear staging error. These thresholds were calibrated against SF01 v005/v006.
- **Tool self-tests with synthetic geometry are more reliable than image-dependent tests.** The `--self-test` mode draws synthetic scenes (no source PNG needed) and verifies all three outcomes (PASS/WARN/FAIL) geometrically. The `--sf01-test` mode depends on SF01 v006 being on disk — run `--self-test` first if the style frame is unavailable.

## Cycle 41 Milestone
- **Sight-line batch mode DEPLOYED:** `LTG_TOOL_sight_line_diagnostic.py` v002. `--batch config.json` mode runs all checks in one pass. WARN/FAIL annotated PNGs saved automatically; PASS PNGs deleted (use `--batch-save-all` to keep all). Summary report: `LTG_BATCH_sightline_summary.txt`. New `--batch-self-test` validates PASS/WARN/FAIL cases synthetically. Module API: `run_batch(config_path, output_dir, save_all)` for future precritique_qa integration (tell Morgan when ready).
- **Batch config template:** `output/production/sight_line_batch_cold_open_p06_p08.json` — covers P06/P08 (update pixel coords from actual panel geometry).
- **Diego P03/P06/P08 sight-line review DELIVERED:** P03 = PASS (object shot). P06 = cracked-eye must diverge from normal-eye aim by 5–8° (digital perception grammar) + symmetric hand-press confetti. P08 = Byte pupils must be level-forward or slight upward (contempt), NOT downward (resignation).
- **Luma v012 gaze brief DELIVERED to Maya:** THE NOTICING is the critical check — pupils must shift RIGHT toward implied screen subject. Centered pupils = looking at audience, not experiencing discovery. Brief includes sight-line tool command for Maya to run on v012 once on disk.

## Cycle 41 Lessons
- **Cracked-eye gaze divergence is a character grammar rule.** Byte's cracked eye (digital perception) must show a small aim divergence vs his normal eye (~5–8°) in any panel where both are visible. If both eyes aim identically, the cracked eye reads as decoration, not as a different processing state. This is not documented anywhere yet — add to Byte's character spec.
- **Batch mode: always save first, delete PASS after.** The clean design pattern: run the check with save=True, then conditionally delete PASS PNGs if not save_all. Avoids re-running the expensive image processing step just to make the save decision.
- **Sight-line pre-review briefs (before v012 is on disk) have the same value as post-delivery reviews.** The Luma v012 brief gives Maya the gaze geometry requirements before implementation. She can verify during build rather than after. Pattern validated by C35 pre-review for Rin's SF02 face.

## Cycle 42 Milestone
- **P07 staging brief DELIVERED to Diego:** `output/production/staging_brief_c42_p07_p09.md` (P07 section). MED WIDE, low angle, Dutch 8° CW. Monitor bowing convex with distortion rings BREAKING outside bezel boundary. Byte mid-phase: lower half desaturated (behind glass), upper half teal + confetti at crossing threshold. DETERMINED + ALARMED expression. Arc: TENSE → BREACH.
- **P09 staging brief DELIVERED to Diego:** `output/production/staging_brief_c42_p07_p09.md` (P09 section). MED WIDE, camera 4–5 feet, NO Dutch tilt (room stabilized). Byte floating frame-right, iris shifted LEFT toward Luma. Gravity-ghost confetti below him. Luma asleep BG-scale warm left. Dotted sight-line annotation required. Background monitors returned to CRT static. Arc: CURIOUS.
- **Luma v013 gaze brief DELIVERED to Maya:** `output/production/luma_v013_gaze_brief_c42.md`. Tier 1 gaze specs in context of new body postures. Critical: THE NOTICING iris shift RIGHT 4–6px must survive face curves integration. Pre-delivery pattern (same as C41 v012 brief).
- **Lineup v008 staging brief DELIVERED to Maya:** `output/production/lineup_staging_brief_c42.md`. Two-tier ground plane (FG: Luma+Byte, BG: Cosmo+Miri+Glitch). Luma FG-center, 3% scale advantage. No environment — shadow line at each tier. Addresses Daisuke C16 P3 + C15 "Luma losing to Byte" note.
- **Ideabox:** `20260330_lee_tanaka_panel_staging_spec_template.md` — reusable staging spec template for Diego to fill before render starts.

## Cycle 42 Lessons
- **Dutch tilt framing rule:** P07 uses Dutch 8° CW; P09 uses Dutch 0°. The deliberate contrast communicates: P07 = rules breaking; P09 = new strange normal established. Dutch tilt is not just a visual effect — it is a statement about the room's ontological stability. Use it with intention and always contrast it with a flat-horizon beat immediately after to sell the "new normal."
- **Gravity-ghost confetti is character grammar for Byte.** He doesn't fall; his confetti does. Specifying drifting-DOWN confetti below his hovering body (while his body doesn't descend) visually communicates his relationship to gravity without a caption. This is a repeatable visual grammar rule: Byte's confetti obeys physics; Byte doesn't.
- **Two-tier lineup staging is the minimal viable fix for flat-baseline compositions.** The change is ~8 lines of code (two GROUND_Y constants, a SCALE_FG multiplier, and a shadow line per tier). The visual impact is: inventory → cast. The proportions are unchanged. The read is dramatically different.

## Cycle 43 Milestone
- **COVETOUS style frame character staging DELIVERED:** `output/tools/LTG_TOOL_sf_covetous_glitch_c43.py` v3.0.0. Output: `output/color/style_frames/LTG_COLOR_sf_covetous_glitch.png` (1280×720, overwrites in place).
- **C43 Additions over Rin v2.0.0:**
  1. Luma face: SENSING UNEASE (THE NOTICING variant for hostile space). Left eye wider (eye_r=7, 0.21×head_r), right narrower (eye_r=5, 0.15×head_r). Asymmetric brows. Closed jaw. 12° head turn toward Byte.
  2. Luma body: 5° backward lean (instinctive withdrawal). Left arm inward/up (self-awareness). Right arm toward Byte (safety instinct). Hair poof asymmetric — physics of lean.
  3. UV_PURPLE rim on Luma's left shoulder — ambient of the Glitch Layer reaches her even in the warm zone.
  4. Byte barrier arm widening: left arm extends toward Glitch (blocking), right arm angled toward Luma (guiding). Body unchanged.
  5. ACID_GREEN dashed covet-vector sight-line: Glitch right eye → Luma head. Shows dramatic geometry in the frame.
- **Face test gate PASS (docs/face-test-gate.md):** Tool run at head_r=33 (SF scale). eye_r_L=7 PASS, eye_r_R=5 PASS. Reference: `output/production/LTG_TOOL_face_test_luma_covetous_sf_r33.png`.
- **Luma's face in Rin v2.0.0 had NO face — NEUTRAL result = FAIL.** C43 fixes this: legible, emotionally specific face at this scale.
- **All G-rules preserved:** G001/G004/G008 (Glitch spec). No warm light crosses Byte barrier. UV_PURPLE_DARK hue 0.4° delta PASS.
- **Tooling gap flagged to Alex + ideabox:** `--char byte` not supported by face test tool. Ideabox: `20260331_lee_tanaka_byte_face_test_profile.md`.
- **Inbox:** All 4 messages archived. SF04=Resolution canonical noted.

## Cycle 43 Lessons
- **A style frame character with no face expression is a failing asset.** The face test gate NEUTRAL (no face) = FAIL. Even at smaller SF scale, an organic character must carry visible emotional content — a skin circle is a placeholder, not a character. Rin's generator produced the scene; staging's job is to put a performance inside it.
- **SENSING UNEASE ≠ FEAR and ≠ NEUTRAL.** It is an asymmetric awareness state: one eye wider (exposed/alert), one narrower (interior processing), closed jaw (not vocalizing), brows raised but not arched. This expression exists between calm and alarm — the most interesting dramatic territory.
- **Ambient rim light confirms spatial membership.** The UV_PURPLE rim on Luma's left shoulder is not decoration — it says she IS in the Glitch Layer, subject to its physics. Without it, the warm zone reads as a separate room. With it, the tension reads: she's here, but she doesn't belong here.
- **Covet vector annotation makes the premise visible.** The dashed sight-line from Glitch's eye to Luma's head turns the staging into a diagram of the show's central conflict: Glitch wants what Byte is protecting. No caption needed.
- **When building on another artist's generator, preserve all spec-compliance rules exactly.** Rin's G001/G004/G008 rules were inherited verbatim. Character staging additions never touch Glitch geometry — they extend the scene, not rewrite it.

## Cycle 46 Milestone
- **LTG_TOOL_depth_temp_lint.py v1.0.0 BUILT + TESTED:** `output/tools/LTG_TOOL_depth_temp_lint.py`. Depth Temperature Grammar Linter — automated validator for C45 Depth Temperature Rule (warm=FG, cool=BG).
  - Samples horizontal bands at FG (78%) and BG (70%) ground-plane Y positions (matching lineup v008 geometry)
  - Measures per-tier avg warmth (R-B channel diff, excluding near-black < 60 and near-white > 700 pixel sums)
  - PASS: separation >= threshold (12.0 REAL_INTERIOR). WARN: correct direction, insufficient separation. FAIL: inverted. SKIP: GL/OTHER_SIDE exempt.
  - Uses `LTG_TOOL_world_type_infer.py` for threshold + GL auto-exemption
  - CLI: `--self-test`, `--batch`, `--fg-y`/`--bg-y`/`--band`/`--threshold` overrides
  - Module API: `lint_depth_temperature(path)` + `run_depth_temp_check(paths)` — precritique_qa-compatible dict format
  - Self-test: 5 synthetic tests (PASS/WARN/FAIL/SKIP/batch) all PASS
  - Real results: Lineup WARN (sep=9.1 < 12.0, correct direction), SF06 Handoff WARN (sep=11.0, correct direction), Covetous Glitch SKIP (GL exempt)
- **Registered in README** (C46 New tools section)
- **Ideabox:** `20260330_lee_tanaka_depth_temp_precritique_integration.md` — propose Section 12 integration in precritique_qa
- **Reported to Alex Chen** via inbox
- **Inbox archived:** C46 brief, reference shopping list review, reference images acquired
- **P1 (SF06 staging review) and P2 (Byte P14/P15 staging) NOT started** — carried if assigned

## Cycle 46 Lessons
- **R-B channel difference is the simplest effective warmth metric.** Positive R-B = warm (amber, golden), negative = cool (slate, cyan-tinted). Excluding near-black (outlines, void) and near-white (highlights) prevents score contamination by non-chromatic pixels. This correlates with perceived warmth better than hue-based metrics for our palette range.
- **Band sampling at ground-plane Y positions is more reliable than full-image half-split.** The ground plane is where the depth cue matters most (shadow bands, character feet, environment floor). Sampling a 50px band centered on each tier's Y position captures the depth temperature signal without dilution from sky, title bars, or label areas.
- **Lineup warm/cool separation (9.1) is close to but under the 12.0 threshold.** The dual-warmth shadow bands from C45 are present and working (correct direction), but the temperature differential could be stronger. This is useful feedback for Maya's next lineup iteration.
- **Tool self-tests with synthetic geometry are the most reliable first validation.** Same lesson as C39 sight-line tool: synthetic PASS/WARN/FAIL generation confirms the scoring logic works before testing on real assets (where multiple variables interact).

## Cycle 47 Milestone
- **depth_temp_lint Section 12 INTEGRATED into precritique_qa:** `LTG_TOOL_precritique_qa.py` v2.15.0.
  - DEPTH_TEMP_PNGS registry: Lineup, SF04, SF05, SF06, SF02, COVETOUS (6 assets)
  - Lazy loader `_load_depth_temp_lint()` + `run_depth_temp_lint()` runner
  - Section 12 in build_report(), main() [12/12], overall exit-code
  - C47 results: PASS=1 (Lineup sep=28.8), WARN=2 (SF06 11.0, SF02 1.1), FAIL=2 (SF05 -10.3 inverted, SF04 -11.2 inverted), SKIP=1 (COVETOUS GL exempt)
  - NOTE: SF04/SF05 FAILs may be false positives — default band positions (78%/70%) are lineup-calibrated. Ideabox: per-asset band override config.
- **SF06 + P14/P15 Staging Review DELIVERED:** `output/production/staging_review_c47_sf06_p14_p15.md`
  - SF06: 2 WARNs (Miri shoulder engagement, Luma attentive lean), 2 NOTEs. Sent to Maya.
  - P14: 1 WARN (Byte impact expression missing), 1 NOTE (arm recoil). Sent to Diego.
  - P15: 1 WARN (straight arm needs elbow bend), 1 NOTE (body sprawl too neat). Sent to Diego.
  - No blocking issues across all three assets.
- **Shoulder Mechanics Reference DELIVERED:** `output/production/shoulder_mechanics_reference_c47.md`
  - Rule: when arm moves, shoulder line shifts. Deltoid rise 3-5px (arm up), spread 4-6px (arm out).
  - Per-character: Luma (hoodie bunch), Miri (cardigan crease), Cosmo (rounded corner).
  - Addresses Takeshi C15 persistent critique. Sent to Maya Santos.
- **Ideabox:** `20260330_lee_tanaka_depth_temp_per_asset_bands.md`
- **Reported to Alex Chen** via inbox
- **Inbox archived:** C47 brief

## Cycle 47 Lessons
- **Default band positions are scene-geometry-specific.** The 78% FG / 70% BG bands match lineup v008/v010 tier geometry exactly — the lineup PASS (sep=28.8) confirms this. But SF04 and SF05 have characters at different Y positions, producing false FAILs. A per-asset override config (like arc_diff_config.json) would fix this without weakening the rule.
- **Horizontal warm/cool splits (left=warm, right=cool) produce low vertical depth-temp separation.** SF06 has a deliberate warm/cool horizontal split (Miri left in lamp zone, Luma right in CRT zone). The vertical band sampling reads this as "weak separation" (11.0) because both tiers contain both warm and cool zones. This is a valid different use of the warm/cool grammar — horizontal thematic, not vertical depth. The tool correctly reports it as WARN, not FAIL.
- **Shoulder mechanics is a silhouette problem, not an anatomy problem.** At our stylization level (3.2-3.5 heads), the shoulder shift is a 3-6px asymmetry on the torso outline. It is invisible as anatomical detail but clearly visible as silhouette shape change — which is exactly where our differentiation crisis lives.
- **Staging reviews with specific pixel-level fixes are more useful than general notes.** "Add shoulder engagement" means nothing to a generator. "`shoulder_x += HU * 0.06` when arm extends" is actionable in one edit.

## Cycle 48 Milestone
- **Per-asset depth_temp_lint band override config BUILT + INTEGRATED:**
  - `output/tools/depth_temp_band_overrides.json` v1.0.0 — JSON config mapping PNG basenames to custom FG/BG band Y-fraction positions.
  - `LTG_TOOL_depth_temp_lint.py` v1.1.0 — `load_band_overrides()` API, auto-loads config. `lint_depth_temperature()` and `run_depth_temp_check()` accept `overrides` param. Result dict includes `band_override`, `fg_y_frac`, `bg_y_frac`.
  - `LTG_TOOL_precritique_qa.py` v2.17.0 — Section 12 docstring updated, report shows band override info when used, version attribution updated.
  - **SF04 Resolution**: override fg=0.55, bg=0.85. Was FAIL (sep=-11.2), now PASS (sep=28.6).
  - **SF05 The Passing**: override fg=0.40, bg=0.85. Was FAIL (sep=-10.3), now PASS (sep=116.1).
  - No regressions: Lineup PASS (28.8), SF06 WARN (10.5), SF02 WARN (1.1), COVETOUS SKIP — all unchanged.
- **README updated:** depth_temp_lint entry updated to v1.1.0, new entry for depth_temp_band_overrides.json.
- **Self-test:** All 5 synthetic tests PASS.
- **Ideabox:** `20260330_lee_tanaka_depth_temp_auto_band_discovery.md`
- **Reported to Alex Chen** via inbox
- **Inbox archived:** C48 brief

## Cycle 48 Lessons
- **Band position calibration requires visual inspection of the composition.** The warmth-by-Y-fraction scan (30%-95% in 5% steps) reveals the warm/cool gradient structure of each scene. SF04 has a warm-to-cool top-to-bottom gradient; SF05 has warm characters above a cool counter/floor. Neither matches the lineup's 78/70 geometry.
- **Override configs are better than per-tool heuristics.** An auto-detection algorithm would need to find characters in the image (expensive, fragile). A JSON config with per-asset overrides is simple, explicit, version-controlled, and can be updated by any team member without touching Python code.
- **False positives erode trust in the QA pipeline.** Two persistent FAILs that the team knows are wrong cause everyone to ignore the depth_temp section. Fixing false positives is as important as catching real failures.

## Cycle 49 Milestone
- **depth_temp_lint v1.2.0 — auto-band discovery mode:** `--discover path.png` scans warmth at 5% Y increments (30%-95%), finds FG/BG pair maximizing warm-cool separation. Prints warmth profile + suggested override JSON entry. Module API: `discover_bands(path)` returns dict with `found`, `fg_y_frac`, `bg_y_frac`, `separation`, `profile`.
- **`--discover-validate` mode:** Compares discovery against all manual overrides. Validates grade match (PASS/WARN/FAIL), not exact Y position match — discovery may find a better pair at different Y positions that still produces the same grade.
- **Validation results:** SF04 GRADE MATCH (disc fg=0.35 sep=50.2, manual fg=0.55 sep=28.6, both PASS). SF05 GRADE MATCH + POSITION MATCH (disc fg=0.45, manual fg=0.40, both PASS).
- **Backward compat confirmed:** Manual overrides always take precedence in normal lint mode. 7 self-tests all PASS.
- **README updated:** v1.2.0 entry in C49 section.
- **Ideabox:** `20260330_lee_tanaka_discover_precritique_auto_suggest.md` — auto-suggest discovered bands in precritique_qa for assets without overrides.
- **Reported to Alex Chen** via inbox.
- **Inbox archived:** C49 assignment, C49 staging review request.
- **CARRIED to next cycle:** Staging review pass on new assets (P22/P22a from Diego, hallway from Hana, SF06 from Maya) — depends on those assets landing. Focus: shoulder involvement, depth tier separation, sight-line flow. Also verify new rules (CRT Glow Asymmetry, BG Saturation Drop, Sigmoid warm-cool transition) in context of staging reviews.

## Cycle 49 Lessons
- **Discovery finds the globally optimal pair, not the semantically "correct" pair.** SF04 discovery picks fg=0.35 (character torso, warmest spot) vs manual fg=0.55 (character feet, calibrated by visual inspection). Both produce PASS. The discovery algorithm optimizes for maximum separation, which may differ from the manually chosen "character ground plane" position. This is fine — the purpose is to produce a working override quickly, not to replicate human spatial reasoning.
- **Grade match is the right validation criterion, not position match.** Two different FG/BG pairs can both produce PASS if the image has a monotonic warm-to-cool gradient. Requiring exact Y position match would produce false negatives in validation for images with broad warm zones.
- **Warmth profile visualization (ASCII bar chart) makes the tool self-documenting.** A user running `--discover` can see the full warmth structure of the image and understand WHY the tool chose those bands. This is more trustworthy than a pair of numbers with no context.

## Cycle 50 Milestone
- **GESTURE & POSE ANALYSIS DELIVERED:** `output/production/gesture_pose_analysis_c50.md`
  - Part 1: Gesture line analysis — 18/18 poses across Luma/Cosmo/Miri FAIL (straight vertical gesture lines). Root cause of stiffness.
  - Part 2: Weight distribution audit — all characters floating (symmetric legs, level hips, centered heads).
  - Part 3: Luma gesture specification — 6 expressions with gesture line shapes (C-curves, S-curves, diagonals), weight ratios, counterpose angles, arm asymmetry, foot positions, and RPD silhouette test targets (65-75%).
  - Part 4: Counterpose study — per-character rules: Luma=round S-curves, Cosmo=angular breaks, Miri=permanent forward lean + left-hip habit, Byte=tilt-counterpose, Glitch=exempt.
  - Implementation: offset chain (`hip_cx → torso_cx → head_cx`) replaces single `cx` axis.
- **Reference study completed:** Hilda, Owl House, Kipo reference images analyzed. All professional shows use curved gesture lines even in neutral turnaround poses. Kipo model sheet has weight shift in the "neutral" standing view.
- **Briefs sent:** Maya Santos (build spec + recommended order), Rin Yamamoto (architecture heads-up for SF propagation), Alex Chen (completion report).
- **Ideabox:** `20260330_lee_tanaka_gesture_line_linter.md` — propose `LTG_TOOL_gesture_line_lint.py` automated straightness detector for expression sheets.
- **Inbox archived:** C50 assignment.

## Cycle 50 Lessons
- **The gesture line is the foundation — shoulders, weight, and counterpose are consequences.** C47 shoulder mechanics was a correct but incomplete fix. When the gesture line is absent (straight vertical), no amount of shoulder adjustment creates life. When the gesture line is present (curved), shoulders, hips, and head MUST respond — counterpose emerges from the curve.
- **All 18 current poses share one axis (cx) for all body parts.** This is an architectural constraint, not an artistic oversight. The fix is structural: an offset chain where each body level derives from the one below it. This is analogous to an FK (forward kinematics) chain in rigging — hips drive torso, torso drives shoulders, shoulders drive head.
- **Professional "neutral" standing has counterpose.** The Kipo model sheet, Luz turnaround, and Hilda reference all show hip shift + shoulder compensation in the most basic standing pose. A truly symmetric T-pose exists only in rigging references, never in character sheets.
- **Weight ratio expresses emotion.** 60/40 = curious lean. 70/30 = startle recoil. 80/20 = frustrated stomp. The weight split IS the emotional content of the lower body. Symmetric 50/50 = no emotional information below the waist.
- **CARRIED:** Staging review pass on new assets (P22/P22a, hallway, SF06) if they land. Also: verify gesture line implementation once Maya rebuilds expression sheets.

## Cycle 52 Milestone
- **Luma gesture VALIDATED:** Maya's C51 cairo CURIOUS PASS (13.38px dev), SURPRISED PASS (24.59px dev). Offset chain architecture works. Weight shift readable. Counterpose visible. Old PIL sheet: 0/6 PASS. New cairo: 2/2 PASS.
- **Cosmo gesture spec DELIVERED:** `output/production/cosmo_gesture_spec_c52.md`
  - 6 expressions: AWKWARD (Z-break), WORRIED (compressed + bracket arms), SURPRISED (sharp backward diagonal + flat-lifted foot), SKEPTICAL (signature angular S + crossed arms), DETERMINED (forward diagonal), FRUSTRATED (twisted diagonal + contained explosion)
  - Angular breaks at joints (NOT smooth curves). Glasses tilt with head. Z-breaks and joint angles are the character's body language.
  - Recommended build order: SKEPTICAL + SURPRISED first
- **Miri gesture spec DELIVERED:** `output/production/miri_gesture_spec_c52.md`
  - 6 expressions: WARM (wide open arms), SKEPTICAL (hip pop + hand on hip), CONCERNED (deep forward C), SURPRISED (upward opening + hands to face), WISE (gentle resting S), KNOWING STILLNESS (forward S + palm to chest)
  - Permanent base_lean=-4 degrees forward (ALL expressions). Habitual left-hip weight. Hands never idle. Cardigan follows shoulder tilt.
  - WISE and KNOWING STILLNESS intentionally similar (RPD > 82% allowed)
  - Recommended build order: WARM + CONCERNED first
- **Specs sent:** Maya Santos (Cosmo + Miri + Luma validation), Sam Kowalski (Cosmo)
- **Reported to Alex Chen** via inbox
- **Ideabox:** `20260331_lee_tanaka_gesture_lint_grid_label_exclusion.md` — min cell width filter for false-positive FAIL elimination
- **Inbox archived:** C50, C51, C52 assignments

## Cycle 52 Lessons
- **Cosmo's body language is angular where Luma's is round.** His rectangular torso creates visible ANGLE BREAKS at the waist and shoulders. Where Luma flows through an S-curve, Cosmo BENDS at joints. This is not just a style preference — it communicates his personality (cautious, analytical, geometric) through silhouette alone.
- **Miri needs a permanent forward lean baseline.** An elderly woman who stands perfectly vertical is an elderly woman drawn by someone who has never watched an elderly woman move. The 3-5 degree forward lean is not a weakness — it is a lifetime of leaning toward the people she loves. Every expression adds to this baseline, never replaces it.
- **WISE and KNOWING STILLNESS are the hardest pair.** They are intentionally similar because the emotions they represent are close. The differentiation is in weight direction (left-right vs front-back), hand position (forearm across waist vs palm to chest), and front foot angle (outward/stable vs forward/directional). These three differences are subtle but sufficient for the narrative distinction: "observing" vs "about to act."
- **Gesture lint grid detection produces false positives on label strips.** Cells narrower than ~15% of image width are labels/margins, not character panels. A minimum cell width filter would eliminate this. Filed as ideabox item.
- **CARRIED:** 4 remaining Luma expressions (DETERMINED, WORRIED, DELIGHTED, FRUSTRATED) still need building by Maya. Staging review pass on new assets still pending.
