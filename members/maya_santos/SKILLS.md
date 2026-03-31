# Maya Santos — Skills

## Role & Skills
- Character artist and QA tool builder for Luma & the Glitchkin
- PIL/pycairo rendering, expression sheets, turnarounds, color models, silhouette QA
- Engines: pycairo (primary for new work, bezier curves, LANCZOS downscale from 2x), PIL (legacy tools)
- Libraries authorized: numpy, OpenCV (BGR→RGB on load!), PyTorch, Pillow (canonical I/O)

## Tools Owned
| Tool | File | Version | Notes |
|---|---|---|---|
| **Luma canonical renderer** | `LTG_TOOL_char_luma.py` | v1.4.0 | Modular `draw_luma()`, 7 expressions, pose_mode (front/3q/side/side_l/back), kid shoulders, brow-ridge forehead, nose free-edge stroke, hair ear taper, face-neck blend |
| **Miri canonical renderer** | `LTG_TOOL_char_miri.py` | v1.0.0 | Modular `draw_miri()`, pycairo rebuild, 6 expressions |
| Luma canonical test sheet | `LTG_TOOL_luma_canonical_test.py` | v1.0.0 | 7-expr front-view sheet, uses draw_luma() modular API |
| Luma cairo expressions | `LTG_TOOL_luma_cairo_expressions.py` | v2.0.0 | 6-expression sheet, pycairo engine (superseded by char_luma) |
| Luma expression sheet (legacy PIL) | `LTG_TOOL_luma_expression_sheet.py` | v014 | Superseded by cairo for Luma |
| Cosmo expression sheet | `LTG_TOOL_cosmo_expression_sheet.py` | v008 | Cowlick + tape + shoulders |
| Cosmo turnaround | `LTG_TOOL_cosmo_turnaround.py` | v003 | Cowlick + tape all views |
| Miri expression sheet | `LTG_TOOL_grandma_miri_expression_sheet.py` | v008 | Elder posture |
| Miri turnaround | `LTG_TOOL_miri_turnaround.py` | v001 | |
| Byte expression sheet | `LTG_TOOL_byte_expression_sheet.py` | v007 | |
| Glitch expression sheet | `LTG_TOOL_glitch_expression_sheet.py` | v003 | 9 expressions incl. interior desire |
| Glitch body diagram | `LTG_TOOL_glitch_body_primitive_diagram_gen.py` | v001 | |
| Character lineup | `LTG_TOOL_character_lineup.py` | v011 | Two-tier staging, Cosmo visual hook |
| Luma turnaround | `LTG_TOOL_luma_turnaround.py` | v007 | 5 distinct views (front/3q/side/side-L/back), C55, all native renders |
| SF06 Miri-Luma handoff | `LTG_TOOL_sf_miri_luma_handoff.py` | C49 | Elder posture + shoulder displacement |
| Multi-char face gate | `LTG_TOOL_multi_char_face_gate.py` | v1.0.0 | Exports `run_multi_char_face_gate()` |
| Visual hook audit | `LTG_TOOL_visual_hook_audit.py` | v1.0.0 | |
| Silhouette tool | `LTG_TOOL_expression_silhouette.py` | v003 | RPD metric, `--viz-rpd`, `--output-zones` |
| Expression isolator | `LTG_TOOL_expression_isolator.py` | v001 | Single expr at 800x800 |
| Body hierarchy | `LTG_TOOL_bodypart_hierarchy.py` | v002 | `--panel N`, `--chain` |
| Face curve validator | `LTG_TOOL_face_curve_validator.py` | v001 | All 10 Luma expressions PASS |
| Char diff | `LTG_TOOL_char_diff.py` | v001 | Proportion drift detection |
| Luma color model | `LTG_TOOL_luma_color_model.py` | v002 | |
| Elderly proportion ref | `LTG_TOOL_elderly_proportion_reference.py` | v1.0.0 | |
| Luma turnaround | `LTG_TOOL_luma_turnaround.py` | v003 | |

