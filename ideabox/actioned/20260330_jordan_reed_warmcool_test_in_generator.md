**Author:** Jordan Reed
**Cycle:** 41
**Date:** 2026-03-30
**Idea:** Add a `--check-warmcool` flag to style frame generators that prints inline warm/cool separation diagnostics (top/bottom median hue in PIL units) before saving. SF04 v005 needed 2 iterations to discover the teal wash alpha was insufficient — an inline check would catch this in one run. The pixel_font tool already has a self-test pattern; warm/cool could follow the same model. Could also auto-increase teal wash alpha until separation target is met (same auto-iterate pattern as warmth_inject_hook).
**Benefits:** Saves iteration cycles for any team member adding a new temperature split. Particularly useful for SF01–SF04 reworks where warm/cool is the primary failure mode. Morgan Walsh could integrate into the precritique_qa pipeline as Section 11.
