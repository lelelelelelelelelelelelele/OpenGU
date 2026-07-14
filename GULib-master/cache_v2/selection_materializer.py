"""Exact-only V2 Selection planning and materialization.

The experiment YAML is a request envelope, never Artifact identity.  This
module projects the YAML onto the minimal inputs consumed by a registered
Selection producer, resolves ``(artifact_type, recipe_hash)`` directly through
the SQLite index, and calls the producer only on a clean exact miss.

Only the topology-only IM producer is registered initially.  TracIn and
Hybrid are represented as structured skips until their model/Score provenance
contracts are ready; adding them later is a registry extension rather than a
new lookup path.
"""

from __future__ import annotations

import hashlib
import json
import math
import operator
import os
import sys
import time
from contextlib import contextmanager, redirect_stdout
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Type

import numpy as np
import torch
import yaml

from .canonical import sha256_bytes
from .contracts import ArtifactRecipe, ArtifactType, ProducerVersion
from .errors import (
    CacheV2Error,
    ContractValidationError,
    LegacySourceChangedError,
    PathValidationError,
)
from .index import CacheIndex
from .resolver import ArtifactResolver
from .store import ArtifactStore, CacheResolutionError, StoreResult


GRAPH_FINGERPRINT_VERSION = 1
NODE_ID_SPACE = "pyg-global-node-index-v1"
IM_NUMBA_ALGORITHM_VERSION = "opengu-im-batch-celf-numba-v1"
IM_PYTHON_ALGORITHM_VERSION = "opengu-im-classic-celf-python-v1"
IM_PRODUCER_SEMANTIC_VERSION = "opengu-im-selection-v1"
PLANETOID_DATASETS = frozenset(("cora", "citeseer", "pubmed"))
OGB_NODE_DATASETS = frozenset(("ogbn-arxiv", "ogbn-products"))
FUTURE_PRODUCERS = frozenset(("tracin", "hybrid"))


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


def _ordered_nodes_hash(nodes: Sequence[int]) -> str:
    return sha256_bytes(_plain_json_bytes([int(node) for node in nodes]))


def canonical_candidate_nodes(nodes: Iterable[int], num_nodes: int) -> Tuple[int, ...]:
    if isinstance(num_nodes, bool) or not isinstance(num_nodes, int) or num_nodes < 0:
        raise ContractValidationError("num_nodes must be a non-negative integer")
    values: List[int] = []
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
    canonical = canonical_edge_index(edge_index, num_nodes)
    edges = canonical.numpy().astype("<i8", copy=False)
    digest = hashlib.sha256()
    digest.update(b"cache-v2-graph\x00")
    digest.update(np.asarray([GRAPH_FINGERPRINT_VERSION], dtype="<i8").tobytes())
    digest.update(np.asarray([num_nodes, edges.shape[1]], dtype="<i8").tobytes())
    digest.update(edges.tobytes(order="C"))
    return digest.hexdigest()


def legacy_graph_fingerprint(
    edge_index: Any, num_nodes: int, candidate_nodes: Sequence[int]
) -> str:
    """Mirror the Legacy AttackManager fingerprint for comparison only."""

    edges = torch.as_tensor(edge_index, dtype=torch.long).detach().cpu().numpy()
    edges = edges.astype(np.int64, copy=False)
    candidates = np.asarray(candidate_nodes, dtype=np.int64)
    digest = hashlib.sha256()
    digest.update(np.int64(num_nodes).tobytes())
    digest.update(edges.tobytes())
    digest.update(candidates.tobytes())
    return digest.hexdigest()[:32]


def candidate_fingerprint(candidate_nodes: Sequence[int], num_nodes: int) -> str:
    candidates = canonical_candidate_nodes(candidate_nodes, num_nodes)
    return sha256_bytes(_plain_json_bytes(list(candidates)))


@dataclass(frozen=True)
class SelectionInputs:
    edge_index: torch.Tensor
    num_nodes: int
    candidate_nodes: Tuple[int, ...]
    graph_fingerprint: str
    candidate_set_hash: str
    legacy_graph_fingerprint: str


def make_selection_inputs(
    edge_index: Any, num_nodes: int, candidate_nodes: Sequence[int]
) -> SelectionInputs:
    candidates = canonical_candidate_nodes(candidate_nodes, num_nodes)
    legacy_fingerprint = legacy_graph_fingerprint(edge_index, num_nodes, candidates)
    canonical_edges = canonical_edge_index(edge_index, num_nodes)
    return SelectionInputs(
        edge_index=canonical_edges,
        num_nodes=num_nodes,
        candidate_nodes=candidates,
        graph_fingerprint=graph_fingerprint(canonical_edges, num_nodes),
        candidate_set_hash=candidate_fingerprint(candidates, num_nodes),
        legacy_graph_fingerprint=legacy_fingerprint,
    )


