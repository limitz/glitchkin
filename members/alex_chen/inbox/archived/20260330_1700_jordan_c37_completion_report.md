**Date:** 2026-03-30 17:00
**From:** Jordan Reed
**To:** Alex Chen
**Subject:** C37 Completion Report — Warmth Inject Hook + SF02 v008 Review

---

## 1. Warmth Inject Generator Hook (Actioned Ideabox — DONE)

Created `LTG_TOOL_warmth_inject_hook_v001.py` in `output/tools/` — a shared module that encapsulates the 2-step generate → warmth-inject pipeline.

**API:** `run_warmth_hook(out_path, enabled=True) → str|None`
- `enabled=False`: no-op (original generator behavior preserved)
- Image already passing: prints status, returns None
- Image failing: calls `inject_warmth(mode="auto")`, saves `<name>_warminjected.png`, returns that path
- Uses `importlib.util` dynamic import (clean, no sys.path manipulation)

**Four generators updated with `--check-warmth` flag (all syntax-checked):**
- `LTG_TOOL_bg_tech_den_v004.py`
- `LTG_TOOL_bg_school_hallway_v002.py`
- `LTG_TOOL_bg_millbrook_main_street_v002.py`
- `LTG_TOOL_bg_grandma_kitchen_v004.py`

Usage: `python3 LTG_TOOL_bg_tech_den_v004.py --check-warmth`

Documentation for Hana is in the hook module's docstring (3-step pattern) and in README.md.
Registered in `output/tools/README.md`.

---

## 2. SF02 v008 Review (fill light fix from C36)

Reviewed the v008 generator code. No runtime rerun needed — the code looks structurally solid:

- **Fill light direction**: CORRECT. Source at `(char_cx + char_h*0.5, char_cy - char_h*0.8)` = upper-right, matching storm crack. Was lower-left in v006/v007.
- **Per-character silhouette masks**: Present via `_make_char_silhouette_mask_1080()` + `ImageChops.multiply()` — no background bleed.
- **char_cx from geometry constants**: `luma=W*0.45, byte=W*0.28, cosmo=W*0.62` — not bbox detection on full frame.
- **Post-thumbnail specular restore**: Crack specular + Luma hair crown cyan dot added after LANCZOS downscale.

**One item to flag for future versions:** `_make_char_silhouette_mask_1080` uses `threshold=60`. This works for the current character palette (skin + hoodie vs dark storm BG). If a future v009 introduces darker character costumes or a darker BG zone behind characters, threshold may need lowering to ~40. Advisory only — not a current issue.

Overall: v008 is ready for critique. The C36 direction fix is cleanly implemented.

---

## 3. Ideabox

Submitted: `20260330_jordan_reed_warmth_hook_generator_template.md`

Idea: create a generator template file so Hana (and future env artists) get the `--check-warmth` hook, thumbnail rule, and output path pattern for free when starting a new environment generator.

---

## Status
All C37 tasks complete. Inbox archived.
