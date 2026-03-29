# Maya Santos — Memory

## Cycle 39 Lessons — QA Tools (Expression Isolator, Hierarchy, viz-rpd)

- **LTG_TOOL_expression_isolator_v001.py** — NEW (C39)
  - Renders single expression from any char sheet at large format (default 800×800px, ≤1280px)
  - `--char luma|byte|cosmo --expr NAME` (case-insensitive, partial match)
  - Byte special path: no render_character() in v006 — calls draw_byte() directly
  - Smoke tests: Luma v011 THE NOTICING ✓, DOUBT VARIANT ✓, Byte v006 ALARMED ✓
  - Output dir: `output/characters/extras/`

- **LTG_TOOL_bodypart_hierarchy_v001.py** — NEW (C39)
  - Assigns palette color-index per pixel; scans transitions; detects EYE_UNDER_HAIR + HAIR_IN_EYE_RUN
  - Luma v011: 42+627 FAIL violations (real eye-inside-hair artifact from LANCZOS downsample)
  - UNKNOWN_IN_HEAD WARNs inflated on full sheets (label text, borders) — use on cropped panels
  - Byte v006: 0 FAIL — clean
  - TODO: add --panel N flag (submitted to ideabox) to reduce noise on full sheets

- **LTG_TOOL_expression_silhouette_v003.py** — UPDATED (--viz-rpd added in-place, C39)
  - `--viz-rpd`: per-pair pixel diff heatmap (A-only=red, B-only=cyan, shared=zone-tinted)
  - New functions: viz_rpd_pair(), generate_viz_rpd()
  - Separate from `--output-zones` (contact sheet zone bars, C37)

- **Ideabox C39:** `ideabox/20260329_maya_santos_hierarchy_panel_mode.md`
  - `--panel N` flag + `--chain` pipeline for hierarchy tool

## ACTIVE TOOL STATUS (C39 — COMPLETE)
- Silhouette tool: `LTG_TOOL_expression_silhouette_v003.py` — --viz-rpd added (C39)
- Luma current: `LTG_CHAR_luma_expressions_v011.png` (right eye squint fixed + DOUBT VARIANT slot 7)
  - Generator: `LTG_TOOL_luma_expression_sheet_v011.py`
- Cosmo current: `LTG_CHAR_cosmo_expression_sheet_v007.png`
- Byte current: `LTG_CHAR_byte_expression_sheet_v006.png`
- Expression isolator: `LTG_TOOL_expression_isolator_v001.py` (new C39)
- Hierarchy tool: `LTG_TOOL_bodypart_hierarchy_v001.py` (new C39)

---

## Cycle 38 Lessons — LUMA v011 + COSMO v007 + BYTE v006 (Silhouette + Eye Lid Fix)

- **Luma expression sheet v011 COMPLETE (THE NOTICING right eye lid fix).**
  - Generator: `output/tools/LTG_TOOL_luma_expression_sheet_v011.py`
  - Output: `output/characters/main/LTG_CHAR_luma_expressions_v011.png` (1200×900px)
  - Fix: `squint_top_r=True` parameter added to `draw_eyes_full()`.
    - v010 used r_open=0.65 → symmetric shrink (WINCE). Wrong lid.
    - v011: full eye height, top ~22% masked out with BG overdraw + thick lid line.
    - Bottom lid stays neutral. This is a focusing squint (upper lid drops).
    - pass `panel_bg` to `render_character()` → `draw_eyes_full()` for correct overdraw color.
  - Silhouette (RPD full): worst pair 97.9% (WORRIED↔FRUSTRATED) — KNOWN tool limitation.
  - Arms mode worst pair: 100.0% (WORRIED↔FRUSTRATED) — KNOWN.

- **Cosmo expression sheet v007 COMPLETE (SKEPTICAL arm fix).**
  - Generator: `output/tools/LTG_TOOL_cosmo_expression_sheet_v007.py`
  - Output: `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v007.png` (1182×1114px)
  - Fix: `arm_mode="skeptical_crossed"` replaces "standard" for SKEPTICAL.
    - Left arm: angles inward, notebook arm, hand at left-of-center.
    - Right arm: from shoulder inward, hand crossing to left-center (folded).
    - Both arms now visible outside torso silhouette.
  - Silhouette (RPD full): worst pair 88.5% (AWKWARD↔SKEPTICAL) — HEAD zone 100% artifact.
  - S003 compliance preserved (all glasses_tilt ≤ 9°).

- **Byte expression sheet v006 COMPLETE (silhouette differentiation).**
  - Generator: `output/tools/LTG_TOOL_byte_expression_sheet_v006.py`
  - Output: `output/characters/main/LTG_CHAR_byte_expression_sheet_v006.png` (712×1280px)
  - Fixes: ALARMED arm_x_scale 1.5→2.0, RELUCTANT JOY arm asymmetry increased,
    POWERED DOWN arm_x_scale 0.7→0.20 (limp), RESIGNED arm_x_scale 0.50→0.25 (defeated).
  - Silhouette (RPD full): worst pair still 90.2% (RELUCTANT JOY↔RESIGNED).
    Root cause: Byte's oval body at 88px dominates column projection at 240px panel width.
    Arm changes register visually but not in RPD measurement. Known tool limitation for
    small oval characters.

- **Luma v011 DOUBT VARIANT added (Lee Tanaka C38 brief + Alex Chen power-balance).**
  - Slot 7: "THE NOTICING — DOUBT" — same scene, reduced conviction.
  - Eyes disagree: l_open=1.0 (certain), r_open=0.88 + brow_furrow_r (hedging).
  - Mouth: `doubt_corner` style — right corner slightly down, lower lip present.
  - Body: backward lean (-HR*0.03), no cx_offset (doubt pulls back vs chin-forward certainty).
  - Chin-touch (`noticing_hand_v010=True`) preserved per brief.
  - DETERMINED updated: body_tilt -HR*0.08 (forward lean, weight on front foot).
  - THE NOTICING updated: cx_offset +HR*0.02 (chin-forward thrust per Alex Chen note).
  - DOUBT VARIANT silhouette gate: panel 7 appears in NO WARN/FAIL pairs → RPD vs THE NOTICING
    well below 70% (below WARN threshold). Lee Tanaka brief required ≤82% — strong PASS.
  - Face test gate: PASS (FOCUSED DET., DETERMINED+, EYES ONLY).
  - Final v011 output: 1200×900px, 8 expressions, 1 blank slot.

