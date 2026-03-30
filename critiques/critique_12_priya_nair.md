# Color Critique — Cycle 12 (Priya Nair)
**Critic:** Priya Nair, Color Theory and Emotional Palette Specialist
**Date:** 2026-03-29
**Scope:** Master palette, SF01–SF04 generators, color story document, character color models (Luma, Cosmo, Grandma Miri)

---

## Palette Extraction and Hue Angle Inventory

Before the critique, the palette sorted by hue angle (approximate, HSL):

| Hue Angle | Color | Hex | Family |
|---|---|---|---|
| ~0° (red-orange edge) | Rust Shadow | #8C3A22 | RW shadow |
| ~9° | Terracotta | #C75B39 | RW architecture |
| ~18° | Hoodie Orange | #E8703A | Character |
| ~20° | Corrupted Amber base shadow | #A84C00 | GL shadow |
| ~22° | Sunlit Amber | #D4923A | RW warm |
| ~33° | Corrupted Amber | #FF8C00 | GL bridge |
| ~38° | Soft Gold | #E8C95A | RW light |
| ~38° | Ochre Brick | #B8944A | RW mid |
| ~47° | Warm Tan (skin) | #C4A882 | RW character |
| ~76° | Acid Green | #39FF14 | GL digital |
| ~90° | Sage Green | #7A9E7E | RW nature |
| ~113° | Muted Teal | #5B8C8A | RW analogue |
| ~177° | Electric Cyan | #00F0FF | GL primary |
| ~183° | Byte Teal | #00D4E8 | GL character |
| ~200° | Data Stream Blue | #2B7FFF | GL navigation |
| ~272° | UV Purple | #7B2FBE | GL void |
| ~280° | Dusty Lavender | #A89BBF | RW cool |
| ~335° | Hot Magenta | #FF2D6B | GL danger |

The warm-to-cold span: ~9° (RW darkest warm) → ~183° (GL cool peak) = 174° of hue separation. The Real World palette occupies roughly 9°–113° (warm-to-teal), and the Glitch palette occupies 76°–335°. The boundary colors (Acid Green ~76°, Muted Teal ~113°) are correctly positioned as transitional. The range is intentional and documented. This is structurally sound.

---

## SECTION 1 — MASTER PALETTE

**Overall assessment: Exceptionally well-documented. The shadow companion system is complete and logically consistent. The governing principles are explicit. The warm/cool narrative is written into the palette rules themselves, not implied.**

That said: there are four issues that must be addressed.

### Issue 1 — Luma Skin Base: Three-Value Conflict

The master palette carries three different values for Luma's skin base that are in active conflict:

- **Section 3 Character Specifications:** `#C4A882` (Warm Tan, RW-10) — this is stated as the definitive skin base.
- **Luma color model sheet:** `#C8885A` — described as the "lamp-lit Frame 01 derivation." The footnote explains that `#C4A882` is for "standard/neutral lighting."
- **SF04 generator (LTG_COLOR_styleframe_luma_byte_v002.py):** `SKIN = (200, 136, 90)` = `#C8885A` — matches the color model sheet, not Section 3.

In HSL: `#C4A882` ≈ (38°, 33%, 64%) versus `#C8885A` ≈ (26°, 47%, 57%). These are not the same color. The hue shifts 12°, the saturation increases 14 points, the value drops 7 points. On screen, `#C8885A` reads noticeably warmer and darker than `#C4A882`. This is not a lamp-effect derivation — it is a different base.

The color model sheet handles this correctly by explaining the derivation, but it creates a situation where painters without the full context will use whichever value they encounter first. Section 3 says one thing; the character color model says another; the generator implements the character model value. The result is that the "canonical source of truth" (master palette Section 3) is already not what is being rendered.

**Directive:** Either revise Section 3 to formally adopt `#C8885A` as the lamp-lit standard base and demote `#C4A882` to "neutral outdoor" (which is how the color model sheet already treats it), or explicitly state in Section 3 that two bases exist for different lighting conditions. The current state creates real confusion. This must be resolved, not annotated around.

