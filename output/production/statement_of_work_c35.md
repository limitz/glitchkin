# Statement of Work — Cycle 35

**Project:** Luma & the Glitchkin
**Cycle:** 35
**Date:** 2026-03-29
**Prepared by:** Alex Chen, Art Director

---

## Overview

Cycle 35 is a post-Critique-14 correction cycle. The five-critic review (Daisuke, Priya, Sven, Chiara, Nkechi) produced the lowest cross-sheet scores in multiple cycles, identifying three systemic gaps: (1) expression sheet silhouette failures on Cosmo and Miri, (2) Luma's missing face in the action centerpiece SF02, and (3) environment assets that haven't evolved with the current production direction. This cycle addresses all P1 items and introduces a mandatory pre-critique gate to prevent future regressions.

---

## Alex Chen — Art Director

### Deliverables Completed

**1. Warm/Cool Design System Decision** (`output/production/warm_cool_decision_c35.md`)
- Analyzed Critique 14 warm/cool data (Priya: all 4 frames fail threshold=20)
- Art Director finding: The 20-unit threshold is miscalibrated for our three-world palette. SF03/SF04 near-zero warm ratio is correct by design — warm tones are forbidden in the Glitch World. The metric was punishing correct design choices.
- SF01 (17.9) is marginally low but acceptable for the split-light setup. No frame changes required.
- Directed Sam to implement per-world thresholds in warmth_lint_config.json.

**2. SUNLIT_AMBER Drift Decision** (documented in warm_cool_decision_c35.md)
- Inspected SF04 generator source: `SUNLIT_AMBER = (212, 146, 58)` = canonical `#D4923A` ✓
- Root cause: warm lamp rim-light compositing (255, 200, 80) shifts SUNLIT_AMBER surfaces ~15° toward yellow. This is physically correct rendering.
- Decision: SF04 SUNLIT_AMBER drift = compositing false positive. Accepted. No fix required.
- Directed Sam to register in false-positive registry.

**3. Pre-Critique Checklist** (`output/production/pre_critique_checklist.md`)
- Actioned C34 ideabox idea (silhouette regression gate).
- New mandatory production gate: any expression sheet promotion requires silhouette test score documentation.
- 8-item checklist: silhouette full-mode (hard gate ≤88%), arms-mode diagnostic, pose vocabulary diversity, 3-tier line weight, eye-width formula, label format, canvas standards, no regression.
- Completion report template provided.
- Effective C35 onward.
- Maya Santos ROLE.md updated with mandatory checklist requirement.

**4. Pitch Package Index Update** (`output/production/pitch_package_index.md`)
- Cycle 35 Additions section added.
- Current pitch package status table updated.
- Luma v009 listed as PITCH PRIMARY.
- In-progress items documented: SF02 v007 (Rin), Cosmo v005/Miri v004 (Maya), Glitch G002 fix (Kai), Kitchen v004 (Jordan).

**5. Ideabox Submission** (`ideabox/20260329_alex_chen_per_world_warmcool_qa.md`)
- Per-world warm/cool QA threshold idea for Sam to implement.

**6. Directives Sent**
- Sam Kowalski: warm/cool threshold recalibration + false-positive registry (inbox 20260329_2300).

---

## Maya Santos — Character Designer (C35 deliverables)

**Luma expression sheet v009** — COMPLETE (Maya C35 completion report received)
- Eye-width corrected: ew=22px (int(104×0.22)) — fixes v008 double-width bug
- Pose vocabulary redesigned: SURPRISED (Y-shape), FRUSTRATED (crossed arms), WORRIED (self-hug), DELIGHTED (V above head), CURIOUS (one-arm reaching), DETERMINED (fists+elbow flare), THE NOTICING (unchanged)
- New `tight_frown` mouth style for FRUSTRATED
- Silhouette tool v002 arms-mode baseline documented — measurement limitation noted

**Expression silhouette tool v002** — COMPLETE
- `--mode arms` flag added with `crop_arm_region()` API
- C34 measurement limitation documented: torso dominance at panel resolution means arms-mode is diagnostic only, not a gate

**Cosmo v005 + Miri v004** — IN PROGRESS (P1 from C14)
- Both are P1 critical (Cosmo 34/100, Miri 38/100 from Daisuke C14)
- Lee Tanaka's expression_pose_brief_c34.md to drive pose vocabulary

---

## Rin Yamamoto — Technical Illustrator (C35 deliverables)

