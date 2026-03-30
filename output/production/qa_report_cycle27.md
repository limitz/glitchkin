<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# LTG Render QA Report — Cycle 27

**Generated:** 2026-03-29  
**Tool:** LTG_TOOL_render_qa.py v1.1.0  
**Total assets evaluated:** 29

## Summary

| File | Asset Type | Silhouette | Value Range | Color Fidelity | Warm/Cool | Line Weight | Grade |
|------|-----------|-----------|-------------|----------------|-----------|-------------|-------|
| LTG_CHAR_luma_expression_sheet.png | character_sheet | distinct | PASS | WARN | SKIP | PASS | **WARN** |
| LTG_CHAR_byte_expression_sheet.png | character_sheet | distinct | PASS | PASS | SKIP | PASS | PASS |
| LTG_CHAR_cosmo_expression_sheet.png | character_sheet | distinct | PASS | PASS | SKIP | PASS | PASS |
| LTG_CHAR_grandma_miri_expression_sheet.png | character_sheet | distinct | PASS | WARN | SKIP | PASS | **WARN** |
| LTG_CHAR_glitch_expression_sheet.png | character_sheet | distinct | PASS | PASS | SKIP | WARN | **WARN** |
| LTG_CHAR_lineup.png | character_sheet | blob | PASS | WARN | SKIP | PASS | **FAIL** |
| LTG_CHAR_luma_turnaround.png | character_sheet | distinct | PASS | WARN | SKIP | PASS | **WARN** |
| LTG_CHAR_byte_turnaround.png | character_sheet | distinct | PASS | PASS | SKIP | PASS | PASS |
| LTG_CHAR_cosmo_turnaround.png | character_sheet | distinct | PASS | PASS | SKIP | PASS | PASS |
| LTG_CHAR_miri_turnaround.png | character_sheet | distinct | PASS | PASS | SKIP | WARN | **WARN** |
| LTG_CHAR_glitch_turnaround.png | character_sheet | ambiguous | WARN | WARN | SKIP | PASS | **WARN** |
| LTG_COLOR_luma_color_model.png | color_model | distinct | PASS | WARN | SKIP | PASS | **WARN** |
| LTG_COLOR_byte_color_model.png | color_model | distinct | PASS | PASS | SKIP | PASS | PASS |
| LTG_COLOR_cosmo_color_model.png | color_model | distinct | PASS | PASS | SKIP | PASS | PASS |
| LTG_COLOR_grandma_miri_color_model.png | color_model | distinct | PASS | WARN | SKIP | PASS | **WARN** |
| LTG_COLOR_glitch_color_model.png | color_model | distinct | PASS | WARN | SKIP | WARN | **WARN** |
| LTG_COLOR_styleframe_discovery.png | style_frame | distinct | PASS | PASS | WARN | PASS | **WARN** |
| LTG_COLOR_styleframe_glitch_storm.png | style_frame | distinct | PASS | PASS | WARN | PASS | **WARN** |
| LTG_COLOR_styleframe_otherside.png | style_frame | distinct | PASS | WARN | WARN | PASS | **WARN** |
| LTG_COLOR_styleframe_luma_byte.png | style_frame | distinct | PASS | WARN | WARN | PASS | **WARN** |
| LTG_ENV_tech_den.png | environment | distinct | WARN | PASS | WARN | PASS | **WARN** |
| LTG_ENV_school_hallway.png | environment | distinct | WARN | WARN | PASS | PASS | **WARN** |
| LTG_ENV_millbrook_main_street.png | environment | distinct | WARN | PASS | PASS | PASS | **WARN** |
| LTG_ENV_classroom_bg.png | environment | blob | PASS | WARN | WARN | WARN | **FAIL** |
| LTG_ENV_grandma_kitchen.png | environment | distinct | WARN | PASS | WARN | WARN | **WARN** |
| LTG_ENV_other_side_bg.png | environment | distinct | PASS | WARN | WARN | PASS | **WARN** |
| LTG_ENV_glitchlayer_frame.png | environment | distinct | PASS | PASS | WARN | PASS | **WARN** |
| LTG_ENV_glitch_storm_bg.png | environment | distinct | PASS | PASS | WARN | PASS | **WARN** |
| LTG_ENV_lumashome_study_interior.png | environment | distinct | PASS | PASS | WARN | PASS | **WARN** |

