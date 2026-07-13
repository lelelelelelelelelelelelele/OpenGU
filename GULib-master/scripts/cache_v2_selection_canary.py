#!/usr/bin/env python3
"""Run an isolated real-data Cache V2 Selection cold/warm canary.

This CLI deliberately does not import or call the experiment runner.  It loads
the real Planetoid Citeseer graph, derives OpenGU's seed-42 transductive
80/0/20 candidate split, invokes the existing IM selector with both Legacy
ScoreCache layers disabled, and stores only a small V2 Selection Artifact
below an explicitly absolute ``--store-root``.

Run the two phases as separate processes against the same store::

    python scripts/cache_v2_selection_canary.py cold \
        --store-root /tmp/opengu-cache-v2-citeseer \
        --dataset-root /tmp/opengu-cache-v2-citeseer-data \
        --legacy-results-root /path/to/GULib-master/results \
        --allow-download

    python scripts/cache_v2_selection_canary.py warm \
        --store-root /tmp/opengu-cache-v2-citeseer \
        --dataset-root /tmp/opengu-cache-v2-citeseer-data \
        --legacy-results-root /path/to/GULib-master/results \
        --config-name renamed --yaml-path elsewhere.yaml \
        --experiment-id different-request

``warm`` always arms the store's fail-if-called producer sentinel.  Therefore
a successful warm result proves that the producer was not invoked.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import operator
import sys
import time
from contextlib import contextmanager, redirect_stdout
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Sequence, Tuple, Type

import numpy as np
import torch


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cache_v2 import ArtifactRecipe, ProducerVersion, sha256_bytes  # noqa: E402
from cache_v2.errors import ContractValidationError, PathValidationError  # noqa: E402
from cache_v2.store import ArtifactStore, StoreResult  # noqa: E402


DATASET_NAME = "citeseer"
PLANETOID_SOURCE_SPLIT = "public"
SPLIT_SEED = 42
TRAIN_RATIO = 0.8
VAL_RATIO = 0.0
TEST_RATIO = 0.2
NODE_ID_SPACE = "planetoid-global-node-index-v1"
NUMBA_SELECTOR_ALGORITHM_VERSION = "opengu-im-batch-celf-numba-canary-v1"
PYTHON_SELECTOR_ALGORITHM_VERSION = "opengu-im-classic-celf-python-canary-v1"
GRAPH_FINGERPRINT_VERSION = 1
PRODUCER_SEMANTIC_VERSION = "opengu-im-selection-canary-v1"

DEFAULT_LEGACY_RESULTS_ROOT = (REPO_ROOT / "results").resolve(strict=False)


@dataclass(frozen=True)
class SelectionInputs:
    """Canonical graph and candidate inputs consumed by one producer."""

    edge_index: torch.Tensor
    num_nodes: int
    candidate_nodes: Tuple[int, ...]
    graph_fingerprint: str
    candidate_set_hash: str


@dataclass(frozen=True)
class ImParameters:
    propagation_prob: float = 0.1
    mc_rounds: int = 100
    candidate_fraction: float = 1.0
    im_selector_seed: int = 2024
    im_batch_size: int = 5
    parallel_mc: bool = True

    def __post_init__(self) -> None:
        if not 0.0 <= float(self.propagation_prob) <= 1.0:
            raise ContractValidationError("propagation_prob must be in [0, 1]")
        if isinstance(self.mc_rounds, bool) or int(self.mc_rounds) <= 0:
            raise ContractValidationError("mc_rounds must be a positive integer")
        if not 0.0 < float(self.candidate_fraction) <= 1.0:
            raise ContractValidationError("candidate_fraction must be in (0, 1]")
        if isinstance(self.im_batch_size, bool) or int(self.im_batch_size) <= 0:
            raise ContractValidationError("im_batch_size must be a positive integer")


def _plain_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_candidate_nodes(nodes: Iterable[int], num_nodes: int) -> Tuple[int, ...]:
    """Return a sorted, unique, range-checked candidate set."""

    if isinstance(num_nodes, bool) or not isinstance(num_nodes, int) or num_nodes < 0:
        raise ContractValidationError("num_nodes must be a non-negative integer")
    values = []
    for position, node in enumerate(nodes):
        if isinstance(node, bool):
            raise ContractValidationError(
                "candidate node at position {0} must be an integer".format(position)
            )
        try:
            integer = operator.index(node)
        except (TypeError, ValueError, OverflowError):
            raise ContractValidationError(
                "candidate node at position {0} must be an integer".format(position)
            )
        if integer < 0 or integer >= num_nodes:
            raise ContractValidationError(
                "candidate node {0} is outside [0, {1})".format(integer, num_nodes)
            )
        values.append(integer)
    if len(values) != len(set(values)):
        raise ContractValidationError("candidate nodes contain duplicates")
    return tuple(sorted(values))


def canonical_edge_index(edge_index: Any, num_nodes: int) -> torch.Tensor:
    """Return lexicographically sorted, deduplicated CPU int64 edges."""

    tensor = torch.as_tensor(edge_index, dtype=torch.long).detach().cpu()
    if tensor.ndim != 2 or tensor.shape[0] != 2:
        raise ContractValidationError("edge_index must have shape [2, E]")
    if isinstance(num_nodes, bool) or not isinstance(num_nodes, int) or num_nodes < 0:
        raise ContractValidationError("num_nodes must be a non-negative integer")
    if tensor.numel() == 0:
        return tensor.reshape(2, 0).contiguous()
    if bool((tensor < 0).any()) or bool((tensor >= num_nodes).any()):
        raise ContractValidationError("edge_index contains a node outside graph bounds")

    pairs = tensor.t().numpy().astype(np.int64, copy=False)
    order = np.lexsort((pairs[:, 1], pairs[:, 0]))
    pairs = pairs[order]
    keep = np.ones(pairs.shape[0], dtype=np.bool_)
    if pairs.shape[0] > 1:
        keep[1:] = np.any(pairs[1:] != pairs[:-1], axis=1)
    pairs = np.ascontiguousarray(pairs[keep], dtype=np.int64)
    return torch.from_numpy(pairs.T.copy()).long().contiguous()


def graph_fingerprint(edge_index: Any, num_nodes: int) -> str:
    """Full SHA-256 over a canonical topology representation."""

    canonical = canonical_edge_index(edge_index, num_nodes)
    edges = canonical.numpy().astype("<i8", copy=False)
    digest = hashlib.sha256()
    digest.update(b"cache-v2-planetoid-graph\x00")
    digest.update(np.asarray([GRAPH_FINGERPRINT_VERSION], dtype="<i8").tobytes())
    digest.update(np.asarray([num_nodes, edges.shape[1]], dtype="<i8").tobytes())
    digest.update(edges.tobytes(order="C"))
    return digest.hexdigest()


def candidate_fingerprint(candidate_nodes: Sequence[int], num_nodes: int) -> str:
    """Hash candidates exactly as the Selection payload store validates them."""

    candidates = canonical_candidate_nodes(candidate_nodes, num_nodes)
    # ArtifactStore validates candidate_set_hash as SHA-256(canonical JSON list).
    return sha256_bytes(_plain_json_bytes(list(candidates)))


def make_selection_inputs(
    edge_index: Any, num_nodes: int, candidate_nodes: Sequence[int]
) -> SelectionInputs:
    edges = canonical_edge_index(edge_index, num_nodes)
    candidates = canonical_candidate_nodes(candidate_nodes, num_nodes)
    return SelectionInputs(
        edge_index=edges,
        num_nodes=num_nodes,
        candidate_nodes=candidates,
        graph_fingerprint=graph_fingerprint(edges, num_nodes),
        candidate_set_hash=candidate_fingerprint(candidates, num_nodes),
    )


def implementation_backend(has_numba: bool, parallel_mc: bool) -> str:
    if not has_numba:
        return "python"
    return "numba-parallel" if parallel_mc else "numba-serial"


def selector_algorithm_version(has_numba: bool) -> str:
    """Name the semantic algorithm variant, not the execution backend."""

    return (
        NUMBA_SELECTOR_ALGORITHM_VERSION
        if has_numba
        else PYTHON_SELECTOR_ALGORITHM_VERSION
    )


def build_selection_recipe(
    inputs: SelectionInputs,
    k: int,
    parameters: ImParameters,
    has_numba: bool,
) -> ArtifactRecipe:
    """Project only Artifact-producing inputs into a minimal Recipe."""

    if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
        raise ContractValidationError("k must be a positive integer")
    if k > len(inputs.candidate_nodes):
        raise ContractValidationError("k exceeds the candidate count")
    im_parameters = {
        "propagation_prob": float(parameters.propagation_prob),
        "mc_rounds": int(parameters.mc_rounds),
        "candidate_fraction": float(parameters.candidate_fraction),
        "im_selector_seed": int(parameters.im_selector_seed),
    }
    # The Python fallback runs classic CELF and does not consume batch size.
    # Only the Numba batch-CELF Recipe may therefore depend on this field.
    if has_numba:
        im_parameters["im_batch_size"] = int(parameters.im_batch_size)
    return ArtifactRecipe(
        {
            "graph_fingerprint": inputs.graph_fingerprint,
            "candidate_set_hash": inputs.candidate_set_hash,
            "node_id_space": NODE_ID_SPACE,
            "selector": "im",
            "selector_algorithm_version": selector_algorithm_version(has_numba),
            "k": k,
            "im_parameters": im_parameters,
        }
    )


def build_request_envelope(
    config_name: Optional[str],
    yaml_path: Optional[str],
    experiment_id: Optional[str],
    selection_ratio: Optional[float],
) -> Dict[str, Any]:
    """Keep experiment-owned labels outside Artifact identity."""

    values = {
        "config_name": config_name,
        "yaml_path": yaml_path,
        "experiment_id": experiment_id,
        "selection_ratio": selection_ratio,
    }
    return {key: value for key, value in values.items() if value is not None}


@contextmanager
def _sanitized_framework_argv() -> Iterable[None]:
    """Protect the legacy eager parser while importing the isolated strategy."""

    original = sys.argv
    sys.argv = [original[0]]
    try:
        yield
    finally:
        sys.argv = original


def load_im_strategy() -> Tuple[Type[Any], bool, Path]:
    """Load IMStrategy without exposing this CLI's arguments to config.py."""

    with _sanitized_framework_argv():
        from attack.attack_strategies.im_strategy import HAS_NUMBA, IMStrategy

    module_path = REPO_ROOT / "attack" / "attack_strategies" / "im_strategy.py"
    return IMStrategy, bool(HAS_NUMBA), module_path


