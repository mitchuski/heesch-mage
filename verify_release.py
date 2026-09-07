"""Check release hashes and explicit periodic partitions; requires upstream verifier."""
import hashlib
import json
from pathlib import Path
from heesch_verify.canonical import canonical_digest
from heesch_verify.grids import GRIDS

ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'MANIFEST.json').read_text())
for name,expected in manifest.items():
    path=ROOT/name
    assert path.resolve().is_relative_to(ROOT.resolve())
    assert hashlib.sha256(path.read_bytes()).hexdigest()==expected, name

def check(row):
    shape=row['cells']; grid=GRIDS['H']
    assert canonical_digest(shape,grid,True)==row['canonical_digest']
    cert=row.get('certificate') or row['periodic_search']['certificate']
    (a,z),(b,d)=cert['lattice_basis']; assert z==0 and a>0 and d>0
    occupied=set()
    assert len(cert['placements'])==cert['copies_per_period']
    for orientation,dx,dy in cert['placements']:
        residues=set()
        for cell in shape:
            x,y=grid.orientations[orientation].apply(cell); x+=dx; y+=dy
            residues.add(((x-b*(y//d))%a,y%d))
        assert len(residues)==len(shape) and not residues&occupied
        occupied.update(residues)
    assert occupied=={(x,y) for x in range(a) for y in range(d)}

public=json.loads((ROOT/'public-queue-certificates.json').read_text())['records']
repair=json.loads((ROOT/'research/results/repair-periodic.json').read_text())['records']
assert len(public)==3 and len(repair)==184
assert len({r['canonical_digest'] for r in repair})==184
for row in public+repair: check(row)
print(f'Manifest: {len(manifest)} files; public partitions: {len(public)}; repair partitions: {len(repair)}; all passed.')
