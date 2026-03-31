**Date:** 2026-03-31 18:54
**From:** Producer
**To:** Maya Santos
**Re:** Nose looks stuck on — needs to connect to face

Human feedback:

> "nose needs to connect to the face. now there is outline, looks like it is sticked on"

The nose is drawn with a full outline stroke, making it look like a separate shape pasted onto the face rather than part of it.

**Fix:** The nose should read as growing out of the face surface, not sitting on top of it.

- **Remove the outline stroke** on the parts of the nose that connect to the face. Only the outer/free edge of the nose gets a line — the base where it meets the face skin should have no stroke, just the filled skin color blending into the face.
- For the profile nose (side views): the bump protrudes from the face silhouette. The line at the tip/bridge is fine, but where the nose base meets the cheek/face surface — no outline there.
- For the front nose arc + nostril dots: the nostril area can have a subtle line, but there should be no box or full-perimeter stroke around the whole nose shape.
- Technique: draw nose fill first (matching face skin tone or slightly warmer), then stroke only the outer contour segments — not the segment that lies against the face. Use `ctx.new_path()` carefully to stroke only the free edges.

Apply to all views where the nose is visible. Queue for next available cycle.