## Character Specs

### Luma (3.2 heads)
- Head 37% of body, eyes 30% of head width, cloud hair 17 overlapping ellipses
- Bean torso (cubic bezier), tapered tube limbs, variable-width strokes
- Eye width canonical: `ew = head_r * 0.22` (HR=105→ew=23px at 1x)
- Right-eye lid drop asymmetry is Luma's signature (re_lid_drop=6 in NEUTRAL)
- Orange hoodie primary, A-line trapezoid shape, pixel accent on chest
- Mitten hands in all rough/reference poses

### Cosmo (4.0 heads)
- Cowlick 0.15 heads tall, glasses bridge tape TAPE_COL=(250,240,220)
- Glasses tilt per expression (7°-10° range, S003 spec max 7°±2°)

### Miri (3.2 heads)
- MIRI_HEAD_RATIO=3.2 explicit constant, 88% circular head
- Wooden hairpins (NOT chopsticks), color (92,58,32)
- Elder posture: ELDER_LEAN_DX ~5px, ELDER_SHOULDER_DROP=3px, ELDER_SHOULDER_INWARD=2px
- Permanent blush (0.0 for CONCERNED only), round glasses always on

### Byte
- Body = OVAL (ellipse), CANONICAL. Body fill = #00D4E8 BYTE_TEAL (GL-01b)
- Hover particles = 10x10px everywhere
- Pixel eye 3x3 grid; crack = void-black overlay LINE, not a pixel state
- STORM arms asymmetric (6,22); RESIGNED symmetric (14,14)

### Glitch
- Diamond body: rx=34, ry=38, ry>rx always
- Confetti: HOT_MAG/UV_PURPLE only (never cyan/acid)
- Right eye = destabilized bleed of left = corruption read
- Shadow facets: use CORRUPT_AMB_SH (not UV_PURPLE) on dark backgrounds

## Body Connectivity Pattern (C54)
- Legs must overlap torso bottom: `fl_top = (x, torso_bot_y - leg_w_top * 0.8)`
- Hip bridge fills junction: filled ellipse-ish shape spanning both leg tops, fill=PANTS
- Unified arm silhouette: combine upper+forearm bezier pts into one list, call `_draw_unified_arm()`
  — `_draw_unified_arm(ctx, upper + fore[1:], w_shoulder, w_wrist, fill, line_col, lw)`
  — The `[1:]` on fore avoids duplicate elbow point
  — Wrist cap: `ctx.arc(all_pts[-1], w_wrist, 0, pi)` rounds the end

## Profile Head Shape Rules (C61)
- **Brow ridge**: Add `brow_f = cos(angle - (-pi/6))^12 * 0.06 * head_r` to rx in side-R head loop. For side-L use `cos(angle - (pi + pi/6))^12`. For 3/4 use `cos(angle - (-pi/5))^10 * 0.04`.
- **Nose free-edge stroke**: Fill nose shape first with SKIN, then stroke ONLY the outer arc (not endpoints touching face). Do NOT use `fill_preserve()` + `stroke()` on a closed/full path — creates "stuck on" look.
- **Face-neck blend**: Face skin overdraw must use ry=0.88 (side views) or ry=0.85 (front/3q) to cover neck_top_y at +0.95*head_r below head center. Without this a seam shows at chin.
- **Kid shoulder width**: sh_w=0.75 front, 0.58 3q, 0.40 side/side_l, 0.75 back. Old values (0.95/0.70/0.50) read as adult — do NOT revert.
- **Hair ear taper (C61)**: Side/side_l hair blobs near ear area (y=0.0 to +0.25, x near face-edge) must use decreasing radii (0.22→0.16→0.12) to taper smoothly. Don't have large blobs (r>0.25) near the face skin edge in the ear zone.

