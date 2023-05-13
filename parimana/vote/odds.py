# from enum import Enum
from functools import cached_property
from typing import Collection, Mapping
from dataclasses import dataclass

import pandas as pd

from parimana.base.eye import BettingType, Eye
from parimana.vote.vote import VoteTally


@dataclass(frozen=True)
class Odds:
    eye: Eye
    odds: float

    @cached_property
    def record(self):
        return self.eye.record | {"odds": self.odds}

    @classmethod
    def from_text(cls, text: str):
        splitted = text.split(": ")
        return Odds(Eye(splitted[0]), float(splitted[1]))

    @classmethod
    def from_record(cls, rec):
        return Odds(Eye.from_record(rec), rec["odds"])

    @classmethod
    def odds_to_df(cls, odds: Collection["Odds"]) -> pd.DataFrame:
        return pd.DataFrame.from_records([o.record for o in odds])


@dataclass(frozen=True)
class VoteTallyByType:
    vote_ratio: Mapping[BettingType, float]
    total: float

    @cached_property
    def df(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(
            {k.name: [k.name, v, v * self.total] for k, v in self.vote_ratio.items()},
            orient="index",
            columns=["type", "ratio", "vote_tally"],
        )


def calc_vote_tally(
    odds: Collection[Odds], vote_ratio: VoteTallyByType
) -> Collection["VoteTally"]:
    odds_df = Odds.odds_to_df(odds)
    expected_df = vote_ratio.df
    return VoteTally.df_to_votes(calc_vote_tally_by_pd(odds_df, expected_df))


def calc_vote_tally_by_pd(
    odds_df: pd.DataFrame, expected_df: pd.DataFrame
) -> pd.DataFrame:
    odds_df["odds_inv"] = 1 / odds_df["odds"]

    type_grouped = odds_df.groupby("type")["odds_inv"].sum().reset_index()
    correction = pd.merge(type_grouped, expected_df, on="type")
    correction["correction_factor"] = correction["vote_tally"] / correction["odds_inv"]

    df = pd.merge(odds_df, correction[["type", "correction_factor"]], on="type")
    df["vote_tally"] = df["odds_inv"] * df["correction_factor"]

    return df
