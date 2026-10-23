"""Check the audit's source/HTML agreement, structure and local links."""
from collections import Counter
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
WRITING = HERE.parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.hrefs = []
        self.hash = None
        self.tags = Counter()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags[tag] += 1
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "a":
            self.hrefs.append(attrs.get("href", ""))
        if tag == "meta" and attrs.get("name") == "source-sha256":
            self.hash = attrs["content"]


sources = [WRITING / "outline/OUTLINE.md", *sorted(HERE.rglob("*.md"))]
errors = []
pages = []
local_links = 0
for source in sources:
    md = source.read_text(encoding="utf-8")
    html_path = source.with_suffix(".html")
    html = html_path.read_text(encoding="utf-8")
    page = Page()
    page.feed(html)
    digest = sha256(source.read_bytes()).hexdigest()
    if page.hash != digest:
        errors.append(f"Stale HTML: {source}")
    if len(page.ids) != len(set(page.ids)):
        errors.append(f"Duplicate IDs: {html_path}")
    if "\ufffd" in md or "\ufffd" in html:
        errors.append(f"Replacement characters: {source}")
    for href in page.hrefs:
        if not href or re.match(r"^(https?://|mailto:)", href):
            continue
        if href.startswith("#"):
            if unquote(href[1:]) not in page.ids:
                errors.append(f"Broken anchor {source.name}: {href}")
            continue
        path = unquote(href.split("#", 1)[0]).strip("<>")
        # Codex source references can end in :line or :line-line.
        path = re.sub(r":\d+(?:[-–]\d+)?$", "", path)
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = source.parent / candidate
        local_links += 1
        if not candidate.exists():
            errors.append(f"Broken link {source.relative_to(WRITING)}: {href}")
    pages.append(dict(source=str(source.relative_to(WRITING)),
                      sha256=digest, h2=page.tags["h2"],
                      ordered_lists=page.tags["ol"], tables=page.tags["table"]))

outline = sources[0].read_text(encoding="utf-8")
counts = {term: outline.count(term) for term in ["**核心目标（要说什么）：**", "**准备怎么说：**", "**注意点／强调：**"]}
if len(set(counts.values())) != 1:
    errors.append(f"Uneven paragraph planning fields: {counts}")
if "详细提纲 v3" not in outline:
    errors.append("Outline version is not v3")
result = dict(passed=not errors, pages=pages, local_links_checked=local_links,
              outline_writing_units=counts, errors=errors,
              visual_browser_check="not_performed; structural checks only",
              no_new_gpu_runs=True)
(HERE / "DOCUMENT_VALIDATION.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if not errors else 1)
