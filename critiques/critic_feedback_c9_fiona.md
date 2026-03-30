# Critic Feedback — Cycle 9
## Production Design & Package Consistency Review
### "Luma & the Glitchkin"

**Critic:** Fiona O'Sullivan — Production Design Specialist
**Date:** 2026-03-29
**Cycle:** 9
**Scope:** Verification pass — addressing Cycle 8 C+ grade failures; consistency audit; production-readiness assessment

---

## Overall Grade: C+

The grade does not move. I want to be precise about why.

Several of the specific issues I raised in Cycle 8 have been addressed — and I acknowledge that clearly below. But the single most important item on my entire remediation list — the Byte design document inconsistency — was not fixed. It was made dramatically worse. The chamfered-cube language that I asked to have retired now runs through more than half the document, coexisting with oval language in the same sections, producing a design document that is actively contradictory. A new animator reading byte.md v3.0 will encounter the word "cube" dozens of times in production-critical turnaround descriptions and construction notes. The version header says "Oval Body." The document says "cube." These two things cannot both be true.

Until that document is a clean, internally consistent oval body spec, I cannot upgrade this grade. The Byte design sheet is the most-referenced character document in the package. Its integrity is non-negotiable.

---

## VERIFICATION FINDINGS — CYCLE 8 REMEDIATION ITEMS

### 1. BYTE DESIGN DOCUMENT — OVAL BODY (CRITICAL — C8 Item 1)
**Status: FAILED. Condition worsened.**

The document header (v3.0) and the first three paragraphs of Section 2 are correct. The revision notice is clear. The oval rationale is well-written. Section 4's construction section opens correctly with an oval-body header.

Then the document falls apart comprehensively.

**Specific contamination points found in byte.md v3.0:**

- **Section 2, Shape Language — Limb Expressions header (line 91):** "Because Byte cannot change his posture much (**cube body**, stubby limbs)..." — This is in the current, non-retired body of the document. Active contradiction.

- **Section 4, Color Table (line 233–234):** Shadow tone described as occupying "the underside of the **cube body**." Highlight tone described as "The top face of the **cube** and the top surfaces of limbs." Active contradiction.

- **Section 4, Color Table (line 244):** "Scar continuation — The main scar line continues onto the side face of the **cube** at reduced width." Active contradiction.

- **Section 8, Face Plane (line 165):** "Byte's face is the front face of his **cube**. It is bounded by the **cube's** front edges." This is in the face construction section — a section any character animator or rig artist will use constantly. It says cube.

- **Section 10, Turnaround — View 1 (line 650):** "Body edges: both left and right body edges visible as straight vertical lines with **chamfered corners**. The right-side notches are partially visible as dark indentations at the upper-right corner of the body."

- **Section 10, Turnaround — View 2 (line 677):** "The **cube's** LEFT side face: visible in perspective... Side-face highlight: the left side face receives reflected light." The turnaround section describes a cube throughout.

- **Section 10, Turnaround — View 3 (line 693):** "The left side face: a vertical rectangle with **chamfered corners**." And: "**Key visual purpose:** Establishes the **cube's** depth dimension."

- **Section 10, Turnaround — View 4 (line 712):** "The **cube's** RIGHT side face: the main damage zone. The two **triangular notches** at the upper-right corner of the front face are now visible as dark cavities."

- **Section 10, Turnaround — View 5 (line 727):** "Back face: a clean, flat rectangle with **chamfered corners**."

- **Section 10, Turnaround Production Notes (line 753):** "Body **cube**: approximately W:H:D = 1.0:1.1:0.9" — the production data table specifies a cube.

- **Section 10, Depth specification (line 754):** "This means in perfect side view, he appears slightly narrower than in front view. This slight reduction confirms the **cube** depth without making him look flat."

- **Section 11, Design Principles — DO NOT list (line 927):** "DO NOT make him cute-round... Keep the **chamfered corners**, keep the notches, keep the spike." This is in the DO NOT list — the explicit prohibitions that a new artist will follow. It currently prohibits rounding him and tells artists to maintain chamfered corners.

- **Section 11, Silhouette Test (line 935):** "Reading Byte as a solid black silhouette: A roughly **cubic** form with **chamfered corners** and visible geometric complexity at the edges."

- **Section 11, Size Comparison (line 848):** "the visual contrast — her rounded warm orange form against his small sharp **cyan cube**."

- **Section 11, Size Comparison — Cosmo (line 851):** "Three completely different visual weights and silhouettes: tall rectangle (Cosmo), medium rounded mass (Luma), tiny jagged **cube** (Byte)."

