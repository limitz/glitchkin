# Statement of Work — Cycle 36

**Date:** 2026-03-30
**Work cycles complete:** 36
**Critique cycles complete:** 14 (next at C37)

---

## Deliverables

### Style Frames
- **SF02 v008** — Fill light direction corrected (upper-right source per storm crack position), per-character silhouette mask applied (no background bleed). Sven's C14 P1 issues resolved. QA: PASS/WARN only.

### Characters
- *(No new character sheets this cycle — Cosmo v006 glasses-tilt fix queued C37)*

### Environments
- **Tech Den v004_warminjected** — warm/cool separation fixed (7.9→23.2 PASS) using new warmth inject utility.

### Tools (New)
- `LTG_TOOL_expression_silhouette_v003.py` — Regional Pose Delta (RPD) metric replaces broken IoM. Human characters now correctly assessed. Arms mode fixed.
- `LTG_TOOL_spec_sync_ci_v001.py` — CI gate for all 5 characters. C36 baseline: Cosmo P1 FAIL (glasses tilt 10° vs spec 7°±2) — all others pass.
- `LTG_TOOL_palette_warmth_lint_v004.py` — `--world-type` flag, auto-inference from filename, CHAR-L hoodie scope expansion.
- `LTG_TOOL_warmth_inject_v001.py` — Warm/cool injection utility for environments. Auto-finds alpha step to meet threshold.
- `LTG_TOOL_proportion_audit_v002.py` — Asymmetric eye detection added. C36: 2 ASYM-WARNs on SF02 sprint face (intentional).
- `ltg_warmth_guarantees.json` — New primary warmth config, replaces warmth_lint_config.json as source of truth.
- `LTG_TOOL_precritique_qa_v001.py` (v2.1.0) — Delta report (Section 0), baseline persistence, README sync prominence. C36 baseline: 321 PASS / 37 WARN / 0 FAIL.

### Policy & Documentation
- Face test gate deployed to ROLE.md files for Maya, Rin, Jordan, Lee.
- `output/production/face_test_gate_policy.md` — policy document with thresholds and scope.
- `output/production/draw_order_lint_back_pose_diagnostic_c36.md` — P3 latent risk documented.
- `output/production/proportion_audit_c36.md` — C36 proportion audit results.
- `output/production/color_qa_c36_baseline.md` — full color QA baseline.
- `output/production/precritique_qa_c36.md` — QA run results with delta.
- `output/production/pitch_package_index.md` — updated through C36.
- Rin Yamamoto ROLE.md created from scratch (was missing).

### CRITICS.md / CLAUDE.md Updates
- 5 audience critics added (Zoe Park, Marcus Okafor, Jayden Torres, Eleanor Whitfield, Taraji Coleman).
- CLAUDE.md: critic rotation rule, audience panel composition (min 1 audience critic per cycle), CLAUDE.md note on artistic integrity.

### Team Expansion
- 4 new members added (C37 start): Diego Vargas (Storyboard), Priya Shah (Story & Script), Hana Okonkwo (Environment), Ryo Hasegawa (Motion Concept).
- Active team cap raised to 12. Max simultaneous agents stays at 8 (batched). Longest tasks start first.

---

## Key Findings

- **Cosmo v005 P1 FAIL**: glasses tilt 10° vs spec 7°±2. Caught by new spec_sync_ci tool. Maya to fix in C37 (v006).
- **Jordan's fill light module hardcoded to 1280×720**: Rin had to inline the algorithm. Rin filed ideabox: make canvas_w/canvas_h params. Actioned C37.
- **IoM metric was fundamentally wrong for standing humans**: RPD fix in v003 is a proper algorithmic solution.
- **Tech Den warmth**: required cool-bottom injection (not warm-top) — top half was already in amber range.

---

## Ideabox — C36 (8 ideas, all actioned → C37)
- Morgan: glitch spec suppression list (Kai C37)
- Alex: draw order back-pose suppression (Kai C37)
- Jordan: warmth inject generator hook (Jordan C37)
- Kai: CI suite consolidation (Kai C37)
- Lee: contact sheet arc-diff tool (Lee C37)
- Maya: RPD zone visualization mode (Maya C37)
- Rin: fill light resolution adapter (Rin C37)
- Sam: world-type inference for render_qa (Kai C37)

---

## QA Baseline (C36)
- Precritique QA v2.1.0: **321 PASS / 37 WARN / 0 FAIL**
- Delta vs C35: +0 FAIL, +1 WARN (new SF02 v008 G007 — consistent with known pattern), -0 resolved
