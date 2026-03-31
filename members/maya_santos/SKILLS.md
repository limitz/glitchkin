# Maya Santos — Skills

## Role & Skills
- Character artist & QA tool builder. pycairo primary (bezier, 2x→LANCZOS→1x), PIL for legacy/compositing.
- Libraries: numpy, OpenCV (BGR→RGB on load!), PyTorch, Pillow (canonical I/O).

## Tools Owned (active)
| Tool | File | Ver |
|---|---|---|
| Luma canonical renderer | `LTG_TOOL_char_luma.py` | v1.5.0 |
| Miri canonical renderer | `LTG_TOOL_char_miri.py` | v1.0.0 |
| Luma canonical test sheet | `LTG_TOOL_luma_canonical_test.py` | v1.0.0 |
| Luma turnaround | `LTG_TOOL_luma_turnaround.py` | v007 |
| Character lineup | `LTG_TOOL_character_lineup.py` | v011 |
| Miri expression sheet | `LTG_TOOL_grandma_miri_expression_sheet.py` | v008 |
| Miri turnaround | `LTG_TOOL_miri_turnaround.py` | v001 |
| Silhouette tool | `LTG_TOOL_expression_silhouette.py` | v003 |
| Multi-char face gate | `LTG_TOOL_multi_char_face_gate.py` | v1.0.0 |
| Char diff | `LTG_TOOL_char_diff.py` | v001 |
| Face curve validator | `LTG_TOOL_face_curve_validator.py` | v001 |

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

## Luma Arm Draw Order Per View (C62)
- `ls_pt` = canvas-left shoulder attachment; `rs_pt` = canvas-right.
- **Side-R (facing right):** back=ls_pt first, front=rs_pt last. Character's LEFT = near = rs_pt.
- **Side-L (facing left):** back=rs_pt first, front=ls_pt last. Character's RIGHT = near = ls_pt.
- **3/4 (facing right):** far=rs_pt first, near=ls_pt last. Character's LEFT = near = ls_pt.
- **Hip seam (all views):** `hip_bridge_y_top = torso_bot_y` — hoodie fill covers seam. No gap math.
- **3/4 legs:** `near_leg_x = fl_x (hip_cx - offset)` = character's LEFT = near in 3/4 right-facing.

## Luma Construction Rules (C54/C61)
- **Body join**: Legs overlap torso: `fl_top = (x, torso_bot_y - leg_w_top * 0.8)`. Hip bridge ellipse fills junction (fill=PANTS). Unified arm: `_draw_unified_arm(ctx, upper + fore[1:], w_sh, w_wrist, fill, lw)` — `[1:]` avoids duplicate elbow. `shoulder_open=True` (default) strokes outer silhouette only.
- **Brow ridge**: Add `brow_f = cos(angle - (-pi/6))^12 * 0.06 * head_r` to rx in side-R head loop. For side-L use `cos(angle - (pi + pi/6))^12`. For 3/4 use `cos(angle - (-pi/5))^10 * 0.04`.
- **Nose free-edge stroke**: Fill nose shape first with SKIN, then stroke ONLY the outer arc (not endpoints touching face). Do NOT use `fill_preserve()` + `stroke()` on a closed/full path — creates "stuck on" look.
- **Face-neck blend**: Face skin overdraw must use ry=0.88 (side views) or ry=0.85 (front/3q) to cover neck_top_y at +0.95*head_r below head center. Without this a seam shows at chin.
- **Kid shoulder/torso (C61)**: sh_w=0.75 front, 0.58 3q, 0.40 side/side_l, 0.75 back; w_bot=0.50*head_r front. Old values (0.95/0.70/0.50) read as adult — do NOT revert. Arms in side/3q must be inline code (NOT `_draw_arms()` dispatch — offset tuned for front only). Relaxed arm descent: shoulder+~5s → elbow+~28s → hand+~28s = hand at hip.
- **Hair ear taper (C61)**: Side/side_l hair blobs near ear area (y=0.0 to +0.25, x near face-edge) must use decreasing radii (0.22→0.16→0.12) to taper smoothly. Don't have large blobs (r>0.25) near the face skin edge in the ear zone.

## Key Pitfalls / Gotchas
- **squint_top_r**: Use BG overdraw + lid line, NOT r_open scaling (scales symmetrically = wince not squint). Pass `panel_bg` through render chain.
- **THE NOTICING gaze**: `gaze_dx=-0.5` in EXPR_SPECS is fallback only. Rightward gaze lives in `_FACE_CURVES_OVERRIDES` (LI/RI_CENTER_dx: +6). Do NOT remove either.
- **le_lid_drop / re_lid_drop**: Scalar values in pts_dict, added at RENDER TIME. Extract directly from `pts_dict["re_lid_drop"]`, not as P1 delta.
- **Silhouette RPD**: Column-projection dominated by trunk mass at small panel scale. Arms must extend far beyond body to register. Direction flipping (opposite lean) is most effective differentiator.
- **Arms-mode silhouette FAIL**: Known measurement limit for human chars — shared torso column dominates. Full-mode is the primary production metric.
- **Hairline rule (C58):** Hair blob centers above ~by=-0.55 in front/3q views. Below that = flat cut by face overdraw. Side blobs (x<-0.68) can go lower.
- **Shoulder involvement**: `_shoulder_dy()` = % of arm raise, capped. Torso gains 8 vertices (outer, deltoid_peak, inner × 2 sides + bottom corners).
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

## Profile Face Features (C57/C58)
- Side view nose: `nose_x_base = head_rx * 0.94` — start AT face edge so bump protrudes outside; peak control point at +24s (was +18s before C58)
- Side view mouth: `mouth_x_base = head_rx * 0.62`, `mouth_y = head_r * 0.54`
- Side-L nose: `nose_x_base = -head_rx * 0.94` (C58: was 0.82, now matches side-R), mirrored control points at -14s/-18s
- Side-L mouth: `mouth_x_base = -head_rx * 0.62` (C58: was -0.30, now at face edge to match side-R logic)
- 3/4 nose: visible arc 9s wide + near-side nostril dot; `mouth_y = head_r * 0.56`
- Front nose: upturned arc (-7s to +7s wide) with two nostril dots at ±5s, y=head_r*0.28
- **Mouth y-offsets (C58):** front=0.56, side=0.54, 3/4=0.56, side-L=0.54 (all down from 0.42-0.44)

## Key Production Rules
- Full body in every expression panel (head to feet) — bust format insufficient for silhouette differentiation
- Every expression needs unique SILHOUETTE, not just unique face features
- Backward lean (positive body_tilt) = skeptical/avoidance; forward (negative) = engaged
- Corrugator kink (inner brow UP) = worry; V-brows = aggression
- Bilateral brow raise = surprised; asymmetric = skeptical
- Droopy lid needs parabolic sag curve on lower lid, not just reduced aperture
- Narrative stillness CAN be an expression (total lack of movement = silhouette statement)
