# Cycle 2 Color Critique — "Luma & the Glitchkin"
**Critic:** Naomi Bridges, Color Theory Specialist
**Date:** 2026-03-29
**Documents Reviewed:**
- master_palette.md v2.0
- scene_color_keys.md v2.0
- style_frame_01_discovery.md v2.0
- style_frame_02_glitch_storm.md v2.0
- style_frame_03_other_side.md v2.0
**Previous Grade:** B-minus
**Methodology:** Hex-level audit, contrast verification, cross-document consistency check, semantic rule verification, paint-department readiness assessment.

---

## Cycle 1 Feedback Resolution

### Issue 1 — Opacity-based shadow specifications
**Status: FIXED.**
All opacity-based shadow specs have been replaced with flat hex values throughout every document. Specifically: `#3D2F4F` (Shadow Plum Deep) introduced as a new swatch (RW-09b) to replace the former "Shadow Plum at 70%" spec. The color keys now carry explicit "do not use at any opacity" language at every shadow specification. The master palette's RW-09 entry carries the corrective note directly. This was the most systemic problem in Cycle 1 and it has been addressed completely.

### Issue 2 — Color Key 04 ambient fill violation (Sunlit Amber at 20%)
**Status: FIXED.**
Key 04 ambient fill corrected from `#D4923A` (Sunlit Amber) to `#FAF0DC` (Warm Cream). The correction is documented in both the color key header note and the master palette's RW-03 entry, which now carries an explicit callout: "NOTE: Sunlit Amber must not be used as a 20% ambient fill in Color Key 04." This level of cross-referencing is correct practice — the fix is in the document and the prohibition is anchored in the source. Palette ratios in Key 04 have been updated accordingly (+5% Warm Cream, +2% Warm Tan to compensate for the removed amber). The correction is coherent end-to-end.

### Issue 3 — Rust Shadow vs. Skin Shadow disambiguation
**Status: FIXED, with a residual concern noted below.**
RW-05 and RW-10b now carry detailed comparison notes spelling out the RGB channel differences (`#8C3A22` vs. `#8C5A38` — green channel 32-point gap, blue channel 22-point gap) and explicitly separating use cases: architectural/object surfaces vs. character skin only. The language is clear and unambiguous. The residual concern: in style_frame_01, the shelving wood shadow note references `#8C5A38` (Skin Shadow) first before walking it back toward Rust Shadow. That hesitation in the documentation reflects a real painter confusion risk. The fix is technically in place but the prose in Frame 01 still introduces Skin Shadow before correcting itself on the same line. A painter skimming at production pace may stop at the first value. Flag this for a line edit before paint department receives Frame 01.

### Issue 4 — Acid Green semantic violation (storm confetti)
**Status: FIXED.**
Frame 02 v2.0 removes Acid Green from storm confetti and provides a corrected specification: storm confetti uses `#00F0FF`, `#F0F0F0`, `#FF2D6B`, `#7B2FBE`. A conditional exception is carved out for Glitchkin-attributed particles with clear spatial-separation language. The master palette GL-03 entry carries a cross-reference note to Frame 02. Forbidden #8 is now explicitly codified in Section 4. The semantic rule is now written, cross-referenced, and enforced in the frame spec. This was handled correctly.

### Issue 5 — Byte visibility in cyan-dominant scenes
**Status: FIXED — solution is defensible though not ideal aesthetically.**
The Corrupted Amber outline exception (`#FF8C00`, 2px) is a production-sound solution to a genuine contrast problem. The condition rule (Byte below 15% of frame height in cyan-dominant environments) is specific enough to be actionable. The positioning change to Luma's LEFT shoulder in Frame 02 is a good secondary fix — it puts his void-black body against dark warm shadow rather than against the cyan-lit side. The narrative rationalization for the amber outline ("Real World homing signal") is acceptable handwaving for a production tool that painters need to apply.
One unresolved downstream concern: the condition trigger ("cyan-dominant environment AND smaller than 15% frame height") requires a paint supervisor to make a scene-by-scene judgment. There is no clear guidance for borderline cases where the ambient is partly cyan but not exclusively. This will need clarification before series production.

