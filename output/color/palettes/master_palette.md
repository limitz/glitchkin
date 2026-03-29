# Master Color Palette — "Luma & the Glitchkin"

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**Version:** 2.0 (Cycle 2 Audit — full hex reconciliation, shadow companion system, forbidden combination expansion)
**References:** style_guide.md v1.0, style_frame_01_discovery.md, style_frame_02_glitch_storm.md, style_frame_03_other_side.md

> This document is the single source of truth for all color decisions on the show. Every hex code herein is final until a revision is issued. If a color is not in this document, it does not belong in a frame.
>
> **Cycle 2 Change Summary:** All hex values referenced in style frames 01–03 and character specifications have been audited and added. Shadow companion colors now documented for every fill color in both palettes. Opacity-based specs have been eliminated — all shadows are flat hex. `#050508` exception documented (see Section 2). Rust Shadow and Skin Shadow distinguished and confirmed as non-conflicting. Acid Green shadow companion added. Three additional forbidden combinations added.

---

## SECTION 1 — REAL WORLD PALETTE

The Real World palette evokes the warmth, safety, and slight scruffiness of a small analog town. Colors are drawn from mid-century illustration, golden-hour photography, and aged paper. Nothing is too saturated. Nothing is too bright. The world is *inviting* before it is exciting.

**Governing principle:** Real World colors are warm-leaning, slightly desaturated relative to glitch colors, and grounded in earthy hue families (yellows, oranges, reds, greens, purples as shadows). They should feel like they belong in a storybook painting that has been left in the sun for a few years.

---

### RW-01 — Warm Cream
- **Hex:** `#FAF0DC`
- **RGB:** 250, 240, 220
- **Role:** Primary light value; default sky in daytime scenes, bright interior walls, paper surfaces, light fabric fills
- **Shadow companion:** `#E8C95A` (Soft Gold — warm cream in shadow steps toward gold, not grey); deepest shadow: `#D4923A`
- **Use-case notes:** This is the most common large-area fill in the Real World. Apply it to any surface that is catching strong warm daylight. It reads as "white" to the eye in context but never creates the stark harshness of true white. Works as the baseline from which all warm shadows descend.
- **Pairs with:** #E8C95A (sunlit areas), #D4B896 (mid-tone transitions), #3B2820 (line work)
- **Avoid using:** As a character fill — too pale for skin tones and costume primaries. Characters always need higher saturation than this.

---

### RW-02 — Soft Gold
- **Hex:** `#E8C95A`
- **RGB:** 232, 201, 90
- **Role:** Sunlight color, warm accent, optimism and safety signifier
- **Shadow companion:** `#D4923A` (Sunlit Amber — gold steps toward amber in shadow)
- **Use-case notes:** The color of afternoon sunlight striking a surface. Use for lit window frames, sunbeam shafts, bright grass in golden hour, Luma's hoodie pixel accents. Also used as a warm rim-light tone on characters facing the sun. This color says "you are safe here."
- **Pairs with:** #FAF0DC (light-to-gold transition), #C75B39 (warm harmony), #7A9E7E (warm/cool contrast)
- **Avoid using:** In shadow areas. It is strictly a light-side color. Do not use it as a neutral mid-tone.

---

