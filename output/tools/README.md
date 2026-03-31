<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->

# Output Tools Index

> For historical changes, see `git log`. API details live in each tool's docstring, not here.
> Legacy tools are in `legacy/`. Deprecated tools are in `deprecated/`. Neither should be imported.

---

## Image Output Rule
**Prefer the smallest resolution appropriate for the task.** Hard limit: **≤ 1280px in both dimensions.**
Apply before saving any image:
```python
img.thumbnail((1280, 1280), Image.LANCZOS)
```
Aspect ratio is preserved automatically. Only use large sizes when fine detail inspection is required. For detail/crop images: also ≤ 1280x1280px.

---

## Open Source Tools Policy

This production uses **open source tools exclusively**. No proprietary software is permitted.

| Tool | Role |
|---|---|
| **OpenToonz** | 2D animation |
| **Krita** | Digital painting |
| **Inkscape** | Vector graphics |
| **Natron** | Compositing |
| **Python + Pillow/PIL** | Image scripting |
| **Python + pycairo / svgwrite** | Vector scripting |
| **ImageMagick** | CLI image processing |
| **Git + Git LFS** | Version control |

If a required tool does not exist in the open source ecosystem, build it in Python and register it below.

---

## Script Index

### Drawing / Rendering

| Filename | Description |
|---|---|
| `LTG_TOOL_render_lib.py` | Shared rendering library (flatten_rgba_to_rgb, paper texture, vignette) |
| `LTG_TOOL_procedural_draw.py` | Procedural shape drawing primitives |
| `LTG_TOOL_cairo_primitives.py` | Cairo-based vector drawing primitives |
| `LTG_TOOL_curve_draw.py` | Bezier/spline curve drawing |
| `LTG_TOOL_curve_utils.py` | Curve math utilities |
| `LTG_TOOL_draw_shoulder_arm.py` | Shoulder/arm construction drawing helper |
| `LTG_TOOL_pixel_font_v001.py` | Pixel-art bitmap font renderer |
| `LTG_TOOL_fill_light_adapter.py` | Fill-light color temperature adapter |
| `LTG_TOOL_warmth_inject.py` | Warm-tone injection pass for composites |
| `LTG_TOOL_warmth_inject_hook.py` | Pre-save hook that runs warmth injection |
| `LTG_TOOL_contact_shadow.py` | Contact shadow generator for grounded composites |
| `LTG_TOOL_bodypart_hierarchy.py` | Body-part layering/hierarchy definitions |
| `LTG_TOOL_construction_stiffness.py` | Construction-line stiffness metric |
| `LTG_TOOL_logo.py` | Main logo generator |
| `LTG_TOOL_logo_asymmetric.py` | Asymmetric logo lockup generator |
| `LTG_TOOL_thumbnail_preview_v001.py` | Thumbnail preview renderer |
| `LTG_TOOL_character_color_enhance.py` | Character color enhancement pass |

### Character Renderers (Modular)

| Filename | Description |
|---|---|
| `LTG_TOOL_char_byte.py` | Canonical Byte modular renderer (10 expressions, cairo, transparent ARGB surface) |
| `LTG_TOOL_char_cosmo.py` | Canonical Cosmo modular renderer (7 expressions incl. OBSERVING, cairo, angular gesture spec, transparent ARGB surface) |
| `LTG_TOOL_char_glitch.py` | Canonical Glitch modular renderer (9 expressions, cairo, transparent ARGB surface) |
| `LTG_TOOL_char_luma.py` | Canonical Luma modular renderer (7 expressions incl. DOUBT-IN-CERTAINTY, cairo, pose_mode: side/front/threequarter/back) |
| `LTG_TOOL_char_miri.py` | Canonical Grandma Miri modular renderer (6 expressions, cairo, transparent ARGB surface) |
| `LTG_TOOL_char_module_test.py` | Modular character renderer integration test |

### Character Generators

