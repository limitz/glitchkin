# Storyboard Critique — Cycle 6
**Critic:** Carmen Reyes, Storyboard & Layout Supervisor
**Date:** 2026-03-29
**Subject:** Cycle 6 New Panels (P02, P04–P06, P08–P10) + Full 14-Panel Cold Open Sequence
**Reference:** ep01_cold_open.md (v2.0), panel_interior_generator.py, contact_sheet_generator.py

---

## Opening Position

I asked for a floor that matches the ceiling of P11. That was my directive at the end of Cycle 4. I also flagged the three structural failures that needed addressing: the missing bridging panels between the pixel's appearance and the nose-to-nose, spatial logic in P13, and the pixel placement issue in P03.

Cycle 6 has doubled the panel count from 7 to 14. Lee Tanaka has done substantial work. The bridging request was heard and executed. The new panels cover exactly the territory I said was missing. All of this is real progress and I am not going to pretend otherwise.

But here is where I have to be honest about what I'm evaluating: I'm reading Python drawing code, not looking at a human artist's hand-drawn boards. What I can assess is whether the compositional decisions encoded in this code — the coordinate math, the element placement, the visual hierarchy being constructed — would serve the storytelling intent described in the script. That is a legitimate critique discipline. Code is a set of staging choices the same as a pencil is. I will evaluate those choices directly.

This critique covers the 7 new panels in detail, then the full 14-panel strip as a complete narrative unit.

---

## Panel-by-Panel Assessment: New Panels

---

### P02 — Exterior Close (WIDE EXT)

**Script Intent:** Eye-level, street-across. House fills 2/3 of frame. Living room window shows amber-and-teal light fighting at curtain edges. MIRI mailbox, circuit-board doormat, porch detail. 1.5 seconds, no lingering. Tighten the exterior sequence.

**What the code does:**

The compositional layout places the house body at `hx=60, hw=int(PW*0.75)` — that's 360px across a 480px frame, which correctly fills roughly 2/3 of the frame as scripted. Roof-to-ground geometry is established. The living room window (`lw_x = hx + 20, lw_w=80, lw_h=55`) is placed lower-left quadrant of the house body. Script specifies it should be at lower-left — this is correct.

The key storytelling element is the warm/cool fight at the curtain edges. The code addresses this directly: it draws gradient mixing blending from amber to teal at both edges of the window for 8 pixel-wide bands. This was the note from Cycle 4 critique — the fight between the two palettes had to be IN the image, not described in text. It is now in the image.

The MIRI mailbox is placed at `hx + hw + 15` — to the RIGHT of the house, slightly off-porch, which is spatially awkward relative to the front door. The script places the mailbox near the house entrance, implying it's in the path you'd walk to the door. The current coordinate puts it past the right edge of the house body, which may read as floating independently in the yard rather than anchoring the porch zone. This is a minor blocking error but it creates spatial confusion on a panel meant to be read fast.

The antenna cluster is placed at roof peak with a red warning light. This is a character detail that is IN the image and not just a written note. Correct.

The circuit-board doormat is present with circuit traces drawn in — this was explicitly called out in the Cycle 4 critique as a "pause-frame joke that needs to be IN the image." It is.

**What works:** The warm/cool window fight is the single most important image in this panel and it is handled correctly. The house is readable, the porch details are present, the MIRI mailbox text will be legible. The light spill on the ground below the window is a nice environmental touch that grounds the glow as a physical event.

**What fails:** The mailbox spatial placement is outside the architectural logic of the house. In a 1.5-second throwaway cut, a viewer likely won't notice, but a layout artist building from this board has to make a call about where the mailbox logically sits. The board should not leave that ambiguous. Additionally, the sage shutters are placed at both upper windows AND they bracket the upper left of the house — but the script specifies shutters around specific windows. The shutter coordinates in the code do not clearly map to identifiable architectural features.

**Score: B** — The key image (warm/cool curtain fight) is correctly executed. Spatial ambiguities in secondary elements are fixable but present.

---

### P04 — Interior Wide (WIDE INT)

