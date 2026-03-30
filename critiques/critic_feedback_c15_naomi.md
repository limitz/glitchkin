# Naomi Bridges — Critique Cycle 8
**Date:** 2026-03-29

---

## SF02 Glitch Storm [B]

### What is Working

The broad color architecture is sound. The sky-to-street invasion narrative is legible: Void Black / UV Purple / Hot Magenta / Electric Cyan dominating the upper frame, contested warm remnants at street level. The complementary tension between Luma's orange hoodie and the cyan key is conceptually correct. The confetti semantic correction (Acid Green removed from storm confetti) was the right call and the corrected spec is properly applied here.

Byte's Corrupted Amber (#FF8C00) outline is doing its job. The 2px warm rim reads at distance against the cyan-dominant background, pulling his silhouette out of the glitch energy. His placement on the LEFT shoulder — away from the crack, silhouetted against the deep hoodie shadow (#3A1A14) — gives the outline something to work with. The narrative plausibility justification (Real World homing signal under digital stress) is a bonus; the production rationale is what matters and it holds.

The VOID_BLACK body on Byte is intentional and reads correctly as thematic weight: he is a creature consumed by the digital, with only the amber outline anchoring him to the warmth of Luma's world. This is good color storytelling.

### Critical Failures

**DRW-07 is out of date in the rendered frame.** The master palette documents a Cycle 13 correction: DRW-07 was changed from #C07A70 RGB(192,122,112) to #C8695A RGB(200,105,90). The spec as rendered still references the OLD value. Looking at the frame: Luma's storm-lit hoodie face reads warmer and less saturated than it should. Under the corrected DRW-07, the hoodie should read at approximately 50% saturation — HSL roughly (9°, 50%, 57%). What I see reads closer to the old 39% saturation value. This is a direct compliance failure against the Cycle 13 correction. Jordan Reed / Alex Chen: verify your constant in the background and character scripts against #C8695A, not #C07A70.

**ENV-06 is still wrong in the rendered output.** The master palette explicitly flags this: "The SF02 background generator (`LTG_TOOL_style_frame_02_glitch_storm.py`) still uses the old value `TERRA_CYAN_LIT = (154, 140, 138)`." Looking at the Cyan-lit building walls in the frame: the right-facing terracotta walls read slightly warm — R channel visually dominant. Under a cyan key, G must exceed R and B must approach or exceed R. The corrected value RGB(150, 172, 162) requires G=172 > R=150, B=162 > R=150. What is rendered fails that test — it reads as a warm grey neutralization rather than a true cyan-lit surface. The generator has not been updated. This is a flagged outstanding correction that should have been resolved before this review cycle.

**Verify ENV-06 arithmetic in the rendered image:**
- Old value #9A8C8A: R=154, G=140, B=138. R > G > B. This reads WARM. Wrong.
- Correct value #96ACA2: R=150, G=172, B=162. G > B > R. This reads COOL (cyan-lit). Required.
The building walls in the frame fail the G > R AND B > R test for cyan-lit surfaces.

**The cyan key rule is directly violated on the background architecture.** Under a cyan key light — by definition — G > R AND B > R individually must hold for any lit surface that is intended to read as cyan-influenced. The terracotta walls in the rendered frame do not satisfy this. That is not a stylistic preference. It is the physics of complementary hue mixing coded into the show's own color system.

**Dutch angle at 4 degrees is too subtle to register.** The spec calls for 4 degrees as a deliberate choice — "mild end, keeping readability high." Conceptually I accept the rationale, but looking at the rendered frame, the tilt is so minimal that it reads as a composition error rather than an intentional stylistic choice. The style guide cites 5-15 degrees for tension. 4 degrees is below even the lower bound. This needs to be pushed to at least 6-7 degrees or justified with a formal deviation note in the spec.

**The warm spill at street level (window light) is too weak.** The spec states that ENV-03 warm spill runs at alpha 40/255 (~16%). In the rendered frame, the warm pool on the left sidewalk is nearly invisible — it is reading closer to 8-10% visually. The warm light is the frame's emotional anchor — "the world still lit from within, still alive." If that anchor is invisible, the narrative of contested warmth collapses. The cyan-dominant read then covers everything. This is not a production goal; the frame is meant to show the tension between warm and cold. The warm spill needs to be visible, not just technically present.

---

## SF03 Other Side [B+]

### What is Working

