**Author:** Morgan Walsh
**Cycle:** 42
**Date:** 2026-03-30
**Idea:** Add an automated close-or-confirm prompt to the stale known-issue workflow. When `--warn-stale N` fires on a CI run, generate a short review stub file (e.g. `ci_stale_review_C42.md`) listing each stale entry with a YES/NO/EXTEND field. A team member fills it in; the CI suite can then auto-remove confirmed-closed entries from `ci_known_issues.json` on the next run (with a `--apply-stale-review PATH` flag). This removes the manual step of editing JSON by hand and ensures stale suppressions are actually triaged rather than just warned about and forgotten.
**Benefits:** Reduces the friction of clearing aged suppressions. Prevents the known-issues list from silently inflating over many cycles. Kai or any pipeline-aware member could use the review file to confirm FPs are still genuine without having to parse the raw JSON.