### Issue 6 — Hoodie/screen glow pixel grid separation (Frame 01)
**Status: FIXED.**
Zone A/Zone B protocol is well-defined. Zone B switches from `#00F0FF` to `#F0F0F0` fill with a 1px `#0A0A14` outline stroke. The blending mode table is now a proper table with specific layer names, blend modes, hex values, and application scopes. The critical rule against blending modes on master character fill layers is stated explicitly. This is the level of specificity paint departments need.

### Issue 7 — Blending modes unspecified in Frame 01
**Status: FIXED.**
The blending mode table in Frame 01 v2.0 is thorough and structured correctly: Screen for glow bloom and rim light; Multiply for scan lines; Normal for specular pops; Overlay for warm glass reflection. Layer ordering and application scope (which layers receive which mode) are called out. No ambiguity remains on this point.

### Issue 8 — Below-Void-Black exception undocumented
**Status: FIXED.**
GL-08a now carries a full exception note. Two permitted uses are explicitly defined (Byte crevices; platform void abyss). A maximum area coverage of 2-3% per frame is specified. Language prohibiting new uses without Art Director approval is in place.

### Issue 9 — Key 02 dominant color count (8 vs. standard 7)
**Status: FIXED — documented and formally argued.**
The exception documentation in Key 02 is rigorous: three-point justification (narrative necessity, micro-accent argument for the 8th color, Art Director approval notation). The argument that `#FAF0DC` at 5% is "functionally accent-tier" is legitimate from a visual-weight standpoint. The prohibition on any further expansion beyond 8 is a necessary guardrail and it is stated. This is the right approach to an exception — document it thoroughly, justify it precisely, and close the door behind you.

---

## Master Palette — Cycle 2 Assessment

The Cycle 2 master palette represents a substantial structural improvement. The shadow companion system is now comprehensive: every fill color in both the Real World and Glitch palette sections has a documented shadow companion hex. The DRW (Derived Real World) color section has expanded from roughly 6 entries in Cycle 1 to 17 named entries plus the ENV environmental table. This is correct scaling — as the style frames were developed, light-modification derivatives had to be captured so painters are not re-deriving them individually.

The Glitch Shadow Companion table in Section 2 is a good addition. Having a centralized table before the individual entries gives painters a quick-reference that does not require reading every entry for shadow guidance.

**Positive findings:**
- The distinction between `#1A1428` (Night Sky Deep, Real World) and `#7B2FBE` (UV Purple, Glitch ambient) is now explicitly stated in the RW-NS entry with language noting "not derived from the glitch palette, despite similar hue family." This distinction matters — painters confusing these two would break the visual separation of the worlds in nighttime scenes.
- Forbidden #9 (UV Purple as Real World shadow tone) and Forbidden #10 (Warm Cream/Soft Gold as large-area interior ambient fill) are new additions that codify exactly the kinds of errors that Cycle 1 produced. These are additions that demonstrate the team has internalized the feedback rather than merely addressed the letter of specific notes.
- The Cool Skin Shadow (`#7A5A7A`, RW-10c) now has an explicit "replaces Skin Shadow when cool/night" instruction. Cycle 1 did not make this substitution rule clear.

**Remaining concerns in the Master Palette:**

**Concern A — DRW-13b (`#8A6A7A`) and DRW-13 (`#4AB0B0`) terminology mismatch.**
DRW-13 is labeled "Glitch Layer Skin Highlight (Warm)" but its hex `#4AB0B0` is a cyan-tinted teal — not what a painter would describe as "warm." The "warm" label refers to its relative warmth compared to DRW-13b, but the entry header does not make that clear. A painter who encounters "Warm" in the name and looks at `#4AB0B0` will be confused. Rename to "Glitch Layer Skin Highlight (Cyan Bounce)" — which is more accurate and less misleading.

**Concern B — DRW-16 (`#9A7AA0`) is described as "the most complex single-surface color in the show" but has no shadow companion documented.**
Every other DRW entry carries a shadow companion reference. DRW-16 does not. A painter rendering Luma's right shoulder in Frame 03 needs to know what DRW-16 steps down to in its shadow zone. This is a gap. Low priority for Cycle 2 since DRW-16 covers a very small area, but it needs resolution before series production.