def build_im_producer(
    inputs: SelectionInputs,
    k: int,
    parameters: ImParameters,
    strategy_class: Type[Any],
) -> Callable[[], Sequence[int]]:
    """Build a producer with both Legacy IM ScoreCache namespaces disabled."""

    strategy_args = {
        "propagation_prob": float(parameters.propagation_prob),
        "mc_rounds": int(parameters.mc_rounds),
        "candidate_fraction": float(parameters.candidate_fraction),
        "im_selector_seed": int(parameters.im_selector_seed),
        "im_batch_size": int(parameters.im_batch_size),
        "im_parallel_mc": bool(parameters.parallel_mc),
        "enable_score_cache": False,
    }
    strategy = strategy_class(strategy_args)
    if getattr(strategy, "_score_cache", None) is not None:
        raise ContractValidationError("IM per-candidate Legacy ScoreCache is not disabled")
    if getattr(strategy, "_celf_cache", None) is not None:
        raise ContractValidationError("IM CELF Legacy ScoreCache is not disabled")

    def produce() -> Sequence[int]:
        selected, _ = strategy.compute_im_celf(
            inputs.edge_index,
            inputs.num_nodes,
            k,
            list(inputs.candidate_nodes),
        )
        return [int(node) for node in selected]

    return produce


def producer_source_fingerprint(strategy_source: Path) -> str:
    digest = hashlib.sha256()
    for label, path in ((b"canary\x00", Path(__file__)), (b"im-strategy\x00", strategy_source)):
        digest.update(label)
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _path_is_within(path: Path, root: Path) -> bool:
    path_text = os.path.normcase(str(path.resolve(strict=False)))
    root_text = os.path.normcase(str(root.resolve(strict=False)))
    try:
        return os.path.commonpath([path_text, root_text]) == root_text
    except ValueError:
        return False


