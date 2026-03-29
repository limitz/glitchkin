# MILLBROOK MIDDLE SCHOOL — Interior Environment Design
### "Luma & the Glitchkin" | Background & Environment Design
**Artist:** Jordan Reed | **Date:** 2026-03-29 | **Version:** 2.0

---

## Production Specifications

| Spec | Value |
|---|---|
| **Canvas size** | 1920 x 1080 px (16:9, 1080p HD) |
| **Print-ready resolution** | 300 DPI |
| **Screen delivery resolution** | 72 DPI |
| **Color space** | sRGB |
| **Master file format** | PSD with named layers (see layer naming below) |
| **Working file bit depth** | 16-bit PNG / PSD |
| **Delivery format** | 16-bit PNG sequences |
| **Web/presentation export** | 8-bit PNG |
| **Primary painting software** | Krita (backgrounds, color keys, character sheets) |
| **Primary animation software** | OpenToonz (character animation, scene assembly) |
| **Compositing software** | Natron (final composite, color grade) |

> **Blend mode note:** All blend mode references in this document (Multiply, Screen, etc.) refer to Natron's blend mode terminology, which follows the industry-standard naming convention consistent across open source compositors.

### Naming Convention — This Environment
Two sub-locations are each a separate deliverable under the unified LTG convention.

**Sub-location A — Hallway:**
- **Filename convention:** `LTG_ENV_school-hallway_v###.psd`
  - Example: `LTG_ENV_school-hallway_v001.psd`
  - Example: `LTG_ENV_school-hallway_v002.psd`
- **Delivery PNG:** `LTG_ENV_school-hallway_v###.png`
- **Shot codes in use:** `WIDE_ESTAB` / `MED_LOCKER_LUMA` / `MED_LOCKER_147` / `CU_LOCKER_DETAIL`

**Sub-location B — Classroom:**
- **Filename convention:** `LTG_ENV_school-classroom_v###.psd`
  - Example: `LTG_ENV_school-classroom_v001.psd`
  - Example: `LTG_ENV_school-classroom_v002.psd`
- **Delivery PNG:** `LTG_ENV_school-classroom_v###.png`
- **Shot codes in use:** `WIDE_BACK_CORNER` / `MED_LUMA_DESK` / `MED_FRONT_BOARD` / `CU_BOARD` / `CU_PLANT`

> **Note on internal PSD layer naming:** The layer naming conventions inside the files (e.g. `MS_HAL_BG`, `MS_CLS_MG_CHAR`, `MS_CLS_GLITCH_EP##`) remain unchanged. These are intra-file identifiers, not filenames. The `LTG_ENV_` convention applies to filenames only.

### Required PSD Layer Structure
All master PSDs for this environment must include the following named layer groups, in order from top to bottom:
1. `FG` — Foreground locker/desk edges, coat rack, nearest objects
2. `MG_CHAR` — Character plane (empty — reserved for animation)
3. `MG_BG` — Midground furnishings, lockers, desks
4. `BG` — Background wall details, far lockers, front wall/board
5. `WINDOW_LIGHT` — Natural light shaft overlays (warm gold parallelograms) — screen layer
6. `FLUORO_LIGHT` — Fluorescent light pools on floor — screen layer
7. `SHADOW_OVERLAY` — Cast shadow shapes — multiply layer
8. `BASE` — Base color shapes (walls, floor, ceiling)
9. `GLITCH_ESCALATION` — (Separate, episodic overlay) Cyan glow on locker 147, plant bioluminescence, board ghost text. Updated per episode. Named `MS_CLS_GLITCH_EP[##].psd`.

---

## Overview & Design Intent

The school is the "normal life" counterpoint to the glitch adventures. Luma and Cosmo come here to try to be regular kids between extraordinary events. The design should communicate: institutional, slightly underfunded, full of personality despite (or because of) that underfunding.

