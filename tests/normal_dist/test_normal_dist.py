import math

import pytest
from parimana.normal_dist.normal_dist import (
    estimate_mean_delta,
    estimate_mean_delta_slow,
    simulate,
)


@pytest.mark.parametrize(
    ("win_rate", "sd_x", "sd_y", "cor"),
    [(0.3, 1.1, 0.8, 0.4), (0.7, 1, 1, -0.4), (0.5, 1, 1, 1)],
)
def test_estimate_mean_delta(win_rate, sd_x, sd_y, cor):
    expected = estimate_mean_delta_slow(win_rate, sd_x, sd_y, cor)
    actual = estimate_mean_delta(win_rate, sd_x, sd_y, cor)
    assert math.isclose(expected, actual)


def test_simulate():
    mean = [1, 10]
    cov = [[1, 0], [0, 1]]
    result = simulate(mean=mean, cov=cov, n=10)
    assert result.shape == (10, 2)