### Issue 2 — Cosmo Skin: Color Model Diverges from Master Palette

Master palette Section 3 (Character: Cosmo) lists skin base as `#C4A882` — the same as Luma. The Cosmo color model sheet lists `#D9C09A`. In HSL: `#C4A882` ≈ (38°, 33%, 64%) versus `#D9C09A` ≈ (38°, 32%, 72%). These are the same hue angle and nearly identical saturation — the difference is purely in value (8 points lighter). The hue relationship holds.

However, this divergence is undocumented in both the master palette and the color model sheet. There is no note in either document explaining why Cosmo's skin differs from the Section 3 spec, nor any derivation logic. This is not a lamp-modified variant; it is simply a different base.

The visual intent is apparently to distinguish Cosmo from Luma (lighter, less warm skin) — this is a legitimate design choice. But undocumented choices become errors when handed to painters. The color story relies on these two characters reading as distinct individuals while sharing warm-skin visual DNA. That distinction is currently carried by a 8-point value difference with no paper trail.

**Directive:** Document this difference explicitly in both the master palette Section 3 Cosmo entry and the Cosmo color model sheet. State that Cosmo's skin is a lighter value variant of the shared warm-tan family, and give the rationale. The rationale exists — write it down.

### Issue 3 — DATA_BLUE in SF02 Generator: Undocumented Non-Canonical Value

The SF02 generator (`LTG_TOOL_style_frame_02_glitch_storm.py`) defines:

```
DATA_BLUE = (10, 79, 140)  # #0A4F8C
```

The master palette GL-06 Data Stream Blue is `#2B7FFF` = (43, 127, 255). These are not the same color. In HSL: `#2B7FFF` ≈ (217°, 100%, 60%) versus `#0A4F8C` ≈ (210°, 87%, 29%). The SF02 DATA_BLUE is 31 value points darker and substantially less saturated — it behaves as a storm shadow/depth value, not as the canonical data stream blue.

Checking the depth-tier table in master palette Section 2: `MID_COLOR = (10, 72, 120)` = `#0A4878` — the SF02 DATA_BLUE (10, 79, 140) is similar in the R and G channels but with a slightly higher B (140 vs 120), sitting between `MID_COLOR` and a lightened version of it. The comment in the generator says it is used as "dominant storm confetti color." The visual logic appears to be: in a storm, data energy appears bruised and dark rather than fully saturated.

This is not necessarily wrong as a design choice. But it is completely undocumented. The master palette has no entry, no note, and no cross-reference. The comment in the generator calls it `#0A4F8C` with no justification, no derivation from GL-06, and no note that it deviates from the canonical value.

If this bruised data-blue is an intentional atmospheric modification for the storm scene (analogous to how ENV-06 documents Terracotta under Cyan key), it needs to be formally added to master palette Section 1B or Section 1C as a derived environment value with its derivation formula. If it is not intentional — if it was simply defined by eye and never compared to GL-06 — then it needs to be evaluated against the canonical value and a decision made.

The narrative stakes are high here: the storm confetti is 70% this color. What the audience sees as "cold, threatening storm energy" is not the show's canonical data-blue — it is a substantially darker, less saturated variant. If that is the intent, document it. If it is not the intent, fix it.

**Directive:** Add `DATA_BLUE_STORM = #0A4F8C` as a derived Glitch palette entry with an explicit derivation from GL-06 and a scene-restriction note (storm context only), OR correct the SF02 generator to use GL-06 `#2B7FFF` and evaluate whether the storm sky still reads correctly. Do not leave an undocumented, unnamed value carrying 70% of the frame's dominant cold color.

### Issue 4 — UV_PURPLE_DARK in SF03 Generator

The SF03 generator defines `UV_PURPLE_DARK = (43, 32, 80)` but the master palette's documented shadow step for UV Purple (GL-04) is `#3A1060` = (58, 16, 96). In HSL: master palette Deep Digital Void (58, 16, 96) ≈ (273°, 72%, 22%) versus SF03's `UV_PURPLE_DARK` (43, 32, 80) ≈ (261°, 31%, 22%). These are the same value level, same hue family, but the master palette version is far more saturated (72% vs 31%). The SF03 version is considerably desaturated — closer to a grey-purple than a deep void.

