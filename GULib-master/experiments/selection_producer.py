"""OpenGU experiment-owned Selection input preparation and production.

The cache boundary is resolve/store only.  This module loads canonical OpenGU
processed inputs, imports Selection strategies, calls selectors on a clean
miss, validates their nodes against the persisted candidate set, and then asks
Cache V2 to materialize the explicit result.
"""

from __future__ import annotations

import hashlib
import json
import math
import operator
import sys
import time
from collections.abc import Mapping
from contextlib import contextmanager, redirect_stdout
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Type, Union

import torch
import yaml
from torch_geometric.data import Data

from cache_v2.canonical import sha256_bytes
from cache_v2.contracts import ArtifactRecipe, ArtifactType, ProducerVersion
from cache_v2.errors import (
    CacheV2Error,
    ContractValidationError,
    LegacySourceChangedError,
    PathValidationError,
)
from cache_v2.selection_materializer import (
    SelectionArtifactRequest,
    build_selection_recipe,
    resolve_selection_artifact,
    store_selection_artifact,
)
from cache_v2.store import StoreResult
from experiments.selection_inputs import (
    DatasetSelectionInputs,
    load_processed_selection_inputs,
)


IM_NUMBA_ALGORITHM_VERSION = "opengu-im-batch-celf-numba-v1"
IM_PYTHON_ALGORITHM_VERSION = "opengu-im-classic-celf-python-v1"
IM_PRODUCER_SEMANTIC_VERSION = "opengu-im-selection-v2"
RANDOM_ALGORITHM_VERSION = "opengu-random-torch-randperm-v1"
DEGREE_ALGORITHM_VERSION = "opengu-degree-torch-topk-v1"
PAGERANK_ALGORITHM_VERSION = "opengu-pagerank-undirected-networkx-topk-v1"
RANDOM_PRODUCER_SEMANTIC_VERSION = "opengu-random-selection-v2"
DEGREE_PRODUCER_SEMANTIC_VERSION = "opengu-degree-selection-v4"
PAGERANK_PRODUCER_SEMANTIC_VERSION = "opengu-pagerank-selection-v2"
FUTURE_PRODUCERS = frozenset(("tracin", "hybrid"))


class UpstreamProducerCalledError(CacheV2Error):
    """The experiment-layer fail-if-called producer sentinel was reached."""


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


def _path_is_within(path: Path, root: Path) -> bool:
    try:
        Path(path).resolve(strict=False).relative_to(Path(root).resolve(strict=False))
        return True
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


@dataclass(frozen=True)
class SelectionRequest:
    config_path: Optional[Path]
    config_name: str
    dataset: str
    base_model: str
    ratio: float
    methods: Tuple[str, ...]
    strategies: Tuple[str, ...]
    seeds: Tuple[int, ...]
    train_ratio: float
    val_ratio: float
    test_ratio: float
    is_transductive: bool
    is_balanced: bool
    pagerank_alpha: float
    im_parameters: ImParameters


@dataclass(frozen=True)
class SelectionInputs:
    """Normalized producer input, including all Selection identity fields."""

    dataset: DatasetSelectionInputs
    strategy: str
    seed: int
    k: int
    producer_version: ProducerVersion
    algorithm_version: str
    parameters: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.dataset, DatasetSelectionInputs):
            raise ContractValidationError("dataset must be DatasetSelectionInputs")
        strategy = str(self.strategy).strip().lower()
        if not strategy or "\x00" in strategy:
            raise ContractValidationError("strategy must be a non-empty string")
        if isinstance(self.seed, bool) or not isinstance(self.seed, int):
            raise ContractValidationError("seed must be an integer")
        if isinstance(self.k, bool) or not isinstance(self.k, int) or self.k <= 0:
            raise ContractValidationError("k must be a positive integer")
        if self.k > self.dataset.candidate_count:
            raise ContractValidationError("k exceeds candidate_count")
        if not isinstance(self.producer_version, ProducerVersion):
            raise ContractValidationError("producer_version must be ProducerVersion")
        if not self.producer_version.is_identified:
            raise ContractValidationError("producer_version must identify its producer")
        if not isinstance(self.parameters, Mapping):
            raise ContractValidationError("parameters must be a mapping")
        if not str(self.algorithm_version).strip():
            raise ContractValidationError("algorithm_version must be a non-empty string")
        object.__setattr__(self, "strategy", strategy)
        object.__setattr__(self, "parameters", dict(self.parameters))

    @property
    def edge_index(self) -> torch.Tensor:
        return self.dataset.edge_index

    @property
    def num_nodes(self) -> int:
        return self.dataset.num_nodes

    @property
    def candidate_nodes(self) -> Tuple[int, ...]:
        return self.dataset.candidate_nodes


