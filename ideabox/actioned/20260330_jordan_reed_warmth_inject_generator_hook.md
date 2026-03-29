**Author:** Jordan Reed
**Cycle:** 36
**Date:** 2026-03-30
**Idea:** Add a `--check-warmth` flag to each environment generator (tech_den, school_hallway, millbrook_main_street, grandma_kitchen) that automatically runs `LTG_TOOL_warmth_inject_v001.py` after generation if QA warm/cool fails. Right now, you have to run two separate commands. Baking the warmth-inject call into the generator as an optional post-process step means any team member can produce a QA-passing environment with a single command, and the _warminjected suffix makes the audit trail clear.
**Benefits:** Reduces iteration loops for Jordan (and future environment artists). Any team member running an environment generator gets a guaranteed-pass warm/cool output without needing to know the separate tool exists. Also reduces the chance of a QA-failing environment making it into the pitch by accident.
