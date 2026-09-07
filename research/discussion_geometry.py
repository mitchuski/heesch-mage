"""Bounded geometric follow-up while native SAT is unavailable."""
import json
import argparse
from finite_obstruction import screen
from search import LAB, verify_witness
from heesch_verify.result import VerifyError
from multiring import seek

parser = argparse.ArgumentParser()
parser.add_argument('--offset', type=int, default=12)
parser.add_argument('--seconds', type=float, default=3)
args = parser.parse_args()
source = json.loads((LAB/f'results/discussion75-periodic-{args.offset}.json').read_text())['records']
records = []
for row in source:
    if row['certificate']:
        continue
    cells = row['cells']
    result = screen(cells, 2, args.seconds)
    record = {'source_index': row['source_index'], 'canonical_digest': row['canonical_digest'],
              'screen': result, 'verified_depth': 0}
    if result['relaxed_witness']:
        rings = result['relaxed_witness']
        text = 'H ' + ' '.join(f'{x} {y}' for x,y in cells) + '\n~ 2 2 1\n'
        text += str(1 + sum(map(len,rings))) + '\n0 <1,0,0,0,1,0>\n'
        for level, ring in enumerate(rings, 1):
            text += ''.join(f'{level} <'+','.join(map(str,xf))+'>\n' for xf in ring)
        try:
            checked = verify_witness(text)
        except VerifyError as error:
            record['strict_rejection'] = str(error)
        else:
            record['verified_depth'] = checked.hc_corona.max_level
            path = LAB/'results/shapes'/f"discussion75-geometry-d2-{row['canonical_digest'][:16]}.heesch"
            path.write_text(text); record['witness'] = str(path.relative_to(LAB))
            deeper, witness = seek(cells, 3, 5)
            record['deeper_search'] = deeper
            if witness and deeper['verified_depth'] >= 3:
                path = LAB/'results/shapes'/f"discussion75-geometry-d3-{row['canonical_digest'][:16]}.heesch"
                path.write_text(witness); record['deeper_witness'] = str(path.relative_to(LAB))
                record['verified_depth'] = deeper['verified_depth']
    records.append(record)
    (LAB/f'results/discussion75-geometry-{args.offset}.json').write_text(json.dumps({'records':records,
        'scope':'Bounded relaxed geometry search; positives independently checked. No official non-tiler certificates.'},indent=2))
    print(row['source_index'], result['status'], record['verified_depth'], flush=True)