The key emotional dynamic here is CONTRAST. After the wild visual intensity of the Glitch Layer, the school should feel mundane and grounding — but in a warm, lived-in way rather than a grim way. The students have made it theirs. Every blank wall has been decorated, every bulletin board is bursting, every locker has a personality. The institution provided the bones; the students and teachers made it human.

The dual-temperature lighting is the most important visual decision in this location: fluorescent lights (cool, slightly green-tinted) fight with natural window light (warm, amber-gold). This creates a distinct zoning system within the building — you're either in fluorescent country or window country. The overlap zones where both light sources reach are the most interesting compositionally.

**Two distinct sub-locations:** The hallway and the classroom are separate environments with shared visual DNA but distinct character. Design them together but implement them as separate deliverables.

---

## LOCATION A: THE HALLWAY

### Spatial Layout

**The Shot: Long perspective hallway, lockers on both sides**

**Proportions:**
- Width: Narrow for what we're told is a public school hallway — roughly 8 feet wide. This creates strong converging perspective and makes the hallway feel both long and slightly claustrophobic in a teenager-appropriate way.
- Height: Drop ceiling at about 9 feet. The ceiling is acoustic tile panels in a metal grid framework — classic institutional.
- Length (visible): The wide shot shows roughly 60 feet of hallway before a T-intersection at the far end. The hallway is not straight — there's a very gentle rightward lean, breaking the total symmetry and making it feel like a real building rather than a render.

**Left wall:** Lockers from floor to ceiling (approximately). A row of lockers runs the full length. Above the lockers: a strip of wall (roughly 18 inches) before the ceiling. This strip has a bulletin board running much of its length. Small windows high on the wall at two points — these are the natural light sources.
- Locker height: Floor to approximately 6 feet. Standard single-column lockers.
- Locker color: See prop sheet in key_props.md
- Bulletin board content: See rotating gags section.

**Right wall:** Lockers mirroring the left. Between locker clusters, two doorways (classroom entrances) with small windowed rectangles in each door. Above the lockers: same bulletin board strip, but this side also has a long handmade paper banner ("MILLBROOK MIDDLE — HOME OF THE MILLBROOK MARLIN") that has faded significantly from whatever original color it was (now reads as a dusty lavender-beige) and has a few safety-pinned additions by various students.

**Floor:** Linoleum tile, 12"x12" squares in an alternating pattern — cream and sage green tiles, a classic institutional 2-color checkerboard. Key detail: there are visible wear-paths. The tiles along the center of the hallway are slightly more worn (lighter, more reflective) than the tiles near the walls. The wear path is not perfectly centered — it drifts slightly right, because the lockers on one side are more popular and students tend to walk that side.

**Ceiling:** Drop ceiling acoustic tiles (2'x2' panels, slightly yellowed cream color in the field, slightly grayer where the metal grid holds them). Fluorescent light fixtures embedded in the ceiling grid — long rectangular flush fixtures, 4 feet long, running parallel to the hallway direction. Two per every 10 feet of hall.

**The T-Intersection (far end):** The hallway terminates at a T — cross hallways visible. A large hand-painted school seal on the wall at the T (circle motif, shows a cartoon marlin fish and "MMMS" in the center). The paint is slightly chipped at the bottom where backpacks have hit it for years.

### Lighting Setup — Hallway

