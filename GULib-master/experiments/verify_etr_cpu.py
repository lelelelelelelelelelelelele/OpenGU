"""Reproducible local ETR parity check against pinned benchmark with explicit eval/float64-intermediate adjustments.

All outputs belong to --root (a new disposable directory). This is software
verification, never a formal experiment or a performance reproduction.
"""
import argparse
import copy
import importlib.util
import inspect
import json
import logging
from pathlib import Path
import pickle
import shutil
import subprocess
import sys
import time
import textwrap
import types

import numpy as np
import torch
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REFERENCE_SHA = '9c95ac387b528967cc1c3aebbd20ce78bcf418c8'
REFERENCE_FILES = {
    'ETRTrainer.py': 'b55bebe00346922d8586582ee93e4975539796e7063e49356ca014bfd90d73a4',
    'etr_utils.py': '76de74a00a48252c3b997190c9f319edc19d79213cd9bc2a6ae407b113c4a365',
    'etr_pipeline.py': '091bd2953af9404809bafdf5045f63ca635549806da27c076e2274dde41af0a4',
}
# Fixed before observing comparison results, for CPU float32 calculations.
ATOL, RTOL = 1e-6, 1e-5


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')


def write_yaml(path, value):
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding='utf-8')


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def snapshot(model):
    return {name: value.detach().cpu().clone() for name, value in model.state_dict().items()}


def compare(left, right):
    if set(left) != set(right):
        raise AssertionError('comparison keys differ')
    maximum = 0.0
    for key in left:
        torch.testing.assert_close(left[key], right[key], atol=ATOL, rtol=RTOL)
        maximum = max(maximum, float((left[key] - right[key]).abs().max()))
    return maximum


def prepare_inputs(root, data_file):
    from utils.target_checkpoint import sha256_file, data_identity
    source = pickle.loads(data_file.read_bytes()).cpu()
    if int(source.num_nodes) != 2708 or source.x.shape[1] != 1433:
        raise ValueError('verification requires the full Cora graph')
    if source.val_mask.any() or int(source.train_mask.sum()) != 2166 or int(source.test_mask.sum()) != 542:
        raise ValueError('expected the explicit legacy Cora 80/0/20 input')
    data = source.clone()
    # Explicit verification-only split: preserve the original 542 test nodes.
    # Hold out 270 of 2166 original training nodes, once, with NumPy seed 2024.
    candidates = np.flatnonzero(source.train_mask.numpy())
    validation = np.random.RandomState(2024).permutation(candidates)[:270]
    data.val_mask[validation] = True
    data.train_mask[validation] = False
    for name in ('train', 'val', 'test'):
        setattr(data, name+'_indices', getattr(data, name+'_mask').nonzero().flatten().numpy())
    # Legacy precomputed training-edge views are not consumed by the ordinary lane.
    for name in ('train_edge_index', 'val_edge_index', 'test_edge_index'):
        if name in data:
            del data[name]
    graph = root/'graph.pkl'
    graph.write_bytes(pickle.dumps(data))
    instance = dict(kind='dataset_split', schema_version=1,
        dataset={'name': 'Cora', 'family': 'Planetoid'},
        preprocessing={'adapter': 'OpenGU_persisted_processed_pair'},
        split=dict(profile='aagu106_local_holdout_seed2024', train_ratio=1896/2708,
                   val_ratio=270/2708, test_ratio=542/2708, seed=2024))
    manifest = {k: instance[k] for k in ('dataset', 'preprocessing', 'split')}
    manifest.update(schema='opengu.persisted_dataset_split', version=1, data_path='graph.pkl',
                    data_sha256=sha256_file(graph), data_identity=data_identity(data))
    write_json(root/'dataset.json', manifest)
    instance['artifacts'] = dict(manifest='dataset.json', manifest_sha256=sha256_file(root/'dataset.json'),
        split_hash=data_identity(data)['split_hash'], node_id_space='pyg-global-node-index-v1')
    write_yaml(root/'dataset.yaml', instance)
    write_json(root/'input-provenance.json', dict(source_path=str(data_file), source_sha256=sha256_file(data_file),
        source_identity=data_identity(source), verification_identity=data_identity(data),
        validation_nodes=validation.tolist(), train_nodes=data.train_indices.tolist(),
        test_nodes=data.test_indices.tolist(), purpose='local software verification only'))
    shared = dict(model={'architecture': 'OpenGU.GCNNet', 'hidden_channels': 64},
                  training=dict(epochs=100, optimizer='Adam', lr=.01, weight_decay=.0005, seed=42))
    write_yaml(root/'etr.yaml', dict(kind='unlearning', schema_version=1, method='ETR', **shared))
    write_yaml(root/'retrain.yaml', dict(kind='unlearning', schema_version=1, method='Retrain', **shared))
    write_yaml(root/'paired.yaml', dict(kind='evaluation', schema_version=1,
                                      case='post_unlearning_utility_and_retrain_gap'))
    for selector, ratio in [('random', .1), ('degree', .05)]:
        write_yaml(root/(selector+'.yaml'), dict(kind='selector', schema_version=1, method=selector,
            candidate={'pool': 'train_mask'}, budget={'mode': 'ratio', 'value': ratio}))
        write_yaml(root/(selector+'-experiment.yaml'), dict(kind='experiment', schema_version=1,
            experiment_id='aagu106-'+selector, stage='unlearning', matrix='cartesian_product',
            dataset_refs=['./dataset.yaml'], selector_refs=['./'+selector+'.yaml'],
            unlearning_refs=['./retrain.yaml', './etr.yaml'], evaluation_refs=['./paired.yaml']))
    return data