@dataclass(frozen=True)
class PreparedSelectionJob:
    inputs: SelectionInputs
    recipe: ArtifactRecipe
    producer: Callable[[], Sequence[int]]
    consumer_requests: int = 1
    request_envelope: Mapping[str, Any] = None
    legacy_seed: int = 0
    legacy_strategy_parameters: Mapping[str, Any] = None
    execution_backend: str = "cpu"

    def __post_init__(self) -> None:
        if not callable(self.producer):
            raise ContractValidationError("producer must be callable")
        object.__setattr__(
            self,
            "request_envelope",
            dict(self.request_envelope or {}),
        )
        object.__setattr__(
            self,
            "legacy_strategy_parameters",
            dict(self.legacy_strategy_parameters or {}),
        )

    @property
    def strategy(self) -> str:
        return self.inputs.strategy

    @property
    def producer_version(self) -> ProducerVersion:
        return self.inputs.producer_version

    @property
    def k(self) -> int:
        return self.inputs.k

    def to_dict(self) -> Dict[str, Any]:
        dataset = self.inputs.dataset
        return {
            "artifact_type": ArtifactType.SELECTION.value,
            "strategy": self.strategy,
            "recipe_hash": self.recipe.recipe_hash,
            "recipe": self.recipe.to_dict(),
            "k": self.k,
            "selector_seed": self.inputs.seed,
            "num_nodes": dataset.num_nodes,
            "candidate_count": dataset.candidate_count,
            "dataset_fingerprint": dataset.dataset_fingerprint,
            "graph_fingerprint": dataset.graph_fingerprint,
            "candidate_set_hash": dataset.candidate_set_hash,
            "legacy_graph_fingerprint": dataset.legacy_graph_fingerprint,
            "execution_backend": self.execution_backend,
            "algorithm_version": self.inputs.algorithm_version,
            "parameters": dict(self.inputs.parameters),
            "producer_version": self.producer_version.to_dict(),
            "consumer_requests": self.consumer_requests,
            "request_envelope": dict(self.request_envelope),
        }


