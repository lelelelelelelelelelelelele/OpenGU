"""Read verified Observer runs and report per-checkpoint candidate stability.

This post-run analyzer never executes an experiment or edits its configuration.
Each input is a completed run.json, its trusted SHA-256 receipt, and the exact
theory proposal JSON used to create that run's candidate table.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import posixpath
import re
import subprocess
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
DATASETS = ("Cora", "CiteSeer", "PubMed")
HIDDEN_WIDTHS = (16, 64)
METHODS = ("GIF", "IDEA")
ITERATIONS = (100, 200, 400)
OBSERVER_VERSIONS = {
    "linear_solver_trace": "linear-solver-trace-v1",
    "same_graph_change": "same-graph-change-v1",
    "hessian_calibration": "hessian-calibration-v1",
}
LIMITS = {
    "hvp_relative_error": 1e-5,
    "shifted_relative_residual": 1e-3,
    "relative_update_norm_variation": 1e-3,
    "update_to_rhs_ratio_min_exclusive": 1e-6,
    "original_graph_logits_max_abs_min_exclusive": 1e-8,
}
CANDIDATE_RE = re.compile(r"^(gif|idea)_h(16|64)_theory_rho_(0p8|0p5)_(100|200|400)\.yaml$")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def numeric(value, label):
    if type(value) not in (float, int) or not math.isfinite(value):
        raise ValueError(label + " must be a finite number")
    return float(value)


def safe_relative(value: str, label: str) -> str:
    if (not isinstance(value, str) or not value or "\\" in value or ":" in value
            or PurePosixPath(value).is_absolute() or ".." in PurePosixPath(value).parts):
        raise ValueError(label + " must be a safe project-relative POSIX path")
    return str(PurePosixPath(value))


def resolve_project_ref(base_directory: str, value: str, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value or PurePosixPath(value).is_absolute():
        raise ValueError(label + " must be a relative POSIX path")
    resolved = posixpath.normpath(posixpath.join(base_directory, value))
    if resolved == ".." or resolved.startswith("../"):
        raise ValueError(label + " escapes the project root")
    return resolved


def artifact_path(run_path: Path, cell_path: str, name: str) -> Path:
    cell_path = safe_relative(cell_path, "cell path")
    name = safe_relative(name, "artifact path")
    base = (run_path.parent / cell_path).resolve()
    target = (base / Path(*PurePosixPath(name).parts)).resolve()
    target.relative_to(base)
    return target


def read_git_yaml(root: Path, commit: str, path: str, label: str):
    import yaml

    path = safe_relative(path, label)
    prefix = subprocess.run(
        ["git", "rev-parse", "--show-prefix"], cwd=root, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    ).stdout.strip()
    git_path = posixpath.join(prefix, path) if prefix else path
    try:
        raw = subprocess.run(
            ["git", "show", f"{commit}:{git_path}"], cwd=root, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout
    except subprocess.CalledProcessError as exc:
        raise ValueError(f"{label} is absent from run commit {commit}: {path}") from exc
    value = yaml.safe_load(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(label + " must contain a YAML mapping")
    return value, raw


def load_theory(path: Path):
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema") != "aagu062.theory-analysis.v1" or value.get("status") != "candidate_proposal":
        raise ValueError("theory JSON is not a completed AAGU-062 proposal: " + str(path))
    condition = value.get("condition", {})
    if condition.get("dataset") not in DATASETS or condition.get("hidden_channels") not in HIDDEN_WIDTHS:
        raise ValueError("theory JSON identifies an unregistered case")
    checkpoint = value.get("checkpoint", {})
    if not checkpoint.get("state_hash") or not checkpoint.get("file_sha256"):
        raise ValueError("theory JSON lacks the exact checkpoint identity")
    methods = {row.get("method"): row for row in value.get("methods", [])}
    if set(methods) != set(METHODS):
        raise ValueError("theory JSON must contain GIF and IDEA")
    for method in METHODS:
        candidates = methods[method].get("candidate_design", {}).get("proposed_candidates", [])
        if [row.get("candidate_id") for row in candidates] != ["target_rho_0p8", "target_rho_0p5"]:
            raise ValueError("theory JSON candidate set differs from the registered proposal policy")
        for candidate in candidates:
            if candidate.get("iteration_values") != list(ITERATIONS):
                raise ValueError("theory proposal does not cover T=100/200/400")
            if type(candidate.get("scale")) is not int or candidate["scale"] <= 0:
                raise ValueError("theory proposal scale must be a positive integer for the solver config schema")
            numeric(candidate.get("scale"), "theory scale")
            numeric(candidate.get("damp"), "theory damp")
            numeric(candidate.get("mu"), "theory mu")
    return value, methods, sha256_bytes(path.read_bytes())


def load_verified_run(run_path: Path, expected_sha256: str):
    run_path = run_path.resolve()
    if sha256_bytes(run_path.read_bytes()) != expected_sha256:
        raise ValueError("run.json SHA-256 does not match the supplied trusted receipt")
    run = json.loads(run_path.read_text(encoding="utf-8"))
    if run.get("status") != "completed" or run.get("stage") != "unlearning":
        raise ValueError("after-exp requires a completed unlearning run")
    commit = run.get("commit")
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("run has no full source commit identity")
    cells = run.get("cells")
    if not isinstance(cells, list) or not cells:
        raise ValueError("completed run has no cells")
    observations = {}
    seen = set()
    for cell in cells:
        cell_id = cell.get("cell_id")
        if not cell_id or cell_id in seen or cell.get("status") != "completed":
            raise ValueError("run contains a duplicate or incomplete cell")
        seen.add(cell_id)
        refs = {entry.get("name"): entry for entry in cell.get("observers", [])}
        if set(refs) != set(OBSERVER_VERSIONS):
            raise ValueError("each calibration cell must contain all three registered Observers")
        folder = cell.get("path")
        if not isinstance(folder, str):
            raise ValueError("cell has no relative artifact folder")
        documents = {}
        for name, version in OBSERVER_VERSIONS.items():
            reference = refs[name]
            if reference.get("status") != "completed" or reference.get("semantic_version") != version:
                raise ValueError("Observer is incomplete or uses an unknown semantic version: " + name)
            identity = reference.get("identity", {})
            if (identity.get("cell_id") != cell_id or identity.get("conditions") != cell.get("conditions")
                    or identity.get("run_id") != run.get("run_id")
                    or identity.get("experiment_id") != run.get("experiment_id")
                    or identity.get("commit") != commit):
                raise ValueError("Observer provenance does not match its run cell")
            for relpath, declaration in reference.get("files", {}).items():
                if relpath not in cell.get("files", {}) or cell["files"][relpath] != declaration:
                    raise ValueError("Observer file hash is not bound by run.json")
                target = artifact_path(run_path, folder, relpath)
                raw = target.read_bytes()
                if sha256_bytes(raw) != declaration.get("sha256"):
                    raise ValueError("Observer artifact SHA-256 mismatch: " + relpath)
                if name == "linear_solver_trace" and relpath.endswith("/trace.jsonl"):
                    documents[(cell_id, name, "trace")] = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line]
                else:
                    documents[(cell_id, name, "result")] = json.loads(raw.decode("utf-8"))
            for key in ("output_identity",):
                if key not in identity:
                    raise ValueError("Observer identity lacks output identity")
            target = identity["output_identity"].get("target", {})
            if not target.get("checkpoint_state_hash"):
                raise ValueError("Observer output identity lacks checkpoint state hash")
            observations[cell_id] = {
                "cell": cell,
                "observer_refs": refs,
                "documents": documents,
                "checkpoint_state_hash": target["checkpoint_state_hash"],
                "output_target": target,
            }
    return run_path, run, observations


def load_run_configuration(root: Path, run: dict, expected_theory_sha: str):
    import yaml

    table_path = safe_relative(run.get("config_path"), "run config path")
    table, raw = read_git_yaml(root, run["commit"], table_path, "experiment table")
    if table.get("experiment_id") != run.get("experiment_id"):
        raise ValueError("run experiment_id differs from its committed table")
    if f"Theory JSON SHA-256: {expected_theory_sha}" not in raw.decode("utf-8"):
        raise ValueError("run table was not generated from the supplied theory JSON")
    table_dir = posixpath.dirname(table_path)
    dataset_refs = table.get("dataset_refs", [])
    if len(dataset_refs) != 1:
        raise ValueError("calibration table must bind exactly one dataset")
    dataset_path = resolve_project_ref(table_dir, dataset_refs[0], "dataset ref")
    dataset, _ = read_git_yaml(root, run["commit"], dataset_path, "dataset config")
    dataset_name = dataset.get("dataset", {}).get("name")
    unlearning_refs = table.get("unlearning_refs", [])
    if len(unlearning_refs) != len(METHODS) * 2 * len(ITERATIONS):
        raise ValueError("calibration table must contain exactly two theoretical candidates per method")
    instances = {}
    for reference in unlearning_refs:
        path = resolve_project_ref(table_dir, reference, "unlearning ref")
        instance, raw_instance = read_git_yaml(root, run["commit"], path, "unlearning config")
        match = CANDIDATE_RE.fullmatch(posixpath.basename(path))
        if not match:
            raise ValueError("unlearning config filename is not a theory-generated candidate: " + path)
        method = match.group(1).upper()
        hidden = int(match.group(2))
        rho = match.group(3).replace("p", ".")
        iteration = int(match.group(4))
        candidate_id = "target_rho_" + match.group(3)
        params = instance.get("parameters", {})
        if (instance.get("kind") != "unlearning" or instance.get("method") != method
                or instance.get("model", {}).get("hidden_channels") != hidden
                or params.get("iteration") != iteration):
            raise ValueError("method YAML identity disagrees with its filename: " + path)
        if f"Theory JSON SHA-256: {expected_theory_sha}" not in raw_instance.decode("utf-8"):
            raise ValueError("method YAML is not bound to the supplied theory JSON: " + path)
        if not any(line.startswith("# Theory YAML SHA-256: ") for line in raw_instance.decode("utf-8").splitlines()):
            raise ValueError("method YAML lacks theory input provenance")
        key = (method, candidate_id, iteration)
        if key in instances:
            raise ValueError("duplicate theoretical parameter cell")
        instances[key] = {"instance": instance, "path": path, "rho": float(rho)}
    if len(instances) != len(METHODS) * 2 * len(ITERATIONS):
        raise ValueError("calibration table does not cover all method/candidate/budget cells")
    return table_path, table, dataset_name, instances


def observer_document(entry, observer, kind):
    document = entry["documents"].get((entry["cell"]["cell_id"], observer, kind))
    if document is None:
        raise ValueError(f"cell {entry['cell']['cell_id']} is missing {observer} {kind}")
    return document


def evaluate_candidate(entries, theoretical, method, candidate_id):
    failures, missing = [], []
    by_iteration = {}
    theoretical_candidate = next(row for row in theoretical["candidate_design"]["proposed_candidates"]
                                if row["candidate_id"] == candidate_id)
    expected_scale = numeric(theoretical_candidate.get("scale"), "candidate scale")
    expected_damp = numeric(theoretical_candidate.get("damp"), "candidate damp")
    for entry in entries:
        cell = entry["cell"]
        output_target = entry["output_target"]
        expected_parameters = entry["candidate_config"]["parameters"]
        expected_iteration = expected_parameters["iteration"]
        target_params = output_target.get("parameters", {})
        if output_target.get("method") != method or target_params.get("iteration") != expected_iteration:
            failures.append("output identity method/iteration differs from configuration")
        if target_params.get("scale") is None or not math.isclose(float(target_params["scale"]), expected_scale, rel_tol=1e-12, abs_tol=1e-12):
            failures.append("output identity scale differs from the theory proposal")
        if target_params.get("damp") is None or not math.isclose(float(target_params["damp"]), expected_damp, rel_tol=1e-12, abs_tol=1e-12):
            failures.append("output identity damp differs from the theory proposal")
        calibration = observer_document(entry, "hessian_calibration", "result")
        if calibration.get("status") != "completed" or calibration.get("identity") != entry["observer_refs"]["hessian_calibration"]["identity"]:
            failures.append("Hessian Observer metadata is incomplete or has conflicting identity")
        measurements = calibration.get("measurements", {})
        hvp = measurements.get("hvp", {})
        if hvp.get("finite") is not True:
            failures.append("HVP check is not finite")
        for key in ("probe_relative_error", "rhs_relative_error", "repeat_relative_error"):
            value = hvp.get(key)
            if value is None or not math.isfinite(float(value)) or float(value) > LIMITS["hvp_relative_error"]:
                failures.append(f"HVP {key} is missing or exceeds 1e-5")
        system = measurements.get("system", {})
        if (system.get("iterations") != expected_iteration
                or system.get("scale") is None or not math.isclose(float(system["scale"]), expected_scale, rel_tol=1e-12, abs_tol=1e-12)
                or system.get("damp") is None or not math.isclose(float(system["damp"]), expected_damp, rel_tol=1e-12, abs_tol=1e-12)):
            failures.append("Hessian Observer system parameters differ from the theory proposal")
        trace_result = observer_document(entry, "linear_solver_trace", "result")
        trace = observer_document(entry, "linear_solver_trace", "trace")
        if trace_result.get("status") != "completed" or trace_result.get("identity") != entry["observer_refs"]["linear_solver_trace"]["identity"]:
            failures.append("solver-trace Observer metadata is incomplete or has conflicting identity")
        if not isinstance(trace, list):
            failures.append("solver trace is not a row list")
            trace = []
        row_by_step = {row.get("step"): row for row in trace if isinstance(row, dict)}
        budget_row = row_by_step.get(expected_iteration)
        if budget_row is None:
            missing.append(f"solver trace lacks T={expected_iteration}")
        else:
            if budget_row.get("finite") is not True:
                failures.append(f"T={expected_iteration} update is not finite")
            sr = budget_row.get("shifted_relative_residual")
            if sr is None or not math.isfinite(float(sr)) or float(sr) > LIMITS["shifted_relative_residual"]:
                failures.append(f"T={expected_iteration} shifted residual exceeds 1e-3")
            if (budget_row.get("scale") is None or not math.isclose(float(budget_row["scale"]), expected_scale, rel_tol=1e-12, abs_tol=1e-12)
                    or budget_row.get("damp") is None or not math.isclose(float(budget_row["damp"]), expected_damp, rel_tol=1e-12, abs_tol=1e-12)):
                failures.append("solver trace parameters differ from the theory proposal")
            if expected_iteration == 100:
                rhs = budget_row.get("rhs_l2")
                delta = budget_row.get("update_l2")
                if rhs is None or delta is None or not math.isfinite(float(rhs)) or float(rhs) <= 0:
                    failures.append("T=100 right-hand side is zero or invalid")
                elif float(delta) / float(rhs) <= LIMITS["update_to_rhs_ratio_min_exclusive"]:
                    failures.append("T=100 update-to-rhs ratio is at or below 1e-6")
        same_graph = observer_document(entry, "same_graph_change", "result")
        if same_graph.get("status") != "completed" or same_graph.get("identity") != entry["observer_refs"]["same_graph_change"]["identity"]:
            failures.append("same-graph Observer metadata is incomplete or has conflicting identity")
        original = same_graph.get("measurements", {}).get("graphs", {}).get("original", {})
        logits = original.get("logits_delta_max_abs")
        if (expected_iteration == 100 and
                (logits is None or not math.isfinite(float(logits))
                 or float(logits) <= LIMITS["original_graph_logits_max_abs_min_exclusive"])):
            failures.append("original-graph logits max-abs change is at or below 1e-8")
        by_iteration[expected_iteration] = {
            "shifted_relative_residual": budget_row.get("shifted_relative_residual") if budget_row else None,
            "original_relative_residual": budget_row.get("original_relative_residual") if budget_row else None,
            "update_l2": budget_row.get("update_l2") if budget_row else None,
            "rhs_l2": budget_row.get("rhs_l2") if budget_row else None,
            "same_graph_logits_max_abs": logits,
            "hvp_errors": {key: hvp.get(key) for key in ("probe_relative_error", "rhs_relative_error", "repeat_relative_error")},
        }
    norms = {step: (row.get("update_l2"), row.get("rhs_l2")) for step, row in by_iteration.items()}
    if set(norms) != set(ITERATIONS):
        missing.extend(f"candidate lacks T={step}" for step in ITERATIONS if step not in norms)
    else:
        norm100 = norms[100][0]
        if norm100 is None or not math.isfinite(float(norm100)) or float(norm100) <= 0:
            failures.append("T=100 update norm is zero or invalid")
        else:
            for step in (200, 400):
                value = norms[step][0]
                if value is None or not math.isfinite(float(value)):
                    failures.append(f"T={step} update norm is invalid")
                elif abs(float(value) - float(norm100)) / float(norm100) > LIMITS["relative_update_norm_variation"]:
                    failures.append(f"T={step} update norm variation exceeds 1e-3")
    status = "unstable" if failures else "inconclusive" if missing else "stable"
    return {
        "candidate_id": candidate_id,
        "scale": expected_scale,
        "damp": expected_damp,
        "mu": theoretical_candidate["mu"],
        "status": status,
        "failures": sorted(set(failures)),
        "missing": sorted(set(missing)),
        "budgets": {str(step): by_iteration.get(step) for step in ITERATIONS},
    }


def analyze_case(root: Path, run_path: Path, expected_sha256: str, theory_path: Path):
    theory, theory_methods, theory_sha = load_theory(theory_path)
    run_path, run, observations = load_verified_run(run_path, expected_sha256)
    table_path, table, dataset_name, instances = load_run_configuration(root, run, theory_sha)
    condition = theory["condition"]
    dataset, hidden = condition["dataset"], condition["hidden_channels"]
    if dataset_name != dataset:
        raise ValueError("run dataset differs from theory case")
    dataset_config, _ = read_git_yaml(root, run["commit"],
        resolve_project_ref(posixpath.dirname(table_path), table.get("dataset_refs", [])[0], "dataset ref"),
        "dataset config")
    if dataset_config.get("artifacts", {}).get("manifest_sha256") != theory.get("dataset_split", {}).get("manifest_sha256"):
        raise ValueError("run dataset manifest differs from the theory analysis")
    groups = {(method, candidate_id): [] for method in METHODS
              for candidate_id in ("target_rho_0p8", "target_rho_0p5")}
    selection_ids = set()
    for entry in observations.values():
        cell = entry["cell"]
        conditions = cell.get("conditions", {})
        ref = conditions.get("unlearning_ref")
        table_dir = posixpath.dirname(table_path)
        normalized_ref = resolve_project_ref(table_dir, ref, "cell unlearning ref")
        instance = next((value for value in instances.values() if value["path"] == normalized_ref), None)
        if instance is None:
            raise ValueError("run cell references an undeclared candidate config")
        config = instance["instance"]
        method = config["method"]
        width = config["model"]["hidden_channels"]
        if (width != hidden or conditions.get("dataset_name") != dataset
                or conditions.get("random_selector_seed") != 104245
                or not math.isclose(float(conditions.get("budget_ratio", -1)), 0.1, rel_tol=0, abs_tol=1e-12)
                or conditions.get("seed") != 42):
            raise ValueError("run cell condition differs from the registered one-point calibration")
        if config.get("training") != theory.get("training") or config.get("model") != theory.get("model"):
            raise ValueError("candidate training/model identity differs from the theory checkpoint")
        checkpoint_path = resolve_project_ref(posixpath.dirname(instance["path"]), config.get("checkpoint"), "checkpoint ref")
        theory_checkpoint_path = theory["checkpoint"].get("path", "").replace("\\", "/")
        if not theory_checkpoint_path.endswith("/" + checkpoint_path):
            raise ValueError("candidate checkpoint path differs from its theory analysis")
        target_state = entry["checkpoint_state_hash"]
        if target_state != theory["checkpoint"]["state_hash"]:
            raise ValueError("Observer used a checkpoint state different from the theory analysis")
        dataset_input = entry["observer_refs"]["hessian_calibration"]["identity"]["output_identity"].get("dataset_input", {})
        dataset_instance = dataset_input.get("instance", {})
        if (dataset_instance.get("dataset", {}).get("name") != dataset
                or dataset_instance.get("artifacts", {}).get("manifest_sha256")
                != theory.get("dataset_split", {}).get("manifest_sha256")
                or dataset_instance.get("artifacts", {}).get("split_hash")
                != theory.get("dataset_split", {}).get("identity", {}).get("split_hash")):
            raise ValueError("Observer used a Dataset/Split different from the theory analysis")
        target_params = entry["output_target"].get("parameters", {})
        if (entry["output_target"].get("method") != method
                or target_params.get("iteration") != config["parameters"].get("iteration")
                or not math.isclose(float(target_params.get("scale", -1)), float(config["parameters"]["scale"]), rel_tol=1e-12, abs_tol=1e-12)
                or not math.isclose(float(target_params.get("damp", -1)), float(config["parameters"]["damp"]), rel_tol=1e-12, abs_tol=1e-12)):
            raise ValueError("actual Output identity parameters differ from its committed candidate YAML")
        theo = next(row for row in theory_methods[method]["candidate_design"]["proposed_candidates"]
                    if row["candidate_id"] == next(key[1] for key, value in instances.items() if value is instance))
        if (not math.isclose(float(config["parameters"]["scale"]), float(theo["scale"]), rel_tol=1e-12, abs_tol=1e-12)
                or not math.isclose(float(config["parameters"]["damp"]), float(theo["damp"]), rel_tol=1e-12, abs_tol=1e-12)):
            raise ValueError("candidate YAML parameters differ from their theory result")
        selection_ids.add(cell.get("selection_id"))
        candidate_id = next(key[1] for key, value in instances.items() if value is instance)
        entry["candidate_config"] = config
        groups[(method, candidate_id)].append(entry)
    if len(selection_ids) != 1 or None in selection_ids:
        raise ValueError("all calibration candidates must share the same verified Random selection")
    method_results = {}
    for method in METHODS:
        candidate_results = []
        all_complete = True
        for candidate_id in ("target_rho_0p8", "target_rho_0p5"):
            entries = groups[(method, candidate_id)]
            if sorted(entry["output_target"]["parameters"].get("iteration") for entry in entries) != list(ITERATIONS):
                all_complete = False
            if instances.get((method, candidate_id, 100)) is None:
                raise ValueError("missing theory-generated T=100 parameter instance")
            theoretical = theory_methods[method]
            candidate_results.append(evaluate_candidate(entries, theoretical, method, candidate_id))
        passing = [row for row in candidate_results if row["status"] == "stable"]
        complete = all_complete and all(row["status"] != "inconclusive" for row in candidate_results)
        frozen = min(passing, key=lambda row: row["mu"]) if complete and passing else None
        if frozen:
            status = "stable"
        elif complete:
            status = "unstable"
        else:
            status = "inconclusive"
        method_results[method] = {"status": status, "candidates": candidate_results,
            "frozen_candidate": frozen["candidate_id"] if frozen else None,
            "frozen_parameters": ({key: frozen[key] for key in ("scale", "damp", "mu")} if frozen else None),
            "selection_id": next(iter(selection_ids))}
    return {
        "dataset": dataset,
        "hidden_channels": hidden,
        "status": "stable" if all(result["status"] == "stable" for result in method_results.values())
                  else "unstable" if any(result["status"] == "unstable" for result in method_results.values())
                  else "inconclusive",
        "run": {"path": str(run_path), "run_id": run["run_id"], "experiment_id": run["experiment_id"],
                "commit": run["commit"], "sha256": expected_sha256, "config_path": table_path,
                "theory_json_sha256": theory_sha},
        "checkpoint": theory["checkpoint"],
        "methods": method_results,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--input", nargs=3, action="append", metavar=("RUN_JSON", "RUN_SHA256", "THEORY_JSON"),
                        help="repeat per completed dataset/hidden calibration run")
    parser.add_argument("--output", type=Path, help="write JSON summary here; otherwise print to stdout")
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    rows = {}
    for run_json, run_sha256, theory_json in args.input or []:
        row = analyze_case(root, Path(run_json), run_sha256, Path(theory_json))
        key = (row["dataset"], row["hidden_channels"])
        if key in rows:
            raise ValueError("multiple calibration runs supplied for one dataset/hidden case")
        rows[key] = row
    cases = []
    for dataset in DATASETS:
        for hidden in HIDDEN_WIDTHS:
            key = (dataset, hidden)
            cases.append(rows.get(key, {
                "dataset": dataset, "hidden_channels": hidden, "status": "inconclusive",
                "reason": "no checksum-verified Observer run supplied",
                "methods": {method: {"status": "inconclusive", "frozen_candidate": None,
                                     "frozen_parameters": None, "candidates": []} for method in METHODS},
            }))
    summary = {
        "schema": "aagu062.after-exp-analysis.v1",
        "status": "complete" if all(row["status"] == "stable" for row in cases) else "pending_or_failed",
        "criteria_source": "AAGU-065 Work Plan pre_run_gate, applied unchanged to all six dataset/hidden conditions",
        "criteria": LIMITS,
        "uses_f1_for_parameter_selection": False,
        "candidate_freeze_rule": "choose the smallest mu among passing theoretical proposals only when all registered proposals and T=100/200/400 cells are complete; otherwise no freeze",
        "cases": cases,
        "interpretation": "This read-only after-exp report does not modify YAML or authorize downstream multi-selector/seed runs. A stable result is a one-point calibration decision, not a claim that all selectors are stable.",
    }
    encoded = json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        destination = args.output.resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("x", encoding="utf-8") as handle:
            handle.write(encoded)
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
