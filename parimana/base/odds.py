from abc import ABC, abstractmethod
from dataclasses import dataclass


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
        return self.max
