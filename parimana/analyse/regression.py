from dataclasses import dataclass

import scipy.stats


@dataclass
class RegressionModel:
    slope: float
    intercept: float
    rvalue: float = 1
    pvalue: float = 0
    stderr: float = 0


def linereg(x, y) -> RegressionModel:
    return RegressionModel(*(scipy.stats.linregress(x, y)))
