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
        self.fig: mpfig.Figure = mpplt.figure(figsize=(6.4, 4.8))

    def add_double_log(self, *args, **kwargs) -> "DoubleLogAxes":
        return DoubleLogAxes(self.fig.add_subplot(*args, **kwargs))

    def save(self, path: Path) -> None:
        self.fig.savefig(path, dpi=300)


class DoubleLogAxes:
    def __init__(self, ax: mpaxes.Axes) -> None:
        self.ax: mpaxes.Axes = ax
        self.ax.set_xscale("log")
        self.ax.set_yscale("log")

    def line(self, reg, xmin, xmax, label, cdict, fmt="-", **kwargs) -> None:
        x = np.logspace(np.log(xmin), np.log(xmax), base=np.e)
        y = x**reg.slope * np.exp(reg.intercept)
        legend_label = (
            f"{label}: $y={np.exp(reg.intercept):.2f}x^{{{reg.slope:.2f}}}$"
            f"  ($R^2={(reg.rvalue)**2:.2f}$)"
        )
        self.ax.plot(x, y, fmt, label=legend_label, c=cdict[label], **kwargs)

    def pw_line(self, pwm, xmin, xmax, label, cdict, fmt="-", **kwargs) -> None:
        x = np.logspace(np.log(xmin), np.log(xmax), base=np.e)
        y = np.exp(pwm.func(np.log(x)))
        legend_label = (
            f"{label}: "
            f"$y={np.exp(pwm.intercept - pwm.slope1 * pwm.boundary):.2f}"
            f"x^{{{pwm.slope1:.2f}}}$  ($x < 10^{{{pwm.boundary/(np.log(10)):.2f}}}$), "
            f"$y={np.exp(pwm.intercept - pwm.slope2 * pwm.boundary):.2f}"
            f"x^{{{pwm.slope2:.2f}}}$"
        )
        self.ax.plot(x, y, fmt, label=legend_label, c=cdict[label], **kwargs)

    def legend(self, *args, **kwargs) -> None:
        self.ax.legend(*args, **kwargs)

    def scatter(self, *args, **kwargs) -> None:
        self.ax.scatter(*args, **kwargs)
