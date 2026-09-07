"""Contact-graph regression tests: geometric oracle and existing CNF goldens."""
import hashlib
import json
import pathlib
import random
import unittest

from heesch_encoder.multilevel.api import encode_multilevel
from heesch_encoder.multilevel.universe import multilevel_universe, touching_cellset_pairs
from heesch_verify.grids import GRIDS


class TouchGraphTests(unittest.TestCase):
    def test_geometric_oracle(self):
        rng = random.Random(260907)
        for grid in GRIDS.values():
            valid = [(x, y) for x in range(-6, 7) for y in range(-6, 7)
                     if grid.cell_valid((x, y))]
            for mode in ('point', 'edge'):
                contact = grid.contact(mode)
                for _ in range(40):
                    sets = [frozenset(rng.choice(valid) for _ in range(rng.randrange(0, 8)))
                            for _ in range(20)]
                    sets.extend(sets[:3])  # Duplicate geometric placements.
                    expected = []
                    for i, a in enumerate(sets):
                        for j in range(i + 1, len(sets)):
                            b = sets[j]
                            if a.isdisjoint(b) and any(n in b for c in a for n in contact.neighbors(c)):
                                expected.append((i, j))
                    self.assertEqual(touching_cellset_pairs(sets, contact), expected)

    def test_committed_multilevel_goldens(self):
        here = pathlib.Path(__file__).parent
        fixtures = json.loads((here / 'touch_fixtures.json').read_text())
        goldens = json.loads((here / 'golden/ml_digests.json').read_text())
        for name, gid, cells, depth in fixtures:
            with self.subTest(name=name):
                grid = GRIDS[gid]; contact = grid.contact('point')
                tile = frozenset(map(tuple, cells))
                uni = multilevel_universe(tile, grid, contact, depth)
                serialized = '\n'.join(f'{level} {p.symmetry_index} {p.ty} {p.tx}'
                    for level, placements in enumerate(uni.levels, 1) for p in placements)
                enc = encode_multilevel(tile, grid, contact, depth)
                self.assertEqual([hashlib.sha256(serialized.encode()).hexdigest(), enc.digest], goldens[name])


if __name__ == '__main__':
    unittest.main()
