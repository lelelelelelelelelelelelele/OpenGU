"""Obtain dataset counts from the bound persisted graph, never operator input."""
import json
from pathlib import Path
import shlex
import subprocess


def requests_for(config, root):
    root = Path(root).resolve()
    requests = []
    for instance, directory in zip(config['datasets'], config['dataset_directories']):
        manifest = (Path(directory) / instance['artifacts']['manifest']).resolve()
        relative = manifest.relative_to(root).as_posix()
        requests.append({'instance': instance, 'manifest': relative})
    return requests


def read_counts(requests, root):
    from experiments.dataset_inputs import read_dataset, input_path
    import copy
    counts = []
    for request in requests:
        path = input_path(root, request['manifest'])
        instance = copy.deepcopy(request['instance'])
        instance['artifacts']['manifest'] = path.name
        # Validates manifest SHA, graph SHA, actual split/masks and input identity.
        _, inputs = read_dataset(instance, path.parent)
        counts.append({'num_nodes': inputs.num_nodes, 'candidate_count': inputs.candidate_count})
    return counts


REMOTE_READER = '''import json,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root))
requests=json.load(sys.stdin)
from experiments.dataset_inputs import read_dataset,input_path
counts=[]
for request in requests:
    path=input_path(root,request['manifest'])
    instance=request['instance']
    instance['artifacts']['manifest']=path.name
    _,inputs=read_dataset(instance,path.parent)
    counts.append({'num_nodes':inputs.num_nodes,'candidate_count':inputs.candidate_count})
print(json.dumps(counts))
'''


def dataset_counts(config, root, *, node=None, device_file=None):
    requests = requests_for(config, root)
    if node is None:
        return read_counts(requests, root)
    from syncmate_core import context, devices
    with context.use(Path(root)):
        device, warnings = devices.load_device(Path(device_file))
    if warnings:
        raise ValueError('; '.join(warnings))
    peer = device.get('peers', {}).get(node)
    if not peer or peer.get('role') not in ('runner', 'runner+collector'):
        raise ValueError('dataset source must be a configured runner')
    if devices.peer_uses_local_transport(peer):
        return read_counts(requests, peer['repo_path'])
    command = shlex.join([devices.peer_python_executable(peer), '-B', '-c', REMOTE_READER, peer['repo_path']])
    result = subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=20',
                             '--', peer['ssh'], command], input=json.dumps(requests),
                            capture_output=True, text=True, encoding='utf-8', timeout=180)
    if result.returncode:
        raise ValueError('bound dataset evidence unavailable on runner: ' + result.stderr[-1500:])
    try:
        counts = json.loads(result.stdout)
    except ValueError as exc:
        raise ValueError('dataset reader did not return valid counts') from exc
    if not isinstance(counts, list) or len(counts) != len(requests):
        raise ValueError('dataset reader returned a different dataset count')
    return counts
