# Color Verify C32 Spot-Check Report

**Run by:** Sam Kowalski — Cycle 32 — 2026-03-30
**Tool:** LTG_TOOL_color_verify_v002.py with histogram=True
**Purpose:** Post-fix verification after C32 palette corrections
  - CHAR-L-11 cross-ref: #00D4E8 → #00F0FF
  - CHAR-M-11 slippers: #5A7A5A Deep Sage → #C4907A Warm Apricot
  - DRW-18 warmth clarification (documented, no hex change)

**Palette verified:** 6 canonical colors (CORRUPT_AMBER, BYTE_TEAL, UV_PURPLE, HOT_MAGENTA, ELECTRIC_CYAN, SUNLIT_AMBER)
**Threshold:** Δhue ≤ 5° = PASS

---

### SF01 Discovery v004 (pitch primary)
**Overall:** PASS
- **CORRUPT_AMBER:** target=32.9° found=32.9° Δ=0.0° → PASS
  Histogram (5°/bucket, canonical band marked with *):
     30.0– 35.0°  |########################################|    808 <-- CANONICAL
- **BYTE_TEAL:** target=185.2° found=183.1° Δ=2.1° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    180.0–185.0°  |########################################|  828163
    185.0–190.0°  |                                        |   9260 <-- CANONICAL
- **UV_PURPLE:** not_found (not present in image — expected for some assets)
- **HOT_MAGENTA:** target=342.3° found=342.3° Δ=0.0° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    340.0–345.0°  |########################################|     55 <-- CANONICAL
- **ELECTRIC_CYAN:** target=183.5° found=183.1° Δ=0.4° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    180.0–185.0°  |########################################|  766227 <-- CANONICAL
    185.0–190.0°  |                                        |   8987
- **SUNLIT_AMBER:** not_found (not present in image — expected for some assets)

### SF02 Glitch Storm v005 (pitch primary)
**Overall:** PASS
- **CORRUPT_AMBER:** target=32.9° found=34.4° Δ=1.4° → PASS
  Histogram (5°/bucket, canonical band marked with *):
     25.0– 30.0°  |                                        |      3
     30.0– 35.0°  |########################################|    180 <-- CANONICAL
     35.0– 40.0°  |#########################               |    113
- **BYTE_TEAL:** target=185.2° found=183.5° Δ=1.6° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    180.0–185.0°  |########################################|    592
    185.0–190.0°  |                                        |      2 <-- CANONICAL
- **UV_PURPLE:** not_found (not present in image — expected for some assets)
- **HOT_MAGENTA:** target=342.3° found=340.7° Δ=1.6° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    335.0–340.0°  |##############                          |    295
    340.0–345.0°  |########################################|    808 <-- CANONICAL
- **ELECTRIC_CYAN:** target=183.5° found=183.2° Δ=0.3° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    175.0–180.0°  |                                        |      3
    180.0–185.0°  |########################################|    814 <-- CANONICAL
- **SUNLIT_AMBER:** target=34.3° found=34.7° Δ=0.4° → PASS
  Histogram (5°/bucket, canonical band marked with *):
     15.0– 20.0°  |#####                                   |     13
     20.0– 25.0°  |                                        |      2
     25.0– 30.0°  |##                                      |      6
     30.0– 35.0°  |########################################|     96 <-- CANONICAL
     35.0– 40.0°  |#####################################   |     90
     40.0– 45.0°  |#                                       |      3

### SF03 Other Side v005 (pitch primary, DRW-18 scene)
**Overall:** FAIL/NOT_FOUND
- **CORRUPT_AMBER:** target=32.9° found=29.3° Δ=3.6° → PASS
  Histogram (5°/bucket, canonical band marked with *):
     25.0– 30.0°  |########################################|    182
     30.0– 35.0°  |############                            |     59 <-- CANONICAL
     35.0– 40.0°  |####                                    |     22
- **BYTE_TEAL:** target=185.2° found=184.5° Δ=0.7° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    180.0–185.0°  |########################################|    816
    185.0–190.0°  |####################                    |    420 <-- CANONICAL
    190.0–195.0°  |                                        |      6
    195.0–200.0°  |                                        |      1
