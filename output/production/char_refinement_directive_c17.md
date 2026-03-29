# LTG_PROD_char_refinement_directive_v001
## Character Refinement Directive — Cycle 17
**Project:** Luma & the Glitchkin
**Author:** Alex Chen, Art Director
**Date:** 2026-03-29
**Status:** ACTIVE — Directing Maya Santos, Cycle 17

---

## PART 1 — WHAT "REFINED" MEANS FOR THIS SHOW

"Luma & the Glitchkin" is a character-driven comedy-adventure aimed at a wide audience. Our visual style sits at the intersection of contemporary TV animation (bold graphic shapes, flat construction, strong read-at-distance silhouettes) and digital/pixel aesthetics (CRT warmth, glitch textures, pixel-pattern surface detail). Refinement does not mean adding complexity — it means making the existing design language execute at its full declared intention.

A refined character sheet for this production satisfies ALL of the following:

### 1. Construction Clarity
Every body part can be traced from a single, named shape. No ambiguous geometry, no blended-in detail that obscures the underlying form. The construction order must be: (1) primary shape silhouette, (2) secondary shape subdivisions, (3) surface detail. A production artist working only from the sheet — with no access to design documents — must be able to identify all three tiers instantly.

**Standard:** Cover the color. The grayscale silhouette alone must communicate character identity. Cover the face. The body geometry alone must communicate emotional register in every expression pose.

