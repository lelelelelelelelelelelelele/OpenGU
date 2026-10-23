"""CPU-only audit of collected fixed-checkpoint GIF/IDEA validation evidence.

Reads immutable indexed run files; writes only beside this script. No training,
remote access, experiment-state edit, or V2 Artifact modification.
"""
from pathlib import Path
from collections import defaultdict
import csv
import hashlib
import json
import statistics

OUT = Path(__file__).resolve().parent
ROOT = next(p for p in OUT.parents if (p / 'experiments/modular_run.py').exists())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                     allow_nan=False) + '\n', encoding='utf-8')


def main():
    index_path = ROOT / '.syncmate/artifact_index.json'
    index = {x['path']: x for x in read(index_path)['peers']['gpu4090']['items']}
    specs = [('EXP-066', 'Cora', 16, 'validation-h16-20260924.json'),
             ('EXP-066', 'Cora', 64, 'validation-h64-20260924.json'),
             ('EXP-067', 'CiteSeer', 64, 'validation-h64-20260924.json'),
             ('EXP-068', 'PubMed', 64, 'validation-h64-20260924.json')]
    provenance, all_rows, run_proofs = [], [], []
    for exp, dataset, width, filename in specs:
        analysis_path = ROOT / 'self/research/analyses' / exp / filename
        analysis = read(analysis_path)
        matches = [x for x in index.values() if x['path'].endswith('/run.json')
                   and '/' + analysis['run_id'] + '/' in x['path']]
        assert len(matches) == 1
        run_entry = matches[0]
        run_path = ROOT / run_entry['local_path']
        prefix = run_entry['path'][:-len('run.json')]
        entries = [v for k, v in index.items() if k.startswith(prefix)]
        for entry in entries:
            path = ROOT / entry['local_path']
            digest = sha(path)
            assert digest == entry['sha256'], path
            provenance.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=digest,
                                   indexed_path=entry['path']))
        run = read(run_path)
        assert sha(run_path) == analysis['run_sha256']
        assert run['status'] == 'completed' and len(run['cells']) == 21
        assert run['commit'] == analysis.get('execution_sha', analysis.get('commit'))
        run_proofs.append(dict(experiment=exp, dataset=dataset, width=width,
                              run_id=run['run_id'], execution_sha=run['commit'],
                              run_path=run_path.relative_to(ROOT).as_posix(),
                              run_sha256=sha(run_path), verified_files=len(entries),
                              analysis_path=analysis_path.relative_to(ROOT).as_posix(),
                              analysis_sha256=sha(analysis_path)))
        cells = []
        retrains = {}
        for cell in run['cells']:
            assert cell['status'] == 'completed'
            folder = run_path.parent / cell['path']
            for name, meta in cell['files'].items():
                assert sha(folder / name) == meta['sha256']
                assert index[prefix + cell['path'] + '/' + name]['sha256'] == meta['sha256']
            c = cell['conditions']
            assert c['seed'] == 42 and c['budget_ratio'] == .1 and c['selector'] == 'random'
            request = c['random_selector_seed']
            metrics = {r['stage']: r['values'] for r in read(folder / 'metrics.json')['rows']}
            selection = read(folder / 'selection.json')['selected_nodes']
            if c['method'] == 'Retrain':
                retrains[request] = (metrics['method']['accuracy'], selection)
                continue
            change = read(folder / 'observers/same_graph_change/result.json')
            calib = read(folder / 'observers/hessian_calibration/calibration.json')
            trace = [json.loads(line) for line in
                     (folder / 'observers/linear_solver_trace/trace.jsonl').read_text(encoding='utf-8').splitlines()]
            ident = change['identity']['output_identity']
            assert ident['pairing']['model']['hidden_channels'] == width
            assert ident['pairing']['deletion']['evaluation_graph'] == 'original'
            assert ident['pairing']['training']['seed'] == 42
            params = ident['target']['parameters']
            iterations = params['iteration']
            assert trace[-1]['step'] == iterations and trace[-1]['finite']
            g, h, t = change['measurements'], calib['measurements'], trace[-1]
            assert abs(metrics['method']['accuracy'] - g['graphs']['original']['accuracy']) < 1e-6
            row = dict(experiment=exp, dataset=dataset, hidden=width, training_seed=42,
                       random_request_seed=request, ratio=.1, method=c['method'], T=iterations,
                       cell_id=cell['cell_id'], selection_id=cell['selection_id'],
                       checkpoint_state_hash=ident['target']['checkpoint_state_hash'],
                       scale=params['scale'], damp=params['damp'], shift=params['scale'] * params['damp'],
                       parameter_delta_l2=g['parameter_delta_l2'],
                       parameter_delta_relative_l2=g['parameter_delta_relative_l2'],
                       update_rhs_ratio=t['update_l2'] / t['rhs_l2'],
                       shifted_relative_residual=t['shifted_relative_residual'],
                       original_relative_residual=t['original_relative_residual'],
                       writeback_max_abs_error=h['writeback']['actual_vs_expected_max_abs'],
                       utility_metric='test_accuracy', flip_node_scope='all_nodes',
                       logits_node_scope='all_nodes',
                       source_folder=folder.relative_to(ROOT).as_posix())
            for graph in ['original', 'retained']:
                x = g['graphs'][graph]
                for key in ['accuracy', 'baseline_accuracy', 'prediction_flip_rate',
                            'logits_delta_l2', 'logits_delta_max_abs']:
                    row[graph + '_' + key] = x[key]
                row[graph + '_accuracy_change_pp'] = 100 * (x['accuracy'] - x['baseline_accuracy'])
            cells.append((row, selection))
        assert set(retrains) == {104246, 104247, 104248}
        for row, selection in cells:
            acc, ref_selection = retrains[row['random_request_seed']]
            assert selection == ref_selection
            row['retrain_original_accuracy'] = acc
            row['gu_minus_retrain_original_pp'] = 100 * (row['original_accuracy'] - acc)
            # We have no retained-graph Retrain output in this collected batch.
            row['retrain_retained_accuracy'] = None
            all_rows.append(row)
    assert len(all_rows) == 72
    production = [r for r in all_rows if r['T'] == 100]
    assert len(production) == 24
    groups = defaultdict(list)
    for row in production:
        groups[(row['dataset'], row['hidden'], row['method'])].append(row)
    summaries = []
    fields = ['parameter_delta_l2', 'parameter_delta_relative_l2', 'update_rhs_ratio',
              'shifted_relative_residual', 'original_relative_residual',
              'original_prediction_flip_rate', 'original_logits_delta_max_abs',
              'retained_prediction_flip_rate', 'retained_logits_delta_max_abs',
              'original_accuracy_change_pp', 'retained_accuracy_change_pp',
              'gu_minus_retrain_original_pp']
    for (ds, hidden, method), rows in sorted(groups.items()):
        summary = dict(dataset=ds, hidden=hidden, method=method, independent_training_seeds=1,
                       random_request_draws=3, training_seed=42, ratio=.1, T=100)
        for field in fields:
            values = [r[field] for r in rows]
            summary[field] = dict(mean=statistics.mean(values), min=min(values), max=max(values),
                                  request_sd=statistics.stdev(values))
        summaries.append(summary)
    with (OUT / 'calibration_rows.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_rows[0]))
        writer.writeheader(); writer.writerows(all_rows)
    dump('calibration_summary.json', dict(scope='4 fixed checkpoints, seed42, Random10%, requests104246-104248',
         observed_rows=len(all_rows), production_rows=len(production), summaries=summaries,
         conclusions=dict(nonzero_parameter_updates=all(r['parameter_delta_l2'] > 0 for r in all_rows),
                          nonzero_same_graph_logit_changes=all(r['original_logits_delta_max_abs'] > 1e-8 for r in all_rows),
                          exact_writeback=all(r['writeback_max_abs_error'] == 0 for r in all_rows),
                          shifted_residual_max=max(r['shifted_relative_residual'] for r in all_rows),
                          original_residual_min=min(r['original_relative_residual'] for r in all_rows),
                          original_residual_max=max(r['original_relative_residual'] for r in all_rows)),
         unavailable=['GU vs Original test-only disagreement (observer flips are all-node)',
                      'Original vs Retrain predictive disagreement',
                      'Retained-graph Retrain predictions',
                      'MEGU no-update/C&S control',
                      'main079/080 cell-level same-graph update traces'],
         new_gpu_jobs=0, scientific_acceptance='not_changed'))
    dump('calibration_provenance.json', dict(script_sha256=sha(Path(__file__)),
         trusted_index_sha256=sha(index_path), runs=run_proofs, verified_files=len(provenance),
         sources=provenance, output_csv_sha256=sha(OUT / 'calibration_rows.csv'),
         summary_sha256=sha(OUT / 'calibration_summary.json')))
    print(json.dumps({'verified_files': len(provenance), 'rows': len(all_rows),
                      'production_rows': len(production), 'groups': len(summaries)}))


if __name__ == '__main__':
    main()
