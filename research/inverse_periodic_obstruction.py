"""Exact rational row-space test: does protected occupancy force a periodic tile?

A records finite-patch incidence; B records periodic incidence. If every row of
B lies in rowspace(A), preserving A*x also preserves B*x. This is a finite-domain
conditional statement, not a theorem about arbitrary Heesch constructions.
"""
from collections import Counter
from fractions import Fraction
import json
from search import LAB, verify_witness, required_set

def basis(rows):
    pivots={}
    for row in rows:
        vector=list(map(Fraction,row))
        for p,b in sorted(pivots.items()):
            coefficient=vector[p]
            if coefficient: vector=[x-coefficient*y for x,y in zip(vector,b)]
        p=next((i for i,x in enumerate(vector) if x),None)
        if p is not None:
            coefficient=vector[p]; pivots[p]=[x/coefficient for x in vector]
    return pivots

sub=verify_witness((LAB/'results/shapes/discussion75-d3-f8df9dc177363142.heesch').read_text()).submission
grid=sub.grid; shape=set(sub.cells); poses=sub.patches[0]
domain=sorted(shape|{c for s in shape for c in grid.edge_neighbors(s)})
inside=frozenset().union(*(xf.apply_all(shape) for lv,xf in poses if lv<=1))
protected=sorted(inside|required_set(inside,grid.contact('point')))
columns=[Counter(xf.apply(c) for _,xf in poses) for c in domain]
A=[[column[cell] for column in columns] for cell in protected]
certificate=json.loads((LAB/'results/discussion75-refinement.json').read_text())['periodic_search']['certificate']
(a,zero),(b,d)=certificate['lattice_basis']; assert zero==0
def reduce(x,y): return ((x-b*(y//d))%a,y%d)
periodic_columns=[]
for cell in domain:
    counts=Counter()
    for orientation,dx,dy in certificate['placements']:
        x,y=grid.orientations[orientation].apply(cell)
        counts[reduce(x+dx,y+dy)]+=1
    periodic_columns.append(counts)
B=[[column[(x,y)] for column in periodic_columns] for x in range(a) for y in range(d)]
indicator=[int(c in shape) for c in domain]
assert all(sum(x*y for x,y in zip(row,indicator))==1 for row in A+B)
rank_a=len(basis(A)); rank_joint=len(basis(A+B))
# Produce explicit rational identities B = C*A, not just a rank assertion.
pivots={}
for index,row in enumerate(A):
    vector=list(map(Fraction,row)); weights={index:Fraction(1)}
    for p,(v,w) in sorted(pivots.items()):
        f=vector[p]
        if not f: continue
        vector=[x-f*y for x,y in zip(vector,v)]
        for key,value in w.items(): weights[key]=weights.get(key,Fraction(0))-f*value
    p=next((i for i,x in enumerate(vector) if x),None)
    if p is not None:
        f=vector[p]; pivots[p]=([x/f for x in vector],{i:x/f for i,x in weights.items() if x})
identities=[]
for row in B:
    vector=list(map(Fraction,row)); weights={}
    for p,(v,w) in sorted(pivots.items()):
        f=vector[p]
        if not f: continue
        vector=[x-f*y for x,y in zip(vector,v)]
        for key,value in w.items(): weights[key]=weights.get(key,Fraction(0))+f*value
    assert not any(vector)
    identities.append([[i,x.numerator,x.denominator] for i,x in sorted(weights.items()) if x])
out={'domain':domain,'protected_cells':protected,'matrix_A':A,'matrix_B':B,
     'row_combination_certificate':identities,
     'original_occupancy':indicator,'periodic_certificate':certificate,
     'rank_A':rank_a,'rank_stacked_A_B':rank_joint,'nullity_A':len(domain)-rank_a,
     'periodicity_forced_under_protected_occupancy':rank_a==rank_joint,
     'arithmetic':'Exact rational Gaussian elimination',
     'scope':'Only this finite 44-cell candidate domain and fixed placement pattern; no general Heesch impossibility claim.'}
(LAB/'results/inverse-periodic-obstruction.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k not in ('domain','protected_cells','matrix_A','matrix_B','original_occupancy','periodic_certificate','row_combination_certificate')},indent=2))
