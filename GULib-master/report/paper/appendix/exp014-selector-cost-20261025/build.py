"""Regenerate numeric table rows only; manuscript prose is author-owned LaTeX."""
import json
from pathlib import Path


def build(source, output):
    summary = json.loads(source.read_text(encoding='utf-8'))
    rows = {row['condition']: row for row in summary['conditions']}
    lines = ['% Generated numeric table only; edit narrative in selector_cost.tex.',
             r'\begin{tabular}{llrrl}', r'\toprule',
             r'Selector & Computation & Selector entry & Whole job (s) & Outcome \\', r'\midrule']
    for name in ['R-point', 'D-full', 'IM-RR4096', 'IM-RR16384', 'IM-RR65536']:
        row = rows[name]
        device = 'CPU only' if name.startswith('IM-') else 'GPU + CPU'
        seconds = row['selector_entry_seconds']
        entry = r'6--8 h (est.)\textsuperscript{*}' if seconds is None else f'{seconds:.3f} s'
        outcome = 'Timeout (2 h)' if row['state'] == 'timeout' else 'Completed'
        lines.append(f"{name} & {device} & {entry} & {row['job_wall_seconds']:.0f} & {outcome} " + r'\\')
    lines.extend([r'\bottomrule', r'\end{tabular}'])
    output.write_bytes(('\n'.join(lines) + '\n').encode('utf-8'))


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    build(here / 'SUMMARY.json', here.parents[3] / 'report/paper/overleaf/sections/selector_cost_rows.tex')
