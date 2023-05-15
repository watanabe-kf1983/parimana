from typing import (
    Collection,
    Sequence,
    TypeVar,
)
from dataclasses import dataclass


from parimana.vote.eye import Eye
from parimana.vote.vote import Odds, VoteTally, VoteTallyByType, calc_vote_tally
from parimana.situation.situation import Situation, Distribution

T = TypeVar("T")

# https://www.jra.go.jp/keiba/overseas/yougo/c10080_list.html

# pari-mutuel betting


@dataclass(frozen=True, order=True)
class Contestant:
    name: str

    def __str__(self) -> str:
        return self.name

    def match(self, name: str) -> bool:
        return self.name == name


@dataclass(frozen=True)
class Race:
    contestants: Sequence[Contestant]
    name: str = ""

    def _find_contestant(self, name) -> Contestant:
        matched = [c for c in self.contestants if c.match(name)]
        if matched:
            return matched[0]
        else:
            raise ValueError(f"{name} Not Found in contestants")

    def situation(self, eye: Eye, frequency: float = 1) -> Situation[Contestant]:
        selected = eye.map(self._find_contestant)
        unselected = set(self.contestants) - set(selected)
        return Situation.from_collections((selected, unselected), frequency)

    def destribution(
        self, vote_tallies: Collection[VoteTally]
    ) -> Distribution[Contestant]:
        return Distribution([self.situation(v.eye, v.amount) for v in vote_tallies])

    def destribution_from_odds(
        self, odds: Collection[Odds], ratio: VoteTallyByType
    ) -> Distribution[Contestant]:
        return self.destribution(calc_vote_tally(odds, ratio))

    @classmethod
    def no_absences(cls, number_of_contestants: int, name="") -> "Race":
        digits = len(str(number_of_contestants))
        constrants = [
            Contestant(f"{i:0{digits}}") for i in range(1, number_of_contestants + 1)
        ]
        return Race(constrants, name)