This is a shadow companion accuracy failure. The shadow companion system in master palette Section 2 exists precisely to prevent shadows from going grey. GL-04a `#3A1060` is defined as the shadow that "keeps the digital void active even in shadow areas." Using (43, 32, 80) instead flattens the void toward grey and undermines the Glitch Layer's chromatic identity in its darkest zones.

**Directive:** Replace `UV_PURPLE_DARK = (43, 32, 80)` in the SF03 generator with the canonical `#3A1060` = (58, 16, 96), which is both more accurate and more chromatically alive. Run the output and verify. If the atmospheric quality is lost, document why as a formal override.

---

## SECTION 2 — STYLE FRAME PALETTE RATINGS

### SF01 — Discovery

**Warm/cool narrative:** Correctly implemented. The frame is warm-dominant with a single cyan intrusion. The split-light logic (Soft Gold lamp at left, Electric Cyan screen at right) is architecturally sound.

**Hue analysis — key relationships:**
- Lamp-lit skin `#C8885A` (~26°) against Warm Cream walls `#FAF0DC` (~38°): 12° separation, same hue family, low contrast by design. Correct — Luma belongs here.
- Cyan screen `#00F0FF` (~177°) against Terracotta window trim `#C75B39` (~9°): approximately 168° separation. This is very close to a pure complementary pair. This is the correct emotional function — "warm vs cold as near-complement, not harmony."
- Orange hoodie `#E8703A` (~18°) against Electric Cyan `#00F0FF` (~177°): 159° separation. The complementary tension on a single character's body is exactly the correct encoding of Luma's in-between status.

**Cold overlay boundary (11.8% at x=880):** The documented arithmetic is correct and the decision to keep `cold_alpha_max = 60` is defensible. However, the cold wash at the warm zone boundary (~11.8%) produces a result around `#B1946D` on Luma's skin — which is still warm but slightly greyed. This greying at 12% is perceptible and intentional (cross-light, not Glitch Layer immersion). The documentation is clear. This passes.

