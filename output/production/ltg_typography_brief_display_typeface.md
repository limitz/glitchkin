<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->

# Typography Brief — Logo Display Typeface
**"Luma & the Glitchkin"**

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-30
**Cycle:** 43
**Prepared for:** Alex Chen, Art Director

---

## The Problem

The show's logo has used DejaVu Sans Bold as its display typeface for 30 cycles. DejaVu Sans is a workhorse utility font — it is readable, robust, and entirely neutral. That neutrality is the problem.

"Luma & the Glitchkin" is a show premised on two worlds in tension: a warm domestic Real World defined by analog imperfection and human roundness, and a cold Glitch Layer defined by digital precision and pixel geometry. The title text is the first thing a viewer reads. It should encode that tension before a single frame of animation plays. DejaVu Sans communicates nothing about either world.

Jonas Feld's 52/100 score was correct. A show this visually intentional deserves type that is equally intentional.

---

## Design Requirements

### Structural requirements (non-negotiable)
- Open source / freely licensable (SIL Open Font License or equivalent). Must be downloadable and usable in our PIL pipeline via `ImageFont.truetype()`.
- Must render cleanly at large display sizes (160–180pt for "Luma" / 72pt for "Glitchkin") and remain legible at thumbnail scale (the logo appears in 1280×720 frames).
- Must support standard Latin (A–Z, a–z, digits, ampersand "&").
- Must be available on Google Fonts or a comparable open-source repository — no proprietary foundry licensing.

### Identity requirements
- The typeface for **"Luma"** should read as warm, rounded, and approachable — consistent with Luma's circular shape language and the Real World's analog character. It should have a slightly hand-constructed or humanist quality without being a literal handwriting face.
- The typeface for **"Glitchkin"** (and optionally "the") should read as geometric, precise, and digital — consistent with the Glitch Layer's pixel logic and Glitch's diamond body structure. A monoweight geometric or a face with pixel-construction DNA is ideal.
- The two sides can be the **same family in different weights/styles**, or two **complementary typefaces from the same design ecosystem**, or two **contrasting typefaces that share a compatible x-height and cap-height**. The logo layout already does the heavy lifting on warmth (amber) vs. cold (cyan) — the type does not need to scream contrast; it needs to *confirm* it.
- The "&" is the hinge between both worlds and currently receives a warm-to-cold gradient treatment. Any typeface chosen should have an "&" character with sufficient visual mass to carry this treatment.

### "the" requirement
"the" appears in small type above "Glitchkin" and is secondary to the title lockup. It may use the same face as "Glitchkin" at a lighter weight, or a separate companion face, as long as it reads as subordinate.

---

## Candidate Typefaces

### Candidate 1 — Nunito Bold (for "Luma") + Space Grotesk Bold (for "Glitchkin")
**License:** SIL OFL (both)
**Source:** Google Fonts

**Nunito** is a rounded humanist sans with circular terminals. Its letterforms are constructed around a consistent round ending — the stems terminate in rounded butt cuts rather than the sharp angled cuts of a conventional grotesque. At 180pt, "Luma" in Nunito Bold has the weight of a dominant headline with the warmth of hand-lettered character. The `L`, `u`, `m`, `a` letterforms are all pleasantly round without being cartoonish — appropriate for a 12-year-old protagonist, not a toddler show.

**Space Grotesk** is a proportional geometric grotesque derived from Space Mono, designed by Florian Karsten. It retains deliberate "constructed" details — ink traps, slightly mechanical stroke junctions — that read as digital/technical without being a literal monospace or pixel face. "Glitchkin" in Space Grotesk Bold has geometric precision with enough weight to carry the Electric Cyan color treatment and glitch scatter FX. The `k` in particular has a geometric leg-arm junction that reads as Glitch Layer–appropriate.

**Compatibility:** Nunito and Space Grotesk share a similar x-height (both designed for screen use) and work well in combination. Their cap-heights are close enough that "Luma" and "Glitchkin" can lock at the same baseline without feeling mis-matched in scale.

**"& the" treatment:** Nunito's `&` is a full-bodied, organic ampersand — good for the warm-to-cold gradient treatment currently in the generator. "the" in Space Grotesk Light or Regular reads as subordinate to "Glitchkin" Bold.