def cli(root, selector, run_id, dry=False):
    command = [sys.executable, str(ROOT/'experiments/run.py'), str(root/(selector+'-experiment.yaml'))]
    command += ['--dry_run'] if dry else ['--device', 'cpu', '--verification-root', str(root), '--run-id', run_id]
    started = time.perf_counter()
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    prefix = selector + '-' + ('dry' if dry else run_id)
    (root/(prefix+'.stdout.json')).write_text(result.stdout, encoding='utf-8')
    (root/(prefix+'.stderr.log')).write_text(result.stderr, encoding='utf-8')
    write_json(root/(prefix+'.command.json'), dict(command=command, returncode=result.returncode,
        wall_seconds=time.perf_counter()-started))
    if result.returncode:
        raise RuntimeError('CLI failed; see '+prefix+'.stdout.json and .stderr.log')
    return json.loads(result.stdout)


def reference_run(root, refs, model, data, nodes, label, parameters):
    """Run pinned pipeline/trainer with eval/float64-intermediate and device/path bindings."""
    from experiments.modular_model import runtime_defaults
    from attack.cache_identity import seeded_execution
    runtime_defaults()
    package = types.ModuleType('etr_benchmark_reference')
    package.__path__ = [str(refs)]
    sys.modules[package.__name__] = package
    load_module(package.__name__+'.etr_utils', refs/'etr_utils.py')
    trainer_module = load_module(package.__name__+'.trainer', refs/'ETRTrainer.py')
    pipeline_module = load_module(package.__name__+'.pipeline', refs/'etr_pipeline.py')
    trainer_module.device = torch.device('cpu')
    # Intentional semantic adjustment: the benchmark GCN enables Dropout,
    # while the original author GCN comments it out. Keep its gradient math.
    source = textwrap.dedent(inspect.getsource(trainer_module.ETRTrainer._grad_and_info))
    assert source.count('model.train()') == 1
    namespace = dict(vars(trainer_module))
    source = source.replace('model.train()', 'model.eval()')
    source = source.replace('parameter_importance = self._zerolike(model)',
        'parameter_importance = {name: value.to(torch.float64) for name, value in self._zerolike(model).items()}')
    source = source.replace('p.grad.data.clone().pow(2)', 'p.grad.data.clone().to(torch.float64).pow(2)')
    exec(source, namespace)
    trainer_module.ETRTrainer._grad_and_info = namespace['_grad_and_info']
    erase_source = textwrap.dedent(inspect.getsource(trainer_module.ETRTrainer._modify_weight))
    for mask, value, quantile in [('loc1', 'b1', 'q1'), ('loc2', 'b2', 'q2')]:
        update = 'p[{0}].mul({1}[{0}] / {2})'.format(mask, value, quantile)
        assert erase_source.count(update) == 1
        erase_source = erase_source.replace(update, update + '.to(p.dtype)')
    exec(erase_source, namespace)
    trainer_module.ETRTrainer._modify_weight = namespace['_modify_weight']
    pipeline_module.unlearning_path = str(root/(label+'-request'))
    np.savetxt(pipeline_module.unlearning_path+'_0_nodes_'+str(len(nodes))+'.txt', nodes, fmt='%d')
    args = dict(parameters, unlearn_task='node', device='cpu', num_unlearned_nodes=len(nodes))
    trainer = trainer_module.ETRTrainer(args, logging.getLogger('reference'), copy.deepcopy(model), data.clone())
    # Bind the existing pipeline hook to an already prepared model/request.
    pipeline = pipeline_module.etr.__new__(pipeline_module.etr)
    pipeline.args, pipeline.run, pipeline.data, pipeline.target_model = args, 0, data.clone(), trainer
    pipeline.unlearning_request()
    states = {}
    for method_name, stage in [('_modify_weight', 'erase'), ('_modify_weight2', 'rectify')]:
        original = getattr(trainer, method_name)
        def capture(self, edited, *values, _original=original, _stage=stage):
            _original(edited, *values)
            states[_stage] = snapshot(edited)
        setattr(trainer, method_name, types.MethodType(capture, trainer))
    trainer._save_unlearned_model = lambda run: torch.save(snapshot(trainer.model), root/(label+'-reference.pt'))
    started = time.perf_counter()
    with seeded_execution(42):
        internal_seconds, retained_f1 = trainer.etr_unlearning(np.asarray(nodes), run=0)
    wall = time.perf_counter() - started
    trainer.model.eval()
    with torch.no_grad():
        logits = trainer.model(data.x, data.edge_index).detach()
    return states, logits, trainer, dict(wall_seconds=wall, reported_edit_seconds=internal_seconds,
                                       retained_graph_f1=retained_f1)


