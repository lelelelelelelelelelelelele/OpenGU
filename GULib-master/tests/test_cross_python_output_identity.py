"""Cross-runtime provenance must stay strict without depending on inspect quirks."""
import copy
import inspect
from dataclasses import dataclass

import pytest
from cache_v2 import canonical_sha256
from experiments.implementation_identity import computation_source, implementation_fingerprint
from scripts.syncmate.opengu_method_output import verify_evaluation


@dataclass(frozen=True)
class DecoratedPayload:
    value: int


def test_class_fingerprint_is_independent_of_inspect_decorator_start(monkeypatch):
    original = inspect.getsourcelines
    expected = implementation_fingerprint(DecoratedPayload)
    assert computation_source(DecoratedPayload).startswith('@dataclass(frozen=True)\n')
    def class_start(value):
        lines, start = original(value)
        if value is DecoratedPayload:
            while lines[0].startswith('@'):
                lines, start = lines[1:], start + 1
        return lines, start
    monkeypatch.setattr(inspect, 'getsourcelines', class_start)
    assert implementation_fingerprint(DecoratedPayload) == expected


def receipt():
    identity = {'output': {'artifact_id': 'bound-output'}, 'protocol': 'fixed-test-v1',
                'implementation': 'reviewed-source',
                'metric_libraries': {'torch': '2.1.2', 'numpy': '1.26.4', 'sklearn': '1.3.2'}}
    return {'identity': identity, 'evaluation_receipt_id': 'evalr_' + canonical_sha256(identity)[:32],
            'metrics': {'accuracy': .75, 'cross_entropy': .451, 'classification_auc_status': 'computed'}}


def test_different_collector_library_versions_preserve_producer_receipt():
    saved = receipt()
    local = copy.deepcopy(saved)
    local['identity']['metric_libraries']['torch'] = '2.2.1'
    local['identity']['metric_libraries']['numpy'] = '1.21.6'
    local['evaluation_receipt_id'] = 'evalr_' + canonical_sha256(local['identity'])[:32]
    local['metrics']['cross_entropy'] += 1e-12
    verify_evaluation(saved, local, saved['evaluation_receipt_id'])


@pytest.mark.parametrize('fault', ['metric', 'nan', 'protocol', 'output', 'digest', 'status'])
def test_receipt_or_measurement_tampering_fails_closed(fault):
    saved = receipt()
    current = copy.deepcopy(saved)
    if fault == 'metric': saved['metrics']['accuracy'] = .8
    elif fault == 'nan': saved['metrics']['accuracy'] = float('nan')
    elif fault in ('protocol', 'output'): saved['identity'][fault] = 'different'
    elif fault == 'digest': saved['evaluation_receipt_id'] = 'evalr_wrong'
    elif fault == 'status': saved['metrics']['classification_auc_status'] = 'missing'
    with pytest.raises(ValueError):
        verify_evaluation(saved, current, current['evaluation_receipt_id'])
