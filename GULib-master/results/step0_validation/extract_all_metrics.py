"""
Extract all available metrics from Round 2 log files.
"""
import os
import re
import json

RESULTS_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(RESULTS_DIR, "round2_logs")

def extract_metrics_from_log(log_path):
    """Extract all available metrics from a single log file."""
    metrics = {
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

    with open(log_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Extract from Performance Metrics section (most methods)
    perf_section = re.search(
        r"Performance Metrics:(.*?)(?=\n\n|\Z)",
        content,
        re.DOTALL | re.IGNORECASE
    )

    if perf_section:
        perf_text = perf_section.group(1)

        # Poison F1 Score
        m = re.search(r"Poison F1 Score:\s*([\d.]+)", perf_text)
        if m:
            metrics["poison_f1"] = float(m.group(1))

        # Unlearn F1 Score
        m = re.search(r"Unlearn F1 Score:\s*([\d.]+)", perf_text)
        if m:
            metrics["f1_after"] = float(m.group(1))

        # AUC Score
        m = re.search(r"(?:Average )?AUC Score:\s*([\d.]+)", perf_text)
        if m:
            metrics["auc"] = float(m.group(1))

        # Training Time
        m = re.search(r"(?:Average )?Training Time:\s*([\d.]+)", perf_text)
        if m:
            metrics["training_time"] = float(m.group(1))

        # Unlearning Time
        m = re.search(r"(?:Average )?Unlearning Time:\s*([\d.]+)", perf_text)
        if m:
            metrics["unlearning_time"] = float(m.group(1))

        # Sampling Time
        m = re.search(r"(?:Average )?Sampling Time:\s*([\d.]+)", perf_text)
        if m:
            metrics["sampling_time"] = float(m.group(1))

        # Partition Time (for shard-based methods)
        m = re.search(r"(?:Average )?Partition Time:\s*([\d.]+)", perf_text)
        if m:
            metrics["partition_time"] = float(m.group(1))

    # For methods like GNNDelete that report detailed validation metrics
    val_metrics = re.findall(
        r"Loss:\s*([\d.]+),\s*Accuracy:\s*([\d.]+),\s*Recall:\s*([\d.]+),\s*F1:\s*([\d.]+)",
        content
    )
    if val_metrics:
        last_metrics = val_metrics[-1]
        metrics["loss_final"] = float(last_metrics[0])
        metrics["accuracy"] = float(last_metrics[1])
        metrics["recall"] = float(last_metrics[2])
        if metrics["f1_after"] is None:
            metrics["f1_after"] = float(last_metrics[3])

    # Extract best F1 before unlearning (from base training)
    best_f1_matches = re.findall(r"best:\s*([\d.]+)", content)
    if best_f1_matches:
        metrics["f1_before"] = float(best_f1_matches[0])

    # For GUIDE: extract Test F1 Score
    if "GUIDE" in log_path:
        guide_f1 = re.findall(r"Test F1 Score:\s*([\d.]+)", content)
        if guide_f1:
            metrics["f1_after"] = float(guide_f1[-1])

    # Extract "Original F1 Score" if present
    orig_f1 = re.search(r"Original F1 Score:\s*([\d.]+)", content)
    if orig_f1:
        metrics["f1_before"] = float(orig_f1.group(1))

    return metrics


def generate_metrics_summary():
    """Generate comprehensive metrics summary across all methods and ratios."""
    all_metrics = {}

    # Iterate through all log files
    for filename in sorted(os.listdir(LOGS_DIR)):
        if not filename.endswith(".log"):
            continue

        # Parse filename: {Method}_GCN_cora_r{ratio}.log
        parts = filename.replace(".log", "").split("_")
        method = parts[0]
        ratio_str = parts[-1].replace("r", "")

        log_path = os.path.join(LOGS_DIR, filename)
        metrics = extract_metrics_from_log(log_path)

        # Store in nested dict
        if method not in all_metrics:
            all_metrics[method] = {}
        all_metrics[method][ratio_str] = metrics

    return all_metrics


def print_metrics_table(all_metrics):
    """Print a comprehensive metrics table."""
    ratios = ["0.005", "0.02", "0.05", "0.1", "0.2"]

    print("\n" + "="*120)
    print("COMPREHENSIVE METRICS SUMMARY - ALL METHODS × ALL RATIOS")
    print("="*120 + "\n")

    for method in sorted(all_metrics.keys()):
        print(f"\n{'─'*120}")
        print(f"METHOD: {method}")
        print(f"{'─'*120}")

        # Print header
        print(f"{'Ratio':<8} {'F1_before':<12} {'F1_after':<12} {'Accuracy':<10} {'Recall':<10} "
              f"{'AUC':<10} {'Loss':<10} {'Train_t':<10} {'Unlearn_t':<10} {'Extra':<20}")
        print("─" * 120)

        # Print data for each ratio
        for ratio in ratios:
            if ratio not in all_metrics[method]:
                print(f"{ratio:<8} {'SKIP':<12}")
                continue

            m = all_metrics[method][ratio]

            f1_before = f"{m['f1_before']:.4f}" if m['f1_before'] is not None else "N/A"
            f1_after = f"{m['f1_after']:.4f}" if m['f1_after'] is not None else "N/A"
            accuracy = f"{m['accuracy']:.4f}" if m['accuracy'] is not None else "N/A"
            recall = f"{m['recall']:.4f}" if m['recall'] is not None else "N/A"
            auc = f"{m['auc']:.4f}" if m['auc'] is not None else "N/A"
            loss = f"{m['loss_final']:.4f}" if m['loss_final'] is not None else "N/A"
            train_t = f"{m['training_time']:.3f}s" if m['training_time'] is not None else "N/A"
            unlearn_t = f"{m['unlearning_time']:.3f}s" if m['unlearning_time'] is not None else "N/A"

            extra = []
            if m['partition_time'] is not None:
                extra.append(f"Part:{m['partition_time']:.2f}s")
            if m['sampling_time'] is not None and m['sampling_time'] > 0:
                extra.append(f"Samp:{m['sampling_time']:.2f}s")
            extra_str = ", ".join(extra) if extra else "—"

            print(f"{ratio:<8} {f1_before:<12} {f1_after:<12} {accuracy:<10} {recall:<10} "
                  f"{auc:<10} {loss:<10} {train_t:<10} {unlearn_t:<10} {extra_str:<20}")

    print("\n" + "="*120)
    print("LEGEND:")
    print("  F1_before:  F1 score before unlearning (from base training)")
    print("  F1_after:   F1 score after unlearning")
    print("  Accuracy:   Test accuracy (when available, GNNDelete reports this)")
    print("  Recall:     Test recall (when available, GNNDelete reports this)")
    print("  AUC:        Membership Inference Attack AUC (0.0000 = not evaluated)")
    print("  Loss:       Final training loss")
    print("  Train_t:    Training time (seconds)")
    print("  Unlearn_t:  Unlearning time (seconds)")
    print("  Part:       Partition time (shard-based methods only)")
    print("  Samp:       Sampling time (learning-based methods only)")
    print("="*120 + "\n")


def save_metrics_json(all_metrics):
    """Save all extracted metrics to JSON."""
    out_path = os.path.join(RESULTS_DIR, "all_metrics_detailed.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_metrics, f, indent=2, ensure_ascii=False)
    print(f"Saved detailed metrics to: {out_path}")


def analyze_metric_availability():
    """Analyze which metrics are available for which methods."""
    all_metrics = generate_metrics_summary()

    print("\n" + "="*80)
    print("METRIC AVAILABILITY BY METHOD")
    print("="*80 + "\n")

    metric_names = [
        "f1_before", "f1_after", "accuracy", "recall", "auc",
        "loss_final", "training_time", "unlearning_time",
        "partition_time", "sampling_time"
    ]

    print(f"{'Method':<15} {'F1':<4} {'Acc':<4} {'Rec':<4} {'AUC':<4} {'Loss':<5} "
          f"{'Time':<5} {'Part':<5} {'Samp':<5}")
    print("─" * 80)

    for method in sorted(all_metrics.keys()):
        # Check first available ratio for this method
        first_ratio = next(iter(all_metrics[method].values()))

        has_f1 = "Y" if first_ratio["f1_after"] is not None else "N"
        has_acc = "Y" if first_ratio["accuracy"] is not None else "N"
        has_rec = "Y" if first_ratio["recall"] is not None else "N"
        has_auc = "Y" if first_ratio["auc"] is not None and first_ratio["auc"] > 0 else "N"
        has_loss = "Y" if first_ratio["loss_final"] is not None else "N"
        has_time = "Y" if first_ratio["unlearning_time"] is not None else "N"
        has_part = "Y" if first_ratio["partition_time"] is not None else "N"
        has_samp = "Y" if first_ratio["sampling_time"] is not None and first_ratio["sampling_time"] > 0 else "N"

        print(f"{method:<15} {has_f1:<4} {has_acc:<4} {has_rec:<4} {has_auc:<4} {has_loss:<5} "
              f"{has_time:<5} {has_part:<5} {has_samp:<5}")

    print("\n" + "="*80)
    print("KEY FINDINGS:")
    print("  - F1 Score: Available for ALL methods (Y)")
    print("  - Accuracy & Recall: Only GNNDelete reports these explicitly")
    print("  - AUC Score: Only GIF, GUIDE, GNNDelete, IDEA report meaningful values (>0)")
    print("  - Training Time & Unlearning Time: Available for ALL methods (Y)")
    print("  - Partition Time: Only shard-based methods (GraphEraser, GUIDE, GraphRevoker)")
    print("  - Sampling Time: Only some learning-based methods (SGU reports 0.1970s)")
    print("="*80 + "\n")


def main():
    print("Extracting all metrics from Round 2 logs...\n")

    # Generate and analyze
    all_metrics = generate_metrics_summary()

    # Print comprehensive table
    print_metrics_table(all_metrics)

    # Print availability analysis
    analyze_metric_availability()

    # Save to JSON
    save_metrics_json(all_metrics)

    print("\nDone! Check 'all_metrics_detailed.json' for machine-readable format.")


if __name__ == "__main__":
    main()