**Results:** 6 PASS / 21 WARN / 2 FAIL

---

## Detailed Results

### LTG_CHAR_luma_expression_sheet.png
*Asset type: character_sheet*

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=255, range=255

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: target=185.2° found=182.6° delta=2.6° [PASS]
  - UV_PURPLE: not_found
  - HOT_MAGENTA: target=342.3° found=340.8° delta=1.5° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=180.0° delta=3.5° [PASS]
  - SUNLIT_AMBER: target=34.3° found=25.1° delta=9.2° [FAIL]

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** PASS — mean=31.7px, std=87.41px, outliers=1

---

### LTG_CHAR_byte_expression_sheet.png
*Asset type: character_sheet*

**Overall Grade:** PASS

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=10, max=255, range=245

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: target=185.2° found=185.2° delta=0.0° [PASS]
  - UV_PURPLE: not_found
  - HOT_MAGENTA: target=342.3° found=342.3° delta=0.0° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=185.2° delta=1.6° [PASS]
  - SUNLIT_AMBER: not_found

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** PASS — mean=27.6px, std=73.25px, outliers=2

---

### LTG_CHAR_cosmo_expression_sheet.png
*Asset type: character_sheet*

**Overall Grade:** PASS

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=15, max=241, range=226

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: not_found

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** PASS — mean=4.8px, std=7.49px, outliers=1

---

### LTG_CHAR_grandma_miri_expression_sheet.png
*Asset type: character_sheet*

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=1, max=255, range=254

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: target=34.3° found=18.1° delta=16.2° [FAIL]

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** PASS — mean=80.15px, std=149.98px, outliers=0

---

### LTG_CHAR_glitch_expression_sheet.png
*Asset type: character_sheet*

**Overall Grade:** WARN

**WARN conditions:**
- line_weight: inconsistent widths

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=250, range=250

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: target=32.9° found=33.3° delta=0.4° [PASS]
  - BYTE_TEAL: target=185.2° found=183.6° delta=1.6° [PASS]
  - UV_PURPLE: target=271.9° found=272.1° delta=0.2° [PASS]
  - HOT_MAGENTA: target=342.3° found=342.0° delta=0.3° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=181.6° delta=1.9° [PASS]
  - SUNLIT_AMBER: target=34.3° found=36.5° delta=2.2° [PASS]

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** WARN — mean=58.95px, std=136.53px, outliers=3
  - Line weight inconsistency — 3 outlier widths detected (mean=59.0px, std=136.5px)

---

### LTG_CHAR_lineup.png
*Asset type: character_sheet*

**Overall Grade:** FAIL

**FAIL conditions:**
- silhouette=blob

**WARN conditions:**
- color_fidelity: hue drift detected

**A. Silhouette:** `blob`

**B. Value Range:** PASS — min=0, max=255, range=255

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: target=32.9° found=32.9° delta=0.0° [PASS]
  - BYTE_TEAL: target=185.2° found=185.2° delta=0.0° [PASS]
  - UV_PURPLE: target=271.9° found=271.9° delta=0.0° [PASS]
  - HOT_MAGENTA: target=342.3° found=342.1° delta=0.2° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=185.2° delta=1.6° [PASS]
  - SUNLIT_AMBER: target=34.3° found=22.8° delta=11.5° [FAIL]

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** PASS — mean=429.05px, std=590.68px, outliers=0

---

### LTG_CHAR_luma_turnaround.png
*Asset type: character_sheet*

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=255, range=255

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: target=185.2° found=182.7° delta=2.5° [PASS]
  - UV_PURPLE: not_found
  - HOT_MAGENTA: target=342.3° found=342.8° delta=0.5° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=182.8° delta=0.8° [PASS]
  - SUNLIT_AMBER: target=34.3° found=25.1° delta=9.2° [FAIL]

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** PASS — mean=19.75px, std=29.86px, outliers=1

---

### LTG_CHAR_byte_turnaround.png
*Asset type: character_sheet*

**Overall Grade:** PASS

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=13, max=250, range=237

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: not_found

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** PASS — mean=187.25px, std=315.77px, outliers=0

---

### LTG_CHAR_cosmo_turnaround.png
*Asset type: character_sheet*

**Overall Grade:** PASS

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=1, max=255, range=254

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: not_found

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** PASS — mean=13.2px, std=35.53px, outliers=1

---

### LTG_CHAR_miri_turnaround.png
*Asset type: character_sheet*

