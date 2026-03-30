<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# LUMA'S HOUSE — Interior Environment Design
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
- **Filename convention:** `LTG_ENV_lumas-house-int_v###.psd`
  - Example: `LTG_ENV_lumas-house-int_v001.psd`
  - Example: `LTG_ENV_lumas-house-int_v002.psd`
- **Delivery PNG:** `LTG_ENV_lumas-house-int_v###.png`
- **Shot codes in use:** `WIDE_ESTAB` / `MED_COUCH` / `MED_DESK` / `CU_MONITOR` / `CU_CABINET`

> **Note on internal PSD layer naming:** The layer naming convention inside the file (e.g. `LH_INT_BG`, `LH_INT_FG`) remains unchanged. These are intra-file identifiers, not filenames. The `LTG_ENV_` convention applies to the filename only.

### Required PSD Layer Structure
All master PSDs for this environment must include the following named layer groups, in order from top to bottom:
1. `FG` — Foreground elements (z=1)
2. `MG_CHAR` — Character plane (z=2, empty — reserved for animation)
3. `MG_BG` — Midground background elements (z=2)
4. `BG` — Background layer (z=3)
5. `LIGHT_OVERLAY` — Lighting overlays (monitor glow, window light pools) — multiply/screen layers
6. `SHADOW_OVERLAY` — Shadow shapes — multiply layers
7. `BASE` — Base color shapes (walls, floor, ceiling)

---

## Overview & Design Intent

Luma's house is the emotional core of the show. Every time we cut back here, the audience should exhale — it's safe, warm, and endlessly interesting. The design challenge is "cozy clutter" rather than "messy chaos." Grandma Miri is not a hoarder; she is a curator. Every piece of vintage tech on display has a story. The space should feel like a museum that also happens to be somebody's home, and a very loving home at that.

The architectural slight-wonkiness is key. The house has settled over many decades, like Grandma Miri herself. Nothing is at a perfect 90-degree angle. But the slant has personality — the ceiling leans in like it's listening to the conversation below.

**Recurring hero location.** This environment needs the highest detail density of any interior. Every rewatch should reveal something new.

---

## Spatial Layout

### Room: The Living Room / Tech Den (Combined Space)
The living room and Grandma Miri's "tech den" are the same room — there was never a formal separation. A couch defines the "living" zone. Banks of monitors and shelving define the "tech" zone. They bleed into each other naturally.

**Proportions (feel, not measured):**
- Ceiling height: Low — roughly 8 feet at the highest point, dropping to maybe 6.5 feet near the far wall where the room has settled. The ceiling plane is not flat; it bows gently.
- Room depth: Medium-deep. Wide establishing shot shows a room roughly 20 feet wide, 15 feet deep. Feels intimate, not cavernous.
- Floor plan: Roughly rectangular but the far-left corner has a bay window alcove that pushes out, adding visual interest and an extra lighting source.

**Room zones (left to right in establishing shot):**
1. **Bay Window Alcove (far left)** — A deep window seat with faded, mismatched cushions. The exterior view shows the front yard and a big oak tree. Afternoon light pours through sheer curtains here.
2. **The Couch Area (left-center)** — The action zone. A worn, oversized sofa with three different cushion patterns faces the main monitor stack. A low coffee table in front holds remote controls, snack bowls, and a stack of vintage tech magazines.
3. **THE Monitor Stack (center-right)** — The focal point. Three vintage CRT monitors stacked in a slight pyramid, with THE monitor (the Glitchkin source) on the top center. Cables drape down like vines. Old keyboards are propped against the sides.
4. **Grandma's Workspace (far right)** — A roll-top desk, half-open, revealing a controlled chaos of wires, component boards, and hand-labeled floppy disks. A desk lamp with a warm amber shade. A wheeled office chair with a crocheted seat cover.
5. **The Cable Drawer Cabinet (against the right wall near the desk)** — A wide, shallow wooden cabinet with many small drawers, like an old card catalog or a watchmaker's parts cabinet. Labels in Grandma Miri's handwriting identify each drawer.

