"""Counterexample filter for the inverse-design placement-repair queue."""
import json
from search import LAB
from periodic_anchored import find_anchored

if __name__=='__main__':
    inputs=json.loads((LAB/'results/overlap-repair-profile.json').read_text())['records']
    path=LAB/'results/repair-periodic.json'
    prior={r['canonical_digest']:r for r in json.loads(path.read_text())['records']} if path.exists() else {}
    out={'records':[],'scope':'Explicit positive partitions exclude tilers; bounded failures remain UNKNOWN.'}
    for row in inputs:
        saved=prior.get(row['canonical_digest'])
        if saved and saved['periodic_search']['status']=='PERIODIC_TILER':
            out['records'].append(saved)
        else:
            out['records'].append({'canonical_digest':row['canonical_digest'],'cells':row['cells'],
                                   'periodic_search':find_anchored(row['cells'],1)})
        (LAB/'results/repair-periodic.json').write_text(json.dumps(out,indent=2))
    print('Periodic:',sum(r['periodic_search']['status']=='PERIODIC_TILER' for r in out['records']), '/',len(inputs))