The overall atmosphere is a genuine achievement. The void is vast. The atmospheric perspective inversion is structurally correct: far structures do shift toward UV Purple (#7B2FBE family) and darken rather than lighten. The spec's core emotional premise — "warmth as something you carry, not something you're given" — is readable in the palette. Luma's HOODIE_UV_MOD (#C07038) reads as warm pigment under cold ambient, which is exactly the right effect. The near-complementary relationship between her hoodie orange and the UV Purple mid-distance creates a strong silhouette.

The data waterfall at midground is correctly executed: DATA_BLUE (#2B7FFF) columns, with DATA_BLUE_HL (#6ABAFF) on individual character highlights. The waterfall acting as both compositional element and tertiary light source (washing Luma's right shoulder) is solid color scriptwriting.

The warm-light prohibition is satisfied at the system level. No light sources emit warm temperature. CORRUPT_AMBER on the Real World fragments reads as material corruption, not illumination. This is the most important rule in the SF03 spec and it holds.

### Critical Failures

**The data waterfall is far too saturated and bright for the ambient depth it occupies.** The waterfall column (#2B7FFF, bright cobalt blue) is the highest-chroma, highest-luminance element in the frame by a significant margin — brighter even than Luma's HOODIE_UV_MOD on the orange hoodie. This destroys the figure-ground hierarchy. Luma and Byte should be the dominant focal elements. A world-building architectural element — however beautiful — must not outcompete the characters in visual weight. The waterfall, at current values, is the first thing my eye goes to. That is wrong. It needs to be pushed down in luminance by 15-20% and the column width reduced, or the haze on its far edge increased to integrate it more convincingly into the depth layer it occupies.

**Luma's hair in the Glitch Layer is visually unresolved.** The spec defines DRW-18 (#1A0F0A, RGB 26,15,10) as her hair base — near-void-dark, with UV Purple rim sheen (GL-04 #7B2FBE) on the crown. The rendered Luma shows hair that is simply dark with no visible purple rim sheen. At the scale she occupies in this wide shot (approximately 1/5 frame height), the crown rim sheen is a critical readability detail — it separates her head silhouette from the dark void background. Without it, her head and the dark structures behind her bleed together. The UV Purple rim on the hair crown must be explicitly drawn, even if just 1-2 pixel rows at production resolution.

**The far-distance atmospheric perspective is correct in hue but incorrect in depth progression.** The spec establishes a multi-layer recession: midground structures at ENV-09/ENV-10, mid-distance at ENV-11 (#2A1A40), far-distance at ENV-12 (#2B2050) and ENV-13 (#211136) edge strokes. In the rendered frame, the jump from mid-distance to far-distance is too abrupt — there is insufficient intermediate tonal stepping. Structures at mid-distance (center of frame, visible large rectangles) are reading at nearly the same tonal value as structures that should be two depth layers further back (upper right area). The inverted atmospheric perspective is only convincing if the layers are genuinely graduated. Currently the depth tiers visually collapse in the upper-right quadrant.

**The pixel-art plants on the platform are not visible.** The spec explicitly defines them: ACID_GREEN (#39FF14) forms in platform cracks, with DARK_ACID (#1AA800) undersides and ELEC_CYAN bounce light on upper faces. At the platform level in the rendered frame, there are small green triangular marks — but they are too small and too dark to register at viewing distance. The Acid Green should be luminous against the Void Black platform base. These plants are not a minor texture detail — they are a semantic element (the only "alive" organic material in the Glitch Layer, establishing that life can persist here). They need to be legible. Minimum 3-4px on the final render, saturated to full GL-03 (#39FF14) value.

**Byte on Luma's shoulder is not legible at this scale.** The spec acknowledges Byte is 1/10 of frame height and that his dual-eye colors must be visible. They are not. His body reads as a dark smear. His ELEC_CYAN eye and HOT_MAGENTA eye — which are the frame's most important narrative color detail (the eyes that tell the entire relationship story between Byte, Luma, and the void) — are not distinguishable at the rendered scale. This is a failure of execution, not of concept. The eyes must be painted as explicit colored ellipses of minimum 6-8px width per the sf03_other_side_color_notes.md eye-size specification. This cannot be left ambiguous.

**The confetti distribution reads as random, not physics-governed.** The spec establishes that SF03 confetti is ambient (low-velocity, small particles, settled background emission from the platform). The rendered confetti, while sparse, includes a cluster of brighter particles near the mid-frame area that has no source proximity justification. Per the governing physics rule, particle size and density must diminish with distance from the source (the platform). Mid-air clusters with no adjacent active source are a physics violation. Pull those particles back to the platform area or make them visibly smaller at distance.

---

## Byte Expression Sheet v002 [C]

### What is Working

The state machine logic is clear and readable. The transition labels (was: / next:) add genuine production value. The addition of RESIGNED as a new expression is the right call — it fills a necessary emotional gap in Byte's range. The overall layout is clean and legible at glance. The dual-eye color system (ELEC_CYAN left / HOT_MAGENTA right) is consistently applied across all expressions, which is exactly what a character model sheet requires.

### Critical Failures

**Byte's body fill is wrong across the entire sheet.** Per master palette GL-01b (Byte Teal, Cycle 5 Art Director decision), Byte's body fill should be #00D4E8 RGB(0, 212, 232). What I see across all 8 expressions is a fill that reads at or very close to #00F0FF Electric Cyan — maximum luminance cyan, not Byte Teal. This is not a subtle distinction. The palette specifically created GL-01b because using Electric Cyan as Byte's fill caused figure-ground failures in cyan-dominant environments. The entire rationale for the separate color is undermined if the expression sheet is modeled on the wrong base. The difference: #00F0FF HSL (183°, 100%, 50%) vs. #00D4E8 HSL (188°, 100%, 45%). Byte Teal is approximately 6% darker and slightly shifted toward teal. The expression sheet must be repainted to GL-01b.

**The background colors in the expression sheet cells are narratively unmotivated and colorimetrically problematic.** The sheet uses multiple different background values: NEUTRAL/DEFAULT appears on a dark teal-grey, GRUMPY and CONFUSED on near-black, ALARMED on a distinctly warm brown, RELUCTANT JOY on dark charcoal. The ALARMED cell (#3B2820 range, warm cocoa) is particularly problematic — Byte's Void Black body against a warm brown background generates a low-contrast read AND sends the wrong color semantic. ALARMED is a danger state; it should read against a cool or neutral background. The warm background makes ALARMED read like a Real World comfort moment, which is the opposite of its narrative intent. Expression sheet backgrounds should either be uniform (to isolate the character) or deliberately chosen to reflect the scene context — but if scene context, each background choice must be justified and consistent with the show's color semantics. As designed, the varied backgrounds appear arbitrary and one is actively misleading.

**The shadow values on Byte's body form read as desaturated grey, not Deep Cyan (#00A8B4).** Per the Glitch Shadow Companion System in the master palette, Byte's shadow companion is GL-01a Deep Cyan (#00A8B4, RGB 0,168,180). His shadow areas across the expression sheet read as a cold grey (approximately RGB 80-90, 130-140, 150-160 range by visual estimate). That is not #00A8B4. If the shadow has drifted to a generic cool grey, the shadow system is broken — Byte's shadows should stay in the cyan family to maintain his visual identity as a glitch entity. Grey-shadowed Byte reads as a generic robot. Cyan-shadowed Byte reads as a digital lifeform. That distinction is material.

**The Hot Magenta accents (the small squares on limb joints and base of expression cells) are inconsistent in size and placement.** Across the 8 panels, the small magenta accent squares vary visually — some panels show 3 squares, some 2, sizes differ by approximately 20-30%. These are presumably semantic markers (GL-02 Hot Magenta read as danger/alert-state indicators). If they are structural design elements of Byte's model, they must be consistent across all expressions. If they scale with emotional intensity, that rule is not stated and is not being applied consistently. Either establish the rule and apply it, or standardize to a single layout.

**The pixel-screen faceplate (the rectangular grid display on Byte's face) is not consistently sized relative to the head circle.** Comparing NEUTRAL to POWERED DOWN to RESIGNED: the faceplate grid appears to shift in scale relative to the head. In POWERED DOWN it is notably wider relative to the head than in NEUTRAL. At this level of geometric inconsistency, animation will be impossible without a model correction. This is a rigorous consistency failure for a character on-model sheet.

---

## Priority Fixes (top 3)

1. **Update DRW-07 and ENV-06 in the SF02 background generator immediately.** DRW-07 must be corrected to #C8695A (RGB 200,105,90). ENV-06 must be corrected to #96ACA2 (RGB 150,172,162). Both are documented Cycle 13 corrections that have not been implemented in the production script. ENV-06 is a hard color system rule violation: the cyan-lit terracotta walls must satisfy G > R AND B > R. The current rendering fails this test. Until the generator is corrected, every SF02 derivative output inherits the error.

2. **Repaint Byte's body fill on the expression sheet from Electric Cyan (#00F0FF) to Byte Teal (#00D4E8, GL-01b).** This is a foundation error. The entire purpose of GL-01b is to prevent Byte from merging with cyan-dominant environments. If the character model is built on the wrong base, every downstream production asset inherits the figure-ground problem the palette specifically solved. Repaint all 8 expressions and re-derive all shadow values from GL-01a (#00A8B4) while the correction is being made.

3. **Resolve Byte's legibility on the SF03 shoulder at production scale, and enforce the pixel-plant visibility standard on the platform.** Both are failures of execution rather than concept. Byte's dual-eye colors are the single most important color narrative detail in the SF03 frame — they cannot be invisible. Paint the eyes as explicit 6-8px colored ellipses. The ACID_GREEN pixel plants must read at full GL-03 luminance. These are small corrections that prevent the frame's color storytelling from being lost entirely in the translation from spec to rendered output.
