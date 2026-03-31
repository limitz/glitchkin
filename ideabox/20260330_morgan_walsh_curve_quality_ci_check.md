**Author:** Morgan Walsh
**Date:** 2026-03-30
**Cycle:** C51

## Idea: Curve Quality CI Check via curvature_at_t()

**Problem:** Character curves are hand-tuned but there's no automated check for kinks, overly sharp bends, or flat spots. Reviewers catch these visually but the checks are subjective and consume critic time.

**Proposal:** Add a new CI check (or precritique_qa section) that samples curvature at regular intervals along every registered character curve. Flag:
- **FAIL:** curvature spike > threshold (kink / corner that should be smooth)
- **WARN:** zero-curvature run > N samples (dead-straight segment in what should be a curve)
- **PASS:** curvature within expected range for the curve type

The `curvature_at_t()` function in `LTG_TOOL_curve_utils.py` already does the math. Integration needs: (1) a registry of character curves to check (control points per expression), (2) per-curve-type thresholds, (3) a runner function in precritique_qa or ci_suite.

**Benefit:** Catches construction quality regressions automatically. Reduces critic load on curve smoothness feedback. Pairs well with Kai's construction_stiffness tool (which checks outlines; this checks the underlying bezier definitions).
