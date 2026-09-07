"""Inverse tile design: preserve a protected patch while exchanging tile cells.

Meet-in-the-middle integer incidence signatures match one/two removed cells to
one/two added cells across every fixed placement. Matches preserve occupancy of
the protected first-ring region exactly. The unchanged witness checker decides
whether all claimed rings remain valid. This restricted search is not a general
impossibility proof for tile deformation or for a shape's Heesch number.
"""
from collections import Counter, defaultdict
from itertools import combinations
import json
import time
from search import LAB, verify_witness, required_set
from heesch_verify.canonical import canonical_digest
from heesch_verify.result import VerifyError
from heesch_verify.shape import check_shape
from periodic_anchored import find_anchored

def signature(cells, poses, protected):
    counts=Counter(xf.apply(c) for c in cells for _,xf in poses if xf.apply(c) in protected)
    return tuple(sorted(counts.items()))

def run(path, protected_override=None, max_seconds=None):
    start=time.monotonic()
    checked=verify_witness(path.read_text()); sub=checked.submission
    grid=sub.grid; shape=frozenset(sub.cells); poses=sub.patches[0]
    depth=checked.hc_corona.max_level
    inside=frozenset().union(*(xf.apply_all(shape) for lv,xf in poses if lv<=1))
    protected=inside|required_set(inside,grid.contact('point'))
    if protected_override is not None: protected=frozenset(protected_override)
    boundary=sorted({c for s in shape for c in grid.edge_neighbors(s)}-shape)
    base_id=canonical_digest(shape,grid,True)
    counts={'signature_matches':0,'legal_new_shapes':0,'verified_deep_shapes':0}
    candidates=[]; seen={base_id}; rejected=Counter(); rejected_edits=[]; search_sizes=[]; complete=True
    for k in (1,2):
        additions=defaultdict(list)
        for add in combinations(boundary,k):
            additions[signature(add,poses,protected)].append(add)
        removes=list(combinations(sorted(shape),k))
        search_sizes.append({'exchanged_cells':k,'removal_sets':len(removes),
                             'addition_sets':sum(map(len,additions.values()))})
        for removed in removes:
            if max_seconds is not None and time.monotonic()-start>=max_seconds:
                complete=False; break
            for added in additions.get(signature(removed,poses,protected),[]):
                if max_seconds is not None and time.monotonic()-start>=max_seconds:
                    complete=False; break
                counts['signature_matches']+=1
                candidate=(shape-set(removed))|set(added)
                try: check_shape(candidate,grid,max_cells=20,max_span_sum=29)
                except VerifyError: continue
                identity=canonical_digest(candidate,grid,True)
                if identity in seen: continue
                seen.add(identity); counts['legal_new_shapes']+=1
                body='H '+' '.join(f'{x} {y}' for x,y in sorted(candidate))+f'\n~ {depth} {depth} 1\n{len(poses)}\n'
                body+=''.join(f'{lv} {xf.as_text()}\n' for lv,xf in poses)
                try: outcome=verify_witness(body)
                except VerifyError as error:
                    reason=str(error).split(':')[0]; rejected[reason]+=1
                    rejected_edits.append({'canonical_digest':identity,'cells':sorted(candidate),
                                           'removed':removed,'added':added,'reason':reason})
                    continue
                counts['verified_deep_shapes']+=1
                target=LAB/'results/shapes'/f'inverse-{identity[:16]}.heesch'
                target.write_text(body)
                periodic=find_anchored(sorted(candidate),3)
                candidates.append({'canonical_digest':identity,'cells':sorted(candidate),
                    'removed':removed,'added':added,'verified_depth':outcome.hc_corona.max_level,
                    'witness':str(target.relative_to(LAB)),'periodic_search':periodic})
        if not complete: break
    return {'source_witness':str(path.relative_to(LAB)),'source_depth':depth,
        'protected_cells':len(protected),'boundary_candidates':len(boundary),
        'search_sizes':search_sizes,**counts,'rejections':dict(rejected),'candidates':candidates,
        'rejected_edits':rejected_edits,
        'enumeration_complete':complete,
        'seconds':time.monotonic()-start}

if __name__=='__main__':
    sources=sorted((LAB/'results/shapes').glob('sat-d3-*.heesch'))
    sources.append(LAB/'results/shapes/discussion75-d3-f8df9dc177363142.heesch')
    sources.append(LAB/'baseline.heesch')
    records=[]
    for path in sources:
        row=run(path); records.append(row)
        (LAB/'results/inverse-patch-design.json').write_text(json.dumps({'records':records,
            'scope':'Complete one/two-cell exchanges in each specified first edge-neighbor shell, requiring protected occupancy signatures and fixed poses. No broader completeness claim.'},indent=2))
        print(path.name,row['signature_matches'],row['verified_deep_shapes'],round(row['seconds'],3),flush=True)
