# Statement of Work — Cycle 29

**Date:** 2026-03-29
**Work cycles completed:** 29
**Critique cycles completed:** 12
**Next critique:** Cycle 13 (after Cycle 30)

---

## Deliverables

### Maya Santos — Character Designer
- **LTG_CHAR_luma_expressions_v007.png** (1200×900) — Luma expression sheet rebuilt to 3.2-head canon: torso_h = HR×2.10, pants_h = HR×1.68, eye width = h×0.22. Closes C28 P1 proportion/eye-spec blocker.
- **LTG_CHAR_luma_lineup_v006.png** (1280×508) — Lineup rebuilt with LUMA_HEADS = 3.2, HEAD_UNIT = 87.5px, eye width h×0.22. All other characters unchanged from v005.
- Generators: LTG_TOOL_luma_expression_sheet_v007.py, LTG_TOOL_character_lineup_v006.py

### Sam Kowalski — Color & Style Artist
- No new outputs required. Color story and SF02 spec doc already reflected C28 fixes (GL-06c, UV_PURPLE_DARK, YEARNING/COVETOUS/HOLLOW).

### Kai Nakamura — Technical Art Engineer
- **LTG_TOOL_naming_cleanup_v001.py** — cleanup script with dry-run mode; executed by producer, removing 22 legacy LTG_CHAR_/LTG_COLOR_/LTG_BRAND_ source files.
- **output/tools/README.md** updated: C29 legacy archive section, cleanup tool registered, header updated.
- character_sheet_standards_v001.md line weight table verified correct (head=4, structure=3, detail=2 at 2×).

### Rin Yamamoto — Procedural Art Engineer
- **LTG_COLOR_styleframe_discovery_v004.png** (1280×720) — SF01 procedural quality pass: wobble polygon (Luma head, CRT frame, couch), variable stroke, add_face_lighting() (warm lamp upper-left), add_rim_light(side="right") (cool CRT teal). Blush corrected to peach (232,168,124). Canvas rescaled 1920→1280px.
- Generator: LTG_TOOL_styleframe_discovery_v004.py

### Alex Chen — Art Director
- **pitch_audit_cycle29.md** updated: C29 in-progress status noted, C30 risk profile raised.
- C30 directives issued to team.

---

## Policy Changes (Producer)
- **Image Handling policy** extended from critics-only to all agents. Rules now in CLAUDE.md `## Image Handling` section (applies to team members and critics).
- **Critique format** changed: critics now use compact format — Score (0–100), bullet issues (≤2 lines each), one Bottom line sentence. Total ≤ 15 lines per asset.
- **CRITIC_WORKFLOW.md** retired — all content consolidated into CLAUDE.md. All 15 critic bios updated to reference CLAUDE.md.
- **22 legacy naming-violation files** deleted from output/tools/ (LTG_CHAR_*/LTG_COLOR_*/LTG_BRAND_* — canonical LTG_TOOL_* versions already on disk).

---

## Pitch Package Status — End of Cycle 29

### Style Frames
| Asset | Version | Status |
|-------|---------|--------|
| SF01 Discovery | v004 NEW | Procedural pass complete |
| SF02 Glitch Storm | v005 | Current |
| SF03 Other Side | v005 | Current |
| SF04 Luma+Byte | v003 | Current |

### Characters
| Asset | Version | Notes |
|-------|---------|-------|
| Luma expressions | v007 NEW | 3.2 heads + h×0.22 eyes — P1 blocker CLOSED |
| Luma turnaround | v003 | Current |
| Luma color model | v001 | Current |
| Byte expressions | v004 | Current |
| Byte turnaround | v001 | Current |
| Byte color model | v001 | Current |
| Cosmo expressions | v004 | Current |
| Cosmo turnaround | v002 | Current |
| Cosmo color model | v001 | Current |
| Miri expressions | v003 | Current |
| Miri turnaround | v001 | Current |
| Glitch expressions | v003 | Current |
| Glitch turnaround | v002 | Current |
| Glitch color model | v001 | Current |
| Character lineup | v006 NEW | 3.2 heads — P1 blocker CLOSED |

### C30 Directives (from Alex Chen)
- Rin: SF01 v004 still needs Luma proportions verified at 3.2 heads / h×0.22 eyes in the frame
- Kai: drawing order audit across active generators; any remaining naming/README gaps
- All: prepare for Critique 13 — weakest remaining asset is SF01 (procedural but proportions unverified in scene context)
