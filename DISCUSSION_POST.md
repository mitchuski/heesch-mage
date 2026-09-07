# Preserve CNF output while accelerating the multilevel contact graph

Large multilevel encodings spend substantial time constructing tile-contact pairs
that are later discarded because the placements overlap. This patch filters them
using cell-incidence bitsets before materializing pairs. In six paired local
formula-generation measurements, elapsed time improved by 4.18–9.79x while the
ordered clause digests, variable counts and clause-family counts stayed identical.

This is a proposed encoder performance contribution. It does not change the
benchmark score, establish a new Heesch number, or demonstrate faster SAT solving.

## Change and correctness argument

For each occupied cell c, build an integer bitset I(c) containing the indices of
placements that occupy c. For placement A, union I(c) over its cells to obtain
overlapping placements, and union I(n) over neighboring cells to obtain contacts.
Subtract the overlap bitset from the contact bitset. Retain indices j greater
than A's index i and extract set bits in ascending order.

On valid grid cells, the contact relation is symmetric. Consequently this produces
exactly the disjoint touching pairs (i,j), once each, in the original sorted order.
Intermediate unions are independent of cell iteration order. The existing
emission-order pragma count is preserved, with the changed site explained.

The three-file patch changes one production function and adds a geometric-oracle
test plus fixture data drawn from the existing multilevel determinism suite.
It adds no runtime dependency. The patch was built against upstream commit
`ce3b8d6974d3f318c3c6081b421ed51c7d041d6e`; `git apply --check` passed against that
local checkout. The GitHub API independently reported that same master HEAD on 7 September 2026.

## Validation completed

- Seven committed upstream full-CNF and universe digest fixtures pass.
- 240 randomized direct geometric comparisons cover square, hex and triangle
  grids, point and edge contacts, empty sets and duplicate placements.
- Those checks pass in four fresh Python processes with hash seeds 0, 1, 42 and
  260907. These are repeated checks, not 960 distinct random instances.
- All three existing emission-order lint checks pass, including pinned pragmas.
- Five known-record hex shapes at depth two and the 11-cell control at depth
  three have identical ordered-clause SHA-256 values and formula metadata under
  the original and experimental graph implementations. Depth three exercises
  the additional separation constraints absent at depth two.

## Local performance evidence

Windows, CPython 3.14, sequential original/replacement runs, one sample each.
The measured full-generation path includes clause hashing. These timings are
preliminary; they are not medians or results from the official Linux runner.

| Shape | Depth | Original seconds | Bitsets seconds | Ratio |
|---|---:|---:|---:|---:|
| 11-hex | 2 | 5.711 | 1.049 | 5.45x |
| 13-hex | 2 | 9.892 | 1.461 | 6.77x |
| 15-hex a | 2 | 12.081 | 1.612 | 7.50x |
| 16-hex | 2 | 22.722 | 2.472 | 9.19x |
| 15-hex b | 2 | 25.334 | 2.589 | 9.79x |
| 11-hex | 3 | 61.225 | 14.637 | 4.18x |

The 15-hex b depth-three replacement also completed encoding 1,218,929 clauses
and 325,147 variables in 42.158s. This is an unmatched measurement and is excluded
from the ratios above.

The bitset method avoids storing overlapping candidate pairs, but peak memory
was not measured. Cell-incidence bitsets and the final edge list still consume
memory; scaling at proof depths six and seven needs measurement.

## Suggested maintainer review

First run the full existing encoder determinism, revision-freeze, round-trip and
proof-pipeline suites on a supported Linux runner. Measure repeated elapsed time
and peak RSS at representative larger depths before choosing default adoption.
Native Glucose4 now recovers verified third-ring witnesses on all five local known-Hc4
controls. The final 15-b control takes 27.375s including encoding, solving and
witness checking. This does not replace the official dual-checker proof pipeline,
which has not been rerun for this patch.

To inspect the proposal in a clean checkout:

```sh
git apply --check touch-graph-bitsets.patch
git apply touch-graph-bitsets.patch
python -m unittest discover -s tests/encoder -p test_touch_bitsets.py -v
```

