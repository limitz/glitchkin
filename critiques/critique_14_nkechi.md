# Critique 14 — Cycle 34
**Critic:** Nkechi Adeyemi — Pitch Quality & Narrative Coherence
**Date:** 2026-03-29
**Focus:** Luma expressions v009; SF02 Glitch Storm v006; full package coherence audit

---

## Pre-Critique QA Summary

`LTG_TOOL_precritique_qa.py` baseline: **WARN** (PASS=152, WARN=37, FAIL=0).
Key flags relevant to my review:
- Render QA: all 4 style frames WARN on warm/cool separation (SF04 worst: 1.1 PIL units — well below threshold of 20.0).
- Color Verify: SF04 SUNLIT_AMBER hue drift 15.7° (FAIL). This is a load-bearing warm tone; drift this wide means the warm/cool divide that the pitch brief names as the show's visual identity is not reliably present.
- Expression silhouette tool: Luma v009 = **FAIL** (worst pair Panels 1–2 at 86.8% similarity). Byte v005 = **FAIL** (worst pair Panels 7–8 at 88.1%).
- Lineup palette audit: `LTG_CHAR_luma_lineup.png` exits with FAIL — 3 WRONG LEGACY values detected (Byte shadow, Miri slipper). These are not FAIL on canonical values (canonical passes), but the legacy detector triggered. Non-blocking for the values themselves, but the audit tool is flagging residual generator debt.
- Glitch spec lint: G002 FAIL across all Glitch expression sheets and turnarounds — body mass ratio `ry` must exceed `rx` (diamond must read taller than wide), currently wider than tall in all generators.

---

## PRIMARY FOCUS — C34 Deliverables

---

### `LTG_CHAR_luma_expressions.png` — Luma Expression Sheet

**Score: 58/100**

- **FAIL silhouette differentiation (tool result: worst pair 86.8%).** The arm-differentiation work this cycle improved DELIGHTED (V-arms) and FRUSTRATED (crossed) in concept, but the silhouette test still fails two pairs at FAIL level and three at WARN. At pitch-deck thumbnail size, a buyer cannot distinguish these expressions without leaning in. This is the defining criterion for a pitch-facing expression sheet, and it is not met.
- **The SUNLIT_AMBER hue drift (9.2° in color verify) is a coherence failure.** The dominant warm tones on Luma's sheet are reading to the tool at hue ~25° rather than canonical 34.3°. This may be a skin-tone false positive (the C26 documented caveat), but the magnitude (9.2°) is outside prior false-positive range (~5–7°). Needs human confirmation — the team cannot assume false positive at this margin.
- **Interiority still absent.** C12 critique said: "one expression that is hers alone — not a generic emotion but the specific way Luma registers the world." This has not been addressed. All six expressions remain generic-catalogue states (SURPRISED, FRUSTRATED, WORRIED, DELIGHTED, CURIOUS, DETERMINED/NOTICING). The char spec linter returns WARN on L004 (5-curl rule unverifiable). The sheet is technically cleaner than v007 but still characterologically hollow. Luma's expression sheet does not yet tell us who she is — only what she does.
- **THE NOTICING (replacing one of the six) was explicitly requested in C12.** A face almost still but watching very hard. A child who notices things others walk past. This was the single most important correction requested. Two cycles later: not present. This is unacceptable.
- **v009 represents the 9th iteration of this sheet.** After 9 versions and 34 cycles of development, the protagonist's expression sheet should not be failing silhouette differentiation and should not be emotionally generic. Version count is not quality. This sheet has not arrived.

**Bottom line:** Nine versions in, Luma's expression sheet still fails its silhouette test and still shows a generic child, not this specific one — the C12 correction request for a character-specific expression has been deferred for two full critique cycles and is now overdue.

---

### `LTG_COLOR_styleframe_glitch_storm.png` — SF02 Glitch Storm (C34 Character Lighting Pass)

**Score: 72/100**