def legacy_cache_roots(results_root: Path) -> Tuple[Path, Path, Path]:
    return (
        results_root / "cache",
        results_root / "selection_cache",
        results_root / "score_cache",
    )


def validate_legacy_results_root(results_root: Path) -> Path:
    supplied = Path(results_root).expanduser()
    if not supplied.is_absolute():
        raise PathValidationError("--legacy-results-root must be explicitly absolute")
    if ".." in supplied.parts:
        raise PathValidationError("--legacy-results-root must not contain '..'")
    return supplied.resolve(strict=False)


def validate_isolated_store_root(
    store_root: Path, forbidden_roots: Sequence[Path]
) -> Path:
    supplied = Path(store_root).expanduser()
    if not supplied.is_absolute():
        raise PathValidationError("--store-root must be explicitly absolute")
    if ".." in supplied.parts:
        raise PathValidationError("--store-root must not contain '..'")
    resolved = supplied.resolve(strict=False)
    for legacy_root in forbidden_roots:
        if _path_is_within(resolved, legacy_root):
            raise PathValidationError(
                "--store-root must not be inside Legacy cache path {0}".format(
                    legacy_root
                )
            )
    return resolved


def validate_dataset_root(dataset_root: Path, allow_download: bool) -> Path:
    supplied = Path(dataset_root).expanduser()
    if not supplied.is_absolute():
        raise PathValidationError("--dataset-root must be explicitly absolute")
    if ".." in supplied.parts:
        raise PathValidationError("--dataset-root must not contain '..'")
    root = supplied.resolve(strict=False)
    processed = root / DATASET_NAME / "processed" / "data.pt"
    if not allow_download and not processed.is_file():
        raise FileNotFoundError(
            "processed Planetoid Citeseer data is missing at {0}; "
            "pass --allow-download explicitly to let PyG create it".format(processed)
        )
    return root


