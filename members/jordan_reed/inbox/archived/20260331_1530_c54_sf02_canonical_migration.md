**Date:** 2026-03-31 15:30
**From:** Producer
**To:** Jordan Reed

## C54 Task — SF02 Canonical Character Migration

Human flagged: "SF02 running characters are not canonical."

Your C53 memory already notes this: "Luma/Cosmo/Byte still use old PIL rendering (composited onto img directly)."

**Task:** Migrate all characters in SF02 (Luma, Cosmo, Byte) to the canonical char_*.py renderers.

- Luma: `LTG_TOOL_char_luma.py` → `draw_luma()`
- Cosmo: `LTG_TOOL_char_cosmo.py` → `draw_cosmo()`
- Byte: `LTG_TOOL_char_byte.py` → `draw_byte()`

All three are in the canonical modular registry. Use `draw_X_on_context()` or render to RGBA surface and composite, whichever fits your Wand pipeline.

The characters should match the canonical designs — running/dynamic expressions as appropriate for the Glitch Storm scene.

File: `output/color/style_frames/LTG_TOOL_style_frame_02_glitch_storm.py`
Output: `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm.png`

Run precritique_qa after regeneration. Check color_verify passes.

Update your MEMORY.md when done. Send results to members/producer/inbox/.
