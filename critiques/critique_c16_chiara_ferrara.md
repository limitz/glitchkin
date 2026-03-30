# Critique 16 — Background Environments & Style Frames
## Critic: Chiara Ferrara — Background Art & Environment Design

**Date:** 2026-03-30
**Cycle:** 39 (C16 critique cycle)
**Scope:** Complete pitch — all environment backgrounds and style frames
**Assets reviewed:** Kitchen v005, Living Room v001 (NEW), Tech Den v004_warminjected, School Hallway v003, Millbrook Street v002, Glitch Layer v003, Other Side ENV, Luma Study Interior (legacy); SF01 v006, SF02 v008, SF03 v005, SF04 v004
**Tools used:** LTG_TOOL_render_qa.py (v2.0.0), LTG_TOOL_color_verify.py (v002)

---

## Preamble — What Has Changed Since C14

My C14 critique (2026-03-29) issued five priority actions. I am now reviewing the results of those actions alongside the new living room asset and checking all style frames for environment-relevant issues.

**C14 priority action outcomes:**
1. School Hallway v003 — PARTIAL. Locker color remap and figure-ground fix done (correct). SUNLIT_AMBER drift: **still 9.7° FAIL at 44.0°, zero samples at canonical 30–35° band.** The PNG on disk was not regenerated after the code fix.
2. Grandma's Kitchen v004/v005 — RESOLVED. Value range min=20 (was 62), warm/cool separation=32.6 (was 1.7). Both QA failures cleared. Good work.
3. Glitch Layer v004 — NOT DONE. Still v003. UV_PURPLE_DARK pre-saturation-fix values unaddressed. No HOT_MAGENTA fissure lines.
4. Tech Den v005 — NOT DONE. Still v004_warminjected variant. SUNLIT_AMBER not found in canonical color range (not_found = not a failure by tool logic, but color-verify absence means the warm shaft remains unconfirmed).
5. Millbrook Street v003 — NOT DONE. Still v002. Value floor 45 (was 45 in C14).

---

## 1 — GRANDMA'S KITCHEN v005

**QA:** WARN | value range min=20 max=230 (range=210, PASS) | warm/cool separation=32.6 (PASS) | SUNLIT_AMBER PASS (delta=1.7°) | line weight: 3 outliers WARN

**Score: 76/100**

- Both critical failures from C14 are resolved: value floor to 20 (was 62, crevice shadow depth now present) and warm/cool separation 32.6 (was 1.7, dual-temperature system now working). The MIRI-specific spatial details (rose-pattern mug, knitting bag, travel fridge magnets, medicine bottles, wall calendar) are correct in principle — they make this a room a person lives in.
- SUNLIT_AMBER 1.7° delta PASS with 2,599 samples — the warm light is canonically anchored. This is the Real World benchmark all other interiors should match.
- Three line weight outliers persist. In a hand-built environment these may be structural lines (table edge vs ambient detail line) drawing at non-spec width. Not a blocker but warrants a targeted check of the floor tile grid lines — they use a different draw system than the furniture.
- **Remaining gap:** The perspective floor grid (per v004 spec: non-linear row spacing, converging column lines to vp_x) is the strongest architectural move in this environment. What is missing is atmospheric value recession — far-wall detail should be lighter/more desaturated than foreground. At present the back wall and its decorations read at near-identical contrast to foreground objects. Apply at minimum a 15–20% value lift on all BG-plane elements.
- **Bottom line:** A genuine improvement from C14's 58/100 — the kitchen now reads as warm, inhabited, and light-differentiated; the remaining work is atmospheric recession in the far plane.

---

## 2 — GRANDMA MIRI'S LIVING ROOM v001 (NEW ASSET — first review)

**QA:** WARN | value range min=26 max=228 (range=202, PASS) | warm/cool separation=25.4 (PASS) | SUNLIT_AMBER PASS (delta=0.2° — best canonical anchor in the entire suite) | line weight: 0 outliers PASS

**Score: 72/100**

I found 1 perspective concern. It is as follows:

