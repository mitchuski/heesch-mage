"""Exhaustive-or-UNKNOWN relaxed corona search for non-tiler screening.

Unlike witness lookahead, this search permits holes at every layer and has no
per-child truncation. Every plane tiling induces a successful finite expansion:
take all tiles touching the previous patch. Thus exhausted expansion proves a
finite obstruction within this implementation. This is NOT the official frozen
encoder's DRAT/LRAT certificate and must not be submitted as one.
Global deadlines propagate as UNKNOWN; failed patch occupancies are memoized.
"""
import argparse,json,time
from search import LAB,placements,CoverSearch,required_set
from heesch_verify.grids import GRIDS,Contact
from heesch_verify.shape import check_shape

def screen(cells,depth,seconds):
    shape=frozenset(map(tuple,cells)); grid=GRIDS['H']; contact=Contact(grid,'point')
    check_shape(shape,grid,max_cells=200,max_span_sum=29)
    deadline=time.monotonic()+seconds; start=time.monotonic(); failures=set(); nodes=0
    expansions={}; successful=None
    class Deadline(Exception): pass
    def expand(P,remaining,path):
        nonlocal nodes,successful
        if time.monotonic()>deadline: raise Deadline
        if remaining==0: successful=path; return True
        key=(P,remaining)
        if key in failures: return False
        expansions[remaining]=expansions.get(remaining,0)+1
        R=required_set(P,contact); U=placements(shape,grid,P,R)
        def accept(ids):
            return expand(P.union(*(U[i][0] for i in ids)),remaining-1,
                          path+[[(U[i][1].a,U[i][1].b,U[i][1].c,U[i][1].d,U[i][1].e,U[i][1].f) for i in ids]])
        answer=CoverSearch(U,R).solve(0,max(.001,deadline-time.monotonic()),accept)
        nodes+=answer['nodes']
        if answer['status']=='UNKNOWN_TIMEOUT': raise Deadline
        if answer['status']=='SAT': return True
        failures.add(key); return False
    try: status='RELAXED_EXPANSION_FOUND' if expand(shape,depth,[]) else 'EXHAUSTED_RELAXED_EXPANSION'
    except Deadline: status='UNKNOWN_TIMEOUT'
    return {'status':status,'depth':depth,'seconds':time.monotonic()-start,
        'search_nodes_completed_subcalls':nodes,'expansions_by_remaining_depth':expansions,
        'cached_failed_patches':len(failures),'relaxed_witness':successful,
        'official_non_tiler_certificate':False}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--seconds',type=float,default=8)
    ap.add_argument('--depth',type=int,default=3); args=ap.parse_args()
    rows=json.loads((LAB/'results/unclassified-queue.json').read_text())['records']; results=[]
    for row in rows:
        out=screen(row['cells'],args.depth,args.seconds); out['id']=row['id']; results.append(out)
        print(row['id'],out['status'],'failed patch cache',out['cached_failed_patches'],flush=True)
        (LAB/f'results/finite-obstruction-depth-{args.depth}-budget-{args.seconds:g}.json').write_text(json.dumps({'records':results},indent=2))
if __name__=='__main__': main()
