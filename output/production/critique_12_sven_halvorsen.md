# Critique 12 — Lighting, Compositing, and Visual Effects
**Critic:** Sven Halvorsen
**Date:** 2026-03-29
**Scope:** Style frames SF01–SF04, environment spot-checks, procedural draw library

---

## Method

I read each generator to reconstruct the implied light setup, then compared what the code produces against the stated intent. Every gap between specification and implementation is a numbered line item. I do not estimate — I read the draw calls.

---

## SF01 — The Discovery (v003)
**Rating: WARN**

**Implied light setup from spec:**
- Warm amber lamp at upper centre-left (approx. x=W×0.40, ceiling level)
- Cool Elec Cyan emanating from monitor wall (right half of frame)
- Two-zone warm/cool split

**Code analysis:**

### Inconsistency 1 — Lamp position vs. shadow direction on Luma's face
The lamp is placed at x≈768 (W×0.40), near ceiling, centre-left of frame. Luma stands at x≈W×0.29 — to the *left* of the lamp. The light therefore arrives from Luma's right side, upper. The face shader in `draw_luma_head()` runs a left-to-right horizontal gradient: `t_x = (col - cx) / max(1, rx)` with `w_f = 0.5 + 0.5 * t_x`, mapping SKIN (darker) on the left to SKIN_HL (lighter) on the right. This is correct in direction. However, the gradient is purely horizontal with no vertical component. The lamp is at ceiling height — it should cast a significant top-down component as well as lateral. There is no brow shadow, no nose shadow, no chin underside in shadow. The face receives only a flat horizontal gradient, which does not correspond to a point source at upper-centre-right.

**Expected:** shadow on Luma's left upper face (brow ridge), lit zone on right cheek/forehead with downward falloff.
**Found:** uniform horizontal gradient only.

### Inconsistency 2 — Lamp glow does not project onto Luma's body
The warm atmospheric overlay `draw_lighting_overlay()` fills the left half of the frame with a SOFT_GOLD ellipse centred at x≈768 (lamp), y≈H×0.35. Luma's torso occupies x≈W×0.23–0.35 and the warm overlay is cropped to x < W/2 = 960. The warm light does reach Luma's torso zone. However, `draw_luma_body()` renders the hoodie as a linear left-to-right pixel scan blending HOODIE_ORANGE → HOODIE_CYAN_LIT. The cyan-lit side is `x_right`, i.e. the right side of the torso. Luma faces the monitor (right). So the right side of Luma's torso is the monitor-facing side, correctly receiving cool teal. The left side should receive warm lamp light. But the warm atmospheric overlay is a radial fill composited before the character is drawn — the character is painted over it, flat. The warm atmospheric overlay never modulates the character paint. Luma's left arm is painted with CYAN_SKIN (a teal-warm blend, R=122 G=188 B=186), which reads as teal, not as warm lamp illumination. A character lit from upper-left by a warm amber lamp should not have teal-coloured left-facing skin surfaces.

**Expected:** Left arm and left torso face in warm HOODIE_ORANGE range; any cool tint reserved for right-facing surfaces.
**Found:** Left arm painted CYAN_SKIN (teal), contradicting warm-left lamp position.

### Inconsistency 3 — Warm/cold overlay split origin does not match lamp position
The warm overlay is centred at `lamp_glow_cx = lamp_x + 32` ≈ x=800, which is lamp x + 32. The lamp is at W×0.40 = 768. The centroid of the warm glow is at x=800, which is in the middle of the frame. The cold overlay from the monitor wall spans from `W//2 - 80` to W. These two zones overlap from x=880 to x=960. In this overlap band, both warm and cold overlays composite together — the zone reads as neutral or muddied rather than one temperature winning. There is no defined boundary or linear blend managing the transition. The result is an ambiguous temperature zone at the compositional centre.

