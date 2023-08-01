from pathlib import Path

import numpy as np
import matplotlib.pyplot as mpplt
import matplotlib.figure as mpfig
import matplotlib.axes as mpaxes


class Chart:
    def __init__(self) -> None:
        fig, ax = mpplt.subplots()
        self.fig: mpfig.Figure = fig
        self.ax: mpaxes.Axes = ax


class DoubleLogChart(Chart):
    def __init__(self) -> None:
        super().__init__()
        self.ax.set_xscale("log")
        self.ax.set_yscale("log")

    def line(self, reg, format, xmin, xmax, color, label) -> None:
        x = np.logspace(np.log(xmin), np.log(xmax), base=np.e)
        y = x**reg.slope * np.exp(reg.intercept)
        label = (
            f"{label}: $y={np.exp(reg.intercept):.3f}x^{{{reg.slope:.3f}}}$"
            # + f"  (rsq={(reg.rvalue)**2:.3f})"
        )
        self.ax.plot(x, y, format, c=color, label=label)
        self.ax.legend()

    def scatter(self, x, y, color) -> None:
        self.ax.scatter(x, y, s=1, c=color, marker="o")

    def save(self, path: Path) -> None:
        self.fig.savefig(path, dpi=300)
