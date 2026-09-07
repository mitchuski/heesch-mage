"""Find explicit small-period plane tilings to reject false Heesch leads.
For each lattice HNF of index k*area, solve exact covering of its residue cells
with k translated/oriented copies. Every candidate tile must have area distinct
residues. A checked coset partition lifts to a disjoint tiling of the plane.
No solution within this bounded search says nothing about non-tilerhood.
"""
import json,time
from search import LAB,CoverSearch
from heesch_verify.grids import GRIDS
def find_periodic(shape,seconds=5):
    grid=GRIDS['H']; n=len(shape); deadline=time.monotonic()+seconds
    found=None; tested=0
    for k in (2,3,4):
        m=k*n
        # Search balanced fundamental domains first; inspect sheared domains too.
        bases=[(a,b,m//a) for a in range(1,m+1) if m%a==0 for b in range(a)]
        bases.sort(key=lambda v:(abs(v[0]-v[2]),v[1],v[0]))
        for a,b,d in bases:
            if time.monotonic()>deadline: break
            def reduce(c):
                x,y=c; return ((x-b*(y//d))%a,y%d)
            required={(x,y) for x in range(a) for y in range(d)}; U=[]; seen=set()
            for sym in grid.orientations:
                oriented=[sym.apply(c) for c in shape]
                for dx,dy in sorted(required):
                    residues=frozenset(reduce((x+dx,y+dy)) for x,y in oriented)
                    if len(residues)!=n or residues in seen: continue
                    seen.add(residues); U.append((residues,(sym.index,dx,dy)))
            tested+=1
            out=CoverSearch(U,required).solve(0,min(.1,max(.001,deadline-time.monotonic())))
            if out['status']=='SAT':
                selected=[U[i] for i in out['selected']]
                assert len(selected)==k
                assert sum(len(s) for s,_ in selected)==len(set().union(*(s for s,_ in selected)))==m
                found={'lattice_basis':[[a,0],[b,d]],'copies_per_period':k,
                    'placements':[xf for _,xf in selected],'residue_partition_checked':True}; break
        if found or time.monotonic()>deadline: break
    return {'status':'PERIODIC_TILER' if found else 'UNRESOLVED',
        'lattices_tested':tested,'certificate':found}

def main():
    data=json.loads((LAB/'results/shape-frontier.json').read_text())
    shapes={c['id']:c for c in data['candidates']}
    leads=[r for r in json.loads((LAB/'results/lookahead.json').read_text())['records'] if not r['control'] and r['status']=='VERIFIED_TWO_CORONAS']
    results=[dict(find_periodic(shapes[r['id']]['cells']),id=r['id']) for r in leads]
    (LAB/'results/periodic-filter.json').write_text(json.dumps({'records':results},indent=2))
    print(json.dumps(results,indent=2))
if __name__=='__main__': main()
