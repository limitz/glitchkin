# Critique 11 — Character Design Authority Review
## "Luma & the Glitchkin" — Pitch Package Character Assets

**Critic:** Kwame Asante — Character Design Authority & Construction Purist
**Date:** 2026-03-29
**Cycle:** 24
**Assets Reviewed:**
- `output/characters/main/` — all expression sheets (v004 series), turnarounds, lineups
- `output/characters/color_models/` — color model PNGs
- `output/production/character_sheet_standards.md`
- `output/characters/main/character_export_manifest.md`

---

## Overall Verdict

**Grade: B-**

This is a package that has been worked and reworked over many cycles, and the cumulative effect of that labour is visible — mostly for the better, occasionally for the worse. The production standards document (v001) is genuinely professional: it articulates line weight tiers, construction logic, and thumbnail readability as binding requirements, and several characters show evidence of those standards being applied. Grandma Miri's expression sheet is the most improved asset in the package and deserves acknowledgment. Byte remains the strongest individual character design — coherent, legible, show-specific, animation-ready.

However, this is not a package that can be called excellent without reservation, and excellence is my threshold. Three fundamental problems persist. First: Luma's expression sheet does not deliver the body language the show requires of its protagonist. Second: Glitch is criminally undersized and visually illegible at any practical viewing scale, and this is not a minor production footnote — it is a pitch-facing antagonist who disappears on the page. Third: the character-to-character construction language is inconsistent across the cast; several characters appear to inhabit different shows. A buyer should be able to look at the full lineup and see a single unified graphic world. They cannot do that yet.

I can see what the team was trying to do. On Luma, I can see the attempt at confident cartoon construction — the hat mass, the A-line hoodie, the circular head. That is worse than not being able to see it, because the attempt is not the execution.

---

## Asset-by-Asset Findings

---

### 1. LUMA — Expression Sheet v004

**Annotation count: 9**

**1.** The expression sheet is predominantly a head sheet wearing a body accessory. In every panel, the lower body — hoodie, hands, legs — is present but makes no expressive contribution. CURIOUS, DETERMINED, and FRUSTRATED read identically from the waist down. This directly violates the show's own char_refinement_directive (Part 1, Standard 3): "Cover the face. The body geometry alone must communicate emotional register in every expression pose." It does not.

**2.** CURIOUS and DETERMINED are not silhouette-distinguishable at thumbnail scale. Both show a centre-weighted upright figure with arms in an identical floating-neutral position. The CURIOUS forward lean claimed in the QC notes (manifest: "CURIOUS forward lean confirmed") is not legible in the rendered output. If it exists in the generator at -8°, it is not reading. The two poses share a thumbnail silhouette, which is a direct criterion failure.

**3.** DELIGHTED claims an "arm-raised silhouette differentiator" in the QC notes. Looking at the rendered sheet: one arm raises marginally. The silhouette differential between DELIGHTED and SURPRISED is insufficient at squint scale. These must read as categorically different body states, not as small positional variations.

**4.** The hat — a critical, show-specific silhouette element — is positioned and scaled identically across all six panels with zero expression-based adjustment. The hat is a flat disc perched on the head. In animated character design, a hat participates in performance: it tips, it shifts forward on focus, it lifts on alarm. This sheet shows a hat that is bolted on. That is not animation-readiness — it is a prop that ignores its host's emotional state.

**5.** Brow differentiation between WORRIED and FRUSTRATED is too subtle. Both show medially-lowered brows above rounded eyes. The distinction at small scale is one of degree, not of shape. These two expressions currently require the label to be read before the emotion can be identified. That is a failure condition by this production's own stated standard.

**6.** SURPRISED is the only expression on this sheet that achieves full three-level expression (eyes, mouth, body) with any conviction — the open mouth and eye aperture change create a readable delta. It is the one pass.

**7.** The turnaround (v001) shows Luma as a silhouette-only rendering. This is correct for construction verification. However, the front silhouette and the side silhouette reveal a problem: the A-line hoodie reads as a flat skirt shape in side profile. The side view has almost no depth differentiation between the chest plane and the hem plane. This means the character collapses to a nearly 2D shape from the side — which is not a problem on an expression sheet but will be a production problem the moment a layout artist needs Luma at any angle other than 3/4.