This is not a matter of a few stray words. The entire turnaround section — the most production-critical section of any character document — describes a chamfered cube. Every view description refers to cube depth, cube faces, chamfered corners, triangular notches. The Section 10 turnaround is the cube design document. The Section 4 color table describes cube body shadow placement. The Section 11 design rules tell artists to keep chamfered corners.

**The document tells two completely different stories simultaneously.** Version 3.0 is not an oval body document. It is a Frankenstein document with oval language grafted onto a cube scaffold. Any animator given this document is being set up to fail.

The only path forward: the turnaround section (Section 10) must be rewritten from scratch for an oval body. Every turnaround view description must describe an oval. The color table must replace "cube body" with "oval body." The DO NOT list must remove the instruction to keep chamfered corners. The silhouette test must describe an oval form. The size comparison must stop calling Byte a cube.

Additionally: the character_turnaround_generator.py tool generated luma_turnaround.png and byte_turnaround.png. I cannot inspect the PNGs directly in text, but if the Python tool was written with the chamfered-cube design (pre-Cycle 8), those PNG turnarounds may themselves be cube renderings. The SOW notes "Byte turnaround still uses chamfered-cube description — needs oval update" — the team flagged this themselves and shipped it anyway. This is not acceptable. A turnaround with the wrong body shape is worse than no turnaround: it is confident misinformation.

---

### 2. SKIN COLOR SYSTEM — SECTION 7 (HIGH — C8 Item 2)
**Status: SUBSTANTIALLY RESOLVED. One action item incomplete.**

Section 7 is competent work. The two-tier system (RW-10 canonical neutral base / CHAR-L-01 scene-derived lamp-lit base) is clearly explained and logically sound. The CHAR-C-01 registration for Cosmo's skin is correct and fills the gap I identified. The Grandma Miri CHAR-M-01 was already documented. The warm/cool skin tables in 7.4 and 7.5 are clear and usable.

The resolution language in Section 7.6 is appropriately specific about what was wrong and why it was not actually a conflict.

**The one outstanding item:** Section 7.6 explicitly states: "The color model sheet requires a clarification note to prevent future confusion. The skin entry in luma_color_model.md should note that #C8885A is the lamp-lit derivation of the neutral base #C4A882, not a replacement for it."

I verified luma_color_model.md. **This cross-reference note has been added.** The skin entry now reads: "Base = Warm Caramel (lamp-lit Frame 01 derivation of neutral base #C4A882 / RW-10 under Soft Gold key). For standard/neutral lighting, use #C4A882 (RW-10) as base. See master_palette.md Section 7 for full two-tier skin system."

That is correct. The discrepancy is resolved. Section 7 of the master palette is coherent and the supporting document has been updated to match.

**Score for this item: PASS.** This was one of my two critical-priority items. The team delivered a real solution, not a workaround.

---

### 3. NAMING CONVENTION COMPLIANCE CHECKLIST (HIGH — C8 Item 3)
**Status: PARTIAL. Checklist exists; compliance remains near-zero.**

The naming_convention_compliance_checklist.md is well-constructed. It is clear, operational, format-correct, and provides the team with actionable guidance at the moment of file creation. Sam Kowalski understood what was needed here: not another policy document, but a daily-use reference card. The category quick reference table and the Common Mistakes table are good work.

**However:**

The checklist itself is filed as `naming_convention_compliance_checklist.md` — not `LTG_PROD_naming_convention_compliance_checklist_v001.md`. The document that explains how to name files is not named correctly. This is the same circular non-compliance I flagged in Cycle 8 for the naming_conventions.md document itself. We now have two compliance documents that violate their own standard.

More substantively: I audited LTG-compliant files in the output folder. The total count is **three files**:
- `LTG_ENV_lumashome_study_interior.png`
- `LTG_ENV_glitchlayer_frame.png`
- `LTG_TOOL_bg_glitch_layer_frame.py`

Three files out of an output folder containing dozens of assets. Jordan Reed created these three compliant files in Cycle 9. Everyone else created new files this cycle under non-compliant names: `statement_of_work_cycle9.md`, `naming_convention_compliance_checklist.md`, `critic_feedback_c9_*.md`. The checklist is on the shelf. The team is not using it.

The checklist's Section 8 acknowledges that legacy files will not be renamed yet, which I accepted as a reasonable interim position. But Cycle 9 produced new files that are non-compliant. The checklist says "Do apply the convention to ALL new files created from Cycle 9 forward." That instruction was not followed by most team members this cycle, including the person who wrote the checklist.

**Score for this item: INCOMPLETE.** Tool exists. Adoption has not occurred.

---

### 4. CHARACTER TURNAROUNDS (HIGH — C8 Item 4)
**Status: PARTIAL. Assets exist; Byte turnaround is potentially incorrect.**

