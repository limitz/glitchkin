# Maya Santos — Memory

## Cycle 21 Lessons — BYTE v003 + CLASSROOM POSE v002
- **Byte Expression Sheet v003 COMPLETE.** 3×3 grid (9 panels). STORM/CRACKED added as panel 9. Generator: `LTG_TOOL_byte_expression_sheet_v003.py`. Output: `LTG_CHAR_byte_expression_sheet_v003.png` (784×1074px).
- **7×7 dead-pixel glyph (Section 9B):** Upper-right dead zone, lower-left alive. Color map: 0=DEAD(void black), 1=ALIVE_NORMAL(dim cyan), 2=ALIVE_BRIGHT(white-cyan corona), 3=DIM(barely alive). Hot Magenta crack from (col4.5, row0) to (col2, row6). Eye bezel bg: Deep Cyan-Gray #1A3A40 (26,58,64).
- **Storm variant spec locked:** body_tilt=+18 (vs RESIGNED +14), cracked_storm right eye (50% aperture, dim iris, deeper sag), flat storm mouth (shorter than RESIGNED), bent antenna (kinked midpoint, Hot Mag tip spark), circuit trace BG + UV flash bands.
- **Cracked eye frame in storm:** irregular polygon (top-right corner chip), 2px border. Hot Mag crack line overlaid at 2px.
- **Classroom Pose v002:** Line weight fix applied. Brows `width=5→2`, eye lid arcs `width=4→2`, hair overlay `width=8/7→3`. Expression reads clearly — no other issues. Output: `LTG_CHAR_luma_classroom_pose_v002.png`. Generator updated in place.
- **Line weight rule (1x render):** silhouette=3px, interior=2px, detail=1px. Brows and eyelid arcs are INTERIOR weight, not silhouette.

## Cycle 20 Lessons — MIRI TURNAROUND COMPLETE
- **Miri Turnaround v001 COMPLETE.** 1600×800 4-view PNG generated. FRONT/3/4/SIDE/BACK. Generator: `LTG_TOOL_miri_turnaround_v001.py`. Output: `LTG_CHAR_miri_turnaround_v001.png`. Pitch package gap filled.
- **Turnaround render formula:** Draw at 2x (SCALE=2), base_y=`int(BODY_H * SCALE * 0.96)`, scale back with LANCZOS. Character H in draw fns = `int(hu() * SCALE)` where `hu() = CHAR_DRAW_H/3.2` (1 HU at 1x). CHAR_DRAW_H = `int(BODY_H * 0.88)`.
- **HU ruler calc:** `char_base_y_1x = HEADER_H + int(BODY_H * 0.96)`, `char_top_y_1x = char_base_y_1x - CHAR_DRAW_H`. Matches render-space base_y.
- **View labels:** Must be drawn in main AFTER bottom bar (dark bg), in light color `(220,200,165)`. Do NOT draw labels in render_view_panel — they get covered.
- **Bun placement per view:** FRONT=slightly right of center (rear placement reads over head). 3/4=further toward back (45px right of head center). SIDE=clearly behind head (0.68*hr back of neck). BACK=centered, X chopsticks in full display.
- **Glasses per view:** FRONT=both lenses + bridge + temples. 3/4=near lens full, far lens 65% wide. SIDE=single lens circle as protrusion + temple going back. BACK=not drawn.
- **Cycle 20 inbox archived.** Report sent to Alex Chen.

