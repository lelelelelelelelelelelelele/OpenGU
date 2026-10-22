"""Bounded sampler and actual pre-change cache consumption on disposable CPU data."""
import ast
from contextlib import contextmanager
import copy
import functools
import hashlib
import json
from pathlib import Path
import pickle
import subprocess
import tempfile

import numpy as np
import pytest
import torch
from torch_geometric.data import Data

from test_modular_consumers import tables, run, write_yaml
from experiments.modular_config import unlearning
from experiments.modular_gu import gu_producer
from experiments.checkpoint_references import ensemble_identity
from experiments.node_deletion import retained_graph
from utils.target_checkpoint import data_identity, sha256_file


ROOT = Path(__file__).resolve().parents[1]
BASELINE = '8fb8169475b015ac4cc6dd1a61c6d26ee5ff7670'
OLD = {
    'GraphEraser': ('112176d596f8b929d0f4bce628effcc0c852cefe9b74286e66f0fdd14029322d',
                    '8d5f54e8dfdec6e3b91b2e170a5779914426215dceaf75ba8ac3cdc15cd7eb8f'),
    'GraphRevoker': ('7398f295ca630567f7a60b81c5b8bad7162bb084df7fe420975be310ddd13680',
                     'e4d5310092d569bc1e20626c62662096e5413d521b465ef778ea79fc05e038dd'),
}


def lane(method):
    import experiments.modular_shards as shards
    import experiments.modular_graphrevoker as revoker
    return (shards, 'aggregate_weights', 'prepare_ensemble', 'initial_ensemble') if method == 'GraphEraser' else (
        revoker, 'graphrevoker_weights', 'prepare_graphrevoker_ensemble', 'initial_graphrevoker_ensemble')


@contextmanager
def baseline_sampler(method, monkeypatch):
    """Load the exact committed function, retaining its name and real source hash.

    Only the sampler changed in each production module. The source fixture stays
    inside ROOT so the real fingerprint traversal includes it; no fake hashes or
    patched cache registry are used. Temporary source is removed on exit.
    """
    module, name, _, _ = lane(method)
    relative = Path(module.__file__).relative_to(ROOT).as_posix()
    source = subprocess.check_output(['git', 'show', BASELINE + ':GULib-master/' + relative],
                                     cwd=ROOT, text=True, encoding='utf-8')
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name)
    source = ''.join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])
    fixture_root = ROOT / '.pytest_cache'
    fixture_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='aagu102-source-', dir=str(fixture_root)) as directory:
        path = Path(directory) / 'baseline_sampler.py'
        path.write_text(source, encoding='utf-8')
        namespace = dict(vars(module))
        exec(compile(source, str(path), 'exec'), namespace)
        with monkeypatch.context() as patch:
            patch.setattr(module, name, namespace[name])
            yield namespace[name]


def sample_data(remaining):
    # Interleaved held-out nodes and seven genuinely deleted training nodes.
    n = 2 * (remaining + 7) + 4
    ids = torch.arange(n)
    train = (ids % 2 == 0) & (ids < 2 * (remaining + 7))
    edges = torch.stack([ids[:-1], ids[1:]])
    data = Data(x=torch.stack([ids.float(), torch.sin(ids.float()), torch.cos(ids.float())], 1),
                y=ids % 3, edge_index=torch.cat([edges, edges.flip(0)], 1), train_mask=train,
                val_mask=(~train) & (ids % 3 == 0), test_mask=(~train) & (ids % 3 != 0))
    deleted = data.train_mask.nonzero().flatten()[:7].tolist()
    return retained_graph(data, deleted), deleted


class RecordingModel(torch.nn.Module):
    def __init__(self, shift):
        super().__init__()
        self.shift = shift
        self.seen = None

    def forward(self, x, edges):
        self.seen = x[:, 0].long().clone()
        return torch.stack([torch.sin(x[:, 0] + self.shift), x[:, 1], x[:, 2]], 1)


def sample_run(function, data, count=1000):
    from types import SimpleNamespace
    torch.set_num_threads(1)
    torch.manual_seed(42)
    np.random.seed(42)
    models = [RecordingModel(0), RecordingModel(1)]
    weights = function(SimpleNamespace(shard_models=models), data,
                       dict(num_shards=2, num_opt_samples=count, opt_num_epochs=2, opt_lr=.01))
    return weights, models[0].seen, np.random.random(5), torch.rand(5)