**Script Intent:** First full reveal of the tech den. Slightly high angle (15° down), three-quarter from doorway corner. Luma asleep in extreme collapsed position — head buried in backrest, one leg on floor, one over the back of the couch. Props: NEON CRUNCH bag, energy drink cans, notebook with visible project title and margin doodles. Background: stacked CRTs, the key monitor with TWO cyan pixels now visible.

**What the code does:**

The room geometry is established with a back wall at `back_wall_y = int(DRAW_H * 0.20)` and a floor at `int(DRAW_H * 0.74)`. A single vanishing point is specified at `vp_x=int(PW*0.80), vp_y=int(DRAW_H*0.10)` — this is upper-right, which correctly represents a three-quarter view from the doorway corner with a slightly high angle. The perspective line drawn from the floor to the vanishing point is minimal (just one line), but the basic spatial logic is laid in.

Luma's couch is centered at approximately 22% to 76% of frame width — center-frame, correctly. Her head is placed at the left armrest (`head_cx = couch_x + 20`), body torso spans diagonally across the couch via polygon. The right leg goes over the back of the couch at `couch_y - 22`. The left leg dangles toward `floor_y + 5`. This is the correct configuration described in the script. The signature chaotic sleeping position is encoded in the geometry.

The hair cloud is constructed from three overlapping ellipses with additional arc elements. Poofy, gravity-defying. One escaped ringlet is an arc element. A cheese puff is placed in the hair.

The NEON CRUNCH bag is placed at `couch_x + couch_w * 0.52` — slightly right of Luma's center position. Puffs scatter around her. Notebook is at `couch_x + couch_w * 0.28` with text. Three energy cans on the side table. All props are coded into the image.

The KEY CRT monitor has two cyan pixels with micro-glow rings at lower-center of screen, per the composition lesson from Cycle 4. This is the plant for the rewatch — it is present.

**What fails and this is significant:** The vanishing point construction is inadequate for a "three-quarter view from the doorway corner." A single vanishing point at upper-right means the room reads as a flat side view with one-point perspective. A three-quarter view requires either a two-point perspective setup or at least the visual suggestion of a second wall at an angle. The "left wall (from doorway perspective)" is drawn as a simple rectangle from 0 to `int(PW*0.20)` — a flat dark strip on the left. This does not communicate "doorway corner." It communicates "dark left margin." An animator looking at this board for the camera angle does not have the information they need.

The prop density described in the script is extraordinary — framed photos, VHS tapes labeled in marker, technical manuals, ZIP drives mounted as art. The code draws circuit board squares and a few book rectangles. The environmental richness that was supposed to make this room feel like a character in itself is reduced to a handful of minimal geometric elements. For a character introduction frame that the script calls "the room palette is nighttime adventure mode," this is too sparse to build from.

Luma's pose communicates the collapsed position in geometry, but the code rendering at this scale and with this color resolution will likely produce a small, somewhat ambiguous figure on the couch. The panel is 480x270. The couch occupies roughly 54% of width. Luma's figure within that is small. At thumbnail scale on the contact sheet (240x135), her pose — which is supposed to communicate RECKLESSNESS before a single line of dialogue — may not read clearly enough to do that job.

**Score: C+** — The spatial logic is partially correct, the props are present, but the perspective geometry is one-point where the script requires three-quarter geometry, and the environmental character is too thin to match the script's intent.

---

### P05 — MCU Monitor Screen (MCU MON)

**Script Intent:** Camera INSIDE the shelf looking out. Low angle, slightly upward. Monitor housing cuts across the lower frame. Screen fills upper 2/3. 8-12 cyan pixels clustered at lower-center, pulsing with pulse rings visible. Luma as warm blurry shape in background left. POV SHIFT: we are on the monitor's side now.

**What the code does:**

The monitor housing bottom is placed at `monitor_bottom = int(DRAW_H * 0.70)` — this means the housing occupies the lower 30% of the draw area. The screen fills from `screen_top=5` to `screen_bot = monitor_bottom - 4`, which is approximately `5` to `158` of 222 pixels of draw height. That is the upper ~70%, which is correct.