Luma and Byte turnarounds now exist as PNG files at `/output/characters/main/turnarounds/`. The generator tool exists. Two of the four main characters have turnaround assets. This is forward progress and I acknowledge it.

The problems:

**Byte's turnaround PNG:** The SOW itself states: "Byte turnaround still uses chamfered-cube description — needs oval update." The team shipped a turnaround asset they knew was wrong. This is worse than the Cycle 8 situation where the turnaround directory was simply empty. An empty directory tells a new animator to wait. A turnaround with the wrong body shape tells them the wrong shape is correct. The Byte turnaround PNG may be actively misleading production.

**Cosmo and Miri:** No turnarounds for either character. This was not explicitly addressed in the Cycle 9 SOW. The remediation only targeted Luma and Byte. Cosmo is a main character. Miri appears in a third of the scripts. We are now three cycles past my first critique and two of the four characters still have no turnaround assets.

**Score for this item: INCOMPLETE.** Two turnarounds exist; one of them may be wrong; two are still missing.

---

### 5. MIRI LOCKED — MIRI-B REMOVAL (HIGH — C8 Item 5)
**Status: PASS.**

grandma_miri.md v1.2 is clean. MIRI-A is locked with clear rationale documented. MIRI-B is formally retired with a note. The silhouette generator has been updated to recognize only MIRI-A. The character design package for Miri is complete at the spec-document level.

One observation: Miri's character document is locked but there is still no Miri turnaround asset. Her design is locked — now she needs a turnaround so her locked design can be used by other artists.

---

## ITEMS I RAISED IN CYCLE 8 THAT WERE NOT ADDRESSED THIS CYCLE

### Show Logo / Title Card Asset
**Status: DOES NOT EXIST.**

`/output/storyboards/panels/panel_p25_title_card.png` exists — that is a storyboard panel. I checked for any standalone logo or title card asset. There is none. No logo file, no title treatment document, no type spec. The SOW does not mention this as a cycle objective. After two cycles of me calling this "embarrassing," the team has not assigned it to anyone.

A show called "Luma & the Glitchkin" still has no visual identity for its title. This is not a minor omission. It is the single most visible gap in any pitch package. When a development executive opens the folder, they want to see what the show is called and how it looks. The answer is: we don't know yet.

### Composite Reference Image (All 4 Characters at Relative Scale)
**Status: DOES NOT EXIST.**

`character_lineup.md` is a text document describing character proportions. `proportion_diagram.png` generates abstract height bars. Neither is a composite reference image. There is no image showing all four characters standing together at correct relative scale, in their full designs, suitable for use in a pitch deck or as a production reference.

This item was raised in Cycle 8. It was not addressed in Cycle 9. It is not in the Cycle 9 SOW.

### Style Guide — Animation Style, Props, Glitchkin Construction
**Status: NOT ADDRESSED.**

The style guide gaps I identified (no animation style notes, no prop design section, no Glitchkin construction rules) remain. These were medium priority items. No Cycle 9 work addressed them.

### Tools Directory Location
**Status: NOT ADDRESSED.**

Tools remain at `output/tools/` while the production bible specifies `production/tools/`. Minor but unresolved.

---

## NEW ISSUES IDENTIFIED IN CYCLE 9

### byte.md Section 10 Turnaround — Describes a Different Character
The turnaround section of byte.md v3.0 is not merely contaminated by stray cube references — it describes a character with triangular notches, chamfered side faces, a geometric spike, and rectangular front and back faces. This is the original chamfered-cube character design, written as a complete turnaround with five views, precise measurements, and detailed visibility notes. It describes a cube body with W:H:D = 1.0:1.1:0.9 proportions. The oval body has no such depth dimension in the same sense — it is a 2D projected ellipse.

These are not the same character. The turnaround in Section 10 is the old Byte. Every measurement, every visibility note, every production note in that section is for a design that was retired.

This is not a documentation inconsistency. It is a design document that describes two incompatible characters under one version number. The production consequence is that any artist who reads Section 10 — which is the most production-relevant section, the one they would open when rigging or boarding — will draw the retired design.

### Cycle 9 New Files Are Non-Compliant
New files created this cycle include the SOW, the compliance checklist itself, and all critic feedback files. All are non-compliant with the naming convention. The team adopted the checklist in theory on the day the checklist was written and ignored it in practice on the same day.

---

## WHAT IS GENUINELY BETTER IN CYCLE 9

I will not give this package its credit only through criticism. These are real improvements:

