# -*- coding: utf-8 -*-
"""Reflow private proof copies only, using the accepted plot function and unchanged data."""
from pathlib import Path
import ast
import csv
import hashlib
import json
import statistics as stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
SOURCE = ROOT / 'self/research/experiments/drafts/round3-graph-analysis'
RUN = SOURCE / 'e85gr1'
ORIGINAL = SOURCE / 'interpret_graph.py'
OUT = HERE / 'images'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

initial = json.loads((HERE / 'INPUTS.json').read_text(encoding='utf-8'))
for relative, expected in initial['source_before_sha256'].items():
    assert sha(ROOT / relative) == expected, relative
source = ORIGINAL.read_text(encoding='utf-8')
tree = ast.parse(source)
function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'figures')
original = '\n'.join(source.splitlines()[function.lineno - 1:function.end_lineno]) + '\n'
plot = original
changes = [
    ("'font.size':10", "'font.size':8.5,'axes.titlesize':9.5,'figure.titlesize':10.5,'axes.labelsize':8.5,'xtick.labelsize':8.5,'ytick.labelsize':8.5,'legend.fontsize':8.5"),
    (",bbox_inches='tight'", ''),
    ('figsize=(10.5,7)', 'figsize=(506.295/72.27,6.55)'),
    ('figsize=(11,7.5)', 'figsize=(506.295/72.27,6.4)'),
    ('figsize=(11,5.5)', 'figsize=(506.295/72.27,5.5)'),
    ('bbox_to_anchor=(.5,-.01)', 'bbox_to_anchor=(.5,.012)'),
    ('bbox_to_anchor=(.5,-.07)', 'bbox_to_anchor=(.5,.012)'),
    ('rect=(0,.05,1,.95)', 'rect=(0,.09,1,.93)'),
    ('rect=(0,.12,1,.94)', 'rect=(0,.19,1,.92)'),
    ('Fixed-weight graph and MEGU postprocessing controls | CiteSeer', 'Graph and postprocessing controls | CiteSeer'),
    ('Truth decomposition of the Ret-only prediction change | published pipeline', 'Ret-only truth categories | published pipeline'),
    ('MEGU four-endpoint controls | mean and sample SD across 3 joint runs', 'MEGU four-endpoint controls | 3 joint seeds'),
    ('Change caused by specified C&S comparison (pp)', 'Specified C&S difference (pp)'),
]
replacement_log = []
for old, new in changes:
    count = plot.count(old)
    assert count > 0, old
    plot = plot.replace(old, new)
    replacement_log.append({'old': old, 'new': new, 'matches': count})
(HERE / 'original_plot_function.py').write_text(original, encoding='utf-8')
(HERE / 'private_plot_function.py').write_text(plot, encoding='utf-8')

def read(p):
    with p.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

endpoints = read(RUN / 'endpoints.csv')
for row in endpoints:
    for key in ['ret_only_corrects', 'ret_only_harms', 'ret_only_both_wrong']:
        row[key + '_pct'] = 100 * float(row[key]) / float(row['node_count'])
contrasts = read(RUN / 'interpretation/request_contrast_summary.csv')
cs = read(RUN / 'interpretation/cs_summary.csv')
for rows in [contrasts, cs]:
    for row in rows:
        for key, value in list(row.items()):
            if key.endswith('_mean') or key.endswith('_sd'):
                row[key] = float(value)
namespace = {'OUT': OUT, 'stats': stats, 'number': lambda row, key: float(row[key])}
exec(compile(plot, str(HERE / 'private_plot_function.py'), 'exec'), namespace)
namespace['figures'](endpoints, contrasts, cs)
after = {relative: sha(ROOT / relative) for relative in initial['source_before_sha256']}
assert after == initial['source_before_sha256']
record = {
    'status': 'private_layout_copies_generated',
    'original_generator_unchanged': True,
    'all_17_source_files_unchanged': True,
    'data_aggregation_or_scientific_analysis_modified': False,
    'plot_function_source': str(ORIGINAL.relative_to(ROOT)),
    'plot_source_sha256': sha(ORIGINAL),
    'width_inches': 506.295 / 72.27,
    'base_font_pdf_pt': 8.5,
    'layout_only_replacements': replacement_log,
    'source_after_sha256': after,
    'private_outputs': {p.name: sha(p) for p in sorted(OUT.glob('*'))},
}
(HERE / 'REFLOW_PROVENANCE.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': record['status'], 'width_inches': record['width_inches'], 'unchanged_sources': len(after)}))
