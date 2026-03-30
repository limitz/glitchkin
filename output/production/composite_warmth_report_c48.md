# Composite Warmth Score Report

**Generated:** 2026-03-30 16:06
**Tool:** LTG_TOOL_composite_warmth_score.py v1.0.0
**Author:** Sam Kowalski (Color & Style Artist)
**Cycle:** 48

---

## Methodology

Composite warmth score combines two metrics:

1. **Warm-pixel-percentage** (weight 70%): fraction of chromatic pixels
   with PIL HSV hue in the warm range (0-42 or 213-255).
2. **Hue-split separation** (weight 30%): circular hue distance between
   median hue of top-half and bottom-half of the image.

Formula: `composite = 0.7 * (warm_pct / 100) + 0.3 * min(hue_split / 127.5, 1.0)`

| World Type | Threshold | Direction |
|---|---|---|
| REAL_INTERIOR | >= 0.25 | Above |
| REAL_STORM | >= 0.04 | Above |
| GLITCH | <= 0.12 | Below |
| OTHER_SIDE | <= 0.04 | Below |

---

## Summary

- **Images analyzed:** 19
- **PASS:** 19
- **FAIL:** 0
- **Composite range:** 0.0071 -- 0.6727
- **Composite median:** 0.4485

---

## reference/living room night

| File | Size | Warm% | Cool% | Hue-Split | Composite | World | Verdict |
|---|---|---|---|---|---|---|---|
| a-living-room-with-a-view-of-the-city-at-night-ai-generated-photo.jpg | 525x350 | 48.2% | 45.7% | 123.4 | 0.6277 | REAL_INTERIOR | PASS |
| dark-vintage-living-room-large-260nw-2632950729.webp | 462x280 | 42.0% | 32.0% | 2.0 | 0.2990 | REAL_INTERIOR | PASS |
| gettyimages-1212170511-612x612.jpg | 612x367 | 51.5% | 17.4% | 6.1 | 0.3749 | REAL_INTERIOR | PASS |
| interior-modern-living-room-night_1004592-10982.avif | -- | -- | -- | -- | -- | -- | SKIPPED (Unsupported format: .avif (pillow-avif not installed)) |
| istockphoto-2182807281-612x612.jpg | 612x344 | 85.8% | 3.4% | 2.3 | 0.6060 | REAL_INTERIOR | PASS |
| living-room-interior-night_1029473-770962.avif | -- | -- | -- | -- | -- | -- | SKIPPED (Unsupported format: .avif (pillow-avif not installed)) |
| table-with-vase-flowers-sign-that-says-piano-it_1221953-68128.avif | -- | -- | -- | -- | -- | -- | SKIPPED (Unsupported format: .avif (pillow-avif not installed)) |

## reference/kitchen predawn

| File | Size | Warm% | Cool% | Hue-Split | Composite | World | Verdict |
|---|---|---|---|---|---|---|---|
| image-11854.jpg | 1344x768 | 60.9% | 31.5% | 5.0 | 0.4382 | REAL_INTERIOR | PASS |
| image-13179.jpg | 1344x768 | 84.1% | 8.8% | 0.6 | 0.5903 | REAL_INTERIOR | PASS |
| low-kitchen-ceiling-lights-985165.webp | 1456x832 | 96.1% | 0.6% | 0.1 | 0.6727 | REAL_INTERIOR | PASS |

## output/color/style_frames

| File | Size | Warm% | Cool% | Hue-Split | Composite | World | Verdict |
|---|---|---|---|---|---|---|---|
| .gitkeep | -- | -- | -- | -- | -- | -- | SKIPPED (Unsupported format: ) |
| LTG_COLOR_sf_covetous_glitch.png | 1280x720 | 2.2% | 9.5% | 0.9 | 0.0179 | GLITCH | PASS |
| LTG_COLOR_sf_final_check_c23.md | -- | -- | -- | -- | -- | -- | SKIPPED (Unsupported format: .md) |
| LTG_COLOR_sf_miri_luma_handoff.png | 1280x720 | 61.5% | 4.4% | 16.9 | 0.4706 | REAL_INTERIOR | PASS |
| LTG_COLOR_styleframe_discovery.png | 1280x720 | 58.1% | 37.0% | 17.9 | 0.4485 | REAL_INTERIOR | PASS |
| LTG_COLOR_styleframe_glitch_layer_showcase.png | 1280x720 | 0.1% | 4.8% | 2.7 | 0.0071 | GLITCH | PASS |
| LTG_COLOR_styleframe_glitch_storm.png | 1280x720 | 11.1% | 50.8% | 6.5 | 0.0931 | REAL_STORM | PASS |
| LTG_COLOR_styleframe_luma_byte.png | 1280x720 | 95.6% | 4.4% | 1.1 | 0.6716 | REAL_INTERIOR | PASS |
| LTG_COLOR_styleframe_otherside.png | 1280x720 | 1.6% | 24.7% | 2.2 | 0.0166 | OTHER_SIDE | PASS |
| LTG_COLOR_styleframe_sf04.png | 1280x720 | 76.5% | 2.4% | 13.1 | 0.5660 | REAL_INTERIOR | PASS |
| LTG_COLOR_styleframe_sf05.png | 1280x720 | 74.8% | 18.6% | 16.7 | 0.5625 | REAL_INTERIOR | PASS |
| LTG_SF_covetous_glitch_v001.png | 1280x720 | 0.7% | 10.6% | 1.4 | 0.0085 | GLITCH | PASS |
| LTG_SF_luma_byte_v005.png | 1280x720 | 69.2% | 22.2% | 27.9 | 0.5497 | REAL_INTERIOR | PASS |
| LTG_TOOL_style_frame_02_glitch_storm.py | -- | -- | -- | -- | -- | -- | SKIPPED (Unsupported format: .py) |
| ltg_style_frame_color_story.md | -- | -- | -- | -- | -- | -- | SKIPPED (Unsupported format: .md) |
| sf02_color_notes.md | -- | -- | -- | -- | -- | -- | SKIPPED (Unsupported format: .md) |
| sf03_color_review.md | -- | -- | -- | -- | -- | -- | SKIPPED (Unsupported format: .md) |
| sf04_resolution_color_review.md | -- | -- | -- | -- | -- | -- | SKIPPED (Unsupported format: .md) |
| style_frame_01_discovery.md | -- | -- | -- | -- | -- | -- | SKIPPED (Unsupported format: .md) |
| style_frame_01_rendered.png | 1280x720 | 58.9% | 36.2% | 13.7 | 0.4443 | REAL_INTERIOR | PASS |
| style_frame_02_glitch_storm.md | -- | -- | -- | -- | -- | -- | SKIPPED (Unsupported format: .md) |
| style_frame_03_other_side.md | -- | -- | -- | -- | -- | -- | SKIPPED (Unsupported format: .md) |

