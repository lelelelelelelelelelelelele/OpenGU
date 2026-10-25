"""Compile each source slice with TeX, then expose browser-readable page images."""
import re
import subprocess

from .model import digest


def render(desk, key):
    block = desk.block(key)
    inputs = [p for p in desk.paper.rglob('*') if p.is_file() and p.suffix in {'.tex', '.pdf'}]
    fingerprint = digest(block['source'].encode() + b''.join(p.read_bytes() for p in sorted(inputs)))
    out = desk.state / 'preview' / key / fingerprint
    if (out / 'ready').exists():
        return sorted(out.glob('page-*.png'))
    out.mkdir(parents=True, exist_ok=True)
    body = block['source']
    # Keep the exact text, caption, math and figure/table content; only adapt float placement.
    body = re.sub(r'\\begin\{(figure|table)\*?\}(?:\[[^\]]*\])?', r'\\begin{\1}[H]', body)
    body = re.sub(r'\\end\{(figure|table)\*\}', r'\\end{\1}', body)
    preamble = r'''\documentclass[10pt]{article}
\usepackage[paperwidth=230mm,paperheight=310mm,margin=16mm]{geometry}
\usepackage{graphicx,booktabs,float,xcolor}
\input{math_commands.tex}
\newcommand{\Description}[1]{}
\newcommand{\draftnote}[1]{\textcolor{blue}{#1}}
\newcommand{\todo}[1]{\textcolor{red}{#1}}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\begin{document}
'''
    counter = {'fig3': 2, 'fig4': 3, 'exp014': 0}[key]
    source = preamble + '\\setcounter{figure}{' + str(counter) + '}\n' + body + '\n\\end{document}\n'
    path = out / 'preview.tex'
    path.write_text(source, encoding='utf-8')
    log = []
    for _ in range(2):
        run = subprocess.run(['pdflatex', '-no-shell-escape', '-interaction=nonstopmode',
                              '-halt-on-error', '-output-directory', str(out), str(path)],
                             cwd=desk.paper, capture_output=True, timeout=60)
        log.append(run.stdout)
        (out / 'compile.txt').write_bytes(b'\n'.join(log))
        if run.returncode:
            raise ValueError('LaTeX 预览编译失败，请检查源码。日志：' + str(out / 'compile.txt'))
    subprocess.run(['pdftoppm', '-scale-to', '1800', '-png', str(out / 'preview.pdf'), str(out / 'page')],
                   capture_output=True, check=True, timeout=60)
    (out / 'ready').touch()
    return sorted(out.glob('page-*.png'))
