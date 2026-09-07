"""Check the exported row identities by direct multiplication, without elimination."""
import json
from fractions import Fraction
from pathlib import Path
root=Path(__file__).resolve().parent
data=json.loads((root/'results/inverse-periodic-obstruction.json').read_text())
A=data['matrix_A']; B=data['matrix_B']; certificate=data['row_combination_certificate']
from search import verify_witness
source=verify_witness((root/'results/shapes/discussion75-d3-f8df9dc177363142.heesch').read_text()).submission
poses=source.patches[0]; domain=[tuple(c) for c in data['domain']]
assert A==[[sum(xf.apply(candidate)==tuple(target) for _,xf in poses)
            for candidate in domain] for target in data['protected_cells']]
period=data['periodic_certificate']; (a,z),(b,d)=period['lattice_basis']; assert z==0
rebuilt=[]
for x in range(a):
    for y in range(d):
        row=[]
        for candidate in domain:
            count=0
            for orient,dx,dy in period['placements']:
                u,v=source.grid.orientations[orient].apply(candidate); u+=dx; v+=dy
                count+=((u-b*(v//d))%a,v%d)==(x,y)
            row.append(count)
        rebuilt.append(row)
assert rebuilt==B
assert len(certificate)==len(B)==80
for target,identity in zip(B,certificate):
    actual=[Fraction(0)]*len(data['domain'])
    for index,numerator,denominator in identity:
        assert 0<=index<len(A) and denominator>0
        weight=Fraction(numerator,denominator)
        for j,value in enumerate(A[index]): actual[j]+=weight*value
    assert actual==target
x=data['original_occupancy']
assert set(x)<={0,1} and sum(x)==20
assert all(sum(a*b for a,b in zip(row,x))==1 for row in A+B)
out={'exact_row_identities_checked':len(B),'candidate_variables':len(x),
     'geometric_matrices_independently_rebuilt':True,
     'matrix_entries_checked':len(B)*len(x),'baseline_occupancy_passed':True,
     'claim':'B=C*A checked exactly: preserving this protected occupancy forces this periodic partition.',
     'official_non_tiler_proof':False}
(root/'results/inverse-identity-check.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