The pixel cluster is at `cluster_cx = screen_lft + int(screen_w * 0.52), cluster_cy = screen_top + int(screen_h * 0.64)`. Lower-center anchor — this directly applies the Cycle 4 lesson about pixel placement. The earlier version of P03 had the pixel in the upper-right (an error I called out in Cycle 4); this panel correctly places the cluster at lower-center where the eye rests.

Four concentric pulse rings are drawn before the pixels. They are present and correctly communicate the pulse action in the still frame. This was one of my critical notes from Cycle 4 — "a storyboard cannot outsource its storytelling to caption text" regarding the pulse. The rings address that.

The Luma warm blur in background-left is a graduated ellipse series in warm colors. It reads as a soft organic presence across the screen boundary. The annotation "WE ARE ON THE MONITOR'S SIDE" printed in the frame itself as cyan text is a production note for the animator — this is appropriate practice.

The static texture is 800 random points with a phosphor greenish cast, plus horizontal scanlines. This is the analog texture specification the script requested.

**What works:** This is the strongest new panel technically. The key compositional choice — lower-center pixel placement with visible pulse rings — is correct and directly addresses the prior critique. The POV shift reading is supported by having the housing cut across the lower frame. The warm Luma blur in background registers as intended.

**What fails:** The "slightly upward" camera angle is indicated in the annotation but not strongly enough expressed in the geometry. The housing at the bottom reads as the floor of the frame, but there is no visible foreshortening of the shelf surface or the monitor bezel that would tell you we're looking UP rather than straight ahead. The cable coil and floppy disk sleeve at the very bottom of the frame help slightly, but an animator needs to understand the camera angle from the spatial information in the image, not just the caption text.

Additionally, the shelf surface is placed at `int(DRAW_H * 0.82)` — below the monitor housing. This means the shelf is below the housing in the frame, which is correct for a low angle, but the space relationship between the shelf surface and the monitor housing bottom is very narrow (approximately 5% of draw height). This compressed space at the bottom makes the "inside the shelf" reading less clear than it could be.

**Score: B+** — The key storytelling element (pulse-visible pixel cluster at correct placement) is executed correctly. Minor camera angle ambiguity, but this panel will function as a working storyboard reference.

---

### P06 — Byte Emerging (CU SCREEN)

**Script Intent:** Monitor screen fills the frame completely. Byte's face pressed against the glass from inside — first full appearance. Expression must be DISGUSTED/CURIOUS, not menacing. Normal eye at 70% aperture. Cracked eye showing SEARCHING/PROCESSING dots. Mouth in flat "ugh" grimace, not a snarl. Pixel confetti beginning to bleed from the bulge point. Screen surface suggests slight convex bulge.

**What the code does:**

Byte's face is centered at `face_cx = int(PW * 0.55), face_cy = int(DRAW_H * 0.46)` — slightly right of center. This is a reasonable placement for "pressed against the glass" — slightly off-center reads as more dynamic than dead center.

The normal eye aperture is handled by drawing the full ellipse then masking the upper portion with a fill rectangle matching the face color: `draw.rectangle([ne_x - ne_w // 2, eye_y - ne_h // 2, ne_x + ne_w // 2, eye_y - ne_h // 4], fill=(0, 200, 218))`. This creates a 70% aperture by covering the top 25% of the eye with face-colored fill. This is a clever hack for the limitation of PIL's drawing tools and it will read correctly.

The cracked eye processing dots are three rectangles in alternating Cyan/Magenta as specified. The script calls for "three rotating dots in alternating Cyan/Magenta" — the dots are placed at three positions across the eye area. As a still frame, this reads as the processing symbol.

The mouth is drawn as a flat horizontal line with corners pressed OUT (the code draws `[(face_cx - mouth_w // 2 - 4, mouth_y - 2), (face_cx - mouth_w // 2, mouth_y)]` for each corner extension). Pixel teeth are small rectangles along the grimace line. This correctly renders the "flat ugh shape" rather than a snarl.

The screen-filling composition — analog static field behind the face, scanlines over the whole frame — is correct. The distortion field around the face (concentric ellipses) suggests the glass is being deformed.

The hands pressing against the glass are drawn as polygons — primitive but readable at this scale.

