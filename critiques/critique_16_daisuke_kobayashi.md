# Critique 16 — Daisuke Kobayashi, Character Design Formalist
**Date:** 2026-03-30
**Cycle:** 40
**Assets Reviewed:**
- `LTG_CHAR_luma_expressions.png` (v011, current)
- `LTG_CHAR_byte_expression_sheet.png` (v006, current)
- `LTG_CHAR_cosmo_expression_sheet.png` (current)
- `LTG_CHAR_grandma_miri_expression_sheet.png` (current)
- `LTG_CHAR_glitch_expression_sheet.png` (v003, current)
- `LTG_CHAR_lineup.png` (v007, current)
- `LTG_CHAR_luma_turnaround.png` (v004, current)
- C40 deliverable: `luma_face_curve_spec_supplement_c40.md` (CONFIDENT, SOFT_SURPRISE, DETERMINED)

**QA tools referenced:** C40 RPD baseline (Maya Santos), C39 precritique_qa v2.7.0, proportion_audit_c39, CI suite C39 report.

---

## LTG_CHAR_luma_expressions.png — v011

**Score: 44/100**

- **FAIL (silhouette — critical, persistent):** C40 RPD baseline: worst pair Panels 3↔6 = 97.9%, 9 FAIL pairs total. This is functionally unchanged from C33. Seven work cycles have passed since the silhouette problem was first documented at FAIL level. v011's only change from v010 was the right-eye squint fix (THE NOTICING lid drop). That is a face-only change. Silhouette cannot improve from a face change alone.
- **Arm vocabulary is insufficient at production scale:** The C34 brief produced new arm functions (crossed-arms, self-hug, Y-spread) that introduced real visual differences in the source code but produce sub-4px height deltas at 1× panel resolution — confirmed again in C40 RPD. Maya's own C40 RPD notes correctly diagnose this as a measurement-limit issue, but the measurement limit is a production reality. If the silhouette tool cannot distinguish the poses, a 200px thumbnail on a pitch deck cannot either.
- **Face curve spec (C40 supplement) — construction spec quality:** The CONFIDENT, SOFT_SURPRISE, and DETERMINED delta dicts are well-specified. The asymmetry preservation rationale is correct — SOFT_SURPRISE retaining right-eye lid drop at +2 is the right call; it differentiates it from ALARMED at the level of the character's "thinking eye" identity. DETERMINED's symmetric bilateral squint with level gaze is a clean disambiguation from WORRIED. These deltas are producible from the spec alone. This is good work.
- **CRITICAL HOLD: Eye width discrepancy not resolved.** The C40 face curve spec supplement cannot be integrated into any generator until the spec 56px vs generator ~100px discrepancy is resolved. This was an open C39 item carried forward. At the critique level: a spec document that references a pixel measurement that does not match the canonical generator is not a finished spec document. It is a draft. Until Alex Chen resolves this and Maya validates the corrected control points, the bezier face system cannot be built or critiqued as a finished asset.
- **THE NOTICING squint fix (v011):** The squint_top_r mechanic — overdrawing the upper portion of the right eye with a background-colored rectangle to simulate lid drop — is an acceptable production workaround for a Pillow-based system. The implementation description is clear enough for another artist to reproduce. However, this is a simulation, not construction. If any generator ever draws the head at a different background color, this overdraw will leave an artifact. The construction risk must be documented in the spec.

**Bottom line:** Seven cycles of FAIL on silhouette differentiation with no arm-vocabulary change that survives production resolution — v011 closes the face fix but the sheet's core production problem remains unaddressed, and a new spec deliverable (bezier face system) cannot be built until a numeric discrepancy is resolved.

---

## LTG_CHAR_byte_expression_sheet.png — v006

**Score: 65/100**

