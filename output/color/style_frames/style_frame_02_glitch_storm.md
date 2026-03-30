<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Style Frame 02 — "Glitch Storm"

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**Version:** 2.0 (Cycle 2 — Byte visibility fix, Acid Green semantic fix, confetti physics governing rule applied)
**Status:** Approved for illustration
**References:** master_palette.md v2.0, scene_color_keys.md v2.0 (Color Key 02), style_guide.md

---

## Frame Identity

**Frame title:** Glitch Storm
**Episode position:** Mid-season — a major escalation sequence, possibly the Act 2 break of the first multi-part episode. The stakes are at maximum for this part of the story.
**Narrative function:** The action promise frame. If "The Discovery" sold the premise, this frame sells the scale. The audience must feel the physical vastness of the threat — the sky itself is cracking. And in the middle of that vast impossible disaster, two small kids are running as fast as they can. The contrast of scale (enormous glitch storm vs. small children) is the image's core tension, and color must serve that contrast.
**Mood:** Kinetic terror with a wild heart. This is terrifying and also, under the surface, exhilarating. It is the most *alive* these characters have ever been.

---

## Composition

### Framing
- **Aspect:** 16:9 widescreen
- **Shot type:** Wide shot — full environment visible. Characters are small relative to the frame (occupying approximately the lower third), which is intentional and critical: the glitch storm is the subject; the characters are in it.
- **Rule of thirds:** Luma at the left third-line, angled toward the right, in full sprint. Cosmo one stride behind her, also right-facing. The main lightning crack in the sky descends from the upper-right corner down through the right vertical third — it mirrors the direction of their run, as if the storm is chasing them specifically (it is).
- **Dutch angle:** 4-degree tilt, clockwise — subtle but unmistakable. The world is tilted. Things are not right. Per the style guide (5-15 degree range for tension); this is at the mild end, keeping readability high.

### Depth Layers
- **Far background:** The sky. This is the most important layer in the frame — it is enormous and it is the storm itself. Two-thirds of the frame's total area is sky. The sky is the antagonist of this shot.
- **Mid-background:** The town of Millbrook at night. Rooftops, chimneys, power lines, streetlamps. The skyline of a small, normal town caught in something it has no language for.
- **Midground:** The empty Main Street — road surface, sidewalk, parked cars partially visible, a knocked-over bicycle, trash cans — the wreckage of a street that people evacuated in a hurry.
- **Foreground:** Luma and Cosmo, running. On the right side of the foreground, a shattered storefront window (a "Millbrook Hardware" type shop) with glitch cracks spreading from it — the Glitch is already on the ground level.

### Character Positioning
**Luma:**
- Full sprint — left foot forward, right foot behind, arms pumping. Classic cartoon run: maximum squash-and-stretch. Her hair and hoodie are streaming behind her — motion.
- Her face is turned slightly back over her shoulder, one eye visible to the viewer. Expression: determined, not quite scared. She has seen the scale of this and it does not stop her — it just makes her run faster. Mouth set hard, eyes wide with focus.
- Position: Low in the frame, slightly below center-height, at the left third-line, moving right.

**Cosmo:**
- One stride behind Luma, slightly to her right/behind (staggered so both figures read clearly). His run is less graceful — his glasses have slid down his nose, his jacket flaps open, his arms are pumping too high (over-efficient bad technique that communicates "academic who doesn't run much").
- Expression: pure panic, face fully toward the viewer — all we can see of him is his wide mouth, his foggy glasses reflecting cyan lightning, and the absolute conviction that they are about to die. This is the comedy of the frame: Luma's focused determination vs. Cosmo's honest terror.
- Byte is visible as a tiny shape on Luma's shoulder — clinging on, ears (if he has ears) flat back, eyes squeezed mostly shut.

### Background Townspeople
- Three to five townspeople visible in the background — in doorways, at windows, pressed against a wall. They are small, secondary, simplified.
- Their silhouettes matter more than their individual design at this scale.
- They should read as: "ordinary people in the wrong story." Their color values are deliberately desaturated — they are part of the background, not the action.

---

## Sky Design — The Glitch Storm

The sky is the most complex element of this frame. It must read as:
1. An actual stormy sky (recognizable as threatening sky, not just abstract pattern)
2. A digitally corrupted sky (wrong colors, digital geometry, pixel-breaking)
3. A sky that is *failing* — reality itself coming apart at the seams

