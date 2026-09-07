"""Depth-first, verifier-checked multi-corona lookahead on shortlisted shapes.
Subsearch caps and the global deadline are deliberately incomplete. A failure
is UNKNOWN. Positive witnesses are exact geometry, with no non-tiler inference.
"""
import argparse,json,time
from search import LAB,placements,CoverSearch,required_set,verify_witness
from heesch_verify.grids import GRIDS,Contact
from heesch_verify.transform import Xform
from heesch_verify.result import VerifyError

def seek(cells,depth,seconds):
    shape=frozenset(map(tuple,cells)); grid=GRIDS['H']; contact=Contact(grid,'point')
    header='H '+' '.join(f'{x} {y}' for x,y in sorted(shape))+'\n'
    start=time.monotonic(); deadline=start+seconds; best=0; witness=None; counts={}
    class End(Exception): pass
    def descend(patch,P,level):
        nonlocal best,witness
        if time.monotonic()>deadline: raise End
        R=required_set(P,contact); U=placements(shape,grid,P,R)
        def accept(ids):
            nonlocal best,witness
            if time.monotonic()>deadline: raise End
            nxt=patch+tuple((level,U[i][1]) for i in ids)
            body=header+f'~ {level} {level} 1\n{len(nxt)}\n'+''.join(f'{lv} {xf.as_text()}\n' for lv,xf in nxt)
            try: checked=verify_witness(body)
            except VerifyError: return False
            counts[level]=counts.get(level,0)+1
            if level>best: best=level; witness=body
            if level==depth: return True
            return descend(nxt,checked.hc_corona.patch_cells,level+1)
        # Avoid spending the entire budget on one attractive early boundary.
        cap=seconds if level==1 else .15 if level==2 else .08
        return CoverSearch(U,R).solve(0,min(cap,max(.001,deadline-time.monotonic())),accept)['status']=='SAT'
    try: descend(((0,Xform(1,0,0,0,1,0)),),shape,1)
    except End: pass
    return {'verified_depth':best,'target_depth':depth,'seconds':time.monotonic()-start,
        'valid_patches_by_depth':counts,'upper_bound':None},witness

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--seconds',type=float,default=2)
    ap.add_argument('--depth',type=int,default=3); args=ap.parse_args()
    rows={}
    for p in sorted((LAB/'results').glob('paired-growth-*.json')):
        for r in json.loads(p.read_text())['records']:
            if r['status']=='TWO_RINGS_TILING_UNRESOLVED': rows[r['id']]=r
    results=[]
    for id,row in rows.items():
        out,witness=seek(row['cells'],args.depth,args.seconds); out['id']=id
        out['previous_verified_depth']=2
        out['best_known_verified_depth']=max(2,out['verified_depth'])
        if out['verified_depth']<2:
            witness=(LAB/row['witness']).read_text()
        if witness:
            p=LAB/'results/shapes'/f'multiring-{id}.heesch'; p.write_text(witness); out['witness']=str(p.relative_to(LAB))
        results.append(out)
        print(f"{id}: found depth {out['verified_depth']} (target {args.depth})",flush=True)
    (LAB/'results/multiring.json').write_text(json.dumps({'records':results,'non_tiler_proofs_generated':0},indent=2))
if __name__=='__main__': main()