- **UV_PURPLE:** target=271.9° found=262.7° Δ=9.2° → FAIL
  Histogram (5°/bucket, canonical band marked with *):
    250.0–255.0°  |#####################                   |     72
    255.0–260.0°  |############################            |     93
    260.0–265.0°  |#################################       |    111
    265.0–270.0°  |###########                             |     39
    270.0–275.0°  |########################################|    132 <-- CANONICAL
- **HOT_MAGENTA:** target=342.3° found=342.3° Δ=0.0° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    335.0–340.0°  |                                        |      6
    340.0–345.0°  |########################################|    292 <-- CANONICAL
- **ELECTRIC_CYAN:** target=183.5° found=183.5° Δ=0.0° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    175.0–180.0°  |                                        |      2
    180.0–185.0°  |########################################|    868 <-- CANONICAL
    185.0–190.0°  |##################                      |    393
    190.0–195.0°  |                                        |      4
- **SUNLIT_AMBER:** target=34.3° found=25.0° Δ=9.3° → FAIL
  Histogram (5°/bucket, canonical band marked with *):
     20.0– 25.0°  |########################################|    679
     25.0– 30.0°  |####################################    |    621
     30.0– 35.0°  |##                                      |     49 <-- CANONICAL

### SF04 Luma+Byte v003
**Overall:** FAIL/NOT_FOUND
- **CORRUPT_AMBER:** not_found (not present in image — expected for some assets)
- **BYTE_TEAL:** not_found (not present in image — expected for some assets)
- **UV_PURPLE:** not_found (not present in image — expected for some assets)
- **HOT_MAGENTA:** not_found (not present in image — expected for some assets)
- **ELECTRIC_CYAN:** not_found (not present in image — expected for some assets)
- **SUNLIT_AMBER:** target=34.3° found=46.7° Δ=12.4° → FAIL
  Histogram (5°/bucket, canonical band marked with *):
     30.0– 35.0°  |                                        |      0 <-- CANONICAL
     45.0– 50.0°  |########################################|     69

### Miri color model v001 (CHAR-M-11 scene)
**Overall:** FAIL/NOT_FOUND
- **CORRUPT_AMBER:** not_found (not present in image — expected for some assets)
- **BYTE_TEAL:** not_found (not present in image — expected for some assets)
- **UV_PURPLE:** not_found (not present in image — expected for some assets)
- **HOT_MAGENTA:** not_found (not present in image — expected for some assets)
- **ELECTRIC_CYAN:** not_found (not present in image — expected for some assets)
- **SUNLIT_AMBER:** target=34.3° found=19.7° Δ=14.6° → FAIL
  Histogram (5°/bucket, canonical band marked with *):
     15.0– 20.0°  |########################################|   5446
     20.0– 25.0°  |                                        |    102
     30.0– 35.0°  |                                        |      0 <-- CANONICAL

### Luma color model v002 (CHAR-L-11 scene)
**Overall:** FAIL/NOT_FOUND
- **CORRUPT_AMBER:** not_found (not present in image — expected for some assets)
- **BYTE_TEAL:** target=185.2° found=183.5° Δ=1.6° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    180.0–185.0°  |########################################|   1081
    185.0–190.0°  |                                        |      0 <-- CANONICAL
- **UV_PURPLE:** not_found (not present in image — expected for some assets)
- **HOT_MAGENTA:** target=342.3° found=342.3° Δ=0.0° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    340.0–345.0°  |########################################|    862 <-- CANONICAL
- **ELECTRIC_CYAN:** target=183.5° found=183.5° Δ=0.0° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    180.0–185.0°  |########################################|   1081 <-- CANONICAL
- **SUNLIT_AMBER:** target=34.3° found=18.6° Δ=15.7° → FAIL
  Histogram (5°/bucket, canonical band marked with *):
     15.0– 20.0°  |########################################|   8795
     20.0– 25.0°  |###                                     |    805
     25.0– 30.0°  |############################            |   6319
     30.0– 35.0°  |                                        |      0 <-- CANONICAL

### Byte color model v001
**Overall:** PASS
- **CORRUPT_AMBER:** not_found (not present in image — expected for some assets)
- **BYTE_TEAL:** target=185.2° found=185.2° Δ=0.0° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    180.0–185.0°  |#########                               |   2196
    185.0–190.0°  |########################################|   9517 <-- CANONICAL