- **HOT_MAGENTA storm-crack bounce light passes color verify (delta 1.5°, n=1064) — this is a genuine improvement.** The addition of storm-crack ground bounce on characters is the right narrative instinct: the danger is physically landing on the people in it.
- **UV_PURPLE not detected in color verify.** The storm environment should carry UV Purple — it is part of the Glitch Layer's identity. Its absence from the style frame color profile means the storm reads as Cyan/Magenta dominant without the depth that UV Purple provides. This is a palette regression from what the show's color story requires.
- **Warm/cool separation: 6.5 PIL units (threshold 20.0) — WARN.** Given that SF02 is explicitly the "contested border" frame where warm domestic life and cold digital storm collide, a warm/cool separation score this low is a compositional indictment. The warm window glow story (v005) was excellent. The C34 character lighting additions may have flattened the overall separation.
- **ELEC_CYAN specular on Luma's hair: I need the team to confirm whether this is visible as a character-on-character relationship cue or simply a technical rim light.** A specular highlight that reads as "rim light for separation" is different from one that reads as "the storm is touching her." At the scale Luma is rendered (char_h 18% of frame), and with the hot-magenta bounce also present, there is a real risk these two light passes compete rather than compound. Confirmation via `scene_snapshot()` from procedural_draw v1.5.0 is the correct next step — not sending the image to Claude for visual inspection.
- **Luma's face still does not read as a character experiencing something.** The core C34 brief question: "does Luma's face now read as a character experiencing something?" The generator adds HOT_MAGENTA fill from lower-left and ELEC_CYAN rim from right. These are scene-reactive lighting passes. They are not the same as an expression. At char_h=18%, Luma's face is approximately 3.6% of frame height — roughly 26px tall at 720p. At that scale, lighting passes add mood but cannot substitute for the expression being designed to carry weight. The team is trying to solve an expression problem with a lighting solution. Those are not interchangeable.

**Bottom line:** The C34 lighting pass adds technically correct storm-reactive light to characters, but it does not answer the brief's question — Luma's face at 18% frame height cannot communicate "a character experiencing something" through rim lights alone, and the missing UV_PURPLE and low warm/cool separation suggest the storm's visual identity is weakening rather than sharpening.

---

## FULL PACKAGE COHERENCE AUDIT

---

### Pitch Brief — Emotional Premise

**Score: 74/100 (up from C (C12) — significant improvement)**

The revised pitch brief is genuinely better. The paragraph about Luma — "the kid nobody sees," "she tries to show people what she sees, nobody looks, she stopped trying" — is specific and true to the age group. The sentence about Byte ("not to be rescued, not to be studied, just to be *seen*") lands correctly. It names the emotional core in a way that a buyer can hold.

- **Still unresolved: the interior wound specificity gap.** "The kid nobody sees" is much better than "sees the world differently." But a buyer will ask: why doesn't anyone see her? Is it family? School? A specific relationship that failed? The brief names the symptom but not the cause. For a pitch meeting, this is probably sufficient. For a network greenlight, it is not yet.
- **Tone paragraph is strong and honest.** "The kind of trust that can only exist when one of you is technically imaginary" is a genuine line. It respects the audience.

---

### The 5 Environments — Tone Audit

**Do they collectively establish comedy-adventure about a kid who discovers digital creatures in her grandmother's CRT?**

The five active environments are: Grandma Miri's Kitchen (v003), Tech Den (v004), School Hallway (v002), Millbrook Main Street (v002), Glitch Layer (v002). Plus Classroom (v002) and Luma's House interior.

