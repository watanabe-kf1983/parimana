from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from typing import Mapping

from parimana.domain.base.eye import BettingType, Eye
from parimana.domain.base.contestants import Contestants


def text2float(text: str) -> float:
    return float(text.strip().replace(",", ""))


class Odds(ABC):
    @property
    @abstractmethod
    def odds(self) -> float:
        pass

    @classmethod
    def from_text(cls, text: str) -> "Odds":

        if "-" in text:
            min, max, *_ = text.split("-")
            return PlaceOdds(text2float(min), text2float(max))
        else:
            return NormalOdds(text2float(text))


@dataclass
class NormalOdds(Odds):
    odds_: float

    @property
    def odds(self) -> float:
        return self.odds_


@dataclass
class PlaceOdds(Odds):
    min: float
    max: float

    @property
    def odds(self) -> float:
        return round((self.min * 2 + self.max) / 3, 1)


@dataclass
class OddsPool:
    odds: Mapping[Eye, Odds]
    vote_ratio: Mapping[BettingType, float]

    def __post_init__(self):
        self.odds = {eye: odds for eye, odds in self.odds.items() if odds.odds > 0}

    @cached_property
    def contestants(self) -> Contestants:
        nameset = {name for eye in self.odds.keys() for name in eye.names}
        return Contestants.from_names(sorted(nameset))
