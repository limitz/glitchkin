# TECHNICAL PIPELINE & ASSET QUALITY REVIEW
## "Luma & the Glitchkin" — Cycle 2 Critique
**Reviewer:** James "JT" Thornton, Technical Pipeline & Asset Quality Reviewer
**Date:** 2026-03-29
**Documents Reviewed:**
- `output/production/production_bible.md` (Production Standards section)
- `output/backgrounds/production_outline_exceptions.md`
- `output/backgrounds/props/pixel_face_continuity.md`
- `output/production/fx_confetti_density_scale.md`
- `output/production/fx_spec_cold_open.md`
- `output/backgrounds/environments/lumas_house_interior.md` (Production Specs)
- `output/backgrounds/environments/glitch_layer.md` (Production Specs)
- Directory tree: `output/` (full recursive listing)

---

## Overall Assessment

This production has strong creative documentation. Some of these specs — particularly the FX confetti density scale and the pixel face continuity tracker — are well above average for a project at this stage. The art director clearly has a vision and has worked to codify it.

That said, this pipeline has significant structural problems that will cause real production pain at scale. The naming convention system is partially implemented and partially ignored. The directory structure in the production bible does not match what is actually on disk. There is no version-controlled asset manifest, no asset status tracker, and no clear FX compositing software specification. Critical technical metadata is scattered across documents with no central lookup.

**Pipeline Readiness Score: 4/10.** Creative documentation: 8/10. Technical infrastructure: 2/10.

If a new background artist joins this production tomorrow and is told "follow the standards," they will have contradictions to navigate immediately and no way to know which document wins.

---

## File Organization & Naming Conventions

### The Production Bible Specifies a Directory Structure That Does Not Exist

The production bible (Section 9, Directory Structure) defines the following subdirectories:

```
characters/
  main/
  supporting/
  extras/         ← DOES NOT EXIST ON DISK
  turnarounds/    ← DOES NOT EXIST ON DISK
backgrounds/
  environments/
  props/
  layouts/        ← DOES NOT EXIST ON DISK
storyboards/
  sequences/      ← DOES NOT EXIST ON DISK (storyboards are flat in /storyboards/)
  thumbnails/     ← DOES NOT EXIST ON DISK
production/
  tools/          ← DOES NOT EXIST ON DISK
  templates/      ← DOES NOT EXIST ON DISK
```

What actually exists on disk:
```
output/
  style_guide.md
  characters/main/
  characters/supporting/
  backgrounds/environments/
  backgrounds/props/
  storyboards/           ← flat, no sequences/ or thumbnails/ subdirectory
  color/palettes/
  color/color_keys/
  color/style_frames/    ← NONE of these are in the production bible directory spec
  production/            ← flat, no tools/ or templates/ subdirectory
```

The `color/` directory hierarchy — `palettes/`, `color_keys/`, `style_frames/` — appears nowhere in the production bible. It was built and populated without being added to the canonical directory spec. This means the spec is already stale on Day 1.

The storyboards directory spec calls for `sequences/` and `thumbnails/` subdirectories. The actual file `ep01_cold_open.md` sits at the root of `/storyboards/` with no subdirectory organization.

**This is a blocker for onboarding.** Any new team member reading the production bible and then looking at the actual disk will immediately hit a discrepancy and not know which to trust.

### Two Incompatible Naming Convention Systems Are Running in Parallel

The production bible (Section 9) specifies a universal naming convention:

```
[category]_[descriptor]_[version].[ext]
```

Examples from the bible: `char_luma_designsheet_v01.png`, `bg_millbrook_lumashome_exterior_day_v01.png`

The environment design documents define their own environment-local prefixes that do not follow this pattern:

- `lumas_house_interior.md` specifies: `LH_INT_[shot-code]_v[##].psd` and `LH_INT_[shot-code]_FINAL.png`
- `glitch_layer.md` specifies: `GL_[shot-code]_v[##].psd` and `GL_[shot-code]_FINAL.png`

