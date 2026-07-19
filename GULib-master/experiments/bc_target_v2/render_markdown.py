"""Render a Markdown experiment document as a standalone static HTML page."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path
from typing import List, Sequence, Tuple

import mistune


class AnchoredRenderer(mistune.HTMLRenderer):
    """Mistune renderer that records headings and emits stable anchors."""

    def __init__(self) -> None:
        super().__init__(escape=False)
        self.headings: List[Tuple[int, str, str]] = []
        self._slug_counts = {}

    def heading(self, text: str, level: int, **attrs) -> str:
        plain = re.sub(r"<[^>]+>", "", text)
        plain = html.unescape(plain).strip()
        base = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "-", plain).strip("-")
        base = base.lower() or "section"
        count = self._slug_counts.get(base, 0)
        self._slug_counts[base] = count + 1
        slug = base if count == 0 else f"{base}-{count + 1}"
        self.headings.append((level, plain, slug))
        return f'<h{level} id="{slug}">{text}</h{level}>\n'


def _strip_front_matter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end < 0:
        return text
    return text[end + 5 :]


def _nav_html(headings: Sequence[Tuple[int, str, str]]) -> str:
    items = []
    for level, text, slug in headings:
        if level not in (2, 3):
            continue
        css_class = "sub" if level == 3 else ""
        items.append(
            f'<a class="{css_class}" href="#{html.escape(slug)}">'
            f"{html.escape(text)}</a>"
        )
    return "\n".join(items)


def render_document(
    source: Path,
    output: Path,
    title: str,
    badge: str,
    kicker: str,
) -> None:
    renderer = AnchoredRenderer()
    markdown = mistune.create_markdown(
        renderer=renderer,
        plugins=["table", "strikethrough", "task_lists", "url"],
    )
    source_text = source.read_text(encoding="utf-8")
    body = markdown(_strip_front_matter(source_text))
    nav = _nav_html(renderer.headings)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root{{--bg:#07111f;--panel:#0f1c2e;--panel2:#14253c;--text:#e9f0fa;--muted:#9dafc7;--line:#29435f;--cyan:#59d8d2;--green:#75d79d;--amber:#f2bc62;--red:#ff8d86;--code:#081726}}
    *{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:linear-gradient(135deg,#06101d,#0a1728 55%,#07121f);color:var(--text);font:15px/1.7 system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}}.layout{{display:grid;grid-template-columns:285px minmax(0,1fr);min-height:100vh}}aside{{position:sticky;top:0;height:100vh;padding:28px 22px;border-right:1px solid var(--line);background:rgba(7,17,31,.97);overflow:auto}}main{{width:min(1240px,100%);padding:42px 54px 80px}}.brand{{font-size:11px;letter-spacing:.15em;color:var(--cyan);font-weight:800}}.side-title{{font-size:20px;line-height:1.35;margin:10px 0}}.badge{{display:inline-block;padding:4px 9px;border:1px solid #315f48;border-radius:999px;background:#102c21;color:var(--green);font-size:11px;font-weight:800}}nav{{margin-top:24px}}nav a{{display:block;color:var(--muted);text-decoration:none;padding:4px 0}}nav a.sub{{padding-left:12px;font-size:12px}}nav a:hover{{color:var(--cyan)}}.hero{{padding:28px 34px;margin-bottom:30px;border:1px solid var(--line);border-radius:18px;background:linear-gradient(145deg,rgba(20,37,60,.97),rgba(9,23,40,.97));box-shadow:0 20px 60px rgba(0,0,0,.25)}}.kicker{{color:var(--cyan);font-size:12px;letter-spacing:.13em;font-weight:800}}.hero h1{{font-size:32px;line-height:1.2;margin:8px 0 6px}}article>h1:first-child{{display:none}}h2{{font-size:24px;margin:43px 0 15px;padding-bottom:9px;border-bottom:1px solid var(--line)}}h3{{font-size:18px;color:#d5eaff;margin:27px 0 9px}}h4{{font-size:15px;color:var(--cyan);margin-top:22px}}p,li{{max-width:1020px}}a{{color:#81d9ff}}strong{{color:#fff}}code{{padding:.14em .36em;border-radius:5px;background:var(--code);color:#b9ecff;font-family:Consolas,monospace}}pre{{overflow:auto;padding:15px 17px;border:1px solid var(--line);border-radius:10px;background:var(--code)}}pre code{{padding:0}}blockquote{{margin:18px 0;padding:13px 18px;border-left:4px solid var(--green);background:rgba(117,215,157,.08)}}table{{width:100%;border-collapse:collapse;margin:17px 0 28px;background:rgba(15,28,46,.75);font-size:13px}}th,td{{border:1px solid var(--line);padding:9px 10px;vertical-align:top}}th{{background:var(--panel2);color:#ddf8ff;text-align:left}}tr:nth-child(even) td{{background:rgba(20,37,60,.43)}}hr{{border:0;border-top:1px solid var(--line);margin:38px 0}}.source{{margin-top:54px;padding-top:18px;border-top:1px solid var(--line);color:var(--muted);font-size:12px}}@media(max-width:950px){{.layout{{display:block}}aside{{position:relative;height:auto;border-right:0;border-bottom:1px solid var(--line)}}nav{{display:none}}main{{padding:28px 20px}}.hero h1{{font-size:27px}}table{{display:block;overflow:auto}}}}
  </style>
</head>
<body>
<div class="layout">
  <aside>
    <div class="brand">OPENGU / B–C MATRIX</div>
    <div class="side-title">{html.escape(title)}</div>
    <span class="badge">{html.escape(badge)}</span>
    <nav>{nav}</nav>
  </aside>
  <main>
    <section class="hero">
      <div class="kicker">{html.escape(kicker)}</div>
      <h1>{html.escape(title)}</h1>
    </section>
    <article>{body}</article>
    <div class="source">由同名 Markdown 源文件生成；Markdown 是可编辑的事实源。</div>
  </main>
</div>
</body>
</html>
""",
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--badge", default="LOCAL MATRIX")
    parser.add_argument("--kicker", default="CORA · CITESEER · PUBMED · GCN")
    return parser


def main(argv: Sequence[str] = None) -> int:
    args = build_parser().parse_args(argv)
    render_document(
        args.source.resolve(),
        args.output.resolve(),
        args.title,
        args.badge,
        args.kicker,
    )
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
