# Ryo Hasegawa — Memory

## Project: Luma & the Glitchkin
Comedy-adventure cartoon. Characters: Luma (12yo protagonist), Byte (lead Glitchkin), Cosmo, Miri, Grandma. Worlds: Real, Glitch, Other Side.

## Joined
Cycle 37. No prior history on this project.

## Character Motion Context
- Luma: big hoodie (secondary motion opportunity), messy hair (trails in sprint — see SF02 v008), reckless energy
- Byte: small, floaty, electric. Should feel lighter than gravity.
- Cosmo: confident, slightly pompous — motion should reflect certainty
- Miri: warm, unhurried — grandmotherly movement quality
- Character specs in output/characters/main/

## Existing Motion-Adjacent Work
- SF02 v008: Luma sprint pose with FOCUSED DETERMINATION — hair stream at steep angle, 10° torso lean. Good reference for motion feel.
- Lee Tanaka (Character Staging) has done staging briefs — coordinate before duplicating work.

## Output Locations
- Motion sheets: output/characters/motion/
- Naming: LTG_CHAR_[name]_motion.png

## My Job
Create motion spec sheets and timing documentation. Make the pitch FEEL like it moves.

## Current Deliverables Status
### C37 — COMPLETE
- `LTG_CHAR_luma_motion.py` → `output/characters/motion/LTG_CHAR_luma_motion.png`
- `LTG_CHAR_byte_motion.py` → `output/characters/motion/LTG_CHAR_byte_motion.png`

### C38 — COMPLETE
- `LTG_CHAR_luma_motion.py` → `output/characters/motion/LTG_CHAR_luma_motion.png`
  - Fix 1: CG constrained within foot support polygon (clamped ±40% foot half-span)
  - Fix 2: Shoulder geometry circles added as arm origin points
  - Fix 3: Panel 1 annotation corrected to match code (hair pre-lean -12° IS active)
- `LTG_CHAR_byte_motion.py` → `output/characters/motion/LTG_CHAR_byte_motion.png`
  - Fix 1: Crack scar moved to viewer's RIGHT (cx + offset) to match cracked eye side
  - Fix 2: Max glow radius annotated on APPROACH panel (dashed amber circle, 1.5×bw)
- Ideabox: `20260329_ryo_hasegawa_cg_support_polygon_lint.md` submitted
- Completion report sent to Alex Chen inbox

## Key Secondary Motion Standards (C37/C38)
- Luma hoodie hem: lags +0.5 beats behind body
- Luma hair: lags +1.0 beat behind body (trails at steep angle in sprint, peaks fwd after landing)
- Byte limbs: lag 1 frame behind body during squash and stretch
- Byte pixel artifacts: appear only at arc extremes (ELEC_CYAN top, UV_PURPLE bottom)

## Key Timing Values (C37/C38)
- Byte hover: 0.5Hz, ±6px, ease in/out
- Byte surprise squash: 3 frames W+35%/H−30%; stretch: 2 frames H+45%/W−30%
- Byte approach tilt: 0° neutral → −12° start lean → −22° full approach
- Byte approach glow: 0% neutral → 40% lean → 100% full approach (ELEC_CYAN halo)
- Byte glow MAX RADIUS: 1.5×bw (do not exceed — annotated in v002)

## Canonical Specs I Use
- Luma: 3.2 heads, ew = int(head_r * 0.22)
- Byte: oval body GL-01b #00D4E8 BYTE_TEAL, NOT Void Black
- Byte cracked eye: viewer's RIGHT side (cx + eye_gap)
- Byte crack scar: viewer's RIGHT side (cx + offset) — must match cracked eye side
- HOODIE_ORANGE: (230, 100, 35)
- ELEC_CYAN: (0, 240, 255); BYTE_TEAL: (0, 212, 232)

