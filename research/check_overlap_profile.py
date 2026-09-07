"""Independent geometry rebuild and disjoint-edge lower-bound certificates."""
import json
from collections import deque
from search import LAB,verify_witness

poses=verify_witness((LAB/'results/shapes/discussion75-d3-f8df9dc177363142.heesch').read_text()).submission.patches[0]
data=json.loads((LAB/'results/overlap-repair-profile.json').read_text()); records=[]
for row in data['records']:
    occupied={}; expected=set()
    for i,(_,xf) in enumerate(poses):
        for c in row['cells']:
            cell=xf.apply(c)
            for j in occupied.get(cell,[]): expected.add((j,i))
            occupied.setdefault(cell,[]).append(i)
    assert expected=={tuple(e) for e in row['edges']}
    adj={}
    for a,b in expected: adj.setdefault(a,set()).add(b); adj.setdefault(b,set()).add(a)
    color={}
    for start in sorted(adj):
        if start in color: continue
        color[start]=0; queue=deque([start])
        while queue:
            v=queue.popleft()
            for w in adj[v]:
                if w not in color: color[w]=1-color[v]; queue.append(w)
                assert color[w]!=color[v]
    paired={}
    def augment(v,seen):
        for w in sorted(adj[v]):
            if w in seen: continue
            seen.add(w)
            if w not in paired or augment(paired[w],seen):
                paired[w]=v; return True
        return False
    for v in sorted(adj):
        if color[v]==0: augment(v,set())
    matching=[sorted((v,w)) for w,v in paired.items()]
    vertices=[v for edge in matching for v in edge]
    assert len(vertices)==len(set(vertices))
    assert all(tuple(e) in expected for e in matching)
    removed=set(row['cover']['removed'])
    assert 0 not in removed and all(removed.intersection(e) for e in expected)
    # Any overlap-free remainder must delete >=1 endpoint per disjoint edge.
    assert len(matching)==len(removed)==row['cover']['removal_count']
    records.append({'canonical_digest':row['canonical_digest'],'lower_bound_disjoint_edges':matching,
                    'minimum_removals':len(matching)})
out={'geometry_graphs_rebuilt':len(records),'matching_lower_bounds_checked':len(records),
     'records':records,'scope':'Exact minimum deletion count for fixed inherited poses, center retained. Not a Heesch-number bound.'}
(LAB/'results/overlap-repair-check.json').write_text(json.dumps(out,indent=2))
print('Independently checked geometry and matching bounds:',len(records))
