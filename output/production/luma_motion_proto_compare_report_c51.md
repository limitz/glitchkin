# Character Comparison Report

**Old:** `/home/wipkat/team/output/characters/motion/LTG_CHAR_luma_motion_proto_old.png`
**New:** `/home/wipkat/team/output/characters/motion/LTG_CHAR_luma_motion_proto_new.png`
**Grade:** MAJOR_CHANGE

## Metrics

| Metric | Value |
|--------|-------|
| SSIM | 0.8336 |
| Pixel Delta | 16.3% |
| Mean Abs Diff | 21.9 |
| Silhouette IoU | 0.2116 |
| FG Pixel Delta | 99.8% |
| Hue Shift (mean) | 28.7 deg |
| Value Shift (mean) | -40.3 |

**Comparison PNG:** `/home/wipkat/team/output/characters/motion/LTG_CHAR_luma_motion_proto_compare_c51.png`

## Interpretation

Significant silhouette change detected. Verify character identity is preserved.

**WARNING:** Silhouette IoU below 0.80 — character shape changed significantly.

**NOTE:** Mean hue shift > 15 degrees — color palette may have shifted.