import math

import numpy as np
import scipy as sc


def estimate_mean_delta_slow(
    win_rate: float, sd_x: float, sd_y: float, cor: float
) -> float:
    if math.isclose(cor, 1) and math.isclose(win_rate, 0.5):
        return 0

    cov = np.array([[sd_x**2, cor * sd_x * sd_y], [cor * sd_x * sd_y, sd_y**2]])

    def integrate_mvn(dist: float) -> float:
        mean = np.array([0, dist])
        a, _ = sc.integrate.dblquad(
            lambda y, x: sc.stats.multivariate_normal.pdf([x, y], mean=mean, cov=cov),
            -sd_x * 10,
            sd_x * 10,
            -sd_y * 10 + dist,
            lambda x: x,
        )
        return 1 - a

    return sc.optimize.root_scalar(
        lambda x: integrate_mvn(x) - win_rate, x0=0, x1=0.01
    ).root


def estimate_mean_delta(win_rate: float, sd_x: float, sd_y: float, cor: float) -> float:
    if math.isclose(cor, 1) and math.isclose(win_rate, 0.5):
        return 0

    # 理屈はわからないけど結果としてこれでestimate_mean_delta_slowと同じ計算ができた
    scale = (sd_x**2 + sd_y**2 - 2 * cor * sd_x * sd_y) ** (0.5)
    return sc.stats.norm.ppf(win_rate, loc=0, scale=scale)
