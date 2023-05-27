from typing import Mapping

import pandas as pd

from parimana.vote.eye import BettingType, Eye


def vote_ratio_to_tally(
    vote_ratio: Mapping[BettingType, float], total: float
) -> pd.Series:
    sum_ = sum(vote_ratio.values())
    return pd.DataFrame.from_records(
        [
            {"type": k.name, "vote_tally": v / sum_ * total}
            for k, v in vote_ratio.items()
        ],
        index="type",
    )["vote_tally"]


def odds_to_df(odds: Mapping[Eye, float]) -> pd.DataFrame:
    return pd.DataFrame.from_records(
        [{"eye": e.text, "type": e.type.name, "odds": o} for e, o in odds.items()],
        index="eye",
    )


def calc_vote_tally(
    odds: Mapping[Eye, float], vote_ratio: Mapping[BettingType, float], total: float
) -> Mapping[Eye, float]:
    odds_df = odds_to_df(odds)
    tally_by_type = vote_ratio_to_tally(vote_ratio, total)

    odds_df["odds_inv"] = 1 / odds_df["odds"]

    inv_sum_by_type = odds_df.groupby("type")["odds_inv"].sum()
    correction = tally_by_type / inv_sum_by_type
    df = odds_df.join(correction.rename("correction"), on="type")

    sr = df["odds_inv"] * df["correction"]

    return {Eye(i): r for i, r in sr.items()}


def calc_expected_dividend(
    odds: Mapping[Eye, float], chance: Mapping[Eye, float]
) -> Mapping[Eye, float]:
    odds_sr = odds_to_df(odds)["odds"]
    chance_sr = pd.DataFrame.from_records(
        [{"eye": k.text, "chance": v} for k, v in chance.items()], index="eye"
    )["chance"]
    ed = (odds_sr * chance_sr).dropna() * 100
    return {Eye(i): d for i, d in ed.items()}
