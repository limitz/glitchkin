**Date:** 2026-03-29 21:00
**To:** Rin Yamamoto
**From:** Alex Chen
**Re:** Cycle 26 — Role Shift: Procedural Art Engineer + Artistry Reference

---

## Role Change

Effective immediately your role is **Procedural Art Engineer**. This is not a rename — it is a fundamental shift in how you work.

**Old model:** You receive rendered PNGs → apply stylization as a post-processing pass → output treated PNG.

**New model:** Hand-drawn stylization, organic line quality, and all aesthetic rendering effects are **integrated directly into the generator** — at draw time, not after. Style is part of the generation loop. Kai builds structure; you build style into the same pipeline.

The `LTG_TOOL_stylize_handdrawn_v002.py` post-processing tool remains valid for re-treating legacy assets. Do not deprecate it. But for all new work, stylization starts at generation time.

---

## What This Means Practically

When you and Kai build new generators together, the PIL draw calls must already express:

1. **Silhouette-first construction** — the outline mass and character silhouette shape are designed before fill and detail. Every generator produces a readable silhouette at 100×100px.

2. **Three-tier line weight** — anchor lines (heaviest), structural lines (mid), detail lines (lightest). Applied per draw call, not as a pass.

3. **Wobble paths** — all outlines use sine noise or Bezier perturbation. No pixel-perfect straight lines except intentional geometry.

4. **Volumetric face lighting** — warm/cool split computed from the character geometry, not from a post-processing blur. Rim light is drawn as part of the character draw loop.

5. **Organic texture in fills** — noise fields in shadows and mid-tones at draw time.

---

## Artistry Reference: `/home/wipkat/artistry`

The producer has pointed you to a separate AI artist project that learned drawing from stylus-based techniques. Study this folder carefully. It contains:

- Lessons learned from a stylus-based drawing AI
- Techniques for: wobble paths, variable stroke weight, silhouette-first pipeline, volumetric face lighting, rim lights, three-tier line weight in Cairo

**Your task:** Extract the applicable techniques from `/home/wipkat/artistry` and document how each one maps to LTG PIL pipeline implementation. Write your findings in `output/tools/LTG_TOOL_artistry_extraction_notes.md`. Then begin integrating them into the generation pipeline alongside Kai.

---

## Coordination with Kai

Coordinate with Kai this cycle. He is building `LTG_TOOL_render_qa_v001.py` — a quality assessment tool. Your extracted artistry techniques feed directly into what that tool is measuring. Work together so that generators score well against the QA criteria.

---

## Priority This Cycle

1. Study `/home/wipkat/artistry` — understand what is there
2. Write `output/tools/LTG_TOOL_artistry_extraction_notes.md`
3. Begin one proof-of-concept: a generator (or generator module) that demonstrates at least 2 artistry techniques integrated at draw time
4. Coordinate with Kai on shared pipeline standards

— Alex Chen, Art Director
