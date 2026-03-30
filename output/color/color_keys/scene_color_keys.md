<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Scene Color Keys — "Luma & the Glitchkin"

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**Version:** 2.0 (Cycle 2 — opacity specs eliminated, Key 02 exception documented, Key 04 ambient fill corrected)
**References:** master_palette.md v2.0, style_guide.md v1.0

> Color keys define the definitive light and atmosphere of each major scene type. These are not suggestions — they are the emotional and visual contract between the color department and every artist who paints a frame in this scene. Every background, every effect, every shadow in a scene must answer to its color key.
>
> **Cycle 2 Change Summary:** All opacity-based shadow specifications replaced with flat hex values. Key 02 dominant color count exception formally documented. Key 04 ambient fill corrected from Sunlit Amber (violates use-case caveat) to Warm Cream.

---

## COLOR KEY 01 — SUNNY AFTERNOON AT LUMA'S HOUSE

**Scene Type:** Daytime interior/exterior establishing / slice-of-life
**Emotional Intent:** Safety, warmth, wonder, the feeling of a home that holds secrets. This is the calm before the adventure. The audience should feel *at home* here — and therefore feel what Luma has to lose when the Glitch World threatens it.
**Palette Family:** Real World dominant (95%). Glitch intrusion: trace level only (5% — just enough to hint the CRT is alive).

---

### Lighting Setup

**Sky / Ambient Color**
- Primary: `#FAF0DC` (Warm Cream) — an afternoon sky so gentle it's almost white-gold
- At the horizon: `#E8C95A` (Soft Gold) bleeds upward from the light source direction
- Ambient fill on shadow-facing walls: `#A89BBF` (Dusty Lavender) — cool sky bounce, barely visible

**Key Light**
- Color: `#E8C95A` (Soft Gold) with a slight push toward `#D4923A` (Sunlit Amber) on surfaces that have been sun-soaked for decades (aged wood, old brick)
- Direction: From the right — about 2-3 o'clock, low in the sky for late-afternoon feel
- Quality: Soft-edged but directional; this is not harsh noon light. Think of sunlight coming through leafy curtains, slightly dappled.
- Shadow cast color: `#5C4A72` (Shadow Plum) — flat hex, no opacity modifier. Warm sunlight creates cool purple-leaning shadows; use this value directly.

**Fill Light**
- Color: `#A89BBF` (Dusty Lavender) — indirect skylight from the open window
- Direction: Left side, slightly above horizontal — the open side of the scene
- This is the secondary light that holds detail in shadow — it prevents shadow areas from going too dark and maintains the safe, welcoming quality

**Shadow Color**
- Shadow fill on warm surfaces (cream walls, wood floors): `#5C4A72` (Shadow Plum) — deep lavender shadows keep warmth in the scene without going flat
- Shadow fill on green surfaces (plants, garden): `#4A6B4E` (Deep Sage)
- Shadow fill on skin: `#8C5A38` (Skin Shadow)
- Deepest shadow (under furniture, in corners): `#3B2820` (Deep Cocoa)
- Shadow cast on floor from characters: `#3D2F4F` (Shadow Plum Deep) — a slightly deeper flat value for cast shadows; provides separation from ambient shadow without requiring opacity blending. **Do not use "#5C4A72 at any opacity" — use `#3D2F4F` directly.**

---

### Palette Composition

