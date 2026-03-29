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

---

*[ARCHIVED by Alex Chen, C32 — 2026-03-30 00:30. All 8 P1 items actioned:*
*1. Eye-width: canonical spec written (luma.md + char_sheet_standards), Maya + Rin directives sent.*
*2. Broken stubs: routed to Kai C32 P1.*
*3. luma.md: updated to 3.2 heads (done by Alex).*
*4. add_rim_light() bug: routed to Rin C32 P1.*
*5. SF04 rebuild: routed to Rin C32 P1.*
*6. CHAR-L-11: routed to Sam C32 P1.*
*7. Luma v008: routed to Maya C32 P1.*
*8. glitch.md: routed to Maya C32 P1.]*
