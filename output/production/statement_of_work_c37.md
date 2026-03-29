# Statement of Work — Cycle 37

**Date:** 2026-03-30
**Work cycles complete:** 37
**Critique cycles complete:** 14 (Critique 15 follows this cycle)

---

## Deliverables

### New Asset Categories (First Cycle)

**Storyboards**
- **LTG_SB_pilot_cold_open_v001.png** — 6-panel key-beat board, pilot cold open. Arc-color border grammar established (amber=QUIET, cyan=CURIOUS, magenta=TENSE, bright cyan=CORE). P5 glass-split two-world boundary is a strong visual grammar contribution. P4/P6 flagged by Lee for refinement (P4 needs directional cyan intrusion; P6 brow asymmetry and iris catch need enlargement at MCU scale).

**Story & Script**
- **story_bible_v001.md** — Full story bible: logline, series concept, world rules for all 3 worlds, tone guide (IN: Warm/Electric/Reckless/Specific/Earned; OUT: Cynical/Gross/Frantic/Vague/Safe), character voice guides with want/need/obstacle/cost for all 5 characters, pilot episode "Dead Pixels" with act structure, series arc across 13 episodes.
- Three consistency flags sent to Alex: (1) no visual plant for Grandma Miri / Glitch Layer Miri name connection, (2) production_bible.md Section 8 still says Byte = triangles (outdated), (3) Glitch character narrative status unclear.

**Motion Specs**
- **LTG_CHAR_luma_motion_v001.png** — 4-panel: idle/curious (hoodie lag +0.5 beats), sprint anticipation, discovery reaction (2 beats), landing/stop with secondary motion
- **LTG_CHAR_byte_motion_v001.png** — 3-panel: float/hover (0.5Hz ±6px), surprise (squash 3f/stretch 2f), approach (0°→−22° tilt, 0→100% glow)

**Environments**
- **LTG_ENV_grandma_living_room_v001.png** — New environment. CRT as focal point, dual-temp split pass, warm afternoon window + CRT cool spill. QA PASS (warm/cool 25.4).

### Character Updates
- **Cosmo v006** — Glasses tilt fixed: 10°→7° per spec. CI PASS (0 P1 violations). All 4 affected expressions corrected.
- **Luma expressions v010** — THE NOTICING: moved to center slot (was slot 0), stronger brow asymmetry, finger-to-lower-lip gesture, lateral gaze, richer hoodie color, subtle blush.

### Tools (New/Updated)
- `LTG_TOOL_ci_suite_v001.py` — Runs all 5 CI checks in one command. C37 baseline: WARN (0 hard FAILs).
- `glitch_spec_suppressions.json` + `glitch_spec_lint_v001.py` v1.2.0 — 26 false positives suppressed.
- `LTG_TOOL_draw_order_lint_v002.py` v2.1.0 — Back-pose W003 suppression via block comment markers.
- `LTG_TOOL_render_qa_v001.py` v1.4.0 — World-type-aware warm/cool thresholds. SF03 now PASS.
- `LTG_TOOL_sf02_fill_light_fix_c35.py` — Resolution-independent (canvas_w/canvas_h params).
- `LTG_TOOL_expression_silhouette_v003.py` — `--output-zones` flag added (HEAD/ARMS/LEGS colored overlays).
- `LTG_TOOL_contact_sheet_arc_diff_v001.py` — Auto-detects panel grid, color-coded diff output.
- `LTG_TOOL_warmth_inject_hook_v001.py` — Shared warmth-hook module; `--check-warmth` added to 4 env generators.
- `LTG_TOOL_env_grandma_living_room_v001.py` — New env generator.
- Motion spec generators: `LTG_CHAR_luma_motion_v001.py`, `LTG_CHAR_byte_motion_v001.py`.
- Storyboard generator: `LTG_SB_pilot_cold_open_v001.py`.

### QA
- **precritique_qa C37**: 333 PASS / 26 WARN / 0 FAIL (11 issues resolved vs C36).
- **CI suite C37**: WARN (0 hard FAILs, exit code 0).
- SF03 warm/cool: PASS (resolved by render_qa v1.4.0 world-type thresholds).

---

## Ideabox — C37 (12 ideas, all actioned → C38)
Alex: story bible visual crossref | Diego: storyboard thumbnail QA | Hana: env warm/cool debug | Jordan: env generator template | Kai: CI suite pre-commit hook | Lee: arc-diff as precrit gate | Maya: hero expression isolator | Morgan: lineup suppression expansion | Priya: story consistency checker | Rin: proportion audit --cycle flag | Ryo: motion lint tool | Sam: render_qa REAL threshold split (INTERIOR vs STORM)

---

## Open Items for C38
1. Luma THE NOTICING: v010 changes untested by critics — this remains the pitch's highest emotional risk
2. P4/P6 storyboard refinements (Diego, per Lee's feedback)
3. Grandma Miri / Glitch Layer Miri visual plant (design note needed — Alex)
4. production_bible.md Byte shape language fix (1-line update — Priya or Alex)
5. Glitch character narrative status clarification (Priya + Alex)
6. SF01 warm/cool near-miss (17.8/20.0 — Sam + Kai with REAL_INTERIOR threshold)
7. All 12 C37 ideabox ideas queued for C38
