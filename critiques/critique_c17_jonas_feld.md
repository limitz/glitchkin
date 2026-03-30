# Critique C17 — Jonas Feld (Typography, Logo, and In-World Graphic Design)
**Cycle 43 / Critique 17 — 2026-03-30**
**Assets reviewed:** LTG_BRAND_logo_asymmetric.png (v002, C13), LTG_TOOL_pixel_font_v001.py (C40 Jordan Reed), in-world text in LTG_TOOL_bg_grandma_kitchen.py (v005 MIRI label), LTG_TOOL_bg_classroom.py (C41 chalkboard), LTG_TOOL_bg_school_hallway.py (v003 school seal), storyboard caption typography (LTG_TOOL_sb_panel_a101.py representative sample)
**Tools used:** Source code analysis (LTG_TOOL_logo_asymmetric.py, pixel_font_v001.py, all generator source). No image measurement tool exists for kerning or typographic metrics — I am working from source.

---

## Preamble

This is my first engagement with this pitch. Before I review individual assets I want to state the methodological problem I face: there are no QA tools for typography. The production has tools for warm/cool separation, value floor, glitch spec compliance, VP detection, silhouette RPD, and motion annotation occupancy. It has nothing that measures kerning, baseline alignment, cap-height-to-ascender ratios, or grid-derived logo proportions. I am therefore working entirely from source code analysis, which is the correct method for generative assets but means I am reading the design's intentions rather than verifying its pixel output.

The absence of a typographic QA tool is itself a finding. I am noting it for the producer.

---

## 1 — SHOW LOGO: LTG_BRAND_logo_asymmetric.png (v002, C13)

**Score: 52/100**

- **The typeface is DejaVu Sans at 180pt Bold for "Luma" and 72pt Bold for "Glitchkin."** This is the system default typeface — installed because it is there, not because anyone chose it for this show. Victoria Ashford flagged this in Cycle 12 and again in Cycle 13. It is now Cycle 43. The problem has been documented for 30 cycles and not addressed. At 180pt, the optical characteristics of DejaVu Sans are fully exposed: neutral humanist letterforms designed for screen legibility at small sizes, not for display work. The "L" in "Luma" at dominant scale reads as a functional character, not as a designed one. There is no visual personality in the letterform that could not equally belong to a utility invoice. This is the show's title. It is the first and last thing a pitch audience sees. The current letterform communicates nothing about the show it names.
- **The "&" gradient treatment (C13 fix) is conceptually correct and the execution is sound.** Per-column RGBA gradient from SUNLIT_AMBER through WARM_ORANGE to BYTE_TEAL through ELEC_CYAN — the "&&" as narrative hinge between two worlds. Victoria Ashford confirmed A grade for this in C13. I agree the concept is right. The gradient is applied with precision. This remains the strongest single typographic decision in the package. My only concern: at 56pt body size for the "&", the gradient transitions occur over approximately 40 pixels. Whether those transitions read as intentional dual-world symbolism or as "this character has two colors applied to it" depends entirely on the surrounding letterforms giving the viewer a reason to read carefully. With DejaVu Sans at every other point, I am not confident the careful reading is happening.
- **The "the/Glitchkin" vertical gap (C13 fix: int(H * 0.028) = ~13px) is improved from C12 but still not a lockup.** "the" at 38pt and "Glitchkin" at 72pt are different font sizes from the same neutral typeface. The visual mass of "Glitchkin" overwhelms "the" regardless of the inter-line gap. A typographic lockup requires either a weight relationship (one element structurally anchors the other), a spatial rhythm (the gap is proportionally derived from the letter heights), or a style contrast (the elements are designed to read as a unit). None of these conditions exist. "the" floats above "Glitchkin" without purpose. A true stacked lockup has a logic you can document. This one does not.
- **No construction grid exists for this logo.** I can reconstruct approximate proportional logic from the source code (margin=int(W*0.05), amp_x=luma_x+luma_w+int(W*0.025), stack_x=amp_x+amp_w+int(W*0.028)) but these are layout constants, not a grid system. A logo with a documented construction grid can be reproduced consistently at any scale, in any medium, by anyone who reads the spec. A logo positioned by percentage-of-canvas constants can only be reproduced by running the specific generator. This is not a logo — it is a single composited image. The difference matters for brand deployment.
- **Bottom line:** The asymmetric composition logic is correct and was correctly validated in C13; everything else — the typeface, the lockup logic, the absence of a construction grid — remains at default-tool level, and 30 cycles is not a short time to leave the show's title in placeholder typography.

