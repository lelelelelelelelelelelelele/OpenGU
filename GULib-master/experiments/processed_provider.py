"""Canonical OpenGU processed-artifact paths owned by the experiment layer."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import hashlib
import math
from pathlib import Path
import re
from typing import Any, Dict, Mapping, Optional, Tuple


class ProcessedArtifactError(RuntimeError):
    """Raised when an explicit processed-data contract cannot be satisfied."""


PROCESSED_PROFILE_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
DEFAULT_TRAIN_RATIO = 0.7
DEFAULT_VALIDATION_RATIO = 0.1
DEFAULT_TEST_RATIO = 0.2
DEFAULT_SPLIT_SEED = 2024


def normalized_processed_profile(value: Any) -> str:
    """Return a safe optional persisted-split profile token.

    Ratio-derived filenames remain the default.  A named profile is reserved
    for an explicitly persisted split whose masks cannot be represented by a
    train/validation/test ratio triplet (for example Planetoid's public split).
    """

    if value in (None, ""):
        return ""
    profile = str(value).strip().lower()
    if PROCESSED_PROFILE_RE.fullmatch(profile) is None:
        raise ProcessedArtifactError(
            "processed_profile must match {0}".format(PROCESSED_PROFILE_RE.pattern)
        )
    return profile


def _ratio_profile_token(value: float) -> str:
    percent = (Decimal(str(float(value))) * Decimal("100")).normalize()
    token = format(percent, "f")
    if "." in token:
        token = token.rstrip("0").rstrip(".")
    return token.replace(".", "p")


def canonical_split_profile(
    *,
    profile_prefix: str,
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    split_seed: int,
) -> str:
    """Derive one stable persisted-profile name from split semantics."""

    prefix = normalized_processed_profile(profile_prefix)
    if not prefix:
        raise ProcessedArtifactError("profile_prefix is required")
    ratios = (float(train_ratio), float(val_ratio), float(test_ratio))
    tokens = tuple(_ratio_profile_token(item) for item in ratios)
    profile = "{0}_{1}_{2}_{3}_seed{4}".format(
        prefix, tokens[0], tokens[1], tokens[2], int(split_seed)
    )
    if PROCESSED_PROFILE_RE.fullmatch(profile) is not None:
        return profile
    identity = "{0}|{1}|{2}|{3}|{4}".format(
        prefix,
        *(format(Decimal(str(item)).normalize(), "f") for item in ratios),
        int(split_seed),
    )
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:20]
    return "split_{0}_seed{1}".format(digest, int(split_seed))


@dataclass(frozen=True)
class ProcessedSplitContract:
    """Identity of one persisted OpenGU dataset split."""

    processed_profile: str
    train_ratio: float
    val_ratio: float
    test_ratio: float
    split_seed: int

    def to_manifest(self) -> Dict[str, Any]:
        return {
            "processed_profile": self.processed_profile,
            "train_ratio": self.train_ratio,
            "val_ratio": self.val_ratio,
            "test_ratio": self.test_ratio,
            "split_seed": self.split_seed,
        }


def processed_split_contract(
    value: Mapping[str, Any],
    *,
    require_explicit: bool = False,
    require_profile: bool = False,
    profile_prefix: Optional[str] = None,
) -> ProcessedSplitContract:
    """Parse and validate the reusable split contract declared by an experiment."""

    split = value.get("split")
    if split is None:
        if require_explicit:
            raise ProcessedArtifactError("split mapping is required")
        split = {}
    if not isinstance(split, Mapping):
        raise ProcessedArtifactError("split must be a mapping")
    declared_profile = normalized_processed_profile(value.get("processed_profile"))

    raw_ratios = (
        split.get("train_ratio", DEFAULT_TRAIN_RATIO),
        split.get("val_ratio", DEFAULT_VALIDATION_RATIO),
        split.get("test_ratio", DEFAULT_TEST_RATIO),
    )
    if any(isinstance(item, bool) for item in raw_ratios):
        raise ProcessedArtifactError("split ratios must be numeric")
    try:
        train_ratio, val_ratio, test_ratio = (
            float(item) for item in raw_ratios
        )
    except (TypeError, ValueError) as exc:
        raise ProcessedArtifactError("split ratios must be numeric") from exc
    ratios = (train_ratio, val_ratio, test_ratio)
    if (
        any(not math.isfinite(item) for item in ratios)
        or train_ratio <= 0
        or val_ratio < 0
        or test_ratio <= 0
        or abs(sum(ratios) - 1.0) > 1e-12
    ):
        raise ProcessedArtifactError(
            "split ratios must be finite, train/test positive, validation "
            "non-negative, and sum to 1"
        )
    train_ratio, val_ratio, test_ratio = (
        0.0 if item == 0.0 else item for item in ratios
    )

    raw_seed = split.get("split_seed", DEFAULT_SPLIT_SEED)
    if isinstance(raw_seed, bool):
        raise ProcessedArtifactError("split_seed must be a non-negative integer")
    try:
        split_seed = int(raw_seed)
    except (TypeError, ValueError) as exc:
        raise ProcessedArtifactError(
            "split_seed must be a non-negative integer"
        ) from exc
    if split_seed < 0 or str(raw_seed).strip() != str(split_seed):
        raise ProcessedArtifactError("split_seed must be a non-negative integer")

    profile = declared_profile
    if profile_prefix is not None:
        profile = canonical_split_profile(
            profile_prefix=profile_prefix,
            train_ratio=train_ratio,
            val_ratio=val_ratio,
            test_ratio=test_ratio,
            split_seed=split_seed,
        )
        if declared_profile and declared_profile != profile:
            raise ProcessedArtifactError(
                "processed_profile conflicts with the canonical split identity"
            )
    if require_profile and not profile:
        raise ProcessedArtifactError("processed_profile is required")

    return ProcessedSplitContract(
        processed_profile=profile,
        train_ratio=train_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        split_seed=split_seed,
    )


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
    profile = normalized_processed_profile(args.get("processed_profile"))
    if profile:
        stem = "{0}__{1}".format(args["dataset_name"], profile)
    else:
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
