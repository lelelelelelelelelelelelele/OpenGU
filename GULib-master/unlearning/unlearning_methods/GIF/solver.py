"""Checked Richardson solve for GIF's (H + scale*damp I) delta = v.

The loss and parameter population belong to GIF. This routine never changes
the equation, chooses damping, or uses downstream predictive performance.
"""
import math

import torch


class GIFConvergenceError(RuntimeError):
    def __init__(self, diagnostics):
        self.diagnostics = diagnostics
        super().__init__(f"GIF solve {diagnostics['status']}: residual="
                         f"{diagnostics['relative_residual']}; model was not updated")


def solve_gif_system(matvec, rhs, *, iterations, scale, damp, rtol=1e-3):
    """Return a finite solution and residual trace, or fail before model writes.

    With delta_0=v/scale, the historical h recurrence divided by scale is
    delta_{t+1}=delta_t+(v-(H+scale*damp I)delta_t)/scale.
    Convergence requires the iteration operator's spectral radius below one.
    A small step or unchanged F1 is not a convergence criterion.
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
    diagnostics = dict(equation='(H + scale*damp I) delta = v',
                       scale=scale, damp=damp, shift=shift, rtol=rtol,
                       max_iterations=iterations, rhs_l2=denominator, trace=trace)
    if denominator == 0:
        diagnostics.update(status='converged', iterations=0, relative_residual=0.0)
        return torch.zeros_like(rhs), diagnostics
    for step in range(iterations + 1):
        with torch.enable_grad():
            curvature = matvec(delta).detach()
        residual = rhs - curvature - shift * delta
        finite = bool(torch.isfinite(delta).all() and torch.isfinite(residual).all())
        relative = float(torch.linalg.vector_norm(residual.double())) / denominator if finite else None
        if step == 0 or step % 10 == 0 or step == iterations or not finite or relative <= rtol:
            trace.append(dict(iteration=step, relative_residual=relative))
        diagnostics.update(iterations=step, relative_residual=relative)
        if not finite:
            diagnostics['status'] = 'nonfinite'
            raise GIFConvergenceError(diagnostics)
        if relative <= rtol:
            diagnostics['status'] = 'converged'
            return delta.detach(), diagnostics
        if step < iterations:
            delta = (delta + residual / scale).detach()
    diagnostics['status'] = 'not_converged'
    raise GIFConvergenceError(diagnostics)
