"""Bounded larger-period search with a fixed identity tile in each torus.

Fixing a tile removes translation freedom. Missing a solution proves nothing;
every positive is exported as an explicit, independently checkable partition.
"""
import json
import time
from search import LAB, CoverSearch
from heesch_verify.grids import GRIDS

def find_anchored(shape, seconds=20, copies=(4,5,6,8)):
    start=time.monotonic(); deadline=start+seconds; grid=GRIDS['H']; tested=0
    identity=next(s.index for s in grid.orientations if all(s.apply(c)==tuple(c) for c in ((0,0),(1,0),(0,1))))
    for k in copies:
        area=k*len(shape)
        bases=[(a,b,area//a) for a in range(1,area+1) if area%a==0 for b in range(a)]
        bases.sort(key=lambda t:(abs(t[0]-t[2]),t[1],t[0]))
        for a,b,d in bases:
            if time.monotonic()>=deadline: break
            def reduce(x,y): return ((x-b*(y//d))%a,y%d)
            anchor=frozenset(reduce(x,y) for x,y in shape)
            if len(anchor)!=len(shape): continue
            required={(x,y) for x in range(a) for y in range(d)}-anchor
            universe=[]; seen=set(); timed_out=False
            for sym in grid.orientations:
                image=[sym.apply(c) for c in shape]
                for dx in range(a):
                    if time.monotonic()>=deadline: timed_out=True; break
                    for dy in range(d):
                        residues=set()
                        for x,y in image:
                            cell=reduce(x+dx,y+dy)
                            if cell in anchor or cell in residues: break
                            residues.add(cell)
                        else:
                            cells=frozenset(residues)
                            if cells not in seen:
                                seen.add(cells); universe.append((cells,(sym.index,dx,dy)))
                if timed_out: break
            if timed_out: break
            tested+=1
            answer=CoverSearch(universe,required).solve(0,min(.15,max(.001,deadline-time.monotonic())))
            if answer['status']=='SAT':
                placements=[(identity,0,0)]+[universe[i][1] for i in answer['selected']]
                occupied=set()
                for orient,dx,dy in placements:
                    residues=set()
                    for c in shape:
                        x,y=grid.orientations[orient].apply(c)
                        residues.add(reduce(x+dx,y+dy))
                    assert len(residues)==len(shape) and not occupied.intersection(residues)
                    occupied.update(residues)
                assert occupied=={(x,y) for x in range(a) for y in range(d)}
                assert len(placements)==k
                return {'status':'PERIODIC_TILER','seconds':time.monotonic()-start,'lattices_tested':tested,
                    'certificate':{'lattice_basis':[[a,0],[b,d]],'copies_per_period':k,
                                   'placements':placements,'residue_partition_checked':True}}
        if time.monotonic()>=deadline: break
    return {'status':'UNRESOLVED','seconds':time.monotonic()-start,'lattices_tested':tested,'certificate':None}

if __name__=='__main__':
    inputs=json.loads((LAB/'results/discussion75-followup-0.json').read_text())['records']
    control=next(r for r in inputs if r['source_index']==1)
    calibration=find_anchored(control['cells'],10,(4,))
    assert calibration['certificate'], calibration
    (LAB/'results/anchored-calibration.json').write_text(json.dumps(calibration,indent=2))
    print('Known periodic control passed',flush=True)
    leads=json.loads((LAB/'results/discussion75-refined-24.json').read_text())['records']; records=[]
    for row in leads:
        result=find_anchored(row['cells'],20)
        records.append({'canonical_digest':row['canonical_digest'],'source_index':row['source_index'],
                        'cells':row['cells'],'periodic_search':result})
        (LAB/'results/discussion75-refined-wide.json').write_text(json.dumps({'records':records},indent=2))
        print(row['source_index'],result['status'],result['lattices_tested'],flush=True)
