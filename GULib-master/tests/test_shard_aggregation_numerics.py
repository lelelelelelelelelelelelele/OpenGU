"""Exercise real optimizer methods without importing the global CLI/dataset stack."""
import ast
import copy
import logging
from pathlib import Path
import time
from types import SimpleNamespace

import pytest
import torch
from torch import nn, optim
from torch.nn import functional as F
from torch.optim.lr_scheduler import MultiStepLR
from torch.utils.data import DataLoader, Dataset


ROOT = Path(__file__).resolve().parents[1] / 'unlearning/unlearning_methods'


def optimizer_class(method, legacy=False):
    folder = ROOT / method / ('aggregation' if method == 'GraphEraser' else 'lib_aggregator')
    namespace = dict(copy=copy, logging=logging, time=time, torch=torch, nn=nn,
                     optim=optim, F=F, MultiStepLR=MultiStepLR, DataLoader=DataLoader,
                     Dataset=Dataset, tqdm=lambda iterable, **kwargs: iterable)
    for filename, name in [('opt_dataset.py', 'OptDataset'), ('optimal_aggregator.py', 'OptimalAggregator')]:
        source = (folder / filename).read_text(encoding='utf-8')
        if legacy and name == 'OptimalAggregator':
            # Restore precisely the two pre-fix expressions. Everything else,
            # including batching, Adam and best-epoch selection, is real code.
            source = source.replace('torch.clamp(weight_para, min=torch.finfo(weight_para.dtype).eps)',
                                    'torch.clamp(weight_para, min=0.0)')
            source = source.replace('torch.linalg.vector_norm(weight_para)',
                                    'torch.sqrt(torch.sum(weight_para ** 2))')
        tree = ast.parse(source)
        tree.body = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == name]
        exec(compile(tree, str(folder / filename), 'exec'), namespace)
    return namespace['OptimalAggregator']


def fixture(method, legacy=False, normal=False):
    torch.set_num_threads(1)
    torch.manual_seed(2024)
    instance = optimizer_class(method, legacy)(
        0, SimpleNamespace(model=None), None,
        dict(num_shards=2, opt_lr=.001 if normal else .01,
             opt_num_epochs=5 if normal else 100), logging.getLogger('numerics'))
    instance.device = torch.device('cpu')
    instance.true_labels = torch.zeros(32, dtype=torch.long)
    if normal:
        instance.posteriors = {0: torch.tensor([[.9999, .0001]]).log().repeat(32, 1),
                               1: torch.tensor([[.0001, .9999]]).log().repeat(32, 1)}
    else:
        instance.posteriors = {i: torch.full((32, 2), -0.69314718) for i in range(2)}
    return instance


@pytest.mark.parametrize('method', ['GraphEraser', 'GraphRevoker'])
def test_collapsed_weights_old_red_new_green(method):
    old = fixture(method, legacy=True).optimization()
    assert not torch.isfinite(old).all(), 'pre-fix zero-sum normalization must reproduce'
    new = fixture(method).optimization().detach()
    assert torch.isfinite(new).all() and (new > 0).all()
    torch.testing.assert_close(new.sum(), torch.tensor(1.))
    assert torch.equal(new, fixture(method).optimization().detach())


@pytest.mark.parametrize('method', ['GraphEraser', 'GraphRevoker'])
def test_zero_norm_gradient_old_red_new_green(method):
    for legacy in (True, False):
        instance = fixture(method, legacy=legacy)
        weights = torch.zeros(2, requires_grad=True)
        instance._loss_fn(instance.posteriors, instance.true_labels, weights).backward()
        assert bool(torch.isfinite(weights.grad).all()) is not legacy


@pytest.mark.parametrize('method', ['GraphEraser', 'GraphRevoker'])
def test_nondegenerate_weights_preserve_original_optimization(method):
    old = fixture(method, legacy=True, normal=True).optimization().detach()
    new = fixture(method, normal=True).optimization().detach()
    assert torch.isfinite(new).all() and (new > 0).all()
    assert new[0] > new[1], 'optimizer must learn a preference, not return uniform weights'
    torch.testing.assert_close(new, old, rtol=1e-6, atol=1e-7)
    torch.testing.assert_close(new.sum(), torch.tensor(1.))
    assert torch.equal(new, fixture(method, normal=True).optimization().detach())
