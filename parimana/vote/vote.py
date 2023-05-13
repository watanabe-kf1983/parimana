# from enum import Enum
from typing import Collection
from dataclasses import dataclass

import pandas as pd

from parimana.base.eye import Eye


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

    @classmethod
    def df_to_votes(cls, df: pd.DataFrame) -> Collection["VoteTally"]:
        return [VoteTally.from_record(rec) for rec in df.to_dict(orient="records")]