def transductive_candidates(
    num_nodes: int, split_seed: int, train_ratio: float
) -> Tuple[int, ...]:
    if isinstance(num_nodes, bool) or not isinstance(num_nodes, int) or num_nodes <= 0:
        raise ContractValidationError("num_nodes must be a positive integer")
    if isinstance(split_seed, bool) or not isinstance(split_seed, int):
        raise ContractValidationError("split_seed must be an integer")
    if not 0.0 < float(train_ratio) < 1.0:
        raise ContractValidationError("train_ratio must be in (0, 1)")
    generator = torch.Generator(device="cpu")
    generator.manual_seed(split_seed)
    permutation = torch.randperm(num_nodes, generator=generator)
    count = int(float(train_ratio) * num_nodes)
    return canonical_candidate_nodes(permutation[:count].tolist(), num_nodes)


def _path_is_within(path: Path, root: Path) -> bool:
    path_text = os.path.normcase(str(path.resolve(strict=False)))
    root_text = os.path.normcase(str(root.resolve(strict=False)))
    try:
        return os.path.commonpath([path_text, root_text]) == root_text
    except ValueError:
        return False


def _absolute_path(value: Any, label: str) -> Path:
    supplied = Path(value).expanduser()
    if not supplied.is_absolute():
        raise PathValidationError("{0} must be explicitly absolute".format(label))
    if ".." in supplied.parts:
        raise PathValidationError("{0} must not contain '..'".format(label))
    return supplied.resolve(strict=False)


def legacy_cache_roots(results_root: Path) -> Tuple[Path, Path, Path]:
    return (
        results_root / "cache",
        results_root / "selection_cache",
        results_root / "score_cache",
    )


def validate_legacy_results_root(results_root: Any) -> Path:
    return _absolute_path(results_root, "legacy results root")


def validate_store_root(store_root: Any, legacy_roots: Sequence[Path]) -> Path:
    root = _absolute_path(store_root, "store root")
    for legacy_root in legacy_roots:
        legacy = legacy_root.resolve(strict=False)
        if _path_is_within(root, legacy) or _path_is_within(legacy, root):
            raise PathValidationError(
                "store root must not overlap Legacy cache path: {0}".format(legacy)
            )
    return root


def _dataset_marker(dataset_root: Path, dataset_name: str) -> Path:
    if dataset_name in PLANETOID_DATASETS:
        return dataset_root / dataset_name / "processed" / "data.pt"
    if dataset_name in OGB_NODE_DATASETS:
        return (
            dataset_root
            / dataset_name.replace("-", "_")
            / "processed"
            / "geometric_data_processed.pt"
        )
    raise ContractValidationError(
        "no Selection dataset adapter is registered for {0}".format(dataset_name)
    )


def _dataset_storage_root(dataset_root: Path, dataset_name: str) -> Path:
    if dataset_name in PLANETOID_DATASETS:
        return dataset_root / dataset_name
    if dataset_name in OGB_NODE_DATASETS:
        return dataset_root / dataset_name.replace("-", "_")
    raise ContractValidationError(
        "no Selection dataset adapter is registered for {0}".format(dataset_name)
    )


def validate_dataset_root(
    dataset_root: Any,
    dataset_name: str,
    allow_download: bool,
    legacy_roots: Sequence[Path],
) -> Path:
    root = _absolute_path(dataset_root, "dataset root")
    for legacy_root in legacy_roots:
        if _path_is_within(root, legacy_root) or _path_is_within(legacy_root, root):
            raise PathValidationError(
                "dataset root must not overlap Legacy cache path: {0}".format(
                    legacy_root
                )
            )
    marker = _dataset_marker(root, dataset_name)
    if not allow_download and not marker.is_file():
        raise FileNotFoundError(
            "processed dataset is missing at {0}; pass --allow-download explicitly"
            .format(marker)
        )
    return root


def load_selection_inputs(
    dataset_name: str,
    dataset_root: Path,
    split_seed: int,
    train_ratio: float,
) -> SelectionInputs:
    marker = _dataset_marker(dataset_root, dataset_name)
    if marker.is_file():
        try:
            stored = torch.load(marker, map_location="cpu", weights_only=False)
        except TypeError:  # torch < 2.0 has no weights_only argument
            stored = torch.load(marker, map_location="cpu")
        data = stored[0] if isinstance(stored, tuple) else stored
        if not hasattr(data, "edge_index"):
            raise ContractValidationError(
                "processed dataset does not contain a graph Data object: {0}".format(
                    marker
                )
            )
    elif dataset_name in PLANETOID_DATASETS:
        from torch_geometric.datasets import Planetoid

        dataset = Planetoid(root=str(dataset_root), name=dataset_name, split="public")
        data = dataset[0]
    elif dataset_name in OGB_NODE_DATASETS:
        from ogb.nodeproppred import PygNodePropPredDataset

        dataset = PygNodePropPredDataset(name=dataset_name, root=str(dataset_root))
        data = dataset[0]
    else:
        raise ContractValidationError(
            "no Selection dataset adapter is registered for {0}".format(dataset_name)
        )
    if dataset_name in OGB_NODE_DATASETS:
        from torch_geometric.transforms import ToUndirected

        data = ToUndirected()(data)
    num_nodes = int(data.num_nodes)
    candidates = transductive_candidates(num_nodes, split_seed, train_ratio)
    if not candidates:
        raise ContractValidationError("derived transductive candidate set is empty")
    return make_selection_inputs(data.edge_index, num_nodes, candidates)


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
        if isinstance(self.im_selector_seed, bool) or not isinstance(
            self.im_selector_seed, int
        ):
            raise ContractValidationError("im_selector_seed must be an integer")
        if isinstance(self.im_batch_size, bool) or int(self.im_batch_size) <= 0:
            raise ContractValidationError("im_batch_size must be a positive integer")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "propagation_prob": float(self.propagation_prob),
            "mc_rounds": int(self.mc_rounds),
            "candidate_fraction": float(self.candidate_fraction),
            "im_selector_seed": int(self.im_selector_seed),
            "im_batch_size": int(self.im_batch_size),
            "parallel_mc": bool(self.parallel_mc),
        }