def opengu_train_candidates(num_nodes: int, split_seed: int = SPLIT_SEED) -> Tuple[int, ...]:
    """Mirror OpenGU's seed-controlled transductive 80/0/20 node split."""

    if isinstance(num_nodes, bool) or not isinstance(num_nodes, int) or num_nodes <= 0:
        raise ContractValidationError("num_nodes must be a positive integer")
    if isinstance(split_seed, bool) or not isinstance(split_seed, int):
        raise ContractValidationError("split_seed must be an integer")
    generator = torch.Generator(device="cpu")
    generator.manual_seed(split_seed)
    permutation = torch.randperm(num_nodes, generator=generator)
    train_count = int(TRAIN_RATIO * num_nodes)
    return canonical_candidate_nodes(permutation[:train_count].tolist(), num_nodes)


def load_planetoid_citeseer(dataset_root: Path) -> SelectionInputs:
    from torch_geometric.datasets import Planetoid

    dataset = Planetoid(
        root=str(dataset_root), name=DATASET_NAME, split=PLANETOID_SOURCE_SPLIT
    )
    data = dataset[0]
    # Mirror OpenGU's transductive_split_node with a local Generator so the
    # canary neither consumes nor mutates the process-global torch RNG state.
    candidates = opengu_train_candidates(int(data.num_nodes))
    if not candidates:
        raise ContractValidationError("derived OpenGU Citeseer train split is empty")
    return make_selection_inputs(data.edge_index, int(data.num_nodes), candidates)


def _tree_snapshot(root: Path) -> Dict[str, Any]:
    if not root.exists():
        return {"exists": False, "files": []}
    files = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        stat = path.stat()
        files.append(
            {
                "path": path.relative_to(root).as_posix(),
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
                "sha256": _sha256_file(path),
            }
        )
    return {"exists": True, "files": files}


def legacy_cache_state(roots: Sequence[Path]) -> Tuple[str, Dict[str, int]]:
    state = {}
    counts = {}
    for root in roots:
        snapshot = _tree_snapshot(root)
        state[root.name] = snapshot
        counts[root.name] = len(snapshot["files"])
    return sha256_bytes(_plain_json_bytes(state)), counts


def run_store_phase(
    mode: str,
    store_root: Path,
    recipe: ArtifactRecipe,
    producer: Callable[[], Sequence[int]],
    inputs: SelectionInputs,
    producer_version: ProducerVersion,
    request_envelope: Mapping[str, Any],
) -> Tuple[StoreResult, float]:
    """Execute one cold or warm phase; callers may use separate processes."""

    if mode not in ("cold", "warm"):
        raise ContractValidationError("mode must be cold or warm")
    store = ArtifactStore(store_root, producer_version=producer_version)
    if mode == "cold":
        if store.index.database_path.exists():
            raise RuntimeError(
                "cold phase requires a fresh store without an existing index"
            )
        store.initialize()
    else:
        # A warm command must never create a missing database. An explicit
        # read-only schema check fails closed before resolution if the cold
        # process did not initialize this exact store.
        store.index.check_schema()
    started = time.perf_counter()
    result = store.get_or_compute(
        recipe,
        producer,
        num_nodes=inputs.num_nodes,
        candidate_nodes=inputs.candidate_nodes,
        request_envelope=request_envelope,
        fail_if_called=(mode == "warm"),
    )
    elapsed = time.perf_counter() - started
    if mode == "cold" and (result.hit or not result.producer_called):
        raise RuntimeError(
            "cold phase expected a miss with producer_called=true; use a fresh store root"
        )
    if mode == "warm" and (not result.hit or result.producer_called):
        raise RuntimeError("warm phase did not prove an exact hit without producer")
    return result, elapsed


