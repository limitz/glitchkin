# Critique — Color Design, "Luma & the Glitchkin"
**Critic:** Naomi Bridges, Color Theory Specialist
**Date:** 2026-03-29
**Materials Reviewed:**
- style_guide.md (color sections)
- color/palettes/master_palette.md
- color/color_keys/scene_color_keys.md
- color/style_frames/style_frame_01_discovery.md
- color/style_frames/style_frame_02_glitch_storm.md
- color/style_frames/style_frame_03_other_side.md

---

## Overall Assessment

This is a solid first-pass color system with a clear conceptual spine — warm analog world versus cool digital intrusion — and a color artist who understands the narrative function of palette. The master palette is well-annotated, the forbidden combinations list is genuinely thoughtful, and the three style frames demonstrate a real command of how light modifies color in context. These are not nothing.

However, there are structural problems that will compound at production scale, specific hex choices that undermine stated design intentions, unresolved technical contradictions between documents, and at least one character-palette decision that is going to cause real pain in the paint department. Some of the color narrative logic is poetic but imprecise in ways that will produce inconsistent results across a team. The system is not yet producible at scale as written. It needs a revision pass before it goes to any background painter or character colorist who wasn't in the room when this was designed.

**Grade: B-. Strong concept, incomplete execution.**

---

## Master Palette — Critique

### What Works

The governing principle of each section (Real World = storybook-left-in-the-sun; Glitch = maximally saturated invader) is clearly stated and consistently applied. The "Pairs with" and "Avoid using" notes show a colorist who has thought beyond swatches in isolation. The distinction between Deep Cocoa (`#3B2820`) as a warm line color and Void Black (`#0A0A14`) as a cold digital dark is excellent — this is exactly the kind of purposeful temperature-range management that makes a palette feel authored rather than assembled. The slight blue bias in Void Black (RGB 10, 10, 20 — note the blue channel lift of 20 vs. red/green at 10) is a genuinely smart choice and is correctly identified in the notes.

GL-07 Corrupted Amber (`#FF8C00`) as a bridge color between worlds is one of the best conceptual decisions in this palette. A transition hue that belongs to neither camp is necessary for the glitch-intrusion sequences to read as a *process* rather than an abrupt switch. Good.

### Problems

**Problem 1: The skin highlight color `#E8D4B0` is not documented in the master palette.**

The character section lists `#E8D4B0` as Luma's skin highlight ("one step lighter and less saturated than base"). This color appears nowhere in the master palette sections. It is a derived color — computed from `#C4A882` — which is fine, but the system claims to be the single source of truth. If an artist needs to recreate the skin highlight from scratch, they are mixing without a recipe. This needs an entry in Section 3 or a clear derivation note (e.g., "Skin Highlight = `#C4A882` desaturated 15% and lightened 15% in HSL"). As written, it is an undocumented color floating in the character spec.

**Problem 2: The cool-lit skin shadow `#7A5A7A` is similarly undocumented.**

The same issue as above. `#7A5A7A` (described as "desaturated violet shadow for night/glitch scenes") is used for both Luma and Cosmo but appears in no section of the master palette. It is a critical color — it governs how the human characters read in every Glitch Layer scene. Its absence from the master palette is a production error waiting to happen.

**Problem 3: RW-05 Rust Shadow and the shadow naming convention is inconsistent.**

The palette uses "Rust Shadow" (`#8C3A22`) as the shadow companion to Terracotta (`#C75B39`), but the character skin shadow (`#8C5A38`) is called "Skin Shadow" and the two values are only 0.08 units apart in hue. In hex:

- Rust Shadow: `#8C3A22` — RGB 140, 58, 34
- Skin Shadow: `#8C5A38` — RGB 140, 90, 56

