**Author:** Jordan Reed
**Cycle:** 43
**Date:** 2026-03-30
**Idea:** Add a `# GLITCH-COLOR-IN-REAL-WORLD` sentinel comment pattern for the rare intentional cases where a GL-palette color is used in a Real World scene. The comment would follow a standard format: `# GLITCH-COLOR-IN-REAL-WORLD: [color name] — intentional, [reason], alpha ≤ [max]`. This creates a grep-able marker that QA tools and reviewers can search for, distinguishing deliberate narrative choices (like SF04's GL-07 lamp halo) from accidental palette bleed. Morgan Walsh could integrate a check into ci_suite that counts these occurrences and emits an INFORMATIONAL line (not a WARN) so they stay visible without triggering false failures.
**Benefits:** Prevents Sam Kowalski from needing to raise P2 flags each cycle for documented intentional choices; gives Morgan Walsh a machine-readable audit trail; helps critics and reviewers understand thematic color decisions without re-reading old briefs.