**Assessment:** The strongest candidate for the current logo layout. Nunito is already used in children's media at the premium end (see Duolingo, various Netflix animated titles). Space Grotesk is unusual enough to feel distinctive.

---

### Candidate 2 — Outfit ExtraBold (for "Luma") + Roboto Mono Bold (for "Glitchkin")
**License:** SIL OFL (both)
**Source:** Google Fonts

**Outfit** is a clean geometric sans with pronounced rounded letterforms — particularly the `O`, `u`, `a`, and `m`. It sits between Nunito's warmth and a strict geometric sans. At heavy weights it has significant visual presence. The letters are slightly wider than Nunito, which would give "Luma" a more dominant lockup footprint — appropriate given the asymmetric layout where "Luma" is the visual anchor.

**Roboto Mono** is the monospaced variant of Roboto. Using a monospace face for "Glitchkin" is a strong conceptual choice: monospace is the typographic language of code, terminals, and digital systems. It signals the Glitch Layer's origins in corrupted digital broadcast — the characters are data, and data is presented in monospaced type. The even letter spacing creates a slightly formal, mechanical rhythm that contrasts with Outfit's fluid warmth.

**Risk:** Roboto Mono is very recognizable as a developer tool / IDE font. Depending on Alex's direction for the show's tone, this may read as "hacker aesthetic" rather than "corrupted digital dimension." This is a valid choice for a harder sci-fi register; it is a riskier choice if the show's tone should remain accessible and warm overall.

**"& the" treatment:** Outfit has a conventional `&` — functional but not especially distinctive. "the" in Roboto Mono Regular would align with the Glitch Layer treatment, but its monowidth feel may look odd at the small scale.

**Assessment:** Compelling conceptual clarity (Warm + Code) but carries real-world developer associations that could undercut the show's original voice. Recommend as a discussion option, not a primary recommendation.

---

### Candidate 3 — Fredoka One (for "Luma") + Barlow Condensed Bold (for "Glitchkin")
**License:** SIL OFL (both)
**Source:** Google Fonts

**Fredoka One** is an aggressively rounded display face — the letterforms are inflated, almost buoyant, with very short descenders and a high x-height. It reads as exuberant and youthful. At 180pt, "Luma" in Fredoka One would be unmistakably playful and character-driven, matching Luma's large reckless eyes and hair cloud that defies physics.

**Barlow Condensed Bold** is a tightly-spaced geometric condensed grotesque. Its narrow form gives "Glitchkin" (a 9-letter word) more room to breathe at the secondary scale while maintaining strong visual weight. Condensed faces have a "screen display" quality — they are common in UI systems, HUDs, and technical readouts — appropriate for a Glitch Layer reference.

**Risk:** Fredoka One is a very strong personality statement. It may skew the show's visual register younger than intended (more Nick Jr. than Cartoon Network / streaming animation). The contrast between Fredoka One and Barlow Condensed is also quite large — they may feel like they belong to different productions rather than two sides of the same show.

**Assessment:** Highest contrast option. Appropriate only if Alex wants to emphasize the accessible/family-audience appeal over the show's more sophisticated conceptual underpinning. Not recommended as primary.

---

### Candidate 4 — Raleway ExtraBold (for "Luma") + Share Tech Mono (for "Glitchkin")
**License:** SIL OFL (both)
**Source:** Google Fonts

**Raleway** is an elegant display sans with geometric construction but refined, humanist proportions. Its distinctive feature is the stylistic `W` with an overlapping mid-crossing — and the letterforms have a slightly art-deco quality at heavy weights. At 180pt ExtraBold, "Luma" in Raleway would have sophistication and warmth without tipping into child-display territory. Raleway reads as slightly older-audience — appropriate if the pitch is targeting 9–13 and their parents simultaneously.

**Share Tech Mono** is a monospace typeface designed to evoke early computer terminal and broadcast text systems. Its letterforms have a CRT-screen character — slightly rounded pixel-style construction with deliberate scan-line aesthetic references. "Glitchkin" in Share Tech Mono would directly reference the CRT monitor at the center of the show's premise (Byte emerges from Grandma Miri's ancient CRT). The face is slightly less recognizable than Roboto Mono, giving it a more original feel.

