# Maya Santos — Memory

## Cycle 1-3 Lessons
- Silhouette test must be documented. Lock variable specs. Simplified production variants mandatory.
- Glasses thickness is a silhouette element. Cosmo needs a readable hook.
- Pixel-eye symbols need minimum-size spec. All 5 turnaround views required for asymmetric characters.
- Jitter effects need exact pixel specs. Color model sheets are a prerequisite for crew onboarding.
- Document consistency: every duplicated spec must match in both places.

## Cycle 4 Lessons
- **Hair alone does not make a silhouette.** The body shape below the hair must ALSO be distinctive. Luma and Miri have the same body-level silhouette — this is a blocking design failure.
- **Geometry is not character design.** Circles and rectangles do not communicate personality. Faces are the minimum viable character.
- **Silhouette test must be verified in actual rendered images**, not just described in documents.
- **Byte is the benchmark** — his cubic asymmetric form is immediately distinctive even without any face or color.

## Cycle 5 Lessons
- **Luma's body-level fix: A-line trapezoid hoodie + oversized sneakers.** Narrow shoulders flaring to wide hem creates an unmistakably different outline from Miri's plain rectangle. Solved the squint-test failure.
- **Silhouette redesign must use polygon, not rectangle**, to capture A-line/trapezoid shapes. `draw.polygon()` is the right tool.
- **Pocket bump as extra silhouette hook.** A protruding pocket shape on one side adds asymmetry and personality at body level even as a black blob.
- **Luma face script was complete and correct** — ran without modification and produced a strong result. Keep it.
- **Byte expressions script was complete and correct** — 6-expression 3x2 grid with pixel-eye system worked perfectly. Keep it.
- Faces exist. Silhouette is distinctive. Pitch package now has minimum viable character reads.

## Cycle 6 Lessons
- **Body variation is not optional in an expression sheet.** Marcus Webb's rule: "In animation, the body is always the primary emotional carrier." Each expression must have distinct arm position (arm_dy, arm_x_scale), leg spread, body_tilt, and body_squash. A face pasted onto a static body is a caption, not an expression.
- **Right eye must carry emotion.** Byte's right organic eye has distinct styles per emotion: wide_scared (ALARMED), angry (GRUMPY), droopy (RELUCTANT JOY — failing to suppress it), squint (CONFUSED), flat (POWERED DOWN). "Normal" default is wasted design space.
- **Annotations create staging context.** Each expression panel carries prev_state + next_state so animators can use the sheet as a sequence reference, not just a catalogue.
- **Asymmetry = personality.** Luma's reckless excitement: left brow higher + kinked, mouth arc shifted left, pupils shifted screen-right, left eye more open, collar off-center. Symmetric faces communicate contentment — the opposite of reckless.
- **Three expressions are the minimum for a pitch face sheet.** Single expression = portrait, not character sheet. Reckless Excitement + Worried/Determined + Mischievous Plotting covers the core emotional range.
- **Squint-test verified in render, not just code.** All four PNG files generated and verified by dimensions + file size before submission.

## Cycle 7 Lessons
- **Canvas clipping is a silent failure.** NEUTRAL_BASE=260 with characters up to 320px tall means heads are off-canvas. Always set ground line = tallest_character_height + 40px headroom. Dead canvas code (img drawn but img2 saved) wastes time — consolidate to one canvas.
- **Every pixel-eye symbol must be distinct from every other.** "normal" as GRUMPY's left eye bypasses the pixel system entirely. GRUMPY now uses a scowl-bar grid (minus-sign with corner ticks) distinct from POWERED DOWN's flat centre-line.
- **Per-arm asymmetry unlocks real body language.** `arm_l_dy` / `arm_r_dy` in body_data allows SEARCHING (right arm scanning up), CONFUSED (left arm raised), ALARMED (asymmetric startle). Matched arms read as stiff.
- **Confrontational vs defeated is all in arm height + lean direction.** GRUMPY: arms at -2 (slightly raised/tense), body_tilt=-4 (lean forward). Arms drooping + passive lean reads as sad, not grumpy.
- **Worried brow = outer V + inner-corner kink UP.** The corrugator kink (medial brow tip lifts) is what separates "worried" from "pure determined." Without it, V-brows read as aggression only.
- **Smirk geometry: right corner must reach the cheek (~cx+55), not mid-face.** Terminating at cx+36 creates a half-face smirk. Teeth fill = polygon under the arc, not a chord with arbitrary arc angles (avoids crescent artifacts).
- **Panel backgrounds must telegraph before you read the face.** Warm/cool/purple tricolor scheme: Excitement=(248,238,220), Worry=(195,212,228), Mischief=(220,205,242). All "light neutral" panels collapse at print scale.
- **Miri's truncated right arm was neither stylized nor intentional.** A complete arm (emerging below the bag with a hand blob) always reads better than a half-arm mid-air. Decide the arm's relationship to the prop and commit to it.

