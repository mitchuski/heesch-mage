"""Direct cell-set check of saved center-halo repair examples."""
import json
from coordinated_repair import SOURCE
from search import LAB, verify_witness, required_set
from heesch_verify.transform import Xform

source=verify_witness((LAB/SOURCE).read_text()); poses=source.submission.patches[0]
records=json.loads((LAB/'results/coordinated-repair-center.json').read_text())['records']
checked=0
for row in records:
    example=row['relaxed_center_example']
    if example is None: continue
    removed=set(example['removed']); assert len(removed)==9 and 0 not in removed
    transforms=[xf for i,(_,xf) in enumerate(poses) if i not in removed]
    transforms += [Xform(*map(int,text.split())) for text in example['added']]
    occupied=set()
    for xf in transforms:
        cells={xf.apply(c) for c in row['cells']}
        assert len(cells)==len(row['cells']) and not cells&occupied
        occupied.update(cells)
    central=poses[0][1].apply_all(row['cells'])
    assert required_set(central,source.submission.grid.contact('point'))<=occupied
    checked+=1
out={'center_halo_examples_independently_checked':checked,'full_corona_claimed':False}
(LAB/'results/repair-example-check.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out))
