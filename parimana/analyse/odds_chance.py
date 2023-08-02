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
            for lbl, df in self.df.query("odds > 0 & chance >= 0.000001").groupby(
                "type"
            )
        }

    @cached_property
    def chart(self) -> DoubleLogChart:
        df = self.df.query("odds > 0 & chance > 0")
        dlc = DoubleLogChart()
        dlc.scatter(
            df["odds"],
            df["chance"],
            c=df["type"].map(lambda t: BettingType[t].color),
            s=2,
            zorder=2
            # marker="o",
        )

        for lbl in df["type"].unique():
            t_df = df[df["type"] == lbl]
            rgm = self.regression_model[BettingType[lbl]]
            dlc.line(
                rgm,
                xmin=t_df["odds"].min() / 2,
                xmax=t_df["odds"].max() * 2,
                label=lbl,
                c=BettingType[lbl].color,
                fmt="--",
                linewidth=0.5,
                zorder=1,
            )

        dlc.line(
            RegressionModel(-1, np.log(0.75)),
            xmin=df["odds"].min() / 2,
            xmax=df["odds"].max() * 2,
            label="Theoretical",
            c="lightgray",
            linewidth=3,
            zorder=0,
        )
        dlc.line(
            RegressionModel(-1, 0),
            xmin=df["odds"].min() / 2,
            xmax=df["odds"].max() * 2,
            label="Breakeven",
            c="mistyrose",
            linewidth=3,
            zorder=0,
        )

        return dlc