- **Section 7 of the master palette is well-executed.** The two-tier skin system is clear, logical, and resolves my primary color discrepancy critique. The CHAR-C-01 registration for Cosmo fills a genuine gap. This is production-grade work.
- **luma_color_model.md has been updated** with the required cross-reference. The action item from Section 7.6 was completed.
- **Miri is locked.** A character who was in variant limbo for multiple cycles is now formally sealed. The design rationale is documented and the generator reflects the decision.
- **The Glitch Layer background exists.** `LTG_ENV_glitchlayer_frame.png` is a real deliverable. This was one of my Cycle 8 HIGH-priority items (a full pitch needs the second world). It now exists.
- **Luma turnaround exists** and is presumably correct (the generator produced her first, before the oval Byte issue arose).
- **Jordan Reed is applying the naming convention** to new files. Three compliant files is three more than Cycle 8. It is not enough, but it demonstrates the convention can be followed.
- **The byte.md version header and oval rationale are correct.** The intent was right. The execution of the full document update was not completed.

---

## GRADE BREAKDOWN

| Category | C8 Grade | C9 Grade | Movement |
|---|---|---|---|
| Style Guide Completeness | 6/10 | 6/10 | No change — same gaps |
| Cross-Tool Consistency | 4/10 | 5/10 | Skin resolved; Byte doc worsened |
| Naming Convention Compliance | 2/10 | 3/10 | Checklist exists; adoption near-zero |
| Asset Organization | 5/10 | 6/10 | Glitch Layer added; turnarounds partial |
| Pitch Package Completeness | 5/10 | 5/10 | No logo; no composite; limited new content |
| **Overall** | **C+** | **C+** | **No movement** |

---

## PRIORITY REMEDIATION LIST — CYCLE 10

In order of urgency:

1. **CRITICAL — Rewrite byte.md Section 10 from scratch for the oval body.** Every turnaround view description must describe an oval body. Remove all references to cube faces, chamfered corners, triangular notches, cube depth ratios, and cube geometry. The turnaround production notes must reflect oval construction. This is not a light editing pass — it is a full section replacement.

2. **CRITICAL — Audit and purge all remaining cube references from byte.md.** Minimum affected locations: Section 2 (limb expression header), Section 4 (color table), Section 8 (face plane description), Section 11 (DO NOT list, silhouette test, size comparison). Every instance of "cube," "chamfered corner," and "triangular notch" outside the retired design note must be evaluated and either removed or replaced with oval-appropriate language.

3. **CRITICAL — Regenerate Byte turnaround PNG using oval body geometry.** The current byte_turnaround.png may represent the retired cube design. If so, it is misinformation in asset form. Regenerate immediately.

4. **HIGH — Produce a show logo / title card asset.** Assign this to someone with graphic design capability. Minimum deliverable: a typographic treatment of "Luma & the Glitchkin" in a defined font at defined scale with defined color treatment. One file. One spec note. It does not have to be final — it has to exist.

5. **HIGH — Produce a composite reference image** showing all four main characters at correct relative scale, in full design. This is a standard pitch deck deliverable that remains missing after multiple critique cycles.

6. **HIGH — Produce turnarounds for Cosmo and Miri.** Luma and Byte have turnarounds (with caveats). Cosmo and Miri have locked designs but no turnaround assets. Add them.

7. **MEDIUM — Apply LTG naming convention to new files immediately.** The checklist exists. The convention is documented. New files from Cycle 9 are non-compliant. There is no acceptable reason for this. Cycle 10 files must be compliant from creation.

8. **MEDIUM — Rename the compliance checklist itself** to `LTG_PROD_naming_convention_compliance_checklist_v001.md`.

9. **MEDIUM — Complete the batch renaming of legacy output files.** This has been deferred since Cycle 8. Schedule it, assign it, and complete it.

10. **LOW — Fix tools directory location** — either move tools to `production/tools/` or update the production bible to reflect `output/tools/`.

---

## CLOSING ASSESSMENT

Nine cycles in. The core creative work — world-building, palette logic, character design, cold open storyboard — remains genuinely strong and continues to develop. Sam Kowalski's Section 7 is the kind of rigorous, clear documentation this package needs more of. Miri locking is overdue but completed.

But the show cannot pitch with a design document where the character's body shape changes depending on which section you read. It cannot pitch without knowing what the title looks like. It cannot pitch with a naming system that exists as a checklist no one is using.

The team is doing work. The team is not doing the right work. We are nine cycles in and I am still writing the same three paragraphs I wrote in Cycle 8. Fix Byte. Make a logo. Name your files correctly.

The grade does not move until those three things are done.

---

*Fiona O'Sullivan — Production Design Specialist*
*Critique prepared for relay to Art Director (Alex Chen)*
*2026-03-29*
