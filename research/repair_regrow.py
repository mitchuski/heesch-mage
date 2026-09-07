"""Retain a repaired first corona, then regrow outer rings without old poses."""
import json
import time
from coordinated_repair import SOURCE, verified_body
from search import LAB, placements, CoverSearch, required_set, verify_witness
from heesch_verify.transform import Xform
from heesch_verify.result import VerifyError
from periodic_anchored import find_anchored

def regrow(body,seconds=2):
    seed=verify_witness(body); shape=seed.submission.cells; grid=seed.submission.grid
    deadline=time.monotonic()+seconds; best=body; depth=1
    class End(Exception): pass
    def grow(patch,occupied,lv):
        nonlocal best,depth
        if time.monotonic()>deadline: raise End
        required=required_set(occupied,grid.contact('point'))
        universe=placements(shape,grid,occupied,required)
        def accept(ids):
            nonlocal best,depth
            if time.monotonic()>deadline: raise End
            nxt=patch+tuple((lv,universe[i][1]) for i in ids)
            text='H '+' '.join(f'{x} {y}' for x,y in sorted(shape))+f'\n~ {lv} {lv} 1\n{len(nxt)}\n'
            text+=''.join(f'{level} {xf.as_text()}\n' for level,xf in nxt)
            try: checked=verify_witness(text)
            except VerifyError: return False
            if lv>depth: best=text; depth=lv
            if lv==3: return True
            return grow(nxt,checked.hc_corona.patch_cells,lv+1)
        return CoverSearch(universe,required).solve(0,min(.15 if lv==3 else seconds,max(.001,deadline-time.monotonic())),accept)['status']=='SAT'
    try: grow(seed.submission.patches[0],seed.hc_corona.patch_cells,2)
    except End: pass
    return best,depth

if __name__=='__main__':
    source=verify_witness((LAB/SOURCE).read_text()); poses=source.submission.patches[0]
    records=json.loads((LAB/'results/coordinated-repair-center.json').read_text())['records']
    out={'records':[],'scope':'First saved center repair per shape; bounded outer regrowth. Missing rings remain UNKNOWN.','non_tiler_proofs_generated':0}
    for row in records[:12]:
        example=row['relaxed_center_example']; removed=set(example['removed'])
        xforms=[xf for i,(_,xf) in enumerate(poses) if i not in removed]
        xforms += [Xform(*map(int,text.split())) for text in example['added']]
        body=verified_body(row['cells'],xforms,source.submission.grid,1)
        result={'canonical_digest':row['canonical_digest'],'cells':row['cells'],'verified_depth':0}
        if body:
            body,depth=regrow(body); path=f"results/shapes/repair-regrow-{row['canonical_digest'][:16]}.heesch"
            (LAB/path).write_text(body); verify_witness(body)
            result.update(verified_depth=depth,witness=path)
            result['periodic_search']=find_anchored(row['cells'],1)
        out['records'].append(result)
        (LAB/'results/repair-regrow.json').write_text(json.dumps(out,indent=2))
        print(result['canonical_digest'][:12],result['verified_depth'],result.get('periodic_search',{}).get('status'),flush=True)
