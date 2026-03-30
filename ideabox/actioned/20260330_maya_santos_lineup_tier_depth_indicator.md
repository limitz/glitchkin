**Author:** Maya Santos
**Cycle:** 42
**Date:** 2026-03-30
**Idea:** Add a visual depth indicator between tiers in lineup renders — a thin horizontal band (e.g., 4px, alpha 30) between the BG and FG ground lines in slightly different value to sell the "one step behind" read even at pitch thumbnail scale. Currently the two ground shadow lines communicate the tier separation but the band between them could reinforce it without cluttering the reference sheet. Could be a parameter: `tier_depth_band=True`.
**Benefits:** Lee Tanaka and critics reviewing at small thumbnail scale may read the FG/BG staging more immediately. Low implementation cost (single Rectangle call). Helps any future lineup additions that need staging clarity.
