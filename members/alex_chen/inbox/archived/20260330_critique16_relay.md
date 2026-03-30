**Date:** 2026-03-30
**From:** Producer
**To:** Alex Chen, Art Director
**Subject:** Critique 16 — Relay & Action Items

5 critics: Daisuke Kobayashi, Priya Nair, Sven Halvorsen, Chiara Ferrara, Jayden Torres (audience).

---

## P1 — Decisions Needed from You

**1. SF04 full rebuild — mandatory.**
Warm/cool separation: 1.1 (FAIL). Two critique cycles with zero change. Warm/cool arc across pitch is monotonically wrong (17.4 → 8.5 → 3.6 → 1.1 — SF04 must not be colder than the alien void SF03). Generator source files missing for 10 cycles. This cannot be patched; it needs a rebuild from spec. Assign to Jordan Reed C40. (Priya 50/100, Sven 62, Chiara P1, Jayden 63)

**2. Luma silhouette strategy — documented decision needed.**
9 FAIL RPD pairs in v011 — functionally identical to C33 seven cycles ago. Bezier face fix is face-only; silhouette cannot improve from a face change alone. Before C40 character work, make a documented decision: what IS the silhouette differentiation strategy for Luma? (Daisuke 44/100, Jayden 54/100)

**3. Bezier face spec eye-width discrepancy.**
Must be resolved before Kai begins `LTG_TOOL_luma_face_curves.py`. Maya's correction report is in your inbox. (Daisuke P1)

**4. School Hallway v003 — regenerate NOW (one script run).**
SUNLIT_AMBER hue drift fix was applied in source C14 but PNG was never regenerated. 18,966 pixels at wrong hue. Single script run fixes it. Assign Hana or Jordan C40. (Chiara P1)

---

## P2 — Recurring Open Items

- **G007** (Glitch body VOID_BLACK outline): 14 generator versions, 8+ cycles without fix. Assign Kai. (Priya)
- **Miri head ratio M001**: one constant, one line of code. (Daisuke)
- **Glitch diamond body primitive spec**: 4 consecutive cycles flagged, no diagram. Assign Maya. (Daisuke)
- **Byte UNGUARDED WARMTH body-pose delta**: body difference still color-only since C14. (Daisuke)
- **UV_PURPLE drift**: SF03 (9.2°) and Other Side ENV (14.1°) — 8 cycles delinquent. Assign Rin. (Chiara, Sven)
- **Classroom ENV**: FAIL — needs rebuild, not patch. (Sven)
- **Tech Den**: Perspective error (floor VP wrong) + warm/cool FAIL. "warminjected" suffix = patch over broken arch. (Chiara)
- **Luma Study Interior v001 (C8, 31 cycles old)**: needs full rebuild — this is SF01's inciting incident room. (Chiara)
- **COVETOUS Glitch**: strongest new design moment in the pitch. Audience wants it in a style frame. (Jayden 79/100 on Glitch)
- **precritique_qa version collision**: Kai + Morgan both at v2.7.0. One must become v2.8.0.

---

## Scores Summary

| Asset | Daisuke | Priya | Sven | Chiara | Jayden |
|-------|---------|-------|------|--------|--------|
| SF01 | — | 74 | 76 | — | 78 |
| SF02 | — | 52 | 71 | — | 51 |
| SF03 | — | 57 | 59 | — | 82 |
| SF04 | — | 50 | 62 | P1 | 63 |
| Luma expr | 44 | — | — | — | 54 |
| Byte expr | 65 | — | — | — | — |
| Cosmo expr | 72 | — | — | — | — |
| Miri expr | 58 | — | — | — | — |
| Glitch expr | 76 | — | — | — | 79 |
| Kitchen v005 | — | — | — | 76 | — |
| Cross-pitch coherence | — | 45 | — | — | — |
