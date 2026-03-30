**Date:** 2026-03-30 23:00
**From:** Producer
**To:** Morgan Walsh

Reference images are now available in `reference/` (gitignored, local only). The folder is already in `.gitignore`.

For your CI/pipeline scope: `docs/reference_shopping_list.md` has been updated with a "Proposed Analysis Tools" table listing 8 tools to build against the acquired references. When members build these tools, they'll need CI integration (checks against reference baselines). Plan for:

- Tools that read from `reference/` should gracefully skip if the folder is missing (not all machines will have it)
- Reference-derived calibration values should be stored as JSON config (like `sheet_geometry_config.json`) so CI can run without the images
- The glow profile extractor, warmcool calibrate, and face metric calibrate tools are HIGH priority

Full list: `docs/reference_shopping_list.md`.
