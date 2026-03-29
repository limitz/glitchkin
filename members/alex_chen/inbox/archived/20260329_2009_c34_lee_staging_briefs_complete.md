**Date:** 2026-03-29 20:09
**To:** Alex Chen
**From:** Lee Tanaka
**Subject:** C34 Work Complete — SF02 Staging Brief + Expression Pose Brief

Both C34 deliverables are complete.

---

## Task 1 — SF02 Luma Interiority Staging Brief

**File:** `/home/wipkat/team/output/production/sf02_staging_brief_c34.md`

**Key decisions:**
- Expression type: FOCUSED DETERMINATION — a sprint-adapted version of THE NOTICING (v008). Not fear. Not heroism. The face of a kid who has made a choice.
- Eyes: asymmetric (left wider than right — Luma's visual signature), both angled forward/down. 4px pupils at sprint scale.
- Brows: left brow pulled inward (corrugator), right level — asymmetric brow is the most efficient interiority signal at this scale.
- Mouth: compressed/set jaw, not open fear oval.
- Body: forward torso lean 8–12° toward motion direction. Arm counter-rotation exaggerated.
- Hair stream: angle more sharply rearward to read as velocity.
- New sub-function `_draw_luma_face_sprint(draw, cx, head_cy, head_r)` to be extracted inside `_draw_luma()`.

**For Rin:** Please implement as `LTG_TOOL_style_frame_02_glitch_storm_v006.py` → `LTG_COLOR_styleframe_glitch_storm_v006.png`. The brief has precise pixel guidance for sprint-scale face rendering.

---

## Task 2 — Expression Pose Vocabulary Brief

**File:** `/home/wipkat/team/output/production/expression_pose_brief_c34.md`

**Covers:** Luma (v008 → v009), Cosmo (v003 → v005), Miri (v003 → v004)

**Key findings from silhouette analysis:**
- Root cause: expressions differentiated only in face, not in body shape. Glitch passes (71%) because its expressions have distinct body configurations. Human characters must apply the same principle.
- Every expression assigned a distinct silhouette hook (arm position, lean, head angle, width change). No two expressions within a sheet share the same primary hook.
- Luma: DELIGHTED (arms-up Y shape, currently unused), FRUSTRATED (one-sided arm fling — replaces adult-sulk pose), SURPRISED (backward lean + raised arms) are highest priority.
- Cosmo: AWKWARD (maximum asymmetry — jagged silhouette), WORRIED (head-grab bracket), SURPRISED (horizontal spread) are highest priority.
- Miri: WELCOMING (wide-open arms gives the sheet its full range), SURPRISED/DELIGHTED (hand-to-cheek) are highest priority.
- KNOWING STILLNESS / WISE are accepted as intentionally similar; brief provides one small gesture hook to reduce overlap.
- Brief instructs Maya to test with `LTG_TOOL_expression_silhouette_v001.py` and `LTG_TOOL_render_qa_v001.py` before submitting.

**For Maya:** Brief is in `/home/wipkat/team/output/production/expression_pose_brief_c34.md`. Actionable without further review — all pose changes specified with parameter-level guidance.

---

## Ideabox

Submitted: `/home/wipkat/team/ideabox/20260329_lee_tanaka_sprint_face_tool.md` — proposal for `LTG_TOOL_character_face_test_v001.py`, a standalone face-at-sprint-scale QA tool to prevent "invisible face" problems before they reach full generator iterations.

---

Lee Tanaka — C34 — 2026-03-29
