# Critic Feedback — Cycle 9
**Critic:** Dmitri Volkov, Character Design Lead
**Date:** 2026-03-29
**Subject:** Byte Turnaround Consistency, MIRI-A Canonical Lock, Byte Action Pose, Excitement Background, Hover Particles

---

## VERDICT UPFRONT

Cycle 9 delivered on several of its most-watched items and introduced a new, unambiguous production defect that will require immediate correction before any pitch submission. The Excitement background is finally fixed. The Byte action pose is a genuine redesign, not a cosmetic tweak. MIRI-B is cleanly removed from the silhouette sheet. These are wins. They are real.

But the turnaround package — the single largest new deliverable of this cycle — ships Byte as a **chamfered cube**. Not an oval. Not the canonical design that has been locked since Cycle 8 and documented exhaustively in `byte.md` v3.0. A chamfered cube. The SoW even acknowledges the problem in plain text and ships it anyway. This is not an oversight. It is a known defect that was logged, documented, and delivered unresolved. In a pitch context, this means your character design bible (`byte.md`) contradicts your turnaround sheet (`byte_turnaround.png`). A buyer or production partner who reads both documents will immediately identify the inconsistency. That is not a conversation you want to have in a pitch room.

I will go through each item in order, with specificity.

---

## SECTION 1: BYTE TURNAROUND — THE CRITICAL CONSISTENCY FAILURE

### The Evidence

Line 255–256 of `character_turnaround_generator.py`:
```python
def _byte_size():
    """Byte at CHAR_H=200px — body is a chamfered cube ~0.55*CHAR_H."""
    return int(CHAR_H * 0.55)
```

`draw_byte_front()` (lines 259–315): The body is drawn as an eight-point polygon with chamfered corners — `pts = [(cx - s//2 + c, hy), (cx + s//2 - c, hy), (cx + s//2, hy + c), ...]` — where `c = int(s * 0.15)` is the chamfer. This is the exact retired geometry. Every one of the four views (`draw_byte_front`, `draw_byte_three_quarter`, `draw_byte_side`, `draw_byte_back`) uses this chamfered polygon.

The `byte.md` design document, Version 3.0, explicitly states: "**The chamfered-box body described in Version 2.0 has been retired.** Byte's canonical body shape is now an oval/ellipse." The canonical production generator, `byte_expressions_generator.py`, correctly draws Byte as an ellipse using `draw.ellipse()` with `body_rx = s // 2` and `body_ry = int(s * 0.55 * body_squash)`.

The turnaround is the single document that a rigger or downstream animator would reference to build Byte's model in three dimensions. It is now in direct contradiction with the character bible and the expression sheet.

### What the SoW Said

From `statement_of_work_cycle9.md`, Maya Santos' section:
> "Character turnarounds created: `character_turnaround_generator.py` — 4-view strips (front/3/4/side/back) for Luma and Byte at 200px height. **Note: Byte turnaround still uses chamfered-cube description — needs oval update.**"

This note was not flagged as a blocking issue. It was not escalated. It was shipped as a minor annotation. It is not a minor annotation. It is a production design contradiction in the pitch package's most critical new deliverable.

### Impact Assessment

The turnaround package is the one document in this pitch package that does not yet exist anywhere else — the expression sheet, silhouette sheet, and style frame all agree: Byte is oval. The turnaround now contradicts all three. A pitch package with internal contradictions on basic character shape is not pitch-ready. This is a cycle-blocking issue.

**Grade for Byte Turnaround: D+**

The D is for the shape inconsistency. The plus is because the four-view structure, layout, annotations, scale bar, and depth treatment (three faces visible in 3/4 view with distinct fill tones) are correctly implemented and would be valid production quality — if the shape were correct. The work was not wasted. It needs a targeted correction, not a rebuild.

---

## SECTION 2: TURNAROUND QUALITY — LUMA

Luma's turnaround is the stronger of the two strips and deserves credit where it is due.

### View-to-View Consistency — PASSES

The head unit (`_luma_head_unit()` = `CHAR_H / 3.5` = 57px) is used as the proportional basis for all four views. The body trapezoid maintains the same top/bottom width ratios across front and back views. The hair cloud is correctly asymmetric in 3/4 (near side wider) and correctly extends behind the head in profile. The pocket bump is present in front, 3/4, and profile, and absent in back — which is the correct behavior.

### The Sneaker Depth — MINOR FAILURE

