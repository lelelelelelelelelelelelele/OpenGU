from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
RUNS = {
    "AAGU-032": {
        "path": Path("results/runs/gpu4090/aagu032-extended-v2-multi-gcn-retrain/aagu032-recovery-full-20260920/run.json"),
        "sha256": "8391e397c1c12075e66249844fe93ca70423a0fede0785faae23185e0541e1ed",
        "run_id": "aagu032-recovery-full-20260920",
        "cells": 360,
    },
    "AAGU-053": {
        "path": Path("results/runs/gpu4090/aagu053-im-group-budget10/aagu053-newtraining-full-20260920/run.json"),
        "sha256": "dfb6f7c88021291847765a901d61efa698df889a8157fedc2f9639d50a852e7e",
        "run_id": "aagu053-newtraining-full-20260920",
        "cells": 96,
    },
}
DATASETS = ("Cora", "CiteSeer", "PubMed")
BASELINES = ("degree", "random")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_run(label: str) -> tuple[dict, dict[str, dict]]:
    spec = RUNS[label]
    path = ROOT / spec["path"]
    if sha256(path) != spec["sha256"]:
        raise ValueError(f"{label}: run manifest SHA-256 mismatch: {path}")
    run = json.loads(path.read_text(encoding="utf-8"))
    if run.get("status") != "completed" or run.get("run_id") != spec["run_id"]:
        raise ValueError(f"{label}: run identity/status mismatch")
    if len(run.get("cells", [])) != spec["cells"]:
        raise ValueError(f"{label}: expected {spec['cells']} cells, found {len(run.get('cells', []))}")

    loaded: dict[str, dict] = {}
    seen: set[str] = set()
    for cell in run["cells"]:
        cell_id = cell["cell_id"]
        if cell_id in seen:
            raise ValueError(f"{label}: duplicate cell_id {cell_id}")
        seen.add(cell_id)
        if cell.get("status") != "completed":
            raise ValueError(f"{label}: non-completed cell {cell_id}")
        cell_root = path.parent / cell["path"]
        for name, declaration in cell["files"].items():
            artifact = cell_root / name
            if sha256(artifact) != declaration["sha256"]:
                raise ValueError(f"{label}: artifact hash mismatch: {artifact}")
        metrics = json.loads((cell_root / "metrics.json").read_text(encoding="utf-8"))
        selection = json.loads((cell_root / "selection.json").read_text(encoding="utf-8"))
        if metrics.get("cell_id") != cell_id or selection.get("cell_id") != cell_id:
            raise ValueError(f"{label}: artifact cell_id mismatch: {cell_id}")
        loaded[cell_id] = {"cell": cell, "metrics": metrics, "selection": selection}
    return run, loaded


def metric(cell_record: dict, field: str) -> float | None:
    for row in cell_record["metrics"].get("rows", []):
        if row.get("stage") == "utility":
            value = row.get("values", {}).get(field)
            return float(value) if value is not None else None
    raise ValueError(f"utility.{field} missing")


def method_metric(cell_record: dict, field: str) -> float | None:
    for row in cell_record["metrics"].get("rows", []):
        if row.get("stage") == "method":
            value = row.get("values", {}).get(field)
            return float(value) if value is not None else None
    return None


def sample_sd(values: list[float]) -> float | None:
    return statistics.stdev(values) if len(values) > 1 else None


def pct(value: float | None) -> float | None:
    return value * 100 if value is not None else None


def selector_name(value: str) -> str:
    return value.replace("\\", "/").rsplit("/", 1)[-1].removesuffix(".yaml")


def fmt_mean_sd(mean: float, sd: float | None, unit: str) -> str:
    return f"{mean:.2f} ± {sd:.2f} {unit}" if sd is not None else f"{mean:.2f} {unit}"


def write_csv(name: str, rows: list[dict]) -> None:
    path = OUT / name
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def cache_counts(run: dict) -> dict:
    result = {}
    for layer in ("method", "selection", "score"):
        result[layer] = dict(sorted(Counter(c.get("cache", {}).get(layer, "unknown") for c in run["cells"]).items()))
    result["method_producer_called"] = dict(sorted(Counter(str(c.get("producer_called", {}).get("method", "unknown")).lower() for c in run["cells"]).items()))
    return result


