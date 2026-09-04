"""The method recipe must track actual dependencies without bundle pollution."""
import copy
import torch
from torch_geometric.data import Data
from experiments.c_target_v1.core import GateGCN, capture_state
from experiments.target_direct_v1.methods import Computations, resolve_parameters
from experiments.target_direct_v1.recipe import build_recipe


def test_only_trajectory_consumers_bind_changed_checkpoint():
    torch.manual_seed(5)
    model = GateGCN(3, 4, 2, .5)
    data = Data(x=torch.randn(8, 3), y=torch.arange(8) % 2,
        edge_index=torch.tensor([[0,1,2,3],[1,2,3,4]]),
        train_mask=torch.arange(8)<4, val_mask=(torch.arange(8)>=4)&(torch.arange(8)<6), test_mask=torch.arange(8)>=6)
    checkpoints = [{'global_step': i+1, 'update_lr': .01, 'state': capture_state(model)} for i in range(6)]
    c = Computations(model, data, checkpoints)
    def identity(name):
        return build_recipe(name=name, computations=c, parameters=resolve_parameters(name))[0].recipe_hash
    names = ['degree', 'b_param_hutch', 'tracin_cp_point_3', 'tracin_cp_point_6']
    before = [identity(name) for name in names]
    key = next(iter(checkpoints[1]['state']))
    checkpoints[1]['state'][key].add_(.1)
    after = [identity(name) for name in names]
    assert [a == b for a, b in zip(before, after)] == [True, True, True, False]
    fields = build_recipe(name='degree', computations=c, parameters={})[0].fields
    assert 'selector_model' not in fields and 'training' not in fields
