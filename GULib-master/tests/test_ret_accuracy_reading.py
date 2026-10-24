"""Integer-bound float64 accuracy checks for saved Ret endpoint predictions."""
import math

import numpy as np
import pytest

from experiments.ret_reference_reading import _accuracy_matches


def adjacent(value, direction, steps):
    for _ in range(steps):
        value = float(np.nextafter(value, direction))
    return value


@pytest.mark.parametrize('correct,total', [(0, 666), (1, 666), (333, 666),
                                           (479, 666), (484, 666), (666, 666)])
def test_exact_count_and_two_ulp_boundary(correct, total):
    canonical = correct / total
    assert _accuracy_matches(canonical, correct, total)
    for direction in (-math.inf, math.inf):
        for steps in (1, 2):
            value = adjacent(canonical, direction, steps)
            assert _accuracy_matches(value, correct, total) == (0 <= value <= 1)
        assert not _accuracy_matches(adjacent(canonical, direction, 3), correct, total)
    other = correct + 1 if correct < total else correct - 1
    assert not _accuracy_matches(other / total, correct, total)


@pytest.mark.parametrize('saved,correct', [(0.7267267267267267, 484),
                                           (0.7192192192192192, 479)])
def test_observed_saved_accuracies_keep_the_same_integer(saved, correct):
    assert saved != correct / 666
    assert round(saved * 666) == correct
    assert _accuracy_matches(saved, correct, 666)
    assert not _accuracy_matches(saved, correct + 1, 666)


@pytest.mark.parametrize('saved', [math.nan, math.inf, -math.inf, -0.01, 1.01,
                                   True, False, None, '0.5'])
def test_invalid_saved_accuracy_rejected(saved):
    assert not _accuracy_matches(saved, 333, 666)


@pytest.mark.parametrize('correct,total', [(0, 0), (-1, 666), (667, 666)])
def test_invalid_count_rejected(correct, total):
    assert not _accuracy_matches(0.5, correct, total)
