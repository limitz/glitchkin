**Author:** Morgan Walsh
**Cycle:** 46
**Date:** 2026-03-30
**Idea:** Add a `--auto-seed --dry-run` mode to ci_suite that shows what WOULD be seeded without actually writing to ci_known_issues.json. This would let team members preview auto-seed results before committing, useful for distinguishing real regressions from expected new FAILs during large asset drops. Could also generate a reviewable diff in markdown format for the Producer to approve before seeding.
**Benefits:** Reduces risk of accidentally seeding real bugs as known-issues. Gives the Producer and Art Director visibility into what auto-seed would do before it modifies the baseline. Especially valuable when multiple new assets land in a single cycle.