### Inconsistency 4 — Byte emerging from CRT: no local light contribution
Byte is drawn emerging from the CRT screen. The CRT emits Elec Cyan. Byte's body is BYTE_TEAL (0, 212, 232). A character emerging from a light source should carry that source's temperature as a strong key on their forward face. The highlight in `draw_byte()` uses `draw_filled_glow()` centred at `byte_cx - int(byte_rx * 0.2), byte_cy - int(byte_ry * 0.25)` — upper-left of Byte's body. The CRT screen is to Byte's right (Byte faces left toward Luma). The specular highlight should be on Byte's right side (screen side), not upper-left. The highlight placement does not correspond to the screen as a light source.

**Expected:** Byte's right-facing surfaces brightest (screen proximity key), left surfaces in shadow.
**Found:** Highlight at upper-left quadrant of Byte body, inconsistent with screen position.

---

## SF02 — Glitch Storm (v004)
**Rating: WARN**

**Implied light setup from spec:**
- Three-tier: cyan crack (upper right, radiating down-left), magenta fill (diffuse storm sky), warm gold windows (domestic, downward cones)
- Window pane glow vs cone glow must be consistent systems

**Code analysis:**

### Inconsistency 5 — Sky crack as light source: no consistent cyan key on building faces
The main crack is defined by `crack_pts` in `_draw_main_crack()`. The crack radiates from approximately x=1400, upper sky, travelling down-left. Buildings are drawn left of centre. The crack is to the upper-right of most buildings. Cyan rim lighting on buildings is applied via `_draw_building_storm_rims()`, which correctly applies STORM_RIM_CYAN to the right-facing edges (`rx` side) of each building, with strength modulated by proximity to crack_x=1400. This is logically consistent.

However, Luma and Cosmo are drawn by `_draw_luma()` and `_draw_cosmo()`. Luma receives a shadow ellipse on the *left* half of the torso (`torso_left, torso_top, cx, torso_bot`). This places shadow on the left. If the crack key light is upper-right, shadow should fall on the lower-left of forms — consistent. However there is no corresponding highlight or fill specular on Luma's right-facing surfaces from the crack source. The `DRW_HOODIE_STORM` fill is flat. There is no differential between left and right sides of the torso other than the shadow on the left half. The right side (crack-facing) should carry a cyan tint highlight. It does not.

**Expected:** Right torso of Luma/Cosmo carries a cyan rim or specular from upper-right crack source.
**Found:** Right torso painted flat DRW_HOODIE_STORM with no cyan contribution.

### Inconsistency 6 — Magenta fill light: no magenta colour temperature present on character surfaces
The spec calls for Hot Magenta as a fill light source. HOT_MAGENTA (255, 45, 107) is used for the storefront frame highlight (`outline=(*HOT_MAGENTA,)`), the crack glow layers, and character hair (`DRW_HAIR_MAGENTA = (106, 42, 58)` — a muted dark, not the actual fill-light temperature). The character skin is painted DRW_SKIN_STORM (106, 180, 174) — a teal-green, representing the cold storm ambient. There is no magenta component anywhere in the character's illuminated surfaces. If magenta is specified as a fill light (the secondary source that illuminates shadow sides and provides warmth in an otherwise cold scene), it should appear as a low-key tint on the fill-side character surfaces. It does not appear at all as a light-colour tint.

**Expected:** Character fill-side surfaces carry a perceptible magenta tint from the fill light.
**Found:** No magenta light contribution on any character surface. Magenta exists only as a line element (crack glow, frame edge, hair accent), not as an illumination value.

### Inconsistency 7 — Window cone vs. window pane glow: two unsynchronised systems
Window pane glow is drawn via `win_colors = [(*SOFT_GOLD, 180), (*WARM_CREAM, 160)]` as opaque-to-semi-transparent filled rectangles. The cone glow below each window is WIN_GLOW_WARM = (200, 160, 80) at alpha 90–110. These two systems use different colours. The pane itself emits SOFT_GOLD (232, 201, 90) at alpha 180 — bright yellow-gold. The cone below it emits (200, 160, 80) at alpha 90–110 — a dimmer amber-orange. A cone of light projected from a pane should be the same colour as the pane at the point of exit and shift toward ambient as it spreads. Instead the cone is distinctly warmer (more orange) and dimmer than the source pane. To a viewer, the cone does not feel like it came from the pane above it. The two systems are not tuned to the same colour temperature.

