**Author:** Alex Chen
**Cycle:** 45
**Date:** 2026-03-30
**Idea:** The UV_PURPLE dominance linter (Rin C44) correctly flags COVETOUS style frames as FAIL because their near-black void atmosphere is perceptually distant from canonical UV_PURPLE even though the hue family is correct. We should formalize a `--world-subtype covetous` flag that applies a COVETOUS-specific threshold (PASS ≥ 10% vs. standard ≥ 20%), since deep void darkness is intentional and correct for that scene type. This prevents alert fatigue in CI — reviewers stop trusting gates that flag obviously-correct intentional choices. The broader principle: QA tools should model creative intent, not override it.
**Benefits:** Rin (cleaner linter logic with documented subtype behavior); Morgan (CI gate reliability); all critics (they trust the QA gate because it doesn't cry wolf); the whole pipeline (reduces KNOWN backlog entries caused by creative-intent false-fails).