**Overall Grade:** WARN

**WARN conditions:**
- line_weight: inconsistent widths

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=255, range=255

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: target=34.3° found=29.8° delta=4.5° [PASS]

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** WARN — mean=211.6px, std=465.88px, outliers=3
  - Line weight inconsistency — 3 outlier widths detected (mean=211.6px, std=465.9px)

---

### LTG_CHAR_glitch_turnaround.png
*Asset type: character_sheet*

**Overall Grade:** WARN

**WARN conditions:**
- silhouette=ambiguous
- value_range: compressed or missing extreme
- color_fidelity: hue drift detected

**A. Silhouette:** `ambiguous`

**B. Value Range:** WARN — min=2, max=207, range=205
  - No bright highlights — brightest pixel is 207 (threshold ≥ 225)

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: target=32.9° found=33.3° delta=0.4° [PASS]
  - BYTE_TEAL: not_found
  - UV_PURPLE: target=271.9° found=272.4° delta=0.5° [PASS]
  - HOT_MAGENTA: target=342.3° found=349.6° delta=7.3° [FAIL]
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: target=34.3° found=38.2° delta=3.9° [PASS]

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** PASS — mean=4.3px, std=3.84px, outliers=1

---

### LTG_COLOR_luma_color_model.png
*Asset type: color_model*

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=12, max=241, range=229

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: target=185.2° found=183.5° delta=1.6° [PASS]
  - UV_PURPLE: not_found
  - HOT_MAGENTA: target=342.3° found=342.3° delta=0.0° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=183.5° delta=0.0° [PASS]
  - SUNLIT_AMBER: target=34.3° found=18.6° delta=15.7° [FAIL]

**D. Warm/Cool Separation:** SKIPPED — color_model — uniform bg by design

**E. Line Weight:** PASS — mean=2.9px, std=1.59px, outliers=0

---

### LTG_COLOR_byte_color_model.png
*Asset type: color_model*

**Overall Grade:** PASS

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=8, max=244, range=236

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: target=185.2° found=185.2° delta=0.0° [PASS]
  - UV_PURPLE: target=271.9° found=271.9° delta=0.0° [PASS]
  - HOT_MAGENTA: target=342.3° found=342.3° delta=0.0° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=185.2° delta=1.6° [PASS]
  - SUNLIT_AMBER: not_found

**D. Warm/Cool Separation:** SKIPPED — color_model — uniform bg by design

**E. Line Weight:** PASS — mean=4.7px, std=7.51px, outliers=1

---

### LTG_COLOR_cosmo_color_model.png
*Asset type: color_model*

**Overall Grade:** PASS

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=8, max=243, range=235

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: not_found

**D. Warm/Cool Separation:** SKIPPED — color_model — uniform bg by design

**E. Line Weight:** PASS — mean=8.95px, std=14.75px, outliers=1

---

### LTG_COLOR_grandma_miri_color_model.png
*Asset type: color_model*

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=6, max=255, range=249

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: target=34.3° found=19.7° delta=14.6° [FAIL]

**D. Warm/Cool Separation:** SKIPPED — color_model — uniform bg by design

**E. Line Weight:** PASS — mean=89.8px, std=219.87px, outliers=2

---

### LTG_COLOR_glitch_color_model.png
*Asset type: color_model*

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected
- line_weight: inconsistent widths

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=11, max=245, range=234

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: target=32.9° found=32.9° delta=0.0° [PASS]
  - BYTE_TEAL: target=185.2° found=183.5° delta=1.6° [PASS]
  - UV_PURPLE: target=271.9° found=271.9° delta=0.0° [PASS]
  - HOT_MAGENTA: target=342.3° found=342.3° delta=0.0° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=183.5° delta=0.0° [PASS]
  - SUNLIT_AMBER: target=34.3° found=40.0° delta=5.7° [FAIL]

**D. Warm/Cool Separation:** SKIPPED — color_model — uniform bg by design

**E. Line Weight:** WARN — mean=8.5px, std=12.61px, outliers=3
  - Line weight inconsistency — 3 outlier widths detected (mean=8.5px, std=12.6px)

---

### LTG_COLOR_styleframe_discovery.png
*Asset type: style_frame*

**Overall Grade:** WARN

