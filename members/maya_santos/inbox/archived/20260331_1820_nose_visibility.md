**Date:** 2026-03-31 18:20
**From:** Producer
**To:** Maya Santos
**Re:** Nose not visible on face

Human feedback:

> "face doesn't show nose"

The nose is not reading clearly. Check all views in the turnaround:

- **Front view:** Currently drawn as a dot. A dot is too subtle — needs to be a small but readable nose shape. Even in cartoon front-face, a nose is usually a small upturned shape, two nostril dots, or a short curved line. Make it visible without overdoing it.
- **Side view:** The bezier nose bump must clearly protrude beyond the face silhouette. If it's currently drawn but clipping or too small, increase the protrusion distance and make it readable as a nose shape.
- **3/4 view:** Nose should be visible on the near side as a readable bump or shape — not just a hint.
- **Back view:** No nose (expected — leave as-is).

This is likely a size/protrusion issue — the nose features exist in code but aren't drawn large enough to be legible at turnaround scale. Increase nose prominence until it reads clearly as a nose from normal viewing distance.

Regenerate turnaround, send completion to Producer inbox.
