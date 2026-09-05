"""Read-only Metrics CLI over explicit, verified GU and Retrain outputs.

No data preparation, selection, model forward pass or training is performed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from types import SimpleNamespace
import numpy as np

from experiments.modular_config import load_instance
from experiments.modular_evaluation import evaluate_modular
from experiments.unlearning_outputs import load_output


def evaluate_outputs(evaluation, pairs, *, store_root, output_dir):
    output_dir = Path(output_dir)
    targets = [output_dir / name for name in ('collateral.json', 'predictions.npz')]
    if any(path.exists() for path in targets):
        raise FileExistsError('Metrics output already exists; select a new output directory')
    annotations = [pair['strategy'] for pair in pairs]
    if len(set(annotations)) != len(annotations):
        raise ValueError('each comparison needs a unique annotation; do not overwrite method predictions')
    evaluated = evaluate_modular(evaluation, pairs, store_root=store_root)
    if len(evaluated['rows']) != len(pairs):
        raise ValueError('each Metrics pair must name one GU and one Retrain output')
    rows, arrays = [], {}
    from experiments.gate3_degree_adapter import _scalar_metrics_from_prediction
    for pair, row in zip(pairs, evaluated['rows']):
        gu = load_output(pair['unlearning'], store_root)
        retrain = load_output(pair['retrain'], store_root)
        strategy = pair['strategy']
        if not isinstance(strategy, str) or not strategy or '/' in strategy or '__' in strategy:
            raise ValueError('invalid strategy annotation')
        a, r = gu.arrays, retrain.arrays
        bundle = dict(logits_before=a['logits_before'], logits_unlearned=a['logits'],
                      logits_retrained=r['logits'], y=a['y'], test_mask=a['test_mask'],
                      retain_mask=a['retain_mask'], selected_nodes=a['selected_nodes'])
        # This existing evaluator consumes arrays only, despite its Prediction type hint.
        diagnostics = _scalar_metrics_from_prediction(SimpleNamespace(**bundle))
        rows.append({'strategy': strategy, **row['metrics'],
                     **{k: diagnostics[k] for k in ('mean_pred_shift', 'max_pred_shift', 'fraction_flipped')},
                     'evaluation_receipt_id': row['evaluation_receipt_id'], 'identity': row['identity']})
        arrays.update({strategy + '__' + key: value for key, value in bundle.items()})
        for key in ('train_mask', 'evaluation_edge_index'):
            arrays[strategy + '__' + key] = a[key]
    output = {'schema': 'opengu.output_metrics', 'version': 1,
              'evaluation': evaluation, 'results': rows, 'training_producer_called': False}
    output_dir.mkdir(parents=True, exist_ok=True)
    with targets[0].open('x', encoding='utf-8') as handle:
        json.dump(output, handle, indent=2, allow_nan=False)
        handle.write('\n')
    with targets[1].open('xb') as handle:
        np.savez(handle, **arrays)
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store-root', type=Path, required=True)
    parser.add_argument('--inputs', type=Path, required=True, help='JSON list of strategy / unlearning / retrain references')
    parser.add_argument('--evaluation', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args(argv)
    pairs = json.loads(args.inputs.read_text(encoding='utf-8'))
    result = evaluate_outputs(load_instance(args.evaluation, 'evaluation'), pairs,
                              store_root=args.store_root, output_dir=args.output_dir)
    print(json.dumps({'rows': len(result['results']), 'training_producer_called': False}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
