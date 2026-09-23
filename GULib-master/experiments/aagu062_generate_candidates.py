"""Generate one Observer calibration table from a theory-analysis result."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path, root):
    path = Path(path).resolve()
    try:
        return path.relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError("generated configuration path escapes project root") from exc


def _load_inputs(theory_config, theory_json, root):
    import yaml

    config_path = Path(theory_config).resolve()
    result_path = Path(theory_json).resolve()
    config_bytes = config_path.read_bytes()
    config = yaml.safe_load(config_bytes.decode("utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    config_hash, result_hash = hashlib.sha256(config_bytes).hexdigest(), sha256(result_path)
    if result.get("schema") != "aagu062.theory-analysis.v1" or result.get("status") != "candidate_proposal":
        raise ValueError("theory result is not a complete AAGU-062 candidate proposal")
    if result.get("execution", {}).get("theory_config_sha256") != config_hash:
        raise ValueError("theory result was produced from a different theory YAML")
    condition = {"dataset": config["condition"]["dataset"],
                 "hidden_channels": config["condition"]["hidden_channels"]}
    if result.get("condition") != condition:
        raise ValueError("theory result condition differs from its input YAML")
    if result.get("model") != config["model"] or result.get("training") != config["training"]:
        raise ValueError("theory result model or training identity differs from its input YAML")
    checkpoint = (config_path.parent / config["checkpoint"]).resolve()
    try:
        checkpoint_relative = checkpoint.relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError("checkpoint reference escapes project root") from exc
    if not result.get("checkpoint", {}).get("path", "").replace("\\", "/").endswith(checkpoint_relative):
        raise ValueError("theory result checkpoint path differs from its input YAML")
    if not result.get("checkpoint", {}).get("file_sha256") or not result.get("checkpoint", {}).get("state_hash"):
        raise ValueError("theory result is missing checkpoint identity")
    methods = result.get("methods")
    if not isinstance(methods, list) or [row.get("method") for row in methods] != ["GIF", "IDEA"]:
        raise ValueError("theory result must contain GIF and IDEA analyses")
    for method in methods:
        candidates = method.get("candidate_design", {}).get("proposed_candidates", [])
        if [candidate.get("candidate_id") for candidate in candidates] != ["target_rho_0p8", "target_rho_0p5"]:
            raise ValueError("theory result does not contain both registered spectral-radius candidates")
        for candidate in candidates:
            if candidate.get("iteration_values") != [100, 200, 400]:
                raise ValueError("candidate iteration values differ from the registered calibration budgets")
            for key in ("scale", "damp", "mu", "target_spectral_radius"):
                if not isinstance(candidate.get(key), (int, float)) or not math.isfinite(candidate[key]):
                    raise ValueError("candidate has missing or non-finite " + key)
            if type(candidate["scale"]) is not int or candidate["scale"] <= 0 or not 0 <= candidate["damp"] < 1:
                raise ValueError("derived scale/damp is outside the solver parameter domain")
    return config, result, config_hash, result_hash, checkpoint_relative


def _yaml_bytes(value, comments):
    import yaml
    body = yaml.safe_dump(value, sort_keys=False, allow_unicode=True, default_flow_style=False)
    return ("\n".join("# " + comment for comment in comments) + "\n" + body).encode("utf-8")


def generate(theory_config, theory_json, table_path, project_root, replace_table=False):
    import yaml

    root = Path(project_root).resolve()
    config, result, config_hash, result_hash, checkpoint_relative = _load_inputs(
        theory_config, theory_json, root)
    table_path = Path(table_path)
    if not table_path.is_absolute():
        table_path = root / table_path
    table_path = table_path.resolve()
    try:
        table_parent_relative = table_path.parent.relative_to(root)
    except ValueError as exc:
        raise ValueError("table output escapes project root") from exc
    table_parent = root / table_parent_relative
    dataset_path = (Path(theory_config).resolve().parent / config["dataset_ref"]).resolve()
    public_datasets = (root / "experiments/configs/datasets").resolve()
    dataset_reference = (dataset_path.name if dataset_path.parent == public_datasets
                         else Path(os.path.relpath(dataset_path, table_path.parent)).as_posix())
    checkpoint_path = root / checkpoint_relative
    checkpoint_ref = Path(os.path.relpath(checkpoint_path, table_path.parent)).as_posix()

    case = config["condition"]
    hidden = case["hidden_channels"]
    pending_files = []
    refs = []
    generated_paths = []
    for method_result in result["methods"]:
        method = method_result["method"]
        for candidate in method_result["candidate_design"]["proposed_candidates"]:
            rho_label = candidate["candidate_id"].replace("target_", "")
            for iteration in candidate["iteration_values"]:
                filename = f"{method.lower()}_h{hidden}_theory_{rho_label}_{iteration}.yaml"
                path = table_path.parent / filename
                if path.exists():
                    raise FileExistsError("refusing to overwrite generated/unowned YAML: " + str(path))
                parameters = {"iteration": iteration, "scale": candidate["scale"], "damp": candidate["damp"]}
                if method == "GIF":
                    parameters["GIF_method"] = "GIF"
                else:
                    parameters.update(gaussian_mean=0.0, gaussian_std=0.0)
                instance = {
                    "kind": "unlearning", "schema_version": 1, "method": method,
                    "model": config["model"], "training": config["training"],
                    "checkpoint": checkpoint_ref, "parameters": parameters,
                }
                content = _yaml_bytes(instance, [
                    "Generated from AAGU-062 theory analysis.",
                    "Theory JSON SHA-256: " + result_hash,
                    "Theory YAML SHA-256: " + config_hash,
                    f"Candidate {candidate['candidate_id']} for {case['dataset']} H{hidden}; Observer validation required.",
                ])
                pending_files.append((path, content))
                refs.append("./" + filename)
                generated_paths.append(relative(path, root))

    experiment_id = f"aagu{Path(table_path.parent).name[-3:]}-{case['dataset'].lower()}-h{hidden}-theory-candidates-v1"
    table = {
        "kind": "experiment", "schema_version": 1, "experiment_id": experiment_id,
        "stage": "unlearning", "dataset_refs": [dataset_reference],
        "selector_refs": ["random.yaml"], "unlearning_refs": refs,
        "matrix": "cartesian_product", "random_selector_seeds": [104245],
        "budget_ratios": [0.1], "return_scores": False,
        "execution": {"gu_cache": {"GIF": "disabled", "IDEA": "disabled"}},
        "observers": [
            {"name": "linear_solver_trace", "methods": ["GIF", "IDEA"]},
            {"name": "same_graph_change", "methods": ["GIF", "IDEA"]},
            {"name": "hessian_calibration", "methods": ["GIF", "IDEA"]},
        ],
    }
    table_bytes = _yaml_bytes(table, [
        "Generated only after the matching checkpoint theory calculation.",
        "Theory JSON SHA-256: " + result_hash,
        f"Case: {case['dataset']} H{hidden}; proposed parameters are not stability decisions.",
    ])
    if table_path.exists() and not replace_table:
        raise FileExistsError("table already exists; use --replace-table only for the registered draft: " + str(table_path))
    if table_path.exists() and replace_table:
        old = yaml.safe_load(table_path.read_text(encoding="utf-8"))
        if not isinstance(old, dict) or old.get("kind") != "experiment" or not old.get("experiment_id", "").startswith("aagu065-"):
            raise ValueError("--replace-table only permits replacing the registered AAGU-065 draft table")
    for path, content in pending_files:
        path.write_bytes(content)
    table_path.write_bytes(table_bytes)
    return {"table": relative(table_path, root), "experiment_id": experiment_id,
            "theory_json_sha256": result_hash, "theory_config_sha256": config_hash,
            "generated_unlearning_yamls": generated_paths, "logical_cells": len(refs)}


def main(argv=None):
    global ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--theory-config", type=Path, required=True)
    parser.add_argument("--theory-json", type=Path, required=True)
    parser.add_argument("--table-path", type=Path, required=True)
    parser.add_argument("--replace-table", action="store_true")
    args = parser.parse_args(argv)
    ROOT = args.project_root.resolve()
    sys.path.insert(0, str(ROOT))
    result = generate(args.theory_config, args.theory_json, args.table_path, ROOT, args.replace_table)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