def implementation_backend(has_numba: bool, parallel_mc: bool) -> str:
    if not has_numba:
        return "python"
    return "numba-parallel" if parallel_mc else "numba-serial"


def im_algorithm_version(has_numba: bool) -> str:
    return IM_NUMBA_ALGORITHM_VERSION if has_numba else IM_PYTHON_ALGORITHM_VERSION


def build_im_recipe(
    inputs: SelectionInputs,
    k: int,
    parameters: ImParameters,
    has_numba: bool,
) -> ArtifactRecipe:
    if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
        raise ContractValidationError("k must be a positive integer")
    if k > len(inputs.candidate_nodes):
        raise ContractValidationError("k exceeds the candidate count")
    im_parameters: Dict[str, Any] = {
        "propagation_prob": float(parameters.propagation_prob),
        "mc_rounds": int(parameters.mc_rounds),
        "candidate_fraction": float(parameters.candidate_fraction),
        "im_selector_seed": int(parameters.im_selector_seed),
    }
    if has_numba:
        im_parameters["im_batch_size"] = int(parameters.im_batch_size)
    return ArtifactRecipe(
        {
            "graph_fingerprint": inputs.graph_fingerprint,
            "candidate_set_hash": inputs.candidate_set_hash,
            "node_id_space": NODE_ID_SPACE,
            "selector": "im",
            "selector_algorithm_version": im_algorithm_version(has_numba),
            "k": k,
            "im_parameters": im_parameters,
        }
    )


@contextmanager
def _sanitized_framework_argv() -> Iterable[None]:
    original = sys.argv
    sys.argv = [original[0]]
    try:
        yield
    finally:
        sys.argv = original


def load_im_strategy() -> Tuple[Type[Any], bool, Path]:
    with _sanitized_framework_argv():
        from attack.attack_strategies.im_strategy import HAS_NUMBA, IMStrategy

    source = Path(__file__).resolve().parents[1] / "attack" / "attack_strategies" / "im_strategy.py"
    return IMStrategy, bool(HAS_NUMBA), source


def build_im_producer(
    inputs: SelectionInputs,
    k: int,
    parameters: ImParameters,
    strategy_class: Type[Any],
) -> Callable[[], Sequence[int]]:
    strategy = strategy_class(
        {
            "propagation_prob": float(parameters.propagation_prob),
            "mc_rounds": int(parameters.mc_rounds),
            "candidate_fraction": float(parameters.candidate_fraction),
            "im_selector_seed": int(parameters.im_selector_seed),
            "im_batch_size": int(parameters.im_batch_size),
            "im_parallel_mc": bool(parameters.parallel_mc),
            "enable_score_cache": False,
        }
    )
    if getattr(strategy, "_score_cache", None) is not None:
        raise ContractValidationError("IM per-candidate Legacy ScoreCache is enabled")
    if getattr(strategy, "_celf_cache", None) is not None:
        raise ContractValidationError("IM CELF Legacy ScoreCache is enabled")

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
    for label, path in (
        (b"selection-materializer\x00", Path(__file__)),
        (b"im-strategy\x00", strategy_source),
    ):
        digest.update(label)
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _stable_hash32(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_plain_json_bytes(dict(value))).hexdigest()[:32]


def _legacy_im_parameter_fingerprint(parameters: ImParameters) -> str:
    return _stable_hash32(
        {
            "propagation_prob": float(parameters.propagation_prob),
            "mc_rounds": int(parameters.mc_rounds),
            "candidate_fraction": float(parameters.candidate_fraction),
            "im_batch_size": int(parameters.im_batch_size),
        }
    )


def _require_list(config: Mapping[str, Any], key: str) -> Tuple[Any, ...]:
    value = config.get(key)
    if not isinstance(value, list) or not value:
        raise ContractValidationError("config.{0} must be a non-empty list".format(key))
    return tuple(value)


