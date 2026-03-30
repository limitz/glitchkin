**Author:** Priya Shah
**Cycle:** 47
**Date:** 2026-03-30
**Idea:** Add a doc staleness check to the CI suite that flags production documents not updated in 10+ cycles. The doc_governance_tracker.md I built this cycle is a manual audit — but Morgan's CI suite could automate this by scanning for cycle markers (e.g., "Cycle NN", "Updated: Cycle NN", "Last Updated: Cycle NN") in all .md files under output/production/ and comparing against the current cycle number. STALE warnings would surface in the precritique QA report, preventing Reinhardt's "23 undocumented decisions" problem from recurring.
**Benefits:** Morgan Walsh (CI suite owner) gets a new automated check. Alex Chen and all team members get early warning on stale docs. Reduces manual audit overhead for story/production roles. Prevents knowledge drift between canonical docs and actual production state.
