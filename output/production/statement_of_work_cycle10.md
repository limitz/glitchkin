# Statement of Work — Cycle 10

**Date:** 2026-03-29
**Cycle:** 10

## Work Completed

### Alex Chen — Art Director
- **byte.md v3.1**: All remaining chamfered-cube references purged from Sections 5, 6, 8, 10, 11
- **Show logo created**: `logo_generator.py` → `show_logo.png` (1200×480) — "Luma" in SUNLIT_AMBER, "& the Glitchkin" in ELEC_CYAN with pixel corruption, void bg with warm/cold glow zones
- **Luma lean increased**: `lean_offset` 28px → 48px (~9° → ~16°) — genuine urgency toward screen
- **Monitor screen content**: receding perspective grid + pixel figure silhouettes + noise scatter — implies Byte's origin world
- **Output:** `style_frame_01_rendered.png` regenerated, `show_logo.png` created

### Maya Santos — Character Designer
- **Byte turnaround fixed to oval**: all 4 views updated from chamfered-cube to ellipse matching canonical expression sheet. `byte_turnaround.png` regenerated.
- **Cosmo and Miri turnarounds**: both added — Cosmo's glasses per-view, Miri's MIRI-A design from all angles. `cosmo_turnaround.png`, `miri_turnaround.png` generated.
- **Character lineup composite** (5 cycles overdue): `character_lineup_generator.py` → `character_lineup.png` — all 4 in color at correct relative heights with labels
- **Hover particles fixed**: `byte_expressions_generator.py` 4×4px → 10×10px
- **Output:** All character assets regenerated

### Jordan Reed — Background & Environment Artist
- **9 Glitch Layer depth-tier colors documented**: named constants + GL parent refs in script; "Glitch Layer — Depth Tiers" subsection added to master_palette.md
- **Aurora tuple named**: `AURORA_CYAN_BLEED` with GL-01 reference
- **Platform variety**: L-shaped, bridge, fragmented variants added to MID and NEAR tiers
- **Output:** `glitch_layer_frame.png` regenerated

### Sam Kowalski — Color & Style Artist
- **HOODIE_AMBIENT corrected**: `#B06040` → `#B36250` — matches documented 70/30 formula
- **Cold overlay analysis**: documented, no adjustment needed (max 3.5% alpha at boundary)
- **luma_color_model.md cross-reference**: "Skin System Cross-Reference" section added
- **Color keys** regenerated with Cycle 10 labels

### Lee Tanaka — Storyboard Artist
- **P22 Glitchkin shapes**: varied 4-7 sided polygons with per-vertex jitter
- **P23 monitor bowing**: white-hot fill + bezel-breaking rings + white center punch
- **P15 body language**: torso squash, defensive arm, shock-reflex leg, head tilted back
- **Contact sheet**: version string updated to Cycle 10
- **Output:** All 12 chaos panels + contact sheet regenerated

## Key Improvements Over Cycle 9
- byte.md fully oval — no cube references remain
- Show logo exists — first visual branding asset
- All 4 character turnarounds complete (Luma, Byte, Cosmo, Miri)
- Character lineup composite finally exists (5-cycle blocker resolved)
- Glitch Layer palette fully traceable
- Monitor screen has content — Byte's origin implied visually

## Work Completed

### Maya Santos — Character Designer

- **Byte turnaround oval fix (P0 ship blocker):** All four `draw_byte_*` functions in `character_turnaround_generator.py` updated from chamfered-cube polygon to OVAL ellipse. Body proportions now match `byte_expressions_generator.py` canonical: `body_rx = s//2`, `body_ry = int(s*0.55)`. `_byte_size()` docstring updated to say "oval body." Center-back data-port NEG_SPACE slot carried forward into oval back view. `byte_turnaround.png` regenerated.

- **Cosmo turnaround created (new):** All 4 views added to `character_turnaround_generator.py`. Defining feature: thick plastic glasses (espresso brown frames, NEG_SPACE cutout lenses) visible from every angle — front: both full, 3/4: near full + far compressed, side: single lens protrudes beyond face silhouette + ear arm shown, back: no lenses. Notebook edge visible in 3/4 and side views. `cosmo_turnaround.png` generated.

- **Miri turnaround created (new — MIRI-A canonical):** All 4 views added. Defining feature: tall oval bun + V-pair chopsticks readable from all angles. Back view = same symmetric bun geometry as front. Side view = narrow oval bun + single chopstick. Soldering iron visible front/3/4/side, hidden in back. Wide inverted-flare cardigan shape consistent across all views. `miri_turnaround.png` generated.

- **Character lineup image created (5 cycles overdue):** New tool `character_lineup_generator.py` renders all 4 characters in COLOR at correct relative heights on a shared baseline. Heights: Luma 280px (3.5 heads), Cosmo 320px (4.0 heads), Miri 256px (3.2 heads), Byte 162px (~Luma chest). Dashed height-reference lines show Cosmo top, Luma top, Miri top, Byte/Luma-chest. Colors from master_palette.md (canonical hex values). Per-character brackets with px labels. `character_lineup.png` generated.

- **Hover particle confetti corrected to 10×10px in byte_expressions_generator.py:** Line ~392 changed from `px+4` to `px+10`. "GL spec" rationalization comment deleted. Now matches turnaround generator spec. `byte_expressions.png` regenerated.

## Output Files

| File | Path | Status |
|---|---|---|
| `byte_turnaround.png` | `/output/characters/main/turnarounds/` | Regenerated (oval fix) |
| `luma_turnaround.png` | `/output/characters/main/turnarounds/` | Regenerated (cycle label update) |
| `cosmo_turnaround.png` | `/output/characters/main/turnarounds/` | NEW |
| `miri_turnaround.png` | `/output/characters/main/turnarounds/` | NEW |
| `character_lineup.png` | `/output/characters/main/` | NEW — all 4 chars at scale, in color |
| `byte_expressions.png` | `/output/characters/main/` | Regenerated (10px particles) |
| `character_turnaround_generator.py` | `/output/tools/` | Updated — oval Byte + Cosmo + Miri |
| `character_lineup_generator.py` | `/output/tools/` | NEW tool |
| `byte_expressions_generator.py` | `/output/tools/` | Particle size fix |

## Blockers Closed

| Blocker | Cycles Outstanding | Resolution |
|---|---|---|
| Byte turnaround oval shape | 1 (Cycle 9 ship blocker) | Fixed — all 4 views now use ellipse |
| Character lineup reference image | 5 | Delivered — `character_lineup.png` |
| Hover particles 4px→10px | 4 | Fixed in `byte_expressions_generator.py` |
| Cosmo turnaround missing | 1 | Delivered |
| Miri turnaround missing | 1 | Delivered (MIRI-A canonical) |

## Notes

- MIRI-A (bun+chopsticks+cardigan+soldering iron) is the sole canonical Miri design per Alex Chen's lock. All new assets use MIRI-A only.
- Cosmo color: Dusty Lavender jacket #A89BBF, cerulean+sage striped shirt, espresso glasses #5C3A20, chinos #8C8880.
- Miri color: Terracotta rust cardigan #B85C38, silver hair #D8D0C8, deep sage slippers #5A7A5A, deep warm brown skin #8C5430.

*Compiled by Maya Santos, Character Designer — Cycle 10*
