**Author:** Hana Okonkwo
**Cycle:** 47
**Date:** 2026-03-30
**Idea:** Create a per-room furniture VP specification document that maps each piece of furniture in Real World interiors to its expected vanishing point alignment. Chiara flagged "systemic perspective: furniture in flat elevation" across all interiors, but fixing this properly requires knowing which VP each object should converge toward (some rooms have multiple VPs for different wall planes). A spec document per room would let us batch-fix furniture across all generators in one dedicated cycle instead of ad hoc fixes that may conflict.
**Benefits:** Helps all environment generators (Kitchen, Living Room, Classroom, Tech Den, Luma Study) achieve consistent furniture perspective. Would also serve as QA reference for VP detect tool to validate per-object alignment rather than whole-image VP.
