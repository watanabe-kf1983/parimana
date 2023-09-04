from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Mapping, Optional


from parimana.base.contestants import Contestants
from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds


@dataclass
class Race:
    race_id: str
    odds: Mapping[Eye, Odds]
    vote_ratio: Mapping[BettingType, float]

    @property
    def contestants(self) -> Contestants:
        names = [eye.text for eye in self.odds.keys() if eye.type == BettingType.WIN]
        return Contestants.from_names(names)


class RaceSource(ABC):
    @property
    @abstractmethod
    def race_id(self) -> str:
        pass

    @abstractmethod
    def scrape_race(self) -> Race:
        pass

    @classmethod
    @abstractmethod
    def from_race_id(cls, race_id: str) -> Optional["RaceSource"]:
        pass
