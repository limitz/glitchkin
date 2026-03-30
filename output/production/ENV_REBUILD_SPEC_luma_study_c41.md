# Rebuild Spec: LTG_ENV_lumashome_study_interior — Cycle 41
**Author:** Hana Okonkwo
**Date:** 2026-03-30
**Cycle:** 40
**Based on:** C16 critique feedback (Chiara: warm/cool 5.4 FAIL, no atmospheric recession), C40 brief

---

## Current State (C40 QA)
```
Silhouette:  distinct
Value range: min=0 max=246 range=246 PASS
Warm/cool:   separation=5.4 FAIL (threshold: 12)
Line weight: mean=77.3px outliers=2 PASS
Grade:       WARN
```
**No generator script exists.** The existing PNG (`LTG_ENV_lumashome_study_interior.png`) is a legacy file (C8, 31 cycles old) with no known source script. Full rebuild from scratch required.

---

## Scene Context

This is **Luma's study/bedroom** — the inciting incident room for Style Frame 01 (SF01). It's where Luma first sees the Glitch signal through the CRT monitor. The room must:

1. Feel inhabited by a curious, creative kid — warm and slightly chaotic
2. Have a CRT monitor as the visual centrepiece and light source
3. Read as REAL WORLD (warm palette, zero Glitch colors)
4. Support SF01's emotional tone: "ordinary evening about to become extraordinary"
5. Contain atmospheric recession (things get hazier/cooler toward back wall)

---

## Architecture Spec

### Canvas
`1280×720px`

### Camera
- 3/4 view from front-right corner, looking toward back-left
- Low camera angle (seated / child perspective)
- VP_X = int(W * 0.18), VP_Y = int(H * 0.38)

### Light Sources
| Source | Color | Position | Role |
|---|---|---|---|
| CRT monitor glow | (180,200,180) blue-green warm | Desk, mid-left | KEY LIGHT — dominant fill in dark room |
| Warm bedside lamp | SUNLIT_AMBER (212,146,58) | Right wall | Fill light, warm-side pull |
| Window (night/eve) | (100,110,140) very cool blue | Back wall | Atmospheric distance marker, cool signal |
| Deep crevice shadows | NEAR_BLACK_WARM (20,12,8) | Floor/wall junctions | Value floor anchor |

### Dual-Temp Split for QA
- TOP half: warm amber ceiling + lamp glow → push with SUNLIT_AMBER overlay alpha 55
- BOTTOM half: cooler floor shadow → CRT spill is blue-green, floor below desk is in deep shadow
- Target: separation ≥ 14 PIL hue units before warmth inject

### Zones
| Zone | Content | Value | Light |
|---|---|---|---|
| Back wall | Bookshelf with books/toys, window (dark/evening) | 30-55 | Window cool, atmospheric haze |
| Left wall | Posters/maps, desk left end | 45-65 | CRT glow |
| Desk surface | CRT monitor (KEY), keyboard, papers, homework | 40-75 | CRT primary |
| Floor area | Worn rug, scattered books/backpack | 25-50 | Shadow, CRT spill |
| Ceiling + upper wall | Warm cream, lamp glow upper right | 65-85 | Lamp warm |
| FG anchor | Near floor corner with object (shoe, bag) | ≤30 | Deep shadow |

### Character Note (Luma — SF01 positioning)
Luma will be composited in front of the CRT. Background in her zone must:
- Be slightly darker than her hoodie (≤230 value vs hoodie fill ~240)
- No magenta/cyan in this room (Real World only)
- The CRT glow creates a natural character backing that frames her

---

## Required Miri-Specific Content
Per C40 brief: "Luma Study Interior v001 (C8, 31 cycles old) — no Miri-specific content."

Grandma Miri connection elements to include:
- **Framed photo** on bookshelf or desk: warm small rectangle with rounded-rect frame
- **Knitted object** (small blanket or toy animal) on desk chair or floor — uses Grandma's warm earth tones
- These are subtle details, not dominant — they're Easter eggs for close readers

---

## Atmospheric Recession
This was explicitly called out as missing. Fix:
- Back wall is ~20% lighter value AND ~15% more desaturated than mid-ground (desk zone)
- Apply a cool-haze overlay on the back 40% of image: (160,165,180, alpha 18) — reads as room depth
- Objects on back shelves are drawn with less detail density (fewer outlines, simpler shapes)

---

## Key Contents
- CRT monitor (70×55px approx): warm-green glow, pixel content optional but hinted
- Desk surface: homework papers (PAPER_WHITE / PAPER_YELLOW), ruler, pencil cup
- Bookshelf (back wall): books (mixed warm/cool spines), a small globe or toy
- Rug: warm terracotta/cream pattern, worn, slightly off-center
- Chair at desk (pulled out, Luma standing)
- Bedding visible right side (DUVET warm blue, pillow cream)

---

## QA Requirements Before Submission
1. `render_qa`: warm/cool ≥ 12, value floor ≤30, value ceiling ≥225 — target PASS or ≤1 WARN item
2. Figure-ground: Luma staging zone (in front of CRT) ≤230 avg value in character zone
3. No Glitch colors: zero pixels in GL palette ranges

---

## Execution Notes for C41
- **New script**: `LTG_TOOL_bg_luma_study.py`
- Import `LTG_TOOL_render_lib`: `gaussian_glow()` for CRT and lamp, `vignette()` final pass
- Use seeded RNG (seed=62)
- Output: `output/backgrounds/environments/LTG_ENV_lumashome_study_interior.png` (overwrite legacy)
- Also update `output/tools/README.md` table with new script entry