**Concern C — The ENV color table lacks scene-restriction language.**
The ENV entries are keyed to specific frames ("Frame 02," "Frame 03") but there is no explicit prohibition against using, say, ENV-06 (Terracotta under Cyan) in a non-storm scene. The DRW entries carry "Scene use" notes that function as implicit restrictions, but the ENV table format does not include this. If ENV-06 appears in a non-storm scene, it would make any terracotta wall read as though it is under cyan light even when it should not be. A "Restricted to:" column in the ENV table would close this.

---

## Color Keys — Cycle 2 Assessment

All four keys are improved. The structural issues (opacity specs, Forbidden violations) have been resolved as documented above. What follows is a technical pass on each key.

**Key 01 — Sunny Afternoon at Luma's House:**
This key is the cleanest in the document. The three-shadow architecture (Shadow Plum for warm surfaces, Deep Sage for green surfaces, Skin Shadow for characters, Deep Cocoa for deepest values, Shadow Plum Deep for cast shadows) is complete and internally consistent. The explicit "Do not use '#5C4A72 at any opacity'" language is the right corrective. Palette ratios total correctly. Electric Cyan at 2% as a trace accent is properly positioned.
One note: the use of `#5C4A72` (Shadow Plum) as the cast shadow for both the "cast shadow on floor" (Key 01) and the "shadow fill on cool surfaces" role means two different shadow types share a hex value. In production, a painter for Key 01 will need to distinguish between a shadow fill (diffuse, area fill) and a cast shadow (hard edge, projected from object) using the same hex. The document instructs on this correctly, but this is the kind of subtle distinction that breaks down when briefing large painting teams. Worth a supplementary note in a future revision.

**Key 02 — Nighttime Glitch Attack:**
The 8-color exception is properly handled as noted. The warm-cold horizontal split is clearly specified: ground level retains Real World warmth, sky is completely glitch-infected. The detail that `#050F14` is used for cast shadows under competing glitch lights (not `#0A0A14 at 80%`) is correct and specific.
One gap remains: the key specifies that "old shadows and new Cyan shadows are overlapping and creating double-shadow confusion" as an intentional lighting effect, but provides no hex value for what the overlap zone should read as. A painter rendering the zone where a moonlit Shadow Plum shadow and a Cyan cast shadow overlap needs to know the target value. The current spec leaves this to individual judgment, which in a scene already at 8 dominant colors means painters will likely introduce ad hoc values. Assign an explicit overlap target hex — likely something in the `#0A1A2A` range — before this key goes to paint.

**Key 03 — First Entry Into the Glitch Layer:**
The inverted atmospheric perspective rule is clearly stated and the depth progression is fully specified layer by layer (close = cyan and acid green; mid = data blue and UV purple; far = near-void). The `#050508` restriction is cross-referenced and applied correctly (shadow zones only; 2-3% maximum).
One significant gap: the key specifies Luma and Cosmo's skin via `#C4A882` (Warm Tan at 3%) as "the only Real World warmth" but does not cross-reference to DRW-11 (`#A87890`) for how that skin renders under the Glitch Layer ambient. A painter reading Key 03 in isolation would apply `#C4A882` directly — which is incorrect; the skin must be rendered as `#A87890` in this environment. The key needs an explicit line: "Under Glitch Layer ambient, `#C4A882` renders as `#A87890` — refer to DRW-11 and the Glitch Layer Skin Highlight system." This cross-reference is critical and it is missing.

**Key 04 — Quiet Emotional Moment:**
The Sunlit Amber correction is thorough and well-documented. The palette ratio adjustments (+5% Warm Cream, +2% Warm Tan) are internally coherent. The distinction between "a warm room (broad desaturated fill) and warm light striking surfaces (key light on specific shapes)" is one of the most technically valuable passages in this entire document set — it describes a lighting principle that separates skilled background painters from careless ones. Keep it.
The key is now compliant. No outstanding structural issues.

---

## Style Frames — Cycle 2 Assessment

**Frame 01 — The Discovery:**

The blending mode table is a significant upgrade. All six specified effects are fully described with layer names, blend modes, hex values, and scope. The prohibition on blending modes for master character fill layers is correctly placed.

