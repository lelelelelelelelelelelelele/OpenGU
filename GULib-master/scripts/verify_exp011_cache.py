"""EXP-011 cache-only gate: five selectors x five historical GU lanes.

Run in the SSH active checkout. This reads the unmodified Table02 configuration,
uses its first Cora/seed42 budget, and fails on any cache miss before computation.
It is a cache-reuse gate, not a full-matrix or scientific acceptance gate.
"""
import functools
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SELECTORS = ('r_point', 'gt_full', 'degree', 'random', 'pagerank')
METHODS = ('GNNDelete', 'MEGU', 'GraphEraser', 'GraphRevoker', 'Retrain')


def forbid(function):
    @functools.wraps(function)
    def guard(*args, **kwargs):
        raise AssertionError('cache gate forbids producer: ' + function.__name__)
    return guard


def require_hit(function):
    @functools.wraps(function)
    def guard(root, request):
        result = function(root, request)
        if result is None:
            raise AssertionError('cache MISS: ' + request.recipe.recipe_hash)
        return result
    return guard


def main():
    import torch
    from contextlib import ExitStack
    from experiments.modular_model import runtime_defaults
    runtime_defaults()
    import experiments.modular_model as mm
    import experiments.modular_gu as gu
    import experiments.modular_shards as shards
    import experiments.modular_graphrevoker as revoker
    import experiments.artifact_producer as artifacts
    import experiments.model_trajectory as trajectory
    from experiments.modular_megu import run_megu_unlearning
    from experiments.target_direct_v1.method_cache import resolve_methods
    from experiments.modular_config import load_experiment, experiment_batches, resolve_budget
    from experiments.dataset_inputs import read_dataset, bind_input
    from experiments.modular_run import verified_selection, selection_prefix

    store = ROOT / 'results/cache_v2'
    index = store / 'index.sqlite'
    before = hashlib.sha256(index.read_bytes()).hexdigest()
    config_path = ROOT / 'experiments/configs/aagu011/table02_v2.yaml'
    config = load_experiment(config_path)
    batches = list(experiment_batches(config))
    data, inputs = read_dataset(config['datasets'][0], config['dataset_directories'][0])
    assert inputs.dataset_name.lower() == 'cora'
    data = data.to('cpu')
    torch.set_num_threads(1)
    reference = bind_input(config['datasets'][0], config['dataset_directories'][0], ROOT)
    consumers = dict.fromkeys(METHODS, gu.run_unlearning)
    consumers.update(MEGU=run_megu_unlearning, GraphEraser=shards.run_shard_unlearning,
                     GraphRevoker=revoker.run_graphrevoker_unlearning)
    rows = []
    with ExitStack() as stack:
        # wraps preserves the real implementation fingerprint. No fake identities,
        # historical Selection injection, registry replacement, or training allowed.
        for module, name in ((mm, 'train_supervised'), (trajectory, 'train_supervised'),
                             (shards, 'initial_ensemble'), (revoker, 'initial_graphrevoker_ensemble')):
            stack.enter_context(patch.object(module, name, forbid(getattr(module, name))))
        stack.enter_context(patch.object(artifacts, 'resolve_formal_artifact',
                                        require_hit(artifacts.resolve_formal_artifact)))
        for name in SELECTORS:
            batch = next(b for b in batches if b['matrix_values']['dataset_index'] == 0
                         and b['matrix_values']['training_seed'] == 42
                         and any(x['method'] == name for x in b['selectors']))
            item = next(x for x in batch['selectors'] if x['method'] == name)
            item['budget'] = resolve_budget(item['budget'], inputs.candidate_count)
            model, checkpoints = None, []
            if 'model' in item:
                model, checkpoints, observation = mm.prepare_model(item, data=data,
                    dataset_name=inputs.dataset_name, checkpoint_root=ROOT / 'results/runtime/modular/checkpoints',
                    device=torch.device('cpu'), reference_directory=Path(config['source_directory']))
                assert observation['hit'], 'selector checkpoint MISS'
            selected = resolve_methods(store_root=store, data=data, dataset_name=inputs.dataset_name,
                model=model, checkpoints=checkpoints, selectors=[item], model_config=item.get('model'),
                training=item.get('training'), fail_if_score_called=True, fail_if_selection_called=True)[name]
            assert selected['selection']['cache']['hit']
            assert not selected['selection']['cache']['producer_called']
            assert not selected['score']['producer_called']
            ref = {k: selected['selection']['artifact'][k] for k in ('artifact_id', 'recipe_hash', 'content_hash')}
            loaded = verified_selection(ref, store_root=store, data=data, inputs=inputs,
                expected_selector=name, expected_k=selected['selection']['artifact_k'])
            selection = selection_prefix(loaded, item['budget']['k'])
            for method in METHODS:
                instance = next(x for x in batch['unlearnings'] if x['method'] == method)
                model, checkpoint = None, None
                if method != 'Retrain':
                    model, _, checkpoint = mm.prepare_model(instance, data=data,
                        dataset_name=inputs.dataset_name, checkpoint_root=ROOT / 'results/runtime/modular/checkpoints',
                        device=torch.device('cpu'), reference_directory=Path(config['source_directory']))
                    assert checkpoint['hit'], 'GU checkpoint MISS'
                result = consumers[method](instance, selection=selection, model=model, data=data,
                    dataset_name=inputs.dataset_name, checkpoint=checkpoint, store_root=store,
                    runtime_root=ROOT / '.syncmate/exp011-cache-gate-forbidden', dataset_input=reference, dataset_root=ROOT)
                assert result['hit'] and not result['producer_called']
                preparation = result.get('ensemble_preparation')
                if preparation:
                    assert preparation['hit'], 'ensemble checkpoint MISS'
                    assert result['target']['ensemble_state_hash'] == preparation['state_hash']
                row = dict(selector=name, method=method, k=item['budget']['k'], selection_id=ref['artifact_id'],
                           prediction_id=result['artifact_id'], hit=True, producer_called=False,
                           ensemble_state_hash=result.get('target', {}).get('ensemble_state_hash'))
                rows.append(row)
                print(json.dumps(row), file=sys.stderr, flush=True)
    assert len(rows) == 25
    assert hashlib.sha256(index.read_bytes()).hexdigest() == before, 'cache index changed'
    assert not (ROOT / '.syncmate/exp011-cache-gate-forbidden').exists()
    print(json.dumps(dict(status='passed', scope='Cora seed42 first configured budget; 5 selectors x 5 historical GU methods',
        config_sha256=hashlib.sha256(config_path.read_bytes()).hexdigest(), rows=rows,
        index_sha256=before, index_unchanged=True, producer_calls=0), indent=2))


if __name__ == '__main__':
    main()