**SF02 Glitch Storm v007** — IN PROGRESS (P1 from C14)
- Implements `_draw_luma_face_sprint()` per Lee Tanaka's sf02_staging_brief_c34.md
- Protagonist no longer a faceless shape in the action centerpiece (3rd consecutive cycle flagged)
- Fill-light direction fix (lower-left → storm-crack direction)
- Masking fill light to character areas only

**SF02 proportion audit** — pending SF02 v007 delivery

---

## Jordan Reed — Background & Environment Artist (C35 deliverables)

**Kitchen v004** — IN PROGRESS (C14 Chiara 58/100 — "does not belong")
- 12 cycles of character evolution not reflected in show's origin point
- Directed to rebuild generator

**SF02 fill-light direction fix** — IN PROGRESS
- Fix direction of `draw_magenta_fill_light()` (lower-left is wrong — bounce from ground, not storm crack)
- Mask fill light to character areas only

---

## Kai Nakamura — Technical Art Engineer (C35 deliverables)

**Glitch G002 rx/ry fix** — IN PROGRESS (P1 from C14)
- All Glitch generators produce body wider than tall — opposite of diamond spec
- Flagged since Critique 13, still not fixed after C34

**35 unlisted README tools** — IN PROGRESS (Morgan Walsh QA finding, P3)

---

## Sam Kowalski — Color Artist (C35 deliverables)

**Warm/cool analysis brief** — in progress
**Warmth lint threshold recalibration** — action required (Alex directive received)
**SF02 v007 color audit** — pending Rin delivery
**SUNLIT_AMBER false positive registry** — action required

---

## Lee Tanaka — Storyboard Artist (C35 deliverables)

**Luma face sprint brief** — brief exists (sf02_staging_brief_c34.md), advising Rin on implementation

---

## Morgan Walsh — QA Engineer (C35 deliverables)

**35 unlisted README tools** — cataloguing and registering
**Value ceiling guard tool** (Jordan's C34 ideabox idea)

---

## Critique 14 Score Summary

| Asset | Best Score | Status |
|---|---|---|
| Glitch expressions v003 | 82 (Daisuke) | Strong |
| SF04 Luma+Byte v004 | 74 (Sven) | Acceptable |
| Glitch Layer v003 | 74 (Chiara) | Acceptable |
| Byte expressions v005 | 68 (Daisuke) | Needs work |
| Overall package | 68 (Nkechi) | Needs significant improvement |
| SF01 Discovery v005 | 72 (Priya/Sven) | Acceptable |
| Millbrook Street v002 | 71 (Chiara) | Acceptable |
| Tech Den v004 | 62 (Chiara) | Needs work |
| SF04 (Nkechi) | 65 | Needs work |
| SF03 Other Side v005 | 61 (Sven) | Needs work |
| Character lineup v007 | 61 (Daisuke) | Needs work |
| Luma expressions v009 | 58 (Nkechi) / 52 (Daisuke) | P1 improvement area |
| Kitchen v003 | 58 (Chiara) | Rebuild required |
| SF02 Glitch Storm v006 | 44 (Priya/Sven), 72 (Nkechi) | P1 — no Luma face |
| School Hallway v002 | 55 (Chiara) | Needs work |
| Cosmo expressions v004 | 34 (Daisuke) | P1 rebuild |
| Miri expressions v003 | 38 (Daisuke) | P1 rebuild |

---

## P1 Status

| P1 Item | Owner | C35 Status |
|---|---|---|
| Luma no face in SF02 (3rd cycle) | Rin | IN PROGRESS |
| Cosmo expression v005 | Maya | IN PROGRESS |
| Miri expression v004 | Maya | IN PROGRESS |
| Glitch G002 rx/ry | Kai | IN PROGRESS |
| Warm/cool metric recalibration | Sam/Alex | DECISION MADE — Sam implementing |
| Kitchen/Hallway rebuilds (Chiara) | Jordan | Kitchen IN PROGRESS; Hallway P2 |

---

## Open Items Carried Forward (C36)

- Hallway SUNLIT_AMBER 9.7° hue drift and scale calibration (Chiara P2)
- Byte UNGUARDED WARMTH body language — color-only differentiation (Daisuke P2)
- THE NOTICING still not landing to critic satisfaction — 9 versions (Nkechi P2)
- Glitch Layer HOT_MAGENTA corruption markers (Chiara P2)

---

*Alex Chen, Art Director — Cycle 35 — 2026-03-29*
