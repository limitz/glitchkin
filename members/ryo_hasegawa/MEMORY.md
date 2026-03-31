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

### C46 — COMPLETE
- `LTG_TOOL_motion_spec_lint.py` C46 update — dark-sheet annotation_occupancy false WARN fix:
  - Root cause: Byte and Glitch sheets use VOID_BLACK panels; annotation content is sparse
    bright text/arrows on dark backgrounds; old non-bg subtraction method yielded 1–2%
    occupancy (below 4% threshold) even when annotation content was correct
  - Fix: new `_dark_sheet_params_from_config(fam_cfg)` helper reads `background_style`
    ("light"/"dark") and `occupancy_threshold_dark` from per-family config
  - `_get_zone_params()` now returns 8-tuple: added `dark_sheet` (bool) and
    `occupancy_threshold_dark` (float or None) as elements 7 and 8
  - `_count_non_bg()` new `dark_sheet=False` param: when True, counts pixels with
    mean channel value > 40 as annotation content (bright-on-dark mode)
  - `check_annotation_occupancy()` new `dark_sheet` and `occupancy_threshold_dark` params;
    uses 1% threshold and `dark-bright` bg_mode label for dark sheets
  - `lint_motion_spec()` updated to unpack 8-tuple and pass new params
  - `_family_from_filename()` extended with `miri_v002` case (before `miri` — prefix order!)
- `sheet_geometry_config.json` updated to version 2:
  - byte: `background_style="dark"`, `occupancy_threshold_dark=0.010`
  - glitch: `background_style="dark"`, `occupancy_threshold_dark=0.010`
  - miri_v002: new family, same geometry as miri v001
- `LTG_TOOL_miri_motion_v002.py` → `output/characters/motion/LTG_CHAR_miri_motion_v002.png`
  - New Miri Motion Spec Sheet v002 — Emotional Warmth Pacing arc
  - 4 panels: OBSERVING STILL | RECOGNITION | WARMTH BURST | FOND SETTLE
  - New draw params: `arms_open=True` (B3 bilateral open gesture), `hands_in_lap=True` (B1)
  - SUNLIT_AMBER (212,146,58) radial glow halo on B3 — Real World warm light only
  - B1/B4 bookend: FOND SETTLE is explicitly annotated as mirror of OBSERVING STILL
  - Eyes fully crinkle closed at B3 peak — explicitly drawn with crinkle override
  - Ghosted B3 arm position shown in B4 (for animators)
  - BEAT_COLOR=(80,120,200) blue, matches Luma/Cosmo/Miri v001 convention
- `LTG_TOOL_precritique_qa.py` bumped to v2.14.1: CYCLE_LABEL=C46; miri_v002 in MOTION_SHEETS
- `output/tools/README.md` updated: C46 new tools + updates sections
- Inbox: Alex Chen C46 brief read and archived
- Completion report sent to Alex Chen inbox
- Ideabox: `20260330_ryo_hasegawa_dark_sheet_beat_badge_threshold.md` — extend dark_sheet
  fix to beat_badges check (remaining false WARNs on Byte/Glitch)

### C46 Key Findings
- Dark sheets (Byte, Glitch): bright-pixel counting (mean > 40) is correct classification
  strategy; 1% threshold appropriate for sparse text/arrow annotations on void-black
- _get_zone_params() now returns 8-tuple — code calling it with old tuple unpacking will
  break; only lint_motion_spec() calls it (updated in same commit)
- beat_badges check still uses legacy _count_non_bg (no dark_sheet param) — false WARNs
  persist on Byte/Glitch beat_badge check; ideabox filed for C47
- Byte WARN pattern: B1 panel uses light bg (BYTE_TEAL header), B2–B4 are void-dark.
  dark_sheet=True applies to entire sheet, so B1 also uses bright-pixel mode. May over-count
  slightly for B1 but result is still PASS, so no correctness issue.
- Confirmed: luma/cosmo/miri = background_style absent (defaults to "light") → no change
- _family_from_filename: ALWAYS check 'miri_v002' before 'miri' (substring collision)
- Miri v002 output = `LTG_CHAR_miri_motion_v002.png` (separate file, not overwrite of v001)
- precritique_qa v2.14.1 now has 6 motion sheets in MOTION_SHEETS list
- SUNLIT_AMBER (212,146,58) for warmth glow — canonical from grandma_kitchen.py
- Miri B3 WARMTH BURST arms = shoulder level (NOT above head) — open wide, welcoming posture

