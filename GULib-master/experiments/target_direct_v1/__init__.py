"""White-box target-direct Selection→GNNDelete experiment lane."""

from experiments.processed_provider import ProcessedSplitContract

PROFILE = "planetoid_70_10_20_seed2024"
SPLIT_SEED = 2024
MODEL_SEEDS = (42, 212, 2024)
TRAIN_RATIO = 0.7
VALIDATION_RATIO = 0.1
TEST_RATIO = 0.2

DEFAULT_SPLIT_CONTRACT = ProcessedSplitContract(
    processed_profile=PROFILE,
    train_ratio=TRAIN_RATIO,
    val_ratio=VALIDATION_RATIO,
    test_ratio=TEST_RATIO,
    split_seed=SPLIT_SEED,
)
