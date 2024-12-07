from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from functools import total_ordering
from typing import Optional

from parimana.base import OddsPool


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


class RaceSource(ABC):
    @abstractmethod
    def scrape_odds_pool(self) -> "RaceOddsPool":
        pass

    @abstractmethod
    def scrape_odds_timestamp(self) -> "OddsTimeStamp":
        pass

    @abstractmethod
    def get_uri(self) -> str:
        pass


@total_ordering
@dataclass
class OddsTimeStamp:
    update_time: Optional[datetime] = None

    def long_str(self) -> str:
        return (
            "confirmed"
            if self.update_time is None
            else "updated at " + self.update_time.strftime("%Y-%m-%d %H:%M")
        )

    def __str__(self) -> str:
        return (
            "Confirmed"
            if self.update_time is None
            else self.update_time.strftime("%Y%m%d%H%M")
        )

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.is_confirmed:
            return False
        elif other.is_confirmed:
            return True
        else:
            return self.update_time < other.update_time

    @property
    def is_confirmed(self) -> bool:
        return not bool(self.update_time)

    @classmethod
    def confirmed(cls) -> "OddsTimeStamp":
        return OddsTimeStamp(None)


@dataclass
class RaceOddsPool(OddsPool):
    race: Race
    timestamp: OddsTimeStamp

    @property
    def key(self) -> str:
        return f"{self.race.race_id}/{self.timestamp}"


class OddsUpdatedException(Exception):
    pass