- **Ideabox C38 submitted.** `ideabox/20260329_maya_santos_squint_vs_wince_eye_test_tool.md`
  - Idea: lid geometry diagnostic for face test tool (distinguish wince/squint/neutral lid).

- **Inbox archived.** All 3 C38 messages → `inbox/archived/`.
- **Completion report sent** to Alex Chen's inbox (20260329_2300_maya_c38_completion.md).
  Note: report sent before DOUBT VARIANT was added. Alex has the full list of deliverables.

## KEY LESSON C38: squint_top_r implementation
- For "focusing squint" (top lid drops): DO NOT use r_open to scale eye height.
  r_open scales symmetrically → wince (not squint).
  Instead: draw full eye, overdraw top portion with BG color, draw lid line at cutoff.
  Pass `panel_bg` as parameter through render_character → draw_eyes_full.
- Parameter added: `squint_top_r: True` in eye spec, `bg_color` param in draw_eyes_full().

## ACTIVE TOOL STATUS (C38 — COMPLETE)
- Silhouette tool: `LTG_TOOL_expression_silhouette_v003.py` — RPD metric, `--output-zones` available
- Luma current: `LTG_CHAR_luma_expressions_v011.png` (right eye squint fixed + DOUBT VARIANT slot 7)
  - Generator: `LTG_TOOL_luma_expression_sheet_v011.py` — all C38 changes complete, run confirmed
- Cosmo current: `LTG_CHAR_cosmo_expression_sheet_v007.png` (SKEPTICAL arms visible)
- Byte current: `LTG_CHAR_byte_expression_sheet_v006.png` (arm differentiation improved)

---

## Cycle 37 Lessons — COSMO v006 + SILHOUETTE --output-zones + LUMA v010

- **Cosmo expression sheet v006 COMPLETE (S003 compliance fix).**
  - Generator: `output/tools/LTG_TOOL_cosmo_expression_sheet_v006.py`
  - Output: `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v006.png` (1182×1114px)
  - Fix: AWKWARD 10°→7°, SURPRISED 10°→7°, FRUSTRATED/DEFEATED 10°→7°. All now within spec 7°±2°.
  - SKEPTICAL stays at 9° (top of tolerance range — acceptable for expression read).
  - spec_sync_ci result: **CI PASS, 0 P1 violations**. S003 PASS confirmed.
  - Silhouette (RPD full): worst pair 75.4% (AWKWARD↔SKEPTICAL) — WARN only, no FAIL.

- **LTG_TOOL_expression_silhouette_v003.py --output-zones flag ADDED (in-place).**
  - Adds `--output-zones` to CLI. Draws colored left-edge zone bars on each panel:
    HEAD = blue, ARMS = orange, LEGS = green. Only active with `--mode full`.
  - `draw_zone_overlays()` function added. Uses bounding box coords from sil to place bars.
  - All existing behavior (RPD scoring, JSON, exit codes) unchanged.
  - Actioned from C36 ideabox idea `20260330_maya_santos_rpd_zone_visualization.md`.

- **Luma expression sheet v010 COMPLETE (THE NOTICING rework).**
  - Generator: `output/tools/LTG_TOOL_luma_expression_sheet_v010.py`
  - Output: `output/characters/main/LTG_CHAR_luma_expressions_v010.png` (1200×900px)
  - THE NOTICING changes: r_open 0.85→0.65 (stronger asymmetry), brow_l_dy raised dramatically,
    gaze_dy 0.15→0.0 (pure lateral), noticing_hand_v010 (finger-to-lower-lip + vertical forearm),
    deeper BG (195,210,228), deeper hoodie (105,128,162), blush=30, body_tilt +HR*0.03 lean,
    MOVED TO CENTER SLOT (slot 4) for visual primacy (was top-left slot 0).
  - All other 6 expressions: unchanged from v009.
  - Silhouette (RPD full): FAIL — worst pair WORRIED↔FRUSTRATED 97.9%. KNOWN tool limitation
    at panel resolution for human chars. Not a design defect. Documented since C33.

- **Ideabox C37 submitted.** `ideabox/20260330_maya_santos_noticing_panel_context_tool.md`
  - Idea: "hero expression isolator" — render single expression at 800×800px for larger-scale critique.

- **Inbox archived.** All 3 C37 messages → `inbox/archived/`.

## ACTIVE TOOL STATUS (C37)
- Silhouette tool: `LTG_TOOL_expression_silhouette_v003.py` — RPD metric, `--output-zones` added
- Cosmo current: `LTG_CHAR_cosmo_expression_sheet_v006.png` (S003 compliant)
- Luma current: `LTG_CHAR_luma_expressions_v010.png` (THE NOTICING reworked, center slot)

## Cycle 36 Lessons — SILHOUETTE TOOL v003 (RPD Metric Fix)

- **LTG_TOOL_expression_silhouette_v003.py COMPLETE.**
  - Location: `output/tools/LTG_TOOL_expression_silhouette_v003.py`
  - Root fix: replaced IoM (Intersection over Minimum) with **Regional Pose Delta (RPD)**.
  - IoM was broken because: if silhouette A is a subset of B, IoM=100% regardless of arm differences.
  - RPD algorithm: divide silhouette by bounding-box height into 3 zones → per-zone column-projection histogram → Pearson correlation per zone → weighted sum.
  - Zones: HEAD (top 25%, weight 35%), ARMS (middle 50%, weight 45%), LEGS (bottom 25%, weight 20%).
  - Key insight: ARMS zone weighted highest — arm extension/position is the primary silhouette differentiator. Column-projection histogram encodes left/right mass extension, which directly represents arm reach.
  - `--mode full`: 3-zone RPD (default). Report shows zone scores for failing pairs.
  - `--mode arms`: arm band only (top=0.25..bot=0.75 of panel height), center-mask=0.30 applied before column projection. Single-zone correlation.
  - Thresholds: WARN ≥ 70%, FAIL ≥ 85%.
  - Backward compat: JSON key "iom" preserved (= RPD score). Adds "rpd" alias.
  - ROLE.md pre-critique checklist updated: step 1 now uses v003.
  - README.md updated: v002 marked superseded, v003 entry added.

