"""Recheck all saved geometry and periodic tiling certificates from their cells."""
import json
from search import LAB,verify_witness
from heesch_verify.defect import verify_defect
from heesch_verify.grids import GRIDS
checked=0
for p in sorted((LAB/'results').rglob('*.heesch')):
    w=verify_witness(p.read_text()); sub=w.submission
    if sub.defect: verify_defect(sub.cells,sub.grid,w.hc_corona,sub.defect,w.contact)
    checked+=1
shapes={r['id']:r for r in json.loads((LAB/'results/shape-frontier.json').read_text())['candidates']}
for p in (LAB/'results').glob('paired-growth-*.json'):
    shapes.update({r['id']:r for r in json.loads(p.read_text())['records']})
mutation_path=LAB/'results/template-mutation.json'
if mutation_path.exists():
    shapes.update({r['id']:r for r in json.loads(mutation_path.read_text())['records']})
tilings=0
evidence=[]
for name in ('repair-regrow.json','repair-periodic.json'):
    path=LAB/'results'/name
    if path.exists():
        for row in json.loads(path.read_text())['records']:
            shapes[row['canonical_digest']]=row
            evidence.append((row['canonical_digest'],row.get('periodic_search',{}).get('certificate')))
inverse_path=LAB/'results/inverse-patch-design.json'
if inverse_path.exists():
    for experiment in json.loads(inverse_path.read_text())['records']:
        for row in experiment['candidates']:
            shapes[row['canonical_digest']]=row
            evidence.append((row['canonical_digest'],row['periodic_search']['certificate']))
for p in (LAB/'results').glob('discussion75-followup-*.json'):
    for row in json.loads(p.read_text())['records']:
        shapes[row['canonical_digest']]=row
refinement_path=LAB/'results/discussion75-refinement.json'
for p in (LAB/'results').glob('discussion75-refined-*.json'):
    for row in json.loads(p.read_text())['records']:
        shapes[row['canonical_digest']]=row
        evidence.append((row['canonical_digest'],row['periodic_search']['certificate']))
for p in (LAB/'results').glob('discussion75-periodic-*.json'):
    for row in json.loads(p.read_text())['records']:
        shapes[row['canonical_digest']]=row
        evidence.append((row['canonical_digest'],row['certificate']))
if refinement_path.exists():
    row=json.loads(refinement_path.read_text())
    evidence.append((row['canonical_digest'],row['periodic_search']['certificate']))
for name in ('periodic-filter.json','refined-leads.json','swap-refinement.json','queue-periodic.json'):
    p=LAB/'results'/name
    if p.exists():
        for row in json.loads(p.read_text())['records']:
            evidence.append((row['id'],row.get('certificate') or row.get('periodic_search',{}).get('certificate')))
for identity,row in shapes.items():
    for field in ('tiling_search','periodic_search'):
        if row.get(field,{}).get('certificate'): evidence.append((identity,row[field]['certificate']))
seen=set()
for id,cert in evidence:
    if cert is None: continue
    key=(id,json.dumps(cert,sort_keys=True))
    if key in seen: continue
    seen.add(key)
    shape=shapes[id]['cells']; (a,zero),(b,d)=cert['lattice_basis']; assert zero==0
    occupied=set()
    for orientation,dx,dy in cert['placements']:
        sym=GRIDS['H'].orientations[orientation]; residues=set()
        for cell in shape:
            x,y=sym.apply(cell); x+=dx; y+=dy
            residues.add(((x-b*(y//d))%a,y%d))
        assert len(residues)==len(shape) and not occupied&residues
        occupied|=residues
    assert occupied=={(x,y) for x in range(a) for y in range(d)}
    tilings+=1
out={'geometry_artifacts_verified':checked,'periodic_certificates_rechecked':tilings,
    'official_non_tiler_proof_gate_run':False}
(LAB/'results/artifact-check.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