- **FAIL (silhouette):** C40 RPD: worst pair Panels 4↔7 = 90.2%. Three FAIL pairs. The C38 arm differentiation pass introduced real changes (ALARMED arm_x_scale 1.5→2.0, POWERED DOWN arm near-zero). Maya's C40 RPD notes confirm this is at the measurement limit for Byte's 88px oval body at 240px panel width. I accept the measurement-limit diagnosis for Byte — a small oval robot has fewer silhouette degrees of freedom than a human character.
- **UNGUARDED WARMTH body-language deficit (C14 P2 — still open):** The SOFT_GOLD confetti and star/heart pixel symbols remain the primary differentiators for UNGUARDED WARMTH. The 9px body pose delta (body_tilt=-4, arms-floating -5 dy) is not a silhouette signal — it is a color signal. The brief was: increase body-tilt and arm-float delta to register at 200px thumbnail. This has not been actioned since C14.
- **10-expression vocabulary is getting long:** At 10 expressions across a 4×3 grid, the sheet is carrying COVETOUS, HOLLOW, UNGUARDED WARMTH, and RESIGNED alongside the 6 original expressions. The interior states (COVETOUS, HOLLOW) were requested by critics for narrative reasons — correct. But the sheet is now doing two jobs: acting reference AND narrative character development. These should eventually split into a core 6-expression acting sheet and a supplementary states sheet. Not a blocking issue for this cycle, but I am flagging it now.

**Bottom line:** Byte v006 is the best-performing non-Glitch character sheet by metric, but UNGUARDED WARMTH's body-language deficit has been open since C14 and the sheet is approaching a size where it needs to split.

---

## LTG_CHAR_cosmo_expression_sheet.png — current version

**Score: 72/100**

- **PASS (silhouette — breakthrough):** C40 RPD baseline: PASS, worst pair 45.5%. This is a genuine improvement from C33's 95.9% FAIL. Cosmo v007 with the C34 brief's pose vocabulary (head-grab, wide-startle, crossed-arms, deliberate body-language differentiation) has worked. This is what happens when the brief is implemented.
- **Arms mode FAIL — noted as measurement artifact:** Arms mode FAIL is consistent with all characters at this resolution. The full-mode PASS is the primary metric.
- **Cross-sheet on-model (Cosmo):** S001 head ratio 4.0 — spec lint PASS (C39 CI). S003 glasses tilt 7° — PASS. Cosmo's taller proportion makes the 4.0 ratio relatively easy to hold across generators. No regressions detected since C14.
- **Remaining concern — glasses construction spec:** S004 frame thickness 0.06×hu is in the lint checks, but the spec document does not include a primitive-by-primitive construction diagram for the rectangular frame with rounded corners and the distinctive tilt. An animator recreating Cosmo from this spec would have to infer the frame construction geometry. This is the same category of gap I flagged at C12 P8 for Glitch.

**Bottom line:** Cosmo v007 passes the silhouette test decisively — the C34 brief worked, and this is the strongest improvement in the cast since C14; the glasses construction spec still needs a construction diagram.

---

## LTG_CHAR_grandma_miri_expression_sheet.png — v004

**Score: 58/100**

- **WARN (silhouette — improvement from C14):** C40 RPD: WARN, worst pair 84.4%, no FAIL pairs. This is a genuine improvement from C14's 96.9% FAIL. v004 (C38) with the wide-open arms for WELCOMING, hand-to-chest for NOSTALGIC, and clasped-hands for CONCERNED has moved seven pairs out of FAIL and into WARN range. The brief was actioned.
- **KNOWING STILLNESS vs WISE — by-design face-only differentiation:** The C40 RPD notes confirm these remain high-similarity pairs (WARN range). This is accepted per production brief since C33. My position: accepted, but both critics and animators should be aware that these two expressions will be indistinguishable in silhouette — context dependence is mandatory for reading them correctly. Document this explicitly in the character spec.
- **M001 head ratio (3.2) — spec lint WARN unresolved:** This has been open across multiple critique cycles. Maya's tool reports WARN because the generator does not contain an explicit canonical M001 ratio constant — the value is inferred. For a supporting character, this is tolerable. For a production that will have multiple animators on Miri, it is not. One explicit `MIRI_HEAD_RATIO = 3.2` constant in the generator closes this WARN permanently.
- **Bun and chopstick construction:** M004 is detected by the spec linter (bun/chopstick marker found). But there is still no drawn spec showing the bun construction geometry from a rear view or a 3/4 view. This is the Glitch construction spec problem applied to Miri — the design is clear in the front view and unclear in every other view.