The Zone A/Zone B hoodie grid protocol is clearly specified and solves the original legibility problem logically. `#F0F0F0` pixels with `#0A0A14` outline against `#BF8A78` base under Screen-blend `#00A8B4` glow creates three distinct readable layers. This is correct cel-animation color engineering.

**Residual Frame 01 issue — the shelving wood shadow note:**
As flagged in the Feedback Resolution section above, the Frame 01 background section reads: "Shelving wood ... `#8C5A38` in shadow (note: this is a wood surface, not skin — ... however preference is `#8C3A22` Rust Shadow for wood grain in shadow to maintain use-case discipline)." The correction is present but buried in a parenthetical. Paint department briefs should present one definitive value, not a value followed by a correction. This line should read: "Shelving wood in shadow: `#8C3A22` (Rust Shadow)." Full stop. Remove the Skin Shadow reference from this line entirely. The existing text undermines the very use-case separation the master palette is trying to enforce.

**Pixel confetti physics governing rule is correctly established in Frame 01** and propagates correctly to Frames 02 and 03. Size scaling, source-proximity density, and the anti-re-animation note in Frame 03 are all coherent with the originating spec. Cross-frame consistency on this point is good.

**Frame 02 — Glitch Storm:**

The Byte visibility solution is practical and the implementation spec (2px `#FF8C00` outline, separate layer, left shoulder repositioning, cracked eye facing crack) is specific enough to execute without ambiguity. The narrative rationalization for the amber outline is acceptable.

The corrected storm confetti spec is executed correctly. Acid Green removed from storm particle set. Conditional Glitchkin attribution exception is bounded by spatial-separation language.

**Remaining Frame 02 issue — Luma's laces in storm:**
The spec notes that Luma's `#00F0FF` laces "merge with the scene's ambient Cyan light — a small detail; they are present but do not read distinctly." This is accepted passively rather than solved. In a wide shot this reads as a minor rendering failure — a character detail goes invisible in a specific scene type. The correct solution is to note that in storm-wide-shot conditions, Luma's shoe laces use `#F0F0F0` (Static White) rather than Electric Cyan for visibility. This is a one-line fix and it should be in the spec rather than accepted as a known deficiency.

**Frame 02 issue — ENV-07 deep warm shadow value:**
`#5A3820` is listed as ENV-07 for building shadow sides in the storm. The value is not in the master palette as a named swatch. It falls between Rust Shadow (`#8C3A22`) and Deep Cocoa (`#3B2820`) in the warm-dark range, but has no parent, no shadow companion, and no use restriction. An ENV value that exists only in the frame spec without a corresponding master palette entry creates a color that painters will re-derive inconsistently across scenes. Either add ENV-07 to the master palette formally, or map it to the nearest named swatch with a "derived from" note.

**Frame 03 — The Other Side:**

The Glitch Layer Skin Highlight Variants table is a genuine improvement. The three-row skin variant system (standard warm tan, cooler warm tan, hypothetical darker skin) with base/shadow/highlight for each is exactly the kind of systematic documentation that scales to series production. The rule of thumb ("warm orange-tan = standard; neutral to slightly cool tan = DRW-13b") is usable by a non-specialist.

The "absence of warm light" as an explicit narrative and color design statement is the most emotionally articulate passage in the entire document set. It belongs in the series bible.

**Remaining Frame 03 issue — Key 03 cross-reference gap:**
As flagged in the color key assessment, the frame spec does not reference DRW-11 explicitly in its lighting breakdown. Frame 03's "Effect on Luma: skin becomes `#A87890`" appears in the lighting section, but a painter working from Key 03 without also reading Frame 03 will miss this. The fix belongs in Key 03, not Frame 03.

**Frame 03 issue — `#7B2FBE` edge lines at "very low opacity" in far-distance structures:**
The far-distance spec reads: "Structure edges (barely visible): `#7B2FBE` lines at very low opacity." This is an opacity specification — the exact type of error the Cycle 2 revision was supposed to eliminate throughout the documents. A flat hex value must replace this. If the intent is that these edges are nearly invisible, specify `#2A1040` or `#3A1060` (Deep Digital Void) as the flat hex edge value at that distance layer. "Very low opacity `#7B2FBE`" is not a paintable instruction.