def result_document(
    mode: str,
    store_root: Path,
    result: StoreResult,
    recipe: ArtifactRecipe,
    inputs: SelectionInputs,
    request_envelope: Mapping[str, Any],
    k: int,
    selection_ratio: Optional[float],
    parameters: ImParameters,
    backend: str,
    algorithm_version: str,
    producer_version: ProducerVersion,
    dataset_load_seconds: float,
    resolve_seconds: float,
    total_seconds: float,
    legacy_before: str,
    legacy_after: str,
    legacy_counts: Mapping[str, int],
    legacy_results_root: Path,
) -> Dict[str, Any]:
    payload_path = store_root.joinpath(*PurePosixPath(result.semantic_path).parts)
    stat = payload_path.stat()
    payload_hash = _sha256_file(payload_path)
    if payload_hash != result.content_hash:
        raise RuntimeError("reported payload hash does not match StoreResult content_hash")
    producer_call_count = ArtifactStore(
        store_root, producer_version=producer_version
    ).producer_call_count
    return {
        "ok": True,
        "report_version": 1,
        "mode": mode,
        "dataset": DATASET_NAME,
        "planetoid_source_split": PLANETOID_SOURCE_SPLIT,
        "selection_split": {
            "kind": "opengu-transductive-randperm",
            "seed": SPLIT_SEED,
            "train_ratio": TRAIN_RATIO,
            "val_ratio": VAL_RATIO,
            "test_ratio": TEST_RATIO,
        },
        "store_root": str(store_root),
        "hit": result.hit,
        "outcome": result.outcome,
        "producer_called": result.producer_called,
        "producer_call_count": producer_call_count,
        "artifact_id": result.artifact_id,
        "recipe_hash": recipe.recipe_hash,
        "content_hash": result.content_hash,
        "semantic_path": result.semantic_path,
        "payload_sha256": payload_hash,
        "payload_mtime_ns": stat.st_mtime_ns,
        "payload_size_bytes": stat.st_size,
        "selected_nodes": list(result.payload.selected_nodes_ordered),
        "ordered_nodes_hash": result.payload.ordered_nodes_hash,
        "node_set_hash": result.payload.node_set_hash,
        "graph_fingerprint": inputs.graph_fingerprint,
        "candidate_fingerprint": inputs.candidate_set_hash,
        "candidate_set_hash": inputs.candidate_set_hash,
        "num_nodes": inputs.num_nodes,
        "candidate_count": len(inputs.candidate_nodes),
        "k": k,
        "selection_ratio": selection_ratio,
        "selector_algorithm_version": algorithm_version,
        "execution_backend": backend,
        "im_parameters": {
            "propagation_prob": float(parameters.propagation_prob),
            "mc_rounds": int(parameters.mc_rounds),
            "candidate_fraction": float(parameters.candidate_fraction),
            "im_selector_seed": int(parameters.im_selector_seed),
            "im_batch_size": int(parameters.im_batch_size),
        },
        "producer_version": producer_version.to_dict(),
        "request_envelope": dict(request_envelope),
        "legacy_score_cache_enabled": False,
        "legacy_results_root": str(legacy_results_root),
        "legacy_cache_unchanged": legacy_before == legacy_after,
        "legacy_cache_state_hash_before": legacy_before,
        "legacy_cache_state_hash_after": legacy_after,
        "legacy_cache_file_counts": dict(legacy_counts),
        "dataset_load_seconds": dataset_load_seconds,
        "resolve_seconds": resolve_seconds,
        "elapsed_seconds": total_seconds,
        "miss_reasons": list(result.miss_reasons),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("mode", choices=("cold", "warm"))
    parser.add_argument("--store-root", type=Path, required=True)
    parser.add_argument("--dataset-root", type=Path, required=True)
    parser.add_argument(
        "--legacy-results-root",
        type=Path,
        default=DEFAULT_LEGACY_RESULTS_ROOT,
        help="absolute Legacy results root to snapshot read-only",
    )
    parser.add_argument("--allow-download", action="store_true")
    budget = parser.add_mutually_exclusive_group()
    budget.add_argument("--k", type=int)
    budget.add_argument("--selection-ratio", type=float)
    parser.add_argument("--propagation-prob", type=float, default=0.1)
    parser.add_argument("--mc-rounds", type=int, default=100)
    parser.add_argument("--candidate-fraction", type=float, default=1.0)
    parser.add_argument("--im-selector-seed", type=int, default=2024)
    parser.add_argument("--im-batch-size", type=int, default=5)
    parser.add_argument("--serial-mc", action="store_true")
    parser.add_argument("--config-name")
    parser.add_argument("--yaml-path")
    parser.add_argument("--experiment-id")
    return parser


def execute(args: argparse.Namespace) -> Dict[str, Any]:
    total_started = time.perf_counter()
    legacy_results_root = validate_legacy_results_root(args.legacy_results_root)
    legacy_roots = legacy_cache_roots(legacy_results_root)
    store_root = validate_isolated_store_root(
        args.store_root, (legacy_results_root,)
    )
    dataset_root = validate_dataset_root(args.dataset_root, args.allow_download)
    if _path_is_within(dataset_root, legacy_results_root):
        raise PathValidationError(
            "--dataset-root must not be inside the Legacy results tree"
        )
    parameters = ImParameters(
        propagation_prob=args.propagation_prob,
        mc_rounds=args.mc_rounds,
        candidate_fraction=args.candidate_fraction,
        im_selector_seed=args.im_selector_seed,
        im_batch_size=args.im_batch_size,
        parallel_mc=not args.serial_mc,
    )

    legacy_before, legacy_counts = legacy_cache_state(legacy_roots)
    load_started = time.perf_counter()
    # Redirect third-party progress to stderr so stdout remains one JSON object.
    with redirect_stdout(sys.stderr):
        inputs = load_planetoid_citeseer(dataset_root)
        strategy_class, has_numba, strategy_source = load_im_strategy()
    dataset_load_seconds = time.perf_counter() - load_started

    ratio = args.selection_ratio
    if args.k is None and ratio is None:
        ratio = 0.05
    if args.k is None:
        if not 0.0 < float(ratio) <= 1.0:
            raise ContractValidationError("selection_ratio must be in (0, 1]")
        k = max(1, int(len(inputs.candidate_nodes) * float(ratio)))
    else:
        k = args.k

    backend = implementation_backend(has_numba, parameters.parallel_mc)
    algorithm_version = selector_algorithm_version(has_numba)
    recipe = build_selection_recipe(inputs, k, parameters, has_numba)
    envelope = build_request_envelope(
        args.config_name, args.yaml_path, args.experiment_id, ratio
    )
    producer = build_im_producer(inputs, k, parameters, strategy_class)
    producer_version = ProducerVersion(
        semantic_version=PRODUCER_SEMANTIC_VERSION,
        source_fingerprint=producer_source_fingerprint(strategy_source),
    )
    with redirect_stdout(sys.stderr):
        result, resolve_seconds = run_store_phase(
            args.mode,
            store_root,
            recipe,
            producer,
            inputs,
            producer_version,
            envelope,
        )

    legacy_after, _ = legacy_cache_state(legacy_roots)
    if legacy_after != legacy_before:
        raise RuntimeError("a Legacy cache path changed during the isolated canary")
    total_seconds = time.perf_counter() - total_started
    return result_document(
        args.mode,
        store_root,
        result,
        recipe,
        inputs,
        envelope,
        k,
        ratio,
        parameters,
        backend,
        algorithm_version,
        producer_version,
        dataset_load_seconds,
        resolve_seconds,
        total_seconds,
        legacy_before,
        legacy_after,
        legacy_counts,
        legacy_results_root,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _parser()
    try:
        args = parser.parse_args(argv)
        document = execute(args)
    except Exception as exc:
        document = {
            "ok": False,
            "report_version": 1,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        print(json.dumps(document, ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(document, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
