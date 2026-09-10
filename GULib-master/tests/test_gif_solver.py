"""Independent explicit-matrix references for GIF's finite approximation."""
import pytest
import torch

from unlearning.unlearning_methods.GIF.solver import GIFNumericalError, solve_gif_system


@pytest.mark.parametrize('damp', [0., .2])
@pytest.mark.parametrize('steps', [1, 4, 100])
def test_fixed_budget_matches_explicit_matrix_polynomial(damp, steps):
    # Includes negative curvature: finite GIF remains defined even when its
    # infinite Neumann series does not converge. No replacement inverse/shift.
    h = torch.tensor([[4., 1.], [1., -2.]], dtype=torch.double)
    p = torch.tensor([.2, -.3], dtype=torch.double, requires_grad=True)
    gradient, = torch.autograd.grad(.5*p@h@p, p, create_graph=True)
    rhs = torch.tensor([2., -1.], dtype=torch.double, requires_grad=True)
    def hvp(v):
        assert not v.requires_grad
        result, = torch.autograd.grad(gradient@v, p, retain_graph=True)
        torch.testing.assert_close(result, h@v)
        return result
    delta, info = solve_gif_system(hvp, rhs, iterations=steps, scale=6., damp=damp)
    transition = (1-damp)*torch.eye(2, dtype=h.dtype)-h/6
    reference = sum(torch.linalg.matrix_power(transition, j)@rhs.detach()
                    for j in range(steps+1))/6
    torch.testing.assert_close(delta, reference)
    assert info['iterations'] == steps
    assert info['status'] == 'finite_truncation'
    assert info['shift'] == 6*damp
    assert not delta.requires_grad
    expected = torch.linalg.vector_norm(rhs-(h+6*damp*torch.eye(2))@delta)/rhs.norm()
    assert info['relative_residual'] == pytest.approx(float(expected))


def test_large_scale_reports_truncation_instead_of_claiming_an_inverse():
    delta, info = solve_gif_system(lambda v: 2*v, torch.ones(2), iterations=100, scale=1e9, damp=0.)
    torch.testing.assert_close(delta, torch.full((2,), 101/1e9), rtol=1e-5, atol=1e-12)
    assert info['relative_residual'] > .999
    assert not info['residual_within_tolerance']
    assert info['rtol_role'] == 'diagnostic_only'


def test_tolerance_does_not_change_finite_iteration_or_early_stop():
    h = torch.diag(torch.tensor([1., 2.], dtype=torch.double))
    rhs = torch.ones(2, dtype=torch.double)
    a, first = solve_gif_system(lambda v:h@v, rhs, iterations=10, scale=3., damp=0., rtol=.9)
    b, second = solve_gif_system(lambda v:h@v, rhs, iterations=10, scale=3., damp=0., rtol=1e-12)
    torch.testing.assert_close(a, b, rtol=0, atol=0)
    assert first['iterations'] == second['iterations'] == 10
    assert first['residual_within_tolerance'] and not second['residual_within_tolerance']


def test_nonfinite_and_zero_rhs():
    with pytest.raises(GIFNumericalError):
        solve_gif_system(lambda v:v*float('nan'), torch.ones(2), iterations=2, scale=1., damp=0.)
    solution, info = solve_gif_system(lambda v:v, torch.zeros(2), iterations=2, scale=1., damp=0.)
    assert torch.count_nonzero(solution)==0 and info['relative_residual']==0


def test_cross_entropy_hvp_and_long_convergent_series_match_exact_solve():
    x=torch.tensor([[1.,2.],[-1.,.5],[.3,-.2]],dtype=torch.double)
    y=torch.tensor([0,1,0])
    weights=torch.tensor([[.2,-.4],[.1,.3]],dtype=torch.double,requires_grad=True)
    loss=lambda w:torch.nn.functional.cross_entropy(x@w,y,reduction='sum')
    h=torch.autograd.functional.hessian(loss,weights).reshape(4,4)
    gradient,=torch.autograd.grad(loss(weights),weights,create_graph=True)
    rhs=torch.tensor([1.,-1.,.5,-.5],dtype=torch.double)
    def hvp(v):
        value,=torch.autograd.grad((gradient*v.reshape_as(weights)).sum(),weights,retain_graph=True)
        torch.testing.assert_close(value.flatten(),h@v)
        return value.flatten()
    delta,info=solve_gif_system(hvp,rhs,iterations=300,scale=10.,damp=.1)
    torch.testing.assert_close(delta,torch.linalg.solve(h+torch.eye(4),rhs),rtol=1e-8,atol=1e-8)
    assert info['relative_residual'] < 1e-9
    mean_delta,_=solve_gif_system(lambda v:hvp(v)/3,rhs/3,iterations=300,scale=10./3,damp=.1)
    torch.testing.assert_close(mean_delta,delta)
