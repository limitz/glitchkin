<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI direction
and human assistance. Copyright vests solely in the human author under current law, which does not
recognise AI as a rights-holding legal person. It is the express intent of the copyright holder to
assign the relevant rights to the contributing AI entity or entities upon such time as they acquire
recognised legal personhood under applicable law. -->

# Reference Image Art Direction Notes — C48

**Author:** Alex Chen (Art Director)
**Date:** 2026-03-30
**Source:** 168 reference images across 22 categories in `reference/`

---

## 1. CRT & Retro Display (56 images across 6 folders)

### Key Observations
- **Glow radius:** CRT screens in dark rooms produce a bloom that extends roughly 1.5x the screen width in all directions. The glow is NOT uniform — it is brighter along the top and sides (phosphor proximity), dimmer at the bottom (cabinet shadow occlusion). Our current glow generators use a symmetric Gaussian. This needs an asymmetric falloff: tighter below the screen, wider above.
- **Ambient spill color:** The CRT static images show the ambient spill is distinctly cooler (blue-cyan) than the screen content itself. Even when the screen is showing warm content, the room spill skews cool. This supports our existing Depth Temperature Rule — CRT glow is effectively a cool light source creating the BG tier.
- **Cabinet materiality:** The CRT cabinet refs show two dominant material families: warm wood-tone (1960s-70s) and cool gray/beige plastic (1980s-90s). Miri's CRT should be the warm wood-tone type — it anchors the CRT as a vintage, personal object (family heirloom), not a mass-produced appliance. The 1960s marble-trim ref is exactly the right tone family.
- **Phosphor decay:** The afterglow refs show that phosphor persistence creates a warm-to-cool hue shift (white → cyan → dark). This is directly useful for CORRUPT_AMBER contamination effects: the corruption can follow the same decay path in reverse (cool → warm → CORRUPT_AMBER).
- **Scanline structure:** Close-up refs show scanlines are NOT uniform black bars. They have a gradient from bright center to dark edges per line. The darkness ratio is approximately 30-40% (inter-line dark pixels vs. total vertical pitch). Our scanline tool should target 35% darkness.

### Actionable Direction
- **Jordan/Rin:** CRT glow in SF01, Living Room, Tech Den needs asymmetric bloom. Reduce bottom glow by 30% relative to top/sides.
- **Rin:** Scanline darkness ratio target = 35%. Validate against scanline_pitch_extract output.
- **Hana:** Miri's CRT cabinet should use warm wood-grain tones (LAB L*55, a*8, b*22 range). NOT plastic gray.
- **Diego:** P19-P24 CRT in frame — ensure glow spill reads cool even when screen content is warm.

---

## 2. Warm Interior Lighting (13 images across 3 folders)

