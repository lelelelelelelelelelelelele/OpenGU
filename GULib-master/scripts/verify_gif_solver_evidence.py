"""Read-only local/SSH verification of AAGU-052's completed evidence."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import xml.etree.ElementTree as ET


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--item',type=Path,required=True)
    p.add_argument('--ssh-host',required=True)
    p.add_argument('--ssh-root',required=True)
    args=p.parse_args();ev=args.item/'evidence'
    read=lambda path:json.loads(path.read_text(encoding='utf-8-sig'))
    sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
    run=lambda *cmd:subprocess.check_output(cmd,cwd=args.repo,text=True).strip()
    candidate=run('git','rev-parse','HEAD')
    assert not run('git','status','--porcelain','--untracked-files=all')
    compared=read(ev/'compare-v1.json');confirmed=read(ev/'confirm-v1.json')
    assert compared['finished'] and confirmed['finished']
    assert len(compared['cells'])==18 and len(confirmed['cells'])==2
    assert all(row['producer']==read(ev/'local-producer.json') for row in confirmed['cells'])
    assert all(row['graph_matches_declared_deletion'] and row['matched_residual']<=1e-3
               for row in compared['cells'] if row['arm']=='full-shift20')
    assert all(row['solver']['relative_residual']<=1e-3 and row['status']=='converged' for row in confirmed['cells'])
    assert all(row['state_hash']==compared['checkpoint']['state_hash'] for row in compared['cells'] if row['status']=='rejected')
    remote_code='''import hashlib,json,subprocess
from pathlib import Path
root=Path(ROOT)
base=root/'results/diagnostics/AAGU-052'
hash_file=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
checks={}
def check(path,expected=None):
    p=Path(path);value=hash_file(p)
    if expected is not None:assert value==expected,str(p)
    checks[str(p)]=value
for folder in ['source-curvature-v1','source-curvature-v2','source-updates-v1','source-confirm-v1']:
    manifest=read(base/folder/'manifest.json')
    check(base/folder/'manifest.json')
    for name,expected in manifest['files'].items():check(base/folder/name,expected)
previous=read(base/'source-updates-v1/stress50-v1.json')
for entry in previous['files']:check(entry['path'],entry['sha256'])
check(previous['checkpoint']['path'],previous['checkpoint']['file_sha256'])
check(root/previous['dataset_input']['graph'],previous['dataset_input']['graph_sha256'])
check(root/previous['dataset_input']['manifest'],previous['dataset_input']['instance']['artifacts']['manifest_sha256'])
for folder in ['curvature-v2','updates-v1','compare-v1','confirm-v1']:
    check(base/folder/'result.json')
compared=read(base/'compare-v1/result.json');confirmed=read(base/'confirm-v1/result.json')
assert compared['finished'] and confirmed['finished']
for row in compared['cells']:check(row['saved_file']['path'],row['saved_file']['sha256'])
for row in compared['retrain']:
    if 'path' in row['provenance']:check(row['provenance']['path'],row['provenance']['sha256'])
for row in confirmed['cells']:
    check(row['checkpoint']['path'],row['checkpoint']['file_sha256'])
    check(row['file']['path'],row['file']['sha256'])
for key in ['run','retrain_run']:check(confirmed[key]['path'],confirmed[key]['sha256'])
head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
dirty=subprocess.check_output(['git','-C',str(root),'status','--porcelain','--untracked-files=no'],text=True).strip()
assert head=='77858b6549929450dfff622b613012e7c51a4e63' and not dirty
print(json.dumps(dict(ssh_sha=head,tracked_clean=not dirty,files=checks)))
'''.replace('ROOT',repr(args.ssh_root))
    command=['ssh','-o','BatchMode=yes',args.ssh_host,
             'cd '+shlex.quote(args.ssh_root)+' && /root/miniconda3/bin/python -B -']
    execution=subprocess.run(command,input=remote_code,text=True,capture_output=True,check=True)
    remote=json.loads(execution.stdout)
    (ev/'remote-verification.json').write_text(json.dumps(remote,indent=2),encoding='utf-8')
    remote_base=args.ssh_root+'/results/diagnostics/AAGU-052/'
    for local,folder in [('curvature-v2.json','curvature-v2'),('updates-v1.json','updates-v1'),('compare-v1.json','compare-v1'),('confirm-v1.json','confirm-v1')]:
        assert sha(ev/local)==remote['files'][remote_base+folder+'/result.json']
    # Reproduce the original edge-index failure using its exact historical body.
    import numpy as np
    import torch
    old_source=run('git','show','8f4702bb212d565bcbfd0ef78c83138c1419e2eb:GULib-master/unlearning/unlearning_methods/GIF/gif.py')
    klass=next(n for n in ast.parse(old_source).body if isinstance(n,ast.ClassDef) and n.name=='gif')
    function=next(n for n in klass.body if isinstance(n,ast.FunctionDef) and n.name=='update_edge_index_unlearn')
    namespace={'np':np,'torch':torch};exec(compile(ast.Module(body=[function],type_ignores=[]),'historical-gif','exec'),namespace)
    from types import SimpleNamespace
    edges=torch.tensor([[0,1,1,2,2,3,3,0],[1,0,2,1,3,2,0,3]])
    expected=edges[:,~(edges==1).any(0)]
    actual=namespace['update_edge_index_unlearn'](SimpleNamespace(args={'unlearn_task':'node'},data=SimpleNamespace(edge_index=edges)),[1])
    assert not torch.equal(actual,expected)
    before=dict(source='8f4702bb:GIF.update_edge_index_unlearn',actual=actual.tolist(),expected=expected.tolist(),status='FAIL as expected')
    (ev/'regression-before.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
    passed=set()
    for name in ['cpu-verification.xml','cpu-corrected-fixtures.xml','cpu-final-targeted.xml']:
        for case in ET.parse(ev/name).iter('testcase'):
            if case.find('failure') is None and case.find('error') is None:
                passed.add((case.attrib['classname'],case.attrib['name']))
    assert len(passed)==50,len(passed)
    # Real GPU evidence may be reused only while production bytes are identical.
    for name,path in [('gif.py','unlearning/unlearning_methods/GIF/gif.py'),('solver.py','unlearning/unlearning_methods/GIF/solver.py'),('modular_gu.py','experiments/modular_gu.py')]:
        assert sha(args.repo/path)==read(ev/'source-updates-v1/manifest.json')['files'][name]
        assert sha(args.repo/path)==read(ev/'source-confirm-v1/manifest.json')['files'][name]
    manifest=dict(candidate=candidate,authority_item=str(args.item),
                  source_checkpoints=['7122ba70fb2d9ae339d4f51e6f1f95b0f765dfe6','57ea01a4fe1a47291205103abaabe074f3897633'],
                  dependency_candidate='47282e6eee6172e1c6e6bdb1ceec76fda15d6cb5',
                  dataset=compared['dataset_input'],checkpoint=compared['checkpoint'],
                  producer=read(ev/'local-producer.json'),remote_files=remote['files'],
                  local_evidence={p.name:sha(p) for p in ev.iterdir() if p.is_file() and p.suffix in ('.json','.xml')
                                  and p.name not in ('input-output-manifest.json','final-verification.json')})
    (ev/'input-output-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    verification=dict(candidate=candidate,status='PASS for scoped software and diagnostic delivery',
                      scientific_effectiveness='NOT CONFIRMED',unique_cpu_tests=len(passed),
                      core_updates=18,confirmation_updates=2,new_retrain=1,
                      remote_files_verified=len(remote['files']),remote_tracked_clean=True,local_clean=True,
                      checked_source_reuse='Production files byte-identical to both tested GPU bundles; later changes are diagnostic/report/test only.',
                      human_acceptance='pending')
    (ev/'final-verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
    print(json.dumps(verification,indent=2))


if __name__=='__main__':main()