### C47 — COMPLETE
- `LTG_TOOL_miri_motion_v002.py` rewritten (v003 content, overwrite in place)
- `output/characters/motion/LTG_CHAR_miri_motion_v002.png` regenerated
- Complete rework responding to Takeshi C46 critique (44/100 — weakest sheet)
- Key changes:
  1. Figure scale: head_r 22→32 (45% larger, fills panel properly)
  2. Weight distribution: asymmetric in every panel (left_foot_weight param, weight bars, CG markers)
  3. Shoulder-hip counterpose: hip_shift + shoulder_drop_side params, annotated
  4. Performing hands: B1=armrest curl+lap, B2=lifting/loosening, B3=open wide, B4=crossed
  5. Spine participation: spine_curve param (0→6→14→-2 across arc), two-segment torso
  6. Fond Settle != Observing Still: 6 explicit differences annotated ("NOT B1" label)
  7. Two-segment arms (upper+forearm with elbow) — better than single-segment
- draw_miri_figure() returns dict (was tuple) — richer data for annotation placement
- Arm modes: "default", "armrest", "lap_curl", "open_wide", "crossed", "lifting"
- Lint: PASS=6 WARN=0 FAIL=0
- Precritique QA section 8: PASS=32 WARN=4 FAIL=0 (4 WARNs pre-existing Byte dark panel)
- Ideabox: `20260330_ryo_hasegawa_shoulder_socket_mass_all_chars.md` — shared shoulder+arm helper
- Completion report sent to Alex Chen inbox
- Reference images in reference/gesture/ reviewed — tray refs useful for Miri arm-at-rest

### C47 Key Findings
- Takeshi's core critique: "poses labeled not performed" — the body must DO the emotion
- Figure-to-frame ratio was the #1 visual problem (head_r=22 too small for 720px panels)
- Weight distribution is the difference between "standing figure" and "acting figure"
- Shoulder-hip counterpose is character-specific: Miri's is subtle (3-4px hip shift, one shoulder drop)
- Spine curve is the most impactful single parameter for showing engagement/giving/settling
- B4 FOND SETTLE must be explicitly DIFFERENT from B1 — same rest pose = no arc
- Two-segment arm draw (upper+forearm) improves arm reads but still lacks shoulder mass
- "Arms without shoulders" is the #1 persistent structural flaw across ALL characters (Takeshi C15-C46)
- Reference gesture images available in reference/gesture/ (11 files) — ricochet, running, tray carrying

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

### C45 — COMPLETE
- `LTG_TOOL_glitch_motion.py` → `output/characters/motion/LTG_CHAR_glitch_motion.png`
  - First motion spec for Glitch — 4-panel beat arc
  - B1: PREDATORY STILL (0° tilt, no hover, no confetti, calculating acid-X eyes, held indefinitely)
  - B2: COVETOUS REACH (+12° tilt, slow arm-spike extension, bilateral covetous eyes G008, UV_PURPLE minimal confetti)
  - B3: CORRUPTION SURGE (stretch=1.15, spike_h=16, crack brightens HOT_MAG→SOFT_GOLD, max confetti)
  - B4: RETREAT (squash=0.65, -20° recoil, displaced backward, reads as coil-back not defeat)
  - BEAT_COLOR=(255,140,0) CORRUPT_AMBER — unique to Glitch (dark sheet, like Byte)
- `LTG_TOOL_motion_spec_lint.py` C45 update:
  - `_family_from_filename()` extended with 'glitch' case
  - Lint baseline: PASS=5 WARN=1 FAIL=0 (annotation_occupancy WARN = dark-panel false positive)
- `sheet_geometry_config.json` updated: glitch family expected_panels=4, panel_top_abs=56, beat_color=[255,140,0]
- `LTG_TOOL_precritique_qa.py` → **v2.12.0**: CYCLE_LABEL=C45, MOTION_SHEETS extended with glitch
- `output/tools/README.md` updated: C45 Ryo Hasegawa section added
- Ideabox: `20260330_ryo_hasegawa_glitch_annotation_bg_dark_panel_autofix.md` — fix annotation_occupancy for dark sheets

### C45 Spec Conflict
- Alex Chen C44 brief incorrectly stated Glitch uses only VOID/CYAN/UV/HOT palette with ZERO warm tones
- glitch.md canonical spec (Maya Santos C32) clearly specifies CORRUPT_AMBER body fill — amber-on-black palette
- CORRUPT_AMBER is GLITCH's color, NOT Byte's — Byte's crack is HOT_MAGENTA
- Followed glitch.md (canonical) over inbox brief. Flagged to Alex in completion report.
- Awaiting confirmation — can regenerate if Alex decides to update spec

