from functools import cached_property
from typing import Collection, Mapping, TypeVar
from dataclasses import dataclass

import numpy as np
import pandas as pd

from parimana.base.race import Race
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
        records = [
            relation.record | {"weight": weight}
            for (selection, weight) in self.selections.items()
            for relation in selection.relations.relations
        ]
        return (
            pd.DataFrame.from_records(records)
            .groupby(["a", "b", "sa"])
            .sum()
            .reset_index()
        )


@dataclass(frozen=True)
class RaceOdds:
    race: Race
    odds: Collection[Odds]

    def estimate_vote(self, ratio: VoteTallyByType) -> RaceVote:
        return RaceVote(self.race, calc_vote_tally(self.odds, ratio))