**8.** The turnaround was produced in Cycle 10. The manifest acknowledges the Act 2 standing pose work (v002) is NOT integrated into the turnaround, and flags this as a known production gap. That gap is still open. A pitch package cannot have its protagonist's construction document out of sync with her current proportions. This is not a minor inconsistency — it means the turnaround is lying to anyone who uses it.

**9.** No color model PNG exists for Luma. The color documentation lives in a markdown file. The art director's own self-assessment names this as a vulnerability. I agree, and I am registering it here as a formal defect, not merely a polish item: a character design package for a pitch is incomplete without a visual palette reference for the lead character.

---

### 2. BYTE — Expression Sheet v004 + Turnaround v001

**Annotation count: 5**

Byte is the strongest character in this package. The design is coherent, show-specific, and demonstrates genuine construction thinking: the oval body reads at every scale, the pixel face-plate provides a clear focal point, and the arm-position language is actually doing expressive work across expressions. This is what animation-ready character design looks like.

**1.** RESIGNED and POWERED DOWN remain too similar in body silhouette. The directive (C17) flagged this explicitly. RESIGNED has a slightly tilted body and droopy lid; POWERED DOWN shows a flat, low posture. At thumbnail scale — a genuine squint test — both read as "deflated oval with retracted limbs." The stipulated droopy_resigned lower lid is present but it operates at detail level, not at silhouette level. One of these expressions needs a macro silhouette change: a distinct arm position, a significant body axis shift, something that reads at 10% scale without the face information.

**2.** The STORM/CRACKED panel uses a different background color (darker, with scatter lines) and a different rendering mode (the crack void treatment). This is visually correct and the expression is the most dramatic thing on the sheet. However, the crack line as rendered is a single void-black diagonal — it reads as a line, not as structural damage. The distinction between a crack and a line requires some asymmetric deformation of the surrounding form. Currently it looks like someone drew a line on a face. If this is the character's most extreme emotional state, it must look like the character is breaking, not annotated.

**3.** The RELUCTANT JOY arm asymmetry (arm_l_dy=-2, resistance signal) is too subtle. The resistance reading — one arm barely dropping below neutral while the other complies — is a concept that sounds strong in a spec document and disappears in execution at production scale. The RELUCTANT element is invisible without the label. This is exactly the note I make on every sheet that relies on parameter-level differentiation rather than actual graphic change.

**4.** Turnaround: the FRONT, 3/4, SIDE, BACK silhouettes are consistent and read correctly. Byte is construction-stable across angles. The side view is the strongest: the oval body with the faceplate depth and the arm stub give genuine 3D information. This is a turnaround that does its job.

**5.** No color model PNG exists for Byte. Same defect as Luma. The spec exists in markdown only.

---

### 3. COSMO — Expression Sheet v004 + Turnaround v002

**Annotation count: 7**

Cosmo is a character the team clearly understands conceptually — the rectangular head with glasses as a key silhouette element is a strong design choice — but the execution has unresolved problems that have been sitting in the notes for multiple cycles.

**1.** The storyboard annotations in each panel (A2-03, A2-06, A2-05b etc.) have no business appearing on a pitch-facing expression sheet. An expression sheet is a character model reference, not a storyboard index. These panel codes read as production housekeeping bleeding onto a presentation document. Remove them from the pitch export. They undermine the professionalism of the sheet immediately.

**2.** The "← was / → next" beat annotations (state machine labels) in the lower third of each panel: I have a specific position on this. On an internal production document, these annotations are useful. On a pitch-facing sheet, they telegraph unresolved process thinking. A buyer does not need to see "→ next: RESIGNED / RECALIBRATING" — they need to see that FRUSTRATED/DEFEATED is a clear, confident, readable expression. The annotations suggest the team is still narrating what the expressions mean rather than trusting the design to communicate it. Internal reference only.

**3.** FRUSTRATED/DEFEATED and NEUTRAL/OBSERVING — at thumbnail, these two share an upright rectangular body silhouette with arms at sides. The body differentiation between defeated and neutral is present (brow, mouth) but again operating at facial detail level. A defeated character folds; the body mass drops; the spine curves. Cosmo defeated should have a measurably different centre of gravity than Cosmo neutral.

**4.** WORRIED (A2-02) has the same body mass distribution as NEUTRAL. Two different head tilts and a changed brow cannot carry the weight of this distinction. The body needs to commit.

