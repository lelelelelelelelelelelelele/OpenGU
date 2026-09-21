"""Render AAGU-066 scalar results only after SyncMate index verification."""
from __future__ import annotations

import argparse
import base64
import html
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def render(run, documents, output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    evidence = output / 'evidence'
    evidence.mkdir(exist_ok=True)
    figure, axes = plt.subplots(1, 3, figsize=(15, 4), constrained_layout=True)
    rows, md_rows = [], []
    for request in run['requests']:
        seed = request['seed']
        for method in ('gif', 'idea', 'retrain'):
            row = documents[f'seed{seed}/{method}.json']
            if method != 'retrain':
                trace = row['diagnostics']['trace']
                for axis, field in zip(axes, ('shifted_relative_residual', 'original_relative_residual', 'delta_l2')):
                    axis.plot([p['iteration'] for p in trace], [max(p[field], 1e-16) for p in trace],
                              label=f'{seed} {row["method"]}')
                verdict = 'PASS' if row['numerical_passed'] else 'FAIL'
            else:
                verdict = '—'
            original = row['metrics']['original']['test']['macro_f1']
            retained = row['metrics']['retained']['test']['macro_f1']
            gap = row.get('test_metric_gap_vs_retrain', {}).get('original', {}).get('macro_f1')
            values = [str(seed), row['method'], verdict, f'{original:.6f}', f'{retained:.6f}',
                      '—' if gap is None else f'{gap:+.6f}', f'{row["weight_update_l2"]:.6g}']
            rows.append('<tr>' + ''.join('<td>' + html.escape(v) + '</td>' for v in values) + '</tr>')
            md_rows.append('| ' + ' | '.join(values) + ' |')
    for axis, title in zip(axes, ('Shifted residual', 'Original-equation residual', 'Update L2')):
        axis.set(title=title, xlabel='Iteration', yscale='log')
        axis.grid(alpha=.2)
    axes[0].axhline(run['policy']['residual_tolerance'], linestyle='--', color='black', linewidth=1)
    axes[-1].legend(fontsize=7)
    image_path = evidence / 'solver-trajectories.png'
    figure.savefig(image_path, dpi=160)
    plt.close(figure)
    headers = ['Random seed', '方法', '数值检查', '原图 test F1', '删减图 test F1', '原图 F1−Retrain', '权重变化 L2']
    count = len(run['requests']) * 2
    passed = sum(documents[f'seed{r["seed"]}/{m}.json']['numerical_passed']
                 for r in run['requests'] for m in ('gif', 'idea'))
    observation = f'{passed}/{count} 个 GIF/IDEA 条件通过预定数值检查；每个请求均包含独立从头训练的 Retrain。'
    limit = ('数值检查针对正阻尼的移位方程；原方程残差另行展示。'
             '预算一致性沿用065的更新范数相对差口径，不把它称为完整向量差。'
             'F1和Retrain差异用于观察，不作为选参或数值通过条件。')
    recommendation = '建议审阅数值与效用结果后作科学接受决定。' if passed == count else '建议返工或接受失败结论；当前不能打开下游成功门槛。'
    markdown = ('# AAGU-066 · Cora H16 Random 验证\n\n## Human Result\n\n### 实际增量\n\n'
                '固定PT和参数，完成GIF/IDEA/Retrain配对比较；计算中间张量不落盘。\n\n### 核心观察\n\n'
                + observation + '\n\n' + '| ' + ' | '.join(headers) + ' |\n|' + '---|' * len(headers)
                + '\n' + '\n'.join(md_rows) + '\n\n![求解轨迹](evidence/solver-trajectories.png)\n\n'
                + limit + '\n\n### 当前决定\n\n' + recommendation + '\n\n> 当前验收决定：`待决定`\n\n'
                + f'运行：`{run["run_id"]}`；代码：`{run["commit"]}`。完整指标见 [核验结果](evidence/verified-results.json)。\n')
    (output / 'REPORT.md').write_text(markdown, encoding='utf-8')
    table = '<table><thead><tr>' + ''.join('<th>' + html.escape(h) + '</th>' for h in headers) + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'
    encoded = base64.b64encode(image_path.read_bytes()).decode()
    page = ('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>AAGU-066 验证</title>'
            '<style>body{max-width:1200px;margin:36px auto;padding:20px;font:16px/1.7 system-ui;color:#172235}'
            'table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:left}'
            'img{width:100%}code{overflow-wrap:anywhere}</style><h1>AAGU-066 · Cora H16 Random 验证</h1>'
            '<section data-workblock-human-result><h2>Human Result</h2><h3>实际增量</h3><p>固定PT和参数，完成GIF/IDEA/Retrain配对比较；计算中间张量不落盘。</p>'
            '<h3>核心观察</h3><p>' + observation + '</p>' + table + f'<img alt="求解轨迹" src="data:image/png;base64,{encoded}">'
            '<p>' + limit + '</p><h3>当前决定</h3><p>' + recommendation + '</p>'
            '<p>当前验收决定：<span data-workblock-decision="pending">待决定</span></p></section>'
            '<p>运行：<code>' + html.escape(run['run_id']) + '</code>；代码：<code>' + html.escape(run['commit'])
            + '</code>。<a href="evidence/verified-results.json">完整核验指标</a></p></html>')
    (output / 'REPORT.html').write_text(page, encoding='utf-8')
    (evidence / 'verified-results.json').write_text(json.dumps({'run': run, 'documents': documents}, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe', required=True, choices=('opengu-aagu066-h16-gate-v1', 'opengu-aagu066-h16-v1'))
    parser.add_argument('--node-id', required=True)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    from scripts.syncmate.opengu_recipes import recipe_definitions
    from scripts.syncmate.opengu_acceptance import acceptance_payload
    from experiments.aagu066_validation import verify_run
    definition = recipe_definitions()[args.recipe]
    index = json.loads((ROOT / '.syncmate/artifact_index.json').read_text(encoding='utf-8'))
    peer = index['peers'][args.node_id]
    sha = peer['remote']['git']['sha']
    verdict = acceptance_payload('aagu066-validation-v1', definition, {
        'project_root': str(ROOT), 'artifact_index': index, 'node_id': args.node_id, 'expected_git_sha': sha})
    if not verdict['passed']:
        raise ValueError('unverified results: ' + '; '.join(verdict['errors']))
    remote_run = next(p for p in definition['expected_artifact_paths'] if p.endswith('/run.json'))
    entry = next(e for e in peer['items'] if (e.get('remote_path') or e.get('path')) == remote_run)
    run, documents = verify_run(ROOT / entry['local_path'], ROOT / definition['config_path'], sha)
    render(run, documents, args.output)
    print(json.dumps({'passed': True, 'report': str(args.output / 'REPORT.html')}))


if __name__ == '__main__':
    main()