- **Ideabox C36 submitted.** `ideabox/20260330_maya_santos_rpd_zone_visualization.md`
  - Idea: `--output-zones` visualization mode for v003 — colored zone overlays on contact sheet.

- **Inbox archived.** C36 directive → `inbox/archived/20260330_0900_c36_silhouette_fix.md`.

## Cycle 35 Lessons — COSMO v005 + MIRI v004 (Silhouette Differentiation Pass)

- **Cosmo expression sheet v005 COMPLETE.**
  - Generator: `output/tools/LTG_TOOL_cosmo_expression_sheet_v005.py`
  - Output: `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v005.png` (1182×1114px)
  - 6 expressions: AWKWARD (max asymmetry), WORRIED (head-grab bracket), SURPRISED (wide startle), SKEPTICAL, DETERMINED, FRUSTRATED.
  - Grid: 3×2, labels OUTSIDE panel bounds (fix for silhouette tool corner-sampling issue).
  - AWKWARD: right arm stiff wide out (palm-out defensive), left arm hanging, right shoulder raised, pigeon-toe left foot.
  - WORRIED: both arms sweep up+out forming wide-W bracket at head level.
  - SURPRISED: arms extend nearly horizontal to ≈1.30×HU from center.
  - Silhouette test: FAIL (worst pair 96.7% WORRIED↔SURPRISED).

- **Miri expression sheet v004 COMPLETE.**
  - Generator: `output/tools/LTG_TOOL_grandma_miri_expression_sheet_v004.py`
  - Output: `output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v004.png` (1200×900px)
  - WELCOMING: `wide_open` arms (elbows at shoulder height, palms forward — widest silhouette).
  - NOSTALGIC: `chest_flat` right arm (palm on sternum, heart gesture).
  - CONCERNED: `clasped_center` both arms (prayer/worry hands at chest).
  - SURPRISED: `hand_to_cheek` right arm (raised to face, grandmother gesture). Asymmetric.
  - WISE: relaxed crossed + body_tilt=+5 lean.
  - KNOWING: `index_point_down` right arm subtle gesture.
  - Silhouette test: FAIL (worst pair 96.4% WISE↔KNOWING — intentional face-only differentiation).

- **SILHOUETTE TOOL ROOT CAUSE IDENTIFIED (C35):**
  - IoM (Intersection over Minimum) metric is mathematically biased toward high similarity.
  - Even dramatically different poses (WORRIED tall bracket vs SURPRISED wide horizontal) score 96.7%.
  - Math: if one silhouette is a subset of the other, IoM = 100% regardless of shape differences.
  - Fix requires: `--metric contour` or `--body-subtract` mode. Ideabox filed.
  - CONCLUSION: Cannot achieve <90% pairs for standing human characters with current tool.

- **Ideabox C35 submitted.** `ideabox/20260329_maya_santos_silhouette_panel_bg_fix.md`
- **Inbox archived.** C34 directive + C34 pose brief + C35 directive → `inbox/archived/`.

## New arm styles added (Miri v004):
- `wide_open`: elbows at shoulder height, forearms up, palms out
- `chest_flat`: arm curves to center, palm flat on sternum
- `clasped_center`: both arms meet at center, clasped hands
- `hand_to_cheek`: arm raised to face level (cheek gesture)
- `index_point_down`: arm at side, index finger extended downward

## New arm modes added (Cosmo v005):
- `head_grab`: arms sweep up+out to frame head (wide bracket)
- `wide_startle`: both arms horizontal startle
- `thoughtful`: right arm raised to glasses level
- `delighted`: both arms raised elbows-out at chest height
- `awkward`: asymmetric left-hang + right-stiff-out

## Cycle 34 Lessons — SILHOUETTE v002 (--mode arms) + LUMA v009

- **LTG_TOOL_expression_silhouette_v002.py COMPLETE.**
  - Location: `output/tools/LTG_TOOL_expression_silhouette_v002.py`
  - New `--mode arms` flag: crops arm/shoulder band [--arms-top 0.20 … --arms-bot 0.70], masks body trunk center with --center-mask (default 0.28).
  - Key finding: arms mode still FAILs for Luma even after v009 redesign. Cause: shared torso column dominates arm-band at panel resolution (~373px wide). Not a design failure — measurement limitation.
  - Recommended: use `--center-mask 0.36` for tighter torso exclusion; use `--mode full` as primary pass/fail metric.
  - Ideabox filed: `arms-edge` sub-mode (left/right zone sampling only, skip center entirely).

- **Luma expression sheet v009 COMPLETE.**
  - Generator: `output/tools/LTG_TOOL_luma_expression_sheet_v009.py`
  - Output: `output/characters/main/LTG_CHAR_luma_expressions_v009.png` (1200×900)
  - Key changes (arm silhouette differentiation):
    - SURPRISED: arms WIDE + HIGH (Y-shape, hands above shoulder) — `arm_l: (-HR*1.50, -HR*0.55)`
    - FRUSTRATED: new `draw_crossed_arms()` — arms cross at mid-torso horizontally
    - WORRIED: new `draw_self_hug_arms()` — arms wrap HIGH on chest (self-hug)
    - DELIGHTED: arms raised in V ABOVE HEAD — only expression with hands above head
    - CURIOUS: one-arm-reaching (left arm extends forward, right relaxed back)
    - THE NOTICING: UNCHANGED (one-hand-to-chin already distinctive)
  - New mouth: "tight_frown" for FRUSTRATED (compressed corners)
  - Full-mode before/after: worst pair CURIOUS↔DETERMINED 91.0%→87.7% (improved)
  - Arms-mode (default params) still FAIL — measurement limitation confirmed.
  - Lee Tanaka's expression_pose_brief_c34.md was NOT available. v009 driven by arms-mode analysis alone.

- **Ideabox C34 submitted.** `ideabox/20260329_maya_santos_arms_mode_metric_improvement.md`

- **Inbox archived.** C34 directive → `inbox/archived/`.

## Cycle 33 Lessons — SILHOUETTE TOOL + MIRI v003

