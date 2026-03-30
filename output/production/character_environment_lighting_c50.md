<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Character-Environment Lighting Spec — Cycle 50
**Author:** Hana Okonkwo, Environment & Background Artist
**Date:** 2026-03-30

---

## Purpose

This document defines how each environment lights the characters placed in it. Currently, characters carry their own baked-in lighting regardless of scene — warm highlight on one side, generic shadow on the other. The result is paper-doll compositing. This spec describes the correct lighting per room so that character generators and style frame compositors can apply scene-responsive shading.

The principle from reference study (Hilda living room, Owl House interiors): **the character's lit side picks up the actual color of the dominant light source**. Shadow side picks up the ambient/fill color. No character carries its own lighting — the scene dictates it.

---

## Lighting Protocol (All Rooms)

### Step 1: Identify Light Sources
Every environment has 1-3 active light sources. Each has:
- **Position** (relative to canvas: left/right/above/below)
- **Color** (the actual RGB value of the light)
- **Intensity** (key, fill, or rim)

### Step 2: Character Shading Direction
The character's lit/shadow split follows the **dominant light source position**.
- Light source to character's RIGHT → character's right side is lit, left is shadowed
- Light source ABOVE → top of head/shoulders lit, under-chin/body shadowed
- Multiple sources → primary source sets the main shadow direction, secondary adds fill/rim

### Step 3: Color Influence
- **Highlight color** = blend of character base color + scene light color at 20-30% influence
- **Shadow color** = blend of character base color + ambient/fill color at 10-20% influence
- **Bounce color** = ground surface color at 10-15% influence on character's lower quarter

### Step 4: Contact Shadow
- Color derived from ground surface (darken 65-70%, desaturate 15%)
- Alpha 40-60 (subtle, not heavy)
- Elliptical, width = character width * 1.1
- Use `LTG_TOOL_contact_shadow.py` functions

---

## Per-Environment Lighting

### Kitchen (Grandma's) — `LTG_ENV_grandma_kitchen.png`
**Scene type:** Real World, warm interior
**Time of day:** Variable (default: afternoon / pre-dawn for SF05)

| Light Source | Position | Color (RGB) | Role |
|---|---|---|---|
| Window (left wall) | Upper-left | SUNLIT_AMBER (245, 208, 140) | Key light |
| Overhead fluorescent | Above-center | (240, 235, 215) warm white | Fill |
| CRT doorway (right) | Right, mid-height | ELEC_CYAN (100, 220, 220) or CORRUPT_AMBER (230, 160, 60) depending on scene | Accent/rim |

**Character shading:**
- **Default (afternoon):** Warm amber fill from upper-left. Character's left side is lit (warm amber highlight). Right side receives softer shadow with slight cool fill from ambient. Top of head/shoulders catch warm from above.
- **SF05 (pre-dawn):** Dimmer. CRT from doorway becomes the dominant accent. Characters closest to doorway get warm amber/cyan rim on that side. Window side is cool pre-dawn blue.
- **Miri position note:** Miri typically stands at counter (left-center). She is closer to the window → stronger warm highlight on her left. If seated at table (center), more even fill from overhead.
- **Luma position note:** Luma typically enters from doorway (right). CRT-facing side gets the accent color.

**Contact shadow:** Surface = FLOOR_TILE_WARM (200, 184, 150). Shadow alpha 50.
**Bounce light:** Warm floor bounce on lower legs/feet. Ground color (200, 184, 150) at alpha 20.

---

### Luma's Study — `LTG_ENV_luma_study_interior.png`
**Scene type:** Real World, mixed lighting interior
**Time of day:** Night (CRT is on)

| Light Source | Position | Color (RGB) | Role |
|---|---|---|---|
| CRT monitor | Right of center, mid-height | CRT_GLOW (160, 195, 165) | Key light |
| Bedside lamp | Left, mid-height | SUNLIT_AMBER (245, 208, 140) | Warm fill |
| Night window | Far left | Cool blue (120, 140, 180) | Ambient/mood |

**Character shading:**
- **CRT is the dominant source.** Character's CRT-facing side gets blue-green tint on highlights. CRT glow is NOT pure cyan — it is muted green (PIL hue ~60-65). Highlight = skin base + CRT_GLOW at 25%.
- **Lamp fills the away side.** Character's left side (facing lamp) gets warm amber fill. Shadow = skin base + SUNLIT_AMBER at 15%.
- **The two-source split is what makes this room visually interesting.** Characters should show a clear warm-left / cool-right temperature divide.

**CRITICAL NOTE (from C42 memory):** CRT_GLOW (160,195,165) reads as muted green, NOT blue. The warm/cool divide is amber (~hue 18-25) vs. green (~hue 60-65). This is correct and intentional — do not replace with pure cyan.

**Contact shadow:** Luma is typically seated on couch. Use `draw_seated_shadow()` with surface = dark couch fabric (100, 85, 70). Shadow alpha 40.
**Bounce light:** If seated on couch, minimal (dark fabric). If standing on floor, warm wood bounce (180, 150, 110) at alpha 15.

