# MILLBROOK MAIN STREET — Exterior Environment Design
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
- **Filename convention:** `LTG_ENV_millbrook-main-st_v###.psd`
  - Example: `LTG_ENV_millbrook-main-st_v001.psd`
  - Example: `LTG_ENV_millbrook-main-st_v002.psd`
- **Delivery PNG:** `LTG_ENV_millbrook-main-st_v###.png`
- **Shot codes in use:** `WIDE_ESTAB` / `MED_CORNER` / `MED_DINER` / `MED_SQUARE` / `CU_CLOCKTOWER` / `CU_SANDWICH_BOARD`

> **Note on internal PSD layer naming:** The layer naming convention inside the file (e.g. `MM_EXT_BG`, `MM_EXT_SKY`) remains unchanged. These are intra-file identifiers, not filenames. The `LTG_ENV_` convention applies to the filename only.

### Required PSD Layer Structure
All master PSDs for this environment must include the following named layer groups, in order from top to bottom:
1. `FG` — Foreground elements (nearest sidewalk elements, partial building facades)
2. `MG_CHAR` — Character plane (empty — reserved for animation)
3. `MG_BG` — Midground buildings, street furniture, signage
4. `ANTENNA_NETWORK` — Power lines and antenna overlay (separate for easy adjustment)
5. `BG_BUILDINGS` — Background street block, clock tower
6. `SKY` — Sky and atmospheric depth
7. `LIGHT_OVERLAY` — Time-of-day light (sun angle, shadow overlays)
8. `BASE` — Base color shapes (road, sidewalk, building walls)

---

## Overview & Design Intent

Millbrook is the kind of town where nothing exciting has happened in 40 years, and the architecture shows it. Nobody has renovated anything. Nobody has torn anything down. The town just... settled. The buildings lean against each other like old friends who are tired. Everything is slightly sun-faded and slightly too much.

The critical visual metaphor: Millbrook is unknowingly an enormous antenna for glitch energy. The absurd density of power lines and antennas above the roofline isn't just quirky local flavor — it's foreshadowing. Every antenna on every rooftop, every sagging power line between poles, forms an invisible network that the Glitchkin are exploiting. The audience doesn't know this at first. The design does.

The tone of this exterior should be: "Something quietly wonderful might be about to happen here." Not ominous. Charming. But with a slightly held breath.

**Recurring hero location — exterior.** Used for establishing shots before school/town scenes, for chase sequences, and for quiet moments on the corner.

---

## Spatial Layout

### The Scene: Looking Down Main Street Toward the Clock Tower

**Camera position (wide establishing shot):** Standing at the near end of Main Street, slight elevation (as if standing on a low step), looking down a gently curving street toward the town square clock tower in the middle distance. The street has a very subtle curve to it — not a straight shot. This keeps the composition interesting and makes the clock tower feel like a destination rather than just a backdrop.

**Street proportions:**
- Street width: Two-lane (though barely) plus sidewalks. The sidewalks are wide — this is a town that used to have more foot traffic.
- Block depth: The wide shot shows roughly two full blocks before the town square.
- Building height: 2-3 stories maximum. No building is taller than 3 stories. They vary in height, creating an uneven roofline skyline that is one of the most important shapes in the establishing composition.

**Building arrangement (left side of street, near-to-far):**
1. **Corner Bakery** — Nearest, slightly cropped at frame left. Wide awning in faded sage green. Painted window lettering: "FINCH'S BAKERY est. 1958." Display window shows a few items. Large planter boxes on the window ledge, overflowing with flowers.
2. **Hardware Store** — Two stories. Brick face. A hand-painted sign: "KOWALSKI HARDWARE." External merchandise display: a rack of rakes and shovels chained to a post outside. Upper floor has mismatched windows (one was clearly added later).
3. **A narrow "sliver" building** — Only about 15 feet wide, three stories tall. Feels like it grew between two bigger buildings. A tailor or alterations shop. The name is illegible in wide shots (reward for close-up viewing).
4. **A gap-tooth gap** — An empty lot between two buildings, converted to an informal parking area. One old truck permanently parked there. A hand-painted "PARKING - KOWALSKI CUSTOMERS ONLY" sign.
5. **Post Office** — Solid, slightly larger than its neighbors. The most "official" building in town. A flagpole with a flag. Brick, cream-painted window frames. Even the post office leans slightly — a point of quiet pride or embarrassment depending on who you ask.

