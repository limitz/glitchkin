# Idea: Auto-generate spec lint checks from spec .md files

**Submitted by:** Kai Nakamura
**Date:** 2026-03-29
**Cycle:** 34

## Problem
`LTG_TOOL_char_spec_lint.py` was hand-coded: I manually read luma.md,
cosmo.md, and grandma_miri.md, extracted the key numbers, and wrote individual
check functions for each. This means:
- Adding a new character requires hand-coding new check functions
- If a spec value changes (e.g. Luma eye-width coefficient updates from 0.22 to
  0.23), the linter must be manually updated separately from the spec file
- The linter can silently drift out of sync with the spec without anyone noticing

## Idea
Build `LTG_TOOL_spec_extractor.py` — a tool that parses character spec .md
files and auto-generates check functions for `char_spec_lint`:

1. **Numeric table extraction:** Scan tables in .md files for rows with numeric
   values and a "canonical" column. Example: the proportion table in luma.md
   already has explicit "Canonical Value" column. Extract all rows.

2. **Color table extraction:** Scan .md color tables for Hex column values and
   the constant name they map to.

3. **Constraint generation:** Emit Python check functions for each extracted
   value (ratio check, coefficient check, color check).

4. **Auto-sync check:** Run the extractor and diff against the current
   char_spec_lint checks on every commit. Flag if a spec value has changed
   but the lint check has not been updated.

## Expected benefit
- Adding Byte, Glitch as characters to the spec linter takes minutes, not hours
- Spec changes (e.g. revised eye-width after feedback) automatically propagate
  to the linter on next commit
- Eliminates the "linter drifted from spec" silent-failure mode

## Effort estimate
Medium — ~2 cycles. The main challenge is reliably parsing arbitrary markdown
tables for numeric/hex values.