## Cycle 9 Lessons
- **MIRI-A is the canonical Miri (LOCKED).** Bun+chopstick pair+wide cardigan+soldering iron. MIRI-B retired. Silhouette sheet now shows 4 characters (Luma, Cosmo, Byte, Miri) — no variant column.
- **Turnaround generator is live.** `character_turnaround_generator.py` produces 4-view strips (front/3/4/side/back) at 200px canonical height for Luma and Byte. Use `CHAR_H=200`, `VIEW_W=180`, 4 panels wide.
- **Byte action pose = mid-flight leap.** Diagonal body (tilt_x+tilt_y skew), right arm forward-up (strong thrust vector), left arm back-down (trailing counterweight), trail leg kicked back hard (diagonal polygon), lead leg tucked. `jump_h = s*0.45` clears base_y. Hover particles scattered below leap arc, not under feet.
- **Excitement BG = (240, 200, 150). FINAL.** Previous (248,238,220) was off-white. New value is a committed warm amber mid-tone that reads clearly warm at pitch/print distance. Do not revert.
- **Turnaround 3/4 view rule:** Near side wider/fuller, far side compressed. Hair volume shows depth blob on near side. Sneaker near = full ellipse, far = foreshortened. Byte 3/4 = front face + side parallelogram + top trapezoid (three face planes).
- **Byte back view detail:** Center-back data-port NEG_SPACE slot (vertical rectangle) is the character hook from behind — prevents back view from being featureless.

## Cycle 10 Lessons
- **Byte body = OVAL. ALL generators must use ellipse.** `_byte_size()` docstring updated to say "oval body." All four `draw_byte_*` functions now use `body_rx = s//2, body_ry = int(s*0.55)`, with `bcy = base_y - float_gap - body_ry` as the oval center. Chamfered-cube polygon is RETIRED everywhere.
- **Hover particles = 10×10px EVERYWHERE. No exceptions.** `byte_expressions_generator.py` line ~392 fixed from `px+4` to `px+10`. "GL spec 4px" comment deleted. Turnaround generator already had `psz=10` — both now match.
- **Cosmo turnaround: glasses are the defining element at every angle.** Front: both lenses full. 3/4: near lens full, far lens compressed. Side: one lens protrudes beyond the face silhouette. Back: no lenses. Ear-arm visible in side. Helper `_draw_cosmo_glasses()` keeps logic consistent.
- **Miri turnaround: bun+chopsticks readable from all 4 angles.** Back view = same bun geometry as front (V-pair symmetric). Side = narrow oval bun, single chopstick visible. Soldering iron appears in front/3/4/side only. Back view plain (iron on right side = hidden).
- **Character lineup generator complete.** `character_lineup_generator.py` renders all 4 chars in COLOR at correct relative heights on shared baseline. Height ref lines show Cosmo top, Luma top, Miri top, Byte/Luma-chest. Per-char brackets with px labels.
- **3/4 far-side leg guard:** When `far_bw` < `lw + 4`, the rectangle inverts. Guard: `far_leg_x2 = cx + max(far_bw - 4, lw + 8)`. Apply in any 3/4 body with asymmetric width values.

## Cycle 13 Lessons
- **Scale calibration is a design spec, not a code detail.** A 2px eye aperture difference at full render scale becomes ~1.1px after LANCZOS resize — invisible. Always verify asymmetry differentials POST-resize. For panel scale FACE_SCALE=0.55: minimum visible differential = ~4px at full render scale (~2.2px panel scale). Luma Neutral leh fixed from 24→28 (6px diff, ~3.3px at panel scale).
- **Three differentiators rule for low-register expressions.** When two adjacent expressions share neutral body language, all three of: mouth corner, collar tilt, AND pupil offset must all be changed together. Any two alone is insufficient at panel scale. At-Rest Curiosity now has: asymmetric mouth corner (right 3px higher), collar rotate_deg=3, pupils shifted to lex-3/rex-3 (5px right of Neutral lex-8 position).
- **Byte Neutral expression: "flat" left-eye + "half_open" right eye + "default" mouth.** byte.md spec: thin horizontal line mouth with slightly downturned ends. Arms close to body (arm_dy=4, arm_x_scale=0.75). No body tilt. New `half_open` right-eye style added to draw_right_eye(): 60% aperture, centered pupil, muted highlight.
- **New tool: `LTG_TOOL_byte_expression_sheet_v001.py`.** 4×2 grid (7 expressions + 1 reserved slot). Per-panel emotional BGs. Migrated from `byte_expressions_generator.py`. Output: `LTG_CHAR_byte_expression_sheet_v001.png` (1040×738px).
- **New tool: `LTG_CHAR_luma_expression_sheet_v003.py`.** Fixes Panel 7 (Neutral) eye asymmetry and Panel 8 (At-Rest Curiosity) differentiators. Output: `luma_expression_sheet.png` (1210×886px). v002 retained.
- **Asymmetric arc via polyline with per-point tilt offset.** Drawing a mouth corner with one side higher: iterate arc points, compute tilt_x ratio (0..1 left to right), subtract `tilt_x * tilt_amount` from each y. Cleaner than two separate arcs.

