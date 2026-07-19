#!/usr/bin/env python3
"""Run a Cache V2 Selection cold/warm canary through the OpenGU layer.

The canary intentionally delegates dataset access and Selection production to
``experiments.selection_inputs`` and ``experiments.selection_producer``.  Its
input is OpenGU's canonical processed pickle; it has no downloader and never
constructs a split.  Cache V2 receives only the resulting Recipe identity and
ordered Selection Artifact.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Optional, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROCESSED_ROOT = (REPO_ROOT / "data" / "processed").resolve(strict=False)
DEFAULT_LEGACY_RESULTS_ROOT = (REPO_ROOT / "results").resolve(strict=False)


def _absolute_path(value: Path, label: str) -> Path:
    supplied = Path(value).expanduser()
    if not supplied.is_absolute():
        raise ValueError("{0} must be explicitly absolute".format(label))
    if ".." in supplied.parts:
        raise ValueError("{0} must not contain '..'".format(label))
    return supplied.resolve(strict=False)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("mode", choices=("cold", "warm"))
    parser.add_argument("--store-root", type=Path, required=True)
    parser.add_argument(
        "--processed-root",
        type=Path,
        default=DEFAULT_PROCESSED_ROOT,
        help="OpenGU canonical data/processed root",
    )
    parser.add_argument(
        "--legacy-results-root",
        type=Path,
        default=DEFAULT_LEGACY_RESULTS_ROOT,
        help="Legacy results root, snapshotted read-only",
    )
    parser.add_argument("--dataset", default="cora")
    parser.add_argument("--base-model", default="GCN")
    parser.add_argument("--method", default="GIF")
    parser.add_argument(
        "--strategy", choices=("random", "degree", "pagerank", "im"), default="im"
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--selection-ratio", type=float, default=0.05)
    parser.add_argument("--train-ratio", type=float, default=0.8)
    parser.add_argument("--val-ratio", type=float, default=0.0)
    parser.add_argument("--test-ratio", type=float, default=0.2)
    parser.add_argument("--balanced", action="store_true")
    parser.add_argument("--inductive", action="store_true")
    parser.add_argument("--pagerank-alpha", type=float, default=0.85)
    parser.add_argument("--propagation-prob", type=float, default=0.1)
    parser.add_argument("--mc-rounds", type=int, default=100)
    parser.add_argument("--candidate-fraction", type=float, default=1.0)
    parser.add_argument("--im-selector-seed", type=int, default=2024)
    parser.add_argument("--im-batch-size", type=int, default=5)
    parser.add_argument("--serial-mc", action="store_true")
    return parser


def _selection_config(args: argparse.Namespace) -> Dict[str, Any]:
    return {
        "name": "cache-v2-selection-canary",
        "dataset": str(args.dataset),
        "base_model": str(args.base_model),
        "ratio": float(args.selection_ratio),
        "methods": [str(args.method)],
        "strategies": [str(args.strategy)],
        "seeds": [int(args.seed)],
        "extra_args": [
            "--train_ratio", str(float(args.train_ratio)),
            "--val_ratio", str(float(args.val_ratio)),
            "--test_ratio", str(float(args.test_ratio)),
            "--is_transductive", str(not bool(args.inductive)).lower(),
            "--is_balanced", str(bool(args.balanced)).lower(),
            "--pagerank_alpha", str(float(args.pagerank_alpha)),
            "--propagation_prob", str(float(args.propagation_prob)),
            "--mc_rounds", str(int(args.mc_rounds)),
            "--candidate_fraction", str(float(args.candidate_fraction)),
            "--im_selector_seed", str(int(args.im_selector_seed)),
            "--im_batch_size", str(int(args.im_batch_size)),
            "--im_parallel_mc", str(not bool(args.serial_mc)).lower(),
        ],
    }


def _validate_phase(mode: str, document: Dict[str, Any]) -> None:
    results = document.get("results") or []
    if not results:
        raise RuntimeError("canary produced no Selection result")
    if mode == "cold":
        if any(item.get("hit") or not item.get("producer_called") for item in results):
            raise RuntimeError("cold canary requires a clean miss and one upstream producer call")
        return
    if any(not item.get("hit") or item.get("producer_called") for item in results):
        raise RuntimeError("warm canary requires exact hits and zero producer calls")


def execute(
    args: argparse.Namespace,
    *,
    dataset_inputs: Optional[Any] = None,
) -> Dict[str, Any]:
    from experiments.selection_producer import materialize_selection

    store_root = _absolute_path(args.store_root, "store root")
    processed_root = _absolute_path(args.processed_root, "processed root")
    legacy_results_root = _absolute_path(
        args.legacy_results_root, "legacy results root"
    )
    document = materialize_selection(
        config_source=_selection_config(args),
        processed_root=processed_root,
        store_root=store_root,
        legacy_results_root=legacy_results_root,
        verify=True,
        fail_if_producer_called=args.mode == "warm",
        compare_legacy=False,
        include_nodes=True,
        dataset_inputs=dataset_inputs,
    )
    _validate_phase(args.mode, document)
    output = dict(document)
    output.update(
        {
            "canary_mode": args.mode,
            "dataset_access_owner": "experiments.selection_inputs",
            "selection_producer_owner": "experiments.selection_producer",
            "download_performed": False,
            "split_reconstructed": False,
        }
    )
    return output


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parser().parse_args(argv)
    print(json.dumps(execute(args), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
