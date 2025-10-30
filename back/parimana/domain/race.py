from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from functools import total_ordering
from typing import Collection, Optional, Sequence, Type

from parimana.domain.base import OddsPool


class Race(ABC):
    @property
    @abstractmethod
    def race_id(self) -> str:
        pass

    @property
    @abstractmethod
    def odds_source(self) -> "OddsSource":
        pass

    @classmethod
    @abstractmethod
    def from_id(cls, race_id: str) -> Optional["Race"]:
        pass

    @classmethod
    @abstractmethod
    def from_uri(cls, uri: str) -> Optional["Race"]:
        pass

    @classmethod
    @abstractmethod
    def odds_source_type(cls) -> Type["OddsSource"]:
        pass


@dataclass
class RaceSelector:
    race_types: Collection[Type[Race]]

    def select(self, race_id_or_uri: str) -> "Race":
        for race_type in self.race_types:
            if found := race_type.from_id(race_id_or_uri):
                return found

        for race_type in self.race_types:
            if found := race_type.from_uri(race_id_or_uri):
                return found

        raise ValueError(f"race_id_or_uri: {race_id_or_uri} is illegal")

    def odds_source_sites(self) -> Sequence[str]:
        return [
            race_type.odds_source_type().site_name() for race_type in self.race_types
        ]


class OddsSource(ABC):
    @abstractmethod
    def scrape_odds_pool(self) -> "RaceOddsPool":
        pass

    @abstractmethod
    def scrape_timestamp(self) -> "OddsTimeStamp":
        pass

    @abstractmethod
    def get_uri(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def site_name(cls) -> str:
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
        return cls(None)

    @classmethod
    def from_str(cls, s: str) -> "OddsTimeStamp":
        if s == "Confirmed":
            return cls.confirmed()
        else:
            dt = datetime.strptime(s, "%Y%m%d%H%M")
            return cls(updatetime=dt)


@dataclass
class RaceOddsPool(OddsPool):
    race: Race
    timestamp: OddsTimeStamp

    @property
    def key(self) -> str:
        return f"{self.race.race_id}/{self.timestamp}"


class OddsUpdatedException(Exception):
    pass
