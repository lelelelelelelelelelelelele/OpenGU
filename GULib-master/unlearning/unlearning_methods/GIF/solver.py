"""Checked MINRES solve for GIF's (H + scale*damp I) delta = v.

The loss and parameter population belong to GIF. This routine never changes
the equation, chooses damping, or uses downstream predictive performance.
"""
import math

import numpy as np
from scipy.sparse.linalg import LinearOperator, minres
import torch


class GIFConvergenceError(RuntimeError):
    def __init__(self, diagnostics):
        self.diagnostics = diagnostics
        super().__init__(f"GIF solve {diagnostics['status']}: residual="
                         f"{diagnostics['relative_residual']}; model was not updated")


def solve_gif_system(matvec, rhs, *, iterations, scale, damp, rtol=1e-3):
    """Return a finite solution and residual trace, or fail before model writes.

    MINRES permits a symmetric indefinite Hessian without changing the target
    equation. Neither its internal stopping test nor a small parameter step
    substitutes for our explicit relative residual on the returned tensor.
    scale*damp is an explicit shift; no implicit regularization is added.
    """
    if (type(iterations) is not int or iterations <= 0
            or not math.isfinite(scale) or scale <= 0
            or not math.isfinite(damp) or not 0 <= damp < 1
            or not math.isfinite(rtol) or not 0 < rtol < 1):
        raise ValueError('invalid GIF solver parameters')
    rhs = rhs.detach()
    if not torch.isfinite(rhs).all():
        raise ValueError('GIF right-hand side is not finite')
    denominator = float(torch.linalg.vector_norm(rhs.double()))
    shift = scale * damp
    if not math.isfinite(shift):
        raise ValueError('GIF damping shift is not finite')
    delta = rhs / scale
    trace = []
    diagnostics = dict(solver='scipy.MINRES', equation='(H + scale*damp I) delta = v',
                       scale=scale, damp=damp, shift=shift, rtol=rtol,
                       max_iterations=iterations, rhs_l2=denominator, trace=trace)
    if denominator == 0:
        diagnostics.update(status='converged', iterations=0, relative_residual=0.0)
        return torch.zeros_like(rhs), diagnostics
    def check(vector, step):
        with torch.enable_grad():
            curvature = matvec(vector.detach()).detach()
        residual = rhs - curvature - shift * vector
        finite = bool(torch.isfinite(vector).all() and torch.isfinite(residual).all())
        relative = float(torch.linalg.vector_norm(residual.double())) / denominator if finite else None
        if step == 0 or step % 10 == 0 or step == iterations or not finite or relative <= rtol:
            trace.append(dict(iteration=step, relative_residual=relative))
        diagnostics.update(iterations=step, relative_residual=relative)
        if not finite:
            diagnostics['status'] = 'nonfinite'
            raise GIFConvergenceError(diagnostics)
        if relative <= rtol:
            diagnostics['status'] = 'converged'
            return True
        return False

    if check(delta, 0):
        return delta.detach(), diagnostics

    def tensor(vector):
        return torch.as_tensor(vector, device=rhs.device, dtype=rhs.dtype).detach()

    def product(vector):
        current = tensor(vector)
        with torch.enable_grad():
            value = matvec(current).detach() + shift * current
        if not torch.isfinite(value).all():
            diagnostics.update(status='nonfinite', relative_residual=None)
            raise GIFConvergenceError(diagnostics)
        return value.double().cpu().numpy()

    operator = LinearOperator((rhs.numel(), rhs.numel()), matvec=product, dtype=np.float64)
    state = {'step': 0, 'solution': None}

    class ResidualReached(Exception):
        pass

    def callback(vector):
        state['step'] += 1
        current = tensor(vector)
        if check(current, state['step']):
            state['solution'] = current.clone()
            raise ResidualReached()

    try:
        # Both registered runtimes use SciPy 1.10.1. Its internal tolerance is
        # intentionally tighter: only check() decides our residual acceptance.
        solution, info = minres(operator, rhs.double().cpu().numpy(),
            x0=delta.double().cpu().numpy(), tol=np.finfo(np.float64).eps,
            maxiter=iterations, callback=callback)
        delta = tensor(solution)
        diagnostics['library_info'] = int(info)
    except ResidualReached:
        delta = state['solution']
        diagnostics['library_info'] = 0
    if check(delta, state['step']):
        return delta.detach(), diagnostics
    diagnostics['status'] = 'not_converged'
    raise GIFConvergenceError(diagnostics)
