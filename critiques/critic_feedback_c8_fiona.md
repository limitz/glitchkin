# Critic Feedback — Cycle 8
## Production Design & Package Consistency Review
### "Luma & the Glitchkin"

**Critic:** Fiona O'Sullivan — Production Design Specialist
**Date:** 2026-03-29
**Cycle:** 8 (First review of this project by this critic)
**Scope:** Whole-package evaluation — style guide completeness, cross-tool consistency, naming convention compliance, asset organization, pitch package readiness

---

## Overall Grade: C+

The bones are good. The conceptual work on this show is genuinely strong — the world is clearly defined, the palette has logic, and there is evident love and care in the documentation. But this package is nowhere near production-ready, and several of the problems I am about to describe are the kind that silently compound until a studio development executive opens a shared folder and loses confidence in the team's ability to deliver. This review is not gentle because the work does not merit gentleness yet. Every problem I name below is fixable. Fix them.

---

## 1. STYLE GUIDE ASSESSMENT

### What Exists
The primary style guide lives at `/home/wipkat/team/output/style_guide.md` — a flat file at root level. The production bible references a `style_guide/` subdirectory (plural, a folder), but no such folder exists. The style guide is a single file, not a system. This is a meaningful structural gap.

**What the style guide covers well:**
- Shape language per character — clear, specific, correctly differentiated
- Color palette principles for real world vs. glitch palettes — well-articulated
- Background art direction — the warm/flat painterly hybrid is defined with enough specificity to be usable
- Line work standards — character vs. background line weight distinction is clear
- Visual dos and don'ts — useful, specific, not generic

**What the style guide is missing entirely:**

1. **No animation style reference.** There is a float physics spec for Byte in the production folder, but the style guide itself says nothing about movement style, timing philosophy, or squash-and-stretch expectations. A show bible's style guide without animation style notes is a character design guide, not a production style guide. These are not the same thing.

2. **No title card / graphic design standards.** No type treatment. No title font specification. No logo standards. No lower-third or caption style. A pitch package without these is not a pitch package — it is a character bible fragment. The title card format produced in storyboards (the panel_p25_title_card.png) exists as a storyboard frame, not as a graphic design spec document.

3. **No turnaround model sheets for any character.** The `characters/turnarounds/` directory exists in the folder structure but is completely empty. There is not a single front/side/back turnaround in this entire package. This is a fundamental character production deliverable. Without turnarounds, you cannot rig a character consistently across a crew. This is a hard blocker for production.

4. **No secondary character style specification.** Glitchkin are described conceptually in the bible and corruption brief, but there is no style guide section explaining construction rules for episodic Glitchkin designs. How jagged? How asymmetric? What is the minimum readable size? What makes a Glitchkin "not a corruption fragment"? Without this, every episode's Glitchkin designer is working from scratch.

5. **No transition rules for the warm/cold visual zones.** The real world vs. glitch layer palette logic is excellent on paper. But when are we in a "transition zone"? What rules govern how real-world colors desaturate as glitch energy increases? The corruption visual brief touches this for Corruption-specific events (Stage 1/2/3 desaturation halos), but there are no general rules for ambient glitch contamination without a full Corruption event. Background artists will invent their own rules. They will be wrong.

6. **No prop design style guide section.** The `key_props.md` and `pixel_face_continuity.md` documents exist in the backgrounds/props folder but the style guide itself has no props section. Props used in close-up (Cosmo's notebook, Miri's mug, the CRT monitor — the most important prop in the show) need design standards just as characters do.

**Score: 6/10.** Strong foundation, but missing critical production-layer specifications that would make this actually usable as a crew reference.

---

## 2. CROSS-TOOL CONSISTENCY

### Byte Body Shape — RESOLVED but only for this cycle
The most significant cross-tool consistency issue I found has been corrected in Cycle 8: `byte_expressions_generator.py` and `style_frame_01_rendered.py` now both use an oval/ellipse body for Byte. The decision is explicitly noted in `byte_expressions_generator.py` line 255 with a comment confirming the Cycle 8 fix and retirement of the chamfered-box polygon.

However — and this is important — the character design document at `characters/main/byte.md` still describes Byte's body as **"a modified cube... the base shape is a cube where the edges have been chamfered"** (Section 2). The design document has not been updated to reflect the oval decision. This means a new artist reading the design document will draw Byte as a chamfered cube. The person reading the style frame reference and expression sheet will see an oval. A third artist trying to reconcile these will either guess or ask — and if they ask, they will find conflicting source-of-truth documents.

**This is an unresolved documentation inconsistency.** The fix in the Python scripts is insufficient. The design document must be updated.