**Expected:** Cone colour at origin closely matches pane glow colour; gradients away to ambient.
**Found:** Cone at (200, 160, 80) alpha 90–110 is noticeably dimmer and oranger than pane at (232, 201, 90) alpha 180. Temperature and intensity discontinuity.

### Inconsistency 8 — Ground lighting: single cyan source at crack_x=1300, no magenta ground bounce
The ground pool is a single ELEC_CYAN wash emanating from x=1300, spreading left. The spec defines three tiers. There is no warm gold or magenta contribution at street level. In a night exterior with illuminated windows above the street, warm ground bounce from the window cones should be visible on the sidewalk directly below each lit window. The cone geometry correctly reaches the ground (`cone_bot_y = min(gy, horizon_y + 30)`), but `draw_ground_lighting()` only adds cyan. The warm amber cones land on the ground but `draw_ground_lighting()` re-applies only cyan on top of them. The warm pools are partially overwritten.

---

## SF03 — The Other Side (v004)
**Rating: PASS (with reservations)**

**Implied light setup from spec:**
- Zero warm light mandate
- Electric Cyan as key light
- UV Purple atmosphere

**Code analysis:**

### Finding: Zero warm light mandate is enforced
`draw_lighting_overlay()` is explicitly documented "Three light passes — NO WARM LIGHT." The three passes are: UV_PURPLE atmospheric gradient (full frame), ELEC_CYAN rising from the platform base (left 45% of frame), and DATA_BLUE vertical column (36–44% of frame width). No warm colours (reds, oranges, ambers, golds) appear in any overlay pass. The character palette uses SKIN_UV_MOD and HOODIE_UV_MOD — desaturated, UV-shifted. CORRUPT_AMBER debris is present as pigment only, not as a light source. The zero warm light mandate is technically enforced in the lighting passes.

### Inconsistency 9 — Cyan key light direction is not spatially consistent
The ELEC_CYAN overlay rises from the platform level (plat_y ≈ H×0.66) upward, covering the left 45% of the frame. The light reads as rising from below-left. Luma's face shading in `draw_luma()` applies SKIN_SHADOW as a right-side strip (`head_x + head_w - shadow_w, head_top` to `head_x + head_w, torso_top`) — right side dark. SKIN_BOUNCE highlight is a strip at the top of the head (`head_top + hi_h`). This places highlight at top, shadow at right. A rising left-side cyan key would place highlight on the left face and lower surfaces (upward component), not at the top. The shadow would fall on the right and downward surfaces. The top-edge highlight is inconsistent with a below-left source.

**Expected:** Luma's face shows lit left cheek/jaw (from rising left cyan), dark right and upper surfaces.
**Found:** Highlight at top of head, shadow at right edge — implies an overhead or upper-right source.

### Inconsistency 10 — UV Purple atmosphere interacts with Luma as tinted ambient but not with Byte
The UV_PURPLE overlay (full frame, alpha 20–50) modifies all pre-drawn content by tinting it purple. Luma is drawn after the lighting overlay (STEP 7 comment), meaning Luma is drawn on the untinted base. Wait — re-reading the code: `draw_lighting_overlay()` is called in `generate()` and it modifies `img` in place before the character draw calls are made. Checking the draw order in the v004 generator: characters are drawn SEVENTH, after lighting overlay (comment in code confirms "draw SEVENTH — after lighting overlay"). This means Luma and Byte are drawn onto the already-tinted background, then composited over it — they are NOT tinted by the overlay because they are drawn on top of it. As a result, Luma and Byte sit in a UV-tinted world but carry no UV tint themselves. They appear slightly alien to the background. This is a compositing ambient-light mismatch: characters share neither the UV atmosphere nor are they given UV-tinted versions of their surface colours sufficient to explain their presence in that atmosphere.

