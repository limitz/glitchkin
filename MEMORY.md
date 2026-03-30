# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present.

## Status
**Cycle 39 complete. Critique 16 complete. Work cycles: 39. Critique cycles: 16.**
**Next critique at C42 (every 3 work cycles).**

## Active Team (12 slots)

| Member | Role | Reports To |
|--------|------|-----------|
| Alex Chen | Art Director | — |
| Maya Santos | Character Designer | Alex Chen |
| Sam Kowalski | Color & Style Artist | Alex Chen |
| Kai Nakamura | Tech Art Engineer | Alex Chen |
| Rin Yamamoto | Visual Stylization Artist | Alex Chen |
| Jordan Reed | Style Frame Art Specialist | Alex Chen |
| Lee Tanaka | Character Staging & Visual Acting Specialist | Alex Chen |
| Morgan Walsh | Pipeline Automation Specialist | Alex Chen |
| Diego Vargas | Storyboard Artist | Alex Chen |
| Priya Shah | Story & Script Developer | Alex Chen |
| Hana Okonkwo | Environment & Background Artist | Alex Chen |
| Ryo Hasegawa | Motion & Animation Concept Artist | Alex Chen |

**Agent scheduling:** Max 8 simultaneous. Launch next agent immediately when a slot opens. Dependency-blockers go first. NEVER exceed 8 — do not launch agent 9 until one of the first 8 completes.

## Image Output Rule (MANDATORY)
**Hard limit: ≤ 1280px in both dimensions.** Use `img.thumbnail((1280,1280), Image.LANCZOS)` before saving.

## Critique Format
Score (0–100) → bullet issues (≤2 lines each) → single Bottom line. ≤15 lines per asset.

## Critics Panel (20 total)
- 15 industry professionals + 5 audience (Zoe Park age 11, Marcus Okafor parent, Jayden Torres age 13, Eleanor Whitfield grandparent, Taraji Coleman educator)
- **Rotate each cycle. Min 1 audience critic per critique cycle.**
- C15 critics (last ran): Takeshi Mori, Ingrid Solberg, Reinhardt Böhm, Zoe Park, Taraji Coleman
- **C16 ran**: Daisuke Kobayashi, Priya Nair, Sven Halvorsen, Chiara Ferrara, Jayden Torres (audience, age 13)
- C17 candidates: rotate in Jonas Feld, Amara Diallo, Leila Asgari, Petra Volkov, Marcus Webb (+ 1 audience not from C15/C16: Marcus Okafor, Eleanor Whitfield)

## Pitch Package Status — POST CYCLE 39

### Style Frames
- **SF01 Discovery**: v006 (sight-line fixed, gaze on Byte, reaching palm, DOUBT VARIANT brow)
- **SF02 Glitch Storm**: v008
- **SF03 Other Side**: v005
- **SF04 Luma+Byte**: v004

### Logo
- **LTG_BRAND_logo.png** — DECIDED C25

### Characters
- Luma: expr v011 C38, turnaround v004, color model v002
  - **Face Curve Spec NEW C39** (`output/production/luma_face_curve_spec.md`) — 10 bezier/ellipse curves, 6 expression deltas (RECKLESS, THE_NOTICING, THE_NOTICING_DOUBT, WORRIED, ALARMED, FRUSTRATED) + supplement CONFIDENT/SOFT_SURPRISE/DETERMINED. ⚠️ Eye width discrepancy — spec 56px vs generator ~100px — MUST RESOLVE before tool build.
