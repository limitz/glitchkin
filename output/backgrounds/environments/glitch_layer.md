<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# THE GLITCH LAYER — Digital Dimension Environment Design
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
- **Filename convention:** `LTG_ENV_glitch-layer_v###.psd`
  - Example: `LTG_ENV_glitch-layer_v001.psd`
  - Example: `LTG_ENV_glitch-layer_v002.psd`
- **Delivery PNG:** `LTG_ENV_glitch-layer_v###.png`
- **Shot codes in use:** `WIDE_ARRIVAL` / `WIDE_CHASE` / `MED_PLATFORM_CONVO` / `MED_BOSS_ZONE` / `CU_CORRUPTION_ZONE` / `CU_WATERFALL`
- **Tile/module assets** (reusable elements): `LTG_ENV_glitch-layer_TILE_[element-code]_v###.psd`
  - Example: `LTG_ENV_glitch-layer_TILE_PLATFORM-A_v001.psd`, `LTG_ENV_glitch-layer_TILE_FLORA-GRASS_v001.psd`

> **Note on internal PSD layer naming:** The layer naming convention inside the file (e.g. `GL_BG_VOID`, `GL_MG_PLATFORMS`, `GL_CORRUPTION_OVERLAY`) remains unchanged. These are intra-file identifiers, not filenames. The `LTG_ENV_` convention applies to the filename only.

### Required PSD Layer Structure
All master PSDs for this environment must include the following named layer groups, in order from top to bottom:
1. `FG` — Foreground platform fragments, foreground pixel flora
2. `MG_CHAR` — Character plane (empty — reserved for animation)
3. `MG_PLATFORMS` — Primary character-accessible platforms and flora
4. `MG_WATERFALLS` — Code waterfall columns (midground)
5. `DEEP_MG` — Deep midground platforms, impossible geometry structures
6. `BG_AURORA` — Aurora data-streams (soft, large-scale background)
7. `BG_VOID` — Void depth base, grid overlay, UV purple depth banding
8. `CORRUPTION_OVERLAY` — Corruption Zone patches (separate for easy escalation across episodes)
9. `CONFETTI` — Pixel confetti particle layer (animated separately)
10. `WRONG_PARALLAX_NOTE` — (Annotation layer only, non-printing) Notes on inverted parallax direction for layout team

---

## Overview & Design Intent

The Glitch Layer is the most demanding environment in the show — and the most free. It has no architectural rules borrowed from the real world. Gravity is optional. Scale is unreliable. Logic is decorative.

The design challenge is not creating chaos — chaos is easy. The challenge is creating a space that feels genuinely alien and wrong while still being beautiful, navigable, and narratively legible. Characters need somewhere to stand and talk. The audience needs to understand what they're looking at. But none of it should feel safe or familiar in the way Millbrook and Luma's house do.

My core design principle for the Glitch Layer: **it is a broken memory of what digital space once tried to be.** Early computing imagined cyberspace as something grand — vast, geometric, ordered. The Glitch Layer is what happened to that vision when the data started to corrupt. It's trying to be something beautiful and organized and it's failing in fascinating ways. The geometry that should be perfect has errors. The code that should flow cleanly is scrambled. The colors that should be harmonious are oversaturating, bleeding, clashing.

But the broken-ness is not ugly. It's art. A cracked stained-glass window is still beautiful.

**Most visually complex environment in the show.** Every shot here should feel like a discovery. Use restraint in individual elements to let the composition as a whole breathe.

---

## Spatial Layout

### The Nature of Glitch Layer Space

The Glitch Layer does not have a fixed geography in the way the real world does. It is not a planet you could map. However, certain features recur reliably and constitute the "landmarks" of this dimension:

**The Void Floor (The Absence):**
- The baseline of the dimension is void — Void Black (#0A0A14) with a faint grid overlay (very subtle, grid lines in #141428 at 10% opacity). The grid is not perfectly straight — it curves and bends near high-energy zones, suggesting spacetime distortion.
- The "floor" is not truly a floor. Characters can fall through it if the narrative calls for it. But in most shots, there is an implied ground plane — it's just that the implied plane is a floating platform, not a continuous surface.
- Important: the void should always have depth. It is not flat. Distant zones of the void show faint deep-space color banding (UV purple #7B2FBE at extreme distance, barely perceptible) suggesting it goes on forever.

**The Platform Archipelago:**
- Floating geometric platforms of wildly varying sizes. These are the "land" of the Glitch Layer.
- Size range: From platforms small enough for one character to stand on (roughly 6 feet across) to massive floating islands covering the area of a city block.
- Shape vocabulary: All platforms are geometric — squares, rectangles, hexagons, L-shapes, stepped pyramids, rings with holes, impossible multi-sided shapes. NO organic/natural shapes except where explicitly overridden by pixel-flora growth.
- Material appearance: The platforms are made of what looks like solid pixel blocks — their faces are uniformly colored flat shapes with occasional visible "pixel seams" (faint grid lines within the surface at 8% opacity). They are not stone or wood or metal — they are pure rendered geometry.
- Surface colors: Each platform type has its own color identity (see tile/module sheet section below)
- Edges: The edges of platforms are sharp and clean. The contrast between a platform's flat face and the void beneath it is one of the most important shapes in any Glitch Layer composition.

**The Code Waterfalls:**
- Waterfalls of scrolling text/code that descend from nowhere (they don't start at a ceiling or water source) and fall into the void below (they don't end in a pool or a floor).
- The code itself: The characters are a mix of binary (01001), hexadecimal notation (0xF3 A2 7B), and something that looks like a language that doesn't exist. Some of the "code" resolves, if read carefully, into fragments of words: "HUNGRY" "HERE" "WHERE" "LUMA" "NO" "STAY." The Glitchkin are in this code.
- Visual treatment: The code is rendered as light — glowing lines of Acid Green (#39FF14) against the void. The lines scroll downward at a constant rate. The edges of each waterfall are slightly soft (the column of scrolling text is defined but the outer edges have a glow halo of 3-4 pixels).
- Width variety: Code waterfalls range from narrow trickles (one character wide) to broad rivers 20+ feet across.
- The sound design team should note: these have a visual tempo. The scroll speed is about 60 lines per second for fast waterfalls, 20 for slow. This can be suggested in timing marks on background layouts.

**The Aurora Data-Streams:**
- Far in the background of wide Glitch Layer shots, flowing bands of light travel horizontally across the void like aurora borealis.
- Colors: Electric Cyan (#00F0FF), UV Purple (#7B2FBE), Hot Magenta (#FF2D6B) — in broad soft bands that pulse slowly.
- These are large-scale, distant. They are never in the foreground. Their purpose is to give the void background a sense of scale and motion.
- The flow direction is always left-to-right in establishing shots (a visual convention that helps the audience orient).
- These bands have soft, cloudlike edges — they are the only truly soft/gradient element in the Glitch Layer (everything else is flat/sharp).

**The Pixel Flora:**
- Plants exist in the Glitch Layer but they are made of visible pixel blocks. They are digital approximations of organic life, rendered at various resolutions.
- Resolution rules: Plants near the camera are rendered at lower resolution (bigger, more visible pixel blocks) while plants in the distance paradoxically render at higher resolution (smaller, tighter pixel blocks). This is one of the space's wrong-direction parallax rules.
- Flora types (detailed descriptions below in the Prop section)
- Color: Pixel flora is primarily Acid Green (#39FF14) with secondary accents of Electric Cyan (#00F0FF) and Soft Gold (#E8C95A — a real-world color intruding, which feels slightly wrong and slightly wonderful)
- The flora does NOT move organically. It either remains perfectly still (no wind-sway) or animates in rigid rotations (a "flower" opening is 4 frames: bud → half open → open → back to bud, on a loop with no easing).

**The Impossible Geometry Structures:**
- The architectural set-dressing of the Glitch Layer: structures that use Escher-like spatial impossibility.
- Examples: A staircase that connects a high platform to a low platform but if you follow it you arrive back where you started. A corridor that is visible from the outside but contains more interior space than its exterior suggests. A tower that is simultaneously wider at the top and bottom than in the middle. A bridge with two endpoints but no clear middle section — it just... continues on both ends into the void.
- These structures are not physically traversable (they break the rules they would need to follow) but they are powerful BACKGROUND ELEMENTS that establish the wrongness of this space.
- Visual treatment: Rendered in UV Purple (#7B2FBE) and Electric Cyan (#00F0FF) — the coolest colors of the palette, suggesting unreality.

**The Corruption Zones:**
- Areas where even Glitch Layer logic breaks down — the equivalent of a blue-screen-of-death in this dimension.
- Visual: Patches of pure Static White (#F0F0F0) noise — like television snow — that hang in the void. They are flat, 2D-looking (like a sticker placed on a 3D scene). They have jagged, shifting edges.
- Hot Magenta (#FF2D6B) sparks fly off them intermittently.
- Corruption Zones are danger indicators. Characters and Glitchkin alike avoid them. They represent the True Corruption — the villain of the show — and their visual vocabulary (white noise, magenta sparks) is distinct from everything else in the Glitch Layer.
- Size: Usually small in early episodes (tennis-ball to car size). Grow throughout the season.

---

## Lighting Setup

### The Nature of Glitch Layer Light

There is no single light source in the Glitch Layer. Everything glows slightly. But glow levels are not uniform — they create a hierarchy of luminance that guides the eye.

**1. The Ambient Base Glow**
- The void itself emits a barely-perceptible ambient light. Not from a direction — from everywhere, equally.
- Color: Very dark cyan-blue (#0A1E28) as a base ambient fill
- Effect: Nothing in the Glitch Layer is ever in complete shadow. The darkest area of any platform is still a rich, saturated dark — not a flat black.

**2. Platform Surface Luminance**
- Each platform glows slightly from within — as if it contains data that leaks through its surface.
- The glow is brightest at the platform edges (like a neon outline effect, but achieved through a secondary slightly-lighter color strip at the edge, not a bloom/glow filter)
- Different platform types glow in different colors (see tile/module sheet)

**3. Code Waterfall Light (Acid Green, Environmental)**
- Code waterfalls are the primary environmental light sources in terms of visual impact.
- They cast Acid Green light on everything nearby — platforms in the splash zone of a waterfall have their surface colors shifted toward green.
- This green-tinted zone can be very useful for scenes where characters should feel immersed in the digital world.

**4. Aurora Data-Streams (Background Fill)**
- The auroras in the background provide a slow-shifting colored fill — cycling through Electric Cyan, UV Purple, and Hot Magenta on a long loop.
- This means the Glitch Layer's overall color temperature slowly shifts over the course of a scene. This is intentional — it makes the space feel alive and slightly unpredictable even when nothing is visually "happening."

**5. Character / Glitchkin Glow**
- In the Glitch Layer, Glitchkin glow significantly brighter than in the real world.
- Byte's glow (Electric Cyan, #00F0FF) serves as a character-sourced key light in close-up shots.
- This character-sourced light means close-up shots in the Glitch Layer can have dynamic lighting that changes with Byte's emotional state and energy level.

**6. Hot Magenta Accents (Danger)**
- Wherever there is danger (a Corruption Zone edge, an aggressive Glitchkin, a structural failure), Hot Magenta sparks and glow intrudes.
- This creates a clear visual danger signal that the audience learns to read quickly.

### Shadow Notes
- Shadows in the Glitch Layer are rendered as a flat UV Purple shape (#7B2FBE, dark), simulating the ambient-source environment.
- Shadows point DOWN regardless of where the nearest light source is (since there's no directional sun, shadows default to "below the object" — like an ambient occlusion shadow).
- On platform surfaces, the shadow under any object has slightly jagged edges (as if the shadow rendering has precision errors) — a subtle but important detail that reinforces the digital wrongness.

---

## Color Breakdown

| Element | Color | Hex | Notes |
|---|---|---|---|
| Void base | Void Black | #0A0A14 | Never pure black |
| Void grid lines | Near-void purple | #141428 | 10% opacity, very subtle |
| Void background depth | UV Purple (faint) | #7B2FBE | Very low opacity at extreme distance |
| Standard platforms (lit face) | Electric Cyan (dark) | #003A4A | Base surface color |
| Standard platforms (edge glow) | Electric Cyan | #00F0FF | Brighter at edges |
| Elevated platforms (lit face) | UV Purple (mid) | #3A1060 | Higher platforms are cooler |
| Elevated platforms (edge glow) | Hot Magenta | #FF2D6B | |
| Ground-level platforms (lit face) | Dark acid green | #0A2A00 | Lower, more organic feel |
| Ground-level platforms (edge glow) | Acid Green | #39FF14 | |
| Platform shadow face | Deep void | #06080F | Very dark, not black |
| Code waterfall (characters) | Acid Green | #39FF14 | Primary text color |
| Code waterfall (glow halo) | Dark acid green | #1A4400 | Soft halo around the text column |
| Code waterfall (shadow cast) | Dark acid green wash | #0D2200 | Floor color in splash zone |
| Aurora bands: band 1 | Electric Cyan | #00F0FF | Soft, large-scale |
| Aurora bands: band 2 | UV Purple | #7B2FBE | |
| Aurora bands: band 3 | Hot Magenta | #FF2D6B | |
| Aurora edges | Void Black (fade) | #0A0A14 | Soft edges, feather into void |
| Pixel flora (primary) | Acid Green | #39FF14 | Bright, living |
| Pixel flora (shadow side) | Dark acid green | #1A5A08 | Shaded pixel faces |
| Pixel flora (gold accent) | Soft Gold | #E8C95A | Intrusion of real-world warmth |
| Impossible structures | UV Purple | #7B2FBE | |
| Impossible structures (lit) | Electric Cyan | #00F0FF | Lit face |
| Corruption Zone | Static White | #F0F0F0 | Noise patch |
| Corruption Zone sparks | Hot Magenta | #FF2D6B | |
| Pixel confetti particles | Mixed glitch | #00F0FF / #FF2D6B / #39FF14 | Floating squares |
| Character shadow (on platforms) | UV Purple dark | #1A0A30 | Cast shadow |

---

## Prop List / Tile Module Sheet — Reusable Elements

This section defines the modular visual vocabulary for building Glitch Layer compositions. Each element can be reused in new configurations to build any Glitch Layer scene efficiently.

---

### PLATFORM TYPES (4 core types + variants)

**Type A: Standard Cyan Block**
- Shape: Rectangle (various aspect ratios: 1:1, 2:1, 3:1, 4:1)
- Surface: Dark electric cyan (#003A4A) with faint pixel-grid seam lines at 8% opacity
- Edge: Bright electric cyan (#00F0FF) edge strip 2-3px wide (working resolution)
- Underside: Void black — invisible in most shots (platforms are lit from above)
- Variant A-tall: Same as above but with 2x height (creates sense of floating pillar)
- Usage: Most common platform type. The default "safe standing zone" for characters.

**Type B: Elevated Purple Block**
- Shape: Usually wider than tall. Square or 2:1 rectangle.
- Surface: Dark UV purple (#3A1060) with slightly larger pixel-grid seams than Type A
- Edge: Hot Magenta (#FF2D6B) edge glow — this type feels more dangerous, more elevated
- Usage: Platforms that characters must work to reach. Boss zones. High-stakes conversations.
- Variant B-stepped: A Type B block with two or three stepped levels (like a ziggurat), each step slightly smaller than the one below.

**Type C: Ground-Level Green Block**
- Shape: Wider and flatter than other types. Often appears in clusters to create a "ground zone."
- Surface: Dark acid green (#0A2A00) with dense pixel-grid seams
- Edge: Acid Green (#39FF14) edge glow — vivid, bio-luminescent feeling
- Usage: The "floor" zone of character-accessible areas. Where pixel flora grows. Feels slightly more organic despite being geometric.
- Variant C-terrain: Groups of Type C blocks at slightly varying heights to simulate rough terrain.

**Type D: Fragment Block**
- Shape: Irregular polygon — a broken piece. As if a larger platform shattered and only this shard remains floating.
- Surface: Can be any of the above surface treatments — it's defined by its broken shape, not its color.
- Edge: Slightly irregular edge glow (the light is "leaking" through the breaks)
- Usage: The most precarious-feeling platforms. For chase scenes, for moments of peril.
- Variant D-crumbling: A Fragment Block with additional smaller fragments visibly breaking off and floating nearby (background animation element — looping slowly)

---

### PIXEL FLORA (5 types)

**Flora 1: Pixel Grass**
- Appearance: A cluster of upward-pointing rectangular "blades" in varying heights. Each blade is 1-2 pixels wide, varying pixel heights (3, 4, 5, 6 pixel heights, randomly mixed).
- Color: Primary blades in Acid Green (#39FF14). Every 5th or 6th blade is a slightly desaturated green (#50B030). Occasional single blade in Soft Gold (#E8C95A) — the real-world color intrusion.
- Behavior: Static in background. In foreground, cycles through 3 frames (upright → slightly left lean → slightly right lean → upright) on a very slow 90-frame loop. No easing. Just key poses.
- Resolution scaling: Near camera = bigger pixel blocks (each "blade" is 4-6px at screen resolution). Far = smaller blocks.

**Flora 2: Pixel Flower**
- Appearance: A square-pixel blocky flower. Stem is a 2-pixel-wide vertical rectangle. At the top, a 3x3 pixel grid creates the flower head: center pixel in Soft Gold, surrounding 8 pixels in Acid Green. Or a variant: center in Hot Magenta (rare — marks an unusual/special flower).
- Behavior: 4-frame animation loop: closed bud (3x1 rectangle) → half-open (2x2 square) → open (3x3 grid) → half-close → back to bud. Loops very slowly.
- Color: As above. The Soft Gold center is important — it feels faintly wrong and warm in this cold digital space.

**Flora 3: Pixel Tree (Small)**
- Appearance: Trunk is a 4-pixel wide rectangle in dark muted green (#2A5010). The canopy is a stepped pyramid of squares: bottom layer is a wide rectangle of Acid Green, middle layer is slightly narrower, top is a 4x4 square. Pixel-art Christmas tree silhouette, basically.
- Height: Roughly 20-30 pixels tall at standard background resolution (adapts to scale).
- Behavior: Static. Absolutely still. This is uncanny — real trees move.

**Flora 4: Pixel Tree (Large)**
- Appearance: Same vocabulary as small tree but scaled up 4-6x. At this size the individual pixel blocks of the canopy become more visible and distinct — you can see them as separate square leaves.
- Special feature: One or two of the canopy pixel-blocks are the wrong color: a single Electric Cyan block among the Acid Green, or a single Hot Magenta block. As if a rendering error got into the tree.
- Behavior: Static.

**Flora 5: Pixel Mushroom**
- Appearance: A wide, low dome cap (semicircle approximated in pixel blocks) in UV Purple (#7B2FBE) with spots in Electric Cyan. Stem in darker purple.
- Height: Short and wide. Usually found in clusters of 3-5.
- Behavior: Pulses slowly between normal brightness and +20% brightness on a 60-frame loop. Like breathing. Like bioluminescence.
- Special use: These appear in zones near Corruption influence — they are the Glitch Layer's "warning flora," pretty but concerning.

---

### CODE WATERFALLS (3 types)

**Waterfall W1: Wide Flow**
- Width: 40-80 pixels wide at standard resolution
- Density: Dense — lines of code nearly touching each other
- Color: Acid Green (#39FF14) characters, background within the waterfall column is #0A1A00 (very dark green, slightly differentiated from the void)
- Use: Major background element, landmark-level. One or two per wide composition.

**Waterfall W2: Narrow Stream**
- Width: 8-15 pixels wide
- Density: Medium — space between lines
- Color: Slightly lower saturation acid green (#28CC10) — these are older, calmer streams
- Use: Fills middle-distance gaps. Multiple narrow streams together suggest complexity.

**Waterfall W3: Trickle**
- Width: 2-4 pixels
- Density: Sparse — individual characters with gaps
- Color: Very low saturation (#1A7A08) — almost just implied
- Use: Texture fill in close-up shots. The "drips" of this dimension.

---

### IMPOSSIBLE GEOMETRY ELEMENTS (5 types)

**IG1: The Penrose Staircase Fragment**
- A section of staircase that, if followed, loops back on itself at the same elevation
- Rendered in UV Purple (#7B2FBE) for the stone, Electric Cyan (#00F0FF) for the edge trim
- Size: Background use — too large to climb in normal staging, creates architectural impression

**IG2: The Nested Archway**
- An arch that contains a smaller arch that contains a smaller arch, repeating until the innermost arch is 1 pixel wide
- Each arch is a different shade from Electric Cyan → UV Purple → Hot Magenta as they recede
- The vanishing-point center is always placed off-center in the arch (for unease)

**IG3: The Klein Bottle Platform**
- A platform whose surface connects to its underside without a clear edge — you could walk off the edge and, by some impossible geometry, find yourself walking on the underside
- Surface treatment: The surface-meets-underside transition is shown as a fold in the texture, like a Möbius strip corner
- Used sparingly — this is a "wow" element for hero wide shots

**IG4: The Fractured Column**
- A column (cylinder approximated in pixel blocks) that appears to be falling but has been frozen mid-fall
- The top section is at a 45-degree angle; the bottom section is vertical. They don't connect but they're clearly the same column
- The gap between them emits hot magenta sparks

**IG5: The Infinity Mirror Floor**
- A flat platform surface that reflects the platforms above it — but the reflection shows platforms that DON'T EXIST in the actual scene
- This is suggested by the floor surface color including a faint "reflection" shape in a color not present elsewhere in the frame
- Subtle. Eerie. For hero shots only.

---

## Foreground / Midground / Background Layer Breakdown

### Wide Establishing Shot ("The Arrival")

This is the "wow" shot. Characters have just crossed from the real world. We are seeing the Glitch Layer for the first time.

**Foreground Layer:**
- Fragment platforms (Type D) partially in frame at the extreme bottom edges, out of focus — these are the "floor" that characters crossed the portal onto
- Pixel grass (Flora 1) growing on these platforms, in extreme close-up — individual pixel blocks clearly visible
- A piece of pixel confetti particle near the camera
- Rendering: Sharp focus on the pixel-block detail of the flora. This close-up texture contrast makes the wide shot feel more vast by establishing the unit of measure (one pixel block = X inches)

**Midground Layer (action zone):**
- A generous Type A platform cluster where characters stand — this is their "ground"
- A Type C cluster with Flora 1, 2, 3 growing on it, to the left
- One major code waterfall (W1) in the right portion of the frame, descending from above-frame
- One Type B elevated platform visible above and behind the character platform
- IG1 (Penrose staircase) visible behind and left, partially obscured by a W2 waterfall

**Deep Midground:**
- More platforms at various heights and angles, some at impossible orientations (a platform at 90 degrees, clearly "vertical" rather than horizontal)
- A large pixel tree (Flora 4) growing from a platform
- More code waterfalls (W2 and W3) filling distance
- An Impossible Geometry structure (IG2 archways) in the center-back

**Background Layer:**
- The aurora data-streams filling the upper portion of the void
- The UV Purple void depth at the very back
- Faint distant platforms visible as silhouettes against the aurora
- Corruption Zone (very small) visible in the far upper-left corner — a tiny warning

**Wrong-Direction Parallax Note:**
The background layer SHOULD move in the opposite direction to the standard parallax when the camera moves. If the camera pans right, the aurora bands should shift right (instead of left as expected). This is disorienting and correct. It should be a subtle effect — 30% of the normal parallax magnitude, in the wrong direction. Audiences will not consciously register this but will feel that something is slightly off, which is exactly right.

### Medium Shot (Platform Conversation)

Characters are standing on a Type A platform, having a scene. The Glitch Layer must stay interesting in the background without competing.

**Foreground Layer:**
- The platform edge in the extreme lower foreground — the clean cyan edge glow provides a horizon line
- Pixel flora at the platform edge

**Midground Layer:**
- The platform surface (where characters stand) — kept simple, clean
- Characters own this zone

**Background Layer:**
- A W1 code waterfall at mid-distance, slightly left or right (not centered, not to compete with characters)
- Platform layers receding at various heights
- Aurora bands providing color variation in the void
- One Impossible Geometry element (IG1 or IG3) partially visible

---

## The Rules of Glitch Layer Space — Visual Reference Card

These rules must be applied consistently. They are what make the Glitch Layer feel like a coherent WRONG place rather than generic sci-fi chaos.

| Rule | Description | Visual Result |
|---|---|---|
| **Gravity: Optional** | Some platforms float at impossible angles. Debris drifts upward. Characters must actively seek stable footing. | Rotated platform orientations. Upward-drifting particle confetti. |
| **Scale: Unreliable** | Distant objects may appear larger than near objects. The size of pixel flora is inconsistent with scene scale. | Near flora has bigger pixel blocks than far flora — OPPOSITE of normal perspective. |
| **Parallax: Inverted** | Background moves with the camera, not against it. Foreground behaves normally. | See above. Apply in animation direction notes. |
| **Resolution: Backwards** | Objects near the camera render at lower resolution (more visible pixel blocks). Distant objects render sharper. | Close flora: large pixel blocks. Distant flora: fine pixel grid. |
| **Color: Bleeding** | Colors in the Glitch Layer bleed into adjacent areas slightly — like wet ink. A cyan platform near a green flora zone will have a slight cyan bleed into the flora edge. | 1-2 pixel color bleed at color boundaries. Subtle — not a full bleed, just a "halo" of adjacent color. |
| **Shadow direction: Down** | Shadows always fall downward, regardless of light source direction (because there's no consistent light source). | All shadows point "below" the object. |
| **Edges: Intermittent** | Some platform edges "flicker" or have missing sections (like rendering errors). | 1-2 short gaps in the otherwise-continuous edge glow line per platform. |
| **Code: Readable** | If the audience pauses on a code waterfall, there are hidden words. | Words embedded in the code columns. Changes per episode. Always relevant to the plot. |
| **Time: Non-linear** | Some pixel flora can be seen in both its open and closed state simultaneously in a single frame. | 2 overlapping flora animation states (50% opacity each) visible in wide shots. |

---

## Rules Hierarchy

The nine rules in the table above are not created equal. Applying all nine simultaneously in every shot produces visual noise — the eye has nowhere to anchor. This section defines which rules are always in effect, which are selectable for emphasis, and the hard ceiling on simultaneous active rules.

### Always-On Rules (Active in EVERY Glitch Layer shot — no exceptions)

These three rules define the Glitch Layer at its quietest. Even in a calm, low-energy scene, these must be present or the environment will not read as the Glitch Layer:

| # | Rule | Why Always-On |
|---|---|---|
| **AO-1** | **Resolution: Backwards** — near objects render at lower pixel resolution than far objects | This is the single most immediate and readable "wrongness" signal. It costs almost nothing compositionally and constantly reminds the eye that physics are reversed here. |
| **AO-2** | **Shadow direction: Down** — all shadows fall directly below objects regardless of light source | Removes all directional lighting logic. Establishes the ambient-source environment. Any shot missing this will immediately suggest a real-world light is present. |
| **AO-3** | **Edges: Intermittent** — 1-2 short gaps in the edge glow line of each visible platform | A platform with a perfectly continuous edge glow looks like a video game, not a broken dimension. The gaps signal system error. Quick to implement; never skippable. |

### Optional Rules (Selected for emphasis based on scene energy)

These six rules are available to the background artist and layout team to dial up the intensity or mood of a given shot. They are NOT active by default — they must be deliberately chosen:

| Code | Rule | Best Use |
|---|---|---|
| **OP-A** | **Gravity: Optional** — platforms at impossible angles, debris drifting upward | Chase sequences; moments of immediate peril; arrival shots where disorientation is the goal |
| **OP-B** | **Scale: Unreliable** — foreground objects visually larger or smaller than expected relative to background | Wide establishing shots where a sense of epic scale or vertiginous wrongness is needed |
| **OP-C** | **Parallax: Inverted** — background moves WITH camera rather than against | Any moving camera shot (pan, truck). Applied in animation direction notes, not the static BG itself. |
| **OP-D** | **Color: Bleeding** — 1-2 pixel color halo bleeds at color boundaries between adjacent areas | Scenes where the Glitch Layer feels especially active or unstable; scenes near Corruption Zones |
| **OP-E** | **Code: Readable** — visible words embedded in code waterfall columns | Plot-relevant scenes where the environment is "speaking." Requires art direction approval for word content. |
| **OP-F** | **Time: Non-linear** — pixel flora visible simultaneously in two animation states (50% opacity each) | Dreamlike or disorienting scenes; scenes about memory or information loops |

### Maximum Simultaneous Active Rules

**Hard ceiling: 5 rules active in any single shot** (3 Always-On + a maximum of 2 Optional).

Rationale: The Always-On rules establish baseline wrongness at zero compositional cost. Each Optional rule adds a specific kind of visual complexity. Two Optional rules is the maximum before the viewer's eye begins to lose the ability to locate characters and follow action.

Exception: The production designer may authorize up to 3 Optional rules (total 6) for a designated "maximum chaos" shot — a single hero wide shot per episode, subject to review. These shots must be flagged `GL_MAX_CHAOS` in the file name.

---

### Scene Energy Examples

**Example A — Quiet conversation in the Glitch Layer**
_Luma and Byte on a Type A platform, mid-season. Relatively calm. Low stakes in this moment._

Active rules: **AO-1, AO-2, AO-3** (all Always-On) + **OP-B** (Scale unreliable — the wide shot includes a tiny platform next to an enormous one, emphasizing the alien scale of the environment without disrupting the conversation).

Rules NOT active: No inverted parallax (static shot). No color bleed (nothing is destabilizing). No readable code (no plot-relevant word content needed). Flora is static, not double-exposed.

**Example B — Chase sequence through the Glitch Layer**
_Luma running from an aggressive Glitchkin pack. High energy, fast cuts, camera moving._

Active rules: **AO-1, AO-2, AO-3** (all Always-On) + **OP-A** (Gravity optional — tilted platforms increase the panic of the space) + **OP-C** (Inverted parallax — camera is moving; apply to animation direction notes).

Rules NOT active: Color bleed is held back (will be added in the subsequent scene when Luma gets cornered and the Corruption Zone appears nearby). Readable code is not active (too many fast cuts; words would be unreadable).

**Example C — Discovery scene near a Corruption Zone (mid-season)**
_Luma finds a new Corruption Zone that has grown significantly. She stops. Studies it. A slow, unnerving wide shot._

Active rules: **AO-1, AO-2, AO-3** (all Always-On) + **OP-D** (Color bleed — cyan from platforms bleeding into adjacent flora, the proximity to Corruption raises the instability) + **OP-F** (Time non-linear — the pixel flora in the foreground shows double-exposure, suggesting the zone is distorting time as well as space).

Rules NOT active: No gravity optional (the stillness is important — chaos would reduce tension, not increase it). No scale unreliable (the Corruption Zone's actual size should read correctly; scale wrongness would dilute its threat).

---

## Painterly-Flat Rendering Notes

### The Core Tension
In the real world, the painterly-flat style means soft textures and gentle shapes. In the Glitch Layer, the flat style is taken to its EXTREME — shapes here are maximally flat, maximally graphic. There is LESS texture overlay than in any real-world environment (the glitch palette purity should not be muddied by grain). What texture exists is digital: pixel patterns, grid seams, dither patterns.

### Dithering
- Where the Glitch Layer style calls for a "gradient" effect (aurora bands, glow fades), achieve it through DITHERING rather than actual gradients: alternating pixels of two colors in a checkerboard pattern that creates the illusion of an intermediate tone.
- Dither pattern should be large enough to be visible (this is not anti-aliasing — it's a deliberate aesthetic choice). Each dither "pixel" should be 2-3px at working resolution.
- This technique references classic low-bit computer graphics and is a key part of the Glitch Layer's visual identity.

### Edge Glow Technique
- Platform edge glows are NOT achieved with blur or bloom. They are achieved with a secondary, slightly lighter, narrower shape inside the edge. Two clean flat shapes, not a soft glow.
- This keeps the Glitch Layer consistent with the show's flat-graphic style while still creating a sense of luminosity.

### Pixel Confetti
- Floating square particles (2x2 pixels each at standard resolution) in #00F0FF, #FF2D6B, and #39FF14
- These appear near any active glitch activity — denser near code waterfalls, near Corruption Zones, near the portal arrival point
- Their movement should be: gentle, slow drift (some drifting up, some sideways, some rotating) — NOT frantic. Frantic confetti loses visual hierarchy to the important action.
- In background layers, they are rendered at 50% opacity.

---

## Key Storytelling Details & Discoverable Background Gags

### Persistent Narrative Details
- **The Hidden Words:** In every code waterfall, readable fragments change each episode. In Episodes 1-4, the words are location-based ("HERE" "MILLBROOK" "BELOW"). In Episodes 5-8, they become emotional ("SCARED" "ALONE" "HOME"). In Episodes 9-12, they shift to urgent ("COMING" "WAKE" "TOO LATE").
- **The Corruption Zones grow:** In Episode 1's Glitch Layer shots, there are 2 tiny Corruption Zones visible in background areas. By Episode 6, 7. By Episode 10, 12. And they're bigger. Nobody on the team explicitly points this out in the first viewing; it's background storytelling.
- **Byte's Glow:** In the Glitch Layer, Byte glows significantly brighter than in the real world. In Episode 7, Byte is noticeably dimmer in the Glitch Layer than in previous episodes. This is a plot hint (something is wrong) embedded entirely in background lighting.
- **The phantom platforms:** In some shots, very faint (20% opacity) platform shapes can be seen passing through the space — not stopping, not landing, just drifting. These are ghosts of old data. The audience may or may not notice them. They have no dialogue or plot function but their accumulation across the season implies the Glitch Layer is remembering things.

### Background Gags
- **The Pixel Duck:** From Episode 3 onward, a small (4x4 pixel) duck shape can be found somewhere in each Glitch Layer shot. It serves no function. It glows slightly. The showrunner's commentary will eventually explain what it means. (It means nothing. Except that it means everything to someone.)
- **Wrong-size objects:** In every Glitch Layer shot, at least one object is visibly the wrong scale — a platform the size of a coin floating near a platform the size of a building, as if scale units were mixed up in the rendering.
- **The Mirror Platform:** From Episode 5 forward, one platform in each Glitch Layer shot has a reflection in its surface showing a scene from Millbrook (a specific location, not a mirror of the current scene). The reflected location changes each episode.

---

## Design Rationale

The Glitch Layer needed to feel like it had RULES, even though the rules are wrong. Without rules, chaos is visually illegible. With rules that are consistently broken in specific, defined ways, the space becomes alien but comprehensible. The audience learns the language of wrongness.

The decision to make the Glitch Layer beautiful rather than frightening comes from the show's core thesis: Glitchkin are not evil, just misunderstood. The digital dimension they come from should reflect that — it's genuinely wonderful, even though it's also genuinely dangerous. Beauty and danger are not mutually exclusive. Ask any ocean.

The palette here is the one space where the glitch colors completely dominate. This is important. The real world stays warm and analog. The Glitch Layer is purely digital. The visual contrast makes the emotional contrast land: home is warm amber. This unknown world is electric cyan. Both are beautiful. Luma gets to love both of them. That's the show.

The modular tile/platform approach ensures that the background artists can build new Glitch Layer compositions efficiently without reinventing the visual language each time. The platform types, flora types, waterfall types, and geometry elements defined here should be the vocabulary — new compositions are new sentences using familiar words.