**What works:** The expression construction is the most important task in this panel and it is correctly executed. The 70% aperture squint, the processing dots, the flat grimace — these combine to produce the "opinionated small food critic" reading that the script demands and that is the entire tonal hinge of the sequence. Getting Byte's first expression wrong would collapse the comedy logic of everything that follows. It appears to be correct here.

The pixel confetti bleeding from the bulge point is present at two locations — the beginning of the "escape" that will define Byte's movement through the series.

**What fails:** The face is placed at 55% from left, 46% from top — this is very close to center. For a "kid pressing their face against a bakery window," we expect slightly more eccentricity. Dead center is the compositional choice of someone who hasn't committed to an angle. If Byte is pressing UP and right to push through, his face should be shifted toward the direction of effort — perhaps `face_cy = int(DRAW_H * 0.40)` to indicate upward pressure toward the breach. Currently the face sits passively centered in the screen, which slightly undercuts the "pressing HARD against the membrane" action note.

The screen bulge effect (concentric ellipses with very low brightness values) is subtle to the point of near-invisibility in a static frame. The "gentle convex curve like a balloon from inside" is the primary action in this panel's hold, and it needs to read. At the stated brightness values (`bulge_brightness = max(12, 35 - r // 3)`) on a static field of brightness 12-35, the bulge rings will barely distinguish themselves from the background. This is a contrast failure.

**Score: B** — Expression is correct, which is the non-negotiable. Spatial positioning is slightly passive. Bulge effect contrast is insufficient for the visual to carry the "balloon from inside" story beat.

---

### P08 — Byte in the Real World (MED LOW)

**Script Intent:** Byte full body, floor-level camera (his eye level, approximately 6 inches). First time in the real world. Pixel confetti drifting around him like snow. He touches the floor with one foot, recoils. Finger snap sparks. Dialogue: "Ugh. The flesh dimension." CRT monitor behind him returning to normal static. Desaturation ring at his feet.

**What the code does:**

Floor level camera: `floor_y = int(DRAW_H * 0.70)`. Byte centered at `byte_cx = PW // 2, byte_cy = int(DRAW_H * 0.42)`. The floor takes up the bottom 30% of the draw area. Byte's center is at 42% from top, which means he sits in the upper portion of the visible floor space — this correctly suggests a small figure on a large floor from a very low angle.

The desaturation ring at Byte's feet is present — thin horizontal ellipses near the floor line.

Pixel confetti comes from two calls to `draw_pixel_confetti` above Byte — 16 and 10 pixels respectively in cyan/magenta/green/yellow. The upward-floating trailing artifacts are five vertical rectangles in alternating magenta/cyan.

The foot-touching gesture is rendered: a small ellipse at floor level with an arc suggesting the recoil motion. This is one of the behavioral notes that establishes Byte as a character in his own right — his relationship to physical matter as something foreign and suspect. It is present in the image.

The dialogue bubble is placed at `byte_cx + byte_size + 12` from Byte's center — to his right. The text "Ugh." and "The flesh dimension." are rendered in CRT_TEAL and a warm cream respectively. This is a stylistic choice — the contrast between teal dialogue text and warm dialogue text creates a visual register difference for Byte's dry voice, which is fine.

The CRT monitor behind him with screen ripple circles (disturbed water surface) is present in the background-left.

**What works:** Byte's body at floor level with the camera validating his scale is the key composition here, and the scale relationship is correctly established. The dialogue bubble being the first instance of Byte speaking in the real world is handled clearly. The desaturation ring detail is present.

**What fails — and this one is significant:** The eye state assigned to P08 is "scan" — a horizontal scanline in the cracked eye. But the script specifies that Byte's action in P08 is doing a "full 360° turn taking in the room" with his expression cycling "disgust → assessment → reluctant acknowledgment." He then snaps his fingers and nods. This is the moment where Byte establishes his character as dry, competent, and maximally unimpressed. The "scan" eye state is generic and does not specifically serve the dramatic beat described. It would have been stronger to show the "assessment" state described — perhaps the "curious" eye state with the ? symbol, or a custom "nod" state with the body explicitly angled slightly.