**Building arrangement (right side of street, near-to-far):**
1. **Corner shop** — The action zone for medium shots. A general store/convenience hybrid. The kind of place that sells both fishing bait and birthday cards. Sage green awning. A hand-painted sandwich board on the sidewalk (changes messages episode-to-episode).
2. **Millbrook Diner** — Wider building, one story with a large plate glass window. A neon sign ("MILLBROOK DINER") that works except the "M" in "MILLBROOK" flickers. Vinyl booths visible through the window.
3. **A bookshop** — Two stories, dark green painted facade (faded to a dusty sage). Bay window protruding at street level. An overcrowded display visible inside.
4. **Empty storefront** — Papered windows. A "FOR LEASE" sign that is clearly very old. Something has scratched into the lower window paper from inside but it's unreadable in wide shots.

**Town Square (middle distance, focal point):**
- A modest square, roughly circular, defined by a ring of old trees with wide canopies.
- The clock tower stands at the center-back of the square — not a grand civic building, but a charming standalone stone tower, maybe 40 feet tall, with a large clock face on all four sides.
- The clock reads 7 minutes behind the correct time. Always. Every shot.
- A fountain in the square (currently non-functional — a piece of public art that has become a planter for wildflowers).
- Park benches around the fountain. A few always have someone on them.

### Overhead Infrastructure (The Antenna Network)
This is Millbrook's most distinctive visual feature and must be drawn with care.

**Power line system:**
- Wooden poles every 30-40 feet along both sides of the street. Old, weathered poles, some with a slight lean.
- Lines run in chaotic layers: primary power lines (thick, 3-4 per run), telephone lines (thinner, more numerous), cable television lines, and a number of lines that seem to have no clear origin or destination.
- At each pole, a cluster of hardware: transformers (barrel-shaped, gray), junction boxes, ceramic insulators in rows, and at certain poles — antenna-like structures that aren't clearly labeled as anything standard.
- Cross-street lines create a dense web overhead. Looking straight up from the middle of the street, the sky is divided into irregular polygons by the overlapping wires.
- From the side (the primary establishing shot angle), this overhead net creates a complex layered silhouette against the sky.

**Building-mounted antennas:**
- Every building has at least 2-3 antennas of different ages and types: old TV rabbit ears (giant, rooftop-scale), satellite dish (small, residential), a few that are clearly custom-built, and some that are simply mysterious metal structures.
- The cumulative effect: the roofline of Millbrook is COVERED. The buildings themselves are modest, but above them is an elaborate spiky crown of signal-catching hardware.
- This should feel slightly absurd. A little too much. Why does a town this small need this many antennas? (We know why.)

---

## Lighting Setup

### Primary Sources (Daytime / Golden Afternoon)

