"""Verify the Fig. 4 adoption snapshot and render its Markdown to embedded HTML.

Uses existing EXP-080 returns only. Requires mistune and pdftoppm on PATH.
Run with --check to verify the saved snapshot without rewriting it.
"""

import argparse
import base64
import csv
import hashlib
import html
import json
import math
from pathlib import Path
import re
import statistics
import subprocess
from collections import defaultdict

import mistune

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
DATA = ROOT / 'self/research/analyses/EXP-080/full-20261021'
FIGURE = ROOT / 'report/paper/overleaf/figures/citeseer_selector_responses.pdf'
PAPER = ROOT / 'report/paper/overleaf/sections/results.tex'
REPORT = OUT / 'REPORT.md'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(name):
    with (DATA / name).open(encoding='utf-8', newline='') as stream:
        return [r for r in csv.DictReader(stream) if r['dataset'] == 'CiteSeer']


def verify():
    raw, seeds, summary = map(read_csv, ['cells.csv', 'seed_values.csv', 'condition_summary.csv'])
    assert (len(raw), len(seeds), len(summary)) == (1029, 735, 245)
    requests, draws, means = defaultdict(list), defaultdict(list), defaultdict(list)
    for row in raw:
        requests[(row['selector'], row['ratio'], row['seed'], row['im_seed'])].append(row)
        for metric in ['accuracy', 'disagreement']:
            if row[metric]:
                draws[(row['selector'], row['method'], row['ratio'], row['seed'], metric)].append(float(row[metric]))
    assert len(requests) == 147
    for key, rows in requests.items():
        assert len(rows) == 7 and len({r['method'] for r in rows}) == 7, key
        assert len({r['selected_nodes_sha256'] for r in rows}) == 1, key
        assert len({r['split'] for r in rows}) == 1, key
    indexed = {(r['selector'], r['method'], r['ratio'], r['seed']): r for r in seeds}
    assert len(indexed) == len(seeds)
    for (selector, method, ratio, seed, metric), values in draws.items():
        assert len(values) == (3 if selector == 'im_rr_greedy' else 1)
        value = statistics.mean(values)
        assert math.isclose(value, float(indexed[(selector, method, ratio, seed)][metric]), abs_tol=1e-9)
        means[(selector, method, ratio, metric)].append(value)
    checked = 0
    for row in summary:
        for metric in ['accuracy', 'disagreement']:
            if metric == 'disagreement' and row['method'] == 'Retrain':
                continue
            values = means[(row['selector'], row['method'], row['ratio'], metric)]
            assert len(values) == 3 == int(row[metric + '_count'])
            assert math.isclose(statistics.mean(values), float(row[metric + '_mean']), abs_tol=1e-9)
            assert math.isclose(statistics.stdev(values), float(row[metric + '_std']), abs_tol=1e-9)
            checked += 1
    assert checked == 455
    by_seed = {(r['selector'], r['method'], float(r['ratio']), r['seed']): r for r in seeds}
    utility_losses = []
    for method in ['Retrain', 'GNNDelete', 'GraphEraser', 'GraphRevoker']:
        loss = {'method': method}
        for ratio in [.33, .5]:
            values = [float(by_seed[('random', method, ratio, seed)]['accuracy'])
                      - float(by_seed[('r_point', method, ratio, seed)]['accuracy'])
                      for seed in ['42', '212', '2024']]
            loss[str(ratio)] = statistics.mean(values)
        utility_losses.append(loss)
    with (OUT / 'disagreement_increment_seed_values.csv').open(encoding='utf-8', newline='') as stream:
        increments = list(csv.DictReader(stream))
    assert len(increments) == 504
    increment_groups = defaultdict(list)
    increment_keys = set()
    for row in increments:
        selector, method, ratio, seed = row['selector'], row['method'], float(row['ratio']), row['seed']
        assert selector in ['degree', 'r_point', 'gt_full', 'im_rr_greedy']
        assert method in ['GIF', 'IDEA', 'MEGU', 'GNNDelete', 'GraphEraser', 'GraphRevoker']
        key = selector, method, ratio, seed
        assert key not in increment_keys
        increment_keys.add(key)
        value = float(by_seed[key]['disagreement'])
        baseline = float(by_seed[('random', method, ratio, seed)]['disagreement'])
        for column, expected in [('disagreement_selector', value), ('disagreement_random', baseline),
                                 ('delta_disagreement_pp', value-baseline)]:
            assert math.isclose(float(row[column]), expected, abs_tol=1e-9), (key, column)
        increment_groups[(selector, method, ratio)].append(value-baseline)
    assert len(increment_groups) == 168 and all(len(v) == 3 for v in increment_groups.values())
    negative_means = sum(statistics.mean(v) < 0 for v in increment_groups.values())
    assert negative_means == 62
    band_min = min(statistics.mean(v)-statistics.stdev(v) for v in increment_groups.values())
    band_max = max(statistics.mean(v)+statistics.stdev(v) for v in increment_groups.values())
    assert -6 < band_min < 0 < band_max < 38
    changes = []
    for selector, method in [('r_point', 'GIF'), ('r_point', 'IDEA'), ('r_point', 'MEGU'),
                             ('im_rr_greedy', 'GIF'), ('im_rr_greedy', 'MEGU')]:
        change = {'selector': selector, 'method': method}
        for metric in ['accuracy', 'disagreement']:
            a = {r['seed']: float(r[metric]) for r in seeds
                 if r['selector'] == selector and r['method'] == method and float(r['ratio']) == .1}
            b = {r['seed']: float(r[metric]) for r in seeds
                 if r['selector'] == selector and r['method'] == method and float(r['ratio']) == .5}
            assert a.keys() == b.keys() and len(a) == 3
            delta = [b[s] - a[s] for s in a]
            change[metric] = {'at_10': statistics.mean(a.values()), 'at_50': statistics.mean(b.values()),
                              'paired_change_mean': statistics.mean(delta),
                              'paired_change_sample_sd': statistics.stdev(delta),
                              'paired_change_min': min(delta)}
        changes.append(change)
    md = REPORT.read_text(encoding='utf-8')
    for loss in utility_losses:
        assert f"| {loss['method']} | {loss['0.33']:+.2f} | {loss['0.5']:+.2f} |" in md
    # Confirm the report table values are the independently reconstructed values.
    names = {'r_point': 'R-point', 'im_rr_greedy': 'IM-RR'}
    for row in changes:
        acc, d = row['accuracy'], row['disagreement']
        line = (f"| {names[row['selector']]} / {row['method']} | {acc['at_10']:.2f} | {acc['at_50']:.2f} | "
                f"{d['at_10']:.2f} | {d['at_50']:.2f} | {d['paired_change_mean']:+.2f} ± {d['paired_change_sample_sd']:.2f} |")
        assert line in md, line
    english = md.split('## 与论文正文一致的英文段落\n\n', 1)[1].split('\n## ', 1)[0].strip()
    paper = PAPER.read_text(encoding='utf-8')
    paper_text = paper.split('\\subsection{Selector effects persist with method-dependent GU responses}\n', 1)[1].split('\\begin{figure*}', 1)[0].strip()
    paper_text = paper_text.replace('Figure~\\ref{fig:exp080-budget-response}', 'Figure 4').replace('\\%', '%')
    assert ' '.join(english.split()) == ' '.join(paper_text.split()), 'Paper/report prose differs'
    for link in re.findall(r'\]\(([^)]+)\)', md):
        if '://' not in link and not link.startswith('#') and link not in ['fig4.png', 'verification.json']:
            assert (OUT / link.split('#')[0]).exists(), link
    paths = [DATA / p for p in ['cells.csv', 'seed_values.csv', 'condition_summary.csv', 'verification.json']]
    paths += [REPORT, PAPER, FIGURE, ROOT / 'scripts/plot_exp080_selector_response.py']
    paths += [ROOT / 'scripts/plot_exp080_disagreement_increment.py',
              OUT / 'disagreement_increment_seed_values.csv', OUT / 'disagreement_increment.pdf']
    record = json.loads((ROOT / 'self/research/analyses/EXP-080.json').read_text(encoding='utf-8'))
    return {'scope': 'EXP-080 CiteSeer figure adoption; 5 selectors, 7 methods, 7 ratios, 3 training seeds',
            'raw_cells': len(raw), 'seed_aggregated_rows': len(seeds), 'matched_request_groups': len(requests),
            'verified_mean_sd_points': checked, 'paired_changes': changes, 'paper_report_prose_identical': True,
            'r_point_extra_utility_losses_vs_random': utility_losses,
            'supplement': {'paired_seed_differences': len(increments), 'mean_sd_points': len(increment_groups),
                           'negative_mean_points': negative_means, 'mean_minus_sd_min': band_min,
                           'mean_plus_sd_max': band_max},
            'execution_sources': [{'run_id': run, 'execution_sha': sha} for run, sha in
                                  sorted({(r['run_id'], r['execution_sha']) for r in raw})],
            'scientific_decision_at_build': record['decision']['state'],
            'remote_raw_file_reaudit_performed': False,
            'input_sha256': {p.relative_to(ROOT).as_posix(): digest(p) for p in paths}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    facts = verify()
    manifest = OUT / 'verification.json'
    if args.check:
        saved = json.loads(manifest.read_text(encoding='utf-8'))
        assert all(saved[k] == v for k, v in facts.items()), 'Snapshot source or computed facts changed'
        for name, sha in saved['output_sha256'].items():
            assert digest(OUT / name) == sha, name
        print('PASS: archived source hashes, paired statistics, links and paper/report prose match.')
        return
    subprocess.run(['pdftoppm', '-singlefile', '-r', '200', '-png', str(FIGURE), str(OUT / 'fig4')], check=True)
    render = mistune.create_markdown(plugins=['table'])
    body = render(REPORT.read_text(encoding='utf-8'))
    for name in ['fig4.png', 'disagreement_increment.png']:
        data_url = 'data:image/png;base64,' + base64.b64encode((OUT / name).read_bytes()).decode('ascii')
        body = body.replace('src="' + name + '"', 'src="' + data_url + '"')
    css = 'body{max-width:1120px;margin:42px auto;padding:0 28px;color:#202b36;font:16px/1.7 system-ui,sans-serif}h1{font-size:30px;line-height:1.3}h2{font-size:22px;margin-top:36px}img{width:100%;height:auto}table{border-collapse:collapse;display:block;overflow:auto;font-size:14px}th,td{padding:9px 13px;border-bottom:1px solid #dfe5ea;text-align:left;white-space:nowrap}th{background:#eff4f6}a{color:#146c83}code{font-size:.9em;background:#f3f5f7;padding:2px 4px}p{margin:14px 0}@media(max-width:650px){body{padding:0 15px;margin:22px auto}h1{font-size:25px}}'
    document = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape('Fig. 4 · EXP-080 论文采用与归档') + '</title><style>' + css + '</style><main>' + body + '</main></html>\n'
    (OUT / 'REPORT.html').write_bytes(document.encode('utf-8'))
    facts['output_sha256'] = {name: digest(OUT / name) for name in
                              ['REPORT.html', 'fig4.png', 'disagreement_increment.png']}
    manifest.write_bytes((json.dumps(facts, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    print('PASS: 1,029 cells, 147 matched requests, 455 mean/SD points; paper prose and Markdown/HTML snapshot saved.')


if __name__ == '__main__':
    main()
