**Date:** 2026-03-30 12:00
**From:** Dmitri Volkov, Character Design Critic
**To:** Alex Chen, Art Director
**Re:** Cycle 12 Critique — Items for Art Director

---

Alex,

Cycle 12 delivered. Three multi-cycle items are closed. Grade: B+. Full critique at `output/production/critic_feedback_c12_dmitri.md`. Below are the items that fall on your desk.

---

## ITEM 1: BYTE FLOAT-HEIGHT ANNOTATION — CLOSED BUT NEEDS UPGRADE

The annotation exists. It is functional. It is not production quality.

What was delivered: a dashed line at ground level under Byte's column, labeled "ground floor.", with a small downward-pointing arrow. This communicates that the ground exists. It does not communicate how high Byte floats above it.

What is needed: a **two-headed dimension arrow** spanning the gap between Byte's lower limb tips and the ground-floor line, labeled "float gap: 0.25 HU (canonical)". The current annotation reads as a caption. Production annotation reads as a measurement.

**Action required for Cycle 13:** Update `character_lineup_generator.py` to add a measured float-gap dimension arrow. Thirty minutes. This should not carry to Cycle 14.

---

## ITEM 2: COSMO SIDE-VIEW GLASSES — CLOSED, CONFIRMED CORRECT

The `_draw_cosmo_glasses()` refactor is structurally correct. The consistency guarantee is restored. All four views now use the shared helper.

One maintenance note I am logging here: inside `_draw_cosmo_glasses()`, the `is_side` branch receives `cx=front_x` and `front_x=front_x` — the same value passed as both arguments. This is intentional but undocumented. A future engineer could read this as a redundancy error. Add a two-line comment in the function body explaining that in side-view calls, `cx` is the head front edge (not the character center). No code change required — just a comment.

**This item is closed. The comment is optional but recommended.**

---

## PRIORITY ORDER FOR CYCLE 13 (Art Direction level)

1. **Byte neutral expression panel** — this falls under character design (Maya), but you need to direct it. The Byte expression sheet has no neutral panel while Luma's now has two. This asymmetry in the documentation set is visible to anyone who compares the two sheets. Assign it explicitly.

2. **Byte float annotation upgrade** — as above.

3. **Style Frame 03 (Other Side)** — the SOW lists this as spec approved, background pending. What is the timeline? This has been open-ended for two cycles.

---

Nothing here is a crisis. Everything here is completeness work. The package is pitch-ready. The goal now is production-ready. These items are on that path.

Dmitri Volkov
