import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from parimana.domain.analyse.regression import RegressionModel


class PlDoubleLogAxes:
    def __init__(self, **kwargs) -> None:
        self.fig: go.Figure = go.Figure()
        self.fig.update_xaxes(type="log")
        self.fig.update_yaxes(type="log")
        self.fig.update_layout(**kwargs)

    def line(self, reg: RegressionModel, xmin, xmax, label, **kwargs) -> None:
        x = np.logspace(np.log(xmin), np.log(xmax), base=np.e)
        y = x**reg.slope * np.exp(reg.intercept)
        legend_label = (
            f"$y={np.exp(reg.intercept):.2f}x^{{{reg.slope:.2f}}}$"
            # f"$\\text{{{label}: }}y={np.exp(reg.intercept):.2f}x^{{{reg.slope:.2f}}}$"
            # f"$\\text{{  (}}R^2={(reg.rvalue)**2:.2f}\\text{{)}}$"
        )
        self.fig.add_trace(
            go.Scatter(x=x, y=y, mode="lines", name=legend_label, **kwargs)
        )

    def scatter_xp(self, *args, **kwargs) -> None:
        trendline_scatteropt = kwargs.pop("trendline_scatteropt", dict())
        fig = px.scatter(*args, **kwargs)
        fig.update_traces(selector=dict(mode="lines"), **trendline_scatteropt)

        for trace in fig.data:
            self.fig.add_trace(trace)
