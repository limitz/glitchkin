**Author:** Lee Tanaka
**Cycle:** 50
**Date:** 2026-03-30
**Idea:** Build `LTG_TOOL_gesture_line_lint.py` — an automated gesture line straightness detector. Given an expression sheet PNG, it extracts each panel's character silhouette, computes the centroid at head, torso, hip, and foot level, and measures the deviation of these centroids from a straight vertical line. A straight line (deviation < 3px) = FAIL. A curved line (deviation > 8px) = PASS. This would catch the "all poses have identical vertical gesture lines" problem automatically before any critic sees the sheet.
**Benefits:** Maya, Rin, and Diego would get instant feedback on whether a rebuilt pose actually has a gesture line or has regressed to the centered-rectangle default. Integrates into precritique_qa as a new section. Prevents the stiffness problem from recurring after the C50 fix.