def main() -> None:
    run032, cells032 = load_run("AAGU-032")
    run053, cells053 = load_run("AAGU-053")
    provenance = {}
    for label, run in (("AAGU-032", run032), ("AAGU-053", run053)):
        spec = RUNS[label]
        manifest = ROOT / spec["path"]
        provenance[label] = {
            "manifest": str(spec["path"]).replace("\\", "/"),
            "manifest_sha256": sha256(manifest),
            "run_id": run["run_id"],
            "commit": run["commit"],
            "config_path": run["config_path"],
            "status": run["status"],
            "cells": len(run["cells"]),
            "declared_files_verified": sum(len(c["files"]) for c in run["cells"]),
            "cache": cache_counts(run),
        }

    # AAGU-032: Retrain-only test accuracy, retaining the complete selector identity.
    groups032: dict[tuple, list[dict]] = defaultdict(list)
    coord032 = set()
    for record in cells032.values():
        cell = record["cell"]
        cond = cell["conditions"]
        if cond["method"] != "Retrain":
            raise ValueError("AAGU-032 contains a non-Retrain cell")
        key = (cond["dataset_name"], cond["selector_ref"], cond["budget_ratio"], cond["training_seed"])
        if key in coord032:
            raise ValueError(f"AAGU-032 duplicate scientific coordinate {key}")
        coord032.add(key)
        after = metric(record, "f1_after")
        if after is None:
            raise ValueError(f"AAGU-032 missing utility.f1_after: {cell['cell_id']}")
        groups032[key[:3]].append({"seed": cond["training_seed"], "accuracy": after, "selection_id": record["selection"].get("selection_id")})

    summary032 = []
    index032 = {}
    for (dataset, selector_ref, budget), rows in sorted(groups032.items()):
        vals = [r["accuracy"] for r in rows]
        summary = {
            "dataset": dataset,
            "selector": selector_name(selector_ref),
            "selector_ref": selector_ref,
            "budget_ratio": budget,
            "n_training_seeds": len(vals),
            "training_seeds": ";".join(str(r["seed"]) for r in sorted(rows, key=lambda x: x["seed"])),
            "test_accuracy_after_mean_percent": statistics.mean(vals) * 100,
            "test_accuracy_after_sample_sd_pp": (sample_sd(vals) * 100) if sample_sd(vals) is not None else None,
        }
        summary032.append(summary)
        index032[(dataset, selector_name(selector_ref), budget)] = rows
    if len(summary032) != 120:
        raise ValueError(f"AAGU-032 expected 120 selector/budget/dataset summaries, got {len(summary032)}")

    contrasts032 = []
    datasets032: dict[str, dict] = {}
    for dataset in DATASETS:
        dataset_rows = [r for r in summary032 if r["dataset"] == dataset]
        all_values = [r["test_accuracy_after_mean_percent"] for r in dataset_rows]
        datasets032[dataset] = {
            "groups": len(dataset_rows),
            "cells": sum(r["n_training_seeds"] for r in dataset_rows),
            "equal_group_mean_test_accuracy_after_percent": statistics.mean(all_values),
        }
    for dataset in DATASETS:
        selectors = sorted({selector for ds, selector, _ in index032 if ds == dataset})
        budgets = sorted({budget for ds, _, budget in index032 if ds == dataset})
        for budget in budgets:
            for selector in selectors:
                for baseline in BASELINES:
                    a = index032[(dataset, selector, budget)]
                    b = index032[(dataset, baseline, budget)]
                    by_seed_a = {r["seed"]: r["accuracy"] for r in a}
                    by_seed_b = {r["seed"]: r["accuracy"] for r in b}
                    if by_seed_a.keys() != by_seed_b.keys():
                        raise ValueError(f"AAGU-032 seed mismatch: {(dataset, selector, baseline, budget)}")
                    diffs = [(by_seed_a[s] - by_seed_b[s]) * 100 for s in sorted(by_seed_a)]
                    contrasts032.append({
                        "dataset": dataset,
                        "budget_ratio": budget,
                        "selector": selector,
                        "reference": baseline,
                        "n_paired_training_seeds": len(diffs),
                        "test_accuracy_difference_pp": statistics.mean(diffs),
                        "paired_sample_sd_pp": sample_sd(diffs),
                        "lower/equal/higher": "lower" if statistics.mean(diffs) < -1e-12 else "higher" if statistics.mean(diffs) > 1e-12 else "equal",
                    })

    # AAGU-053: strict within-run GNNDelete/Retrain pairs on identical selected nodes.
    pairs053: dict[tuple, dict] = {}
    for record in cells053.values():
        cell = record["cell"]
        cond = cell["conditions"]
        selector = selector_name(cond["selector_ref"])
        selector_seed = cond.get("im_selector_seed", cond.get("random_selector_seed", "fixed"))
        key = (cond["dataset_name"], selector, selector_seed, cond["training_seed"], cond["budget_ratio"])
        method = cond["method"]
        if method not in ("GNNDelete", "Retrain"):
            raise ValueError(f"AAGU-053 unexpected method {method}")
        if method in pairs053.setdefault(key, {}):
            raise ValueError(f"AAGU-053 duplicate pair member: {key}/{method}")
        pairs053[key][method] = record

    pair_rows = []
    group053: dict[tuple, list[dict]] = defaultdict(list)
    for key, methods in sorted(pairs053.items(), key=lambda item: tuple(str(v) for v in item[0])):
        if set(methods) != {"GNNDelete", "Retrain"}:
            raise ValueError(f"AAGU-053 unmatched methods: {key}")
        gu, retrain = methods["GNNDelete"], methods["Retrain"]
        sel_gu, sel_rt = gu["selection"], retrain["selection"]
        if sel_gu.get("selection_id") != sel_rt.get("selection_id") or sel_gu.get("selected_nodes") != sel_rt.get("selected_nodes"):
            raise ValueError(f"AAGU-053 selection mismatch: {key}")
        p0 = metric(gu, "f1_before")
        f_gu = metric(gu, "f1_after")
        f_rt = metric(retrain, "f1_after")
        if None in (p0, f_gu, f_rt):
            raise ValueError(f"AAGU-053 missing paired endpoint: {key}")
        row = {
            "dataset": key[0],
            "selector": key[1],
            "selector_seed": key[2],
            "training_seed": key[3],
            "budget_ratio": key[4],
            "selection_id": sel_gu["selection_id"],
            "requested_k": sel_gu.get("requested_k"),
            "P0_test_accuracy_percent": p0 * 100,
            "GNNDelete_test_accuracy_percent": f_gu * 100,
            "Retrain_test_accuracy_percent": f_rt * 100,
            "P0_minus_GU_pp": (p0 - f_gu) * 100,
            "P0_minus_Retrain_pp": (p0 - f_rt) * 100,
            "Retrain_minus_GU_pp": (f_rt - f_gu) * 100,
            "GNNDelete_update_detection_auc": method_metric(gu, "update_detection_auc"),
        }
        pair_rows.append(row)
        group053[(key[0], key[1])].append(row)
    if len(pair_rows) != 48:
        raise ValueError(f"AAGU-053 expected 48 strict pairs, got {len(pair_rows)}")

    summary053 = []
    for (dataset, selector), rows in sorted(group053.items()):
        n = len(rows)
        summary = {"dataset": dataset, "selector": selector, "n_selection_requests": n}
        for field in (
            "P0_test_accuracy_percent",
            "GNNDelete_test_accuracy_percent",
            "Retrain_test_accuracy_percent",
            "P0_minus_GU_pp",
            "P0_minus_Retrain_pp",
            "Retrain_minus_GU_pp",
        ):
            vals = [r[field] for r in rows]
            summary[f"{field}_mean"] = statistics.mean(vals)
            summary[f"{field}_sample_sd"] = sample_sd(vals)
        summary["update_detection_auc_mean"] = statistics.mean(
            [r["GNNDelete_update_detection_auc"] for r in rows if r["GNNDelete_update_detection_auc"] is not None]
        ) if any(r["GNNDelete_update_detection_auc"] is not None for r in rows) else None
        summary["update_detection_auc_n"] = sum(r["GNNDelete_update_detection_auc"] is not None for r in rows)
        summary053.append(summary)

    dataset_summary053 = []
    for dataset in DATASETS:
        rows = [r for r in pair_rows if r["dataset"] == dataset]
        if len(rows) != 16:
            raise ValueError(f"AAGU-053 expected 16 requests for {dataset}, got {len(rows)}")
        out = {"dataset": dataset, "n_selection_requests_equal_weight": len(rows)}
        for field in (
            "P0_test_accuracy_percent",
            "GNNDelete_test_accuracy_percent",
            "Retrain_test_accuracy_percent",
            "P0_minus_GU_pp",
            "P0_minus_Retrain_pp",
            "Retrain_minus_GU_pp",
        ):
            out[f"{field}_mean"] = statistics.mean(r[field] for r in rows)
        aucs = [r["GNNDelete_update_detection_auc"] for r in rows if r["GNNDelete_update_detection_auc"] is not None]
        out["update_detection_auc_mean"] = statistics.mean(aucs) if aucs else None
        out["update_detection_auc_n"] = len(aucs)
        dataset_summary053.append(out)

    full_variants = ("gt_full", "gt_full_all_trainable", "gt_full_all_trainable_hops3")
    full_variant_contrasts = {}
    full_variant_random_contrasts = {}
    for dataset in DATASETS:
        rows = [r for r in contrasts032 if r["dataset"] == dataset and r["reference"] == "degree" and r["selector"] in full_variants]
        random_rows = [r for r in contrasts032 if r["dataset"] == dataset and r["reference"] == "random" and r["selector"] in full_variants]
        if len(rows) != 12:
            raise ValueError(f"AAGU-032 expected 12 D-full/degree contrasts for {dataset}, got {len(rows)}")
        if len(random_rows) != 12:
            raise ValueError(f"AAGU-032 expected 12 D-full/random contrasts for {dataset}, got {len(random_rows)}")
        full_variant_contrasts[dataset] = {
            "n_selector_budget_means": len(rows),
            "lower": sum(r["lower/equal/higher"] == "lower" for r in rows),
            "equal": sum(r["lower/equal/higher"] == "equal" for r in rows),
            "higher": sum(r["lower/equal/higher"] == "higher" for r in rows),
            "mean_difference_pp": statistics.mean(r["test_accuracy_difference_pp"] for r in rows),
            "by_variant": {
                selector: {
                    "mean_difference_pp_across_four_budgets": statistics.mean(r["test_accuracy_difference_pp"] for r in rows if r["selector"] == selector),
                    "lower/equal/higher_budgets": {
                        label: sum(r["lower/equal/higher"] == label for r in rows if r["selector"] == selector)
                        for label in ("lower", "equal", "higher")
                    },
                }
                for selector in full_variants
            },
        }
        full_variant_random_contrasts[dataset] = {
            "n_selector_budget_means": len(random_rows),
            "lower": sum(r["lower/equal/higher"] == "lower" for r in random_rows),
            "equal": sum(r["lower/equal/higher"] == "equal" for r in random_rows),
            "higher": sum(r["lower/equal/higher"] == "higher" for r in random_rows),
            "mean_difference_pp": statistics.mean(r["test_accuracy_difference_pp"] for r in random_rows),
        }

    write_csv("AAGU-032-selector-budget-summary.csv", summary032)
    write_csv("AAGU-032-paired-baseline-contrasts.csv", contrasts032)
    write_csv("AAGU-053-paired-GNNDelete-Retrain.csv", pair_rows)
    write_csv("AAGU-053-selector-summary.csv", summary053)
    write_csv("AAGU-053-dataset-summary.csv", dataset_summary053)
    summary = {
        "analysis_scope": "current 3000-epoch parameter run outputs only; no prior-parameter results are read",
        "training_default_source": "experiments/modular_config.py:73-75",
        "provenance": provenance,
        "AAGU-032": {
            "per_dataset": datasets032,
            "selector_names": sorted({r["selector"] for r in summary032}),
            "budget_ratios": sorted({r["budget_ratio"] for r in summary032}),
            "comparisons_vs_degree": {
                dataset: {
                    "lower": sum(r["lower/equal/higher"] == "lower" for r in contrasts032 if r["dataset"] == dataset and r["reference"] == "degree" and r["selector"] not in BASELINES),
                    "equal": sum(r["lower/equal/higher"] == "equal" for r in contrasts032 if r["dataset"] == dataset and r["reference"] == "degree" and r["selector"] not in BASELINES),
                    "higher": sum(r["lower/equal/higher"] == "higher" for r in contrasts032 if r["dataset"] == dataset and r["reference"] == "degree" and r["selector"] not in BASELINES),
                    "mean_difference_pp": statistics.mean(r["test_accuracy_difference_pp"] for r in contrasts032 if r["dataset"] == dataset and r["reference"] == "degree" and r["selector"] not in BASELINES),
                }
                for dataset in DATASETS
            },
            "D-full_variants_vs_degree": full_variant_contrasts,
            "D-full_variants_vs_random": full_variant_random_contrasts,
            "contrasts_against_two_baselines": len(contrasts032),
        },
        "AAGU-053": {
            "strict_pairs": len(pair_rows),
            "per_dataset_equal_request_weight": dataset_summary053,
            "selector_summaries": summary053,
            "seed_interpretation": "selector seed varies for IM/Random; the three requests are not independent training seeds",
        },
            "metric_units": "test accuracy levels in percent; differences in percentage points; sample SD is descriptive",
    }
    (OUT / "summary-current-only.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    selector_order032 = list(dict.fromkeys(selector_name(c["conditions"]["selector_ref"]) for c in run032["cells"]))
    selector_order053 = list(dict.fromkeys(selector_name(c["conditions"]["selector_ref"]) for c in run053["cells"]))
    budget_order = sorted({r["budget_ratio"] for r in summary032})
    lookup032 = {(r["dataset"], r["selector"], r["budget_ratio"]): r for r in summary032}
    lookup053 = {(r["dataset"], r["selector"]): r for r in summary053}
    for dataset in DATASETS:
        lines = [
            f"# {dataset}: current 3000-epoch result tables",
            "",
            "> Scope: generated only from the current AAGU-032 and AAGU-053 run manifests; previous-parameter result files were not read.",
            "> Metric note: `utility.f1_after` / `f1_before` is computed by direct argmax accuracy in `experiments/unlearning_outputs.py`. Tables therefore label the endpoint test accuracy. Since these are single-label classification tasks, micro-F1 would numerically equal accuracy; macro-F1 is not present in these artifacts.",
            "",
            "## AAGU-032 · Retrain test accuracy",
            "",
            "Entries are mean ± sample SD over 3 training seeds; levels are percentages. AAGU-032 contains only full Retrain outcomes, so this table describes retained-task utility, not the behavior of GNNDelete or forgetting quality.",
            "",
            "| Selector | " + " | ".join(f"{b:.0%}" for b in budget_order) + " |",
            "|---|" + "|".join(["---:"] * len(budget_order)) + "|",
        ]
        for selector in selector_order032:
            entries = []
            for budget in budget_order:
                row = lookup032[(dataset, selector, budget)]
                entries.append(fmt_mean_sd(row["test_accuracy_after_mean_percent"], row["test_accuracy_after_sample_sd_pp"], "%"))
            lines.append(f"| {selector} | " + " | ".join(entries) + " |")
        lines += [
            "",
            "## AAGU-053 · GNNDelete and same-request Retrain",
            "",
            "Each GU/Retrain comparison uses identical selected nodes. `n` is the number of selector requests (Degree: 1; other selectors: 3), with one training seed. Means ± sample SD describe variation across requests, not across independently trained models. Difference columns are percentage points.",
            "",
            "| Selector | n | P0 test acc. (%) | GNNDelete (%) | Retrain (%) | P0−GU (pp) | P0−Retrain (pp) | Retrain−GU (pp) |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for selector in selector_order053:
            row = lookup053[(dataset, selector)]
            def col(field: str, unit: str) -> str:
                return fmt_mean_sd(row[f"{field}_mean"], row[f"{field}_sample_sd"], unit)
            lines.append(
                f"| {selector} | {row['n_selection_requests']} | "
                f"{col('P0_test_accuracy_percent', '%')} | "
                f"{col('GNNDelete_test_accuracy_percent', '%')} | "
                f"{col('Retrain_test_accuracy_percent', '%')} | "
                f"{col('P0_minus_GU_pp', 'pp')} | "
                f"{col('P0_minus_Retrain_pp', 'pp')} | "
                f"{col('Retrain_minus_GU_pp', 'pp')} |"
            )
        lines += [
            "",
            "Exact 48 paired requests: `AAGU-053-paired-GNNDelete-Retrain.csv`. Equal-request-weight dataset means, including the posterior-change membership AUC: `AAGU-053-dataset-summary.csv`. This AUC is an auxiliary update-detection measure, not a standalone privacy guarantee.",
            "",
        ]
        (OUT / f"{dataset.lower()}-3000-only-tables.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
