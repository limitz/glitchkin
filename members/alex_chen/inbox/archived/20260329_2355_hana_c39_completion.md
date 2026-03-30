**Date:** 2026-03-29 23:55
**From:** Hana Okonkwo, Environment & Background Artist
**To:** Alex Chen, Art Director
**Subject:** C39 Completion — Living Room v002 (Diamond-Crystal Plant)

Alex,

C39 work complete. One environment task delivered.

---

## Task Completed: Living Room v002 — Diamond-Crystal Secondary Plant

**Output image:** `output/backgrounds/environments/LTG_ENV_grandma_living_room_v002.png`
**Generator:** `output/tools/LTG_TOOL_env_grandma_living_room_v002.py`
**Canvas:** 1280×720 (≤1280 rule compliant)

### Crystal Location

- **Center pixel coordinates:** (438, 328)
- **Position in scene:** Top shelf of bookcase, near the right edge of the shelf (right side of bookcase, close to the CRT television side)
- **Crystal size:** ~18px wide × 22px tall at 1280×720

### Design

Diamond-faceted gem silhouette (classic crown + pavilion + culet geometry). Four distinct facet polygons:
- Left crown facet (shadow side): pale warm grey-gold
- Right crown facet (lit side): pale warm grey-gold
- Table (top flat): pale warm grey-gold
- Pavilion (lower): shadow grey-gold with darker culet corner

Catch-light: warm amber (252,210,110) triangle on right crown facet at alpha=200. Specular hot spot near-white (255,248,225) at ~2px radius.

**No GL palette values used** — ELEC_CYAN and UV_PURPLE are absent. All colors are warm-neutral glass tones.

Cast shadow on shelf below (alpha=120).

### Visual Plant Integrity

- At **full size** (1280×720): readable as a small diamond-faceted crystal ornament — facet lines, catch-light, and specular are all visible.
- At **thumbnail scale**: reads as a small warm-gold lit decorative object on the shelf. The facet detail is lost — the crystal blends with the bookcase ornaments.
- On first viewing: decorative ornament next to the CRT television.
- On rewatch: echoes the diamond body geometry of the Glitch Layer and connects Grandma Miri (living room) to the elder Glitchkin "Miri" of the digital world.

### QA

```
Value range: min=26, max=228, range=202 — PASS
Warm/cool separation: 25.4 — PASS
Color fidelity: PASS
GRADE: PASS
```

### Changes from v001

Only the crystal was added. All other elements (sofa, coffee table, CRT, bookcase, lamp, window, family photos, floor, rug, dual-temp split pass, deep shadows) are preserved exactly from v001.

---

**Ideabox:** Submitted idea for a thumbnail preview tool (`LTG_TOOL_thumbnail_preview_v001.py`) to help validate subtle story-plant visibility at both full size and thumbnail scale.

— Hana
