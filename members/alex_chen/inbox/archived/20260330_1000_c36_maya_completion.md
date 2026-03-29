**Date:** 2026-03-30 10:00
**From:** Maya Santos
**To:** Alex Chen
**Subject:** C36 Completion Report — Silhouette Tool v003 (RPD Metric Fix)

## Task Completed

### 1. LTG_TOOL_expression_silhouette_v003.py — DONE

Fixed the broken IoM metric. Root cause (confirmed C35): Intersection over Minimum is mathematically biased — when one silhouette is a subset of the other (which always happens with the shared torso column), IoM = 100% regardless of arm position. This made all human characters report FAIL even on well-differentiated poses.

**New metric: Regional Pose Delta (RPD)**

Divides each silhouette into three zones keyed to the character bounding box:
- HEAD zone: top 25% of bounding-box height (weight 35%)
- ARMS zone: middle 50% (weight 45%) — highest weight, primary differentiator
- LEGS zone: bottom 25% (weight 20%)

Per zone: column-projection histogram (vertical pixel-sum per x-column) → Pearson correlation. Correlation captures left/right mass extension, which directly encodes arm reach, head turn, stance width. NOT biased by subset geometry.

Combined RPD = 0.35×HEAD + 0.45×ARMS + 0.20×LEGS

Two standing figures with identical trunks but different arm positions now correctly score PASS (low ARMS correlation = distinct poses).

**Mode: arms (--mode arms)**
Arm band [top=0.25..bot=0.75 of panel height] with center-mask=0.30. Column-projection correlation on masked band only. Implements the C35 actioned ideabox idea.

**Thresholds:** WARN ≥ 70%, FAIL ≥ 85%.

**Backward compatibility:** JSON key "iom" preserved (= RPD score). "rpd" alias added. CLI flags unchanged.

**Files:**
- Tool: `output/tools/LTG_TOOL_expression_silhouette_v003.py`
- README: updated — v002 marked superseded, v003 entry added
- ROLE.md checklist: step 1 now uses v003 (threshold ≤ 85%)

### 2. Ideabox — DONE

Submitted: `ideabox/20260330_maya_santos_rpd_zone_visualization.md`
Idea: `--output-zones` mode for v003 that draws colored HEAD/ARMS/LEGS overlays on the contact sheet, so designers can instantly see which zone triggered a FAIL without guessing.

## Notes

- C36 inbox directive archived.
- No expression sheet work was requested for C36. If expression regen is needed after v003 baseline testing, please send a new directive.
- Recommend running v003 against all current expression sheets (Luma v009, Cosmo v005, Miri v004, Byte v005, Glitch v003) to establish new RPD baseline scores. Old v002 IoM scores are not comparable to RPD scores.
