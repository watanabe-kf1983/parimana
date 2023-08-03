from pathlib import Path

import numpy as np
import matplotlib.pyplot as mpplt
import matplotlib.figure as mpfig
import matplotlib.axes as mpaxes


class Cmap:
    def __init__(self, name="tab10") -> None:
        self.cmap = mpplt.get_cmap(name)
        self.n = self.cmap.N

    def get(self, i: int):
        return self.cmap(i % self.n)


class Chart:
    def __init__(self) -> None:
        self.fig: mpfig.Figure = mpplt.figure(figsize=(6.4 * 3, 4.8 * 3))
        self.cdict: dict = {}

    def add_double_log(self, *args, **kwargs) -> "DoubleLogAxes":
        return DoubleLogAxes(self.fig.add_subplot(*args, **kwargs), self.cdict)

    def save(self, path: Path) -> None:
        self.fig.savefig(path, dpi=300)


class DoubleLogAxes:
    def __init__(self, ax: mpaxes.Axes, cdict: dict) -> None:
        self.ax: mpaxes.Axes = ax
        self.ax.set_xscale("log")
        self.ax.set_yscale("log")
        self.cdict = cdict

    def line(self, reg, xmin, xmax, label, fmt="-", **kwargs) -> None:
        x = np.logspace(np.log(xmin), np.log(xmax), base=np.e)
        y = x**reg.slope * np.exp(reg.intercept)
        legend_label = (
            f"{label}: $y={np.exp(reg.intercept):.2f}x^{{{reg.slope:.2f}}}$"
            f"  ($R^2={(reg.rvalue)**2:.2f}$)"
        )
        self.ax.plot(x, y, fmt, label=legend_label, c=self.cdict[label], **kwargs)

    def legend(self, *args, **kwargs) -> None:
        self.ax.legend(*args, **kwargs)

    def scatter(self, *args, **kwargs) -> None:
        self.ax.scatter(*args, **kwargs)