def verify_case(root, refs, data, selector, summary, warm):
    from experiments.modular_config import load_instance
    from experiments.modular_model import prepare_model
    from experiments.unlearning_outputs import load_output, restore_model
    from experiments.modular_artifacts import read_run
    from unlearning.unlearning_methods.ETR.etr import run_etr, edit_subgraphs
    from attack.cache_identity import seeded_execution
    from utils.target_checkpoint import sha256_file
    etr = next(row for row in summary['unlearning'] if row['target']['method'] == 'ETR')
    retrain = next(row for row in summary['unlearning'] if row['target']['method'] == 'Retrain')
    assert not etr['hit'] and not retrain['hit']
    assert all(row['hit'] for row in warm['unlearning'])
    assert [row['output'] for row in summary['unlearning']] == [row['output'] for row in warm['unlearning']]
    store = root/'results/cache_v2'
    payload = load_output(etr['output'], store, data=data, dataset_root=root)
    paired = load_output(retrain['output'], store, data=data, dataset_root=root)
    nodes = payload.arrays['selected_nodes'].tolist()
    assert nodes == paired.arrays['selected_nodes'].tolist()
    instance = load_instance(root/'etr.yaml', 'unlearning')
    model, _, checkpoint = prepare_model(instance, data=data, dataset_name='cora',
        checkpoint_root=root/'results/runtime/modular/checkpoints', device='cpu', reference_directory=root)
    assert checkpoint['state_hash'] == etr['checkpoint']['state_hash']
    before = snapshot(model)
    with torch.no_grad():
        model.eval()
        original_logits = model(data.x, data.edge_index).detach()
    states, reference_logits, trainer, timing = reference_run(root, refs, model, data, nodes, selector, instance['parameters'])
    integrated_states = {}
    with seeded_execution(42):
        edited, seconds = run_etr(model, data.clone(), nodes, erase_ratio=instance['parameters']['etr_erase_ratio'],
            coefficient=instance['parameters']['etr_l'], trace=lambda phase, m: integrated_states.update({phase: snapshot(m)}))
    differences = {stage: compare(integrated_states[stage], states[stage]) for stage in states}
    compare(snapshot(model), before)
    differences['persisted_state'] = compare(snapshot(restore_model(payload)), states['rectify'])
    differences['logits'] = compare({'logits': torch.tensor(payload.arrays['logits'])}, {'logits': reference_logits})
    train, forgotten, influence, after, ids = edit_subgraphs(data, nodes)
    for left, right in [(train, trainer.dataset_train), (forgotten, trainer.unlearn_subgraph),
                        (influence, trainer.influenced_subgraph), (after, trainer.influenced_subgraph_unlearned)]:
        assert torch.equal(left.edge_index, right.edge_index) and torch.equal(left.x, right.x)
        assert torch.equal(left.y, right.y)
        if hasattr(left, 'mapping'):
            assert torch.equal(left.mapping, right.mapping)
    assert ids.tolist() == trainer.influenced_nodes.tolist()
    for rid in ('cold', 'warm'):
        run_path = root/'results/runs'/('aagu106-'+selector)/rid/'run.json'
        _, documents = read_run(run_path, sha256_file(run_path))
        assert len(documents) == 2
    mask = data.test_mask.numpy()
    accuracy = lambda logits: float((np.asarray(logits)[mask].argmax(1) == data.y.numpy()[mask]).mean())
    np.savez_compressed(root/(selector+'-predictions.npz'), original=original_logits.numpy(),
        benchmark=reference_logits.numpy(), integrated=payload.arrays['logits'], retrain=paired.arrays['logits'],
        selected_nodes=np.asarray(nodes), test_mask=mask)
    torch.save(dict(original=before, benchmark=states, integrated=integrated_states), root/(selector+'-stages.pt'))
    return dict(selector=selector, selected_count=len(nodes), candidate_count=int(data.train_mask.sum()),
        connected_forget_count=len(forgotten.mapping), influenced_count=len(ids),
        connected_influence_after_count=len(after.mapping), max_abs_error=differences,
        original_accuracy=accuracy(original_logits.numpy()), benchmark_accuracy=accuracy(reference_logits.numpy()),
        integrated_accuracy=accuracy(payload.arrays['logits']), retrain_accuracy=accuracy(paired.arrays['logits']),
        gu_retrain_disagreement=float((payload.arrays['logits'][mask].argmax(1) != paired.arrays['logits'][mask].argmax(1)).mean()),
        erase_delta=max(float((states['erase'][k]-before[k]).abs().max()) for k in before),
        rectify_delta=max(float((states['rectify'][k]-states['erase'][k]).abs().max()) for k in before),
        timing=dict(reference=timing, integrated_including_subgraphs=seconds,
                    cli_etr_compute=etr['compute_seconds'], cli_retrain_compute=retrain['compute_seconds']),
        outputs={'ETR': etr['output'], 'Retrain': retrain['output']}, checkpoint=checkpoint,
        evaluations=summary['evaluations'], cold_warm_verified=True, result_files_verified=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--data-file', required=True, type=Path)
    parser.add_argument('--reference-directory', required=True, type=Path)
    args = parser.parse_args()
    # OpenGU's config module parses sys.argv at import time. The verification
    # arguments have already been consumed; downstream imports get a clean CLI.
    sys.argv = ['verify-etr-cpu']
    from utils.target_checkpoint import sha256_file
    for name, digest in REFERENCE_FILES.items():
        if sha256_file(args.reference_directory/name) != digest:
            raise ValueError('pinned benchmark source mismatch: '+name)
    root = args.root.resolve()
    root.mkdir(parents=True, exist_ok=False)
    refs = root/'reference'
    refs.mkdir()
    for name in REFERENCE_FILES:
        shutil.copy2(args.reference_directory/name, refs/name)
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    diff = subprocess.check_output(['git', 'diff', '--binary', 'HEAD'], cwd=ROOT)
    (root/'source.patch').write_bytes(diff)
    write_json(root/'protocol.json', dict(atol=ATOL, rtol=RTOL, reference_commit=REFERENCE_SHA,
        reference_files=REFERENCE_FILES, reference_adjustment='all four _grad_and_info calls use eval; importance/Erase intermediates float64; final weights original dtype; autograd retained', source_commit=sha, source_patch_sha256=sha256_file(root/'source.patch'),
        torch=torch.__version__, training_seed=42, split_seed=2024, ratios={'random': .1, 'degree': .05},
        budget_denominator='persisted training nodes', evaluation_graph='original', level='verification'))
    torch.set_num_threads(1)
    data = prepare_inputs(root, args.data_file)
    results = []
    for selector in ('random', 'degree'):
        cli(root, selector, 'dry', dry=True)
        cold = cli(root, selector, 'cold')
        warm = cli(root, selector, 'warm')
        row = verify_case(root, refs, data, selector, cold, warm)
        results.append(row)
        write_json(root/'comparison.json', dict(passed=len(results)==2, cases=results))
        print(selector, 'PASS', row['max_abs_error'], flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