### Sky Color Architecture (top to bottom)

**Upper zone (top ~40% of frame):**
- Base: `#1A1428` (deep blue-purple night sky)
- Glitch infection: `#7B2FBE` (UV Purple) in large, cloud-like masses replacing normal cloud forms. These are not organic cumulus shapes — they are fractal, angular, geometrically impossible. They have the silhouettes of corrupted data structures: rectangular, blocky, with sharp 90-degree angles eating into their edges.
- Within the UV Purple masses: `#0A0A14` (Void Black) core areas — the deepest parts of the storm, where there is nothing, not even digital color
- Storm edge luminance: `#FF2D6B` (Hot Magenta) outlining the aggressive edges of the glitch storm masses — the "active front" of the storm glows magenta, as if the corruption is burning the sky away

**Middle zone (from about 30% to 60% of frame height):**
- The CRACK: the primary visual element of the frame. A massive jagged fracture runs from upper-right to lower-middle — as if someone took a hammer to the sky. The crack has:
  - Core (inside the crack): `#00F0FF` (Electric Cyan) at maximum luminance — this is the Glitch Layer showing through, the sky peeled back to reveal digital space underneath
  - Inner core: `#F0F0F0` (Static White) at the very center of the crack — overexposed, too bright, almost painful to look at
  - Crack edges: `#FF2D6B` (Hot Magenta) burning around the perimeter of the crack
  - Secondary sub-cracks branching from the main crack: smaller versions of the same structure, in `#00F0FF` thinning to `#2B7FFF` at their tips (like digital lightning branching)
- The geometry of the crack: NOT like regular lightning (organic, jagged but naturalistic). Instead: the crack is partly orthogonal — some of its angles are perfect 90 degrees, some 45 degrees, as if the fracture is following invisible grid lines. This is what makes it read as *digital* damage and not weather.

**Lower sky zone (near the horizon, above the rooftops):**
- `#1A1428` (deep night) receding toward the town
- Faint ambient wash of `#7B2FBE` (UV Purple) tinting the air above the buildings
- Warm remnant: where the buildings block the sky near ground level, there is a faint `#C75B39` (terracotta) and `#E8C95A` (warm gold) glow from interior lights of the buildings below — the town is still lit from within, still alive

### Pixel Confetti in the Sky — CORRECTED SPECIFICATION

**Cycle 1 issue:** The original specification listed `#39FF14` (Acid Green) as one of the pixel confetti colors in the storm zone. This was an error. Acid Green is semantically defined as "healthy glitch energy" (master palette GL-03). Its appearance as a storm-effect particle directly contradicts its meaning — the audience has been trained to read Acid Green as positive/alive. In a danger-storm context, it sends the wrong signal and undermines the color language.

**Corrected confetti specification:**
- Storm-generated pixel confetti colors: `#00F0FF` (Electric Cyan), `#F0F0F0` (Static White), `#FF2D6B` (Hot Magenta), `#7B2FBE` (UV Purple)
- Acid Green (`#39FF14`) confetti is **permitted only** if Glitchkin characters are visible in or near the storm, shedding their own markings. In that case, a small cluster of Acid Green particles may appear in the immediate vicinity of those characters — attributed to them, not to the storm. Their particles must be spatially distinct from the storm particle clusters (i.e., close to the Glitchkin, not streaming from the crack).
- **Governing physics rule (cross-reference from Frame 01):** Confetti originates from its source and diminishes with distance. Storm confetti streams outward from the crack. Glitchkin confetti clusters close to the Glitchkin. The two types of confetti must not be intermingled.

- Large clusters of `#00F0FF`, `#F0F0F0`, `#FF2D6B`, and `#7B2FBE` square particles fill the storm zone.
- Size variation: near the crack, they are large (10-15px at production res); further away they diminish per the governing physics rule.
- Motion direction: emanating outward from the crack — the storm is *projecting* them.
- A few pixel confetti particles are falling near Luma and Cosmo's level — the storm is reaching down to street level. These are smaller (2-4px) having traveled farther from the source.

---

## Lighting Breakdown