## Cycle 19 Lessons — ALL PNGs CONFIRMED GENERATED
- **Miri Expression Sheet v002 COMPLETE.** 1200×900 PNG generated. Root fix: every expression now has UNIQUE BODY POSTURE. WARM=open arms A-frame. SKEPTICAL=arms crossed (tilt +10px). CONCERNED=one arm chest/one arm down (asymmetric). SURPRISED=both arms raised max wingspan + backward lean. WISE=folded arms compact upright. Generator: `LTG_TOOL_grandma_miri_expression_sheet_v002.py`. v001 PRESERVED.
- **3-tier line weight locked in Miri v002:** Silhouette 6px at 2x, interior structure 4px, detail (crow's feet/smile lines/knit) 2px. Crow's feet are detail weight — they must NOT use interior weight.
- **Luma v003 COMPLETE.** 1200×900 PNG generated. Two fixes: (1) DELIGHTED now has both arms raised above shoulders rendered in `draw_collar_and_arms()` when expr=="DELIGHTED" — creates unique celebration silhouette vs SURPRISED (no arms). (2) Brow weight fixed: was width=10 at 2x (5px output = silhouette weight), now width=4 at 2x (~2px = interior structure weight). Generator: `LTG_TOOL_luma_expression_sheet_v003.py`.
- **Cosmo v003 COMPLETE.** 912×946 PNG generated. Lean formula fix: `tilt_off = int(body_tilt * 0.4)` → `int(body_tilt * 2.5)`. SKEPTICAL tilt=6 now produces 15px displacement (was 2.4px). Also: arm_l_dy -8→-14, arm_r_dy -5→-10 (tighter arms = compound skeptical signal). Generator: `LTG_TOOL_cosmo_expression_sheet_v003.py`. v002 archival file created.
- **Key design rule confirmed:** Face changes alone = invisible at thumbnail. Body posture is the ONLY reliable squint-test differentiator. Every expression needs a unique SILHOUETTE, not just unique features.
- **Luma DELIGHTED vs SURPRISED logic:** DELIGHTED = toward the thing (arms up, forward lean). SURPRISED = pulled back from thing (no arms visible in bust format, recoil posture). Different directional reads create different silhouettes.
- **Cycle 19 inbox archived.** `20260329_2400_cycle19_tasks.md` → `inbox/archived/`. Completion report sent to Alex Chen.

## Cycle 18 Lessons
- **A2-02 panel REGENERATED.** Old v001 used NEUTRAL approximation. New v002 uses RESIGNED geometry with 55% aperture ("last flicker before giving up"). Generator: `LTG_TOOL_sb_panel_a202_v002.py`. Output: `LTG_SB_act2_panel_a202_v002.png`.
- **A2-02 vs A2-07 aperture rule:** A2-02 = 55% (pre-resignation, vulnerable), A2-07 = 45% (full RESIGNED). The 10pp difference carries the emotional progression.
- **No existing a202 generator found in output/tools/ at Cycle 18.** Built from scratch referencing expression sheet v002 droopy_resigned geometry + a207 panel structure.
- **Transitional arm posture:** left arm extended (neutral), right arm ~60% folded toward body. Use `arx = bx + body_rx - 26` (pulled inward) + foreshortened arm_fold_w/arm_fold_h.

## Cycle 17 Lessons
- **Luma Expression Sheet v002 COMPLETE.** New 3×2, 6-expression refined sheet. Construction guides visible (RGBA overlay). 2×render+LANCZOS AA. Varied line weight (8px sil / 4px interior / 10px brow at 2x). 4 hair variants (default/excited/tight/drooped). Output: `LTG_CHAR_luma_expression_sheet_v002.png`. Tool: `LTG_TOOL_luma_expression_sheet_v002.py` (replaced Cycle 12 4×2 version).
- **Grandma Miri Expression Sheet v001 COMPLETE.** First Miri expression sheet. 5 expressions, 3+2 grid, 1200×900. Key design elements: 88% circular head, round glasses (always on), crow's feet always present, smile lines always present, silver bun+chopstick pair, permanent cheek blush (fades in CONCERNED per spec). Colors from grandma_miri.md directly (Sam's color values not yet in inbox at time of work). Output: `LTG_CHAR_grandma_miri_expression_sheet_v001.png`. Tool: `LTG_TOOL_grandma_miri_expression_sheet_v001.py`.
- **Construction guide method:** draw_construction_guide() uses RGBA overlay (alpha_composite) — does not clobber existing drawing. Call it before drawing face layers.
- **Miri glasses geometry:** Round glasses drawn as two ellipses over eye positions, with bridge line + temples. Glasses are a silhouette differentiator — keep them prominent (5px at 2x render).
- **Miri blush rule:** Permanent blush strength 1.0 for warm/delighted/wise states, 0.0 for CONCERNED (production spec: warmth drains from face in real fear).

