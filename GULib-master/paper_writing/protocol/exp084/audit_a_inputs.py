"""One-shot, read-only EXP-084 frozen-request audit on the active runner.

No training, ranking, selection, Output production, or cache mutation is allowed.
The runner must be idle. Normal mode checks the installed repair. An explicit
planned-source mode can query the reviewed future identity before installation;
it must be repeated after installation. This is not a GPU/scientific gate.
"""
import argparse
from copy import deepcopy
from contextlib import ExitStack
import functools
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]


def forbid(function):
    @functools.wraps(function)
    def denied(*args, **kwargs):
        raise AssertionError('Frozen input audit forbids producer: ' + function.__name__)
    return denied


class AuditedOutput(Exception):
    def __init__(self, result):
        self.result = result


def main():
    global ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=ROOT)
    parser.add_argument('--frozen-inputs', type=Path, default=Path(__file__).with_name('FROZEN_A_INPUTS.json'))
    parser.add_argument('--config', default='experiments/configs/exp084/main.yaml')
    parser.add_argument('--require-all-gnndelete-miss', action='store_true')
    parser.add_argument('--query-planned-source', action='store_true',
        help='Before deployment only: query the reviewed repair source without importing or running repair code. Must repeat after install.')
    parser.add_argument('--expected-new-source', default='b6dc18cc580f6184cc500459b3b36d1f2f3002ddd3f7da81a969714ee2c0329e')
    args = parser.parse_args()
    ROOT = args.repo_root.resolve()
    sys.path.insert(0, str(ROOT))
    frozen_path = args.frozen_inputs.resolve()
    frozen = json.loads(frozen_path.read_text(encoding='utf-8'))
    expected = {(r['seed'], r['selector_ref']): r for r in frozen['requests']}

    import torch
    from cache_v2 import CacheIndex, ArtifactRecipe, ProducerVersion
    from cache_v2.source_compatibility import stored_recipe, recipe_candidates
    from experiments.modular_model import runtime_defaults
    runtime_defaults()
    import experiments.modular_model as mm
    import experiments.modular_gu as gu
    import experiments.artifact_producer as artifacts
    from experiments.modular_config import load_experiment, experiment_batches, resolve_budget
    from experiments.dataset_inputs import read_dataset, bind_input
    from experiments.modular_run import verified_selection, selection_prefix
    from experiments.target_direct_v1.method_cache import resolve_methods
    from experiments.implementation_identity import fingerprint_session

    store = ROOT / 'results/cache_v2'
    index_path = store / 'index.sqlite'
    before_index = hashlib.sha256(index_path.read_bytes()).hexdigest()
    config_path = ROOT / args.config
    config = load_experiment(config_path)
    assert config['experiment_id'] == 'exp084-gnndelete-checkpoint-audit'
    data, inputs = read_dataset(config['datasets'][0], config['dataset_directories'][0])
    assert inputs.dataset_name.lower() == 'cora'
    data = data.to('cpu')
    torch.set_num_threads(1)
    dataset_input = bind_input(config['datasets'][0], config['dataset_directories'][0], ROOT)
    output_rows = []
    original_resolve = artifacts.resolve_formal_artifact
    current_expected = None

    def intercept_output(root, request, **kwargs):
        method = request.recipe.fields['target']['method']
        record = current_expected
        actual_producer = request.producer_version.to_dict()
        if method == 'GNNDelete':
            if args.query_planned_source:
                from experiments.artifact_producer import FormalArtifactRequest
                fields = deepcopy(request.recipe.fields)
                fields['producer_version']['source_fingerprint'] = args.expected_new_source
                planned = ProducerVersion(**fields['producer_version'])
                request = FormalArtifactRequest(request.artifact_type, ArtifactRecipe(fields), planned)
            else:
                assert actual_producer['source_fingerprint'] == args.expected_new_source, 'Reviewed repair not installed'
        result = original_resolve(root, request, **kwargs)
        if method == 'Retrain':
            assert result is not None, 'Frozen Retrain is missing under current exact identity'
            assert result.artifact_id == record['expected_retrain_output']['artifact_id']
            assert result.content_hash == record['expected_retrain_output']['content_hash']
            outcome = {'method': method, 'hit': True, 'output_id': result.artifact_id}
        else:
            assert method == 'GNNDelete'
            index = CacheIndex(index_path)
            with index.read_session():
                old = index.get_artifact(record['old_gnndelete_output']['artifact_id'])
                old_recipe = stored_recipe(old)
            assert old['content_hash'] == record['old_gnndelete_output']['content_hash']
            assert request.recipe.fields['target']['checkpoint_state_hash'] == old_recipe.fields['target']['checkpoint_state_hash'], 'Initial GCN state drifted'
            assert all(candidate.recipe_hash != old_recipe.recipe_hash for candidate in recipe_candidates('prediction', request.recipe)), 'Old test-selected Output remains source-compatible'
            if args.require_all_gnndelete_miss:
                assert result is None, 'Initial repaired run unexpectedly has an Output HIT'
            if result is not None:
                assert result.generation_producer == request.producer_version.to_dict(), 'Only current repaired Output may HIT'
                assert result.artifact_id != record['old_gnndelete_output']['artifact_id']
            outcome = {'method': method, 'hit': result is not None,
                       'output_id': result.artifact_id if result else None,
                       'new_recipe_hash': request.recipe.recipe_hash,
                       'new_producer': request.producer_version.to_dict(),
                       'runtime_producer': actual_producer,
                       'old_output_id': record['old_gnndelete_output']['artifact_id'],
                       'checkpoint_state_hash': request.recipe.fields['target']['checkpoint_state_hash']}
        raise AuditedOutput(outcome)

    with fingerprint_session(), ExitStack() as stack:
        stack.enter_context(patch.object(mm, 'train_supervised', forbid(mm.train_supervised)))
        stack.enter_context(patch.object(artifacts, 'resolve_formal_artifact', intercept_output))
        for batch in experiment_batches(config):
            seed = batch['matrix_values']['training_seed']
            assert batch['matrix_values']['budget_ratio'] == 0.1
            for item in batch['selectors']:
                ref_name = 'degree.yaml' if item['method'] == 'degree' else item['method'] + '_sgc.yaml'
                current_expected = expected[(seed, ref_name)]
                item['budget'] = resolve_budget(item['budget'], inputs.candidate_count)
                assert item['budget']['k'] == current_expected['requested_k']
                model, checkpoints, selector_checkpoint = None, [], None
                if 'model' in item:
                    model, checkpoints, selector_checkpoint = mm.prepare_model(item, data=data,
                        dataset_name=inputs.dataset_name, checkpoint_root=ROOT / 'results/runtime/modular/checkpoints',
                        device=torch.device('cpu'), reference_directory=Path(config['source_directory']))
                    assert selector_checkpoint['hit'], 'Selector checkpoint MISS'
                selected = resolve_methods(store_root=store, data=data, dataset_name=inputs.dataset_name,
                    model=model, checkpoints=checkpoints, selectors=[item], include_scores=False,
                    model_config=item.get('model'), training=item.get('training'),
                    fail_if_score_called=True, fail_if_selection_called=True)[item['method']]
                assert selected['selection']['cache']['hit']
                assert not selected['selection']['cache']['producer_called']
                assert not selected['score']['producer_called']
                ref = {k: selected['selection']['artifact'][k] for k in ('artifact_id', 'recipe_hash', 'content_hash')}
                assert ref['artifact_id'] == current_expected['selection_id'], 'Selection identity drifted'
                loaded = verified_selection(ref, store_root=store, data=data, inputs=inputs,
                    expected_selector=item['method'], expected_k=selected['selection']['artifact_k'])
                selection = selection_prefix(loaded, item['budget']['k'])
                assert list(selection.selected_nodes) == current_expected['selected_nodes'], 'Ordered request drifted'
                for instance in batch['unlearnings']:
                    target_model, checkpoint = None, None
                    if instance['method'] != 'Retrain':
                        target_model, _, checkpoint = mm.prepare_model(instance, data=data,
                            dataset_name=inputs.dataset_name, checkpoint_root=ROOT / 'results/runtime/modular/checkpoints',
                            device=torch.device('cpu'), reference_directory=Path(config['source_directory']))
                        assert checkpoint['hit'], 'Base GCN checkpoint MISS'
                    try:
                        gu.run_unlearning(instance, selection=selection, model=target_model, data=data,
                            dataset_name=inputs.dataset_name, checkpoint=checkpoint, store_root=store,
                            runtime_root=ROOT / '.syncmate/exp084-forbidden-producer',
                            dataset_input=dataset_input, dataset_root=ROOT)
                    except AuditedOutput as passed:
                        output_rows.append(dict(seed=seed, selector_ref=ref_name,
                            selection_id=ref['artifact_id'], selector_checkpoint=selector_checkpoint,
                            **passed.result))
                    else:
                        raise AssertionError('Output consumer escaped audit sentinel')
    expected_count = 2 * len(config['selectors']) * len(config['seeds'])
    assert len(output_rows) == expected_count
    assert hashlib.sha256(index_path.read_bytes()).hexdigest() == before_index, 'Cache index changed during audit'
    assert not (ROOT / '.syncmate/exp084-forbidden-producer').exists()
    print(json.dumps(dict(status='passed', scope='frozen request and producer boundary only; no scientific acceptance',
        source_mode='planned_source_query_requires_postinstall_recheck' if args.query_planned_source else 'actual_installed_source',
        frozen_manifest_sha256=hashlib.sha256(frozen_path.read_bytes()).hexdigest(),
        config_sha256=hashlib.sha256(config_path.read_bytes()).hexdigest(),
        index_sha256=before_index, index_unchanged=True, producer_calls=0, rows=output_rows), indent=2))


if __name__ == '__main__':
    main()