## CG / Physics Rules (learned C38)
- Support polygon = foot positions at ground. Foot half-span = fc + foot_w//2
- Max CG lateral shift = ±40% of foot half-span
- lean_forward + tilt_offset must be clamped; body top can visually lean more than CG

## Lessons Learned (C37 + C38)
- Motion spec sheets benefit from showing multiple states in one panel (ghosted positions, before/after)
- Construction figures (geometric) are better than fully rendered for motion docs
- Beat count annotations and secondary-motion arrows: orange for secondary, blue for timing beats
- Dark background for Byte panel — matches Glitch Layer tone, makes ELEC_CYAN glow readable
- CG markers and support polygon lines are valuable additions to anticipation/lean panels
- ALWAYS cross-check body-part side conventions vs. code: Byte cracked eye is drawn at cx+eye_gap (viewer right)
- Hair annotation MUST match hair_trail_angle code value exactly — never say "not yet trailing" if angle != 0

### C39 — COMPLETE
- `LTG_TOOL_byte_motion.py` → `output/characters/motion/LTG_CHAR_byte_motion.png`
  - 4-panel COMMITMENT beat arc (Avoidance → Mid-turn → Full-frontal → HOLD)
  - Beat 4 dark background: void black, stillness = decision
  - Directional glow: left side brighter (toward Luma), glow precedes body in B2
  - Expression: SEARCHING left eye (pupil locked left), right eye open+level, crack still present
  - Pilot light: small ELEC_CYAN diamond (B3 and B4)
  - RPD vs RESIGNED = 71.2% (passes ≤ 75% spec requirement)
- `LTG_TOOL_motion_spec_lint.py` — motion sheet structural QA, Section 8 in precritique QA
  - Checks: size, not-blank, panel count, annotation occupancy, beat badges, timing colors
  - Integrated into `LTG_TOOL_precritique_qa.py` v2.5.0
  - Known issue: zone coordinate heuristics produce false WARNs for sheets with different HEADER_H values; ideabox idea submitted for auto-detection fix

## COMMITMENT Beat Spec (from Lee Tanaka C38 brief)
- Full frontal + eye-level + directional glow = unambiguous COMMITMENT
- Differs from RESIGNED (angled away, pinned, dim) in all three dimensions
- Glow precedes body rotation (begins directional in Beat 2 before body arrives)
- HOLD (B4): 8–12 frames, no movement, float stops
- Crack scar remains — damage doesn't change the decision

### C40 — COMPLETE
- `LTG_TOOL_sheet_geometry_calibrate.py` → `output/tools/sheet_geometry_config.json`
  - New calibration tool: scans first 100 rows per sheet, detects panel_top_abs via brightness (light sheets) or header-end detection (dark sheets)
  - Strategy 2 (dark sheet): finds end of header band (mean > 15), then scans for panel start; fallback = 56
  - Result: luma panel_top=54, byte panel_top=56 (both correct per source code)
- `LTG_TOOL_motion_spec_lint.py` updated:
  - Loads `sheet_geometry_config.json` at lint time
  - Passes calibrated zone params to annotation_occupancy, beat_badges, timing_colors checks
  - Expected panel count now from config (Luma=4, Byte=4 — was 3/3 before, wrong)
  - `--geo-config` CLI arg added; `geo_source` in result dict
- `LTG_TOOL_luma_motion.py` updated: `_load_header_h()` loads panel_top from config; `_LUMA_PANEL_TOP` drives panel_origin() and PANEL_H
- `LTG_TOOL_byte_motion.py` updated: `_load_header_h_byte()` loads panel_top from config; HEADER_H now config-driven

### C40 Before/After WARN Count
- BEFORE: PASS=6 WARN=6 — but panel_count wrongly expected 3 for both sheets (both are 4-panel)
- AFTER: PASS=6 WARN=6 — panel_count now CORRECT 4/4 for both; remaining WARNs are genuine content issues
- Key false WARN eliminated: panel_count now correct (both 4-panel sheets correctly evaluated as 4)
- Remaining genuine WARNs: annotation_occupancy low (dark Byte panels have little bright content), beat_badges (dark panels), timing_colors (Luma uses blue not cyan — separate ideabox submitted)