@pytest.mark.parametrize('method', OLD)
@pytest.mark.parametrize('remaining', [1100, 1000, 948, 1])
def test_retained_pool_and_real_optimization(method, remaining, caplog):
    data, deleted = sample_data(remaining)
    module, name, _, _ = lane(method)
    with caplog.at_level('INFO'):
        weights, sampled, _, _ = sample_run(getattr(module, name), data)
    assert len(sampled) == min(1000, remaining)
    assert sampled.unique().numel() == len(sampled)
    assert data.train_mask[sampled].all()
    assert not set(sampled.tolist()) & set(deleted)
    assert torch.isfinite(weights).all() and (weights >= 0).all()
    assert weights.sum().item() == pytest.approx(1.)
    assert 'configured=1000 retained=%s actual=%s' % (remaining, min(remaining, 1000)) in caplog.text
    if remaining <= 1000:
        assert torch.equal(sampled, data.train_mask.nonzero().flatten())


@pytest.mark.parametrize('method', OLD)
@pytest.mark.parametrize('remaining,count', [(1100,1000), (1000,1000), (29,1), (29,10000), (29,9)])
def test_successful_old_domain_is_bitwise_equal_including_rng(method, remaining, count, monkeypatch):
    data, _ = sample_data(remaining)
    module, name, _, _ = lane(method)
    current = sample_run(getattr(module, name), data, count)
    with baseline_sampler(method, monkeypatch) as old:
        previous = sample_run(old, data, count)
    for a,b in zip(current,previous):
        np.testing.assert_array_equal(a,b)


@pytest.mark.parametrize('method', OLD)
def test_old_infeasible_and_empty_pool_guards(method, monkeypatch):
    from experiments.effective_config import ConfigurationError
    data, _ = sample_data(948)
    with baseline_sampler(method, monkeypatch) as old:
        with pytest.raises(ConfigurationError, match='exceeds retained'):
            sample_run(old, data)
    data.train_mask[:] = False
    module, name, _, _ = lane(method)
    with pytest.raises(ConfigurationError, match='requires retained'):
        sample_run(getattr(module, name), data)


def large_tables(tables, method):
    root = tables[0]
    torch.manual_seed(7)
    n = 1120
    ids = torch.arange(n)
    edges = torch.stack([ids, (ids + 1) % n])
    data = Data(x=torch.randn(n,3), y=ids % 2,
                edge_index=torch.cat([edges,edges.flip(0)],1),
                train_mask=ids<1100, val_mask=(ids>=1100)&(ids<1110), test_mask=ids>=1110)
    (root/'graph.pkl').write_bytes(pickle.dumps(data))
    manifest=json.loads((root/'dataset.json').read_text(encoding='utf-8'))
    manifest.update(data_sha256=sha256_file(root/'graph.pkl'),data_identity=data_identity(data))
    (root/'dataset.json').write_text(json.dumps(manifest),encoding='utf-8')
    import yaml
    dataset=yaml.safe_load((root/'dataset.yaml').read_text(encoding='utf-8'))
    dataset['artifacts'].update(manifest_sha256=sha256_file(root/'dataset.json'),split_hash=data_identity(data)['split_hash'])
    write_yaml(root/'dataset.yaml',dataset)
    parameters=dict(shard_epochs=2,num_shards=2,opt_num_epochs=1,num_opt_samples=1000)
    if method=='GraphRevoker':
        parameters.update(gpa_epochs=1,gpa_hidden_channels=8,gpa_batch_size=256)
    value=dict(kind='unlearning',schema_version=1,method=method,
               training={'epochs':1},parameters=parameters)
    write_yaml(root/'method.yaml',value)
    return data,unlearning(value),dict(stage='unlearning',selector_refs=['degree.yaml'],unlearning_refs=['method.yaml'])


def forbid(patch, module, name):
    original = getattr(module, name)
    @functools.wraps(original)
    def forbidden(*args, **kwargs):
        raise AssertionError('HIT called ' + module.__name__ + '.' + name)
    patch.setattr(module,name,forbidden)


def cache_files(root):
    paths=[]
    for directory in (root/'checkpoints',root/'results/cache_v2',root/'results/runtime/modular/checkpoints'):
        paths.extend(p for p in directory.rglob('*') if p.is_file())
    return {str(p.relative_to(root)):(hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_mtime_ns) for p in paths}


@pytest.mark.parametrize('method', OLD)
def test_old_cap_sources_do_not_alias_new_training_semantics(tables, method):
    from cache_v2.source_compatibility import source_candidates, checkpoint_candidates
    data, instance, _ = large_tables(tables, method)
    current = gu_producer(method, instance['model'])
    candidates = list(source_candidates('prediction', method,
        {'model': instance['model'], 'semantic_version': current.semantic_version},
        {'source_fingerprint': current.source_fingerprint}))
    assert {'source_fingerprint': OLD[method][0]} not in candidates
    metadata = ensemble_identity(instance, data)
    assert all(c['implementation'] != OLD[method][1]
               for c in checkpoint_candidates(metadata, 'ensemble_checkpoint'))


