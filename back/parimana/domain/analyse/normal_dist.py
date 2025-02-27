import math

import numpy as np
import scipy.integrate
import scipy.stats
import scipy.optimize


def estimate_mean_delta_slow(pp: float, sd_x: float, sd_y: float, cor: float) -> float:
    if math.isclose(cor, 1) and math.isclose(pp, 0.5):
        return 0

    cov = np.array([[sd_x**2, cor * sd_x * sd_y], [cor * sd_x * sd_y, sd_y**2]])

    def integrate_mvn(dist: float) -> float:
        mean = np.array([0, dist])
        a, _ = scipy.integrate.dblquad(
            lambda y, x: scipy.stats.multivariate_normal.pdf(
                [x, y], mean=mean, cov=cov
            ),
            -sd_x * 10,
            sd_x * 10,
            -sd_y * 10 + dist,
            lambda x: x,
        )
        return 1 - a

    return scipy.optimize.root_scalar(
        lambda x: integrate_mvn(x) - pp, x0=0, x1=0.01
    ).root


def estimate_mean_delta(pp: float, sd_x: float, sd_y: float, cor: float) -> float:
    if math.isclose(cor, 1) and math.isclose(pp, 0.5):
        return 0

    # 理屈はわからないけど結果としてこれでestimate_mean_delta_slowと同じ計算ができた
    scale = (sd_x**2 + sd_y**2 - 2 * cor * sd_x * sd_y) ** (0.5)
    return scipy.stats.norm.ppf(pp, loc=0, scale=scale)


def rvs(mean: np.ndarray, cov: np.ndarray, size: int):
    # if not is_symmetric(cov):
    #     raise ValueError("not symmetric")

    # if not is_positive_semidefinite(cov):
    #     eigvals = np.linalg.eigvalsh(cov)
    #     print(eigvals)
    #     raise ValueError("not positive_semidefinite")
    return np.random.multivariate_normal(mean, cov, size)
    # return scipy.stats.multivariate_normal.rvs(mean=mean, cov=cov, size=size)


def is_symmetric(matrix):
    return np.allclose(matrix, matrix.T)


def is_positive_definite(matrix):
    eigvals = np.linalg.eigvalsh(matrix)
    return np.all(eigvals > 0)


def is_positive_semidefinite(matrix):
    eigvals = np.linalg.eigvalsh(matrix)
    return np.all(eigvals >= 0)