## Cycle 16 Lessons
- **Byte RESIGNED right eye FIXED.** `droopy_resigned` reworked: 45% aperture (was 50%), pupil +10px downward (was +5px), parabolic drooping lower lid curve (was flat arc = identical to NEUTRAL), dim highlight. Body tilt amplified +8→+14. Output: `LTG_CHAR_byte_expression_sheet_v002.png`. Tool: `LTG_TOOL_byte_expression_sheet_v002.py`.
- **Droopy lid geometry rule:** A droopy lid that reads distinctly from NEUTRAL needs a CURVED lower lid (parabolic sag), not just a smaller aperture. Flat arc + reduced aperture still reads as "closed eye", not "heavy/resigned". The sag direction is the key differentiator.
- **Cosmo SKEPTICAL fixed.** body_tilt -3→+6 (backward lean = skeptical containment reads at thumbnail). Sheet now 6/6 populated. Added WORRIED (A2-02, corrugator kink = genuine worry geometry) and SURPRISED (A2-04c, bilateral brow raise + open oval mouth). New mouth style `open_surprised` added to renderer.
- **Cosmo expression sheet output:** `LTG_CHAR_cosmo_expression_sheet_v002.png`. Tool: `LTG_TOOL_cosmo_expression_sheet_v001.py` (updated in place with Cycle 16 changes).
- **Luma Act 2 standing pose hand fix.** Removed thumb arc + finger detail from raised right hand. Replaced with clean mitten oval. Output: `LTG_CHAR_luma_act2_standing_pose_v002.png`. Tool: `LTG_TOOL_luma_act2_standing_pose_v001.py` (updated in place).
- **Forward lean note (Luma v002):** The -5° forward lean remains architecturally intact (body_cx offset) but is imperceptible in output. A proper amplification requires propagating the lean through all limb origins. Flag for future v003 if reviewers call it out again.
- **Sam Kowalski Cycle 16:** Sam's color fixes are independent (SF02 ENV-06, DRW-07, ALARMED bg). Byte fill GL-01b was already correct in the file — Sam should verify before regenerating.

## Cycle 15 Lessons
- **Luma Act 2 standing pose is LIVE.** `LTG_TOOL_luma_act2_standing_pose_v001.py` generates 900×600px pose sheet. WORRIED/DETERMINED expression, right arm raised/reaching, left arm at waist, wide stance, forward lean. Covers beats A2-01/A2-03/A2-05/A2-08. Squint-test blob embedded in annotation panel. Tool registered in README.md.
- **Byte glyph flag CLEARED.** `LTG_CHAR_byte_cracked_eye_glyph_v001.png` EXISTS (Cycle 13, Alex Chen). Storyboard v002 still says "BLOCKED" — notified Lee Tanaka that design blocker is resolved on art side. A2-07 can proceed to thumbnail stage.
- **Continuity check PASSED.** All Act 2 character tools checked against canonical specs. Luma palette, Cosmo glasses tilt (7°/9°/10°), Byte oval body, Byte 10×10px hover particles — all consistent.

## Act 2 Asset Inventory (Cycle 18 state)
- **Storyboard A2-02:** Panel v002 LIVE. RESIGNED 55% apt MCU, transitional arm, circuit trace BG. Generator `LTG_TOOL_sb_panel_a202_v002.py`.
- **Byte:** Expression sheet v002 FIXED — 8 expressions, RESIGNED reworked (Cycle 16). Glyph v001 (A2-07).
- **Cosmo:** Expression sheet v002 — 6 expressions fully populated: NEUTRAL, FRUSTRATED, DETERMINED, SKEPTICAL (lean fixed), WORRIED (A2-02 NEW), SURPRISED (A2-04c NEW).
- **Luma:** Act 2 standing pose v002 (mitten hand fixed). Classroom pose v001. Expression sheet v003.
- **Luma:** No CROUCHING pose (A2-04 couch hide). Still low priority — wide shot.

