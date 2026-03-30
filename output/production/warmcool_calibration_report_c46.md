# Warm/Cool Scene Calibration Report

**Generated:** 2026-03-30 15:06
**Tool:** LTG_TOOL_warmcool_scene_calibrate.py v1.0.0
**Threshold under test:** REAL_INTERIOR = 12.0 PIL hue units

---

## Executive Summary

- **Images analyzed:** 7
- **Validates threshold (sep >= 12.0):** 1
- **Challenges threshold (sep < 12.0):** 6
- **Mean separation:** 19.93 PIL hue units
- **Median separation:** 2.30 PIL hue units
- **Range:** 0.14 – 123.38

**Conclusion:** REAL_INTERIOR threshold of 12.0 **NEEDS ADJUSTMENT** — 6/7 photos fall below. Recommend lowering to ~1.8.

---

## Directory: `kitchen predawn/`

Files: 3 total, 3 analyzed, 0 skipped
Separation range: 0.14 – 4.99 (mean 1.9, median 0.56)

| File | Size | Separation | Warm% | Cool% | W:C Ratio | Verdict |
|------|------|-----------|-------|-------|-----------|---------|
| image-11854.jpg | 1344x768 | 5.0 | 60.9% | 31.5% | 1.94 | CHALLENGES |
| image-13179.jpg | 1344x768 | 0.6 | 84.1% | 8.8% | 9.6 | CHALLENGES |
| low-kitchen-ceiling-lights-985165.webp | 1456x832 | 0.1 | 96.1% | 0.6% | 159.73 | CHALLENGES |

## Directory: `living room night/`

Files: 7 total, 4 analyzed, 3 skipped
Separation range: 2.04 – 123.38 (mean 33.45, median 4.19)

| File | Size | Separation | Warm% | Cool% | W:C Ratio | Verdict |
|------|------|-----------|-------|-------|-----------|---------|
| a-living-room-with-a-view-of-the-city-at-night-ai-generated-photo.jpg | 525x350 | 123.4 | 48.2% | 45.7% | 1.05 | VALIDATES |
| dark-vintage-living-room-large-260nw-2632950729.webp | 462x280 | 2.0 | 42.0% | 32.0% | 1.31 | CHALLENGES |
| gettyimages-1212170511-612x612.jpg | 612x367 | 6.1 | 51.5% | 17.4% | 2.96 | CHALLENGES |
| interior-modern-living-room-night_1004592-10982.avif | — | — | — | — | — | SKIPPED: Unsupported format: .avif (pillow-avif not installed) |
| istockphoto-2182807281-612x612.jpg | 612x344 | 2.3 | 85.8% | 3.4% | 25.15 | CHALLENGES |
| living-room-interior-night_1029473-770962.avif | — | — | — | — | — | SKIPPED: Unsupported format: .avif (pillow-avif not installed) |
| table-with-vase-flowers-sign-that-says-piano-it_1221953-68128.avif | — | — | — | — | — | SKIPPED: Unsupported format: .avif (pillow-avif not installed) |

---

## Threshold Context

| World Type | Threshold | Source |
|-----------|-----------|--------|
| REAL_INTERIOR | 12.0 | render_qa v1.6.0, warmth_lint_v004 |
| REAL_STORM | 3.0 | render_qa v1.6.0 |
| GLITCH | 3.0 | render_qa v1.6.0 |
| OTHER_SIDE | 0.0 | render_qa v1.6.0 |

## Metric Definition

Warm/cool separation = circular distance between median PIL HSV hue of
top half and bottom half of the image, on a 0–255 scale. This is the
same metric used by `LTG_TOOL_render_qa.py _check_warm_cool()`. Pixels
with saturation < 5% are excluded as achromatic.
