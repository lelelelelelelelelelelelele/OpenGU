# AAGU-028 findings

- Baseline e27425e6ad8ba8dd34663098d759d83ab4804023; prerequisites AAGU-001 and AAGU-026 accepted.
- modular_config.gu_defaults and modular_gu.GU_METHODS only register GNNDelete/GIF.
- modular GU persists aggregate AttackResult only; rounded serialization then from_dict recomputes derived quantities.
- modular_evaluation rejects retrain-gap; currently reads summary fields rather than verified stored predictions.
- eval_collateral.main calls pipeline.run_retrain and reruns GU. Existing run_retrain chooses another GU through UnlearningManager and excludes train_mask only.
- Existing supervised training owner: experiments.modular_model.train_supervised / c_target_v1.core.train_trajectory. Reuse it rather than implement another optimizer loop.
- Cache V2 formal Store already supports Prediction and Evaluation, producer identity, immutable payloads, dependencies and read-only integrity verification.