---

### School Hallway — `LTG_ENV_school_hallway.png`
**Scene type:** Real World, institutional interior
**Time of day:** Daytime (school hours)

| Light Source | Position | Color (RGB) | Role |
|---|---|---|---|
| Fluorescent overhead | Above, evenly spaced | Cool white (235, 235, 245) | Key light |
| Window shafts (far end) | Far-center | SUNLIT_AMBER (245, 208, 140) at reduced intensity | Secondary |
| Ambient | Diffuse | Desaturated warm (210, 200, 185) | Fill |

**Character shading:**
- **Flat, institutional lighting.** Characters are lit primarily from above — top of head, shoulders catch highlight. Under-chin, torso underside are in soft shadow.
- **Desaturated fill.** Hallway lighting is intentionally less dramatic than home scenes. Character colors should be slightly desaturated compared to kitchen/study versions.
- **No strong directional shadow.** Overhead fluorescent = soft, diffuse, minimal cast shadow direction. Contact shadow is directly beneath (not offset to one side).
- **Value floor context:** Character shadow side values must not drop below hallway's value floor (NEAR_BLACK_WARM at 20). Deep shadows on characters = locker base shadows.

**Contact shadow:** Surface = hallway floor. Sample from FLOOR tile at character position. Shadow alpha 45 (slightly less than kitchen — fluorescent fill softens everything).
**Bounce light:** Minimal — institutional floor is close to neutral gray. Alpha 15 max.

**Cosmo note:** This is Cosmo's key environment. His figure-ground separation was a C38 fix (locker colors pushed lighter to avoid merge with his cardigan). Character shadow side must NOT approach LOCKER_LAV values.

---

### Classroom — `LTG_ENV_classroom_bg.png`
**Scene type:** Real World, institutional interior
**Time of day:** Daytime

| Light Source | Position | Color (RGB) | Role |
|---|---|---|---|
| Fluorescent overhead | Above-center | Cool white (235, 235, 245) | Key light |
| Window (left wall) | Upper-left | SUNLIT_AMBER (245, 208, 140), diffused | Warm fill |
| Ambient | Diffuse | Neutral warm (215, 205, 190) | Fill |

**Character shading:**
- **Even overhead + warm window fill.** Characters near the window (left side of frame) get warmer fill. Characters far from window (right/center) are more neutrally lit.
- **Slight warm fill.** Warmer than hallway but less dramatic than kitchen. Think of classroom as "gentle warmth" — not golden hour, not institutional sterile.
- **Chalkboard backing:** Characters standing at the chalkboard have a dark backing (chalkboard is darkest element). This is actually helpful for silhouette — ensure character HIGHLIGHTS are bright enough to read against the board.

**Contact shadow:** Surface = classroom floor. Sample from floor tile. Shadow alpha 45.
**Bounce light:** Similar to hallway. Neutral floor, alpha 15.

---