**Bottom line:** Miri v004 is a real improvement — seven pairs moved from FAIL to WARN — but M001 is an open constant that needs one line of code, and the bun construction spec for non-front views is absent.

---

## LTG_CHAR_glitch_expression_sheet.png — v003

**Score: 76/100**

- **PASS (silhouette):** C40 RPD: PASS, worst pair 55.5%. Glitch continues to pass because body geometry IS the expression. This is the correct design philosophy.
- **COVETOUS and HOLLOW luminance floor — C14 P4 — status check:** C40 RPD: arms mode FAIL as expected (no arms). The README notes that bodypart_hierarchy_v002 can now run --panel N on individual panels. Has anyone run this on the COVETOUS and HOLLOW panels to verify they are not near-background in luminance? I see no evidence of this check in the C39/C40 QA record. This is not a tool gap — the tool exists. This is a missing QA step.
- **C12 P8 — Glitch construction spec — STILL OPEN:** Three critique cycles have passed since I first flagged the absence of a written primitive-by-primitive construction spec for Glitch's diamond body. A diamond/rhombus drawn from a rect with corner coordinates (rx=34, ry=38 per the glitch spec lint check) is a producible spec. The rx/ry values are in the lint tool source. The spec document does not contain them in a labeled diagram. This is the single most persistent open item in my review record for this production.
- **Interior expression states (YEARNING, COVETOUS, HOLLOW, REMEMBERING):** These were added across C28–C33 at critics' request and are narratively motivated. At 9 expressions in a 3×3 grid, Glitch's sheet is now the same size as Byte's 4×3. The interior states are visually distinct from the active states (the YEARNING/COVETOUS/HOLLOW low-luminance read is itself a differentiator for the state class). I accept the design.

**Bottom line:** Glitch v003 passes silhouette metrics and the design philosophy is correct, but the construction spec for the diamond body primitive is still absent after three critique cycles — this is the single item I will not stop requesting until it is done.

---

## LTG_CHAR_lineup.png — v007

**Score: 66/100**

- **Proportion alignment — improvement confirmed:** Luma at 3.2 heads, eye r×0.22 matches v011 expression sheet. C14 P3 cross-sheet alignment issue is closed for Luma. Byte oval body, Cosmo at 4.0 heads — all consistent with individual character sheets.
- **Palette audit — Byte layer legacy pixels:** The C14 palette audit flagged both canonical AND legacy Byte body values co-existing in the PNG. The C39 CI suite shows the lineup palette audit is running (tool exists and is in precritique_qa). However, the C39 precritique_qa report does not show a lineup palette audit result explicitly — it appears this check may not be in the current precritique_qa run. If the Byte legacy pixel contamination was fixed in v007, that fix needs to be confirmed with a fresh audit run. No confirming evidence in the QA record.
- **Staging — five characters in a row:** My C14 P5 observation stands. The lineup places all five characters on a flat baseline with Glitch hovering at approximately the same delta as the natural height variation between the human characters. The composition reads as an inventory, not a cast. This is a producible asset but not a pitch-grade asset. A half-step stagger or ground-plane angled staging communicates cast dynamics. This has now been open two critique cycles.
- **On-model fresh check:** Glitch body CORRUPT_AMBER dominant — the G006 organic warm fill WARNs from the lineup generator code (character_lineup.py) persist in the C39 CI report. These are flagged as false positives by the Glitch spec lint's tolerance scan, but the warm fill values (138,122,112) / (168,152,140) / (184,154,120) are in the lineup source and produce visible pixels. At lineup scale, these may be anti-aliasing artifacts on the CORRUPT_AMBER body edge. They need explicit investigation — either suppress them in the lint as confirmed anti-alias noise, or fix the source values.

