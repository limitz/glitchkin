# Critique Cycle 10 — Dmitri Volkov, Character Design Lead
**Guest Critic: "Luma & the Glitchkin"**
**Date: 2026-03-29**

---

## Priority 1 — Byte Expression Sheet v003: STORM/CRACKED Panel

### The Spec vs. The Code

Section 9B is explicit. I read it. The team read it. Let me go through what was actually implemented versus what was specified, point by point.

**9B Grid Layout — FAIL (partial)**

The canonical 7×7 grid from byte.md Section 9B reads:
```
Row 0:  DIM   DIM   DIM   DIM   CRACK DEAD  DEAD
Row 1:  DIM   MID   DIM   CRACK DEAD  DEAD  DEAD
Row 2:  MID   DIM   CRACK DEAD  DEAD  BRIG  DEAD
Row 3:  DIM   CRACK DEAD  DEAD  BRIG  DEAD  DEAD
Row 4:  CRACK DEAD  DEAD  DIM   DIM   DEAD  DIM
Row 5:  DEAD  DEAD  DIM   MID   DIM   DIM   DIM
Row 6:  DEAD  CRACK DIM   DIM   MID   DIM   DIM
```

The tool's `glyph` array in `draw_pixel_symbol()` implements:
```python
glyph = [
    [1, 1, 1, 1, 0, 0, 0],   # row 0
    [1, 1, 1, 2, 0, 0, 0],   # row 1
    [1, 1, 2, 0, 0, 0, 3],   # row 2
    [1, 2, 0, 0, 0, 3, 3],   # row 3
    [2, 0, 0, 0, 3, 3, 3],   # row 4
    [0, 0, 0, 3, 3, 3, 3],   # row 5
    [0, 0, 3, 3, 3, 3, 3],   # row 6
]
# 0=dead, 1=alive_normal, 2=alive_bright, 3=dim
```

**Divergences from spec:**

1. **Row 0, col 4:** Spec says CRACK — code says DEAD (0). The diagonal crack position starts one column off.
2. **Row 1, col 3:** Spec says CRACK — code assigns BRIGHT (2). CRACK is not a glyph state; it is the physical Hot Magenta overlay line drawn separately. But the code is placing BRIGHT pixels *at the crack coordinates* rather than letting the crack overlay handle it. This is a layer order confusion.
3. **Row 2, col 6:** Spec says DEAD — code says DIM (3). Upper-right dead zone should be fully dead, not dim.
4. **Row 3, col 4:** Spec says BRIG — code says DEAD (0). Corona near crack is missing at (row 3, col 4).
5. **Row 4:** Spec says CRACK at col 0, then DEAD/DIM/DIM/DEAD/DIM. Code puts BRIGHT (2) at col 0 — again confusing the CRACK position with ALIVE_BRIGHT.
6. **Row 6, col 1:** Spec says CRACK — code says DEAD (0). Bottom of the crack diagonal is absent in the glyph.

**Summary on glyph:** The team has misread the CRACK row in the spec as "ALIVE_BRIGHT" and placed pixel states there. The crack is not a pixel state — it is a physical overlay. The glyph has 6 documented cell-level deviations from the canonical spec.

**Color values — PARTIAL FAIL**

Section 9B specifies:
- ALIVE_DIM: `#005064`
- ALIVE_MID: `#00A8B4`
- CRACK_LINE: `#FF2D6B`
- ALIVE_BRIGHT: `#C8FFFF` (White-Cyan)

Tool implements:
```python
DIM_PX    = (18, 52, 60)      # ≈ #123C3C — NOT #005064 — darker and greenish
ALIVE_PX  = (0, 180, 200)     # ≈ #00B4C8 — close to ALIVE_MID but not exact
BRIGHT_PX = (200, 255, 255)   # ≈ #C8FFFF — CORRECT
HOT_MAG   = (255, 45, 120)    # ≈ #FF2D78 — spec is #FF2D6B; 9 units off on blue channel
```

DIM_PX is substantially wrong — the eye background will read green-gray rather than the pure deep cyan mandated. At thumbnail this washes the whole dead-zone out. ALIVE_MID is within acceptable variance. BRIGHT is correct. HOT_MAG is 9 units off on the blue channel — close but not spec-compliant. These color deviations compound in the dead zone read.

**Crack line direction — PASS (barely)**