### Primary Light Source — The Crack
- **Color:** `#00F0FF` (Electric Cyan) — the crack is the sun of this scene. It is the source.
- **Direction:** From the upper right (where the crack is). Light floods down and left across the scene.
- **On Luma (right-facing side):** Her right side (facing the crack) is washed in intense Cyan. Her orange hoodie `#E8703A` under the cyan key reads as `#C8695A` (DRW-07 — Storm-Modified Hoodie Orange). The warm color fights the cool light, and NEITHER WINS — the result is a complex, deeply cinematic color that looks neither purely warm nor purely cold.
- **On Cosmo:** Since he is behind Luma and slightly angled differently, the Cyan hits him at a slightly different angle. His Dusty Lavender jacket `#A89BBF` under Cyan light reads as `#80C0CC` (DRW-09 — Storm-Modified Jacket). The lavender's purple component partially cancels against the cyan and what remains reads as a coherent teal-lavender.
- **On the road surface:** A strong cyan pool of light on the tarmac directly below the crack — the most intense zone of Cyan in the ground plane, fading as it goes left (toward safety).
- **On building facades:** Cyan light strikes the right-facing walls of buildings on the left side of the frame. The terracotta walls under cyan light read as `#96ACA2` (ENV-06 — Terracotta under Cyan) — the familiar warm world visually neutralized by the glitch light.

### Secondary Light Source — Hot Magenta Edge
- **Color:** `#FF2D6B` (Hot Magenta) — from the burning edges of the storm
- **Direction:** Ambient, from the right and above, coming from the storm mass perimeter rather than from a point source
- **Effect:** Adds a magenta fill light on the upper surfaces of elements facing the storm — tops of heads, top of car roofs, chimney caps. The result is a cyan key from one direction, magenta from another: characters standing in between receive both.
- **On Luma's hair:** The top of Luma's hair catches the magenta fill. Her deep cocoa hair (`#3B2820`) under magenta light reads as `#6A2A3A` (DRW-17 — Magenta-Influenced Hair). In motion streaks, this becomes visible as a magenta rim along the windswept arc of her hair.

### Tertiary Light Source — Building Interior Glow
- **Color:** `#E8C95A` (Soft Gold) and `#FAF0DC` (Warm Cream) — the warm windows of Millbrook
- **Direction:** Emanating forward from building faces at street level
- **Effect:** A warm spill of golden light across the sidewalk in front of the buildings — the only warm light in the scene. It is weak relative to the Cyan storm light, but it is an emotional beacon. Where the warm light falls, the world still feels like itself.

---

## BYTE VISIBILITY — CYCLE 2 FIX

