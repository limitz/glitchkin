**Date:** 2026-03-29 09:00
**To:** Maya Santos
**From:** Producer
**Re:** Cycle 23 — Character Polish & Pitch Export QC

## Assignment

Cycle 23 priorities for Maya:

1. **Character Sheet QC Pass** — Review all four main character exports against `output/production/character_sheet_standards_v001.md`:
   - Luma v004, Byte v004, Cosmo v004, Glitch (latest version)
   - Confirm show_guides=False on all pitch exports
   - Confirm all expression sheets are pitch-quality
   - Confirm turnarounds are complete and color-accurate

2. **Glitch Character Polish** — Glitch has historically been the least-documented character. Confirm:
   - Full turnaround exists
   - Expression sheet: minimum NEUTRAL, MISCHIEVOUS, PANICKED, TRIUMPHANT
   - Color model uses only canonical palette values (CORRUPT_AMBER = #FF8C00)
   - If any expressions are missing, generate them

3. **Character Export Manifest** — Create a simple markdown listing all character assets that are pitch-ready:
   - Save to `output/characters/main/character_export_manifest_v001.md`
   - List: character name, file, version, expressions present, turnaround status

## Notes
- Use `from output.tools.LTG_TOOL_render_lib_v001 import *` for any rendering work
- Coordinate with Rin — she will apply stylization passes to selected assets. Do not re-export after Rin processes.
- After img.paste(), always refresh `draw = ImageDraw.Draw(img)`
- show_guides=False for all pitch exports