Spec: "upper-right to lower-left across the eye bezel."
Tool: crack drawn from `(ox + 4.5*cell, oy)` to `(ox + 2.0*cell, oy + 7*cell)` — this does run upper-right to lower-left. Directionally correct. But the crack line is rendered IN the glyph function, before the outer frame is drawn over it. The spec says crack overlay goes on top of everything (layer 4 in the production stack). Here the crack is rendered at the same layer as the pixel fill, potentially obscured by the frame rectangle drawn immediately before the glyph call. The draw order in `draw_byte()` does draw the chip_pts frame before calling `draw_pixel_symbol()` — correct. But within `draw_pixel_symbol()` the crack is drawn AFTER the glyph pixels, which should be fine. The ordering concern is minor here, but the single-line crack at `width=2` will likely disappear at panel scale (panels are 240×320). At `eye_size = max(14, int(body_ry * 0.46))` ≈ 28–32px, each cell is 4px. The crack line at 2px in a 28px eye is genuinely marginal — one lost anti-alias pixel and it's invisible.

**Crack overlay spec compliance — FAIL**

Section 9B says: "The crack is rendered in Void Black (#0A0A14) as a 1–2px line OVER the glyph display." The STORM/CRACKED eye should therefore have a void-black crack, not the Hot Magenta one the tool draws inside the dead_zone function. The Hot Magenta (#FF2D78) is the *physical surface crack on the body* and *the crack_frame exterior mark* — those are correctly HOT_MAG. The dead-zone pixel glyph crack overlay should be void-black per spec. This is a direct spec violation.

**Cracked eye frame — PASS**

The chip_pts polygon correctly implements the spec's "top-right corner has a small chip/fragment missing (triangular gap)." The irregular frame is handled well. This part works.

**Right organic eye (cracked_storm style) — PASS**

50% aperture, downcast pupil, dimmed highlight, heavy upper lid, parabolic lower lid sag — all implemented, all distinct from droopy_resigned (deeper sag: `sag = 8 * 4 * t * (1-t)` vs `7 * 4`). This is the best-implemented part of the STORM panel. It reads.

**Body posture — MARGINAL PASS**

body_tilt=18 vs RESIGNED body_tilt=14. Difference is 4 units — at the panel scale (PANEL_W=240, figure ~88px wide), this is a few pixels of lean delta. It's measurably different from RESIGNED in code but likely imperceptible at thumbnail. The bent antenna and storm_damage crack marks add texture that helps differentiate at thumbnail even when the lean delta is too small to read alone. Saved by the details, not the posture itself.

**Storm background texture — PASS**

Circuit trace fragments + UV diagonal + spark noise. It reads as damaged/cold against the other panels' cleaner backgrounds. Squint test: the near-void BG_STORM (12,10,22) vs BG_RESIGNED (24,26,34) — the STORM panel is noticeably darker. Panel differentiation at thumbnail: adequate.

**9-panel layout coherence — MARGINAL PASS**

The 3×3 grid fills correctly. 9 panels, no empty slots, no overflow. Label bars are consistent. STORM occupies position [2,2] (bottom-right) — the natural escalation endpoint position. The [NEW v003] tag in HOT_MAG is legible and appropriate. The layout itself is coherent. What it cannot hide is that STORM and RESIGNED share near-identical body-language at thumbnail distance, and POWERED DOWN reads darker than STORM in some tonal environments. Position reads are: NEUTRAL center-mass, GRUMPY wide-stance, SEARCHING forward reach, ALARMED exploded limbs, RELUCTANT JOY slightly collapsed, CONFUSED lean + arm asymmetry, POWERED DOWN uniform slump, RESIGNED narrow slump, STORM narrow slump + lean. The last two are not sufficiently differentiated at thumbnail.

### Priority 1 Grade: **C+**

The panel exists, the intent is correct, and several elements (organic eye, chip frame, storm BG, antenna bend) are solid. The glyph implementation diverges from spec at 6+ cell positions, the DIM pixel color is wrong, the crack overlay color is wrong (should be void-black, not magenta), and STORM/RESIGNED are not thumb-distinct. Not acceptable for production.

---

## Priority 2 — Grandma Miri Expression Sheet v002

### Ground-Up Rebuild Assessment

The rebuild directly addressed the failure mode from v001: face-only differentiation. Let me apply the squint test to each of the 5 expressions.

**Squint test — expression by expression:**

1. **WARM/WELCOMING** — `arm_l_style: "extended"`, `arm_r_style: "extended"`, `body_tilt: -6`. Extended arms use a bezier curve sweeping outward. At thumbnail: the A-frame wide arm silhouette should be visible. The extended arm terminus drops to `arm_h * 0.60` = approximately 42% of arm length along the bezier — the hands end at mid-width. This is wider than the torso but not dramatically so. The forward lean (-6px tilt at torso top) is minimal at render scale. **Squint test: MARGINAL PASS.** The arms extend but the bezier midpoint pull is not aggressive enough to guarantee a wide read at 200px thumbnail. It'll pass at 300px+.

2. **SKEPTICAL/AMUSED** — `arm_l_style: "crossed"`, `arm_r_style: "crossed"`, `body_tilt: +10`. The crossed arm style sends each arm across the centerline: `cross_x = cx + (-side) * int(HR * 0.30)`. At render scale (HR=136), that's ±41px cross distance. With `arm_w=27px`, the crossed arms create a horizontal band across the torso. At thumbnail this reads as a chest-mass block — the classic arms-crossed silhouette read. The hip lean (+10px) adds slight asymmetry to the torso top. **Squint test: PASS.** This is the strongest expression in the sheet — the arms-crossed bulk reads clearly even at 150px.

3. **CONCERNED** — `arm_l_style: "hanging"`, `arm_r_style: "chest"`, `body_tilt: -10`. Asymmetric: one arm straight down, one curved to chest level. The asymmetric shoulder line is the read — at thumbnail, a hanging arm vs. a raised elbow creates a visible left/right weight difference. Forward lean at -10px is marginally visible. **Squint test: PASS.** The asymmetry saves it.

4. **SURPRISED/DELIGHTED** — `arm_l_style: "raised"`, `arm_r_style: "raised"`, `body_tilt: +14`. Both arms raised: the bezier terminus is at `ay - arm_h * 0.42` — arms go UP, above shoulder line. At thumbnail this is the maximum wingspan-up silhouette. Combined with `pupils_wide: True`, open mouth, and raised brows (-int(HR * 0.28) = -38px raise). **Squint test: STRONG PASS.** This is unmistakable. Cannot be confused with anything else on the sheet.

5. **WISE/KNOWING** — `arm_l_style: "folded"`, `arm_r_style: "folded"`, `body_tilt: 0`. Arms fold inward toward center at `fold_x = cx + side * int(HR * 0.28)`. Both arms pulled toward body center — a compact settled rectangle. At thumbnail: arms in, upright posture, no lean. Reads as still. The eyes at `l_open: 0.62, r_open: 0.62` (half-lidded) and `knowing` mouth style are face signals that support but cannot be read at thumbnail. **Squint test: PASS (posture-dependent).** The folded arm geometry produces a distinctively narrow profile compared to the other expressions. But this is the expression most at risk of reading like a slightly different SKEPTICAL at very small sizes — both have arms pulled toward body center.

**Technical quality:**

The 3-tier line weight system is correctly applied: silhouette at 6px (draw_ellipse outline=LINE, width=6), interior structure at 4px, detail (crow's feet, smile lines) at 2px. This is disciplined. Crow's feet are ALWAYS PRESENT regardless of expression — that's a character-correct canonical detail and it's implemented. The cardigan cable-knit lines, pocket details, and chopstick pair all render at appropriate weights.

**Brow asymmetry for SKEPTICAL** — `brow_l_dy: -int(HR * 0.18)` = -24px raise (left brow high), `brow_r_dy: 0` (right brow flat). This one-brow read is correctly implemented. The smirk mouth (`style: "smirk"`) — bezier with one corner up — complements it.

**Palette compliance** — All colors traced back to grandma_miri.md canonical palette. SKIN_BASE (#8C5430), CARDIGAN (#B85C38), GLASSES_COL (#3B2820) — all correct.

**One structural concern:** The `cy_offset` per expression shifts the face position vertically by -8 to -12px within the panel. This means the face is not consistently placed across panels. At thumbnail when comparing expressions side by side, the face appears to float at slightly different heights. This is a minor but real inconsistency in the layout — a production pipeline reviewer will notice it.

**Body-to-face agreement:** Each expression's face parameters are aligned with body posture direction. WARM has genuine blush + warm mouth + extended arms — all three channels agree. SKEPTICAL has one raised brow + smirk + arms crossed — three-channel agreement. This is a material improvement over v001. The rebuild succeeded at its stated goal.

### Priority 2 Grade: **B+**

The rebuild is substantially better than v001. Four of five expressions pass the squint test confidently. WISE/KNOWING is a marginal pass — too visually similar to SKEPTICAL at extreme reduction. The cy_offset inconsistency is a minor technical flaw. The technical quality of the drawing code (line weights, bezier curves, Bezier-based brows, crow's feet system) is genuinely strong work. This sheet is production-eligible with one fix.

---

## Priority 3 — Cosmo Expression Sheet v003: SKEPTICAL Lean Fix

### The Fix

v001/v002 bug: `tilt_off = int(body_tilt * 0.4)`. For `body_tilt=6`: 6 × 0.4 = 2.4px — invisible.
v003 fix: `tilt_off = int(body_tilt * 2.5)`. For `body_tilt=6`: 6 × 2.5 = 15px.

I previously said the fix was not visible in the output despite being in the code. Now the code has been rewritten with the new multiplier. Let me assess whether 15px is sufficient.

**At panel scale:** PANEL_W=280, PANEL_H=420. Cosmo's torso is `torso_hw = int(hu * 0.41)` where `HU = int(PANEL_H * 0.155)` ≈ 65px. So `torso_hw` ≈ 27px. The torso is 54px wide. A 15px displacement at the top of the torso (while the bottom remains at center) means the torso's top edge is shifted 15px. Over a 54px-wide torso, that's a 28% offset — this should read as a lean even at small sizes.

**Squint test for SKEPTICAL vs. other expressions:**

- NEUTRAL: `body_tilt=0`, `arm_l_dy=0`, `arm_r_dy=0`. Upright, centered arms.
- FRUSTRATED: `body_tilt=4` (tilt_off=10px), `arm_l_dy=20, arm_r_dy=12` — arms lower.
- DETERMINED: `body_tilt=-5` (tilt_off=-12.5px forward), `arm_r_dy=-30` — right arm notably high.
- SKEPTICAL: `body_tilt=6` (tilt_off=15px backward), `arm_l_dy=-14, arm_r_dy=-10` — arms pulled up/tight.
- WORRIED: `body_tilt=-4` (tilt_off=-10px), `arm_l_dy=6, arm_r_dy=6` — slight forward lean, symmetric arms.
- SURPRISED: `body_tilt=5` (tilt_off=12.5px), `arm_l_dy=-18, arm_r_dy=-22` — arms raised high.

**Lean delta analysis:** SKEPTICAL (15px backward) vs. SURPRISED (12.5px also backward-tilted). These two are tilting in the SAME direction with only 2.5px difference. At thumbnail the lean direction will be identical. What differentiates them is arm position: SKEPTICAL has arms pulled tight to chest (arm_l_dy=-14), SURPRISED has arms flung high (arm_l_dy=-18, arm_r_dy=-22). At thumbnail the arm position difference is the read, not the lean. The lean itself is not what distinguishes SKEPTICAL — it was supposed to be the distinctive backward-lean read, but SURPRISED is also backward-leaning, undermining the differentiation strategy.

**The actual SKEPTICAL differentiator:** `brow_data: l_raise=18, r_raise=0` — asymmetric brows (only one raised). This is a face signal, not a body signal. At thumbnail the asymmetric brow is not legible. The arm-tuck (`arm_l_dy=-14`) reads as arms held high and tight, which at thumbnail looks like a raised-arm posture rather than a contained/skeptical one. Arms drawn at `-14` and `-10` from base — these are pushed upward. A true arms-crossed skeptical body language would have the arms moved laterally in toward center, not just pushed upward.

**The fix works but the expression design has a structural flaw.** The lean is now visible. The squint test for SKEPTICAL: small dark shape with arms tight and tilted backward. The squint test for SURPRISED: small dark shape with arms flung upward and tilted backward. These are distinct enough at panel scale but blur together at extreme reduction. The lean fix is real and meaningful. The expression still has a design debt.

**Notebook position in SKEPTICAL:** `notebook_open=False` — notebook is tucked. Tuck position is `nb_tuck_x = cx - torso_hw - int(hu * 0.02)` — left side, under the left arm. With arm_l_dy=-14 (arm raised), the notebook tuck position follows the arm. This is geometrically correct but visually slightly awkward — the arm is raised but the notebook doesn't suggest hugging behavior because the arm is raised vertically rather than crossing the body horizontally.

**One-brow asymmetry** — `l_raise=18, r_raise=0`. At panel scale, this should be the strongest face read. `brow_thick = max(3, int(hu * 0.028))` ≈ max(3, 2) = 3px. A 3px brow at panel scale is legible. The 18px raise on the left brow is a full eyebrow length above the right. This is the SKEPTICAL read that works, and it works only at panel scale, not thumbnail.

### Priority 3 Grade: **B-**

The lean formula fix is real, confirmed, and produces a visible result (15px vs. 2.4px — a 6× improvement). Full credit for fixing the bug as instructed. The SKEPTICAL expression now has a genuine backward lean that differentiates it from NEUTRAL and WORRIED. It does NOT fully differentiate from SURPRISED at thumbnail because both expressions lean backward. The one-brow asymmetry saves the expression at panel scale. This passes, but the expression design needs a future revision to make the body language truly unambiguous — ideally a lateral arm cross rather than a vertical arm raise to sell "skeptical containment" instead of "slightly startled."

---

## Overall Assessment

| Sheet | Grade | Status |
|---|---|---|
| Byte v003 — STORM/CRACKED | C+ | Not production-ready. Glyph spec deviations, wrong crack overlay color, RESIGNED/STORM thumb-ambiguity. |
| Grandma Miri v002 — Rebuild | B+ | Production-eligible. WISE/KNOWING thumbnail risk needs watch. cy_offset inconsistency minor. |
| Cosmo v003 — SKEPTICAL lean fix | B- | Lean fix confirmed effective. SKEPTICAL/SURPRISED backward-lean collision is a known design debt. |

---

## Top 3 Priority Fixes

**Fix 1 — Byte v003 STORM/CRACKED: Correct the dead_zone glyph against Section 9B canonical spec.**
The glyph array has 6+ cell-level deviations. The DIM pixel color is wrong (#123C3C vs. #005064). The crack overlay inside the dead_zone function must be changed from HOT_MAG to void-black (#0A0A14) per spec — the hot magenta crack belongs on the *body surface and frame exterior*, not the dead-zone pixel glyph overlay. Fix the glyph array row-by-row against the canonical grid. Fix DIM_PX to (0, 80, 100). Fix the crack line inside draw_pixel_symbol dead_zone branch to fill=LINE (void black). This is a spec compliance issue, not a stylistic one.

**Fix 2 — Byte v003 STORM/CRACKED: Differentiate STORM from RESIGNED at thumbnail.**
body_tilt delta of 4 units (+18 vs +14) is insufficient at panel scale (240px wide). STORM needs at minimum one additional visual differentiator that reads at thumbnail: either a significantly wider leg spread than RESIGNED (currently leg_spread=0.72 vs RESIGNED 0.70 — effectively identical), or an arm extension asymmetry (one arm up, one hanging for "collapse-stagger" instead of symmetric drop). The arm_l_dy=12, arm_r_dy=10 in STORM is nearly identical to RESIGNED's arm_l_dy=14, arm_r_dy=14. Introduce a 20+ unit asymmetry between arms in STORM — e.g., arm_l_dy=6, arm_r_dy=22 — to suggest physical imbalance. The storm state should read as damaged-asymmetric at thumbnail, not just-slightly-more-resigned.

**Fix 3 — Cosmo v003 SKEPTICAL: Redesign arm posture to read as containment rather than vertical raise.**
The arm_l_dy=-14 and arm_r_dy=-10 pushes arms upward, which at thumbnail looks like a mild SURPRISED rather than skeptical containment. Change the SKEPTICAL body language to use laterally-inward arm positioning — simulate the arms crossing or tucking across the torso center. This requires either extending the body renderer to support a crossed-arm style (analogous to Grandma Miri's "crossed" style) or compensating with arm_x_scale reduction and a body_squash change that visually compresses the arm width read. The goal: SKEPTICAL should read as "contracted inward" at thumbnail, not "raised slightly."

---

*The dead-pixel glyph compliance issue on Byte is not negotiable. Section 9B exists precisely because that eye is the character's central visual hook. If the production team cannot implement the spec correctly in a tool, the tool cannot be trusted in production. Fix it from the canonical spec. No shortcuts.*

— Dmitri Volkov, Character Design Lead
