from functools import cached_property
from typing import (
    Mapping,
    Sequence,
    TypeVar,
)
from dataclasses import dataclass


from parimana.base.eye import BettingType, Eye
from parimana.base.vote import calc_vote_tally
from parimana.base.situation import Situation, Distribution

T = TypeVar("T")


@dataclass(frozen=True, order=True)
class Contestant:
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Contestants:
    contestants: Sequence[Contestant]

    @cached_property
    def contestants_map(self) -> Mapping[str, Contestant]:
        return {c.name: c for c in self.contestants}

    def _find_contestant(self, name) -> Contestant:
        if name in self.contestants_map:
            return self.contestants_map[name]
        else:
            raise ValueError(f"{name} Not Found in contestants")

    def situation(self, eye: Eye, frequency: float = 1) -> Situation[Contestant]:
        selected = eye.map(self._find_contestant)
        unselected = set(self.contestants) - set(selected)
        return Situation.from_collections((selected, unselected), eye.text, frequency)

    def destribution(
        self, vote_tallies: Mapping[Eye, float]
    ) -> Distribution[Contestant]:
        return Distribution([self.situation(k, v) for k, v in vote_tallies.items()])

    def destribution_from_odds(
        self,
        odds: Mapping[Eye, float],
        vote_ratio: Mapping[BettingType, float],
        vote_tally_total: float,
    ) -> Distribution[Contestant]:
        return self.destribution(calc_vote_tally(odds, vote_ratio, vote_tally_total))

    @classmethod
    def from_names(cls, names: Sequence[str]) -> "Contestants":
        constrants = [Contestant(name) for name in names]
        return Contestants(constrants)

    @classmethod
    def no_absences(cls, number_of_contestants: int) -> "Contestants":
        digits = len(str(number_of_contestants))
        names = (f"{i:0{digits}}" for i in range(1, number_of_contestants + 1))
        return Contestants.from_names(names)