**WARN conditions:**
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=255, range=255

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: target=32.9° found=33.2° delta=0.2° [PASS]
  - BYTE_TEAL: target=185.2° found=183.6° delta=1.5° [PASS]
  - UV_PURPLE: not_found
  - HOT_MAGENTA: target=342.3° found=341.3° delta=1.0° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=183.6° delta=0.0° [PASS]
  - SUNLIT_AMBER: target=34.3° found=35.2° delta=0.9° [PASS]

**D. Warm/Cool Separation:** WARN — zone_a=40.09, zone_b=24.55, separation=15.55
  - Flat palette — warm/cool separation is 15.5 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=89.05px, std=123.27px, outliers=1

---

### LTG_COLOR_styleframe_glitch_storm.png
*Asset type: style_frame*

**Overall Grade:** WARN

**WARN conditions:**
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=255, range=255

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: target=32.9° found=34.4° delta=1.4° [PASS]
  - BYTE_TEAL: target=185.2° found=183.5° delta=1.6° [PASS]
  - UV_PURPLE: not_found
  - HOT_MAGENTA: target=342.3° found=340.7° delta=1.6° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=183.2° delta=0.3° [PASS]
  - SUNLIT_AMBER: target=34.3° found=34.7° delta=0.4° [PASS]

**D. Warm/Cool Separation:** WARN — zone_a=176.54, zone_b=170.0, separation=6.54
  - Flat palette — warm/cool separation is 6.5 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=5.5px, std=6.05px, outliers=2

---

### LTG_COLOR_styleframe_otherside.png
*Asset type: style_frame*

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=255, range=255

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: target=32.9° found=29.3° delta=3.6° [PASS]
  - BYTE_TEAL: target=185.2° found=184.5° delta=0.7° [PASS]
  - UV_PURPLE: target=271.9° found=262.7° delta=9.2° [FAIL]
  - HOT_MAGENTA: target=342.3° found=342.3° delta=0.0° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=183.5° delta=0.0° [PASS]
  - SUNLIT_AMBER: target=34.3° found=25.0° delta=9.3° [FAIL]

**D. Warm/Cool Separation:** WARN — zone_a=177.97, zone_b=187.71, separation=9.74
  - Flat palette — warm/cool separation is 9.7 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=192.1px, std=385.71px, outliers=2

---

### LTG_COLOR_styleframe_luma_byte.png
*Asset type: style_frame*

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

### LTG_ENV_tech_den.png
*Asset type: environment*

**Overall Grade:** WARN

**WARN conditions:**
- value_range: compressed or missing extreme
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** WARN — min=31, max=239, range=208
  - No deep darks — darkest pixel is 31 (threshold ≤ 30)

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: not_found

**D. Warm/Cool Separation:** WARN — zone_a=31.48, zone_b=23.61, separation=7.87
  - Flat palette — warm/cool separation is 7.9 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=101.1px, std=146.85px, outliers=1

---

### LTG_ENV_school_hallway.png
*Asset type: environment*

**Overall Grade:** WARN

**WARN conditions:**
- value_range: compressed or missing extreme
- color_fidelity: hue drift detected

**A. Silhouette:** `distinct`

**B. Value Range:** WARN — min=45, max=236, range=191
  - No deep darks — darkest pixel is 45 (threshold ≤ 30)

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: target=34.3° found=44.0° delta=9.7° [FAIL]

**D. Warm/Cool Separation:** PASS — zone_a=132.22, zone_b=67.29, separation=64.93

**E. Line Weight:** PASS — mean=156.7px, std=385.75px, outliers=2

---

### LTG_ENV_millbrook_main_street.png
*Asset type: environment*

**Overall Grade:** WARN

**WARN conditions:**
- value_range: compressed or missing extreme

**A. Silhouette:** `distinct`

**B. Value Range:** WARN — min=45, max=239, range=194
  - No deep darks — darkest pixel is 45 (threshold ≤ 30)

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: target=34.3° found=31.8° delta=2.5° [PASS]

**D. Warm/Cool Separation:** PASS — zone_a=65.38, zone_b=19.83, separation=45.55

**E. Line Weight:** PASS — mean=11.8px, std=18.36px, outliers=1

---

### LTG_ENV_classroom_bg.png
*Asset type: environment*

**Overall Grade:** FAIL

**FAIL conditions:**
- silhouette=blob

**WARN conditions:**
- color_fidelity: hue drift detected
- warm_cool: insufficient separation
- line_weight: inconsistent widths

