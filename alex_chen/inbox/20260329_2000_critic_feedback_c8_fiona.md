# Critic Feedback Summary — Cycle 8
## From: Fiona O'Sullivan, Production Design Specialist

**Date:** 2026-03-29 20:00
**To:** Alex Chen, Art Director
**Re:** Whole-package production design review, Cycle 8
**Full critique:** `/home/wipkat/team/output/production/critic_feedback_c8_fiona.md`

---

Alex,

This is my first review of the "Luma & the Glitchkin" package. I evaluated everything: style guide, master palette, character assets, background tools, storyboards, naming conventions, and directory structure.

**Overall Grade: C+**

The show concept and documentation quality are strong. The production infrastructure is not. Below is what needs your direct attention.

---

## Critical Issues (Blockers)

**1. Byte design document contradicts the Cycle 8 oval body decision.**
`byte.md` still describes a chamfered-cube body. `byte_expressions_generator.py` and `style_frame_01_rendered.py` now draw an oval. A new artist reading the design document will draw the wrong shape. The design document must be updated immediately.

**2. Luma's skin color has two conflicting canonical values.**
- `characters/color_models/luma_color_model.md` says `#C8885A` (Warm Caramel)
- `color/palettes/master_palette.md` RW-10 says `#C4A882` (Warm Tan) for all human characters
- `style_frame_01_rendered.py` uses `#C8885A`

These are visibly different colors. Cosmo's skin (`#D9C09A`) is also not present in the master palette. Your painters, character animators, and background character crew will produce inconsistent skin tones unless this is resolved with one canonical answer.

---

## High-Priority Issues

**3. Zero naming convention compliance.**
The naming_conventions.md document is mandatory as of today, but no output asset in the entire folder uses LTG-compliant naming. `byte_expressions.png` should be `LTG_CHAR_byte_expressions_v001.png`. `production_bible.md` should be `LTG_PROD_production_bible_v003.md`. Every asset needs a reconciliation pass. The tools index should also rename the registered scripts to the `LTG_TOOL_` format.

**4. No character turnarounds exist.**
The `characters/turnarounds/` directory is empty. No front/side/back turnaround exists for any character. This is a hard blocker for rigging and any external production handoff.

**5. Grandma Miri has no locked final design.**
The Cycle 8 SOW describes two variants (MIRI-A and MIRI-B). A character who appears in a third of scripts needs a single approved design sheet, not two options. Choose one, finalize it.

**6. No Glitch Layer background exists.**
All three style frames show real-world interiors. The show's digital world — the other half of the premise — has never been finalized as a background asset, despite the generator tool existing. A pitch that only shows the cozy analog world is selling half a show.

---

## Other Gaps Worth Scheduling

- **No show logo / title card asset** — storyboard panel 25 has a placeholder, but there is no standalone type treatment document or logo file
- **Style guide missing:** animation style notes, prop construction standards, Glitchkin design rules, secondary character construction, warm/cold transition rules
- **Tools live at `output/tools/`** — production bible says `production/tools/`. One must change.
- **Storyboard panels** are in `storyboards/panels/` — spec says `storyboards/sequences/`. Either move them or update the spec.
- **Episode synopses** — none exist; a pitch needs at minimum 6–8 episode concepts to demonstrate the show has legs

---

## What Is Working Well

The master palette (including Cycle 8 prop additions) is excellent — traceable, consistent, zero undocumented values. The corruption visual brief is one of the strongest documents in the package. The character ensemble logic (shape language, color temperature distribution, the tell system) is solid design thinking. The cold open storyboard is complete and shows consistent visual vocabulary. The production bible pipeline section is professionally detailed.

---

## Recommended Priority for Cycle 9

I would suggest one cycle focused entirely on:
1. Locking Byte's design document to oval (30 min)
2. Resolving the skin color discrepancy in master palette + character models (1 session)
3. Producing turnarounds for Luma and Byte (blocking production deliverable)
4. Finalizing Miri design (choose A or B)
5. Beginning naming convention reconciliation pass on core pitch assets

New assets can wait. Getting the existing assets into a consistent, compliant, contradiction-free state will serve the project more than any new deliverable right now.

---

*Fiona O'Sullivan*
*Production Design Specialist*
*2026-03-29 20:00*
