from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Mapping

from parimana.base.eye import BettingType, Eye
from parimana.base.contestants import Contestants


class Odds(ABC):
    @property
    @abstractmethod
    def odds(self) -> float:
        pass

    @classmethod
    def from_text(cls, text: str) -> "Odds":
        if "-" in text:
            sp = text.split("-")
            return PlaceOdds(float(sp[0]), float(sp[1]))
        else:
            return NormalOdds(float(text))


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
        return (self.max + self.min) / 2


@dataclass
class OddsPool:
    odds: Mapping[Eye, Odds]
    vote_ratio: Mapping[BettingType, float]

    @property
    def contestants(self) -> Contestants:
        names = [eye.text for eye in self.odds.keys() if eye.type == BettingType.WIN]
        return Contestants.from_names(names)
