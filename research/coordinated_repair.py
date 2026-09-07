"""Bounded scaffold repair over every minimum cover of disjoint overlap edges.

Preserves the source inner-two-ring region and its halo. This is a restricted
repair experiment, not an exhaustive corona search or a non-tiler test.
"""
import argparse
from collections import Counter
from itertools import product
import json
import time
from search import LAB, CoverSearch, placements, required_set, verify_witness
from heesch_verify.result import VerifyError

SOURCE = 'results/shapes/discussion75-d3-f8df9dc177363142.heesch'

def verified_body(shape, xforms, grid, depth=3):
    tiles=[xf.apply_all(shape) for xf in xforms]
    levels={0:0}; pending=set(range(1,len(tiles))); frontier=tiles[0]
    for level in range(1,len(tiles)):
        halo=required_set(frontier,grid.contact('point'))
        newly={i for i in pending if tiles[i]&halo}
        if not newly: break
        levels.update((i,level) for i in newly)
        pending-=newly; frontier=frozenset().union(*(tiles[i] for i in newly))
    # Disconnected outer scaffolding is not part of the claimed corona.
    chosen=[(lv,xforms[i]) for i,lv in levels.items() if lv<=depth]
    body='H '+' '.join(f'{x} {y}' for x,y in sorted(shape))+f'\n~ {depth} {depth} 1\n{len(chosen)}\n'
    body+=''.join(f'{lv} {xf.as_text()}\n' for lv,xf in chosen)
    try: checked=verify_witness(body)
    except VerifyError: return None
    return body if checked.hc_corona.max_level==depth else None

def run(row, source, seconds, target_mode='inner-two'):
    start=time.monotonic(); deadline=start+seconds
    shape=frozenset(map(tuple,row['cells'])); grid=source.submission.grid
    poses=source.submission.patches[0]; tiles=[xf.apply_all(shape) for _,xf in poses]
    edges=row['edges']; vertices=[i for edge in edges for i in edge]
    assert len(vertices)==len(set(vertices)), 'This experiment requires disjoint edges'
    inner=frozenset().union(*(xf.apply_all(source.submission.cells) for lv,xf in poses if lv<=2))
    target=inner|required_set(inner,grid.contact('point'))
    if target_mode=='center': target=tiles[0]|required_set(tiles[0],grid.contact('point'))
    universe=placements(shape,grid,tiles[0],target-tiles[0])
    blockers=[sum(1<<i for i,tile in enumerate(tiles) if cells&tile) for cells,_ in universe]
    allmask=(1<<len(poses))-1; counts=Counter(); witness=None; successful_removed=None; relaxed_example=None
    for endpoints in product(*edges):
        if time.monotonic()>deadline: break
        if 0 in endpoints: continue
        counts['covers_tested']+=1
        removed=sum(1<<i for i in endpoints); retained=allmask^removed
        fixed=frozenset().union(*(tile for i,tile in enumerate(tiles) if retained>>i&1))
        gaps=target-fixed
        available=[u for u,b in zip(universe,blockers) if not b&retained and u[0]&gaps]
        possible=frozenset().union(*(u[0] for u in available))
        if not gaps<=possible:
            counts['uncoverable_gap']+=1; continue
        fixed_xforms=[xf for i,(_,xf) in enumerate(poses) if retained>>i&1]
        def accept(ids):
            nonlocal witness
            witness=verified_body(shape,fixed_xforms+[available[i][1] for i in ids],grid)
            return witness is not None
        result=CoverSearch(available,gaps).solve(0,min(.1,max(.001,deadline-time.monotonic())),
                                               None if target_mode=='center' else accept)
        counts[result['status']]+=1
        if target_mode=='center' and result['status']=='SAT' and relaxed_example is None:
            relaxed_example={'removed':list(endpoints),
                             'added':[available[i][1].as_text() for i in result['selected']]}
        if witness:
            successful_removed=list(endpoints); break
    path=None
    if witness:
        path=f"results/shapes/coordinated-{row['canonical_digest'][:16]}.heesch"
        (LAB/path).write_text(witness)
    return {'canonical_digest':row['canonical_digest'],'cells':row['cells'],
            'minimum_removals':len(edges),'possible_covers':2**len(edges),
            'counts':dict(counts),'candidate_placements':len(universe),
            'seconds':time.monotonic()-start,'witness':path,'successful_removed':successful_removed,
            'relaxed_center_example':relaxed_example,
            'all_covers_tested':counts['covers_tested']==2**len(edges)}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--limit',type=int,default=6)
    ap.add_argument('--seconds',type=float,default=8)
    ap.add_argument('--target',choices=('inner-two','center'),default='inner-two'); args=ap.parse_args()
    source=verify_witness((LAB/SOURCE).read_text())
    # Calibration must reconstruct the known positive patch from its poses.
    assert verified_body(source.submission.cells,[xf for _,xf in source.submission.patches[0]],source.submission.grid)
    rows=json.loads((LAB/'results/overlap-repair-profile.json').read_text())['records']
    rows=[r for r in rows if len(r['edges'])==9][:args.limit]
    out={'source':SOURCE,'positive_calibration_passed':True,'records':[],
         'target':args.target,
         'scope':'Minimum nine-pose repairs. Inner-two target requires verified depth three; center target only tests disjoint coverage of the center halo, with no hole or full-corona claim. Failures concern retained poses only.',
         'non_tiler_proofs_generated':0}
    for row in rows:
        result=run(row,source,args.seconds,args.target); out['records'].append(result)
        (LAB/f'results/coordinated-repair-{args.target}.json').write_text(json.dumps(out,indent=2))
        print(result['canonical_digest'][:12],result['counts'],result['witness'],flush=True)