| Filename | Description |
|---|---|
| `LTG_TOOL_luma_turnaround.py` | Luma character turnaround sheet (v006: 5 true views — front/3q/side/side-L/back) |
| `LTG_TOOL_cosmo_turnaround.py` | Cosmo character turnaround sheet |
| `LTG_TOOL_miri_turnaround.py` | Grandma Miri character turnaround sheet |
| `LTG_TOOL_glitch_turnaround.py` | Glitchkin character turnaround sheet |
| `LTG_TOOL_byte_turnaround.py` | Byte character turnaround sheet |
| `LTG_TOOL_luma_expression_sheet.py` | Luma expression sheet |
| `LTG_TOOL_cosmo_expression_sheet.py` | Cosmo expression sheet |
| `LTG_TOOL_byte_expression_sheet.py` | Byte expression sheet (8 expressions) |
| `LTG_TOOL_grandma_miri_expression_sheet.py` | Grandma Miri expression sheet |
| `LTG_TOOL_glitch_expression_sheet.py` | Glitchkin expression sheet |
| `LTG_TOOL_luma_color_model.py` | Luma color model swatches |
| `LTG_TOOL_cosmo_color_model.py` | Cosmo color model swatches |
| `LTG_TOOL_byte_color_model.py` | Byte color model swatches |
| `LTG_TOOL_glitch_color_model.py` | Glitchkin color model swatches |
| `LTG_TOOL_grandma_miri_color_model.py` | Grandma Miri color model swatches |
| `LTG_TOOL_character_lineup.py` | Full character lineup sheet |
| `LTG_TOOL_character_face_test.py` | Character face test gate (automated) |
| `LTG_TOOL_luma_act2_standing_pose.py` | Luma Act 2 standing reactive pose |
| `LTG_TOOL_luma_classroom_pose.py` | Luma classroom seated pose |
| `LTG_TOOL_luma_cold_overlay_swatches.py` | Luma cold-light overlay color swatches |
| `LTG_TOOL_byte_cracked_eye_glyph.py` | Byte cracked-eye glyph reference sheet |
| `LTG_TOOL_expression_silhouette.py` | Expression silhouette squint-test generator |
| `LTG_TOOL_expression_isolator.py` | Single-expression isolator/cropper |
| `LTG_TOOL_glitch_body_primitive_diagram_gen.py` | Glitchkin body primitive diagram |
| `LTG_TOOL_lineup_tier_depth_sketch.py` | Lineup tier depth sketch |
| `LTG_TOOL_elderly_proportion_reference.py` | Elderly character proportion reference |
| `LTG_TOOL_luma_construction_prototype.py` | Luma construction-line prototype |
| `LTG_TOOL_luma_gesture_prototype.py` | Luma gesture drawing prototype |
| `LTG_TOOL_luma_motion_prototype_c51.py` | Luma motion prototype (C51) |
| `LTG_TOOL_luma_motion.py` | Luma motion/action pose generator |
| `LTG_TOOL_luma_cairo_expressions.py` | Luma expressions via Cairo renderer |
| `LTG_TOOL_luma_face_curves.py` | Luma face curve definitions |
| `LTG_TOOL_scale_reference_sheet.py` | Scale/proportion reference sheet |
| `LTG_TOOL_sheet_geometry_calibrate.py` | Expression sheet geometry calibration |
| `LTG_TOOL_byte_commitment_rpd_test.py` | Byte commitment RPD visual test |

### Environment Generators

| Filename | Description |
|---|---|
| `LTG_TOOL_bg_glitch_layer_frame.py` | Glitch Layer full environment background |
| `LTG_TOOL_bg_glitchlayer_frame.py` | Glitch Layer frame variant |
| `LTG_TOOL_bg_glitch_layer_encounter.py` | Glitch Layer encounter scene background |
| `LTG_TOOL_bg_glitch_storm_colorfix.py` | Glitch Storm background (color-fixed, no characters) |
| `LTG_TOOL_bg_other_side.py` | "The Other Side" CRT-world environment |
| `LTG_TOOL_bg_luma_study_interior.py` | Luma's study/bedroom interior |
| `LTG_TOOL_bg_classroom.py` | Millbrook school classroom |
| `LTG_TOOL_bg_tech_den.py` | Cosmo's tech den/workspace |
| `LTG_TOOL_bg_grandma_kitchen.py` | Grandma Miri's kitchen |
| `LTG_TOOL_bg_school_hallway.py` | Millbrook school hallway |
| `LTG_TOOL_bg_millbrook_main_street.py` | Millbrook main street exterior |
| `LTG_TOOL_env_grandma_living_room.py` | Grandma Miri's living room |

### Style Frame Generators

