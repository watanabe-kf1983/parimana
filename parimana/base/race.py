from typing import (
    Mapping,
    TypeVar,
)
from dataclasses import dataclass


from parimana.base.eye import BettingType, Eye
from parimana.base.vote import calc_vote_tally
from parimana.base.situation import Situation, Distribution

T = TypeVar("T")

# https://www.jra.go.jp/keiba/overseas/yougo/c10080_list.html

# pari-mutuel betting


@dataclass(frozen=True, order=True)
class Contestant:
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Race:
    contestants: Mapping[str, Contestant]
    name: str = ""

    def _find_contestant(self, name) -> Contestant:
        if name in self.contestants:
            return self.contestants[name]
        else:
            raise ValueError(f"{name} Not Found in contestants")

    def situation(self, eye: Eye, frequency: float = 1) -> Situation[Contestant]:
        selected = eye.map(self._find_contestant)
        unselected = set(self.contestants.values()) - set(selected)
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
    def no_absences(cls, number_of_contestants: int, name="") -> "Race":
        digits = len(str(number_of_contestants))
        names = (f"{i:0{digits}}" for i in range(1, number_of_contestants + 1))
        constrants = {name: Contestant(name) for name in names}
        return Race(constrants, name)
