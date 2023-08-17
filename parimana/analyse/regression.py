from dataclasses import dataclass

import scipy.stats
import scipy.optimize
import numpy as np


@dataclass
class RegressionModel:
    slope: float
    intercept: float
    rvalue: float = 1
    pvalue: float = 0
    stderr: float = 0

    @property
    def func(self):
        return lambda x: self.slope * x + self.intercept


def linereg(x, y) -> RegressionModel:
    return RegressionModel(*(scipy.stats.linregress(x, y)))


@dataclass
class PiecewiseModel:
    boundary: float
    intercept: float
    slope1: float
    slope2: float

    @property
    def func(self):
        return lambda x: piecewise_line(
            x, self.boundary, self.intercept, self.slope1, self.slope2
        )


def piecewise_linereg(x, y) -> PiecewiseModel:
    p, e = scipy.optimize.curve_fit(piecewise_line, x, y)
    return PiecewiseModel(*p)


def piecewise_line(x, boundary, intercept, slope1, slope2):
    def piecewise_line_0_bound(x, b, a1, a2):
        # print(x)
        return np.piecewise(
            x,
            [x < 0, x >= 0],
            [
                lambda x: a1 * x + b,
                lambda x: a2 * x + b,
            ],
        )

    return piecewise_line_0_bound(x - boundary, intercept, slope1, slope2)