These share an identical red channel (140) and are separated by only 32 points in green and 22 in blue. In context — small areas, surrounded by high-saturation colors — they are functionally indistinguishable. Forbidden combination #7 explicitly bans using Skin Shadow (`#8C5A38`) as a costume fill because it reads as flesh. But Rust Shadow (`#8C3A22`) is close enough that the same perceptual problem applies. If a painter reaches for the wrong swatch in either direction, they will not notice the error. These two colors need more separation or one of them needs to be reconsidered.

**Problem 4: `#1A1428` (night sky deep) is used in Color Key 02 but is absent from the master palette.**

Color Key 02 uses `#1A1428` as the primary night sky fill — it carries 25% of the palette in that scene, making it the largest single area color in the color key. It is not defined anywhere in either the Real World or Glitch palette sections. It is not GL-08 Void Black (`#0A0A14`) — it is meaningfully lighter and warmer (RGB 26, 20, 40 vs. 10, 10, 20). Style Frame 02 uses it directly. An undefined color carrying 25% of a major scene's visual mass is a significant gap.

**Problem 5: GL-03 Acid Green (`#39FF14`) has no shadow companion defined.**

Every Real World color in the palette that is used as a surface fill has a corresponding shadow tone (Sage Green → Deep Sage, Terracotta → Rust Shadow, skin → Skin Shadow, etc.). Acid Green, which is the primary fill for Glitchkin markings and the digital flora in the Glitch Layer, has no shadow companion specified. What is the shadow of a Glitchkin marking? What is the shadow color of the digital plant-life? In the Glitch Layer (Color Key 03), the ambient light is UV Purple — so Acid Green in shadow should shift toward what, exactly? `#1AA800` appears in Style Frame 03's plant section without being defined anywhere. This is an improvised color, not a system color. Define it.

**Problem 6: The Data Stream Blue (`#2B7FFF`) — UV Purple (`#7B2FBE`) pairing creates a simultaneous contrast problem that is not acknowledged.**

Both colors appear together extensively in Glitch Layer scenes. At their respective saturation levels and with `#2B7FBE`'s blue having a slight purple lean, these two are hue-adjacent (blue vs. blue-violet). When both appear on the `#0A0A14` void background, their simultaneous contrast will cause the blue to look greenish and the purple to look more red. This is a basic color interaction effect that is not addressed anywhere in the palette documentation. Either acknowledge it as intentional (it could be interesting) or add a note about managing this adjacency in compositions.

**Problem 7: The Character Color Keys for Byte contain a specification the production rules technically prohibit.**

Byte's body crevice shadow is listed as `#050508` (RGB 5, 5, 8 — essentially pure black with a blue ghost). The darkest value in the system is defined as `#0A0A14`. This is darker than the documented system minimum by a perceptible delta on screen. Either the system minimum needs updating or this shadow value needs to match. As written, the master palette claims `#0A0A14` is "the absolute dark value of the show" and then immediately violates that claim two pages later. Pick one.

---

## Color Keys — Critique

### Color Key 01 — Sunny Afternoon at Luma's House

This is the strongest of the four color keys. The 95%/5% Real World/Glitch split is correctly calibrated for a "calm before the adventure" scene. The three-light-source setup (Soft Gold from right, Dusty Lavender bounce, Shadow Plum shadows) is coherent and technically sound. The warm-from-upper-right to cool-interior gradient as a visual metaphor for the narrative journey within a single frame is exactly the kind of thinking this show needs.

**Issue: The shadow color for warm surfaces is `#5C4A72` (Shadow Plum) at 60% opacity.**

Opacity-based shadows are fine in concept, but the master palette specifies flat cel-shadow ("one flat shadow tone, no gradient" per the style guide). A shadow at 60% opacity is not flat — it will produce different values depending on the base color beneath it, which is composite behavior, not cel behavior. This either needs to be pre-multiplied into a fixed hex value for production (what does Shadow Plum at 60% opacity look like over `#FAF0DC`? It reads as approximately `#C3B8CF` — define that as the actual color) or the style guide's flat-shadow rule needs to explicitly permit opacity-based shadows. As written, there is a contradiction.

