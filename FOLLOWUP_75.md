Independent follow-up: a checkable tiling certificate for one of the 153 open cases

Thanks for publishing the exact unresolved inputs and the periodic-calibration
audit. We used your `open-153.jsonl` unchanged (SHA-256
`c131631a5fb1806f722031175e51d8576ddd74b46cc745eaeb7a76ab991621de`) and
independently checked all 153 canonical identities and native-input hashes.
Credit for this bank remains with nasqret, the overlay recipe with Frodan, and
the underlying parent shapes with Kaplan.

We tested the first twelve entries in file order with a bounded native Glucose4
driver and an experimental bitset acceleration of the official multilevel
encoder's contact graph. That graph change preserves ordered clauses on the six
record-control formula comparisons tested so far; it is not an official harness
change.

One entry now has a positive, independently checked plane-tiling certificate:
the **second entry (zero-based index 1)**, canonical digest
`f8df9dc177363142ba2df27d279a12b78b974c40f2f66d9418841fc5036bd0f6`.
Its two-ring witness passed the unchanged geometry checker; a subsequent search
found the explicit periodic partition below. A three-ring witness also passed,
but the tiling certificate excludes it as a finite-Heesch candidate.

The lattice basis is `(8,0), (3,10)`, with four oriented/translated copies of the
20-cell tile per period. All 80 residue cells are covered exactly once. This is
an explicit partition certificate, not a native periodic status marker.

Run this from the unchanged public verifier checkout to check it independently:

```python
from heesch_verify.grids import GRIDS
from heesch_verify.canonical import canonical_digest
shape = [[0, 1], [0, 2], [0, 3], [0, 5], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, 1], [2, 2], [2, 3], [2, 4], [3, 1], [3, 2], [3, 3], [3, 4], [4, 0], [4, 1], [4, 3]]
placements = [[1, 0, 5], [10, 5, 3], [4, 4, 8], [7, 4, 0]]
grid = GRIDS['H']
assert canonical_digest(shape, grid, True) == 'f8df9dc177363142ba2df27d279a12b78b974c40f2f66d9418841fc5036bd0f6'
seen = set()
for orientation, dx, dy in placements:
    residues = set()
    for cell in shape:
        x, y = grid.orientations[orientation].apply(cell)
        x += dx
        y += dy
        residues.add(((x - 3 * (y // 10)) % 8, y % 10))
    assert len(residues) == 20
    assert seen.isdisjoint(residues)
    seen.update(residues)
assert seen == {(x, y) for x in range(8) for y in range(10)}
print('Four copies partition all 80 lattice residues: periodic tiling checked.')
```

Each tile has distinct residues, different tiles have disjoint residues, and
their union is the full quotient. Translating these four tiles by every lattice
vector therefore gives a disjoint covering of the plane.

The other eleven entries returned UNSAT at depth two, without official proof
certificates. Those remain provisional solver results; I am not claiming an
official closure of them or of the whole queue. The remaining 141 inputs were
not tested in this batch. No new finite Heesch record or score improvement is
claimed. Prepared with Codex.

<details><summary>Verified two-ring geometry witness</summary>

```text
H 0 1 0 2 0 3 0 5 1 0 1 1 1 2 1 3 1 4 2 1 2 2 2 3 2 4 3 1 3 2 3 3 3 4 4 0 4 1 4 3
~ 2 2 1
19
0 <1,0,0,0,1,0>
1 <-1,0,-1,0,-1,4>
1 <-1,0,8,0,-1,5>
1 <0,1,-1,1,0,-4>
1 <0,1,0,1,0,5>
1 <0,-1,8,-1,0,0>
1 <0,-1,0,-1,0,8>
2 <1,0,-1,0,1,-9>
2 <1,0,8,0,1,-8>
2 <1,0,-9,0,1,-1>
2 <1,0,9,0,1,1>
2 <1,0,-8,0,1,8>
2 <1,0,1,0,1,9>
2 <-1,0,7,0,-1,-4>
2 <-1,0,0,0,-1,13>
2 <0,1,8,1,0,-3>
2 <0,1,-9,1,0,4>
2 <0,-1,-1,-1,0,-1>
2 <0,-1,9,-1,0,9>

```
</details>