The source benchmark restricts participant submissions to `submission/` and
checks regenerated CNF hashes. This proposal therefore belongs in a maintainer
PR or a research Discussion, not a leaderboard submission. The repository has
an active [research Discussion area](https://github.com/Layr-Labs/heesch/discussions).
The [benchmark contract](https://github.com/Layr-Labs/heesch#the-benchmark-precisely)
explains why preserving exact formula output matters.

## Connection to an open research queue

Discussion #75 provides a useful target for independent follow-up rather than
regenerating an already explored mutation bank. Credit nasqret for the published
inputs and calibration audit, Frodan for the overlay construction and earlier
pipeline work, and Kaplan for the parent shapes and native solver.

We checked all 153 published shape identities and native-input hashes, then tested
the first twelve entries in source order. Eleven returned UNSAT from the
experimental depth-two formula; these are preliminary solver results without
official proof certificates. One yielded a strictly verified two-ring witness,
then a checked four-copy periodic tiling certificate. That positive tiling
certificate is a useful exclusion; the other eleven should not be labelled
officially closed from these solver outputs alone. No leaderboard improvement
or new finite Heesch number is claimed.

The bitset technique is standard. The contribution proposed here is a tested
implementation improvement to this encoder, plus a reproducible follow-up of an
open shared queue. Prepared with Codex. Upstream authorship and fixture provenance
are preserved in the patch.

Would maintainers prefer this as a small performance PR? The next validation I
would find most useful is repeated elapsed-time and peak-RSS measurement on the
Linux runner at deeper levels, together with the complete existing CI suite.

<details><summary>Complete three-file patch</summary>

```diff
--- a/heesch_encoder/multilevel/universe.py
+++ b/heesch_encoder/multilevel/universe.py
@@ -149,27 +149,27 @@
 
 
 def touching_cellset_pairs(cellsets: list, contact: Contact) -> list[tuple[int, int]]:
-    """Index pairs (i, j), i < j, of disjoint touching cell sets — the
-    geometric touch graph shared by feasibility counting and clause emission
-    (families 4/5/6) so the two can never drift. Deterministic: input order
-    defines indices; output sorted."""
-    cell_index: dict = {}
-    for i, cs in enumerate(cellsets):
-        for c in cs:
-            cell_index.setdefault(c, []).append(i)
-    pairs: set = set()  # membership/dedup only
-    for i, cs in enumerate(cellsets):
-        for c in cs:
-            for n in contact.neighbors(c):
-                for j in cell_index.get(n, ()):
-                    if j == i:
-                        continue
-                    a, b = (i, j) if i < j else (j, i)
-                    pairs.add((a, b))
-    # Touching requires disjointness; overlapping sets sharing a neighbor
-    # relation are filtered here.
-    out = [
-        (a, b) for (a, b) in sorted(pairs)  # ordered-ok: sorted
-        if not (cellsets[a] & cellsets[b])
-    ]
-    return out
+    """Sorted pairs of disjoint touching sets on valid grid cells.
+
+    Cell incidence bitsets filter overlap before pair materialization.
+    Neighbor contact is symmetric on valid cells; j > i emits each edge once.
+    Bitwise unions are independent of cell iteration order.
+    """
+    index = {}
+    for i, cells in enumerate(cellsets):
+        bit = 1 << i
+        for cell in cells:
+            index[cell] = index.get(cell, 0) | bit
+    out = []
+    for i, cells in enumerate(cellsets):
+        overlaps = neighbors = 0
+        for cell in cells:
+            overlaps |= index[cell]
+            for other in contact.neighbors(cell):
+                neighbors |= index.get(other, 0)
+        candidates = neighbors & ~overlaps & ~((1 << (i + 1)) - 1)
+        while candidates:
+            bit = candidates & -candidates
+            out.append((i, bit.bit_length() - 1))
+            candidates ^= bit
+    return out  # ordered-ok: ascending i and ascending set-bit j
--- /dev/null
+++ b/tests/encoder/test_touch_bitsets.py
@@ -0,0 +1,49 @@
+"""Contact-graph regression tests: geometric oracle and existing CNF goldens."""
+import hashlib
+import json
+import pathlib
+import random
+import unittest
+
+from heesch_encoder.multilevel.api import encode_multilevel
+from heesch_encoder.multilevel.universe import multilevel_universe, touching_cellset_pairs
+from heesch_verify.grids import GRIDS
+
+
+class TouchGraphTests(unittest.TestCase):
+    def test_geometric_oracle(self):
+        rng = random.Random(260907)
+        for grid in GRIDS.values():
+            valid = [(x, y) for x in range(-6, 7) for y in range(-6, 7)
+                     if grid.cell_valid((x, y))]
+            for mode in ('point', 'edge'):
+                contact = grid.contact(mode)
+                for _ in range(40):
+                    sets = [frozenset(rng.choice(valid) for _ in range(rng.randrange(0, 8)))
+                            for _ in range(20)]
+                    sets.extend(sets[:3])  # Duplicate geometric placements.
+                    expected = []
+                    for i, a in enumerate(sets):
+                        for j in range(i + 1, len(sets)):
+                            b = sets[j]
+                            if a.isdisjoint(b) and any(n in b for c in a for n in contact.neighbors(c)):
+                                expected.append((i, j))
+                    self.assertEqual(touching_cellset_pairs(sets, contact), expected)
+
+    def test_committed_multilevel_goldens(self):
+        here = pathlib.Path(__file__).parent
+        fixtures = json.loads((here / 'touch_fixtures.json').read_text())
+        goldens = json.loads((here / 'golden/ml_digests.json').read_text())
+        for name, gid, cells, depth in fixtures:
+            with self.subTest(name=name):
+                grid = GRIDS[gid]; contact = grid.contact('point')
+                tile = frozenset(map(tuple, cells))
+                uni = multilevel_universe(tile, grid, contact, depth)
+                serialized = '\n'.join(f'{level} {p.symmetry_index} {p.ty} {p.tx}'
+                    for level, placements in enumerate(uni.levels, 1) for p in placements)
+                enc = encode_multilevel(tile, grid, contact, depth)
+                self.assertEqual([hashlib.sha256(serialized.encode()).hexdigest(), enc.digest], goldens[name])
+
+
+if __name__ == '__main__':
+    unittest.main()
--- /dev/null
+++ b/tests/encoder/touch_fixtures.json
@@ -0,0 +1,159 @@
+[
+  [
+    "mono-m2",
+    "O",
+    [
+      [
+        0,
+        0
+      ]
+    ],
+    2
+  ],
+  [
+    "domino-m2",
+    "O",
+    [
+      [
+        0,
+        0
+      ],
+      [
+        1,
+        0
+      ]
+    ],
+    2
+  ],
+  [
+    "T-m2",
+    "O",
+    [
+      [
+        0,
+        0
+      ],
+      [
+        1,
+        0
+      ],
+      [
+        2,
+        0
+      ],
+      [
+        1,
+        1
+      ]
+    ],
+    2
+  ],
+  [
+    "slotblock-m1",
+    "O",
+    [
+      [
+        0,
+        0
+      ],
+      [
+        0,
+        1
+      ],
+      [
+        0,
+        2
+      ],
+      [
+        1,
+        0
+      ],
+      [
+        1,
+        1
+      ],
+      [
+        1,
+        2
+      ],
+      [
+        2,
+        0
+      ],
+      [
+        3,
+        0
+      ],
+      [
+        3,
+        1
+      ],
+      [
+        3,
+        2
+      ],
+      [
+        4,
+        0
+      ],
+      [
+        4,
+        1
+      ],
+      [
+        4,
+        2
+      ]
+    ],
+    1
+  ],
+  [
+    "hex1-m2",
+    "H",
+    [
+      [
+        0,
+        0
+      ]
+    ],
+    2
+  ],
+  [
+    "hexprop-m2",
+    "H",
+    [
+      [
+        0,
+        0
+      ],
+      [
+        1,
+        0
+      ],
+      [
+        -1,
+        1
+      ],
+      [
+        0,
+        -1
+      ]
+    ],
+    2
+  ],
+  [
+    "iam2-m2",
+    "I",
+    [
+      [
+        0,
+        0
+      ],
+      [
+        1,
+        1
+      ]
+    ],
+    2
+  ]
+]

```
</details>

<details><summary>Raw paired measurements: fast-touch-check.json</summary>

```json
{
  "random_graph_checks": 120,
  "full_formula_comparisons": 5,
  "records": [
    {
      "id": "hex11-kaplan-hc4hh4",
      "depth": 2,
      "runs": [
        {
          "touch_graph_seconds": 4.875729100313038,
          "touch_graph_vertices": 3260,
          "touch_graph_edges": 340774,
          "experimental_fast_graph": false,
          "seconds": 5.710903599858284,
          "ordered_clause_sha256": "9cc0b2dc957b65002439c5594c4fa51b49d26dcb21c194bd68a638136f6198ca",
          "clauses": 120991,
          "variables": 37647,
          "family_counts": [
            [
              "1",
              21
            ],
            [
              "2",
              110797
            ],
            [
              "4",
              2880
            ],
            [
              "5",
              0
            ],
            [
              "6",
              7293
            ]
          ]
        },
        {
          "touch_graph_seconds": 0.207676500082016,
          "touch_graph_vertices": 3260,
          "touch_graph_edges": 340774,
          "experimental_fast_graph": true,
          "seconds": 1.0485042999498546,
          "ordered_clause_sha256": "9cc0b2dc957b65002439c5594c4fa51b49d26dcb21c194bd68a638136f6198ca",
          "clauses": 120991,
          "variables": 37647,
          "family_counts": [
            [
              "1",
              21
            ],
            [
              "2",
              110797
            ],
            [
              "4",
              2880
            ],
            [
              "5",
              0
            ],
            [
              "6",
              7293
            ]
          ]
        }
      ]
    },
    {
      "id": "hex13-kaplan-hc4hh4",
      "depth": 2,
      "runs": [
        {
          "touch_graph_seconds": 8.814394500106573,
          "touch_graph_vertices": 4029,
          "touch_graph_edges": 484841,
          "experimental_fast_graph": false,
          "seconds": 9.892427599988878,
          "ordered_clause_sha256": "ad1fc49acd85518e787f0a1a4225d0154108c994faf5947a4cde65c7945858d6",
          "clauses": 167470,
          "variables": 55217,
          "family_counts": [
            [
              "1",
              20
            ],
            [
              "2",
              156500
            ],
            [
              "4",
              3624
            ],
            [
              "5",
              0
            ],
            [
              "6",
              7326
            ]
          ]
        },
        {
          "touch_graph_seconds": 0.36300629982724786,
          "touch_graph_vertices": 4029,
          "touch_graph_edges": 484841,
          "experimental_fast_graph": true,
          "seconds": 1.4608982000499964,
          "ordered_clause_sha256": "ad1fc49acd85518e787f0a1a4225d0154108c994faf5947a4cde65c7945858d6",
          "clauses": 167470,
          "variables": 55217,
          "family_counts": [
            [
              "1",
              20
            ],
            [
              "2",
              156500
            ],
            [
              "4",
              3624
            ],
            [
              "5",
              0
            ],
            [
              "6",
              7326
            ]
          ]
        }
      ]
    },
    {
      "id": "hex15-kaplan-hc4hh4-a",
      "depth": 2,
      "runs": [
        {
          "touch_graph_seconds": 10.861471199896187,
          "touch_graph_vertices": 4088,
          "touch_graph_edges": 473403,
          "experimental_fast_graph": false,
          "seconds": 12.080651999916881,
          "ordered_clause_sha256": "085a55bf0c9adbb730ceca277ceceaf7e5055232d4cfb8570758ae68af2876b4",
          "clauses": 195179,
          "variables": 64009,
          "family_counts": [
            [
              "1",
              20
            ],
            [
              "2",
              184091
            ],
            [
              "4",
              3680
            ],
            [
              "5",
              0
            ],
            [
              "6",
              7388
            ]
          ]
        },
        {
          "touch_graph_seconds": 0.3851999999023974,
          "touch_graph_vertices": 4088,
          "touch_graph_edges": 473403,
          "experimental_fast_graph": true,
          "seconds": 1.6116110999137163,
          "ordered_clause_sha256": "085a55bf0c9adbb730ceca277ceceaf7e5055232d4cfb8570758ae68af2876b4",
          "clauses": 195179,
          "variables": 64009,
          "family_counts": [
            [
              "1",
              20
            ],
            [
              "2",
              184091
            ],
            [
              "4",
              3680
            ],
            [
              "5",
              0
            ],
            [
              "6",
              7388
            ]
          ]
        }
      ]
    },
    {
      "id": "hex16-kaplan-hc4hh4",
      "depth": 2,
      "runs": [
        {
          "touch_graph_seconds": 20.990186600014567,
          "touch_graph_vertices": 5106,
          "touch_graph_edges": 689312,
          "experimental_fast_graph": false,
          "seconds": 22.722183000296354,
          "ordered_clause_sha256": "3dcdf6f738b2d82de3ae875074892a1e3bf412e9b5e22a4148643a30be3b1cc2",
          "clauses": 259378,
          "variables": 85225,
          "family_counts": [
            [
              "1",
              24
            ],
            [
              "2",
              244295
            ],
            [
              "4",
              4635
            ],
            [
              "5",
              0
            ],
            [
              "6",
              10424
            ]
          ]
        },
        {
          "touch_graph_seconds": 0.6212148000486195,
          "touch_graph_vertices": 5106,
          "touch_graph_edges": 689312,
          "experimental_fast_graph": true,
          "seconds": 2.4722878001630306,
          "ordered_clause_sha256": "3dcdf6f738b2d82de3ae875074892a1e3bf412e9b5e22a4148643a30be3b1cc2",
          "clauses": 259378,
          "variables": 85225,
          "family_counts": [
            [
              "1",
              24
            ],
            [
              "2",
              244295
            ],
            [
              "4",
              4635
            ],
            [
              "5",
              0
            ],
            [
              "6",
              10424
            ]
          ]
        }
      ]
    },
    {
      "id": "frontier-15hex-b",
      "depth": 2,
      "runs": [
        {
          "touch_graph_seconds": 23.57921769982204,
          "touch_graph_vertices": 5848,
          "touch_graph_edges": 848454,
          "experimental_fast_graph": false,
          "seconds": 25.33392810029909,
          "ordered_clause_sha256": "36759053558e3209dbd4e6d0dc3a5eb44dfd7967e91acb97c497839c37a4b194",
          "clauses": 279851,
          "variables": 91257,
          "family_counts": [
            [
              "1",
              23
            ],
            [
              "2",
              264546
            ],
            [
              "4",
              5376
            ],
            [
              "5",
              0
            ],
            [
              "6",
              9906
            ]
          ]
        },
        {
          "touch_graph_seconds": 0.828114700037986,
          "touch_graph_vertices": 5848,
          "touch_graph_edges": 848454,
          "experimental_fast_graph": true,
          "seconds": 2.588986699935049,
          "ordered_clause_sha256": "36759053558e3209dbd4e6d0dc3a5eb44dfd7967e91acb97c497839c37a4b194",
          "clauses": 279851,
          "variables": 91257,
          "family_counts": [
            [
              "1",
              23
            ],
            [
              "2",
              264546
            ],
            [
              "4",
              5376
            ],
            [
              "5",
              0
            ],
            [
              "6",
              9906
            ]
          ]
        }
      ]
    }
  ]
}
```
</details>

<details><summary>Raw paired measurements: fast-touch-check-d3-offset-0.json</summary>

```json
{
  "random_graph_checks": 120,
  "full_formula_comparisons": 1,
  "records": [
    {
      "id": "hex11-kaplan-hc4hh4",
      "depth": 3,
      "runs": [
        {
          "touch_graph_seconds": 49.5015406999737,
          "touch_graph_vertices": 7940,
          "touch_graph_edges": 1126054,
          "experimental_fast_graph": false,
          "seconds": 61.22457369975746,
          "ordered_clause_sha256": "6ea6d031a3acd8d63c1d4c4de18c3271dc4fa8ec673b5204ba5faf5671b50173",
          "clauses": 529105,
          "variables": 127407,
          "family_counts": [
            [
              "1",
              21
            ],
            [
              "2",
              361567
            ],
            [
              "4",
              10440
            ],
            [
              "5",
              89304
            ],
            [
              "6",
              67773
            ]
          ]
        },
        {
          "touch_graph_seconds": 2.0302221002057195,
          "touch_graph_vertices": 7940,
          "touch_graph_edges": 1126054,
          "experimental_fast_graph": true,
          "seconds": 14.63710379973054,
          "ordered_clause_sha256": "6ea6d031a3acd8d63c1d4c4de18c3271dc4fa8ec673b5204ba5faf5671b50173",
          "clauses": 529105,
          "variables": 127407,
          "family_counts": [
            [
              "1",
              21
            ],
            [
              "2",
              361567
            ],
            [
              "4",
              10440
            ],
            [
              "5",
              89304
            ],
            [
              "6",
              67773
            ]
          ]
        }
      ]
    }
  ]
}
```
</details>