These two conventions are not the same. The production bible says `bg_millbrook_lumashome_exterior_day_v01.png`. The environment doc says `LH_INT_WIDE_ESTAB_v01.psd`. A delivery package built from environment doc specs will be full of files that do not match the production bible's sorting/categorization conventions.

Additionally, the `_FINAL` suffix designation in the environment docs conflicts with the production bible's versioning spec, which states: "Current canonical version is always the highest number unless explicitly marked `_FINAL`." The environment doc uses `_FINAL` as a routine delivery format designation (e.g., `LH_INT_WIDE_ESTAB_FINAL.png`), not as an exceptional override. If `_FINAL` is both "this overrides the version number" AND "this is just the export format," the designation is meaningless.

### Naming Convention Omissions

The production bible naming examples cover: `char_`, `bg_`, `color_`, `sb_`, `prop_`. There is no established naming prefix for:
- FX documents / FX assets (the FX spec docs are under `production/` but no naming convention covers FX asset files: particle sheets, shimmer overlays, blend mode layers)
- Critique documents (these currently sit in `production/` alongside the production bible and specs with no prefix: `critique_carmen_reyes.md`, etc.)
- Style frames (in the `color/style_frames/` directory — the production bible lists style frames under file formats but gives no naming convention example)
- Storyboard PDFs vs. storyboard markdown source docs (the storyboard naming example is `sb_ep01_seq03_v01.pdf` but the actual file is `ep01_cold_open.md` — wrong prefix, wrong extension, no version number)

The file `ep01_cold_open.md` fails the naming convention on three counts: no category prefix, no version number, wrong extension for a document that the bible says should ship as PDF.

---

## Resolution & Format Standards

### The 300 DPI / 72 DPI Dual Specification Is Incomplete

Both `lumas_house_interior.md` and `glitch_layer.md` list two resolution values:
- Print-ready resolution: 300 DPI
- Screen delivery resolution: 72 DPI

This creates an immediate question: which file is the master? At 1920x1080 pixels, 72 DPI gives you a 26.67" x 15" physical document. At 300 DPI, the same 1920x1080 pixel canvas is a 6.4" x 3.6" physical document. These are the same pixel dimensions. DPI metadata on a screen-delivery PNG is not the resolution — it is metadata that affects how print software interprets the file. The environment specs list "300 DPI" and "72 DPI" as if they are two different physical outputs, but the canvas size listed is 1920x1080px in both cases.

The production bible (Section 9) specifies delivery resolution as 1920x1080 and working resolution as optionally 3840x2160 (2x). It does not mention DPI at all. The environment docs add DPI specs that the production bible does not define, contradict each other in purpose (print vs. screen), and do not specify what the actual working file resolution should be when the 2x working resolution option is used. If an artist works at 3840x2160 per the production bible, and exports to 1920x1080, the "300 DPI" notation on the export is irrelevant metadata.

**This needs a single, unambiguous statement:** "All deliverables are 1920x1080px. DPI metadata on PNG exports must be set to 72 DPI. Source PSD files may be 3840x2160px for 2x working resolution."

### No Color Space Management Specification

The environment docs specify sRGB color space. The production bible does not mention color space at all. No document specifies:
- Whether source files must be 8-bit or 16-bit per channel
- How to handle color space conversion from working files to delivery
- What color profile must be embedded in deliverables
- Whether compositing is expected to happen in linear light or gamma-corrected space

This is not a minor omission. FX work with additive and multiply blend modes (specified extensively in `fx_spec_cold_open.md`) will look different in linear vs. gamma-corrected compositing environments. If nobody specifies this, every FX artist will default to whatever their software uses, and the composited result will vary.

### Particle Size Specifications Create Rounding Issues

`fx_spec_cold_open.md` states particles must be multiples of 2px (2px, 4px, 8px, 16px, 32px). The density scale document specifies particle sizes like "2×2 px to 4×4 px" for Level 1 and "3×3 px to 8×8 px" for Level 2.

Level 2 specifies 3×3 px as the minimum, but the cold open spec says no odd pixel sizes. These two documents conflict. A 3×3px particle is explicitly forbidden by the cold open spec's technical requirements and simultaneously listed as the Level 2 minimum particle size by the density scale spec. An FX artist following one document will violate the other.