**5.** The glasses are the defining silhouette element for Cosmo — the 7-degree tilt and the circular lens pair are immediately readable and distinctive. This is a strong design decision that works. But the glasses sit absolutely flat against the face in the 3/4 views visible in the lineup — they become a surface decal rather than a physical object that sits on a nose. A character who wears glasses as their primary identity marker must have those glasses behaving like physical objects in all views.

**6.** The SKEPTICAL expression fix (arms near-neutral, body_squash=0.92) is documented as a resolved issue. Looking at the rendered sheet: SKEPTICAL and NEUTRAL/OBSERVING are nearly indistinguishable in body posture. A 0.92 body squash at this scale is imperceptible. The fix is technically present and visually absent.

**7.** Turnaround (v002): The side view silhouette of Cosmo is an almost perfectly flat rectangle. The character's depth profile is essentially zero — from the side, there is no chest projection, no shoulder taper, no waist indication. This is a character that works only in front and 3/4 views. That is exactly what I will not accept.

---

### 4. GRANDMA MIRI — Expression Sheet v002 + Turnaround v001

**Annotation count: 4**

The best expression sheet in the package, and it is not close. Five distinct full-body postures that actually communicate five different emotional states at thumbnail scale. The WARM/WELCOMING (arms slightly open, upright) vs. WISE/KNOWING (compact, contained posture) vs. SKEPTICAL/AMUSED (arms crossed, hip engagement) vs. CONCERNED (forward lean) is genuine expression depth. This is what the rest of the cast's sheets should be doing.

**1.** The turnaround is rendered at small scale and the color palette is significantly muted against the parchment-tone background — the character nearly disappears in the BACK and SIDE views. A turnaround must read as a clear construction document. The Miri turnaround does not serve a production artist trying to model or animate this character. Increase contrast between character and background, or darken the line weight, or both.

**2.** The bun-and-chopstick silhouette element is the strongest silhouette read in the show — it is immediately distinctive and belongs only to this character. However, in the BACK view on the turnaround, the chopstick pair is rendered with such low contrast against the dark bun mass that it disappears. The turnaround is failing to communicate the construction of its most distinctive element.

**3.** The CONCERNED expression: the spec (C17 directive) stipulates "subtle — it must not read as dramatic worry." It does not read as dramatic worry, but it also barely reads as concern. The eyes-first subtlety concept is sound but at this rendering scale and style, the subtlety tips into illegibility. The expression reads nearly identical to NEUTRAL from the bottom half of the frame. This is a case where the design intent (Miri expresses worry privately) has been taken so literally that the expression loses function as a production reference.

