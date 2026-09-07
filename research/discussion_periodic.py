"""Certificate-only screening of Discussion #75 without native SAT imports."""
import argparse
import hashlib
import json
from search import LAB
from periodic_filter import find_periodic
from heesch_verify.grids import GRIDS
from heesch_verify.canonical import canonical_digest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--offset', type=int, default=12)
    parser.add_argument('--limit', type=int, default=12)
    parser.add_argument('--seconds', type=float, default=3)
    args = parser.parse_args()
    source = LAB / 'contribution/public-inputs/open-153.jsonl'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == 'c131631a5fb1806f722031175e51d8576ddd74b46cc745eaeb7a76ab991621de'
    inputs = [json.loads(line) for line in source.read_text().splitlines()]
    records = []
    for index in range(args.offset, min(len(inputs), args.offset + args.limit)):
        original = inputs[index]
        tokens = original['shape_line'].split(); assert tokens[0] == 'H'
        coords = list(map(int, tokens[1:]))
        cells = tuple(zip(coords[::2], coords[1::2]))
        assert canonical_digest(cells, GRIDS['H'], True) == original['canonical_digest']
        result = find_periodic(cells, args.seconds)
        certificate = result['certificate']
        if certificate:
            (a, zero), (b, d) = certificate['lattice_basis']; assert zero == 0
            occupied = set()
            for orientation, dx, dy in certificate['placements']:
                residues = set()
                for cell in cells:
                    x, y = GRIDS['H'].orientations[orientation].apply(cell)
                    x += dx; y += dy
                    residues.add(((x - b * (y // d)) % a, y % d))
                assert len(residues) == len(cells) and occupied.isdisjoint(residues)
                occupied.update(residues)
            assert occupied == {(x, y) for x in range(a) for y in range(d)}
        records.append(dict(result, source_index=index, cells=cells,
                            canonical_digest=original['canonical_digest']))
        out = {'source': 'https://github.com/Layr-Labs/heesch/discussions/75',
               'offset': args.offset, 'next_offset': index + 1, 'seconds_per_shape': args.seconds,
               'records': records, 'scope': 'Only explicit checked partitions exclude a shape; other results remain UNKNOWN.'}
        (LAB / f'results/discussion75-periodic-{args.offset}.json').write_text(json.dumps(out, indent=2))
        print(index, result['status'], flush=True)

if __name__ == '__main__':
    main()