def _extra_args(config: Mapping[str, Any]) -> Dict[str, Any]:
    raw = config.get("extra_args", [])
    if raw is None:
        return {}
    if not isinstance(raw, list):
        raise ContractValidationError("config.extra_args must be a list")
    values: Dict[str, Any] = {}
    index = 0
    while index < len(raw):
        token = str(raw[index])
        if not token.startswith("--") or len(token) <= 2:
            raise ContractValidationError(
                "config.extra_args item {0} is not an option".format(index)
            )
        key = token[2:].replace("-", "_")
        if index + 1 < len(raw) and not str(raw[index + 1]).startswith("--"):
            values[key] = raw[index + 1]
            index += 2
        else:
            values[key] = True
            index += 1
    return values


def _config_arg(
    config: Mapping[str, Any], extra: Mapping[str, Any], names: Sequence[str], default: Any
) -> Any:
    defaults = config.get("defaults") or {}
    if not isinstance(defaults, Mapping):
        raise ContractValidationError("config.defaults must be an object")
    for name in names:
        if name in extra:
            return extra[name]
    for name in names:
        if name in defaults:
            return defaults[name]
    return default


def _as_bool(value: Any, label: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("1", "true", "yes", "on"):
            return True
        if normalized in ("0", "false", "no", "off"):
            return False
    if isinstance(value, int) and value in (0, 1):
        return bool(value)
    raise ContractValidationError("{0} must be boolean".format(label))


@dataclass(frozen=True)
class SelectionRequest:
    config_path: Path
    config_name: str
    dataset: str
    base_model: str
    ratio: float
    methods: Tuple[str, ...]
    strategies: Tuple[str, ...]
    seeds: Tuple[int, ...]
    split_seed: int
    train_ratio: float
    val_ratio: float
    test_ratio: float
    im_parameters: ImParameters


def load_selection_request(config_path: Any, split_seed: Optional[int] = None) -> SelectionRequest:
    path = Path(config_path).expanduser().resolve(strict=True)
    try:
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ContractValidationError("config could not be read: {0}".format(exc))
    if not isinstance(config, Mapping):
        raise ContractValidationError("config root must be an object")
    for key in ("dataset", "base_model", "ratio"):
        if key not in config:
            raise ContractValidationError("config is missing {0}".format(key))
    methods = tuple(str(value) for value in _require_list(config, "methods"))
    strategies = tuple(str(value).strip().lower() for value in _require_list(config, "strategies"))
    try:
        seeds = tuple(int(value) for value in _require_list(config, "seeds"))
    except (TypeError, ValueError):
        raise ContractValidationError("config.seeds must contain integers")
    ratio = float(config["ratio"])
    if not 0.0 < ratio <= 1.0:
        raise ContractValidationError("config.ratio must be in (0, 1]")
    extra = _extra_args(config)
    is_transductive = _as_bool(
        _config_arg(config, extra, ("is_transductive",), True), "is_transductive"
    )
    is_balanced = _as_bool(
        _config_arg(config, extra, ("is_balanced",), False), "is_balanced"
    )
    if not is_transductive or is_balanced:
        raise ContractValidationError(
            "Selection materializer currently supports only transductive unbalanced splits"
        )
    train_ratio = float(_config_arg(config, extra, ("train_ratio",), 0.8))
    val_ratio = float(_config_arg(config, extra, ("val_ratio",), 0.0))
    test_ratio = float(_config_arg(config, extra, ("test_ratio",), 0.2))
    if not math.isclose(train_ratio + val_ratio + test_ratio, 1.0, abs_tol=1e-9):
        raise ContractValidationError("train/val/test ratios must sum to 1")
    chosen_split_seed = seeds[0] if split_seed is None else int(split_seed)
    parameters = ImParameters(
        propagation_prob=float(
            _config_arg(config, extra, ("propagation_prob",), 0.1)
        ),
        mc_rounds=int(_config_arg(config, extra, ("mc_rounds",), 100)),
        candidate_fraction=float(
            _config_arg(config, extra, ("candidate_fraction",), 1.0)
        ),
        im_selector_seed=int(
            _config_arg(config, extra, ("im_selector_seed",), 2024)
        ),
        im_batch_size=int(
            _config_arg(config, extra, ("im_batch_size", "im_v4_batch_size"), 5)
        ),
        parallel_mc=_as_bool(
            _config_arg(config, extra, ("im_parallel_mc",), True),
            "im_parallel_mc",
        ),
    )
    return SelectionRequest(
        config_path=path,
        config_name=str(config.get("name") or path.stem),
        dataset=str(config["dataset"]),
        base_model=str(config["base_model"]),
        ratio=ratio,
        methods=methods,
        strategies=strategies,
        seeds=seeds,
        split_seed=chosen_split_seed,
        train_ratio=train_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        im_parameters=parameters,
    )


@dataclass(frozen=True)
class PreparedSelectionJob:
    strategy: str
    recipe: ArtifactRecipe
    inputs: SelectionInputs
    producer: Callable[[], Sequence[int]]
    producer_version: ProducerVersion
    parameters: ImParameters
    k: int
    execution_backend: str
    algorithm_version: str
    consumer_requests: int
    request_envelope: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "artifact_type": ArtifactType.SELECTION.value,
            "strategy": self.strategy,
            "recipe_hash": self.recipe.recipe_hash,
            "recipe": self.recipe.to_dict(),
            "k": self.k,
            "num_nodes": self.inputs.num_nodes,
            "candidate_count": len(self.inputs.candidate_nodes),
            "graph_fingerprint": self.inputs.graph_fingerprint,
            "candidate_set_hash": self.inputs.candidate_set_hash,
            "legacy_graph_fingerprint": self.inputs.legacy_graph_fingerprint,
            "execution_backend": self.execution_backend,
            "algorithm_version": self.algorithm_version,
            "producer_version": self.producer_version.to_dict(),
            "consumer_requests": self.consumer_requests,
            "request_envelope": dict(self.request_envelope),
        }


