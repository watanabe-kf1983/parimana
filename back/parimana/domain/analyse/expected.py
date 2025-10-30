from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Optional, Sequence

import pandas as pd
import numpy as np
from plotly.graph_objects import Figure

from parimana.domain.base import BettingType, Eye, Odds
from parimana.domain.analyse.chart_pl import PlDoubleLogAxes
from parimana.domain.analyse.regression import (
    RegressionModel,
    linereg,
)


@dataclass(frozen=True)
class EyeExpectedValue:
    eye: Eye
    odds: float
    chance: float
    expected: float
    others: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_record(
        cls,
        eye: str,
        type: str,
        odds: float,
        chance: float,
        expected: float,
        **rest_kwargs,
    ) -> "EyeExpectedValue":
        return cls(Eye(eye), odds, chance, expected, MappingProxyType(rest_kwargs))


def eye_expected_df(
    odds: Mapping[Eye, Odds], chances: Mapping[Eye, float]
) -> pd.DataFrame:
    """
    odds: {Eye: Odds}
    chances: {Eye: chance(float)}
    return: DataFrame with columns: eye(index), type, tid, odds, chance, expected
    """
    odds_df = odds_to_df(odds)
    odds_sr = odds_df["odds"]
    chance_sr = chance_to_sr(chances)
    expected_sr = (odds_sr * chance_sr).fillna(0).rename("expected")
    return odds_df.join(chance_sr, how="left").join(expected_sr, how="left").fillna(0)


def combine_with_mean(named_dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    named_dfs = {"modelA": eye_expected_df_A, "modelB": eye_expected_df_B, ...}
    return: DataFrame with columns: eye(index), type, tid, odds,
                                    MultiIndex (name_or_mean, {chance, expected})。
    """

    if not named_dfs:
        return pd.DataFrame()

    first_df = next(iter(named_dfs.values()))
    base_df = first_df[["type", "odds"]]

    value_dfs = {name: df[["chance", "expected"]] for name, df in named_dfs.items()}
    values_wide = pd.concat(value_dfs, axis=1)  # columns: MultiIndex(model, variable)
    values_flat = values_wide.copy()
    values_flat.columns = [f"{m}_{v}" for m, v in values_wide.columns]

    mean = values_wide.T.groupby(level=1).mean().T  # columns: chance/expected

    return pd.concat([base_df, mean, values_flat], axis="columns")


def odds_to_df(odds: Mapping[Eye, Odds]) -> pd.DataFrame:
    """
    odds: {Eye: Odds}
    return: DataFrame with columns: eye(index), type, odds
    """
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
    """
    chances: {Eye: chance(float)}
    return: Series with index: eye, name: chance
    """
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
        df = eye_expected_df(odds, chances)
        return cls(df, calc_regression_model(df))

    @classmethod
    def combine(cls, dict: Mapping[str, "EyeExpectedValues"]) -> "EyeExpectedValues":
        df = combine_with_mean({name: eev.df for name, eev in dict.items()})
        return cls(df, {})

    def filter(
        self, query: Optional[str] = None, size: Optional[int] = None
    ) -> "EyeExpectedValues":
        df = self.df.sort_values("expected", ascending=False)
        if query:
            df = df.query(query)
        if size:
            df = df.head(size)

        return EyeExpectedValues(df, self.regression_model)

    def values(self) -> Sequence[EyeExpectedValue]:
        return [
            EyeExpectedValue.from_record(**d)
            for d in self.df.reset_index().to_dict(orient="records")
        ]

    def chart(self) -> Figure:
        df = self.df.query("odds > 0 & chance > 0").sort_values("odds", ascending=False)
        rgms = self.regression_model

        fig = PlDoubleLogAxes(
            title=dict(text="Odds v.s. Chance of hitting"),
            xaxis=dict(title="Odds"),
            yaxis=dict(title="Chance of hitting", tickformat="p"),
            margin=dict(t=50, b=50, r=20, l=50, autoexpand=True),
            legend=dict(
                xanchor="left",
                yanchor="top",
                x=0,
                y=-0.1,
                orientation="h",
            ),
            # hoverlabel=dict(align="right"),
        )
        ply_draw(fig, df, rgms)
        return fig


def ply_draw(dla: PlDoubleLogAxes, df, rgms) -> None:
    xmin = max(1, df["odds"].min() / 1.5)
    xmax = df["odds"].max() * 1.5

    dla.line(
        RegressionModel(-1, np.log(0.75)),
        xmin=xmin,
        xmax=xmax,
        label="Theoretical",
        legendrank=5001,
        hoverinfo="none",
        opacity=0.3,
        line=dict(color="grey", width=5),
    )
    dla.line(
        RegressionModel(-1, 0),
        xmin=xmin,
        xmax=xmax,
        label="Breakeven",
        legendrank=5000,
        hoverinfo="none",
        opacity=0.3,
        line=dict(color="red", width=5),
    )
    # for lbl in sorted(df["type"].unique(), key=lambda x: BettingType[x].id):
    #     t_df = df[df["type"] == lbl]
    #     rgm = rgms[BettingType[lbl]]
    #     dla.line(
    #         rgm,
    #         xmin=t_df["odds"].min() / 1.5,
    #         xmax=t_df["odds"].max() * 1.5,
    #         label=lbl,
    #         hoverinfo="none",
    #         line=dict(dash="dash"),
    #     )

    df["eye"] = df.index
    df["size"] = 10
    dla.scatter_xp(
        df,
        x="odds",
        y="chance",
        color="type",
        size="size",
        size_max=10,
        opacity=0.7,
        hover_name="eye",
        hover_data={
            "type": False,
            "size": False,
            "odds": ":.1f",
            "chance": ":.4p",
            "expected": ":.4f",
        },
        trendline="ols",
        trendline_options=dict(log_x=True, log_y=True),
        trendline_scatteropt=dict(
            line=dict(dash="dash"),
            hoverinfo="none",
            hovertemplate="",
        ),
    )
