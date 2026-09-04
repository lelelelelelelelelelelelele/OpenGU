"""Software regression for IF-family write-back and retired repair entrypoints."""
import ast
import inspect
from pathlib import Path
import subprocess
import sys
import textwrap

import pytest

from scripts import verify_if_writeback_patch as verifier
from unlearning.unlearning_methods.GIF.gif import gif
from unlearning.unlearning_methods.IDEA.idea import idea

METHODS = [("GIF", gif), ("IDEA", idea)]
REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("label,method", METHODS)
def test_actual_writeback_reaches_collateral_hop_consumer(label, method):
    observed = verifier.check_model_writeback(label, method)
    assert observed["fraction_flipped"] == 0.0


def without_writeback(function):
    """Reproduce the original defect in memory; source/comments stay intact."""
    tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
    node = tree.body[0]

    def writes_parameters(statement):
        return isinstance(statement, ast.With) and any(
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr == "copy_"
            for child in ast.walk(statement)
        )

    assert sum(writes_parameters(statement) for statement in node.body) == 1
    node.body = [statement for statement in node.body if not writes_parameters(statement)]
    namespace = {}
    exec(compile(tree, function.__code__.co_filename, "exec"), function.__globals__, namespace)
    return namespace["approxi"]


@pytest.mark.parametrize("label,method", METHODS)
def test_verifier_rejects_missing_writeback_despite_unchanged_source(label, method, monkeypatch, capsys):
    original = method.approxi
    source = Path(original.__code__.co_filename)
    original_bytes = source.read_bytes()
    assert "Write params_esti back" in original_bytes.decode("utf-8")
    monkeypatch.setattr(method, "approxi", without_writeback(original))
    assert not verifier.verify_loaded_writeback(label, method, source.relative_to(REPO_ROOT))
    assert "write-back missing" in capsys.readouterr().out
    assert source.read_bytes() == original_bytes


def test_verifier_rejects_a_method_loaded_from_a_different_checkout(capsys):
    assert not verifier.verify_loaded_writeback("GIF", gif, "other-checkout/gif.py")
    assert "expected active-checkout source" in capsys.readouterr().out


def test_aagu009_retired_entrypoints_are_absent():
    for relative in (
        "scripts/redo_collateral_if_family.py",
        "scripts/cleanup_if_family_collateral.py",
        ".workblock/items/AAGU-009/evidence/repair-scope.yaml",
    ):
        assert not (REPO_ROOT / relative).exists()


def test_direct_verifier_runs_from_outside_the_checkout(tmp_path):
    completed = subprocess.run(
        [sys.executable, "-B", "-X", "utf8", str(REPO_ROOT / "scripts/verify_if_writeback_patch.py")],
        cwd=tmp_path, capture_output=True, text=True, check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "loaded GIF source:" in completed.stdout
    assert "loaded IDEA source:" in completed.stdout
    assert "ALL CHECKS PASSED" in completed.stdout
