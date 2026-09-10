"""GIF's fixed-budget inverse-Hessian approximation (paper Eq. 24).

Residuals describe approximation accuracy; they do not change the prescribed
number of iterations or gate a finite truncated estimate.
"""
import math

import torch


class GIFNumericalError(RuntimeError):
    def __init__(self, diagnostics):
        self.diagnostics = diagnostics
        super().__init__(f"GIF approximation {diagnostics['status']}; model was not updated")


def solve_gif_system(matvec, rhs, *, iterations, scale, damp, rtol=1e-3):
    """Compute h_0=v, h_(t+1)=v+(1-damp)h_t-Hh_t/scale; delta=h_T/scale.

    The infinite-series target, when it converges, is (H+scale*damp I)delta=v.
    The returned value is the finite series used by GIF, not an exact linear solve.
    rtol only labels the diagnostic residual; no early stop or implicit damping is
    applied. Differentiation through the HVP vector would change this recurrence.
    """
    if (type(iterations) is not int or iterations <= 0
            or not math.isfinite(scale) or scale <= 0
            or not math.isfinite(damp) or not 0 <= damp < 1
            or not math.isfinite(rtol) or not 0 < rtol < 1):
        raise ValueError('invalid GIF approximation parameters')
    rhs = rhs.detach()
    if not torch.isfinite(rhs).all():
        raise ValueError('GIF right-hand side is not finite')
    denominator = float(torch.linalg.vector_norm(rhs.double()))
    shift = scale * damp
    if not math.isfinite(shift):
        raise ValueError('GIF damping shift is not finite')
    trace = []
    diagnostics = dict(solver='GIF.truncated_neumann', equation='(H + scale*damp I) delta = v',
                       scale=scale, damp=damp, shift=shift, rtol=rtol,
                       rtol_role='diagnostic_only', max_iterations=iterations,
                       rhs_l2=denominator, trace=trace)

    def fail(step):
        diagnostics.update(status='nonfinite', iterations=step, relative_residual=None)
        raise GIFNumericalError(diagnostics)

    def product(vector, step):
        with torch.enable_grad():
            value = matvec(vector.detach()).detach()
        if not torch.isfinite(value).all():
            fail(step)
        return value

    def record(estimate, step):
        delta = estimate / scale
        curvature = product(delta, step)
        residual = rhs - curvature - shift * delta
        if not torch.isfinite(delta).all() or not torch.isfinite(residual).all():
            fail(step)
        relative = float(torch.linalg.vector_norm(residual.double())) / denominator
        undamped = float(torch.linalg.vector_norm((rhs-curvature).double())) / denominator
        trace.append(dict(iteration=step, relative_residual=relative,
                          undamped_relative_residual=undamped))
        diagnostics.update(iterations=step, relative_residual=relative,
                           undamped_relative_residual=undamped,
                           residual_within_tolerance=relative <= rtol)
        return delta.detach()

    if denominator == 0:
        diagnostics.update(status='zero_rhs', iterations=0, relative_residual=0.,
                           undamped_relative_residual=0., residual_within_tolerance=True)
        return torch.zeros_like(rhs), diagnostics
    estimate = rhs.clone()
    record(estimate, 0)
    for step in range(1, iterations + 1):
        curvature = product(estimate, step)
        with torch.no_grad():
            estimate = rhs + (1-damp)*estimate - curvature/scale
        if not torch.isfinite(estimate).all():
            fail(step)
        if step % 10 == 0 or step == iterations:
            delta = record(estimate, step)
    diagnostics['status'] = 'finite_truncation'
    return delta, diagnostics
