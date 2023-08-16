from dataclasses import dataclass
from functools import cached_property
from typing import Mapping

import pandas as pd
import numpy as np

from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds
from parimana.analyse.chart import Chart, Cmap, DoubleLogAxes
from parimana.analyse.regression import RegressionModel, linereg


@dataclass
class OddsChance:
    odds: Mapping[Eye, Odds]
    chances: Mapping[Eye, float]

    @cached_property
    def odds_df(self) -> pd.DataFrame:
        return pd.DataFrame.from_records(
            [
                {
                    "eye": e.text,
                    "type": e.type.name,
                    "tid": e.type.id,
                    "odds": o.odds,
                }
                for e, o in self.odds.items()
            ],
            index="eye",
        ).sort_values(["tid", "eye"])[["type", "odds"]]

    @cached_property
    def odds_sr(self) -> pd.Series:
        return self.odds_df["odds"]

    @cached_property
    def chance_sr(self) -> pd.Series:
        return pd.DataFrame.from_records(
            [{"eye": e.text, "chance": o} for e, o in self.chances.items()],
            index="eye",
        )["chance"].rename("chance")

    @cached_property
    def expected_sr(self) -> pd.Series:
        return (self.odds_sr * self.chance_sr * 100).fillna(0).rename("expected")

    @cached_property
    def df(self) -> pd.DataFrame:
        return (
            self.odds_df.join(self.chance_sr, how="left")
            .join(self.expected_sr, how="left")
            .fillna(0)
        )

    @cached_property
    def regression_model(self) -> Mapping[BettingType, RegressionModel]:
        return {
            BettingType[lbl]: linereg(np.log(df["odds"]), np.log(df["chance"]))
            for lbl, df in self.df.query("odds > 0 & chance > 0").groupby("type")
        }

    @cached_property
    def chart(self) -> Chart:
        df = self.df.query("odds > 0 & chance > 0").sort_values("odds", ascending=False)
        lbls = sorted(df["type"].unique(), key=lambda lbl: BettingType[lbl].id)
        cmap = Cmap()
        fig = Chart()
        cdict = {lbl: cmap.get(i) for i, lbl in enumerate(lbls)}
        cdict["Theoretical"] = cmap.get(len(lbls))
        cdict["Breakeven"] = cmap.get(len(lbls) + 1)
        fig.cdict = cdict

        xmin = df["odds"].min() / 1.5
        xmax = df["odds"].max() * 1.5

        ax = fig.add_double_log(3, 3, 1)
        self.draw(ax, df, xmin, xmax, hidereg=True)

        for idx, lbl in enumerate(lbls):
            ax = fig.add_double_log(3, 3, idx + 2)
            self.draw(ax, df[df["type"] == lbl], xmin, xmax)
            ax.legend(fontsize="small")

        ax = fig.add_double_log(3, 3, 9)
        self.draw(ax, df, xmin, xmax, hidescat=True)
        ax.legend(fontsize="xx-small")

        return fig

    def draw(
        self, dla: DoubleLogAxes, df, xmin, xmax, hidereg=False, hidescat=False
    ) -> Chart:
        if not hidescat:
            dla.scatter(
                df["odds"],
                df["chance"],
                c=df["type"].map(dla.cdict),
                zorder=1,
                alpha=0.5,
            )

        if not hidereg:
            for lbl in sorted(df["type"].unique(), key=lambda x: BettingType[x].id):
                t_df = df[df["type"] == lbl]
                rgm = self.regression_model[BettingType[lbl]]
                dla.line(
                    rgm,
                    xmin=t_df["odds"].min() / 1.5,
                    xmax=t_df["odds"].max() * 1.5,
                    label=lbl,
                    fmt="--",
                    zorder=2,
                )

        dla.line(
            RegressionModel(-1, np.log(0.75)),
            xmin=xmin,
            xmax=xmax,
            label="Theoretical",
            linewidth=3,
            alpha=0.5,
            zorder=0,
        )
        dla.line(
            RegressionModel(-1, 0),
            xmin=xmin,
            xmax=xmax,
            label="Breakeven",
            linewidth=3,
            alpha=0.5,
            zorder=0,
        )
