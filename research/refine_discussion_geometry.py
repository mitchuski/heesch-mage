"""Strong periodic exclusion before spending more time on new geometric leads."""
import json
from search import LAB
from periodic_filter import find_periodic
from multiring import seek

bank = {r['canonical_digest']: r for r in json.loads((LAB/'results/discussion75-periodic-24.json').read_text())['records']}
leads = [r for r in json.loads((LAB/'results/discussion75-geometry-24.json').read_text())['records'] if r['verified_depth'] >= 2]
records = []
for lead in leads:
    shape = bank[lead['canonical_digest']]['cells']
    row = dict(canonical_digest=lead['canonical_digest'], source_index=lead['source_index'],
               cells=shape, verified_depth=lead['verified_depth'])
    periodic = find_periodic(shape, 8)
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
    (LAB/'results/discussion75-refined-24.json').write_text(json.dumps({'records':records},indent=2))
    print(row['source_index'],row['status'],row['verified_depth'],flush=True)
