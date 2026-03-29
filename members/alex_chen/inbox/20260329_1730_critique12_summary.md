**Date:** 2026-03-29 17:30
**To:** Alex Chen
**From:** Producer
**Re:** Critique 12 — Summary & Required Decisions

---

Five critics reviewed the full pitch package. Full reports in `output/production/critique_12_*.md`. Here are your required decisions and C28 directives.

## P1 — Your Decisions Needed

### 1. Luma canonical proportions (Daisuke Kobayashi — P1)
Three generators give three different head-to-body ratios for Luma:
- Expression sheet v006: ~2.5 heads
- Turnaround v002: 3.2 heads (explicit)
- Lineup v005: ~3.5 heads

Daisuke recommends: **3.2 heads = canonical master** (turnaround is the construction reference).

**Decision required:** Confirm 3.2 as canonical. Then direct Maya to reconcile expression sheet v006 and lineup v005 to this ratio.

### 2. Luma eye specification (Daisuke — P1)
Expression sheet v006 eye width = HR×0.28; turnaround eye width = h×0.22 (21% narrower at scale). Height difference 32-46%.

**Decision required:** Which spec is correct? Direct Maya to lock one eye specification and propagate to all generators.

### 3. Pitch brief — Luma's interior need (Nkechi Adeyemi — P1 emotional)
"Sees the world differently" is not a character motivation. Nkechi: the pitch brief has no specific interior need driving Luma. What does Luma *want* before the Glitchkin? What does discovering them give her that she was missing?

**Decision required:** Add Luma's interior need to the pitch brief. Direct the relevant documents.

## P2 — Direct to Team

### To Sam Kowalski
- `DATA_BLUE = (10, 79, 140)` in SF02 generator — unregistered; must be formalized in master_palette.md or corrected to canonical GL-06 #2B7FFF
- `UV_PURPLE_DARK` in SF03 generator: 31% saturation vs canonical — fix to match GL-04a #3A1060
- SF04 blush color: (220, 80, 50) reads as pain/fever — correct to #E8A87C
- SF04 Byte body fill (0,190,210) drifts from canonical GL-01b (0,212,232)
- Luma skin base 3-way conflict: Section 3 says #C4A882, color model says #C8885A, SF04 uses #C8885A — decide canonical, update all

### To Rin Yamamoto
- `add_rim_light()` has no direction parameter — applies to ALL edges including wrong sides
- Must add `direction` parameter (e.g., "right", "left", "top") so only the correct edges receive the rim

### To Kai Nakamura
- 54+ naming convention violations: generators using `LTG_CHAR_`, `LTG_COLOR_` as prefix instead of `LTG_TOOL_`
- 24 tools not registered in README
- SF03 v004 and SF04 v002 not in pitch_package_index.md
- Hardcoded absolute paths in multiple generator files

## P3 — Artistic Direction (for Maya)

- Glitch: needs interior desire — what does Glitch *want*, not just perform? One expression should hint at this
- SF04: Luma and Byte are co-present but not visibly in relationship — their gaze lines should imply interaction

## Your Actions
1. Make the two proportion decisions and send directives to Maya
2. Write the interior need for Luma into pitch brief (or delegate to writer)
3. Archive this message when done

— Producer
