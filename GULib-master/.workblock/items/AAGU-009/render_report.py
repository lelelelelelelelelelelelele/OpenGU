"""Render the canonical acceptance Markdown with the available MarkdownIt library."""
from pathlib import Path
import re

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent


def main():
    rendered = MarkdownIt("commonmark").render((ROOT / "REPORT.md").read_text(encoding="utf-8"))
    start = rendered.index("<h2>Human Result</h2>")
    end = rendered.index("<h2>", start + 4)
    decision = r"<blockquote>\s*<p>当前验收决定：<code>(待决定|接受)</code></p>\s*</blockquote>"
    human = rendered[start:end]
    def project_decision(match):
        label = match.group(1)
        state = "pending" if label == "待决定" else "accepted"
        return f'<p class="decision">当前验收决定：<span data-workblock-decision="{state}">{label}</span></p>'
    human, count = re.subn(decision, project_decision, human)
    assert count == 1
    rendered = rendered[:start] + '<section data-workblock-human-result="2.1">' + human + '</section>' + rendered[end:]
    page = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AAGU-009 · 软件修复验收</title><style>
*{box-sizing:border-box}body{margin:0;background:#f2f4f7;color:#17263a;font:16px/1.7 "Segoe UI","Microsoft YaHei",sans-serif}
main{max-width:1060px;margin:30px auto;padding:36px 44px;background:white;border:1px solid #dce2e9;border-radius:12px}
.eyebrow{font-size:12px;letter-spacing:1.5px;color:#506882;font-weight:700}h1{font-size:29px;line-height:1.3;margin:12px 0 24px}
h2{font-size:22px;margin:32px 0 15px;border-bottom:1px solid #dce2e9;padding-bottom:8px}h3{font-size:18px;margin:23px 0 8px}
p{margin:9px 0 16px}li{margin:10px 0}a{color:#175c99;text-underline-offset:3px}code{font:14px/1.6 Consolas,monospace;background:#edf1f5;padding:2px 4px;border-radius:4px;overflow-wrap:anywhere}
section[data-workblock-human-result]{background:#f0f6fc;border-left:4px solid #326da6;padding:18px 24px 12px;border-radius:5px}
section h2{margin:0 0 12px;font-size:17px;color:#506882;border:0;padding:0}section h3{margin:12px 0 6px}.decision span{color:#77520c;background:#fff0c9;padding:3px 10px;border-radius:4px;font-weight:700}
@media(max-width:650px){main{margin:0;padding:24px 18px;border:0;border-radius:0}h1{font-size:25px}section[data-workblock-human-result]{padding:15px}ul{padding-left:22px}body{font-size:15px}}
</style></head><body><main><div class="eyebrow">AAGU / SOFTWARE ACCEPTANCE / 2026-09-04</div>'''+rendered+'''</main></body></html>'''
    (ROOT / "REPORT.html").write_text(page, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
