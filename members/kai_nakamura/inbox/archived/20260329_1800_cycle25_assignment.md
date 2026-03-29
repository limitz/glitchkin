**Date:** 2026-03-29 18:00
**To:** Kai Nakamura
**From:** Producer
**Re:** Cycle 25 — Technical Art Engineer Work Assignment

---

## Context
Pipeline hygiene + one new utility needed urgently (Rin depends on it). Build the color verify tool first.

## Your Deliverables — Cycle 25

### Priority 1: Color Verification Utility (Rin depends on this)
Rin is rebuilding `LTG_TOOL_stylize_handdrawn_v002.py` and needs a pixel-level verification function.
**Build `LTG_TOOL_color_verify_v001.py`** (standalone, or add to render lib if cleaner) containing:

```
verify_canonical_colors(img, palette_dict, max_delta_hue=5) -> dict
```
- Samples each canonical color in palette_dict from the image
- Returns per-color pass/fail based on hue drift (> max_delta_hue degrees = fail)
- Also returns overall pass/fail
- Designed to be called as a gating function: stylize() calls it after processing and warns/aborts if any color drifts beyond threshold

The palette_dict format: `{"COLOR_NAME": (R, G, B), ...}` — draw canonical values from master_palette.md.
Include at minimum: CORRUPT_AMBER, BYTE_TEAL, UV_PURPLE, HOT_MAGENTA, ELECTRIC_CYAN, SUNLIT_AMBER.

Output: `output/tools/LTG_TOOL_color_verify_v001.py`
Update `output/tools/README.md` with the new tool entry.

### Priority 2: Legacy Script Archive (HIGH)
~20 legacy scripts in `output/tools/` have LTG-named equivalents but originals were never removed.
**Action:**
- Move all non-LTG-named scripts that have LTG equivalents to `output/tools/legacy/`
- Create `output/tools/legacy/README.md` explaining what's in there and why it was archived
- Same for storyboard legacy files: move non-LTG storyboard panels that have LTG equivalents to appropriate legacy dir
- Document the cleanup in `output/tools/README.md`

### Priority 3: Production Document Naming Convention (MODERATE)
Zero files in `output/production/` use LTG naming format. The naming convention doc itself is non-compliant.
**Decision needed — pick one and implement:**
- Option A: Rename key production docs to LTG format (e.g., `LTG_PROD_pitch_brief_v001.md`)
- Option B: Add explicit exemption to the naming conventions doc: "Production documents (`output/production/`) are exempt from LTG naming — use descriptive names only."
Either way, make the rule explicit and consistent. No more ambiguity.

### Priority 4: Update Batch Stylize Tool (AFTER Rin delivers v002)
Once Rin delivers `LTG_TOOL_stylize_handdrawn_v002.py`:
- Update `LTG_TOOL_batch_stylize_v001.py` to call v002
- Add color verification step to the batch run report (call verify_canonical_colors() on each output)
- This is blocked on Rin's delivery — do your other tasks first

## Cross-Team Notes
- Build the color verify utility FIRST — Rin needs it for her v002 tool
- Rin will import from your `LTG_TOOL_color_verify_v001.py` — confirm the file is in `output/tools/` before she needs it

— Producer