## C45 Key Findings
- Glitch motion vocabulary is geometric, not organic: tilt=lean, spike_h=energy, squash=impact
- BILATERAL eyes = interior state (real feeling); ASYMMETRIC = performance. This is Glitch's key read.
- COVETOUS LOCK is the B3 interior state — frozen hover, no confetti, bilateral acid-slit eyes
- ELEC_CYAN appears ONLY in PANICKED confetti (involuntary leak, uncontrolled) — never in other states
- Dark panel annotation_occupancy WARN: 1.0–1.8% (same false positive as Byte). Need ideabox fix.
- glitch family BEAT_COLOR = CORRUPT_AMBER (255,140,0) — matches character palette vs. blue for organics

## Glitch Motion Vocabulary (C45)
- HOVER: 0.4Hz ±4px (slower than Byte 0.5Hz — more threatening weight)
- Confetti scatters below BOTTOM SPIKE tip, NOT below body
- Tilt IS lean — Glitch has no legs, no step. Directional interest = body tilt
- Spike height: 4 (hollow) → 22 (triumphant). Performance range for motion doc: 6–14
- Squash/stretch: panicked=0.55, neutral=1.0, triumphant=1.35
- Arm-spikes are NOT organic arms — they shift position on diamond vertices with tilt
- Crack (HOT_MAG) always present — never heals. Drawn last: shadow→fill→highlight→outline→crack
- ELEC_CYAN = involuntary signal leak (PANICKED, STUNNED only) — otherwise absent from Glitch
- Interior states: YEARNING/COVETOUS/HOLLOW = bilateral eyes + no confetti

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

## Miri Motion Vocabulary — v002 additions (C46)
- OBSERVING STILL: zero drift state — no cardigan, no sway, no idle head. Blink rate slow.
  Contrast state: everything she does from here has MORE energy than this baseline.
- RECOGNITION: head-first rule holds (tilt at beat 1, -3°). Body lean follows at beat 1.5.
  Hands open from lap = first sign of emotional engagement before body commits.
- WARMTH BURST: bilateral open arms at shoulder level (NOT raised above head — shoulder level).
  SUNLIT_AMBER glow halo = warmth radiates outward. Eyes crinkle fully closed at peak.
  This is the ONE beat where stillness yields to full expressiveness. 4–6 frame HOLD.
