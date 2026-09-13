"""Bounded AAGU-052 CPU verification against an independent autograd recurrence."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import sys
import time
from unittest.mock import patch

import numpy as np
import torch
from torch_geometric.datasets import Planetoid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from aagu052_local_if_debug import (split_real_cora, common_args, state_copy,
    parameter_vector, f1_and_logits, metrics)


def tensor_hash(value):
    return hashlib.sha256(value.detach().cpu().contiguous().numpy().tobytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--calibration', type=Path, required=True)
    opts = parser.parse_args()
    assert (opts.data / 'Cora/processed/data.pt').is_file(), 'existing local diagnostic graph required'
    out = opts.output.resolve()
    out.relative_to(ROOT / 'results/diagnostics/AAGU-052')
    out.mkdir(parents=True, exist_ok=False)
    sys.argv = ['verify_if_production']
    torch.set_num_threads(2)
    from attack.cache_identity import seeded_execution
    from experiments.modular_model import create_model, runtime_defaults
    from experiments.modular_gu import gif_node, gu_producer
    from experiments.modular_idea import idea_node
    from unlearning.unlearning_methods.GIF.gif import gif
    from unlearning.unlearning_methods.IDEA.idea import idea

    data = split_real_cora(Planetoid(str(opts.data), 'Cora')[0], 2024)
    data.num_classes = int(data.y.max()) + 1
    config = dict(architecture='OpenGU.GCNNet', layers=2, hidden_channels=8)
    training = dict(epochs=30, optimizer='Adam', lr=.005, weight_decay=.000001, seed=42)
    with seeded_execution(42):
        model = create_model(config, 'Cora', data, torch.device('cpu'))
    model.load_state_dict(torch.load(opts.checkpoint, map_location='cpu', weights_only=True))
    calibration = json.loads(opts.calibration.read_text())
    assert hashlib.sha256(opts.checkpoint.read_bytes()).hexdigest() == calibration['checkpoint_sha256']
    parameters = calibration['parameters']
    budget = parameters['iteration']
    scale, damp = parameters['scale'], parameters['damp']
    state = state_copy(model)
    _, logits = f1_and_logits(model, data)
    torch.save(state, out / 'checkpoint.pt')
    nodes = data.train_indices
    requests = [nodes[:18].tolist(), nodes[18:36].tolist()]
    report = dict(level='local CPU verification, not formal experiment', model=config,
        training=training, graph_hash=tensor_hash(data.edge_index), x_hash=tensor_hash(data.x),
        y_hash=tensor_hash(data.y), train_mask_hash=tensor_hash(data.train_mask),
        test_mask_hash=tensor_hash(data.test_mask), checkpoint_hash=tensor_hash(parameter_vector(model)),
        normalization='sum CE on original supervised population; raw graph normalized by trained model',
        standard_parameters=parameters, calibration=calibration,
        noise='IDEA mean=std=0 for deterministic update verification; no certification claim', cases=[])
    for name, cls, adapter in [('GIF', gif, gif_node), ('IDEA', idea, idea_node)]:
        outputs = []
        for request_index, steps in [(0,budget),(1,budget),(0,2*budget)]:
            selected = requests[request_index]
            args = common_args(runtime_defaults, method=name,
                parameters=dict(iteration=steps, scale=scale, damp=damp),
                model_config=config, training=training, k=len(selected))
            runtime = out / f'{name}-{request_index}-{steps}'
            runtime.mkdir()
            target = copy.deepcopy(model)
            initial = parameter_vector(target)
            verification = {}
            original = cls.approxi

            def checked(self, gradients):
                params = [p for p in self.target_model.model.parameters() if p.requires_grad]
                rhs = tuple((a-b).detach() for a,b in zip(gradients[1], gradients[2]))
                # Reference H uses the actual trained forward, independently of
                # either method's HVP helper and shared finite-series solver.
                raw = self.target_model.model(self.data.x, self.data.edge_index)
                loss = torch.nn.functional.cross_entropy(raw[self.data.train_mask],
                    self.data.y[self.data.train_mask], reduction='sum')
                train_grad = torch.autograd.grad(loss, params, create_graph=True)
                for actual, expected in zip(gradients[0], train_grad):
                    torch.testing.assert_close(actual, expected, rtol=1e-4, atol=1e-5)
                h = [v.clone() for v in rhs]
                for _ in range(steps):
                    hv = torch.autograd.grad(train_grad, params,
                        grad_outputs=tuple(h), retain_graph=True)
                    h = [(v + (1-damp)*old - curvature / scale).detach()
                         for v,old,curvature in zip(rhs,h,hv)]
                expected = [p.detach()+v/scale for p,v in zip(params,h)]
                expected_vector = torch.cat([p.flatten() for p in expected])
                result = original(self, gradients)
                actual_vector = parameter_vector(self.target_model.model)
                torch.testing.assert_close(actual_vector, expected_vector, rtol=1e-5, atol=2e-7)
                verification.update(reference_max_abs=float((actual_vector-expected_vector).abs().max()),
                    actual_training_gradient_match=True, rhs_l2=float(torch.cat([v.flatten() for v in rhs]).norm()),
                    deleted_edges_match=not bool(torch.isin(self.data.edge_index_unlearn,
                        torch.tensor(selected)).any()))
                assert verification['deleted_edges_match']
                return result

            started = time.perf_counter()
            with patch.object(cls, 'approxi', checked), seeded_execution(42):
                updated, _ = adapter(args, target, data.clone(), selected, runtime)
            info = json.loads((runtime / f'{name.lower()}-solver.json').read_text())
            delta = parameter_vector(updated)-initial
            assert torch.isfinite(delta).all() and delta.norm() > 0
            row = dict(method=name, request=selected, iterations=steps, scale=scale, damp=damp,
                seconds=time.perf_counter()-started, verification=verification,
                metrics=metrics(updated,data,state,logits), solver=info,
                producer=gu_producer(name,config).to_dict())
            report['cases'].append(row)
            if steps == budget:
                outputs.append(delta)
            (out/'result.json').write_text(json.dumps(report,indent=2,allow_nan=False),encoding='utf-8')
            print(json.dumps(dict(method=name,request=request_index,steps=steps,
                delta=float(delta.norm()),residual=info['relative_residual'],verification=verification)),flush=True)
        assert not torch.equal(*outputs), 'update must respond to the deletion request'
        first, _, doubled = report['cases'][-3:]
        for row in report['cases'][-3:]:
            assert row['solver']['relative_residual'] < 1e-3
        standard_delta = outputs[0]
        stability = float((delta-standard_delta).norm()/standard_delta.norm())
        assert stability < 1e-3, stability
        doubled['budget_doubling_relative_update_difference'] = stability
    report['status']='PASS'
    (out/'result.json').write_text(json.dumps(report,indent=2,allow_nan=False),encoding='utf-8')


if __name__ == '__main__':
    main()
