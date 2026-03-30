**Date:** 2026-03-29 22:48
**From:** Producer
**To:** Maya Santos, Character Designer
**Subject:** C39 — Character QA Tools

Maya,

Cycle 39. Three tool tasks from your C38 ideabox proposals (all actioned), plus one unattributed ideabox idea assigned to you.

## Task 1 — Hero Expression Isolator (noticing_panel_context_tool idea) — P1

Build `LTG_TOOL_expression_isolator_v001.py`:
- Renders a single named expression from any character expression sheet at 2x panel size (800×800px)
- Input: character name + expression name (e.g., `--char luma --expr THE_NOTICING`)
- Output: standalone PNG of just that expression, large format, for critic review and pitch materials
- Review `ideabox/actioned/20260330_maya_santos_noticing_panel_context_tool.md` for full spec
- Test: isolate THE NOTICING (DOUBT VARIANT) from Luma expr v011

## Task 2 — RPD Zone Visualization (rpd_zone_visualization idea)

Build a visual debugging overlay for RPD (Reduced Panel Difference) analysis:
- Shows which pixels drove the RPD score between two expression panels
- Helps distinguish design issues from scale/resolution issues in critique feedback
- Review `ideabox/actioned/20260330_maya_santos_rpd_zone_visualization.md` for the spec
- Integrate as a flag into `LTG_TOOL_expression_silhouette_v003.py` (e.g., `--viz-rpd`)

## Task 3 — Body-Part Color-Index Hierarchy Tool (unattributed ideabox idea)

Build `LTG_TOOL_bodypart_hierarchy_v001.py`:
- Assign a color-index ID to each character body part (eye, hair, skin, outline, etc.) in a character sprite
- For each horizontal and vertical scan line, list the color-index transitions
- Detect violations: e.g., eye pixel appearing inside/under hair polygon = hierarchy violation
- Use this to catch "eye inside hair" rendering issues in Luma expressions
- Output: PASS/WARN/FAIL with pixel coordinates of any violations
- Reference: `ideabox/actioned/my_idea_1.md`

## Delivery
- New tools in `output/tools/`
- Run expression isolator on Luma expr v011 and Byte expr v006 as smoke tests
- Submit 1 ideabox idea to `/home/wipkat/team/ideabox/`

Start by reading your ROLE.md, then output/tools/README.md, then all inbox messages.

— Producer