Note: HOODIE_UV_MOD and SKIN_UV_MOD are provided as palette variants to address this — they are manually tuned UV-shifted colours. This is the correct approach. The issue is whether the manual tuning is sufficient: SKIN_UV_MOD is a fixed colour. The UV overlay changes the background progressively from top to bottom (alpha 20–50). The character's skin does not vary in UV tint with vertical position. A character standing in a volumetric UV atmosphere should show stronger UV tint toward the areas exposed to more atmosphere. The fixed SKIN_UV_MOD cannot model this.

---

## SF04 — Luma + Byte: The Dynamic (v002)
**Rating: WARN**

**Implied light setup from spec:**
- Warm window left (upper-left, RW-03 Sunlit Amber)
- Cool monitor right (GL-01b Byte Teal)
- `add_face_lighting()` for warm window, `add_rim_light()` for cool monitor

**Code analysis:**

### Inconsistency 11 — `add_rim_light()` is source-agnostic: applies to all bright edges equally
`add_rim_light()` in `LTG_TOOL_procedural_draw_v001.py` detects bright regions via luminance threshold (>170) and dilates their edges, painting those edges with BYTE_TEAL. This is a global operation on all bright areas. It applies equally to the left edge of Luma's body (window-facing side), the right edge, the hair crown, Byte's body, and any other bright element in the frame. A rim light should come from a specific direction — in this scene from the right (monitor side). The current implementation will paint a BYTE_TEAL halo around every bright element regardless of direction. The window-facing left side of Luma's body will receive a teal rim where it should have warm light; the right side will receive a teal rim where it is correct; and Byte (already teal) will receive a teal rim of its own colour, producing no visible separation.

**Expected:** Rim light appears only on right-facing edges of characters (monitor side).
**Found:** Rim light applied to all bright-region edges in all directions. No directional constraint.

### Inconsistency 12 — `add_face_lighting()` with `light_dir=(-1, -1)` correctly models upper-left
The call in `generate()` uses `light_dir=(-1, -1)` (upper-left). The library correctly computes shadow direction as the opposite: `sdx, sdy = 1.0, 1.0` (lower-right). The brow shadow is displaced to `brow_cx = cx + sdx * rx * 0.30` (right of centre, lower). The nose shadow is similarly displaced lower-right. The chin shadow is at the bottom. The highlight is on the upper-left. This correctly models a light coming from upper-left. The face lighting is geometrically accurate.

However: `shadow_color = SKIN_SH = (160, 104, 64)`. This is a warm-dark brown. In a scene with a warm light on the left, the shadow sides would be expected to show some degree of cool influence from the opposite cool fill (monitor, right). The shadow is purely warm, receiving no cool influence from the BYTE_TEAL right-side source. A warm shadow in this dual-lit scene is technically correct for the warm-side geometry, but the monitor should contribute cool bounce to the shadow side, reducing shadow warmth. Without cool-tinted shadow sides, the warm/cool contrast that makes dual-lit scenes dramatic is partially lost.

