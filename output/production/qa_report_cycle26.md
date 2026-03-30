<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# LTG Render QA Report — Cycle 26

**Generated:** 2026-03-29  
**Tool:** LTG_TOOL_render_qa.py  
**Total assets evaluated:** 8

## Summary

| File | Silhouette | Value Range | Color Fidelity | Warm/Cool | Line Weight | Grade |
|------|-----------|-------------|----------------|-----------|-------------|-------|
| LTG_CHAR_luma_expression_sheet.png | distinct | PASS | WARN | WARN | PASS | **WARN** |
| LTG_CHAR_luma_turnaround.png | distinct | PASS | WARN | WARN | PASS | **WARN** |
| LTG_CHAR_cosmo_turnaround.png | distinct | PASS | PASS | WARN | PASS | **WARN** |
| LTG_CHAR_grandma_miri_expression_sheet.png | distinct | PASS | WARN | WARN | PASS | **WARN** |
| LTG_COLOR_styleframe_luma_byte.png | distinct | PASS | WARN | WARN | PASS | **WARN** |
| LTG_COLOR_luma_color_model.png | distinct | PASS | WARN | WARN | PASS | **WARN** |
| LTG_COLOR_byte_color_model.png | distinct | PASS | PASS | WARN | PASS | **WARN** |
| LTG_COLOR_cosmo_color_model.png | distinct | PASS | PASS | WARN | PASS | **WARN** |

**Results:** 0 PASS / 8 WARN / 0 FAIL

---

## Detailed Results

### LTG_CHAR_luma_expression_sheet.png

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=1, max=255, range=254

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: target=185.2° found=182.6° delta=2.6° [PASS]
  - UV_PURPLE: not_found
  - HOT_MAGENTA: target=342.3° found=340.8° delta=1.5° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=180.0° delta=3.5° [PASS]
  - SUNLIT_AMBER: target=34.3° found=25.1° delta=9.2° [FAIL]

**D. Warm/Cool Separation:** WARN — zone_a=25.5, zone_b=27.59, separation=2.09
  - Flat palette — warm/cool separation is 2.1 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=116.35px, std=171.94px, outliers=0

---

### LTG_CHAR_luma_turnaround.png

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=255, range=255

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: target=185.2° found=178.6° delta=6.6° [FAIL]
  - UV_PURPLE: not_found
  - HOT_MAGENTA: target=342.3° found=344.1° delta=1.8° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=180.2° delta=3.3° [PASS]
  - SUNLIT_AMBER: target=34.3° found=25.1° delta=9.2° [FAIL]

**D. Warm/Cool Separation:** WARN — zone_a=26.15, zone_b=26.15, separation=0.0
  - Flat palette — warm/cool separation is 0.0 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=73.5px, std=284.24px, outliers=1

---

### LTG_CHAR_cosmo_turnaround.png

**Overall Grade:** WARN

**WARN conditions:**
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=1, max=255, range=254

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: not_found

**D. Warm/Cool Separation:** WARN — zone_a=26.15, zone_b=26.15, separation=0.0
  - Flat palette — warm/cool separation is 0.0 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=13.2px, std=35.53px, outliers=1

---

### LTG_CHAR_grandma_miri_expression_sheet.png

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=1, max=255, range=254

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: target=34.3° found=18.1° delta=16.2° [FAIL]

**D. Warm/Cool Separation:** WARN — zone_a=23.75, zone_b=28.05, separation=4.3
  - Flat palette — warm/cool separation is 4.3 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=80.15px, std=149.98px, outliers=0

---

### LTG_COLOR_styleframe_luma_byte.png

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=233, range=233

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: target=34.3° found=46.5° delta=12.2° [FAIL]

**D. Warm/Cool Separation:** WARN — zone_a=22.79, zone_b=21.61, separation=1.18
  - Flat palette — warm/cool separation is 1.2 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=236.15px, std=314.04px, outliers=1

---

### LTG_COLOR_luma_color_model.png

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=12, max=241, range=229

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: target=185.2° found=183.5° delta=1.6° [PASS]
  - UV_PURPLE: not_found
  - HOT_MAGENTA: target=342.3° found=342.3° delta=0.0° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=183.5° delta=0.0° [PASS]
  - SUNLIT_AMBER: target=34.3° found=18.6° delta=15.7° [FAIL]

**D. Warm/Cool Separation:** WARN — zone_a=18.21, zone_b=18.89, separation=0.67
  - Flat palette — warm/cool separation is 0.7 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=2.9px, std=1.59px, outliers=0

---

### LTG_COLOR_byte_color_model.png

**Overall Grade:** WARN

**WARN conditions:**
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=8, max=244, range=236

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: target=185.2° found=185.2° delta=0.0° [PASS]
  - UV_PURPLE: target=271.9° found=271.9° delta=0.0° [PASS]
  - HOT_MAGENTA: target=342.3° found=342.3° delta=0.0° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=185.2° delta=1.6° [PASS]
  - SUNLIT_AMBER: not_found

**D. Warm/Cool Separation:** WARN — zone_a=155.83, zone_b=155.83, separation=0.0
  - Flat palette — warm/cool separation is 0.0 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=4.7px, std=7.51px, outliers=1

---

### LTG_COLOR_cosmo_color_model.png

**Overall Grade:** WARN

**WARN conditions:**
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=8, max=243, range=235

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: not_found

**D. Warm/Cool Separation:** WARN — zone_a=28.33, zone_b=28.33, separation=0.0
  - Flat palette — warm/cool separation is 0.0 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=8.95px, std=14.75px, outliers=1

---
