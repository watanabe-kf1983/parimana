from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
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
class OddsTimeStamp:
    update_time: Optional[datetime] = None

    def __str__(self) -> str:
        return (
            "Confirmed"
            if self.is_confirmed
            else self.update_time.strftime("%Y%m%d%H%M")
        )

    @property
    def is_confirmed(self) -> bool:
        return not bool(self.update_time)

    @classmethod
    @property
    def confirmed(cls) -> "OddsTimeStamp":
        return OddsTimeStamp(None)


class OddsUpdatedException(Exception):
    pass


@dataclass
class RaceOddsPool:
    race: Race
    odds: Mapping[Eye, Odds]
    timestamp: OddsTimeStamp
    vote_ratio: Mapping[BettingType, float]

    @property
    def contestants(self) -> Contestants:
        names = [eye.text for eye in self.odds.keys() if eye.type == BettingType.WIN]
        return Contestants.from_names(names)


class RaceSource(ABC):
    @abstractmethod
    def scrape_odds_pool(self) -> RaceOddsPool:
        pass