@pytest.mark.parametrize('method', OLD)
def test_new_small_pool_full_lane_cold_warm_and_changed_inputs(tables, method, monkeypatch):
    # Small real graph, all phases including partition, shard retraining and persistence.
    root=tables[0]
    parameters=dict(shard_epochs=2,num_shards=2,opt_num_epochs=1,num_opt_samples=1000)
    if method=='GraphRevoker':
        parameters.update(gpa_epochs=1,gpa_hidden_channels=8,gpa_batch_size=64)
    value=dict(kind='unlearning',schema_version=1,method=method,model={'hidden_channels':4},
               training={'epochs':2},parameters=parameters)
    write_yaml(root/'method.yaml',value)
    options=dict(stage='unlearning',selector_refs=['degree.yaml'],unlearning_refs=['method.yaml'])
    cold=run(tables,'capped_cold',**options)['unlearning'][0]
    warm=run(tables,'capped_warm',**options)['unlearning'][0]
    assert cold['producer_called'] and warm['hit'] and not warm['producer_called']
    assert cold['output']==warm['output']
    value['parameters']['opt_lr']=.0123
    write_yaml(root/'method.yaml',value)
    changed=run(tables,'changed_optimizer',**options)['unlearning'][0]
    assert changed['producer_called'] and not changed['ensemble_preparation']['hit']
    assert changed['output']!=cold['output']


@pytest.mark.parametrize('method', OLD)
@pytest.mark.parametrize('fault', ['invalid', 'conflict', 'corrupt_payload'])
def test_current_output_errors_are_not_normal_misses(tables, method, fault, monkeypatch):
    from cache_v2 import CacheIndex, ArtifactConflictRecord, ArtifactType
    from cache_v2.store import ArtifactIntegrityError
    from experiments.unlearning_outputs import load_output
    import experiments.modular_run as runner
    root=tables[0]
    _,_,options=large_tables(tables,method)
    old=run(tables,'current_for_fault',**options)['unlearning'][0]
    store=root/'results/cache_v2'
    index=CacheIndex(store/'index.sqlite')
    record=index.get_artifact(old['artifact_id'])
    if fault=='invalid':
        with index.transaction() as writer:
            writer.connection.execute("UPDATE artifacts SET status='invalid' WHERE artifact_id=?",(old['artifact_id'],))
    elif fault=='conflict':
        index.record_conflict(ArtifactConflictRecord(artifact_type=ArtifactType.PREDICTION,
            recipe_hash=old['recipe_hash'],existing_artifact_id=old['artifact_id'],
            existing_content_hash=old['content_hash'],observed_content_hash='0'*64))
    else:
        (store/record['semantic_path']).write_bytes(b'corrupt output')
        # Explicit payload consumption, not an Evaluation HIT that needs no arrays.
        with pytest.raises(ArtifactIntegrityError):
            load_output(old['output'],store,dataset_root=root)
        return
    forbid(monkeypatch,runner,'prepare_model')
    with pytest.raises(ValueError,match='Output lookup failed closed'):
        run(tables,'new_reads_fault',**options)


@pytest.mark.parametrize('method', OLD)
def test_half_deletion_retrains_shards_and_aggregates_948_nodes(method, caplog):
    from attack.cache_identity import seeded_execution
    from experiments.modular_shards import run_grapheraser
    from experiments.modular_graphrevoker import run_graphrevoker
    torch.set_num_threads(1)
    torch.manual_seed(7)
    n=1905
    ids=torch.arange(n)
    edges=torch.stack([ids,(ids+1)%n])
    data=Data(x=torch.randn(n,3),y=ids%2,edge_index=torch.cat([edges,edges.flip(0)],1),
              train_mask=ids<1895,val_mask=(ids>=1895)&(ids<1900),test_mask=ids>=1900)
    parameters=dict(shard_epochs=2,num_shards=2,opt_num_epochs=1,num_opt_samples=1000)
    if method=='GraphRevoker':
        parameters.update(gpa_epochs=1,gpa_hidden_channels=8,gpa_batch_size=256)
    instance=unlearning(dict(kind='unlearning',schema_version=1,method=method,
        model={'hidden_channels':4},training={'epochs':1},parameters=parameters))
    module,_,_,initial=lane(method)
    with seeded_execution(42):
        ensemble=getattr(module,initial)(instance,data)
    # A controlled request isolates aggregation from the separate empty-shard issue.
    groups=[(ensemble.assignment==i).nonzero().flatten().tolist() for i in range(2)]
    selected=[node for group in groups for node in group[:len(group)//2]]
    assert len(selected)==947
    assert int(retained_graph(data,selected).train_mask.sum())==948
    with seeded_execution(42),caplog.at_level('INFO'):
        after,before,_=(run_grapheraser if method=='GraphEraser' else run_graphrevoker)(instance,data,selected,ensemble)
    assert 'configured=1000 retained=948 actual=948' in caplog.text
    assert before.shape==(n,2)
    assert torch.isfinite(after(data.x,data.edge_index)).all()
    assert after.weights.sum().item()==pytest.approx(1.)
