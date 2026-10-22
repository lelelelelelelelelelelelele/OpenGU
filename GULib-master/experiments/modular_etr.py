"""Exact Selection adapter for ETR's two-stage node parameter edit."""
from unlearning.unlearning_methods.ETR.etr import run_etr


def etr_node(args, model, data, nodes, runtime_root, observer=None):
    if observer is not None:
        raise ValueError('ETR does not provide Observer events')
    return run_etr(model, data, nodes, erase_ratio=args['etr_erase_ratio'], coefficient=args['etr_l'])