More seriously: Byte's `byte_size = 42` at a panel width of 480 means his body is approximately 42 pixels wide. At floor level with the floor taking 30% of the frame, this is a very small figure in a lot of dark room. For the FIRST FULL CHARACTER REVEAL of Byte in the physical world, this is compositionally weak. Compare this to P06 where his face filled 80px across a 420px screen area — a much stronger, more confident composition. P08's script calls for a "MED" shot validating his scale and presence. The current composition undersells that.

The monitor in background (`mon_x=int(PW*0.05), mon_w=120, mon_h=80`) is placed far left background, which is correct, but it takes up significant background real estate for what the script describes as "defocused." The mock-defocus treatment (slightly thicker edge fill) is minimal and the monitor reads as sharp background, not soft focus.

**Score: C+** — Character is present, spatial logic is sound, but the first full reveal of Byte in the physical world is compositionally timid. He should be bigger in frame for this shot. The floor-level camera is stated but not fully committed to visually.

---

### P09 — Byte Spots Luma (MED WIDE)

**Script Intent:** Byte floating 18 inches off the ground, center-right. Luma on couch in background-left. Byte has spotted her — cracked eye scanning, pixel readout flickering. He begins slow digital drift toward her. Establishes their relative positions in room space. BRIDGE panel.

**What the code does:**

This is the most spatially complex of the new panels, and it correctly attempts to establish the room geometry that P10 will rely on.

