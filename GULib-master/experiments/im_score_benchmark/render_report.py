"""Render one aggregate JSON into matching Markdown and static HTML reports."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any, List, Mapping, Sequence


def _number(value: Any, digits: int = 4) -> str:
    if value is None:
        return "N/A"
    return ("{0:." + str(digits) + "f}").format(float(value))


def render_markdown(aggregate: Mapping[str, Any]) -> str:
    if (
        aggregate.get("schema") != "im_score_benchmark.aggregate"
        or aggregate.get("version") != 1
    ):
        raise ValueError("input is not an IM aggregate v1 document")
    lines: List[str] = [
        "# IM 成熟算法 Selector 结果报告",
        "",
        "> 本报告只汇总输入 artifact；是否属于 formal evidence 由各 source manifest 与 Git provenance 决定。",
        "",
        "## 1. 方法汇总",
        "",
        "| Method | Rows | Mean time (s) | Max time (s) | Mean spread / degree | Registered win rows |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for method, summary in sorted(aggregate["method_summary"].items()):
        lines.append(
            "| {0} | {1} | {2} | {3} | {4} | {5} |".format(
                method,
                summary["row_count"],
                _number(summary["wall_seconds_mean"]),
                _number(summary["wall_seconds_max"]),
                _number(summary["spread_ratio_vs_degree_mean"]),
                summary["registered_degree_win_row_count"],
            )
        )
    lines.extend(
        [
            "",
            "## 2. 逐行结果",
            "",
            "| Dataset | Seed | k | Method | Time (s) | Peak RSS | Spread ratio | Paired CI95 | Certificate |",
            "|---|---:|---:|---|---:|---:|---:|---|---|",
        ]
    )
    for row in aggregate["rows"]:
        rss = row["peak_rss_bytes"]
        rss_text = "N/A" if rss is None else _number(rss / (1024 ** 3), 3) + " GiB"
        lines.append(
            "| {dataset} | {selector_seed} | {budget} | {method} | {time} | {rss} | {ratio} | [{lower}, {upper}] | {certificate} |".format(
                dataset=row["dataset"],
                selector_seed=row["selector_seed"],
                budget=row["budget"],
                method=row["method"],
                time=_number(row["wall_seconds"]),
                rss=rss_text,
                ratio=_number(row["spread_ratio_vs_degree"]),
                lower=_number(row["paired_ci95_lower_probability"]),
                upper=_number(row["paired_ci95_upper_probability"]),
                certificate=row["certificate_kind"] or "none",
            )
        )
    lines.extend(
        [
            "",
            "## 3. 解释边界",
            "",
            "- 单行 degree win：spread ratio 至少 1.02，且 paired 95% CI 下界大于 0。",
            "- 单行胜出不等于通过小图/大图 promotion gate。",
            "- paper_equivalent=false 的 certificate 只能按其显式 kind 解读。",
            "",
        ]
    )
    return "\n".join(lines)


def render_html(markdown_text: str, aggregate: Mapping[str, Any]) -> str:
    del markdown_text
    method_rows = []
    for method, summary in sorted(aggregate["method_summary"].items()):
        method_rows.append(
            "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>".format(
                html.escape(method),
                summary["row_count"],
                _number(summary["wall_seconds_mean"]),
                _number(summary["wall_seconds_max"]),
                _number(summary["spread_ratio_vs_degree_mean"]),
                summary["registered_degree_win_row_count"],
            )
        )
    detail_rows = []
    for row in aggregate["rows"]:
        detail_rows.append(
            "<tr><td>{dataset}</td><td>{seed}</td><td>{budget}</td><td>{method}</td><td>{time}</td><td>{ratio}</td><td>[{lower}, {upper}]</td><td>{certificate}</td></tr>".format(
                dataset=html.escape(str(row["dataset"])),
                seed=row["selector_seed"],
                budget=row["budget"],
                method=html.escape(str(row["method"])),
                time=_number(row["wall_seconds"]),
                ratio=_number(row["spread_ratio_vs_degree"]),
                lower=_number(row["paired_ci95_lower_probability"]),
                upper=_number(row["paired_ci95_upper_probability"]),
                certificate=html.escape(str(row["certificate_kind"] or "none")),
            )
        )
    return """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>IM 成熟算法 Selector 结果报告</title>
  <style>
    body {{ margin:0; background:#07111f; color:#e8eef6; font:16px/1.65 "Segoe UI","Microsoft YaHei",sans-serif; }}
    main {{ max-width:1180px; margin:auto; padding:48px 28px 90px; }}
    h1 {{ font-size:2.4rem; }} h2 {{ margin-top:48px; border-bottom:1px solid #29415e; padding-bottom:8px; }}
    .note {{ border-left:4px solid #55d6be; background:#10253a; padding:16px 18px; }}
    .table {{ overflow-x:auto; }} table {{ width:100%; border-collapse:collapse; margin:20px 0; }}
    th,td {{ border:1px solid #29415e; padding:10px; text-align:left; vertical-align:top; }}
    th {{ background:#142a42; }} tr:nth-child(even) td {{ background:#0d1b2d; }}
  </style>
</head>
<body><main>
<h1>IM 成熟算法 Selector 结果报告</h1>
<p class="note">本报告只汇总输入 artifact；formal status 仍由 source manifest 与 Git provenance 决定。</p>
<h2>1. 方法汇总</h2>
<div class="table"><table>
<thead><tr><th>Method</th><th>Rows</th><th>Mean time</th><th>Max time</th><th>Mean spread / degree</th><th>Win rows</th></tr></thead>
<tbody>{method_rows}</tbody></table></div>
<h2>2. 逐行结果</h2>
<div class="table"><table>
<thead><tr><th>Dataset</th><th>Seed</th><th>k</th><th>Method</th><th>Time</th><th>Spread ratio</th><th>Paired CI95</th><th>Certificate</th></tr></thead>
<tbody>{detail_rows}</tbody></table></div>
<h2>3. 解释边界</h2>
<ul><li>单行 degree win 要求 ratio ≥ 1.02 且 paired CI95 下界大于 0。</li>
<li>单行胜出不等于通过完整 promotion gate。</li>
<li>paper_equivalent=false 的 certificate 只能按显式 kind 解读。</li></ul>
</main></body></html>
""".format(
        method_rows="\n".join(method_rows),
        detail_rows="\n".join(detail_rows),
    )


def _write_text(path: Path, text: str, overwrite: bool) -> None:
    target = path.expanduser().resolve(strict=False)
    if target.exists() and not overwrite:
        raise FileExistsError(
            "output already exists; pass --overwrite explicitly: {0}".format(
                target
            )
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--html", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    return parser


def main(argv: Sequence[str] = None) -> int:
    args = _parser().parse_args(argv)
    aggregate = json.loads(args.input.read_text(encoding="utf-8"))
    markdown_text = render_markdown(aggregate)
    html_text = render_html(markdown_text, aggregate)
    _write_text(args.markdown, markdown_text, bool(args.overwrite))
    _write_text(args.html, html_text, bool(args.overwrite))
    print(
        json.dumps(
            {
                "markdown": str(args.markdown.expanduser().resolve(strict=False)),
                "html": str(args.html.expanduser().resolve(strict=False)),
                "row_count": len(aggregate["rows"]),
            },
            ensure_ascii=False,
            allow_nan=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
