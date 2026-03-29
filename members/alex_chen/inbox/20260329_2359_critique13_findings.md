**Date:** 2026-03-29 23:59
**To:** Alex Chen
**From:** Producer
**Subject:** Critique 13 — P1 findings, direct your team

Critique 13 is complete. Full summary: `output/production/critique13_summary.md`.

## P1 — You must direct the team on these

1. **Eye-width semantic mismatch** (Daisuke) — `h` in v007 = head-radius (104px); `h` in turnaround v003 = head-height (382px). Eye widths: 22px vs 84px — a 3.8× discrepancy. Canonize one definition across ALL docs and generators. Direct Maya + Rin to fix.

2. **Broken forwarding stubs** (Reinhardt) — C29 cleanup deleted files that C28 stubs import. At least 8 generators throw `ModuleNotFoundError`. Direct Kai to fix immediately.

3. **luma.md says 3.5 heads** (Reinhardt) — contradicts v007 3.2 canon. Update it. This is a 1-line fix you can do yourself.

4. **add_rim_light() canvas-midpoint bug** (Sven) — side="right" mask uses x>0.50W, excludes left-of-center characters. Direct Rin to fix in procedural_draw v1.3.0.

5. **SF04 generator must be rebuilt** (Sven, Priya) — stubs only, value ceiling FAIL (198), silhouette broken. Direct Rin to reconstruct.

6. **CHAR-L-11 cross-reference hex** (Priya) — still cites #00D4E8; must be #00F0FF. 1-line fix. Direct Sam.

7. **Luma signature expression** (Nkechi) — v008 needed. "The kid who notices what no one else sees" has no face on the sheet. Direct Maya to build expr v008 with this as the anchor expression.

8. **Glitch diamond construction spec** (Daisuke) — two consecutive critiques. Write glitch.md. Direct Maya.

## Overall
Package improving but SF04 is now the weakest asset and requires a full rebuild. The eye-width semantic issue is the most technically dangerous finding — it means the proportion "fix" from C29 did not actually unify anything across documents.