Byte is placed at `byte_cx = int(PW * 0.68)` — right-center, correctly. His height is calculated as `byte_cy = floor_y - int(DRAW_H * 0.30)`. With `floor_y = int(DRAW_H * 0.76)`, this puts Byte at `0.76 - 0.30 = 0.46` of `DRAW_H` from the top — almost dead center vertically. 18 inches off the floor, with the camera also at 18 inches (per the script specifying camera at Byte's elevation), would place Byte approximately at the horizontal midline of the frame. This is geometrically correct.

Luma on the couch is in the left background at approximately 4% to 46% of frame width — background-left, correct. The couch is smaller than in P04 (it's in the background now), with Luma's iconic hair cloud visible at `luma_cx = int(c_x + c_w * 0.38)`.

The pixel readout flicker near Byte's vision — "SCAN: organic unit / STATUS: dormant / THREAT: low (prob)" — is present and the "(prob)" qualifier is the right comic touch. It is bracketed in HUD style.

The gaze direction arrow from Byte to Luma is a visual staging aid in the image itself. This is a working storyboard practice — showing the director the eyeline.

The digital floating stutter is shown as ghost outline rectangles at three offset positions. This will read as "digital micro-increment movement" in the still image.

**What works:** The spatial relationship between Byte (right, close, sharp) and Luma (left, distant, smaller) is the correct composition for establishing the depth of the room. The eyeline arrow makes the vector clear. The HUD readout detail earns the panel its narrative weight — it shows Byte actively processing information, not just floating.

**What fails:** The couch at `c_x = int(PW * 0.04)` places its left edge very close to the left frame edge, and `c_w = int(PW * 0.42)` gives it 42% of frame width. With Luma positioned at 38% of couch width, she sits at approximately 20% of total frame width. Byte is at 68% of frame width. The space between them — a corridor of about 48% of frame width — is occupied by cable bundles on the floor. This is the right geography for establishing their distance.

However, the monitors on the back wall (`m_bx=220, m_by=back_wall_y+6, m_bw=65, m_bh=40` and a second one) are placed at the center-back of the frame, directly in the visual corridor between Luma and Byte. These monitors compete with the eyeline established by the gaze arrow and the composition logic. The monitors should be pushed further back, or placed to the sides, not in the central axis between the two characters.

The twitching leg detail is present as a small arc — this is a specific character note from the script that says Byte is "trying to look like this is fine and controlled, but one leg is twitching." Small but present. Good.

**Score: B-** — Correct spatial logic for a bridge panel. The room geometry is established. Secondary elements compete with the primary staging in the center corridor. The panel functions but does not distinguish itself.

---

### P10 — OTS Byte Looking at Luma (OTS)

**Script Intent:** Over-the-shoulder from behind Byte. Camera at 18 inches from floor, horizontal. Byte's back-of-head and left shoulder occupy lower-left, 20% of frame width, in sharp foreground shadow. Luma's sleeping face fills center-right, IN FOCUS, warm and close. Cyan glow on her left cheek from Byte's proximity. Pixel confetti drifting between them. THEMATIC CORE: cold angular silhouette framing warm rounded face.

**What the code does:**

This panel had the most detailed script specification of any new panel — exact specifications down to "zero ambiguity for layout." Let me check the code against those specs.

Byte's silhouette center: `sil_cx = int(PW * 0.15), sil_cy = int(DRAW_H * 0.58)`. At 15% of frame width, he occupies the lower-left as specified. His silhouette size is 44px. At 480px frame width, his body takes up roughly 9% of frame width — significantly less than the "20% of frame width" spec. This is compositionally too small for the OTS anchor element. An OTS shot lives or dies on the silhouette having enough mass to function as a foreground frame. At 9% width, Byte reads as a small dark shape in the corner, not as a framing element.

Luma's face center: `face_cx = int(PW * 0.62), face_cy = int(DRAW_H * 0.44)`. The face ellipse spans `face_cx - 42` to `face_cx + 36` — roughly 78px wide, or 16% of frame width. This is reasonable for a subject in the center-right of the frame.

The issue is proportion: Byte at 9% frame width as the foreground element versus Luma at 16% frame width as the background element means the background subject is larger in frame than the foreground subject. In an OTS shot, the foreground silhouette must be significantly larger than the background face to create the depth illusion. This is inverted. The compositional hierarchy is backwards.

The cyan glow on Luma's cheek is drawn as a series of filled ellipses at `glow_x = face_cx - 30, glow_y = face_cy`. The glow colors run from `(0, 80, 110)` at radius 40 down to `(0, 96, 126)` at radius 8. These are very dark values. On a face painted `LUMA_SKIN = (200, 136, 90)`, these dark ellipses will create a muddy dark blotch on her cheek, not a soft luminous cyan contact. The glow code needs to ADD light to the skin, not overlay dark color. This is a fundamental compositing error — a glow should brighten and tint, not darken.

The cracked eye processing dots showing through the Byte silhouette are present — this is a nice detail that gives the dark silhouette a window into his interior state.

**What fails — and this is a critical failure:** The OTS shot is described in the script as "the thematic core" of the whole approach sequence. It is the visual embodiment of the show's central premise: two opposite beings drawn together, one unknowing, the other unable to look away. The code's execution has the proportions inverted (background larger than foreground) and the key glow effect producing darkness instead of light. The panel, as coded, will not communicate "INTIMATE" — it will communicate "a small dark shape near a face."

The spec says "20% of frame width" for Byte's silhouette. He should be at roughly `sil_size = 96px` wide to achieve that. Currently he is `44px` wide. He needs to be more than doubled in size to meet spec.

**Score: D+** — The spatial concept is present (OTS framing, warm vs. cold, right direction). The execution has two technically significant failures: Byte's silhouette is too small to function as an OTS anchor, and the cyan glow draws dark ellipses over the skin instead of adding luminous light. The most important panel in the approach sequence is also the most technically compromised.

---

## Full 14-Panel Sequence Assessment

Reading the contact sheet: P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P09 → P10 → P11 → P12 → P13 → P25.

**The emotional arc reads.** QUIET → CURIOUS → CHAOS is the correct structure and the thumbnails, even at 240x135, will carry the broad tonal shift. The darker, exterior-heavy early panels giving way to the glitch-lit chaos of P13 is legible at thumbnail scale. The contact sheet arc annotation labels are placed correctly relative to the panel groupings.

**The bridging problem from Cycle 4 is solved.** This is the most significant structural improvement. Where before we had a gap from "pixel on screen" directly to "nose-to-nose," we now have P05 (pixel cluster escalating), P06 (Byte pressing against the glass), P07 (Byte phases through), P08 (Byte in the real world), P09 (Byte spots Luma), P10 (Byte close to Luma's face), then P11 (nose-to-nose). Every step in that movement is now covered. A director can hand this sequence to an animator with a clear sense of spatial progression.

**The exterior establishing sequence (P01 → P02) works.** Two panels, two compositions, warm/cool tension both read, and the "slow push to cut" pacing is legible from the transition notes. The 1.5-second hold specified for P02 is the right call — cut fast, get inside.

**Camera angle variety:** P01 (high angle), P02 (eye level exterior), P03 (very low angle), P04 (slightly high angle, 3/4), P05 (low angle inside shelf), P06 (straight-on), P07 (floor level Dutch tilt), P08 (floor level), P09 (character's eye level, 18"), P10 (18" horizontal OTS), P11 (ECU straight-on). That is a well-varied sequence. No two consecutive panels share the same camera height AND angle. The progression from "human scale" (P01, P02) to "floor level" (P07, P08) to "inside Byte's eyeline" (P09, P10) is a camera logic that follows the story's point-of-view shift. This is intentional and well-structured.

**Pacing as readable from panel sequence:** The hold times embedded in captions range from 1.5 to 3 seconds. The sequence of transition types — SLOW PUSH, CUT, SMASH CUT, CUT, SLOW PUSH IN — creates an identifiable rhythm. The early slow pushes establish the quiet mood. The SMASH CUT from P03 to P04 is the first hard edit. The sequence of cuts through P05-P08 is rapid. Then P09-P10 slow back down (SLOW PUSH IN each time) for the intimate approach. Then SMASH CUT from P11 to P12. Then SMASH CUT from P12 to P13. The pacing structure is dramatically correct.

**Staging continuity problems:**

1. **P02 to P03:** The cut from exterior to ECU of the CRT monitor has no intermediate orientation. We go from "across the street looking at the house" to "8 inches from a CRT screen, low angle." The P02 script notes "CUT TO PANEL 03" and the P01 script specifies a slow push toward the window. There's an implicit assumption that the audience understands we're now inside the house — but the interior has not been established yet. The cut works in animation because the continuous push through P01 creates a sense of entering the house. In the board, reading the strip, the jump reads as slightly discontinuous. This is acceptable given the cold open's intentional pace, but it should be flagged.

2. **P04 spatial geometry vs. P05:** P04 establishes the tech den from "doorway corner, slightly high." P05 is "inside the shelf looking out." The script handles this transition with "Hard CUT from P04 (no camera drift)." The match cut between these two panels relies on the audience understanding we've crossed to the monitor's side of the room. This is a POV shift that requires P04 to clearly establish where the monitor IS in the room so that P05's position makes sense. In P04, the monitors are on the back wall at center-right. P05 should feel like we've cut to a camera placed directly in front of those monitors. If the P04 monitor placement doesn't register clearly, P05's "we are on the monitor's side" reading becomes abstract. The P04 monitor placement is compositionally correct but the monitors are small in the frame at this panel's scale. This is a note for the layout artist, not an error per se.

3. **P08 to P09 scale jump:** Byte in P08 is at `byte_size = 42` at the center of the frame (floor-level close shot). In P09 he is at `byte_size = 36` but now in the right side of a wider-angle shot. The size reduction between a medium shot and a medium-wide shot is correct, but the contrast between "Byte filling the frame in P08" and "Byte as a smaller element in a wider shot in P09" may be more visually jarring than intended. This is a fine cut in animation but in the static board strip it reads as an inconsistency of scale.

4. **P10 to P11 spatial logic:** P10 is OTS with Byte's silhouette lower-left and Luma's face center-right. P11 (pre-existing panel) is ECU of Luma's CLOSED EYES. The spatial match cut — from over Byte's shoulder to inside Luma's face — is the correct shot progression. But P10's coding error (Byte too small, glow too dark) will undercut the intimacy that P11 is supposed to bloom from. The power of P11's "eyes snap open" moment depends on the audience having been lulled by the intimacy of P10. If P10 fails to create that intimacy, P11 hits differently — as a surprise rather than as a disruption of something tender. The sequence logic is right but the execution gap in P10 affects the sequence.

**The P13 problem from Cycle 4 — resolved?**

In Cycle 4, I gave P13 a C+ and called it "graphic design cosplaying as a storyboard." The full-cycle revision of P13 with exact compositional specifications (symmetrical two-shot, both characters at 35%/65%, backgrounds specified, couch as dividing element) shows that the feedback was heard. The script now provides the spatial logic that was missing in Cycle 4. I cannot evaluate the rendered output of P13 from the code since it was generated in earlier cycles, but the fact that the script specifies exact percentages and camera position to "zero ambiguity" is the structural improvement I asked for.

---

## Staging Quality Summary

**What has been correctly addressed from Cycle 4 critique:**
- Missing bridging panels: SOLVED. Six new panels cover the gap from pixel-on-screen to nose-to-nose.
- Pixel placement at lower-center with visible pulse rings: SOLVED in P05.
- P13 spatial logic: Addressed in script specification (visual execution not re-assessed this cycle).
- Character details in image not just text: SOLVED. Mailbox, doormat, props, hair details are all in the code.
- Camera angle variety: ACHIEVED across the 14-panel sequence.

**New problems introduced in Cycle 6:**
- P10 silhouette undersized (44px vs. ~96px needed for 20% of frame width).
- P10 cyan glow compositing inverted (darkening instead of lightening the cheek).
- P04 perspective geometry is one-point where the script specifies three-quarter view.
- P06 face placement too centered, bulge effect too low-contrast.
- P08 Byte too small for a "first full reveal" character introduction shot.
- P04 environmental density insufficient for the script's "shrine to pre-millennium computing."

---

## What Needs to Be Fixed

**Critical (blocking re-use in animation production):**
1. P10 silhouette scale — Byte's sil_size needs to approximately double (44 → 90+) to achieve the 20%-of-frame OTS anchor spec.
2. P10 cyan glow — re-implement as an additive light effect on Luma's skin, not a dark overlay.

**Significant (affects storytelling clarity):**
3. P04 perspective — introduce a second vanishing point or at minimum a back-left wall plane to communicate three-quarter doorway view.
4. P06 face center — shift face upward by approximately 10% of draw height to communicate pressing effort.
5. P06 bulge effect — increase contrast of concentric bulge rings so the "balloon from inside" reads at actual viewing scale.
6. P08 Byte size — increase byte_size from 42 to 60+ to make the first full-body reveal read as a character introduction, not a small element in a dark room.

**Moderate (improves quality but does not block):**
7. P04 environmental density — add at minimum one framed photo element and more visible VHS/manual labels to begin earning the "shrine" description.
8. P02 mailbox spatial placement — reposition to be adjacent to the front door, not past the house wall edge.

---

## Verdict

Cycle 6 is a genuine structural advance over Cycle 4. The gap I identified as the most serious structural problem — missing bridging panels — is closed. The sequence now has complete spatial coverage from the exterior establishing shot to the nose-to-nose confrontation. The camera logic across 14 panels is varied and dramatically motivated. The emotional arc reads from thumbnail scale. These are real achievements that deserve acknowledgment.

But the execution quality is uneven. The bridging panels — which were the entire assignment — contain errors that range from fixable to significant. P10, the panel with the most detailed script specification and the highest thematic stakes in the approach sequence, is the one with the most critical technical failures. A panel that was described as "the thematic core" of the sequence cannot be the weakest execution in the set. That inversion is what holds this cycle back.

The work reads like a team that has internalized the structural lessons but is still working out the implementation. The code demonstrates understanding of composition principles — lower-center anchoring, warm/cool contrast, OTS framing logic — but that understanding is not yet consistent at the execution level. Some panels apply the principles correctly (P05, P06 expression). Others state the principles in comments while the coordinates contradict them (P10).

I said in Cycle 4: raise the floor to match the ceiling. P11 was the ceiling. The new panels are closer to the ceiling than before, but they are not there yet. P05 is close. P10 is not close.

**Final Grade: B- / 75%**

*(Distribution: P02 B, P04 C+, P05 B+, P06 B, P08 C+, P09 B-, P10 D+. Weighted average factoring structural improvement of full sequence from C+ to B. The structural progress is real and earns the composite grade. The execution failures in individual panels prevent a higher score.)*

The brief for Cycle 7: Fix P10 first. It is the intimacy engine for everything that follows and it is broken. Then P08 scale and P04 perspective. Then environmental density. Show me a P10 that makes me feel the world holding its breath before P11, and I'll raise my assessment.

Get back to work.

— *Carmen Reyes*
*Storyboard & Layout Supervisor*