- **Single vanishing point at VP_X=55%, VP_Y=36%.** The camera is described as "mild 3/4 angle." However, a 3/4 interior view requires either two-point perspective (two vanishing points, one outside each side of frame) or a carefully managed single-point system where the angled wall is handled as a separate face. The generator draws the back wall as a rectangle-based polygon, the floor with planks converging to VP_X, and the sofa with "slight 3/4 perspective" as a separate function that may not share the same VP. The result: the back wall reads as flat-on (like a camera directly facing it), while the floor converges to a point that implies an off-center camera. These two planes do not share a consistent spatial logic. A viewer trying to orient in this space will feel the room shift.
- **SUNLIT_AMBER 0.2° delta — the best canonical result in the suite.** 480 samples at hue 34.1°. The afternoon light shaft from the left window is Real World-accurate. This is the standard all other Real World interiors should be measured against.
- **CRT focal point is the story's central object.** The generator positions it "off-center right, clearly old, gently glowing." The warm/cool separation at 25.4 confirms the CRT cool bounce is creating a zone differentiation — this is correct for the show's founding dramatic device. The diamond-crystal figurine (C39 addition) connecting to Glitch Layer geometry is a strong narrative plant.
- **Value ceiling at 228** — acceptable but the CRT screen (a light emitter) and the afternoon window should reach near-255 at their hotspot centers. Sam Kowalski's v002 ceiling-guard principle applies: light sources must have a specular point that survives thumbnail downscaling.
- **The back wall is doing no spatial work.** Described as wallpaper-textured, it is the room's primary depth plane and should be doing the most atmospheric work (lightest value, softest edges, most desaturated). It reads as mid-value flat fill. Miri's history should be on that wall — framed photos, a clock, stacked books — not as decoration but as a compressed timeline.
- **Bottom line:** A promising first pass with correct light logic and strong canonical color anchoring — the CRT and afternoon lamp premise holds — but the perspective inconsistency between the flat back-wall read and the converging floor plane must be resolved before this room can be trusted in character-composited panels.

---

## 3 — TECH DEN — COSMO'S WORKSPACE v004_warminjected

**QA:** WARN | value range min=31 max=239 (range=208, FAIL) | warm/cool separation=7.9 (FAIL) | SUNLIT_AMBER not_found (no canonical warm samples) | line weight: 1 outlier PASS

**Score: 58/100**

- **C14 priority action NOT done.** The same value range, same warm/cool separation, same absent SUNLIT_AMBER as last cycle. A warm-inject post-process pass was applied but it has not resolved the structural dual-temperature problem. The warm/cool separation at 7.9 means the two light zones are still fighting to a near-draw. A "_warminjected" suffix in the filename tells me a patch was applied on top of a broken light architecture, not a rebuilt one.
- **Value floor at 31** — the minimum is ≤30, so this is a marginal fail. One additional shadow pass in the desk underside and floor corners would resolve it.
- **Value ceiling at 239.** CRT monitors are light emitters. A 239 ceiling means the monitors are not registering as sources; they are registering as bright surfaces. The distinction matters in compositing: a character placed near a monitor should receive a color-accurate light contribution, and the monitor itself should have a near-255 hotspot at screen center.
- I found 2 perspective violations. They are as follows: (1) Floor planks drawn as horizontal lines at `ly = int(FLOOR_Y_FAR + t*(H-FLOOR_Y_FAR))` — these converge at infinity, not at the stated VP_X=820. Any floor plank line that is horizontal reads as if the camera is directly above the floor, not at a 3/4 angle. (2) Vertical plank dividers drawn at `fx = int(t * W)` — equally spaced, no convergence. In a correctly drawn floor at this camera angle, the vertical dividers converge toward the right vanishing point. Both errors are systematic, not incidental.
- **Cosmo's space still does not know who Cosmo is.** The jacket exists as an inhabited silhouette. The oscilloscope, breadboards, and cable tangles are documented in the spec. But after 25 cycles of Cosmo character development (v004 turnaround, v007 expression sheet, documented color model with cerulean/sage stripes, AWKWARD and WORRIED expressions, notebooks), none of these objects are Cosmo-specific. The notebook spec says color #5B8DB8. Put a notebook at that color on the desk. The jacket is Dusty Lavender. Where is his cerulean-stripe shirt over the back of the chair?
- **Bottom line:** The warm-inject patch has not fixed the dual-temperature failure — the light logic is broken at design level, not at parameter level — and the floor perspective errors compromise the room's spatial coherence at a time when the character who occupies it has grown into one of the show's most carefully specified people.

---

## 4 — SCHOOL HALLWAY v003

**QA:** WARN | value range min=19 max=237 (range=218, PASS) | warm/cool separation=34.8 (PASS) | SUNLIT_AMBER **FAIL** (delta=9.7°, found=44.0°, 18,966 samples — zero at canonical 30–35° band) | line weight: 0 outliers PASS

