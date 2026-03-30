**Author:** Sam Kowalski
**Cycle:** 41
**Date:** 2026-03-30
**Idea:** Build a threshold composition validator tool. When a character is positioned near a world-boundary (Glitch Layer / Real World threshold), verify that the warm-zone and cool-zone do not accidentally overlap on the character's pixel mass. Input: character PNG + background PNG + threshold x-position. The tool samples the character's bounding box pixels and checks for any warm-toned pixel contamination (R > G+B combined) that should not exist in that world context. This would catch the "warm light on Glitch" class of error programmatically before any style frame is finalized. For Jordan Reed and Rin Yamamoto — any threshold scene now requires this check.
**Benefits:** Prevents the core error in COVETOUS-style frames (warm zone bleeding onto Glitch), which would undermine the entire visual premise. Reusable for any threshold/boundary scene in the show.
