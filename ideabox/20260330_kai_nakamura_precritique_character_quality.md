**Author:** Kai Nakamura
**Cycle:** 50
**Date:** 2026-03-30
**Idea:** Integrate the three new character quality tools (silhouette_distinctiveness, expression_range_metric, construction_stiffness) into LTG_TOOL_precritique_qa.py as new sections (14, 15, 16). This would make character quality metrics part of every automated QA pass, so regressions or persistent issues get flagged before critics ever see the work. Currently these run standalone — baking them into precritique gives automatic coverage on every asset update.
**Benefits:** All team members generating character assets get instant feedback on silhouette overlap, expression sameness, and construction stiffness. Catches the exact problems critics have been flagging (Cosmo/Miri identical silhouettes, stiff construction) at the tool level instead of waiting for human critique cycles.