**Palette Ratio:**
- `#FAF0DC` Warm Cream — 30% (largest area: walls, ceiling, sky outside window)
- `#E8C95A` Soft Gold — 18% (sunlit floor, open window, lit surfaces)
- `#C75B39` Terracotta — 15% (architectural details, brickwork, warm furnishings)
- `#7A9E7E` Sage Green — 12% (plants, garden outside window, Grandma's cardigan)
- `#A89BBF` Dusty Lavender — 10% (shadow areas, blue-grey objects)
- `#3B2820` Deep Cocoa — 8% (furniture, lines, Luma's hair)
- `#C4A882` Warm Tan — 5% (skin, wooden floor planks)
- `#00F0FF` Electric Cyan — 2% (trace glow from the CRT screen — barely visible, just enough to notice)

**Total: 7 dominant colors — at the upper limit of scene budget. The Cyan trace is the one "wrong note" that signals this safe space is not entirely ordinary.**

---

### Accent Colors
1. `#B8944A` (Ochre Brick) — aged books, worn wood details, vintage tech casings; provides warmth-within-warmth
2. `#5B8C8A` (Muted Teal) — the CRT monitor casing; its slightly digital quality quietly foreshadows the glitch world
3. `#00F0FF` (Electric Cyan) — only as a very subtle screen glow on the CRT face; this single intrusion of glitch color makes the scene *hum* with possibility without breaking the warm idyll

---

### Cinematography Notes
The warmth should cascade from upper-right to lower-left. The viewer's eye should be guided from the warm exterior light at the window toward the room's interior, where the CRT sits in a cooler zone. This creates a natural lighting path from "safe warm world" to "mysterious digital world" within a single frame. Luma, as protagonist, should be positioned where both light sources touch her — she belongs to both worlds.

---
---

## COLOR KEY 02 — NIGHTTIME GLITCH ATTACK ON MAIN STREET

**Scene Type:** Action / tension / intrusion scene; typically in Act 2 of a standard episode
**Emotional Intent:** Danger, urgency, the violation of a familiar safe space. The Real World is no longer safe — the Glitch is HERE. The town the viewer has come to love is under attack, and the color must communicate that wrongness immediately. This should feel like a fever dream — familiar shapes in wrong colors.
**Palette Family:** Real World dominant (55%) fighting Glitch intrusion (45%). Neither side is winning yet. This is the escalation before the climax.

---

### Lighting Setup

**Sky / Ambient Color**
- Primary sky: `#1A1428` — a deep blue-purple, darker than Shadow Plum, approaching void but with warmth of a real night sky (not derived from the glitch palette)
- Glitch-affected sky zones: `#7B2FBE` (UV Purple) replacing the natural dark sky wherever glitch energy is active — this is the key visual signature of an attack; the sky itself changes color
- Moon light ambient: `#C8BFD8` (light lavender) — thin, cool, and slightly eerie

**Key Light**
- Color: `#00F0FF` (Electric Cyan) — the primary glitch energy acts as the key light in glitch-active zones. Street lamps have been overloaded and flicker; wherever glitch energy arcs, it washes everything in cyan.
- Direction: Multiple sources — glitch energy can come from multiple angles, so there may be competing key lights in the same frame (intentional chaos). Primary crack in the sky illuminates from above-left.
- The natural moonlight key (cool silver-lavender) is being overridden by the Cyan — old shadows and new Cyan shadows are overlapping and creating double-shadow confusion

**Fill Light**
- Color: `#FF2D6B` (Hot Magenta) — the secondary glitch light fills in from the opposite direction, from cracks in the road and walls. This means characters caught between a Cyan key and a Magenta fill are dramatically lit by both glitch colors simultaneously — their flesh and costume reads as surreal and alien.
- The real-world fill light (ambient moonlight/lavender) is still present as a weak underlying source; it is being overpowered

**Shadow Color**
- Shadows in glitch-lit zones: `#0A0A14` (Void Black) — the combined cyan and magenta light creates extremely high-contrast, nearly-black shadows. This is intentional: when the Glitch attacks, the world loses its nuance.
- Shadows in moonlit zones (away from glitch activity): `#5C4A72` (Shadow Plum) — normal nighttime shadows still apply in un-glitched areas
- **Double-shadow overlap zone** (where glitch-lit shadow and moonlit shadow co-occur at the boundary between infected and uninfected areas): `#332A43` — target hex for the overlap zone. Derivation: arithmetic average of Void Black (`#0A0A14`, R:10 G:10 B:20) and Shadow Plum (`#5C4A72`, R:92 G:74 B:114) → R:51 G:42 B:67. Decision rationale: average chosen over the darker value because the overlap zone is a transitional boundary, not a pure glitch shadow — using the average produces a dark, deep purple that reads as "both shadow systems present simultaneously" rather than "glitch has fully won." It is darker than Shadow Plum alone and warmer than Void Black alone — the correct expression of contested territory.
- Cast shadows on ground from characters: `#050F14` — a very dark, hard shadow value for the extreme contrast of a multi-source glitch attack; use flat, no opacity modifier. **Do not use "#0A0A14 at 80%" — use `#050F14` directly.** This is a near-void dark blue value that reads as an extremely sharp, disorienting shadow under competing glitch lights.

---

### Palette Composition

**Palette Ratio:**
- `#1A1428` Night Sky — 25% (sky field)
- `#3B2820` Deep Cocoa — 15% (building forms at night, darkened storefronts)
- `#00F0FF` Electric Cyan — 18% (glitch energy, crack illumination, overloaded streetlamps)
- `#FF2D6B` Hot Magenta — 12% (danger glitch cracks, corruption flares)
- `#7B2FBE` UV Purple — 10% (glitch-infected sky segments, portal haze)
- `#C75B39` Terracotta — 8% (building walls, still partially lit by warm remnant of prior daylight — memory of warmth)
- `#F0F0F0` Static White — 7% (glitch sparks, overload flashes, pixel confetti)
- `#FAF0DC` Warm Cream — 5% (window lights from scared townspeople inside buildings — the last vestige of the safe warm world, seen as glowing rectangles)

**DOMINANT COLOR COUNT EXCEPTION — FORMALLY DOCUMENTED:**
This key lists 8 dominant colors against the standard 7-color scene budget. This exception is justified on the following grounds:
1. The narrative premise of this scene type is *two palette worlds in direct conflict* — Real World (warm) vs. Glitch (cool). Both palette families must be present in meaningful proportion for the scene to function. Reducing to 7 would require eliminating either `#C75B39` (Terracotta) or `#FAF0DC` (Warm Cream) — both of which are structurally critical: Terracotta is the residual-warmth that signals "this was a safe town," and Warm Cream windows are the emotional heart of the key (the last vestige of safety, being extinguished). Neither can be cut.
2. The 8th color (`#FAF0DC`) covers only 5% of the palette — it is a micro-accent, not a dominant. In terms of visual weight, this is functionally a 7-dominant + 1-accent composition. The listed 8th should be treated as accent-tier, not dominant-tier, when balancing the scene.
3. **Art Director approval noted for this exception.** Any further expansion beyond 8 dominant colors in this scene type is not approved.

---

### Accent Colors
1. `#39FF14` (Acid Green) — Glitchkin emerging from cracks; their markings (not storm energy) cutting across the cool glitch palette. **Acid Green here is attributed to specific Glitchkin characters only — do not use it as a freestanding storm effect particle (see Forbidden #8).**
2. `#E8C95A` (Soft Gold) — an isolated warm glow from a single lamp that hasn't been overloaded yet; one warm light in a glitching world is devastating
3. `#A89BBF` (Dusty Lavender) — townspeople's pale faces seen in windows; their fear rendered in desaturated lavender skin is quietly heartbreaking

---

### Cinematography Notes
The warm-cold split should be horizontal: ground level and building bases retain residual warmth (Terracotta architecture, remnant warm lighting), while everything above eye level transitions into glitch-infected purple-night. The "invasion comes from above" visual metaphor is built into the color — warm below, cold chaos above. Luma and Cosmo running in the foreground are surrounded by warmth from the building walls (their world is still close) but the sky above them is entirely lost. This reinforces that they are fighting for ground they are already losing.

---
---

## COLOR KEY 03 — FIRST ENTRY INTO THE GLITCH LAYER

**Scene Type:** World-reveal / awe / otherworldly environment introduction
**Emotional Intent:** Disorientation, wonder, overwhelm, and a precise undercurrent of danger. This must be *beautiful* in a way that is totally unlike the Real World — a beauty that is alien and slightly wrong, like looking at deep-sea creatures for the first time. The audience should feel what Luma feels: "I should not be here, but I cannot look away."
**Palette Family:** Glitch dominant (90%). Real World presence: 10% or less — trace memory on Luma and Cosmo's warm skin tones and Cosmo's lavender jacket.

---

### Lighting Setup

**Sky / Ambient Color**
- Primary void: `#0A0A14` (Void Black) — the sky/background is the digital void, vast and lightless
- Ambient luminance: `#7B2FBE` (UV Purple) fills the space between structures — the Glitch Layer is not dark so much as *differently lit*; the ambient is purple, like light from a star that doesn't exist in the Real World
- Data-stream glow: `#2B7FFF` (Data Stream Blue) streams of scrolling code descend in columns, each acting as a secondary ambient light source, casting blue light on nearby platforms

**Key Light**
- Color: `#00F0FF` (Electric Cyan) — the primary light sources in the Glitch Layer are glitch energy itself. The closest structure to Luma (a floating platform, an active data node) emits Cyan light as the key.
- Direction: Below and slightly forward — much of the Glitch Layer's light comes from *below* (from glowing structures, from light emanating off the void floor far below). This creates an unusual under-lighting that makes familiar faces look slightly alien — intentional. This is not their world.
- The under-lighting on Luma's face is one of the most important single color decisions in the show: it signifies she has crossed into somewhere genuinely Other.

**Fill Light**
- Color: `#7B2FBE` (UV Purple) — the ambient purple glow fills the opposite side of all forms
- Secondary fill: `#39FF14` (Acid Green) — from the digital flora: pixel-art plants and data-moss glow faintly with green light, providing a tertiary fill on nearby surfaces

**Shadow Color**
- Shadow zones: `#050508` — even deeper than Void Black for the absolute dark zones behind structures (nearly invisible; gives depth and scale). Per master palette GL-08a exception note: restricted to small-area use, maximum 2-3% of frame.
- Character shadow zones under Cyan key: `#7B2FBE` (UV Purple) — in this world, shadows take on the ambient purple color
- The interaction of Cyan key + Purple shadow on warm-skinned characters creates an extraordinary effect: skin reads as slightly teal-purple, unlike anything in the Real World. This should be striking, not alarming — wonder, not horror.

---

### Palette Composition

**Palette Ratio:**
- `#0A0A14` Void Black — 35% (deep space, shadow volumes, void background)
- `#7B2FBE` UV Purple — 22% (ambient sky, shadow fill, mid-space volumes)
- `#00F0FF` Electric Cyan — 18% (primary light sources, platform edges, Byte's glow)
- `#2B7FFF` Data Stream Blue — 10% (data waterfalls, navigable pathway indicators)
- `#39FF14` Acid Green — 8% (digital flora, Glitchkin markings in background)
- `#F0F0F0` Static White — 4% (specular pops on node surfaces, glitch sparks)
- `#C4A882` Warm Tan — 3% (Luma and Cosmo's skin — the only Real World warmth; this single remnant of human color in a sea of glitch makes them feel vulnerably, preciously human)

**Total: 7 colors — at palette limit. The warm skin tone #C4A882 at 3% may be the most emotionally important 3% this show will ever use.**

---

### Skin Rendering in the Glitch Layer
**All character skin tones in this environment use DRW-11 (Glitch-Modified Skin Base) and its shadow/highlight companions (DRW-11a, DRW-11b) instead of standard skin values. See master_palette.md Section 1B.** Painters must not apply standard warm-skin values (RW-10, RW-10b) to any human character in the Glitch Layer. The UV Purple ambient modifies all warm skin toward a lavender-washed tone — using standard skin creates incorrect warm-skin results in a cyan-dominant, purple-ambient environment. Reference the full skin variant table in style_frame_03_other_side.md (Glitch Layer Skin Highlight Variants section).

### Accent Colors
1. `#FF2D6B` (Hot Magenta) — visible at distance, in the deeper glitch structures; signals that the dangerous parts of the Glitch Layer are out there, even if they're not here yet. Use it only in the far background on first entry.
2. `#FF8C00` (Corrupted Amber) — objects from the Real World that have been drawn into the Glitch Layer (a mailbox, a street sign) shimmer at the edges with this corrupted amber glow, half-transformed
3. `#F0F0F0` (Static White) — pixel confetti particles of this color drift in the air all around the Glitch Layer; it is the most consistent visual signature of this world (per the style guide's "pixel confetti" directive)

---

### Cinematography Notes
Scale is the visual priority of this scene. The color must serve the sense of vastness. This is achieved through atmospheric perspective using the Glitch palette: close structures are in bright Cyan and Acid Green, mid-distance structures shift toward Data Stream Blue and UV Purple, far structures approach Void Black. The standard warm atmospheric haze of the Real World (where distant things go warm) is inverted here — distant things in the Glitch Layer go cool and then dark. Up close is alien and saturated; far away is the void. This makes the world feel like it extends forever and that "forever" is terrifying.

---
---

## COLOR KEY 04 — QUIET EMOTIONAL MOMENT

**Scene Type:** Intimate dialogue scene / character moment / emotional beat
**Emotional Intent:** Vulnerability, connection, the world going quiet so two people can be real with each other. This is the counterweight to all the chaos. The Glitch World should feel very far away. This scene is warm, small, and honest.
**Palette Family:** Real World dominant (98%). Glitch: effectively absent — only a trace if the scene calls for a single poignant reminder (e.g., Byte quietly present, his glow just barely visible).

---

### Lighting Setup

**Sky / Ambient Color**
- Setting: Late evening interior, or early morning. Time-of-day creates intimacy.
- Ambient: `#FAF0DC` (Warm Cream) at low intensity — the ambient fill for walls and large background surfaces in this scene. **CORRECTION FROM v1.0: Sunlit Amber (`#D4923A`) has been removed as the ambient fill. Sunlit Amber's use-case notes explicitly state "avoid as broad fill — too saturated for large ambient areas." Using it at 20% of the scene palette directly violated this constraint. The amber quality of the scene is preserved through the key light (Soft Gold on specific lit surfaces) while the ambient remains the correctly desaturated Warm Cream.**
- The golden hour quality is still present in this scene — it comes from the key light hitting specific surfaces, not from a broad saturated ambient wash. The distinction is between "a warm room" (broad desaturated fill) and "warm light striking surfaces" (key light on specific shapes).
- Secondary ambient: `#A89BBF` (Dusty Lavender) from the blueing sky outside — there is a slight cool from the window that keeps the frame from becoming saccharine

**Key Light**
- Color: `#E8C95A` (Soft Gold) — a single warm practical light source (a lamp, a candle, the last light through a closing window). This is *small* light. Not sun-scale: human-scale.
- Direction: Slightly above eye level, close — this is an intimate light. The kind of light that says "we are the only two people in the world right now."
- Quality: Soft fall-off. The light does not reach far; the edges of the frame drift toward the ambient twilight.

**Fill Light**
- Color: `#A89BBF` (Dusty Lavender) — the cool blue of the evening sky outside fills the shadow side of characters, providing just enough detail to read clearly without competing with the warm key
- This creates a warm/cool split on each character's face: warm gold on the light side, soft lavender in the shadow. This is the cinematographer's classic "beauty light" and it reads as "tender" in this context.

**Shadow Color**
- Lit side shadows: `#8C5A38` (Skin Shadow) — warm as always
- Shadow side: `#5C4A72` (Shadow Plum) — the secondary cool shadow, slightly deeper than the fill light in value
- Clothing shadows: deepened versions of their respective costume colors (see master palette character sections)
- The floor shadow from characters: `#5C4A72` (Shadow Plum) — use this flat value directly. The scene has low contrast overall; the Shadow Plum reads as the soft, barely-visible cast shadow appropriate to this mood. **Do not use "#5C4A72 at 50%" or any opacity modifier — use the flat hex and rely on its inherent lightness to read as a gentle shadow. If a yet-softer cast shadow is needed, step up to `#A89BBF` (Dusty Lavender) as a very faint cast shadow tone.**

---

### Palette Composition

**Palette Ratio:**
- `#FAF0DC` Warm Cream — 35% (walls, surfaces — the quiet background; increased from v1.0 to account for removal of Sunlit Amber ambient)
- `#E8C95A` Soft Gold — 15% (direct warm lamp light on lit surfaces — now correctly identified as key light on specific shapes, not ambient fill)
- `#A89BBF` Dusty Lavender — 15% (shadow fill, evening sky, cool secondary light)
- `#C4A882` Warm Tan — 12% (skin fills — characters are close and their faces are large; increased from 10% to compensate for palette shift)
- `#5C4A72` Shadow Plum — 8% (deepest shadow areas, shadow sides of faces)
- `#3B2820` Deep Cocoa — 4% (line color, Luma's hair, small dark accents)
- `#00F0FF` Electric Cyan — 1% (barely-visible Byte glow, if present; an ember of the adventure, kept in)

**Note: Sunlit Amber (`#D4923A`) has been removed from the dominant palette of this scene. It may appear in small supporting details (a warm mug, a book spine catching the lamp light) as an accent, but it must not exceed 3% of the palette and must not be used as the ambient fill for room surfaces. Total: 7 dominant colors — within palette limit.**

---

### Accent Colors
1. `#8C5A38` (Skin Shadow) — the warm shadow tone on faces; in close-up, skin gradation is everything
2. `#C75B39` (Terracotta) — a warm-colored object nearby (a blanket, a mug, a worn chair) that provides a single saturated warm note in an otherwise muted scene
3. `#00F0FF` (Electric Cyan) — used at extreme restraint (1% of palette); if Byte is present, his glow is the only source of this color. It is both beautiful and slightly sad in this context — a reminder of the other world, present but quiet.

---

### Cinematography Notes
The compositional principle for this scene is *proximity*. Faces fill more of the frame than in any other scene type. The backgrounds are reduced to soft washes of color — no hard edges, no sharp detail. Focus pulls the eye inward to the characters. The color temperature split (warm light, cool shadow) should be cleanest in this scene — it is the most "composed" lighting in the show, because the moment itself is composed and considered. There are no surprises in the light. Every shadow is where it belongs. The Glitch World is, briefly, elsewhere.

---

*Document version 2.0 — Sam Kowalski — 2026-03-29*
*Cycle 2 revision: All opacity-based shadow specs replaced with flat hex values. Key 02 dominant color count exception formally documented. Key 04 ambient fill corrected from Sunlit Amber to Warm Cream.*
