"""Bounded AAGU-001 documentation/example checks; not a production config loader.

Runs only the existing sanity dry-run and read-only formal config parser.
No training, data preparation, cache producer, SSH or SyncMate dispatch.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
DOC = ROOT / "docs" / "experiment_contract"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def literal_default(path, flag):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr != "add_argument":
                continue
            if not any(isinstance(arg, ast.Constant) and arg.value == flag for arg in node.args):
                continue
            for keyword in node.keywords:
                if keyword.arg == "default":
                    return ast.literal_eval(keyword.value)
    raise ValueError("Default not found: " + flag)


def differences(left, right, prefix=""):
    if isinstance(left, dict) and isinstance(right, dict):
        result = []
        for key in sorted(set(left) | set(right)):
            path = prefix + "." + key if prefix else key
            result.extend(differences(left.get(key), right.get(key), path))
        return result
    return [] if left == right else [prefix]


def check_examples():
    examples = {path.name: read_yaml(path) for path in sorted((DOC / "examples").glob("*.yaml"))}
    require(len(examples) == 8, "Expected eight concrete documentation examples")
    for name, value in examples.items():
        require(value["schema_version"] == 1, name + ": example version")
        kind = value["kind"]
        require(kind in {"dataset_split", "selector", "unlearning", "experiment"}, name + ": kind")
        if kind == "experiment":
            require(value["execution_authorized"] is False, name + ": no execution authority")
            require(value["dataset_ref"] in examples, name + ": dataset reference")
            require(bool(value["research_question"]) and bool(value["evaluation"]), name + ": research contract")
            for key in ("selector_refs", "unlearning_refs"):
                for ref in value.get(key, []):
                    require(ref in examples, name + ": module reference " + ref)
        if kind == "selector":
            require("unlearn_lr" not in value.get("parameters", {}), name + ": GU leakage")
            budget = value["budget"]
            require(budget["mode"] == "ratio" and 0 < budget["value"] <= 1, name + ": ratio")
            require(budget["denominator"] == "train_candidate_count", name + ": denominator")
        if kind in {"selector", "unlearning"}:
            require("experiment_id" not in value and "case_id" not in value, name + ": experiment metadata leakage")
    require(differences(examples["selector_b_hutch32.yaml"], examples["selector_b_hutch64.yaml"]) == ["parameters.hutchinson.probes"], "Hutch variants must differ only by probes")
    require(differences(examples["unlearning_gnndelete.yaml"], examples["unlearning_gnndelete_lr002.yaml"]) == ["parameters.unlearn_lr"], "GU variants must differ only by lr")
    require("model" not in examples["selector_degree.yaml"], "Degree must not require a model")
    require("unlearning_refs" not in examples["experiment_selector_only.yaml"], "Selector-only must not require GU")
    require("selector_refs" not in examples["experiment_gu_from_selection.yaml"], "Existing Selection must not require selector config")
    require(examples["dataset_cora.yaml"]["artifacts"]["split_hash"] is None, "Do not invent formal asset hashes")
    return examples


def check_sources(examples):
    formal_path = ROOT / "experiments/configs/syncmate_target_direct_formal_v2.yaml"
    formal = read_yaml(formal_path)
    gcn = read_yaml(ROOT / "model/properties/GCN.yaml")
    selector = examples["selector_b_hutch32.yaml"]
    require(selector["training"]["lr"] == gcn["lr"] == 0.005, "GCN effective learning rate")
    require(selector["training"]["weight_decay"] == gcn["decay"] == 0.000001, "GCN effective decay")
    require(selector["training"]["epochs"] == formal["epochs"] == 100, "Training epochs")
    source = ROOT / "experiments/target_direct_v1/run_selection.py"
    observed = {}
    for flag, expected in {"--lissa-iterations": 20, "--lissa-scale": 25.0, "--lissa-damp": 0.01, "--hutch-probes": 32, "--hutch-seed": 1729, "--affected-hops": 2, "--parameter-scope": "last_layer"}.items():
        observed[flag] = literal_default(source, flag)
        require(observed[flag] == expected, "Current selector default drift: " + flag)
    gu = examples["unlearning_gnndelete.yaml"]["parameters"]
    parser_path = ROOT / "parameter_parser.py"
    for field in ("unlearn_lr", "unlearning_epochs", "alpha", "loss_fct", "loss_type"):
        observed[field] = literal_default(parser_path, "--" + field)
        require(observed[field] == gu[field], "Current GU default drift: " + field)
    require(formal["checkpoint_epochs"][0::3] == [1, 50], "Checkpoint source drift")
    require(formal["claims"]["candidate_full_matrix_authorized"] is False, "No full matrix authorization")
    return observed


def check_links():
    count = 0
    for path in (DOC / "README.md", DOC / "PARAMETERS.md"):
        for match in re.finditer(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            target = match.group(1).split("#", 1)[0]
            if not target or "://" in target:
                continue
            require((path.parent / target).resolve().exists(), "Broken link: " + str(path) + " -> " + target)
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True, help="Exact source candidate supplied by run_git finish")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    require(re.fullmatch(r"[0-9a-f]{40}", args.checkpoint) is not None, "Exact Git checkpoint required")
    output = args.output.resolve()
    allowed = (ROOT / ".workblock/runtime/evidence/AAGU-001").resolve()
    require(allowed in output.parents, "Evidence output must remain in this Block runtime directory")
    examples = check_examples()
    defaults = check_sources(examples)
    links = check_links()
    # Real project parser, read-only: no profile materialization or Cache Store.
    sys.path.insert(0, str(ROOT))
    from experiments.target_direct_v1.syncmate_stage import load_config
    from experiments.target_direct_v1.scoring import checkpoint_view_indices
    config = load_config()
    views = checkpoint_view_indices(len(config["checkpoint_epochs"]))
    require([config["checkpoint_epochs"][i] for i in views["cp3"]] == [1, 50, 100], "cp3 effective epochs")
    budgets = {name: {"candidate_count": value["expected_candidate_count"], "k": value["expected_k_by_ratio"]} for name, value in config["datasets"].items()}
    require(budgets["cora"]["candidate_count"] == 1895 and budgets["cora"]["k"] == {"0.01": 18, "0.05": 94}, "Cora derived budget")
    command = [sys.executable, "-B", "-X", "utf8", "experiments/run.py", "experiments/configs/sanity_one_cell.yaml", "--dry_run"]
    completed = subprocess.run(command, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    require(completed.returncode == 0, "Existing sanity dry-run failed: " + completed.stderr)
    require("total cells: 1" in completed.stdout and "would_run: 1" in completed.stdout, "Expected current one-cell dry-run observation")
    sources = [ROOT / "experiments/configs/sanity_one_cell.yaml", ROOT / "experiments/configs/syncmate_target_direct_formal_v2.yaml", ROOT / "experiments/target_direct_v1/run_selection.py", ROOT / "parameter_parser.py", ROOT / "model/properties/GCN.yaml"]
    result = {"schema": "aagu001.contract_verification.v1", "checkpoint": args.checkpoint, "observed_at": datetime.now(timezone.utc).isoformat(), "status": "PASS", "example_count": len(examples), "resolved_doc_links": links, "source_defaults": defaults, "planned_budgets_not_asset_observations": budgets, "cp3_epochs": [1, 50, 100], "sanity_dry_run": {"argv": command, "exit_code": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}, "source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}, "boundaries": {"formal_gpu_run": "NOT OBSERVED", "formal_asset_hashes": "NOT OBSERVED", "cache_identity_fix": "NOT IMPLEMENTED - AAGU-026", "human_acceptance": "NOT CONFIRMED"}}
    require(not output.exists(), "Evidence path already exists; use a new observation file")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
