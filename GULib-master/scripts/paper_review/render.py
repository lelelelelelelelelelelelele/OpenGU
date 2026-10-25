"""Convert manuscript LaTeX to selectable HTML/MathML with vector figures."""
import html
import os
from pathlib import Path
import re
import subprocess

from .model import digest


def render(desk, key):
    block = desk.block(key)
    inputs = sorted(p for p in desk.paper.rglob('*') if p.is_file() and p.suffix in {'.tex', '.pdf'})
    fingerprint = digest(Path(__file__).read_bytes() + block['source'].encode('utf-8') +
                         b''.join(p.read_bytes() for p in inputs))
    out = desk.state / 'html-preview' / key / fingerprint
    document = out / 'preview.html'
    if (out / 'ready').exists():
        return document
    out.mkdir(parents=True, exist_ok=True)
    body = block['source'].replace('{figure*}', '{figure}').replace('{table*}', '{table}')
    preamble = r'''\documentclass[10pt]{article}
\usepackage{graphicx,booktabs,hyperref,xcolor}
\input{math_commands.tex}
\newcommand{\Description}[1]{}
\newcommand{\draftnote}[1]{\textcolor{blue}{#1}}
\newcommand{\todo}[1]{\textcolor{red}{#1}}
\renewcommand{\includegraphics}[2][]{\href{/paper/#2}{Open original figure (PDF)}}
\begin{document}
'''
    counter = {'fig3': 2, 'fig4': 3, 'exp014': 0}[key]
    source = preamble + '\\setcounter{figure}{' + str(counter) + '}\n' + body + '\n\\end{document}\n'
    (out / 'preview.tex').write_bytes(source.encode('utf-8'))
    env = dict(os.environ)
    # Keep all converter outputs outside manuscript sources.
    env['TEXINPUTS'] = desk.paper.as_posix() + '//' + os.pathsep + env.get('TEXINPUTS', '')
    run = subprocess.run(['make4ht', '-a', 'warning', 'preview.tex', 'mathml'],
                         cwd=out, env=env, capture_output=True, timeout=60)
    (out / 'compile.txt').write_bytes(run.stdout + run.stderr)
    if run.returncode or not document.exists():
        raise ValueError('LaTeX 转 HTML 失败，请检查源码。日志：' + str(out / 'compile.txt'))
    text = document.read_text(encoding='utf-8')

    def figure(match):
        url = match.group(1)
        path = (desk.paper / url.removeprefix('/paper/')).resolve()
        if not path.is_relative_to(desk.paper / 'figures') or path.suffix != '.pdf':
            raise ValueError('图文件必须位于论文 figures 目录。')
        name = digest(path.read_bytes()) + '.svg'
        subprocess.run(['pdftocairo', '-svg', str(path), str(out / name)],
                       check=True, capture_output=True, timeout=60)
        return (f'<a class="figure-link" href="{html.escape(url, quote=True)}" target="_blank" '
                f'rel="noreferrer"><img src="{name}" alt="{html.escape(block["title"], quote=True)}" '
                'class="vector-figure" /></a>')

    text = re.sub(r"<a href='(/paper/figures/[^']+\.pdf)'>Open original figure \(PDF\)</a>", figure, text)
    text = text.replace('</head>', '<link href="/reader.css" rel="stylesheet" /></head>')
    document.write_bytes(text.encode('utf-8'))
    (out / 'ready').touch()
    return document
