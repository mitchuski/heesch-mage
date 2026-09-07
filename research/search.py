"""Isolated participant search. Reads the unchanged Heesch verifier; no solver dependencies.

python -B outputs/heesch_search.py --seconds 30
Search outcomes are geometry results, never non-tiler certificates.
"""
from __future__ import annotations
import argparse, hashlib, json, sys, time
from functools import lru_cache
from pathlib import Path

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB/'vendor'))
from heesch_verify import verify_witness, required_set
from heesch_verify.transform import Xform
from heesch_verify.shape import holes_of
from heesch_verify.defect import verify_defect
from heesch_verify.parse import DefectBlock

@lru_cache(maxsize=256)
def _orientations(shape,grid):
    return tuple((sym,tuple(sym.apply(c) for c in shape)) for sym in grid.orientations)

def placements(shape, grid, patch, required):
    """Complete finite universe: align each tile cell with each required cell.
    Every useful next-corona tile covers a required cell. Dedup by occupied cells.
    """
    seen = {}
    for sym,oriented in _orientations(tuple(shape),grid):
        attempted=set()
        for rx, ry in sorted(required):
            for x, y in oriented:
                dx, dy = rx-x, ry-y
                if (dx,dy) in attempted:
                    continue
                attempted.add((dx,dy))
                if not grid.translation_legal(dx, dy):
                    continue
                # Most aligned placements collide immediately. Avoid building
                # a full frozenset for these; preserve original enumeration order.
                if any((a+dx,b+dy) in patch for a,b in oriented):
                    continue
                cells = frozenset((a+dx, b+dy) for a,b in oriented)
                if cells not in seen:
                    seen[cells] = Xform(sym.a,sym.b,sym.c0+dx,sym.d,sym.e,sym.f0+dy)
    return list(seen.items())

class CoverSearch:
    """Exact disjoint set-packing feasibility, with an uncovered-cell budget.
    Bitsets track full-tile conflicts, not only required-cell overlap.
    A timeout is UNKNOWN. Exhaustion proves only this fixed-boundary relaxation.
    Hole-free acceptance is an optional leaf predicate; exhaustion with that
    predicate is not a general Heesch upper bound.
    """
    def __init__(self, universe, required):
        self.universe=universe; self.required=sorted(required)
        self.cover=[0]*len(self.required); self.masks=[]
        owners={}
        for i,(cells,_) in enumerate(universe):
            bit=1<<i; mask=0
            for j,c in enumerate(self.required):
                if c in cells: self.cover[j]|=bit; mask|=1<<j
            self.masks.append(mask)
            for c in cells: owners[c]=owners.get(c,0)|bit
        self.conflicts=[]
        for cells,_ in universe:
            mask=0
            for c in cells: mask|=owners[c]
            self.conflicts.append(mask)

    def solve(self, budget, seconds, accept=None, preferred=(), required_mask=None):
        self.nodes=0; self.leaves=0; deadline=time.monotonic()+seconds
        preferred=set(preferred); failed=set(); result=None
        def walk(todo, available, left, chosen):
            nonlocal result
            self.nodes+=1
            if time.monotonic()>deadline: raise TimeoutError
            if not todo:
                self.leaves+=1
                if accept is None or accept(chosen): result=chosen; return True
                return False
            key=(todo, available, left)
            # Predicate may depend on previously occupied off-boundary cells.
            if accept is None and key in failed: return False
            scan=todo; target=None; options=0; count=10**9; forced=0
            while scan:
                b=scan & -scan; scan-=b; j=b.bit_length()-1
                opts=self.cover[j]&available; n=opts.bit_count()
                if n==0: forced|=b
                elif n<count: target=b; options=opts; count=n
            if forced:
                n=forced.bit_count()
                if n>left: return False
                return walk(todo ^ forced, available, left-n, chosen)
            ids=[]
            while options:
                b=options & -options; options-=b; ids.append(b.bit_length()-1)
            ids.sort(key=lambda i:(i not in preferred,-(self.masks[i]&todo).bit_count(),i))
            for i in ids:
                if walk(todo & ~self.masks[i], available & ~self.conflicts[i],left,chosen+(i,)):
                    return True
            if left and walk(todo ^ target,available & ~self.cover[target.bit_length()-1],left-1,chosen):
                return True
            if accept is None and len(failed)<200000: failed.add(key)
            return False
        try:
            todo=(1<<len(self.required))-1 if required_mask is None else required_mask
            ok=walk(todo,(1<<len(self.universe))-1,budget,())
            status='SAT' if ok else 'EXHAUSTED'
        except TimeoutError: status='UNKNOWN_TIMEOUT'
        return {'status':status,'nodes':self.nodes,'leaves':self.leaves,'selected':result}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--seconds',type=float,default=30)
    ap.add_argument('--budget',type=int,default=2); args=ap.parse_args()
    source=LAB/'baseline.heesch'; text=source.read_text()
    w=verify_witness(text); sub=w.submission; patch=w.hc_corona.patch_cells
    required=required_set(patch,w.contact); universe=placements(sub.cells,sub.grid,patch,required)
    engine=CoverSearch(universe,required)
    current={xf.apply_all(sub.cells) for _,xf in sub.defect.tiles}
    preferred=[i for i,(cells,_) in enumerate(universe) if cells in current]
    def accept(ids):
        block=DefectBlock(5,args.budget,args.budget,len(required),tuple((5,universe[i][1]) for i in ids))
        try: verify_defect(sub.cells,sub.grid,w.hc_corona,block,w.contact); return True
        except Exception as e:
            from heesch_verify.result import VerifyError
            if isinstance(e,VerifyError): return False
            raise
    start=time.monotonic()
    result=engine.solve(args.budget,args.seconds,accept,preferred)
    result.update(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        required_cells=len(required),candidate_placements=len(universe),budget=args.budget,
        elapsed_seconds=time.monotonic()-start,proof_gate_run=False,
        scope='Entire fifth-ring placement universe with the four inner rings fixed')
    if result['selected'] is not None:
        ids=result['selected']
        body=text.split('#DEFECT')[0]+f'#DEFECT 5 {args.budget} {args.budget} {len(required)}\n{len(ids)}\n'
        body+=''.join('5 '+universe[i][1].as_text()+'\n' for i in ids)
        body+='#PROOF'+text.split('#PROOF',1)[1]
        (LAB/'results/candidate.heesch').write_text(body)
    (LAB/f'results/fixed-ring-budget-{args.budget}.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__': main()
