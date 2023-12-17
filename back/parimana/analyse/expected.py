from dataclasses import dataclass
from functools import cached_property
from typing import Mapping, Optional, Sequence

import pandas as pd
import numpy as np

from parimana.base import BettingType, Eye, Odds
from parimana.analyse.chart import Chart, Cmap, DoubleLogAxes
from parimana.analyse.regression import (
    RegressionModel,
    linereg,
)


@dataclass(frozen=True)
class EyeExpectedValue:
    eye: Eye
    odds: float
    chance: float
    expected: float


def eye_expected_df(
    odds: Mapping[Eye, Odds], chances: Mapping[Eye, float]
) -> pd.DataFrame:
    odds_df = odds_to_df(odds)
    odds_sr = odds_df["odds"]
    chance_sr = chance_to_sr(chances)
    expected_sr = (odds_sr * chance_sr * 100).fillna(0).rename("expected")
    return odds_df.join(chance_sr, how="left").join(expected_sr, how="left").fillna(0)


def odds_to_df(odds: Mapping[Eye, Odds]) -> pd.DataFrame:
    return pd.DataFrame.from_records(
        [
            {
                "eye": e.text,
                "type": e.type.name,
                "tid": e.type.id,
                "odds": o.odds,
            }
            for e, o in odds.items()
        ],
        index="eye",
    ).sort_values(["tid", "eye"])[["type", "odds"]]


def chance_to_sr(chances: Mapping[Eye, float]) -> pd.Series:
    return pd.DataFrame.from_records(
        [{"eye": e.text, "chance": o} for e, o in chances.items()],
        index="eye",
    )["chance"].rename("chance")


def calc_regression_model(df: pd.DataFrame) -> Mapping[BettingType, RegressionModel]:
    return {
        BettingType[lbl]: linereg(np.log(df["odds"]), np.log(df["chance"]))
        for lbl, df in df.query("odds > 0 & chance > 0").groupby("type")
    }


# def calc_pw_regression_model(df: pd.DataFrame)
# -> Mapping[BettingType, PiecewiseModel]:
#     return {
#         BettingType[lbl]: piecewise_linereg(
#             np.log(df["odds"].to_numpy()), np.log(df["chance"].to_numpy())
#         )
#         for lbl, df in df.query("odds > 0 & chance > 0").groupby("type")
#     }


@dataclass(frozen=True)
class EyeExpectedValues:
    df: pd.DataFrame
    regression_model: Mapping[BettingType, RegressionModel]

    @classmethod
    def from_odds_and_chances(
        cls, odds: Mapping[Eye, Odds], chances: Mapping[Eye, float]
    ) -> "EyeExpectedValues":
        df = eye_expected_df(odds, chances).sort_values("expected", ascending=False)
        return EyeExpectedValues(df, calc_regression_model(df))

    def filter(
        self, query: str = "expected >= 100", size: Optional[int] = None
    ) -> "EyeExpectedValues":
        df = self.df
        if query:
            df = df.query(query)
        if size:
            df = df.head(size)

        return EyeExpectedValues(df, self.regression_model)

    def values(self) -> Sequence[EyeExpectedValue]:
        return [
            EyeExpectedValue(Eye(rec.Index), rec.odds, rec.chance, rec.expected)
            for rec in self.df.itertuples()
        ]

    @cached_property
    def chart(self) -> Chart:
        df = self.df.query("odds > 0 & chance > 0").sort_values("odds", ascending=False)
        rgms = self.regression_model

        fig = Chart()
        ax = fig.add_double_log(1, 1, 1)
        draw(ax, df, rgms)

        return fig


def draw(dla: DoubleLogAxes, df, rgms) -> None:
    cdict = get_cdict()
    xmin = df["odds"].min() / 1.5
    xmax = df["odds"].max() * 1.5

    dla.scatter(
        df["odds"],
        df["chance"],
        c=df["type"].map(cdict),
        zorder=1,
        alpha=0.5,
    )

    for lbl in sorted(df["type"].unique(), key=lambda x: BettingType[x].id):
        t_df = df[df["type"] == lbl]
        rgm = rgms[BettingType[lbl]]
        dla.line(
            rgm,
            xmin=t_df["odds"].min() / 1.5,
            xmax=t_df["odds"].max() * 1.5,
            label=lbl,
            cdict=cdict,
            fmt="--",
            zorder=2,
        )

    dla.line(
        RegressionModel(-1, np.log(0.75)),
        xmin=xmin,
        xmax=xmax,
        label="Theoretical",
        cdict=cdict,
        linewidth=3,
        alpha=0.5,
        zorder=0,
    )
    dla.line(
        RegressionModel(-1, 0),
        xmin=xmin,
        xmax=xmax,
        label="Breakeven",
        cdict=cdict,
        linewidth=3,
        alpha=0.5,
        zorder=0,
    )
    dla.legend(fontsize="xx-small")


def get_cdict():
    cmap = Cmap()
    cdict = {}
    cdict["WIN"] = cmap.get(0)
    cdict["PLACE"] = cmap.get(1)
    cdict["SHOW"] = cdict["PLACE"]
    cdict["EXACTA"] = cmap.get(2)
    cdict["QUINELLA"] = cmap.get(3)
    cdict["WIDE"] = cmap.get(4)
    cdict["TRIFECTA"] = cmap.get(5)
    cdict["TRIO"] = cmap.get(6)
    cdict["Theoretical"] = cmap.get(7)
    cdict["Breakeven"] = cmap.get(8)

    return cdict
