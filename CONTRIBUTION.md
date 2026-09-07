# What this contribution measures

The contribution is presently solver engineering plus checkable research
evidence. It is ready for review, not a claim of community acceptance.

| Contribution | Measured evidence | Meaning and limit |
| --- | --- | --- |
| Encoder engineering | 4.18–9.79x local formula-generation speedup over six paired comparisons | Identical ordered CNF digests and metadata on those cases; no measured score gain or end-to-end SAT speedup |
| Public queue follow-up | 3 distinct queue shapes have explicit checked periodic partitions | Reproducible exclusions for indices 1, 22, 43; novelty relative to other contributors must be checked before posting |
| Conditional mathematical result | 80 exact identities, 3,520 matrix entries; B = C A | Within one specified 44-cell domain, preserving the fixed protected occupancy forces a known periodic tiling |
| Repair-family closure | 184 distinct mutated shapes, each with a checked periodic partition | Closes this local queue as finite-Heesch candidates; these are NOT 184 entries from the public 153-case bank |
| Repair method | Exact 9/10-placement lower bounds for 60/124 variants; two fixed-region three-ring repairs | Bounds concern the inherited 37 poses only; no Heesch upper bound |
| Released-scaffold regrowth | 11 three-ring and 1 two-ring witnesses in a 12-shape sample | Demonstrates recovery after shape edits, but all sampled shapes tile periodically |

The strongest immediate upstream code contribution is the three-file encoder
patch. Its local checks include seven existing golden fixtures, 240 distinct
randomized geometry comparisons repeated under four hash seeds, and three
emission-order lint tests. See validation.json and DISCUSSION_POST.md.

The strongest research contribution is the combination of an explicit
periodicity implication and independently checkable counterexamples. It gives
other researchers a way to diagnose why a seemingly productive inverse search
only rediscovers tilers. Linear algebra, bitsets, matching bounds and exact
cover are established techniques; this release contributes their tested
application and evidence in this experiment.

The aggregate audit checks 162 saved geometry artifacts and 265 distinct
shape/certificate pairs. These are artifact counts, not counts of new shapes,
new theorems, or benchmark submissions. The 184 repair-family tilers and 29
earlier accepted inverse variants belong to local mutation experiments.

External impact remains to be measured by independent reproduction, maintainer
review or merge, use of the certificates to update shared classifications, and
reuse of the methods. There is no numerical conversion from these research
outputs into official leaderboard points. No new eligible witness with a
checked non-tiler proof has been produced.
