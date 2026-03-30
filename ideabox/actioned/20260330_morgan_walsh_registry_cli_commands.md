**Author:** Morgan Walsh
**Cycle:** C49
**Date:** 2026-03-30
**Idea:** Add CLI subcommands to the CI suite for managing the check registry: `--registry-list` to show current slot assignments, `--registry-swap SLOT CHECK` to swap a check into a slot and auto-record in swap_history, `--registry-disable SLOT` to disable a slot. This would let any team member modify the CI pipeline via command line without manually editing JSON.
**Benefits:** Reduces friction for check management. Currently, swapping a check requires knowing the JSON schema. CLI commands would validate inputs (e.g., reject unknown check names, prevent duplicate slot assignments) and auto-timestamp swap_history entries. Helps Alex and Kai manage the pipeline without needing Morgan's involvement for routine slot changes.
