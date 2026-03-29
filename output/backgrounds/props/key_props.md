# KEY PROPS — Design Document
### "Luma & the Glitchkin" | Background & Environment Design
**Artist:** Jordan Reed | **Date:** 2026-03-29 | **Version:** 1.0

---

## Overview

This document covers four interactive prop designs that recur throughout the series. All of these props are **foreground-interactive objects** and therefore receive **thin outlines** to tie them to the character layer (per style guide). Non-interactive versions of these same props (seen in background layers) use the no-outline painterly-flat treatment.

Props in this show must do two things simultaneously:
1. Feel physically real and specific — weighted, worn, believable as actual objects
2. Feel consistent with the show's flat-graphic visual language — simplified shapes, bold silhouettes, legible at a distance

The balance between these two requirements is different for each prop, and I've noted where each falls on that spectrum.

---

## PROP 1: GRANDMA MIRI'S CRT MONITOR — "THE MONITOR"

**Context:** This is the single most important prop in the show. Everything begins here. The Glitchkin emerged from it. Byte lives in it (partly). When the show needs to feel magical, this monitor needs to earn that magic.

It is not a generic CRT. It is a specific CRT — the kind of high-resolution monitor used by graphic designers and desktop publishers in the mid-to-late 1990s. Grandma Miri acquired it for professional work. It is a serious piece of hardware, larger and more imposing than consumer televisions of the same era.

---

### Shape Language

**Overall silhouette:**
- A deep rectangular box — the CRT tube extends back from the screen face creating a housing that is roughly as deep as it is wide. The screen face is square-ish but with rounded corners (an important distinction from modern flat screens, which have hard rectangular corners).
- The front face has a characteristic 1990s professional-monitor design vocabulary: a slight bevel where the screen glass meets the plastic housing, a recessed screen area (the glass sits slightly back from the outermost plastic edge), and a wide plastic border ("bezel") that is thicker at the bottom than the top.
- The bottom bezel is the "control panel" of the monitor — home to the power button, brightness and contrast knobs, and other adjustments.

**Profile/side view:**
- The critical CRT "wedge" shape: from the side, the housing is deepest at the center-back and tapers slightly toward the top and bottom. The screen face is vertical; the back is a slightly angled surface.
- The neck of the CRT tube (internal, but the housing shape reveals it) creates a slight narrowing behind the screen area.

**Key shape beats (simplified for background use):**
1. The rounded-corner rectangle of the screen face
2. The wider trapezoid of the full housing (wider at the bottom, slightly narrower at the top)
3. The recessed circle of the power button (lower right of bezel)
4. The two adjustment knobs (lower left of bezel) — cylindrical, small
5. The overall silhouette from the front reads as: a wide, rounded rectangle with a slight trapezoidal lean (wider at the base than the top — this is subtle but important for grounding the prop)

---

### Color

| Part | Color | Hex | Notes |
|---|---|---|---|
| Main housing (plastic bezel) | Aged off-white | #D8CEB0 | This is NOT white. It is the specific yellowed cream of 30-year-old computer plastic — a warm cream tending toward yellow. |
| Shadow side of housing | Warm medium gray | #A09080 | The housing shadow is warm, not cool — it's old plastic with decades of ambient warmth soaked in |
| Housing highlight (top/front edges) | Light cream | #E8DEC8 | Where the bevel catches light |
| Adjustment knobs | Slightly darker cream | #B8AA90 | Same material as housing but recessed, lower value |
| Power button | Terracotta red | #B84030 | The one accent color on the monitor. Important. When lit, the LED glow matches electric cyan (the power LED was a feature of this model). |
| Power LED (off) | Dark teal | #203028 | Not glowing, just the lens |
| Power LED (on) | Electric cyan | #00F0FF | A tiny but vital detail — this dot of glitch color on an otherwise analog object is the first visual hint of what this monitor is |
| Screen glass face (off/dark) | Deep teal-black | #0A1E28 | The screen glass has a slight blue-green tint even when off — all CRT glass does |
| Screen glass face (normal/static) | Mixed dark teal → electric noise | #0A1E28 + #00F0FF noise | Rolling static pattern: mostly dark with electric cyan pixel noise |
| Screen glass face (glitch active) | Electric cyan dominant | #00F0FF | Full electric cyan with hot magenta and acid green pixel confetti |
| Screen glass face (the face) | Pixel pattern in cyan | #00F0FF on #0A1E28 | The faint pixel face that stares back. Always present in wide shots if you look. |
| Screen glare highlight | Warm cream (soft) | #F0E8D0 | A soft warm glare shape on the upper-left of the screen glass — mimicking room light reflection. Soft-edged, approximately oval. |
| Ventilation slots | Shadow gray | #706050 | Horizontal slot patterns on the sides and back of the housing |
| Back panel | Slightly darker cream | #C0B290 | The back of the monitor is rarely visible but should be designed |
| Cable sockets (back) | Dark gray | #4A4040 | Multiple socket holes visible in back panel |

