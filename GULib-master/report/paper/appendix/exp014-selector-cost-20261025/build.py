"""Build the paper's bounded selector-cost supplement from frozen evidence."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE = ROOT / 'self/research/experiments/drafts/EXP-014/SUMMARY.json'
summary = json.loads(SOURCE.read_text(encoding='utf-8'))
estimate = summary['rr65536_extrapolation']
rows = {r['condition']: r for r in summary['conditions']}
methods = [('R-point', 'GPU + CPU'), ('D-full', 'GPU + CPU'),
           ('IM-RR4096', 'CPU only'), ('IM-RR16384', 'CPU only'), ('IM-RR65536', 'CPU only')]
intro = (
    'On ogbn-arxiv (169,343 nodes), we use a random 70/10/20 split with seed 2024, '
    'rather than the official temporal split, and select 5,927 nodes from 118,540 '
    'training candidates (5%). R-point, D-full, and fixed-budget IM-RR with 4,096 '
    'and 16,384 samples produced complete requests with the required size, uniqueness, '
    'candidate membership, and input identity verified. IM uses selector seed 11 and '
    'propagation probability 0.1; D-full retains the gt_full GCN configuration and '
    'training seed 42. IM sampling and greedy coverage execute entirely on the CPU, '
    'without model training or GPU acceleration. R-point and D-full use the GPU for '
    'model/gradient computation and include CPU processing. These experiments evaluate '
    'request generation only; they contain no large-graph GU or retraining outcomes.')
boundary = (
    'Selector-entry time includes current request access and verification; for R-point '
    'and D-full it also includes model preparation. Whole-job time is measured between '
    'Core start and finish and excludes queue and return. Successful IM runs invoked '
    'the Selection producer on a MISS; R-point and D-full had Checkpoint/Score/Selection '
    'MISS. The RR=65,536 run reached its 7,200-second limit without a complete trusted '
    'output; its 7,202-second wall includes termination overhead. RR=16,384 completed '
    'normally at 6,511 seconds, crossing the pre-agreed 6,480-second expansion-stop '
    'threshold. CPU model and thread allocation were not normalized; code/Core '
    'versions differ across runs. The table is not a controlled hardware or speedup comparison.')
scaling = (
    'Existing small-graph tests recomputed sampling plus greedy selection for Cora, '
    'CiteSeer, and PubMed at four RR budgets and three selector seeds (11, 22, 33). '
    'These timings exclude graph loading/construction and cache access, and the replayed '
    'node sequences matched the verified selections. The small-graph deletion budget '
    'was 10%, versus 5% on ogbn-arxiv. From 16,384 to 65,536 samples, mean computation '
    'time increased by 4.33, 4.37, and 4.36 times, respectively. This is empirical '
    'support for approximately proportional growth over those tested budgets, not '
    'a universal scaling law. For fixed graph and sampling distribution, expected '
    'sampling work is additive in the number of samples; greedy/index operations '
    'and memory effects need not follow the same proportionality.')
projection = (
    '* Estimated selector-entry completion time, extrapolated from measured '
    'ogbn-arxiv RR timings and small-graph replay tests (4 times as many samples '
    'took 4.33--4.37 times as long at the highest two tested budgets). The '
    'approximately 6--8 hours is not a measured completion or runtime bound; '
    'the observed run timed out after 2 hours. Exact scenarios and original '
    'timing boundaries are retained in the evidence report.')

md = '# EXP-014 · Paper appendix: request-generation cost\n\n'
md += '2026-10-25 · 用户确认纳入论文：正文一句指向附录，估计合入同一成本表并用脚注标明。\n\n'
md += '## Paper text and measured costs\n\n' + intro + '\n\n'
md += '| Selector | Computation | Selector entry | Whole job (s) | Outcome |\n| --- | --- | ---: | ---: | --- |\n'
texrows = []
for name, device in methods:
    row = rows[name]
    entry = '6–8 h (est.)*' if row['selector_entry_seconds'] is None else '%.3f s' % row['selector_entry_seconds']
    texentry = r'6--8 h (est.)\textsuperscript{*}' if row['selector_entry_seconds'] is None else entry
    outcome = 'Timeout (2 h)' if row['state'] == 'timeout' else 'Completed'
    md += f"| {name} | {device} | {entry} | {row['job_wall_seconds']:.0f} | {outcome} |\n"
    texrows.append(f"{name} & {device} & {texentry} & {row['job_wall_seconds']:.0f} & {outcome} " + r'\\')
md += '\n' + projection + '\n\n' + boundary + '\n\n## Small-graph timing evidence\n\n' + scaling + '\n\n'
md += '| Graph | RR1024 (s) | RR4096 (s) | RR16384 (s) | RR65536 (s) | Last-tier ratio |\n| --- | ---: | ---: | ---: | ---: | ---: |\n'
for row in estimate['small_graph_rows']:
    values = row['mean_sampling_plus_greedy_seconds']
    md += '| ' + row['dataset'] + ' | ' + ' | '.join('%.3f' % values[str(r)] for r in (1024,4096,16384,65536)) + ' | %.2f |\n' % row['last_fourfold_time_ratio']
md += '\n## Provenance and rebuild\n\n'
md += '[EXP-014 full report](../../../../self/research/experiments/drafts/EXP-014/REPORT.html) · [Frozen numbers](../../../../self/research/experiments/drafts/EXP-014/SUMMARY.json) · [36-condition raw timings](../../../../.workblock/items/AAGU-053/evidence/rr10-20260913/rr-condition-summary.csv)\n\n'
md += '原执行SHA、缓存、身份核验与源文件哈希沿EXP-014冻结数字保留。SHA256(SUMMARY.json): `' + hashlib.sha256(SOURCE.read_bytes()).hexdigest() + '`.\n\n'
md += '由本目录 build.py 从冻结数字生成；HTML由同目录 build_report.ps1 生成。LaTeX片段为 sections/selector_cost.tex，估计合入原成本表并加脚注；原始产物、科学接纳和执行范围保持原记录。\n'
(HERE / 'REPORT.md').write_text(md, encoding='utf-8')

tex = '% Generated by report/paper/appendix/exp014-selector-cost-20261025/build.py\n'
tex += '\\subsection{Request-generation cost on a larger graph}\n\\label{app:arxiv-selector-cost}\n' + intro.replace('%', r'\%').replace('_', r'\_') + '\n\n'
tex += r'''\begin{table*}[t]
\centering\small
\caption{Request-generation costs on ogbn-arxiv. Times are measured except the starred estimate; entry and whole-job times have different boundaries.}
\label{tab:arxiv-selector-cost}
\begin{tabular}{llrrl}
\toprule
Selector & Computation & Selector entry & Whole job (s) & Outcome \\
\midrule
'''
tex += '\n'.join(texrows) + '\n' + r'''\bottomrule
\end{tabular}
\par\smallskip
\begin{minipage}{\textwidth}\footnotesize
'''
tex += projection.replace('* ', r'\textsuperscript{*} ', 1) + '\n' + r'''\end{minipage}
\end{table*}
'''
tex += '\n' + boundary + '\n'
(ROOT / 'report/paper/overleaf/sections/selector_cost.tex').write_text(tex, encoding='utf-8')
print(json.dumps({'report': str(HERE / 'REPORT.md'), 'latex': 'report/paper/overleaf/sections/selector_cost.tex', 'estimated_hours': [r['hours'] for r in estimate['scenarios']]}, ensure_ascii=False))