**Score: 56/100**

- **SUNLIT_AMBER drift is unchanged from C14 at 9.7° FAIL — the file was not regenerated.** The v003 generator source code at line 84 shows the corrected constant `SUNLIGHT_SHAFT = (212, 146, 58)` with a comment noting the correction from the old (232,201,90). The color_verify histogram shows 18,966 samples at hue 40–45° (the old value) and zero at the canonical 30–35° band. This means the PNG on disk was not regenerated after the source fix. This is a pipeline failure, not a design failure. But the result is the same: the school hallway's window shaft is a different color from SF01, SF02, and the kitchen. The Real World is not consistent.
- **Warm/cool separation 34.8 — structurally sound.** The fluorescent overhead vs window shaft temperature differentiation is working. Once the SUNLIT_AMBER constant is regenerated correctly, the separation logic will hold.
- **Value range PASS at min=19, max=237.** This is the best-performing hallway metric. The deep shadow work (NEAR_BLACK_WARM for crevices, v003 spec) has taken effect.
- **Figure-ground fix (v003, Hana Okonkwo, C38) is correct in principle.** Pushing locker values lighter than Cosmo's cardigan (~171 avg → ~205 avg, delta ~34) is the right approach. The shadow plum overlay in the character zone (alpha 22) is an appropriate compositor tool.
- **Linoleum checkerboard floor.** The floor tile perspective uses a standard grid-lines-to-VP system. I have not confirmed the tile convergence mathematically from source, but the rendered warm/cool separation on the floor zone suggests the perspective-projected grid is functional.
- **The hallway still has no Millbrook identity.** The notice board papers are colored rectangles. The stickers on lockers are shapes. After 20 cycles of world-building, this school should have a name on its seal, a specific banner, posters that reference the show's story beats. The human evidence (backpack, jacket) is generic — not from any named character.
- **Bottom line:** This environment's primary failure is a pipeline gap — the corrected source was never run — and the fix is a single regeneration call; after that, the warm/cool logic is sound but the space remains narratively empty.

---

## 5 — MILLBROOK MAIN STREET v002

**QA:** WARN | value range min=45 max=239 (range=194, FAIL) | warm/cool separation=21.2 (PASS) | SUNLIT_AMBER FAIL (not run — color_verify returned non-canonical warm on previous run; current check not run separately) | line weight: 1 outlier PASS

**Score: 64/100**

