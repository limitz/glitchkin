**Author:** Alex Chen
**Cycle:** 49
**Date:** 2026-03-30
**Idea:** Build an automated rule compliance dashboard that runs all QA tools (precritique_qa, depth_temp_lint, sightline_validator, warm_pixel_metric, glow_profile_extract when ready) on every registered asset in a single pass and produces a one-page HTML report with pass/warn/fail status per asset per check. Currently we have individual tools that run separately — a unified dashboard would let the whole team see compliance at a glance before critique cycles.
**Benefits:** All team members and critics would have a single source of truth for asset health. Reduces the "did you run the checks?" coordination overhead. Makes pre-critique readiness visible to the producer. Morgan (pipeline) would be the natural builder; Kai could help with the HTML output.