**Issue: 7 dominant colors is at the stated upper limit. The palette itself acknowledges this.**

This is not a critique of the choice — pushing to the limit for the show's "home base" scene is a defensible call. But the note in the document ("at the upper limit") reads as slightly anxious about its own decision. Either commit to 7 as correct here (and explain why), or cut one. My recommendation: the Electric Cyan trace at 2% is doing critical narrative work (the CRT hum), but the Warm Tan (`#C4A882`) skin tone is listed separately from other palette entries when characters are not visible in this establishing shot. If this is an environment-only key, the skin tone should not be in the palette ratio. That gets you to 6 meaningful environment colors plus the 1 glitch trace, and the justification becomes cleaner.

### Color Key 02 — Nighttime Glitch Attack on Main Street

The warm/cold split — ground retains warmth, sky is lost to glitch — is conceptually strong and the cinematography note about the horizontal invasion metaphor is good. The "warm cream windows as the emotional heart" note is exactly right. The 55%/45% Real World/Glitch tension is appropriately unresolved.

**Issue: The undefined `#1A1428` is the single largest area color (25%) in this key.**

Already noted above in the master palette critique. This is where the omission causes actual production impact. A colorist working from this key has to invent this color or search through all the documentation to understand what "a deep blue-purple, darker than Shadow Plum, approaching void but with warmth of a real night sky" means in hex. Tell them.

**Issue: The palette ratio lists 8 distinct color areas, but the stated maximum per scene is 5-7.**

Count them:
1. `#1A1428` Night Sky (25%)
2. `#3B2820` Deep Cocoa (15%)
3. `#00F0FF` Electric Cyan (18%)
4. `#FF2D6B` Hot Magenta (12%)
5. `#7B2FBE` UV Purple (10%)
6. `#C75B39` Terracotta (8%)
7. `#F0F0F0` Static White (7%)
8. `#FAF0DC` Warm Cream (5%)

That is 8 distinct primary fills. The style guide's "5-7 dominant colors max" rule is violated here. The document's own statement of work limits the palette to 7, and this scene needs 8. Either revise the scene's palette to consolidate two of these (Static White and Warm Cream are both light-value neutrals and could potentially collapse into one descriptive category), or formally update the scene palette limit to 8 for action-peak scenes. Do not leave this unresolved — every artist will count differently.

**Issue: Hot Magenta fills as a secondary key light on skin.**

The spec says Hot Magenta (`#FF2D6B`) fills from the storm's edge and falls as a fill light on the "upper surfaces of elements facing the storm — tops of heads, top of car roofs." This means Hot Magenta is landing on skin. Hot Magenta on Warm Tan skin produces approximately `#E46070` — a slightly desaturated salmon-pink that could easily read as a bruise or a burn depending on context. The show is described as "playful, energetic, and slightly surreal" — not violent. Be specific about exactly how this light interacts with skin and document the resulting skin color, because painters will not compute it consistently if it is left to interpretation.

### Color Key 03 — First Entry into the Glitch Layer

