**Author:** Ryo Hasegawa
**Cycle:** 39
**Date:** 2026-03-29
**Idea:** The motion spec lint tool and expression silhouette tool both use fixed pixel-occupancy thresholds that assume a fixed panel layout (HEADER_H, PAD, etc.). Different sheet authors use different panel offsets. A lightweight "sheet geometry detection" pass — scanning the first 100 rows for the first non-background horizontal band — would let the lint tool auto-detect where panels actually begin, eliminating false WARNs from misaligned zone sampling. One-time calibration pass per sheet family (Luma, Byte, Cosmo), result stored in a small JSON config alongside the lint tool.
**Benefits:** Reduces false WARN noise in Section 8 of precritique QA. Motion lead (me) and QA lead (Morgan Walsh/Kai Nakamura) both benefit. Reduces manual threshold tuning each time a new sheet author joins the team.