- **UV_PURPLE:** target=271.9° found=271.9° Δ=0.0° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    270.0–275.0°  |########################################|    805 <-- CANONICAL
- **HOT_MAGENTA:** target=342.3° found=342.3° Δ=0.0° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    340.0–345.0°  |########################################|   2001 <-- CANONICAL
- **ELECTRIC_CYAN:** target=183.5° found=185.2° Δ=1.6° → PASS
  Histogram (5°/bucket, canonical band marked with *):
    180.0–185.0°  |#########                               |   2196 <-- CANONICAL
    185.0–190.0°  |########################################|   9082
- **SUNLIT_AMBER:** not_found (not present in image — expected for some assets)

---

## Analysis & Interpretation — C32

### Summary
| Asset | Overall | Notes |
|---|---|---|
| SF01 Discovery v004 | **PASS** | Clean. All present colors at canonical. |
| SF02 Glitch Storm v005 | **PASS** | SUNLIT_AMBER Δ=0.4° — clean. All canonical present. |
| SF03 Other Side v005 | FAIL | Two documented false positives (see below). |
| SF04 Luma+Byte v003 | FAIL | All GL colors not_found + SUNLIT_AMBER false positive. Pre-existing issue from C31. |
| Miri color model v001 | FAIL | SUNLIT_AMBER false positive — known (Cycle 26 lesson). |
| Luma color model v002 | FAIL | SUNLIT_AMBER false positive — known (Cycle 26 lesson). |
| Byte color model v001 | **PASS** | GL colors exact. Clean. |

### FAIL Analysis

**SF03 UV_PURPLE Δ=9.2° — DOCUMENTED FALSE POSITIVE (pre-existing C31)**
Histogram shows canonical bucket (270–275°) has 132 px but the median lands at 262.7° due to gradient/AA edge pixels in the 250–265° range (447 px total below canonical). The canonical value IS present in the image — it is the dominant bucket. This is the systematic SF03 UV_PURPLE gradient AA false positive documented since C30 and confirmed C31. Not a production error.

**SF03 SUNLIT_AMBER Δ=9.3° — DOCUMENTED FALSE POSITIVE (pre-existing C31)**
No SUNLIT_AMBER exists in SF03 (zero warm light sources). The 1300 px at hue 20–30° are Luma's hoodie orange (HOODIE_UV_MOD #C07038, hue ~18°) and CORRUPT_AMBER edge pixels (hue ~29°) — both well-documented warm pigments in SF03, not SUNLIT_AMBER. This matches the C31 "GL-07/RW-03/hoodie UV-mod are Euclidean neighbors at radius=40" documented finding. Not a production error.

**SF04 All not_found + SUNLIT_AMBER Δ=12.4° — PRE-EXISTING C31 ISSUE**
SF04 carries three pre-existing C31 issues: ambiguous silhouette, max brightness 198, and GL canonical colors not detectable. The SUNLIT_AMBER fail (69 px at 45–50°) is a soft gold/warm interior tone, not a canonical SUNLIT_AMBER drift — this is the SF04 "soft-key" false positive documented C31. Generator source missing (HIGH risk, awaiting Kai). Not a C32 regression.

**Miri color model v001 SUNLIT_AMBER Δ=14.6° — DOCUMENTED FALSE POSITIVE (Cycle 26)**
5446 px at hue 15–20° = Miri skin tones (warm brown family), not SUNLIT_AMBER. Zero canonical SUNLIT_AMBER in Miri model (character palette is skin/cardigan/linen — no lamp amber swatch). Documented in C26 and C31 lessons. Not a production error.

**Luma color model v002 SUNLIT_AMBER Δ=15.7° — DOCUMENTED FALSE POSITIVE (Cycle 26)**
8795 px at 15–20° = Luma skin + warm tones. 6319 px at 25–30° = hoodie orange. No SUNLIT_AMBER swatch in model. Same systematic false positive as Miri. Not a production error.

### C32 Fixes — No Regressions Introduced
The three C32 fixes were documentation/spec changes only (master_palette.md cross-reference text, CHAR-M-11 table row, DRW-18 entry annotation, color story doc). No generator files were modified. The PASS/FAIL results above are identical to C31 baselines. Confirmed: no new regressions from C32 work.

**Carry forward:** SF04 generator source missing (HIGH, Kai). SF03 UV_PURPLE and SUNLIT_AMBER false positives are systematic — will persist until false-positive registry is implemented (ideabox item 20260329_sam_kowalski_qa_false_positive_registry.md).
