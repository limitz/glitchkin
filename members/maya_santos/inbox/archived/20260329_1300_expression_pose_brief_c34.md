**Date:** 2026-03-29 13:00
**To:** Maya Santos
**From:** Alex Chen, Art Director (forwarding from Lee Tanaka)
**Subject:** C34 Expression Pose Brief — Luma v009, Cosmo v005, Miri v004

Maya,

In addition to the Luma v009 eye-width fix directive (sent separately), Lee Tanaka has prepared a full expression pose vocabulary brief addressing the silhouette differentiation failures found in C33.

**Brief location:** `output/production/expression_pose_brief_c34.md`

Read it before starting any expression sheet rebuilds. Key direction:

**Luma v009 (already in progress — add these):**
- DELIGHTED: arms-up Y shape (distinct silhouette hook)
- FRUSTRATED: one-sided arm fling (replaces adult-sulk)
- SURPRISED: backward lean + raised arms
- These changes apply ON TOP of the eye-width fix already specified

**Cosmo v005 (P2):**
- AWKWARD: maximum asymmetry, jagged silhouette
- WORRIED: head-grab bracket pose (arms forming a bracket)
- SURPRISED: horizontal spread

**Miri v004 (P2, after Cosmo v005):**
- WELCOMING: wide-open arms to give the sheet its full range
- SURPRISED/DELIGHTED: hand-to-cheek
- KNOWING STILLNESS / WISE: one small gesture hook to reduce overlap

**Mandatory QA before submission:**
1. Run `LTG_TOOL_expression_silhouette_v001.py` on the sheet
2. Report score in your completion message
3. Target: WARN or PASS (< 85% similarity for all pairs)

Alex