**Primary: Fluorescent Overhead**
- Color: Cool white with a very subtle green tint (#F0FFF0 on the lightest surfaces — this reads as nearly white but with a green undertone that the eye perceives as "institutional")
- Temperature: Cool. Approximately 4000K equivalent.
- Behavior: Even overhead wash. The ceiling tiles nearest the fixtures are brightest. The center of the floor beneath each fixture has a brighter reflection pool.
- Key detail: Fluorescent lights flicker slightly. Not constantly — this is not a horror movie. But in background scenes, one or two fixtures per shot should have a subtle, slow flicker (on a 4-5 second cycle, dimming about 15% for a single frame). This is a background animation element that adds life and a sense of a budget-stretched school.

**Secondary: Natural Light from Windows**
- Color: Warm gold (#E8C95A) — a strong contrast against the fluorescents
- Direction: Raking in from the high windows at roughly 45 degrees, falling in distinct light column shapes on the opposite wall and floor. These columns of warm light are the most beautiful element in the hallway.
- Behavior: The light columns move very slowly throughout the day (background animation — barely perceptible shift in their angle across several scenes). In the establishing shot, one warm light column should overlap with the nearest section of lockers, illuminating a small section of locker faces in warm gold against the cool-lit majority.
- The dual-temperature overlap zone: The floor area at the edge of a warm light column, where it meets the fluorescent-lit floor, has an interesting transition — the linoleum color shifts from the cool-tinted (#D8E8D8) fluorescent zone to the warm-tinted (#E8D8B0) window zone. This transition zone is where directors might choose to stage emotionally significant moments.

**Light color mixing on surfaces:**
- Lockers in fluorescent zone: Sage green lockers look like a muted, slightly-cool sage (#6A8870)
- Lockers in window light column: The same lockers look warmer and more vivid (#7AAA78) — temperature-shifted toward gold
- This is a beautiful effect for character staging: a character standing in the window light column will visually "pop" against the surrounding cool fluorescent environment.

### Shadow Notes — Hallway
- Shadows from lockers, students: Flat shapes in a cool sage-gray (#7A9080) for fluorescent-zone shadows
- Shadows in the window-light zones: Dusty lavender (#A89BBF) — a warmer shadow tone appropriate to the warmer light
- The floor is the primary shadow receiver — cast shadows from the locker protrusions and door frames are clean-edged shapes on the linoleum

---

## LOCATION B: THE CLASSROOM

### Spatial Layout

**The Shot: From the back of the room, looking toward the teacher's desk and front board**

**Proportions:**
- Width: 36 feet wide *(revised from 30 feet — see Camera Angle Note below)*
- Depth: 30 feet from back to front wall *(revised from 25 feet — see Camera Angle Note below)*
- Height: 9 feet, same drop ceiling as the hallway

**Camera Position — Classroom 3/4 Angle (revised v2.0):**

> **Camera Angle Note:** The original v1.0 spec placed the camera at the back-left corner and described a 3/4 view showing three walls (front, left, and the diagonal desk rows). In a 30'W x 25'D x 9'H room, the back-left corner is approximately 39 feet from the front-right corner. At a standard 50mm-equivalent lens (the closest approximation to a flat-graphic animation framing with no perspective distortion), the horizontal field of view at 9 feet of vertical ceiling height covers approximately 28 feet of width at 30 feet of depth. This is NOT sufficient to show the full front wall AND the full left window wall simultaneously without a wide-angle lens that would introduce unwanted perspective distortion incompatible with the show's style.
>
> **Fix:** Room dimensions expanded to 36 feet wide x 30 feet deep. Camera is repositioned as follows:
>
> - **Camera position:** 4 feet inside the back-right corner (NOT the back-left corner). The camera is on the RIGHT side of the room looking diagonally toward the front-left.
> - **Camera height:** 5.5 feet (eye-level standing, slightly above seated student height — this is the "overhead observer" position standard for classroom backgrounds)
> - **Camera angle:** Approximately 35 degrees left of the room's center axis (looking toward the front-left, not straight ahead)
> - **Lens equivalent:** 40mm equivalent — a very slightly wide but not distorting lens that is compatible with the show's flat-graphic style. The slight width prevents any compression artifacts at 36 feet room width.
>
> **What this shot now shows:** From the back-right looking front-left:
> - The front wall (whiteboard, teacher's desk, map, posters) fully visible across the left-to-center of the frame
> - The LEFT window wall (three windows, venetian blinds, radiator below) visible along the left third of the frame
> - The diagonal rows of desks filling the center of the frame, receding toward the front wall
> - Luma's desk (front-left area) and Cosmo's desk directly visible without obstruction
> - The RIGHT wall (bulletin boards, student cubbies) is NOT prominently visible in this shot — it is behind and to the right of the camera. This is correct: the right wall is captured in dedicated medium shots, not the wide classroom angle.
>
> **Why the room was made larger:** A 30' x 25' classroom holds 30 desks comfortably but leaves no staging margin for the back-right camera position and the sight lines required. A 36' x 30' room is a standard "large classroom" dimension for institutional buildings of the school's construction era (1960s-70s), and is internally consistent with a public school that was built when space was less expensive and natural-light classroom design was prioritized.

- Camera position: Back-right corner of the room, 4 feet in from the right wall, looking diagonally toward the front-left. This gives us a 3/4 angle that shows: the full front wall (with board), the left wall (with windows), and diagonal rows of student desks filling the space.

**Front wall (teacher's zone):**
- A wide whiteboard/chalkboard hybrid (the board is a whiteboard but the tray at the bottom still has chalk dust from the era before — it has never been fully cleaned). Current board content varies by episode but always includes at least one thing that's clearly been there for weeks (a complex diagram in faded dry-erase marker that no one has erased).
- Teacher's desk: Large, heavy, wood-laminate top. Facing the class (behind the desk, not to the side). ON the desk: stacks of paper in various degrees of urgency, a mug of pens/pencils, a small plant (surviving against all odds), a name placard ("MS. PETRAKIS"), and a stapler that has been in this school longer than the current students have been alive.
- Above the board: A map of the world, slightly crooked, with a few pushpins. One country has been circled in marker for reasons unknown.
- To the left of the board: A periodic table poster (standard issue, slightly faded). To the right: A reading poster ("READING IS BRIGHT!") with a cartoon sun holding books, circa early 2000s. Both are held up with tape that has started to yellow.

**Left wall (window wall):**
- Three large windows, evenly spaced. Windows reach from about 3 feet off the floor to about 7 feet — a tall window proportion. The school was built in an era that believed in natural light.
- Venetian blinds on each window, partially closed (the second window has a broken slat that flips perpendicular to all others — a background running gag).
- The window light enters in warm diagonal shafts, crossing the rows of desks and creating the beautiful dual-light situation (see Lighting section).
- Below the windows: A heating radiator (old cast iron, covered in layers of paint). Very warm — visually communicated by a slight shimmer/heat-haze effect on the background paint directly above it in warm shots.

**Right wall:**
- Bulletin boards — more chaotic than the teacher's front board. Student work pinned in dense layers (newer work pinned over older work, so the edges of older work peek out around the newer layers). Assignment instruction sheets. Emergency procedures poster. A class schedule. A "Word of the Week" section with the word "PERSEVERANCE" (it has been "word of the week" for at least 3 weeks based on its level of fade). A cluster of student artwork — hands-drawn animals and scenes, varying skill levels, all treated with equal display space and dignity.
- One section of the right wall: Student lockers (individual cubbies, not the tall hallway lockers — shorter, shallower, each student's name on a small card)

**Student Desks:**
- Standard school desks: the kind with the attached chair arm-desk. Slight slope to the desk surface.
- Arranged in diagonal rows (not straight rows) from the back corner camera position — this is both more realistic (most teachers arrange diagonals for discussion) and more visually interesting.
- Six rows of five desks: 30 desks, though not all are filled. There are always a few empty desks.
- Each desk has visible surface wear: scratches, old ink marks, carved initials (close-up detail only). A few desks have small stickers on the side frame.
- Luma's desk (front-left area): A specific desk that the audience will recognize — it has a small pixel-pattern sticker on the left corner that matches her hoodie. Cosmo's desk (next to hers) has a library book always sitting on it.

**Back wall (camera is near here):**
- A row of student cubbies at floor level
- A shelf with reference books and a dictionary that has not been opened
- A paper recycling bin that is always overfull
- Near the camera: a coat rack (low hooks for backpacks), always cluttered with bags, jackets, a random musical instrument case (changes instrument per episode)

### Lighting Setup — Classroom

**Primary: Fluorescent Overhead**
- Same cool (#F0FFF0-tinted) fluorescent wash as the hallway
- The classroom ceiling has two rows of fluorescent fixtures running the length of the room (parallel to the left wall, so they run front-to-back)
- The desks beneath the fixtures are in the brightest fluorescent zone
- The desks between the two fixture rows catch slightly less direct light — this creates subtle lighting variation across the desk rows

**Secondary: Window Light (LEFT SIDE)**
- Warm gold (#E8C95A) shafts entering from the left windows at an angle
- The angle creates diagonal light bars across the desk rows — some desks catch full window sunlight, others are in fluorescent-only zones
- This is a POWERFUL compositional element: the diagonal light bars create natural framing lines across the room
- In shots where something important is happening at a specific desk, that desk can be positioned in a window-light bar for visual emphasis
- The light bars shift position between morning scenes (steep angle, more to the back of the room) and afternoon scenes (shallow angle, more to the front of the room)

**The Dual-Temperature Map:**
- Left third of the room: Window-light zone (warm, gold-tinted surfaces)
- Center third: Mixed zone (both temperatures, resulting in complex mid-tones)
- Right third: Pure fluorescent zone (cool, green-tinted surfaces)
- Front wall: Primarily fluorescent (the windows are on the left wall, not the front)
- This means the teacher at the front desk is almost always in fluorescent light — creating a cool, official quality to that zone
- Students near the windows are in warm light — a subconscious association between the outside world and warmth

### Shadow Notes — Classroom
- Desk shadows on the floor: Cool sage-gray (#7A9080) under fluorescent
- Desk shadows in window-light bars: Dusty lavender (#A89BBF)
- Long cast shadows from window frames cross the floor — the window frame bars create a grid of shadow lines on the floor, which can be a beautiful background detail
- The radiator under the window has a slightly warm shadow immediately below it (the heat warps the air and thus the light slightly)

---

## Color Breakdown — Both Locations

| Element | Color | Hex | Notes |
|---|---|---|---|
| Hallway walls | Dusty lavender | #A89BBF | Faded from whatever original color, now this |
| Classroom walls | Sage green (muted) | #8A9E8A | Same fading-through-decades effect |
| Ceiling tiles | Aged cream | #D8D4C0 | Slightly yellow, unevenly stained |
| Ceiling grid metal | Cool silver-gray | #909898 | |
| Fluorescent fixtures | Near-white | #E8F0E8 | Very slightly green cast even when not looking directly at them |
| Floor tile (cream) | Warm cream | #D8CEB0 | Worn center: slightly lighter (#E0D6BC) |
| Floor tile (sage) | Muted sage | #8A9E88 | Slightly darker than wall sage to differentiate |
| Floor (fluorescent zone tint) | Cool sage cast | #D0DDD0 | The whole floor reads slightly green under fluorescents |
| Floor (window light zone tint) | Warm amber cast | #E8D8A8 | Warm where sun hits |
| Lockers (standard) | Sage green (faded) | #7A9A7A | Main locker color |
| Lockers (accent variants) | Dusty lavender, terracotta | #A89BBF / #B06050 | Some lockers are different, mismatched from replacement history |
| Locker vents | Dark sage | #4A6050 | Recessed shadow |
| Locker handles | Cool gray metal | #909090 | |
| Bulletin board backing | Faded goldenrod | #C8A850 | That specific cork-board-with-color-paper look |
| Bulletin board cork | Natural tan | #C0A870 | Where backing paper is missing |
| Student work (pinned) | Multiple | — | Varied colors, deliberately vivid vs background |
| Classroom board | Medium gray | #C0C8C0 | Whiteboard, slightly gray |
| Board active writing | Deep cocoa | #3B2820 | Current lesson notes |
| Board faded writing | Muted gray | #9A9898 | Old marks not fully erased |
| Teacher's desk surface | Wood laminate | #9A7A50 | Warm but worn |
| Student desks | Lighter laminate | #B0925C | |
| Desk frames (metal) | Dark gray | #4A5050 | Institutional metal |
| Window glass | Sky reflection | #C8DCE0 | Same as exterior |
| Venetian blinds | Cream | #D8CCAC | Yellowed institutional beige |
| Broken slat | Same cream | #D8CCAC | Just turned perpendicular — same color, wrong angle |
| Radiator | Multi-paint-layer gray | #909080 | Many coats of institutional paint |
| Door (hallway to class) | Terracotta | #C05838 | Doors are the terracotta accent color — pops against the sage walls |
| Door window glass | Cool gray | #B0C0C8 | Safety glass, wire mesh pattern visible |
| Accent: "MMMS" banner | Dusty lavender-beige | #BEB0A0 | Faded from original school colors |
| Natural light (warm shaft) | Soft gold | #E8C95A | Direct sunlight on floor |
| Fluorescent light (on floor) | Cool cream | #D8E8D0 | Slightly green-tinted pools |

---

## Prop List — Detailed

### Key Interactive Props (thin outlines)

**The Classroom Board:**
- Content varies per episode. Standard permanent features: the date (always shown — a good continuity tool), the class name ("LANGUAGE ARTS" or "SCIENCE" etc.), and a corner section with the word of the week.
- Faint ghost traces of old writing always visible — suggests this board has never been perfectly cleaned.

**Ms. Petrakis's Desk:**
- The name placard: Small wooden rectangle, gold-foil engraved text. Slightly tilted (she nudged it once and it never got fixed right).
- The mug: Overfull with pens, pencils, one marker without a cap. A gift mug — "WORLD'S MOST PATIENT TEACHER" — slightly ironic given her documented impatience.
- The plant: A small succulent in a terracotta pot. Miraculously alive. In later episodes, it begins to glow faintly and imperceptibly in electric cyan during Glitch Layer encroachments into the school. (The audience won't notice until Episode 10.)

**Student Lockers (Hallway):**
See `/home/wipkat/team/output/backgrounds/props/key_props.md` for full design document.

### Background Props (no outlines unless noted)

**Hallway:**
- A water fountain between two locker sections (the kind recessed into the wall). The water arc runs slightly too far left and has left a stain on the wall to the left of the drain.
- A fire extinguisher mounted to the wall in a red cabinet (one of the few red elements in the school).
- A trash can (gray cylindrical, slightly dented) near the intersection. A small pile of paper and wrappers that didn't quite make it in.
- Trophy case (if visible): Glass cabinet built into the wall near the T-intersection. Trophies visible, but the school's last championship was in 1997. One trophy is turned backward (background gag — it was turned backward in Episode 2 and nobody has turned it forward).

**Classroom:**
- The coat rack (near camera): Always overloaded. Backpacks competing for hooks. One jacket has slid to the floor and has been there since September. A musical instrument case (changes episode to episode: violin → trumpet → what appears to be a tuba despite the physical impossibility of fitting it on a coat hook).
- The paper recycling bin: Always overflowing. By mid-season, there's an entire student art project that didn't make the cut sitting on top.
- The reference shelf: A dictionary, an atlas (old enough that several countries have changed name since publication), a set of encyclopedias (Volume D-F only, suggesting the others were lost or never acquired), a worn copy of a grammar handbook.
- The class fish tank (right wall, high up): A small tank with two fish. One fish is clearly much larger than when it arrived. The other fish seems to be the same fish it's always been, permanently 1 inch long. They do not interact. The tank has a slight film of algae on the rear glass. Background animation: the fish swim on a very slow loop.

---

## Foreground / Midground / Background Layer Breakdown

### Hallway Wide Shot

**Foreground Layer:**
- Edge of nearest lockers, slightly cropped at bottom frame edge
- A corner of nearest bulletin board content at frame top
- A backpack hanging on a locker handle at the very front, partially cropped
- Rendering: Boldest values, most texture detail on the locker surface/signage closest to camera

**Midground Layer:**
- Full locker faces on both sides, most of the visible bulletin board content
- The floor with its dual-lighting zone interplay
- The ceiling with its fluorescent fixtures
- Background characters (students) in this zone — this is the action plane
- Rendering: Full detail. Careful attention to the lighting zones on locker faces.

**Background Layer:**
- The locker rows receding in perspective to the T-intersection
- The hand-painted school seal on the back wall
- The cross-hallway visible as a lit section beyond
- The trophy case (if shown)
- Rendering: Atmospheric simplification. The cool fluorescent light has a slight blueing effect in the far hallway distance (atmosphere even in interiors). Far lockers are simplified to flat value blocks, not individual locker detail.

### Classroom Shot (from back corner)

**Foreground Layer:**
- The corner of the nearest student desk at the very bottom of frame
- Edge of the coat rack/backpack zone at frame left

**Midground Layer:**
- The diagonal rows of desks
- Students seated (or absent) at desks
- The window light bars crossing the room diagonally from left
- This is the action plane — where Luma and Cosmo's seats are

**Background Layer:**
- The front wall with teacher's desk and board
- Ms. Petrakis at the front
- The map, posters, etc. on the front and side walls
- The windows (from this angle, we can see out to the school exterior — a parking lot, a playing field, the sky)
- Rendering: The front wall is simplified. The board is clear and readable (key information must be legible for plot purposes). The teacher's desk area has enough detail to read but the distant walls are simplified shapes.

---

## Painterly-Flat Rendering Notes

### Linoleum Floor Treatment
- The 12"x12" tile pattern: Suggest the grid with very faint lines at the grout seams (10% opacity maximum — they are almost invisible). The pattern is implied, not drawn.
- The wear path: A slightly lighter/more reflective tone running down the hallway center. Achieved with a soft-edged lighter color shape layered over the floor.
- Tile color variation: Each tile is NOT exactly the same color. Very slight variation (±5-8% in value) between adjacent tiles gives the floor a realistic, worn character.

### Locker Surface Rendering
- Flat color per locker face. No highlights/shadows on individual locker faces (they are flat panels).
- The locker edge (the slight 3D depth where the door meets the frame) is rendered as a thin darker-value strip — achieved through a secondary color shape, NOT a line.
- Stickers/decorations on lockers: Flat graphic shapes at higher saturation than the locker background. Simple silhouettes of sticker content.
- The vents: Horizontal slots, rendered as a slightly darker tone than the door face — parallel thin rectangles at the top and bottom of each locker door.

### Fluorescent Light Rendering
- Light is not rendered as a visible beam (that would be film noir, not institutional). It's implied through the color temperature of ALL surfaces beneath it.
- The "circle" of brightest light on the floor under each fixture: A soft-edged oval of slightly lighter floor color.
- A very subtle "screen-line" overlay at 8% opacity runs the length of the hallway — thin horizontal lines suggesting the scan-line aesthetic, a nod to the monitors at Luma's house, a suggestion that even the most mundane places have a digital layer underneath.

### Natural Light Shafts
- These are the most beautiful rendering challenge in the school.
- Each light shaft: A clean-edged parallelogram of warm gold (#E8C95A at 40% opacity) layered over the floor and desks beneath.
- The parallelogram edges are CLEAN, not soft (Venetian blinds create sharp light bars, not diffuse). The distinction between the warm gold light shaft and the surrounding cool floor is crisp.
- Dust motes in the light shafts: Very subtle. A few tiny warm-gold dot particles drifting slowly in the shaft area. Optional — only include if the shot is a wide shot with significant breathing room.

---

## Key Storytelling Details & Discoverable Background Gags

### Persistent Details
- **The broken slat:** Second window's venetian blind has one slat turned perpendicular. Every single hallway/classroom shot. It has NEVER been fixed. The maintenance request is presumably in the same pile as all the other maintenance requests.
- **Ms. Petrakis's classroom plant:** Begins as a normal succulent. After Episode 5's glitch incursion, it starts to exhibit very faint electric cyan bioluminescence visible only in wide shots with careful attention. By Episode 10 it's undeniably glowing. Nobody in the class has mentioned it. Ms. Petrakis refers to it as her "healthy plant."
- **The backward trophy:** Turned backward in Episode 2 (Cosmo knocked it while hiding from a Glitchkin). Still backward in every subsequent episode. Running background gag.
- **The "Perseverance" word of the week:** Has been word of the week since the show started. Will remain word of the week for the entire season. Season 2 will have a different word. (It will be "Persistence.")

### Rotating Gags
- **The musical instrument on the coat rack:** A different instrument appears each episode, following no discernible logic. Episode 1: violin. Episode 2: saxophone. Episode 4: recorder (out of place, but here we are). Episode 7: cello. Episode 9: a didgeridoo (nobody acknowledges this).
- **The classroom board content:** Changes per episode to reflect the subject being taught. The "ghost" writing from previous lessons visible in the background should occasionally contain cryptic phrases relevant to the episode's theme.
- **The overflowing paper recycling bin:** Gains new content each episode. By Episode 10 it has gained a structural personality — it looks like a papier-mache art project of itself.
- **Cosmo's library book:** A different book each episode, always related to the episode's challenge. He has read it. He has dog-eared the wrong pages.

### Long-Term Story Details
- **Locker 147:** A specific locker in the hallway (marked in a background detail shot with the number "147" barely visible on the combination lock). In Episodes 1-4: perfectly normal. Episode 5: a faint cyan glow through the vents. Episode 7: the glow is undeniable. Episode 8: the lock has changed. Nobody has locker 147. Nobody knows what's inside. (It's the Glitch Layer encroaching. A second portal is forming.)
- **The class fish tank:** The large fish grows perceptibly across the season — a subtle scale reference that rewards careful viewers. By Episode 11 the fish has exceeded any reasonable size for the tank. Its eye, visible in shots, has taken on a faint electrical quality. Nobody mentions this either.

---

## Design Rationale

The school's design thesis is: "Normal is maintained by tremendous ongoing effort." The students of Millbrook Middle are actively making this institutional space personal and habitable against its institutional defaults. Every piece of student work on the bulletin board, every sticker on a locker, every plant fighting to survive on Ms. Petrakis's desk — these are acts of small, persistent humanity against beige walls.

This makes the school an interesting thematic counterpoint to both the warmth of Luma's house (where the humanity has had decades to accumulate) and the chaos of the Glitch Layer (where humanity hasn't arrived yet). The school is humanity mid-process.

The dual-temperature lighting is the signature of this location. I want it to be as distinctly recognizable as THE monitor's cyan glow in Luma's house, or the void black of the Glitch Layer. When you see warm gold light shafts fighting cool fluorescent wash, you know you're at Millbrook Middle. It's the visual fingerprint of the place.

The Glitch Layer encroachments (the plant, the fish, locker 147, the ghost writing on the board) serve a crucial storytelling function: they tell the audience that the Glitch Layer is growing. The real world is not as separate from the digital dimension as everyone assumes. The intrusions start small and grow — and the audience is the only one who sees all of them. This creates the dramatic irony that makes the tension escalate even in "normal day at school" episodes.
