from typing import Mapping

import pandas as pd
from parimana.analyse.regression import RegressionModel

from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds


def calc_vote_tally(
    odds: Mapping[Eye, Odds],
    vote_ratio: Mapping[BettingType, float],
    odds_model: Mapping[BettingType, RegressionModel] = {},
) -> Mapping[Eye, float]:
    odds_df = odds_to_df(odds).join(type_exponent(odds_model), on="type", how="left")

    odds_df["odds_inv"] = odds_df["odds"] ** odds_df["exponent"]

    tally_by_type = vote_ratio_to_tally(vote_ratio)
    inv_sum_by_type = odds_df.groupby("type")["odds_inv"].sum()
    correction = tally_by_type / inv_sum_by_type
    df = odds_df.join(correction.rename("correction"), on="type")

    sr = df["odds_inv"] * df["correction"]

    return {Eye(i): v for i, v in sr.items()}


def odds_to_df(odds: Mapping[Eye, Odds]) -> pd.DataFrame:
    return pd.DataFrame.from_records(
        [{"eye": e.text, "type": e.type.name, "odds": o.odds} for e, o in odds.items()],
        index="eye",
    )


def type_exponent(odds_model: Mapping[BettingType, RegressionModel]) -> pd.Series:
    return pd.DataFrame.from_records(
        [
            {
                "type": bt.name,
                "exponent": odds_model.get(bt, RegressionModel(-1, 0)).slope,
            }
            for bt in BettingType
        ],
        index="type",
    )["exponent"]


def vote_ratio_to_tally(vote_ratio: Mapping[BettingType, float]) -> pd.Series:
    sum_ = sum(vote_ratio.values())
    return pd.DataFrame.from_records(
        [{"type": k.name, "vote_tally": v / sum_} for k, v in vote_ratio.items()],
        index="type",
    )["vote_tally"]
