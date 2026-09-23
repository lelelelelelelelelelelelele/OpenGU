"""Derive per-checkpoint GIF/IDEA candidates before Observer calibration.

The finite Lanczos Ritz range is used as an estimate, not a full-spectrum
certificate. Generated values are proposals; the registered Observer run owns
the stability decision.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
TARGET_RADII = (0.8, 0.5)
ITERATIONS = (100, 200, 400)
LANCZOS_SEEDS = (173, 941)
LANCZOS_STEPS = 80
CONFIG_FIELDS = {"kind", "schema_version", "condition", "dataset_ref", "model", "training", "checkpoint", "methods"}


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _norm(value):
    import torch
    return float(torch.linalg.vector_norm(value.detach().double()))


def _lanczos(matvec, size, device, seed):
    import torch

    generator = torch.Generator(device=device).manual_seed(seed)
    q = torch.randn(size, dtype=torch.float64, device=device, generator=generator)
    q = q / q.norm()
    basis, diagonal, off_diagonal = [], [], []
    previous, beta = torch.zeros_like(q), 0.0
    for step in range(min(LANCZOS_STEPS, size)):
        basis.append(q)
        z = matvec(q) - beta * previous
        alpha = q @ z
        z = z - alpha * q
        for _ in range(2):
            for vector in basis:
                z = z - (vector @ z) * vector
        diagonal.append(float(alpha))
        beta = _norm(z)
        if step + 1 == min(LANCZOS_STEPS, size) or beta < 1e-12:
            break
        off_diagonal.append(beta)
        previous, q = q, z / beta

    tri = torch.diag(torch.tensor(diagonal, dtype=torch.float64, device=device))
    if off_diagonal:
        off = torch.tensor(off_diagonal, dtype=torch.float64, device=device)
        tri += torch.diag(off, 1) + torch.diag(off, -1)
    values, vectors = torch.linalg.eigh(tri)
    result = {"seed": seed, "steps": len(diagonal)}
    for name, index in (("minimum", 0), ("maximum", -1)):
        ritz_vector = sum(float(coef) * vector for coef, vector in zip(vectors[:, index], basis))
        value = float(values[index])
        result[name] = {"value": value, "ritz_residual": _norm(matvec(ritz_vector) - value * ritz_vector)}
    return result


def _proposals(ritz):
    values = [row[label]["value"] for row in ritz for label in ("minimum", "maximum")]
    lower, upper = min(values), max(values)
    width = upper - lower
    if not (width > 0):
        raise ValueError("observed Ritz range is not positive-width")
    candidates, rejected = [], []
    for target_radius in TARGET_RADII:
        # OpenGU's registered GIF/IDEA parameter parser requires scale to be an
        # integer. Round the ideal scale, then center the endpoint factors with
        # damp; report the resulting (slightly adjusted) measured Ritz radius.
        scale = int(round(width / (2.0 * target_radius)))
        damp = 1.0 - (upper + lower) / (2.0 * scale)
        shift = scale * damp
        if not (scale > 0 and 0 <= damp < 1):
            rejected.append({"target_radius": target_radius,
                             "reason": "derived damp is outside the GIF/IDEA parameter domain",
                             "scale": scale, "damp": damp, "shift": shift})
            continue
        q_lower = 1.0 - damp - lower / scale
        q_upper = 1.0 - damp - upper / scale
        candidates.append({
            "candidate_id": "target_rho_" + str(target_radius).replace(".", "p"),
            "target_spectral_radius": target_radius,
            "iteration_values": list(ITERATIONS),
            "scale": scale,
            "damp": damp,
            "mu": shift,
            "estimated_endpoint_factors": {"lambda_min": q_lower, "lambda_max": q_upper},
            "estimated_spectral_radius": max(abs(q_lower), abs(q_upper)),
        })
    return {"observed_ritz_range": {"minimum": lower, "maximum": upper},
            "proposed_candidates": candidates, "rejected_targets": rejected,
            "formula": {
                "recurrence_factor": "q(lambda)=1-damp-lambda/scale",
            "target": "integer scale nearest to (lambda_max-lambda_min)/(2*rho); damp centers endpoint factors",
            "ideal_scale": "(lambda_max-lambda_min)/(2*rho)",
            "scale": "round(ideal_scale) to nearest integer, as required by GIF/IDEA config schema",
            "damp": "1-(lambda_max+lambda_min)/(2*scale)",
                "shift": "mu=scale*damp",
            }}


def _relative_config_path(value, base, label):
    if not isinstance(value, str) or not value.strip() or Path(value).is_absolute() or "\\" in value:
        raise ValueError(label + " must be a nonempty project-relative POSIX path")
    resolved = (base / value).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(label + " escapes the project root") from exc
    return resolved


def _load_config(path, config_bytes=None):
    import yaml
    path = path.resolve()
    raw = path.read_bytes() if config_bytes is None else config_bytes
    value = yaml.safe_load(raw.decode("utf-8"))
    if not isinstance(value, dict) or set(value) != CONFIG_FIELDS:
        raise ValueError("theory config must contain exactly: " + ", ".join(sorted(CONFIG_FIELDS)))
    if value["kind"] != "aagu062_theory" or value["schema_version"] != 1:
        raise ValueError("expected aagu062_theory schema_version 1")
    condition = value["condition"]
    if (not isinstance(condition, dict) or set(condition) != {"dataset", "hidden_channels"}
            or condition["dataset"] not in ("Cora", "CiteSeer", "PubMed")
            or type(condition["hidden_channels"]) is not int or condition["hidden_channels"] not in (16, 64)):
        raise ValueError("condition must identify one registered dataset and hidden width")
    model = value["model"]
    if (not isinstance(model, dict) or set(model) != {"architecture", "layers", "hidden_channels"}
            or model["architecture"] != "OpenGU.GCNNet" or model["layers"] != 2
            or model["hidden_channels"] != condition["hidden_channels"]):
        raise ValueError("model identity must match the condition's two-layer GCN checkpoint")
    training = value["training"]
    training_fields = {"seed", "epochs", "optimizer", "lr", "weight_decay", "scheduler"}
    if (not isinstance(training, dict) or set(training) != training_fields
            or training != {"seed": 42, "epochs": 3000, "optimizer": "Adam", "lr": 0.05,
                            "weight_decay": 0.0001, "scheduler": "none"}):
        raise ValueError("training identity must match the registered seed42/3000-epoch PT")
    if value["methods"] != ["GIF", "IDEA"]:
        raise ValueError("methods must be exactly [GIF, IDEA]")
    dataset_config = _relative_config_path(value["dataset_ref"], path.parent, "dataset_ref")
    checkpoint = _relative_config_path(value["checkpoint"], path.parent, "checkpoint")
    if not dataset_config.is_file():
        raise FileNotFoundError("dataset config does not exist: " + str(dataset_config))
    if not checkpoint.is_file():
        raise FileNotFoundError("fixed checkpoint does not exist: " + str(checkpoint))
    return path, value, dataset_config, checkpoint, hashlib.sha256(raw).hexdigest()


def analyze(config_path, device_name, config_bytes=None):
    import torch
    import torch.nn.functional as F
    from experiments.dataset_inputs import read_dataset
    from experiments.modular_config import load_instance
    from experiments.modular_model import create_model
    from utils.target_checkpoint import data_identity, load_weights

    config_path, config, dataset_config, checkpoint, config_sha256 = _load_config(config_path, config_bytes)
    dataset = load_instance(dataset_config, "dataset_split")
    if dataset["dataset"]["name"] != config["condition"]["dataset"]:
        raise ValueError("dataset_ref name differs from the declared condition")
    data, _ = read_dataset(dataset, dataset_config.parent)
    identity = data_identity(data)
    device = torch.device(device_name)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("requested CUDA device is unavailable")
    data = data.to(device)
    results = []
    started = time.perf_counter()
    checkpoint_identity = None
    for method in config["methods"]:
        model = create_model(config["model"], dataset["dataset"]["name"], data, device)
        checkpoint_info = load_weights(checkpoint, model)
        current_checkpoint = {"path": str(checkpoint), "file_sha256": checkpoint_info["file_sha256"],
                             "state_hash": checkpoint_info["state_hash"]}
        if checkpoint_identity is not None and current_checkpoint != checkpoint_identity:
            raise ValueError("method models loaded different checkpoint identities")
        checkpoint_identity = current_checkpoint
        model = model.double().eval()
        working = data.clone()
        working.x = working.x.double()
        parameters = list(model.parameters())
        sizes = [parameter.numel() for parameter in parameters]
        output = model.reason_once(working) if method == "GIF" else model.forward_once(working, None)
        loss = F.cross_entropy(output[working.train_mask], working.y[working.train_mask], reduction="sum")
        gradient = torch.autograd.grad(loss, parameters, create_graph=True, retain_graph=True)

        def matvec(vector):
            pieces = [part.reshape_as(parameter) for part, parameter in zip(vector.detach().split(sizes), parameters)]
            products = torch.autograd.grad(gradient, parameters, grad_outputs=pieces, retain_graph=True)
            return torch.cat([product.detach().reshape(-1) for product in products])

        ritz = [_lanczos(matvec, sum(sizes), device, seed) for seed in LANCZOS_SEEDS]
        results.append({"method": method,
                        "loss": {"definition": "sum cross entropy on persisted train_mask",
                                 "forward": "reason_once" if method == "GIF" else "forward_once(data, None)",
                                 "reduction": "sum", "parameter_count": sum(sizes), "dtype": "float64"},
                        "lanczos": {"seeds": list(LANCZOS_SEEDS), "steps": LANCZOS_STEPS, "starts": ritz},
                        "candidate_design": _proposals(ritz)})
        del model, working, parameters, gradient, output, loss
        if device.type == "cuda":
            torch.cuda.empty_cache()
    try:
        source_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        source_commit = None
    return {
        "schema": "aagu062.theory-analysis.v1",
        "status": "candidate_proposal",
        "condition": config["condition"],
        "dataset_split": {"identity": identity,
                          "manifest": dataset["artifacts"]["manifest"],
                          "manifest_sha256": dataset["artifacts"]["manifest_sha256"]},
        "checkpoint": checkpoint_identity,
        "model": config["model"],
        "training": config["training"],
        "methods": results,
        "candidate_policy": {"target_spectral_radii": list(TARGET_RADII),
                             "iteration_values": list(ITERATIONS),
                             "lanczos_seeds": list(LANCZOS_SEEDS),
                             "lanczos_steps": LANCZOS_STEPS},
        "execution": {"device": str(device), "torch_version": torch.__version__,
                      "source_commit": source_commit,
                      "analysis_tool_sha256": getattr(analyze, "analysis_tool_sha256", None),
                      "theory_config": str(config_path), "theory_config_sha256": config_sha256,
                      "seconds": time.perf_counter() - started},
        "limitation": "Finite Lanczos Ritz estimates are not certified full-spectrum bounds. These values are theory-derived proposals only; the registered Observer calibration must test finite updates, residuals, budget consistency, and nontriviality.",
    }


def main(argv=None):
    global ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--config-yaml-base64")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--analysis-tool-sha256")
    args = parser.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    ROOT = args.project_root.resolve()
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))
    sys.argv[:] = [sys.argv[0]]
    import torch
    torch.set_num_threads(2)
    analyze.analysis_tool_sha256 = args.analysis_tool_sha256
    config_bytes = base64.b64decode(args.config_yaml_base64) if args.config_yaml_base64 else None
    result = analyze(args.config, args.device, config_bytes)
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
