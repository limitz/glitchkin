# Master Palette Audit — Cycle 23
**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**Cycle:** 23
**Document under audit:** `output/color/palettes/master_palette.md` (v2.0, last updated Cycle 22)

---

## Audit Scope

Full verification of all canonical color values against production deliverables for the Cycle 23 pitch package. Priorities per task brief:

1. GL-01b Byte Teal (`#00D4E8`) — Byte's body fill
2. GL-07 Corrupted Amber (`#FF8C00`) — figure-ground outline and corruption signal
3. JEANS_BASE — Luma jeans canonical vs. scene-derived values
4. Any undocumented colors in recent style frames or character generators

---

## Section 1 — GL Entry Completeness Check

**Result: COMPLETE AND UNBROKEN.**

All GL entries present and numbered sequentially:

| Entry | Name | Hex | Shadow Companion | Status |
|---|---|---|---|---|
| GL-01 | Electric Cyan | `#00F0FF` | GL-01a `#00A8B4` | LOCKED |
| GL-01a | Deep Cyan | `#00A8B4` | — | LOCKED |
| GL-01b | Byte Teal | `#00D4E8` | GL-01a `#00A8B4` | LOCKED |
| GL-02 | Hot Magenta | `#FF2D6B` | GL-02a `#8C1A3A` | LOCKED |
| GL-02a | Magenta Shadow | `#8C1A3A` | — | LOCKED |
| GL-03 | Acid Green | `#39FF14` | GL-03a `#1AA800` | LOCKED |
| GL-03a | Dark Acid Green | `#1AA800` | — | LOCKED |
| GL-04 | UV Purple | `#7B2FBE` | GL-04a `#3A1060` | LOCKED |
| GL-04a | Deep Digital Void | `#3A1060` | — | LOCKED |
| GL-04b | Atmospheric Depth Purple | `#4A1880` | GL-04a | LOCKED |
| GL-05 | Static White | `#F0F0F0` | GL-05a `#B0B0C0` | LOCKED |
| GL-05a | Light Glitch Grey | `#B0B0C0` | — | LOCKED |
| GL-06 | Data Stream Blue | `#2B7FFF` | GL-06a `#1040A0` | LOCKED |
| GL-06a | Deep Data Blue | `#1040A0` | — | LOCKED |
| GL-06b | Light Data Blue | `#6ABAFF` | — | LOCKED |
| GL-07 | Corrupted Amber | `#FF8C00` | GL-07a `#A84C00` | LOCKED |
| GL-07a | Corrupted Amber Shadow | `#A84C00` | — | LOCKED |
| GL-08 | Void Black | `#0A0A14` | GL-08a `#050508` | LOCKED |
| GL-08a | Below-Void-Black | `#050508` | — | LOCKED |

**No numbered gaps. All shadow companions documented in Section 2 table.**

---

## Section 2 — Priority Value Verification

### GL-01b — Byte Teal

**Master palette:** `#00D4E8` = RGB(0, 212, 232)
**SF03 v003 generator (`LTG_TOOL_style_frame_03_other_side_v003.py`):** `BYTE_BODY = (0, 212, 232)` — line 80
**SF02 v005 generator (`LTG_TOOL_style_frame_02_glitch_storm_v005.py`):** `BYTE_TEAL = (0, 212, 232)` — line 77

**VERIFIED. Canonical value matches all production generators.**

Key enforcement note (from master palette GL-01b section): GL-01b is Byte's body fill ONLY. World screen emission and environment ambient colors use GL-01 (`#00F0FF`). This distinction is enforced in both generators — SF03 uses `ELEC_CYAN = (0, 240, 255)` for circuit traces and ambient, `BYTE_BODY = (0, 212, 232)` for character fill. Correct.

---

### GL-07 — Corrupted Amber

**Master palette:** `#FF8C00` = RGB(255, 140, 0)
**SF02 v005 generator:** `CORRUPT_AMBER = (255, 140, 0)` — confirmed in header comment as "GL-07 canonical #FF8C00 — C22 fix: was (200,122,32)=#C87A20"
**SF03 v003 generator:** `CORRUPT_AMBER = (255, 140, 0)` — line 49

**VERIFIED. Cycle 22 correction to SF02 generator is confirmed in place. The Cycle 22 fix resolved the 4-version error where the generator had `(200, 122, 32) = #C87A20`. Canonical GL-07 `#FF8C00` is now in both generators.**

Cyan-dominant threshold rule: Amber outline applies when Electric Cyan + Byte Teal together exceed 35% of visible background area around Byte. SF02 (storm scene — cyan dominant sky) APPLIES. SF03 (UV Purple dominant, not cyan dominant) DOES NOT APPLY — confirmed per v003 generator (no amber outline call for SF03).

---

### JEANS_BASE — Luma Jeans Canonical vs. Scene-Derived

**Master palette canonical (CHAR-L-05):** `#3A5A8C` = RGB(58, 90, 140)
**SF03 v003 generator:** `JEANS_BASE = (38, 61, 90)` = `#263D5A`