| Filename | Description |
|---|---|
| `LTG_TOOL_style_frame_02_glitch_storm.py` | SF02 "Glitch Storm" full style frame |
| `LTG_TOOL_style_frame_03_other_side.py` | SF03 "The Other Side" full style frame |
| `LTG_TOOL_style_frame_04_resolution.py` | SF04 "Resolution" style frame |
| `LTG_TOOL_style_frame_05_relationship.py` | SF05 "Relationship" style frame |
| `LTG_TOOL_sf04_luma_byte_v005.py` | SF04 Luma+Byte composition |
| `LTG_TOOL_sf_covetous_glitch.py` | Covetous Glitch style frame |
| `LTG_TOOL_sf_covetous_glitch_c43.py` | Covetous Glitch style frame (C43 revision) |
| `LTG_TOOL_sf02_fill_light_fix_c35.py` | SF02 fill-light fix pass |
| `LTG_TOOL_sf_miri_luma_handoff.py` | Miri-Luma handoff style frame |
| `LTG_TOOL_styleframe_discovery.py` | SF01 "Discovery" style frame |
| `LTG_TOOL_styleframe_discovery_scenelit.py` | SF01 Discovery with scene lighting |
| `LTG_TOOL_styleframe_glitch_layer_showcase.py` | Glitch Layer showcase style frame |
| `LTG_TOOL_styleframe_luma_byte.py` | Luma+Byte character style frame |
| `LTG_TOOL_colorkey_glitchstorm_gen.py` | Color key thumbnail for Glitch Storm |
| `LTG_TOOL_colorkey_otherside_gen.py` | Color key thumbnail for Other Side |
| `LTG_TOOL_colorkey_glitch_covetous_gen.py` | Color key thumbnail for Covetous Glitch |

### Storyboard Generators

| Filename | Description |
|---|---|
| `LTG_TOOL_pilot_cold_open.py` | Pilot cold open sequence generator |
| `LTG_TOOL_sb_pilot_cold_open.py` | Pilot cold open storyboard panels |
| `LTG_TOOL_sb_char_draw.py` | Storyboard character drawing helper |
| `LTG_TOOL_sb_caption_retrofit.py` | Retrofit captions onto existing panels |
| `LTG_TOOL_sb_cold_open_P{02-25}.py` | Cold open panels P02-P25 (22 generators). Cairo/pycairo: P02, P04, P09, P10, P12, P13, P15, P17, P20, P21, P23. PIL: P03, P05, P06-P08, P11, P14, P16, P18, P19, P22, P22a, P24, P25. Also P17_chartest. |
| `LTG_TOOL_sb_panel_a10{1-4}*.py` | Act 1 panels A1-01 through A1-04 (4 generators; a104 = kitchen) |
| `LTG_TOOL_sb_panel_a20{1-8}*.py` | Act 2 panels A2-01 through A2-08 (9 generators; includes a206_insert, a207b) |
| `LTG_TOOL_sb_act1_contact_sheet.py` | Act 1 contact sheet |
| `LTG_TOOL_sb_act1_full_contact_sheet.py` | Act 1 full contact sheet |
| `LTG_TOOL_sb_act2_contact_sheet.py` | Act 2 contact sheet |
| `LTG_TOOL_sb_a2_cycle15.py` | Act 2 storyboard batch (C15) |
| `LTG_TOOL_sb_ep05_covetous.py` | Episode 5 "Covetous" storyboard |
| `LTG_TOOL_act2_panels_cycle14.py` | Act 2 panel batch (C14) |
| `LTG_TOOL_cycle13_panel_fixes.py` | Cycle 13 panel fix batch |
| `LTG_TOOL_contact_sheet_arc_diff.py` | Contact sheet arc-to-arc diff viewer |

### Motion Generators

| Filename | Description |
|---|---|
| `LTG_TOOL_byte_motion.py` | Byte motion/animation poses |
| `LTG_TOOL_miri_motion.py` | Miri motion/animation poses |
| `LTG_TOOL_miri_motion_v002.py` | Miri motion v002 |
| `LTG_TOOL_cosmo_motion.py` | Cosmo motion spec sheet (gesture-first pycairo, C53) |
| `LTG_TOOL_glitch_motion.py` | Glitchkin motion/animation poses |

### QA / Lint Tools