**Unresolved decorative element:** The HOODIE_AMBIENT value `#B36250` = (179, 98, 80) does not appear explicitly in the master palette. It appears in the SF01 generator and the cold overlay table in luma_color_model.md. Its HSL is approximately (14°, 38%, 51%). This is a plausible ambient/secondary surface value between the hoodie base and shadow, but it carries no formal registration in the palette. It is used in a structural role (the hoodie's non-lit, non-shadow intermediate surface) and therefore earns its place narratively — but it is undocumented.

**Rating: B+.** The palette concept is excellent. The cold overlay system is rigorous. The warm/cool split is clean. Deducted for HOODIE_AMBIENT being structurally load-bearing without formal registration.

---

### SF02 — Glitch Storm

**Warm/cold narrative:** The contested warm-cold thesis is correctly implemented in principle. The composition is structured correctly: cold storm above, warm street life below. The Corrupted Amber fix (to `#FF8C00` = ~33°) was the right call — the prior `#C87A20` (~28°) was too warm and too dark to function as a complement to Electric Cyan (~177°). The 144° hue separation between the corrected GL-07 and Electric Cyan is close enough to complementary to deliver the required visual tension. The previous value would have provided only ~149° separation but at much lower saturation — the saturation mismatch was the real problem, not the hue.

**DATA_BLUE undocumented value — critical narrative implication:** This frame's dominant color (70% of confetti mass) is `#0A4F8C`, a value that reads as a cold, bruised near-navy. This is used as "threatening storm energy." But GL-06 `#2B7FFF` is a clear, vivid data-navigation blue. These produce different emotional temperatures: `#0A4F8C` feels oppressive and dark; `#2B7FFF` feels functional and navigable. The frame is using the oppressive variant — which may be correct for a storm — but no one has explicitly made this design decision on paper. This is the most significant undocumented color choice in the entire project.

**ENV-06 correction acknowledged:** The terracotta-under-cyan-key correction (from `#9A8C8A` to `#96ACA2`, ensuring G > R and B > R on cyan-lit walls) was necessary and correct. The prior value was physically wrong — it produced a warm face on a cyan-lit surface. However, the master palette note says the SF02 background generator still uses the old value. If this was not corrected in v005, the frame may be rendering incorrectly colored building walls. Verification is required.

**Window glow alpha correction:** The reduction from alpha 160/180 to 115/110 was correct. At 160+, window panes were more saturated than Luma's storm-modified hoodie — inverting the character-warmth hierarchy. This is now fixed. The 115/110 range allows the warm amber window light to function as narrative support (the Real World persisting) without competing with the protagonist's color.

**DRW-07 storm hoodie `#C8695A`:** HSL approximately (9°, 50%, 57%). Correct — it retains warm identity (9° is still red-orange) while the B channel (90) reflects the cyan temperature bleed. The 50% saturation provides clear separation from background building walls (ENV-06 saturation ~28%). This passes the character-over-background rule.

**Rating: B.** The contested warm-cold composition structure is sound. The canonical GL-07 fix was essential and correct. DATA_BLUE is the elephant in the room — 70% of the frame's dominant cold is an undocumented, unregistered value, and until that decision is formalized, this frame's palette cannot be called complete.

---

### SF03 — The Other Side

**Zero warm light rule:** The generator enforces this correctly at the code level — "NO WARM LIGHT. Zero." is stated as a CRITICAL RULE and the warm-color inventory is explicitly labelled for pigment-only use. This is the correct approach and it is architecturally enforced, not just hoped for.

**UV_PURPLE_DARK desaturation problem:** As noted in Section 1, `UV_PURPLE_DARK = (43, 32, 80)` ≈ (261°, 31%, 22%) substantially undercuts the canonical GL-04a `#3A1060` ≈ (273°, 72%, 22%). Both sit at the same value level, but the generator's version is more than half as saturated. In practice this means the darkest zones of the Glitch Layer sky (where UV_PURPLE_DARK appears) are washing toward desaturated grey-purple rather than maintaining the deep digital void character. The void should be chromatically active — cold and alien even in its deepest register. A desaturated grey-purple reads as merely dark. This is a quality failure.

**Inverted atmospheric perspective — conceptually correct, implementation requires scrutiny:** The stated rule "things get MORE PURPLE and DARKER with distance" is the right inversion of Real World perspective. Real World atmospheric perspective lightens and desaturates with distance; the Glitch Layer deepens and purples. This correctly encodes the Glitch Layer as a world with different physical laws. The implementation uses lerp gradients toward UV Purple at depth. This is sound in principle.

**Byte Teal body fix confirmed:** `BYTE_BODY = (0, 212, 232)` = GL-01b Byte Teal. This is the correct value, confirmed corrected from the prior (10, 10, 20) Void Black error. The comment in the generator makes the fix history explicit. This passes.

**DRW-18 hair base `#1A0F0A`:** HSL ≈ (18°, 45%, 7%). This is a very dark near-void with residual warm undertone. In the Glitch Layer context, the UV Purple rim sheen on the hair crown (GL-04 `#7B2FBE` = ~272°) provides the only chromatic information on the hair. The warm undertone of the hair base is functionally invisible at this value level (7% lightness). The purpose — to carry a vestige of real-world warmth in the hair even in the Glitch Layer — is present in the documentation but absent in the perceptual result. At 7% lightness, the warm base does nothing visible.

This is a philosophical failure, not a technical one. If Luma's warm pigment memory is supposed to survive in her hair in the Glitch Layer, it needs to be visible. The hair base at `#1A0F0A` is indistinguishable from Void Black to any viewer. Only the UV Purple rim sheen (correctly placed) is doing actual narrative work. The "residual warmth in the hair base" argument is not supported by the actual color value.

**Rating: B-.** The zero-warm-light enforcement is correct and necessary. The inverted atmospheric perspective concept is right. But the UV_PURPLE_DARK desaturation is a concrete quality issue, and the hair warmth argument is narratively claimed but visually absent. These are not minor issues — the Glitch Layer palette must remain chromatically active even in its darkest zones to maintain the alien-cold-beauty quality that makes SF03 work.

---

### SF04 — The Dynamic (Luma + Byte)

**Dual warm/cool lighting premise:** Warm window from left (Sunlit Amber, RW-03 `#D4923A` ~22°), cool monitor from right (Byte Teal, GL-01b `#00D4E8` ~183°). The hue angle separation between these two sources is approximately 161° — nearly complementary. This is the correct architecture for a split-light scene. It mirrors SF01's lamp/screen split and is clearly intentional.

**HOODIE_AMBIENT = (179, 98, 80) = `#B36250`:** HSL ≈ (14°, 38%, 51%). This is the secondary hoodie surface value — neither the lit nor shadow face, but the ambient-side fill. This value appears in both SF01 and SF04 generators without registration in the master palette. In SF04, where the scene explicitly features a cool monitor ambient from the right, the right-side hoodie shadow is listed as `HOODIE_SH = (184, 74, 32)` = `#B84A20` — which is the master palette canonical hoodie shadow. There is no cool-side hoodie variant (equivalent to DRW-07 from SF02) documented for the bedroom context with monitor ambient light. This is a gap: the monitor-facing hoodie surface in a bedroom dusk scene with Byte Teal as the cool key should produce a specific derived value, just as the storm cyan key produced DRW-07. Instead, the warm shadow color is applied to the cool-side face, which produces incorrect temperature on that surface.

**Blush values in SF04 generator:** The code applies blush as raw RGB (220, 80, 50, 55) and (208, 72, 48, 55) — neither of which corresponds to any registered palette value. The Luma color model specifies blush as `#E8A87C` (Reckless Excitement) or `#E8A87C` at 60% (Guilty Sheepishness). The generator's blush RGB (220, 80, 50) at alpha 55 would composite to approximately a desaturated orange-red over warm skin — this is not `#E8A87C` (198, 168, 124), which is a warm peach. The generator's blush is dramatically more red-orange and more saturated than the specified value. HSL of (220, 80, 50) ≈ (16°, 68%, 53%) versus `#E8A87C` ≈ (28°, 55%, 63%). The hue is 12° apart, the saturation is 13 points higher, the value is 10 points lower. On a child character, this produces a blush that reads as fever or embarrassment-to-the-point-of-pain rather than curiosity-delight. This is a character voice error.

**Byte body fill in SF04:** `BYTE_FILL = (0, 190, 210)` = `#00BED2`. The master palette GL-01b is `#00D4E8` = (0, 212, 232). The SF04 value is 22 points darker in both G and B channels. HSL: `#00D4E8` ≈ (183°, 100%, 45%) versus `#00BED2` ≈ (183°, 100%, 41%). The hue is identical, the saturation identical, the value 4 points different. This is a minor difference in isolation, but the master palette exists precisely to prevent this kind of drift. There is no annotation in the generator explaining why a darker value was used. The canonical value must be used unless there is a documented lighting reason for the deviation.

**Rating: C+.** The dual warm/cool lighting architecture is correctly conceived. But the execution has three concrete failures: no cool-key hoodie derivation for the monitor-facing surface, blush in the wrong saturation/hue family entirely, and Byte's body fill drifting 22 points from canonical without justification. The SF04 palette is not internally consistent with the established system.

---

## SECTION 3 — COLOR STORY DOCUMENT

The color story document is, genuinely, one of the clearest pieces of narrative color writing I have encountered in a production bible. The three-sentence arc — "SF01: This is Luma's world. SF02: Neither world owns this frame. SF03: This is not Luma's world." — is not only a clean pitch summary but an actual structural description of what the palette is doing. This is what a color story document is for.

However, three issues must be raised:

**1. The "material pigment vs. lighting" argument in SF03 is correct but needs technical support.** The document argues that in SF03, Luma's warmth is "entirely material" — her pigments survive because they are intrinsic to her, not because any light source supports them. This is a legitimate color theory argument: in a cool-ambient environment, a highly saturated warm pigment (like `#E8703A` orange at HSL 18°, 78%, 57%) will not disappear — it will desaturate toward the ambient color but retain hue identity. The DRW-14 value (`#C07038` = ~22°, 55%, 48%) correctly shows this: saturation drops from 78% to 55%, value drops from 57% to 48%, but hue is preserved at ~22°. This is physically correct. The argument works. But the document does not make this explicit — it states the conclusion ("warmth survives only as pigment memory") without showing the spectral arithmetic. For a production bible, the arithmetic is required. Painters who do not understand why the orange persists will either over-warm or over-cool it.

**2. The Grandma Miri "bridge character" palette rationale is excellent conceptually but makes an implicit promise the color model cannot keep.** The document states: "Any contamination from GL palette hues in her environment scenes would undercut this ambiguity — her space should read as unambiguously warm until the story itself provides the recontextualization." However, Miri's color model lists her house slippers as Deep Sage `#5A7A5A` — a cool-leaning green that sits at approximately 120° (HSL ~120°, 15%, 40%). Deep Sage in this context, on a character whose warmth should be non-negotiable, is a muted intrusion of cool color that subtly signals the Glitch Layer's teal/green family (Acid Green at ~76°, Muted Teal at ~113°). This is not GL palette contamination in a glitch-energy sense, but it introduces ambiguity where the color story document says there should be none. If Miri's footwear reads as cool-green, the argument that her palette is "unambiguously warm" fails at the ground plane — the most read area of a standing character in a wide shot.

**3. The CORRUPT_AMBER analysis is correct and the argument is precise.** The section explaining why GL-07 `#FF8C00` must be at full saturation (255, 140, 0) and cannot be desaturated is exactly right. A murkier amber reads as aged, warm, organic — the opposite of corrupted. The section earns its place.

---

## SECTION 4 — CHARACTER COLOR MODELS (Spot Check)

### Luma Color Model

The cold overlay table is the most rigorous piece of technical documentation in the project. The per-channel arithmetic is correct, the cyan-dominance thresholds are accurate, and the distinction between SF01 cross-light (intentionally not cyan-dominant) and Glitch Layer immersion (deliberately cyan-dominant) is clearly drawn. This is exactly what should exist in a character color model for a show where the same character appears across two radically different color environments.

**Outstanding issue:** The DRW-16 shoulder warning is well-placed and important. The color `#9A7AA0` = (154, 122, 160) for the hoodie shoulder under Data Stream Blue overhead deserves scrutiny. HSL ≈ (280°, 17%, 55%) — a very desaturated violet-grey. The B channel (160) exceeds R (154) by only 6 points. The documentation says R=154 "retains slight orange warmth" while B=160 "reflects the Data Stream Blue dominance." This is technically correct: the residual R warmth signals the original hoodie orange, and the slight B elevation signals the blue key. However, at 17% saturation, this color provides almost no chromatic information. The shoulder read as "Luma touched by the Glitch Layer" depends entirely on context — in isolation, `#9A7AA0` reads as medium grey-lavender with no obvious warmth. Whether painters can read the intent is a legitimate question.

### Cosmo Color Model

Cosmo's shirt stripe colors (`#5B8DB8` Cerulean Blue and `#7A9E7E` Sage Green) are a persistent minor concern. Neither color belongs to the Real World palette primary family (warm ambers, terracottas). The Sage Green stripe is registered (RW-06 `#7A9E7E`), and Cosmo's character notes say he provides "breathing room" via cool hues. But the Cerulean Blue `#5B8DB8` ≈ (211°, 38%, 54%) sits adjacent to the Glitch palette's blue family without being from it. It is too cool for the Real World and not saturated enough to be Glitch. It floats. The document describes it as his "intellectual, notebook" color — but the color does not belong to either world's logic, which means it is a decoration without a palette home.

This is not a crisis. Cosmo's visual identity works. But when every other color in the show has been assigned to either the Real World or the Glitch palette with documented rationale, Cerulean Blue is an anomaly. It needs either a narrative justification for being neither-world, or it needs to be pushed toward an established palette entry.

### Grandma Miri Color Model

**Strong.** The warm terracotta cardigan (`#B85C38` ≈ 15°, 56%, 47%) as a settled, aged version of Luma's hoodie orange (`#E8703A` ≈ 18°, 78%, 57%) is excellent — same hue family, lower saturation, lower value, the visual equivalent of lived-in warmth versus energetic warmth. The design intent is clear. The visual DNA links are explicit and logically grounded.

The slippers issue is documented above. Resolve it.

---

## SUMMARY OF ACTIONABLE DIRECTIVES

In order of severity:

**P1 — DATA_BLUE_STORM must be formally registered.** The dominant cold color in SF02 (70% of confetti mass, also used in sub-cracks) is `#0A4F8C`, which deviates substantially from GL-06 `#2B7FFF`. This color is doing the most narrative work in the most contested frame in the show. It is not documented. Register it as a derived storm variant with derivation formula, or correct it to GL-06 and evaluate the output. This is the single highest-priority color documentation gap in the project.

**P1 — UV_PURPLE_DARK in SF03 must use the canonical shadow companion.** Replace `(43, 32, 80)` with GL-04a `#3A1060` = (58, 16, 96). The current value desaturates the deepest voids toward grey, undermining the Glitch Layer's chromatic identity in its darkest register. The void must remain purple, not grey.

**P2 — SF04 blush values are wrong.** The generator applies (220, 80, 50) at alpha 55, which is not `#E8A87C` and does not match any registered blush value for Luma. This is a character voice error on a child protagonist. Fix to `#E8A87C` at the appropriate opacity per the character model disambiguation table.

**P2 — SF04 Byte body fill deviates without justification.** `(0, 190, 210)` must be corrected to GL-01b `(0, 212, 232)` = `#00D4E8` unless a documented lighting reason exists for the deviation.

**P2 — Luma skin base conflict between master palette Section 3 and character model.** Resolve the three-value conflict. Choose one base for standard lighting and document it formally in both locations.

**P3 — HOODIE_AMBIENT `#B36250` must be registered in master palette.** It is load-bearing in both SF01 and SF04 and appears in the cold overlay table. It is not in any palette section. Register it.

**P3 — SF04 needs a cool-key hoodie derivation.** The monitor-facing (Byte Teal key) hoodie surface in SF04 requires a DRW entry analogous to DRW-07 in SF02. The warm shadow `#B84A20` applied to the monitor-facing face is thermally incorrect.

**P3 — Cosmo skin divergence from master palette must be documented.** The 8-point value difference between Cosmo's skin model (`#D9C09A`) and Section 3 (`#C4A882`) is an undocumented design choice.

**P3 — Grandma Miri's slippers contradict the color story document's warm-palette guarantee.** Deep Sage `#5A7A5A` on her footwear introduces a cool-green signal in a character whose warmth the narrative depends on being unambiguous. Either rationalize the slipper color within the warm-palette story, or change it to a warm earth tone.

**P4 — Cosmo's Cerulean Blue shirt stripe needs palette assignment.** It belongs to neither the Real World nor the Glitch palette logic and is undocumented as an intentional anomaly.

---

*The color arc (warm → contested → cold/alien) is clearly conceived and mostly correctly implemented. The documentation system is more rigorous than most productions achieve at this stage. The shadow companion system is complete. The narrative-color logic in the color story document is sound. None of that changes the fact that this work is not ready until the P1 and P2 items above are resolved. The dominant cold in SF02 must be named. The Glitch Layer void must not go grey. The blush on the protagonist must match the character model. These are not optional refinements.*

*Priya Nair*
*2026-03-29*
