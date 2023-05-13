from functools import cached_property
from typing import Collection, Mapping, Tuple, TypeVar
from dataclasses import dataclass

import numpy as np
import pandas as pd

from parimana.base.race import Race, Contestant
from parimana.base.selection import Selection
from parimana.vote.odds import Odds, VoteTally, VoteTallyByType, calc_vote_tally

T = TypeVar("T")


@dataclass(frozen=True)
class RaceVote:
    race: Race
    vote_tallies: Collection[VoteTally]

    @cached_property
    def selections(self) -> Mapping[Selection, float]:
        return {Selection(self.race, v.eye): v.amount for v in self.vote_tallies}

    @cached_property
    def relations(self) -> pd.DataFrame:
        cs = self.race.constrants
        records = [
            {"sup": str(x), "inf": str(y), "weight": 0} for x in cs for y in cs
        ] + [
            relation.record | {"weight": weight}
            for (selection, weight) in self.selections.items()
            for relation in selection.relations
        ]
        df = (
            pd.DataFrame.from_records(records)
            .groupby(["inf", "sup"])
            .sum()
            .reset_index()
        )
        df2 = pd.merge(
            df, df, how="left", left_on=["sup", "inf"], right_on=["inf", "sup"]
        ).fillna(0)
        df2["count"] = df2["weight_x"] + df2["weight_y"]
        df2["ratio"] = df2["weight_x"] / df2["count"]
        return pd.pivot_table(
            df2,
            index="sup_x",
            columns="inf_x",
            values=["ratio"],
            aggfunc=np.sum,
        )

    @cached_property
    def ranks(self) -> Collection[Tuple[Mapping[Contestant, float], float]]:
        records = [
            (selection.rank_dict | {"weight": weight})
            for selection, weight in self.selections.items()
        ]
        return pd.DataFrame.from_records(records)


@dataclass(frozen=True)
class RaceOdds:
    race: Race
    odds: Collection[Odds]

    def estimate_vote(self, ratio: VoteTallyByType) -> RaceVote:
        return RaceVote(self.race, calc_vote_tally(self.odds, ratio))