**The orange cable** *(canonical spec — cross-referenced in `lumas_house_interior.md`):*
- Color: Burnt orange (#C86820) — warm, distinct from all other cables in the scene
- Material appearance: Fabric-braided outer covering (not smooth plastic) — suggests it is a custom or modified cable
- It exits the back of the monitor from a specific socket (the leftmost, from the back view) and runs off-frame toward the wall
- Near its wall end: a small circular burn mark (#3A2010) on the cable covering — not enough to be alarming, just enough to be notable on close inspection
- The cable has some characteristic drape and curl where it pools on the shelf/floor before running to the wall
- **Narrative note:** This is the "origin cable" — the burn mark marks the moment of the Glitchkin's first arrival. The cable's visual distinctiveness (fabric braid, warm burnt orange color against all other dark cables) is intentional. It is the first thing a careful viewer notices is different about THE monitor's setup.

---

### Design Notes — Rendering at Different Scales

**Wide shot (monitor is one of many objects):**
- Simplified to: housing shape, dark screen, power LED dot, orange cable
- The screen is mostly dark with a subtle cyan center glow
- No control details visible

**Medium shot (monitor is in the background behind characters):**
- Housing shape with ventilation slot texture implied
- Screen active — static pattern or glitch content visible
- Orange cable prominent

**Close-up / hero shot (the monitor is the subject):**
- Full detail: all control elements, ventilation slots, cable exits, the screen pixel face, the specific glare highlight
- The screen content at this scale: individual pixel blocks visible. The "face" in the static is clearly a face at this resolution — two simple squares for eyes, a row of pixels for a mouth. Watching. Always watching.

---

### The Monitor's "Alive" Quality

The monitor should never feel like dead technology. Even in wide shots where it is not the focus, it needs a sense of quiet hum and watchfulness. Three techniques for achieving this:

1. **The glow is never uniform:** The cyan glow on the screen face should be brighter at the center and subtly, very slightly, different in each shot — as if what's displaying is genuinely changing moment to moment. Not so different that it looks animated constantly, but different enough that going back to check, you notice it changed.

2. **The power LED:** This tiny dot of electric cyan on an otherwise warm-colored object is the most efficient "alive" signal in the frame. It costs nothing. It tells you everything. The monitor is on. Something is in there.

3. **The pixel face:** It is always there in wide shots. The position of the two "eye" pixels and the "mouth" pixels changes very slightly each episode — suggesting the face is mobile, conscious, watching. The changes are subtle enough that you wouldn't notice unless you were looking for it. But once you see it, you can never unsee it.

---

## PROP 2: GRANDMA MIRI'S REMOTE CONTROL

**Context:** Grandma Miri has an absurd number of remote controls (there's a whole wicker caddy of them on the coffee table). This specific remote is THE remote — the one she reaches for habitually. It controls the TV, but she also believes (correctly, it turns out) that it has some effect on THE monitor. This has never been tested or confirmed. She just feels it in her bones.

---

### Shape Language

**Overall form:**
- Classic long-form television remote. The shape vocabulary of TV remotes from the late 1990s/early 2000s: longer and narrower than modern remotes, with a slightly tapered top and a wider hand-grip at the bottom.
- The top tapers to a slight point (infrared emitter dome at the very top — a small oval bump).
- The body has a gentle ergonomic curve along its length — slightly concave on the face, slightly convex on the back.
- A battery door covers the lower third of the back — defined by a slightly different material finish and a small release indent.

**Key shape beats (simplified for background use):**
1. The tapered rectangle of the main body
2. The oval infrared emitter at the top
3. A row of 3-4 prominent large buttons (volume, channel, power) in the upper-third of the face
4. A cluster of smaller buttons in a grid (number pad) in the mid-face
5. A slight "waist" narrowing in the lower-mid section (most 1990s remotes had this)

**The Distinct Feature:** This specific remote has a small piece of electrical tape (black) wrapped around the lower third of the body — the old tape solution to a battery door that won't stay closed. This is the identifying mark. This is Grandma Miri's remote.

---

### Color

| Part | Color | Hex | Notes |
|---|---|---|---|
| Main body | Aged black | #2A2828 | NOT void black. This is old TV remote black — faded, slightly warm (decades of hand oils) |
| Body highlight | Dark warm gray | #4A4442 | Top surface catching light — slight gloss on the plastic |
| Button faces (primary) | Dark gray | #383634 | Slightly different from body — the buttons were a different plastic grade |
| Button label text | Faded cream | #C0B8A8 | Screen-printed labels, heavily worn at the most-used buttons |
| Power button | Slightly red-shifted | #3A2626 | The power button has a very subtle reddish tint to its dark — the red indicator graphic has bled into the plastic slightly |
| Volume/channel buttons | Same dark gray | #383634 | These are the most worn buttons — label text is nearly gone |
| Infrared emitter | Dark translucent red | #2A0808 | The emitter dome is a dark red-tinted plastic — transmissive to IR but looks nearly black |
| Electrical tape wrap | Flat black | #1A1818 | Distinct from the aged main body by being more uniformly dark — tape doesn't age the same way plastic does |
| Battery door | Slightly different dark | #302C2A | Material distinction — same era, slightly different feel |
| Remote back face | Matte dark | #242220 | Matte finish on the back vs. slight gloss on the front |

**Special note:** When Grandma Miri holds the remote near THE monitor, in the right scenes, the infrared emitter should emit a very faint pulse of electric cyan (#00F0FF) rather than the standard invisible infrared. This visual cue tells the audience the remote has some unexpected relationship with the glitch technology. It should appear first in Episode 3 and be visible only to careful viewers at that point.

---

### Design Notes

The remote must read as old but loved. Not neglected — LOVED. There's a difference. Neglected means scratched and dusty. Loved means worn specifically at the grip and the three most-used buttons. The wear is a record of use, not abuse.

The electrical tape is essential to the design. It humanizes the remote. Grandma Miri fixed it. She had tape. She used tape. She continues to use this remote with tape on it rather than replacing it. This tells you volumes about her character in a single prop detail.

---

## PROP 3: THE CABLE DRAWER CABINET

**Context:** This cabinet (visible in Luma's house interior, against the right wall) is a wide, shallow wooden cabinet with many small drawers — resembling an old card catalog, apothecary cabinet, or watchmaker's parts organizer. Each drawer holds a different type of cable, connector, or tech accessory, labeled in Grandma Miri's handwriting.

It is a supporting prop in most scenes but becomes a plot-relevant prop in Episode 4, when Luma needs to find a very specific cable and has to search through the drawers.

---

### Shape Language

**Overall form:**
- Wide and low: approximately 4 feet wide, 3 feet tall, 18 inches deep. It sits on slightly splayed legs (the furniture leg style of the 1950s-60s — angled outward slightly).
- The drawer grid: 5 columns across, 6 rows tall = 30 drawers total. The drawers are all uniform size except for the bottom row, which has 3 wider drawers for larger cable coils.
- Each small drawer has a small brass cup pull handle. The wider bottom drawers have two pulls each.
- The cabinet top surface is flat with a slight lip at the back (prevents small items from falling off). Currently holds: a potted aloe vera plant, a small desk fan, and an improbable stack of sticky notes that is structurally unsound but has not fallen.

**Key shape beats:**
1. The overall wide-low rectangle of the cabinet body
2. The grid of 30 drawers (the dominant visual texture of the cabinet face)
3. The brass cup pulls (small accent details — at a distance just dots; up close, distinct shapes)
4. The small paper labels below each pull
5. The angled legs (slightly visible below the bottom row of drawers)
6. The top-surface items (aloe plant, fan)

---

### Color

| Part | Color | Hex | Notes |
|---|---|---|---|
| Cabinet body (main) | Painted cream/ivory | #D0C4A0 | Old painted wood — the paint is slightly chipped at the corners and edges, revealing the wood beneath |
| Exposed wood (chip reveals) | Honey oak | #A07840 | Same honey-oak family as the floor |
| Drawer fronts | Same cream | #D0C4A0 | Flush with the cabinet face, unified treatment |
| Drawer edges (depth shadow) | Warm medium gray | #9A9080 | The shadow gap between drawers and the cabinet body |
| Brass pulls | Aged brass | #A88020 | Not shiny — these are old, oxidized brass. Slightly greenish in the recessed areas (#706030) |
| Paper labels | Aged ivory | #D8C888 | Slightly yellowed small paper rectangles |
| Label text | Deep cocoa | #3B2820 | Grandma Miri's handwriting — all caps, neat, clear |
| Cabinet back (top surface) | Same cream | #D0C4A0 | Continuous with the front |
| Angled legs | Same painted cream | #D0C4A0 | But the very bottom shows unpainted wood (#A07840) |
| Aloe plant (on top) | Sage green | #7A9E7E | The plant is healthy and slightly overgrown (good sign) |
| Aloe pot | Terracotta | #C05838 | Standard terracotta pot, slightly larger than expected for the plant |
| Desk fan (on top) | Aged white plastic | #D8D0C0 | Small oscillating desk fan, same yellowed-plastic era as the monitors |
| Fan grille | Dark gray metal | #4A4840 | Mesh grille |
| Sticky note stack | Soft yellow | #F0E060 | Standard yellow sticky notes |

**The labels:** Grandma Miri has labeled every drawer. Sample labels include:
- "USB-A to B (long)"
- "USB-A to B (short)"
- "FIREWIRE"
- "DVI (BOTH)"
- "VGA (MALE)"
- "VGA (FEMALE)"
- "COAX (coiled)"
- "RCA (red/white)"
- "RCA (yellow)"
- "3.5mm (short)"
- "MYSTERY" (there is always a drawer labeled "MYSTERY")
- "THE ONES I'M NOT SURE ABOUT"
- "IMPORTANT DO NOT OPEN" (it is never explained what's in here; it's never opened on screen)

---

### Design Notes

The cabinet's deep inventory of labeled drawers is the physical representation of Grandma Miri's mind: organized, specific, deeply knowledgeable, and with exactly one drawer that is mysterious and two that are enigmatic. The system works. She knows where everything is. The system has a logic that is entirely her own.

The prop should feel heavy and permanent. It has been in this spot for decades. It belongs here. The floor beneath it has slightly more worn linoleum than the surrounding area (or slightly less worn, depending on whether it was placed there before or after the floor was new). The plant on top has been there long enough that there's a faint water ring on the top surface beneath the pot.

---

## PROP 4: MILLBROOK MIDDLE SCHOOL LOCKERS

**Context:** The hallway lockers are a repeating background element but also a personal expression space for the students. Each student's locker has individual character. A few specific lockers are narrative-relevant: Luma's locker, Cosmo's locker, and Locker 147 (the Glitch Layer encroachment locker).

---

### Shape Language

**Standard Locker Unit:**
- Height: Full-floor-to-ceiling unit (approximately 72 inches / 6 feet). Standard single-tier locker (not stacked two-tier).
- Width: 12 inches. Depth: 18 inches.
- The door has:
  - A vent slot at the top (horizontal rectangular grid of 4-5 slots, each slot approximately 1x0.3 inches)
  - A second vent slot at the bottom (same)
  - A recessed combination lock dial in the upper-center of the door
  - A handle bar below the lock (horizontal, approximately 6 inches wide)
  - No other standard features

**The door surface:** Flat. The only depth elements are the recessed lock and the handle bar. The door face is one unbroken surface — any decoration comes from what students have added.

**Locker column rhythm:** Lockers repeat in a rhythm: locker-locker-locker-locker-locker [wall pilaster] locker-locker-locker-locker-locker. The structural pillars between locker groups give the hallway a visual beat.

---

### Color

**Standard locker colors:**
The school originally painted all lockers in a single color scheme. Years of replacement and repainting have created a complex patchwork. Current distribution:

| Color | Hex | Notes |
|---|---|---|
| Primary locker color: Sage green (faded) | #7A9A7A | The majority — the original school color |
| Secondary: Dusty lavender | #A89BBF | Replacements from a later era |
| Accent: Faded terracotta | #B06050 | The oldest lockers, pre-dating current students |
| Occasional: Industrial gray | #888880 | Single replacements, clearly from the hardware store |

**Standard locker hardware:**
| Part | Color | Hex |
|---|---|---|
| Combination lock dial | Stainless/cool silver | #9090A0 |
| Lock dial numerals | Black markings | #2A2828 |
| Handle bar | Slightly tarnished silver | #808888 |
| Vent slots (shadow) | Dark shadow tone of locker color | Various |
| Door edge shadow (between door and frame) | Dark neutral | #3A3830 |

**Locker character decoration:**
Locker exteriors in a middle school are a key characterization tool. Permitted decoration per the style guide:

- Stickers: Flat graphic shapes at +20% saturation vs. the locker body. Sticker vocabulary: band names, TV show references (cartoon mascots), motivational typography, abstract pixel/geometric patterns, animals, food.
- Photos: Small rectangular shapes on magnets. At background scale, just small warm rectangles with a colored frame. At close-up scale: actual image content.
- Magnets: Small shapes, various colors.
- Dry-erase marker graffiti (on the metal between lockers): VERY subtle — same color as the wall but slightly shinier.

---

### Specific Lockers

**LUMA'S LOCKER (approximately 1/3 from the front of the near section, slightly above eye-level handle — she's shorter than average):**

Exterior decoration:
- A pixel-grid sticker matching her hoodie pattern (the most distinctive identifier) — Electric Cyan (#00F0FF) on a dark background, approximately 2x2 inches
- A sticker of a small cartoon cat in sage green
- A "CAUTION: GENIUS AT WORK" sticker (given by Cosmo; placed ironically; she kept it earnestly)
- A magnetic photo frame with Grandma Miri — too small to see in standard shots, but visible in close-up. Grandma Miri is holding THE monitor in the photo (an old one — the monitor is boxed, unconnected).

Interior (visible when door is open):
- A small mirror on the inside of the door
- Three textbooks stacked: the bottom one is clearly a library book (different wear pattern)
- A bag of snacks (chip bag, crinkled)
- A sticky note from Grandma Miri: "DON'T FORGET TO BE BRAVE" — in the same handwriting as the cable cabinet labels

Color: Sage green (#7A9A7A) — primary school color. A small nick in the paint near the handle reveals the terracotta color beneath (this locker has been green for a while, but it was terracotta before).

**COSMO'S LOCKER (immediately adjacent to Luma's, to her right):**

Exterior decoration:
- No stickers. Cosmo has opinions about unnecessary adhesives on painted metal.
- One magnetic whiteboard, small (4x4 inches), with a current to-do list in precise small handwriting
- A small framed index card with: "PLAN. PREPARE. PROCEED." (Cosmo's personal motto)

Interior (visible when door is open):
- Alphabetically organized textbooks (the labels are handmade and use his own filing system)
- A small container of emergency supplies: mini flashlight, bandages, a folded emergency plan
- A library book always present — different one each episode, always relevant to whatever challenge they're facing
- A photo of his family, bottom corner of the mirror area — small, neat, properly framed

Color: Dusty lavender (#A89BBF) — a replacement locker from a later era. Cosmo did not choose this color. He has made peace with it.

**LOCKER 147 (The Glitch Locker — specific narrative prop):**

This locker is in the hallway section visible from the school entrance — it's passed every episode. A background element that slowly escalates.

Episodes 1-4:
- A completely generic locker. No decoration. The number "147" on the combination lock label (visible in close-up only).
- Color: Industrial gray (#888880) — a replacement, no personality.
- Nothing unusual. Move along.

Episode 5:
- The ventilation slots at the top emit a very faint tinge of electric cyan (#00F0FF) in darker shots. 20% opacity. Barely there.
- The lock dial appears to be spinning slightly even when no one is touching it.

Episode 7:
- The cyan glow through the vents is undeniable in any reasonably-lit shot.
- The number "147" on the lock label has acquired a secondary faint pixel-pattern overlay.
- The locker feels slightly warm to the touch (narrative note; not visual).

Episode 8:
- The combination lock has changed. The previous lock's scratch marks around the dial are still there, but the lock is different — it's a standard combination lock but the dial numerals are replaced with Glitch Layer symbols.
- If you look at the vent slots close-up: pixel grass (Flora 1 from the Glitch Layer) is growing JUST inside the vent, barely visible. A tiny frond of digital organic life, growing in the dark of an unused locker.

Episodes 10-12:
- A very faint sound (sound design note): a digital hum emanates from this locker, barely audible under dialogue.
- The cyan glow now pulses.
- The seam around the door has a faint line of acid green (#39FF14) — a second Glitch Layer color appearing.
- Something is clearly trying to get out, or come through. This is the secondary portal plot thread.

---

### Locker Rendering Notes

**Standard background use (hallway establishing shot):**
- Individual lockers are simplified to: the main body rectangle, the vents as a horizontal texture pattern (not individual slots), the handle as a horizontal bar, the lock as a small circle.
- The color variation between locker types (sage, lavender, terracotta, gray) gives the wall visual rhythm without requiring each locker to be individually detailed.
- At the farthest visible distance, the entire locker wall simplifies to two alternating tone strips: the locker faces (their color) and the dark door-gap lines between them.

**Close-up / featured locker shots:**
- Full detail: visible vent slot grids, lock dial numbers/markings, handle geometry, decoration in detail.
- Outline treatment: thin line in deep cocoa (#3B2820) on the door edges and handle — the foreground interactive object outline treatment from the style guide.
- The vents receive special care — the shadow within the slots is the darkest value on any locker; this is where the detail reading lives.

---

## Shared Design Notes — All Props

### The Outline Treatment Rule
All four props receive thin outlines in deep cocoa (#3B2820) when they are foreground interactive objects — i.e., when a character is about to touch or use them, or when they are the subject of a close-up shot. Background versions of the same props (visible but not in focus) use the no-outline painterly-flat treatment.

The outline weight: approximately 1.5-2px at standard character layer line weight. Lighter than character outlines. The props should feel connected to the character layer without competing with character silhouettes.

### Age and Wear Vocabulary
All props in Luma's house are old. None of them look new. The age shows in:
- **Plastic:** Yellowing (cream-shift in base color), slight dulling of sheen (the gloss coat has degraded).
- **Metal:** Oxidation on brass (warmer, then greener where moisture collects), tarnish on silver-toned metal (darker, cooler).
- **Paint:** Chips and wear at corners and edges (the highest-contact points wear first). Fading on the areas exposed to light. Ghost marks of previous iterations visible.
- **Fabric/tape:** Yellowing, slight shrinkage/warping.

The school lockers show different aging: institutional metal paint, scratched and dented by the cumulative impact of a decade of backpack impacts, kicked bottoms, and slammed doors.

### The "This Exists" Principle
Every prop should feel as if it exists somewhere in the real world and you could find one if you knew where to look. The monitor is a real class of monitor — research period references. The remote is a real remote. The cabinet is something a real person made or bought. The lockers are the same as millions of school lockers installed between 1985 and 2005.

The world of this show is heightened but not fabricated. The glitch elements are the only truly impossible things. Everything else — every prop, every building, every sticker — should feel like something that actually exists. That groundedness is what makes the Glitch Layer so powerful when it appears. It's wrong against a world that is right.
