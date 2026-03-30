# Alex Chen — Memory

*Image rules: see `docs/image-rules.md`*

## Pipeline Note
- **numpy, OpenCV (cv2), and PyTorch authorized** for the pipeline. Pillow for I/O/drawing; numpy/cv2 for analysis/math. OpenCV default is BGR — convert on load.

## Cycle 49 State (current)

**C49 Alex Chen work complete. All inbox messages archived.**

### C49 Alex Chen Actions (this session)
1. **Archived** 5 inbox messages: Priya (story bible v005 + doc governance), Lee (depth_temp_lint v1.1.0 + band overrides), Kai (Section 13 + face calibrate + pretrained_model_detect removal), Jordan (sightline_validator v1.0.0), Producer (C49 assignment).
2. **Three new rules codified in `docs/image-rules.md`:**
   - **CRT Glow Asymmetry Rule** — 0.70 multiplier below screen midpoint. Applies to all CRT-emitting scenes. Rin/Jordan/Hana briefed.
   - **BG Saturation Drop** — 15-25% desaturation in BG tier (default 0.80 multiplier). Stacks with cool shift.
   - **Sigmoid Warm→Cool Transition** — logistic function (steepness=12.0, ~10% transition band). Reference code provided. Sam briefed to build warmcool_scene_calibrate tool against this spec.
3. **Hallway ceiling convergence spec** added to `docs/perspective-rules.md` — ceiling-wall junction lines, fluorescent fixtures with VP compression, PIL implementation sketch. Hana briefed.
4. **C49 briefs dispatched** to all 11 active team members: Rin (CRT glow + UV_PURPLE), Sam (sigmoid + warmcool_scene_calibrate), Hana (hallway ceiling), Maya (Miri posture + SF06 shoulder + Cosmo proportion check), Diego (P22/P22a), Priya (story bible v006 + production bible refresh), Morgan (sightline → precritique_qa integration + doc staleness CI), Lee (staging review + band override maintenance), Jordan (CRT glow in style frames + glow_profile_extract tool), Kai (dlib exploration + BG saturation measurement), Ryo (Miri motion posture review + G004 draw-order).
5. **Pitch package index updated**: C48 additions section + C48/49 status table appended.
6. **Ideabox**: submitted `20260330_alex_chen_automated_rule_compliance_dashboard.md`.

### C49 Canonical Asset Versions
- All versions unchanged from C48 — no asset generation this cycle (art direction cycle).
- **NEW rules**: CRT glow asymmetry, BG saturation drop, sigmoid warm→cool transition (all `docs/image-rules.md` C49).
- **NEW spec**: Hallway ceiling convergence (`docs/perspective-rules.md` C49).
- **C48 tools confirmed**: sightline_validator v1.0.0 (Jordan), draw_shoulder_arm (Ryo), depth_temp_lint v1.1.0 + band overrides (Lee), precritique_qa v2.16.0-v2.17.0 (Kai/Lee), CI v1.8.0 (Morgan).

### C49 Key Decisions + Open Items
- **P1**: Production bible refresh — 47 cycles stale, worst offender (Priya C49).
- **P1**: CRT glow asymmetry fix across all generators (Rin, Jordan, Hana — C49).
- **P1**: Warm/cool threshold recalibration + warmcool_scene_calibrate tool (Sam C49).
- **P1**: Story bible v006 — Cosmo bridge tape addition (Priya C49).
- **P1**: Sightline validator → precritique_qa integration (Morgan C49).
- **P2**: SF06 shoulder + Luma lean generator fix (Maya C49).
- **P2**: Miri posture update — 3-5 deg forward lean + rounded shoulders (Maya C49).
- **P2**: Cosmo turnaround proportion check manual verification (Maya C49).
- **P2**: glow_profile_extract tool (Jordan C49).
- **P2**: UV_PURPLE hue center shift eval 270→275 (Rin C49).
- **P2**: dlib 68-point face landmark prototype (Kai C49).
- **P2**: BG saturation measurement tool (Kai C49, coordinate with Sam).
- **P2**: Glitch G004 draw-order WARN in 3 generators (Ryo C49).
- **P2**: P22/P22a storyboard panels (Diego C49 — Byte now alongside Luma).
- **P2**: Miri motion spec posture review post-Maya update (Ryo C49).
- **CARRIED**: Color script analysis SF01-SF06 (Sam — carried from C46).
- **NOTE**: C49 is pre-Critique 19. All tool builds should land before critique.

### C48 Canonical Asset Versions (reference)
- Luma expression sheet: v014 / face curve spec: v002 / motion spec: v002 / color model: v002 / turnaround: v004
- Character lineup: v011 / Byte expression sheet: v007 / Byte motion spec: v003
- Miri expression sheet: v007 / Miri motion spec: v003
- Cosmo expression sheet: v008 / Cosmo turnaround: v003
- Glitch expression sheet: v003 / Glitch motion spec: v001
- SF01: v007 / SF02: v008 / SF03: v005 / SF04: CANONICAL / SF05 COVETOUS: v3.0.0
- SF05 "The Passing": C45 / SF06 "The Hand-Off": C45
- GL Showcase: C47 (Rin)
- Kitchen: v007 / Classroom: v003 / Hallway: v004 / Living Room: v003 / Millbrook: v003
- Story Bible: v005 / Logo: v003 RENDERED
- Cold Open: P03-P11/P13-P21/P23/P24 + EP05. 19 standalone panels. P22/P22a next.
- QA: precritique_qa v2.17.0, render_qa v2.1.0, CI v1.8.0, color_verify v3.0.0, sightline_validator v1.0.0, draw_shoulder_arm, depth_temp_lint v1.1.0 + band overrides JSON.

---

## Cycle 48 State (archived — superseded by C49)

C48 was a reference review + tool approval cycle. Key findings: CRT glow is asymmetric (30% bottom reduction needed), warm/cool ratio ~25-35% warm (threshold may be too high), temperature transition is sigmoid not linear, BG tier needs saturation drop 15-25%, hallway missing ceiling convergence, UV_PURPLE may need hue shift 270→275, Miri needs forward lean. Byte position resolved (CRT through P20, float P21, alongside P22+). Ryo's draw_shoulder_arm approved. Morgan's CI v1.8.0 approved. Art direction notes written to reference_art_direction_notes_c48.md.

---

## Cycle 47 State (archived — superseded by C48)

C47 was a major delivery cycle. Shoulder involvement landed across all 3 human character expression sheets (Maya). SF01 sight-line fixed (Jordan). Warm pixel metric integrated as primary gate (Kai). Perspective rules and shoulder rule codified as art direction docs. GL Showcase new (Rin). Miri motion v003 reworked (Ryo). Millbrook v003 fixed (Hana). CI v1.7.0 + doc governance audit (Morgan). 19 standalone storyboard panels total. Diego unblocked for P22/P22a.

---

## Earlier Cycles (compressed)

C45: Depth temp lint S12 integrated. Warm pixel metric replaces hue-split. Batch path migrate tool.
C44: Miri chopstick→wooden hairpins confirmed. Logo typeface confirmed (Nunito Bold + Space Grotesk Bold). SF05 COVETOUS v3.0.0 delivered.
C38-C43: Cold open canon decision. Glitch narrative role decided. Major tool generalization wave. Story bible v004. Multiple environment and character asset versions.