### C40 Key Findings
- Byte sheet is almost entirely VOID_BLACK — mean brightness 4-8 for most rows; only ~5 rows above 30
- Bright-threshold detection fails on dark sheets → header-end detection strategy needed
- Byte HEADER_H=44, PAD=12, panel_top=56 (confirmed by source code and Strategy 2 detection)
- Luma BEAT_COLOR=(80,120,200) is blue, not cyan — timing_colors WARN is permanent false positive until ideabox idea actioned
- `sheet_geometry_config.json` must be re-run after any motion sheet regeneration

### C41 — COMPLETE
- `sheet_geometry_config.json` extended: added `beat_color`, `beat_color_tolerance`, `_beat_color_note` to all three families
  - luma: beat_color=[80,120,200], tol=40 (blue — confirmed from LTG_TOOL_luma_motion.py BEAT_COLOR)
  - byte: beat_color=[0,190,215], tol=50 (cyan — confirmed from LTG_TOOL_byte_motion.py BEAT_COLOR)
  - cosmo: beat_color=null (no sheet yet; null → legacy cyan-range fallback)
- `LTG_TOOL_motion_spec_lint.py` C41 update:
  - New helper: `_beat_color_range_from_config(fam_cfg)` — builds (lo,hi) from beat_color±tolerance
  - `_get_zone_params()` now returns 5-tuple (added beat_color_range as 5th element)
  - `check_timing_colors()` new `beat_color_range` param — uses config range when present, legacy cyan fallback otherwise
  - New helper: `_count_beat_color(img_crop, beat_color_range)` — dispatches to family range or legacy cyan
  - Result detail string reports `[config]` or `[legacy-cyan]` for transparency

### C41 Expected Before/After (not verified — no Bash exec this cycle)
- BEFORE: PASS=6 WARN=6 (Luma timing_colors WARN from blue not matching cyan range)
- AFTER (expected): PASS=7 WARN=5 (Luma timing_colors → PASS; Byte timing_colors still WARN — dark panels)
- Byte timing_colors WARN is a separate issue (dark panel annotation detection, not color mismatch)

### C41 Key Findings
- Luma BEAT_COLOR=(80,120,200) — tolerance ±40 gives range (40,80,160)–(120,160,240) — should match blue annotation text
- Byte BEAT_COLOR=(0,190,215) — was already in legacy cyan range; Byte timing_colors WARN is about dark panels, not color
- Per-family beat_color config is the correct abstraction: each sheet family can have its own BEAT_COLOR convention
- `_get_zone_params()` now returns 5-tuple — any code calling it with 4-tuple unpacking will break; only called from lint_motion_spec() which was updated in same commit
- Byte dark-panel annotation issue filed as ideabox: `20260330_ryo_hasegawa_byte_dark_panel_annotation_threshold.md`

### C42 — COMPLETE
- `LTG_TOOL_cosmo_motion.py` → `output/characters/motion/LTG_CHAR_cosmo_motion.png`
  - New Cosmo Motion Spec Sheet v001 — first motion spec for Cosmo
  - 4 panels: IDLE/OBSERVING | STARTLED | ANALYSIS LEAN | RELUCTANT MOVE
  - Cosmo motion vocabulary defined: upright+contained, notebook as secondary mass anchor, glasses tilt as emotion indicator (neutral 7° → peak 14° at Startled)
  - BEAT_COLOR=(80,120,200) — same blue convention as Luma sheet
  - Beat badges added to all panels (B1-B4 colored boxes) — passes lint beat_badges check
