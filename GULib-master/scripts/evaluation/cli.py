"""Unified command line entrypoint for Step0 evaluation tooling."""

import argparse
from pathlib import Path

from .metrics import extractor


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STEP0_INPUT = REPO_ROOT / "results" / "step0_validation" / "round2_results.json"
DEFAULT_STEP0_OUT_ROOT = REPO_ROOT / "results" / "evaluation" / "step0"
DEFAULT_ATTACK_OUT_ROOT = REPO_ROOT / "results" / "evaluation" / "attack"


def _load_step0_plots():
    from .plotting import step0_plots

    return step0_plots


def _load_attack_charts():
    from .plotting import attack_charts

    return attack_charts


def _cmd_extract(args: argparse.Namespace) -> int:
    all_metrics, availability, output_path = extractor.run_extraction(
        logs_dir=args.logs_dir,
        out_json=args.out_json,
        print_table=not args.no_print_table,
    )
    print(f"Methods parsed: {len(all_metrics)}")
    print(f"Availability entries: {len(availability)}")
    print(f"Saved detailed metrics to: {output_path}")
    return 0


def _cmd_plot(args: argparse.Namespace) -> int:
    if args.type == "step0":
        step0_plots = _load_step0_plots()
        results = step0_plots.load_round2(args.input_json)
        compat_json = args.compat_json or (args.out_dir.parent / "method_compatibility.json")
        report_md = args.report_md or (args.out_dir.parent / "round2_detail.md")
        step0_plots.run_step0_plotting(results, args.out_dir, compat_json, report_md)
        print(f"Step0 plots saved to: {args.out_dir}")
        print(f"Compatibility JSON saved to: {compat_json}")
        print(f"Report saved to: {report_md}")
        return 0

    if args.type == "attack":
        attack_charts = _load_attack_charts()
        payload = attack_charts.load_attack_matrix(args.input_json)
        outputs = attack_charts.generate_attack_charts(payload, args.out_dir)
        for path in outputs:
            print(f"Saved: {path}")
        return 0

    raise ValueError(f"Unsupported plot type: {args.type}")


def _cmd_report(args: argparse.Namespace) -> int:
    step0_plots = _load_step0_plots()
    results = step0_plots.load_round2(args.input_json)
    compat_json = args.compat_json
    compat = step0_plots.generate_compatibility_json(results, compat_json)
    step0_plots.generate_round2_detail_md(results, compat, args.out_md, plot_rel_dir=args.plot_rel_dir)
    print(f"Compatibility JSON saved to: {compat_json}")
    print(f"Report saved to: {args.out_md}")
    return 0


def _cmd_all(args: argparse.Namespace) -> int:
    step0_plots = _load_step0_plots()

    out_root = args.out_root
    plot_dir = out_root / "plots"
    metrics_json = out_root / "all_metrics_detailed.json"
    compat_json = out_root / "method_compatibility.json"
    report_md = out_root / "round2_detail.md"

    extractor.run_extraction(
        logs_dir=args.logs_dir,
        out_json=metrics_json,
        print_table=not args.no_print_table,
    )

    results = step0_plots.load_round2(args.step0_input_json)
    step0_plots.run_step0_plotting(results, plot_dir, compat_json, report_md)

    if args.attack_input_json:
        attack_charts = _load_attack_charts()
        payload = attack_charts.load_attack_matrix(args.attack_input_json)
        attack_out = args.attack_out_dir or (DEFAULT_ATTACK_OUT_ROOT / "plots")
        attack_charts.generate_attack_charts(payload, attack_out)
        print(f"Attack plots saved to: {attack_out}")

    print("All done.")
    print(f"Metrics: {metrics_json}")
    print(f"Step0 plots: {plot_dir}")
    print(f"Step0 report: {report_md}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m scripts.evaluation",
        description="Unified Step0 evaluation utilities",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_parser = subparsers.add_parser("extract", help="Extract metrics from logs")
    extract_parser.add_argument("--logs-dir", type=Path, default=extractor.DEFAULT_LOGS_DIR)
    extract_parser.add_argument("--out-json", type=Path, default=extractor.DEFAULT_OUT_JSON)
    extract_parser.add_argument("--no-print-table", action="store_true")
    extract_parser.set_defaults(handler=_cmd_extract)

    plot_parser = subparsers.add_parser("plot", help="Generate plots")
    plot_parser.add_argument("--type", choices=["step0", "attack"], required=True)
    plot_parser.add_argument("--input-json", type=Path, required=True)
    plot_parser.add_argument("--out-dir", type=Path, required=True)
    plot_parser.add_argument("--compat-json", type=Path)
    plot_parser.add_argument("--report-md", type=Path)
    plot_parser.set_defaults(handler=_cmd_plot)

    report_parser = subparsers.add_parser("report", help="Generate Step0 markdown report")
    report_parser.add_argument("--input-json", type=Path, required=True)
    report_parser.add_argument("--compat-json", type=Path, default=DEFAULT_STEP0_OUT_ROOT / "method_compatibility.json")
    report_parser.add_argument("--out-md", type=Path, default=DEFAULT_STEP0_OUT_ROOT / "round2_detail.md")
    report_parser.add_argument("--plot-rel-dir", type=str, default="plots")
    report_parser.set_defaults(handler=_cmd_report)

    all_parser = subparsers.add_parser("all", help="Run extract + step0 plots + report (and optional attack plots)")
    all_parser.add_argument("--logs-dir", type=Path, default=extractor.DEFAULT_LOGS_DIR)
    all_parser.add_argument("--step0-input-json", type=Path, default=DEFAULT_STEP0_INPUT)
    all_parser.add_argument("--out-root", type=Path, default=DEFAULT_STEP0_OUT_ROOT)
    all_parser.add_argument("--no-print-table", action="store_true")
    all_parser.add_argument("--attack-input-json", type=Path)
    all_parser.add_argument("--attack-out-dir", type=Path)
    all_parser.set_defaults(handler=_cmd_all)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
