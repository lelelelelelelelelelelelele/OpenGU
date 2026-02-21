"""Extract and summarize Step0 metrics from log files."""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Optional


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_LOGS_DIR = REPO_ROOT / "results" / "step0_validation" / "round2_logs"
DEFAULT_OUT_JSON = REPO_ROOT / "results" / "evaluation" / "step0" / "all_metrics_detailed.json"
DEFAULT_RATIOS = ["0.005", "0.02", "0.05", "0.1", "0.2"]


def extract_metrics_from_log(log_path: Path) -> Dict[str, Optional[float]]:
    metrics: Dict[str, Optional[float]] = {
        "f1_before": None,
        "f1_after": None,
        "accuracy": None,
        "recall": None,
        "auc": None,
        "loss_final": None,
        "training_time": None,
        "unlearning_time": None,
        "partition_time": None,
        "sampling_time": None,
        "poison_f1": None,
    }

    with log_path.open("r", encoding="utf-8", errors="replace") as file_obj:
        content = file_obj.read()

    perf_section = re.search(
        r"Performance Metrics:(.*?)(?=\n\n|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if perf_section:
        perf_text = perf_section.group(1)

        field_patterns = {
            "poison_f1": r"Poison F1 Score:\s*([\d.]+)",
            "f1_after": r"Unlearn F1 Score:\s*([\d.]+)",
            "auc": r"(?:Average )?AUC Score:\s*([\d.]+)",
            "training_time": r"(?:Average )?Training Time:\s*([\d.]+)",
            "unlearning_time": r"(?:Average )?Unlearning Time:\s*([\d.]+)",
            "sampling_time": r"(?:Average )?Sampling Time:\s*([\d.]+)",
            "partition_time": r"(?:Average )?Partition Time:\s*([\d.]+)",
        }
        for key, pattern in field_patterns.items():
            match = re.search(pattern, perf_text)
            if match:
                metrics[key] = float(match.group(1))

    val_metrics = re.findall(
        r"Loss:\s*([\d.]+),\s*Accuracy:\s*([\d.]+),\s*Recall:\s*([\d.]+),\s*F1:\s*([\d.]+)",
        content,
    )
    if val_metrics:
        last = val_metrics[-1]
        metrics["loss_final"] = float(last[0])
        metrics["accuracy"] = float(last[1])
        metrics["recall"] = float(last[2])
        if metrics["f1_after"] is None:
            metrics["f1_after"] = float(last[3])

    best_f1_matches = re.findall(r"best:\s*([\d.]+)", content)
    if best_f1_matches:
        metrics["f1_before"] = float(best_f1_matches[0])

    if "GUIDE" in log_path.name:
        guide_f1 = re.findall(r"Test F1 Score:\s*([\d.]+)", content)
        if guide_f1:
            metrics["f1_after"] = float(guide_f1[-1])

    orig_f1 = re.search(r"Original F1 Score:\s*([\d.]+)", content)
    if orig_f1:
        metrics["f1_before"] = float(orig_f1.group(1))

    return metrics


def generate_metrics_summary(logs_dir: Path) -> Dict[str, Dict[str, Dict[str, Optional[float]]]]:
    all_metrics: Dict[str, Dict[str, Dict[str, Optional[float]]]] = {}

    for log_path in sorted(logs_dir.glob("*.log")):
        parts = log_path.stem.split("_")
        if len(parts) < 2:
            continue
        method = parts[0]
        ratio_str = parts[-1].replace("r", "")

        metrics = extract_metrics_from_log(log_path)
        if method not in all_metrics:
            all_metrics[method] = {}
        all_metrics[method][ratio_str] = metrics

    return all_metrics


def print_metrics_table(all_metrics: Dict[str, Dict[str, Dict[str, Optional[float]]]], ratios=None) -> None:
    if ratios is None:
        ratios = DEFAULT_RATIOS

    print("\n" + "=" * 120)
    print("COMPREHENSIVE METRICS SUMMARY - ALL METHODS x ALL RATIOS")
    print("=" * 120 + "\n")

    for method in sorted(all_metrics.keys()):
        print(f"\n{'-' * 120}")
        print(f"METHOD: {method}")
        print(f"{'-' * 120}")

        print(
            f"{'Ratio':<8} {'F1_before':<12} {'F1_after':<12} {'Accuracy':<10} {'Recall':<10} "
            f"{'AUC':<10} {'Loss':<10} {'Train_t':<10} {'Unlearn_t':<10} {'Extra':<20}"
        )
        print("-" * 120)

        for ratio in ratios:
            if ratio not in all_metrics[method]:
                print(f"{ratio:<8} {'SKIP':<12}")
                continue

            record = all_metrics[method][ratio]
            f1_before = f"{record['f1_before']:.4f}" if record["f1_before"] is not None else "N/A"
            f1_after = f"{record['f1_after']:.4f}" if record["f1_after"] is not None else "N/A"
            accuracy = f"{record['accuracy']:.4f}" if record["accuracy"] is not None else "N/A"
            recall = f"{record['recall']:.4f}" if record["recall"] is not None else "N/A"
            auc = f"{record['auc']:.4f}" if record["auc"] is not None else "N/A"
            loss = f"{record['loss_final']:.4f}" if record["loss_final"] is not None else "N/A"
            train_t = f"{record['training_time']:.3f}s" if record["training_time"] is not None else "N/A"
            unlearn_t = (
                f"{record['unlearning_time']:.3f}s" if record["unlearning_time"] is not None else "N/A"
            )

            extras = []
            if record["partition_time"] is not None:
                extras.append(f"Part:{record['partition_time']:.2f}s")
            if record["sampling_time"] is not None and record["sampling_time"] > 0:
                extras.append(f"Samp:{record['sampling_time']:.2f}s")
            extra_str = ", ".join(extras) if extras else "-"

            print(
                f"{ratio:<8} {f1_before:<12} {f1_after:<12} {accuracy:<10} {recall:<10} "
                f"{auc:<10} {loss:<10} {train_t:<10} {unlearn_t:<10} {extra_str:<20}"
            )


def analyze_metric_availability(all_metrics: Dict[str, Dict[str, Dict[str, Optional[float]]]]) -> Dict[str, Dict[str, bool]]:
    availability: Dict[str, Dict[str, bool]] = {}
    for method in sorted(all_metrics.keys()):
        first_ratio = next(iter(all_metrics[method].values()))
        availability[method] = {
            "f1": first_ratio["f1_after"] is not None,
            "accuracy": first_ratio["accuracy"] is not None,
            "recall": first_ratio["recall"] is not None,
            "auc": first_ratio["auc"] is not None and first_ratio["auc"] > 0,
            "loss": first_ratio["loss_final"] is not None,
            "time": first_ratio["unlearning_time"] is not None,
            "partition": first_ratio["partition_time"] is not None,
            "sampling": first_ratio["sampling_time"] is not None and first_ratio["sampling_time"] > 0,
        }
    return availability


def save_metrics_json(all_metrics: Dict[str, Dict[str, Dict[str, Optional[float]]]], out_json: Path) -> Path:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with out_json.open("w", encoding="utf-8") as file_obj:
        json.dump(all_metrics, file_obj, indent=2, ensure_ascii=False)
    return out_json


def run_extraction(logs_dir: Path, out_json: Path, print_table: bool = True):
    all_metrics = generate_metrics_summary(logs_dir)
    if print_table:
        print_metrics_table(all_metrics)
    availability = analyze_metric_availability(all_metrics)
    output_path = save_metrics_json(all_metrics, out_json)
    return all_metrics, availability, output_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract metrics from Step0 logs")
    parser.add_argument("--logs-dir", type=Path, default=DEFAULT_LOGS_DIR)
    parser.add_argument("--out-json", type=Path, default=DEFAULT_OUT_JSON)
    parser.add_argument("--no-print-table", action="store_true")
    return parser


def main(argv=None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    all_metrics, availability, output_path = run_extraction(
        logs_dir=args.logs_dir,
        out_json=args.out_json,
        print_table=not args.no_print_table,
    )
    print(f"Methods parsed: {len(all_metrics)}")
    print(f"Availability entries: {len(availability)}")
    print(f"Saved detailed metrics to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
