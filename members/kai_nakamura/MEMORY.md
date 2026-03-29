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

## LTG_TOOL_batch_stylize_v001.py — RETIRED (C26)
- Moved to `output/tools/legacy/` along with stylize v001 and v002
- Post-processing stylization pipeline fully retired C26
- UV_PURPLE color protection issue in stylize tools is moot — tools no longer active

## LTG_TOOL_render_qa_v001.py — v1.1.0 (C27 UPDATED)
- Full QA pipeline: silhouette, value range, color fidelity, warm/cool, line weight
- `qa_report(img_path, asset_type="auto") → dict` — single image, 5 checks, overall_grade PASS/WARN/FAIL
- `qa_batch(directory, asset_type="auto") → list[dict]` — all PNGs in a directory
- `qa_summary_report(results, output_path)` — writes Markdown report
- `silhouette_test(img) → PIL.Image` — 100×100 B&W (compatible with Rin's procedural_draw)
- `value_study(img) → PIL.Image` — grayscale auto-contrast (compatible with Rin's procedural_draw)
- asset_type values: "auto"|"style_frame"|"character_sheet"|"color_model"|"turnaround"|"environment"
- character_sheet/color_model/turnaround → warm/cool SKIPPED (not a WARN); grade from active checks only
- Import: `from LTG_TOOL_render_qa_v001 import qa_report, qa_batch, qa_summary_report`
- Depends on: LTG_TOOL_color_verify_v001 (must be in same directory / sys.path)

## Cycle 27 — COMPLETE
- Updated LTG_TOOL_render_qa_v001.py → v1.1.0: asset_type param, warm/cool skip for char sheets
- Ran QA on 29 C27 pitch assets → saved `output/production/qa_report_cycle27.md`
- Processed post-processing pipeline retirement notice (inbox archived)

## C27 QA Findings (29 assets: 6 PASS / 21 WARN / 2 FAIL)
- **2 FAILs:**
  - LTG_CHAR_lineup_v004.png — silhouette=blob (character sheet; warm/cool correctly skipped)
  - LTG_ENV_classroom_bg_v002.png — silhouette=blob + multiple WARNs
- **Key WARN patterns:**
  - SUNLIT_AMBER hue drift (Luma assets): found ~25°, target 34.3° — persistent; investigate Luma generator
  - Grandma Miri and Glitch: color fidelity WARN across expression sheets and color models
  - Style frames: warm/cool separation still insufficient (expected for certain frames)
  - Environments: value compression common (no deep darks or bright highlights in some)
  - lineup_v004: silhouette=blob — likely white/flat bg causing all-white threshold; Rin to review
  - classroom_bg_v002: both silhouette and value issues — low contrast asset
- **Character sheet warm/cool correctly SKIPPED** — 0 false WARNs from that check
- Byte, Cosmo: clean PASSes across expression sheets, turnarounds, color models

## Lessons Learned (C25)
- HOT_MAGENTA is #FF2D6B (not #FF0090) — always verify hex in master_palette.md
- RGB sampling radius=40 may miss severely drifted colors; hue drift test needs colors geometrically close to target
- production/ exemption is the right call — renaming ~100 files creates more noise than value

## Lessons Learned (C26)
- Warm/cool check is valid for style frames but not character sheets (flat neutral bg by design)
  Future version: add asset_type param to skip warm/cool for character sheet type assets — DONE C27

## Lessons Learned (C27)
- Auto-inference from filename works well; "lineup" keyword correctly maps to character_sheet
- lineup_v004 silhouette=blob is a real issue to flag to Rin — opaque light bg causes incorrect threshold
- SUNLIT_AMBER hue drift on Luma is a recurring generator issue, not a one-off
