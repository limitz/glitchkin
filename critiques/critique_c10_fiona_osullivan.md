# Critique — Cycle 10
## Production Design Review: "Luma & the Glitchkin"
**Critic:** Fiona O'Sullivan, Production Design Critic
**Date:** 2026-03-29
**Scope:** ltg_render_lib.py / Tool Naming & Organization / Character Sheet Consistency

---

## Priority 1 — ltg_render_lib.py: Shared Rendering Library

**Grade: B+**

### What works

The library is a genuine production engineering achievement. Seven functions, zero circular dependencies, Pillow-only — this is a clean, importable utility that any team member can drop in with three lines of setup code. The module docstring at the top even gives the exact import pattern, which removes friction entirely for non-Kai contributors. That is exactly what a shared library should do.

Documentation quality is high. Every function has a full docstring: purpose, algorithm note, every parameter named and typed, return value described. The distinction between functions that modify in-place (returning the same object) vs. functions that return new objects (`perlin_noise_texture`) is clearly noted. The `Note:` in `dust_motes` about RGBA requirement versus RGB silently-ignoring alpha is precisely the kind of production trap that would otherwise waste half a day for a non-technical artist.

Seeded RNG for reproducibility is the correct production choice — every call with the same seed produces the same output, making re-renders deterministic. Good discipline.

### What concerns me

**1. `gaussian_glow()` has a dead alpha calculation.** Lines 113–115 compute `a` twice — an initial complex formula is immediately overwritten by a simpler quadratic. This is not a crash risk, but it is code noise that signals rushed implementation. In a shared library, confusion here means the next person who reads this function and tries to modify the falloff curve will not understand what the intended behavior actually is. This must be cleaned up before the library is treated as stable.

**2. `perlin_noise_texture()` pixel-by-pixel loop is a performance hazard.** A 1920×1080 call at scale=50, octaves=3 is roughly 2 million point-draw calls. This will take tens of seconds, possibly over a minute on a modest machine. In a batch pipeline where multiple generators call this function, that compounds. The function works but has not been stress-tested at production canvas sizes. Any generator that calls it on a full 1920×1080 canvas without a smaller tile-and-repeat strategy will pay for it. There should be a performance warning in the docstring or an explicit `max_size` recommendation.

**3. No version constant.** The library has no `__version__` string or equivalent. As the library evolves (and it will), generators that depend on a specific function signature or behavior have no way to assert compatibility. For a production pipeline with five active team members, this will cause silent breakage as the library grows.

**4. Non-technical artist usability is mixed.** The import boilerplate (`sys.path.insert`, `os.path.dirname(__file__)`) is not something an artist should need to write. It is fine for Kai, but it is a barrier for Maya or Lee importing this into a new generator. A one-line convenience import wrapper or a proper `__init__.py` making this a package would make the library genuinely accessible to non-technical team members.

**5. `vignette()` has a subtle bug.** The inner ellipses use `fill=(0, 0, 0, 0)` (transparent) plus an outline. That means each ring is a hollow ellipse outline, not a filled gradient ring. The result works visually because overlapping outlines approximate a soft edge — but it is not the radial gradient the docstring describes. It is a Mach band approximation. For CRT-style content this may be acceptable, but it should be documented as intentional, not left as an apparent implementation gap.

---

## Priority 2 — Tool Naming and Organization

**Grade: B–**

### What works

The README is indexed and covers all major tools. The "Misplaced Files" table is a genuinely useful acknowledgment — the team is tracking its own debt. The open-source policy table is clear. Registration instructions are present and specific.

### What concerns me

**1. `ltg_render_lib.py` is not LTG-compliant.** Every other tool in the index follows `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`. The shared library is named `ltg_render_lib.py` — lowercase, no category code, no version number. This breaks the naming convention for the single most important new tool added in Cycle 21. The correct name would be `LTG_TOOL_render_lib.py`. This is not a cosmetic issue: batch scripts, auto-scanners, and future compliance tools will miss this file. Fix it, and update all import references in tech_den_v003 and glitchlayer_frame_v003.

**2. `LTG_CHAR_luma_expression_sheet.py` naming violation is still unresolved.** The README flags it as MISNAMED (CHAR category, should be TOOL) and says "Flag to Alex Chen for rename." That flag was raised in Cycle 12. It is now Cycle 21. An unresolved naming violation sitting in the README for nine cycles is not tracked debt — it is neglected debt. If the team cannot act on its own flagged items, the README becomes a warning graveyard rather than an index.

**3. Legacy files lack a clear sunset plan.** There are nine legacy-named scripts (`color_swatch_generator.py`, `character_lineup_generator.py`, `contact_sheet_generator.py`, `logo_generator.py`, `panel_chaos_generator.py`, `panel_interior_generator.py`, `storyboard_pitch_export_generator.py`, `style_frame_01_rendered.py`, `style_frame_generator.py`) sitting in the index as "legacy filename." No deprecation date, no flag indicating whether these are still executable or purely archived. A new team member looking at this README cannot determine which scripts are live versus fossil. At minimum each legacy entry needs: (a) a canonical replacement named, (b) a note confirming the legacy file is NOT run-safe (or that it is).

**4. The README table has a formatting break.** There is a blank row between `LTG_TOOL_logo_asymmetric.py` and `LTG_TOOL_style_frame_02_glitch_storm.py` entries, and then a second table section for Cycles 19–21 entries appears without a section header. This is a presentation failure. The README is meant to function as a working index for a pitch package — if the index itself is visually inconsistent, that reflects on the production.

