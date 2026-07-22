"""Directed Independent-Cascade reverse-reachable sampling primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np


def _ordered_unique_nodes(
    values: Sequence[int],
    *,
    num_nodes: int,
    label: str,
) -> np.ndarray:
    nodes = np.asarray(values, dtype=np.int64).reshape(-1)
    if nodes.size == 0:
        raise ValueError("{0} must be non-empty".format(label))
    if np.any(nodes < 0) or np.any(nodes >= int(num_nodes)):
        raise ValueError("{0} contains a node outside [0, num_nodes)".format(label))
    if np.unique(nodes).size != nodes.size:
        raise ValueError("{0} must contain unique nodes".format(label))
    return nodes


@dataclass(frozen=True)
class DirectedGraph:
    """Immutable directed graph with sorted incoming and outgoing adjacency."""

    num_nodes: int
    in_neighbors: Tuple[Tuple[int, ...], ...]
    out_neighbors: Tuple[Tuple[int, ...], ...]
    edges: Tuple[Tuple[int, int], ...]

    @classmethod
    def from_edges(
        cls,
        num_nodes: int,
        edges: Iterable[Tuple[int, int]],
    ) -> "DirectedGraph":
        num_nodes = int(num_nodes)
        if num_nodes <= 0:
            raise ValueError("num_nodes must be positive")
        canonical = set()
        for raw_src, raw_dst in edges:
            src = int(raw_src)
            dst = int(raw_dst)
            if not 0 <= src < num_nodes or not 0 <= dst < num_nodes:
                raise ValueError("edge endpoint is outside [0, num_nodes)")
            canonical.add((src, dst))
        ordered = tuple(sorted(canonical))
        incoming: List[List[int]] = [[] for _ in range(num_nodes)]
        outgoing: List[List[int]] = [[] for _ in range(num_nodes)]
        for src, dst in ordered:
            outgoing[src].append(dst)
            incoming[dst].append(src)
        return cls(
            num_nodes=num_nodes,
            in_neighbors=tuple(tuple(values) for values in incoming),
            out_neighbors=tuple(tuple(values) for values in outgoing),
            edges=ordered,
        )

    @classmethod
    def from_edge_index(
        cls,
        edge_index: Any,
        num_nodes: int,
    ) -> "DirectedGraph":
        if hasattr(edge_index, "detach"):
            array = edge_index.detach().cpu().numpy()
        else:
            array = np.asarray(edge_index)
        array = np.asarray(array, dtype=np.int64)
        if array.ndim != 2 or array.shape[0] != 2:
            raise ValueError("edge_index must have shape [2, E]")
        return cls.from_edges(
            num_nodes,
            zip(array[0].tolist(), array[1].tolist()),
        )

    @property
    def edge_count(self) -> int:
        return len(self.edges)


@dataclass(frozen=True)
class RRBundle:
    """Compressed candidate incidences for a fixed RR sample batch."""

    num_nodes: int
    candidate_nodes: np.ndarray
    offsets: np.ndarray
    candidate_local_ids: np.ndarray
    roots: np.ndarray
    propagation_probability: float
    rr_seed: int
    root_domain_size: int
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        num_nodes = int(self.num_nodes)
        if num_nodes <= 0:
            raise ValueError("RR bundle num_nodes must be positive")
        candidates = _ordered_unique_nodes(
            self.candidate_nodes,
            num_nodes=num_nodes,
            label="candidate_nodes",
        ).copy()
        offsets = np.asarray(self.offsets, dtype=np.int64).reshape(-1).copy()
        incidences = np.asarray(
            self.candidate_local_ids,
            dtype=np.int32,
        ).reshape(-1).copy()
        roots = np.asarray(self.roots, dtype=np.int64).reshape(-1).copy()
        if roots.size == 0:
            raise ValueError("RR bundle must contain at least one sample")
        if offsets.shape != (roots.size + 1,):
            raise ValueError("RR offsets must have rr_count + 1 entries")
        if offsets[0] != 0 or offsets[-1] != incidences.size:
            raise ValueError("RR offsets do not span candidate incidences")
        if np.any(np.diff(offsets) < 0):
            raise ValueError("RR offsets must be monotonic")
        if np.any(roots < 0) or np.any(roots >= num_nodes):
            raise ValueError("RR root is outside [0, num_nodes)")
        if incidences.size:
            if np.any(incidences < 0) or np.any(incidences >= candidates.size):
                raise ValueError("RR incidence refers to unknown candidate")
        for rr_index in range(roots.size):
            start = int(offsets[rr_index])
            end = int(offsets[rr_index + 1])
            row = incidences[start:end]
            if row.size != np.unique(row).size:
                raise ValueError("one RR set contains duplicate candidates")
            if row.size > 1 and np.any(np.diff(row) <= 0):
                raise ValueError("RR candidate incidences must be sorted")
        probability = float(self.propagation_probability)
        if not 0.0 <= probability <= 1.0:
            raise ValueError("propagation probability must be in [0, 1]")
        if int(self.root_domain_size) <= 0:
            raise ValueError("root_domain_size must be positive")
        for array in (candidates, offsets, incidences, roots):
            array.setflags(write=False)
        object.__setattr__(self, "num_nodes", num_nodes)
        object.__setattr__(self, "candidate_nodes", candidates)
        object.__setattr__(self, "offsets", offsets)
        object.__setattr__(self, "candidate_local_ids", incidences)
        object.__setattr__(self, "roots", roots)
        object.__setattr__(self, "propagation_probability", probability)
        object.__setattr__(self, "rr_seed", int(self.rr_seed))
        object.__setattr__(self, "root_domain_size", int(self.root_domain_size))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @classmethod
    def from_rr_sets(
        cls,
        *,
        num_nodes: int,
        candidate_nodes: Sequence[int],
        rr_sets: Sequence[Sequence[int]],
        roots: Optional[Sequence[int]] = None,
        propagation_probability: float = 1.0,
        rr_seed: int = 0,
        root_domain_size: Optional[int] = None,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> "RRBundle":
        candidates = _ordered_unique_nodes(
            candidate_nodes,
            num_nodes=int(num_nodes),
            label="candidate_nodes",
        )
        local = {int(node): index for index, node in enumerate(candidates.tolist())}
        offsets = [0]
        incidences: List[int] = []
        for rr_set in rr_sets:
            row = sorted({local[int(node)] for node in rr_set if int(node) in local})
            incidences.extend(row)
            offsets.append(len(incidences))
        if roots is None:
            roots = list(range(len(rr_sets)))
            if roots and max(roots) >= int(num_nodes):
                roots = [0] * len(rr_sets)
        if len(roots) != len(rr_sets):
            raise ValueError("roots must align with rr_sets")
        return cls(
            num_nodes=int(num_nodes),
            candidate_nodes=candidates,
            offsets=np.asarray(offsets, dtype=np.int64),
            candidate_local_ids=np.asarray(incidences, dtype=np.int32),
            roots=np.asarray(roots, dtype=np.int64),
            propagation_probability=float(propagation_probability),
            rr_seed=int(rr_seed),
            root_domain_size=(
                int(num_nodes) if root_domain_size is None else int(root_domain_size)
            ),
            metadata={} if metadata is None else dict(metadata),
        )

    @property
    def rr_count(self) -> int:
        return int(self.roots.size)

    @property
    def candidate_count(self) -> int:
        return int(self.candidate_nodes.size)

    @property
    def total_incidences(self) -> int:
        return int(self.candidate_local_ids.size)

    def local_row(self, rr_index: int) -> np.ndarray:
        rr_index = int(rr_index)
        if not 0 <= rr_index < self.rr_count:
            raise IndexError("RR index outside bundle")
        start = int(self.offsets[rr_index])
        end = int(self.offsets[rr_index + 1])
        return self.candidate_local_ids[start:end]

    def global_row(self, rr_index: int) -> np.ndarray:
        return self.candidate_nodes[self.local_row(rr_index)]

    def incidence_counts(self) -> np.ndarray:
        return np.bincount(
            self.candidate_local_ids.astype(np.int64, copy=False),
            minlength=self.candidate_count,
        ).astype(np.int64, copy=False)

    def inverted_index(self) -> Tuple[np.ndarray, ...]:
        rows: List[List[int]] = [[] for _ in range(self.candidate_count)]
        for rr_index in range(self.rr_count):
            for local_id in self.local_row(rr_index):
                rows[int(local_id)].append(rr_index)
        return tuple(np.asarray(row, dtype=np.int64) for row in rows)

    def coverage_count(self, selected_nodes: Sequence[int]) -> int:
        selected = {int(node) for node in selected_nodes}
        local_selected = {
            index
            for index, node in enumerate(self.candidate_nodes.tolist())
            if int(node) in selected
        }
        if not local_selected:
            return 0
        covered = 0
        for rr_index in range(self.rr_count):
            if any(int(value) in local_selected for value in self.local_row(rr_index)):
                covered += 1
        return covered

    def summary(self) -> Dict[str, Any]:
        row_sizes = np.diff(self.offsets)
        return {
            "num_nodes": self.num_nodes,
            "candidate_count": self.candidate_count,
            "rr_count": self.rr_count,
            "total_incidences": self.total_incidences,
            "mean_candidate_rr_size": float(row_sizes.mean()),
            "max_candidate_rr_size": int(row_sizes.max(initial=0)),
            "propagation_probability": self.propagation_probability,
            "rr_seed": self.rr_seed,
            "root_domain_size": self.root_domain_size,
            "metadata": dict(self.metadata),
        }


def _sample_reverse_reachable(
    graph: DirectedGraph,
    root: int,
    probability: float,
    rng: np.random.Generator,
) -> Tuple[int, ...]:
    visited = {int(root)}
    frontier = [int(root)]
    head = 0
    while head < len(frontier):
        current = frontier[head]
        head += 1
        for predecessor in graph.in_neighbors[current]:
            if predecessor in visited:
                continue
            if probability >= 1.0 or (
                probability > 0.0 and float(rng.random()) < probability
            ):
                visited.add(predecessor)
                frontier.append(predecessor)
    return tuple(sorted(visited))


def sample_rr_bundle(
    graph: DirectedGraph,
    *,
    candidate_nodes: Sequence[int],
    rr_count: int,
    propagation_probability: float,
    rr_seed: int,
    root_nodes: Optional[Sequence[int]] = None,
    metadata: Optional[Mapping[str, Any]] = None,
) -> RRBundle:
    """Generate one fixed-size RR batch under directed static IC semantics."""

    rr_count = int(rr_count)
    if rr_count <= 0:
        raise ValueError("rr_count must be positive")
    probability = float(propagation_probability)
    if not 0.0 <= probability <= 1.0:
        raise ValueError("propagation_probability must be in [0, 1]")
    candidates = _ordered_unique_nodes(
        candidate_nodes,
        num_nodes=graph.num_nodes,
        label="candidate_nodes",
    )
    if root_nodes is None:
        roots_domain = np.arange(graph.num_nodes, dtype=np.int64)
    else:
        roots_domain = _ordered_unique_nodes(
            root_nodes,
            num_nodes=graph.num_nodes,
            label="root_nodes",
        )
    rng = np.random.default_rng(int(rr_seed))
    sampled_roots = roots_domain[
        rng.integers(0, roots_domain.size, size=rr_count, endpoint=False)
    ]
    candidate_lookup = set(candidates.tolist())
    rr_sets = []
    for root in sampled_roots.tolist():
        rr_set = _sample_reverse_reachable(graph, int(root), probability, rng)
        rr_sets.append([node for node in rr_set if node in candidate_lookup])
    bundle_metadata = {
        "sampler": "directed_ic_reverse_bfs",
        "edge_count": graph.edge_count,
        "candidate_fraction": 1.0,
    }
    if metadata:
        bundle_metadata.update(dict(metadata))
    return RRBundle.from_rr_sets(
        num_nodes=graph.num_nodes,
        candidate_nodes=candidates,
        rr_sets=rr_sets,
        roots=sampled_roots,
        propagation_probability=probability,
        rr_seed=int(rr_seed),
        root_domain_size=int(roots_domain.size),
        metadata=bundle_metadata,
    )