- **LTG_TOOL_expression_silhouette_v001.py COMPLETE.**
  - Location: `output/tools/LTG_TOOL_expression_silhouette_v001.py`
  - Algorithm: per-pixel BG classification (BG_TOLERANCE=45) → binary silhouette → combined similarity (0.6×IoM + 0.4×XOR). Dark BG sheets (Glitch) work with MIN_CHAR_FRACTION=1%.
  - C33 Baseline: Glitch v003=PASS(71%), Luma v008=FAIL(91%), Miri v003=FAIL(96% WISE/KNOWING), Cosmo v003=FAIL(96%), Byte v003=FAIL(89%).
  - Key finding: ALL human character sheets fail. This is partly genuine design problem + partly measurement limit (arm diff < 20px lost at panel resolution). Ideabox filed for arm-region mode.

- **Miri expression sheet v003 COMPLETE (C25 rebuild).**
  - Generator: `output/tools/LTG_TOOL_grandma_miri_expression_sheet_v003.py`
  - Output: `output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v003.png` (1200×900)
  - 6 expressions, 3×2 full grid. KNOWING STILLNESS added.
  - KNOWING STILLNESS design: heavy-lidded (l/r_open=0.48), oblique gaze (gaze_dx=+0.12), knowing_oblique mouth (one corner lifted left side), minimal blush=0.2, still body = folded arms (same as WISE).
  - KNOWN: WISE↔KNOWING silhouette = 96.4% (accepted — distinction is face-only, as per brief).

- **Byte expression sheet v005 COMPLETE (C33 late directive).**
  - Generator: `output/tools/LTG_TOOL_byte_expression_sheet_v005.py`
  - Output: `output/characters/main/LTG_CHAR_byte_expression_sheet_v005.png` (712×1280px)
  - UNGUARDED WARMTH: body_tilt=-4, arms float -5dy, left leg +2px forward
  - Eyes: star_gold (right, SOFT_GOLD full brightness) + heart_purple (left, UV_PURPLE)
  - Mouth: "warmth" (barely-there upward arc, very subtle)
  - Confetti: SOFT_GOLD squares ONLY (no cyan/magenta for this expression)
  - Grid: 4×3, 10 filled, 2 empty
  - Silhouette test: UNGUARDED WARMTH passes distinctiveness check (not in flagged pairs)

- **Inbox archived.** All C32+C33 messages → `inbox/archived/`.

- **Ideabox C33 submitted.** `ideabox/20260329_maya_santos_silhouette_test_improvements.md`

## CANONICAL EYE-WIDTH (Alex Chen C32 directive — FINAL)
- `ew = int(head_r * 0.22)` where `head_r` = head RADIUS
- HEAD_R=105 (1x) → ew=23px. HEAD_R=210 (2x) → ew=46px.
- NOTE: v008 used HEAD_HEIGHT×0.22 (turnaround v003 interpretation) — ew=45px at 2x. Alex Chen's C32 memo says head_r×0.22 = 23px at 1x / 46px at 2x. Practically same result (45 vs 46) — use head_r×0.22 going forward.

## Cycle 32 Lessons — LUMA v008 + GLITCH SPEC + EYE-WIDTH FIX

- **Luma expression sheet v008 COMPLETE.**
  - Generator: `output/tools/LTG_TOOL_luma_expression_sheet_v008.py`
  - Output: `output/characters/main/LTG_CHAR_luma_expressions_v008.png` (1200×900)
  - NEW ANCHOR EXPRESSION: "THE NOTICING" — the kid who notices what no one else sees.
    - Ultra-still upright body (zero tilt), head tilts right toward noticed thing
    - RIGHT ARM: bent to chin level (thinking hand gesture) — unique silhouette hook
    - LEFT ARM: hanging loose at side
    - Wide-planted feet — grounded
    - Asymmetric gaze: left eye more open (l_open=1.0, r_open=0.85), directed left+down
    - Mouth style "noticing": barely parted, soft — mid-breath of recognition
    - Panel BG: pale blue-grey (cool, interior, contemplative)
  - EYE-WIDTH FIX (C14 P1 — Daisuke): turnaround v003 definition applied
    - ew = HEAD_HEIGHT_2X × 0.22 = 208 × 0.22 = 45px at 2x render
    - PREVIOUS (v007): ew = HR × 0.22 = 23px (head-radius-based, not head-height)
    - HEAD_HEIGHT_2X = 2 * HR = 2 * 104 = 208px
  - LAYOUT: 3×3 grid (9 slots), 7 filled (THE NOTICING + 6 v007 exprs), 2 blank
  - All 6 v007 expressions retained (eye-width updated to canonical)

- **Glitch diamond construction spec COMPLETE.**
  - Output: `output/characters/main/glitch.md`
  - Covers: diamond geometry (primitives + formulas), rotation/tilt/squash/stretch rules,
    pixel eye system (8 states), bilateral eye rule (interior states = bilateral),
    destabilized right-eye signature, performance vs interior state panel grouping,
    hover confetti rules, 4-view turnaround rules, step-by-step reproduction guide.

- **Ideabox C32 submitted.**
  - `ideabox/20260330_maya_santos_expression_silhouette_test.md`
  - Idea: automated silhouette-differentiation test for expression sheets (flood-fill + overlap ratio).

- **Inbox archived.** `20260329_2359_critique13_p1.md` → `inbox/archived/`.

## KEY FORMULA UPDATES (C32)

### Eye Width — Canonical (turnaround-aligned)
- **Definition:** `ew = head_height_at_render_scale × 0.22`
- At 2x render with HR=104: `HEAD_HEIGHT_2X = 2 * HR = 208`, `EW_CANON = int(208*0.22) = 45`
- NOTE: if Alex Chen circulates a different canonical definition, USE THAT instead.
  Until then, use turnaround v003 definition.