**5. `bg_glitch_layer_encounter.py` in environments/ has been flagged for relocation since the README was updated — still not moved.** This is the same pattern as #2. The team documents what needs to be fixed but does not fix it.

---

## Priority 3 — Design Consistency Across Character Sheets

**Grade: B**

### What works

Both generators use the same 1200×900 canvas, 3×2 grid layout (COLS=3, ROWS=2), PAD=20, HEADER=58, LABEL_H=36 — the spatial scaffolding is identical. Both use RENDER_SCALE=2 for supersampled 2x rendering then downsample. Both use DejaVuSans fonts with the same size hierarchy (26/17/13pt). Both output PNG to `output/characters/main/`. Both apply the 3-tier line weight directive. Both use the same `bezier3()`, `polyline()`, and `arc_draw()` helper geometry. These sheets will sit coherently on the same page in a pitch deck.

The body-language-first approach — the key critique response from Cycle 19 — is implemented in both. Luma uses hair variants plus arm positions; Miri uses full-body postures with arms explicitly specified per expression. Both pass the squint test at the design intent level.

### What concerns me

**1. Head unit sizes are not the same, and the difference is not documented.** Luma's `HEAD_R = 105` (rendering to `HR = 210`). Miri's `HEAD_R = 68` (rendering to `HR = 136`). On the same 1200×900 canvas, Luma's head occupies significantly more panel area than Miri's. This is intentional — Miri is a full-body sheet while Luma is bust-format — but it is nowhere documented as a design decision. A reader of the code, or a future artist adding a new character sheet, does not know whether the different HEAD_R values are character-specific calibration or an inconsistency. The difference should be named explicitly: `HEAD_R_BUST = 105` vs `HEAD_R_FULL_BODY = 68`, or at minimum a comment explaining the bust-vs-full-body format distinction.

**2. Label content conventions differ.** Luma's expression labels use single-word uppercase labels (`CURIOUS`, `DETERMINED`). Miri's use slash-separated extended labels (`WARM / WELCOMING`, `SKEPTICAL / AMUSED`). Both approaches are defensible — Luma's are clean identifiers, Miri's are more descriptive. But in a pitch deck they will look inconsistent side by side. A production standard should be chosen and applied uniformly across all four character sheets.

**3. Background color logic differs.** Luma's panel BGs are keyed directly in the `BG` dict by expression name. Miri's use the same pattern. This is consistent. However, Luma's label backgrounds are computed dynamically (`tuple(max(0, int(c * 0.88)) for c in bg)`) while Miri's... I could not verify Miri's label approach in the truncated read. This is flagged for team verification — if the label background computation differs, sheets will have visually different label bars at the bottom of each panel.

**4. Construction guides are present in Luma's sheet but Miri's does not appear to have them.** Luma calls `draw_construction_guide()` which draws the head circle + crosshairs as a ghosted overlay. This is a production reference tool — useful for animators checking proportions. If Miri's sheet lacks construction guides, the sheets serve different levels of production utility. All character sheets should carry the same reference information. Check and confirm.

**5. The sheets use the same canvas size but Miri has 5 expressions (leaving one panel empty) versus Luma's 6 (filling the grid).** The empty sixth panel in Miri's sheet is a layout issue. In a 3×2 grid, 5 panels leaves a blank cell in the lower right. This is not inherently wrong — a sixth Miri expression may come — but it should either be filled with a placeholder/note or the layout should switch to a 5-panel format. In a pitch deck, a blank cell reads as "unfinished."

---

## Summary Grades

| Area | Grade | Key Issue |
|---|---|---|
| ltg_render_lib.py API design | B+ | Dead alpha calc; perf risk; no version; non-compliant filename |
| Tool naming and organization | B– | Library itself is not LTG-compliant; nine-cycle unresolved debt |
| Character sheet consistency | B | Head unit sizes undocumented; label format mismatch; blank grid cell |

---

## Top 3 Priority Fixes

**1. Rename `ltg_render_lib.py` to `LTG_TOOL_render_lib.py` and add `__version__ = "1.0.0"`.** This is the most urgent fix because it is the shared dependency that all future generators will import. A non-compliant filename on the foundation of the technical pipeline is not acceptable. Update all import references in tech_den_v003 and glitchlayer_frame_v003. Register the corrected name in the README.

**2. Resolve all flagged items in the README that have been open for more than 2 cycles.** Specifically: rename `LTG_CHAR_luma_expression_sheet.py` to `LTG_TOOL_luma_expression_sheet.py`, and relocate `bg_glitch_layer_encounter.py` from environments/ to tools/. The README must function as a live, accurate index — not a historical record of deferred intentions. If items remain unresolved after two cycles, they should be escalated to Alex Chen as blockers, not re-flagged as notes.

**3. Standardize character sheet label conventions and document the HEAD_R format decision.** Before Cycle 22 adds any more character sheets, establish: (a) whether expression labels are single-word or slash-extended, (b) what HEAD_R value maps to which format (bust vs full-body), and write both decisions into the character sheet template or the production bible. Four characters with four individually-calibrated but undocumented parameter choices is not a production system — it is four separate one-offs that happen to look similar.

---

— Fiona O'Sullivan, Production Design Critic
