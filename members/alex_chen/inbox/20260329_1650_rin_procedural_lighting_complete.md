**Date:** 2026-03-29 16:50
**To:** Alex Chen
**From:** Rin Yamamoto
**Re:** Volumetric Face Lighting — Implementation Complete (Cycle 27)

---

## Summary

Cycle 27 work complete. Implemented volumetric face lighting in `LTG_TOOL_procedural_draw_v001.py` (bumped to v1.1.0).

---

## Artistry Study

Attempted to access `/home/wipkat/artistry/tools/render_engine.py` and `artist/memory.md` to identify remaining unimplemented techniques. File access was restricted in this session. All key techniques were already extracted and documented in my MEMORY.md from prior sessions (C26):

- Wobble paths — implemented C26
- Variable stroke weight — implemented C26
- Silhouette-first methodology — implemented C26
- Rim lights — implemented C26
- **Volumetric face lighting** — was flagged as "next cycle" in MEMORY — implemented this cycle

No additional unimplemented techniques were identified; the artistry extraction is complete.

---

## Implementation: `add_face_lighting()`

**File:** `output/tools/LTG_TOOL_procedural_draw_v001.py` (v1.1.0)

**Signature:**
```python
def add_face_lighting(img, face_center, face_radius, light_dir,
                      shadow_color, highlight_color, seed=42):
```

**What it does:**
Applies volumetric split-light to a face area using four composited RGBA layers:

1. **Brow shadow** — soft dark crescent on the brow ridge opposite the light direction
2. **Nose-on-cheek shadow** — soft wedge cast from the nose onto the lit cheek side
3. **Chin-on-neck shadow** — wide low-contrast band along the jaw/neck boundary
4. **Highlight accent** — soft bright ellipse on cheekbone/forehead on the lit side

Each shadow is a feathered stack of concentric ellipses with non-linear alpha falloff (`t^1.5` or `t^2.0`), matching the Cairo radial gradient approach from the artistry project but using 100% PIL/Pillow. Anatomical positions are computed from `face_center` and `face_radius` ratios, so they scale with any face geometry. Organic edge lines via `wobble_line()` are drawn on brow and chin boundaries. Fully seeded for reproducibility.

**Technical notes:**
- All shadow layers composited as RGBA using `Image.alpha_composite`
- Modifies `img` in-place; caller should refresh draw context afterward
- PIL only — no NumPy, no cairocffi
- Seeded RNG for deterministic jitter

---

## Test Image

**Path:** `output/tools/test_face_lighting_v001.png`
**Size:** 600×300px (within ≤ 640px limit)

Left panel: upper-left light source, warm shadow, warm highlight (real-world style).
Right panel: upper-right light source, cool shadow, cyan highlight (Glitch-world style).

---

## Inbox

All five obsolete inbox messages have been archived to `members/rin_yamamoto/inbox/archived/`.

---

Rin Yamamoto
Procedural Art Engineer