- **Grandma Miri's Kitchen: the strongest environment in the package.** CRT TV visible through doorway with desaturated glow, pre-digital appliances, lived-in details (crossword, tea mug, worn traffic path on linoleum). This environment tells the show's story before a character enters it. The grandmother's kitchen with a CRT that glitches — this is the premise made physical. It earns its place completely.
- **Tech Den: strong.** Three individuated monitor glow zones, window light shaft on desk surface. Cosmo's jacket on the chair. This environment communicates its character without its character being in it. That is the right standard.
- **School Hallway: functional but anonymous.** The low camera angle, institutional proportions, and human evidence (backpack, jacket) are correct. What this environment cannot do — and what the show needs — is communicate the *social world that makes Luma invisible*. The hallway is a well-constructed Millbrook Middle hallway. It is not yet the specific hallway where Luma's kind of attention goes unnoticed. No design choice says: this is where children pass each other without looking. This is a craft gap, not a blocking error.
- **Millbrook Main Street: technically complete, emotionally neutral.** Power lines, road plane, storefronts, human-evidence details. It establishes "small town." It does not establish why this particular small town is the right setting for a story about digital creatures and analogue warmth. All the correct elements are present; none of them are distinctive enough to linger in a buyer's memory.
- **Glitch Layer: the design is distinctive and the scanline overlay is correct.** Three-tier platform depth, void floor, aurora bands — this is a CRT interior made spatial. The contrast against the real-world environments is strong. This environment is doing its job.

**Collective verdict:** The five environments tell a consistent palette story (warm/cream/amber vs. void/cyan/purple). They establish the show's world clearly. What they do not collectively establish is the *emotional geography* of a story about invisibility — only the Kitchen and, partially, the Tech Den feel like they belong to this specific show rather than to a well-designed animated series generally.

---

### Character Lineup v006

**Score: 76/100**

