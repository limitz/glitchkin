# Naming Convention Compliance Report — Jordan Reed

**Date:** 2026-03-29 21:00
**From:** Jordan Reed, Background & Environment Artist
**To:** Alex Chen, Art Director
**Re:** Cycle 9 Naming Convention Review

---

## Summary

Per Cycle 9 Task 2, I reviewed `/home/wipkat/team/output/production/naming_conventions.md` and assessed compliance for my background outputs.

---

## Files Reviewed

| Original Filename | Convention Status | Action Taken |
|---|---|---|
| `frame01_house_interior.png` | Non-compliant — no `LTG_ENV_` prefix, no version number | Created compliant copy: `LTG_ENV_lumashome_study_interior_v001.png` |
| `glitch_layer_frame.png` | Non-compliant — no `LTG_ENV_` prefix, no version number | Created compliant copy: `LTG_ENV_glitchlayer_frame_v001.png` |
| `bg_glitch_layer_frame.py` (new tool) | Non-compliant — no `LTG_TOOL_` prefix, no version number | Created compliant copy: `LTG_TOOL_bg_glitch_layer_frame_v001.py` |

Original files have been retained per the "never overwrite" policy. Compliant-named copies exist alongside them.

---

## Notes on the Reconciliation Schedule

The naming_conventions.md states that existing assets with retired prefixes (`LH_INT_`, `GL_`) should not be renamed in isolation — they should wait for the v3.0 environment document reconciliation pass.

The files above do not use retired prefixes — they simply pre-date the naming convention. I have created convention-compliant copies rather than renaming in-place, to avoid version-tracking confusion. **Awaiting Art Director guidance on whether the originals should be deprecated or deleted.**

---

## Naming Convention Gaps Observed

The naming_conventions.md is clear and complete for asset files. However, I note:

1. **Existing older tool scripts** (`bg_layout_generator.py`, `bg_house_interior_frame01.py`, `color_key_generator.py`, etc.) all use non-standard names. These predate the convention. The tools README (`/home/wipkat/team/output/tools/README.md`) references them by old names. Recommend the v3.0 reconciliation pass cover tools as well as environment assets.

2. **The tools README itself** does not follow `LTG_PROD_` naming — though as an index document it is arguably production documentation. Low priority but worth noting.

---

Jordan Reed
Background & Environment Artist
Cycle 9
