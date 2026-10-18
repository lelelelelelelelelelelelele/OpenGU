"""Read-only CPU diagnostic, supplied with AUDIT from before_audit.json on stdin.

No training, optimizer, cache writes or replacement of formal metrics.
"""
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import zipfile

ROOT = Path('/autodl-fs/data/OpenGU/GULib-master')
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
import numpy as np
import torch
torch.set_num_threads(2)
from experiments.dataset_inputs import resolve_input
from experiments.modular_model import create_model
from experiments.modular_shards import ShardEnsemble
from utils.target_checkpoint import load_weights, data_identity

store = ROOT / 'results/cache_v2'
con = sqlite3.connect((store / 'index.sqlite').as_uri() + '?mode=ro', uri=True)
con.row_factory = sqlite3.Row
rows = []
data = None
for previous in AUDIT['records']:
    if previous['dataset'] != 'Cora':
        continue
    ref = previous['output']
    db = dict(con.execute('select * from artifacts where artifact_id=?', (ref['artifact_id'],)).fetchone())
    assert db['status'] == 'valid' and db['verification_status'] == 'verified'
    assert all(db[k] == v for k, v in ref.items())
    artifact = store / db['semantic_path']
    assert artifact.resolve().is_relative_to(store.resolve())
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == ref['content_hash']
    with zipfile.ZipFile(artifact) as z:
        identity = json.loads(z.read('metadata.json'))['identity']
        before = np.load(io.BytesIO(z.read('arrays__logits_before.npy')), allow_pickle=False)
    if data is None:
        data = resolve_input(identity['dataset_input'], ROOT).cpu()
    assert data_identity(data) == identity['pairing']['data_identity']
    cp = Path(previous['checkpoint'])
    assert cp.resolve().is_relative_to((ROOT / 'results/runtime/modular/checkpoints').resolve())
    loaded = load_weights(cp)
    assert loaded['state_hash'] == previous['initial_ensemble_state_hash']
    assert loaded['file_sha256'] == previous['checkpoint_file_sha256']
    state = loaded['state_dict']
    w = state['weights']
    ensemble = ShardEnsemble([create_model(previous['checkpoint_metadata']['model'], 'shard', data, torch.device('cpu')) for _ in w], state['assignment'], w)
    ensemble.load_state_dict({k:v for k,v in state.items() if k in ['assignment','weights'] or k.startswith('shard_models.')}, strict=True)
    ensemble.eval()
    def acc(logits):
        return float((logits[data.test_mask].argmax(-1) == data.y[data.test_mask]).float().mean()) * 100
    with torch.inference_mode():
        logp = torch.stack(ensemble.shard_predictions(data.x, data.edge_index))
        formal = (w[:, None, None] * logp).sum(0)
        assert np.array_equal(formal[data.test_mask].argmax(-1).numpy(), before[data.test_mask.numpy()].argmax(-1))
        weighted_prob = (w[:, None, None] * logp.exp()).sum(0)
        uniform_prob = logp.exp().mean(0)
    counts = [torch.bincount(data.y[data.train_mask & (state['assignment'] == i)], minlength=int(data.y.max())+1).tolist() for i in range(len(w))]
    shard_info = []
    for i, c in enumerate(counts):
        p = np.array(c, dtype=float) / sum(c)
        shard_info.append(dict(shard=i, train_nodes=sum(c), class_counts=c,
            represented_classes=int(np.count_nonzero(c)), dominant_class_fraction=float(max(p)),
            label_entropy=float(-(p[p>0]*np.log(p[p>0])).sum()), weight=float(w[i]),
            test_accuracy=acc(logp[i])))
    row = dict(method=previous['method'], seed=previous['seed'], output=ref,
        checkpoint_state_hash=loaded['state_hash'], checkpoint_file_sha256=loaded['file_sha256'],
        formal_before=acc(formal), diagnostic_weighted_probability=acc(weighted_prob),
        diagnostic_uniform_probability=acc(uniform_prob), shards=shard_info)
    rows.append(row)
    print('checked', row['method'], row['seed'], file=sys.stderr, flush=True)
assert len(rows) == 20
print(json.dumps(dict(read_only=True, new_training_runs=0, cpu_threads=2,
    current_remote_sha=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
    original_execution_sha=AUDIT['execution_sha'], data_identity=data_identity(data),
    interpretation='Alternative pools are diagnostics, not validated replacements for formal metrics.',
    records=rows), indent=2))