@dataclass(frozen=True)
class PreparedSelectionPlan:
    request: SelectionRequest
    jobs: Tuple[PreparedSelectionJob, ...]
    skipped: Tuple[Mapping[str, Any], ...]

    def to_dict(self) -> Dict[str, Any]:
        total_requests = (
            len(self.request.methods)
            * len(self.request.strategies)
            * len(self.request.seeds)
        )
        supported = sum(job.consumer_requests for job in self.jobs)
        return {
            "config_path": str(self.request.config_path),
            "config_name": self.request.config_name,
            "dataset": self.request.dataset,
            "base_model_request_label": self.request.base_model,
            "ratio": self.request.ratio,
            "methods": list(self.request.methods),
            "strategies": list(self.request.strategies),
            "seeds": list(self.request.seeds),
            "split_seed": self.request.split_seed,
            "split": {
                "kind": "opengu-transductive-randperm-v1",
                "train_ratio": self.request.train_ratio,
                "val_ratio": self.request.val_ratio,
                "test_ratio": self.request.test_ratio,
            },
            "total_consumer_requests": total_requests,
            "supported_consumer_requests": supported,
            "skipped_consumer_requests": total_requests - supported,
            "unique_artifact_recipes": len(self.jobs),
            "deduplicated_requests": max(0, supported - len(self.jobs)),
            "registered_producers": sorted(PRODUCER_REGISTRY),
            "jobs": [job.to_dict() for job in self.jobs],
            "skipped": [dict(item) for item in self.skipped],
        }


ProducerBuilder = Callable[
    [SelectionRequest, SelectionInputs, Type[Any], bool, Path], PreparedSelectionJob
]


def _prepare_im_job(
    request: SelectionRequest,
    inputs: SelectionInputs,
    strategy_class: Type[Any],
    has_numba: bool,
    strategy_source: Path,
) -> PreparedSelectionJob:
    k = max(1, int(len(inputs.candidate_nodes) * request.ratio))
    recipe = build_im_recipe(inputs, k, request.im_parameters, has_numba)
    producer = build_im_producer(inputs, k, request.im_parameters, strategy_class)
    producer_version = ProducerVersion(
        semantic_version=IM_PRODUCER_SEMANTIC_VERSION,
        source_fingerprint=producer_source_fingerprint(strategy_source),
    )
    consumer_requests = (
        len(request.methods)
        * len(request.seeds)
        * sum(1 for name in request.strategies if name == "im")
    )
    envelope = {
        "config_name": request.config_name,
        "yaml_path": str(request.config_path),
        "dataset_request": request.dataset,
        "base_model_request": request.base_model,
        "method_requests": list(request.methods),
        "experiment_seeds": list(request.seeds),
        "selection_ratio": request.ratio,
        "split_seed": request.split_seed,
    }
    return PreparedSelectionJob(
        strategy="im",
        recipe=recipe,
        inputs=inputs,
        producer=producer,
        producer_version=producer_version,
        parameters=request.im_parameters,
        k=k,
        execution_backend=implementation_backend(
            has_numba, request.im_parameters.parallel_mc
        ),
        algorithm_version=im_algorithm_version(has_numba),
        consumer_requests=consumer_requests,
        request_envelope=envelope,
    )


PRODUCER_REGISTRY: Dict[str, ProducerBuilder] = {"im": _prepare_im_job}


def prepare_selection_plan(
    config_path: Any,
    dataset_root: Any,
    legacy_results_root: Any,
    *,
    allow_download: bool = False,
    split_seed: Optional[int] = None,
) -> PreparedSelectionPlan:
    request = load_selection_request(config_path, split_seed=split_seed)
    legacy_root = validate_legacy_results_root(legacy_results_root)
    legacy_roots = legacy_cache_roots(legacy_root)
    root = validate_dataset_root(
        dataset_root, request.dataset, allow_download, legacy_roots
    )
    unique_strategies = tuple(dict.fromkeys(request.strategies))
    skipped: List[Mapping[str, Any]] = []
    supported = [name for name in unique_strategies if name in PRODUCER_REGISTRY]
    for strategy in unique_strategies:
        if strategy in PRODUCER_REGISTRY:
            continue
        skipped.append(
            {
                "strategy": strategy,
                "reason": "producer_not_registered",
                "future_registry_extension": strategy in FUTURE_PRODUCERS,
                "consumer_requests": (
                    len(request.methods)
                    * len(request.seeds)
                    * sum(1 for name in request.strategies if name == strategy)
                ),
            }
        )
    if not supported:
        return PreparedSelectionPlan(request=request, jobs=(), skipped=tuple(skipped))
    with redirect_stdout(sys.stderr):
        inputs = load_selection_inputs(
            request.dataset, root, request.split_seed, request.train_ratio
        )
        strategy_class, has_numba, source = load_im_strategy()
    jobs: List[PreparedSelectionJob] = []
    for strategy in supported:
        jobs.append(
            PRODUCER_REGISTRY[strategy](
                request, inputs, strategy_class, has_numba, source
            )
        )
    recipe_hashes = [job.recipe.recipe_hash for job in jobs]
    if len(recipe_hashes) != len(set(recipe_hashes)):
        raise ContractValidationError("prepared Selection Recipes are not unique")
    return PreparedSelectionPlan(request=request, jobs=tuple(jobs), skipped=tuple(skipped))


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