---

## System Coherence — Updated Assessment

**Improved from Cycle 1.**

The cross-document hex consistency is substantially better. The Cycle 2 change summary notes in all five documents align: every document acknowledges the same set of changes and they are consistent across documents. Version numbers are synchronized (all documents are v2.0, dated 2026-03-29).

The shadow companion system is now a genuine system rather than a collection of isolated notes. It operates consistently: every fill has a companion, companions stay within their hue family (Cyan shadows to Deep Cyan, not to grey; Magenta shadows to Magenta Shadow, not to brown), and the system is documented in a central table in Section 2.

The semantic rule architecture (Acid Green = positive; UV Purple = Glitch shadow; Shadow Plum = Real World shadow; Void Black = Glitch deep) is now explicit, cross-referenced, and enforced in the Forbidden section. This is a functional color-semantic framework.

**Remaining coherence gap:** There is no master list of all DRW and ENV codes in a single reference location. They are scattered across Section 1B (DRW), Section 1C (ENV table), and the individual style frame documents. A production-ready document set needs a one-page quick-reference appendix that lists all DRW and ENV codes with their hex values, source colors, and applicable scenes. Painters should not have to search three documents to confirm a light-modification value.

---

## New Issues Found

**New Issue 1 — DRW-13 label is misleading.**
DRW-13 is labeled "Glitch Layer Skin Highlight (Warm)" but the hex `#4AB0B0` is a cyan-teal — not warm by any standard color temperature definition. Rename to "Glitch Layer Skin Highlight (Cyan Bounce)" or "Glitch Layer Skin Highlight (Platform Glow)" to prevent painter confusion. The "warm" label was presumably relative to DRW-13b, but context is not established in the entry header.

**New Issue 2 — No guidance for Key 03 skin rendering.**
Color Key 03 lists `#C4A882` Warm Tan at 3% as the skin presence in the Glitch Layer but does not instruct painters to apply the DRW-11 system. A painter working Key 03 without Frame 03 will render Luma's face in standard warm tan — a fundamental color error for the Glitch Layer environment.

**New Issue 3 — Frame 03 contains a surviving opacity specification.**
"Structure edges (barely visible): `#7B2FBE` lines at very low opacity" — this is an opacity-based spec in a document that is supposed to have eliminated all opacity-based specs. The error is small-area, but it is a direct regression from the Cycle 2 stated objective. Replace with a flat hex.

**New Issue 4 — ENV-07 has no master palette entry.**
`#5A3820` appears in Frame 02 as a named environmental code but has no corresponding swatch in the master palette. If this value is used across multiple storm-type scenes, it will be re-derived inconsistently. It needs either a formal master palette entry (RW or ENV section) or a "derived from" mapping to existing swatches.

**New Issue 5 — DRW-16 has no shadow companion.**
Every other DRW entry documents a shadow companion hex. DRW-16 (`#9A7AA0`, Shoulder Under Waterfall Blue) does not. In a highly complex surface like a blue-light-lit hoodie shoulder in the Glitch Layer, painters need to know the shadow value. Gap to fill before series production.

**New Issue 6 — Byte visibility condition rule needs a borderline case definition.**
The "cyan-dominant environment AND Byte below 15% frame height" trigger for the Corrupted Amber outline exception does not define "cyan-dominant." A scene with equal cyan and magenta ambients is ambiguous. A scene where cyan is the key light but not the fill is ambiguous. Paint supervisors need either a specific percentage threshold ("cyan light covers 30%+ of the frame's ambient") or a scene-type list ("applies in: storm scenes, Glitch Layer scenes, any scene where Electric Cyan is listed as Key or Fill light in the color key").

**New Issue 7 — Key 02 double-shadow overlap zone has no target hex.**
The shadow overlap zone where moonlight Shadow Plum and Cyan cast shadows intersect in Key 02 is specified as an intentional effect but given no target value. Assign one before this key goes to production.

---

## Remaining Problems

Ranked by production impact:

1. **Key 03 missing DRW-11 cross-reference** — Will produce incorrect skin rendering in the Glitch Layer if not fixed before paint. High impact. Simple fix.

