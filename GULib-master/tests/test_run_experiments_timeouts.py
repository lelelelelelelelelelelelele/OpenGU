import run_experiments


def test_phase_state_transitions_by_output_markers():
    phase, strategy = run_experiments._update_phase_state(None, None, "[AttackManager] Running attack with strategy: random")
    assert phase == "selection"
    assert strategy == "random"

    phase, strategy = run_experiments._update_phase_state(phase, strategy, "2026-02-22 10:00:00: Selection took 3.14s")
    assert phase == "unlearning"
    assert strategy == "random"

    phase, strategy = run_experiments._update_phase_state(phase, strategy, "2026-02-22 10:00:00: Unlearning took 8.88s")
    assert phase is None
    assert strategy == "random"


def test_selection_cache_hit_moves_to_unlearning_phase():
    phase, strategy = run_experiments._update_phase_state(None, None, "[AttackManager] Running attack with strategy: im")
    assert phase == "selection"
    assert strategy == "im"

    phase, strategy = run_experiments._update_phase_state(
        phase,
        strategy,
        "[SelectionCache] HIT strategy=im selection_key=abc original_selection_time=12.3s",
    )
    assert phase == "unlearning"
    assert strategy == "im"


def test_method_timeout_override_applies_to_both_phases():
    selection_s, unlearning_s = run_experiments._resolve_phase_timeouts(
        method="GraphEraser",
        default_selection_timeout=600,
        default_unlearning_timeout=600,
        method_timeout_map={"GraphEraser": 900},
    )
    assert selection_s == 900
    assert unlearning_s == 900

    selection_s, unlearning_s = run_experiments._resolve_phase_timeouts(
        method="GIF",
        default_selection_timeout=600,
        default_unlearning_timeout=600,
        method_timeout_map={"GraphEraser": 900},
    )
    assert selection_s == 600
    assert unlearning_s == 600
