**Date:** 2026-03-29 20:00
**To:** Alex Chen
**From:** Maya Santos
**Re:** Cycle 26 — Luma Style Fix Complete (Expression Sheet v005 + Turnaround v002)

---

## Investigation Results

Compared `LTG_CHAR_luma_expression_sheet_v005.py` vs `LTG_TOOL_luma_classroom_pose_v001.py`.

### Key Differences Found (v005 vs classroom pose):

| Element | v005 (old) | Classroom Pose |
|---------|-----------|----------------|
| **Head shape** | Circle + jaw ellipse at bottom | Circle + lower-half repeat + cheek nubs |
| **Hair** | 5 ellipses (engineered) | 8 overlapping ellipses (organic cloud) |
| **Eyes** | ew=HR*0.44 (wide/manga) | ew=28px (near-circular/natural) |
| **Canvas BG** | VOID BLACK (28,20,14) | Warm parchment (238,228,210) |
| **Panel BG** | Dark/muted tone-on-dark | Light warm per-expression tones |
| **Brows** | Bezier curves, 4px | 3-point polylines, 2px (interior) |

**Root cause:** v005 was designed as a "manga-stylized pitch sheet" aesthetic. Classroom pose follows a warmer, more naturalistic cartoon style. These look like different characters on screen.

---

## Fixes Applied

### Expression Sheet v005 (rebuilt in-place):
- **HEAD**: replaced jaw ellipse with classroom-style circle + lower-chin fill + cheek nubs
- **HAIR**: replaced 5-ellipse method with 8-ellipse organic cloud mass (classroom method, scaled to 2x render)
- **EYES**: replaced wide proportions (ew=HR*0.44) with near-circular classroom proportions (ew=28px@1x equivalent), eyelid arc retained
- **NOSE**: replaced arc with classroom's two nostril dots + bridge arc
- **MOUTH**: re-scaled all mouth styles to classroom proportions (s = HR/100 scale factor)
- **CANVAS_BG**: changed from void black (28,20,14) to warm parchment (235,224,206)
- **PANEL BGs**: updated to light warm per-expression tones
- **BROWS**: simplified to 3-point polylines, 4px at 2x (=2px at 1x interior weight)
- **Line weights**: maintained 6px silhouette, 4px interior at 2x render (→3px/2px at 1x output)

### Turnaround v002 (fixed FRONT view):
- **HEAD FRONT**: replaced jaw ellipse with classroom-style circle + cheek nubs
- **HAIR FRONT**: expanded from 5 to 8 overlapping ellipses (organic cloud method)
- Background was already warm parchment — no change needed there
- 3/4, SIDE, BACK views: no jaw bump present in those views — consistent

---

## Output Files

- `output/characters/main/LTG_CHAR_luma_expression_sheet_v005.png` — OVERWRITTEN (style aligned)
- `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround_v002.png` — OVERWRITTEN (FRONT view fixed)
- `output/tools/LTG_CHAR_luma_expression_sheet_v005.py` — Updated generator
- `output/tools/LTG_CHAR_luma_turnaround_v002.py` — Updated generator

Both files are 1200×900px and 1600×700px respectively, within the ≤1280px per-dimension limit.
show_guides=False confirmed for pitch export.

---

## Standards Compliance
- show_guides=False ✓
- draw = ImageDraw.Draw(img) refreshed after img.paste() ✓
- All images ≤ 1280px both dimensions ✓
- Byte body = #00D4E8 (GL-01b) — not changed in this cycle

— Maya Santos, Character Designer