### Inconsistency 13 — Byte's shadow is on the wrong side for the window light
`draw_byte()` draws Byte's shadow on the right half of the body: `sb_draw.ellipse([bcx, bcy - bh // 2, bcx + bw // 2, bcy + bh // 2], fill=(*BYTE_SH, 180))`. Right side is dark. Window is on the left (and Byte sits on Luma's right shoulder, further right in the scene). The window is a left-side source. If window light is the primary warm source, Byte's right side should be in shadow — this is correct. However, the monitor is to Byte's right (Byte is on Luma's right shoulder, closest to the monitor). The monitor should be Byte's primary fill or even key on the right side. A brighter right-side contribution from the monitor is absent. The highlight is on Byte's left-upper quadrant (`bcx - bw // 2, bcy - bh // 2` to `bcx - bw // 8, bcy`), which is left-facing — consistent with window key. The shadow on the right is also consistent with window key. But the monitor-side (right) contribution is zero on Byte, even though Byte is physically closest to the monitor.

**Expected:** Byte's right side has some cyan/teal specular from monitor proximity, partially competing with window light, creating the dual-light character the scene calls for.
**Found:** Byte's right side is pure shadow. No monitor contribution.

### Inconsistency 14 — Torso shadow placed wrong relative to window direction
In `draw_luma()`, the hoodie shadow is placed on the right third of the torso (`torso_cx + torso_w // 4` to `torso_cx + torso_w // 2`). Window is on the left. Shadow on the right is geometrically correct. However, `HOODIE_AMBIENT = (179, 98, 80)` — this is the shadow colour. It is a warm-midtone orange-brown. In a scene with cool monitor on the right, the shadow side of the torso (facing the monitor) should show cool-temperature influence. The shadow colour is warm, which contradicts the right-side cool source.

---

## Procedural Draw Library — `LTG_TOOL_procedural_draw_v001.py`
**Functions reviewed:** `add_face_lighting()`, `add_rim_light()`

### Assessment of `add_face_lighting()`
The function models four anatomical layers: brow shadow, nose-on-cheek shadow, chin shadow, highlight accent. Positions are derived from `face_center` and `face_radius` with light/shadow direction computed correctly from `light_dir`. The feathering approach (stacked concentric ellipses with alpha falloff) is a valid PIL substitute for a gradient fill. The brow edge wobble line adds organic quality. The implementation correctly simulates a directional point source on a spherical face form.

**One structural issue:** The chin shadow (Layer 3) does not use the shadow direction. It is placed at a fixed `chin_y = cy + ry * 0.70` regardless of light direction. For any non-downward light (e.g. `light_dir = (0, 1)` from below), the chin shadow should shift accordingly. As implemented, the chin shadow is always at the bottom of the face regardless of source direction. For the current use case with upper-left sources this is forgivable, but the function does not correctly generalise.

### Assessment of `add_rim_light()`
As described in Inconsistency 11 above: the function is source-agnostic. It applies the rim color to all edges of all bright regions. This is not a rim light simulation — it is a bright-region edge glow. To be an accurate rim light, the function would need a direction parameter and would apply the tint only to edges facing away from the camera toward the back light. As written, it cannot distinguish "the right rim from a right-side back light" from "the left rim on a left-facing surface." This is a fundamental design gap.

---

## Environment Spot-Check

### Tech Den (v004) vs. SF01 Discovery
The tech den is an independent environment, not the SF01 scene, so direct comparison is approximate. However, both scenes share a warm + cool dual-light premise.

Tech den v004 correctly implements three distinct monitor spill zones via separate `gaussian_glow()` calls. The light shaft from the left window correctly projects onto the desk surface (apex at window top-right, base landing on desk). This is geometrically sound — the shaft narrows appropriately toward its source. Shadow direction from the window light source should place object shadows toward the right-centre of the desk. This is not explicitly verified in the renderer but the shaft direction is credible.

**No inconsistencies found** in the tech den environment beyond the scope of what the background alone can confirm without character placement.

### Other Side BG (v002) vs. SF03
Environment `LTG_ENV_other_side_bg_v002.png` generated by `LTG_TOOL_bg_other_side_v002.py`. No warm colours present at the environment level per the spec. The UV Purple and Cyan lighting language is consistent with SF03. Consistent.

---

## Summary Table

| # | Location | Issue | Severity |
|---|----------|-------|----------|
| 1 | SF01 — Luma face | Flat horizontal gradient; no brow/nose/chin shadows from upper lamp source | HIGH |
| 2 | SF01 — Luma left arm | Painted CYAN_SKIN (teal); should be warm lamp-lit | HIGH |
| 3 | SF01 — Lighting overlay | Warm/cold overlap zone at centre produces muddied ambiguous temperature | MEDIUM |
| 4 | SF01 — Byte highlight | Specular at upper-left; should be on screen-facing right side | HIGH |
| 5 | SF02 — Luma/Cosmo torso | No cyan specular on right (crack-facing) side | MEDIUM |
| 6 | SF02 — Characters | No magenta fill light tint on any character surface | HIGH |
| 7 | SF02 — Window system | Cone colour temperature and intensity don't match pane colour | MEDIUM |
| 8 | SF02 — Ground | Warm cone pools overwritten by cyan ground pass; no warm ground bounce | MEDIUM |
| 9 | SF03 — Luma face | Top highlight inconsistent with rising left-side cyan key source | MEDIUM |
| 10 | SF03 — Characters | Fixed UV palette cannot model position-dependent atmospheric tint | LOW |
| 11 | SF04 — `add_rim_light()` | Direction-agnostic: tints all bright edges equally, including wrong sides | HIGH |
| 12 | SF04 — `add_face_lighting()` | Geometrically accurate for upper-left source. Shadow warmth unchallenged by right fill. | LOW |
| 13 | SF04 — Byte | Zero monitor contribution on right side despite proximity | HIGH |
| 14 | SF04 — Hoodie shadow | HOODIE_AMBIENT warm colour on monitor-facing shadow side | MEDIUM |

---

## Style Frame Ratings

| Frame | Rating | Summary |
|-------|--------|---------|
| SF01 — Discovery | **WARN** | Lamp direction inconsistency on face; warm arm in wrong colour temperature; Byte highlight on wrong side. Core warm/cool split is present and directionally correct in atmosphere, but breaks down at character level. |
| SF02 — Glitch Storm | **WARN** | Three-tier spec partially implemented: cyan crack yes, warm windows yes, magenta fill absent from characters. Window-to-cone colour temperature disconnect. |
| SF03 — Other Side | **PASS** | Zero warm light mandate enforced. Lighting overlay is structurally correct. Face highlight direction is inconsistent with source but the deviation is minor at the render scale. |
| SF04 — Luma + Byte | **WARN** | `add_rim_light()` is not a directional rim — it is a global edge glow. Byte receives no monitor contribution despite proximity. Dual-lit quality is not realised in the character rendering. |

---

## What Must Be Improved

1. **`add_rim_light()` requires a direction parameter.** Without it, the function cannot model a back light coming from a specific side. This is a library-level failure that affects every frame that calls it. Fix: add a `light_angle` parameter and confine rim application to edges whose outward normal faces toward that angle.

2. **Character face shading must use `add_face_lighting()` consistently across all frames.** SF01 and SF02 do not use it. They use manual gradient scans or flat fills. Luma's face in SF01 Discovery is the primary close-up character surface in the show — it receives the least sophisticated lighting treatment.

3. **Magenta fill in SF02 must appear on character surfaces.** A fill light is defined precisely by its presence on the unlit sides of objects. If HOT_MAGENTA does not appear as a colour tint in character rendering, the three-tier lighting system exists only in the background, not in the characters. Characters and background will read as separate lighting environments.

4. **Byte's specular highlights must be placed relative to the nearest light source.** In SF01, Byte's primary illumination is the CRT screen behind/below it. In SF04, Byte's right side faces the monitor. Both cases require a screen-side specular. The current upper-left placement in SF01 is not physically grounded.

5. **Window-to-cone colour system in SF02 needs synchronisation.** Pane fill at (232, 201, 90) alpha 180 and cone at (200, 160, 80) alpha 90 are two independent colour decisions. They should be one system: sample the pane colour as the cone's origin colour, then gradient it toward ambient.

6. **SF04 `HOODIE_AMBIENT` on monitor-facing shadow side should carry cool tint.** In dual-lit scenes the shadow side is lit by the fill source. The fill here is BYTE_TEAL from the monitor. The shadow colour should trend toward (HOODIE_SH + BYTE_TEAL influence) rather than the current warm HOODIE_AMBIENT.

---

*Sven Halvorsen — Lighting, Compositing, and Visual Effects Critic*
*Critique 12 | 2026-03-29*
