**Date:** 2026-03-30
**From:** Lee Tanaka
**Subject:** P14/P15 Staging Review — 4 findings

Diego,

I reviewed P14 (Byte Ricochet) and P15 (Luma Floor / Glitch Hair Circle) for staging quality. Both panels are structurally sound. The beats read and the camera choices are correct.

4 refinement items:

**P14:**
1. **WARN — Byte impact silhouette has no ALARMED expression.** `draw_byte_silhouette()` draws identical eyes for all 5 ghost positions. At the impact point (alpha=1.0), Byte should show ALARMED: cracked eye wider, asymmetric brows, mouth line. Ghost trail positions can stay expressionless.
2. **NOTE — Symmetric arms at impact.** Both arms draw identical at the impact position. Bounce-back recoil needs one arm trailing (toward origin) and one flung outward (impact reaction).

**P15:**
3. **WARN — Right arm is a straight line.** Single 18px line from torso to `PW*0.22`. Needs elbow bend (two-segment polyline), hand blob at endpoint, and hoodie sleeve bunching. Same urgency principle from C12/C13.
4. **NOTE — Body sprawl too neat.** Hoodie and pants are aligned rectangles. A 4-6 degree torso rotation + one bent knee would sell "just hit the floor" vs "lying flat by choice."

Full report: `output/production/staging_review_c47_sf06_p14_p15.md`

-- Lee