**VERIFIED — RESOLVED (Cycle 22).** `#263D5A` = CHAR-L-05 shadow companion. Under UV Purple ambient, jeans render at their shadow value. This is environment-specific rendering, not a character color change. The master palette CHAR-L-05 entry includes an explicit SF03 UV-ambient use note. **Canonical jeans base `#3A5A8C` is unchanged and correct for all non-Glitch-Layer scenes.**

---

## Section 3 — Outstanding Named Gaps Status

From Palette Status section (Cycle 21 audit):

| Gap | Status in Cycle 23 |
|---|---|
| **Gap 1:** `UV_PURPLE_MID/DARK` in SF03 v003 vs ENV-11/ENV-12 | Carry forward. Jordan Reed to confirm mapping and add inline comment. SF03 generator has `UV_PURPLE_MID = (42,26,64)` — ENV-11 `#2A1A40` = (42,26,64) EXACT MATCH. `UV_PURPLE_DARK = (43,32,80)` — ENV-12 `#2B2050` = (43,32,80) EXACT MATCH. These ARE registered under ENV-11/ENV-12. Jordan should add a cross-reference comment to the script. Low priority. |
| **Gap 2:** `CIRCUIT_TRACE_DIM (0,192,204)` in SF03 v003 | Acceptable construction value with inline comment. No registration needed. Confirmed. |
| **Gap 3:** `JEANS_BASE (38,61,90)` in SF03 v003 | **RESOLVED (Cycle 22).** Documented under CHAR-L-05. |
| **Gap 4:** `LUMA_SHOE (220,215,200)` in SF03 v003 | Low priority construction value. UV-ambient shift of CHAR-L-09. Jordan to add inline comment on next pass. |
| **Gap 5:** `LTG_TOOL_bg_tech_den_v002.py` construction variances | Jordan to add inline comment noting variance from TD-01. Acceptable. |

**No new named gaps identified in Cycle 23.**

---

## Section 4 — New Cycle 23 Generator Check (SF02 v005)

`LTG_TOOL_style_frame_02_glitch_storm_v005.py` was created in Cycle 22. Full inline constant audit:

| Constant | Value | Palette Match | Disposition |
|---|---|---|---|
| WARM_CREAM | (250,240,220) | RW-01 #FAF0DC ✓ | Registered |
| SOFT_GOLD | (232,201,90) | RW-02 #E8C95A ✓ | Registered |
| SUNLIT_AMBER | (212,146,58) | RW-03 #D4923A ✓ | Registered |
| TERRACOTTA | (199,91,57) | RW-04 #C75B39 ✓ | Registered |
| SAGE_GREEN | (122,158,126) | RW-06 #7A9E7E ✓ | Registered |
| DUSTY_LAVENDER | (168,155,191) | RW-08 #A89BBF ✓ | Registered |
| VOID_BLACK | (10,10,20) | GL-08 #0A0A14 ✓ | Registered |
| ELEC_CYAN | (0,240,255) | GL-01 #00F0FF ✓ | Registered |
| ACID_GREEN | (57,255,20) | GL-03 #39FF14 ✓ | Registered |
| DATA_BLUE | (10,79,140) | GL-06 desaturated — #0A4F8C | Construction — commented in script as "dominant storm confetti" |
| UV_PURPLE | (123,47,190) | GL-04 #7B2FBE ✓ | Registered |
| HOT_MAGENTA | (255,45,107) | GL-02 #FF2D6B ✓ | Registered |
| STATIC_WHITE | (240,240,240) | GL-05 #F0F0F0 ✓ | Registered |
| CORRUPT_AMBER | (255,140,0) | GL-07 #FF8C00 ✓ | **VERIFIED CORRECT — C22 fix** |
| NIGHT_SKY_DEEP | (26,20,40) | RW-NS #1A1428 ✓ | Registered |
| DARK_ASPHALT | (42,42,56) | ENV-01 #2A2A38 ✓ | Registered |
| CYAN_ROAD | (42,90,106) | ENV-02 #2A5A6A ✓ | Registered |
| WARM_ROAD | (74,58,42) | ENV-03 #4A3A2A ✓ | Registered |
| COOL_SIDEWALK | (58,56,72) | ENV-04 #3A3848 ✓ | Registered |
| TERRA_CYAN_LIT | (150,172,162) | ENV-06 #96ACA2 ✓ | **Corrected Cycle 13 — G>R, B>R verified** |
| DEEP_WARM_SHAD | (90,56,32) | ENV-07 #5A3820 ✓ | Registered |
| ROOF_EDGE | (26,24,32) | ENV-08 #1A1820 ✓ | Registered |
| DEEP_COCOA | (59,40,32) | RW-11 #3B2820 ✓ | Registered |
| WIN_GLOW_WARM | (200,160,80) | Warm amber construction value | Acceptable — window light glow cone; in the RW-03/RW-02 family, lower saturation. Not canonical enough for a named entry; used only in SF02 glow cone system. |
| DRW_HOODIE_STORM | (200,105,90) | DRW-07 #C8695A ✓ | Registered |
| DRW_SKIN_STORM | (106,180,174) | DRW-08 #6AB4AE ≈ | Close match (DRW-08 = 106,180,174 confirmed) |
| DRW_HOODIE_SHADOW | (58,26,20) | Construction shadow — deep warm | Acceptable inline construction; too specific to register |
| DRW_JACKET_STORM | (128,192,204) | DRW-09 #80C0CC ✓ | Registered |
| DRW_JACKET_SHADOW | (42,26,50) | DRW-10 #2A1A32 ✓ | Registered |
| DRW_HAIR_MAGENTA | (106,42,58) | DRW-17 #6A2A3A ✓ | Registered |
| BYTE_TEAL | (0,212,232) | GL-01b #00D4E8 ✓ | Registered |
| STORM_RIM_CYAN | (0,180,220) | GL-01 desaturated — construction | Acceptable — building rim construction value |
| STORM_RIM_UV | (80,30,120) | GL-04 desaturated — construction | Acceptable — building rim construction value |

