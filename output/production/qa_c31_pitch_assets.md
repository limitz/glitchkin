# LTG Render QA Report — Cycle 27

**Generated:** 2026-03-29  
**Tool:** LTG_TOOL_render_qa.py v1.2.0  
**Total assets evaluated:** 12

## Summary

| File | Asset Type | Silhouette | Value Range | Color Fidelity | Warm/Cool | Line Weight | Grade |
|------|-----------|-----------|-------------|----------------|-----------|-------------|-------|
| LTG_COLOR_styleframe_discovery.png | style_frame | distinct | PASS | PASS | WARN | PASS | **WARN** |
| LTG_COLOR_styleframe_glitch_storm.png | style_frame | distinct | PASS | PASS | WARN | PASS | **WARN** |
| LTG_COLOR_styleframe_otherside.png | style_frame | distinct | PASS | WARN | WARN | PASS | **WARN** |
| LTG_COLOR_styleframe_luma_byte.png | style_frame | ambiguous | WARN | WARN | WARN | PASS | **WARN** |
| LTG_CHAR_luma_expressions.png | character_sheet | distinct | PASS | WARN | SKIP | PASS | **WARN** |
| LTG_CHAR_luma_turnaround.png | character_sheet | distinct | PASS | WARN | SKIP | PASS | **WARN** |
| LTG_COLOR_luma_color_model.png | color_model | distinct | PASS | WARN | SKIP | PASS | **WARN** |
| LTG_CHAR_byte_expression_sheet.png | character_sheet | distinct | PASS | PASS | SKIP | PASS | PASS |
| LTG_CHAR_cosmo_expression_sheet.png | character_sheet | distinct | PASS | PASS | SKIP | PASS | PASS |
| LTG_CHAR_grandma_miri_expression_sheet.png | character_sheet | distinct | PASS | WARN | SKIP | PASS | **WARN** |
| LTG_CHAR_glitch_expression_sheet.png | character_sheet | distinct | PASS | PASS | SKIP | PASS | PASS |
| LTG_CHAR_luma_lineup.png | character_sheet | distinct | PASS | WARN | SKIP | PASS | **WARN** |

**Results:** 3 PASS / 9 WARN / 0 FAIL

---

## Detailed Results

### LTG_COLOR_styleframe_discovery.png
*Asset type: style_frame*

**Overall Grade:** WARN

**WARN conditions:**
- warm_cool: insufficient separation

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=14, max=241, range=227

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: target=32.9° found=32.9° delta=0.0° [PASS]
  - BYTE_TEAL: target=185.2° found=183.1° delta=2.1° [PASS]
  - UV_PURPLE: not_found
  - HOT_MAGENTA: target=342.3° found=342.3° delta=0.0° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=183.1° delta=0.4° [PASS]
  - SUNLIT_AMBER: not_found

**D. Warm/Cool Separation:** WARN — zone_a=129.7, zone_b=129.7, separation=0.0
  - Flat palette — warm/cool separation is 0.0 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=449.65px, std=625.14px, outliers=0

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

**D. Warm/Cool Separation:** WARN — zone_a=184.66, zone_b=187.71, separation=3.05
  - Flat palette — warm/cool separation is 3.1 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=171.75px, std=383.97px, outliers=2

---

### LTG_COLOR_styleframe_luma_byte.png
*Asset type: style_frame*

**Overall Grade:** WARN

**WARN conditions:**
- silhouette=ambiguous
- value_range: compressed or missing extreme
- color_fidelity: hue drift detected
- warm_cool: insufficient separation

**A. Silhouette:** `ambiguous`

**B. Value Range:** WARN — min=12, max=198, range=186
  - No bright highlights — brightest pixel is 198 (threshold ≥ 225)

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: not_found
  - UV_PURPLE: not_found
  - HOT_MAGENTA: not_found
  - ELECTRIC_CYAN: not_found
  - SUNLIT_AMBER: target=34.3° found=46.7° delta=12.4° [FAIL]

**D. Warm/Cool Separation:** WARN — zone_a=131.18, zone_b=131.18, separation=0.0
  - Flat palette — warm/cool separation is 0.0 PIL units (minimum 20.0 required)

**E. Line Weight:** PASS — mean=418.5px, std=544.73px, outliers=0

---

### LTG_CHAR_luma_expressions.png
*Asset type: character_sheet*

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=1, max=255, range=254

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: not_found
  - BYTE_TEAL: target=185.2° found=182.4° delta=2.7° [PASS]
  - UV_PURPLE: not_found
  - HOT_MAGENTA: target=342.3° found=340.8° delta=1.5° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=181.7° delta=1.9° [PASS]
  - SUNLIT_AMBER: target=34.3° found=25.1° delta=9.2° [FAIL]

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** PASS — mean=24.7px, std=83.2px, outliers=1

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
  - BYTE_TEAL: target=185.2° found=178.6° delta=6.6° [FAIL]
  - UV_PURPLE: not_found
  - HOT_MAGENTA: target=342.3° found=344.1° delta=1.8° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=180.2° delta=3.3° [PASS]
  - SUNLIT_AMBER: target=34.3° found=25.1° delta=9.2° [FAIL]

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** PASS — mean=70.9px, std=284.75px, outliers=1

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

**E. Line Weight:** PASS — mean=8.5px, std=9.97px, outliers=2

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

**Overall Grade:** PASS

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=255, range=255

**C. Color Fidelity:** PASS
  - CORRUPT_AMBER: target=32.9° found=33.2° delta=0.3° [PASS]
  - BYTE_TEAL: target=185.2° found=183.8° delta=1.4° [PASS]
  - UV_PURPLE: target=271.9° found=272.0° delta=0.1° [PASS]
  - HOT_MAGENTA: target=342.3° found=342.1° delta=0.2° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=181.2° delta=2.4° [PASS]
  - SUNLIT_AMBER: target=34.3° found=36.3° delta=2.0° [PASS]

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** PASS — mean=78px, std=152.53px, outliers=0

---

### LTG_CHAR_luma_lineup.png
*Asset type: character_sheet*

**Overall Grade:** WARN

**WARN conditions:**
- color_fidelity: hue drift detected

**A. Silhouette:** `distinct`

**B. Value Range:** PASS — min=0, max=255, range=255

**C. Color Fidelity:** WARN
  - CORRUPT_AMBER: target=32.9° found=32.9° delta=0.0° [PASS]
  - BYTE_TEAL: target=185.2° found=185.2° delta=0.0° [PASS]
  - UV_PURPLE: target=271.9° found=271.9° delta=0.0° [PASS]
  - HOT_MAGENTA: target=342.3° found=342.3° delta=0.0° [PASS]
  - ELECTRIC_CYAN: target=183.5° found=185.2° delta=1.6° [PASS]
  - SUNLIT_AMBER: target=34.3° found=25.1° delta=9.2° [FAIL]

**D. Warm/Cool Separation:** SKIPPED — character_sheet — uniform bg by design

**E. Line Weight:** PASS — mean=269.2px, std=519.68px, outliers=0

---