def _tree_metadata_snapshot(root: Path) -> Dict[str, Any]:
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
            }
        )
    return {"exists": True, "files": files}


def _snapshot_hash(snapshot: Mapping[str, Any]) -> str:
    return sha256_bytes(_plain_json_bytes(snapshot))


def legacy_cache_state(roots: Sequence[Path]) -> Tuple[str, Dict[str, int]]:
    state: Dict[str, Any] = {}
    counts: Dict[str, int] = {}
    for root in roots:
        snapshot = _tree_snapshot(root)
        state[root.name] = snapshot
        counts[root.name] = len(snapshot["files"])
    return sha256_bytes(_plain_json_bytes(state)), counts


def _changed_store_paths(
    before: Mapping[str, Any], after: Mapping[str, Any]
) -> List[str]:
    before_map = {item["path"]: item for item in before.get("files", [])}
    after_map = {item["path"]: item for item in after.get("files", [])}
    return sorted(
        path
        for path in set(before_map).union(after_map)
        if before_map.get(path) != after_map.get(path)
    )


def explain_plan_exact(plan: PreparedSelectionPlan, store_root: Path) -> List[Dict[str, Any]]:
    index_path = store_root / "index.sqlite"
    if not index_path.is_file():
        return [
            {
                "strategy": job.strategy,
                "recipe_hash": job.recipe.recipe_hash,
                "hit": False,
                "miss_reasons": ["store_not_initialized"],
            }
            for job in plan.jobs
        ]
    index = CacheIndex(index_path)
    index.check_schema()
    resolver = ArtifactResolver(index)
    return [
        dict(
            {"strategy": job.strategy},
            **resolver.explain_exact(ArtifactType.SELECTION, job.recipe).to_dict()
        )
        for job in plan.jobs
    ]