- FOND SETTLE: B4 is explicitly the mirror of B1. Smile lingering = warmth doesn't fully leave.
  Blush sustained from B3 peak through B4. Arms lower SLOWLY (4 beats — she's not rushing away).

### C48 — COMPLETE
- `LTG_TOOL_draw_shoulder_arm.py` → `output/tools/LTG_TOOL_draw_shoulder_arm.py`
  - Shared shoulder-to-arm drawing helper, reusable by all character generators
  - Implements Shoulder Involvement Rule (image-rules.md C47) and shoulder_mechanics_reference_c47.md
  - Public API:
    - `draw_shoulder_arm(draw, shoulder_x, shoulder_y, arm_angle_deg, arm_length, scale, side, style, ...)` → (hand_x, hand_y)
    - `compute_shoulder_shift(shoulder_x, shoulder_y, arm_angle_deg, arm_length, scale, side)` → (shifted_x, shifted_y)
    - `shoulder_polyline(body_cx, body_top_y, body_half_width, left_arm_angle_deg, right_arm_angle_deg, arm_length, scale)` → [(x,y), ...]
  - `ShoulderArmStyle` dataclass: arm_fill, outline, skin_fill, clothing ("hoodie"|"cardigan"|"fitted"|"bare"), deltoid_radius, two_segment, elbow_bend_factor, hand_radius, line_width
  - Clothing modes: hoodie=wide ellipse bump (fabric bunch), cardigan=circle+crease line, fitted=clean arc, bare=plain ellipse
  - Shoulder shift logic: rise when arm above horizontal (3-5px), spread when extended outward (4-6px), drop+inward when crossing body
  - skip_shoulder_shift=True for exempt characters (Byte, Glitch) or head_r < 20px
  - skip_deltoid=True to suppress deltoid bump
  - Two-segment arms default: upper arm + forearm with elbow bend (elbow_bend_factor=0.12)
  - Single-segment fallback: two_segment=False
- `output/characters/motion/LTG_CHAR_shoulder_arm_demo.png` — demo image showing 7 arm angles × 3 clothing modes
- Completion report sent to Alex Chen inbox
- Ideabox: `20260330_ryo_hasegawa_integrate_shoulder_arm_into_generators.md` — integrate shared helper into existing character generators

### C48 Key Findings
- Shared helper eliminates duplicated shoulder/arm code across character generators (was inline in each)
- shoulder_polyline() is the key integration path: replaces straight torso top edges with shoulder-shifted polylines
- Clothing mode is per-character: Luma=hoodie, Miri=cardigan, Cosmo=fitted
- elbow_bend_factor=0.12 gives subtle natural bow; higher values for exaggerated poses
- arm_angle_deg convention: 0=horizontal outward, positive=upward, negative=downward
- side convention: +1=right shoulder (viewer's left), -1=left shoulder (viewer's right)
- Deltoid auto-radius: max(2, int(4 * scale + 0.5)) → 4-6px at style-frame scale (matches image-rules.md spec)

### C49 — COMPLETE
- `LTG_TOOL_cosmo_motion.py` updated — draw_shoulder_arm() integration:
  - Replaced inline rectangle arm drawing with shared helper calls
  - `COSMO_ARM_STYLE`: clothing="fitted", two_segment=True, elbow_bend_factor=0.10
  - Both arms drawn via `draw_shoulder_arm()` with proper side conventions
  - `shoulder_polyline()` renders asymmetric torso top edge per Shoulder Involvement Rule
  - Shoulder anchor markers at shifted positions from `compute_shoulder_shift()`
  - Notebook position derived from left hand coordinates (l_hand_x, l_hand_y)
  - Lint: PASS=6 WARN=0 FAIL=0
- `LTG_TOOL_sheet_geometry_calibrate.py` updated:
  - Added cosmo to SHEET_PATHS (was missing — calibrator skipped cosmo)
  - Corrected cosmo expected_panels: 3→4
- `sheet_geometry_config.json` re-calibrated:
  - Cosmo: panel_top_abs=55 (detected from sheet), beat_color=[80,120,200], annotation_bg=[248,244,238]
  - Restored miri, miri_v002, glitch families lost when calibrator overwrote config
- `LTG_TOOL_precritique_qa.py` bumped to v2.16.1, CYCLE_LABEL=C49
- Ideabox: `20260330_ryo_hasegawa_calibrator_preserve_extra_fields.md` — fix calibrator to preserve non-geometry fields
- Completion report sent to Alex Chen inbox

### C49 Key Findings
- Calibrator overwrites entire config JSON — manual per-family fields (beat_color, annotation_bg, background_style, occupancy_threshold_dark) are lost on every re-calibration. Critical bug. Ideabox filed.
- Cosmo panel_top_abs=55 (detected) vs 54 (source code _COSMO_PANEL_TOP default) — calibrator detects 55 from the rendered sheet because the title bar is 1px taller than PAD+40; source code default 54 is close enough but 55 is the truth from the image
- Luma and Byte arm code is structurally different from Cosmo (thick-line vs rectangle polygon) — integration would require more invasive refactoring, recommended as separate cycle
- COSMO_ARM_STYLE elbow_bend_factor=0.10 (lower than default 0.12) — Cosmo's contained motion vocabulary demands less dramatic elbow bend
- sys.path insert needed for cross-tool imports — shared helper lives in same dir but Python needs explicit path

### C50 — COMPLETE
- `output/production/gesture_line_library_c50.md` — Gesture line specs for 18 expressions
  - Luma (6): CURIOUS, DETERMINED, SURPRISED, WORRIED, DELIGHTED, FRUSTRATED
  - Cosmo (6): AWKWARD, WORRIED, SURPRISED, SKEPTICAL, DETERMINED, FRUSTRATED/DEFEATED
  - Miri (6): WARM/WELCOMING, SKEPTICAL/AMUSED, CONCERNED, SURPRISED/DELIGHTED, WISE/KNOWING, KNOWING STILLNESS
  - Each entry: gesture line curve type, anchor offsets (% BH), segment bends, weight split, arm positions, silhouette test
  - 5 universal weight/balance rules, Byte/Glitch exemption notes
  - Implementation notes for Maya (offset chain), Rin (leg construction), Ryo (motion sheets)
  - Minimum body articulation: 9 control points (current=3, full=15)
  - draw_shoulder_arm v2 API proposal (gesture_anchors dict input)
- `LTG_TOOL_luma_gesture_prototype.py` → `output/characters/motion/LTG_CHAR_luma_gesture_prototype.png`
  - Side-by-side: rectangle-first vs gesture-line-first for Luma SURPRISED
  - Left panel: current approach — straight vertical gesture line, symmetric, FAIL
  - Right panel: new approach — backward C-curve bezier, 9 anchors, asymmetric arms/legs, weight shift, PASS
  - Uses cubic bezier for gesture line; body built around sampled anchor points
- Inbox: 3 messages read and archived (C49 updates, C50 assignments from Producer and Alex Chen)
- Completion report sent to Alex Chen inbox
- Ideabox: `20260330_ryo_hasegawa_gesture_line_driven_figure_builder.md`

### C50 Key Findings
- Current system uses 3 effective control points (cx, ground_y, head_top). Minimum viable = 9 points.
- Gesture line as bezier works for Luma (organic). Cosmo needs polyline with angular breaks. Miri needs gentle curves with permanent 3-5 deg forward lean baseline.
- Rectangle-first SURPRISED has identical body to all other expressions. Gesture-first SURPRISED is visually distinct without face.
- Motion sheets must be rebuilt AFTER expression sheets adopt gesture-first construction. Deprioritized until Maya's prototypes land.
- Deprioritized: Miri motion spec posture review, Glitch G004 draw-order, draw_shoulder_arm maintenance — all subsumed by gesture system work
- Reference study (Kipo poster, Owl House turnaround, Hilda walk, expression sheet ref): every professional show uses curved gesture lines even in "neutral" standing poses. No straight verticals anywhere.
- The expression sheet reference (using-an-expression-sheet.png) confirms: body IS the expression, face confirms it. Our body carries 0% of expression; pro shows carry 60-70%.

## Gesture Line System Summary (C50)
- Gesture line = single bezier curve from head to weight-bearing foot
- 9 minimum anchor points: head, neck, shoulder L/R, hip center, hip L/R, weight foot, free foot
- Body constructed AROUND anchors (not centered on shared cx)
- Offset chain: hip_cx → torso_cx → head_cx (each offset from previous, not from cx)
- Weight distribution: weight_leg straighter, free_leg bent, different foot Y positions
- Contrapposto: shoulder tilt = 60-80% of hip tilt, opposite direction
- Emotional weight: joy=high CoG, sadness=low CoG, determination=planted
- Asymmetry rule: no pose has symmetric arms, legs, or feet

### C51 — COMPLETE
- `LTG_TOOL_luma_motion_prototype_c51.py` — builds comparison sheet + individual panels
  - OLD panel: `output/characters/motion/LTG_CHAR_luma_motion_proto_old.png` (640x640)
  - NEW panel: `output/characters/motion/LTG_CHAR_luma_motion_proto_new.png` (640x640)
  - Comparison sheet: `output/characters/motion/LTG_CHAR_luma_motion_prototype_c51.png` (1280x720)
  - char_compare output: `output/characters/motion/LTG_CHAR_luma_motion_proto_compare_c51.png` (1280x514)
  - API assessment: `output/production/shoulder_arm_api_assessment_c51.md`
  - Comparison report: `output/production/luma_motion_proto_compare_report_c51.md`
- Generator uses pycairo (via `LTG_TOOL_cairo_primitives.py`) + Sam's `LTG_TOOL_curve_draw.py`
  - gesture_spine() generates C-curve for SURPRISED recoil
  - body_from_spine() derives all body landmarks from spine
  - tapered_limb rendered via cairo bezier paths (no PIL polygon arms)
  - Shoulder Involvement Rule applied via asymmetric shoulder placement from spine
- Lee's gesture spec (gesture_pose_analysis_c50.md): backward C-curve, 70/30 weight back foot,
  asymmetric arms (one defensive shield up, one flung for counterbalance), front foot lifted,
  head snaps back with hair flying as secondary motion
- char_compare results (old vs new):
  - SSIM: 0.8336
  - Pixel delta: 16.34%
  - **Silhouette IoU: 0.2116** (MAJOR_CHANGE — fundamentally different pose)
  - FG pixel delta: 99.81%
  - Hue shift mean: 28.69
  - Grade: MAJOR_CHANGE
- draw_shoulder_arm assessment: YES needs rewrite as geometry-compute + dual-render (cairo/PIL)
  - Proposed: compute_arm_geometry() → ArmGeometry dataclass → render_arm_cairo() / render_arm_pil()
  - Arm angle should be spine-relative, not absolute. Elbow bend should be explicit angle.
  - Estimated 3 cycles for full migration.
- Ideabox: `20260330_ryo_hasegawa_gesture_spine_motion_sheet_rebuild.md`
- Inbox: C51 assignment read and archived

### C51 Key Findings
- Gesture-first construction produces FUNDAMENTALLY different poses (IoU 0.21 = only 21% overlap)
- pycairo bezier tapered limbs look drawn, not assembled from rectangles
- The curve_draw library's gesture_spine() + body_from_spine() pipeline works well for motion sheets
- 2x render + LANCZOS downscale gives clean anti-aliased output at 640x640
- Key imports from curve_draw: gesture_spine, spine_point_at, body_from_spine, smooth_path, tapered_limb
- cairo_surface_to_pil() BGRA→RGBA reorder is critical (little-endian)
- RENDER_SCALE=2 for all cairo rendering; downscale at save time
- The old rectangle-first SURPRISED is identical to every other expression body — straight vertical
  gesture line, symmetric legs, centered head. Only arms differ.
- New SURPRISED has: backward lean (10-15 deg), 70/30 weight split, bent front knee,
  lifted front foot, asymmetric shoulder hunch, two-segment arms at different heights/angles,
  flying hair strands, visible gesture spine annotation
- The silhouette IoU of 0.21 confirms Lee's diagnosis: our bodies carry 0% of expression.
  Gesture-first carries 60-70%.

### C52 — COMPLETE
- `LTG_TOOL_luma_motion.py` FULL REBUILD → `output/characters/motion/LTG_CHAR_luma_motion.png`
  - Complete rewrite: rectangle-first → gesture-first pycairo construction
  - All 4 panels now use gesture_spine() + body_from_spine() from curve_draw
  - Rendering via pycairo for anti-aliased bezier curves (2x render, LANCZOS downscale)
  - Lee's gesture spec (gesture_pose_analysis_c50.md) drives all pose construction
  - B1 IDLE/CURIOUS: forward C-curve, 60/40 weight front, head tilt, hoodie settle
  - B2 SPRINT ANTICIPATION: strong forward lean C-curve, arms back, wide stance, hair pre-trail
  - B3 DISCOVERY REACTION: backward C-curve (Lee's SURPRISED spec), 70/30 back foot,
    asymmetric arms (one defensive up, one flung), front foot lifted 12px, shoulder hunch
  - B4 LANDING/STOP: subtle S-curve, hoodie flare +8px follow-through, hair trail +16px
  - All panels have visible gesture spine (dashed red) with anchor dots
  - Beat badges: BEAT_COLOR (80,120,200) fill — passes lint >=15% threshold
  - PIL annotation overlay: timing blocks, motion arrows, gesture descriptions
- `ArmGeometry` class + `compute_arm_geometry()` — draw_shoulder_arm v2 geometry-compute layer
  - Pure geometry computation separate from rendering
  - Works with gesture spines (shoulder position from body_from_spine, not rectangle torso)
  - Implements Shoulder Involvement Rule via shoulder shift from arm angle
  - Returns ArmGeometry with: shoulder, elbow, hand positions, deltoid, widths
- `render_arm_cairo()` — cairo renderer for ArmGeometry
  - Deltoid bump (hoodie/cardigan/fitted/bare modes)
  - Two-segment tapered limbs (upper + forearm with elbow bend)
  - Hand circle at wrist
- Lint: PASS=6 WARN=0 FAIL=0 (all checks pass — was PASS=5 WARN=1 before badge fix)
- Inbox: C52 assignment read and archived
- Ideabox: `20260331_ryo_hasegawa_arm_geometry_v2_pil_renderer.md`

### C52 Key Findings
- gesture_spine() + body_from_spine() pipeline scales to all 4 motion sheet panels
- Different gesture params per panel produce visually distinct poses (unlike old generator)
- head_r = 32 at PANEL_W scale (not 22) gives proper figure-to-frame ratio
- RENDER_SCALE=2 + LANCZOS produces clean anti-aliased output at 1280x720
- Beat badge must use BEAT_COLOR (not LABEL_BG) for lint detection — dark fills invisible to _count_non_bg legacy path
- compute_arm_geometry() successfully decouples geometry from rendering — next step is render_arm_pil() for non-cairo generators
- The gesture-first approach gives each panel a UNIQUE silhouette — old generator had identical silhouettes across all 4 panels
- draw_gesture_luma() is reusable: any motion beat can be constructed by changing gesture_params dict
- Hoodie flare and hair trail are secondary motion cues that work naturally with the gesture system (offsets from spine-derived landmarks)

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
