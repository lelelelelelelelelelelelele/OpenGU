import copy

import pytest
import torch

from test_modular_consumers import tables
from experiments.aagu059_diagnostic import measured_series, capture_system, flat, lanczos


def test_trace_matches_explicit_polynomial_and_nonfinite_failure():
    h = torch.tensor([[4., 1.], [1., -2.]], dtype=torch.double)
    rhs = torch.tensor([2., -1.], dtype=torch.double)
    delta, trace, steps, status, _ = measured_series(lambda v: h@v, rhs, 20, 6., 0.)
    transition = torch.eye(2, dtype=h.dtype)-h/6
    for t, row in enumerate(trace):
        reference = sum(torch.linalg.matrix_power(transition,j)@rhs for j in range(t+1))/6
        assert row['relative_residual'] == pytest.approx(float((h@reference-rhs).norm()/rhs.norm()))
    torch.testing.assert_close(delta, reference)
    assert steps == 20 and status == 'finite_truncation'
    bad = measured_series(lambda v: v*float('nan'),rhs,20,6.,0.)
    assert bad[0] is None and bad[3]=='nonfinite_hvp_or_residual'
    spectrum=lanczos(lambda v:h@v,2,'cpu',steps=2)
    for row in spectrum['starts']:
        assert row['minimum']['value']==pytest.approx(float(torch.linalg.eigvalsh(h)[0]))
        assert row['maximum']['ritz_residual']<1e-12


@pytest.mark.parametrize('method',['GIF','IDEA'])
@pytest.mark.parametrize('width',[64,16])
def test_real_adapter_capture_preserves_model_and_fixed_hessian(tables, method, width):
    from experiments.modular_run import read_dataset
    from experiments.modular_config import load_instance,unlearning
    from experiments.modular_model import create_model
    from utils.target_checkpoint import state_hash
    root,_,_=tables
    data,_=read_dataset(load_instance(root/'dataset.yaml','dataset_split'),root)
    data.num_classes=2
    for split in ('train','val','test'):
        setattr(data,split+'_indices',getattr(data,split+'_mask').nonzero().flatten().numpy())
    instance=unlearning(dict(kind='unlearning',schema_version=1,method=method,
        model={'hidden_channels':width},
        parameters=dict(iteration=2,scale=1000,damp=0)))
    model=create_model(instance['model'],'Cora',data,'cpu').eval()
    before=state_hash(model.state_dict())
    system=capture_system(instance,model,data,[8],root)
    assert state_hash(model.state_dict())==before
    params=list(model.parameters())
    loss=torch.nn.functional.cross_entropy(model.reason_once(data)[data.train_mask],data.y[data.train_mask],reduction='sum')
    gradients=torch.autograd.grad(loss,params,create_graph=True)
    sizes=[p.numel() for p in params]
    vector=system['rhs'].detach()
    expected=flat(torch.autograd.grad(gradients,params,grad_outputs=[v.reshape_as(p) for v,p in zip(vector.split(sizes),params)]))
    torch.testing.assert_close(system['matvec'](vector),expected,rtol=1e-4,atol=1e-6)
