"""Run the local B/C selection and set-deletion matrix sequentially."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULT_ROOT = REPO_ROOT / "results" / "bc_target_v2"
DEFAULT_CACHE_ROOT = REPO_ROOT / "results" / "cache_v2" / "bc_target_v2"
DEFAULT_DATA_ROOT = Path(
    "E:/project/OpenGU/GULib-master/data/raw/Planetoid"
)


def _str_list(value: str) -> Sequence[str]:
    result = tuple(item.strip() for item in value.split(",") if item.strip())
    if not result:
        raise argparse.ArgumentTypeError("expected comma-separated names")
    return result


def _int_list(value: str) -> Sequence[int]:
    result = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    if not result:
        raise argparse.ArgumentTypeError("expected comma-separated integers")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--datasets",
        type=_str_list,
        default=("Cora", "CiteSeer", "PubMed"),
    )
    parser.add_argument("--seeds", type=_int_list, default=(42, 212, 2024))
    parser.add_argument(
        "--stage",
        choices=("selection", "downstream", "all"),
        default="all",
    )
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--cache-root", type=Path, default=DEFAULT_CACHE_ROOT)
    parser.add_argument("--result-root", type=Path, default=DEFAULT_RESULT_ROOT)
    parser.add_argument("--overwrite", action="store_true")
    return parser


def _run(command) -> None:
    print("[bc-matrix] RUN {0}".format(" ".join(command)), flush=True)
    subprocess.run(command, cwd=str(REPO_ROOT), check=True)


def main(argv: Sequence[str] = None) -> int:
    args = build_parser().parse_args(argv)
    result_root = args.result_root.expanduser().resolve()
    selection_dir = result_root / "selection"
    downstream_dir = result_root / "downstream"
    selection_dir.mkdir(parents=True, exist_ok=True)
    downstream_dir.mkdir(parents=True, exist_ok=True)

    for dataset in args.datasets:
        for seed in args.seeds:
            prefix = "{0}_gcn_seed{1}".format(dataset.lower(), int(seed))
            selection_output = selection_dir / (prefix + "_selection.json")
            if args.stage in ("selection", "all"):
                if selection_output.exists() and not args.overwrite:
                    print(
                        "[bc-matrix] SKIP existing {0}".format(selection_output),
                        flush=True,
                    )
                else:
                    command = [
                        sys.executable,
                        "-m",
                        "experiments.bc_target_v2.run_selection",
                        "--dataset",
                        dataset,
                        "--seed",
                        str(seed),
                        "--data-root",
                        str(args.data_root.expanduser().resolve()),
                        "--cache-root",
                        str(args.cache_root.expanduser().resolve()),
                        "--output",
                        str(selection_output),
                    ]
                    if args.overwrite:
                        command.append("--overwrite-output")
                    _run(command)

            if args.stage in ("downstream", "all"):
                if not selection_output.exists():
                    raise FileNotFoundError(
                        "selection summary is missing: {0}".format(
                            selection_output
                        )
                    )
                downstream_output = downstream_dir / (
                    prefix + "_downstream.json"
                )
                if downstream_output.exists() and not args.overwrite:
                    print(
                        "[bc-matrix] SKIP existing {0}".format(
                            downstream_output
                        ),
                        flush=True,
                    )
                else:
                    command = [
                        sys.executable,
                        "-m",
                        "experiments.bc_target_v2.run_downstream",
                        "--selection-summary",
                        str(selection_output),
                        "--output",
                        str(downstream_output),
                    ]
                    if args.overwrite:
                        command.append("--overwrite-output")
                    _run(command)

    _run(
        [
            sys.executable,
            "-m",
            "experiments.bc_target_v2.aggregate",
            "--selection-dir",
            str(selection_dir),
            "--downstream-dir",
            str(downstream_dir),
            "--output-dir",
            str(result_root / "aggregate"),
        ]
    )
    print("[bc-matrix] COMPLETE", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