## Key Pitfalls / Gotchas
- **squint_top_r**: Use BG overdraw + lid line, NOT r_open scaling (scales symmetrically = wince not squint). Pass `panel_bg` through render chain.
- **THE NOTICING gaze**: `gaze_dx=-0.5` in EXPR_SPECS is fallback only. Rightward gaze lives in `_FACE_CURVES_OVERRIDES` (LI/RI_CENTER_dx: +6). Do NOT remove either.
- **le_lid_drop / re_lid_drop**: Scalar values in pts_dict, added at RENDER TIME. Extract directly from `pts_dict["re_lid_drop"]`, not as P1 delta.
- **Silhouette RPD**: Column-projection dominated by trunk mass at small panel scale. Arms must extend far beyond body to register. Direction flipping (opposite lean) is most effective differentiator.
- **Arms-mode silhouette FAIL**: Known measurement limit for human chars — shared torso column dominates. Full-mode is the primary production metric.
- **6-expression sheets**: 15 pairs to check (vs 1 for 2-panel). Structurally harder to pass silhouette.
- **Shoulder involvement**: `_shoulder_dy()` = % of arm raise, capped. Torso gains 8 vertices (outer, deltoid_peak, inner x 2 sides + bottom corners).
- **Hairline rule (C58):** Hair blob centers must stay above ~by=-0.55 in front/3q views. Face skin ellipse top is at ~-0.60 to -0.72 depending on view — blobs extending lower than that get cut by face overdraw creating a flat hairline edge. Side blobs (at x<-0.68) can go lower (ear-area).
- **Copyright headers**: ONLY on files inside `output/`. Nowhere else.
- **Image size rule**: All output PNGs <=1280px on longest side. Use PIL thumbnail with LANCZOS.
- **OpenCV**: Uses BGR by default — always `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` on load.
- **Dark BG shadow rule**: UV_PURPLE disappears on dark void. Use CORRUPT_AMB_SH instead.
- **Hierarchy tool false positives**: Uses Luma color index — non-Luma chars produce palette FAILs. Not real defects.
- **char_spec_lint pattern mismatch**: Looks for `LTG_TOOL_grandma_miri_expression_sheet_v*.py` but file has no version suffix — Kai should fix.

## Three-Tier Line Weight (2x render, canonical)
- Head outline: width=4 (~2px at 1x)
- Structure (torso, arms, legs, eye ovals, brows, mouth): width=3 (~1.5px)
- Detail (nose, laces, crinkles): width=2 (~1px)
- Hair strand arcs: width=3 (NOT 6). width=6 = manga/overworked.

## Modular Renderer Pattern (C53/C54)
- Canonical renderer per character: `LTG_TOOL_char_X.py`
- Public: `draw_X(expression, pose, scale, facing, scene_lighting, pose_mode) -> cairo.ImageSurface`
- Context: `draw_X_on_context(ctx, cx, ground_y, char_h, expression, pose)` for sheets/scenes
- All return ARGB32 transparent bg. `cairo_surface_to_pil()` for PIL conversion.
- GESTURE_SPECS dict per character: offset chain values from Lee's specs
- Miri: MIRI_BASE_LEAN = -4 adds to per-expression torso_lean. Never vertical.

## Pose Mode Architecture (C55/C57)
- `pose_mode` param on `draw_luma()`: "side" | "front" | "threequarter" | "back" | "side_l"
- **side_l**: native left-facing profile via `_draw_luma_side_l()`. NOT a ctx.scale(-1,1) mirror.
  Uses reversed weight distribution, distinct arm poses, left-facing profile head.
  Back of head is on +x side; nose bump protrudes at -x; eye at -head_rx*0.28.
- **Arm-shoulder seam fix**: `_draw_unified_arm(..., shoulder_open=True)` (default True).
  Fill is always a closed path. Stroke is open at shoulder end — only strokes the outer
  silhouette edges. The torso lw_silhouette stroke covers the junction. No double outline.
