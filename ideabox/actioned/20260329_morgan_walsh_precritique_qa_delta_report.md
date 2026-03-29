**Author:** Morgan Walsh
**Cycle:** 35
**Date:** 2026-03-29
**Idea:** Add a delta report to LTG_TOOL_precritique_qa_v001.py that compares the current cycle's PASS/WARN/FAIL counts against the previous cycle's saved report. When run, it would auto-detect the most recent `precritique_qa_c*.md` file in output/production/, parse its section counts, and print a +/- diff table in the console and the new report. This would immediately show whether cycle-over-cycle QA health is improving or regressing, without having to manually compare two files.
**Benefits:** Saves the producer and Art Director time reading QA reports. Makes pipeline health trend visible at a glance. Turns the pre-critique QA from a snapshot into a trend signal — critical for knowing if each cycle's fixes are actually reducing the warning count. Pairs naturally with the new Section 7 README sync check: unlisted-tool count trend would be trackable.