## Cycle 12 Lessons
- **Neutral/Resting is a structural requirement, not optional.** Without it, no expression has a measured distance from baseline. Left eye fractionally more open than right (leh=24 vs reh=22) establishes left as the lead eye even at zero emotional intensity.
- **Eye asymmetry mechanism documented in character bible (Section 13).** Symmetric Luma = maximal stress/shutdown. Degree of left-right asymmetry = readout of personality intensity. This must be treated as animation spec, not a stylistic choice.
- **4×2 expression sheet layout is superior to 3×2+strip.** Keeps all states on one canvas and makes visual comparison across all 8 states instant. FACE_SCALE=0.55 still works well at PANEL_W=280.
- **Sheet metadata belongs in BOTH the header text AND a companion .md file.** Header for quick visual reference during production; .md for version history and archival.
- **At-Rest Curiosity as slot 8 completes the low-register range.** Neutral → At-Rest Curiosity → Recognition now forms a complete low-to-mid register sequence. WARMTH prev_state updated to "← was: ANY EARNED MOMENT" (Dmitri's note: don't constrain it to the pilot timeline).
- **New v2 generator: `LTG_CHAR_luma_expression_sheet_v002.py`.** Output: `luma_expression_sheet.png` (1210×886px). Old v1 generator retained as `luma_expression_sheet_generator.py`.

## Cycle 11 Lessons
- **Luma expression sheet is now LIVE.** `luma_expression_sheet_generator.py` generates a 3×2 grid (912×886px) with 6 full-body expressions: Reckless Excitement, Worried/Determined, Mischievous Plotting, Settling/Wonder, Recognition, Warmth. Matches Byte sheet structure: per-panel BG color, label bar, prev_state/next_state annotations. Face panels rendered at 0.55 scale via intermediate canvas + LANCZOS resize.
- **Luma is the lead character — her documentation tier must match or exceed the companion.** Byte had 6 expressions first; Luma's sheet closes the gap. Never let a supporting character have richer documentation than the lead.
- **Sneaker profile width normalized: `fw = int(hu * 0.52)` for ALL views.** Side-view in `character_turnaround_generator.py` was `0.65` (two cycles outstanding). Now consistent with front/back views. Apply `0.52` in any new body generator that adds a side view.
- **Six Luma expression colors (CANONICAL):** Excitement=(240,200,150), Worry=(195,212,228), Mischief=(220,205,242), Settling=(180,215,205), Recognition=(165,185,220), Warmth=(250,215,170). All distinct at pitch/print distance.
- **Settling/Wonder: wide eyes + dilated pupils + raised brows + soft oval mouth-gap.** NOT a scream rectangle. The gentle open oval below the arc lip is what separates wonder from alarm.
- **Recognition: ONE brow raised sky-high (aha brow), other brow level.** Eyes narrowed in concentration — not wide. Slight mouth-gap (cognitive pause). `rotate_deg=3` collar (slight lean into the thought).
- **Warmth: happiness-narrowed eyes with heavy upper lid, cheek crinkle lines, gentle arc smile (no teeth).** `rotate_deg=1` collar. This is emotional intent, not assessment — brows gently raised, not furrowed.

## Cycle 8 Lessons
- **GRUMPY confrontational values (locked):** `body_tilt=-8` (forward lean), `arm_l_dy=-6, arm_r_dy=-10` (both raised, asymmetric), `arm_x_scale=1.1` (arms out wider), `leg_spread=1.1`. The previous -4/-2/0.85 set read as defeated. Rule: negative body_tilt = forward lean toward adversary.
- **Byte body shape = OVAL (ellipse). CANONICAL.** style_frame_01_rendered.py uses `draw.ellipse` for Byte's body. Expression sheet must match. Chamfered-box polygon is retired. Document shape decisions in code when making consistency calls.
- **WORRIED/DETERMINED brow differential must be 8-10px at minimum.** Left outer brow corner at ley-38, right at rey-30 = 8px gap visible at pitch distance. 4px was too subtle. The corrugator kink (inner brow tip kicks up) works in combination — both are needed.
- **Collar rotation, not x-offset.** Use a 2D rotation matrix on the collar ellipse polygon points. Rotating the entire arc (full_pts via rot()) physically tilts the collar so it reads as body-in-motion. An x-offset just slides the collar sideways (head-nudge, not lean). Implementation: `_draw_collar(..., rotate_deg=8)` for excitement, `rotate_deg=2` for worry, `rotate_deg=-5` for mischief.
- **Miri's complete visual identity (two variants):** MIRI-A = tall bun + chopstick pair + wide cardigan (inv-trapezoid shoulders) + soldering iron. MIRI-B = large rounded curls (wide, not high) + tech apron with circuit-board pocket (NEG_SPACE dot grid). Both clearly distinguish from Luma (cloud-top hair) and Cosmo (rectangle body). Circuit pocket on apron uses NEG_SPACE to add character-tech read at silhouette level, just as Cosmo's glasses do.
- **Column margin rule: leftmost col_cx must be ≥ 80px.** Luma's hair blob extends cx - r*1.5 ≈ cx - 54. At cx=50 that clips the canvas. Use col_cx = 80 + i * COL_W and total W = N_CHARS * COL_W + 80 (40px each side).