**Problem:** Byte's base fill is `#0A0A14` (Void Black) and his surface highlight is `#00F0FF` (Electric Cyan). In a Cyan-dominant environment (this entire scene is flooded with Cyan light), Byte's cyan highlights become indistinguishable from the ambient cyan. His void-black body, meanwhile, has near-zero contrast against the dark areas of the storm. In a wide shot where he is already very small (clinging to Luma's shoulder), this combination makes him effectively invisible. The Cycle 1 spec acknowledged this: "his normal luminance is reduced here — he paradoxically disappears." This was accepted as a weakness but it is a production problem and a character-read problem.

**Solution — Warm Outline Exception for Byte in Cyan-Dominant Scenes:**

In scenes where Electric Cyan is the dominant ambient color (including all storm scenes and Glitch Layer scenes), Byte receives a **Corrupted Amber (`#FF8C00`) outline exception**. This is a production rule, not a narrative one — Byte does not have a visible amber outline in the story world. It is a visual clarity tool.

**Implementation:**
- A 2px outline of `#FF8C00` (Corrupted Amber) is applied around Byte's entire silhouette.
- The outline exists on a separate layer above the background and below Byte's body layers, visible only where it peeks beyond his edge.
- At production scale in a wide shot, 2px reads as a warm rim — the eye sees Byte's silhouette as "warm-edged against cool" and immediately separates him from the background.
- The warm amber outline has narrative plausibility: Byte is a reformed Glitchkin who came from the Real World side; the corrupted amber is the bridge color between Real World warmth and Glitch energy. His amber outline in glitch environments can be read as "the Real World homing signal he carries, visible under extreme digital stress."
- **This outline rule applies whenever Byte is in a cyan-dominant environment AND is smaller than 15% of frame height.** In close-ups or medium shots, his regular spec applies without the outline. **Definition — Cyan-dominant:** scenes where Electric Cyan (`#00F0FF`) and/or Data Stream Blue (`#2B7FFF`) together account for more than 35% of total background color area (excluding sky void black `#0A0A14`). When Byte is smaller than 15% of frame height AND the environment is cyan-dominant by this measure, apply the Corrupted Amber outline exception. When either condition is not met — Byte is large enough to read clearly, or cyan/blue together are 35% or less of background area — revert to standard spec.

**Additionally — Position adjustment:**
- In this wide shot composition, Byte is placed on Luma's LEFT shoulder (not right), not her right. This positions him on the side facing AWAY from the crack — the shadow/non-cyan side. His void-black body against the deep warm shadow of Luma's hoodie shadow side (`#3A1A14`) creates better inherent contrast than placing him against the cyan-lit right side. The amber outline still applies, but the base contrast is improved.
- His cracked eye (`#FF2D6B`) is now facing TOWARD the crack (right side), making it visible to the viewer and maintaining the narrative function: his cracked eye sees the danger. His cyan eye faces toward Luma's face.

---

## Full Color Specification — Zone by Zone

### Road and Sidewalk
- Road surface base: `#2A2A38` (ENV-01 — dark blue-grey asphalt, nighttime)
- Road under Cyan light pool: `#2A5A6A` (ENV-02 — cyan-influenced dark grey)
- Road under warm window spill: `#4A3A2A` (ENV-03 — warm asphalt under building light)
- Sidewalk: `#3A3848` (ENV-04 — slightly lighter than road, cool grey-blue)
- Road cracks and gutters: `#0A0A14` (Void Black) — the darkest zones
- Luma's cast shadow: `#0A2A3A` (ENV-05 — very dark cyan-tinted shadow, pointing left away from crack)
- Cosmo's cast shadow: overlapping Luma's, same `#0A2A3A`

### Main Street Buildings (background)
- Wall faces (terracotta, right-facing, Cyan-lit): `#96ACA2` (ENV-06 — desaturated warm, Terracotta neutralized by Cyan key)
- Wall faces (left-facing, away from storm): `#5A3820` (ENV-07 — deep warm shadow; only ambient UV Purple fills here, creating a deep nearly-void zone)
- Window glow: `#FAF0DC` and `#E8C95A` (warm light from inside — the visual memory of safety)
- Roof lines against sky: `#1A1820` (ENV-08 — nearly void, just catching the very edge of light on upper faces)
- Power lines: thin `#3B2820` (Deep Cocoa) lines
- Chimney stacks: `#3B2820` (Deep Cocoa), occasional `#00F0FF` reflection on rain-wet chimney face

### Shattered Storefront Window (right foreground)
- Window frame: `#5B8C8A` (Muted Teal) — aged metal
- Broken glass fragments: `#F0F0F0` (Static White) with `#00F0FF` reflections — brightest non-sky foreground elements
- Glitch cracks spreading from the window: `#00F0FF` core, `#FF2D6B` edge, pixel confetti erupting from spread points
- Interior of store seen through window: `#0A0A14` with faint `#7B2FBE` glow — inside being consumed

### Luma — Full Color (under storm lighting)
- Body right side (Cyan key): orange hoodie desaturated to `#C8695A` (DRW-07), skin to `#6AB4AE` (DRW-08 — Storm skin)
- Body left side (facing away from crack): shadow side reads as `#3A1A14` (DRW-03 deep shadow — the hoodie's orange fights all the way into the shadows)
- Hair windstream (motion): `#3B2820` base with `#6A2A3A` (DRW-17) magenta-influenced highlights at edges of motion arc
- Laces (Electric Cyan): at this lighting, the `#00F0FF` laces merge with the scene's ambient Cyan light — a small detail; they are present but do not read distinctly
- Hoodie pixel grid: the `#00F0FF` pixels are indistinguishable from the scene's ambient Cyan in the lit areas — an acceptable visual effect for this storm scene specifically. The pixels appear to be *on fire* with the storm's energy. (Contrast with Frame 01 where the grid separation protocol is critical for the close-up.)

### Cosmo — Full Color (under storm lighting)
- Jacket (Cyan-lit right side): `#A89BBF` base modified toward `#80C0CC` (DRW-09 — Storm-Modified Jacket)
- Jacket (shadow left side): `#2A1A32` (DRW-10 — Storm Jacket Shadow)
- Glasses: reflecting `#00F0FF` (electric cyan sky) on lens faces — Cosmo's expression is partially obscured by the reflection; we can only see his panic through his mouth
- Striped shirt (visible at collar): `#FAF0DC` and `#C75B39` — the stripes, briefly visible, are a last flash of normalcy

### Byte (on Luma's LEFT shoulder — see Byte Visibility note above)
- Position: LEFT shoulder (corrected from v1.0 right shoulder for contrast reasons)
- Outline: 2px `#FF8C00` (Corrupted Amber) silhouette outline, per Byte Visibility rule
- Body base: `#0A0A14` with `#00A8B4` inner glow traces
- Cyan highlights: `#00F0FF` — reduced distinction from ambient in this frame; amber outline compensates for lost edge definition
- Cracked eye: `#FF2D6B` — facing right (toward the crack/danger). In a cyan world, his magenta eye is still the alarm signal, now even more readable because he faces it toward the danger.
- Cyan eye: `#00F0FF` — facing left (toward Luma's face)
- His claws grip Luma's hoodie: `#00F0FF` claws against `#3A1A14` (deep hoodie shadow on the left/shadow side) — high contrast, clear read

### Townspeople (background)
- Silhouettes: `#1A1428` (dark night) with just enough lavender ambient to separate them from the buildings
- Window watchers: `#E8C95A` warm glow catching their faces from behind (from the window light they stand in front of)
- Running figures (if any): simplified `#2A2A38` silhouettes, no detail

---

## The Color Story of This Frame

This frame is about **invasion**. The color tells it structurally:

**The sky (upper two-thirds):** Completely lost to the Glitch palette. Void Black, UV Purple, Hot Magenta, Electric Cyan. Not a single Real World color survives up here. The invasion is total at altitude.

**The buildings (middle):** Fighting. Terracotta walls partially surviving. Warm windows still lit. But the Cyan key light neutralizes the terracotta — the walls are neither their true warm color nor a glitch color. They are in between, uncertain, losing their identity.

**The street (lower third):** Contested. The warm window spill vs. the Cyan storm pool, competing for the same ground. This is the battlefield.

**Luma and Cosmo (in the street):** The only fully three-dimensional color objects in the scene — they have warm sides and cold sides, lit by both worlds simultaneously. Their color complexity is what makes them feel *alive* in a flattening crisis. They are not losing their identity. They are the most themselves they can be.

The frame argues: the Glitch takes the sky first, then the buildings, then the street. But it cannot take the people. Not yet.

---

## Technical Spec Notes

- Maximum dominant colors: 7 — Night Sky Deep `#1A1428`, UV Purple `#7B2FBE`, Electric Cyan `#00F0FF`, Hot Magenta `#FF2D6B`, Void Black `#0A0A14`, Warm Gold `#E8C95A`, Warm Cream `#FAF0DC` (building windows). Supporting: Static White `#F0F0F0` for specular/crack core, Corrupted Amber `#FF8C00` for Byte's outline exception.
- **Storm confetti dominant cold:** GL-06c STORM_CONFETTI_BLUE `#0A4F8C` (registered in master_palette.md C28). This is a deliberate atmospheric depth derivative of GL-06 (#2B7FFF) — storm confetti reads darker and more desaturated at distance (aerial perspective). Do not substitute GL-06 for GL-06c in the storm generator.
- Acid Green NOT in storm confetti — per master palette Forbidden #8. Storm confetti is `#0A4F8C` (GL-06c), `#F0F0F0`, `#FF2D6B`, `#7B2FBE` only.
- Character check: Luma's orange and Cosmo's lavender remain more saturated than any background element, even under extreme relighting. Characters must pop.
- Byte: Corrupted Amber outline applied. Positioned on LEFT shoulder. Cracked eye faces right (toward crack). See Byte Visibility section above.
- Dutch angle: 4 degrees clockwise on the full composition. Apply at the very end — do not tilt individual elements, tilt the camera.
- Pixel confetti: Governing physics rule applied — source-origin, size/density diminishes with distance from source. No Acid Green storm confetti.
- Scan line distortion: in the crack zone, apply a 2-pixel horizontal offset to background elements (background layer only) as if they have been shifted by a screen glitch. Do not apply to characters.

---

*Frame 02 — "Glitch Storm" — Cycle 2 revision complete*
*Sam Kowalski — 2026-03-29*