**A. Silhouette:** `blob`

**B. Value Range:** PASS — min=10, max=252, range=242

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: target=34.3° found=44.6° delta=10.3° [FAIL]

**D. Warm/Cool Separation:** WARN — zone_a=35.42, zone_b=46.2, separation=10.78
  - Flat palette — warm/cool separation is 10.8 PIL units (minimum 20.0 required)

**E. Line Weight:** WARN — mean=414.65px, std=408.57px, outliers=3
  - Line weight inconsistency — 3 outlier widths detected (mean=414.6px, std=408.6px)

---

### LTG_ENV_grandma_kitchen.png
*Asset type: environment*

**Overall Grade:** WARN

**WARN conditions:**
- value_range: compressed or missing extreme
- warm_cool: insufficient separation
- line_weight: inconsistent widths

**A. Silhouette:** `distinct`

**B. Value Range:** WARN — min=62, max=252, range=190
  - No deep darks — darkest pixel is 62 (threshold ≤ 30)

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: target=34.3° found=34.8° delta=0.5° [PASS]

**D. Warm/Cool Separation:** WARN — zone_a=30.0, zone_b=28.33, separation=1.67
  - Flat palette — warm/cool separation is 1.7 PIL units (minimum 20.0 required)

**E. Line Weight:** WARN — mean=330.8px, std=442.33px, outliers=3
  - Line weight inconsistency — 3 outlier widths detected (mean=330.8px, std=442.3px)

---

### LTG_ENV_other_side_bg.png
*Asset type: environment*

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=255, range=255

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: target=32.9° found=29.2° delta=3.8° [PASS]
  - BYTE_TEAL: target=185.2° found=184.8° delta=0.4° [PASS]
  - UV_PURPLE: target=271.9° found=257.8° delta=14.1° [FAIL]
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: target=183.5° found=182.6° delta=0.9° [PASS]
  - SUNLIT_AMBER: target=34.3° found=28.2° delta=6.1° [FAIL]

**D. Warm/Cool Separation:** WARN — zone_a=182.59, zone_b=188.75, separation=6.16
  - Flat palette — warm/cool separation is 6.2 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=153.85px, std=168.2px, outliers=0

---

### LTG_ENV_glitchlayer_frame.png
*Asset type: environment*

**Overall Grade:** WARN

**WARN conditions:**
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=243, range=243

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: target=185.2° found=183.4° delta=1.8° [PASS]
  - UV_PURPLE: target=271.9° found=271.9° delta=0.0° [PASS]
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: target=183.5° found=183.4° delta=0.1° [PASS]
  - SUNLIT_AMBER: not_found

**D. Warm/Cool Separation:** WARN — zone_a=170.0, zone_b=170.0, separation=0.0
  - Flat palette — warm/cool separation is 0.0 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=256.1px, std=365.43px, outliers=0

---

### LTG_ENV_glitch_storm_bg.png
*Asset type: environment*

**Overall Grade:** WARN

**WARN conditions:**
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=255, range=255

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: target=185.2° found=183.5° delta=1.6° [PASS]
  - UV_PURPLE: target=271.9° found=271.9° delta=0.0° [PASS]
  - HOT_MAGENTA: target=342.3° found=341.6° delta=0.7° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=182.8° delta=0.7° [PASS]
  - SUNLIT_AMBER: not_found

**D. Warm/Cool Separation:** WARN — zone_a=176.54, zone_b=170.0, separation=6.54
  - Flat palette — warm/cool separation is 6.5 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=38.45px, std=140.11px, outliers=1

---

### LTG_ENV_lumashome_study_interior.png
*Asset type: environment*

**Overall Grade:** WARN

**WARN conditions:**
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=246, range=246

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: target=32.9° found=28.7° delta=4.2° [PASS]
  - BYTE_TEAL: target=185.2° found=185.7° delta=0.6° [PASS]
  - UV_PURPLE: not_found
  - HOT_MAGENTA: target=342.3° found=340.9° delta=1.4° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=183.7° delta=0.1° [PASS]
  - SUNLIT_AMBER: target=34.3° found=36.5° delta=2.2° [PASS]

**D. Warm/Cool Separation:** WARN — zone_a=31.87, zone_b=25.25, separation=6.62
  - Flat palette — warm/cool separation is 6.6 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=77.3px, std=147.31px, outliers=2

---