### Tech Den — `LTG_ENV_tech_den.png`
**Scene type:** Real World, warm interior (Cosmo's domain)
**Time of day:** Variable (typically after school / evening)

| Light Source | Position | Color (RGB) | Role |
|---|---|---|---|
| Desk lamp | Right-center | Warm white (255, 240, 200) | Key light |
| Monitor glow | Right, mid-height | Cool blue-white (180, 200, 230) | Accent |
| Ambient | Diffuse | Warm amber throughout | Fill |

**Character shading:**
- **Warm-dominant room.** Character highlight = warm white from desk lamp. The room is inherently warm-amber throughout (this caused the C40/C41 warm/cool QA issues).
- **Monitor accent:** If character is near the desk/monitor, the monitor-facing side gets a subtle cool accent rim. This is the main visual interest — the warm/cool split on the character.
- **Cosmo context:** Cosmo's striped shirt should pick up warm lamp highlight on the closest stripe, and the cool monitor accent on the far side.

**Contact shadow:** Surface = warm wood floor (180, 150, 110). Shadow alpha 50.
**Bounce light:** Warm wood floor bounce, alpha 20. Stronger than hallway/classroom.

---

### Living Room — `LTG_ENV_grandma_living_room.png`
**Scene type:** Real World, warm interior
**Time of day:** Evening / night

| Light Source | Position | Color (RGB) | Role |
|---|---|---|---|
| Reading lamp | Left | SUNLIT_AMBER (245, 208, 140) | Key light (Miri zone) |
| CRT | Center-left (per SF06 alignment C46) | CRT_COOL_SPILL (130, 175, 160) | Cool accent |
| Ambient | Diffuse | Warm (210, 190, 155) | Fill |

**Character shading:**
- **SF06 "The Hand-Off" setup:** Warm left (Miri + lamp) / cool right (CRT zone). Characters in the left half get warm-amber lighting. Characters in the right half near CRT get cool spill.
- **The warm-left / cool-right staging** (Layer 12c from C46) must carry through to character shading — a character moving from left to right in this room should transition from warm to cool highlight.
- **Miri position:** Typically left of CRT. Full warm amber lighting. Strong warm highlight on her left, softer fill on right.
- **Luma position:** Variable. Near CRT = cool highlight on CRT-facing side + warm ambient fill.

**Contact shadow:** Surface = carpet/floor. Warmer than kitchen tile — (185, 165, 125). Shadow alpha 50.
**Bounce light:** Warm floor/carpet bounce, alpha 20.

---

### Millbrook Street — `LTG_ENV_millbrook_main_street.png`
**Scene type:** Real World, exterior
**Time of day:** Dusk

| Light Source | Position | Color (RGB) | Role |
|---|---|---|---|
| Sky / sunset | Above, left | Warm amber-orange (245, 190, 120) | Key light |
| Street lamps | Scattered, above | Warm yellow (240, 220, 160) | Local fill |
| Ambient sky | Above | Cool blue (160, 175, 210) | Fill/bounce |

**Character shading:**
- **Dusk exterior with atmospheric perspective.** Characters in foreground get full color saturation. Characters in background tier lose saturation (per BG Saturation Drop rule: multiply by 0.75-0.85).
- **Warm top / cool bottom:** Sunset light hits from above-left. Top of head and shoulders get warm amber. Lower body receives cool ambient from shadowed street.
- **Street lamp pools:** Characters standing under a street lamp get warm local fill from above. Characters between lamps are in ambient shadow (cooler, less saturated).

**Contact shadow:** Surface = street/sidewalk. Sample from ground. Shadow alpha 55 (exterior shadows are slightly harder than interior).
**Bounce light:** Street surface bounce, alpha 15 (hard surface = less bounce than carpet).

---

### Glitch Layer — `LTG_ENV_glitchlayer_frame.png`
**Scene type:** Glitch World
**Time of day:** N/A (digital space)

| Light Source | Position | Color (RGB) | Role |
|---|---|---|---|
| Platform glow | Below | ELEC_CYAN (100, 220, 220) | Key uplight |
| Aurora bands | Above | HOT_MAGENTA (255, 0, 128) + ELEC_CYAN | Ambient |
| Void | Surrounding | Near-black | Negative fill |

**Character shading:**
- **Dramatic uplight from cyan platform.** Character's underside (legs, lower torso, chin) gets strong cyan tint. This is the opposite of real-world overhead lighting.
- **Luma's hoodie bottom, jeans, shoes should be cyan-tinted.** Upper body catches magenta aurora ambient.
- **Rim light:** Strong edge glow on character silhouette from environmental light. Characters in GL need STRONGER rim than real-world scenes to separate from the dark void.
- **No warm light.** GL has zero warm sources. Any warm on the character (Luma's orange hoodie base color) is the character's own color, not scene lighting.

**Contact shadow:** Platform surface = ELEC_CYAN. Shadow = darkened cyan (30, 80, 80). Alpha 60 (stronger than real-world — GL has harsh light/shadow transitions).
**Bounce light:** Strong cyan bounce from platform. Alpha 35 (strongest of any environment).

---

## Line Weight Audit

### Current State
| Element | Line Weight | Source |
|---|---|---|
| Background structural outlines | 1-2px | Environment generators |
| Background detail lines | 1px | Environment generators |
| Character body outlines | 2-3px | Expression sheet generators |
| Character detail lines (clothing, face) | 1-2px | Expression sheet generators |

### Assessment
Background and character line weights are in the same general range (1-3px), which is correct. However:

1. **Backgrounds have textured lines** (via paper_texture final pass) while **characters have clean, uniform lines**. This creates a visual language mismatch — backgrounds look like they were drawn on paper, characters look like they were drawn in a vector program.
2. **Background lines taper and vary** slightly due to the procedural drawing (polygon outlines with varying widths). Character outlines are uniform width throughout.
3. **Recommendation:** Characters need a `paper_texture` or similar final pass to match background line quality. Alternatively, a `variable_stroke()` function that draws character outlines with slight width variation (2-3px base with +/-0.5px random wobble).

---

## Compositing Pass Order (Corrected)

**Current (broken):**
1. Draw background
2. Apply scene lighting overlay (warm/cool split)
3. Draw character (flat, unlit)
4. Apply face lighting
5. Apply rim light

**Corrected:**
1. Draw background
2. Apply scene lighting overlay to background
3. Draw contact shadow at character position (using `LTG_TOOL_contact_shadow.draw_contact_shadow()`)
4. Draw character
5. Apply scene-responsive body shading (light direction from scene, colors from scene)
6. Apply face lighting (scene light color, not generic)
7. Apply rim light (colored to match scene accent light, not generic teal)
8. Apply bounce light from ground (`LTG_TOOL_contact_shadow.draw_bounce_light()`)
9. Apply edge tint (`LTG_TOOL_contact_shadow.tint_character_edges()`)

---

*Character-Environment Lighting Spec C50 — Hana Okonkwo, Environment & Background Artist*