**All key canonical values: VERIFIED. Two minor construction values (WIN_GLOW_WARM, STORM_RIM_CYAN, STORM_RIM_UV) are acceptable as unregistered — they are one-use construction derivatives, too specific for the master palette.**

---

## Section 5 — Cyan-Lit Surface Rule Verification

Rule: G > R AND B > R individually.

| Surface | Value | G>R | B>R | Status |
|---|---|---|---|---|
| ENV-06 TERRA_CYAN_LIT | (150,172,162) | G:172 > R:150 ✓ | B:162 > R:150 ✓ | PASSES |
| CYAN_ROAD ENV-02 | (42,90,106) | G:90 > R:42 ✓ | B:106 > R:42 ✓ | PASSES |
| COOL_SIDEWALK ENV-04 | (58,56,72) | G:56 < R:58 ✗ | B:72 > R:58 ✓ | NOTE: sidewalk only needs to read as cool night surface, not actively cyan-lit — near-neutral cool acceptable |
| DRW_SKIN_STORM DRW-08 | (106,180,174) | G:180 > R:106 ✓ | B:174 > R:106 ✓ | PASSES |

All actively cyan-lit surfaces pass the G>R AND B>R test. The sidewalk (COOL_SIDEWALK) is a night surface under mixed light, not a direct cyan-lit surface — its near-neutral cool read is acceptable.

---

## Section 6 — Provisional Entries Status

From Cycle 21 Palette Status section:

| Entry | Status |
|---|---|
| CHAR-L-11 Hoodie Pixel (Warm-Lit) | Still provisional — awaiting OpenToonz render verification |
| DRW-13b Cool Skin Highlight | No new renders; remains derived spec only |
| RW-NSM Moon Ambient | No new renders; spec only |
| TD-10/TD-11 Monitor Screen/Glow | Close-but-not-identical values in bg_tech_den generator still pending alignment pass |
| CHAR-M-04 Miri Permanent Blush | Opacity-feel spec not yet translated to flat alpha render constant |
| CHAR-C-01 Cosmo Skin Base | No rendered SF using this value directly |
| SH-01 through SH-12 School Hallway | No rendered generator — acceptable at this Act 2 stage |

**No provisional entries have changed status in Cycle 23. All are low-priority carry-forwards.**

---

## Section 7 — Palette Status Update — Cycle 23

The Cycle 21 audit established the Palette Status section. Cycle 23 updates:

**New LOCKED entries since Cycle 21:**
- None — no new entries have reached the 2-renderer / 1-critique-cycle threshold in Cycle 23.

**Notable confirmations:**
- GL-07 `#FF8C00` is now in both SF02 v005 and SF03 v003 generators, matching master palette. LOCKED status confirmed.
- GL-01b `#00D4E8` is confirmed in both SF02 v005 and SF03 v003. LOCKED status confirmed.
- ENV-06 `#96ACA2` is confirmed in SF02 v005 (TERRA_CYAN_LIT = 150,172,162). LOCKED status confirmed.
- DRW-07 `#C8695A` is confirmed in SF02 v005 (DRW_HOODIE_STORM = 200,105,90). LOCKED status confirmed.

---

## Summary — Audit Verdict

**PASS. No blocking issues. No undocumented critical values.**

The master palette for Cycle 23 pitch readiness:
- All GL entries complete, unbroken, shadow companions documented
- GL-01b `#00D4E8` and GL-07 `#FF8C00` confirmed in all production generators
- JEANS_BASE scene-derivation is documented and resolved
- Three minor carry-forward notes (ENV-11/ENV-12 comment in SF03, LUMA_SHOE comment, Tech Den WALL_WARM note) — none are blockers
- No new named gaps identified this cycle

*Sam Kowalski — Cycle 23 — 2026-03-29*
