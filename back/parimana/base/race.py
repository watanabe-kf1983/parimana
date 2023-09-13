from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Mapping, Optional

from parimana.base.contestants import Contestants
from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds


class Race(ABC):
    @property
    @abstractmethod
    def race_id(self) -> str:
        pass

    @property
    @abstractmethod
    def source(self) -> "RaceSource":
        pass

    @classmethod
    @abstractmethod
    def from_id(cls, race_id: str) -> Optional["Race"]:
        pass


@dataclass
class RaceOddsPool:
    race: Race
    odds: Mapping[Eye, Odds]
    vote_ratio: Mapping[BettingType, float]

    @property
    def contestants(self) -> Contestants:
        names = [eye.text for eye in self.odds.keys() if eye.type == BettingType.WIN]
        return Contestants.from_names(names)


class RaceSource(ABC):
    @abstractmethod
    def scrape_odds_pool(self) -> RaceOddsPool:
        pass