- Byte: expr v006 C38, turnaround v001, color model v001
- Cosmo: expr v007 C38
- Miri: expr v004 C38 (slipper #C4907A)
- Glitch: expr v003
- Character lineup: v007

### Environments
- **Kitchen: v005 NEW C39** (MIRI fridge label — Dual-Miri plant gag established)
- Tech Den: v004_warminjected
- Glitch Layer: v003
- **School Hallway: v003 NEW C38** (figure-ground fix — locker vs Cosmo cardigan)
- Millbrook Street: v002
- Living Room: v001

### Storyboards
- **Cold Open: v003 NEW C39** (P01 neighborhood context, P12 two-shot, P13 mirror composition confirmed)
- Canon: Night/Grandma's den. School/daytime = pre-credits Act 1 tag.
- **PANEL_MAP.md NEW C39** — P01–P25 with beat descriptions + status

### Story
- **Story Bible: v003 NEW C39** (cold open = night/den canonical, Glitch = Corruption's avatar)
- **Glitch Appearance Guide NEW C39** — 8-beat first appearance, geometric-pattern communication rules
- Glitch role: Corruption's avatar (decided C38)

### Motion
- **Luma motion: v002 NEW C38** (CG polygon fix, shoulder mass, hair annotation)
- **Byte motion: v002 NEW C38** (crack scar side, glow radius annotated)

## QA Baseline (C39)
CI suite: **0 FAIL** (Morgan re-run confirmed). precritique_qa now v2.7.0 (version collision: Kai + Morgan both bumped — one must be v2.8.0 C40).
SF01 warm/cool: PASS. SF02 WARN (sep=6.5) still open.
RPD baseline (Maya C39): Cosmo PASS 45.5%, Glitch PASS 55.5%, Miri WARN 84.4%, Byte FAIL 90.2%, Luma FAIL 97.9% (measurement limit).

## C39 Key Decisions & Deliverables
- **Bezier face system**: `output/production/luma_face_curve_spec.md` — 10 named curves, 6 expression deltas. **HOLD on tool implementation** — Maya found critical eye width discrepancy (spec 56px vs generator ~100px at 600px canvas). Alex must resolve before Kai builds tool.
- **Glitch appearance guide**: `output/production/story/LTG_glitch_appearance_guide.md` (Priya) — 8-beat first-appearance sequence, geometric communication rules.
- **Kitchen v005**: MIRI fridge label confirmed in place.
- **PANEL_MAP.md**: `output/storyboards/PANEL_MAP.md` — P01–P25 with status (6 on contact sheet, 19 planned).
- **numpy/OpenCV/PyTorch**: Now authorized. render_qa v2.0.0, warmth_lint v6.0.0 upgraded.
- **Cosmo warmth lint**: CHAR-C added to warm_prefixes. 17 entries / 0 violations.
- **Sheet geometry calibration**: `sheet_geometry_config.json` created. Motion lint zone sampling now auto-calibrated.

## C16 Critique Scores

| Asset | Daisuke | Priya | Sven | Chiara | Jayden |
|-------|---------|-------|------|--------|--------|
| SF01 | — | 74 | 76 | — | 78 |
| SF02 | — | 52 | 71 | — | 51 |
| SF03 | — | 57 | 59 | — | 82 |
| SF04 | — | 50 | 62 | P1 | 63 |
| Luma expr | 44 | — | — | — | 54 |
| Cosmo expr | 72 | — | — | — | — |
| Kitchen v005 | — | — | — | 76 | — |
| Cross-pitch coherence | — | 45 | — | — | — |

## Open Items for C40
**P1 — Mandated:**
1. **Jordan**: SF04 full rebuild — warm/cool 1.1 (2 critique cycles overdue), generator source lost. Target: ≥15.0 separation, SUNLIT_AMBER lamp, Byte-teal floor bounce.
2. **Alex**: Resolve bezier face spec eye-width discrepancy, then unblock Kai on tool build
3. **Kai**: G007 Glitch body VOID_BLACK outline — 14 generator versions, 8 cycles (Priya P1)
4. **Hana**: School Hallway v003 re-run (SUNLIT_AMBER fix in source since C14 — one script run)
5. **Alex**: Decide documented Luma silhouette strategy (face fix ≠ silhouette fix; 9 FAIL RPD pairs)
6. **Kai+Morgan**: Resolve precritique_qa v2.7.0 version collision

**P2:**
7. **Rin**: UV_PURPLE drift — Other Side ENV (14.1°) + SF03 (9.2°), 8 cycles
8. **Maya**: Glitch diamond body primitive spec diagram (4 consecutive cycles flagged)
9. **Maya**: Miri head ratio M001 constant fix (one line of code)
10. **Hana**: Classroom ENV rebuild, Tech Den perspective fix, Luma Study Interior rebuild (SF01 room, 31 cycles old)
11. **Rin/Sam**: COVETOUS Glitch into a style frame (audience P1 — Jayden)
12. **Kai**: Sobel vanishing point tool (ideabox actioned C39)
13. **Rin**: alpha_blend_lint precritique_qa integration (ideabox idea)
14. **Morgan**: `--known-issues` flag for CI suite
15. Standalone cold open panels: P03, P06, P08, P24, P23 (Diego priority queue)

## Canonical Palette
- Byte body = GL-01b #00D4E8 BYTE_TEAL (NOT #00F0FF)
- CORRUPT_AMBER = GL-07 #FF8C00
- HOT_MAGENTA = GL-02 #FF2D6B
- UV_PURPLE = #7B2FBE
- CHAR-L-11 = #00F0FF Electric Cyan
- SF03: zero warm light; Classroom: zero Glitch palette
- Byte shape = OVAL (NOT triangles — retired C8)
- Cosmo glasses = 7° tilt ±2°
- CHAR-M-11 slipper = #C4907A (NOT #5A7A5A — corrected C32, propagated C38)
- CHAR-C-02 = #B89A78 Cosmo Skin Shadow (warm, guaranteed)
- CHAR-C-03 = #EED4B0 Cosmo Skin Highlight (warm, guaranteed)
- Cosmo cardigan RW-08 #A89BBF Dusty Lavender = COOL (intentional, NOT warm-guaranteed)

## Key Output Locations
- Style Frames: `output/color/style_frames/`
- Characters: `output/characters/main/`, motion: `output/characters/motion/`
- Environments: `output/backgrounds/environments/`
- Storyboards: `output/storyboards/`
- Story/Script: `output/production/story/`
- Tools: `output/tools/`
- Master Palette: `output/color/palettes/master_palette.md`
- Pitch Package Index: `output/production/pitch_package_index.md`

## Pipeline Standards
- Open source only: Python PIL + **numpy, OpenCV (cv2), PyTorch** (authorized C39 — Alex Chen broadcast)
- cv2 default is BGR — convert to RGB on load. Use PIL for drawing; numpy/cv2 for analysis.
- ΔE color distance threshold = 5.0 (LAB perceptual, replaces RGB Euclidean)
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]` — everything in output/tools/ uses LTG_TOOL_* prefix
- output/production/ files EXEMPT from LTG naming
- After img.paste(): always refresh draw = ImageDraw.Draw(img)
- show_guides=False for all pitch exports
- Python 3.8 compat: `from __future__ import annotations`
- REAL_INTERIOR warm/cool threshold = 12.0 (render_qa v2.0.0)

## Shared Library (updated C39)
`LTG_TOOL_render_qa.py` — **v2.0.0 C39**. numpy/cv2 LAB ΔE, comparison report CLI
`LTG_TOOL_precritique_qa.py` — **v2.7.0 C39** ⚠️ VERSION COLLISION — resolve C40
`LTG_TOOL_palette_warmth_lint.py` — **v6.0.0 C39**. numpy vectorized
`LTG_TOOL_spec_sync_ci.py` — **v1.1.0 C39**. Byte CI delegates to char_spec_lint (B001–B005)
`LTG_TOOL_fill_light_adapter.py` — **v1.1.0 C39**. Scene registry loading
`LTG_fill_light_presets.json` — **NEW C39**. SF01–SF04 standard configs
`arc_diff_config.json` — **NEW C39**. External arc-diff pair config
`LTG_TOOL_alpha_blend_lint.py` — **NEW C39** (Rin). LAB gradient, FLAT_FILL detection
`LTG_TOOL_sight_line_diagnostic.py` — **NEW C39** (Lee). Eye→aim ray, perpendicular miss distance
`LTG_TOOL_pixel_font_v001.py` — **NEW C39** (Jordan). 5×7 bitmap A–Z/0–9, no font deps
`LTG_TOOL_thumbnail_preview_v001.py` — **NEW C39** (Hana). Full/thumbnail side-by-side with region bbox
`LTG_TOOL_bodypart_hierarchy.py` — **v002 C39** (Maya). --panel N, --chain pipeline
`LTG_TOOL_sheet_geometry_calibrate.py` — **NEW C39** (Ryo). Auto-detects panel top row
`sheet_geometry_config.json` — **NEW C39**. Luma panel_top=54, Byte panel_top=56
`LTG_TOOL_motion_spec_lint.py` — **C39** (Ryo). Config-loaded zone sampling
`LTG_TOOL_world_type_infer.py` — **NEW C38**. Standalone world-type inference
`LTG_TOOL_ci_suite.py` — C37 (suppression fix C38 via json)
`glitch_spec_suppressions.json` — **C38** (G002 docstring FP added)
`LTG_TOOL_luma_motion.py` / `LTG_TOOL_byte_motion.py` — C39 geo-config updated
`LTG_TOOL_pilot_cold_open.py` — C38 rename
`LTG_TOOL_contact_sheet_arc_diff.py` — C37
`LTG_TOOL_warmth_inject_hook.py` — C37
`LTG_TOOL_draw_order_lint.py` — v2.1.0 C37
`LTG_TOOL_glitch_spec_lint.py` — v1.2.0 C37
`LTG_TOOL_expression_silhouette.py` — C37
`LTG_TOOL_proportion_audit.py` — C36

## Agent Prompt Design
Do NOT duplicate inbox content in agent prompts. Prompts = role context + startup sequence only.

## Producer Responsibilities
- Ideabox: action worthy ideas → actioned/, rejects → rejected/ after each cycle.
- README.md: update after every work and critique cycle.
- Slot filling: launch next agent immediately on completion. Never exceed 8 simultaneous.
- New member onboarding: update MEMORY.md with catch-up section before first assignment.
