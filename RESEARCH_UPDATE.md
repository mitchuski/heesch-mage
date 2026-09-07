# Latest batch: indices 24–47

An additional 24 inputs received bounded periodic and geometric searches. Three verified two-ring witnesses were recovered. Stronger periodic follow-up excluded 0 of those shapes; 3 remain geometric leads with unresolved tiling status. No non-tiler certificate or score improvement is claimed. In total, 48 of 153 entries have received some follow-up; 105 are untouched. These remain mixed, bounded tests.

Unresolved leads:

```json
[
  {
    "source_index": 24,
    "canonical_digest": "ca232e7fada5ac5237f57c9818196d89742edf66f47de7667731760342b1c880",
    "verified_depth": 2
  },
  {
    "source_index": 34,
    "canonical_digest": "4155c2546d147999ee5e57798f5ebbf16e620d9e6aa757d7567fd295bdbb5f95",
    "verified_depth": 2
  },
  {
    "source_index": 43,
    "canonical_digest": "b47720b325d371f956b7e58eb28dc0c63053f8b3e15b803a9f2dfa3bef51136e",
    "verified_depth": 2
  }
]
```

The earlier two-batch report follows for provenance.

# Latest research before publication

The user asked to prioritize an actual candidate result before publication.
We completed a further bounded pass of source indices 12–23 from the 153-case
queue. This found a second explicit periodic tiling, at index 22. The eleven
other shapes received three-second relaxed depth-two geometric searches:
four exhausted that implementation, seven timed out, and none yielded a new
two-ring witness. No official non-tiler certificates were produced.

Across both batches, 24 source entries have received some follow-up and 129
have not. There are two checked tiling exclusions. The eleven first-batch SAT
UNSAT reports and four second-batch geometric exhaustions remain computational
evidence without official certificates; the seven timeouts remain UNKNOWN.
Do not aggregate these different tests into a claim that 24 cases are closed.

DISCUSSION_POST.md and FOLLOWUP_75.md describe the first twelve-entry batch.
Integrate this update when publishing. No leaderboard improvement or new finite
Heesch number has been found. The result worth contributing now is reproducible
search acceleration plus two explicit exclusions from a shared open queue.

## Second periodic certificate

The 23rd entry (zero-based index 22) has canonical digest
`378a95b263f7cc868db91bce1d22bbfcb1047073086fb2ca63be402939f3228a`.
It is a different canonical shape from the first exclusion. It also partitions
all 80 residues under lattice basis `(8,0),(3,10)` with four 20-cell copies.
The residue partition was independently rechecked, including distinct residues
within each tile and disjointness between tiles.

Use the exact same checking code in FOLLOWUP_75.md, replacing `shape`,
`placements` and the expected canonical digest with these values:

```json
{
  "status": "PERIODIC_TILER",
  "lattices_tested": 265,
  "certificate": {
    "lattice_basis": [
      [
        8,
        0
      ],
      [
        3,
        10
      ]
    ],
    "copies_per_period": 4,
    "placements": [
      [
        2,
        0,
        6
      ],
      [
        5,
        6,
        7
      ],
      [
        9,
        6,
        2
      ],
      [
        6,
        5,
        1
      ]
    ],
    "residue_partition_checked": true
  },
  "source_index": 22,
  "cells": [
    [
      0,
      1
    ],
    [
      0,
      2
    ],
    [
      0,
      3
    ],
    [
      0,
      4
    ],
    [
      1,
      1
    ],
    [
      1,
      2
    ],
    [
      1,
      3
    ],
    [
      1,
      4
    ],
    [
      2,
      0
    ],
    [
      2,
      1
    ],
    [
      2,
      2
    ],
    [
      2,
      3
    ],
    [
      2,
      4
    ],
    [
      2,
      5
    ],
    [
      3,
      1
    ],
    [
      3,
      2
    ],
    [
      3,
      3
    ],
    [
      3,
      4
    ],
    [
      4,
      1
    ],
    [
      4,
      2
    ]
  ],
  "canonical_digest": "378a95b263f7cc868db91bce1d22bbfcb1047073086fb2ca63be402939f3228a"
}
```
