"""Verify the report's numeric tables and source version without running models."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import csv

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
SHA = 'e02b5fa40ebce66fb45e57ea23b8d6c8d7856685'


def records(name):
    with (OUT / name).open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    names = ['experiments/output_metrics.py', 'experiments/flip_hop_metrics.py',
             'experiments/node_deletion.py', 'experiments/modular_gu.py',
             'experiments/modular_megu.py', 'experiments/modular_shards.py',
             'experiments/modular_graphrevoker.py', 'experiments/unlearning_outputs.py',
             'unlearning/unlearning_methods/Retrain/retrain.py']
    checks = []
    for name in names:
        # Git root is the parent OpenGU directory; :./ resolves relative to cwd.
        old = subprocess.run(['git', 'show', SHA + ':./' + name], cwd=ROOT,
                             check=True, capture_output=True).stdout
        current = (ROOT / name).read_bytes()
        equal = old.replace(b'\r\n', b'\n') == current.replace(b'\r\n', b'\n')
        checks.append({'path': name, 'matches_execution_source': equal,
                       'current_sha256': digest(ROOT / name)})
    assert all(c['matches_execution_source'] for c in checks)
    raw = (OUT / 'FIXED_BUDGET_APPENDIX.md').read_text(encoding='utf-8').replace('−', '-')
    coverage = records('coverage_ranges.csv')
    for r in coverage:
        cells = [r['dataset'], r['method']]
        for metric in ['U', 'D']:
            cells.append(f"{float(r[metric+'_mean_min']):.3f} ～ {float(r[metric+'_mean_max']):.3f}")
        assert '| ' + ' | '.join(cells) + ' |' in raw, cells
    summary = records('all_condition_summary.csv')
    for r in summary:
        if r['dataset'] != 'CiteSeer' or r['method'] not in ('GraphEraser', 'GraphRevoker'):
            continue
        if not (r['selector'] == 'random' or (r['selector'] == 'gt_full' and r['source'] == 'GCN')):
            continue
        label = 'Random' if r['selector'] == 'random' else 'gt_full–GCN'
        cells = [r['method'] + ' / ' + label]
        for metric in ['U', 'G', 'D']:
            cells.append(f"{float(r[metric+'_mean']):.3f} [{float(r[metric+'_lo']):.3f}, {float(r[metric+'_hi']):.3f}]")
        assert '| ' + ' | '.join(cells) + ' |' in raw, cells
    auc = records('update_detection_coverage.csv')
    assert sum(int(r['raw_cells']) for r in auc) == 2160
    assert sum(int(r['computed_cells']) for r in auc) == 2160
    assert sum(int(r['auc_equals_half_cells']) for r in auc) == 0
    for method in ('GIF', 'IDEA'):
        assert {r['dataset']: int(r['U_exact_zero_cells']) for r in auc if r['method'] == method} == {'Cora': 33, 'CiteSeer': 28, 'PubMed': 16}
    verification = json.loads((OUT / 'verification.json').read_text(encoding='utf-8'))
    assert verification['verified_files'] == 5041 and verification['raw_cells'] == 2520
    assert all(verification['checks'].values())
    for name, expected in verification['output_sha256'].items():
        assert digest(OUT / name) == expected, name
    ratio_verification = json.loads((OUT / 'ratio_verification.json').read_text(encoding='utf-8'))
    assert ratio_verification['verified_files'] == 721
    assert ratio_verification['raw_cells'] == 360
    assert all(ratio_verification['checks'].values())
    assert ratio_verification['delivery_top_level_status'] == 'blocked'
    for name, expected in ratio_verification['output_sha256'].items():
        assert digest(OUT / name) == expected, name
    main_raw = (OUT / 'REPORT.md').read_text(encoding='utf-8')
    endpoints = records('ratio_display_endpoint_changes.csv')
    for dataset in ('Cora', 'CiteSeer', 'PubMed'):
        cells = [dataset]
        for selector in ('random', 'degree', 'r_point', 'gt_full'):
            r = next(r for r in endpoints if r['dataset'] == dataset and r['selector'] == selector)
            assert int(r['n']) == 3
            cells.append(f"{float(r['mean']):+.3f} ± {float(r['sd']):.3f}")
        assert '| ' + ' | '.join(cells) + ' |' in main_raw, cells
    assert 3 * 3 * 4 * 4 * 3 == 432 and 3 * 3 * 4 * 4 == 144
    result = {'execution_sha': SHA, 'files': checks, 'checks': {
        'source_identity': True, 'coverage_table_rows_18': True,
        'citeseer_interval_rows_4': True, 'update_auc_claim': True,
        'gif_idea_zero_drop_counts': True, 'analysis_output_hashes': True,
        'ratio_endpoint_table_values_12': True, 'ratio_output_hashes': True,
        'ratio_delivery_limitation_preserved': True,
    }, 'report_sha256': digest(OUT / 'REPORT.md'),
        'appendix_sha256': digest(OUT / 'FIXED_BUDGET_APPENDIX.md'),
        'scope': 'Read-only source and selected numeric report checks. Source identity does not assert remote payload availability. Remaining prose reviewed independently.',
        'new_gpu_runs': 0}
    (OUT / 'source_verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result['checks'], ensure_ascii=False))


if __name__ == '__main__':
    main()