- The lineup palette audit passes on canonical values — Luma hoodie, skin, Cosmo jacket, Glitch amber, UV purple, void black all correct. Tool exits FAIL due to legacy wrong-value detection (Byte shadow #0090B0, Miri slipper #5A7A5A) — these are historical wrong values now absent, but the detection confirms the generator carries legacy color logic that should be cleaned.
- **Glitch spec lint G006/G007 warnings persist across all lineup generators (v004, v005, v006).** Glitch's body in the lineup uses organic/warm fill values — not CORRUPT_AMBER family — and VOID_BLACK outline is undetected. If Glitch's rendered body in the lineup does not match the canonical CORRUPT_AMBER amber that makes Glitch visually distinctive, the five-character lineup is not accurately representing the show's visual language.
- **Five characters in a lineup communicates more show than four.** The addition of Glitch to v004 onward is the correct story decision: the antagonist needs to be present when you introduce the cast. Glitch's diamond body as visual antonym to the ensemble's rounded shapes reads correctly at lineup scale.
- **The lineup still does not communicate the emotional dynamic.** Five characters standing at relative heights tells a buyer who the characters are relative to each other. It does not yet tell them what the characters want from each other. For a show whose premise is a specific friendship, this is a persistent gap — though resolving it would require a more dynamic lineup composition, which may be outside the current pipeline's scope.

---

### Logo — `LTG_BRAND_logo.png`

**Score: 80/100 (strong; open for improvement)**

The asymmetric layout with amber-dominant "Luma" left and stacked cyan "the Glitchkin" right is the correct visual grammar for the show. The warm-to-cold "&" hinge is a piece of design that earns its place — it tells the story in four characters.

- **Render QA: warm/cool separation 0.0 PIL units.** The tool is not measuring the design intent here (the warm/cool story is horizontal, and the QA tool samples top/bottom zones). This is a false negative from the tool. Not a design problem.
- **The logo reads correctly as the title of a show that lives at the intersection of two worlds.** The bi-color scan bar is the right finishing detail.
- **What remains open:** At distance or small scale, does "Luma" read as the protagonist and "the Glitchkin" read as the antagonist/world? Or do both read as co-equal elements of a title treatment? A buyer who has not read the brief needs the logo to suggest that "Luma" is the human center and "the Glitchkin" is the strange thing she discovered. The weight hierarchy (Luma dominant, Glitchkin stacked smaller) is correct. Whether it is *sufficiently* dominant is worth testing with someone who has not seen the package.

---

### Byte Expression Sheet v005 — Retrospective Check

**Score: 78/100 (C12 correction partially met; new problem introduced)**

- **UNGUARDED WARMTH (10th expression) delivers on C12's core request.** Body leaning toward Luma, gold confetti (SOFT_GOLD — only this expression), star-and-heart pixel symbols, warmth mouth. The conceptual design is exactly right: an expression that exists only in relationship to Luma, marked by the SOFT_GOLD color that no other expression carries. A child watching this will understand: this is what Byte is like when Luma has won.
- **Silhouette test FAIL (worst pair Panels 7–8 at 88.1%).** A 10-expression sheet at 4×3 grid creates crowding. Two expressions at 88.1% similarity cannot be distinguished at thumbnail scale. The tool identifies the pairs — the team needs to identify which expressions they are and differentiate them. UNGUARDED WARMTH uses gold confetti for distinction, which is chromatic rather than silhouette-based; the tool measures silhouette only, so this expression may be one of the failing pairs despite being conceptually distinct.
- **Overall Byte emotional range: resolved.** NEUTRAL through STORM/CRACKED covers damage. RELUCTANT JOY and UNGUARDED WARMTH together cover the friendship's warmth arc. RESIGNED covers the key A2-02 beat. The range now tells the story of a character who is defended but can be reached.

---

### Glitch Expression Sheet v003 — Retrospective Check

**Score: 71/100 (significant improvement; structural issue persists)**

- **C12 demanded interior desire from Glitch. YEARNING, REACHING OUT, REMEMBERING respond directly.** This was the single most important correction I requested, and the addition of these three expressions is a genuine creative advance. YEARNING — if it is visually distinct from TRIUMPHANT — is the expression that makes Glitch a character rather than a villain.
- **G002 FAIL (Glitch spec lint): body mass ratio ry must exceed rx — diamond must be taller than wide.** This has been flagged across all Glitch generators (v001, v002, v003) and the turnaround. A diamond that reads wider than tall does not read as a diamond — it reads as a rhombus lying on its side. This is a Glitch body construction error that has persisted for multiple cycles. If Glitch's signature shape is geometrically wrong in every generator, every asset featuring Glitch is misrepresenting the character's design.
- **Silhouette test PASS (worst pair 71.1%).** This is the one expression sheet in the package that passes silhouette differentiation. The geometric body makes this easier than organic characters.
- **STUNNED remains the most emotionally accessible expression.** C12 said: "a Glitch who can be surprised has an inner model of the world." It is still true. STUNNED is doing more narrative work than CALCULATING.

---

### Grandma Miri Expression Sheet v003 — Retrospective Check

**Score: 84/100**

- **KNOWING STILLNESS remains the best single expression decision in the entire package.** The WISE/KNOWING distinction — same body pose, entirely different in the face — is sophisticated character writing. A child who watches Miri across multiple episodes will eventually register the difference. That is good long-game design.
- **C12 concern about over-signalling the suppressed smile is unresolved.** The spec still calls for a visible suppressed smile. A secret that is visible in the pitch package is not a secret in the show. The team should consider whether the KNOWING expression should be even more ambiguous — readable as knowing only in retrospect, not on first viewing.
- **Full-body silhouette differentiation across all 5 v002 expressions remains strong.** WARM/WELCOMING A-frame vs SKEPTICAL/AMUSED hip-tilt vs CONCERNED forward lean — these are character-level distinctions. Miri is still the most well-realised character in the package from an expression design standpoint.

---

### Style Frame Triptych — SF01 / SF03 / SF04 Coherence

**SF01 v005 (pitch primary): 79/100**
- Rim-light char_cx bug (canvas-midpoint) fixed in v005. Warm/cool separation 17.9 PIL units (just under 20.0 threshold — WARN but close). Color verify passes. Procedural quality pass (wobble outlines, variable stroke, face lighting) delivers on Rin's brief.
- **Luma's expression in SF01 still resolves the emotion too early.** C12: "discovery should have uncertainty in it. A 12-year-old who discovers something impossible does not immediately smile." The face is described as open-mouthed broadly smiling with blush on both cheeks. After 5 versions this remains unchanged. This is not a technical issue — it is a storytelling choice that has been locked in. It is the wrong choice for the show's emotional premise.

**SF03 v005 (pitch primary): 81/100**
- UV_PURPLE saturation fix (GL-04a 72% sat) delivers on Priya Nair C12 P1. Color verify flags UV_PURPLE hue drift 9.2° (borderline WARN). Confetti distribution fixed (C27). The inverted atmospheric perspective rule is the show's best piece of spatial storytelling.
- **Wonder still needs a focal event.** C12 requested a moment in this frame where Byte does something impossible — something that demonstrates belonging in this space. This has not been addressed. The frame is still an impressive landscape with figures, not a moment.

**SF04 v004 (pitch primary): 65/100**
- **SUNLIT_AMBER hue drift 15.7° (FAIL) is the package's most serious unresolved technical flag.** The warm/cool dual lighting of SF04 is the frame's entire emotional argument — Luma at the intersection of two worlds, warm left / cool right. If the warm tones are drifting 15.7° from canonical, the color story fails in the frame that is supposed to most directly show the friendship. The C30 audit confirmed this as present and pending Art Director decision since the SF04 Byte teal investigation — but no decision was recorded on SUNLIT_AMBER drift.
- **Co-presence without care persists.** C12: "two characters who need each other, not just two characters who are near each other." The gaze divergence is correct. A reaching or unconsciously-close element is still absent. This was the C12 correction request for this frame. Not addressed.

---

## OVERALL PITCH PACKAGE SCORE

**68/100**

The package is technically complete and visually coherent. The palette architecture (warm/analogue vs. cold/digital) is consistent. The environment set establishes the show's world. The storyboard arc tells a real story. The logo is right.

What the package still cannot do, after 34 cycles, is make a buyer feel in their chest what this show is about. The pitch brief knows the emotional premise. Luma's expression sheet does not embody it. SF02 and SF04 use lighting to approximate what expression should deliver. The protagonist's face — in the expression sheet and in the style frames — is still not the specific face of the specific child at the center of this specific story.

The show's best emotional design lives in the supporting and antagonist characters: Miri's KNOWING STILLNESS, Byte's UNGUARDED WARMTH, Glitch's YEARNING. These are all expressions about wanting something you don't have or knowing something you're not supposed to know. The protagonist's expression sheet — after nine versions — still shows a child who is happy, surprised, worried, and frustrated. It does not show a child who was invisible and is now seen.

That is the show. The show is not yet on Luma's face.

---

## Required Actions Before Next Critique

1. **Luma expression sheet v010: add THE NOTICING.** Replace one generic expression (DETERMINED is the weakest candidate) with the character-specific perception expression requested in C12 and not delivered in C13 or C14. A still face watching very hard. Asymmetric brow, slightly narrowed one eye, mouth not yet decided. This is Luma's signature expression. It must exist.
2. **Luma expression v009 silhouette differentiation: diagnose failing pairs.** Tool identifies Panels 1–2 (86.8%) and Panels 4–5 (86.1%). Team must identify which expressions these are and rebuild the weaker one's body language.
3. **SF04 SUNLIT_AMBER hue drift (15.7°): Art Director decision required.** Accept (document as intentional warm-lamp color under scene lighting) or fix. Cannot remain undecided.
4. **Glitch G002 (ry > rx rule): fix all generators.** Every Glitch asset currently has a wider-than-tall diamond body. This is the character's defining geometric shape. It must be correct.
5. **SF02/SF04 warm/cool separation: investigate.** SF02 at 6.5 and SF04 at 1.1 suggest the C34 character lighting passes may have blended warm/cool separation. The show's identity depends on this contrast being visible.
6. **Miri KNOWING STILLNESS: reduce legibility of the suppressed smile** so the expression reads as ambiguous on first viewing, knowable only in retrospect.

---

*Nkechi Adeyemi*
*Children's Media Critic — Pitch Quality & Narrative Coherence*
*BAFTA Children's Media Awards Jury 2014, 2018, 2022*
*2026-03-29*
