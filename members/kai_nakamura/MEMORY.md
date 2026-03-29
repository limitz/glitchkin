# Kai Nakamura — MEMORY

## Identity
Technical Art Engineer for "Luma & the Glitchkin." Joined Cycle 21. Mission: upgrade PIL toolchain with procedural rendering techniques and build a reusable shared library.

## Project Context
- Animation pitch package for a cartoon about 12yo Luma discovering Glitchkin (pixel creatures) in grandma's CRT TV
- All tools: Python PIL/Pillow (open source only)
- Tools live in `/home/wipkat/team/output/tools/`
- Shared library: `output/tools/LTG_TOOL_render_lib_v001.py` — __version__ = "1.1.0"
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`

## Key Standards
- Byte body fill = GL-01b (#00D4E8 / RGB 0,212,232) — never Void Black
- Glitch palette never in real-world environments
- After img.paste() or alpha_composite(), always refresh draw = ImageDraw.Draw(img)
- All procedural elements use seeded RNG for reproducibility
- output/production/ files are EXEMPT from LTG naming (descriptive names only)
- **IMAGE SIZE RULE: prefer smallest resolution appropriate for the task. Hard limit ≤ 1280px in both dimensions.** Use `img.thumbnail((1280, 1280), Image.LANCZOS)` before saving. Preserve aspect ratio. Only use large sizes when detail inspection requires it; use smaller sizes otherwise. Detail crops also ≤ 1280×1280px.

## Palette Reference (verified C25 from master_palette.md)
- CORRUPT_AMBER:  (255, 140, 0)    #FF8C00  GL-07
- BYTE_TEAL:      (0, 212, 232)    #00D4E8  GL-01b
- UV_PURPLE:      (123, 47, 190)   #7B2FBE  GL-04
- HOT_MAGENTA:    (255, 45, 107)   #FF2D6B  GL-02  (NOT #FF0090)
- ELECTRIC_CYAN:  (0, 240, 255)    #00F0FF  GL-01
- SUNLIT_AMBER:   (212, 146, 58)   #D4923A  RW-03

## LTG_TOOL_render_lib_v001.py — API Summary (Canonical)
__version__ = "1.1.0" (C24: paper_texture added)
Functions: perlin_noise_texture, gaussian_glow, light_shaft, dust_motes,
           catenary_wire, scanline_overlay, vignette, paper_texture
Import: `from LTG_TOOL_render_lib_v001 import ...`

## LTG_TOOL_color_verify_v001.py (C25 NEW)
- `verify_canonical_colors(img, palette_dict, max_delta_hue=5)` → per-color + overall_pass dict
- `get_canonical_palette()` → standard 6-color LTG palette dict
- Sampling: pixels within Euclidean RGB radius=40 of target; median hue; not_found = not a fail
- Standalone (stdlib colorsys + Pillow only)

## LTG_TOOL_batch_stylize_v001.py (C25 updated → v1.1.0)
- Now calls v002 stylize (full canonical color protection)
- Post-job color verification: verify_canonical_colors() on each output PNG
- New params: `verify_colors=True`, `color_max_delta_hue=5.0`

## LTG_TOOL_render_qa_v001.py (C26 NEW)
- Full QA pipeline: silhouette, value range, color fidelity, warm/cool, line weight
- `qa_report(img_path) → dict` — single image, 5 checks, overall_grade PASS/WARN/FAIL
- `qa_batch(directory) → list[dict]` — all PNGs in a directory
- `qa_summary_report(results, output_path)` — writes Markdown report
- `silhouette_test(img) → PIL.Image` — 100×100 B&W (compatible with Rin's procedural_draw)
- `value_study(img) → PIL.Image` — grayscale auto-contrast (compatible with Rin's procedural_draw)
- Import: `from LTG_TOOL_render_qa_v001 import qa_report, qa_batch, qa_summary_report`
- Depends on: LTG_TOOL_color_verify_v001 (must be in same directory / sys.path)

## Cycle 26 — COMPLETE
- Built `LTG_TOOL_render_qa_v001.py` — render QA tool
- Ran QA on 8 C25 assets → all WARN; saved `output/production/qa_report_cycle26.md`
- Updated `output/tools/README.md` with new QA tool entry
- Rin interface note: silhouette_test() + value_study() use PIL.Image in/out; compatible

## C26 QA Findings (key patterns to watch)
- ALL 8 assets: warm/cool separation WARN — character/color model sheets are intentionally
  uniform-hue (no warm vs cool zones by design); consider adjusting threshold or flagging
  these asset types as "character sheet" (exempt from warm/cool check in future version)
- SUNLIT_AMBER hue drift recurring on Luma assets (expression sheet, turnaround, color model):
  found hue ~18–25°, target 34.3°. Investigate in Luma generator — possible value/saturation
  interaction causing hue read low.
- Byte/Cosmo color models: color fidelity PASS (canonical colors correctly placed)
- Silhouette: all DISTINCT — good shape readability across all assets
- Value range: all PASS — full tonal range achieved
- Line weight: all PASS

## Lessons Learned (C25)
- HOT_MAGENTA is #FF2D6B (not #FF0090) — always verify hex in master_palette.md
- RGB sampling radius=40 may miss severely drifted colors; hue drift test needs colors geometrically close to target
- production/ exemption is the right call — renaming ~100 files creates more noise than value

## Lessons Learned (C26)
- Warm/cool check is valid for style frames but not character sheets (flat neutral bg by design)
  Future version: add asset_type param to skip warm/cool for character sheet type assets
- SUNLIT_AMBER consistently reads lower hue on Luma assets — worth investigating generator source