**"& the" treatment:** Raleway's `&` is a clean geometric design. Share Tech Mono's small scale for "the" works better than Roboto Mono because the face has more personality at small sizes.

**Assessment:** The highest-craft option. Raleway + Share Tech Mono honors the show's dual world premise while communicating sophistication appropriate for the pitch context. The CRT-terminal aesthetic of Share Tech Mono is directly diegetically motivated by Grandma Miri's television. Strong secondary recommendation.

---

### Candidate 5 — Jost Medium/Bold (unified single-family approach)
**License:** SIL OFL**
**Source:** Google Fonts

**Jost** is a geometric sans heavily influenced by early twentieth-century German geometric typefaces (Futura, Erbar). It is clean, monolinear, and precise — but it has humanist proportions that prevent it from reading as cold. The approach here is different from the other candidates: use **a single family at different weights**, with the visual distinction between Real World and Glitch Layer carried entirely by color treatment (amber for "Luma," cyan for "Glitchkin") rather than two separate typefaces.

Arguments for this approach: the current logo already has very strong world-distinction via color and layout. Adding a typeface contrast on top risks visual noise. A unified typeface family suggests that "Luma" and "Glitchkin" are two things from the same world — which is true; they are both part of the same show, even if they belong to different internal worlds.

Arguments against: we have a clear opportunity to encode the warm/cold world split into the letterforms themselves, and using a single typeface foregoes that opportunity.

**Assessment:** This is the conservative choice and the safest option if the team's priority is a clean, modern, pitch-ready logo without risk. Jost at heavy weight performs better than DejaVu Sans at every scale. However, it does not solve the creative problem Jonas flagged — it simply upgrades the execution without addressing the concept.

---

## Sam's Recommendation

**Primary recommendation: Nunito Bold (Luma) + Space Grotesk Bold (Glitchkin)**

This pairing best serves the show's dual-world identity at the letter level. Nunito's rounded warmth maps directly to Luma's character shape language and the Real World's domestic quality. Space Grotesk's geometric-technical character maps to the Glitch Layer's constructed, data-origin identity — without being derivative of obvious developer-tool aesthetics.

**Secondary recommendation: Raleway ExtraBold (Luma) + Share Tech Mono (Glitchkin)**

This pairing is the highest-concept option because Share Tech Mono's CRT-terminal origins directly reference the show's central prop (Grandma Miri's television) and Byte's emergence medium. If the pitch is targeting a more sophisticated buyer (streaming rather than broadcast), this pairing would stand out.

**Decision for Alex:** Both recommended options are available on Google Fonts under SIL OFL. Installation requires downloading the .ttf files and placing them in a project fonts directory. The logo generator will need a `load_font()` update to reference the new paths. I can update the generator in C44 once a decision is made.

---

## Pipeline Notes

- All five candidates are available on Google Fonts (fonts.google.com) under SIL Open Font License.
- Download: individual .ttf files from each family's Google Fonts page.
- Suggested install path: `/home/wipkat/team/assets/fonts/` (new directory — does not currently exist).
- Logo generator update: `load_font()` in `LTG_TOOL_logo_asymmetric.py` currently tries DejaVu → Liberation → FreeSans. It needs a new primary path added at the top of the `paths` list once the chosen font is installed.
- The "& the" portion may use a weight between the two primary faces, or a third weight from the same families. This is a generator decision — the brief specifies direction only.
- No changes to master_palette.md, luma_color_model.md, or any color documents are required by this typeface change. The color treatment of the logo (amber "Luma," warm-to-cold "&," cyan "Glitchkin") is typeface-independent.

---

## UV_PURPLE Drift Note (from Jonas Feld / Leila critique)

Leila's flag about UV_PURPLE drifting toward the 2010s dystopian palette is a palette stewardship note, not a typography note. It is noted here for completeness because it was raised alongside the typeface issue. The UV_PURPLE (#7B2FBE) is currently correctly saturated and confined to the Glitch Layer. If GL-04 ever softens toward a desaturated slate-purple, it will read as YA dystopian rather than digital-corruption. This is a watch item for all future palette reviews — flagged to master_palette.md stewardship.