**4.** The sixth panel on the 3×2 grid (per standards: "last panel intentionally empty or used for credit") — it is empty. The standards allow this; I am noting it is a missed opportunity. Five expressions is not enough for the most narratively important supporting character in the show. Miri is where the emotional core of this series lives (based on every storyboard and spec I've read). She deserves a sixth expression.

---

### 5. GLITCH — Expression Sheet v002 + Turnaround v001 + Color Model v001

**Annotation count: 7** *(borderline — the art director's own self-assessment identified the core problem but chose to defer)*

The design concept is strong. A diamond/rhombus body form against a cast of rounded organic shapes is an immediately legible visual antonym, and the CORRUPT_AMBER palette correctly reads as digital-danger without being generic. The dual-pixel-eye glyph system is intelligent character writing. I believe in this design as a concept.

The execution at the pitch presentation stage is, plainly, inadequate.

**1.** The Glitch expression sheet is 800×800 pixels with each panel at 400×400. Glitch's body occupies approximately 25-30% of each panel — that is roughly 100×120 pixels of actual character per panel. At any normal viewing distance, at deck scale, at the scale a buyer would see this in a presentation, this character is a small orange diamond in a large dark square. The art director flagged this in their self-assessment and called it a vulnerability. It is worse than that. It is an antagonist who has been made visually irrelevant by the scale of their own reference document.

**2.** NEUTRAL and MISCHIEVOUS are still not reliably distinguishable at viewing distance. MISCHIEVOUS shows a 20-degree tilt and arm asymmetry per the QC notes — at 100 pixels of rendered figure, these parameters are imperceptible without a magnifier. The claimed silhouette differentiation (manifested as a body tilt + arm diagonal) exists in the generator; it does not exist in the visual output at pitch scale.

**3.** PANICKED reads as a slightly rotated NEUTRAL with confetti. The claimed improvements (tilt=-14, squash=0.55, asymmetric arms) are a specification fix, not a visual fix. The squash to 0.55 on a shape this small produces a figure that reads as smaller, not more distressed. Panic requires a macro graphic statement — the whole body commits to panic. This character's body is too small and too geometrically regular to carry the performance at this scale.

**4.** The turnaround: Glitch is rendered at the same relative scale problem — tiny diamond in the centre of a very large, very dark canvas. The SIDE view is a near-featureless diamond wedge. The turnaround communicates almost nothing about how this character behaves volumetrically. The only view with readable information is the FRONT and 3/4, and even there the detail (pixel eyes, crack accents, arm stubs) is operating below legible scale.

**5.** Four expressions is insufficient for an antagonist character. Every major character on the cast has 5-9 expressions. Glitch has four. An antagonist who can express NEUTRAL, MISCHIEVOUS, PANICKED, and TRIUMPHANT covers approximately one-third of the emotional range required by a comedy-adventure villain. Where is CONTEMPTUOUS? Where is GENUINELY FRIGHTENED (when the tables turn)? Where is CHARMING/MANIPULATIVE (villains who are only threatening are boring)? This character is being treated as a visual accent rather than as a full member of the cast.

**6.** The color model is the one Glitch asset that works. The 10-color palette is clean, properly labeled, and visually distinct from all protagonist palettes. The CORRUPT_AMBER / UV_PURPLE / HOT_MAGENTA combination is exactly right. If the character were rendered at a size where these colors could actually be seen in context, this would be a strong color model. As presented, the model swatches are more legible than the character they describe.

**7.** The glitch label on the Glitch expression sheet reads "STORM/CRACKED" in the manifest but that is Byte's expression. Looking at the actual Glitch sheet: the label is simply "NEUTRAL, MISCHIEVOUS, PANICKED, TRIUMPHANT." Fine. But the v001 sheet was superseded for "expression differentiation issues" — the v002 is pitched as the fix. Looking at the rendered output at actual scale: the differentiation issues are attenuated, not resolved. The body tilt and arm changes exist as generator parameters. They need to exist as visible graphic statements.

---

### 6. CAST LINEUP v004

**Annotation count: 3**

**1.** The lineup confirms the relative scale relationships correctly and Glitch's diamond form reads well as a visual contrast to the organic cast. This is the one context in which Glitch's small scale is appropriate and intentional — the character is meant to be compact relative to Luma and Cosmo. The engineering annotations (head unit markers, height lines, float gap callout) are well-executed and useful.

**2.** However: Cosmo's side profile in the lineup (inheriting the same problem from the turnaround) reads as a flat rectangle with no front-to-back depth. From the front, Cosmo is the tallest character and has the most distinctive silhouette. From any rotated angle in actual animation, Cosmo will have this depth problem. The lineup reveals it by placing all characters at full front view — which is the only view that works for Cosmo.

**3.** The lineup does not include Glitch in a coloured view that shows the CORRUPT_AMBER palette. All other characters are rendered in colour; Glitch appears in amber but the pixel eyes, crack lines, and accent colours are not visible at lineup scale. A buyer's first impression of the antagonist from the lineup is: small orange diamond. That is not a strong introduction to a villain.

---

## Specific Required Improvements (Prioritised)

### PRIORITY 1 — CRITICAL (Blocks pitch quality)

**P1-A: Rebuild Glitch expression sheet at adequate scale.**
800×800 is not a pitch document — it is a thumbnail. Regenerate at minimum 1200×900, 3×2 grid. Four expressions leave two panels available: use one for "IN DEVELOPMENT" or an additional expression; use one for a side-by-side scale comparison with Byte (the closest size reference). The character must be large enough for the expression differentiation work to actually show.

**P1-B: Luma body language — full rebuild of expression sheet.**
CURIOUS, DETERMINED, WORRIED, and FRUSTRATED cannot share the same lower-body template. Four of six expressions have no below-neck differentiation. This is the protagonist. If a buyer cannot read Luma's emotional state from the neck down, the character design is not finished. Minimum fix: commit to distinct arm and torso positions for each of the six expressions such that they are thumbnail-distinguishable without facial information.

**P1-C: Generate visual color model PNGs for Luma, Byte, and Cosmo.**
The art director identified this. I am upgrading it to CRITICAL. A pitch package for a visually-driven animated series cannot have three of its five characters documented in markdown only. This is not a documentation preference — it is a presentation competency issue.

### PRIORITY 2 — HIGH (Visible deficiency in pitch review)

**P2-A: Cosmo's side profile — depth problem.**
The side view of Cosmo must communicate the front-to-back thickness of a physical body. Currently the character is architecturally impossible from the side. Any director of layout or background artist will flag this on day one of production. Fix the construction logic so the side view reads as a real form.

**P2-B: Remove production annotations from Cosmo's pitch-facing expression sheet.**
Storyboard scene codes and state-machine transition labels are internal production tools. They do not belong on a pitch document. Strip all A2-xx labels and the "was/next" beat annotations from the pitch export version. Create an internal production version with those annotations if required.

**P2-C: Luma turnaround — reconcile with Act 2 proportions.**
The turnaround was produced in Cycle 10. The current canonical Luma proportions are from the Act 2 work. These must agree. An animator using the Cycle 10 turnaround is working from wrong information. This gap has been open for multiple cycles. It must close.

**P2-D: Byte — RESIGNED vs POWERED DOWN silhouette differentiation.**
The two lowest-energy Byte states share a macro silhouette. One of them needs a structural change at body level, not at detail level. This was identified in C17 and remains unresolved.

### PRIORITY 3 — SIGNIFICANT (Reduces quality but does not block pitch)

**P3-A: Miri — turnaround contrast and chopstick legibility.**
The turnaround nearly disappears on its background. The BACK view must read as a production document. The defining bun-and-chopstick silhouette must be visible from behind.

**P3-B: Miri — sixth expression.**
The most emotionally important character in the show currently has five expressions on a sheet with space for six. Add an expression. GENUINE LAUGH is the obvious missing entry and is already specified in the C17 directive.

**P3-C: Byte — STORM/CRACKED crack treatment.**
A crack rendered as a single void-black line is a line, not damage. The surrounding form must deform at the crack point for the structural damage reading to land.

**P3-D: Glitch — expand expression count.**
Four expressions is insufficient for an antagonist in a comedy-adventure format. CONTEMPTUOUS and CHARMING/DECEPTIVE are the minimum additions needed to make this character feel fully designed rather than partially developed.

---

## What Works Well

**Byte** is the best character in this package by a significant margin. The design is coherent, distinctive, animation-ready, and consistent across all assets. The oval body, the pixel faceplate, and the arm-language system work together as a unified design system. The STORM/CRACKED concept (even if the crack rendering needs work) demonstrates a designer thinking about what this character uniquely requires rather than applying a generic expression template. Byte would pass my standards independently.

**Grandma Miri's expression sheet** is the strongest evidence that the team can do this work correctly. The five-expression full-body sheet with genuinely differentiated postures is what every sheet in this package should aspire to. WARM/WELCOMING, WISE/KNOWING, and SKEPTICAL/AMUSED are three characters in one face, and the body tells you which one you're looking at without reading the label. This is character design functioning at its intended level.

**The Glitch design concept** — diamond body, CORRUPT_AMBER palette, dual asymmetric pixel eyes — is intelligent and shows a designer making deliberate choices about visual grammar. This is a character that deserves better execution documentation than it has received.

**The cast lineup silhouette sheet** (character_silhouettes.png, Cycle 9) is structurally sound. The five characters are immediately distinguishable in silhouette. This is what the underlying design language is capable of — the problem is that not all of the character sheets at full render quality live up to the promise established by those silhouettes.

**The line weight standards document** and **character sheet standards document** demonstrate genuine production intelligence. The three-tier system (silhouette / interior / detail) is correctly specified. The problem is consistent application, not conceptual understanding.

---

## Summary Statement

Twenty-four cycles of work has produced a package with two excellent assets (Byte, Miri expression sheet), two acceptable assets (Cosmo, Luma color spec), and two assets that are not ready to be seen by a buyer (Luma expression sheet, Glitch expression sheet). The fundamental principle this team needs to absorb before the next production phase is this: *a character exists in three-dimensional space, and every asset you produce must prove that.* A sheet full of characters who only work in 3/4 view, with body language that happens at detail level rather than silhouette level, is not a character design package — it is a series of face studies with bodies attached as an afterthought.

The design vocabulary is there. The construction standards are documented and correct. Apply them without exception.

---

*Kwame Asante — Character Design Authority*
*"The Asante Character Design Review" — Critique 11*
*2026-03-29*
