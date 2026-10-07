"""Bounded, run-owned reuse of verified initial models; consumers get private copies."""
from copy import deepcopy
from cache_v2 import canonical_sha256


class PreparedModels:
    def __init__(self, prepare):
        self.prepare = prepare
        self.group = None
        self.models = {}

    def select_group(self, group):
        # Keep only one Dataset/Split and training seed resident, even in large matrices.
        if group != self.group:
            self.models.clear()
            self.group = group

    def get(self, instance, **kwargs):
        identity = {key: instance.get(key) for key in ('model', 'training', 'checkpoint')}
        if instance.get('kind') == 'selector' and instance['method'].startswith('tracin_cp_'):
            from experiments.model_trajectory import trajectory_steps
            identity['trajectory_steps'] = trajectory_steps(instance)
        key = canonical_sha256(identity)
        reused = key in self.models
        if not reused:
            self.models[key] = self.prepare(instance, **kwargs)
        model, checkpoints, observation = deepcopy(self.models[key])
        if reused:
            observation['hit'] = True
        return model, checkpoints, observation
