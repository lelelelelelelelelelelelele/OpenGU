"""White-box target-direct Selection→GNNDelete experiment lane."""

from typing import Any, Mapping

from experiments.processed_provider import (
    ProcessedArtifactError,
    ProcessedSplitContract,
    processed_split_contract,
)

SPLIT_SEED = 2024
MODEL_SEEDS = (42, 212, 2024)
TRAIN_RATIO = 0.7
VALIDATION_RATIO = 0.1
TEST_RATIO = 0.2


def target_direct_split_contract(
    value: Mapping[str, Any], *, require_explicit: bool = False
) -> ProcessedSplitContract:
    """Parse a Planetoid split and derive its one canonical profile name."""

    contract = processed_split_contract(
        value,
        require_explicit=require_explicit,
        require_profile=True,
        profile_prefix="planetoid",
    )
    if contract.val_ratio <= 0:
        raise ProcessedArtifactError(
            "target-direct split requires a positive validation ratio"
        )
    return contract


DEFAULT_SPLIT_CONTRACT = target_direct_split_contract(
    {
        "split": {
            "train_ratio": TRAIN_RATIO,
            "val_ratio": VALIDATION_RATIO,
            "test_ratio": TEST_RATIO,
            "split_seed": SPLIT_SEED,
        }
    },
    require_explicit=True,
)
PROFILE = DEFAULT_SPLIT_CONTRACT.processed_profile
