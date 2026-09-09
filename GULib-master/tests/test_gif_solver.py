"""Numerical reference problems independent of the OpenGU CLI/model stack."""
import pytest
import torch

from unlearning.unlearning_methods.GIF.solver import GIFConvergenceError, solve_gif_system


@pytest.mark.parametrize('damp', [0., .2])
def test_autograd_hvp_and_solution_match_explicit_reference(damp):
    h = torch.tensor([[4., 1.], [1., 2.]], dtype=torch.double)
    p = torch.tensor([.2, -.3], dtype=torch.double, requires_grad=True)
    gradient, = torch.autograd.grad(.5 * p @ h @ p, p, create_graph=True)
    def hvp(v):
        result, = torch.autograd.grad(gradient @ v, p, retain_graph=True)
        torch.testing.assert_close(result, h @ v)
        return result
    v = torch.tensor([2., -1.], dtype=torch.double)
    solution, info = solve_gif_system(hvp, v, iterations=200, scale=6., damp=damp, rtol=1e-10)
    reference = torch.linalg.solve(h + 6*damp*torch.eye(2, dtype=h.dtype), v)
    torch.testing.assert_close(solution, reference, rtol=1e-9, atol=1e-9)
    assert info['relative_residual'] < 1e-10
    if damp:
        assert float((h @ solution-v).norm()/v.norm()) > .1


def test_old_scale_rejected_despite_finite_tiny_update():
    with pytest.raises(GIFConvergenceError) as error:
        solve_gif_system(lambda v: 2*v, torch.ones(2), iterations=100, scale=1e9, damp=0.)
    assert error.value.diagnostics['relative_residual'] > .999


def test_negative_curvature_needs_explicit_shift():
    h = torch.diag(torch.tensor([-1., 3.], dtype=torch.double))
    rhs = torch.ones(2, dtype=torch.double)
    with pytest.raises(GIFConvergenceError):
        solve_gif_system(lambda v: h@v, rhs, iterations=100, scale=5., damp=0.)
    delta, info = solve_gif_system(lambda v: h@v, rhs, iterations=100, scale=5., damp=.4)
    torch.testing.assert_close(delta, torch.linalg.solve(h+2*torch.eye(2),rhs), rtol=.002, atol=.002)
    assert info['shift'] == 2.


def test_nonfinite_and_zero_rhs():
    with pytest.raises(GIFConvergenceError):
        solve_gif_system(lambda v: v*float('nan'), torch.ones(2), iterations=2, scale=1., damp=0.)
    solution, info = solve_gif_system(lambda v: v, torch.zeros(2), iterations=2, scale=1., damp=0.)
    assert torch.count_nonzero(solution)==0 and info['relative_residual']==0


def test_cross_entropy_sum_mean_and_explicit_hessian_agree():
    x=torch.tensor([[1.,2.],[-1.,.5],[.3,-.2]],dtype=torch.double)
    y=torch.tensor([0,1,0])
    weights=torch.tensor([[.2,-.4],[.1,.3]],dtype=torch.double,requires_grad=True)
    loss=lambda w: torch.nn.functional.cross_entropy(x@w,y,reduction='sum')
    h=torch.autograd.functional.hessian(loss,weights).reshape(4,4)
    gradient,=torch.autograd.grad(loss(weights),weights,create_graph=True)
    rhs=torch.tensor([1.,-1.,.5,-.5],dtype=torch.double)
    def hvp(v):
        value,=torch.autograd.grad((gradient*v.reshape_as(weights)).sum(),weights,retain_graph=True)
        torch.testing.assert_close(value.flatten(),h@v)
        return value.flatten()
    delta,_=solve_gif_system(hvp,rhs,iterations=300,scale=10.,damp=.1,rtol=1e-9)
    torch.testing.assert_close(delta,torch.linalg.solve(h+torch.eye(4),rhs),rtol=1e-8,atol=1e-8)
    mean_delta,_=solve_gif_system(lambda v:hvp(v)/3,rhs/3,iterations=300,scale=10./3,damp=.1,rtol=1e-9)
    torch.testing.assert_close(mean_delta,delta)
