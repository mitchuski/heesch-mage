"""Independent brute-force calibration of the search core on small instances."""
import itertools, random, json
from search import CoverSearch, LAB
rng=random.Random(1907)
checks=0
for case in range(160):
    required=set(range(rng.randint(1,7)))
    universe=[(frozenset(rng.sample(range(10),rng.randint(1,4))),None) for _ in range(rng.randint(1,9))]
    universe=[p for p in universe if p[0]&required]
    best=len(required)
    for bits in range(1<<len(universe)):
        occupied=set(); legal=True
        for i,(cells,_) in enumerate(universe):
            if bits>>i&1:
                if cells&occupied: legal=False; break
                occupied.update(cells)
        if legal: best=min(best,len(required-occupied))
    solver=CoverSearch(universe,required)
    for budget in range(len(required)+1):
        out=solver.solve(budget,2)
        assert out['status']==('SAT' if best<=budget else 'EXHAUSTED'),(case,budget,best,out)
        checks+=1
(LAB/'results/calibration.json').write_text(json.dumps({'random_instances':160,'brute_force_comparisons':checks,'passed':True},indent=2))
print(checks,'brute-force comparisons passed')
