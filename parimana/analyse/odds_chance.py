from dataclasses import dataclass
from functools import cached_property
from typing import Mapping

import pandas as pd
import numpy as np

from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds
from parimana.analyse.chart import DoubleLogChart
from parimana.analyse.regression import RegressionModel, linereg


@dataclass
class OddsChance:
    odds: Mapping[Eye, Odds]
    chances: Mapping[Eye, float]

    @cached_property
    def odds_df(self) -> pd.DataFrame:
        return pd.DataFrame.from_records(
            [
                {"eye": e.text, "type": e.type.name, "odds": o.odds}
                for e, o in self.odds.items()
            ],
            index="eye",
        )

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
            .sort_values(["type", "eye"])
        )

    @cached_property
    def regression_model(self) -> Mapping[BettingType, RegressionModel]:
        return {
            BettingType[lbl]: linereg(np.log(df["odds"]), np.log(df["chance"]))
            for lbl, df in self.df.query("chance >= 0.000001").groupby("type")
        }

    @cached_property
    def chart(self) -> DoubleLogChart:
        chart = DoubleLogChart()
        df = self.df
        chart.scatter(df["odds"], df["chance"], color=df["type"].map(colormap))

        xmin = df["odds"].min()
        xmax = df["odds"].max()

        for lbl in df["type"].unique():
            rgm = self.regression_model[BettingType[lbl]]
            chart.line(
                rgm,
                "--",
                xmax=xmax,
                xmin=xmin,
                color=colormap[lbl],
                label=lbl,
            )

        chart.line(
            RegressionModel(-1, np.log(0.75)),
            "-",
            xmin=xmin,
            xmax=xmax,
            color="gray",
            label="Theoretical",
        )
        chart.line(
            RegressionModel(-1, 0),
            "-",
            xmin=xmin,
            xmax=xmax,
            color="black",
            label="Breakeven",
        )
        return chart


colormap = {
    "WIN": "blue",
    "PLACE": "orange",
    "SHOW": "green",
    "EXACTA": "red",
    "QUINELLA": "purple",
    "WIDE": "brown",
    "TRIFECTA": "pink",
    "TRIO": "cyan",
}