**Bottom line:** Proportion alignment across the cast is finally consistent, but Byte layer legacy-pixel status is unconfirmed, flat staging persists as a production weakness, and warm-fill G006 WARNs in the lineup generator need explicit resolution.

---

## Cast Coherence Review (C16 — complete pitch)

**Progress since C14:**
- Cosmo: 95.9% FAIL → 45.5% PASS. The brief worked.
- Miri: 96.9% FAIL → 84.4% WARN. Real improvement.
- Luma: 87.7% FAIL → 97.9% FAIL. Worsened (THE NOTICING rework added face complexity without arm-vocabulary change).
- Byte: 90.2% FAIL → 90.2% FAIL. Unchanged (at measurement limit).
- Glitch: PASS → PASS. Stable.

The cast is now split: Cosmo and Glitch PASS, Miri WARN, Luma and Byte FAIL. A commissioning panel will see the gap. The machine characters and the human-adjacent supporting character outperform the two protagonists at silhouette level.

The C40 deliverable — the bezier face curve supplement for CONFIDENT, SOFT_SURPRISE, DETERMINED — is the right direction. These three expressions address story beats that are not yet covered by the six-delta base spec. The spec quality is high. But this spec cannot be built into a tool or integrated into the expression sheet until the eye width discrepancy is resolved. The most pressing character asset issue this cycle is not the expression deltas — it is the numeric mismatch that is blocking the entire bezier face system.

---

## Priority Directives

1. **(P1 — Blocking)** Resolve the bezier face spec eye-width discrepancy (spec 56px vs generator ~100px) before any work on `LTG_TOOL_luma_face_curves.py`. Alex Chen must close this; Maya validates. The face curve supplement (CONFIDENT/SOFT_SURPRISE/DETERMINED) is correctly specified in isolation but cannot be used until the baseline coordinate system is confirmed.
2. **(P1 — Blocking)** Luma silhouette: v011 is a face-only fix — it cannot move the RPD metric. The arm-vocabulary changes from C34 produce sub-4px deltas at production scale. This needs a fresh approach: either a fundamentally wider arm stance range across the 6 expressions, or an explicit production acknowledgment that Luma's expression sheet is not silhouette-differentiable at panel resolution and the production will rely on color-per-expression differentiation. One of these two decisions must be made.
3. **(P2 — Serious)** Add `MIRI_HEAD_RATIO = 3.2` as an explicit constant to the Miri expression sheet generator. This is one line of code. M001 WARN has been open multiple cycles.
4. **(P2 — Serious)** Glitch diamond body primitive construction spec: add rx=34, ry=38 in a labeled construction diagram to `glitch.md`. This is the single most persistent open item in my review record. It takes 20 minutes.
5. **(P2 — Serious)** Run bodypart_hierarchy_v002 `--panel N` on COVETOUS and HOLLOW expression panels and confirm luminance floor. The tool exists; the check has not been run.
6. **(P3 — Moderate)** Lineup staging: replace flat-baseline composition with height-stagger or half-step ground-plane staging. This communicates cast dynamics on the pitch page.
7. **(P3 — Moderate)** Lineup Byte layer: run `lineup_palette_audit` on v007 and confirm legacy pixel contamination is resolved. Add this audit to the precritique_qa run if it is not already there.
8. **(P3 — Moderate)** Document the squint_top_r background-overdraw risk explicitly in the Luma spec: if the panel background color changes, the overdraw produces an artifact. Any future generator using this technique must know this.

---

*Daisuke Kobayashi — Character Design Formalist*
*Critique 16 — 2026-03-30*