| Filename | Description |
|---|---|
| `LTG_TOOL_proportion_verify.py` | Proportion verification pass |
| `LTG_TOOL_color_verify.py` | Color palette verification |
| `LTG_TOOL_char_spec_lint.py` | Character spec compliance linter |
| `LTG_TOOL_glitch_spec_lint.py` | Glitchkin spec compliance linter |
| `LTG_TOOL_motion_spec_lint.py` | Motion spec compliance linter |
| `LTG_TOOL_alpha_blend_lint.py` | Alpha-blend correctness linter |
| `LTG_TOOL_draw_order_lint.py` | Draw-order layer validation |
| `LTG_TOOL_palette_warmth_lint.py` | Palette warmth balance linter |
| `LTG_TOOL_uv_purple_linter.py` | UV Purple usage compliance linter |
| `LTG_TOOL_uv_hue_survey_c46.py` | UV hue survey (C46) |
| `LTG_TOOL_stub_linter.py` | Stub/placeholder detection linter |
| `LTG_TOOL_warm_pixel_metric.py` | Warm pixel percentage metric |
| `LTG_TOOL_composite_warmth_score.py` | Composite warmth scoring |
| `LTG_TOOL_precritique_qa.py` | Pre-critique QA pipeline runner |
| `LTG_TOOL_depth_temp_lint.py` | Depth-temperature correlation linter |
| `LTG_TOOL_gesture_line_lint.py` | Gesture line quality linter |
| `LTG_TOOL_face_curve_validator.py` | Face curve geometry validator |
| `LTG_TOOL_expression_target_qa.py` | Expression target QA checker |
| `LTG_TOOL_expression_range_metric.py` | Expression range diversity metric |
| `LTG_TOOL_sightline_validator.py` | Sight-line validation pass |
| `LTG_TOOL_silhouette_distinctiveness.py` | Silhouette distinctiveness metric |
| `LTG_TOOL_multi_char_face_gate.py` | Multi-character face test gate |
| `LTG_TOOL_face_landmark_detector.py` | Face landmark detection |
| `LTG_TOOL_face_metric_calibrate.py` | Face metric calibration |
| `LTG_TOOL_render_qa.py` | Render output QA validator |
| `LTG_TOOL_rendering_comparison.py` | Before/after rendering comparison |
| `LTG_TOOL_warmcool_scene_calibrate.py` | Warm/cool scene calibration |
| `LTG_TOOL_construction_stiffness.py` | Construction-line stiffness metric |
| `LTG_TOOL_character_face_test.py` | Character face test gate (automated) |

### Pipeline / CI Tools

| Filename | Description |
|---|---|
| `LTG_TOOL_spec_sync_ci.py` | Spec-to-asset sync CI check |
| `LTG_TOOL_ci_suite.py` | Full CI suite runner |
| `LTG_TOOL_readme_sync.py` | README auto-sync from tool registry |
| `LTG_TOOL_naming_compliance_copier.py` | Batch LTG-naming compliance copier |
| `LTG_TOOL_naming_compliance_copy.py` | Naming compliance copy (variant) |
| `LTG_TOOL_naming_cleanup.py` | Remove pre-LTG originals after copy |
| `LTG_TOOL_batch_path_migrate.py` | Batch file path migration |
| `LTG_TOOL_doc_governance_audit.py` | Documentation governance audit |
| `LTG_TOOL_char_interface.py` | Character renderer interface contract and modular compliance scanner |

### Utility Tools

| Filename | Description |
|---|---|
| `LTG_TOOL_project_paths.py` | Canonical project path constants |
| `LTG_TOOL_spec_extractor.py` | Spec data extractor |
| `LTG_TOOL_char_diff.py` | Character-to-character visual diff |
| `LTG_TOOL_char_compare.py` | Character side-by-side comparison |
| `LTG_TOOL_world_type_infer.py` | World type (Real/Glitch) inference from image |
| `LTG_TOOL_freetype_eval.py` | FreeType font rendering evaluation |
| `LTG_TOOL_engine_benchmark_c51.py` | Rendering engine benchmark (C51) |
| `LTG_TOOL_library_eval_c51.py` | Library capability evaluation (C51) |
| `LTG_TOOL_wand_compositing_eval.py` | Wand (ImageMagick) compositing evaluation |
| `LTG_TOOL_wand_composite.py` | Wand-based image compositing |

---

> Deprecated tools live in `deprecated/`. Do not run or import. See `git log` for history.