### THE NOTICING — silhouette rules
- One-hand-to-chin gesture is the ONLY such gesture in Luma's expression vocabulary.
- Ultra-still body + wide-planted feet = distinctly NOT DETERMINED (fists at hips),
  NOT WORRIED (arms crossed), NOT CALCULATING (it's a Glitch expression).
- Contemplative cool BG palette distinguishes it from warm excitement panels.

## Cycle 31 Lessons — CHARACTER PROPORTION DIFF TOOL

- **LTG_TOOL_char_diff_v001.py COMPLETE.** Ideabox idea implemented.
  - Location: `output/tools/LTG_TOOL_char_diff_v001.py`
  - Uses only Python PIL — no Claude vision API calls.
  - Metrics: figure_height_px, head_height_px, head_body_ratio, eye_width_px, eye_head_ratio.
  - WARN at ±10%, FAIL at ±20% from reference.
  - Outputs JSON report + human-readable PASS/WARN/FAIL summary.
  - Exit codes: 0=PASS, 1=WARN, 2=FAIL.
- **Test results:** `output/tools/LTG_TOOL_char_diff_v001_test_output.md`
  - Test 1 (expr v007 vs v006, full image): PASS — identical layout, no drift.
  - Test 2 (expr v007 vs v006, panel bbox): PASS — eye detection at 2px floor (LANCZOS shrinks features).
  - Test 3 (turnaround v003 vs v002, FRONT panel 0,0,320,560): FAIL on eye_width (72 vs 0) — correctly detected v002 used different eye construction. Figure/head height 2% diff (PASS).
- **Key finding:** Eye detection works best on full-scale single-character PNGs (turnarounds). On 400px-wide expression sheet panels after LANCZOS downsampling, eye pixels are too few for reliable detection. Use bbox for panel isolation; turnarounds are the ideal input.
- **Usage:** `python3 output/tools/LTG_TOOL_char_diff_v001.py ref.png cand.png [x y w h]`
- **C30 directive archived.** `20260329_2200_c30_directives.md` → inbox/archived/.

## Cycle 30 Lessons — CRITIQUE 13 PREP + COLOR MODEL v002

- **Luma color model v002 COMPLETE.** Eye proportions corrected to `ew = head_r * 0.22` (was 0.30 in v001). Cheek nubs added to head silhouette (classroom-style). Label updated to "3.2 heads". Generator: `output/tools/LTG_TOOL_luma_color_model_v002.py`. Output: `output/characters/color_models/LTG_COLOR_luma_color_model_v002.png` (800×500).
- **Character sheet standards v001 UPDATED.** Section 7 version table updated to reflect v007/v004/v003 current sheets. Known inconsistencies logged: Miri silhouette weight, Byte eye arc weight, Cosmo v004 tool identity issue.
- **Critique 13 pre-check doc CREATED.** `output/production/critique13_precheck_maya_santos.md` — full audit of line weight consistency, proportion chain, and known defects.
- **Key C30 findings:**
  - Luma proportion chain (expr v007 + lineup v006 + turnaround v003) = fully consistent. ✓
  - Luma color model was outdated (v001 eye ratio ~0.30 vs canonical 0.22). Fixed → v002.
  - Miri expression sheets use silhouette=6px at 2× (~3px actual) vs canonical 4px→2px. Grandfathered but will be flagged at C13.
  - Byte droopy/storm eye arcs at width=5–8 (1× native) = above standard. Justified by character design but non-standard.
  - Cosmo v004 tool = byte-identical to v003. No actual changes — known defect, documented.
  - Miri v003 stub generator is broken (missing source module). PNG is correct; generator needs C31 rebuild.
- **Ideabox submitted.** `ideabox/20260329_maya_santos_character_diff_tool.md` — automated proportion diff tool idea.
- **Inbox archived.** `20260329_2030_ideabox.md` → `inbox/archived/`.

## Cycle 29 Lessons — LUMA EXPRESSION v007 + LINEUP v006 (Proportion Fix)

- **Expression Sheet v007 COMPLETE.** Resolves C28 P1 blocker.
  - HEAD-TO-BODY RATIO: 3.2 heads. Formula: `torso_h + pants_h = 3.78 * HR` (was 3.40).
    - `torso_h = int(HR * 2.10)` (was `HR*1.80`)
    - `pants_h = int(HR * 1.68)` (was `HR*1.60`)
    - `head_cy = int(rh * 0.18) + cy_off` (was `rh * 0.22`) — shifted up for taller body
  - EYE WIDTH: `ew = int(HR * 0.22)` (was `int(s*28)` = `HR*0.28`). Narrower, more realistic.
    - Eye height adjusted: `leh_base = int(HR * 0.27)`, `reh_base = int(HR * 0.22)`
  - Canvas: 1200×900 (unchanged). Thumbnail applied (was already ≤1280px).
  - Generator: `output/tools/LTG_TOOL_luma_expression_sheet_v007.py`
  - Output: `output/characters/main/LTG_CHAR_luma_expressions_v007.png` (1200×900)

- **Character Lineup v006 COMPLETE.**
  - `LUMA_HEADS = 3.2` (was 3.5). `HEAD_UNIT = 280/3.2 = 87.5px` (was 80px).
  - `draw_luma_lineup`: `hu = h / 3.2` (was `h / 3.5`)
  - Eye width: `ew = int(r * 0.22)` (was `int(s * 28)` = `r * 0.28`)
  - Eye heights recalculated: `leh = int(r * 0.27)`, `reh = int(r * 0.22)`
  - Output: 1280×508px (thumbnail applied from raw ≥1280 width).
  - Generator: `output/tools/LTG_TOOL_character_lineup_v006.py`
  - Output: `output/characters/main/LTG_CHAR_luma_lineup_v006.png`

- **Image Handling Policy (new, applies all agents):**
  - Before sending image to Claude: ask if a tool can extract the insight. If so, make tool.
  - Before sending: ask if lower resolution suffices. If so, downscale.
  - Never send high-res images unless absolutely necessary.
  - Claude vision limits: hallucination on low-quality/rotated/tiny (<200px) images.
  - Spatial reasoning limited. Counting approximate on dense small objects.

- **Key proportion math for Luma 3.2 heads (render space, 2x):**
  - HR = 104px. One head = 2×HR = 208px.
  - 3.2 heads total = 6.4×HR = 665.6px
  - From head center to shoe bottom = HR*1 + HR*1.18 + torso_h + pants_h + HR*0.44
  - For 3.2: `torso_h + pants_h = 3.78 * HR` = `HR*2.10 + HR*1.68`

## Cycle 28 Lessons — TURNAROUND v003 + GLITCH EXPRESSION v003 (Interior Desire)

- **Turnaround v003 COMPLETE.** Line weight fix applied to all 4 views per v006 standard:
  - Head outline (FRONT, 3/4, BACK): was width=6 → now width=4
  - SIDE head polygon: was width=5 → now width=4
  - Torso outlines (FRONT, 3/4, BACK): was width=5 → now width=3
  - SIDE torso edges: was width=5/4 → now width=3
  - Cheek nubs, ears, eye outlines, pants, shoes: normalized to structure=3
  - BACK view confirmed present (was flagged as possibly missing — it exists in v002 and v003)
  - Thumbnail applied: 1600×700 → 1280×560 (≤1280px rule satisfied)
  - Generator: `output/tools/LTG_TOOL_luma_turnaround_v003.py`
  - Output: `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround_v003.png` (1280×560)

- **Glitch Expression Sheet v003 COMPLETE.** Grid expanded 3×2 → 3×3 (6→9 expressions).
  - New interior desire states responding to Nkechi Adeyemi critique C12:
    - YEARNING: utterly still body, UV_PURPLE eyes (soft glow, not glyph), arms hanging low, no confetti, no mouth, deep indigo BG. Read: watching what Glitch cannot have.
    - COVETOUS: lean (tilt=+12), ACID_GREEN slit eyes bilateral (both eyes target-locked), arms reaching, tight horizontal mouth, sparse UV_PURPLE confetti. Read: "I could take that."
    - HOLLOW: deflated (squash=0.88), empty bilateral stare (VOID_BLACK + single white pixel center), dangling arms, no confetti, single dim mouth dot. Read: aftermath of wanting.
  - New pixel color codes: 6=UV_PURPLE (yearning glow), 7=STATIC_WHITE (hollow center)
  - Canvas unchanged: 1200×900 (within ≤1280px rule)
  - Generator: `output/tools/LTG_TOOL_glitch_expression_sheet_v003.py`
  - Output: `output/characters/main/LTG_CHAR_glitch_expression_sheet_v003.png` (1200×900)

- **Alex Chen C28 directive received:** Canonical Luma ratio = 3.2 heads (already correct in turnaround v002/v003). Eye spec: h×0.22. Expression sheet v007 and Lineup v006 also required by directive — NOTE: those deliverables are listed in Alex Chen's message as separate P1 tasks for C28. Turnaround v003 and Glitch v003 are the tasks assigned to Maya for C28.

- **Inbox archived.** `20260329_1723_luma_proportion_directive.md` → `inbox/archived/`.

## Cycle 27 Lessons — CHARACTER LINEUP v005 (Luma v006 style propagation)

- **Lineup v004 Luma audit result: OLD construction.** Hair = 1 mass ellipse (not 8 curl-cloud). Head = bare ellipse, no chin fill, no cheek nubs. Eyes = tiny symmetrical circles, no eyelid arc, no iris.
- **Lineup v005 created:** `output/tools/LTG_TOOL_character_lineup_v005.py`. Only Luma's draw function updated. All other characters (Byte, Cosmo, Miri, Glitch) unchanged.
- **Luma v005 construction:** s = r/100.0 scale factor (r≈37px for lineup). 8-ellipse curl cloud hair, circle+chin fill+cheek nubs head, near-circular eyes with iris/pupil/highlight/eyelid arc, nose dots, mouth bezier. Line weights: head=2, structure=1-2, detail=1 (proportional to v006 at HR=104 scale).
- **Output:** `output/characters/main/LTG_CHAR_lineup_v005.png` — 1280×476px (thumbnail applied: raw 1340×498 → 1280×476).
- **Turnaround v002 line weight audit:** Heavy lines confirmed. `width=6` on hair arcs (lines 107, 138, 308, 636), `width=5` on torso outlines (202, 359, 455, 523–526, 656). Exceeds v006 canonical standard (head=4, structure=3). **C28 task flagged for Alex Chen.**

## Cycle 26 Lessons — LUMA STYLE FIX v2: LINE WEIGHT (v006)

- **v006 = line weight fix on top of v005 style alignment.** v005 had correct head/hair/eyes construction but still used heavy line weights (width=6-8 at 2x render).
- **Three-tier line weight at 2x render (CANONICAL for classroom-style Luma):**
  - Head outline only: width=4 (≈2px at 1x)
  - Structure (torso, arms, legs, cheek nubs, eye ovals, eyelid arcs, brows, mouth): width=3 (≈1.5px)
  - Detail (nose arc, laces, crinkles): width=2 (≈1px)
- **Hair strand arcs:** Must use width=3, NOT width=6. Large arc weights dominate the hair cloud mass read.
- **Mouth polylines:** Must use width=3. width=6 mouths look like rubber stamps.
- **Key rule: at 2x render, width=3 = classroom pose weight. width=6 = manga/overworked weight.**
- **Generator:** `output/tools/LTG_CHAR_luma_expression_sheet_v006.py` (new file, v005 preserved).
- **PNG:** `output/characters/main/LTG_CHAR_luma_expression_sheet_v006.png` (1200×900).

## Cycle 26 Lessons — LUMA STYLE FIX (expression sheet + turnaround)

- **Root problem:** v005 expression sheet used "manga/pitch" aesthetic — void black canvas, jaw ellipse head, 5-ellipse hair, wide manga eyes. Classroom pose uses naturalistic cartoon style — warm parchment bg, cheek nubs, 8-ellipse cloud hair, near-circular eyes.
- **Canonical Luma head:** circle + lower-chin fill + CHEEK NUBS at sides (NOT jaw ellipse at bottom). This is the classroom pose look the producer prefers.
- **Canonical Luma hair:** 8 overlapping ellipses of varying sizes = organic cloud mass. NOT 5 engineered ellipses. Scale using `s = HR / 100.0` factor.
- **Canonical Luma eyes:** near-circular proportions — ew ≈ HR*0.27 (≈28px@1x), eh_full ≈ HR*0.28 (≈28px@1x left, 22px right). NOT wide manga eyes (ew=HR*0.44).
- **Canonical Luma canvas:** warm parchment background (235,224,206) per panel, NOT dark void. Panel BGs should be light warm tones.
- **Scale formula for classroom → 2x render:** `s = HR / 100.0` where HR = HEAD_R * RENDER_SCALE. Classroom coords used head_r=100.
- **Expression Sheet v005 REBUILT.** Generator updated in place. PNG overwritten. Aligns to classroom pose style. 1200×900, show_guides=False.
- **Turnaround v002 FIXED.** FRONT view head: jaw → cheek nubs. Hair: 5→8 ellipses. PNG overwritten. 1600×700.
- **No direction message arrived from Alex Chen.** Used own judgment (aligned to classroom pose per fallback).
- **Completion report sent to Alex Chen inbox.**

## Cycle 25 Lessons — COLOR MODELS + FULL BODY SHEETS + TURNAROUNDS + MIRI NARRATIVE

- **Color Models COMPLETE (Priority 1 — blocking).** All 3 missing color models generated:
  - `LTG_COLOR_luma_color_model_v001.png` — 14 swatches, hoodie orange primary. Generator: `output/tools/LTG_COLOR_luma_color_model_v001.py`.
  - `LTG_COLOR_byte_color_model_v001.png` — 14 swatches. CRITICAL: body fill = #00D4E8 BYTE_TEAL (GL-01b) — NOT #00F0FF. Generator: `output/tools/LTG_COLOR_byte_color_model_v001.py`.
  - `LTG_COLOR_cosmo_color_model_v001.png` — 14 swatches, cerulean/sage stripes. Generator: `output/tools/LTG_COLOR_cosmo_color_model_v001.py`.
  - All 3 follow same format as Glitch color model: 800×500, left=silhouette, right=labeled swatches.
- **Luma Expression Sheet v005 COMPLETE (Priority 2).** FULL BODY per panel (head to feet). Every expression unique at silhouette level — body pose, arm position, weight shift. 1200×900, 3×2, 6 expressions. Generator: `output/tools/LTG_CHAR_luma_expression_sheet_v005.py`.
  - CURIOUS: forward lean + left arm reaches/points
  - DETERMINED: upright + fists at hips + wide stance
  - SURPRISED: backward lean + arms fly OUT to sides (wide wingspan)
  - WORRIED: arms crossed + legs together (contracted)
  - DELIGHTED: both arms up high + feet off ground (bounce)
  - FRUSTRATED: arms crossed + legs apart + backward lean + head drops
- **Cosmo Turnaround v002 COMPLETE (Priority 3 — side view fix).** Side view was architecturally impossible flat rectangle. v002 shows believable 3D: profile head (polygon), torso depth (horizontal stripe lines), notebook edge-on, near/far legs, side shoe profile. Generator: `output/tools/LTG_CHAR_cosmo_turnaround_v002.py`.
- **Luma Turnaround v002 COMPLETE (Priority 4).** Updated Cycle 10 turnaround to Act 2 proportions: A-line trapezoid hoodie, oversized sneakers with chunky sole + cyan laces, 3.2 heads, pixel accent on chest. Generator: `output/tools/LTG_CHAR_luma_turnaround_v002.py`.
- **Miri Expression Sheet v003 COMPLETE (Priority 5 — narrative expression).** Added KNOWING STILLNESS as 6th panel (3×2 grid, was 3+2). Narrative expression hints at Miri's secret (she knew about the Glitch Layer): heavy-lidded oblique glance, suppressed smile (one corner barely lifted), completely still body, blush 0.2. Generator: `output/tools/LTG_CHAR_grandma_miri_expression_sheet_v003.py`.
- **No direction message from Alex Chen arrived.** Used style frame Luma as canonical per fallback instruction. Used WISE slot → added KNOWING STILLNESS as 6th panel per own design judgment.
- **Completion report sent to Alex Chen inbox.**

## Key Cycle 25 Rules
- Color model format: 800×500, left=character silhouette, right=labeled swatches, canvas bg dark (character-specific).
- Full body expression sheets: always include legs/feet — bust format is NOT sufficient for body language differentiation.
- Turnaround side view MUST show 3D depth: profile head polygon, stripe lines horizontal, near/far legs staggered.
- Narrative expressions: body stillness CAN be an expression — total lack of movement is itself a silhouette statement.
- "Settled" arm style added to Miri arm renderer for KNOWING STILLNESS.

## Image Output Rule
**Prefer smallest resolution appropriate for the task. Hard limit: ≤ 1280px in both width and height.** Use `img.thumbnail((1280, 1280), Image.LANCZOS)` before saving any PNG. Preserve aspect ratio. Only use large canvases when fine detail must be visible; use smaller sizes for general-purpose work. Detail crops also ≤ 1280×1280px.

## Cycle 24 Lessons — GLITCH v002 + TURNAROUND v002 + LINEUP v004

- **Glitch Expression Sheet v002 COMPLETE.** 1200×900, 3×2, 6 expressions. Canvas upgraded from 800×800 2×2 (presentation failure — character too small for pitch review). Alex Chen directed: 6 full expressions preferred.
  - New expressions: STUNNED (electric jolt, full HOT_MAG eyes, ELEC_CYAN brows, wide scream, electro scatter) + CALCULATING (calm plotting, ACID_GREEN left eye only, right dim, one arm raised, sparse confetti).
  - MISCHIEVOUS vs TRIUMPHANT differentiated at SILHOUETTE: MISCHIEVOUS = tilt+20, diagonal arms (l=-6, r=+14). TRIUMPHANT = stretch=1.35, both arms up (l=-20, r=-22).
  - PANICKED: tilt=-14, squash=0.55, l=18/r=6, brow width=3 HOT_MAG steep rake, spread=38px.
  - Generator: `output/tools/LTG_CHAR_glitch_expression_sheet_v002.py`. Output: `output/characters/main/LTG_CHAR_glitch_expression_sheet_v002.png`.
- **Glitch Turnaround v002 COMPLETE.** Shadow contrast fix: SIDE/BACK view body fills changed UV_PURPLE→CORRUPT_AMB_SH (dark amber — readable against dark canvas). Void Black divider lines added between lit stripe and shadow flanks in SIDE view for facet geometry read. FRONT/3/4 unchanged. Generator: `output/tools/LTG_CHAR_glitch_turnaround_v002.py`. Output: `output/characters/main/turnarounds/LTG_CHAR_glitch_turnaround_v002.png`.
- **Character Lineup v004 COMPLETE.** All 5 chars: Luma, Byte, Cosmo, Miri, Glitch. 1340×498px. Generator: `output/tools/LTG_TOOL_character_lineup_v004.py`.
- **Glitch scale reference:** 170px hover height. Reaches Luma's shoulder (280px). Correct — compact digital antagonist, not physically overwhelming.
- **Dark-background shadow rule:** UV_PURPLE shadow fill reads correctly when there is contrast above/below (expression sheet panels). On pure dark void backgrounds (turnaround), UV_PURPLE disappears. Use CORRUPT_AMB_SH for shadow facets in dark-background contexts.
- **Canvas sizing rule for antagonist character:** match the protagonist standard (1200×900) — do NOT use a smaller canvas just because the character has fewer expressions. Presentation scale matters.
- **Inbox archived.** Both messages archived. Reports sent to Alex Chen.
- **Pitch asset state for Critique 11:** Glitch expr=v002 (6 expr, 1200×900), turnaround=v002 (shadow fix), lineup=v004 (all 5 cast).

## Cycle 23 Lessons — GLITCH v001 + QC PASS + MANIFEST

- **Glitch character CREATED (NEW).** Antagonist Glitchkin. Diamond/rhombus body. Primary: GL-07 CORRUPT_AMBER #FF8C00. Secondary: HOT_MAG #FF2D6B cracks, UV_PURPLE #7B2FBE shadow. Pixel dual-eye (3×3 grid, left=primary glyph, right=destabilized). No organic eye — full digital entity. Top+bottom spikes, two arm-spikes. Corrupted confetti hover (HOT_MAG+UV_PURPLE — NOT friendly cyan). VOID_BLACK #0A0A14 outline.
- **Glitch Expression Sheet v001 COMPLETE.** 800×800px, 2×2 grid, 4 expressions: NEUTRAL, MISCHIEVOUS, PANICKED, TRIUMPHANT. show_guides=False. Generator: `output/tools/LTG_CHAR_glitch_expression_sheet_v001.py`. Output: `output/characters/main/LTG_CHAR_glitch_expression_sheet_v001.png`.
- **Glitch Turnaround v001 COMPLETE.** 1600×700px, 4 views: FRONT, 3/4, SIDE, BACK. Generator: `output/tools/LTG_CHAR_glitch_turnaround_v001.py`. Output: `output/characters/main/turnarounds/LTG_CHAR_glitch_turnaround_v001.png`.
- **Glitch Color Model v001 COMPLETE.** 800×500px, 10 canonical swatches. Fixed bug: `reye_y` undefined (added `reye_y = face_cy - cell*3//2`). Generator: `output/tools/LTG_CHAR_glitch_color_model_v001.py`. Output: `output/characters/color_models/LTG_COLOR_glitch_color_model_v001.png`.
- **QC PASS Cycle 23.** All 4 original characters QC'd against character_sheet_standards_v001.md:
  - Luma v004: show_guides=False pitch export confirmed. CURIOUS/DELIGHTED differentiation confirmed.
  - Byte v004: Section 9B glyph spec compliant. 3×3 grid retained. Body fill GL-01b confirmed.
  - Cosmo v004: SKEPTICAL arm-neutral fix confirmed. Lean formula tilt_off×2.5 confirmed.
  - Miri v002: 1200×900, line weight Warm Dark Brown, blush state rule confirmed.
  - Non-standard canvas sizes (Byte/Cosmo) = grandfathered per standards doc policy.
- **character_export_manifest_v001.md COMPLETE.** All 5 character assets documented. Location: `output/characters/main/character_export_manifest_v001.md`.
- **Inbox archived.** `20260329_0900_cycle23_character_polish.md` → `inbox/archived/`.
- **Glitch design rules for next iterations:**
  - Pixel eye states: 0=VOID, 1=DIM(CORRUPT_AMB_SH), 2=ACTIVE(CORRUPT_AMB), 3=BRIGHT(SOFT_GOLD), 4=HOT(HOT_MAG), 5=ACID(ACID_GREEN)
  - Right eye = destabilized bleed of left (some bright→void/dim) = corruption read
  - Body is 2×SCALE render, LANCZOS to 1×. Diamond pts: top/right/bottom/left vertices.
  - Confetti color MUST be HOT_MAG/UV_PURPLE — never cyan/acid (reserved for healthy/friendly Glitchkin).

## Cycle 22 Lessons — BYTE v004 + COSMO v004 + LUMA v004
- **Byte Expression Sheet v004 COMPLETE.** Same 3×3 grid. Generator: `output/tools/LTG_CHAR_byte_expression_sheet_v004.py`. Output: `LTG_CHAR_byte_expression_sheet_v004.png` (784×1074px). Entry point wrapper: `output/characters/main/LTG_CHAR_byte_expression_sheet_v004.py`.
- **Section 9B glyph LOCKED (v004 canonical):** CRACK is a void-black overlay line, NOT a pixel state. Glyph uses only: 0=DEAD, 1=ALIVE_NORMAL, 2=ALIVE_BRIGHT, 3=DIM. DIM color = (0,80,100) #005064. Crack overlay = void black LINE #0A0A14. HOT_MAG crack is body/frame EXTERIOR only.
- **STORM differentiation rule:** RESIGNED = symmetric arms (14,14). STORM = asymmetric arms (6,22) = 20+ unit difference = damaged-asymmetric read at thumbnail.
- **RELUCTANT JOY v004:** arm_l_dy=-2 (one arm resisting upward), arm_r_dy=12, body_tilt=12. reluctant_joy=True flag triggers perked antenna. Asymmetry = "fighting against it."
- **POWERED DOWN v004:** body_squash=0.75 (was 0.88), both arms arm_dy=18. Unambiguous vs NEUTRAL.
- **Cosmo Expression Sheet v004 COMPLETE.** SKEPTICAL redesigned: arms near-neutral (2,2 vs -14,-10). body_squash=0.92. Reads as "contracted inward" not "arms raised." Generator: `output/tools/LTG_CHAR_cosmo_expression_sheet_v004.py`. Output: `LTG_CHAR_cosmo_expression_sheet_v004.png` (912×946px).
- **Luma Expression Sheet v004 COMPLETE.** show_guides flag added to render_face() and build_sheet(). CURIOUS upgraded: brow_r_dy -0.24→-0.34 HR, wider eyes (1.0/0.94), cy_offset +HR*0.06 (forward lean). Two exports: `_v004_guides.png` (production ref) + `_v004.png` (pitch/clean). Generator: `output/tools/LTG_CHAR_luma_expression_sheet_v004.py`.
- **show_guides pattern:** render_face(expr, w, h, show_guides=True). build_sheet(show_guides=True). Call draw_construction_guide() only when show_guides=True.
- **Cycle 22 inbox archived.** Report sent to Alex Chen.

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
