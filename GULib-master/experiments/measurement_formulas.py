"""Scientific calculations only; audit and cache orchestration are excluded."""
import numpy as np
from experiments.effective_config import ConfigurationError


def utility_metrics(output):
    from experiments.unlearning_outputs import utility
    values = utility(output)
    return {**values, 'f1_drop_pct': values['f1_drop_ratio']}, {}


def retrain_gap(output, retrain):
    from experiments.unlearning_outputs import utility
    for name in ('y', 'test_mask', 'evaluation_edge_index'):
        if not np.array_equal(output.arrays[name], retrain.arrays[name]):
            raise ConfigurationError('paired output evaluation inputs differ')
    values = utility(output)
    perf = utility(retrain)['f1_after']
    gap = perf - values['f1_after']
    return dict(perf_before=values['f1_before'], perf_unlearn=values['f1_after'], perf_retrain=perf,
        drop_retrain=values['f1_before']-perf, gap=gap, gap_pct=gap/perf*100 if perf > 0 else 0.0), {}


def flip_metrics(output, retrain):
    from experiments.flip_hop_metrics import exact_retrain, flip_hop
    exact_retrain(output, [(None, retrain)])
    return flip_hop(output, retrain)


def method_values(reference, output):
    from experiments.output_metrics import evaluate_method
    measured = evaluate_method(reference, output)
    return measured['metrics'], measured['identity']
