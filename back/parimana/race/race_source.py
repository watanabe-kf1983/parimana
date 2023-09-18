from abc import ABC, abstractmethod
from typing import Optional

from parimana.race.odds_pool import RaceOddsPool
from parimana.race.race import Race


class RaceSource(ABC):
    @property
    @abstractmethod
    def race(self) -> Race:
        pass

    @abstractmethod
    def scrape_odds_pool(self) -> RaceOddsPool:
        pass

    @classmethod
    @abstractmethod
    def from_race(cls, race: Race) -> Optional["RaceSource"]:
        pass