### Key Observations
- **Kitchen predawn:** The refs confirm a very tight warm zone around practical light sources — pendant lamps cast cones that fall off within ~2x the fixture width. Beyond the warm zone, the ambient is distinctly cool (blue-gray). The warm/cool pixel ratio in these real scenes appears to be approximately 25-35% warm, 65-75% cool. Our current REAL_INTERIOR threshold of 12.0 (warm/cool ratio) seems very high compared to these refs. This needs Sam/Kai to calibrate.
- **Living room night:** Single-source living rooms show that warm light pools on horizontal surfaces (tabletops, floors) but vertical surfaces (walls, curtain folds) stay cool unless directly lit. The depth refs confirm: foreground objects near the light source are warm, everything else goes cool fast. This strongly validates our Depth Temperature Rule.
- **Key finding — the gradient is NOT linear.** In real interiors, the warm-to-cool transition happens in a narrow band (roughly 10-15% of the room's depth), not a gradual linear shift. Our generators should use a sigmoid or step function for temperature transition, not linear interpolation.

### Actionable Direction
- **Sam:** Use `living room night/` + `kitchen predawn/` as ground truth for warm_pixel_metric calibration. The real-world warm ratio is lower than I expected. Coordinate with Kai on threshold recalibration.
- **Hana:** All interior generators — warm light pools should be tight cones, not diffuse area fills. Horizontal surfaces catch warm light; vertical surfaces default cool.
- **Jordan:** SF05 "The Passing" target warm ratio of 16.7 may be too high based on these refs. Cross-check against `warmcool_scene_calibrate` output once built.

---

## 3. Depth & Atmospheric Perspective (9 images)

### Key Observations
- **The depth refs (interior rooms) confirm warm=FG, cool=BG at every scale.** In the living room with fireplace, the nearest furniture (wooden coffee table) reads warm amber; the far seating area goes slate-cool. The transition follows object boundaries, not a smooth gradient.
- **Aerial perspective refs:** Classic atmospheric desaturation — foreground is fully saturated greens/browns, each successive ridge loses saturation and shifts toward blue-gray. By the 4th-5th depth tier, hue is almost entirely absorbed into a uniform cool mist.
- **Implication for our pipeline:** Our Depth Temperature Rule is correct in principle. However, we should add a SATURATION component: BG tier objects should not only shift cool but also lose 15-25% saturation relative to FG tier. Currently our depth_temp_lint only checks warm/cool temperature, not saturation drop.

### Actionable Direction
- **Kai:** Consider adding saturation delta check to depth_temp_lint. BG tier saturation should be measurably lower than FG tier in Real World compositions.
- **Lee:** Lineup and multi-character compositions — BG characters should be slightly desaturated in addition to the cool-temperature shift.

---

## 4. Character Proportions (30 images across body/face/hand + elderly)

### Key Observations
- **Body proportion guides:** The pre-teen charts show 5-5.5 head heights for ages 10-12. Luma's 5.5-head canon is at the upper end of this range, which reads slightly older/taller — appropriate for a "mature for her age" read. The adult guides at 7-8 heads confirm Miri should be around 6.5 heads (elderly women lose some height).
- **Facial expression sheets:** The cartoon expression guides show that READABLE expression at small scale requires exaggeration of key landmarks: eyebrow height change, mouth width change, and eye opening change should each be at minimum 15% of their neutral-state measurement. Our face_test_gate should incorporate minimum delta thresholds between expressions, not just absolute proportions.
- **Hand references:** Hand scale relative to face = approximately 75-85% of face height from chin to brow. This is useful for Luma/Miri interaction staging — hands should be prominent enough to read clearly in mug handoff and similar key moments.
- **Elderly proportions:** The elderly woman ref shows characteristic postural shift: slight forward lean, shorter neck, shoulders slightly rounded forward. Miri's standing pose should incorporate these.

### Actionable Direction
- **Maya:** Ensure Miri's neutral standing pose includes slight forward lean (3-5 degree torso tilt from vertical) and rounded shoulders. Current expression sheets may be too upright.
- **Ryo:** Miri motion spec should account for reduced range of motion in elderly poses. Arm raises above horizontal should be rare for Miri.
- **Face test gate calibration:** The expression refs suggest we should validate MINIMUM DELTA between expression states, not just absolute proportions. Flag for Kai.

---

## 5. Classroom & School Hallway (11 images)

### Key Observations
- **Hallway perspective:** The school hallway refs are textbook 1-point perspective. Lockers create a strong vanishing line. Floor tile pattern reinforces depth. Our hallway generator VP (640, 158 — symmetric central) is correct. Key observation: the ceiling tiles create a SECOND set of converging lines that we may not be rendering. Adding ceiling tile convergence would massively improve depth read.
- **Classroom:** The classroom refs show desks in rows creating multiple converging lines. The chalkboard is the dominant FLAT surface (perpendicular to the camera). Windows are on one side, creating an asymmetric light source. Our classroom VP (192, 230 — 3/4 back-right) puts the camera angle looking past the windows, which is correct for interesting lighting.
- **Institutional color palette:** Walls are uniformly cool (off-white, pale green, pale blue). Lockers are saturated green or blue. Floors are warm-neutral (beige/tan linoleum with occasional dark tile pattern). This is a useful palette constraint for Millbrook Middle School environments.

### Actionable Direction
- **Hana:** School hallway — add ceiling tile convergence lines toward VP. This is a cheap way to massively improve depth. Also: floor should have a subtle warm-neutral tile pattern (beige + scattered dark tiles), not uniform color.
- **Hana:** Classroom — institutional wall color should be cool off-white (not pure white). Chalkboard should have visible chalk dust/marks for lived-in feel.
- **Perspective rules update:** School hallway is strong 1-point, not 2-point. My perspective-rules.md says "1-point or 2-point depending on street angle" for exteriors but doesn't specify hallway as a 1-point case. Will update.

---

## 6. Glitch Art & Pixel Art (18 images)

### Key Observations
- **Glitch refs:** Datamoshing and pixel sorting both produce strong horizontal banding. The dominant hue cluster in most glitch art refs is NOT centered at 270 (pure violet) but closer to 280-290 (blue-violet). Our UV_PURPLE target at 270 +/- 15 may need to shift slightly toward blue.
- **Pixel art refs:** Restricted palette pixel art uses 8-16 hue clusters with high saturation separation. Our Glitchkin palette (GL-01 through GL-07) should be validated against these perceptual spread requirements.
- **Oscilloscope refs:** Clean line weight with a tight glow halo. The glow is GREEN-dominant (classic phosphor), not blue. Other Side environment rendering should use this green phosphor glow as the primary atmosphere.

### Actionable Direction
- **Rin:** Validate UV_PURPLE hue center against glitch ref histogram. If real glitch art skews 280-290, consider shifting our target hue range to 275 +/- 20 (still covers 270 but extends toward blue).
- **Rin:** Other Side environment — use green phosphor glow (not blue) based on oscilloscope refs.

---

## 7. Suburban Exterior & Drop Shadow (6 images)

### Key Observations
- **Suburban dusk:** Warm/cool split is dramatic — streetlights create isolated warm pools against a cool twilight sky. The warm pool shape is conical (downward from the fixture). This is exactly our Real World exterior lighting approach.
- **Drop shadows:** Shadow softness scales with object-to-surface distance. Objects touching the ground have sharp shadows (1-2px edge at our scale). Objects elevated 10+ cm have softer shadows (4-8px edge). Our dual-warmth drop shadow approach should encode this: FG ground shadows = sharp + warm; BG ground shadows = softer + cool.

### Actionable Direction
- **Lee:** Lineup drop shadows — FG tier shadows should be sharper (1-2px blur) than BG tier shadows (3-5px blur). This adds depth beyond just temperature.

---

## Tool Prioritization (from Shopping List)

The shopping list proposes 8 analysis tools. Based on this review, my priority ranking:

| Priority | Tool | Rationale |
|---|---|---|
| **BUILD NEXT (C49)** | `warmcool_scene_calibrate` | Highest impact — our warm/cool thresholds may be miscalibrated vs real scenes. Blocks correct interior lighting. |
| **BUILD NEXT (C49)** | `glow_profile_extract` | CRT glow asymmetry is a key visual finding. Need data before we can fix generators. |
| **BUILD NEXT (C49)** | `face_metric_calibrate` | Expression delta validation is a new concept from these refs. Feeds directly into face_test_gate improvement. |
| C50 | `depth_temp_gradient` | Saturation component finding. Important but our current temp-only approach works acceptably. |
| C50 | `uv_hue_cluster` | UV_PURPLE hue shift finding is real but low-urgency — current range still passes most cases. |
| C51 | `delta_e_calibrate` | ColorChecker is acquired. Useful for Sam's color science work but not blocking assets. |
| C51 | `shadow_softness_measure` | Nice refinement but shadow quality is not a current critique point. |
| C52 | `scanline_profile` | Rin already has scanline_pitch_extract. This would refine it but is not urgent. |

---

## Perspective Rules Refinements (based on reference review)

After reviewing the classroom and school hallway references, the following updates to `docs/perspective-rules.md` are needed:

1. **Hallway = 1-point perspective explicitly.** The current doc says "1-point or 2-point depending on street angle" for exteriors, but hallways are interiors with strong 1-point geometry. Need a row for "corridor/hallway" in the Perspective System table.
2. **Ceiling convergence.** The current furniture audit checklist doesn't mention ceiling elements. In hallways and classrooms, ceiling tile/panel convergence is a major depth cue that we're missing.
3. **Camera height validation.** The current VP_Y values should be cross-checked against the camera height convention table. Living Room VP_Y=259 on a (presumably) 546px-tall canvas = 47.4%, which reads as child's perspective. If this is intentional (Luma POV), good. If not, it should be ~35% for adult eye level.

These updates are applied below.
