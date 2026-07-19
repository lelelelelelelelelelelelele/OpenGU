"""Canonical OpenGU processed-artifact paths owned by the experiment layer."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Tuple


class ProcessedArtifactError(RuntimeError):
    """Raised when an explicit processed-data contract cannot be satisfied."""


@dataclass(frozen=True)
class ProcessedArtifactPaths:
    root: Path
    lane: str
    data_path: Path
    dataset_path: Path
    explicit: bool

    @property
    def available(self) -> bool:
        return self.data_path.is_file() and self.dataset_path.is_file()

    @property
    def missing(self) -> Tuple[Path, ...]:
        return tuple(
            path
            for path in (self.data_path, self.dataset_path)
            if not path.is_file()
        )


def processed_artifact_paths(args: Mapping[str, Any]) -> ProcessedArtifactPaths:
    """Resolve the canonical split and dataset pickle paths for ``args``."""

    configured_root = args.get("processed_root")
    explicit = configured_root not in (None, "")
    if explicit:
        root = Path(str(configured_root)).expanduser()
        if not root.is_absolute():
            raise ProcessedArtifactError(
                "explicit processed_root must be absolute: {0}".format(root)
            )
    else:
        repository_root = Path(str(args.get("root_path") or ".")).expanduser()
        root = repository_root / "data" / "processed"

    root = root.resolve()
    lane = "transductive" if args.get("is_transductive", True) else "inductive"
    split_token = "_".join(
        str(args[name])
        for name in ("train_ratio", "val_ratio", "test_ratio")
    )
    stem = "{0}{1}".format(args["dataset_name"], split_token)
    suffix = "_balanced" if args.get("is_balanced", False) else ""
    lane_root = root / lane
    return ProcessedArtifactPaths(
        root=root,
        lane=lane,
        data_path=lane_root / "{0}{1}.pkl".format(stem, suffix),
        dataset_path=lane_root / "{0}dataset{1}.pkl".format(stem, suffix),
        explicit=explicit,
    )


def require_processed_artifacts(
    args: Mapping[str, Any],
) -> ProcessedArtifactPaths:
    """Fail closed when the explicit canonical processed pair is incomplete."""

    paths = processed_artifact_paths(args)
    if paths.available:
        return paths
    missing = ", ".join(str(path) for path in paths.missing)
    raise ProcessedArtifactError(
        "canonical processed artifacts are incomplete; missing: {0}. "
        "Explicit processed_root forbids raw loading, dataset download, and "
        "split reconstruction.".format(missing)
    )