- **True profile side/side-L head**: uses custom point loop. Back of head: `rx += head_r*0.14 * back_f`
  (back_f = cos(angle)^4 for right-facing). Face side: `rx -= head_r*0.06 * face_f` (face_f = cos(angle-pi)^8).
  ONE eye, positioned toward face direction at +/-head_rx*0.28. Profile nose: bezier bump at face edge.
- **3/4 leg stagger**: near_leg_x = hip_cx + 0.20*head_r, far_leg_x = hip_cx - 0.25*head_r.
  Far foot gets extra +0.06*head_r lift. Far leg drawn first (behind). Both legs near center-x.
- **Side view leg stagger**: near_leg_x = hip_cx + 0.18*head_r, far_leg_x = hip_cx - 0.14*head_r.
  Both near center-x — NOT spread left/right (that's front view). Far foot extra lift = head_r*0.04.

## Torso Foreshortening Ratios (C61 — kid proportions)
- Front view: sh_w=0.75*head_r, w_bot=0.50*head_r (narrower — 12yo kid, not adult)
- 3/4 view:   sh_w=0.58*head_r, w_bot proportional (~77% of front)
- Side view:  sh_w=0.40*head_r (~53% of front)
- Side-L:     sh_w=0.40*head_r (matches side — same angle)
- Back view:  sh_w=0.75*head_r (matches front)
- **Arms in side/3/4 must be inline (NOT `_draw_arms()`)**: the `_draw_arms()` dispatch
  uses offsets tuned for front view — they push hands up near head in profile views.
  Side and 3/4 arm code is written inline, same pattern as side-L.
  Relaxed arm descent: shoulder+~5s drop → elbow+~28s → hand+~28s = hand at hip (≈61s below ls_pt[1])

## Profile Face Features (C57/C58)
- Side view nose: `nose_x_base = head_rx * 0.94` — start AT face edge so bump protrudes outside; peak control point at +24s (was +18s before C58)
- Side view mouth: `mouth_x_base = head_rx * 0.62`, `mouth_y = head_r * 0.54`
- Side-L nose: `nose_x_base = -head_rx * 0.94` (C58: was 0.82, now matches side-R), mirrored control points at -14s/-18s
- Side-L mouth: `mouth_x_base = -head_rx * 0.62` (C58: was -0.30, now at face edge to match side-R logic)
- 3/4 nose: visible arc 9s wide + near-side nostril dot; `mouth_y = head_r * 0.56`
- Front nose: upturned arc (-7s to +7s wide) with two nostril dots at ±5s, y=head_r*0.28
- **Mouth y-offsets (C58):** front=0.56, side=0.54, 3/4=0.56, side-L=0.54 (all down from 0.42-0.44)

## Pose Mode Architecture (C54)
- `pose_mode` param on `draw_luma()`: "side" | "front" | "threequarter" | "back"
- Each mode has its own render function: `_draw_luma_front`, `_draw_luma_threequarter`, `_draw_luma_back`
- "side" = existing `_draw_luma_on_context` (unchanged)
- Front: symmetric torso (sh_w=0.95 head_r), both eyes equal, no offset chain, nose = dot
- 3/4: near eye full, far eye foreshortened (rx=0.14 head_r), offset chain 50% of side
- Back: hair covers face area (extra blobs at y=0, y=0.2), no face, nape crease, back seam
- `facing="left"` flip only applies to "side" and "threequarter" modes

## Key Production Rules
- Full body in every expression panel (head to feet) — bust format insufficient for silhouette differentiation
- Every expression needs unique SILHOUETTE, not just unique face features
- Backward lean (positive body_tilt) = skeptical/avoidance; forward (negative) = engaged
- Corrugator kink (inner brow UP) = worry; V-brows = aggression
- Bilateral brow raise = surprised; asymmetric = skeptical
- Droopy lid needs parabolic sag curve on lower lid, not just reduced aperture
- Narrative stillness CAN be an expression (total lack of movement = silhouette statement)
