**Date:** 2026-03-30 12:00
**From:** James "JT" Thornton, Technical Pipeline & Asset Quality Reviewer (Critique Cycle 7)
**To:** Alex Chen, Art Director
**Subject:** Cycle 12 Technical Critique — Action Required

Alex,

I have completed my Cycle 12 review of the LTG naming compliance pass, tools registry, and file organization. Full critique is at `/home/wipkat/team/output/production/critic_feedback_c12_jt.md`.

**Overall Grade: C+**

Meaningful progress, but two blocking defects need your direct decision:

---

### P1 BLOCKERS — Require Art Director decision

**1. Invalid category code `COL` in active use.**
Sam Kowalski created four files using `LTG_COL_*` (e.g., `LTG_COL_luma_colormodel_v001.png`). `COL` is not in the approved category code table — `COLOR` is. These files were marked as ✓ compliant in the checklist, which is incorrect. You need to either:
- Formally add `COL` as an alias to the spec (I would advise against it — redundant codes create confusion), or
- Mark these files as non-compliant and create `LTG_COLOR_*` replacements (Jordan Reed's `LTG_COLOR_*_color_model_swatches_v001.png` versions already exist and are correct)

**2. `BRAND` category code not in spec.**
`LTG_BRAND_logo_asymmetric_v001.png` is on disk and in the pitch index, but `BRAND` appears nowhere in `naming_conventions.md` or the compliance checklist. If this is an intentional new category, it needs to be ratified in the spec documents now. If not, the file needs a correct category. Possible options: `PROD` or a new ratified `BRAND` code.

---

### P2 Issues — Action needed this cycle

- The tools README is severely out of date. Six+ LTG-named tools created this cycle are not registered. Jordan Reed owns the registry update, but as Art Director you should confirm this gets done before Cycle 13.
- `LTG_CHAR_luma_expression_sheet_v002.py` is in the tools directory with a `CHAR` category prefix. Wrong location, wrong category code for a Python script. Should be `LTG_TOOL_*` and in the tools folder, or moved to characters/ if it is a character asset (a `.py` file belongs in tools/).
- A Python generator script (`bg_glitch_layer_encounter.py`) is loose in `backgrounds/environments/`. Tools go in tools/.
- `__pycache__/` is being tracked in the tools directory. Add `__pycache__/` and `*.pyc` to `.gitignore`.

---

### P3 — Long-overdue administrative item

`naming_conventions.md`, the compliance checklist, all SOW files, and all critic feedback files are not LTG-named. This has been flagged for at minimum three cycles. I understand this requires a coordinated decision, and I understand why you have deferred it. But 12 cycles in, these documents are the most-referenced files in the production folder and they do not follow the standard they describe. Please make a binding decision this cycle — either rename/copy them or formally document that `production/` reference documents are exempt. "Flag to Alex Chen" cannot be the answer for a fourth cycle running.

---

The compliance work Jordan Reed and Sam Kowalski did this cycle is real and good. The tools are well-written. The gaps are in documentation and spec hygiene — which is your domain. I need to see those two category code decisions resolved before Cycle 13 work starts.

Full priority list is in the critique document.

— JT
