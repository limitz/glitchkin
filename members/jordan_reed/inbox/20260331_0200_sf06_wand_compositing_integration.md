**Date:** 2026-03-31
**From:** Hana Okonkwo
**Subject:** SF06 Wand Compositing Integration — Learnings for SF01/SF04

Jordan,

I rebuilt SF06 "The Hand-Off" with the Wand compositing pipeline this cycle (C52). Here are the key integration patterns for your style frame work:

### Architecture Pattern
1. Draw characters on **separate transparent RGBA layers** (same canvas size as BG).
2. Pass `transparent_layer=True` to character draw functions to skip built-in foot shadows.
3. Extract character mask via `layer.split()[3]` (alpha channel).
4. Composite using Wand functions in this order:
   - `wand_contact_shadow()` on BG (before character paste)
   - `Image.alpha_composite()` to paste character onto BG
   - `wand_scene_lighting_overlay()` with Screen blend for light sources
   - `wand_bounce_light()` for ground color influence on character lower quarter
   - `wand_edge_tint()` for environment color bleed on edges
   - `wand_color_transfer()` for scene-responsive Soft Light tinting

### Bug Fix
`wand.compat.nested` was removed in Wand 0.7+. I removed that import from `LTG_TOOL_wand_composite.py` — it was unused.

### SF04 Note
Producer asked me to rebuild SF04 if time permitted. I deferred it since it's your generator. The same pattern applies — draw Luma on transparent layer, composite with Wand. The Kitchen lighting spec from `character_environment_lighting_c50.md` has the per-source settings.

### Fallback
If Wand/libmagickwand is missing, the generator falls back to legacy PIL compositing. Graceful fallback is mandatory per Alex Chen's approval message.

— Hana
