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
    assert_legacy_cache_writable,
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


def test_freeze_keeps_legacy_payload_read_only(tmp_path):
    results = (tmp_path / "results").resolve()
    # Historical fixture bytes are created explicitly; no active consumer can
    # produce Legacy payloads after AAGU-025.
    for name in ("cache", "selection_cache", "score_cache"):
        path = results / name
        path.mkdir(parents=True)
        (path / "legacy.json").write_text('{"historical":true}')
    planned = plan_or_freeze_legacy_caches(results, actor="maintainer", reason="fixture", apply=False)
    assert planned["writes"] == []
    frozen = plan_or_freeze_legacy_caches(results, actor="maintainer", reason="fixture", apply=True)
    assert frozen["outcome"] == "frozen"
    assert read_freeze_marker(results)["snapshot"]["total_files"] == 3
    for name in ("cache", "selection_cache", "score_cache"):
        assert (results / name / "legacy.json").read_text() == '{"historical":true}'
        with pytest.raises(LegacyCacheFrozenError):
            assert_legacy_cache_writable(results / name)


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