**1. Overhead Sun (late afternoon, left-of-camera)**
- Direction: Raking from camera-left at approximately 30 degrees above the horizon
- Color: Soft gold (#E8C95A) for direct lit surfaces, warm cream (#FAF0DC) for secondary bounce
- Behavior: Because the buildings lean slightly in different directions, some receive full sun on their faces while adjacent ones are in partial shade — this creates a pleasant rhythm of light/shadow patches alternating down the street
- Street surface: The asphalt reads as a warm medium gray (#7A7060) with a gold glaze on the near lane

**2. Awning Bounce Light**
- The sage green awnings cast a subtle cool-green tinted light on the sidewalk and walls directly beneath them — a very gentle green tint (#D0E8C8) in the shadow zone under each awning
- This is a small but important detail: it makes the sidewalks feel dappled and interesting

**3. Sky Fill / Ambient**
- Sky color: Warm cream at the horizon (#FAF0DC), deepening to a very pale blue-sage (#C8DCE0) high above. The cloud situation is always "partly cloudy with nice puffy clouds" in daytime shots — this gives the background artist a reason to vary the sky slightly per episode.
- Ambient fill from the sky: The overall fill is warm but slightly cool compared to direct sun. This creates a two-temperature ambient that makes everything feel naturally three-dimensional without elaborate shading.

**4. Neon Sign (Diner) — Secondary Character**
- The diner's neon sign is always on (even in daytime — the owner never turns it off)
- Color: A warm pink-red neon (#FF6050) against the cool plate glass window
- In wide shots this is a tiny point of warm-red among the creams and sages — it catches the eye

**5. Night / Twilight Variant (noted for future use):**
- Sky shifts to dusty lavender (#A89BBF) through deep cocoa at the horizon
- The neon sign becomes dominant — pink-red glow across the diner facade
- The power lines/antennas begin to subtly emit a faint electric-cyan glow along their lengths (#00F0FF at very low opacity) — hinting at their true function
- Streetlamps (single globe lights on wrought iron poles, 1950s style) cast warm amber pools on the sidewalks

### Shadow Notes
- Building shadows fall on adjacent buildings and the street — long raking shadows in the afternoon
- Shadow color: Dusty lavender (#A89BBF) base, very slightly deeper where multiple shadows overlap (#8B7AA0)
- The shadow sides of buildings are NOT dark — they receive sky bounce and stay within a legible middle-value range. No building face should be so dark it becomes unreadable.
- Awning shadows on storefronts are clean-edged geometric shapes (the awning frame is simple) — these create nice graphic patterns on the walls

---

## Color Breakdown

| Element | Color | Hex | Notes |
|---|---|---|---|
| Sky (horizon) | Warm Cream | #FAF0DC | Soft, receding |
| Sky (zenith) | Pale blue-sage | #C8DCE0 | Very gentle, not saturated |
| Cloud forms | White-cream | #F0EBDC | Flat, no gradient within clouds |
| Asphalt street | Warm gray | #7A7060 | Sun-side lighter (#908A7A) |
| Sidewalk | Pale terracotta | #D8C8A8 | Warm, slightly uneven in color |
| Sidewalk cracks | Dusty lavender | #A89BBF | Painted shadows in cracks |
| Main brick buildings | Terracotta | #C75B39 | Varies per building: some more orange, some more brown |
| Aged brick variant | Dusty terracotta | #A04830 | Older buildings |
| Cream/painted facades | Warm cream | #E8D8B8 | Sun-faded white paint |
| Sage awnings | Faded sage | #7A9E7E | Vary: some more faded, some more vivid |
| Awning shadow-side | Darker sage | #506858 | Underside of awning |
| Building shadow faces | Mid terracotta | #9A4828 | Shadowed side of brick |
| Lavender shadow tone | Dusty lavender | #A89BBF | Cast shadows on all surfaces |
| Window glass (sunlit) | Sky reflection | #C8E0E8 | Slightly bluish, reflective |
| Window glass (shadow) | Dark cool | #2A3840 | Interior depth visible |
| Interior through glass | Warm amber | #D0901A | Warm shop interiors visible |
| Wood-frame buildings | Warm cream boards | #D8C8A0 | Painted wood, weathered |
| Clock tower stone | Warm gray stone | #B0A890 | Old limestone, slight yellow |
| Clock face | Cream | #E8E0C8 | Aged ivory color |
| Clock numerals/hands | Deep cocoa | #3B2820 | Standard dark, not black |
| Tree foliage | Sage green | #7A9E7E | Varied: #607A64 in shadow, #90B888 in sun |
| Tree trunks | Warm dark brown | #5A3820 | Textured grain suggested |
| Wildflowers (fountain) | Mix: terracotta, gold, lavender | Various | Loose dot/shape clusters |
| Power poles | Weathered gray-brown | #7A6850 | Old treated wood |
| Power lines | Dark gray | #4A4840 | Thin but confident lines |
| Antenna metal | Cool silver-gray | #889090 | Galvanized steel |
| Rooflines | Various | — | Each building its own: slate, tin, tile variants |
| Slate roofs | Blue-gray | #708090 | |
| Tin roofs | Pewter | #9A9A8A | |
| Terracotta tile | Muted terracotta | #A85030 | |
| Diner neon | Warm pink-red | #FF6050 | Small but eye-catching |
| Sandwich board | Warm cream | #E8D8B0 | Hand-painted text in deep cocoa |

---

## Prop List — Streetscape Dressing

### Recurring / Consistent Props

**Finch's Bakery Exterior:**
- Wide painted sign above the awning: "FINCH'S BAKERY" in sage-green hand lettering on cream board. Est. date below in smaller type.
- Window display: 3-4 items on a tiered shelf visible through glass. Changes slightly each episode (Finch has a daily special).
- Two large wooden planter boxes on the window ledge: overflowing with a mix of herbs (rosemary, lavender, some mint that has gotten out of hand) and flowers (marigolds in terracotta and gold tones)
- A small chalkboard in the window with the daily special

**Kowalski Hardware:**
- External merchandise: A display rack (wrought iron, older style) holding long-handled tools — rakes, brooms, a snow shovel regardless of season. Chained to a cast-iron ring in the sidewalk.
- Hand-painted window lettering: "HARDWARE — PLUMBING — ELECTRIC — MISC."
- A stack of orange plastic crates near the door, half-filled with assorted items

**The Corner Shop (medium-shot action zone):**
- The sandwich board: Hand-painted message, changes per episode. Examples: "TODAY'S SPECIAL: FIGURING IT OUT" / "ASK ABOUT OUR WORMS" (it's a bait shop) / "MILK INSIDE. PROBABLY FINE."
- A gumball machine just inside the door, visible through glass — vintage, bright red
- A display of postcards in a rotating rack in the window, all showing Millbrook scenes from what appears to be the 1970s

**The Clock Tower:**
- Stone base with a small plaque (too small to read in any standard shot — reward for extreme close-up)
- Four clock faces, each identical. All read 7 minutes slow.
- A pigeon or two always perching on the clockface surround (never the same position)
- A small weathervane on top — iron rooster. The rooster always points in the wrong direction relative to the current wind.

**The Fountain (now planter):**
- Stone basin, circular, classic civic fountain design
- Central element: an abstract sculpture of what might be fish or might be flames — ambiguous and local lore argues about it
- Filled with wildflower growth: tall grasses, marigolds, lavender, the occasional sunflower that's gotten unreasonably tall
- A coin visible at the bottom of the stone basin (no water in it for years)
- A hand-lettered sign on a stake: "PLEASE DO NOT PLANT MORE THINGS — The Millbrook Parks Committee (we had a meeting)"

### Rotating Gags

**The Sandwich Board** (corner shop): New message each episode. By Episode 6, the board has been knocked over in the background of a glitch chase and never quite straightened.

**The Parking Gap:** The same truck is always there but different things are in its bed each episode: lumber, a kayak, inexplicably — a grandfather clock.

**Park Bench Occupants:** Background characters on the benches are consistent types (Old Man With Newspaper, Two Teenagers, Woman With Dog) but their exact positions and activities change. Old Man With Newspaper is always reading it upside-down.

---

## Foreground / Midground / Background Layer Breakdown

### Wide Establishing Shot

**Foreground Layer:**
- A power pole base and the sidewalk at the very bottom of frame (suggests street-level positioning)
- Part of a parked bicycle, chained to the pole, partially cropped
- A cracked section of sidewalk at the bottom edge with a weed growing through it
- Fallen leaf or piece of litter at the corner of the frame
- Rendering: Soft focus at the very bottom edge. Bold values — the darkest darks in the frame are here (pole base, tire shadow)

**Midground Layer (buildings, street level):**
- Full faces of the near buildings on both sides
- The street and sidewalks with pedestrians (background characters)
- Awnings, signs, window displays
- The trees of the town square in the mid-distance
- Power lines running from near-side poles to mid-distance poles
- Characters exist on this plane
- Rendering: Full detail. Sharp edges. Clear color identity for each building.

**Deep Midground (middle distance):**
- The far buildings of both blocks
- The entrance to the town square
- The clock tower becoming the focal point — it should sit slightly above the rooflines of the surrounding buildings, acting as a natural landing point for the eye at the end of the street curve
- Rendering: Slightly reduced detail. Atmospheric softening begins — roughly 10% atmospheric haze applied (sky color tinting the building tones very slightly)

**Background Layer:**
- The sky (the dominant shape above the rooflines)
- The antenna/power line silhouette layer — this is its own semi-transparent graphical layer that sits ABOVE the background sky but BEHIND the building midground. It creates the network silhouette against the sky.
- Distant hills or tree line at the very back (Millbrook is surrounded by low rolling hills)
- Rendering: Maximum simplicity. The sky is flat color shapes (clouds as simple rounded shapes). The distant hills are low-saturation, very slightly blue-shifted sage.

### Medium Shot (Street Level — Outside Corner Shop)

**Foreground Layer:**
- The corner of the sandwich board at the very edge of frame
- Partial view of the awning support pole
- Edge of a parked bicycle, a fire hydrant — something at ground level

**Midground Layer:**
- The full corner shop facade
- The sidewalk in front of it
- The adjacent buildings visible to either side
- A section of the street

**Background Layer:**
- The far side of the street buildings
- The overhead wire network (simplified to key lines only)
- A slice of sky

---

## Painterly-Flat Rendering Notes

### Brick Texture
- Brick is NOT rendered with individual brick detail in backgrounds. Instead: a flat color with a very subtle repeating pattern overlay (small offset rectangle dashes at 15% opacity) that reads as "brick texture" without being literal.
- The mortar lines are only implied in the pattern, not drawn.
- Different buildings have slightly different brick colors (some more orange #C75B39, some more brown-red #A04830, some painted over with cream). This variation is important — it keeps the streetscape from feeling uniform.

### Window Treatment
- Windows are defined by their glass color (reflecting sky or showing interior) and a painted frame (cream or a building's trim color).
- No outlines on the windows themselves — they are defined purely by the glass color against the surrounding wall.
- Some windows have a very subtle curtain shape visible (a softer, lighter tone in the lower portion of the glass).

### Power Lines
- These are thin, confident strokes — slightly curved to suggest weight/sag between poles. They should NOT look perfectly straight.
- Three weights: primary power lines (thickest), secondary utility lines (medium), telephone/cable lines (thinnest).
- A very slight warm-gray color (#6A6858) rather than pure dark, which would make them too dominant.

### Antenna Network
- Each antenna is a unique simplified shape. Some are cross-shapes, some are Y-shapes, some are grid-arrays.
- They should all share the same cool silver-gray tone (#889090) but vary in value based on what sky tone is behind them.
- The cumulative impression is what matters. Don't overwork individual antennas.

### Building Lean and Tilt Rules
- No building is perfectly vertical. Every building leans 1-4 degrees in a direction. The lean should be CONSISTENT per building (it doesn't change frame to frame).
- Adjacent buildings lean in slightly DIFFERENT directions — they don't all lean the same way, which would look like a single collapse rather than organic settling.
- The rooflines are similarly uneven — a building described as "two stories" might be exactly 2 stories at one end and 2.5 stories at the other due to an attic dormer or a slightly higher rear section.
- Rule: The lean should be subtle enough that viewers don't consciously register it, but obvious enough that they'd notice immediately if it were corrected to vertical.

---

## Architectural Style Sheet — Building Construction Rules

### Facade Proportions
- Ground floor: Taller than upper floors. Ground floor ceiling height reads as approximately 12-14 feet (generous commercial space). Upper floors: 8-9 feet each.
- Window-to-wall ratio: Medium. Not a glass box; not a fortress. Approximately 30-40% glass on the front face.
- Shop awnings: Always extend out from the facade on fixed metal frames (not retractable). The awning slope is steep enough to be graphically clear (roughly 30-degree angle).

### Window Patterns
- Ground floor: Large display windows (wider than tall, horizontal proportion)
- Upper floors: Smaller, taller windows (portrait proportion, often in pairs)
- Windows align vertically between floors on brick buildings
- Wood-frame buildings may have windows in more irregular positions

### Roof Types and Rules
- **Flat roofs with parapet:** Used on brick commercial buildings. The parapet (the raised lip at the front of the roof) gives the building a "face" — a graphic edge against the sky. Parapets often have decorative brick work or a simple cornice line.
- **Gabled roofs:** Used on wood-frame buildings and the narrower older brick buildings. Slope is relatively steep (45-60 degree pitch).
- **Hip roofs:** On the post office and larger civic buildings. More traditional, symmetrical.
- **Rule:** No two adjacent buildings have the same roof type. Variety creates the interesting silhouette.

### Decorative Vocabulary
- Brick buildings: Simple decorative arches above upper windows (half-circle in brick). A string course (horizontal band of slightly different brick) at the floor transition. A simple cornice at the roof line.
- Wood-frame: Simple trim boards at corners and around windows. A porch element if the building is on a corner.
- All decorative elements: SIMPLIFIED. One or two shapes suggesting each element, not detailed architectural rendering.

### Color Identity Rules per Building
Each building has a clear, memorable color identity for quick recognition:
- Finch's Bakery: Cream walls, sage green awning — warmth and welcome
- Kowalski Hardware: Dark red-brick (most saturated brick on the street) — solid and established
- The Corner Shop: Lighter brick with a bold sage awning and cream trim — friendly
- The Diner: Cream-painted facade, large window, that pink-red neon — retro
- The Bookshop: Dark sage-painted wood — slightly mysterious, overgrown
- Post Office: Pale terracotta brick, cream-painted windows, very official — institutional but not cold

---

## Key Storytelling Details & Discoverable Background Gags

### Episode-Persistent Details
- **The clock:** Always 7 minutes slow. This is mentioned once in Episode 2 and never addressed again.
- **The empty storefront's window paper:** Something is scratched into the paper from inside. In wide shots it's unreadable. In the one close-up moment (Episode 9), it says "WE ARE STILL HERE." Nobody knows who wrote it.
- **The antenna density:** In Episodes 1-4, this reads as quirky local flavor. Episode 5 reveals the connection. Going back to watch Episode 1, the antenna network looks suddenly ominous.
- **The FOR LEASE sign:** It's been in that window for at least 15 years. The paper has yellowed. By Episode 10, something is visible moving behind the papered window.

### Rotating Gags
- The sandwich board message (changes every episode)
- What's in the truck bed in the parking gap
- Old Man With Newspaper's reading position (he's always got the paper upside-down but his expression never suggests anything is wrong)
- The number of pigeons on the clock tower (increases throughout the season)
- New wildflowers growing in the fountain planter (a new species appears every few episodes)

### Long-term Story Gags
- The antenna glow at night: In Episodes 1-3, no glow. Episode 4: one antenna on the hardware store roof has a faint cyan tinge at night. By Episode 7, three or four do. By Episode 10, the entire roofline network is faintly pulsing at night. The audience is seeing the glitch energy building up. Nobody in Millbrook notices.
- The "For Lease" building's story develops entirely through background detail across 12 episodes.
- After the glitch event of Episode 6, one of the windows in the sliver building appears to have been repaired with what looks like pixels rather than glass (a subtle glitch incursion that nobody fixes because nobody looks up in Millbrook).

---

## Design Rationale

Millbrook's design philosophy is "comfortable strangeness." The town should never feel threatening in its weirdness — it should feel like the natural, slightly-too-much flavor of a real small town where everyone's a little odd. The architectural vocabulary (leaning buildings, uneven rooflines, packed business signage) creates visual interest without any single element being a "gag."

The overhead power-line/antenna network is the most important design decision for the exterior. It creates a visual ceiling over the street that's unique to this location. It also tells the show's thematic story in the background: Millbrook is wired — literally. The town has more antennas per capita than any town this size should. The residents don't think about it. They've always been here. Of course they have.

The gentle street curve gives every shot a natural focal point (the clock tower) without requiring a rigidly symmetrical composition. The curve is your friend — it creates depth, gives characters something to move along, and ensures the backgrounds stay interesting as characters travel through them.