---

## 2 — PIXEL FONT: LTG_TOOL_pixel_font_v001.py (C40, Jordan Reed)

**Score: 68/100**

- **The tool exists and the glyph set (A–Z, 0–9) is correctly constructed.** The 5×7 bitmap system is the right approach for in-world prop labels — handmade feel, no font dependency, consistent with the show's pixel-art vocabulary. `draw_pixel_text()` and `measure_pixel_text()` are clean APIs. The centering math in `measure_pixel_text()` correctly subtracts the trailing kerning gap. This is competent, intentional work.
- **The tool is registered in the README but is not deployed in any environment generator.** The kitchen MIRI label uses a bespoke pixel-line system (hline/vline/dline) hand-coded directly in `LTG_TOOL_bg_grandma_kitchen.py`. The classroom chalkboard uses random-width rectangles that simulate chalk marks, not character forms. The school hallway seal uses two concentric ellipses with no text. The tech den bulletin board is colored rectangles. The canonical in-world text tool exists in the library and is being ignored by every generator that needs it.
- **Uppercase-only is a structural constraint, not a design choice.** In-world labels in the Real World register (kitchen notes, Grandma Miri's labels, school notices) would naturally mix case. A pixel font with only uppercase renders every label as a SHOUT or a STENCIL — both are wrong for a warm, lived-in domestic space. The tool requires a lowercase extension before it can serve the emotional register of Real World in-world text.
- **The kerning is fixed at 1px regardless of letter pair.** In a 5×7 grid this is geometrically reasonable for most pairs, but the I-M pair, the L-I pair, and any pair involving I will all read wider than optically correct at scale=2 or scale=3. At small scale (scale=1, 5px wide glyphs) this is not visible. At the scale needed for a readable fridge label or a readable notice board poster, the fixed-kerning problem becomes visible. The tool needs at minimum an exceptions map for the widest optical gaps.
- **Bottom line:** A useful foundation tool that is deployed nowhere that matters; the uppercase-only constraint and fixed kerning are solvable problems, but they must be solved before the tool can serve its intended purpose.

---

## 3 — IN-WORLD TEXT: Classroom Chalkboard (LTG_TOOL_bg_classroom.py, Hana Okonkwo, C41)

**Score: 34/100**

- **The chalkboard contains no text.** The generator draws 5 rows of random-width horizontal rectangles in BOARD_CHALK_TEXT color (188, 196, 190). These are placeholder marks that register as "something written here" at thumbnail scale and as "nothing written here" at inspection scale. The spec says "Binary/math board content." The generator has not implemented this. There is no binary sequence, no math equation, no algebraic notation, no number system. There is a visual impression of chalk marks.
- **A chalkboard in a math/science classroom is one of the show's most valuable in-world typographic surfaces.** Millbrook Middle School is the space where the Real World's logical systems (arithmetic, binary, structured notation) are made visible as environmental text. The Glitch Layer runs on corrupted data. A classroom board filled with correct, readable binary notation is a direct visual argument about what the Glitch Layer is destroying. Random horizontal rectangles make no argument.
- **The pixel font tool exists.** `LTG_TOOL_pixel_font_v001.py` was built for exactly this use case — prop labels and in-world text where no font dependency is acceptable. A single call to `draw_pixel_text(draw, x, y, "01001100 01010101 01001101 01000001", chalk_color, scale=1)` would put genuine binary content on the board at the scale appropriate for a background element. This has not happened.
- **Bottom line:** A chalkboard with placeholder marks where text should be is the same as a sign with a rectangle where a word should be — it tells the viewer this world has not been finished, and that is not the impression a pitch package should create.

---

## 4 — IN-WORLD TEXT: School Hallway Seal (LTG_TOOL_bg_school_hallway.py, v003, C38)

**Score: 38/100**

- **The school seal is two concentric ellipses.** The spec description says "T-intersection far end with daylit windows and school seal." What is rendered is a circle within a circle, filled in SCHOOL_SEAL_BG with a SCHOOL_SEAL_RING outline. No text. No name. The school has no name in its own environment. After 20+ cycles of world-building in which Chiara Ferrara (C16) specifically noted "this school should have a name on its seal, a specific banner, posters that reference the show's story beats" — nothing has changed.
- **At the vanishing-point scale where the seal appears, `draw_pixel_text()` at scale=1 would produce readable text.** The seal is positioned at VP_CX, which is the convergence point of the hallway — the most compositionally prominent location in the entire background. It is exactly where a viewer's eye is drawn. Whatever occupies that point should be a designed element, not a placeholder circle.
- **The bulletin boards above the lockers are colored rectangles.** Poster-shaped polygons in POSTER_BG1/BG2/BG3. In 20+ cycles, not one poster has acquired text — not a school motto, not a show-specific banner, not a binary-code decoration that links the school's institutional space to the Glitch Layer's digital vocabulary.
- **Bottom line:** The hallway's most prominent graphic surface — the school seal at the vanishing point — is a geometric placeholder in a show that has built a comprehensive typographic tool specifically for this kind of problem; deploy it.

---

## 5 — IN-WORLD TEXT: Kitchen MIRI Label (LTG_TOOL_bg_grandma_kitchen.py, v005, C39)

**Score: 62/100**

- **The intent is correct and the implementation is technically competent.** A 44×18px cream paper label with hand-pixel-line "MIRI" text is the right scale for a fridge prop label, the right palette (LINE_DARK ink on AGED_CREAM), and the right story function (a narrative Easter egg planted for series-level payoff). The bespoke hline/vline/dline approach works at this size.
- **The bespoke pixel-line system is not the canonical tool.** `LTG_TOOL_pixel_font_v001.py` was built in Cycle 40, one cycle after this label was built. The kitchen label's hand-coded "MIRI" uses independent letter construction logic that does not share metrics, stroke weight, or kerning with the canonical pixel font. If a second label appears anywhere in this show — a sticky note in the Tech Den, a notebook cover in the classroom, a label on any object anywhere — it will be built from scratch again, with different metrics again, and the in-world graphic language will fragment silently.
- **The underlying issue: there is no in-world typographic system.** The pixel font tool is the beginning of one, but it has not been extended (no lowercase, no punctuation beyond space), not deployed in environments where it is needed, and not formally adopted as the canonical in-world text standard. Every generator with text is solving the same problem independently.
- **Bottom line:** The MIRI label is a good-faith implementation at the correct scale and palette, made before the canonical tool existed; it should be migrated to `draw_pixel_text()` as part of the next kitchen generator pass, not as a blocking issue but as a system consolidation.

---

## 6 — STORYBOARD CAPTION TYPOGRAPHY (representative: LTG_TOOL_sb_panel_a101.py)

**Score: 48/100**

- **All storyboard caption text uses DejaVu Sans at 11–14pt.** This is a utility choice — the font is available, it fits in the 60px caption bar, it is readable. It is the correct choice for a production-internal document. It is not a designed typographic system. The shot code, the scene description, and the arc label are all set in the same weight (regular), the same size (11–12pt), and the same color family (100–235 grey values). There is no visual hierarchy — nothing that separates "A1-01 WIDE" (a structural code) from "Grandma Miri's kitchen, morning" (a narrative description) from "QUIET arc beat — warm, analogue, safe" (an emotional direction).
- **The version tag (`LTG_SB_act1_panel_a101_v001`) is set in the same font at 11pt in the lower right at a near-invisible grey (100, 95, 78).** This is correct practice for a watermark. It correctly does not compete. However, if this is the only text in the caption that uses a different grey value as a hierarchy cue, the system is making one distinction (watermark vs content) where it should be making three (code vs description vs direction).
- **Shot codes and arc labels are the most important text in any storyboard caption.** A director reading a board at speed needs to locate "WIDE" and "QUIET" instantly. With all caption text in the same typeface at the same weight, both of those reads require the same amount of visual work as reading the full narrative description. A bold weight for the shot code and a differentiated color for the arc label — even within the same DejaVu Sans family — would constitute a hierarchy. Currently there is none.
- **This critique applies uniformly across all storyboard panel generators.** The caption system is templated — changing it once changes all panels. The investment required to implement a three-tier hierarchy is small. The return (a pitch-ready board that communicates at scan speed) is significant.
- **Bottom line:** Caption typography communicates "production draft" rather than "professional pitch document" — not because of the font choice, which is acceptable for internal use, but because three tiers of information are set without any typographic hierarchy to separate them.

---

## Suite-Wide Assessment

**The fundamental problem with this pitch package's typography is systemic, not asset-level.** There is no typography specification document. There is no defined in-world text standard. There is no font policy that distinguishes between production-internal use (captions, annotations) and pitch-facing use (logo, title card). The team has built one useful tool (pixel font) and one defensible composition (logo asymmetric layout) and then stopped. Everything else — chalkboards, hallway seals, bulletin boards, kitchen labels — is solved individually, inconsistently, and usually with placeholder marks instead of text.

**Priority actions:**

1. **Typeface.** The show logo must use a designed display typeface, not DejaVu Sans. This is 30 cycles overdue. If a licensed typeface is not permitted under the open-source policy, commission a custom letterform for "Luma" using `pycairo` or Inkscape's node editor, extract the bezier paths, and render them programmatically. The tools exist. The decision to stay with DejaVu Sans is not a constraint — it is inaction.

2. **Pixel font deployment.** Every environment with in-world text surfaces — classroom chalkboard, school hallway seal and bulletin boards, tech den notebook covers, kitchen labels — must use `draw_pixel_text()` from the canonical tool. The uppercase-only constraint should be documented as a design choice (all in-world text is uppercase stencil/label style in the Real World) or the lowercase extension must be built.

3. **Chalkboard content.** The classroom board must contain actual binary or mathematical notation. This is not a decoration — it is environmental storytelling. The pixel font exists. One line of code produces a readable binary string. There is no reason this has not happened.

4. **School seal.** The seal at the hallway vanishing point must have text. "MILLBROOK MIDDLE" in pixel font at scale=1 will fit in the seal's footprint at the scale it renders. This is a one-hour implementation.

5. **Logo construction grid.** A spec document must define the logo's proportional relationships — size ratio between "Luma" and "Glitchkin," the "&" positioning logic, the scan bar height as a fraction of canvas height — so the logo can be redrawn by anyone, in any medium, without running the generator. Logos that only exist as single output files are not logos. They are one rendering.

6. **Storyboard caption hierarchy.** Implement a three-tier weight system in the caption bar: shot code (bold), narrative description (regular), arc label (different color). The generator is templated; the change propagates to all panels.

---

**What is working:**

The "&" gradient treatment in the logo is the single most conceptually sophisticated typographic decision in the entire package. It treats a punctuation character as a narrative hinge and executes that treatment with precision. It deserves a better typographic context than DejaVu Sans around it.

The pixel font tool is a sound foundation. 5×7 bitmap, clean API, measure function, scale parameter. Extend it and deploy it.

---

*Jonas Feld — Typography, Logo, and In-World Graphic Design — Critique 17 — 2026-03-30*
