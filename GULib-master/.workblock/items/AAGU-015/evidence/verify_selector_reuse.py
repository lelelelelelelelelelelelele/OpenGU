"""Disposable CPU proof of AAGU-015 Selector outputs and downstream reuse."""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import pickle
import subprocess
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[4]
CONFIG = ROOT / "experiments/configs/aagu015"


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def hashes(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()} if root.exists() else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="New directory under this source project's .workblock/runtime")
    args = parser.parse_args()
    # OpenGU imports parse process argv; these flags belong only to this verifier.
    sys.argv = [sys.argv[0]]
    output = Path(args.output).resolve()
    runtime = (ROOT / ".workblock/runtime").resolve()
    if runtime not in output.parents:
        raise ValueError("verification output must stay under source .workblock/runtime")
    output.mkdir(parents=True, exist_ok=False)
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    sys.path.insert(0, str(ROOT))
    import torch
    import yaml
    from torch_geometric.data import Data
    from experiments.aagu015.definitions import dry_run
    from experiments.modular_config import load_experiment, load_instance
    from experiments.modular_execution import ExecutionContext
    from experiments.modular_run import execute, read_dataset
    import experiments.modular_run as entry
    import experiments.modular_gu as gu_entry
    from experiments.target_direct_v1.methods import uses_model
    from experiments.c_target_v1.core import pair_metrics
    from utils.target_checkpoint import data_identity, sha256_file

    torch.set_num_threads(1)
    torch.manual_seed(7)
    protected = {p: hashes(ROOT / p) for p in (
        "data", "results/cache_v2", "results/cache", "results/selection_cache",
        "results/score_cache", "results/runs", "results/_journal")}
    yaml_before = {p.relative_to(CONFIG).as_posix(): sha256_file(p)
                   for p in sorted(CONFIG.rglob("*.yaml"))}
    expansion = dry_run()
    plans = [load_experiment(p) for p in sorted((CONFIG / "generated/stage_s").glob("*.yaml"))]
    assert len(plans) == 18
    assert all(p["stage"] == "selector" and len(p["selectors"]) == 17
               and not p["unlearnings"] and not p["evaluations"] for p in plans)
    assert {p["dataset"]["dataset"]["name"] for p in plans} == {"Cora", "CiteSeer", "PubMed"}
    for p in plans:
        split = p["dataset"]["split"]
        assert [split[k] for k in ("train_ratio", "val_ratio", "test_ratio", "seed")] == [0.7, 0.1, 0.2, 2024]
        for selector in p["selectors"]:
            assert selector["candidate"] == {"pool": "train_mask"}
            if "target_loss" in selector["parameters"]:
                assert selector["parameters"]["target_loss"]["source"] == "validation_mask"

    def write_yaml(name, value):
        path = output / name
        path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")
        return path

    # Deliberately separate from the three real datasets: 20-node 70/10/20 fixture.
    n = 20
    edges = torch.stack([torch.arange(n - 1), torch.arange(1, n)])
    data = Data(x=torch.randn(n, 3), y=torch.arange(n) % 2,
                edge_index=torch.cat([edges, edges.flip(0)], dim=1),
                train_mask=torch.arange(n) < 14,
                val_mask=(torch.arange(n) >= 14) & (torch.arange(n) < 16),
                test_mask=torch.arange(n) >= 16)
    graph_file = output / "graph.pkl"
    graph_file.write_bytes(pickle.dumps(data))
    dataset = {"kind": "dataset_split", "schema_version": 1,
               "dataset": {"name": "aagu015_cpu_fixture"},
               "preprocessing": {"adapter": "OpenGU_persisted_processed_pair"},
               "split": {"profile": "fixture_70_10_20", "train_ratio": 0.7,
                         "val_ratio": 0.1, "test_ratio": 0.2, "seed": 7}}
    manifest = {k: dataset[k] for k in ("dataset", "preprocessing", "split")}
    manifest.update(schema="opengu.persisted_dataset_split", version=1, data_path="graph.pkl",
                    data_sha256=sha256_file(graph_file), data_identity=data_identity(data))
    dump(output / "dataset.json", manifest)
    dataset["artifacts"] = {"manifest": "dataset.json", "manifest_sha256": sha256_file(output / "dataset.json"),
                            "split_hash": data_identity(data)["split_hash"], "node_id_space": "pyg-global-node-index-v1"}
    write_yaml("dataset.yaml", dataset)
    stage_source = yaml.safe_load((CONFIG / "stage_s.yaml").read_text(encoding="utf-8"))
    selector_files, methods = [], []
    model = {"architecture": "OpenGU.GCNNet", "hidden_channels": 4}
    training = {"epochs": 6, "seed": 42}
    for ref in stage_source["selector_refs"]:
        value = yaml.safe_load((CONFIG / ref).read_text(encoding="utf-8"))
        method = value["method"]
        effective = load_instance(CONFIG / ref, "selector")
        if uses_model(method):
            value.update(model=model, training=training)
        parameters = value.setdefault("parameters", {})
        if "lissa" in effective["parameters"]:
            parameters["lissa"] = {"iterations": 2}
        if "hutchinson" in effective["parameters"]:
            parameters["hutchinson"] = {"probes": 2}
        if method.startswith("tracin_cp_"):
            parameters["checkpoint_steps"] = [1, 2, 3, 4, 5, 6]
        name = method + ".yaml"
        write_yaml(name, value)
        selector_files.append(name)
        methods.append(method)

    base = {"kind": "experiment", "schema_version": 1, "experiment_id": "aagu015-smoke",
            "stage": "selector", "dataset_ref": "dataset.yaml",
            "selector_refs": selector_files, "matrix": "cartesian_product"}
    def run(name, **changes):
        plan = copy.deepcopy(base)
        plan.update(changes)
        plan["experiment_id"] = name
        path = write_yaml(name + ".yaml", plan)
        return execute(path, context=ExecutionContext(
            run_id=name, level="verification", request_device="cpu", store_root=output / "store",
            checkpoint_root=output / "checkpoints", runtime_root=output / "scratch" / name,
            output=output / (name + ".json"), executor="aagu015-selector-reuse-smoke"))

    def forbidden(*args, **kwargs):
        raise AssertionError("forbidden producer was called")

    actual_resolve = entry.resolve_methods
    def only_hits(**kwargs):
        return actual_resolve(**kwargs, fail_if_score_called=True, fail_if_selection_called=True)

    with patch.object(gu_entry, "run_unlearning", forbidden), patch.object(entry, "evaluate_modular", forbidden):
        cold = run("selector-cold")
        with patch.object(entry, "resolve_methods", only_hits):
            warm = run("selector-warm")
    assert not cold["unlearning"] and not cold["evaluations"]
    candidates = list(range(14))
    observations, rank_rows = [], []
    for method, first, second in zip(methods, cold["selectors"], warm["selectors"]):
        scores, ranking = first["scores"], first["ranking"]
        assert len(scores) == len(ranking) == 14 and all(math.isfinite(x) for x in scores)
        expected = sorted(candidates, key=lambda i: (-scores[i], i))
        assert ranking == expected
        assert second["scores"] == scores and second["ranking"] == ranking
        assert not first["score"]["hit"] and first["score"]["producer_called"]
        assert second["score"]["hit"] and not second["score"]["producer_called"]
        assert second["selection"]["cache"]["hit"] and not second["selection"]["cache"]["producer_called"]
        reference = {k: first["selection"]["artifact"][k] for k in ("artifact_id", "recipe_hash", "content_hash")}
        loaded = entry.verified_selection(reference, store_root=output / "store", data=data,
                    inputs=read_dataset(dataset, output)[1])
        k = first["selection"]["artifact_k"]
        assert list(loaded.selected_nodes) == ranking[:k]
        assert reference == {k: second["selection"]["artifact"][k] for k in reference}
        observations.append({"method": method, "candidate_count": 14, "k": k,
                             "score_cold_hit": first["score"]["hit"], "score_warm_hit": second["score"]["hit"],
                             "selection_warm_hit": second["selection"]["cache"]["hit"],
                             "warm_producer_called": False, "scores_and_ranking_equal": True,
                             "score_artifact_id": first["score"]["artifact_id"], "selection": reference})
        for rank, node in enumerate(ranking, 1):
            rank_rows.append({"selector": method, "node_id": node, "score": scores[node],
                              "rank": rank, "selected": rank <= k})
    with (output / "selector-score-rank.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rank_rows[0]))
        writer.writeheader()
        writer.writerows(rank_rows)

    by_name = dict(zip(methods, cold["selectors"]))
    pairs = []
    def add(question, left, right):
        pairs.append((question, left, right))
    for left, right in [("a_grad_norm", "b_param_hutch"), ("p_point", "r_point"),
                        ("p_simple", "gt_simple"), ("p_graph", "gt_full")]:
        add("Q1", left, right)
    for group in [("r_point", "gt_simple", "gt_full"), ("p_point", "p_simple", "p_graph")]:
        for left, right in itertools.combinations(group, 2):
            add("Q2", left, right)
    for left in ("a_grad_norm", "b_param_hutch"):
        for right in ("r_point", "gt_simple", "gt_full", "degree", "random", "legacy"):
            add("Q3", left, right)
    for source, reference in [("point", "r_point"), ("simple", "gt_simple"), ("graph", "gt_full")]:
        group = ("p_" + source, "tracin_cp_" + source + "_3", "tracin_cp_" + source + "_6")
        for left, right in itertools.combinations(group, 2):
            add("Q4", left, right)
        for left in group:
            add("Q4", left, reference)
    comparisons = []
    for question, left, right in pairs:
        a, b = by_name[left], by_name[right]
        metrics = pair_metrics(a["scores"], b["scores"], a["ranking"], b["ranking"], 1)
        comparisons.append({"question": question, "left": left, "right": right, **metrics})
    # Known vectors validate the meaning of the reused metric consumer.
    same = pair_metrics([1, 2, 3], [1, 2, 3], [2, 1, 0], [2, 1, 0], 1)
    reverse = pair_metrics([1, 2, 3], [3, 2, 1], [2, 1, 0], [0, 1, 2], 1)
    assert same["spearman"] == 1 and same["kendall"] == 1 and same["jaccard"] == 1
    assert reverse["spearman"] == -1 and reverse["kendall"] == -1 and reverse["jaccard"] == 0
    dump(output / "selector-comparisons.json", comparisons)

    reference = next(row["selection"] for row in observations if row["method"] == "p_point")
    write_yaml("gnndelete.yaml", {"kind": "unlearning", "schema_version": 1, "method": "GNNDelete",
               "model": model, "training": training, "parameters": {"unlearning_epochs": 2}})
    write_yaml("gif.yaml", {"kind": "unlearning", "schema_version": 1, "method": "GIF",
               "model": model, "training": training, "parameters": {"iteration": 2}})
    gu_config = {"stage": "unlearning", "selector_refs": [], "selection_input": reference,
                 "unlearning_refs": ["gnndelete.yaml", "gif.yaml"]}
    with patch.object(entry, "resolve_methods", forbidden):
        gu_cold = run("gu-cold-existing-selection", **gu_config)
        gu_warm = run("gu-warm-existing-selection", **gu_config)
        bad = {**reference, "content_hash": "0" * 64}
        try:
            run("gu-bad-reference", **{**gu_config, "selection_input": bad})
        except ValueError as error:
            assert "digest mismatch" in str(error)
        else:
            raise AssertionError("wrong Selection content hash was accepted")
    assert not (output / "gu-bad-reference.json").exists()
    assert not (output / "scratch/gu-bad-reference").exists()
    gu_observations = []
    for first, second in zip(gu_cold["unlearning"], gu_warm["unlearning"]):
        assert first["hit"] is False and second["hit"] is True
        assert second["producer_called"] is False
        assert first["artifact_id"] == second["artifact_id"]
        assert first["result"]["selected_nodes"] == second["result"]["selected_nodes"] == by_name["p_point"]["ranking"][:1]
        assert first["checkpoint"]["hit"] and second["checkpoint"]["hit"]
        gu_observations.append({"method": first["target"]["method"], "first_hit": first["hit"],
                                "second_hit": second["hit"], "warm_producer_called": second["producer_called"],
                                "selection_producer_called": False, "checkpoint_hit": first["checkpoint"]["hit"],
                                "same_gu_artifact": first["artifact_id"] == second["artifact_id"],
                                "artifact_id": first["artifact_id"], "selection": reference,
                                "result_values_equal_in_this_fixture": first["result"] == second["result"]})
    with patch.object(entry, "resolve_methods", only_hits):
        combined = run("future-plan-with-selector-ref", stage="unlearning",
                       selector_refs=["p_point.yaml"], unlearning_refs=["gnndelete.yaml", "gif.yaml"])
    assert combined["selectors"][0]["score"]["hit"]
    assert combined["selectors"][0]["selection"]["cache"]["hit"]
    assert all(row["hit"] for row in combined["unlearning"])
    assert combined["selector_producer_called"] is False

    assert yaml_before == {p.relative_to(CONFIG).as_posix(): sha256_file(p) for p in sorted(CONFIG.rglob("*.yaml"))}
    assert protected == {p: hashes(ROOT / p) for p in protected}
    receipt = {
        "verification": "PASS", "scope": "disposable CPU software proof, not research results",
        "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "fixture": {"nodes": 20, "train_val_test": [14, 2, 4], "classes": 2,
                    "graph_sha256": sha256_file(graph_file), "data_identity": data_identity(data)},
        "smoke_overrides": {"dataset": "aagu015_cpu_fixture", "fixture_seed": 7, "hidden_channels": 4,
                            "training_epochs": 6, "checkpoint_steps": [1, 2, 3, 4, 5, 6],
                            "lissa_iterations": 2, "hutchinson_probes": 2,
                            "gnndelete_epochs": 2, "gif_iterations": 2},
        "config_audit": {"yaml_count": len(yaml_before), "stage_s_plans": len(plans),
                         "cells": expansion["counts"], "stage_s_has_gu": False,
                         "stage_s_has_gu_evaluation": False, "candidate_pool": "train_mask",
                         "conditioned_target": "validation_mask", "official_yaml_unchanged": True,
                         "real_dataset_binding": "not changed; future execution preparation"},
        "selectors": observations, "score_rank_rows": len(rank_rows),
        "selector_metric_cases": len(comparisons), "metric_known_vectors": "PASS",
        "unlearning_reuse": gu_observations,
        "combined_future_plan": {"score_hit": True, "selection_hit": True,
                                 "gu_hits": 2, "selector_producer_called": False},
        "wrong_selection_hash_rejected_before_gu": True,
        "protected_trees_unchanged": True, "protected_files": sum(len(v or {}) for v in protected.values()),
        "limitations": ["No real Cora/CiteSeer/PubMed run", "No Retrain or retrain-gap evaluation",
                        "No full-matrix timing or scientific conclusion",
                        "GU metric cold/warm precision defect is outside this reuse proof"],
        "runtime_directory": str(output)}
    dump(output / "receipt.json", receipt)
    print(json.dumps({"verification": "PASS", "selector_count": len(observations),
                      "score_rank_rows": len(rank_rows), "metric_pairs": len(comparisons),
                      "gu_methods": [r["method"] for r in gu_observations],
                      "runtime": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