def compare_legacy_selection(
    job: PreparedSelectionJob,
    request: SelectionRequest,
    selected_nodes: Sequence[int],
    legacy_results_root: Path,
) -> Dict[str, Any]:
    expected_param_fingerprint = _legacy_im_parameter_fingerprint(job.parameters)
    matches: List[Dict[str, Any]] = []
    anomalies: List[Dict[str, str]] = []
    selection_root = legacy_results_root / "selection_cache"
    for path in sorted(selection_root.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            config = payload.get("config")
            result = payload.get("selection_result")
            if not isinstance(config, Mapping) or not isinstance(result, Mapping):
                continue
            if str(config.get("strategy_name", "")).lower() != job.strategy:
                continue
            if str(config.get("dataset_name", "")) != request.dataset:
                continue
            if str(config.get("base_model", "")) != request.base_model:
                continue
            try:
                ratio_matches = math.isclose(
                    float(config.get("unlearn_ratio")), request.ratio, abs_tol=1e-12
                )
                identity_matches = (
                    ratio_matches
                    and int(config.get("seed")) == job.parameters.im_selector_seed
                    and int(config.get("k")) == job.k
                    and str(config.get("graph_fingerprint"))
                    == job.inputs.legacy_graph_fingerprint
                    and str(config.get("strategy_params_fingerprint"))
                    == expected_param_fingerprint
                )
            except (TypeError, ValueError):
                identity_matches = False
            if not identity_matches:
                continue
            raw_nodes = result.get("selected_nodes")
            if not isinstance(raw_nodes, list):
                anomalies.append(
                    {"path": str(path.resolve()), "reason": "selected_nodes_missing"}
                )
                continue
            nodes = canonical_candidate_nodes(raw_nodes, job.inputs.num_nodes)
            if len(nodes) != job.k:
                anomalies.append(
                    {"path": str(path.resolve()), "reason": "selected_node_count_mismatch"}
                )
                continue
            ordered = tuple(int(node) for node in raw_nodes)
            if set(ordered).difference(job.inputs.candidate_nodes):
                anomalies.append(
                    {"path": str(path.resolve()), "reason": "node_outside_candidate_set"}
                )
                continue
            matches.append(
                {
                    "path": str(path.resolve()),
                    "cache_key": payload.get("cache_key"),
                    "selected_nodes": ordered,
                    "ordered_nodes_hash": _ordered_nodes_hash(ordered),
                }
            )
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
            anomalies.append(
                {"path": str(path.resolve()), "reason": type(exc).__name__}
            )
    v2_nodes = tuple(int(node) for node in selected_nodes)
    v2_ordered_hash = _ordered_nodes_hash(v2_nodes)
    if not matches:
        status = "missing"
        exact = False
        set_match = False
    else:
        unique_hashes = {item["ordered_nodes_hash"] for item in matches}
        if len(unique_hashes) > 1:
            status = "ambiguous_conflict"
            exact = False
            set_match = False
        else:
            legacy_nodes = matches[0]["selected_nodes"]
            exact = legacy_nodes == v2_nodes
            set_match = set(legacy_nodes) == set(v2_nodes)
            status = (
                "exact_order_match"
                if exact
                else "set_match_order_diff"
                if set_match
                else "content_mismatch"
            )
    return {
        "status": status,
        "authoritative": False,
        "used_for_resolution": False,
        "same_selector_seed": job.parameters.im_selector_seed,
        "expected_legacy_graph_fingerprint": job.inputs.legacy_graph_fingerprint,
        "expected_legacy_parameter_fingerprint": expected_param_fingerprint,
        "v2_ordered_nodes_hash": v2_ordered_hash,
        "exact_order_match": exact,
        "set_match": set_match,
        "matching_sources": [
            {key: value for key, value in item.items() if key != "selected_nodes"}
            for item in matches
        ],
        "anomalies": anomalies,
    }


def _store_result_document(
    job: PreparedSelectionJob,
    result: StoreResult,
    store_root: Path,
    elapsed_seconds: float,
    include_nodes: bool,
) -> Dict[str, Any]:
    payload_path = store_root.joinpath(*PurePosixPath(result.semantic_path).parts)
    stat = payload_path.stat()
    document: Dict[str, Any] = {
        "strategy": job.strategy,
        "lookup": "exact-only",
        "hit": result.hit,
        "outcome": result.outcome,
        "producer_called": result.producer_called,
        "artifact_id": result.artifact_id,
        "recipe_hash": job.recipe.recipe_hash,
        "content_hash": result.content_hash,
        "semantic_path": result.semantic_path,
        "payload_path": str(payload_path),
        "payload_sha256": _sha256_file(payload_path),
        "payload_mtime_ns": stat.st_mtime_ns,
        "payload_size_bytes": stat.st_size,
        "selected_node_count": len(result.payload.selected_nodes_ordered),
        "ordered_nodes_hash": result.payload.ordered_nodes_hash,
        "node_set_hash": result.payload.node_set_hash,
        "resolve_seconds": elapsed_seconds,
        "miss_reasons": list(result.miss_reasons),
    }
    if include_nodes:
        document["selected_nodes"] = list(result.payload.selected_nodes_ordered)
    return document


def plan_selection(
    config_path: Any,
    dataset_root: Any,
    store_root: Any,
    legacy_results_root: Any,
    *,
    allow_download: bool = False,
    split_seed: Optional[int] = None,
) -> Dict[str, Any]:
    legacy_root = validate_legacy_results_root(legacy_results_root)
    legacy_roots = legacy_cache_roots(legacy_root)
    target_root = validate_store_root(store_root, legacy_roots)
    request_preview = load_selection_request(config_path, split_seed=split_seed)
    dataset_path = validate_dataset_root(
        dataset_root,
        request_preview.dataset,
        allow_download,
        legacy_roots,
    )
    dataset_storage = _dataset_storage_root(dataset_path, request_preview.dataset)
    dataset_before = _tree_metadata_snapshot(dataset_storage)
    legacy_before, legacy_counts = legacy_cache_state(legacy_roots)
    store_before = _tree_snapshot(target_root)
    plan = prepare_selection_plan(
        config_path,
        dataset_root,
        legacy_root,
        allow_download=allow_download,
        split_seed=split_seed,
    )
    explanations = explain_plan_exact(plan, target_root)
    store_after = _tree_snapshot(target_root)
    dataset_after = _tree_metadata_snapshot(dataset_storage)
    legacy_after, _ = legacy_cache_state(legacy_roots)
    if store_after != store_before:
        raise CacheV2Error("selection plan modified the ArtifactStore")
    if legacy_after != legacy_before:
        raise LegacySourceChangedError("selection plan modified a Legacy cache")
    if not allow_download and dataset_after != dataset_before:
        raise CacheV2Error("selection plan modified the dataset tree")
    return {
        "ok": True,
        "mode": "plan",
        "lookup": "exact-only",
        "plan": plan.to_dict(),
        "resolutions": explanations,
        "execution_performed": False,
        "producer_calls": 0,
        "writes": [],
        "writes_scope": "artifact_store_only",
        "store_root": str(target_root),
        "store_unchanged": True,
        "dataset_unchanged": dataset_after == dataset_before,
        "legacy_cache_unchanged": True,
        "legacy_cache_state_hash_before": legacy_before,
        "legacy_cache_state_hash_after": legacy_after,
        "legacy_cache_file_counts": legacy_counts,
        "dataset_download_allowed": bool(allow_download),
    }


def materialize_selection(
    config_path: Any,
    dataset_root: Any,
    store_root: Any,
    legacy_results_root: Any,
    *,
    allow_download: bool = False,
    split_seed: Optional[int] = None,
    verify: bool = False,
    fail_if_producer_called: bool = False,
    compare_legacy: bool = False,
    include_nodes: bool = False,
) -> Dict[str, Any]:
    total_started = time.perf_counter()
    legacy_root = validate_legacy_results_root(legacy_results_root)
    legacy_roots = legacy_cache_roots(legacy_root)
    target_root = validate_store_root(store_root, legacy_roots)
    request_preview = load_selection_request(config_path, split_seed=split_seed)
    dataset_path = validate_dataset_root(
        dataset_root,
        request_preview.dataset,
        allow_download,
        legacy_roots,
    )
    dataset_storage = _dataset_storage_root(dataset_path, request_preview.dataset)
    dataset_before = _tree_metadata_snapshot(dataset_storage)
    legacy_before, legacy_counts = legacy_cache_state(legacy_roots)
    store_before = _tree_snapshot(target_root)
    plan = prepare_selection_plan(
        config_path,
        dataset_root,
        legacy_root,
        allow_download=allow_download,
        split_seed=split_seed,
    )
    results: List[Dict[str, Any]] = []
    for job in plan.jobs:
        store = ArtifactStore(target_root, producer_version=job.producer_version)
        if not store.index.database_path.is_file():
            if fail_if_producer_called:
                raise CacheResolutionError(
                    "fail-if-producer-called requires an initialized exact store"
                )
            store.initialize()
        else:
            store.index.check_schema()
        started = time.perf_counter()
        with redirect_stdout(sys.stderr):
            result = store.get_or_compute(
                job.recipe,
                job.producer,
                num_nodes=job.inputs.num_nodes,
                candidate_nodes=job.inputs.candidate_nodes,
                request_envelope=job.request_envelope,
                fail_if_called=fail_if_producer_called,
            )
        elapsed = time.perf_counter() - started
        document = _store_result_document(
            job, result, target_root, elapsed, include_nodes
        )
        if verify:
            payload_path = Path(document["payload_path"])
            mtime_before = payload_path.stat().st_mtime_ns
            verification_store = ArtifactStore(
                target_root, producer_version=job.producer_version
            )
            with redirect_stdout(sys.stderr):
                verified = verification_store.get_or_compute(
                    job.recipe,
                    job.producer,
                    num_nodes=job.inputs.num_nodes,
                    candidate_nodes=job.inputs.candidate_nodes,
                    request_envelope={"verification_of": result.artifact_id},
                    fail_if_called=True,
                )
            mtime_after = payload_path.stat().st_mtime_ns
            verification_ok = (
                verified.hit
                and not verified.producer_called
                and verified.artifact_id == result.artifact_id
                and verified.content_hash == result.content_hash
                and verified.payload.selected_nodes_ordered
                == result.payload.selected_nodes_ordered
                and mtime_after == mtime_before
            )
            if not verification_ok:
                raise CacheResolutionError("independent warm verification failed")
            document["verification"] = {
                "ok": True,
                "hit": verified.hit,
                "producer_called": verified.producer_called,
                "artifact_id": verified.artifact_id,
                "content_hash": verified.content_hash,
                "selected_nodes_equal": True,
                "payload_mtime_unchanged": True,
                "payload_mtime_ns_before": mtime_before,
                "payload_mtime_ns_after": mtime_after,
            }
        if compare_legacy:
            document["legacy_comparison"] = compare_legacy_selection(
                job,
                plan.request,
                result.payload.selected_nodes_ordered,
                legacy_root,
            )
        results.append(document)
    legacy_after, _ = legacy_cache_state(legacy_roots)
    if legacy_after != legacy_before:
        raise LegacySourceChangedError("Selection materialization modified a Legacy cache")
    dataset_after = _tree_metadata_snapshot(dataset_storage)
    if not allow_download and dataset_after != dataset_before:
        raise CacheV2Error("Selection materialization modified the dataset tree")
    store_after = _tree_snapshot(target_root)
    changed = _changed_store_paths(store_before, store_after)
    return {
        "ok": True,
        "mode": "materialize",
        "lookup": "exact-only",
        "plan": plan.to_dict(),
        "results": results,
        "store_root": str(target_root),
        "writes": changed,
        "write_scope": "artifact_store_only",
        "dataset_unchanged": dataset_after == dataset_before,
        "legacy_cache_unchanged": True,
        "legacy_cache_state_hash_before": legacy_before,
        "legacy_cache_state_hash_after": legacy_after,
        "legacy_cache_file_counts": legacy_counts,
        "dataset_download_allowed": bool(allow_download),
        "verify_requested": bool(verify),
        "fail_if_producer_called": bool(fail_if_producer_called),
        "compare_legacy": bool(compare_legacy),
        "elapsed_seconds": time.perf_counter() - total_started,
    }