### RW-03 — Sunlit Amber
- **Hex:** `#D4923A`
- **RGB:** 212, 146, 58
- **Role:** Warm midtone, direct afternoon sunlight on mid-value surfaces, transition between gold and terracotta
- **Shadow companion:** `#C75B39` (Terracotta — amber's natural shadow is terracotta)
- **Use-case notes:** Sits between Soft Gold and Terracotta in the warm range. Use on wooden surfaces catching direct sun, warm-toned sidewalks, brick in sun, and as the lit side of orange-toned clothing. Also useful as the ambient underpainting tone for golden-hour scenes. Not as bright as gold, not as saturated as terracotta — it's the workhorse warm mid.
- **Pairs with:** #E8C95A (highlights), #C75B39 (shadow transition), #FAF0DC (direct highlight)
- **Avoid using:** As a broad ambient fill — too saturated for large ambient areas. Works best in small-to-medium shapes. **NOTE: Sunlit Amber must not be used as a 20% ambient fill in Color Key 04 — this violates its use-case notes. Key 04 has been corrected to use Warm Cream (#FAF0DC) for ambient fill at that coverage level.**

---

### RW-04 — Terracotta
- **Hex:** `#C75B39`
- **RGB:** 199, 91, 57
- **Role:** Architecture primary, warm accent, structural color of the Real World
- **Shadow companion:** `#8C3A22` (Rust Shadow)
- **Use-case notes:** The signature architectural color of Millbrook Town. Rooftops, chimney stacks, window surrounds, terracotta pots. Also used in warm-side shadow on pale/cream surfaces when the ambient light is very warm. Cosmo's shirt accent stripe. Provides visual weight and warmth. When placed next to glitch cyan, it creates the "intruder" tension the show needs.
- **Pairs with:** #E8C95A, #FAF0DC (warm palette harmony), #A89BBF (complementary cool contrast)
- **Avoid using:** In scenes set in the Glitch Layer — it reads as too "homey" there and undercuts the alien quality of the digital world.

---

### RW-05 — Rust Shadow
- **Hex:** `#8C3A22`
- **RGB:** 140, 58, 34
- **Role:** Shadow tone for terracotta and warm orange *architectural* surfaces; underside shadow on warm exterior buildings
- **Shadow companion:** `#3B2820` (Deep Cocoa — for deepest crevice in terracotta/orange shadows)
- **Distinction from Skin Shadow (`#8C5A38`):** Rust Shadow `#8C3A22` (R:140, G:58, B:34) vs. Skin Shadow `#8C5A38` (R:140, G:90, B:56). Blue channel: 34 vs. 56 — a 22-point gap. Green channel: 58 vs. 90 — a 32-point gap. **These are architecturally different colors.** Rust Shadow has stronger red-towards-brown character, less orange warmth. Skin Shadow reads as more orange-brown. However the blue channels are within a range that could confuse painters. **Corrective action:** Rust Shadow remains at `#8C3A22`. To prevent painter error, note: Rust Shadow is used ONLY on non-skin architectural and object surfaces. Skin Shadow is used ONLY on character skin. Their use-case separation prevents in-frame confusion. Never use both adjacent on the same character.
- **Use-case notes:** Shadow companion to Terracotta. When a terracotta wall is in shade, use this — not a generic grey or brown. Keeping shadows color-consistent with the lit surface (just darker and more saturated toward cool) maintains the overall warm harmony. Also used as a deep warm accent in architectural details and as the shadow in floor grain (wooden floorboards). Never use on character skin.
- **Pairs with:** #C75B39 (its parent swatch), #3B2820 (for deepest crevice shadows)
- **Avoid using:** As a standalone color in large areas — it is a supporting shadow tone, not a primary fill. Never on character skin.

---

### RW-06 — Sage Green
- **Hex:** `#7A9E7E`
- **RGB:** 122, 158, 126
- **Role:** Foliage, calm backgrounds, school interiors, Grandma Miri's cardigan
- **Shadow companion:** `#4A6B4E` (Deep Sage)
- **Use-case notes:** The principal cool-relief color in the Real World palette. Used for trees, hedges, grass in open shade, interior walls in calmer spaces (school hallways, Luma's bedroom walls). Prevents the warm palette from feeling oppressive. Provides breathing room. When glitch energy appears near sage green, the visual intrusion is immediately readable because of the temperature shock.
- **Pairs with:** #FAF0DC (background harmony), #E8C95A (warm/cool contrast), #4A6B4E (shadows)
- **Avoid using:** In scenes requiring maximum tension — its calm quality works against it there.

---

### RW-07 — Deep Sage
- **Hex:** `#4A6B4E`
- **RGB:** 74, 107, 78
- **Role:** Shadow tone for foliage and green surfaces; depth in tree canopies; Grandma's garden shaded areas
- **Shadow companion:** `#3B2820` (Deep Cocoa — for deepest shadow in green foliage)
- **Use-case notes:** Shadow companion to Sage Green. Carries the cool/green identity into shade without going grey. Necessary for giving foliage believable depth in a flat graphic style — without this deep shadow, trees read as flat discs. Also used in background environmental shadows during daytime scenes.
- **Pairs with:** #7A9E7E (parent swatch), #3B2820 (deepest value shadows)
- **Avoid using:** On characters — too close in value to the line color to be legible.

---

### RW-08 — Dusty Lavender
- **Hex:** `#A89BBF`
- **RGB:** 168, 155, 191
- **Role:** Sky in twilight/overcast scenes, shadow tone for light surfaces, secondary building fill, reflections of open sky in windows
- **Shadow companion:** `#5C4A72` (Shadow Plum)
- **Use-case notes:** The primary "cool" neutral in the Real World palette. It sits in the purple/blue-grey range, providing shadows that feel atmospheric rather than dirty. Use it as the shadow tone on cream-colored walls, as the twilight/evening sky color, and for interior shadows in rooms lit by northern window light. It is the color of "not quite night yet." Also used for Cosmo's jacket fill — it suits his careful, slightly nervous personality.
- **Pairs with:** #FAF0DC (shadow on light surface), #C75B39 (complement tension), #7A9E7E (cool harmony)
- **Avoid using:** As a line color — too light. Never as a primary character color unless it's clearly an intentional personality choice.

---

### RW-09 — Shadow Plum
- **Hex:** `#5C4A72`
- **RGB:** 92, 74, 114
- **Role:** Deep shadow tone for lavender/cool surfaces; nighttime shadow accent; the shadow color when dusk is the ambient light
- **Shadow companion:** `#0A0A14` (Void Black — deepest shadow in cool/night scenes steps toward digital void)
- **Use-case notes:** When Dusty Lavender is in shadow, it drops toward this deep purple-grey. Key for nighttime scenes where the primary cool light source is moonlight or indirect sky. Also essential for shadow-side architecture at night — gives depth without using the glitch palette's UV Purple. The distinction matters: Shadow Plum is an organic, atmospheric shadow; UV Purple is artificial, digital.
- **Flat shadow values (replaces any opacity-based specs):** Shadow Plum used as cast shadow = use flat `#5C4A72` (no opacity). For a deeper cast shadow variation, step down to `#3D2F4F`. Do NOT specify "#5C4A72 at 60%" or "#5C4A72 at 70%" — those were Cycle 1 errors. Use `#5C4A72` directly, or `#3D2F4F` for the deeper pass.
- **Pairs with:** #A89BBF (parent swatch), #0A0A14 (deepest value), #3B2820 (line work adjacent)
- **Avoid using:** Adjacent to Electric Cyan or Hot Magenta in foreground areas — it muddies both.

---

### RW-09b — Shadow Plum Deep
- **Hex:** `#3D2F4F`
- **RGB:** 61, 47, 79
- **Role:** Deeper cast shadow variant for Shadow Plum; replaces all opacity-based specs (e.g., the former "Shadow Plum at 70%" specs in color keys)
- **Use-case notes:** Added in Cycle 2 to provide the flat hex equivalent of the depth variation that was previously specified using opacity. Use this — not an opacity blend — wherever a "heavier" Shadow Plum cast shadow is needed (e.g., character cast shadows on warm floors).
- **Pairs with:** #5C4A72 (parent), #0A0A14 (deepest shadow)
- **Avoid using:** As a costume or fill color — it is a shadow-only tone.

---

### RW-10 — Warm Tan
- **Hex:** `#C4A882`
- **RGB:** 196, 168, 130
- **Role:** Skin mid-tone base for human characters (Luma, Cosmo, Grandma Miri), dirt paths, aged wood
- **Shadow companion (warm light):** `#8C5A38` (Skin Shadow)
- **Shadow companion (cool/night light):** `#7A5A7A` (Cool Skin Shadow — see RW-10c)
- **Use-case notes:** The primary skin tone for the show's human cast. It is warm, readable, and has enough saturation to pop against backgrounds without crossing into orange-orange. Applied as the base fill for all human skin in standard lighting. Paths, worn wood floors, and cardboard also use this tone. Fundamental for believable character rendering.
- **Pairs with:** #E8C95A (skin highlight), #8C5A38 (skin shadow), #3B2820 (line)
- **Avoid using:** On non-organic surfaces — it has a distinctly fleshy quality that feels wrong on metal or glass.

---

### RW-10a — Skin Highlight
- **Hex:** `#E8D4B0`
- **RGB:** 232, 212, 176
- **Role:** Highlight zone on human skin (forehead, cheekbone, nose tip); one step lighter and less saturated than Warm Tan base
- **Use-case notes:** Single highlight tone for all human characters under warm standard lighting. Used in hero close-ups. Not used in background or mid-ground character passes.
- **Pairs with:** `#C4A882` (parent skin base)
- **Avoid using:** As a fill color outside of skin highlight zones.

---

### RW-10b — Skin Shadow
- **Hex:** `#8C5A38`
- **RGB:** 140, 90, 56
- **Role:** Shadow tone for human skin; underside of arms, under chin, inside of mouth
- **Shadow companion:** `#3B2820` (Deep Cocoa — deepest crevice in skin)
- **Distinction from Rust Shadow (`#8C3A22`):** Skin Shadow `#8C5A38` (G:90, B:56) vs. Rust Shadow `#8C3A22` (G:58, B:34). Green channel is 32 points apart; blue channel is 22 points apart. Skin Shadow is noticeably more orange-warm; Rust Shadow leans more toward deep red-brown. Use-case separation enforces the distinction: Skin Shadow = character skin ONLY; Rust Shadow = architectural/object surfaces ONLY.
- **Use-case notes:** The one shadow tone for all human character skin under warm lighting. Stays in the orange/brown family so shadows read as warm and friendly rather than grey and grim. Per the style guide, cel-shadow only — one flat shadow tone. This is that tone. For cool-lit scenes (nighttime, Glitch Layer), this shifts to Cool Skin Shadow `#7A5A7A` applied as the shadow fill.
- **Pairs with:** #C4A882 (parent swatch), #3B2820 (darkest crevice)
- **Avoid using:** As a large-area background color — too "skin-ish." Never as architectural or object fill (see Forbidden #7).

---

### RW-10c — Cool Skin Shadow
- **Hex:** `#7A5A7A`
- **RGB:** 122, 90, 122
- **Role:** Shadow tone for human skin under cool or night lighting (moonlight, Glitch Layer ambient, Glitch storm scenes)
- **Use-case notes:** Replaces Skin Shadow (#8C5A38) when the scene's ambient light is cool. Shifts the shadow toward desaturated violet — cooler than the warm skin shadow, but not grey. The violet quality keeps the skin reading as alive (grey would read as dead). Used in all Glitch Layer scenes and nighttime scenes for human characters.
- **Pairs with:** #C4A882 (skin base), #5A3A5A (deep Glitch Layer shadow — see GL-derived colors)
- **Avoid using:** In warm daytime Real World scenes — default to #8C5A38 there.

---

### RW-11 — Deep Cocoa
- **Hex:** `#3B2820`
- **RGB:** 59, 40, 32
- **Role:** Primary line color for all character and foreground object outlines; deepest shadow accents; hair on dark-haired characters
- **Shadow companion:** N/A — this is the deepest Real World value. The only step below this is Void Black, which belongs to the Glitch palette.
- **Use-case notes:** Per the style guide, this is the universal line color — NOT black. It is warm enough to feel hand-drawn and organic. At small sizes (line weight), it reads as dark enough to define form. As a fill, it is the color of the darkest hair, the inside of a very dark shadow, the crevice under a rock. Luma's hair color. Essential everywhere.
- **Pairs with:** Everything — it is the neutral anchor of the Real World palette
- **Avoid using:** In place of Void Black in digital/glitch contexts — the warmth reads wrong there. Never on Void Black backgrounds (see Forbidden #6).

---

### RW-12 — Muted Teal
- **Hex:** `#5B8C8A`
- **RGB:** 91, 140, 138
- **Role:** Painted metal surfaces (old machinery, CRT casing, vintage appliances), cool interior accent walls
- **Shadow companion:** `#3A5A58` (Dark Teal Shadow — see RW-12a)
- **Use-case notes:** A desaturated teal that bridges the green and blue worlds without going into glitch territory. Perfect for the CRT monitor casing in Grandma's den — it is slightly digital in feel (teal hints at screens) while being clearly aged and analog. Also works for old metal cabinet doors and the faint color of afternoon sky when haze is present. Deliberately lower saturation to keep it in the Real World category.
- **Pairs with:** #FAF0DC (light surface harmony), #3B2820 (line), #E8C95A (warm/cool contrast)
- **Avoid using:** Near Electric Cyan — they compete and the teal looks muddy. Give them separation in a composition.

---

### RW-12a — Dark Teal Shadow
- **Hex:** `#3A5A58`
- **RGB:** 58, 90, 88
- **Role:** Shadow tone for Muted Teal surfaces (CRT casing shadow side, aged metal in shade)
- **Use-case notes:** Shadow companion to Muted Teal. Added in Cycle 2 from style frame documentation. The CRT casing's shadow side uses this tone.
- **Pairs with:** `#5B8C8A` (Muted Teal), `#3B2820` (line)
- **Avoid using:** As a primary fill.

---

### RW-13 — Ochre Brick
- **Hex:** `#B8944A`
- **RGB:** 184, 148, 74
- **Role:** Aged brick, cobblestone mortar, sun-worn wood trim, secondary architectural accent
- **Shadow companion:** `#8C3A22` (Rust Shadow) or `#8C5A38` for warmer-toned brick
- **Use-case notes:** Sits between Soft Gold and Terracotta but more muted — the color of old brickwork that has been in the sun for decades. Millbrook's streets and older buildings rely on this for character. Works as a unifying mid-tone when terracotta and gold are both present in a scene — it bridges them. Also useful for the warm floor tone in Grandma's den.
- **Pairs with:** #C75B39 (harmony), #8C3A22 (shadow), #FAF0DC (light)
- **Avoid using:** As a skin tone — it reads orange in context.

---

## SECTION 1B — DERIVED / LIGHT-MODIFIED REAL WORLD COLORS

These are not freestanding palette colors — they are the documented results of Real World colors being modified by specific lighting conditions (screen glow, glitch storm, Glitch Layer ambient). They exist so that painters always have a flat hex value to reference rather than calculating a blend on their own. Do not use these in scenes other than the ones specified.

---

### DRW-01 — Cyan-Washed Skin (Screen-lit)
- **Hex:** `#7ABCBA`
- **Source:** `#C4A882` (Warm Tan) modified by intense Electric Cyan screen glow
- **Scene use:** Style Frame 01 — Luma's right (screen-facing) cheek. Also applicable to any character lit face-on by Cyan key light.
- **Shadow companion:** `#3A7878` (Deep Cyan-Toned Shadow — see DRW-02)

### DRW-02 — Deep Cyan-Toned Skin Shadow
- **Hex:** `#3A7878`
- **Source:** Shadow on cyan-washed skin
- **Scene use:** Style Frame 01 — Luma's screen-lit face shadow zone.

### DRW-03 — Hoodie Under Cyan Light
- **Hex:** `#BF8A78`
- **Source:** `#E8703A` (Luma's hoodie orange) modified by Electric Cyan key light
- **Scene use:** Style Frame 01 — the orange hoodie's lit surface under screen glow. The complementary hue relationship between orange and cyan produces this desaturated warm-grey.
- **Shadow companion:** `#3A1A14` (deep warm shadow in storm/glitch lighting)

### DRW-04 — Warmed Tan (Window-lit)
- **Hex:** `#D4B88A`
- **Source:** `#C4A882` (Warm Tan) modified by Soft Gold window light
- **Scene use:** Style Frame 01 — Luma's left (window-facing) skin.

### DRW-05 — Teal-Washed Arm Skin
- **Hex:** `#5AB0AE`
- **Source:** `#C4A882` extreme cyan modification (Luma's reaching arm, closest to screen)
- **Scene use:** Style Frame 01 — the most intensely lit zone on Luma's body.

### DRW-06 — CRT Casing Screen-Influenced
- **Hex:** `#3AACAA`
- **Source:** `#5B8C8A` (Muted Teal) casing front face under screen glow
- **Scene use:** Style Frame 01 — CRT casing face only.

### DRW-07 — Storm-Modified Hoodie Orange
- **Hex:** `#C8695A` *(Cycle 13 corrected — was `#C07A70`)*
- **RGB:** 200, 105, 90
- **Source:** `#E8703A` under intense Cyan storm key. Complementary hue relationship (orange vs. cyan) desaturates the orange toward a muted warm tone. The B channel (90) reflects the cyan temperature shift.
- **HSL:** approx. (9°, 50%, 57%) — 50% saturation. Exceeds background building walls (ENV-06 saturation ~28%) per character-over-background saturation rule.
- **Cycle 13 correction (Sam Kowalski — Naomi C12-3):** Prior value `#C07A70` RGB(192,122,112) calculated HSL saturation ≈39% — however background building walls (ENV-06 after correction) have saturation ~28%, and prior ENV-06 `#9A8C8A` had only ~5% saturation. With the ENV-06 correction, the saturation differential was marginal. Fix: increase DRW-07 saturation to min 40%. New value RGB(200,105,90) achieves ~50% saturation — clear margin above corrected ENV-06 background. Orange material identity retained.
- **Scene use:** Style Frame 02 storm sequence. Luma's front-facing hoodie surface (storm key angle).
- **Cross-reference:** Updated in `LTG_TOOL_style_frame_02_glitch_storm_v001.py` and `LTG_TOOL_colorkey_glitchstorm_gen_v001.py` (Cycle 13).

### DRW-08 — Storm-Modified Skin (Cyan key)
- **Hex:** `#6AB4AE`
- **Source:** `#C4A882` under cyan storm key, Frame 02
- **Scene use:** Style Frame 02.

### DRW-09 — Storm-Modified Jacket (Cosmo)
- **Hex:** `#80C0CC`
- **Source:** `#A89BBF` (Dusty Lavender jacket) under cyan storm key
- **Scene use:** Style Frame 02.

### DRW-10 — Storm Jacket Shadow (Cosmo)
- **Hex:** `#2A1A32`
- **Source:** Deep shadow on Cosmo's lavender jacket under storm conditions
- **Scene use:** Style Frame 02.

### DRW-11 — Glitch Layer Skin (UV Ambient)
- **Hex:** `#A87890`
- **Source:** `#C4A882` (Warm Tan) modified by UV Purple ambient in the Glitch Layer
- **Scene use:** Style Frame 03 — Luma's skin in the Glitch Layer. Haunting lavender-warm blend.
- **Shadow companion:** `#5A3A5A` (Deep Lavender-Plum — see DRW-12)

### DRW-12 — Glitch Layer Skin Shadow
- **Hex:** `#5A3A5A`
- **Source:** Deep shadow on Glitch Layer skin
- **Scene use:** Style Frame 03.

### DRW-13 — Glitch Layer Skin Highlight (Cyan-Teal Platform Bounce)
- **Hex:** `#4AB0B0`
- **Source:** Cyan platform-bounce highlight on skin in Glitch Layer
- **Scene use:** Style Frame 03 — forehead and nose tip highlight from platform glow. Note: label corrected from "Warm" — `#4AB0B0` is a cyan-teal (R:74, G:176, B:176), the result of Electric Cyan bounce light striking skin from below. It reads cool and distinctly digital, not warm.

### DRW-13b — Glitch Layer Skin Highlight (Cool-Toned Variant)
- **Hex:** `#8A6A7A`
- **Source:** UV Purple ambient catch-light on skin for characters with cooler warm-skin undertones
- **Use-case notes:** Added Cycle 2 to address Glitch Layer skin rendering for characters whose skin base sits in a cooler warm-tan range. The DRW-11 skin (A87890) derives from the standard #C4A882 warm base. For characters whose skin has a cooler undertone, the UV Purple ambient produces this slightly more grey-lavender result. Painters working on Grandma Miri or background human characters in the Glitch Layer should use this variant.

### DRW-14 — Glitch Layer Hoodie (UV Ambient)
- **Hex:** `#C07038`
- **Source:** `#E8703A` hoodie orange under UV Purple ambient
- **Scene use:** Style Frame 03.

### DRW-15 — Hoodie Hem Under Cyan Bounce
- **Hex:** `#5AA8A0`
- **Source:** Bottom hem of hoodie under platform bounce Cyan light (Style Frame 03)
- **Scene use:** Style Frame 03 — lowest inch of hoodie only.

### DRW-16 — Shoulder Under Waterfall Blue — DRW-16 RESOLVED (Cycle 13)
- **Hex:** `#9A7AA0`
- **RGB:** 154, 122, 160
- **Source:** Hoodie orange right shoulder under Data Stream Blue (`#2B7FFF`) waterfall overhead light. Complementary hue shift: orange (warm) under blue (cold) key → desaturated violet-grey result. R=154 retains slight orange warmth; B=160 reflects the Data Stream Blue dominance.
- **Painter warning (DRW-16):** This is the most complex single-surface color on Luma. It is NOT a shadow value and NOT a neutral grey — it is a hue-shift result specific to the Data Stream Blue key angle at this position in Style Frame 03. Do NOT substitute HOODIE_AMBIENT (#B36250) or HOODIE_SHADOW (#B84A20) — both are too warm and read incorrectly under a blue-dominant overhead key.
- **Scene use:** Style Frame 03 — Luma's right shoulder under the Data Stream Blue waterfall. Glitch Layer scenes with active blue overhead source.
- **Cross-reference:** `luma_color_model.md` — DRW-16 painter warning added Cycle 13.
- **Resolution note:** DRW-16 was flagged by Naomi Bridges Cycle 7 as a required painter warning. The entry existed in this section but the warning was not propagated to `luma_color_model.md`. Cross-reference now bidirectional. DRW-16 RESOLVED — Cycle 13 (Sam Kowalski).

### DRW-17 — Magenta-Influenced Hair (Storm)
- **Hex:** `#6A2A3A`
- **Source:** `#3B2820` hair under Hot Magenta fill light from storm (style frame 02)
- **Scene use:** Style Frame 02 motion arcs, hair rim highlights.

### DRW-18 — Luma Hair Base (Glitch Layer)
- **Hex:** `#1A0F0A`
- **RGB:** 26, 15, 10
- **HSL:** hue ~18°, saturation ~44%, **lightness ~7%**
- **Source:** `#3B2820` (Deep Cocoa) modified by UV Purple ambient in the Glitch Layer. The hair's warm brown identity is suppressed toward near-void-dark; the UV Purple catches only the crown as a rim sheen (GL-04 `#7B2FBE`).
- **Warmth note (C32):** R:26 nominally exceeds G:15, B:10, giving a theoretical hue of ~18°. However, at 7% lightness this hue is **functionally imperceptible** — the value reads as near-void dark, indistinguishable from void black to the eye. DRW-18 does NOT contribute visual warmth to SF03. It is a near-neutral presence whose only visible color quality is the UV Purple rim sheen (GL-04) painted over it on the crown. Warm values in SF03 are hoodie orange and skin only. *(Per Priya Nair C13 P2 — "visually unsupported" warmth claim corrected.)*
- **Scene use:** Style Frame 03 — Luma's hair base fill in the Glitch Layer. Pair with GL-04 (`#7B2FBE`) UV Purple rim sheen on hair crown.
- **Shadow companion:** GL-08a `#050508` (Below-Void-Black — deepest crevice in near-void dark hair).
- **Avoid using:** As a line color or large-area fill. This is hair-base only in Glitch Layer scenes. Do not use in Real World scenes — use `#3B2820` (Deep Cocoa, RW-11) there.
- **Added:** Sam Kowalski — Cycle 15 (2026-03-29), from Style Frame 03 spec `(26, 15, 10)` hair base value.

---

### C10-1 RESOLVED — Cold Overlay Boundary Arithmetic (Style Frame 01)

**Status: RESOLVED — Cycle 13 (Sam Kowalski)**
**Originally flagged: Naomi Bridges Cycle 10. Outstanding 3 cycles.**

**The Issue:** The `draw_lighting_overlay()` function in `style_frame_01_rendered.py` had an incorrect comment claiming the cold overlay alpha was "near-zero / 3.5%" at the 80px warm/cold boundary zone. Naomi identified this as arithmetically wrong in her Cycle 10 report.

**The Arithmetic (verified):**
- Resolution: W=1920, H=1080
- Monitor center x: `monitor_cx = W * 11 // 15 ≈ 1408`
- Warm/cold boundary x: `W // 2 - 80 = 880`
- Distance from monitor center to boundary: 1408 - 880 = 528px
- Cold overlay max radius: `int(W * 0.55) = 1056px`
- Normalized distance at boundary: t = 528 / 1056 = 0.50
- Cold alpha at boundary: `int(cold_alpha_max * (1 - t)) = int(60 * 0.50) = 30`
- As percentage: 30/255 = **11.8%**

**The incorrect prior comment said:** "both alphas near-zero / ~3.5%" — this was wrong.

**Correct values (documented in `style_frame_01_rendered.py` since Cycle 10):**
- `cold_alpha_max = 60` — peak alpha at monitor center
- At the 80px overlap zone (x=880), cold alpha ≈ **30 (~11.8%)**
- At the warm zone's starting edge (x=960), cold alpha ≈ 0 (fully feathered out)

**Visual decision:** `cold_alpha_max = 60` RETAINED. At ~12% opacity, the cold cyan cross-light at the 80px boundary reads as a plausible split-light transition (warm lamp left / cool monitor right). This is not cold contamination — it is intentional atmospheric separation. The warm skin tones under ~12% cold cyan overlay remain readable as warm.

**Code location:** `style_frame_01_rendered.py` header (Cycle 10 note, lines 12–19) and `draw_lighting_overlay()` function inline comments (lines 1292–1294).

---

## SECTION 1C — ENVIRONMENTAL DERIVED COLORS

Flat hex values for environment surfaces under specific lighting conditions. Established in style frames; painters must use these rather than re-deriving.

| Code | Hex | Description | Parent Surface | Scene |
|---|---|---|---|---|
| ENV-01 | `#2A2A38` | Night asphalt base | Road surface, nighttime | Frame 02 |
| ENV-02 | `#2A5A6A` | Asphalt under Cyan key | Road under storm crack light | Frame 02 |
| ENV-03 | `#4A3A2A` | Asphalt under warm spill | Road under building window light | Frame 02 |
| ENV-04 | `#3A3848` | Nighttime sidewalk | Sidewalk surface, night | Frame 02 |
| ENV-05 | `#0A2A3A` | Cyan-cast shadow | Character cast shadows under Cyan key | Frame 02 |
| ENV-06 | `#96ACA2` | Terracotta under Cyan key — CORRECTED Cycle 13 | Building walls Cyan-lit, storm | Frame 02 |
| ENV-07 | `#5A3820` | Dark Warm Wood / Deep warm shadow (building) | Building shadow side, storm; background wood surfaces in warm/amber lighting | Frame 02, Frame 03 |
| ENV-08 | `#1A1820` | Near-void roofline | Roof silhouettes against storm sky | Frame 02 |
| ENV-09 | `#1A2838` | Dark blue-grey slab | Glitch Layer platform surfaces facing up | Frame 03 |
| ENV-10 | `#0A1420` | Near-void slab face | Glitch Layer vertical structure faces | Frame 03 |
| ENV-11 | `#2A1A40` | Deep atmospheric purple | Far-distance Glitch Layer structures | Frame 03 |
| ENV-12 | `#2B2050` | Layer 4-5 transition sky | Glitch Layer sky near-void transition | Frame 03 |
| ENV-13 | `#211136` | Far structure edge (void-scale) | Megastructure silhouettes at void-scale distance | Frame 03 |

### ENV-13 — Far Structure Edge (Void-Scale)
- **Hex:** `#211136`
- **RGB:** 33, 17, 54
- **Derivation:** 20% UV Purple `#7B2FBE` over Void Black `#0A0A14` background. Formula: R: 10×0.8+123×0.2=33, G: 10×0.8+47×0.2=17, B: 20×0.8+190×0.2=54. Result: RGB(33,17,54) = `#211136`.
- **Role:** The edge/silhouette color for the largest far-void megastructures in the Glitch Layer — continent-scale planes barely distinguishable from the void. Used exclusively for structure outlines/edges at maximum depth (Layer 4 / far distance, Style Frame 03).
- **Distinction from Depth Tier `FAR_EDGE` (0,40,55) `#002837`:** The depth-tier FAR_EDGE is a cyan-derived procedural construction value for `bg_glitch_layer_frame.py`. ENV-13 is a purple-over-void derivation for SF03 megastructure silhouettes. Different scenes, different derivation, different family. Do not substitute one for the other.
- **Shadow companion:** GL-08 `#0A0A14` (Void Black — the structure fills are void-dark; the edge is this barely-visible purple lift).
- **Use-case notes:** Draw as thin polygon outlines (1-2px) on far-distance slab polygons in Glitch Layer scenes. Never use as a fill color on large areas — these structures are barely visible at void scale. Their bodies use ENV-11 `#2A1A40` or FAR_EDGE fills; this value is their edge stroke only.
- **Added:** Sam Kowalski — Cycle 15 (2026-03-29), from Style Frame 03 spec far-distance structure edge derivation.

### ENV-06 — Terracotta Under Cyan Key (Corrected Cycle 13)
- **Hex:** `#96ACA2`
- **RGB:** 150, 172, 162
- **Cycle 13 correction (Jordan Reed / Naomi C12-1):** The prior value `#9A8C8A` RGB(154,140,138) was arithmetically wrong — R channel dominated (154 > G:140 > B:138), making the wall read WARMER on the cyan-lit face than on the shadow face. This is the opposite of how cyan key light behaves. Correct derivation requires G > R and B near/above R on any cyan-lit face. New value RGB(150,172,162): G=172 > R=150, B=162 > R=150 — correctly signals cool (cyan) lighting. Implemented in `LTG_TOOL_colorkey_glitchstorm_gen_v001.py` (Cycle 13).
- **NOTE for Jordan Reed:** The SF02 background generator (`LTG_TOOL_style_frame_02_glitch_storm_v001.py`) still uses the old value `TERRA_CYAN_LIT = (154, 140, 138)`. Update to `(150, 172, 162)` (#96ACA2) on next pass.
- **Naomi reference formula (35% cyan wash, for verification):** R: 199×0.65+0×0.35=129, G: 91×0.65+240×0.35=143, B: 57×0.65+255×0.35=126 → RGB(129,143,126). Both formulas agree on the direction: G>R, B≈R. The implemented value RGB(150,172,162) has a stronger cyan influence (~40% mix) and is acceptable.

### ENV-03 — Warm Window Spill (Canonical Alpha)
- **Hex:** `#4A3A2A`
- **RGB:** 74, 58, 42
- **Canonical warm spill alpha:** **40/255 (~16%)** — used in `LTG_TOOL_style_frame_02_glitch_storm_v001.py` (gradient falloff, max 40).
- **Cycle 13 alignment (Sam Kowalski — Naomi C12-2):** The color key generator (`LTG_TOOL_colorkey_glitchstorm_gen_v001.py`) previously used a flat alpha of 150/255 (~59%) for this same scene value. This was misaligned with the SF02 bg script. Both scripts now use alpha 40 (~16%). Rationale: warm window spill in a storm night scene is a subtle background light, not a dominant source — 16% is correct. 59% would overpower the dominant cyan key from the crack.
- **This is the same ENV-03 entry as in the table above — this note adds the canonical alpha specification.**

### ENV-07 — Dark Warm Wood
- **Hex:** `#5A3820`
- **RGB:** 90, 56, 32
- **Role:** Background wood surfaces in warm/amber lighting — floors, furniture, shelving; deep warm shadow on building exteriors in storm or warm night lighting
- **Use-case notes:** Background wood surfaces in warm/amber lighting — floors, furniture, shelving. Also the shadow side of building walls when the ambient is warm rather than cool (storm scenes where the glitch light has not yet reached that surface). A rich, dark walnut-brown that reads as definitively wood without being too orange. Established in Frame 02 (storm scene building shadow sides, left-facing walls away from the glitch crack). Do not use in place of Rust Shadow on character-adjacent surfaces — ENV-07 is for background and architectural surfaces only.
- **Pairs with:** `#B8944A` (Ochre Brick — lit wood surface), `#8C3A22` (Rust Shadow — shadow on warmer wood), `#3B2820` (Deep Cocoa — deepest wood grain shadows)
- **Avoid using:** On character skin or costume — it reads as architectural, not organic.

---

## SECTION 1D — NIGHT SKY COLOR

### RW-NS — Night Sky Deep
- **Hex:** `#1A1428`
- **RGB:** 26, 20, 40
- **Role:** Real World nighttime sky; base sky color for nighttime scenes before glitch intrusion
- **Shadow companion:** `#0A0A14` (Void Black — the sky goes to digital void if the glitch infects it)
- **Use-case notes:** A deep blue-purple that reads as genuine night sky — it has the quality of real darkness, with the warmth of a real night sky (slight purple lift), not the pure cold of the digital void. Not derived from the glitch palette, despite similar hue family — its warmth and slight tonal variation distinguish it. Used in Key 02 and storm-adjacent night scenes.

### RW-NSM — Moon Ambient
- **Hex:** `#C8BFD8`
- **RGB:** 200, 191, 216
- **Role:** Moonlight ambient color; thin cool lavender sheen on surfaces under moonlight
- **Use-case notes:** The light quality of the moon in nighttime scenes — thinner and cooler than Dusty Lavender, without the purple depth of Shadow Plum. Used as a highlight tone on upward-facing surfaces under clear moonlight. Also used for the lit side of characters standing in pure moonlight (no glitch interference).

---

## SECTION 2 — GLITCH PALETTE

The Glitch palette is an invader. These colors do not belong to the natural world — they are the colors of corrupted data, overloaded circuits, and broken display technology. They are maximally saturated, occasionally fluorescent, and should create immediate visual discomfort when placed against the warm Real World tones.

**Governing principle:** Glitch colors are cool-to-neutral in temperature (cyans, magentas, greens, purples) and aggressively saturated. They should feel like they are *wrong* in warm Real World scenes — like a scream in a library. In the Glitch Layer itself, they become the new normal, and the occasional warm accent (a memory of the Real World) becomes the intrusion.

**Glitch Shadow Companion System:** Every Glitch fill color must have a documented shadow tone. In the Glitch Layer, shadows do not go to generic grey — they go toward UV Purple or Void Black, depending on depth. The table below provides the complete shadow companion system for the Glitch palette.

| Fill Color | Fill Hex | Shadow Companion | Shadow Hex | Notes |
|---|---|---|---|---|
| Electric Cyan | `#00F0FF` | Deep Cyan | `#00A8B4` | Cyan shadow stays in the cyan family — do not let it go grey |
| Byte Teal | `#00D4E8` | Deep Cyan | `#00A8B4` | Byte's body fill (Cycle 5). Same shadow companion as Electric Cyan. Highlight is #00F0FF. |
| Hot Magenta | `#FF2D6B` | Magenta Shadow | `#8C1A3A` | Deep saturated magenta-red; keeps danger energy in shadow |
| Acid Green | `#39FF14` | Dark Acid Green | `#1AA800` | Green shadow preserves biological "aliveness" quality |
| UV Purple | `#7B2FBE` | Deep Digital Void | `#3A1060` | Deep purple approaching void; space between data |
| Static White | `#F0F0F0` | Light Glitch Grey | `#B0B0C0` | Off-white steps toward cool blue-grey in shadow |
| Data Stream Blue | `#2B7FFF` | Deep Data Blue | `#1040A0` | Shadow step for data flow structures |
| Corrupted Amber | `#FF8C00` | Corrupted Amber Shadow | `#A84C00` | Deep orange-brown for amber in shadow |
| Void Black | `#0A0A14` | Below-Void-Black | `#050508` | See exception note below |

---

### GL-01 — Electric Cyan
- **Hex:** `#00F0FF`
- **RGB:** 0, 240, 255
- **Role:** Primary glitch energy color; Byte's aura and glow; active scan-line effect; the most common glitch color
- **Shadow companion:** `#00A8B4` (Deep Cyan)
- **Use-case notes:** The signature color of the show's digital world. When glitch energy appears, it is first and most often this. Byte's outline glow is this exact color. Used for the light emitted by the CRT screen, glitch portals, active data streams in the Glitch Layer, and "infected" objects. In Real World scenes, a single stroke of this color signals danger/magic/the digital world intruding.
- **Contrast notes:** Places next to #C75B39 (terracotta) creates maximum visual dissonance — the intended effect. On dark backgrounds (#0A0A14), it reads as pure light.
- **Avoid using:** As a large fill in Real World scenes — reserve it for details and accents there. Save large fills for Glitch Layer scenes.

---

### GL-01a — Deep Cyan
- **Hex:** `#00A8B4`
- **RGB:** 0, 168, 180
- **Role:** Shadow companion to Electric Cyan; Byte's inner glow (subsurface ambient); pixel grid shadow on Luma's hoodie
- **Use-case notes:** This is the shadow tone for all Electric Cyan surfaces. Also used as Byte's ambient inner glow — a deep cyan that reads as "lit from within." Used for interior detail lines on Byte's form. Do not substitute Electric Cyan for this in shadow zones — the contrast is important.
- **Pairs with:** `#00F0FF` (parent)

---

### GL-01b — Byte Teal
- **Hex:** `#00D4E8`
- **RGB:** 0, 212, 232
- **Role:** Byte's body fill color (all flat surfaces — body core, limbs). Replaces the former Electric Cyan (#00F0FF) fill per Cycle 5 Art Director decision.
- **Shadow companion:** `#00A8B4` (Deep Cyan — same as Electric Cyan's shadow companion; the shadow system is shared)
- **Highlight companion:** `#00F0FF` (Electric Cyan — Byte's brightest surfaces and pixel-eye displays use the pure color)
- **Relationship to Electric Cyan:** Byte Teal sits between Electric Cyan (#00F0FF) and Deep Cyan (#00A8B4) in the cyan family. It is approximately 6% darker and slightly more saturated toward the teal end. **It is not a replacement for Electric Cyan — it exists alongside it.**
- **Why this color exists — Shared Visual DNA:** Byte and Luma share the Electric Cyan identity because Byte is made of the same glitch energy that powers Luma's hoodie pixel pattern. This is intentional, not a conflict. However, using identical #00F0FF for both Byte's fill AND Luma's pixel accents caused figure-ground failures (Byte disappearing in cyan-dominant environments — see critic note from Cycle 4). The solution: Byte's FILL shifts to #00D4E8 (Byte Teal), creating visible separation, while his HIGHLIGHTS remain #00F0FF, preserving the identity link where it matters most — at his brightest, most expressive surfaces.
- **Use-case notes:** Apply exclusively as Byte's body fill (body core, limbs). Do not use for glitch energy effects, scan lines, or any other purpose — Electric Cyan (#00F0FF) remains the correct choice for those. This color is Byte-specific.
- **Cyan-dominant environment rule:** When Byte appears in front of a cyan-dominant background, apply a Corrupted Amber (#FF8C00) outline to Byte's silhouette. This is the figure-ground protection rule. Cross-reference GL-07 (Corrupted Amber) for outline width standard.
- **USAGE WARNING — CHARACTER BODY FILL ONLY:** This is Byte's body fill color exclusively. For world CRT screen emission (monitor glow, scan lines, digital environment lighting), use GL-01 (Electric Cyan `#00F0FF`). Do NOT use GL-01b (`#00D4E8`) as a world/environment color — using Byte Teal as ambient monitor screen color merges Byte's body with the environment and destroys figure-ground legibility.
- **Pairs with:** `#00F0FF` (highlight and identity anchor), `#00A8B4` (shadow), `#FF8C00` (Corrupted Amber outline in cyan environments)
- **Avoid using:** For any purpose other than Byte's body fill. Do not use on backgrounds, effects, other characters, or world screen emission.

---

### GL-02 — Hot Magenta
- **Hex:** `#FF2D6B`
- **RGB:** 255, 45, 107
- **Role:** Danger signal, corruption sparks, warning glitches, the Corruption's primary body color
- **Shadow companion:** `#8C1A3A` (Magenta Shadow)
- **Use-case notes:** The second most important glitch color, and the one that carries the most danger. Where Electric Cyan is mysterious and slightly beautiful, Hot Magenta is alarming. It is used for error states, dangerous glitch energy, the crackling edges of a corrupting portal. The Corruption (if/when it appears as a villain) is primarily this color. Also used as the ARIA (alarm) color in the Glitch Layer's interface elements.
- **Contrast notes:** Against #0A0A14 it reads as neon. Against #FAF0DC it reads as aggressive — intentional for intrusion moments.
- **Avoid using:** In warm, safe Real World scenes unless the intent is immediate danger signaling. Never use it casually.

---

### GL-02a — Magenta Shadow
- **Hex:** `#8C1A3A`
- **RGB:** 140, 26, 58
- **Role:** Shadow tone for Hot Magenta surfaces; deep danger zones
- **Use-case notes:** Keeps the danger-red energy active even in shadow areas. Do not let Hot Magenta shadow go to a generic dark — the menace must survive into the shadow.

---

### GL-03 — Acid Green
- **Hex:** `#39FF14`
- **RGB:** 57, 255, 20
- **Role:** Glitchkin body markings, digital flora in Glitch Layer, data-packet trails, "healthy" glitch energy (as opposed to corrupted)
- **Shadow companion:** `#1AA800` (Dark Acid Green)
- **Semantic rule — ENFORCED:** Acid Green = healthy/positive glitch energy. It MUST NOT appear in danger or corrupted contexts without a formal override note. See Style Frame 02 note below.
- **Use-case notes:** The most "alive" of the glitch colors — it reads as biological within the digital world. Glitchkin (other than Byte) use this as their primary marking color. In the Glitch Layer, the pixel-art plants and data-moss are this color. It is the warm (relatively) cousin in the cool glitch family. Also used for positive feedback signals and progress bars in the Glitch Layer's visual language.
- **STYLE FRAME 02 SEMANTIC NOTE:** Acid Green appears as pixel confetti in the Glitch Storm frame. This usage has been corrected in Style Frame 02 v2.0 — see that document for the updated confetti color specification. The storm confetti now uses Hot Magenta and UV Purple for the danger-zone particles; Acid Green confetti, if present, is restricted to particles that have come from Glitchkin themselves (their markings shedding), not from the storm energy.
- **Contrast notes:** On void black, it reads as luminous plant-life. Against lavender or sage green, it creates a jarring vibration — use carefully and always intentionally.
- **FORBIDDEN COMBINATION:** See Section 4 — do not place this on Hot Magenta backgrounds.
- **Avoid using:** In skin-adjacent areas — it makes characters look poisoned.

---

### GL-03a — Dark Acid Green
- **Hex:** `#1AA800`
- **RGB:** 26, 168, 0
- **Role:** Shadow companion to Acid Green; underside of pixel-art plants; Glitchkin marking shadow tones
- **Use-case notes:** Keeps the biological/alive character of Acid Green in shadow areas. Used on the shadow undersides of digital flora in the Glitch Layer. Also the shadow tone for Glitchkin markings. Receives Electric Cyan bounce light on upper faces (see Style Frame 03 plant specification).

---

### GL-04 — UV Purple
- **Hex:** `#7B2FBE`
- **RGB:** 123, 47, 190
- **Role:** Deep digital space, portal interiors, the void between data structures, shadow color within the Glitch Layer
- **Shadow companion:** `#3A1060` (Deep Digital Void)
- **Use-case notes:** The deepest, richest glitch color — the color of the digital deep. Where Void Black is the absence of data, UV Purple is the vast space *between* data. In the Glitch Layer, this is the ambient sky color at depth, the color of distant impossible geometry. Also used as the inside color of active portals and teleport effects. It acts as the "shadow" analog in the Glitch Layer — the cool counterpart to Shadow Plum in the Real World.
- **Pairs with:** #0A0A14 (deep shadow), #00F0FF (neon glow against dark), #FF2D6B (high tension accent)
- **Avoid using:** In Real World scenes — it reads as "fantasy portal" and loses impact if overused there.

---

### GL-04a — Deep Digital Void
- **Hex:** `#3A1060`
- **RGB:** 58, 16, 96
- **Role:** Shadow companion to UV Purple; deepest void shadows in the Glitch Layer
- **Use-case notes:** The shadow step below UV Purple. Used for the absolute darkest zones of Glitch Layer structures where UV Purple is the primary fill. Provides depth without going all the way to Void Black.

---

### GL-04b — Atmospheric Depth Purple (Mid-Void Band)
- **Hex:** `#4A1880`
- **RGB:** 74, 24, 128
- **Role:** Atmospheric perspective band in the Glitch Layer sky at mid-depth; the distinct value layer between ambient UV Purple (`#7B2FBE`) and the near-void upper sky (`#3A1060`). Ensures adjacent aurora bands are separated by at least 2 luminance steps for readability at thumbnail scale.
- **Shadow companion:** `#3A1060` (Deep Digital Void — GL-04a)
- **Relative luminance:** approximately 0.017 — sits between UV Purple (~0.28) and Deep Digital Void (~0.06), creating a legible 4-band value ladder (Void Black → GL-04b → UV Purple → Data Blue).
- **Use-case notes:** Use exclusively as an atmospheric sky band at the mid-depth layer in Glitch Layer scenes. It is not a character color, not a fill for structural surfaces, and not a substitute for UV Purple in shadow roles. Its sole purpose is to create visible tonal separation in Glitch Layer sky gradients where UV Purple and Deep Digital Void would otherwise merge at thumbnail scale. Documented in `color_key_generator.py` as `deep_uv_sep` (Key 03 aurora fix).
- **Pairs with:** `#7B2FBE` (UV Purple — immediate lighter neighbor), `#3A1060` (Deep Digital Void — immediate darker neighbor)
- **Avoid using:** As a surface fill, character color, or anywhere outside atmospheric sky-band context. Do not substitute for GL-04a in shadow roles.

---

### GL-05 — Static White
- **Hex:** `#F0F0F0`
- **RGB:** 240, 240, 240
- **Role:** Glitch noise, specular pops on screen surfaces, extreme overexposure flash effects, highlight on Byte's body
- **Shadow companion:** `#B0B0C0` (Light Glitch Grey)
- **Use-case notes:** The maximum light value in the entire show (except a true-white specular pop, used once per major scene maximum). In glitch contexts, used for: static noise patterns, the brief flash when a portal opens, the highlight dot in digital characters' eyes, the edge-shimmer on active scan lines. This is slightly warm by nature of its off-white quality, which prevents the harshness of pure white while still reading as "maximum brightness."
- **Avoid using:** As a large background fill — reserve for small high-contrast pops. Never on skin.

---

### GL-05a — Light Glitch Grey
- **Hex:** `#B0B0C0`
- **RGB:** 176, 176, 192
- **Role:** Shadow companion to Static White in Glitch contexts; dimmed scan line texture; faint structural grid
- **Use-case notes:** The shadow step of Static White. Cool blue-grey cast keeps it in the Glitch palette family.

---

### GL-06 — Data Stream Blue
- **Hex:** `#2B7FFF`
- **RGB:** 43, 127, 255
- **Role:** Data flow visualization (the "waterfall code" in the Glitch Layer), interface UI elements, safe/navigable pathways in digital space
- **Shadow companion:** `#1040A0` (Deep Data Blue)
- **Use-case notes:** A more legible, less aggressive blue than the Electric Cyan family — used for data structures that are *functional* rather than wild. The waterfalls of scrolling code in the Glitch Layer are this color. Also applied to the "map" display Byte projects, and to navigable paths in the digital world. Provides middle ground between Electric Cyan's chaos and UV Purple's depth.
- **Pairs with:** #00F0FF (hue family harmony), #7B2FBE (depth recession), #0A0A14 (background)
- **Avoid using:** As a primary character color — too close to neutral blue, loses the "digital energy" quality.

---

### GL-06a — Deep Data Blue
- **Hex:** `#1040A0`
- **RGB:** 16, 64, 160
- **Role:** Shadow companion to Data Stream Blue; shadow side of data waterfall columns; deep navigational pathway edges
- **Use-case notes:** Keeps data structures legible in shadow without going to UV Purple.

---

### GL-06b — Light Data Blue
- **Hex:** `#6ABAFF`
- **RGB:** 106, 186, 255
- **Role:** Brightest individual characters in data waterfall columns; lit highlight on Data Stream Blue surfaces
- **Use-case notes:** When the data waterfall has catch-light on individual code characters, they lift to this lighter blue. Not a shadow — a highlight variant. Documented from Style Frame 03.

---

### GL-06c — Storm Confetti Blue
- **Hex:** `#0A4F8C`
- **RGB:** 10, 79, 140
- **Role:** Dominant cold confetti color in the Glitch Storm (Style Frame 02). Carries 70% of cold confetti weight. Darker and cooler than GL-06 Data Stream Blue due to atmospheric perspective — storm confetti in the far/mid distance reads darker as it recedes through the cyan-dominant storm atmosphere.
- **Derivation:** GL-06 (#2B7FFF) desaturated and darkened by approximately 45% to represent atmospheric depth recession within the storm. This is not an error or a substitute for GL-06 — it is the same blue family seen through storm atmosphere and distance haze. Registered in Cycle 28 per Priya Nair critique (C12).
- **Shadow companion:** `#06304A` (near-void confetti shadow — implicit, construction value only)
- **Use-case notes:** Storm scene (SF02) confetti generation only. The 70/20/10 split (Storm Confetti Blue / Void Black / Electric Cyan) creates the cold threat of the storm. At full saturation GL-06 reads too vibrant for distance atmosphere — GL-06c is the correct atmospheric derivative. **Do not substitute GL-06 for GL-06c in the storm generator:** GL-06 reads as close-field data structure, not storm distance.
- **Source file:** `output/tools/LTG_TOOL_style_frame_02_glitch_storm_v004.py` constant `DATA_BLUE`.
- **Pairs with:** GL-01 (Electric Cyan — near-field accent confetti), GL-05 (Void Black — weight/depth confetti)
- **Avoid using:** As a data structure color (use GL-06), as a character color, as any Real World sky or water color.

---

### GL-07 — Corrupted Amber
- **Hex:** `#FF8C00`
- **RGB:** 255, 140, 0
- **Role:** "Corrupted Real World" objects — things from the warm world that have been partially overwritten by glitch energy; warning states in the Glitch Layer interface; Byte's figure-ground outline in cyan-dominant environments
- **Shadow companion:** `#A84C00` (Corrupted Amber Shadow)
- **Use-case notes:** This is the bridge color — the one color that sits between the Real World and the Glitch palette. When a real-world object (a flower, a bicycle, a park bench) begins to be consumed by glitch energy, its warm tones shift toward this corrupted amber before being overtaken by the full glitch palette. It is Soft Gold turned electric and slightly wrong. Also used in warning animations — an amber pulse before a Hot Magenta danger signal.
- **Pairs with:** #FF2D6B (escalation — amber to danger), #E8C95A (Real World echo), #0A0A14 (Glitch Layer background)
- **Avoid using:** As a purely "warm" color in safe contexts — it should always carry a slight unease.

#### GL-07 — Corrupted Amber Usage Guidelines (Cycle 5 — Critic Feedback)

**Similarity to Real World Ambers — Defined Boundary:**
Corrupted Amber `#FF8C00` sits visually close to the Real World amber family (`#E8C95A` Soft Gold, `#D4923A` Sunlit Amber). The distinction is context and saturation:
- Real World ambers (Soft Gold, Sunlit Amber) appear in daytime warm scenes, as light, as sunlit architectural surfaces, as lamplight.
- Corrupted Amber `#FF8C00` is maximally saturated orange — it *cannot* be confused with warm environmental light once the distinction is understood, but in isolation it can look deceptively "warm."
- **The mandatory test:** If Corrupted Amber could be replaced by Soft Gold in the same composition without visual disruption, it is being used incorrectly. Corrupted Amber must always carry an edge of wrongness — it does not comfort.

**Outline Width Standard — Canonical: 3px (Cycle 7)**

The standard Corrupted Amber outline for Byte's silhouette is **3 visual pixels** at production resolution (1920×1080). This resolves the prior inconsistency where GL-07 stated "2px" while implementations used 3–5px at different resolutions.

- **Canonical width:** 3px at 1920×1080
- **At 960×540 thumbnail/preview:** render at 2px (scale proportionally)
- **`draw_amber_outline()` `width` / `offset` parameter:** The `width` parameter (in `style_frame_generator.py`) and the `width` parameter (in `style_frame_01_rendered.py`) both control the number of concentric offset ellipse passes. Each pass = 1 visual pixel of outline thickness. **Set `width=3` for production renders.** Set `width=2` for thumbnail/preview renders.

Do not use 4px or 5px. These produce a halo rather than a clean outline and compete with the character's internal color story.

**Approved Uses (exhaustive):**
1. **Byte's silhouette outline (3px stroke, canonical) when the cyan-dominant threshold is met.** This is the figure-ground protection rule. Apply the Corrupted Amber outline **only when** Electric Cyan (`#00F0FF`) and Byte Teal (`#00D4E8`) together exceed **35% of the visible background color area** in the frame around Byte. This threshold is the governing condition — the outline is a functional tool, not a decorative default. It must not appear in warm-dominant scenes (e.g., Key 01-type interiors) where the narrative purpose ("corruption warning signal") would be violated. See also GL-01b (Byte Teal). **Cycle 6 revision:** Prior notes stating the outline "must appear in every rendered image" have been corrected — that blanket mandate contradicted the threshold rule. The threshold rule governs. The code in `style_frame_generator.py` has been updated to apply the outline only in cyan-dominant frames (Frame 01 and Frame 02). Frame 03 (UV Purple-dominant, not cyan-dominant) does not apply the outline per the style_frame_03 specification.
2. **Corrupted Real World objects in the Glitch Layer.** Objects crossing the boundary (mailboxes, signs, furniture fragments) shimmer with Corrupted Amber at their edges — they are mid-transformation. The amber is the visual marker that they *belong* to the Real World but are being overwritten.
3. **Glitch Layer interface warning states.** A first-level warning pulse (amber) before escalating to Hot Magenta danger signal. The sequence is: Corrupted Amber (caution) → Hot Magenta (danger) → never skip steps.
4. **"Near-corruption" glow on Real World objects.** When a Real World object is *about to* be glitch-corrupted — in the moments before the full event — it may glow faintly amber. This is the final warn state before transformation.

**Prohibited Uses:**
- **Do NOT use as a warm environmental light color.** It is not Soft Gold and must not substitute for it in warm Real World lighting.
- **Do NOT apply to human skin or costume fills.** Its orange quality reads as toxic on skin.
- **Do NOT use in safe, calm Real World scenes** (Key 01-type scenes) unless a specific story event requires a corruption warning in that scene.
- **Do NOT use on Real World objects that are NOT being corrupted.** A warm brick wall is not Corrupted Amber — it is Terracotta. Reserve Corrupted Amber for the transition state only.
- **Do NOT mix with Soft Gold in the same composition** unless the narrative specifically requires the contrast between "safe warmth" and "wrong warmth" — this is a strong emotional beat and must be intentional.

**Cycle 6 Production Note:** The Corrupted Amber outline is governed exclusively by the 35% threshold rule (see Approved Use #1 above). The prior Cycle 5 note stating the outline "must appear in every rendered image" has been **superseded and removed** — it contradicted the threshold condition and created specification-implementation inconsistencies. The current rule: apply the outline programmatically via `draw_amber_outline()` in `style_frame_generator.py` **only when the 35% cyan-dominant threshold is met**. Frame 01 and Frame 02 meet this threshold. Frame 03 (UV Purple-dominant ambient) does not — the outline call has been removed from `generate_frame03()`. This is the single authoritative statement of the rule.

---

### GL-07a — Corrupted Amber Shadow
- **Hex:** `#A84C00`
- **RGB:** 168, 76, 0
- **Role:** Shadow companion to Corrupted Amber; shadow side of corrupted/transitioning objects
- **Use-case notes:** Keeps the "wrongness" of Corrupted Amber active in shadow. A deep orange-brown that never reads as comfortably warm.

---

### GL-08 — Void Black
- **Hex:** `#0A0A14`
- **RGB:** 10, 10, 20
- **Role:** The absolute dark value of the show; digital void backgrounds; corruption core; deepest shadow inside the Glitch Layer
- **Shadow companion:** `#050508` (Below-Void-Black — see exception note)
- **Use-case notes:** Per the style guide, this is the darkest value allowed — never pure black (#000000). The slight blue-violet undertone (note the subtle lift in the blue channel) prevents it from reading as "dead" and instead reads as "deep space" or "the void of digital absence." Large-area fills in the Glitch Layer, the interior of corrupted objects, the negative space around floating platforms. Also used where the style guide calls for "deep cocoa" in characters adapted for the Glitch Layer — the warmer #3B2820 is too cozy for digital darkness.
- **Pairs with:** #00F0FF, #FF2D6B, #39FF14 (all read as pure neon against this), #7B2FBE (deep dark harmony)
- **Avoid using:** In Real World daylight scenes — use Deep Cocoa (#3B2820) instead. Reserve Void Black for the Glitch Layer and extreme nighttime/corruption scenes.

---

### GL-08a — Below-Void-Black
- **Hex:** `#050508`
- **RGB:** 5, 5, 8
- **EXCEPTION NOTE — WHY THIS EXISTS:** This value was cited in Cycle 1 feedback as violating the system minimum of `#0A0A14`. The system minimum applies to FILLS and LARGE AREAS. `#050508` is a permitted exception for two specific micro-contexts only:
  1. Byte's deepest physical crevices (the absolute interior shadow on his Void Black body, where the surface turns inward and the light cannot reach)
  2. The void abyss beneath floating Glitch Layer platforms (the "below" of the world — the floor of the void, viewed from above, should be darker than the void itself to create a sense of depth and gravity)
  In both cases, `#050508` covers no more than 2-3% of any single frame's area. It must never be used as a large fill, a line color, or a background. If any other use is proposed, use `#0A0A14` instead and do not add new uses of `#050508` without Art Director approval.
- **Role:** Absolute crevice depth on Void Black forms; abyss floor beneath Glitch Layer platforms
- **Shadow companion:** N/A — this is the absolute minimum value in the show.

---

### Glitch Layer — Depth Tiers

*Rendering constructs derived from canonical GL swatches. These are NOT standalone palette swatches — they exist only inside `bg_glitch_layer_frame.py` (and related tools) to implement the mandatory 3-value-tier depth system for Glitch Layer platforms. All values derive from canonical entries above. Documented in Cycle 10 per Naomi Bridges C9-1 audit.*

| Constant | RGB | Hex (approx.) | Derivation | Depth Tier |
|---|---|---|---|---|
| `NEAR_COLOR` | 0, 240, 255 | #00F0FF | GL-01 ELEC_CYAN — unchanged | NEAR |
| `NEAR_SHADOW` | 0, 168, 180 | #00A8B4 | GL-01a DEEP_CYAN — unchanged | NEAR |
| `NEAR_EDGE` | 180, 255, 255 | #B4FFFF | GL-01 ELEC_CYAN brightened +30% toward white | NEAR |
| `MID_COLOR` | 10, 72, 120 | #0A4878 | GL-06 DATA_BLUE desaturated 60% and darkened 53% | MID |
| `MID_SHADOW` | 6, 40, 72 | #062848 | MID_COLOR darkened a further ~44% | MID |
| `MID_EDGE` | 20, 110, 160 | #146EA0 | MID_COLOR lightened ~53% | MID |
| `FAR_COLOR` | 0, 26, 40 | #001A28 | GL-08 VOID_BLACK shifted +cyan and darkened | FAR |
| `FAR_SHADOW` | 0, 14, 22 | #000E16 | FAR_COLOR darkened ~46% | FAR |
| `FAR_EDGE` | 0, 40, 55 | #002837 | FAR_COLOR lightened ~54% | FAR |
| `GHOST_COLOR` | 0, 28, 38 | #001C26 | GL-08a BELOW_VOID shifted +cyan — ghost platform fill | GHOST (void) |
| `GHOST_EDGE` | 0, 48, 62 | #00303E | GHOST_COLOR lightened — ghost platform edge | GHOST (void) |
| `AURORA_CYAN_BLEED` | 0, 160, 220 | #00A0DC | GL-01 ELEC_CYAN desaturated and darkened ~14% — aurora band D | Aurora |

**Usage rules:**
- NEAR tier uses full-brightness GL-01 family: these platforms must read at maximum value contrast against the void.
- MID tier desaturates and darkens DATA_BLUE to create a clear middle step. Must never overlap in perceived brightness with NEAR or FAR.
- FAR tier is near-void: platforms are barely distinguishable from VOID_BLACK. They register only as silhouettes at distance.
- GHOST and AURORA values are purely procedural — never use as fills on named surfaces.
- `AURORA_CYAN_BLEED` appears only as a sinusoidal per-row draw.line overlay in the aurora pass — not as a solid color anywhere.

---

## SECTION 3 — CHARACTER COLOR SPECIFICATIONS

These are the definitive, locked color specifications for the three main characters. Deviation from these values requires sign-off from the Art Director.

**Rule:** All character colors must be more saturated than any background they appear in front of. This is enforced, not suggested.

---

### CHARACTER: LUMA

*Luma is the warm heart of the show. Her palette is anchored in ambers, soft oranges, and a pop of electric cyan — the digital world she is drawn toward. She should always read as approachable, energetic, and curious.*

**SKIN**
| Zone | Hex | Notes |
|---|---|---|
| Base fill | `#C4A882` | Warm tan — per RW-10 |
| Shadow (warm light) | `#8C5A38` | Skin shadow — per RW-10b |
| Highlight | `#E8D4B0` | Per RW-10a |
| Cool-lit shadow (night/glitch scenes) | `#7A5A7A` | Per RW-10c |
| Blush | `#E07A6A` | Simple oval on cheeks; warm coral |

**HAIR**
| Zone | Hex | Notes |
|---|---|---|
| Base fill | `#3B2820` | Deep Cocoa |
| Highlight | `#6B4A3A` | Single highlight stripe |
| Sheen pop | `#9A6A50` | Optional; hero close-ups only |

**HOODIE (Primary)**
| Zone | Hex | Notes |
|---|---|---|
| Main fill | `#E8703A` | Bright orange — Luma's signature color |
| Shadow | `#B84A20` | Darker orange-red shadow |
| Pocket/hem accent | `#FAF0DC` | Warm cream detail |
| Pixel grid pattern | `#00F0FF` | Electric Cyan — bridge to digital world |
| Pixel grid shadow | `#00A8B4` | Deep Cyan for pixel pattern in shadow areas |

**JEANS**
| Zone | Hex | Notes |
|---|---|---|
| Base fill | `#3A5A8C` | Medium blue-indigo |
| Shadow | `#263D5A` | Deep blue-grey |
| Highlight | `#5A80B4` | Lighter blue for lit areas |

**SHOES**
| Zone | Hex | Notes |
|---|---|---|
| Main | `#FAF0DC` | Warm cream canvas |
| Sole | `#3B2820` | Deep cocoa rubber sole |
| Laces | `#00F0FF` | Electric Cyan |

**EYES**
| Zone | Hex | Notes |
|---|---|---|
| Iris | `#4A7A4A` | Warm green |
| Pupil | `#0A0A14` | Near-void black |
| Highlight | `#F0F0F0` | Static white dot |
| Sclera | `#FAF0DC` | Warm cream |

---

### CHARACTER: COSMO

*Cosmo is Luma's cautious, overthinking best friend. His palette is cooler, more reserved — dusty lavenders and muted blues.*

**SKIN**
| Zone | Hex | Notes |
|---|---|---|
| Base fill | `#C4A882` | Same base as Luma |
| Shadow | `#8C5A38` | Standard skin shadow |
| Highlight | `#E8D4B0` | Same as Luma |
| Cool shadow | `#7A5A7A` | Same cool-lit shadow as Luma |
| Blush | `#C47A6A` | Slightly cooler blush |

**HAIR**
| Zone | Hex | Notes |
|---|---|---|
| Base fill | `#7A5A38` | Medium warm brown |
| Shadow | `#5A3A20` | Dark brown shadow |
| Highlight | `#A87850` | Warm honey highlight |

**JACKET (Signature)**
| Zone | Hex | Notes |
|---|---|---|
| Main fill | `#A89BBF` | Dusty Lavender |
| Shadow | `#5C4A72` | Shadow Plum — per RW-09 |
| Highlight | `#C8BFD8` | Lighter lavender |
| Collar detail | `#FAF0DC` | Warm cream collar |

**SHIRT (under jacket)**
| Zone | Hex | Notes |
|---|---|---|
| Main fill | `#FAF0DC` | Warm cream stripe |
| Stripe color | `#C75B39` | Terracotta stripes |

**PANTS**
| Zone | Hex | Notes |
|---|---|---|
| Base fill | `#5A6A4A` | Muted olive green |
| Shadow | `#3A4A2A` | Dark olive shadow |

**GLASSES**
| Zone | Hex | Notes |
|---|---|---|
| Frames | `#3B2820` | Deep Cocoa |
| Lens glare | `#F0F0F0` | Static white reflection lines |

**EYES (behind glasses)**
| Zone | Hex | Notes |
|---|---|---|
| Iris | `#6A4A3A` | Warm brown |
| Sclera | `#FAF0DC` | Warm cream |

---

### CHARACTER: BYTE

*Byte is a reformed Glitchkin — made entirely of digital stuff, living in the warm Real World.*

**BODY**
| Zone | Hex | Notes |
|---|---|---|
| Base fill | `#00D4E8` | **Byte Teal — per GL-01b (Cycle 5 revision).** Byte's primary body fill for all flat surfaces (body core, limbs). Replaces former Void Black fill. |
| Silhouette / crevice line | `#0A0A14` | Void Black — used ONLY for Byte's outline stroke and deepest interior crevices. NOT a body fill color. |
| Body glow (inner) | `#00A8B4` | Deep Cyan inner glow |
| Surface highlight | `#00F0FF` | Electric Cyan lit edges — preserves identity link to glitch energy |
| Bright specular | `#F0F0F0` | Static White sharp pops |
| Shadow depth | `#050508` | See Section 2 exception note — crevice use only |

**MARKINGS**
| Zone | Hex | Notes |
|---|---|---|
| Circuit pattern | `#00F0FF` | Electric Cyan |
| Secondary pattern | `#2B7FFF` | Data Stream Blue |

**EYES**
| Zone | Hex | Notes |
|---|---|---|
| Normal eye glow | `#00F0FF` | Electric Cyan |
| Cracked eye glow | `#FF2D6B` | Hot Magenta |
| Eye highlight | `#F0F0F0` | Static White |

**MOUTH / EXPRESSION**
| Zone | Hex | Notes |
|---|---|---|
| Inner mouth | `#7B2FBE` | UV Purple |
| Teeth / data shards | `#F0F0F0` | Static White |

**LINE COLOR**
| Zone | Hex | Notes |
|---|---|---|
| Outline | `#0A0A14` | Void Black (merges with form) |
| Interior lines | `#00A8B4` | Deep Cyan |

---

## SECTION 4 — FORBIDDEN COLOR COMBINATIONS

These specific pairings are banned from use anywhere in the production. Each pairing causes a distinct visual or narrative problem.

---

### FORBIDDEN #1 — Acid Green text/line on Hot Magenta fill
- **Colors:** `#39FF14` on `#FF2D6B`
- **Why banned:** Maximum simultaneous contrast vibration. Both colors are at maximum saturation and near-complementary in hue (green vs. red-pink). The eye cannot simultaneously focus on both; they appear to shimmer and pulse in a genuinely uncomfortable way. Any text or important line rendered in this combination becomes illegible and causes viewer discomfort. Even as a decorative element, it reads as a production error rather than an artistic choice.
- **Exception:** Never.

---

### FORBIDDEN #2 — Electric Cyan on Muted Teal
- **Colors:** `#00F0FF` on `#5B8C8A`
- **Why banned:** These two colors are in the same hue family but drastically different in saturation. The high-saturation Electric Cyan placed on mid-saturation Muted Teal makes the Teal look like a failed version of the Cyan — it reads as a color mistake, not a design choice. It also undermines Muted Teal's role as an "analog" color (it starts to look like a dim version of a glitch color).
- **Exception:** Never as fill-on-fill. An Electric Cyan outline on a Teal-colored object is acceptable if the object outline has sufficient weight.

---

### FORBIDDEN #3 — Warm Cream background with Dusty Lavender text/line
- **Colors:** `#FAF0DC` with `#A89BBF`
- **Why banned:** Insufficient contrast. Both colors are light-valued and desaturated. Their contrast ratio falls below 3:1 — below accessibility standards and barely visible in print/screens with any brightness variation. Important information will disappear in this combination.
- **Exception:** Can be used decoratively for very large shapes (e.g., a lavender tinted cloud against a cream sky) where legibility is not required.

---

### FORBIDDEN #4 — Pure black (#000000) or pure white (#FFFFFF) anywhere
- **Colors:** `#000000`, `#FFFFFF`
- **Why banned:** Per the style guide. Pure black reads as dead and lifeless in this warm-palette show — it breaks the carefully maintained color temperature. Pure white creates harsh optical glare that breaks the slightly aged, analog-warmth quality of the show's visuals. These are absolutes: darkest value is `#0A0A14`, brightest value is `#FAF0DC` (warm) or `#F0F0F0` (neutral light).
- **Exception:** A single pure-white (#FFFFFF) specular pop — no larger than 3-4 pixels in production scale — is permitted once per major scene for the maximum-brightness glitch flash effect (e.g., when a portal opens). This is the only exception.

---

### FORBIDDEN #5 — Sage Green shadow on Hot Magenta
- **Colors:** `#7A9E7E` shadow zones on `#FF2D6B` primary fills
- **Why banned:** Red-pink and green are direct complements. When the Sage Green appears as the shadow tone on a Hot Magenta form, it creates a "Christmas color" effect — unintentional festive association that completely undercuts any tension or danger the Hot Magenta was meant to convey. The Corruption villain becoming accidentally cheerful is a narrative disaster.
- **Exception:** If the intent is genuine comedy/subversion of the Corruption, a controlled use could be discussed — but this requires explicit Art Director approval.

---

### FORBIDDEN #6 — Deep Cocoa line work on Void Black background
- **Colors:** `#3B2820` lines on `#0A0A14`
- **Why banned:** The warm brown line color is invisible against the dark near-black of the void. It provides zero contrast and makes character and object forms unreadable. In Glitch Layer scenes, lines must shift to Electric Cyan, Static White, or a contrasting glitch color. Deep Cocoa is a Real World line color and belongs only in Real World contexts.
- **Exception:** Can be used for deliberately hidden/camouflaged elements — e.g., a character blending into shadow — but the intent must be explicit in the brief.

---

### FORBIDDEN #7 — Skin Shadow (#8C5A38) used as a primary costume fill
- **Colors:** `#8C5A38` as a clothing or object fill (outside of skin)
- **Why banned:** This specific brownish-orange is visually associated with skin/flesh on the characters. If used as a clothing color or object fill, it creates an uncomfortable visual ambiguity — the object reads as flesh-colored, which is distracting in the best case and body-horror-adjacent in the worst. Other brown-adjacent colors (Rust Shadow #8C3A22, Warm Tan #C4A882) are distinguishable enough from the skin shadow to be usable in other contexts. This specific value is too close.
- **Exception:** Intentional gross-out gag animation, if scripted.

---

### FORBIDDEN #8 — Acid Green as a danger/storm/corruption effect color
- **Colors:** `#39FF14` in storm effects, corruption bursts, danger signals
- **Why banned:** Acid Green is semantically defined as "healthy glitch energy." Using it in danger-storm contexts (e.g., as pixel confetti in a glitch storm attack) creates a direct contradiction of its established meaning. If Acid Green appears in a danger scene, the audience reads "positive/healthy" at the same moment the narrative is trying to signal "threat/corruption." These are irreconcilable. Storm and corruption effects must use Hot Magenta (`#FF2D6B`), UV Purple (`#7B2FBE`), or Electric Cyan (`#00F0FF`) for their energy particles.
- **Exception:** Acid Green confetti is permitted in storm frames ONLY if it is specifically attributed to a Glitchkin character present in the scene (their markings shedding under storm energy). It must not appear as a freestanding storm effect particle.

---

### FORBIDDEN #9 — UV Purple as a Real World shadow tone
- **Colors:** `#7B2FBE` as shadow fill on Real World objects or characters in Real World scenes
- **Why banned:** UV Purple is specifically the digital void color — the shadow "between data." If it appears as a shadow tone in a Real World scene, it makes the scene read as digitally infected even when no glitch activity is scripted. The Real World shadow progression stops at Shadow Plum (`#5C4A72`). UV Purple begins where the Glitch Layer's shadow logic starts. Crossing this line bleeds the two worlds together unintentionally and undermines the visual language that makes the glitch intrusion feel meaningful.
- **Exception:** An explicit Glitch intrusion moment in a Real World scene — where the point is that a glitch shadow is falling on a real-world surface (a glitch portal casting its shadow, for example). This requires a specific brief note and Art Director approval. It is a visual event, not a default shadow choice.

---

### FORBIDDEN #10 — Warm Cream or Soft Gold as ambient fill in large-area interior scenes
- **Colors:** `#FAF0DC` or `#E8C95A` as 20%+ ambient fill on walls and room surfaces when the scene is not an active sunlit exterior
- **Why banned:** Sunlit Amber (`#D4923A`) has a specific "avoid as broad fill" caveat, but Soft Gold can also flatten into oversaturation if used as a dominant ambient wash on large room surfaces. More critically, if the ambient fill color is too saturated/bright for the scene's emotional intent (e.g., an intimate evening scene using 20% Sunlit Amber as ambient), it overrides the mood entirely — the golden warmth fights against intimacy and makes the scene feel like midday rather than evening. In emotional/quiet scenes, ambient fills must be desaturated: Warm Cream is the preferred large-area fill; Dusty Lavender for cool-ambient zones.
- **Exception:** In a directly sun-facing exterior daylight scene, Soft Gold as 15–18% of the palette is correct and expected. The prohibition applies to interior ambient fills and evening/intimate scenes.

---

---

## SECTION 6 — ENVIRONMENT / PROPS

Formally documented inline color values used in rendered scripts for recurring prop objects. These values were identified from `style_frame_01_rendered.py` during Cycle 7–8 audit. The couch is Luma's signature furniture and will recur in any home interior scene. The cable clutter is a deliberate prop motif — cables running along the floor are part of the Frame 01 composition language. Any new rendered home-interior script must map back to these entries or add new ones here.

**Source script:** `/home/wipkat/team/output/tools/style_frame_01_rendered.py`

---

### PROP-01 — Couch Seat (Warm Reddish-Brown)
- **Hex:** `#6B3018`
- **RGB:** 107, 48, 24
- **Role:** Primary fill for Luma's living-room couch seat cushion. Recurring prop — appears in any scene set in Luma's home.
- **Shadow companion:** `#501E0E` (deeper warm shadow — seam line and under-cushion)
- **Use-case notes:** A deep, warm reddish-brown that reads as aged, comfortable upholstery. Not a primary palette color but must be consistent across all home-interior frames. Sits harmonically with the warm amber wall tones of Frame 01. Established by Naomi Bridges critique (Cycle 7) as requiring palette registration. Shadow line value `(80, 36, 14)` ≈ `#50240E` used for cushion seam.
- **Pairs with:** PROP-02 (couch back cushion), PROP-03 (couch arm), RW-02 Soft Gold (lamp rim highlight)
- **Avoid using:** As a skin-adjacent fill — too dark and saturated-red.

---

### PROP-02 — Couch Back Cushion
- **Hex:** `#803C1C`
- **RGB:** 128, 60, 28
- **Role:** Fill for Luma's couch back cushion. Slightly lighter and more orange-shifted than the seat.
- **Shadow companion:** `#50280E` (outline and shadow pass — used in code as (80, 40, 16))
- **Use-case notes:** The back cushion receives more direct warm lamp light than the seat, producing this slightly brighter reddish-brown. The three-tone couch system (PROP-01 seat / PROP-02 back / PROP-03 arm) creates believable material depth without complex shading. All three must stay within the same reddish-brown family.
- **Pairs with:** PROP-01, PROP-03

---

### PROP-03 — Couch Arm Rest
- **Hex:** `#73341A`
- **RGB:** 115, 52, 26
- **Role:** Fill for Luma's couch arm rest. Mid-value between seat and back cushion.
- **Shadow companion:** `#50240E` (arm rest outline — same as PROP-01 shadow, (80, 36, 14))
- **Use-case notes:** The arm rest faces the camera front-on in Frame 01 and receives slightly less direct lamp light than the back cushion. Its mid-value preserves couch unity. Together PROP-01/02/03 form the complete couch material system.
- **Pairs with:** PROP-01, PROP-02

---

### PROP-04 — Cable Warm Bronze
- **Hex:** `#B48C50`
- **RGB:** 180, 140, 80
- **Role:** Foreground cable clutter prop color — warm bronze/copper cable. Used in both monitor desk cables and foreground floor cable tangle.
- **Shadow companion:** `#8C6430` (darker bronze for cable underside or loop shadow)
- **Use-case notes:** The warm bronze cable color in Frame 01 cable clutter. Reads as an old analog cable or copper-sheathed data line — deliberately warm against the cyan-heavy monitor wall. Produces visual warmth in what would otherwise be a pure cold-tech composition. Must remain distinct from the show's primary warm colors (Soft Gold, Sunlit Amber) — it is a prop tone, not a key light color. This cable appears in both the monitor desk bundle (`cable_colors`) and foreground floor tangle (`fg_cables`).
- **Pairs with:** PROP-05 (Data Cable Cyan), GL-01 (Electric Cyan), GL-03 (Hot Magenta)
- **Avoid using:** As a character warm-zone fill — too muted for the character lighting system.

---

### PROP-05 — Cable Data Cyan (Mid-Value)
- **Hex:** `#00B4FF`
- **RGB:** 0, 180, 255
- **Role:** Foreground cable clutter prop color — a mid-value blue-cyan cable suggesting data transmission lines. Distinct from Electric Cyan (GL-01, `#00F0FF`) — notably darker and more blue-shifted.
- **Shadow companion:** `#0080C0` (deeper blue for cable shadow side)
- **Use-case notes:** The data-transmission cable color in Frame 01 cable clutter. Its blue-shifted quality (more blue than cyan) distinguishes it from GL-01's pure cyan and prevents confusion with Byte's aura. It reads as a "data cable" rather than a "glitch energy cable." The lower value creates depth in the cable pile and prevents the foreground from competing with the screen's Electric Cyan. This cable appears in both the monitor desk bundle and the foreground floor tangle.
- **Distinction from GL-01:** RGB is (0, 180, 255) vs GL-01 (0, 240, 255). Green channel is 60 points lower, making this noticeably more blue and less pure-cyan. Do not substitute GL-01 for PROP-05 — the brightness difference is essential for spatial layering.
- **Pairs with:** PROP-04 (Cable Warm Bronze), GL-01 (Electric Cyan)
- **Avoid using:** As Byte's body fill or aura — that is GL-01b exclusively.

---

### PROP-06 — Cable Magenta-Purple
- **Hex:** `#C850C8`
- **RGB:** 200, 80, 200
- **Role:** Foreground cable clutter prop color — a magenta-purple cable suggesting a mixed-signal or corrupted data line.
- **Shadow companion:** `#8C2890` (deep magenta-purple for cable shadow/underside)
- **Use-case notes:** The magenta-purple cable in Frame 01's foreground floor tangle. It sits between Hot Magenta (GL-03, `#FF2D6B`) and UV Purple (GL-04, `#7B2FBE`) in both hue and saturation — purposely less intense than both, so it does not compete with either narrative glitch color. Its presence in the cable pile suggests "corrupted signal infrastructure" without triggering the danger-reading of full Hot Magenta. Used only in the foreground cable tangle (single thin line, 1px weight); not in the monitor desk cables.
- **Distinction from GL-03 Hot Magenta:** RGB (200, 80, 200) has a much higher blue channel (200 vs 107) than Hot Magenta (255, 45, 107) — it reads purple-magenta, not pink-red-magenta.
- **Distinction from GL-04 UV Purple:** RGB (200, 80, 200) is substantially lighter and more saturated in red — it reads as a prop accent, not a deep-space void color.
- **Pairs with:** PROP-04, PROP-05, GL-01, GL-03
- **Avoid using:** As a large-area fill or narrative accent — its identity is prop/clutter. If used at large scale it competes with both Hot Magenta and UV Purple.

---

### PROP-07 — Cable Neutral Plum
- **Constant:** `CABLE_NEUTRAL_PLUM`
- **Hex:** `#504064`
- **RGB:** 80, 64, 100
- **Role:** Aged neutral cable in foreground floor tangle — desaturated plum-grey that reads as an aged cable with cool ambient tinting. Replaces the former `(100, 100, 100)` neutral grey (flagged by Naomi Bridges, Cycle 7).
- **Deprecation note:** The `(100, 100, 100)` neutral grey it replaces is formally retired. Neutral mid-grey has no color character in this show's palette — neither warm (Real World) nor cool-saturated (Glitch).
- **Derivation:** RW-09 Shadow Plum DNA (`#5C4A72`) desaturated and darkened; connects to the lavender ambient in the scene. Visually coherent in the show's palette without triggering any narrative signal.
- **Use-case notes:** Single thin cable in the foreground floor tangle (1px weight). This is a prop support color — it must not compete with the narrative glitch cable colors (ELEC_CYAN, HOT_MAGENTA) or the primary warm cable (PROP-04 Cable Warm Bronze). Its purpose is to add density/visual complexity to the floor clutter without drawing the eye.
- **Pairs with:** PROP-04, PROP-05, PROP-06 (cable clutter companions)
- **Avoid using:** As a large-area fill, shadow color, or character color — it has no narrative role outside the cable clutter prop context.
- **Added/finalized:** Sam Kowalski — Cycle 9 (2026-03-29). Constant `CABLE_NEUTRAL_PLUM` added to `style_frame_01_rendered.py` module level; inline `(80, 64, 100)` tuple at line ~477 replaced with named constant.

---

*Section 6 added — Sam Kowalski — Cycle 8 (2026-03-29). Sources: style_frame_01_rendered.py inline audit per Naomi Bridges Cycle 7 critique.*

---

## SECTION 5 — CHARACTER RENDERING COLORS — LUMA

Formal documentation of inline color values used in `style_frame_01_rendered.py`. These values were identified by Naomi Bridges (Cycle 7 critique) as undocumented. All are now canonical palette entries. Alex's rendered script should reference these by name going forward.

**Source script:** `/home/wipkat/team/output/tools/style_frame_01_rendered.py`

---

### CHAR-L-01 — Luma Skin Base (Lamp-Lit)
- **Hex:** `#C8885A`
- **RGB:** 200, 136, 90
- **Role:** Luma's primary skin fill under warm lamp-dominant lighting (Frame 01 three-light setup). This is the base tone for all skin-facing-lamp surfaces.
- **Derivation:** Warmed Tan (`DRW-04` equivalent) shifted toward amber-orange under the Soft Gold lamp key; approximately 2 stops below the highlight.
- **Scene use:** Style Frame 01 (lamp-lit interior). Luma facing left, toward warm lamp side. All front-facing skin surfaces in Frame 01 composition.
- **Shadow companion:** `#A86838` (Luma Skin Shadow — see CHAR-L-03)
- **Highlight companion:** `#E8B888` (Luma Skin Highlight — see CHAR-L-02)
- **Avoid using:** In Glitch Layer or cyan-dominant scenes — use the existing DRW-01 Cyan Skin (`#7ABCBA`) for cool-lit skin surfaces.

---

### CHAR-L-02 — Luma Skin Highlight (Lamp-Lit)
- **Hex:** `#E8B888`
- **RGB:** 232, 184, 136
- **Role:** Luma's brightest skin catch-light under warm lamp key; forehead, cheekbone, tip of nose, upper lip.
- **Derivation:** CHAR-L-01 skin base shifted toward the Soft Gold lamp color (`#E8C95A`); the lit surface bleaches toward the light source.
- **Scene use:** Style Frame 01, lamp-side of Luma's face and hands. Hero close-up; sparingly on mid-shot.
- **Parent:** CHAR-L-01 (Luma Skin Base)
- **Avoid using:** As a body fill or ambient tone — this is a specular highlight value only.

---

### CHAR-L-03 — Luma Skin Shadow (Lamp-Lit)
- **Hex:** `#A86838`
- **RGB:** 168, 104, 56
- **Role:** Luma's shadow tone on skin under warm lamp setup; underside of chin, neck, under-eye shadow, palm of reaching hand.
- **Derivation:** CHAR-L-01 base shifted toward Rust Shadow; the shadow deepens and warms slightly (the lamp's color bleeds into shadow transitions in a warm interior).
- **Scene use:** Style Frame 01. All shadow-side skin surfaces on the lamp-lit character.
- **Parent:** CHAR-L-01 (Luma Skin Base)
- **Distinction from RW-11 Skin Shadow (`#8C5A38`):** CHAR-L-03 `#A86838` is warmer and lighter (R:168 vs 140, G:104 vs 90, B:56 same). RW-11 is the neutral-light skin shadow. CHAR-L-03 is the lamp-biased skin shadow for Frame 01 only. Do not swap them across scene contexts.

---

### CHAR-L-04 — Luma Hoodie Shadow Variant (Lamp-Lit)
- **Hex:** `#B84A20`
- **RGB:** 184, 74, 32
- **Role:** Shadow tone on Luma's orange hoodie under warm lamp lighting, Frame 01 interior setup. Deeper, slightly desaturated relative to the hoodie base orange.
- **Derivation:** Hoodie base (`#E8703A`) shifted toward Rust Shadow at the shadow side.
- **Scene use:** Style Frame 01. Under-arm fold, hoodie hem shadow, anywhere the hoodie surface turns away from the lamp.
- **Note:** This value also appears in the Luma character spec HOODIE table (Shadow row = `#B84A20`). The entries are consistent. This section provides scene-specific documentation of its lamp-lit Frame 01 usage context.
- **Avoid using:** As a primary hoodie fill — it is strictly a shadow companion to `#E8703A`.

---

### CHAR-L-05 — Luma Jeans Base
- **Hex:** `#3A5A8C`
- **RGB:** 58, 90, 140
- **Role:** Luma's jeans primary fill; medium blue-indigo denim. Used in both `style_frame_generator.py` and `style_frame_01_rendered.py`.
- **Derivation:** Mid-value blue-indigo, slightly desaturated relative to Data Stream Blue. Reads as worn denim in warm interior light.
- **Scene use:** All style frames where Luma appears. Consistent across lighting conditions — the jeans are relatively stable in hue because their mid-value absorbs light variation without dramatic hue shift.
- **Shadow companion:** `#263D5A` (deep blue-grey; see Luma character spec JEANS table)
- **Highlight companion:** `#5A80B4` (lighter blue for lit areas; see Luma character spec JEANS table)
- **Note:** This value appears in both the Luma character spec JEANS table and both generator scripts. The value is now formally registered here as a GL/DRW-adjacent production color to prevent drift between scripts.
- **SF03 UV-ambient note:** In SF03 ("The Other Side"), Luma's jeans are rendered as `JEANS_BASE = (38, 61, 90)` = `#263D5A`. This matches the existing CHAR-L-05 shadow companion — the jeans appear at their shadow value under UV Purple ambient light. This is an environment-specific rendering, not a character color change. **Do not use `#263D5A` as the canonical jeans base in neutral or warm-lit scenes.** Future Glitch Layer scenes: use `#263D5A` only when UV Purple ambient is the dominant light source. All other scenes: use canonical `#3A5A8C`.

---

### CHAR-L-06 — Luma Blush (Warm, Dominant)
- **Hex:** `#DC5032`
- **RGB:** 220, 80, 50
- **Role:** High-intensity blush, outer left cheek. Used for Reckless Excitement expression in Frame 01. Warm orange-red — communicates hot embarrassment or excitement, not a delicate flush.
- **Scene use:** Style Frame 01, `draw_luma_head()` — left cheek ellipse (dominant side).
- **Note:** Applied as the outer blush ring. The center is softened by an overlay pass of CHAR-L-01 skin base to prevent full opacity. This is an expression-performance color, not a generic character base color.

---

### CHAR-L-07 — Luma Blush (Warm, Secondary)
- **Hex:** `#D04830`
- **RGB:** 208, 72, 48
- **Role:** High-intensity blush, outer right cheek. Slightly cooler/darker than CHAR-L-06 to give subtle bilateral asymmetry to the expression.
- **Scene use:** Style Frame 01, `draw_luma_head()` — right cheek ellipse.
- **Note:** See CHAR-L-06. Same application notes apply. The 12-point red-channel difference from CHAR-L-06 is intentional — it gives the blush a natural imperfect quality rather than a stamped-on symmetrical look.

---

### CHAR-L-09 — Luma Shoe Canvas
- **Constant (code):** `WARM_CREAM` (RW-01, module constant — no alias needed)
- **Hex:** `#FAF0DC`
- **RGB:** 250, 240, 220
- **Role:** Luma's shoe upper/canvas — warm cream off-white. Same value as RW-01. References the RW-01 module constant directly; do not create a separate shoe-specific alias.
- **Use-case notes:** The cream canvas shoe reads as a slightly grubby off-white sneaker — it has aged warmth, not clinical white. The cream quality also matches the show's no-pure-white rule. Pairs with CHAR-L-10 (Sole) and ELEC_CYAN laces.
- **Pairs with:** CHAR-L-10 (Deep Cocoa sole), ELEC_CYAN (laces — the deliberate glitch-world intrusion in her warm wardrobe)
- **Added:** Sam Kowalski — Cycle 9 (per Naomi Bridges Cycle 8 feedback: shoe colors must be findable in Section 5)

---

### CHAR-L-10 — Luma Shoe Sole
- **Constant (code):** `DEEP_COCOA` (RW-12, module constant — no alias needed)
- **Hex:** `#3B2820`
- **RGB:** 59, 40, 32
- **Role:** Luma's shoe rubber sole — deep cocoa brown. Same value as RW-12 / line color. References the DEEP_COCOA module constant directly; do not create a separate sole-specific alias.
- **Use-case notes:** The deep cocoa sole visually anchors the shoe to the ground, gives it weight, and echoes the character's universal line color — making the sole read as a solid design element rather than an afterthought. The warm-dark sole against the cream upper is a clean two-tone graphic read at any scale.
- **Pairs with:** CHAR-L-09 (canvas upper)
- **Added:** Sam Kowalski — Cycle 9 (per Naomi Bridges Cycle 8 feedback)

---

### CHAR-L-11 — Luma Hoodie Pixel (Warm-Lit Activation)
- **Constant (code):** `SOFT_GOLD` (RW-02 alias — `#E8C95A`)
- **Hex:** `#E8C95A`
- **RGB:** 232, 201, 90
- **Role:** Hoodie pixel grid accents on the lamp-lit (left) side of Luma's torso — warm-side discrete pixel activation
- **Narrative:** Warm world touching digital identity pattern; bridge between real-world Luma and Byte's domain. The pixel pattern on Luma's hoodie carries both her Real World warmth (Soft Gold, lamp-lit) and her connection to the Glitch Layer (Electric Cyan, neutral/cold).
- **Scene use:** SF01 — lamp-lit (left-side) hoodie pixel accents only
- **Constraint 1:** Use ONLY when a warm lamp source is present AND dominant on that face/side. Neutral-lit and cold-lit scenes use GL-01 Electric Cyan (`#00F0FF`) for all hoodie pixel accents. *(Cycle 30 correction: prior text cited `#00D4E8` which is GL-01b Byte Teal — that is Byte's body fill, not the hoodie pixel color. Correct value is GL-01 `#00F0FF`.)*
- **Constraint 2:** Warm-dominant scenes only. If the scene key is cyan, UV, or neutral, all hoodie pixel accents revert to GL-01.
- **Constraint 3:** Lamp-lit hoodie pixel accents only — this is not a fill color, a shadow color, or a large-area tone. It is strictly the small discrete pixel-grid accent elements on the hoodie surface under warm lamp key.
- **Production note:** The SF01 v003 Pillow script uses a continuous gradient (HOODIE_ORANGE → HOODIE_CYAN_LIT) rather than a discrete pixel grid. CHAR-L-11 defines the production spec (OpenToonz pixel-grid activation) — the Pillow approximation is noted as a limitation of the raster preview.
- **Cross-reference:** CHAR-L-09 (shoe canvas, unrelated), GL-01 (`#00F0FF`) for pixel accents in neutral/cold lighting, RW-02 (`#E8C95A`) for the canonical Soft Gold entry
- **Added:** Sam Kowalski — Cycle 14 (2026-03-30), per Alex Chen Art Director confirmation (2026-03-30)

---

### CHAR-L-08 — Luma Hoodie Underside (Lavender Ambient)
- **Constant (code):** `HOODIE_AMBIENT`
- **Hex:** `#B36250`
- **RGB:** 179, 98, 80
- **Role:** Fill color for the underside of Luma's hoodie hem — the surface that faces down, away from both the lamp and the monitor wall. Under the three-light setup in Frame 01, this surface receives ONLY the lavender ambient fill (no direct lamp key, no cyan key).
- **Lighting context:** Three-light Frame 01 setup: LEFT = Soft Gold lamp (HOODIE_ORANGE side), RIGHT = Electric Cyan monitor (HOODIE_CYAN_LIT side), AMBIENT = Dusty Lavender fill. The hoodie underside faces down toward the floor — it receives the ambient fill only, trending cool (lavender/plum), not warm.
- **Derivation:** `HOODIE_SHADOW` (`#B84A20`, RGB 184, 74, 32) blended with `DUSTY_LAVENDER` (`#A89BBF`, RGB 168, 155, 191) at 70/30 ratio. Full arithmetic:
  - R: 184 × 0.7 + 168 × 0.3 = 128.8 + 50.4 = **179**
  - G:  74 × 0.7 + 155 × 0.3 =  51.8 + 46.5 =  **98**
  - B:  32 × 0.7 + 191 × 0.3 =  22.4 + 57.3 =  **80** (rounded from 79.7)
  - Result: RGB(179, 98, 80) = `#B36250`
  - Correction note (Cycle 10): The previous value `#B06040` (176, 96, 64) had an incorrect blue channel — 16 points below what 70/30 actually yields (80 vs. 64). The discrepancy made the underside warmer and less lavender-influenced than the formula states. `#B36250` is the arithmetically correct result. Per Naomi Bridges C9-5.
- **Aesthetic note:** At RGB(179, 98, 80) the hoodie underside reads clearly as orange hoodie fabric. The blue channel of 80 introduces a small but perceptible lavender influence — correct for a surface lit only by DUSTY_LAVENDER ambient fill.
- **Scene use:** Style Frame 01, `draw_luma_body()` — hoodie hem underside polygon.
- **Note:** The interim `SHADOW_PLUM` value used in Cycle 8 has been replaced. Shadow Plum lacked orange component and read as a separate architectural surface rather than a hoodie fabric. `HOODIE_AMBIENT` correctly preserves hoodie material identity under cool light.
- **Added:** Sam Kowalski — Cycle 8 (2026-03-29), per Cycle 8 task assignment.
- **Finalized:** Cycle 9 — `HOODIE_AMBIENT` constant added to `style_frame_01_rendered.py`.
- **Corrected:** Cycle 10 — hex updated from `#B06040` (176,96,64) to `#B36250` (179,98,80); derivation arithmetic verified. Naomi Bridges C9-5.

---

### CHAR-L Hoodie Warmth Guarantee Table

**Production rule:** Every palette entry for Luma's hoodie system must remain "unambiguously warm" — R must be the dominant channel (within soft_tolerance). This table is the machine-readable source for `LTG_TOOL_palette_warmth_lint_v004.py` and the CI warmth gate. Entries are listed here in addition to their prose definitions above. If a value changes in the prose section, it must also be updated here.

| Code | Name | Hex | RGB | Notes |
|---|---|---|---|---|
| CHAR-L-04 | Luma Hoodie Shadow (Lamp-Lit) | `#B84A20` | (184, 74, 32) | Shadow companion to HOODIE_ORANGE. R>G>B — warm guarantee. See prose entry above. |
| CHAR-L-08 | Luma Hoodie Underside (Lavender Ambient) | `#B36250` | (179, 98, 80) | Ambient-lit underside. 70/30 blend of HOODIE_SHADOW + DUSTY_LAVENDER. R>G>B — warm guarantee preserved despite lavender influence. |
| CHAR-L-11 | Luma Hoodie Pixel (Warm-Lit Activation) | `#E8C95A` | (232, 201, 90) | Warm-lit pixel accents only. Alias of RW-02 Soft Gold. R>G>B — warm guarantee. |

*Cycle 36 addition (Sam Kowalski — 2026-03-30): CHAR-L hoodie warmth guarantee table added. These entries are now machine-checked by `LTG_TOOL_palette_warmth_lint_v004.py` with prefix "CHAR-L" when `ltg_warmth_guarantees.json` is active. Only these three hoodie-specific entries appear in table format; all other CHAR-L entries (skin, jeans, shoes) remain in prose format and are intentionally excluded from the warmth lint (jeans = blue, shoes = near-white — not warm-guaranteed).*

---

---

## SECTION 7 — SKIN COLOR SYSTEM

This section establishes the canonical skin tone system for all human characters on "Luma & the Glitchkin." It resolves the discrepancy identified by Fiona O'Sullivan (Cycle 8 critique) between `#C8885A` (Luma's lamp-lit skin in rendered scripts) and `#C4A882` (the master palette's universal skin base, RW-10).

---

### 7.1 — The Two-Tier Skin System

Human skin in this show operates on two tiers:

**Tier 1 — Canonical Neutral Base (RW-10):**
`#C4A882` (Warm Tan) is the canonical neutral-light skin base for all human characters. It is the value a painter uses when no specific lighting condition has been specified, and the value all scene-specific derived colors descend from. It appears in the Section 3 character specs for both Luma and Cosmo (both use `#C4A882` as their base in the character specification tables).

**Tier 2 — Scene/Lighting-Derived Skin (CHAR-L-xx / DRW-xx):**
When a character is rendered under a specific three-light setup, the base skin shifts. CHAR-L-01 (`#C8885A`) is Luma's skin base **under warm lamp-dominant lighting in Frame 01 specifically.** It is warmer and more saturated than `#C4A882` because the Soft Gold lamp key biases the skin toward amber-orange. It is not a contradiction of RW-10 — it is a derived version of it for that lighting context.

**The rule:** `#C4A882` is the starting point. Scene-specific derived values (CHAR-L-01, DRW-04, DRW-11, etc.) are the results of applying that starting point to a specific lighting setup. A painter using only `#C4A882` is correct for neutral/unspecified lighting. A painter rendering Frame 01 uses `#C8885A` as their base because that is what `#C4A882` looks like under a Soft Gold lamp key.

---

### 7.2 — Character Skin Reference Table

| Character | Neutral Base | Hex | Notes |
|---|---|---|---|
| **Luma** | Warm Tan (RW-10) | `#C4A882` | Standard neutral-light base; Section 3 character spec |
| **Luma** (lamp-lit Frame 01) | Warm Caramel (CHAR-L-01) | `#C8885A` | Derived from RW-10 under Soft Gold key |
| **Cosmo** | Light Warm Olive (CHAR-C-01) | `#D9C09A` | Lighter, cooler skin than Luma — see 7.3 below |
| **Grandma Miri** | Deep Brown (CHAR-M-01) | `#8C5430` | Distinct deep brown skin — warm, earthy |
| **Background humans** | Warm Tan (RW-10) | `#C4A882` | Default for any unnamed human character |

---

### 7.3 — CHAR-C-01 — Cosmo Skin Base

- **Hex:** `#D9C09A`
- **RGB:** 217, 192, 154
- **Role:** Cosmo's neutral-light skin base. Lighter and more desaturated than Luma's `#C4A882`. Reads as a lighter warm olive skin tone that matches his more reserved personality palette.
- **Relationship to RW-10:** Cosmo's skin sits in the same warm family as RW-10 but is notably lighter (R: +21, G: +24, B: +24) and less saturated. The desaturation is intentional — it matches the cooler, more reserved tone of his dusty lavender palette. He is not a different palette system; he is the lighter end of the same warm skin family.
- **Shadow companion (warm light):** `#B89A78` (Warm Sand — from Cosmo color model)
- **Highlight (warm light):** `#EED4B0` (Pale Golden — from Cosmo color model)
- **Cool shadow (night/Glitch Layer):** Derive from RW-10c Cool Skin Shadow logic, adjusted for his lighter base. Expected result: approximately `#8A6A8A` (a lighter, slightly more lavender variant of `#7A5A7A`).
- **Source:** Cosmo color model sheet (Maya Santos, Cycle 3). This value was not previously registered in the master palette.
- **Avoid using:** As Luma's skin — the two characters must read as distinct warm tones at distance. CHAR-C-01 is lighter/cooler; CHAR-L base is warmer/more saturated.

---

### 7.4 — Skin Under Warm Light (Real World)

| Zone | Luma (RW-10 base) | Luma (lamp-lit Frame 01) | Cosmo |
|---|---|---|---|
| **Neutral base** | `#C4A882` (RW-10) | `#C8885A` (CHAR-L-01) | `#D9C09A` (CHAR-C-01) |
| **Shadow** | `#8C5A38` (RW-10b) | `#A86838` (CHAR-L-03) | `#B89A78` |
| **Highlight** | `#E8D4B0` (RW-10a) | `#E8B888` (CHAR-L-02) | `#EED4B0` |
| **Deep crevice** | `#3B2820` (RW-12) | `#3B2820` (RW-12) | `#3B2820` (RW-12) |

---

### 7.5 — Skin Under Cool Light (Night / Glitch Layer)

When any human character is in a cool-ambient or Glitch Layer environment, warm skin shadows shift to a desaturated violet tone (the skin reads as alive but not warm). The Real World shadow system does not apply in these contexts.

| Zone | Hex | Source | Notes |
|---|---|---|---|
| **Skin base under UV ambient** | `#A87890` | DRW-11 | Derived from RW-10 under UV Purple Glitch Layer ambient |
| **Shadow under UV ambient** | `#5A3A5A` | DRW-12 | Deep lavender-plum shadow |
| **Skin base under Cyan key** | `#7ABCBA` | DRW-01 | Derived from RW-10 under Electric Cyan screen glow |
| **Shadow under Cyan key** | `#3A7878` | DRW-02 | Deep cyan-toned shadow |
| **Cool shadow replacement (all chars)** | `#7A5A7A` | RW-10c | Replaces warm shadow in night/Glitch scenes |

**Rule:** When a scene transitions from warm Real World to cool Glitch Layer or nighttime, the warm shadow (`#8C5A38`, RW-10b) is replaced with the cool shadow (`#7A5A7A`, RW-10c). The base fill shifts per DRW-01 or DRW-11 depending on the dominant light source. Never apply both warm and cool skin shadow in the same scene unless the frame is an explicit split-light setup (as in Frame 01, which uses both a warm lamp and a cyan monitor).

---

### 7.6 — Canonical Skin Color Decision (Resolving the Fiona Critique)

**The discrepancy:** Fiona O'Sullivan (Cycle 8) identified that `luma_color_model.md` uses `#C8885A` while `master_palette.md` RW-10 specifies `#C4A882`, and that `style_frame_01_rendered.py` matches the color model (`#C8885A`), not the master palette base.

**The resolution:**

1. `#C4A882` (RW-10) **remains the canonical neutral-light skin base** for all human characters including Luma. The Section 3 character spec tables are correct and authoritative. This is what painters use for standard lighting.

2. `#C8885A` (CHAR-L-01) is **not a contradiction** — it is the correct derived result of `#C4A882` under a Soft Gold warm lamp key in the Frame 01 interior setup. The color model sheet (`luma_color_model.md`) documents it as "Warm Caramel" which is CHAR-L-01's scene-specific base.

3. **The color model sheet requires a clarification note** to prevent future confusion. The skin entry in `luma_color_model.md` should note that `#C8885A` is the lamp-lit derivation of the neutral base `#C4A882`, not a replacement for it.

4. Cosmo's `#D9C09A` is now registered as CHAR-C-01 (see 7.3 above) and is explicitly named in the palette as a character-specific lighter variant of the warm skin family.

**Action required (one-time):** The skin entry in `luma_color_model.md` should add a cross-reference note: "Base = Warm Caramel under lamp-lit Frame 01 conditions. Neutral-light canonical base = `#C4A882` (RW-10). See master_palette.md Section 7."

---

### 7.7 — Cross-Reference: RW-10 and CHAR-L-01 (Cycle 28 — Priya Nair C12 fix)

**Both values are correct. They are different tiers of the same skin system.**

- **RW-10 = `#C4A882` — Neutral skin base.** Use when lighting conditions are unspecified, in standard daylight, or as the derivation starting point for any scene variant. This is the value painters default to.
- **CHAR-L-01 = `#C8885A` — Lamp-lit skin derivation.** Use in warm lamp-dominant scenes (specifically Frame 01 three-light interior setup). This is what `#C4A882` looks like under a Soft Gold lamp key. It is warmer, more saturated (R +4, G −32 effective shift toward amber), and is the correct value for all lamp-lit skin surfaces in SF01.

**These are not competing values. They are not a discrepancy.** RW-10 is the neutral base. CHAR-L-01 is the warm-lamp-lit scene derivation. Both are correct in their context. A painter who uses `#C4A882` in a lamp-lit Frame 01 scene is using the wrong tier. A painter who uses `#C8885A` as a default in a neutral-light scene is also using the wrong tier.

*Cross-reference note added — Sam Kowalski — Cycle 28 (2026-03-29). Per Priya Nair C12 critique: P2 Fix 3 (Luma skin base 3-way conflict).*

---

*Section 7 added — Sam Kowalski — Cycle 9 (2026-03-29). Per Fiona O'Sullivan Cycle 8 critique: skin discrepancy between luma_color_model.md, master_palette.md RW-10, and style_frame_01_rendered.py.*

---

## SECTION 8 — ACT 2 REAL-WORLD ENVIRONMENTS

These colors govern the Tech Den (Grandma Miri's home workspace) and the School Hallway (Millbrook Middle School). Both are fully Real World environments — no Glitch Layer palette colors appear here under any circumstances. All values sourced from `output/color/palettes/act2_environments_color_brief.md` (Sam Kowalski, Cycle 17) and `output/characters/color_models/grandma_miri_color_model.md`.

---

### 8.1 — Grandma Miri Character Colors

| Code | Name | Hex | RGB | Notes |
|---|---|---|---|---|
| CHAR-M-01 | Miri Skin Base | `#8C5430` | (140, 84, 48) | Deep Warm Brown. Shadow: `#6A3A1E` (Dark Sienna). Highlight: `#A86A40` (Warm Chestnut). |
| CHAR-M-02 | Miri Skin Shadow | `#6A3A1E` | (106, 58, 30) | Dark Sienna — under chin, inner arm, side of face in 3/4. |
| CHAR-M-03 | Miri Skin Highlight | `#A86A40` | (168, 106, 64) | Warm Chestnut — forehead, nose tip, cheekbone. |
| CHAR-M-04 | Miri Permanent Blush | `#D4956B` | (212, 149, 107) | Always present at 25% opacity feel. See Dual-Blush Rule in grandma_miri_color_model.md. |
| CHAR-M-05 | Miri Hair Silver | `#D8D0C8` | (216, 208, 200) | Warm silver base — NOT cool blue-gray. Shadow: `#A8988C`. Highlight: `#F0ECE8`. |
| CHAR-M-06 | Miri Hair Shadow | `#A8988C` | (168, 152, 140) | Warm Gray within bun and between hair masses. |
| CHAR-M-07 | Miri Cardigan Base | `#B85C38` | (184, 92, 56) | Warm Terracotta Rust. Shadow: `#8A3C1C` (Deep Rust). Highlight: `#D4825A` (Dusty Apricot). |
| CHAR-M-08 | Miri Cardigan Shadow | `#8A3C1C` | (138, 60, 28) | Deep Rust — folds, cable-knit grooves, pocket edges. |
| CHAR-M-09 | Miri Glasses Frame | `#8A7A70` | (138, 122, 112) | Warm Gray — same as eyebrows; recedes so face reads first. |
| CHAR-M-10 | Miri Pants (Linen) | `#C8AE8A` | (200, 174, 138) | Warm Linen Tan. Shadow: `#A08A6A`. Highlight: `#DEC9A8`. |
| CHAR-M-11 | Miri House Slippers | `#C4907A` | (196, 144, 122) | Dusty Warm Apricot — soft in-den footwear. Warm family: R>G>B. Prior value `#5A7A5A` (Deep Sage) was a cool-neutral green that contradicted Miri's warm-palette guarantee (color story doc: "unambiguously warm"). Corrected C32 to a warm dusty apricot consistent with her domestic warmth. Shadow companion: `#A06A50` (warm terracotta shade). |

**Cross-reference:** Full Miri character spec in `output/characters/color_models/grandma_miri_color_model.md`. Miri skin base CHAR-M-01 also appears in skin system reference table at Section 7.2.

---

### 8.2 — Tech Den Environment (Grandma Miri's Home)

Lighting key: Daylight from LEFT window (warm amber-neutral); secondary: Ochre Brick lamp `#B8944A`. Monitor glow must NOT read as GL-01/GL-01b — see monitor safety rules below.

| Code | Name | Hex | RGB | Notes |
|---|---|---|---|---|
| TD-01 | Warm Linen Wall | `#E8D8B8` | (232, 216, 184) | Main wall. Aged bone — slightly darker than RW-01 Warm Cream. |
| TD-02 | Warm Wall Shadow | `#C4A882` | (196, 168, 130) | Shadow side of wall. = RW-10 (Warm Tan). |
| TD-03 | Ochre Plank Floor | `#B8944A` | (184, 148, 74) | Worn wooden floor. = RW-13 (Ochre Brick). |
| TD-04 | Floor Deep Shadow | `#8C5A38` | (140, 90, 56) | Under furniture, corners. = RW-10b (Skin Shadow). |
| TD-05 | Aged Dark Wood Desk | `#8C3A22` | (140, 58, 34) | Desk surface. = RW-05 (Rust Shadow). |
| TD-06 | Worn Wood Sheen | `#C4A882` | (196, 168, 130) | Specular hint on desk from window key. = RW-10. |
| TD-07 | Deep Cocoa Shelves | `#3B2820` | (59, 40, 32) | Bookshelves — recede into background. = RW-11. |
| TD-08 | CRT Monitor Casing | `#5B8C8A` | (91, 140, 138) | Analog aged plastic. = RW-12 (Muted Teal). |
| TD-09 | CRT Shadow Side | `#3A5A58` | (58, 90, 88) | Shadow companion to Muted Teal casing. = RW-12a. |
| TD-10 | Monitor Screen Fill | `#C8D4E0` | (200, 212, 224) | Desaturated blue-white. R:200 prevents Glitch Layer misread. |
| TD-11 | Monitor Glow Ambient | `#B8C8D4` | (184, 200, 212) | Aged phosphor glow on desk/face. R:184 — warm enough to not read digital. |
| TD-12 | Monitor Screen Dark | `#3A4A5A` | (58, 74, 90) | Inactive screen areas. Blue-shifted dark, not Void Black. |
| TD-13 | Window Key Light | `#D4B896` | (212, 184, 150) | Warmed Tan daylight through curtains. Gentler version of RW-03. |

**Monitor Glow Safety Rule:** Monitor glow values MUST maintain R ≥ 150 in the Tech Den at all times. GL-01 Electric Cyan has R:0; GL-01b Byte Teal has R:0. Any monitor glow with R < 150 risks reading as Glitch Layer emission and destroys the safe domestic read of this space.

**Forbidden in Tech Den:** GL-01 through GL-07, Void Black (#0A0A14) except under furniture against baseboard, cool blue ambient as fill.

---

### 8.3 — School Hallway (Millbrook Middle School)

Lighting key: Overhead fluorescent — cool, flat, even, slightly greenish. No directional key light. Shadow depth comes from geometry (locker recesses, under benches), not light direction.

| Code | Name | Hex | RGB | Notes |
|---|---|---|---|---|
| SH-01 | Institutional White (ceiling) | `#DDE8DF` | (221, 232, 223) | Fluorescent tube-shifted warm-white. Not pure white — slightly dingy. G>R ensures cool-green read. |
| SH-02 | Cool Plaster (upper wall) | `#C4CECC` | (196, 206, 204) | Desaturated blue-green neutral above lockers. Was Warm Cream (#FAF0DC) 20 years ago. |
| SH-03 | Scuff Gray (lower wall) | `#B0BABC` | (176, 186, 188) | Slightly cooler than upper wall. Collects scuffs and locker shadows. |
| SH-04 | Institutional Sage (Locker A) | `#8A9E94` | (138, 158, 148) | Primary locker color — muted green-gray. Alternates A/B along wall. |
| SH-05 | Institutional Blue-Gray (Locker B) | `#8A96A4` | (138, 150, 164) | Second locker color — cool counterpart to SH-04. Near-equal value for subtle variation. |
| SH-06 | Locker Shadow | `#5A6268` | (90, 98, 104) | Cast shadow inside vent slits, under handles. Dark cool gray. |
| SH-07 | Aged Metal (handle/detail) | `#A0A8A8` | (160, 168, 168) | Flat worn metal — slightly teal-shifted. Not shiny chrome. |
| SH-08 | Institutional Linoleum | `#B8B49A` | (184, 180, 154) | Main floor tile. Warm sandy base washed cool by fluorescents. |
| SH-09 | Floor Grout | `#8A887A` | (138, 136, 122) | Darker warm-gray seams between tiles. |
| SH-10 | Floor Shadow | `#6A6A60` | (106, 106, 96) | Cast shadow under lockers, benches. Retains faint warm undertone. |
| SH-11 | Fluorescent Tube White | `#E8EEE8` | (232, 238, 232) | Tube color — very slightly green. Not pure white. |
| SH-12 | Fluorescent Cast | `#D0DDD8` | (208, 221, 216) | Overall fluorescent color temperature. G>B shift = institutional fluorescent, not generic cool. |

**Color Safety Rule — All grays must have warm or cool lean:** No pure R=G=B grays in the school hallway. All institutional tones use the fluorescent cast as a desaturation influence. A pure gray would read as a production error (accidental neutral), not institutional architecture.

**Luma Hoodie Rule in Hallway:** Orange hoodie (#E8703A) appears slightly desaturated and greenish-cool under fluorescent key. This is intentional — the hoodie recovers full saturation when Luma exits. This color contrast IS the narrative beat about belonging. Do NOT over-desaturate. The hoodie should look washed out, not fully grey.

**Forbidden in School Hallway:** GL-01 through GL-07, Soft Gold (#E8C95A) or Sunlit Amber (#D4923A) as ambient fill, pure neutral grays (R=G=B).

---

*Section 8 added — Sam Kowalski — Cycle 18 (2026-03-29). Source: act2_environments_color_brief.md (Cycle 17) and grandma_miri_color_model.md (Cycles 3, 17). Resolves TASK 2 Cycle 18 master palette gap — C17 Act 2 environment additions.*

---

*Document version 2.0 — Sam Kowalski — 2026-03-29*
*Cycle 2 revision: Full hex audit, shadow companion system, exception documentation, additional forbidden combinations.*
*Cycle 7 revision: Section 5 added (Character Rendering Colors — Luma, from style_frame_01_rendered.py); GL-01b usage warning added; GL-07 outline width standard set to canonical 3px.*
*Cycle 8 revision: Section 6 added (Environment / Props — couch PROP-01/02/03, cable PROP-04/05/06, neutral grey PROP-07 deprecated/replaced); CHAR-L-08 placeholder added (hoodie underside, lavender ambient).*
*Cycle 9 revision: Section 7 added (Skin Color System — two-tier system, CHAR-C-01 for Cosmo, warm/cool skin tables, Fiona critique resolution); PROP-07 finalized (CABLE_NEUTRAL_PLUM, #504064); CHAR-L-08 finalized (#B06040, HOODIE_AMBIENT); CHAR-L-09/10 added (Luma shoe canvas/sole per Naomi Bridges Cycle 8 feedback).*
*Cycle 10 revision: CHAR-L-08 hex corrected from #B06040 (176,96,64) to #B36250 (179,98,80) — blue channel arithmetic error resolved (Naomi Bridges C9-5). Glitch Layer depth-tier construction values documented in comment block (Naomi C9-1). luma_color_model.md cross-reference confirmed present in both documents.*
*Cycle 13 revision (Sam Kowalski — 2026-03-30): C10-1 RESOLVED — cold overlay boundary arithmetic for SF01 documented in Section 1B (prior comment was wrong: alpha at 80px boundary is 30/11.8%, not near-zero). DRW-16 RESOLVED — painter warning for shoulder-under-Data-Stream-Blue-waterfall expanded and cross-referenced to luma_color_model.md. DRW-07 saturation corrected: #C07A70 → #C8695A (RGB 200,105,90), HSL saturation raised from ~39% to ~50% (Naomi C12-3). ENV-06 corrected: #9A8C8A (warm-dominant grey, wrong) → #96ACA2 (G>R, B>R, correctly cyan-lit) per Jordan Reed / Naomi C12-1. ENV-03 warm spill canonical alpha documented: 40/255 (~16%) — aligned LTG_TOOL_colorkey_glitchstorm_gen_v001.py from prior 150 to 40 (Naomi C12-2). CHAR-L-09 warm pixel activation: pending Alex Chen confirmation (message sent 2026-03-30 14:00).*
*Cycle 14 revision (Sam Kowalski — 2026-03-30): CHAR-L-11 added — Luma Hoodie Pixel (Warm-Lit Activation), hex #E8C95A (Soft Gold, alias RW-02). Registered per Alex Chen Art Director confirmation. Constraints: lamp-lit hoodie pixel accents only, warm-dominant scenes only; neutral/cold scenes use GL-01 (#00D4E8). CHAR-L-09 warm pixel activation thread CLOSED — correctly occupied by shoe canvas; CHAR-L-11 is the warm pixel entry.*
*Cycle 15 revision (Sam Kowalski — 2026-03-29): DRW-18 added — Luma Hair Base (Glitch Layer), hex #1A0F0A (26,15,10); derived from Deep Cocoa #3B2820 under UV Purple ambient. ENV-13 added — Far Structure Edge (Void-Scale), hex #211136 (33,17,54); derived as 20% UV Purple over Void Black; used for SF03 megastructure silhouettes at far-void distance. Source: SF03 Other Side spec color audit (sf03_other_side_color_notes.md).*
*Cycle 21 revision (Sam Kowalski — 2026-03-30): Palette Status section added (final Critique 10 audit).*
*Cycle 30 revision (Sam Kowalski — 2026-03-29): CHAR-L-11 Constraint 1 hex error corrected — prior text cited `#00D4E8` (GL-01b Byte Teal) for neutral/cold-scene hoodie pixel accents; correct value is GL-01 Electric Cyan `#00F0FF`. Byte Teal is Byte's body fill only and must never appear as a hoodie pixel color.*
*Cycle 32 revision (Sam Kowalski — 2026-03-30): CHAR-L-11 cross-reference corrected — cross-ref line cited `#00D4E8` (GL-01b Byte Teal) for cold-scene hoodie pixels; correct is GL-01 `#00F0FF` Electric Cyan (Priya Nair C13 P1). CHAR-M-11 Miri House Slippers corrected — `#5A7A5A` Deep Sage (cool-neutral green, G>R) replaced with `#C4907A` Dusty Warm Apricot (R>G>B, warm family) per Priya Nair C13 P2; Deep Sage contradicted Miri warm-palette guarantee in color story. DRW-18 warmth clarification — added HSL lightness note (7%); warmth of R:26>G:15>B:10 is theoretically present but functionally imperceptible at this luminance; DRW-18 does NOT contribute visual warmth to SF03; warm values in SF03 are hoodie orange and skin only. Color story doc updated with same clarification.*
*Review cycle: Update after each critic feedback pass.*
*Cycle 33 revision (Sam Kowalski — 2026-03-30): QA Scene-Lighting Exceptions section added — SF04 Byte teal dim documented as SCENE-LIGHTING — ACCEPTED per Alex Chen Art Director decision (C32 directive). GL-01b in SF04 at ~60-70% canonical luminance is intentional discovery-scene low-key lighting, not a generation error. LTG_TOOL_palette_warmth_lint_v001.py created and registered in tools README — catches G>R or B>R violations in all CHAR-M entries (actioned ideabox: warmth linter). C33 baseline: 11 CHAR-M entries, 0 violations.*

---

## PALETTE STATUS — Cycle 21 Audit
**Author:** Sam Kowalski — 2026-03-30 (pre-Critique 10)

---

### LOCKED (Canonical — must not change without Art Director sign-off)

These are the show's foundational colors. Every generator, color key, and painted asset references them. Any change would require a full pipeline re-audit.

| Code | Name | Hex | Section |
|---|---|---|---|
| GL-01 | Electric Cyan | `#00F0FF` | 2 |
| GL-01a | Deep Cyan | `#00A8B4` | 2 |
| GL-01b | Byte Teal | `#00D4E8` | 2 |
| GL-02 | Hot Magenta | `#FF2D6B` | 2 |
| GL-04 | UV Purple | `#7B2FBE` | 2 |
| GL-07 | Corrupted Amber | `#FF8C00` | 2 |
| GL-08 | Void Black | `#0A0A14` | 2 |
| RW-01 | Warm Cream | `#FAF0DC` | 1 |
| RW-02 | Soft Gold | `#E8C95A` | 1 |
| RW-04 | Terracotta | `#C75B39` | 1 |
| RW-10 | Warm Tan (skin base) | `#C4A882` | 1 |
| RW-11 | Deep Cocoa (line) | `#3B2820` | 1 |
| CHAR-L (hoodie) | Luma Hoodie Orange | `#E8703A` | 3 |
| CHAR-L (hoodie shadow) | Luma Hoodie Shadow | `#B84A20` | 3 |
| CHAR-L-08 | Hoodie Underside (Ambient) | `#B36250` | 5 |
| All PROP-01 through PROP-07 | Couch/cable prop system | various | 6 |
| ENV-06 | Terracotta under Cyan key | `#96ACA2` | 1C |
| DRW-07 | Storm-Modified Hoodie | `#C8695A` | 1B |

**Locking criteria:** Has appeared in two or more rendered generators, has passed at least one Critique cycle without challenge to the value, and has no outstanding correction note.

---

### PROVISIONAL (May be adjusted — carries outstanding note or single-script use)

| Code | Name | Hex | Reason for Provisional Status |
|---|---|---|---|
| CHAR-L-11 | Hoodie Pixel (Warm-Lit) | `#E8C95A` | Alias of RW-02; production pixel-grid render not yet verified in OpenToonz; Pillow script uses gradient approximation only |
| DRW-13b | Cool Skin Highlight (Glitch Layer) | `#8A6A7A` | Added Cycle 2; no rendering in any generator to date — derived spec only |
| RW-NSM | Moon Ambient | `#C8BFD8` | No rendering yet; referenced in spec only |
| TD-10/TD-11 | Monitor Screen / Glow | `#C8D4E0` / `#B8C8D4` | Close-but-not-identical variants appear in LTG_TOOL_bg_tech_den_v002.py (MON_GLOW_BRIGHT 200,218,240 and MON_GLOW_MID 180,200,210). Needs alignment pass. |
| CHAR-M-04 | Miri Permanent Blush | `#D4956B` | Opacity-feel spec (25%) in grandma_miri_color_model.md not yet translated to a flat alpha render constant |
| CHAR-C-01 | Cosmo Skin Base | `#D9C09A` | In character spec; no rendered SF or generator has used this value directly yet |
| SH-01 through SH-12 | School Hallway palette | various | Documented in Section 8.3; no rendered generator exists for hallway environment yet |

---

### NAMED GAPS (Missing documentation — action required)

1. **`UV_PURPLE_MID (42,26,64)` and `UV_PURPLE_DARK (43,32,80)` in LTG_TOOL_style_frame_03_other_side_v003.py** — These are construction values for the SF03 void sky gradient, sitting between GL-08 Void Black and GL-04a Deep Digital Void. They are not registered anywhere in the master palette. **Disposition:** These are legitimate atmospheric construction gradients. They should be documented as GL-04c (UV Purple Mid-Dark, #2A1A40 approx.) and GL-04d (UV Purple Near-Void, #2B2050 approx.) — or mapped to the existing ENV-11/ENV-12 entries if those match. Cross-check against ENV-11 `#2A1A40` (42,26,64 ≈ match) and ENV-12 `#2B2050` (43,32,80 ≈ match). **Likely already covered by ENV-11 and ENV-12; Jordan Reed to confirm and add cross-reference comment to the script.**

2. **`CIRCUIT_TRACE_DIM (0,192,204)` in SF03 v003** — A dim circuit-trace color between GL-01a Deep Cyan and GL-01 Electric Cyan. Not registered. **Disposition:** Scene-specific construction value acceptable without registration if commented in the script (already is). Low priority.

3. **`JEANS_BASE (38,61,90)` in SF03 v003** — **RESOLVED (Cycle 22).** Confirmed as CHAR-L-05 shadow companion `#263D5A` rendered under UV Purple ambient. SF03 jeans at shadow value = correct environment-specific rendering. Documented under CHAR-L-05 entry with explicit UV-ambient use note. Canonical jeans base `#3A5A8C` unchanged. Future Glitch Layer scenes must use `#263D5A` only when UV Purple ambient is the dominant light source.

4. **`LUMA_SHOE (220,215,200)` in SF03 v003** — Slightly lighter/cooler than CHAR-L-09 Warm Cream `#FAF0DC` (250,240,220). Under UV ambient the shoe canvas shifts slightly. Not registered. **Disposition:** Low priority; construction value. Add inline comment in script citing CHAR-L-09 parent and UV ambient modification.

5. **`LTG_TOOL_bg_tech_den_v002.py` — Multiple new construction values** — WALL_WARM, SUNLIT_AMBER (note: different from master palette RW-03 `#D4923A`), CART_YELLOW/RED/GREY/BLUE, component colors, bedding colors. These are scene-specific prop construction values. **Disposition:** Section 8 covers the canonical Tech Den palette (TD-01 through TD-13). The bg_tech_den generator has additional scene-dressing props that are acceptable as construction values provided the canonical surfaces (walls, floor, CRT) match the Section 8 entries. CRT_CASING and CRT_SHADOW match exactly; wall/floor tones are close but the bg generator uses slightly different values (WALL_WARM 240,228,200 vs TD-01 232,216,184). Jordan Reed should add a comment in the generator noting the variance and citing TD-01.

---

### GL NUMBERING — COMPLETENESS CHECK

The GL (Glitch Layer) palette numbering is **complete and unbroken**: GL-01, GL-01a, GL-01b, GL-02, GL-02a, GL-03, GL-03a, GL-04, GL-04a, GL-04b, GL-05, GL-05a, GL-06, GL-06a, GL-06b, GL-06c, GL-07, GL-07a, GL-08, GL-08a. No numbered gaps. All have documented shadow companions per the Section 2 table. The depth-tier construction values are documented separately and correctly attributed.

**GL-06c** (Storm Confetti Blue, #0A4F8C) added Cycle 28 — atmospheric depth derivative of GL-06 for the Glitch Storm confetti. This is a deliberate distance/atmosphere darkening, not an error or substitute for GL-06.

---

### ACT 2 ENVIRONMENTS — COMPLETENESS CHECK

Section 8 is complete as of Cycle 18:
- Grandma Miri character colors: CHAR-M-01 through CHAR-M-11 (11 entries) — COMPLETE
- Tech Den environment: TD-01 through TD-13 (13 entries) — COMPLETE
- School Hallway: SH-01 through SH-12 (12 entries) — COMPLETE

Outstanding from Section 8: School Hallway has no rendered generator yet. This is an Act 2 asset — acceptable at this stage of production. Hallway generator is a future-cycle deliverable.

---

### QA SCENE-LIGHTING EXCEPTIONS

These are cases where a QA tool (e.g. `LTG_TOOL_render_qa_v001.py` or `LTG_TOOL_color_verify_v002.py`) will flag a value that does NOT represent a production error. Each entry is tagged `SCENE-LIGHTING — ACCEPTED` and must not trigger a production fix request.

| Asset | QA Flag | Canonical Value | Scene Value | Reason | Status | Decision |
|---|---|---|---|---|---|---|
| `LTG_COLOR_styleframe_luma_byte_v004.png` (SF04) | GL-01b BYTE_TEAL below canonical | `#00D4E8` (0,212,232) | Dominant teal at ~(0,138–160), hue 183-185° | SF04 is Luma's first entry into the Glitch Layer — dramatic low-key discovery lighting. Byte exists within his environment at reduced luminance (60-70% of canonical). This is **intentional scene lighting**, not a generation error. Byte's hue is correct; only luminance is reduced. | SCENE-LIGHTING — ACCEPTED | Alex Chen, Art Director — Cycle 33 (2026-03-30) |

**Rule:** A `SCENE-LIGHTING — ACCEPTED` exception does not prevent the underlying canonical value from being updated in the generator if/when the scene lighting intent changes. It prevents QA tools from treating the existing rendered state as a production failure requiring immediate correction.

*Added: Sam Kowalski — Cycle 33 (2026-03-30). Per Alex Chen Art Director decision (C32 directive, carried forward from C26). Closing outstanding carry-forward item.*

---