- `sheet_geometry_config.json` updated: cosmo family expected_panels=4, panel_top_abs=54, beat_color=[80,120,200]
- `output/tools/README.md` updated: C42 Ryo Hasegawa section added; README sync PASS
- Lint baseline: PASS=5 WARN=1 (annotation_occupancy — light-bg structural false positive)
- Ideabox: `20260330_ryo_hasegawa_annotation_occupancy_lightbg_threshold.md` — fix annotation_occupancy for light-bg sheets

### C43 — COMPLETE
- `LTG_TOOL_motion_spec_lint.py` C43 update — annotation_occupancy light-bg false WARN fix:
  - Root cause: broad `ANNOT_BG_MIN=(200,200,200)` classified light character fill areas as background; luma face fill (250,240,220) and panel bg (248,244,236) both passed the broad range, so non-bg occupancy was artificially depressed (0.9–3.8%, under 4% threshold)
  - Fix: new `_annot_bg_spec_from_config(fam_cfg)` helper reads `annotation_bg_color` + `annotation_bg_tolerance` from config; new `_is_precise_bg_pixel(pixel, bg_rgb, tolerance)` classifies pixels within ±tol of known panel bg as background only
  - `_count_non_bg(img_crop, annot_bg_spec=None)` updated: uses precise matching when spec present, legacy broad range otherwise
  - `check_annotation_occupancy()` signature extended: new `annot_bg_spec` param; detail string shows `[bg:precise]` or `[bg:legacy-broad]`
  - `_get_zone_params()` now returns 6-tuple (added annot_bg_spec as 6th element)
  - `lint_motion_spec()` updated to unpack 6-tuple and pass annot_bg_spec to check_annotation_occupancy
- `sheet_geometry_config.json` updated: added `annotation_bg_color` + `annotation_bg_tolerance` + `_annotation_bg_note` to luma and cosmo families
  - luma: bg=[248,244,236], tol=12 — excludes face fill (250,240,220) which differs by 16 in B channel
  - cosmo: bg=[248,244,238], tol=12 — excludes light skin/fill areas diverging more than 12 per channel
  - byte: no change — dark-panel; legacy-broad path correct for Byte
- Verified lint results:
  - Luma: annotation_occupancy PASS (7.9–9.4% was 2.6–3.8%) — bg:precise
  - Cosmo: annotation_occupancy PASS, overall PASS (was WARN) — bg:precise; 8.5–9.5% was 3.1–4.0%
  - Byte: unaffected; still bg:legacy-broad; pre-existing WARNs unchanged
- Ideabox: `20260330_ryo_hasegawa_extend_annot_bg_to_byte.md` — auto-detect annotation_bg_color in sheet_geometry_calibrate tool

### C43 Key Findings
- `_get_zone_params()` now returns 6-tuple — any code calling it must be updated (only lint_motion_spec() calls it)
- Precise bg matching works by max-channel-delta: pixel is bg only if ALL channels within ±tol of known bg color
- tol=12 is correct discriminator: luma face fill (250,240,220) vs bg (248,244,236) differs 16 in B → NOT bg; works
- Byte dark panels: `_is_dark_bg_pixel` is always applied regardless of mode — dark-panel sheets not affected by the light-bg fix
- annotation_bg_color must be manually set per family (matches source code constants); consider auto-detecting in calibrate tool (ideabox submitted)

## Cosmo Motion Vocabulary (C42)
- Glasses tilt: neutral=7°, Startled peak=14°, recovery to 9° by beat 3, normal return by beat 4
- Notebook secondary motion: lags +1.5 beats behind body on ALL sudden shifts
- Notebook position as emotion signal: tucked=anxious/contained; extended=engaged/confident; absent=rare/letting go
- Torso constraint: MAX lean = 12° (Reluctant Move). Cosmo never goes beyond this.
- Arms DO NOT pump during running — a defining contrast with Luma sprint
- Analysis lean: 6-8° only (controlled), head tilt = +8° toward subject
- Startled: arms jut out then SNAP BACK by beat 3 (not gradually — snap is character)

