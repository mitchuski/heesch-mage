"""Strong periodic exclusion before spending more time on new geometric leads."""
import json
import argparse
from search import LAB
from periodic_filter import find_periodic
from multiring import seek
from periodic_anchored import find_anchored

parser=argparse.ArgumentParser()
parser.add_argument('--offset',type=int,default=24)
args=parser.parse_args()
bank = {r['canonical_digest']: r for r in json.loads((LAB/f'results/discussion75-periodic-{args.offset}.json').read_text())['records']}
leads = [r for r in json.loads((LAB/f'results/discussion75-geometry-{args.offset}.json').read_text())['records'] if r['verified_depth'] >= 2]
records = []
for lead in leads:
    shape = bank[lead['canonical_digest']]['cells']
    row = dict(canonical_digest=lead['canonical_digest'], source_index=lead['source_index'],
               cells=shape, verified_depth=lead['verified_depth'])
    periodic = find_anchored(shape, 8)
    row['periodic_search'] = periodic
    if periodic['certificate']:
        row['status'] = 'PERIODIC_TILER'
    else:
        row['status'] = 'UNRESOLVED_GEOMETRIC_LEAD'
        result, witness = seek(shape, 3, 15)
        row['deeper_search'] = result
        if result['verified_depth'] >= 3:
            path=LAB/'results/shapes'/f"discussion75-refined-d3-{lead['canonical_digest'][:16]}.heesch"
            path.write_text(witness); row['witness'] = str(path.relative_to(LAB))
            row['verified_depth'] = result['verified_depth']
    records.append(row)
    (LAB/f'results/discussion75-refined-{args.offset}.json').write_text(json.dumps({'records':records,'periodic_backend':'anchored 4,5,6,8 copies'},indent=2))
    print(row['source_index'],row['status'],row['verified_depth'],flush=True)
