from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from parimana.io.kvs import Storage
from parimana.domain.race import Race, OddsTimeStamp, RaceOddsPool


class OddsRepository(ABC):

    @abstractmethod
    def save_odds_pool(self, odds_pool: RaceOddsPool):
        pass

    @abstractmethod
    def load_odds_pool(self, race: Race, ts: OddsTimeStamp) -> Optional[RaceOddsPool]:
        pass

    @abstractmethod
    def load_latest_odds_pool(self, race: Race) -> Optional[RaceOddsPool]:
        pass

    @abstractmethod
    def odds_pool_exists(self, race: Race) -> bool:
        pass

    @abstractmethod
    def save_latest_odds_time(self, race: Race, ts: OddsTimeStamp) -> None:
        pass

    @abstractmethod
    def load_latest_odds_time(self, race: Race) -> Optional[OddsTimeStamp]:
        pass


@dataclass
class OddsRepositoryImpl(OddsRepository):
    store: Storage

    def save_odds_pool(self, odds_pool: RaceOddsPool):
        race = odds_pool.race
        ts = odds_pool.timestamp
        self.store.write_object(f"odds/{race.race_id}/{ts}/pool.pickle", odds_pool)
        ts = self.load_latest_odds_time(odds_pool.race)
        if (ts is None) or (ts < odds_pool.timestamp):
            self.save_latest_odds_time(odds_pool.race, odds_pool.timestamp)

    def load_odds_pool(self, race: Race, ts: OddsTimeStamp) -> Optional[RaceOddsPool]:
        return self.store.read_object(f"odds/{race.race_id}/{ts}/pool.pickle")

    def load_latest_odds_pool(self, race: Race) -> Optional[RaceOddsPool]:
        ts = self.load_latest_odds_time(race)
        if ts:
            return self.load_odds_pool(race, ts)
        else:
            return None

    def save_latest_odds_time(self, race: Race, ts: OddsTimeStamp) -> None:
        self.store.write_object(f"odds/{race.race_id}/ts.pickle", ts)

    def load_latest_odds_time(self, race: Race) -> Optional[OddsTimeStamp]:
        return self.store.read_object(f"odds/{race.race_id}/ts.pickle")

    def odds_pool_exists(self, race: Race) -> bool:
        return self.store.exists(f"odds/{race.race_id}/ts.pickle")
