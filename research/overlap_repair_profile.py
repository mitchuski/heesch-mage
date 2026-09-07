"""Exact/bounded vertex-cover profile of tile-placement conflicts.

Removing a vertex cover eliminates overlaps, but does not establish that the
holes can be repaired or that the edited shape is a non-tiler.
"""
from collections import Counter
import json
import time
from search import LAB, verify_witness

def cover(edges,seconds=.1):
    deadline=time.monotonic()+seconds
    forced={b if a==0 else a for a,b in edges if a==0 or b==0}
    remaining=[e for e in edges if not forced.intersection(e)]
    greedy=set(forced); rest=remaining
    while rest:
        v=Counter(v for edge in rest for v in edge).most_common(1)[0][0]
        greedy.add(v); rest=[e for e in rest if v not in e]
    best=greedy; nodes=0; timed_out=False
    def visit(es,chosen):
        nonlocal best,nodes
        nodes+=1
        if time.monotonic()>deadline: raise TimeoutError
        if not es:
            if len(chosen)<len(best): best=chosen
            return
        matched=set(); bound=0
        for a,b in es:
            if a not in matched and b not in matched:
                matched.update((a,b)); bound+=1
        if len(chosen)+bound>=len(best): return
        v=Counter(v for edge in es for v in edge).most_common(1)[0][0]
        neighbors={b if a==v else a for a,b in es if v in (a,b)}
        visit([e for e in es if v not in e],chosen|{v})
        visit([e for e in es if not neighbors.intersection(e)],chosen|neighbors)
    try: visit(remaining,forced)
    except TimeoutError: timed_out=True
    assert 0 not in best and all(best.intersection(e) for e in edges)
    return {'removed':sorted(best),'removal_count':len(best),'optimality_proven':not timed_out,'nodes':nodes}

if __name__=='__main__':
    poses=verify_witness((LAB/'results/shapes/discussion75-d3-f8df9dc177363142.heesch').read_text()).submission.patches[0]
    edits=json.loads((LAB/'results/inverse-repair-queue.json').read_text())['records']
    rows=[]
    for edit in edits:
        tiles=[xf.apply_all(edit['cells']) for _,xf in poses]
        edges=[(i,j) for i in range(len(tiles)) for j in range(i+1,len(tiles)) if tiles[i]&tiles[j]]
        result=cover(edges)
        rows.append({'canonical_digest':edit['canonical_digest'],'cells':edit['cells'],
            'edges':edges,'cover':result,'removed_by_level':dict(Counter(poses[i][0] for i in result['removed']))})
    rows.sort(key=lambda r:(r['cover']['removal_count'],len(r['edges']),r['canonical_digest']))
    out={'placements':len(poses),'records':rows,
         'removal_histogram':dict(Counter(r['cover']['removal_count'] for r in rows)),
         'optimality_checks_completed':sum(r['cover']['optimality_proven'] for r in rows),
         'scope':'Minimum removals for these fixed poses only; no general shape bound or repair-existence claim.'}
    (LAB/'results/overlap-repair-profile.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))