The sneaker in profile view (`draw_luma_side`) is an elongated oval with `fw = int(hu * 0.65)`. In the front view the sneaker half-width is derived from `fw = int(hu * 0.52)`. The profile sneaker is thus 25% larger than the front-view sneaker would imply. This is a small but measurable proportional inconsistency. At 200px character height the front sneaker half-width is approximately 30px and the profile sneaker is approximately 37px. This will read as "sneaker changes size based on angle" to anyone who measures across views — which a rigger will.

### The Back View Hair — ACCEPTABLE

The back view correctly replicates the front view hair mass and adds two additional blobs to suggest the back volume of the curls. This is a valid choice. It is not a perfect volumetric reconstruction — the back blobs are slightly arbitrary in placement — but it communicates "this is the back of a voluminous hair cloud" which is the job of the back view.

### Profile Body Depth — ACCEPTABLE

The side view body depth (`body_depth = int(hu * 0.60)`) implies Luma is roughly as deep front-to-back as she is wide shoulder-to-shoulder (approximately 34px vs approximately 43px). This is within plausible range for a rounded character. The A-line taper in profile is subtle but present.

**Grade for Luma Turnaround: B+**

Structurally sound, proportionally consistent across three of four views, properly annotated. The sneaker scale inconsistency in profile is the primary defect.

---

## SECTION 3: MIRI-B REMOVAL — CONFIRMED

This is clean. The silhouette generator explicitly documents the decision:

```python
# MIRI-A is the canonical Miri (Cycle 9 lock: bun+chopsticks+cardigan+soldering-iron).
# MIRI-B (curls+apron) is retired — no longer shown on silhouette sheet.
col_labels    = ["LUMA", "COSMO", "BYTE", "MIRI"]
neutral_drawers = [draw_luma, draw_cosmo, draw_byte, draw_miri]
action_drawers  = [draw_luma_action, draw_cosmo_action, draw_byte_action, draw_miri_action]
```

Only `draw_miri` (MIRI-A) appears in both the neutral and action rows. The `draw_miri_v2` and `draw_miri_v2_action` functions remain in the file as archived code but are not called. This is the correct approach — preserve the work, retire it from production.

The sheet title also includes the lock statement: `"MIRI: bun+chopsticks+cardigan+soldering-iron (MIRI-A — CANONICAL, locked Cycle 9)"`.

**MIRI-A canonical lock: FULLY RESOLVED. Grade: A.**

---

## SECTION 4: BYTE ACTION POSE — MATERIAL IMPROVEMENT

The Cycle 8 critique called the action pose "indicating, not acting." The Cycle 9 redesign addresses this directly and credibly.

### What Changed

`draw_byte_action()` in `silhouette_generator.py` (lines 497–599) is a complete rewrite:
- **Body diagonal**: `tilt_x = int(s * 0.30)` (30% of body width horizontal lean). The top of the body is offset 0.30s rightward relative to the bottom. At `s ≈ 38px` (20% of `LUMA_H`), this is approximately 11px of horizontal lean — meaningful and visible.
- **Right arm: forward-up thrust** — `r_ang_x = int(r_arm_len * 0.72)`, `r_ang_y = -int(r_arm_len * 0.52)`. The arm extends strongly rightward and upward. At body size, the arm tip is approximately 23px above and 23px to the right of the shoulder root. This is not "pointing" — this is reaching.
- **Left arm: trailing back-down** — opposite angle, opposite direction. The asymmetry is physically correct for a mid-leap posture and reads immediately as momentum.
- **Kicked leg**: `kick_len_x = int(s * 0.52)`, `kick_len_y = int(s * 0.62)` — the trailing leg extends approximately 20px back and 24px down. This is the strongest single element. A kicked-back leg is the clearest "leap" signal in 2D animation. It was missing from every previous Byte action pose.
- **Jump height**: `jump_h = int(s * 0.45)` — the body is elevated approximately 17px above the ground line. Combined with the scattered particle confetti below (5 particles in staggered positions), the hover trail reads as a trajectory, not a static float.

### Does It Read at Squint Distance?

Yes. At the silhouette sheet's operating scale (Byte column ~186px wide, body ~38px), a diagonal chamfered form with one arm extending upper-right, one arm trailing lower-left, and one leg kicked back lower-left reads as "in motion." The forward-thrust arm and kick leg are on opposite sides of the body, which creates a visual span that amplifies the speed read. The scattered particles below are 10×10px and visible at this scale. This passes.

### Residual Issue

The front-thrust arm (`r_arm_len = int(s * 0.80)` = approximately 30px) with its blob hand is the dominant limb. If the arm were pointing exactly rightward it would read as "indication." It does not — it angles upward at approximately 36° from horizontal (`r_ang_y / r_ang_x = 0.52 / 0.72 ≈ 0.72 → ~36°`). The upward angle converts "pointing at something" to "reaching toward something." This is the correct instinct. Correct.