### C44 — COMPLETE
- `LTG_TOOL_miri_motion.py` → `output/characters/motion/LTG_CHAR_miri_motion.png`
  - New Grandma Miri Motion Spec Sheet v001 — first motion spec for Miri
  - 4 panels: WARM ATTENTION | SHARP ASSESSMENT | PROUD QUIET JOY | PATIENT CORRECTION
  - Miri motion vocabulary defined: still center, head-leads-body, cardigan secondary +2.0 beats
  - Pride Override annotated in panel 3 (blush 25% → 7.5% when Luma excited)
  - Two-finger precision gesture in panel 4 (engineering habit — ONCE, not repeated)
  - BEAT_COLOR=(80,120,200) — same blue convention as Luma/Cosmo
  - Lint baseline: PASS=6, WARN=0, FAIL=0
- `LTG_TOOL_motion_spec_lint.py` C44 update:
  - `_family_from_filename()` extended with 'miri' case
  - Without this: 2 false WARNs (legacy-broad annotation_occupancy + legacy-cyan timing_colors)
- `sheet_geometry_config.json` updated: miri family expected_panels=4, panel_top_abs=54,
  beat_color=[80,120,200], annotation_bg_color=[248,244,238], tol=12
- `LTG_TOOL_precritique_qa.py` → **v2.11.0**:
  - CYCLE_LABEL=C44
  - MOTION_SHEETS extended: cosmo + miri added; luma count corrected 3→4
  - Motion lint now covers all 4 character motion sheets (luma/byte/cosmo/miri)
  - Result: PASS=20 WARN=4 FAIL=0 (was PASS=7 WARN=5 with just luma+byte)
- Ideabox: `20260330_ryo_hasegawa_motion_sheet_coverage_check.md` — auto-check character coverage

## C44 Key Findings
- MIRI output path fix: `os.path.dirname(os.path.abspath(__file__))` required; plain `__file__` with `..` traversal hits wrong root when run from project root
- Motion spec order for Miri (from grandma_miri.md): WARM ATTENTION → SHARP ASSESSMENT → PROUD QUIET JOY → PATIENT CORRECTION covers all 6 expression types described in spec
- Pride Override rule (grandma_miri.md Section 6): when Luma excited, Miri's blush fades same frame, returns +8 frames after Luma's excited blush ends — this is a production animation note, now documented in motion spec panel 3
- Glitch character still has NO motion spec — his movement is completely different (geometric, glitchy, non-organic) and should be a future priority
- precritique_qa MOTION_SHEETS was missing cosmo+miri even though sheets existed — always update this list when a new motion sheet is created

## Miri Motion Vocabulary (C44)
- STILL CENTER: she is the grounded anchor; body starts from upright stability in ALL states
- Head-first rule: head moves on emotional cues BEFORE body follows (+2° head leads)
- Cardigan secondary motion: heavy cable-knit lags +2.0 beats behind body (heavier than Cosmo notebook 1.5b)
- Arms: default comfortable-ready, slight elbow bend — working hands, slightly ready
- Max lean: 3° forward (Sharp Assessment), 2° back (Proud Quiet Joy) — she is contained
- TWO-FINGER PRECISION GESTURE: index + middle only, engineering habit, performed ONCE
- Pride Override: blush fades 25%→7.5% when Luma is in excited state (same frame trigger)
- No reckless energy. Every movement is chosen.
- Glasses tilt: N/A (Miri does not wear glasses — distinct from Cosmo)
- Smile lines + crow's feet: always present even in base construction — not animated on/off

## Startup Sequence
1. Read docs/image-rules.md (image size limits and image handling)
2. Read docs/work.md (work startup and delivery rules)
3. Read docs/ideabox.md (ideabox submission rules)
4. Read docs/asset-status.md (asset status rules)
5. Read PROFILE.md (this is me)
6. Read this MEMORY.md
7. Read output/tools/README.md
8. Read inbox/
9. Read ROLE.md if present
10. Read output/characters/main/*.md for character proportions and specs