@dataclass(frozen=True)
class PreparedSelectionPlan:
    request: SelectionRequest
    dataset_inputs: Optional[DatasetSelectionInputs]
    jobs: Tuple[PreparedSelectionJob, ...]
    skipped: Tuple[Mapping[str, Any], ...]

    def to_dict(self) -> Dict[str, Any]:
        total_requests = (
            len(self.request.methods)
            * len(self.request.strategies)
            * len(self.request.seeds)
        )
        supported = sum(job.consumer_requests for job in self.jobs)
        source = self.dataset_inputs.source_path if self.dataset_inputs else None
        return {
            "config_path": str(self.request.config_path) if self.request.config_path else None,
            "config_name": self.request.config_name,
            "dataset": self.request.dataset,
            "processed_data_source": str(source) if source else None,
            "dataset_provider": "opengu-canonical-processed-pickle-v1",
            "split_reconstructed": False,
            "base_model_request_label": self.request.base_model,
            "ratio": self.request.ratio,
            "methods": list(self.request.methods),
            "strategies": list(self.request.strategies),
            "seeds": list(self.request.seeds),
            "split": {
                "source": "persisted-processed-masks",
                "is_transductive": self.request.is_transductive,
                "is_balanced": self.request.is_balanced,
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


@dataclass(frozen=True)
class MaterializedSelection:
    hit: bool
    producer_called: bool
    result: StoreResult
    producer_seconds: float

    @property
    def artifact_id(self) -> str:
        return self.result.artifact_id

    @property
    def content_hash(self) -> str:
        return self.result.content_hash


def build_selection_job(
    inputs: SelectionInputs,
    producer: Callable[[], Sequence[int]],
    *,
    consumer_requests: int = 1,
    request_envelope: Optional[Mapping[str, Any]] = None,
    legacy_seed: Optional[int] = None,
    legacy_strategy_parameters: Optional[Mapping[str, Any]] = None,
    execution_backend: str = "cpu",
) -> PreparedSelectionJob:
    if not isinstance(inputs, SelectionInputs):
        raise ContractValidationError("inputs must be SelectionInputs")
    dataset = inputs.dataset
    recipe = build_selection_recipe(
        dataset_fingerprint=dataset.dataset_fingerprint,
        graph_fingerprint=dataset.graph_fingerprint,
        candidate_set_hash=dataset.candidate_set_hash,
        num_nodes=dataset.num_nodes,
        candidate_count=dataset.candidate_count,
        node_id_space=dataset.node_id_space,
        strategy=inputs.strategy,
        seed=inputs.seed,
        k=inputs.k,
        producer_version=inputs.producer_version,
        algorithm_version=inputs.algorithm_version,
        parameters=inputs.parameters,
    )
    return PreparedSelectionJob(
        inputs=inputs,
        recipe=recipe,
        producer=producer,
        consumer_requests=consumer_requests,
        request_envelope=request_envelope or {},
        legacy_seed=inputs.seed if legacy_seed is None else legacy_seed,
        legacy_strategy_parameters=legacy_strategy_parameters or inputs.parameters,
        execution_backend=execution_backend,
    )


def _validated_selected_nodes(
    job: PreparedSelectionJob, selected_nodes: Sequence[int]
) -> Tuple[int, ...]:
    values = []
    for position, node in enumerate(selected_nodes):
        if isinstance(node, bool):
            raise ContractValidationError(
                "selected node at position {0} must be an integer".format(position)
            )
        try:
            value = operator.index(node)
        except (TypeError, ValueError, OverflowError):
            raise ContractValidationError(
                "selected node at position {0} must be an integer".format(position)
            )
        values.append(int(value))
    nodes = tuple(values)
    if len(nodes) != job.k:
        raise ContractValidationError("producer selected-node count does not match k")
    if len(nodes) != len(set(nodes)):
        raise ContractValidationError("producer selected nodes contain duplicates")
    candidate_set = set(job.inputs.candidate_nodes)
    outside = [node for node in nodes if node not in candidate_set]
    if outside:
        raise ContractValidationError(
            "producer selected nodes outside persisted candidate set: {0}".format(outside)
        )
    return nodes


def resolve_or_produce_selection(
    job: PreparedSelectionJob,
    store_root: Union[str, Path],
    *,
    fail_if_producer_called: bool = False,
) -> MaterializedSelection:
    """Resolve first; only the experiment layer invokes the selector on miss."""

    request = SelectionArtifactRequest.from_recipe(
        job.recipe, job.producer_version
    )
    resolution = resolve_selection_artifact(store_root, request)
    if resolution.hit and resolution.result is not None:
        return MaterializedSelection(True, False, resolution.result, 0.0)
    if fail_if_producer_called:
        raise UpstreamProducerCalledError(
            "upstream producer fail-if-called sentinel reached for Recipe {0}".format(
                job.recipe.recipe_hash
            )
        )
    started = time.perf_counter()
    with redirect_stdout(sys.stderr):
        selected = job.producer()
    elapsed = time.perf_counter() - started
    nodes = _validated_selected_nodes(job, selected)
    result = store_selection_artifact(
        store_root,
        request,
        selected_nodes=nodes,
        compute_seconds=elapsed,
    )
    return MaterializedSelection(result.hit, True, result, elapsed)


def implementation_backend(has_numba: bool, parallel_mc: bool) -> str:
    if not has_numba:
        return "python"
    return "numba-parallel" if parallel_mc else "numba-serial"


def im_algorithm_version(has_numba: bool) -> str:
    return IM_NUMBA_ALGORITHM_VERSION if has_numba else IM_PYTHON_ALGORITHM_VERSION


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


def load_simple_strategy(strategy_name: str) -> Tuple[Type[Any], Path]:
    with _sanitized_framework_argv():
        if strategy_name == "random":
            from attack.attack_strategies.random_strategy import RandomStrategy

            strategy_class = RandomStrategy
        elif strategy_name == "degree":
            from attack.attack_strategies.degree_strategy import DegreeStrategy

            strategy_class = DegreeStrategy
        elif strategy_name == "pagerank":
            from attack.attack_strategies.pagerank_strategy import PageRankStrategy

            strategy_class = PageRankStrategy
        else:
            raise ContractValidationError(
                "no simple Selection producer is registered for {0}".format(strategy_name)
            )
    source = (
        Path(__file__).resolve().parents[1]
        / "attack"
        / "attack_strategies"
        / "{0}_strategy.py".format(strategy_name)
    )
    return strategy_class, source


def producer_source_fingerprint(
    strategy_source: Path, strategy_name: str
) -> str:
    digest = hashlib.sha256()
    sources = [
        (b"experiment-selection-producer\x00", Path(__file__)),
        ((strategy_name + "-strategy\x00").encode("utf-8"), strategy_source),
    ]
    if strategy_name in ("random", "degree", "pagerank"):
        sources.append(
            (
                b"base-strategy\x00",
                Path(__file__).resolve().parents[1]
                / "attack"
                / "attack_strategies"
                / "base_strategy.py",
            )
        )
    for label, path in sources:
        digest.update(label)
        digest.update(path.read_bytes())
    return digest.hexdigest()


def build_im_producer(
    dataset: DatasetSelectionInputs,
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
            dataset.edge_index,
            dataset.num_nodes,
            k,
            list(dataset.candidate_nodes),
        )
        return [int(node) for node in selected]

    return produce


def build_simple_producer(
    dataset: DatasetSelectionInputs,
    k: int,
    strategy_class: Type[Any],
    strategy_args: Mapping[str, Any],
    *,
    random_seed: Optional[int] = None,
) -> Callable[[], Sequence[int]]:
    strategy = strategy_class(dict(strategy_args))
    data = Data(
        edge_index=dataset.edge_index.clone(),
        num_nodes=dataset.num_nodes,
        train_indices=torch.tensor(dataset.candidate_nodes, dtype=torch.long),
    )
    model = torch.nn.Identity()

    def select() -> Sequence[int]:
        selected = strategy.select_nodes(data, model, k)
        return [int(node) for node in torch.as_tensor(selected).view(-1).tolist()]

    if random_seed is None:
        return select

    def produce_random() -> Sequence[int]:
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(random_seed)
            return select()

    return produce_random


def build_degree_producer(
    dataset: DatasetSelectionInputs,
    k: int,
    strategy_class: Optional[Type[Any]] = None,
) -> Callable[[], Sequence[int]]:
    if strategy_class is None:
        strategy_class, _ = load_simple_strategy("degree")
    return build_simple_producer(dataset, k, strategy_class, {})


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
    values = {}
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
    config: Mapping[str, Any],
    extra: Mapping[str, Any],
    names: Sequence[str],
    default: Any,
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


def load_selection_request(
    config_source: Union[str, Path, Mapping[str, Any]]
) -> SelectionRequest:
    if isinstance(config_source, Mapping):
        config = dict(config_source)
        source_value = config.get("_source_path")
        path = (
            Path(source_value).expanduser().resolve(strict=False)
            if source_value
            else None
        )
    else:
        path = Path(config_source).expanduser().resolve(strict=True)
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
    strategies = tuple(
        str(value).strip().lower() for value in _require_list(config, "strategies")
    )
    try:
        seeds = tuple(int(value) for value in _require_list(config, "seeds"))
    except (TypeError, ValueError) as exc:
        raise ContractValidationError("config.seeds must contain integers") from exc
    ratio = float(config["ratio"])
    if not 0.0 < ratio <= 1.0:
        raise ContractValidationError("config.ratio must be in (0, 1]")
    extra = _extra_args(config)
    train_ratio = float(_config_arg(config, extra, ("train_ratio",), 0.8))
    val_ratio = float(_config_arg(config, extra, ("val_ratio",), 0.0))
    test_ratio = float(_config_arg(config, extra, ("test_ratio",), 0.2))
    if not math.isclose(train_ratio + val_ratio + test_ratio, 1.0, abs_tol=1e-9):
        raise ContractValidationError("train/val/test ratios must sum to 1")
    pagerank_alpha = float(_config_arg(config, extra, ("pagerank_alpha",), 0.85))
    if not math.isfinite(pagerank_alpha) or not 0.0 <= pagerank_alpha <= 1.0:
        raise ContractValidationError("pagerank_alpha must be finite and in [0, 1]")
    parameters = ImParameters(
        propagation_prob=float(_config_arg(config, extra, ("propagation_prob",), 0.1)),
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
        config_name=str(config.get("name") or (path.stem if path else "inline")),
        dataset=str(config["dataset"]),
        base_model=str(config["base_model"]),
        ratio=ratio,
        methods=methods,
        strategies=strategies,
        seeds=seeds,
        train_ratio=train_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        is_transductive=_as_bool(
            _config_arg(config, extra, ("is_transductive",), True),
            "is_transductive",
        ),
        is_balanced=_as_bool(
            _config_arg(config, extra, ("is_balanced",), False),
            "is_balanced",
        ),
        pagerank_alpha=pagerank_alpha,
        im_parameters=parameters,
    )


def _request_envelope(
    request: SelectionRequest, experiment_seeds: Sequence[int]
) -> Dict[str, Any]:
    return {
        "config_name": request.config_name,
        "yaml_path": str(request.config_path) if request.config_path else None,
        "dataset_request": request.dataset,
        "base_model_request": request.base_model,
        "method_requests": list(request.methods),
        "experiment_seeds": [int(seed) for seed in experiment_seeds],
        "selection_ratio": request.ratio,
        "split_source": "persisted-processed-masks",
    }


def _selection_k(dataset: DatasetSelectionInputs, ratio: float) -> int:
    return max(1, int(dataset.candidate_count * ratio))


def _prepare_jobs_for_strategy(
    strategy: str,
    request: SelectionRequest,
    dataset: DatasetSelectionInputs,
) -> Tuple[PreparedSelectionJob, ...]:
    k = _selection_k(dataset, request.ratio)
    occurrences = sum(1 for name in request.strategies if name == strategy)
    if strategy == "im":
        strategy_class, has_numba, source = load_im_strategy()
        params = request.im_parameters.to_dict()
        inputs = SelectionInputs(
            dataset=dataset,
            strategy="im",
            seed=request.im_parameters.im_selector_seed,
            k=k,
            producer_version=ProducerVersion(
                semantic_version=IM_PRODUCER_SEMANTIC_VERSION,
                source_fingerprint=producer_source_fingerprint(source, "im"),
            ),
            algorithm_version=im_algorithm_version(has_numba),
            parameters=params,
        )
        return (
            build_selection_job(
                inputs,
                build_im_producer(dataset, k, request.im_parameters, strategy_class),
                consumer_requests=len(request.methods) * len(request.seeds) * occurrences,
                request_envelope=_request_envelope(request, request.seeds),
                legacy_seed=request.im_parameters.im_selector_seed,
                legacy_strategy_parameters={
                    "propagation_prob": request.im_parameters.propagation_prob,
                    "mc_rounds": request.im_parameters.mc_rounds,
                    "candidate_fraction": request.im_parameters.candidate_fraction,
                    "im_batch_size": request.im_parameters.im_batch_size,
                },
                execution_backend=implementation_backend(
                    has_numba, request.im_parameters.parallel_mc
                ),
            ),
        )
    strategy_class, source = load_simple_strategy(strategy)
    versions = {
        "random": (
            RANDOM_PRODUCER_SEMANTIC_VERSION,
            RANDOM_ALGORITHM_VERSION,
            "torch-cpu",
        ),
        "degree": (
            DEGREE_PRODUCER_SEMANTIC_VERSION,
            DEGREE_ALGORITHM_VERSION,
            "torch-cpu",
        ),
        "pagerank": (
            PAGERANK_PRODUCER_SEMANTIC_VERSION,
            PAGERANK_ALGORITHM_VERSION,
            "networkx-cpu",
        ),
    }
    semantic, algorithm, backend = versions[strategy]
    producer_version = ProducerVersion(
        semantic_version=semantic,
        source_fingerprint=producer_source_fingerprint(source, strategy),
    )
    if strategy == "random":
        jobs = []
        for seed in dict.fromkeys(request.seeds):
            seed_requests = sum(1 for value in request.seeds if value == seed)
            inputs = SelectionInputs(
                dataset=dataset,
                strategy=strategy,
                seed=seed,
                k=k,
                producer_version=producer_version,
                algorithm_version=algorithm,
                parameters={"seed": seed},
            )
            jobs.append(
                build_selection_job(
                    inputs,
                    build_simple_producer(
                        dataset, k, strategy_class, {}, random_seed=seed
                    ),
                    consumer_requests=len(request.methods) * occurrences * seed_requests,
                    request_envelope=_request_envelope(request, (seed,)),
                    legacy_seed=seed,
                    legacy_strategy_parameters={},
                    execution_backend=backend,
                )
            )
        return tuple(jobs)
    seed = 0
    parameters = (
        {"pagerank_alpha": request.pagerank_alpha}
        if strategy == "pagerank"
        else {}
    )
    inputs = SelectionInputs(
        dataset=dataset,
        strategy=strategy,
        seed=seed,
        k=k,
        producer_version=producer_version,
        algorithm_version=algorithm,
        parameters=parameters,
    )
    producer = (
        build_degree_producer(dataset, k, strategy_class)
        if strategy == "degree"
        else build_simple_producer(dataset, k, strategy_class, parameters)
    )
    return (
        build_selection_job(
            inputs,
            producer,
            consumer_requests=len(request.methods) * len(request.seeds) * occurrences,
            request_envelope=_request_envelope(request, request.seeds),
            legacy_seed=0,
            legacy_strategy_parameters=parameters,
            execution_backend=backend,
        ),
    )


PRODUCER_REGISTRY = {
    "random": _prepare_jobs_for_strategy,
    "degree": _prepare_jobs_for_strategy,
    "pagerank": _prepare_jobs_for_strategy,
    "im": _prepare_jobs_for_strategy,
}


def prepare_selection_plan(
    config_source: Union[str, Path, Mapping[str, Any]],
    processed_root: Union[str, Path],
    *,
    dataset_inputs: Optional[DatasetSelectionInputs] = None,
    input_provider: Callable[..., DatasetSelectionInputs] = load_processed_selection_inputs,
) -> PreparedSelectionPlan:
    request = load_selection_request(config_source)
    unique_strategies = tuple(dict.fromkeys(request.strategies))
    skipped = []
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
        return PreparedSelectionPlan(request, None, (), tuple(skipped))
    if dataset_inputs is None:
        dataset_inputs = input_provider(
            processed_root=processed_root,
            dataset_name=request.dataset,
            train_ratio=request.train_ratio,
            val_ratio=request.val_ratio,
            test_ratio=request.test_ratio,
            is_transductive=request.is_transductive,
            is_balanced=request.is_balanced,
        )
    if dataset_inputs.dataset_name != request.dataset:
        raise ContractValidationError(
            "SelectionInputs dataset does not match experiment request"
        )
    jobs = []
    for strategy in supported:
        with redirect_stdout(sys.stderr):
            jobs.extend(
                _prepare_jobs_for_strategy(strategy, request, dataset_inputs)
            )
    recipe_hashes = [job.recipe.recipe_hash for job in jobs]
    if len(recipe_hashes) != len(set(recipe_hashes)):
        raise ContractValidationError("prepared Selection Recipes are not unique")
    return PreparedSelectionPlan(
        request, dataset_inputs, tuple(jobs), tuple(skipped)
    )


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


def _stable_hash32(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_plain_json_bytes(dict(value))).hexdigest()[:32]


def compare_legacy_selection(
    job: PreparedSelectionJob,
    request: SelectionRequest,
    selected_nodes: Sequence[int],
    legacy_results_root: Path,
) -> Dict[str, Any]:
    expected_param_fingerprint = _stable_hash32(job.legacy_strategy_parameters)
    matches = []
    anomalies = []
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
            identity_matches = (
                math.isclose(
                    float(config.get("unlearn_ratio")), request.ratio, abs_tol=1e-12
                )
                and int(config.get("seed")) == job.legacy_seed
                and int(config.get("k")) == job.k
                and str(config.get("graph_fingerprint"))
                == job.inputs.dataset.legacy_graph_fingerprint
                and str(config.get("strategy_params_fingerprint"))
                == expected_param_fingerprint
            )
            if not identity_matches:
                continue
            raw_nodes = result.get("selected_nodes")
            if not isinstance(raw_nodes, list):
                anomalies.append(
                    {"path": str(path.resolve()), "reason": "selected_nodes_missing"}
                )
                continue
            ordered = tuple(int(node) for node in raw_nodes)
            if len(ordered) != job.k:
                anomalies.append(
                    {"path": str(path.resolve()), "reason": "selected_node_count_mismatch"}
                )
                continue
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
    if not matches:
        status, exact, set_match = "missing", False, False
    elif len({item["ordered_nodes_hash"] for item in matches}) > 1:
        status, exact, set_match = "ambiguous_conflict", False, False
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
        "expected_legacy_seed": job.legacy_seed,
        "expected_legacy_graph_fingerprint": job.inputs.dataset.legacy_graph_fingerprint,
        "expected_legacy_parameter_fingerprint": expected_param_fingerprint,
        "v2_ordered_nodes_hash": _ordered_nodes_hash(v2_nodes),
        "exact_order_match": exact,
        "set_match": set_match,
        "matching_sources": [
            {key: value for key, value in item.items() if key != "selected_nodes"}
            for item in matches
        ],
        "anomalies": anomalies,
    }


def _result_document(
    job: PreparedSelectionJob,
    materialized: MaterializedSelection,
    store_root: Path,
    include_nodes: bool,
) -> Dict[str, Any]:
    result = materialized.result
    payload_path = store_root.joinpath(*PurePosixPath(result.semantic_path).parts)
    stat = payload_path.stat()
    document = {
        "strategy": job.strategy,
        "lookup": "exact-only",
        "hit": materialized.hit,
        "outcome": result.outcome,
        "producer_called": materialized.producer_called,
        "producer_owner": "experiments.selection_producer",
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
        "producer_seconds": materialized.producer_seconds,
        "miss_reasons": list(result.miss_reasons),
    }
    if include_nodes:
        document["selected_nodes"] = list(result.payload.selected_nodes_ordered)
    return document


def plan_selection(
    config_source: Union[str, Path, Mapping[str, Any]],
    processed_root: Union[str, Path],
    store_root: Any,
    legacy_results_root: Any,
    *,
    dataset_inputs: Optional[DatasetSelectionInputs] = None,
) -> Dict[str, Any]:
    legacy_root = validate_legacy_results_root(legacy_results_root)
    legacy_roots = legacy_cache_roots(legacy_root)
    target_root = validate_store_root(store_root, legacy_roots)
    legacy_before, legacy_counts = legacy_cache_state(legacy_roots)
    store_before = _tree_snapshot(target_root)
    plan = prepare_selection_plan(
        config_source,
        processed_root,
        dataset_inputs=dataset_inputs,
    )
    resolutions = []
    for job in plan.jobs:
        resolution = resolve_selection_artifact(
            target_root,
            SelectionArtifactRequest.from_recipe(
                job.recipe, job.producer_version
            ),
        )
        resolutions.append(
            {
                "strategy": job.strategy,
                "recipe_hash": job.recipe.recipe_hash,
                "hit": resolution.hit,
                "miss_reasons": list(resolution.miss_reasons),
            }
        )
    store_after = _tree_snapshot(target_root)
    legacy_after, _ = legacy_cache_state(legacy_roots)
    if store_after != store_before:
        raise CacheV2Error("selection plan modified the ArtifactStore")
    if legacy_after != legacy_before:
        raise LegacySourceChangedError("selection plan modified a Legacy cache")
    return {
        "ok": True,
        "mode": "plan",
        "lookup": "exact-only",
        "plan": plan.to_dict(),
        "resolutions": resolutions,
        "execution_performed": False,
        "producer_calls": 0,
        "writes": [],
        "writes_scope": "artifact_store_only",
        "store_root": str(target_root),
        "store_unchanged": True,
        "legacy_cache_unchanged": True,
        "legacy_cache_state_hash_before": legacy_before,
        "legacy_cache_state_hash_after": legacy_after,
        "legacy_cache_file_counts": legacy_counts,
        "dataset_provider": "opengu-canonical-processed-pickle-v1",
        "split_reconstructed": False,
    }


def materialize_selection(
    config_source: Union[str, Path, Mapping[str, Any]],
    processed_root: Union[str, Path],
    store_root: Any,
    legacy_results_root: Any,
    *,
    verify: bool = False,
    fail_if_producer_called: bool = False,
    compare_legacy: bool = False,
    include_nodes: bool = False,
    dataset_inputs: Optional[DatasetSelectionInputs] = None,
) -> Dict[str, Any]:
    total_started = time.perf_counter()
    legacy_root = validate_legacy_results_root(legacy_results_root)
    legacy_roots = legacy_cache_roots(legacy_root)
    target_root = validate_store_root(store_root, legacy_roots)
    legacy_before, legacy_counts = legacy_cache_state(legacy_roots)
    store_before = _tree_snapshot(target_root)
    plan = prepare_selection_plan(
        config_source,
        processed_root,
        dataset_inputs=dataset_inputs,
    )
    results = []
    for job in plan.jobs:
        materialized = resolve_or_produce_selection(
            job,
            target_root,
            fail_if_producer_called=fail_if_producer_called,
        )
        document = _result_document(job, materialized, target_root, include_nodes)
        if verify:
            verified = resolve_selection_artifact(
                target_root,
                SelectionArtifactRequest.from_recipe(
                    job.recipe, job.producer_version
                ),
            )
            if (
                not verified.hit
                or verified.result is None
                or verified.result.artifact_id != materialized.result.artifact_id
                or verified.result.content_hash != materialized.result.content_hash
                or verified.result.payload.selected_nodes_ordered
                != materialized.result.payload.selected_nodes_ordered
            ):
                raise CacheV2Error("independent warm verification failed")
            document["verification"] = {
                "ok": True,
                "hit": True,
                "producer_called": False,
                "artifact_id": verified.result.artifact_id,
                "content_hash": verified.result.content_hash,
                "selected_nodes_equal": True,
            }
        if compare_legacy:
            document["legacy_comparison"] = compare_legacy_selection(
                job,
                plan.request,
                materialized.result.payload.selected_nodes_ordered,
                legacy_root,
            )
        results.append(document)
    legacy_after, _ = legacy_cache_state(legacy_roots)
    if legacy_after != legacy_before:
        raise LegacySourceChangedError("Selection production modified a Legacy cache")
    store_after = _tree_snapshot(target_root)
    return {
        "ok": True,
        "mode": "materialize",
        "lookup": "exact-only",
        "plan": plan.to_dict(),
        "results": results,
        "store_root": str(target_root),
        "writes": _changed_store_paths(store_before, store_after),
        "write_scope": "artifact_store_only",
        "legacy_cache_unchanged": True,
        "legacy_cache_state_hash_before": legacy_before,
        "legacy_cache_state_hash_after": legacy_after,
        "legacy_cache_file_counts": legacy_counts,
        "dataset_provider": "opengu-canonical-processed-pickle-v1",
        "split_reconstructed": False,
        "verify_requested": bool(verify),
        "fail_if_producer_called": bool(fail_if_producer_called),
        "compare_legacy": bool(compare_legacy),
        "elapsed_seconds": time.perf_counter() - total_started,
    }


__all__ = [
    "DEGREE_ALGORITHM_VERSION",
    "FUTURE_PRODUCERS",
    "IM_NUMBA_ALGORITHM_VERSION",
    "IM_PRODUCER_SEMANTIC_VERSION",
    "ImParameters",
    "MaterializedSelection",
    "PAGERANK_ALGORITHM_VERSION",
    "PRODUCER_REGISTRY",
    "PreparedSelectionJob",
    "PreparedSelectionPlan",
    "RANDOM_ALGORITHM_VERSION",
    "SelectionInputs",
    "SelectionRequest",
    "UpstreamProducerCalledError",
    "build_degree_producer",
    "build_im_producer",
    "build_selection_job",
    "build_simple_producer",
    "compare_legacy_selection",
    "implementation_backend",
    "legacy_cache_roots",
    "legacy_cache_state",
    "load_im_strategy",
    "load_selection_request",
    "load_simple_strategy",
    "materialize_selection",
    "plan_selection",
    "prepare_selection_plan",
    "producer_source_fingerprint",
    "resolve_or_produce_selection",
    "validate_legacy_results_root",
    "validate_store_root",
]