---

## FX Technical Specifications

### No Compositing Software Is Named

`fx_spec_cold_open.md` is the most technically detailed document in this pipeline. It specifies blend modes (Screen, Additive, Multiply, Normal), opacity values down to single percentage points, per-layer ordering, frame durations at 24fps, and RGB hex values for every element.

It does not name a compositing application. Not once.

"Additive blend mode" is implemented differently in After Effects vs. Nuke vs. Toon Boom Harmony vs. Blender's compositor. "Screen blend mode" on a layer in Photoshop is not the same operation as a Screen node in Nuke in a linear-light pipeline. The spec is detailed enough to be useful only if the reader knows which software these blend modes refer to.

There is no document in the output folder that names the production's compositing software. This is a critical gap.

### The Layer Order Specs Have No Source-File Correspondence

`fx_spec_cold_open.md` provides layer orders for all three FX sequences, numbered 1 through 8-10. These are described in plain English (e.g., "CRT screen breach glow (Electric Cyan inner glow on breach edges) — additive blend mode"). There is no specification for:
- How many separate files or pre-comps these layers represent
- Whether the FX layers are delivered as separate PNGs, an animated sprite sheet, a vector file, or baked into the background
- Whether the "Byte character art" layer in the FX stack is the same layer group as the character animation layer, or a separate FX pass

An FX technical lead receiving this document cannot create a compositing template without answering these questions first. Those answers should be in the spec.

### The Cold Open Spec References "Panel 7" and "Panels 23-24" Without a Panel List

`fx_spec_cold_open.md` references "Scene Reference: Panel 7 area" and "Scene Reference: Panels 23–24 area." The storyboard document `ep01_cold_open.md` may contain this information, but there is no confirmed panel count for the cold open storyboard documented anywhere. If panel numbering changes during storyboard revision (which it will), this FX spec has no way to track the change. Panel references in a spec should be shot codes, not panel numbers — panel numbers are ephemeral, shot codes are stable.

### Level 2 Duration Limit vs. Cold Open Runtime

`fx_confetti_density_scale.md` states: "Do not hold Level 2 for more than 60 consecutive seconds of screen time." The cold open FX spec describes an extended sequence in FX Moment 3 (Monitors Flickering to Life) that holds at Level 2 across roughly 60 frames (2.5 seconds) for the simultaneous flicker event, then describes a post-flicker "wonder state" at Level 1-2 for an additional 30 frames (1.25 seconds). That is fine by itself. However, if the cold open is 60-120 seconds total and all three FX moments are occurring within it, no document specifies how the density transitions between FX moments are handled in the time between them. Do they drop to Level 0 between moments? Level 1? The transition rules in the density scale doc say "return to Level 1 (never 0 unless dramatically motivated)" after a Level 3 event, but the cold open structure has Moment 1 ending at Level 1, then Moment 2 running through a Level 3 spike. The transition from the end of Moment 1 to the start of Moment 2 is not specified — what is the density during the animation between landing and the desk-impact event?

---

## Continuity & Asset Tracking Systems

### The Pixel Face Continuity Document Is Well-Constructed — But Not Integrated

`pixel_face_continuity.md` is the best-executed tracking document in this pipeline. The episode-by-episode log table with artist sign-off fields, the rule hierarchy, the expression vocabulary — this is solid work. I have two issues:

First, there is a logical inconsistency in the episode log. The table lists Episode 9 as "Absent" for the face, but the Rule 3 documentation describes the "Fractured" expression (asymmetric right eye) as applying to Episode 9, with a note: "Reserved for future if face appears earlier than Ep 12." The table and the rules are not synchronized — the rule exists, but the table does not show it as applicable, with only a vague explanatory note. If a new artist handles Episode 9 backgrounds and reads the table, they see "Absent." If they read the rules, they see an Episode 9-specific expression defined. This is a continuity error waiting to happen.

Second, the document references a "continuity supervisor" in its production notes. There is no continuity supervisor on the current team roster. This role is referenced but not staffed.