**Grade for Byte Action Pose: A-**

The minus is for the body size still being 20% of Luma's height (`s = int(LUMA_H * 0.20)`) — Byte at the action pose scale is still very small relative to the panel column. The leap reads, but it reads as a very small creature leaping. This is arguably correct to the show's aesthetic. I am not calling it wrong. But the grandeur of the pose is limited by the scale of the character within his panel.

---

## SECTION 5: EXCITEMENT BACKGROUND — CONFIRMED FIXED

`luma_face_generator.py`, line 29:
```python
BG = (240, 200, 150)   # warm amber mid-tone (Cycle 9: pushed from off-white to committed warm amber)
```

This is the correct change. `(240, 200, 150)` is a clear amber mid-tone, not off-white. The code comment is accurate and appropriately documents the reason for the change. The three-panel comparison is now: warm amber / cool blue-grey / warm lavender. Three distinct color temperatures at three distinct values. Panel identification at squint distance is now unambiguous.

This item appeared on my Priority 1 list for three consecutive cycles. It is resolved. I will not mention it again.

**Excitement background: FULLY RESOLVED. Grade: A.**

---

## SECTION 6: HOVER PARTICLES IN EXPRESSION SHEET — FOURTH CONSECUTIVE FAILURE

`byte_expressions_generator.py`, lines 385–392:
```python
# Hover particle confetti (small squares below feet) — fixed at 4x4px per GL spec
for (px, py, pc) in [
    (bcx-20, bcy + body_ry + leg_h + 5,  BYTE_HL),
    (bcx+5,  bcy + body_ry + leg_h + 8,  SCAR_MAG),
    (bcx+25, bcy + body_ry + leg_h + 3,  BYTE_HL),
    (bcx-35, bcy + body_ry + leg_h + 10, (0,200,180)),
]:
    draw.rectangle([px, py, px+4, py+4], fill=pc)
```

The particles remain at 4×4px. The "GL spec" comment rationalization, which I identified and rejected in Cycle 8, is still present and unchanged. This is now the **fourth consecutive cycle** this item has appeared on my priority list.

I said in Cycle 8 that re-labeling a bug as a specification choice is worse than leaving it unfixed because it closes the correction pathway. That is exactly what has happened. Cycles 9 had specific Priority 1 language: "Remove the 'GL spec' comment rationalization. Either enlarge to 10×10px minimum or remove the particles entirely." Neither action was taken.

The contrast between this item and the Excitement background is instructive. The Excitement background change required two numbers to be modified and was on the list for three cycles. The hover particle change requires one number — `+4` becomes `+10` — and has been on the list for four cycles. The Excitement background was fixed this cycle. The hover particles were not. There is a pattern here that is not about difficulty. I will not speculate further. I will state only: the item is outstanding, it is trivial to execute, and it has not been executed.

Compare with the turnaround generator, where the hover particles are correctly drawn at 10×10px (`psz = 10`) in all four Byte views. The team demonstrably knows the correct size and uses it in new work. The expression sheet still has the 4px version. This is inconsistency within a single cycle's output.

**Hover particles in expression sheet: UNRESOLVED. Priority 0 for Cycle 10. No further extensions.**

---

## SECTION 7: OVERALL CYCLE ASSESSMENT

### What Genuinely Improved

1. **MIRI-A canonical lock** — clean, well-documented, correctly executed. No ambiguity.
2. **Excitement background** — three-cycle carry-forward item resolved with a confident number, not a timid nudge.
3. **Byte action pose** — the most substantive single redesign of this cycle. Diagonal body + asymmetric arms + kicked leg = this pose now reads as a character in motion, not a character with an opinion.
4. **Turnaround structure** — the four-view format, layout, scale annotations, label system, and depth treatment for Luma are production-quality. The tool is correct; the body shape for Byte is wrong.
5. **Style frame improvements** — couch scale, draw order, overlay fixes are significant environmental corrections that strengthen the frame's spatial coherence.

### What Remains Blocking Pitch-Readiness

Ranked by severity:

**Priority 0 — Ship Blocker:**
1. **Byte turnaround shape** — chamfered cube contradicts all other production materials. Must be corrected to oval before any external distribution. This is a one-function rewrite (`_byte_size` + four `draw_byte_*` functions: replace polygon with ellipse, update eye/mouth/limb positioning to reference `body_ry` instead of chamfer geometry, propagate float_gap).