### Connected Spaces (partially visible):
- **Kitchen** — visible through a wide doorway at center-back. Warm yellow light, hanging copper pots. Gives depth to the composition.
- **Staircase** — visible at far left of the frame, just past the bay window. A wood bannister with a slight lean. Used for character entrances.

---

## Lighting Setup

### Primary Sources

**1. Bay Window — Diffuse Afternoon Light**
- Direction: Left-to-right rake, entering at roughly 45 degrees
- Color: Warm cream (#FAF0DC) base with soft gold (#E8C95A) on the brightest surfaces
- Behavior: Soft-edged light pools on the floor near the window. Sheer curtains diffuse it into a gentle wash. Not harsh — this is the "safe warmth" light.
- Shadow: Dusty lavender (#A89BBF) shadows cast from the couch and coffee table toward the right

**2. Monitor Stack — Cyan CRT Glow**
- Direction: Front-facing, emanating outward from the monitor screens. Strongest on the floor directly in front, fading back toward the room.
- Color: Electric cyan (#00F0FF) at the source, shifting toward a softer teal-blue (#40C8D8) in the mid-distance
- Behavior: This is the visual tension of the room. The warm window light and the cool monitor glow COMPETE. Where they overlap (the couch, the coffee table) the two temperatures mix into interesting intermediate zones. The couch cushions nearest the monitors catch cyan on their facing surfaces.
- Character use: When characters sit on the couch, their faces are lit warm from the left and cool-cyan from the right — a built-in emotional metaphor for the show (warm world, digital intrusion).
- THE monitor (top center) has a slightly brighter, more electric glow than the others. Its screen is never fully dark — there's always a faint glow even in "off" scenes.

**3. Grandma's Desk Lamp**
- Direction: Downward cone, illuminating only the desk area (far right)
- Color: Deep amber (#D4840A) — warmer and more orange than the window light, suggesting old incandescent bulbs
- Behavior: Tight cone. Creates a cozy "island" of warm light on the right side of the frame, balancing the composition against the window light on the left.

**4. Ambient Fill**
- Overall room fill: Soft warm cream, very low intensity. No room should feel black in its shadows. The darkest values here are a warm deep cocoa (#3B2820) on the underside of shelves and in deep corners.
- The kitchen doorway adds a secondary warm glow from off-screen.

### Shadow Notes
- Shadows are painted flat shapes in dusty lavender (#A89BBF) for warm-zone shadows, and a dark cyan-tinted tone (#1A3A4A) for shadows falling in the monitor-glow zone.
- NO drop shadows. Cast shadows only — blocky, simplified shapes indicating the light source direction.
- The monitor stack casts a complex shadow on the wall behind it — overlapping rectangles, faintly glowing at the edges.

---

## Color Breakdown

| Element | Color | Hex | Notes |
|---|---|---|---|
| Walls | Warm Cream, aged | #F0E6C8 | Slightly yellowed from decades of living |
| Wall texture overlay | Subtle grain | — | Grain texture at 20% opacity, warm tone |
| Ceiling | Warm Cream, shadowed | #DDD1B0 | Lower value than walls, settling darkness |
| Wood floor | Honey oak | #B07A3A | Worn paths are lighter (#C8943E) |
| Floor shadow pools | Dusty lavender | #A89BBF | Cast from furniture |
| Floor monitor glow | Dark cyan wash | #0D2A35 | Very subtle, near the monitor base |
| Couch body | Sage green, faded | #607A64 | Worn and desaturated at wear points |
| Couch cushions (mixed) | Terracotta, soft gold, dusty lavender | #B85030 / #D4B040 / #9080A8 | Each cushion different |
| Coffee table | Deep cocoa | #4A3020 | Dark wood, scratched surface |
| CRT monitor casings | Off-white cream | #D8CEB0 | Yellowed plastic, aged |
| Monitor screens (off) | Dark teal | #102028 | Deep, slightly reflective |
| THE monitor screen (on) | Electric cyan glow | #00F0FF → #002030 | Bright at center, dark at edges |
| Keyboard shelves | Bone / silver | #C0BAA8 / #787878 | Mix of materials |
| Cables | Multiple dark tones | #3B2820 / #1A3A1A / #2A1A40 | Black, dark green, dark purple |
| Roll-top desk | Medium oak | #7A5020 | Older, darker wood than floor |
| Desk lamp shade | Amber | #C87010 | Warm orange-amber |
| Cable drawer cabinet | Painted cream | #D0C4A0 | Old painted wood, chipped at edges |
| Drawer labels | Aged paper | #D8C888 | Hand-written in deep cocoa |
| Bay window frame | Soft white | #E8DFCC | Paint worn at the corners |
| Window curtains | Warm cream gauze | #FAF0DC | Sheer, light passes through |
| Kitchen doorway | Warm amber glow | #F0A830 | Slightly overexposed impression |
| Staircase bannister | Honey oak | #9A6028 | Polished, warm |
| Background walls (depth) | Muted sage | #889878 | Far wall, atmospheric recession |

---

## Prop List — Detailed

### Hero Props (Interactive — thin outlines applied)

**1. THE CRT Monitor (top of stack)**
See `/home/wipkat/team/output/backgrounds/props/key_props.md` for full design document.
- Position: Top-center of the three-monitor pyramid, slightly forward of the other two
- Screen state: Always has a faint glow. In normal scenes, displays rolling static with occasional pixel patterns that look like tiny faces. In glitch scenes, full electric cyan with pixel confetti (floating square particles in #00F0FF and #FF2D6B)
- Cable: A distinctive orange cable (color: #C86820) with a fabric-braided outer covering (not smooth plastic) runs from the leftmost socket at the monitor's back, distinct from all other cables in the scene — this is the "magic cable" and subtle visual storytelling. Near its wall end, a small circular burn mark (#3A2010) is partially hidden behind the cable drawer cabinet. The cable has characteristic drape and curl where it pools on the shelf/floor before running to the wall. See `/home/wipkat/team/output/backgrounds/props/key_props.md` for full cable specification.

**2. Grandma's TV Remote (coffee table)**
See `/home/wipkat/team/output/backgrounds/props/key_props.md` for full design document.
- Position: On the coffee table, usually angled toward the monitor stack
- Background gag: In every episode, the remote is in a different position/configuration on the coffee table

**3. The Cable Drawer Cabinet**
See `/home/wipkat/team/output/backgrounds/props/key_props.md` for full design document.
- Position: Against the right wall, between the monitor stack and Grandma's desk

### Background Props (no outlines)

**Monitor Stack (flanking monitors)**
- Two additional CRT monitors, same cream-yellowed casing but different models (one is rounder, one is older and box-shaped)
- Both are "off" (dark screens) or show static — they frame THE monitor
- Old keyboard draped horizontally between the two lower monitors as a makeshift shelf, holding a potted succulent and a small ceramic cat figurine

**The Tech Shelf (above the monitor stack, wall-mounted)**
- Rough planks supported on old circuit board brackets
- Contents (left to right): A row of VHS tapes with hand-labeled spines, a small CRT portable TV (permanently off), a glass jar full of different-colored cables sorted by color, a vintage modem, a stack of floppy disks in labeled paper sleeves, an old telephone in cream/avocado green
- A framed photo on the right end: Grandma Miri at what appears to be a computer convention, young, huge grin

**Coffee Table Items**
- Stack of tech magazines (titles visible in wide shot: "CIRCUIT QUARTERLY", "BYTE LIFE", "MODEM WORLD")
- A bowl of mixed nuts with one piece left in it
- Two mugs: One with Grandma Miri's tea (steam rising in wide shots), one empty with a dried tea ring inside
- A remote control caddy (wicker, cylindrical) holding 4 more remotes of various ages
- A small cat figurine used as a paperweight on a folded newspaper

**Couch Area**
- The couch has visible wear-paths where people sit most — lighter color at those points (fabric worn thin)
- A crocheted throw blanket in terracotta and cream, half-folded over the right armrest
- A cat bed between the couch and the monitor stack (the cat is rarely in it)
- A floor lamp (off) with a bent neck, behind the left couch armrest

**Grandma's Desk (roll-top, half-open)**
- Inside the roll-top: Small component drawers (like a spice rack), a circuit board mid-repair, a soldering iron in a stand, a hand-magnifier on an arm, reference books (large format, colorful spines)
- Desk surface: Notepad with circuit diagrams in pencil, a coffee mug being used as a pen holder, a USB hub with colorful cables plugged in (note: a delightful anachronism in this otherwise vintage space)
- Pinned to the wall above the desk: A hand-drawn map of Millbrook, multiple sticky notes, a photo of Luma at age 6, a printout of a circuit diagram with handwritten annotations

**Walls / General**
- A large wall clock (visible above the tech shelf) — style: utilitarian plastic, 1970s. The second hand has a slight wobble in its path (background animation gag)
- A bulletin board near the staircase with Luma's school photos year by year (kindergarten through current), plus a few ribbons and certificates
- A houseplant in a terracotta pot in the bay window alcove — large fern type, lush and slightly overgrown, spilling over the edges
- A cat door at the base of the kitchen doorway frame — sized for a medium-sized cat
- An inexplicable traffic cone in the corner by the staircase that has been there long enough to have a small plant growing out of it

---

## Foreground / Midground / Background Layer Breakdown

### Wide Establishing Shot

**Foreground Layer (z=1, closest to camera):**
- A section of couch back/armrest at the very bottom edge of frame (pulls viewer INTO the scene, as if they're sitting on the couch)
- The corner of the coffee table
- A cable that droops into the bottom frame edge
- A crocheted blanket hem
- Rendering: Slightly less sharp than midground. Subtle edge softening. Boldest value contrasts.

**Midground Layer (z=2, action zone):**
- The full couch with cushions
- The coffee table and its contents
- The monitor stack (THE monitor is visually dominant here — brightest point in the frame)
- Grandma's desk area at frame right
- THE cable drawer cabinet
- Characters exist on this plane
- Rendering: Full detail. Sharp color edges. This is where the eye should spend most of its time.

**Background Layer (z=3):**
- The far wall with tech shelf
- The kitchen doorway (glowing, slightly soft)
- The staircase (left)
- The bay window (right) — softest detail of all, window light slightly overexposed
- Ceiling showing the slight bow
- Rendering: Atmospheric perspective applied — slightly more muted, softer color edges, reduced saturation at the far wall. The wall color reads slightly more blue-gray (#C8BCAE) than the actual ceiling (#DDD1B0) due to aerial haze effect even in interiors.

### Medium Shot (Couch Area)

**Foreground Layer:**
- The coffee table surface — seen from above-angle. Contents in sharp detail.
- Edge of the couch seat cushion at the very bottom

**Midground Layer:**
- The couch back and armrests
- THE monitor stack directly behind — this is the dominant visual element even in medium shots, always in frame
- Characters sit here

**Background Layer:**
- Far wall, tech shelf — simplified
- Kitchen doorway — reduced to warm glow impression
- Ceiling in soft focus

---

## Painterly-Flat Rendering Notes

### Texture Strategy
- **Wall surfaces:** A grain texture overlay at 15-20% opacity in a warm tone. Suggests plaster and age without being literal about it. The grain should be slightly larger scale than you'd expect — this is a graphic, not a realistic texture.
- **Wood floor:** Flat color shapes for planks (very subtle plank lines, not dominant). A worn-path shape in a lighter honey tone where people walk most. Grain overlay.
- **Fabric (couch, cushions, blanket):** Flat color with very subtle soft-edge transitions at the fold points (2-3 key folds only). No detailed weave texture.
- **CRT plastic casings:** Flat color with one highlight shape (rectangular, suggesting the flat face of the monitor) and one subtle shadow shape at the bottom/sides. A very faint scan-line texture on the monitor glass at 10% opacity.
- **Cables:** Flat, slightly tubular — a highlight along the top edge of each major cable. No elaborate shading.

### Soft Edge Treatment
- The boundary between the warm window light and the mid-room ambient is a very soft, blurred edge (5-8 pixel soft edge in working resolution). This is the one place gradients are permitted — as a zone transition, not on a single shape.
- The cyan monitor glow fades out through a soft-edged light pool shape on the floor. The edge of this pool is faintly irregular (not a perfect oval) to feel organic.

### Color Shape Discipline
- All color shapes should have clean, confident edges — no fuzzy, uncommitted borders except where specifically noted above.
- When in doubt, simplify. If a shadow shape has too many corners, reduce it.
- Background objects in the far wall zone should have 30% fewer color shapes than midground objects of the same type.

---

## Key Storytelling Details & Discoverable Background Gags

### Episode-Persistent Details (always present)
- **The "origin cable":** The orange, fabric-braided cable (color: #C86820) connecting THE monitor to the wall outlet has a small circular burn mark (#3A2010) near the wall end, partially hidden behind the cable drawer cabinet. This was the moment the Glitchkin first arrived. (Cable specs: see `/home/wipkat/team/output/backgrounds/props/key_props.md`.)
- **Grandma's coffee mug collection:** The shelf behind the desk has 11 mugs but only 2 are ever used. One has a logo for "MILLBROOK TECH EXPO 1987." One says "World's Okayest Programmer."
- **The cat, Magnus:** A large orange tabby cat appears in a different background location every episode. He is never interacted with, never acknowledged, but is always there. He once appeared on top of THE monitor (leaving paw prints on the static).
- **The height chart:** On the doorframe of the kitchen doorway, pencil marks track Luma's height since she was 2 years old. Her current mark is the highest — but barely. New mark appears after a season milestone episode.
- **The dead plant:** In the far right corner behind the cable cabinet, a small succulent sits in a terracotta pot. It is completely dead, a dried husk. It has a sticky note that says "WATER ME" in all caps. It has been dead for years.
- **THE monitor's pixel face:** In wide shots, if you look at THE monitor's screen carefully, you can always see a tiny pixel shape that vaguely resembles a face looking out. This was present before the Glitchkin story started. Easter egg for dedicated fans.

### Rotating Background Gags (change episode to episode)
- The positions of the 5+ remote controls on the coffee table and in the caddy.
- Which VHS tape has been pulled from the shelf and set down somewhere random.
- The number of empty mugs accumulating near Grandma's desk.
- Something new on the bulletin board above Grandma's desk (a new sticky note, a clipped article).
- Magnus the cat's new location.
- A new small item on the couch that indicates what Grandma was doing: a knitting project, a disassembled circuit board, an open book.

### Long-term Story Gags (reward dedicated watchers)
- After Episode 5 (when the Glitchkin are first defeated), THE monitor screen's pixel face disappears. It returns — larger — in Episode 12.
- The traffic cone in the corner gains small accessories over the season: a tiny hat appears in Episode 7, a scarf in Episode 11.
- The map above Grandma's desk slowly gains new marks and annotations as the Glitchkin locations are discovered throughout the season.
- In Episode 3, a second orange cable appears behind the cabinet. In Episode 8, a third. Something is growing.

---

## Design Rationale

The core tension of this room is warm-vs-cool, analog-vs-digital, cozy-vs-unsettling. I've positioned the monitor stack at the visual center-right of the establishing shot so that it always feels like it's watching the couch — which is where the characters (and by proxy, the audience) sit. You can never completely relax here, because the technology is always humming in your peripheral vision.

The bay window on the left provides narrative breathing room — it's the "safe" part of the frame, the part connected to the normal world outside. The right side of the frame is the "interesting danger" zone. This left/right split gives us built-in composition language: scenes where characters are safe and relaxed will push them toward the window side; scenes where the digital world is encroaching will push them toward the monitor side.

The ceiling bow is important: it makes the room feel like it's gently pressing down. The house holds its inhabitants close. This is a shelter in a story about things going wrong in the wider world. Grandma Miri and Luma should always look comfortable and at home here, even when plotting difficult things.