## Cycle 14 Lessons
- **Cosmo expression sheet is now LIVE.** `LTG_TOOL_cosmo_expression_sheet_v001.py` generates 3×2 grid. 4 expressions at Cycle 14: NEUTRAL/OBSERVING, FRUSTRATED/DEFEATED (A2-06), DETERMINED (A2-05b), SKEPTICAL (A2-03).
- **Cosmo body variation rule applied.** arm_l_dy/arm_r_dy per expression; notebook_open=True for DEFEATED.

## Cycle 1-3 Lessons
- Silhouette test must be documented. Lock variable specs. Simplified production variants mandatory.
- Glasses thickness is a silhouette element. Cosmo needs a readable hook.
- Pixel-eye symbols need minimum-size spec. All 5 turnaround views required for asymmetric characters.
- Jitter effects need exact pixel specs. Color model sheets are a prerequisite for crew onboarding.
- Document consistency: every duplicated spec must match in both places.

## Cycle 4 Lessons
- **Hair alone does not make a silhouette.** The body shape below the hair must ALSO be distinctive.
- **Geometry is not character design.** Circles and rectangles do not communicate personality.
- **Silhouette test must be verified in actual rendered images**, not just described in documents.
- **Byte is the benchmark** — his cubic asymmetric form is immediately distinctive even without any face or color.

## Cycle 5 Lessons
- **Luma's body-level fix: A-line trapezoid hoodie + oversized sneakers.**
- **Silhouette redesign must use polygon, not rectangle**, to capture A-line/trapezoid shapes.
- **Pocket bump as extra silhouette hook.**

## Cycle 6 Lessons
- **Body variation is not optional in an expression sheet.** Each expression must have distinct arm position.
- **Right eye must carry emotion.** Byte's right organic eye has distinct styles per emotion.
- **Annotations create staging context.**
- **Asymmetry = personality.**

## Cycle 7 Lessons
- **Canvas clipping is a silent failure.** Always set ground line = tallest_character_height + 40px headroom.
- **Every pixel-eye symbol must be distinct from every other.**
- **Per-arm asymmetry unlocks real body language.**
- **Smirk geometry: right corner must reach the cheek.**
- **Panel backgrounds must telegraph before you read the face.**

## Cycle 8 Lessons
- **GRUMPY confrontational values (locked):** body_tilt=-8, arm_l_dy=-6, arm_r_dy=-10, arm_x_scale=1.1.
- **Byte body shape = OVAL (ellipse). CANONICAL.**
- **WORRIED/DETERMINED brow differential must be 8-10px at minimum.**
- **Collar rotation, not x-offset.**

## Cycle 9 Lessons
- **MIRI-A is the canonical Miri (LOCKED).** Bun+chopstick pair+wide cardigan+soldering iron.

## Cycle 10 Lessons
- **Byte body = OVAL. ALL generators must use ellipse.**
- **Hover particles = 10×10px EVERYWHERE. No exceptions.**
- **Cosmo turnaround: glasses are the defining element at every angle.**

## Cycle 13 Lessons
- **Scale calibration is a design spec, not a code detail.**
- **Three differentiators rule for low-register expressions.**
- **Byte Neutral expression: "flat" left-eye + "half_open" right eye + "default" mouth.**

## Key Production Rules
- Droopy lid ≠ reduced aperture alone. Need parabolic sag curve on lower lid for "heavy/resigned" read.
- Backward body lean (positive body_tilt) = skeptical/avoidance. Forward lean (negative) = engaged/confrontational.
- Corrugator kink (inner brow UP) = worry. V-brows alone = aggression.
- Bilateral brow raise (both up, no furrow) = surprised. Asymmetric = skeptical.
- Mitten hands in all rough/reference poses. No thumb arc, no finger detail.