2. **Frame 03 opacity regression** — Direct regression from Cycle 2 stated objective. Must be corrected for consistency.

3. **Frame 01 shelving wood shadow prose** — Introduces Skin Shadow before correcting to Rust Shadow. Will cause painter error at production pace. Simple line edit.

4. **Key 02 double-shadow overlap zone** — Ambiguous instruction in a complex scene. Will produce ad hoc color values from individual painters.

5. **ENV-07 not in master palette** — Color used in Frame 02 with no master swatch. Will drift across productions.

6. **DRW-13 label misleading** — Will cause confusion. Low-risk but easily fixed.

7. **DRW-16 shadow companion missing** — Incomplete entry in a system that is otherwise complete.

8. **Byte visibility condition ambiguity** — Will produce inconsistent application in series. Needs definition before episode production begins.

9. **No centralized DRW/ENV quick-reference appendix** — Not a blocker for the current three style frames, but a serious inefficiency at series scale.

---

## Recommendations

1. Add a one-line cross-reference to DRW-11 in Color Key 03 under the Warm Tan skin spec: "Renders as `#A87890` (DRW-11) under Glitch Layer ambient. See Frame 03 Skin Highlight Variants table."

2. Replace the opacity spec in Frame 03 far-distance section with `#3A1060` (Deep Digital Void) or `#2A1040` as a flat hex edge value.

3. Edit Frame 01 background section to remove the Skin Shadow reference from the shelving wood shadow note. One value, one use.

4. Assign an explicit hex for the Cyan/moonlight shadow overlap zone in Key 02. Suggested target: `#0A1A2A`.

5. Add ENV-07 to the master palette as either a named Real World swatch or a documented derivation from Rust Shadow / Deep Cocoa.

6. Rename DRW-13 to "Glitch Layer Skin Highlight (Cyan Bounce)."

7. Document a shadow companion for DRW-16. Suggested: something in the `#5A4060` range (UV Purple family deepened by the warm orange base).

8. Clarify the Byte outline exception condition to define "cyan-dominant" with either a percentage threshold or a scene-type list.

9. Add a Luma storm-shoe-laces note to Frame 02: `#F0F0F0` replaces `#00F0FF` on laces in storm-wide-shot conditions.

10. Before series production, build a one-page DRW/ENV quick-reference appendix and include it as an appendix in the master palette.

---

## Updated Verdict

**Grade: B+**

Cycle 2 delivered exactly what was asked of it on the primary structural issues. The opacity elimination is complete and the corrective apparatus (Shadow Plum Deep as a new swatch, explicit "do not use at any opacity" language in every shadow spec) is thorough enough to survive production. The Key 04 ambient fill correction is fully executed end-to-end. The Acid Green semantic fix is codified and enforced. The blending mode specifications are now production-ready. The skin shadow disambiguation is in place.

The shadow companion system is a genuine upgrade — it converts what was a patchwork of shadow references into a real architectural framework. The Glitch Layer skin variant table is the most practically valuable new addition in this cycle, and the "absence of warm light" conceptual framing in Frame 03 shows color design intelligence, not just technical compliance.

The remaining issues are real, but they are narrower and more localized than Cycle 1. There is no longer a systemic opacity problem across all documents. There is no longer a semantic violation of a core palette rule in the style frames. What remains are gaps, cross-referencing failures, and one regression — all of which are correctable without structural revision.

The document set is approaching paint-department readiness. It is not there yet. The Key 03/DRW-11 cross-reference gap is a genuine production risk — it would produce incorrect Glitch Layer skin rendering from a painter working only from the color key. The opacity regression in Frame 03 is a direct failure of the Cycle 2 stated objective. These two items in particular must be resolved before this document set is handed to a paint supervisor.

Do the seven specific fixes listed above. Add the quick-reference appendix. Then this is production-ready.

Not a celebration. A B-plus means the work is close. It means the remaining problems are the kind that lose a production its visual coherence quietly, over time, frame by frame. Fix them before they become systematic.

---

*Critique completed: Naomi Bridges — 2026-03-29*
*Reviewing: Cycle 2 documents v2.0 across all five color design files*