**Priority 1 — Must Fix:**
2. **Hover particle confetti** — 4×4px to 10×10px. Remove the "GL spec" comment. This is now Priority 0 for Cycle 10 given the four-cycle carry status. If it is not resolved in Cycle 10, I will consider the team to be choosing not to fix it, and I will frame my feedback accordingly.
3. **Composite reference image** — all four characters (Luma, Cosmo, Byte, MIRI-A) at correct proportional scale with legible faces in one document. This has been on the Priority 0 list since Cycle 5. It is still absent. The pitch package cannot answer the question "What does this world look like when all four characters are in the same frame?" Five cycles. This is the single most damaging absent deliverable.

**Priority 2 — Quality Issues:**
4. **Luma profile sneaker scale** — 25% larger than front/back sneaker implied scale. Fix proportional reference before Cycle 10 if composite image requires it.
5. **Byte turnaround — no oval back design detail** — once the body is corrected to oval, a decision is needed about the center-back data port detail (present in the current chamfered-cube back view as a NEG_SPACE slot). This is a good design detail that should be preserved in the oval design.

---

## THE SINGLE MOST IMPORTANT THING BLOCKING PITCH-READINESS

The composite reference image. Not the turnaround shape — the turnaround is a one-cycle fix with known solution. The composite image has been requested since Cycle 5 and has never been produced. Every cycle the team has more complete character designs, and every cycle no document shows them all together at scale with legible faces. The pitch package has expression sheets, silhouette sheets, a style frame, storyboards, and now turnarounds. What it does not have is the fundamental document that answers the most basic pitch question: what does the show look like?

A buyer who cannot see all four characters in the same document at correct relative scale must assemble that mental image themselves from four separate sheets. They will not. They will ask. When you cannot show them immediately, you have lost a beat in the room.

The composite reference image is not technically difficult. The character generators exist. The proportional system is documented. The color palette is documented. This is a four-hour task. It has been a four-hour task for five cycles. It must be produced in Cycle 10.

---

## CYCLE 9 GRADE ASSESSMENT

**Grade: B+**

Here is the precise accounting.

The work done this cycle is good. The Miri lock, the Excitement background, the Byte action pose redesign, the storyboard Dutch tilt fixes, the couch scale correction — these are legitimate improvements to a package that is getting stronger. The team is capable of executing at an A level: the Luma turnaround demonstrates it, the Miri lock demonstrates it, the action pose redesign demonstrates it.

The grade is B+ and not A- for three reasons:

1. **The chamfered-cube turnaround.** The team knew it was wrong, logged it in the SoW, and shipped it anyway. A design team that ships a known consistency defect in the pitch package's most critical new deliverable has made a judgment call that the defect is acceptable. That judgment is incorrect, and the grade reflects it.

2. **The hover particles.** Four cycles. A one-number change. Still not done. The pattern is the problem, not the fix.

3. **The composite reference image.** Five cycles. Still absent. This is now the longest-running unresolved critical item on the project.

The A- grade from Cycle 8 recognized a breakthrough cycle. Cycle 9 is a solid improvement cycle. The grade drop from A- to B+ is not a step backward — it reflects that the new deliverables (turnaround) came in with a known defect, which is a different kind of failure than the problems of earlier cycles.

---

## PRIORITY REQUIREMENTS FOR CYCLE 10

**Priority 0 — Ship Blockers:**
1. **Byte turnaround oval correction** — `character_turnaround_generator.py` must draw Byte as an oval body in all four views. Reference `byte_expressions_generator.py` `draw_byte()` function for the correct geometry. Propagate `body_rx`/`body_ry` through all limb, eye, and mouth positioning in the four turnaround views.
2. **Composite reference image** — Luma, Cosmo, Byte (OVAL), MIRI-A at correct proportional scale in one document. All faces legible. All relative heights accurate. This is mandatory for Cycle 10.

**Priority 1 — Must Fix:**
3. **Hover particle confetti** — `byte_expressions_generator.py` line 392: change `+4` to `+10`. Remove "GL spec" comment. Document the particle size decision in the SoW with a reason. This is the final cycle this item appears at Priority 1. In Cycle 11 it will be noted as a standing team failure.

**Priority 2 — Quality:**
4. **Luma turnaround profile sneaker** — scale to be consistent with front/back view sneaker proportions.
5. **Byte turnaround back detail** — once oval body is corrected, decide whether center-back data port (NEG_SPACE slot) is carried forward into oval design. Recommend: yes. Retain it.

---

*"The turnaround is the document a rigger uses on day one of production. Shipping it wrong is not a note for later — it is the wrong first impression for everyone downstream."*

*Dmitri Volkov — Character Design Critic*
*"A pitch package with internal contradictions is not a pitch package. It is a liability."*
