"""Native CLI hardware and disposable-root boundaries require no SyncMate."""
import pytest
import torch

from experiments.modular_execution import native_context, validate_execution_device, REPO_ROOT
from experiments.modular_layout import modular_output_path


@pytest.mark.parametrize('device', [None, '', 'invalid-device', 'mps', 'cpu:0'])
def test_native_device_must_be_explicit_and_supported(device):
    with pytest.raises(ValueError):
        validate_execution_device(device)


def test_cuda_unavailability_never_substitutes_cpu(monkeypatch):
    monkeypatch.setattr(torch.cuda, 'is_available', lambda: False)
    with pytest.raises(ValueError, match='CUDA device unavailable'):
        validate_execution_device('cuda:0')


def test_cuda_index_is_checked_before_execution(monkeypatch):
    monkeypatch.setattr(torch.cuda, 'is_available', lambda: True)
    monkeypatch.setattr(torch.cuda, 'device_count', lambda: 1)
    with pytest.raises(ValueError, match='CUDA device unavailable'):
        validate_execution_device('cuda:1')


def test_native_verification_owns_same_result_layout(tmp_path):
    context = native_context('standalone', run_id='v1', request_device='cpu',
                             verification_root=tmp_path)
    assert context.level == 'verification'
    assert context.request_device == 'cpu'
    assert context.store_root == tmp_path / 'results/cache_v2'
    assert context.output == tmp_path / modular_output_path('standalone', 'v1')
    assert context.executor == 'experiment-run'


def test_formal_cpu_is_refused(tmp_path):
    with pytest.raises(ValueError, match='formal execution requires'):
        native_context('standalone', run_id='v1', request_device='cpu', repository_root=tmp_path)


def test_verification_cannot_write_inside_source_checkout():
    with pytest.raises(ValueError, match='disposable root outside'):
        native_context('standalone', run_id='v1', request_device='cpu',
                       verification_root=REPO_ROOT / 'results')


@pytest.mark.parametrize('value', ['../escape', '', 'nested/path'])
def test_result_layout_rejects_escape(value):
    with pytest.raises(ValueError, match='unsafe'):
        modular_output_path(value, 'v1')
