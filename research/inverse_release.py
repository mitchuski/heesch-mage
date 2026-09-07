"""Measure when releasing protected cells breaks the periodic implication."""
import json
from fractions import Fraction
from search import LAB, verify_witness, required_set
from inverse_patch_design import run

def rank(rows):
    pivots={}
    for row in rows:
        v=list(map(Fraction,row))
        for pivot,b in sorted(pivots.items()):
            coefficient=v[pivot]
            if coefficient: v=[x-coefficient*y for x,y in zip(v,b)]
        p=next((i for i,x in enumerate(v) if x),None)
        if p is not None:
            scale=v[p]; pivots[p]=[x/scale for x in v]
    return len(pivots)

data=json.loads((LAB/'results/inverse-periodic-obstruction.json').read_text())
path=LAB/'results/shapes/discussion75-d3-f8df9dc177363142.heesch'
sub=verify_witness(path.read_text()).submission
shape=frozenset(sub.cells); contact=sub.grid.contact('point')
regions=[('center_only',shape),('center_and_halo',shape|required_set(shape,contact)),
         ('first_ring_without_halo',frozenset().union(*(xf.apply_all(shape) for lv,xf in sub.patches[0] if lv<=1)))]
records=[]
for name,region in regions:
    A=[row for cell,row in zip(data['protected_cells'],data['matrix_A']) if tuple(cell) in region]
    ra=rank(A); rab=rank(A+data['matrix_B'])
    row={'region':name,'protected_cell_count':len(A),'rank_A':ra,'rank_stacked_A_B':rab,
         'periodicity_implication_broken':ra<rab}
    if ra<rab:
        row['inverse_search']=run(path,region,max_seconds=20)
    records.append(row)
    (LAB/'results/inverse-release.json').write_text(json.dumps({'records':records,
        'scope':'Exact row-space tests on three prescribed protected regions; cell-edit searches have twenty-second budgets. Breaking implication is not non-tiler evidence.'},indent=2))
    print(name,ra,rab,row.get('inverse_search',{}).get('verified_deep_shapes'),flush=True)
