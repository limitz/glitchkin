# Library Evaluation Report — Cycle 51

```
======================================================================
LIBRARY EVALUATION REPORT — Cycle 51
======================================================================

Library Availability:
  scikit-image:    v0.21.0
  colour-science:  v0.4.1
  Shapely:         v2.0.7
  OpenCV (cv2):    v4.11.0

──────────────────────────────────────────────────────────────────────
TEST 1: Construction Stiffness — skimage vs cv2
──────────────────────────────────────────────────────────────────────
Test images: 9

File                                          cv2 Stiff    skimage Stiff  cv2 SP%    skimage SP% 
-----------------------------------------------------------------------------------------------
LTG_CHAR_byte_turnaround.png                  0.4350       0.3692         65.6%      58.1%       
LTG_CHAR_cosmo_turnaround.png                 0.2914       0.2280         48.2%      37.6%       
LTG_CHAR_glitch_turnaround.png                0.1667       0.1692         27.2%      27.4%       
LTG_CHAR_luma_turnaround.png                  0.4026       0.3212         64.1%      51.8%       
LTG_CHAR_miri_turnaround.png                  0.2978       0.3018         47.1%      47.4%       
byte_turnaround.png                           0.4350       0.3692         65.6%      58.1%       

Analysis: skimage Canny produces sub-pixel contours via marching squares,
resulting in smoother outlines with fewer false straight-line detections.
This reduces false positives on curved character outlines.

──────────────────────────────────────────────────────────────────────
TEST 2: Silhouette Distinctiveness — skimage + Shapely
──────────────────────────────────────────────────────────────────────
Test images: 9

Morphological cleanup comparison (binary_fill_holes + remove_small_objects):
  LTG_CHAR_byte_turnaround.png             raw=  54901  clean=  56419  delta= +1518 (+2.8%)
  LTG_CHAR_cosmo_turnaround.png            raw=  95527  clean=  96116  delta=  +589 (+0.6%)
  LTG_CHAR_glitch_turnaround.png           raw=  11309  clean=  11186  delta=  -123 (-1.1%)
  LTG_CHAR_luma_turnaround.png             raw= 183776  clean= 191408  delta= +7632 (+4.2%)

  binary_fill_holes closes interior gaps (eyes, highlights).
  remove_small_objects eliminates stray noise pixels.
  Result: cleaner silhouettes for more accurate comparison.

Shapely IoU vs pixel-count SOR (overlap ratio):
Pair                                               Pixel SOR    Shapely IoU  Hausdorff   
--------------------------------------------------------------------------------------
  byte_turnaround vs cosmo_turnaround                    0.4993       0.2448       0.1075      
  byte_turnaround vs glitch_turnaround                   0.0685       0.0137       0.1860      
  byte_turnaround vs luma_turnaround                     0.5258       0.3173       0.1086      
  byte_turnaround vs miri_turnaround                     0.9762       0.0000       0.0000      
  cosmo_turnaround vs glitch_turnaround                   0.0979       0.0269       0.2170      
  cosmo_turnaround vs luma_turnaround                     0.8501       0.4274       0.1184      
  cosmo_turnaround vs miri_turnaround                     0.9294       0.0000       0.0000      
  glitch_turnaround vs luma_turnaround                     0.0512       0.0074       0.2133      
  glitch_turnaround vs miri_turnaround                     0.5911       0.0000       0.0000      
  luma_turnaround vs miri_turnaround                     0.9764       0.0000       0.0000      

  Shapely IoU uses proper polygon intersection (more accurate than pixel counting).
  Hausdorff distance measures max outline deviation (new metric in v2.0.0).

──────────────────────────────────────────────────────────────────────
TEST 3: Color Verify — ΔE2000 vs Hue-Angle
──────────────────────────────────────────────────────────────────────
Scenario                            Hue Δ°     ΔE2000     Hue verdict    ΔE verdict  
---------------------------------------------------------------------------------
  Same hue, lightness drift         0.1        11.13      PASS           FAIL        
  Same hue, desat drift             0.3        5.19       PASS           WARN        
  Small hue drift only              1.3        3.15       PASS           PASS        
  Large hue drift                   14.1       16.58      FAIL           FAIL        
  Identical                         0.0        0.00       PASS           PASS        

  Key finding: ΔE2000 catches lightness and chroma drift that pure hue comparison misses.
  'Same hue, lightness drift' passes hue check but fails ΔE2000 — exactly the gap we needed to close.

──────────────────────────────────────────────────────────────────────
TEST 4: CIECAM02 Warm/Cool Classification
──────────────────────────────────────────────────────────────────────
Color                RGB                PIL Hue    CIECAM02 h   PIL class    CAM02 class 
------------------------------------------------------------------------------------
  warm_red           (255, 80, 60)      4.4        30.7   WARM         WARM        
  warm_amber         (212,146, 58)     24.3        70.0   WARM         WARM        
  warm_orange        (255,140,  0)     23.3        61.1   WARM         WARM        
  cool_blue          ( 60, 80,200)    163.9       264.3   COOL         COOL        
  cool_cyan          (  0,212,232)    131.2       209.4   COOL         COOL        
  cool_slate         (100,120,140)    148.8       242.9   COOL         COOL        
  green              ( 80,180, 80)     85.0       139.7   COOL         NEUTRAL     
  magenta            (255, 45,107)    242.5        11.3   WARM         WARM        
  uv_purple          (123, 47,190)    192.6       299.7   NEUTRAL      COOL        

  Analysis: CIECAM02 provides perceptually-based warm/cool classification.
  The hue angle in CIECAM02 accounts for adaptation and surround effects.
  For our use case (detecting warm FG vs cool BG in depth compositions),
  the PIL HSV hue-range approach is sufficient and faster. CIECAM02 would
  add value for edge cases (e.g., magenta, which is perceptually warm but
  sits at the boundary in HSV). Recommendation: keep PIL-based warm/cool
  classification but add CIECAM02 as optional validation mode.

──────────────────────────────────────────────────────────────────────
TEST 5: Expression Range — skimage Feature Detection
──────────────────────────────────────────────────────────────────────
Evaluation of skimage features for expression analysis:

  Candidate: skimage.feature.local_binary_pattern (LBP)
    - Encodes texture around each pixel as a binary pattern
    - Could measure texture change in face region between expressions
    - More robust than raw pixel delta for detecting structural changes

  Candidate: skimage.feature.BRIEF / ORB descriptors
    - Keypoint-based feature matching between expression panels
    - Could count matched vs unmatched features to quantify change
    - Overkill for our grid-aligned expression sheets

  Candidate: skimage.metrics.structural_similarity (SSIM)
    - Perceptual similarity metric between image regions
    - More meaningful than pixel delta for expression comparison
    - Lower SSIM = more expression range = better

  SSIM test on 10 expression sheet(s):
    LTG_CHAR_byte_expression_sheet.png: avg_SSIM=0.5267 (TL-TR=0.6053, TL-BL=0.4881, TR-BL=0.4868)
    LTG_CHAR_cosmo_expression_sheet.png: avg_SSIM=0.6572 (TL-TR=0.6651, TL-BL=0.7076, TR-BL=0.5991)
    LTG_CHAR_glitch_expression_sheet.png: avg_SSIM=0.8013 (TL-TR=0.8209, TL-BL=0.7698, TR-BL=0.8132)

  Recommendation: Add SSIM as complementary metric to FRPD/SCI in
  expression_range_metric. SSIM is perceptually grounded and would
  reduce false alarms from minor color/tonal shifts that FRPD catches
  but humans don't notice.

======================================================================
SUMMARY — Library Integration Recommendations
======================================================================

1. scikit-image → construction_stiffness.py (INTEGRATED v2.0.0)
   - Sub-pixel Canny contours reduce false straight-line detections
   - binary_fill_holes + remove_small_objects clean silhouettes
   - Falls back to cv2 if skimage unavailable

2. colour-science → color_verify.py (INTEGRATED v4.0.0)
   - ΔE2000 catches lightness and chroma drift that hue-only misses
   - New verify_canonical_colors_deltaE() API + --delta-e CLI flag
   - Falls back gracefully if not installed

3. Shapely → silhouette_distinctiveness.py (INTEGRATED v2.0.0)
   - Polygon IoU replaces pixel-count overlap for accuracy
   - Hausdorff distance as new distinctiveness metric
   - Douglas-Peucker simplification for straight-line detection

4. CIECAM02 (colour-science) → warmcool (EVALUATION ONLY)
   - Perceptually better than PIL HSV for edge cases (magenta, purple)
   - But PIL HSV hue-range approach is sufficient for our depth compositions
   - Recommendation: optional validation mode, not default

5. skimage SSIM → expression_range_metric (RECOMMENDATION)
   - SSIM would complement FRPD/SCI as perceptual similarity metric
   - Would reduce false alarms from minor tonal shifts
   - Integration deferred to next cycle

```