### 2. Line Weight System
Every line on a character sheet serves one of three functions: **silhouette** (heaviest), **interior structure** (medium), **surface detail** (lightest). These three weights must be visibly distinct — not merely theoretically different. Our show targets:
- Silhouette: 3px at 1920px canvas width (the standard established in the style guide)
- Interior structure: 2px
- Surface detail: 1px (including pixel grid outlines on Luma's hoodie, eye detail lines, smile crinkles on Miri)

A sheet with undifferentiated line weight reads as flat and unprofessional regardless of color quality. A sheet with the correct weight system reads as designed.

### 3. Expression Readability at Thumbnail
This is Dmitri Volkov's benchmark: squint the sheet to 10% scale. Every expression must be identifiable without reading its label.

The test is pass/fail per expression. For each expression on a sheet, ask: if I could only see the body contour and major value masses at very small scale, does this look different from every other expression on the sheet? If two expressions share a thumbnail-scale silhouette, one of them needs a body-language anchor added.

**Current known fail states:**
- Cosmo FRUSTRATED vs NEUTRAL: mouth-and-brow-only differentiation. Body-language anchor required.
- Byte POWERED DOWN vs RESIGNED: both show retracted-arm, low-energy posture. Need one additional silhouette-level differentiator between them.
- Any future expression using face-only differentiation without a body-language complement.

### 4. On-Model Consistency
Every character asset — turnaround view, expression sheet, scene pose, lineup appearance — must be derivable from the same set of locked construction numbers. The character bible gives us those numbers (head units, proportion ratios, shape lock specifications). Refinement means zero unexplained deviation from those numbers.

**Non-negotiable locked specs (production standard):**
- Luma: 3.5 head height, 5 curl count (locked), A-line hoodie trapezoid, mitten hands (no finger detail ever)
- Cosmo: 4.0 head height, glasses tilt 7° neutral (never 0°), glasses frame thickness 0.06x head width, notebook always present
- Byte: oval body (no cube/chamfer references), 10×10px hover particles, float gap = 0.25 head units, RESIGNED uses droopy_resigned lower lid (NOT reduced aperture only)
- Miri: 3.2 head height, MIRI-A canonical (bun + chopstick pair + wide cardigan + soldering iron), crow's feet always present

**Check for consistency across all assets currently in output/characters/. Any deviation from the above is a defect to be logged and fixed.**

### 5. Expression Depth — The Emotional Triangle
For each character, expressions are only "deep" when they operate on all three levels simultaneously:
1. **Eye/brow region** — the first thing viewers read
2. **Mouth region** — confirms or complicates what the eyes say
3. **Body posture** — must agree with the face OR be deliberately contradictory (for character complexity)

An expression that operates on only one or two levels is incomplete. Example of incomplete: SKEPTICAL Cosmo with only a raised brow (eye region only). Example of complete: SKEPTICAL Cosmo with raised brow + +6° backward lean + notebook pressed tight (all three levels, all agreeing on "I am evaluating this from a safe distance").

This standard applies to all 6 expressions on Cosmo's sheet, all 8 on Byte's sheet, and all expressions on Luma's sheet.

---

## PART 2 — THE 2-3 MOST CRITICAL CURRENT GAPS

After reviewing all main character sheets through Cycle 16, the following are the highest-priority structural problems:

### GAP 1 (CRITICAL): Grandma Miri has no expression sheet

Miri's character document (v1.2) is excellent — her design is locked (MIRI-A canonical), her color model exists, her turnaround exists. However, there is no expression sheet for Miri in the output. She has a rich described emotional range in her character bible (calm/warm closed-mouth smile, genuine laugh with teeth, the "quiet concern" read where eyes change before the face announces it, the "I knew this would happen" raised brow). None of this is rendered as a production document.

This is a gap because: Miri appears in Act 2 environment scenes. Any animator or storyboard artist working on Miri must currently improvise her expressions from the text description in grandma_miri.md alone — there is no visual reference. The turnaround confirms her construction but does not provide emotional range. This will cause inconsistent Miri performances across the production. It is also a pitch package gap: we have three expression sheets (Luma, Byte, Cosmo) and nothing for the fourth named character.

**Severity:** High. Blocks Act 2 Miri performance quality. Pitch package incomplete.

### GAP 2 (CRITICAL): Construction-to-output gap — line weight undifferentiation

Based on review of the expression sheet PNGs and pose assets currently in output/characters/main/, the line weight system described in the style guide (3px silhouette / 2px structure / 1px detail) is not consistently implemented as distinct visible tiers. The tools generate outlines but the three-tier weight system that gives the characters their "designed" quality — the quality that distinguishes professional TV animation from competent illustration — is not being enforced systematically.

Specifically: internal construction lines (the torso shape inside the hoodie, the ear ring on Luma, the knee indication on Miri's legs) are rendered at near-silhouette weight in some assets. This collapses depth cues and reads as flat. It also affects expression readability — a brow line must read lighter than the silhouette it sits adjacent to, or the face becomes a mass of equal-weight lines.

**Severity:** High. Affects perceived quality of all character assets. This is the core of the producer's "not refined enough" concern.

### GAP 3 (SIGNIFICANT): Luma turnaround is missing the Act 2 standing pose data

The Luma turnaround (v001) predates the Act 2 standing pose work. The Act 2 standing pose (v002) exists as a standalone asset but is not integrated into the turnaround or into a consolidated "Luma complete model sheet" document that shows: (a) front/back/side/3Q views, (b) expression sheet, (c) Act 2 key poses, (d) scale reference against Cosmo and Byte. Animators working from the turnaround have an older, pre-Act-2 version of Luma's proportions. The turnaround and the Act 2 pose tools should be reconciled into a single reference.

**Severity:** Moderate-High. Functional production gap that will cause inconsistency in Act 2 work.

---

## PART 3 — STANDARDS MATRIX

| Standard | Test | Pass Threshold |
|---|---|---|
| Construction clarity | Grayscale silhouette only — does it read as the correct character? | Immediately identifiable without labels |
| Line weight system | Three tiers visible? Silhouette heavier than structure heavier than detail? | All three tiers visibly distinct in every asset |
| Thumbnail expression read | Squint to 10% — unique silhouette per expression? | Every expression distinct from all others at small scale |
| On-model consistency | Do all assets for a character match the locked construction numbers? | Zero deviation without documented exception |
| Expression depth | Face + body operating on at least 2 of 3 levels (eyes/brows, mouth, body)? | All 3 levels for primary expressions; minimum 2 for secondary |
| Color model compliance | Do palette values match master_palette.md and character .md specs? | 100% — no undocumented color variations |
| Pixel detail LOD | Are simplified production variants defined for medium, wide, very wide shots? | Luma hoodie pixel variants documented and implemented |

---

## PART 4 — DIRECTION TO MAYA SANTOS, CYCLE 17

Maya, this cycle's priority assignments are ordered by impact on production readiness. Address them in this sequence:

### ASSIGNMENT 1 (Priority 1): Grandma Miri Expression Sheet

**File to create:** `LTG_CHAR_miri_expression_sheet_v001.png`
**Tool to create:** `LTG_TOOL_miri_expression_sheet_v001.py`

Design and generate a 3×2 expression sheet for Miri. Required expressions:
1. **NEUTRAL / WARM** — Default resting state. Gentle closed-mouth upward curve, eyes "about to engage." Crow's feet visible. Permanent cheek blush at 25% opacity. Soldering iron in non-dominant hand or on work surface.
2. **KNOWING SMILE** — The "I knew this would happen" expression. Wide closed-mouth smile pressing cheeks up into eyes (smile crinkle). Brow neutral to slightly arched. This is her most frequent "responding to Luma" state. Eyes crinkle into "happy crescents" — upper lid arc descends to 40% aperture.
3. **QUIET CONCERN** — Eyes change first: brow descends very slightly medially, inner corners drop 3px. Mouth remains almost neutral — corners barely drop. This is the expression described in the bible as "information in the eyes before the face announces it." Body: slight forward lean, hands held closer to body or clasped. This is a SUBTLE expression — it must not read as dramatic worry (that would be wrong for Miri's character).
4. **GENUINE LAUGH** — Open-mouth laugh, teeth visible. Eyes pressed into crescents. Brow fully relaxed and raised. This is the fullest expression she has. Body: slight backward lean with shoulders up (contained laugh — she is not Luma). Head tilts slightly back.
5. **FOCUSED / WORKING** — Eyes narrowed to ~40% aperture, head tilted 5-8° toward the work, brow very slightly furrowed (not worried — concentrated). Mouth slightly open or pressed in thought. This is Miri at her engineering brain — the expression that shows who she was before she was Grandma.
6. **SKEPTICAL / AMUSED** — One eyebrow arched (left, viewer's right — the more mobile brow). Closed-mouth slight smirk, corner curling upward. Head tilted back very slightly. Body: upright, arms settled — she is not leaning away (she is not defensive), she is simply watching. This must be read as warm skepticism, not cold judgment.

**Construction rules for the sheet:**
- Use MIRI-A design: bun + chopstick pair + wide cardigan + soldering iron prop
- Body construction: 3.2 head height, weathered-rectangle torso, slightly wider shoulders than head (1.1x)
- Crow's feet at outer eye corners — 50% line weight, always present
- Smile lines front-face — 40% line weight, always present
- Panel backgrounds: use a warm value system — warmer/lighter backgrounds for higher-register expressions (LAUGH, KNOWING SMILE), cooler/darker for lower-register (FOCUSED, CONCERNED)
- Flow annotations on each panel: `← was / → next` beat labels per the sheet convention

**Squint test requirement:** At 10% scale, LAUGH must be distinguishable from all others (body lean + open mouth). KNOWING SMILE must be distinguishable from NEUTRAL (cheek press is the body signal — her face width visually widens at cheeks). FOCUSED must be distinguishable (forward head tilt + body lean).

---

### ASSIGNMENT 2 (Priority 2): Line Weight Audit and Fix Pass

**Review all existing character tools for line weight implementation:**
- `LTG_TOOL_byte_expression_sheet_v002.py`
- `LTG_TOOL_cosmo_expression_sheet_v001.py`
- `LTG_TOOL_luma_expression_sheet_v002.py` (or v003)
- `LTG_TOOL_luma_act2_standing_pose_v001.py`

**For each tool, verify and enforce:**
- Silhouette / outline lines: 3px
- Interior structural lines (torso seam indication, knee indication, ear ring, hoodie panel boundaries): 2px
- Surface detail lines (Luma hoodie pixel grid outlines, Byte glitch scar, Byte hover particle outlines, Miri crow's feet, Miri smile lines, Cosmo glasses inner rim): 1px

If regeneration is needed to implement this, regenerate the PNG and note the change in the tool header comment. Do NOT rename the existing tool file — edit in place and note the cycle.

**Verify the following specific elements at 1px detail weight:**
- Byte: glitch scar diagonal, hover pixel confetti outlines
- Luma: hoodie pixel grid squares (all edges), hair highlight shape interior
- Cosmo: glasses lens glare crescent, notebook spine lines
- Miri: crow's feet (2 lines per eye), smile lines (1 line per side)

---

### ASSIGNMENT 3 (Priority 3): Luma Act 2 Pose Forward Lean Fix

The -5° forward lean in `LTG_TOOL_luma_act2_standing_pose_v001.py` is architecturally present but imperceptible in output. Increase to -8° and propagate the lean through all limb origin points (shoulder attachment, hip attachment) so it reads as a genuine body lean rather than a head offset. Regenerate `LTG_CHAR_luma_act2_standing_pose_v003.png`.

---

### COORDINATION NOTE: Sam Kowalski

After Maya completes the Miri expression sheet tool, relay the palette values to Sam Kowalski for color model compliance verification. Sam should cross-check all generated Miri expression values against `master_palette.md` DRW skin entries and confirm the permanent cheek blush value #D4956B at 25% opacity is correctly applied.

---

## PART 5 — ON-MODEL REFERENCE: LOCKED SPECS SUMMARY

The following are non-negotiable. Any asset deviating from these is a defect:

| Character | Locked Element | Spec |
|---|---|---|
| Luma | Hair curl count | Always 5. Never 4 or 6. |
| Luma | Hoodie base color | #E8722A Warm Orange |
| Luma | Hands | Mitten only. No thumb arc, no finger differentiation. |
| Luma | Head shape | Near-perfect circle, 95% circular compression |
| Cosmo | Head shape | Tall rounded rectangle, 1.16:1 H:W ratio, corner radius 0.12x head units |
| Cosmo | Glasses tilt | 7° counterclockwise at neutral. Never 0°. |
| Cosmo | Glasses frame | 0.06x head width thickness |
| Cosmo | Notebook | Always present, tucked under left arm at neutral |
| Byte | Body shape | Oval/ellipse only. No chamfer, no cube references. |
| Byte | Float gap | 0.25 head units clearance above surface |
| Byte | Hover particles | 10×10px. No exceptions. |
| Byte | RESIGNED right eye | droopy_resigned lower lid (parabolic sag, NOT just reduced aperture) |
| Miri | Design | MIRI-A only. Bun + chopstick pair + cardigan + soldering iron. |
| Miri | Eye aging marks | Crow's feet always present at 50% line weight |
| Miri | Cheek tone | #D4956B always at 25% opacity (not situational like Luma's blush) |

---

## NOTES FOR CYCLE 17 REVIEW

When submitting completed assets, include for each:
1. File name following naming convention: `LTG_CHAR_[descriptor]_v[###].png`
2. Squint test confirmation: "passed at 10% — [X] expressions distinct"
3. Construction check: "on-model with [character].md v[X.X]"
4. Line weight confirmation: "three tiers implemented"

This directive will be referenced in the Cycle 18 critique brief. Critics will be asked to evaluate specifically against the standards defined in Part 1.

---

*Alex Chen — Art Director*
*"Luma & the Glitchkin"*
*Cycle 17 — 2026-03-29*
