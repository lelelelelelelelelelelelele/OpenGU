import json

import numpy as np
import pytest
import torch

from attack.attack_result import AttackResult
from attack.result_cache import ResultCache
from attack.score_cache import ScoreCache
from attack.selection_cache import SelectionCache, SelectionResult
from cache_v2.legacy_freeze import (
    LegacyCacheFrozenError,
    plan_or_freeze_legacy_caches,
    read_freeze_marker,
)
from scripts import cachectl


def _result():
    return AttackResult(
        strategy_name="degree",
        selected_nodes=torch.tensor([1, 2]),
        f1_before=0.9,
        f1_after=0.8,
        unlearn_time=1.0,
        total_time=2.0,
    )


def test_freeze_dry_run_is_zero_write_then_existing_caches_are_read_only(tmp_path):
    results = (tmp_path / "results").resolve()
    result_cache = ResultCache(str(results / "cache"), max_age_days=0)
    selection_cache = SelectionCache(str(results / "selection_cache"))
    score_cache = ScoreCache("im", str(results / "score_cache"))
    config = {"strategy_name": "degree", "k": 2}
    result_cache.save(_result(), config)
    selection_cache.save(
        SelectionResult("degree", [1, 2], 0.1, "fixture"), config
    )
    score_cache.save(np.array([1, 2]), np.array([0.2, 0.1]), config)

    planned = plan_or_freeze_legacy_caches(
        results, actor="maintainer", reason="V2 canary cutover", apply=False
    )
    assert planned["mode"] == "dry-run"
    assert planned["writes"] == []
    assert not (results / "cache_v2" / "legacy_freeze.json").exists()

    frozen = plan_or_freeze_legacy_caches(
        results, actor="maintainer", reason="V2 canary cutover", apply=True
    )
    assert frozen["outcome"] == "frozen"
    assert len(frozen["writes"]) == 1
    marker = read_freeze_marker(results)
    assert marker["state"] == "frozen"
    assert marker["snapshot"]["total_files"] == 4

    # Existing trees remain readable after the freeze.
    assert ResultCache(str(results / "cache"), max_age_days=0).get(config) is not None
    assert SelectionCache(str(results / "selection_cache")).get(config)[0] is not None
    assert ScoreCache("im", str(results / "score_cache")).get(config)[0] is not None

    with pytest.raises(LegacyCacheFrozenError):
        result_cache.save(_result(), {"strategy_name": "random", "k": 2})
    with pytest.raises(LegacyCacheFrozenError):
        result_cache.invalidate(config)
    with pytest.raises(LegacyCacheFrozenError):
        selection_cache.save(
            SelectionResult("random", [2, 1], 0.1, "other"), config
        )
    with pytest.raises(LegacyCacheFrozenError):
        score_cache.save(np.array([1]), np.array([0.5]), {"other": True})
    with pytest.raises(LegacyCacheFrozenError):
        ScoreCache("new-namespace", str(results / "score_cache"))
    assert not (results / "score_cache" / "new-namespace").exists()


def test_cachectl_freeze_is_explicit_and_status_is_read_only(tmp_path, capsys):
    results = (tmp_path / "results").resolve()
    results.mkdir()
    args = [
        "legacy",
        "freeze",
        "--root",
        str(results),
        "--actor",
        "maintainer",
        "--reason",
        "archive readiness",
    ]
    assert cachectl.main(args) == 0
    assert json.loads(capsys.readouterr().out)["writes"] == []
    assert cachectl.main([*args, "--apply"]) == 0
    assert json.loads(capsys.readouterr().out)["outcome"] == "frozen"
    assert cachectl.main(
        ["legacy", "freeze-status", "--root", str(results)]
    ) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["state"] == "frozen"
    assert status["writes"] == []
