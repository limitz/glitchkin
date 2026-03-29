# Face Test Gate Policy
## "Luma & the Glitchkin" — Mandatory Pre-Export Check

**Issued:** 2026-03-30
**Authority:** Producer (via C36 directive)
**Documented by:** Lee Tanaka

---

## Problem This Policy Solves

SF02 (Glitch Storm) ran for 3 consecutive cycles (C33–C35) with Luma's face at sprint scale either missing entirely or failing the emotional read. The root cause: no mandatory checkpoint forced face legibility to be verified before asset submission. A generator can silently produce a near-invisible face (eye_r=1px at head_r=23) that passes visual inspection at full scale but fails at thumbnail/screen-viewer scale.

The face test gate closes this gap.

---

## Tool

**`output/tools/LTG_TOOL_character_face_test_v001.py`**

- Renders 6–8 expression variants at sprint scale (head_r configurable, default 23)
- Left sub-panel: actual scale. Right sub-panel: 3× zoom.
- Output ≤ 600×400px
- Supports `--char luma`, `--char cosmo`, `--char miri`
- Returns: PASS / WARN / FAIL

**Key thresholds (empirically confirmed C35):**

| Result | Eye radius condition |
|--------|---------------------|
| PASS   | eye_r ≥ 4px (≥ 0.17 × head_r) |
| WARN   | eye_r 2–3px |
| FAIL   | eye_r ≤ 1px |

---

## Who Must Run This Gate

This gate is mandatory for all team members who produce or modify character-face-containing assets:

| Member | When to run |
|--------|-------------|
| **Maya Santos** | Before exporting any expression sheet or character asset |
| **Rin Yamamoto** | Before exporting any style frame generator output containing character faces at sprint scale |
| **Jordan Reed** | Before exporting any style frame with composited characters at sprint scale |
| **Lee Tanaka** | Before signing off any staging brief that specifies sprint-scale face geometry |

---

## Gate Rules

1. **FAIL = do not submit.** The asset must be fixed before any completion report is filed.
2. **WARN = fix or document.** Either correct the geometry and retest, or include the WARN output verbatim in the completion report with a written explanation of why the WARN is acceptable for this specific asset.
3. **The test output PNG** (saved to `output/production/`) must be referenced in the completion report by filename.
4. **Never override a FAIL with a caption.** A caption reading "face is visible" does not substitute for a passing test.

---

## How to Run

```bash
python output/tools/LTG_TOOL_character_face_test_v001.py --char luma --head-r 23
```

Output saved to: `output/production/LTG_TOOL_face_test_[char]_r[N]_v[###].png`

Register the output filename in your completion report.

---

## Background: Why Sprint Scale Is Hard

At `head_r=23` (the sprint-scale body size in SF02), a face occupies roughly 46×46px of the 1280×720 frame. Eyes at `eye_r=2px` become single-pixel artifacts that disappear under LANCZOS downsampling. Emotional reads require a minimum eye aperture of 4px radius. This is not an aesthetic preference — it is a physical constraint of the rendering pipeline.

The same threshold applies to any character rendered at "background action" scale in a wide or establishing shot.
