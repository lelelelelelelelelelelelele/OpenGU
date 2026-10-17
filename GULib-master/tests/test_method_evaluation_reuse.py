"""Reuse values without changing exact post-Evaluation cache identity."""
import copy
import functools
import json

import pytest

from test_modular_consumers import tables, run, write_yaml
from test_unlearning_paired_evaluations import paired_tables


def setup_post(tables):
    root = paired_tables(tables)
    write_yaml(root/'post.yaml', dict(kind='evaluation', schema_version=1, case='post_method_metrics'))
    return root, dict(stage='unlearning', selector_refs=['degree.yaml'],
        unlearning_refs=['gu.yaml', 'retrain.yaml'], evaluation_refs=['post.yaml'])


def count_formulas(monkeypatch):
    from experiments import output_metrics
    counts = dict(method_metrics=0, update_detection=0)
    for name in counts:
        original = getattr(output_metrics, name)
        def wrap(original, name):
            @functools.wraps(original)
            def measured(*args, **kwargs):
                counts[name] += 1
                return original(*args, **kwargs)
            return measured
        monkeypatch.setattr(output_metrics, name, wrap(original, name))
    return counts


def test_cold_post_uses_once_per_output_and_warm_keeps_artifacts(tables, monkeypatch, record_property):
    root, options = setup_post(tables)
    counts = count_formulas(monkeypatch)
    cold = run(tables, 'reuse-cold', **options)
    assert counts == dict(method_metrics=2, update_detection=2)
    for output, post in zip(cold['unlearning'], cold['evaluations'][0]['rows']):
        assert post['metrics'] == output['evaluation']['metrics']
        assert post['identity']['method_evaluation'] == output['evaluation']['identity']
        assert not post['cache']['hit']
    warm = run(tables, 'reuse-warm', **options)
    assert counts == dict(method_metrics=2, update_detection=2)
    for before, after in zip(cold['evaluations'][0]['rows'], warm['evaluations'][0]['rows']):
        assert before['cache']['artifact_id'] == after['cache']['artifact_id']
        assert before['cache']['recipe_hash'] == after['cache']['recipe_hash']
        assert before['cache']['content_hash'] == after['cache']['content_hash']
        assert after['cache']['hit'] and not after['cache']['producer_called']
    record_property('formula_counts', json.dumps(counts))


def test_post_miss_basic_hit_uses_values_without_prediction_reads(tables, monkeypatch):
    from experiments import unlearning_outputs as outputs
    from experiments.modular_evaluation import evaluate_modular
    root, options = setup_post(tables)
    counts = count_formulas(monkeypatch)
    cold = run(tables, 'base-only', **{**options, 'evaluation_refs':[]})
    warm = run(tables, 'base-hit', **{**options, 'evaluation_refs':[]})
    assert all(row['evaluation_cache']['hit'] for row in warm['unlearning'])
    assert counts == dict(method_metrics=2, update_detection=2)
    def forbidden(*a, **k):
        pytest.fail('post reused base values but loaded predictions')
    monkeypatch.setattr(outputs, 'load_metric_output', forbidden)
    result = run(tables, 'post-backfill', **options)
    assert counts == dict(method_metrics=2, update_detection=2)
    assert all(not row['cache']['hit'] for row in result['evaluations'][0]['rows'])
    item = {**result['evaluations'][0]['effective_config'], 'metrics':['f1', 'classification_auc_status']}
    subset = evaluate_modular(item, warm['unlearning'], store_root=root/'results/cache_v2', dataset_root=root)
    assert all(not row['cache']['hit'] for row in subset['rows'])
    assert subset['rows'][0]['cache']['recipe_hash'] != result['evaluations'][0]['rows'][0]['cache']['recipe_hash']
    assert subset['rows'][0]['metrics'] == {key:cold['unlearning'][0]['evaluation']['metrics'][key] for key in item['metrics']}


@pytest.mark.parametrize('field', ['output', 'protocol', 'implementation', 'metric_libraries', 'receipt_id'])
def test_stale_receipt_is_rejected_before_post_storage(tables, field):
    from experiments.modular_evaluation import evaluate_modular, resolve_evaluation
    root, options = setup_post(tables)
    cold = run(tables, 'base', **{**options, 'evaluation_refs':[]})
    rows = copy.deepcopy(cold['unlearning'])
    receipt = rows[0]['evaluation']
    if field == 'receipt_id':
        receipt['evaluation_receipt_id'] = 'evalr_bad'
    else:
        receipt['identity'][field] = 'foreign'
    item = resolve_evaluation(dict(kind='evaluation',schema_version=1,case='post_method_metrics'))
    with pytest.raises(ValueError, match='receipt does not match'):
        evaluate_modular(item, rows, store_root=root/'results/cache_v2', dataset_root=root)


def test_exact_post_conflict_still_fails_closed(tables):
    from cache_v2 import CacheIndex
    from cache_v2.contracts import ArtifactConflictRecord, ArtifactType
    from experiments.modular_evaluation import evaluate_modular
    root, options = setup_post(tables)
    cold = run(tables, 'conflict-source', **options)
    ref = cold['evaluations'][0]['rows'][0]['cache']
    index = CacheIndex(root/'results/cache_v2/index.sqlite')
    index.record_conflict(ArtifactConflictRecord(artifact_type=ArtifactType.EVALUATION,
        recipe_hash=ref['recipe_hash'], existing_artifact_id=ref['artifact_id'],
        existing_content_hash=ref['content_hash'], observed_content_hash='0'*64,
        quarantine_path='quarantine/owned-test'))
    with pytest.raises(Exception, match='conflict|closed'):
        evaluate_modular(cold['evaluations'][0]['effective_config'], cold['unlearning'],
            store_root=root/'results/cache_v2', dataset_root=root)


def test_standalone_without_base_receipt_keeps_direct_measurement(tables, monkeypatch):
    from experiments.modular_evaluation import evaluate_modular, resolve_evaluation
    root, options = setup_post(tables)
    cold = run(tables, 'base', **{**options, 'evaluation_refs':[]})
    counts = count_formulas(monkeypatch)
    rows = [{'output':row['output']} for row in cold['unlearning']]
    result = evaluate_modular(resolve_evaluation(dict(kind='evaluation',schema_version=1,case='post_method_metrics')),
        rows, store_root=root/'results/cache_v2', dataset_root=root)
    assert counts == dict(method_metrics=2, update_detection=2)
    assert result['rows'][0]['metrics'] == cold['unlearning'][0]['evaluation']['metrics']
