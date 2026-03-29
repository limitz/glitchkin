# Statement of Work — Cycle 32

**Date:** 2026-03-29
**Work cycles completed:** 32
**Critique cycles completed:** 13
**Next critique:** Critique 14 (after Cycle 34)

---

## Deliverables

### Alex Chen — Art Director
- **Eye-width canonical definition decided:** `ew = int(head_r * 0.22)` where `head_r` = head-RADIUS. Resolves 3.8× discrepancy found by Daisuke in C13. Variable name rule: avoid `h`, always use `head_r`.
- **luma.md fixed:** 3.5 heads → 3.2 heads; all canonical proportion values documented; segment measurements updated.
- **character_sheet_standards_v001.md:** new Section 2 with full eye-width definition, lookup table, variable naming rule.
- Eye-width spec circulated to Maya and Rin via inbox.
- SF04 Byte teal formally accepted as scene-lighting intent (`SCENE-LIGHTING — ACCEPTED`).
- Ideabox: `glitch_construction_linter.md` — tool to lint new Glitchkin generators against glitch.md spec.

### Maya Santos — Character Designer
- **LTG_CHAR_luma_expressions_v008.png** (1200×900) — new anchor expression "THE NOTICING": chin-touch gesture, asymmetric eyes (left more open), gaze directed left+down, zero body tilt. Visually distinct at silhouette level. Layout expanded to 3×3 (7 filled).
- **output/characters/main/glitch.md** — full 11-section Glitch diamond construction spec: geometry from primitives, vertex formulas, fill/crack recipe, spike system, rotation/squash/stretch rules, 8-state pixel eye system, bilateral eye rule, destabilized-right-eye signature, panel grouping logic, 4-view turnaround rules, step-by-step reproduction guide.
- Ideabox: `expression_silhouette_test.md` — automated silhouette-differentiation QA tool for expression sheets.

### Sam Kowalski — Color & Style Artist
- **master_palette.md:** CHAR-L-11 cross-reference corrected (#00D4E8 → #00F0FF). CHAR-M-11 Miri slippers changed to warm #C4907A (Dusty Warm Apricot). DRW-18 warmth clarified as functionally imperceptible at 7% lightness.
- **ltg_style_frame_color_story.md:** SF03 Key Color Tension corrected — dark hair removed from warm values list.
- Color verify v002 --histogram spot-check: 0 new regressions.
- Ideabox: `miri_slipper_warmth_audit.md` — warm-channel-ratio lint check for CHAR-M entries.

### Rin Yamamoto — Procedural Art Engineer
- **LTG_TOOL_procedural_draw_v001.py → v1.3.0:** `add_rim_light()` gains optional `char_cx` parameter; `side="right"` uses `x > char_cx` (character-relative) when provided, canvas center otherwise.
- **LTG_TOOL_styleframe_discovery_v005.py + LTG_COLOR_styleframe_discovery_v005.png** (1280×720) — SF01 v005: rim light passes `char_cx=head_cx`, Luma's full right silhouette now correctly lit.
- **LTG_TOOL_styleframe_luma_byte_v004.py + LTG_COLOR_styleframe_luma_byte_v004.png** (1280×720) — SF04 rebuilt from scratch: value ceiling 255 (was 198/FAIL), Byte monitor contribution on CRT-facing flank, canonical Byte Teal GL-01b, Luma blush #E8A87C, char_cx rim lights per character.
- **LTG_CHAR_luma_turnaround_v004.png** — all three views corrected to `ew = int(head_r * 0.22)` (was `ew = int(head_height * 0.22)` — 2× too wide).
- Ideabox: `char_cx_helper_tool.md` — `get_char_bbox()` utility to auto-detect character center x from silhouette.

### Kai Nakamura — Technical Art Engineer
- **8 broken forwarding stubs fixed** — stubs that imported from deleted LTG_CHAR_* files updated to delegate to canonical LTG_TOOL_* replacements (or preservation stubs for SF04 v001–v003).
- **Cosmo v004 generator fixed** — now outputs `LTG_CHAR_cosmo_expression_sheet_v004.png`; SURPRISED expression adds blush (two nested ellipses per cheek).
- **W004 investigation:** most of 55 linter warnings are false positives (docstring text, helper-function local draw objects, in-place paste). One confirmed real fix applied. Linter scope-awareness flagged as ideabox item.
- Ideabox: `stub_linter_tool.md` — stub integrity linter to prevent future cleanup-breakage.

---

## Process Improvement (Producer)
- **Agent prompt duplication eliminated:** agent prompts must not repeat inbox content. Prompts = role context + startup sequence only. Task detail belongs in inbox messages exclusively.

---

## Pitch Package Status — End of Cycle 32

| Asset | Version | Notes |
|-------|---------|-------|
| SF01 Discovery | v005 | char_cx rim light fix |
| SF02 Glitch Storm | v005 | Current |
| SF03 Other Side | v005 | Current |
| SF04 Luma+Byte | v004 NEW | Full rebuild — value ceiling 255, monitor contribution |
| Luma expressions | v008 NEW | THE NOTICING anchor expression |
| Luma turnaround | v004 NEW | Canonical eye-width (head_r×0.22) |
| Luma color model | v002 | Current |
| Character lineup | v006 | Current |
| Glitch spec | glitch.md NEW | Full 11-section construction spec |
