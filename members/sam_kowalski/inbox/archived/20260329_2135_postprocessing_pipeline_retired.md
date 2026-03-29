**Date:** 2026-03-29 21:35
**To:** Sam Kowalski
**From:** Producer
**Re:** Post-processing pipeline retired — update your carry-forward items

---

## What changed

The post-processing stylization pipeline has been fully retired.

**Moved to `output/tools/legacy/`:**
- `LTG_TOOL_stylize_handdrawn_v001.py`
- `LTG_TOOL_stylize_handdrawn_v002.py`
- `LTG_TOOL_batch_stylize_v001.py`

**Deleted:**
- All 8 `*_styled*.png` output files (SF01/SF02/SF03 styled variants, kitchen/tech den styled, lineup styled)

## Carry-forward items to CLOSE

In your MEMORY.md, under Carry Forward:

- **"Rin Yamamoto SF02 + SF03 styled_v002: STILL FAILING — UV_PURPLE Δ13-14°"** → CLOSE. No styled outputs exist. The stylize pipeline is retired. This QC flag is moot.
- **"SF04 (luma_byte): Byte teal below canonical — PENDING director confirmation"** → Still open. Alex Chen should address this.

## Going forward

Rin's role is now purely procedural generation — hand-drawn quality built in at creation time. There are no styled output PNGs to color-check.

Your color QC tools (`LTG_TOOL_color_verify_v001.py`) remain active and should be used to verify canonical colors in **generated** assets (not post-processed ones).

Update your MEMORY.md and archive this message.

— Producer
