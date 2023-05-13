# from enum import Enum
from functools import cached_property
from typing import Collection, Mapping
from dataclasses import dataclass

import pandas as pd

from parimana.base.race import Race
from parimana.base.eye import BettingType, Eye


# https://www.jra.go.jp/keiba/overseas/yougo/c10080_list.html

# pari-mutuel betting


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


@dataclass(frozen=True)
class VoteTally:
    eye: Eye
    amount: float

    @classmethod
    def from_text(cls, text: str):
        splitted = text.split(": ")
        return VoteTally(Eye(splitted[0]), float(splitted[1]))

    @classmethod
    def from_record(cls, rec) -> "VoteTally":
        return VoteTally(Eye.from_record(rec), rec["vote_tally"])


def calc_vote_tally(
    odds: Collection[Odds], vote_ratio: Mapping[BettingType, float], total: float
) -> Collection["VoteTally"]:
    odds_df = odds_to_df(odds)
    expected_df = expected_votes_df(vote_ratio, total)
    return df_to_votes(calc_vote_tally_by_pd(odds_df, expected_df))


def odds_to_df(odds: Collection[Odds]) -> pd.DataFrame:
    return pd.DataFrame.from_records([o.record for o in odds])


def df_to_votes(df: pd.DataFrame) -> Collection["VoteTally"]:
    return [VoteTally.from_record(rec) for rec in df.to_dict(orient="records")]


def expected_votes_df(
    vote_ratio: Mapping[BettingType, float], total: float
) -> pd.DataFrame:
    return pd.DataFrame.from_dict(
        {k.name: [k.name, v, v * total] for k, v in vote_ratio.items()},
        orient="index",
        columns=["type", "ratio", "vote_tally"],
    )


def calc_vote_tally_by_pd(
    odds_df: pd.DataFrame, expected_df: pd.DataFrame
) -> pd.DataFrame:
    odds_df["odds_inv"] = 1 / odds_df["odds"]

    type_grouped = odds_df.groupby("type")["odds_inv"].sum()
    correction = pd.merge(type_grouped.reset_index(), expected_df, on="type")
    correction["correction_factor"] = correction["vote_tally"] / correction["odds_inv"]

    df = pd.merge(odds_df, correction[["type", "correction_factor"]], on="type")
    df["vote_tally"] = df["odds_inv"] * df["correction_factor"]

    return df


@dataclass(frozen=True)
class RaceVote:
    race: Race
    vote_tallies: Collection[VoteTally]


@dataclass(frozen=True)
class RaceOdds:
    race: Race
    vote_tallies: Collection[Odds]