### Luma Skin Color — UNRECONCILED DISCREPANCY
This is the clearest hard inconsistency I found in the package.

- `characters/color_models/luma_color_model.md` specifies Luma's skin base as **`#C8885A`** ("Warm Caramel")
- `color/palettes/master_palette.md` specifies the show's universal skin base as **`#C4A882`** ("Warm Tan") — RW-10
- `tools/style_frame_01_rendered.py` uses **`(200, 136, 90)`** = **`#C8885A`** for SKIN (Luma's skin in the rendered composite)

So the character color model and the rendered style frame agree with each other at `#C8885A` — but the master palette says all human characters use `#C4A882`. These are meaningfully different colors: `#C8885A` is a richer, darker, more saturated caramel; `#C4A882` is a lighter, more desaturated warm tan. They are not interchangeable. A background character painter using the master palette will paint Luma's skin lighter than a character animator using the character color model.

The Grandma Miri color model correctly uses a distinct deep brown skin tone (`#8C5430`), which is correct for her character and consistent with the ensemble's diversity. But what is the canonical base for Luma's skin? The package currently has two conflicting answers.

**Cosmo's skin** (`#D9C09A`) in his color model is also not present in the master palette as a named swatch. The master palette's RW-10 (`#C4A882`) does not match Cosmo's model. With three characters potentially having three different unlisted skin bases, the show lacks a consistent skin tone system that a colorist or background character painter could navigate without calling the character designer.

### Background Tool Color Usage — Generally Consistent
`bg_layout_generator.py` uses hardcoded RGB tuples that match the master palette values for the major environment colors. The monitor wall `(22, 16, 30)` maps to a close approximation of Void Black. The warm amber wall `(212, 146, 58)` matches RW-03 Sunlit Amber exactly. The cyan monitor screen `(0, 212, 232)` matches GL-01b Byte Teal precisely — which is the correct choice for screen ambient glow (not pure Electric Cyan). This is a minor positive finding: Jordan's background tool respects the palette hierarchy.

However, the background tool uses **no named constants** — all colors are hardcoded inline tuples. This means there is no enforcement mechanism. A future change to the master palette does not propagate to background tools unless someone manually hunts and updates every inline tuple. The character tools (byte_expressions_generator.py) use named constants correctly (BYTE_TEAL, ELEC_CYAN, etc.). The background tools should do the same.

### Pixel Confetti — Consistent in Spec, Untested in Output
The confetti particle system is specified in the FX density scale, referenced in the byte float physics document, visible in style frame scripts, and documented in the master palette's glitch section. The specification is internally consistent across documents. What does not exist is any asset that shows the confetti system behaving correctly across different backgrounds — specifically, no test frame showing confetti against a warm real-world background, confetti against a cyan-dominant Glitch Layer environment, or corrupted confetti particles near a Stage 1 Corruption site. These are production-critical tests that have not been made.

---

## 3. NAMING CONVENTION COMPLIANCE

This is the area of most significant failure in the package.

The naming conventions document is excellent — specific, well-structured, and mandatory as of 2026-03-29. The problem is that **nothing in the output folder actually follows it.**

Every deliverable asset in the package uses a different naming system:

| Asset | Actual Filename | Required Naming |
|---|---|---|
| Character design | `byte.md` | `LTG_CHAR_byte_designsheet_v001.md` |
| Expression sheet | `byte_expressions.png` | `LTG_CHAR_byte_expressions_v001.png` |
| Background | `frame01_house_interior.png` | `LTG_ENV_lumas-house-int_v001.png` |
| Style frame | `style_frame_01_rendered.png` | `LTG_COLOR_styleframe_discovery.png` |
| Master palette | `master_palette.md` | `LTG_COLOR_palette_master_v002.md` |
| Production bible | `production_bible.md` | `LTG_PROD_production_bible_v003.md` |
| Storyboard panels | `panel_p01_exterior.png` | `LTG_SB_ep01_cold_open_p01_v001.png` |
| Tools | `bg_layout_generator.py` | `LTG_TOOL_bg_layout_generator_v001.py` |

The naming conventions document acknowledges that prior systems are retired and that a reconciliation pass is pending. But the reconciliation pass has not happened. Cycle 8 has come and gone, and the output folder is still entirely non-compliant. This is not a minor housekeeping issue. A real production pipeline routes assets by filename. An outsourcing partner or studio library system cannot correctly categorize, version-track, or retrieve assets from a folder full of casually-named markdown files and generic snake_case PNGs.

The naming_conventions.md document names itself in the reconciliation plan — but the document's own file is named `naming_conventions.md`, not `LTG_PROD_naming_conventions_v001.md`. The standard is aspirational, not applied.

**Additionally:** The tools in the README are named without the `LTG_TOOL_` prefix. The README notes that scripts "must follow the standard naming convention: `LTG_TOOL_[descriptor]_v[###].[ext]`" — but none of the registered scripts do. This is circular non-compliance: the document describing the convention violates the convention.

---

## 4. ASSET ORGANIZATION

### Directory Structure: Mixed

The production bible specifies a directory structure. The actual structure mostly follows it but with several gaps:

**Present and correct:**
- `characters/main/` — check
- `characters/supporting/` — check
- `characters/color_models/` — present, not in the spec (good addition, but should be in the spec)
- `backgrounds/environments/` — check
- `backgrounds/props/` — check
- `color/palettes/` — check
- `color/color_keys/` — check
- `color/style_frames/` — check
- `production/` — check
- `storyboards/panels/` — present (spec says `sequences/` and `thumbnails/`, not `panels/`)

**Missing entirely:**
- `characters/turnarounds/` — directory exists, zero content
- `characters/extras/` — directory exists, zero content
- `storyboards/sequences/` — directory does not exist (panels are in `panels/`, not `sequences/`)
- `storyboards/thumbnails/` — directory does not exist
- `backgrounds/layouts/` — layouts are stored inside `environments/layouts/`, not at the correct path level

**The `style_guide.md` is a flat file at output root.** The production bible references it at that path. The style guide itself specifies a `style_guide/` subdirectory in the output structure. These are two contradictory specifications. Pick one and enforce it.

**Storyboard panels live in `storyboards/panels/` but are named `panel_p01_exterior.png`.** The spec says storyboard assets should be in `sequences/` subdirectories. The 26 panels constitute a cold open sequence — they should be at `storyboards/sequences/ep01_cold_open/` with the naming convention applied. Currently they are a flat dump of 26 PNGs in a generic panels folder, discoverable only if you know to look there.

### The `output/tools/` folder location is wrong
The production bible specifies tools at `production/tools/`. The tools README is at `output/tools/README.md`. The tools themselves are at `output/tools/*.py`. This is a structural divergence from spec that nobody has corrected. A new team member consulting the production bible to find tools will look in `production/tools/` and find nothing.

---

## 5. WHAT IS MISSING FROM THE PITCH PACKAGE

A pitch package for an animated series typically requires the following to be taken seriously by development executives or commissioning editors. Here is what this package has vs. what it needs:

### Present and Usable
- Logline and elevator pitch — excellent, bible Section 1
- Character descriptions (3 main + 1 supporting) — strong
- World building — strong
- Episode format/structure — clear
- Tone guidelines — clear
- 3 style frames (discovery, glitch storm, other side) — present
- 1 background (house interior) + 3 layout thumbnails — partial
- Cold open storyboard (26 panels) — complete for this sequence
- Master color palette — strong

### Present but Incomplete / Draft Quality
- Grandma Miri: Cycle 8 gives us two variant sketches (MIRI-A and MIRI-B) described in the SOW. But there is no single approved, finalized Miri character design. There are variants, not a final. A character who appears in a third of the scripts should have a locked design. This is a gap.
- Character lineup: Documented in `character_lineup.md` but no actual lineup image showing all four characters at correct relative scale. The image that would exist at `characters/main/proportion_diagram.png` shows characters — but the proportion diagram tool generates abstract height bars, not a proper lineup of designed characters.

### Entirely Missing
1. **Title card / show logo** — Panel 25 of the storyboard has a placeholder title card, but there is no standalone logo design, no type treatment document, and no show title asset that could be placed on a pitch deck. This is embarrassing. A show called "Luma & the Glitchkin" needs to know what its title looks like.

2. **Episode synopsis / series outline** — Not a single episode summary beyond the cold open. A pitch needs at minimum a one-paragraph synopsis for 6-8 episodes to demonstrate the show has legs. The production bible describes the format but contains zero actual episode content.

3. **Animatic** — Not present. Not even referenced as a goal. An animatic of the cold open (even rough) is one of the most persuasive pitch tools available for an animated series.

4. **Supporting cast design sheets beyond Miri** — There are no crowd/extra character designs, no secondary characters who might appear in the pilot, no Glitchkin design system that produces a consistent first-episode creature. The extras directory is empty. No Glitchkin have been designed.

5. **Key props design sheets** — The `key_props.md` document exists and describes props (CRT monitor, Cosmo's notebook, Miri's mug, Luma's hoodie detail). No prop design sheet has been produced. The CRT monitor is the show's most important physical object and it has never been drawn.

6. **Glitch Layer environment** — A layout generator exists for the Glitch Layer and it is in the tool index. But there is no actual finalized Glitch Layer background in the output folder. All three style frames are interior/real-world shots. We have never seen the other world this show is about.

7. **Music and sound design reference** — Not expected in a visual package, but note that the FX spec doc for the cold open specifies sound cues precisely. A pitch package that references audio this specifically without any audio reference (mood board, genre description, reference tracks) leaves that specificity stranded.

8. **Continuity supervisor role** — The production bible (Section 10) clearly states this role "must be filled before Episode 2 begins boarding" and is "a prerequisite for the show entering multi-episode production." No one on the current team fills this role. The pixel face continuity document exists, but continuity supervision is a person-role, not just a document. Calling it out in the bible and then having no one fill it is a credibility problem.

---

## 6. SPECIFIC POSITIVES WORTH NOTING

I do not only report failure. These are genuinely strong:

- **The master palette is excellent.** The shadow companion system, the forbidden combinations section, the Byte/Luma shared visual DNA logic — this is production-grade palette documentation. The Cycle 8 addition of prop colors and deprecation of the undocumented inline grey tuple shows good discipline.

- **The corruption visual brief is exceptional.** It is specific, staged, consistent with the overall visual logic, and provides artists with everything they need to draw the antagonist coherently. The three-stage escalation system with explicit visual markers per stage is exactly the kind of production document that prevents a studio from having fifteen different artists draw "corrupted" environments that look nothing alike.

- **The character design ensemble logic is strong.** The shape language differentiation, color temperature distribution, and "tell" system across all four characters demonstrates genuine design thinking. The Miri/Luma warm family color echo is the kind of subtle system that elevates a show.

- **The cold open storyboard is complete and shows a competent visual vocabulary.** 26 panels covering a full escalation arc, with consistent shot type notations, action notes, and art director flags is production-quality storyboard work.

- **The production bible is thorough.** The open-source pipeline commitment is documented, enforced by the tools index, and the blend mode terminology clarification (Natron standard, not proprietary) demonstrates professional pipeline awareness.

---

## 7. PRIORITY REMEDIATION LIST

In order of urgency for a pitch-ready package:

1. **CRITICAL — Reconcile Byte's design document with the Cycle 8 oval body decision.** Update `byte.md` to reflect the oval body as the current canonical shape. Retire all chamfered-cube descriptions. This is a 30-minute document update that prevents weeks of inconsistent animation.

2. **CRITICAL — Resolve the Luma/Cosmo skin color discrepancy.** Either update the master palette to include character-specific skin bases as named swatches, or update the character color models to align with the master palette's single skin base. Either is acceptable; having both simultaneously is not.

3. **HIGH — Begin the naming convention reconciliation pass.** At minimum, rename the output files that will be included in the pitch package to LTG-compliant names. The tool scripts should be renamed and their hardcoded output paths updated.

4. **HIGH — Produce character turnarounds for Luma and Byte.** These are minimum blocking deliverables. Without front/side/back turnarounds, no character can be handed off to any external animator or rigger.

5. **HIGH — Produce a finalized Grandma Miri design (choose A or B, lock it, produce a design sheet).**

6. **HIGH — Produce a Glitch Layer background.** Three style frames showing a cozy interior is not a full pitch. The show's second world needs a visual.

7. **MEDIUM — Produce a show logo/title card asset.** Even a simple typographic treatment is better than nothing.

8. **MEDIUM — Update the style guide to cover animation style, props, and secondary character (Glitchkin) construction rules.**

9. **MEDIUM — Fix the tools directory location** (production bible says `production/tools/`, tools live at `output/tools/`).

10. **LOW — Populate `storyboards/sequences/` and `storyboards/thumbnails/` directories or update the spec** to match the actual `storyboards/panels/` structure that exists.

---

## Summary

This package has a strong creative foundation that a dedicated team has clearly been building thoughtfully over multiple cycles. The conceptual and documentation work is above average for a show in early development. But the production infrastructure — naming conventions, directory compliance, asset completeness, and cross-document consistency — is in a state that would concern any production supervisor receiving this folder for the first time.

The most actionable cycle-to-cycle improvement would be: stop adding new documents and spend one cycle on nothing but (a) locking the Byte design spec inconsistency, (b) the naming convention reconciliation, and (c) producing turnarounds for at least Luma and Byte. Those three items would move the package from "promising development folder" to "credible pitch package in progress."

The show is good. The package needs work.

---

*Fiona O'Sullivan — Production Design Specialist*
*Critique prepared for relay to Art Director (Alex Chen)*
*2026-03-29*