- **C14 priority action NOT done.** Value floor still at 45, value ceiling at 239. No deep shadow bands. Afternoon sun on a small town in late afternoon should produce cast shadows with floor values near 20–25 (dark asphalt in shade). Storefronts in direct sun should produce specular hits near 255 on pale facades. Neither is present.
- **Best warm/cool separation of all Real World exteriors at 21.2 (PASS).** The afternoon sun logic is still the best-executed light premise in the Real World set. This has not regressed.
- **Catenary power lines and perspective-correct crosswalk stripes** remain the strongest technical achievement in this environment. Correct.
- I found 1 atmospheric perspective concern. The generator uses a VP at (58%x, 38%y). Storefront buildings recede into the distance using this vanishing point. However, the atmospheric haze applied to the far end is a radial opacity fade from VP (per the generator's alpha-composite approach), not a value/saturation fade. These are different phenomena: atmospheric perspective works by lifting value toward 128 (air color) and desaturating color, not merely by making things transparent over a background. The far buildings should read as lighter and less saturated, not as ghosts over a hazy background.
- **Narratively inert after 21 cycles.** A Glitch Layer runs beneath this town. The show's color arc tells us Millbrook is the "belonging" register. But the street looks like a suburb in a generic animated show. One shop window with a hand-painted sign, one awning color that directly quotes a character palette, one bit of sidewalk damage that hints at something below — these are the environmental storytelling choices that make a background irreplaceable. This one is replaceable.
- **Bottom line:** The light logic is correct, the perspective is functional, but the value range fails strip it of atmospheric drama, and it has not learned a single thing from 21 cycles of world-building.

---

## 6 — GLITCH LAYER v003

**QA:** WARN | value range min=0 max=243 (range=243, PASS) | warm/cool separation=25.4 (PASS — cold dominant, separation reading is expected artifact) | BYTE_TEAL PASS (1.8°), UV_PURPLE PASS (0.0°), ELEC_CYAN PASS (0.1°) | line weight: 0 outliers PASS

**Score: 70/100**

- I found 0 perspective errors. Architecture of absence is still architecture. The non-Euclidean floating platform system is spec-compliant. No change from C14 on this count.
- **Three canonical Glitch palette colors confirmed: BYTE_TEAL, UV_PURPLE, ELEC_CYAN — all within 2°.** This is the only environment (alongside the Glitch Layer in style frames) with confirmed canonical color presence. The color system continues to hold.
- **C14 priority action NOT done: UV_PURPLE_DARK pre-saturation-fix values remain unaddressed.** The ENV background uses pre-C28 void zone values. SF03 v005 corrected UV_PURPLE_DARK from (43,32,80) to (58,16,96). The ENV has not been updated. If a character from SF03 is ever composited against this ENV background without color correction, the void zones will read as grey-purple against a saturated digital sky. This is a continuity failure waiting to happen.
- **C14 priority action NOT done: No HOT_MAGENTA fissure lines.** Glitch's crack lines, Byte's cracked-eye glyph, the UNGUARDED WARMTH expression's gold confetti — the show has spent considerable cycles establishing HOT_MAGENTA as the emotional break in the cold system. The world Glitch comes from shows zero evidence of this. Even at 3–5 platform-edge crack lines at alpha 60, HOT_MAGENTA fissures would activate the narrative content of this environment. A world of pure cold light with no emotional fissure does not tell the Glitch story.
- **Scanline overlay is present (v003, render_lib).** This remains correct for the CRT-interior premise.
- **Bottom line:** Color-faithful and architecturally coherent — the strongest environment in the pitch for fidelity — but two unaddressed C14 actions (UV_PURPLE_DARK update, HOT_MAGENTA fissures) mean it is drifting behind a show that has evolved significantly in its emotional and narrative ambition.

---

## 7 — OTHER SIDE ENV (LTG_ENV_other_side_bg.png)

**QA:** WARN | value range min=0 max=255 (range=255, PASS) | warm/cool separation=6.1 (PASS — cold expected) | UV_PURPLE FAIL (14.1°, 553 samples at hue 257.8° vs canonical 271.9°) | SUNLIT_AMBER samples found at 28.2° (621 samples — this is a zero-warm-light environment)

**Score: 60/100**

- **UV_PURPLE drift 14.1° FAIL.** This is the pre-saturation-fix void-zone value, same failure I flagged in C14. The style frame (SF03) was corrected in v005 (C28 UV_PURPLE_DARK saturation fix). The ENV background was not updated. The void zones read as grey-purple instead of the saturated digital void required by spec. This is now 8 cycles delinquent.
- **SUNLIT_AMBER-range warmth detected (621 samples at 28.2°).** This environment is specified as "zero warm light" (from the SF03 spec: "No warm light. Inverted atmospheric perspective."). 621 samples of near-amber hue indicate either a desaturated amber bleed from Real World debris elements (wall/road/lamppost), which would be acceptable but should be at lower saturation, or an unintended warm value not caught by visual inspection. The spec requires zero warm light contribution.
- I found 1 atmospheric perspective concern: this environment uses "inverted atmospheric perspective" per spec — far elements are darker and more saturated, near elements are lighter. The value range of 0–255 (full range, PASS) confirms the system has both deep voids and bright specular points, which is correct. But the color_verify findings suggest the saturation logic may have warped the UV_PURPLE identity in the process.
- **Floor plane readability.** The perspective pixel-grid floor is the show's clearest single-point convergence system outside the hallway. Its vanishing-point glow at the horizon is correctly placed. The floor plane is readable. This is good work that does not need revisiting.
- **Bottom line:** The UV_PURPLE drift (8 cycles delinquent) and the unexpected warm samples in a zero-warm-light environment are the two active failures; the floor plane and spatial logic are correct.

---

## 8 — LUMA STUDY INTERIOR (LTG_ENV_lumashome_study_interior.png)

**QA:** WARN | value range min=0 max=246 (range=246, PASS) | warm/cool separation=5.4 (FAIL) | line weight: 2 outliers PASS | color fidelity: not run separately

**Score: 42/100**

- **This is a Cycle 8 asset (Jordan Reed) renamed via a compliance copier.** It has not been rebuilt in 31 cycles. Every named character in this show has been rebuilt multiple times in that span. This environment — the room where the CRT television sits, the physical setting for SF01 — predates the canonical palette, the character proportions, the light logic system, and the scene-world temperature rules.
- **Warm/cool separation at 5.4 FAIL** is precisely the same failure as the pre-C14 kitchen. The discovery scene (SF01) is specified as warm lamp LEFT / CRT cool RIGHT — that is the show's founding light-as-metaphor moment. The environment behind it has near-zero warm/cool differentiation.
- **SF01 v006** (Rin Yamamoto, C38, PASS on render_qa, value ceiling 242) achieves its warm/cool reading from character-composite lighting passes, not from the background. If the background ENV is ever used for compositing (animatic, test renders), the light logic collapses.
- **No Miri-specific content.** SF01 is set in Grandma Miri's den/study. After v003 of her expression sheet (KNOWING STILLNESS — she knew about the Glitch Layer all along), the room where Luma discovers the Glitchkin should have spatial evidence of Miri's knowledge. The cable cluster, the orange cable prop, the CRT positioning — all of this is Cycle 8 generic. It does not know who Miri is or what she knows.
- **No atmospheric recession.** Background elements and foreground elements are at identical contrast levels. This has been the case since Cycle 8 and no subsequent pass has addressed it.
- **Bottom line:** This is the environment for the show's inciting incident and it is the worst-performing asset in the suite — a 31-cycle-old draft that has been renamed but not rebuilt, with a warm/cool failure that contradicts the founding dramatic logic of SF01.

---

## 9 — STYLE FRAMES (Environment component only)

### SF01 "The Discovery" v006

**Color verify:** CORRUPT_AMBER PASS, BYTE_TEAL PASS (1.6°), HOT_MAGENTA PASS (0.0°), ELEC_CYAN PASS (0.0°), SUNLIT_AMBER PASS (0.8°, 92,090 samples)

**Score: 84/100**
- The only style frame with fully passing color fidelity. 92,090 SUNLIT_AMBER samples at 0.8° delta is the canonical warm-light anchor for the entire show. The sight-line fix (C38, Rin Yamamoto — Luma's gaze reaches Byte) is compositionally correct: the character is now reading the space, not displaying herself in it.
- Environment integration: Luma occupies the foreground plane. The CRT (ghost Byte / light source) occupies the deep background. The depth separation is readable. The warm lamp contribution on Luma's face (add_face_lighting, procedural_draw) and the cool CRT rim light (add_rim_light) create a character-environment integration that the ENV background itself cannot replicate. This is the correct solution for the pitch but it means the ENV is dependent on the style frame composite logic to function.
- **Bottom line:** The strongest color-integrated environment piece in the pitch; the gap between this style frame and the standalone ENV background is a compositing risk.

### SF02 "Glitch Storm" v008

**QA:** WARN | value range PASS | warm/cool separation=8.5 | color verify: all canonical colors PASS

**Score: 79/100**
- Warm/cool separation at 8.5 (open WARN from C39 notes). The HOT_MAGENTA fill light fix (C34, from storm crack source) and ELEC_CYAN specular are present and color-verified. The storefront damage (v004 spec) and window light geometry (v004 spec) are present.
- Dutch angle at 4° is perceptible without being disorienting. The character depth placement (Byte left ~28%, Luma center ~45%, Cosmo right ~62%) creates a functional foreground-scene floor plane.
- The contested street environment is the pitch's most complex compositional problem: warm Real World buildings under siege from cold Glitch storm. At warm/cool separation of 8.5, the siege is not quite registering — the cold storm and the warm town are too close in temperature. This may require a targeted ELEC_CYAN boost on the upper-frame storm zone (currently at PASS color fidelity) to pull the two readings apart.
- **Bottom line:** Functionally correct and color-accurate but the warm/cold contest at the heart of this scene needs a stronger temperature split to read at pitch distance.

### SF03 "The Other Side" v005

**Color verify:** UV_PURPLE FAIL (9.2°, 447 samples at 262.7° vs canonical 271.9°) | SUNLIT_AMBER FAIL (9.3°, 1,349 samples at hue 25.0°) — zero warm light specified

**Score: 68/100**
- **UV_PURPLE still failing at 9.2° in the style frame — same drift as the ENV.** The void zones have the pre-saturation-fix grey-purple rather than the saturated digital void. This was flagged in C14. C28 introduced the UV_PURPLE_DARK saturation fix in the ENV generator but it has not propagated to the style frame fully. The color-verify tool shows the drift is measurable and persistent.
- **1,349 SUNLIT_AMBER-range samples in a zero-warm-light environment.** The Real World debris (wall, road, lamppost) per the SF03 spec introduces warm-adjacent desaturated values from the Real World. At hue 25.0° (closer to orange-red than canonical SUNLIT_AMBER at 34.3°), these are likely the terracotta/brick Real World debris objects. They are not SUNLIT_AMBER — they are warm solids. However, color_verify is catching them as warm-range samples. The spec says "inverted atmospheric perspective" for the Other Side — these debris objects should be the most desaturated, value-lifted, distant elements in the scene. If they are reading at saturation levels that trip the warm-hue detector, they are too present.
- Byte's canonical color (BYTE_TEAL PASS, 0.7°) and ELEC_CYAN (PASS, 0.0°) are confirmed. The cold palette is intact.
- Floor plane readability and the inverted atmospheric perspective are the spatial design strengths here and remain correct.
- **Bottom line:** UV_PURPLE drift is 8 cycles overdue for a fix; the warm debris presence in a zero-warm-light scene is either intentional (Real World remnants) or a color logic gap that needs a spec note.

### SF04 "The Dynamic" v004

**QA:** WARN | value range PASS | warm/cool separation=1.1 (FAIL) | SUNLIT_AMBER FAIL (delta=15.7°, 6,752 samples at hue 18.6°)

**Score: 66/100**
- **SUNLIT_AMBER at 18.6° hue — 15.7° FAIL.** The warm lamp on Luma is reading at a near-red/orange hue rather than SUNLIT_AMBER's golden-amber. This is the largest warm-light hue drift of any asset in the pitch. At hue 18.6° the lamp reads as firelight or sunset, not as a domestic interior lamp. The show's Real World warm light has a defined temperature (SUNLIT_AMBER #D4923A, hue 34.3°) and this style frame is 15.7° away from it. The C32 rebuild spec noted warm lamp "from upper-left" — but the color is not canonical.
- **Warm/cool separation at 1.1 FAIL.** The interaction scene between Luma (warm character, domestic context) and Byte (cold CRT light contributor) should be the most naturally differentiated warm/cool scene in the pitch. At 1.1 PIL separation, the two characters are reading from the same value zone. The scene's fundamental dramatic tension — warm human world / cold digital world reaching toward each other — is not visible as a spatial condition.
- The Byte BYTE_TEAL (PASS, 0.0°) and HOT_MAGENTA (PASS, 0.0°) are correct. The cold palette is handled correctly; the warm palette is not.
- **Bottom line:** The show's primary character-relationship scene has the wrong lamp color and the worst warm/cool separation of all four style frames — these are the two metrics that define whether the scene's emotional logic (warmth-meets-cold) can be read from across the room.

---

## Suite-Wide Assessment

**Priority actions for the team:**

1. **School Hallway** — Regenerate the PNG. The source code is already fixed. This is a one-line run. Every week this sits on disk with a 9.7° drift is a week of Real World palette inconsistency.
2. **Luma Study Interior** — This asset must be rebuilt from scratch. The show's inciting incident environment cannot remain a 31-cycle-old draft with failing warm/cool separation and no character-specific content.
3. **SF04 "The Dynamic"** — Fix the warm lamp hue to SUNLIT_AMBER canonical (34.3°). The current 18.6° reading is firelight, not domestic interior. Also address warm/cool separation (1.1 — worst of all four style frames).
4. **Glitch Layer / Other Side ENV** — Update UV_PURPLE_DARK to post-C28 saturation (58,16,96). One constant change, one regeneration. This is 8 cycles delinquent.
5. **Glitch Layer — HOT_MAGENTA fissures.** Add crack lines at platform edges. The world should show the same emotional register as the character who comes from it.
6. **Tech Den** — Rebuild the floor perspective (not a patch — the plank lines must converge to VP_X). Confirm SUNLIT_AMBER canonical presence with color_verify PASS.
7. **SF03 warm debris** — Add a spec note clarifying whether Real World debris objects at hue ~25° are intentional warm-adjacent solids or a color logic gap. If intentional, update the spec. If unintentional, desaturate.

**What is working:**
- Grandma's Kitchen v005: rebuilt, passing, warm — the show's emotional anchor is now spatially correct.
- Grandma's Living Room v001: promising new asset with excellent canonical color anchoring (SUNLIT_AMBER 0.2°) and the right CRT/lamp premise. Perspective needs one revision pass.
- SF01: the pitch's strongest environment integration.
- Glitch Layer color palette: still the only ENV with three confirmed canonical Glitch colors.
- School Hallway light logic: structurally correct once regenerated.

---

*Chiara Ferrara — Background Art and Environment Design Critic — Critique 16 — 2026-03-30*