### No Master Asset Register

There is no document in the output folder that functions as a master asset register — a list of every approved deliverable, its status (in progress, approved, delivered, superseded), its current version number, and who approved it.

The production bible specifies that "no asset ships without Art Director review" and that artists must "increment the version number" and "never overwrite." These are correct policies. But without an asset register, there is no way to audit compliance. You cannot enforce a version numbering policy if nobody is tracking the version numbers.

### No Episode Asset Matrix

For a 13-episode season, you need a matrix showing which environments, props, characters, and FX elements appear in which episodes. This serves two purposes: scheduling (knowing which assets must be complete before an episode's production starts) and continuity checking (the pixel face continuity doc does this for one prop — there is no equivalent for the other continuity-tracked elements: the cable additions in Episodes 3 and 8, the traffic cone accessories in Episodes 7 and 11, the map annotations above the desk).

The `lumas_house_interior.md` lists multiple long-term story gags that change across the season. None of them have a tracking document equivalent to `pixel_face_continuity.md`. They are described in a prose list with no sign-off structure.

### The Statement of Work Does Not Reference a Deliverables Schedule

`statement_of_work_cycle_01.md` exists in the production folder. This review did not read its full contents, but its presence without an associated schedule or milestone tracker means there is no mechanism to determine whether the project is on track against it.

---

## Missing Technical Specifications

The following information is absent from all documents reviewed:

1. **Compositing software.** Not named anywhere.

2. **Animation software.** Not named anywhere. Character art is described in detail. How it is animated — what software, what frame rate for the working files vs. playback, whether the show uses cut-out animation or frame-by-frame — is never specified.

3. **Source file format for character designs.** The production bible says "source file" as the delivery format for character design sheets but does not specify the application (PSD, TVPaint, Animate, Storyboard Pro, etc.).

4. **Audio format requirements.** The FX specs contain sound design notes (the CRACK sync point in Frame 23-24, the Level 4 audio description). No document specifies audio format, sample rate, bit depth, or channel count for sound design deliverables. This matters for pipeline integration.

5. **Safe zone markings in working files.** The production bible specifies action safe at 90% and title safe at 80%. No document specifies whether these zones must be present as guides in the PSD master files.

6. **Bit depth for deliverables.** 8-bit vs. 16-bit PNG is not specified. The additive and screen blend operations in the FX specs will show visible banding in 8-bit files at low opacity values.

7. **Frame size for storyboard exports.** The production bible says "PDF (panels at 16:9 aspect)" for storyboards. It does not specify the pixel dimensions of storyboard panels within the PDF, whether panels are one per page or multiple per page, or what the minimum line weight is for storyboard readability.

8. **Version control system.** The production bible says files are "version-controlled" for production documents. No document specifies what version control system is in use. Git? A shared drive with folder naming? A production management tool? This matters enormously for how "never overwrite" is enforced and how rollbacks work.

9. **Texture overlay source files.** Multiple documents reference texture overlays (grain texture at 15-20% opacity for walls, scan-line overlays, dither patterns). No document specifies where the master texture files live, what format they are, or whether they are shared assets that must match across all environments.

10. **Color space for FX compositing.** As noted above — linear light vs. gamma, and which compositing application is the authority.

---

## Critical Issues

**CRITICAL 1 — Naming Convention Conflict.** Two systems are running simultaneously (production bible `[category]_[descriptor]_[version].[ext]` vs. environment doc `LH_INT_[shot-code]_v[##].psd`). Assets produced under each system will not sort or search consistently. Must be resolved before any final deliverable is built. **One system. One document. Zero exceptions.**

**CRITICAL 2 — Directory Structure Out of Sync With Spec.** The `color/` hierarchy exists on disk but not in the production bible. Required subdirectories in the bible (`extras/`, `turnarounds/`, `layouts/`, `sequences/`, `thumbnails/`, `tools/`, `templates/`) do not exist. The spec is the wrong document to hand to a new team member. Fix the spec to match reality, or fix reality to match the spec. Either is acceptable. Both being wrong simultaneously is not.

**CRITICAL 3 — No Compositing Software Specified.** Blend mode specs are meaningless without naming the compositing application. The FX specs are detailed enough to be immediately useful — if the software context is established. Until it is, an FX artist will make assumptions and those assumptions will be wrong about 30% of the time in ways that are invisible until final composite review.

**CRITICAL 4 — Particle Size Conflict.** Level 2 minimum particle size (3×3 px, from density scale spec) violates the particle size rule (multiples of 2px only, from cold open spec). One of these documents is wrong. Determine which rule is authoritative and update the other.

**CRITICAL 5 — `_FINAL` Suffix Ambiguity.** The environment docs use `_FINAL` as a standard delivery format designation. The production bible uses `_FINAL` as an override for the highest-version canonical rule. These cannot both be true. `_FINAL` either means "this is the one you use" or "this is the delivery format" — not both.

---

## Recommendations

1. **Reconcile the naming conventions.** Choose one system. My recommendation: adopt the environment-doc prefix system (`LH_INT_`, `GL_`, etc.) because it is more specific and will scale better across 13 episodes and multiple locations, but update the production bible to reflect it and add prefixes for every asset category including FX, critique docs, and style frames.

2. **Update the production bible directory structure to match what is actually on disk.** Create the missing subdirectories (`characters/extras/`, `characters/turnarounds/`, `backgrounds/layouts/`, `storyboards/sequences/`, `storyboards/thumbnails/`, `production/tools/`, `production/templates/`) or remove them from the spec. Today, not next cycle.

3. **Add a single page to the production bible: Technical Stack.** Name the compositing software, the animation software, the bit depth, the color space, the version control system. One page. This is the most high-value hour of writing this production could do right now.

4. **Create a master asset register.** A spreadsheet or markdown table: asset name, category, current version, status, approver, date approved. Even a minimal version of this pays for itself by Episode 3.

5. **Create a season continuity tracker.** The pixel face continuity doc is the right model. Replicate it for every item on the long-term story gag list in `lumas_house_interior.md`: the cable additions, the traffic cone accessories, the map annotations. These are currently described in prose with no sign-off structure.

6. **Fix the storyboard file.** `ep01_cold_open.md` needs a version number, a category prefix, and a format decision (is this the source document that will become a PDF, or is this the deliverable?).

7. **Resolve the Episode 9 / Fractured expression conflict** in `pixel_face_continuity.md`. The rule says one thing; the episode log says another. Pick one and update both tables to match.

8. **Clarify the DPI specification.** Remove the "300 DPI / 72 DPI" dual listing from environment docs. Replace with: "Canvas size: 1920x1080px. PNG exports: 72 DPI metadata. Source PSDs: 1920x1080 or 3840x2160 (2x working)."

9. **Anchor FX spec panel references to shot codes.** Replace "Panel 7 area" and "Panels 23-24 area" in `fx_spec_cold_open.md` with shot codes that will remain stable across storyboard revisions.

10. **Define texture overlay master files.** Specify where shared textures (grain, scan-line, dither) live in the directory, what format they are, and which version is canonical. An artist who rebuilds these from scratch for each environment will produce inconsistent results.

---

## Verdict

This production has done the creative work to a high standard and the documentation effort is genuine. The FX density scale document alone is better than most pipeline specs I see at this stage. The outline exception document is clear and will actually be usable on set.

But the technical infrastructure to support that creative work is not built yet. The naming conventions contradict each other. The directory structure on disk contradicts the spec. Critical technical choices — compositing software, bit depth, color management, version control — are not documented. The pixel face continuity system is excellent but exists in isolation; the other continuity-sensitive story elements across the season have no equivalent.

**A team member who joins this production today, reads the documentation, and sits down to work will hit a naming convention conflict before they finish their first file.** That is not a creative problem. That is a pipeline problem, and pipeline problems compound with every episode added.

Fix the spec. Build the asset register. Name the software. Then this foundation can hold up a 13-episode season.

---

*James "JT" Thornton — Technical Pipeline & Asset Quality Review*
*"Creative brilliance means nothing if I can't find the file or it's the wrong DPI."*