The under-lighting convention (light from below in the Glitch Layer) is a strong worldbuilding decision and the atmospheric perspective inversion (close = saturated, far = purple then void, versus Real World's warm haze) is exactly right. The 90%/10% Glitch/Real split is correct.

**Issue: The key light direction is "below and slightly forward" but the shadow color is UV Purple filling "the opposite side."**

If the key light comes from below, shadows fall upward — on the undersides of chins, the backs of knees, the inside of elbows. But UV Purple as a fill "on the opposite side" implies fill from above or from behind. For characters under-lit by Cyan with UV Purple fill, the resulting shadow pattern on faces is: bright chin, lit nose tip, darkened forehead and eye sockets. This is extremely specific and unusual and it needs a diagram or a much more precise description, because if any artist interprets "opposite side" as they might in a normal three-quarter lighting setup, the under-lighting effect will be wrong in every Glitch Layer frame.

**Issue: Acid Green appears as both a fill light source AND a tertiary ambient in the fill light description.**

The fill light section says: "Secondary fill: `#39FF14` (Acid Green) — from the digital flora: pixel-art plants and data-moss glow faintly with green light." This is a light source. But Acid Green has no defined behavior as a light color — only as a surface fill. What does Acid Green light do to Warm Tan skin? To Electric Cyan surfaces? To UV Purple surfaces? On dark backgrounds Acid Green is luminous, but on the mid-purple ambient surfaces it will create a color interaction that is not described anywhere. Either document the Acid Green lighting effect or remove it as a fill light source and keep it strictly as a surface color.

### Color Key 04 — Quiet Emotional Moment

This is technically the most restrained and emotionally intelligent key. The warm/cool split on character faces (warm gold lit side, Dusty Lavender shadow side) is a classic beauty lighting setup correctly applied. The 98%/2% Real World/Glitch split is right for the scene's function.

**Issue: Same opacity-based shadow problem as Color Key 01.**

Shadow on floor: `#5C4A72` at 50% opacity. This is the same problem noted above. Pre-multiply this into a fixed value. Over `#FAF0DC` base at 50% opacity, Shadow Plum reads as approximately `#CFCAD5` — a very pale lavender-grey. Name it. Lock it.

**Issue: The Sunlit Amber (`#D4923A`) at 20% is being used here as an ambient glow, but its own master palette note says "Avoid using as a broad sky fill — too saturated for large ambient areas."**

In Color Key 04, it covers 20% of the frame as ambient glow on "most surfaces." That is a large-area ambient application. The master palette's own caveat says it "works best in small-to-medium shapes." Either the caveat is wrong and should be revised, or this is a genuine overuse of a color that is being asked to do something it was specified not to do. At 20% ambient fill in an intimate scene, Sunlit Amber will push the scene's warmth into "orange" territory that reads more like a campfire than a lamp. This is one of the most common color warmth errors in animated production — "golden hour" logic applied too broadly, resulting in an orange soup. The Soft Gold (`#E8C95A`) is specified for lamplight in this exact context. Consider reducing Sunlit Amber's proportion and letting Soft Gold carry more of the warm work.

---

## Style Frames — Critique

### Style Frame 01 — "The Discovery"

This is the best color work in the package. The three-point lighting setup (Cyan from screen, Soft Gold from window, Dusty Lavender ambient) uses the show's own palette as a legitimate lighting language. The derived skin blend `#7ABCBA` (cyan-washed warm tan) is correctly computed — that is roughly what you get when you mix Cyan light over the base skin tone at high intensity, though the exact value will depend on the layer blending mode used in production (which is not specified, and it should be). The single Hot Magenta point of Byte's cracked eye in an overwhelmingly cyan-and-gold frame is the frame's best single color decision.

**Issue: The screen bloom at 40% opacity creates the same undocumented color problem as the opacity-based shadows.**

The "wide, soft circle of `#00F0FF` at 40% opacity radiating from the screen face" is an opacity-based color application on top of base fills. Over Warm Cream (`#FAF0DC`) it reads approximately `#97F8FD`. Over Ochre Brick (`#B8944A`) it reads as `#74B494`. These are very different derived colors and they appear on elements that different artists will be painting. Specify the actual resulting color on each major surface, or specify the blending mode and layer structure precisely enough that every artist gets the same result.

**Issue: The cited derived blend on Luma's hoodie — `#BF8A78` (orange desaturated under cyan key light) — is described imprecisely.**

"Orange + Cyan light = a slightly desaturated, slightly teal-washed warm tone" is poetic but not technically accurate. Orange (`#E8703A`) under Cyan light does not simply desaturate — it shifts toward brown/neutral because Cyan is the rough complement of orange on the color wheel (Cyan sits opposite orange-red; the mix of the surface color and the complementary light partially cancels saturation). The result is not "teal-washed" — it is neutralized warm. The distinction matters for consistency: "teal-washed" tells an artist to add cyan; "neutralized" tells them to desaturate. These produce different results. The hex value `#BF8A78` is approximately correct, but the verbal description needs to match the technical reality.

**Issue: The Electric Cyan (`#00F0FF`) pixel-grid pixels on the hoodie "become indistinguishable from the screen glow itself."**

This is called out as a positive effect ("the hoodie's grid appears to light up"), but it is also a readability problem. The hoodie's pixel grid is one of Luma's primary character-design signatures. If that grid merges with the background screen glow in the pilot's inciting incident frame, audiences learn her character signature in a state where it cannot be parsed. It should glow brighter, not merge. Consider specifying that the pixel grid retains a slightly higher value or outline separation (`#F0F0F0` edge on the pixel squares, for instance) even under the screen wash, so the pattern remains legible as a pattern rather than disappearing into the ambient.

**Issue: The frame cites no blending mode anywhere.**

The frame document specifies numerous opacity-based effects, glow treatments, and bloom effects. It cites no software context, no layer blending modes (multiply, screen, overlay?), and no compositing order. In a production with multiple artists contributing layers, this will produce wildly inconsistent results. At minimum, specify whether the CRT bloom is a "screen" blend at 40% opacity or a straight alpha composite. The distinction changes the resulting color completely.

### Style Frame 02 — "Glitch Storm"

This is a technically ambitious frame that works conceptually. The Glitch-owns-sky, buildings-are-fighting, street-is-contested architecture is the right color narrative for this scene. The note about Cosmo's Dusty Lavender jacket reading as teal under Cyan light (`#80C0D0`) is a real observation, not a romanticized one — Dusty Lavender is a blue-purple, and Cyan key light would indeed push it toward blue-green. Good.

**Issue: Luma's cast shadow is `#0A2A3A` but Cosmo's is described as "overlapping Luma's, same color."**

The two characters are presumably lit from the same angle (the crack, upper right), so their shadows would overlap. But Cosmo has a substantially different base palette (Dusty Lavender jacket vs. orange hoodie). The cast shadow color in a flat cel-animation system is determined by the ground surface, not the character — which is correct here (both shadows are the same cyan-tinted dark on the same ground plane). But the phrase "overlapping Luma's, same color" is sloppy. It implies the ground shadow is one flat tone regardless of what is above it. That is actually fine and correct for this style, but the reasoning should be stated, not implied, so later frames do not produce character shadows that have the character's own color bleeding into them (a common beginner error).

**Issue: The road surface at `#2A2A38` is an undefined color.**

This appears as a primary ground fill in this scene. It is not in the master palette. It is not derived from any documented color with any documented method. Same problem as `#1A1428` in the color key — it is a production color with no paper trail.

**Issue: Byte "paradoxically disappears" into the background is a production problem, not a feature.**

The document acknowledges that Byte's base color (`#0A0A14` Void Black) blends with the ambient Cyan atmosphere in a full glitch-attack scene, making him hard to read. This is presented as almost charming ("his cracked eye is still the alarm signal"). But Byte is a main character. He should be readable in every scene. If the ambient environment can swallow him, the character design or the scene lighting needs to compensate. Consider specifying a mandatory Static White (`#F0F0F0`) silhouette edge on Byte in high-cyan-ambient scenes — even a 1px border at production resolution would re-establish his silhouette without changing his color identity. This is not a minor note: a main character becoming invisible in a major action frame is a design failure.

**Issue: The Acid Green pixel confetti listed as a sky confetti color in this frame but Acid Green is GL-03, a Glitchkin and flora color.**

The style frame calls for `#39FF14` (Acid Green) particle confetti falling from the storm crack. But Acid Green is specified in the master palette as the color of Glitchkin markings and digital flora — "healthy glitch energy." If the storm crack is emitting Acid Green particles, it implies the storm itself is "healthy" digital energy, which is the opposite of the danger the scene is supposed to convey. Hot Magenta and Electric Cyan confetti from a danger-storm is correct. Acid Green confetti from a danger-storm contradicts the palette's own semantic assignment. Either remove the Acid Green from the storm confetti or explicitly address this narrative contradiction.

### Style Frame 03 — "The Other Side"

This is conceptually the most emotionally sophisticated frame in the package, and the color story — warmth carried in pigment but absent from lighting — is genuinely poetic and technically precise simultaneously. Byte's two eyes facing opposite directions is the best single character-color detail in any of these documents. The atmospheric perspective inversion (close = saturated, far = purple then void) is exactly right and should be treated as a core worldbuilding rule for every Glitch Layer scene.

**Issue: The skin highlight in Glitch Layer is `#4AB0B0` — this is not documented anywhere.**

"Skin highlight (platform bounce): faint `#4AB0B0` (cyan-influenced highlight) on her forehead and nose tip." This is a third skin-highlight value (the Real World highlight is `#E8D4B0`, the cool-lit highlight in this frame is `#4AB0B0`). Both are undocumented in the master palette. The system is generating scene-specific skin tone variants that no paint supervisor can maintain consistently. There should be a defined skin-modification ruleset for Glitch Layer lighting, not individual hex values invented per frame. Something like: "Under Cyan ambient in Glitch Layer, skin highlight = skin base modified 60% toward `#00F0FF`" is more producible than a unique hex per scene.

**Issue: `#6ABAFF` (lighter Data Blue for individual code characters in the waterfall) is another undocumented derived color.**

One more color appearing in production specs with no master palette entry. The pattern is clear: the system has a master palette that is incomplete, and the style frames are continuously generating new hex values to solve local problems. Every one of these undocumented values is a future consistency error.

**Issue: The "reverse gravity" pixel confetti behavior is called out for the first time here.**

"Predominantly falling-upward (slight reverse gravity in the Glitch Layer)" is a great worldbuilding detail. But it was not established in Color Key 03's confetti notes, and it directly contradicts the confetti behavior in Style Frame 02 where particles "emanate outward from the crack" (neither up nor down — radial). The three frames together imply three different confetti physics:
- Frame 01: particles "drift" in air (neutral float)
- Frame 02: particles "emanate outward" from cracks (radial, directional)
- Frame 03: particles "drift predominantly falling-upward" (reverse gravity)

These are different behaviors and they all occur without documentation about when and why. If confetti behavior changes based on context (Real World vs. Glitch Layer vs. active glitch event), that rule needs to be written down and applied in the color keys, not invented per frame.

---

## System-Level Issues

### Issue 1: The system generates new hex values at the frame level without feeding them back up to the master palette.

This is the most serious structural problem in the whole package. A production color system must be a closed loop: master palette defines all colors, scenes and frames reference master palette, any new color required by a scene is either mapped back to the master palette or formally added to it. This system currently has a one-way flow: master palette → frames, with no feedback mechanism. The undocumented colors currently scattered across the style frames include at minimum: `#7ABCBA`, `#3A7878`, `#BF8A78`, `#1A1428`, `#2A2A38`, `#0A2A3A`, `#6ABAFF`, `#4AB0B0`, `#7A5A7A`, `#E8D4B0`, `#1AA800`, and `#050508`. That is twelve production-critical colors with no master palette entries. On a long-form series, this is how color drift happens. Six months in, you have fifty undocumented colors, and no two painters are using the same values.

### Issue 2: The Real World warm palette is internally coherent; the Glitch palette is not.

The Real World palette has a clear value hierarchy (Warm Cream → Soft Gold → Sunlit Amber → Terracotta → Rust Shadow → Deep Cocoa) and every fill has a corresponding shadow. The Glitch palette has Electric Cyan, Hot Magenta, Acid Green, UV Purple, Static White, Data Stream Blue, and Corrupted Amber — but no defined shadow companions for most of them, no stated value hierarchy, and no explicit relationship between them beyond "they are all saturated." When Glitch Layer scenes require shadow colors, the system is currently improvised. That will produce inconsistency.

### Issue 3: The "5-7 dominant colors per scene" rule is being applied inconsistently.

Color Key 01: 7 colors (plus 2 accents). Color Key 02: 8 colors (plus 3 accents). Color Key 03: 7 colors (plus 3 accents). Color Key 04: 7 colors (plus 3 accents). The distinction between "dominant palette" and "accent colors" is being used to cheat the 7-color limit. If Acid Green confetti covers meaningful visual area in Color Key 02 (large particles "10-15px at production res"), it is not an accent — it is a palette color. The 7-color rule needs a rigorous definition of what counts as dominant vs. accent, or it will be routinely gamed by every artist who needs an eighth color.

### Issue 4: The opacity-based shadow convention contradicts the flat-shadow production rule and is unresolved.

Already cited in multiple individual critiques above. This is a systemic contradiction, not isolated errors. The style guide says "one flat shadow tone, no gradient." Multiple color keys use "Shadow Plum at 60% opacity" and "Shadow Plum at 50% opacity" as shadow specifications. These are not flat tones — they are opacity effects. Either the flat-shadow rule must be amended to allow specified opacity passes, or every opacity reference in the color keys must be converted to pre-computed fixed hex values. There is no middle ground. On a production with ten background painters, "Shadow Plum at 60% opacity" will produce different results depending on whether the artist applies it in Photoshop (blend modes available), TVPaint, or Harmony. Define the resulting color, not the method.

### Issue 5: The forbidden combinations list is too short.

Seven forbidden combinations is a good start. But looking across the palette, there are additional pairings that will cause problems in production and are not addressed:

- `#7A9E7E` (Sage Green) adjacent to `#2B7FFF` (Data Stream Blue): These are hue-adjacent (green and blue) at different saturations. In Glitch Layer scenes where Acid Green digital flora appears, Data Stream Blue data structures nearby will create a low-key color vibration that reads as undefined rather than intentional. This should either be explicitly permitted with context notes or flagged.
- `#A89BBF` (Dusty Lavender) adjacent to `#7B2FBE` (UV Purple): Dusty Lavender is the Real World shadow/sky color; UV Purple is the Glitch Layer ambient. These are in the same hue family at very different values and saturations. In transition scenes where both worlds overlap, placing them adjacently makes the Real World shadow look like a washed-out version of the Glitch color — it undermines both. This is most dangerous in Color Key 02 where both appear in the same scene.
- `#C4A882` (Warm Tan skin) with `#B8944A` (Ochre Brick): These two colors are close enough in hue and value that in small shapes — hands against a wooden surface, a character against a brick wall — they will merge. This is not a forbidden combination per se, but it needs a contrast note or a size restriction.

---

## Critical Issues (Must Fix)

Listed in priority order.

1. **Document all undocumented production colors.** All twelve-plus hex values that appear in style frames but not in the master palette must be added to the master palette or replaced with documented values. This is not optional before production starts.

2. **Resolve the opacity-shadow vs. flat-shadow contradiction.** Every "at X% opacity" shadow specification must be converted to a pre-computed fixed hex value, or the style guide must be formally amended to permit opacity shadows and specify the exact blending mode. Provide the blending mode for every compositing effect in the style frames.

3. **Define the Glitch Layer character skin-modification ruleset.** Luma's skin under Glitch Layer lighting generates at least three different hex values across these documents. Replace all of them with a stated rule that any artist can apply in any scene.

4. **Add `#1A1428` to the master palette.** This is the primary night sky color, the largest area fill in Color Key 02, and the dominant value in the Glitch Storm frame's atmosphere. It is being used as a system color and is not defined as one.

5. **Fix Byte's visibility in high-cyan-ambient scenes.** A main character going invisible in major action frames is not acceptable. Define a silhouette preservation protocol for Byte in Electric Cyan-dominant environments.

6. **Resolve the Acid Green confetti in the danger-storm scene.** Acid Green means "healthy/non-dangerous glitch energy." A danger storm emitting Acid Green confetti is a semantic contradiction. Correct the confetti palette for Frame 02's storm crack to Hot Magenta and Electric Cyan only.

7. **Write the pixel confetti behavior ruleset.** Three frames have three different confetti physics. Document when and why confetti behavior differs, keyed to scene context (Real World vs. Glitch Layer vs. active glitch event).

8. **Separate Rust Shadow (`#8C3A22`) and Skin Shadow (`#8C5A38`) more decisively.** Currently 22 points of blue-channel difference at the same red value. They need to be distinguishable under production conditions. Consider shifting Rust Shadow to `#7A2810` (darker, more muted) to create unambiguous visual distance from the skin value.

---

## Recommendations

1. **Produce a derived-color addendum to the master palette.** Instead of generating new hex values at the frame level, establish a formulaic derivation table: "Under Electric Cyan key light, warm tan skin = RW-10 + [specific modification]." Lock those derived values. Name them (e.g., "CRT-Lit Skin," "Glitch Layer Skin"). Every scene-specific skin variant should derive from a documented rule, not be invented individually.

2. **Add a Glitch palette value hierarchy.** The Real World palette has one. The Glitch palette needs one: the equivalent of the Warm Cream → Deep Cocoa progression but in the cool/neon register. A simple table stating the Glitch palette's lightest-to-darkest value range will prevent artists from inventing intermediate values.

3. **Produce a lighting interaction cheat sheet.** For each primary surface color in the show (orange hoodie, Dusty Lavender jacket, Warm Tan skin), document what that surface looks like under each of the show's four main light types (warm gold, Electric Cyan, Hot Magenta, UV Purple ambient). Twelve cells in a table. This will save more time in production than any other single document the color department could produce.

4. **Formalize the forbidden combination list to ten or twelve entries.** The current seven are correct. Add at minimum the Dusty Lavender/UV Purple adjacency warning and the Sage Green/Data Stream Blue hue-vibration note.

5. **Add blending mode specifications to all effects in style frames.** Every bloom, glow, opacity-based light spill, and scan line overlay needs a stated blending mode and opacity value that will produce a consistent result across software platforms. "40% opacity bloom" is not a production specification; "`#00F0FF` at 40% opacity, Screen blend mode, on top of base layer" is.

6. **Promote Color Key 03's atmospheric perspective inversion to a governing Glitch Layer rule.** It appears only in the cinematography notes of Key 03. It should be a top-level rule in the Glitch Layer section of the master palette, given equal weight to the palette's governing principles. It is that important to the show's visual coherence.

---

## Verdict

The color system for "Luma & the Glitchkin" has a strong conceptual foundation and genuinely good instincts about the show's visual emotional language. The warm/cool narrative architecture is clear. The palette's organic worldbuilding (Soft Gold as safety, Hot Magenta as danger, Corrupted Amber as transition) is well-conceived. The best moments of the style frames — the single magenta eye in the Discovery, the warm windows as the emotional heart of the Glitch Storm, the absence of warm light in the Glitch Layer and what that says about loneliness — demonstrate a colorist who understands that color tells story.

But the system is not production-ready.

It has undocumented colors proliferating below the master palette level. It has a structural contradiction between the flat-shadow rule and the opacity-based shadow specifications. It has a forbidden combination list that is incomplete. It generates improvised values at the frame level instead of deriving consistently from documented rules. And it has a character readability problem (Byte in Cyan environments) that is acknowledged but not solved.

The concept earns a high mark. The execution as a producible system earns a low one. The gap between them is what a revision pass is for.

Fix the twelve undocumented colors. Resolve the opacity contradiction. Write the lighting interaction cheat sheet. Then this system is close to what it needs to be.

Do not send this to the paint department as it currently stands.

---

*Naomi Bridges — Color Theory Specialist*
*Guest Critic, "Luma & the Glitchkin" Review Cycle 01*
*2026-03-29*
