**Author:** Ryo Hasegawa
**Cycle:** C44
**Date:** 2026-03-30
**Idea:** Add a motion sheet coverage check to precritique_qa or ci_suite that verifies EVERY named character in the cast has a motion spec sheet. Currently the MOTION_SHEETS list in precritique_qa.py is manually maintained — it would be better if a tool scanned output/characters/main/ for character names (luma, byte, cosmo, miri, glitch) and verified that a corresponding LTG_CHAR_{name}_motion.png exists in output/characters/motion/. This would automatically catch when a new character is added to the cast without a motion spec, and surface the gap before critique.
**Benefits:** Prevents characters slipping through without motion specs (Glitch still has no motion spec — he moves very differently from all others). Removes manual maintenance burden from MOTION_SHEETS list. Catches coverage gaps proactively rather than at critique.
