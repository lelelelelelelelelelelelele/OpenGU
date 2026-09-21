"""Read-only comparison of AAGU-065 runs with and without observation."""
import json

from experiments.observers.hessian_calibration import HessianCalibration


def compare_runs(observed_path, control_path, *, dataset_root, store_root):
    """Read completed outputs for the 065 integration check; never execute GU."""
    import hashlib
    from pathlib import Path
    import numpy as np
    from experiments.modular_artifacts import read_run
    from experiments.unlearning_outputs import load_output

    def read(path):
        path = Path(path)
        return read_run(path, hashlib.sha256(path.read_bytes()).hexdigest())

    observed, documents = read(observed_path)
    control, _ = read(control_path)
    if observed['commit'] != control['commit']:
        raise ValueError('observer comparison requires the same code commit')
    key = lambda cell: json.dumps(cell['conditions'], sort_keys=True)
    controls = {key(cell): cell for cell in control['cells']}
    if len(controls) != len(control['cells']) or set(controls) != {key(c) for c in observed['cells']}:
        raise ValueError('observer/control condition sets differ')
    pairs = []
    for cell, document in zip(observed['cells'], documents):
        if not cell.get('observers'):
            continue
        baseline = controls[key(cell)]
        if (cell['selection_id'] != baseline['selection_id']
                or cell['output']['recipe_hash'] != baseline['output']['recipe_hash']):
            raise ValueError('observer/control calculation identities differ')
        actual = load_output(cell['output'], store_root, dataset_root=dataset_root)
        expected = load_output(baseline['output'], store_root, dataset_root=dataset_root)
        same_state = (set(actual.state) == set(expected.state) and
                      all(np.array_equal(actual.state[k], expected.state[k]) for k in actual.state))
        same_logits = np.array_equal(actual.arrays['logits'], expected.arrays['logits'])
        calibration = HessianCalibration.read(document['observers/hessian_calibration/calibration.json'])
        trace = [json.loads(line) for line in document['observers/linear_solver_trace/trace.jsonl'].splitlines()]
        pairs.append(dict(conditions=cell['conditions'], state_equal=same_state, logits_equal=same_logits,
            observer_coverage=calibration['coverage'], calibration=calibration['measurements'],
            final_solver_observation=trace[-1], observed_steps=len(trace)))
    return dict(schema='aagu065.observer_integration.v1', commit=observed['commit'],
        observed_run_id=observed['run_id'], control_run_id=control['run_id'], pairs=pairs,
        production_unchanged=bool(pairs) and all(row['state_equal'] and row['logits_equal'] for row in pairs),
        scope='Observer integration and noninterference; no scientific acceptance decision')


if __name__ == '__main__':
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser(description='Read-only AAGU-065 Observer/control comparison')
    parser.add_argument('--observed', type=Path, required=True)
    parser.add_argument('--control', type=Path, required=True)
    parser.add_argument('--dataset-root', type=Path, required=True)
    parser.add_argument('--store-root', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(compare_runs(args.observed, args.control, dataset_root=args.dataset_root,
                                  store_root=args.store_root), indent=2, allow_nan=False))
