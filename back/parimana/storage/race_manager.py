from dataclasses import dataclass
from functools import cached_property
import pickle

from pathlib import Path

from parimana.base.race import Race
from parimana.base.odds_pool import RaceOddsPool
from parimana.race import get_race_source


@dataclass
class RaceManager:
    race: Race

    @cached_property
    def base_dir(self) -> Path:
        dir = Path(".output") / self.race.race_id
        dir.mkdir(exist_ok=True, parents=True)
        return dir

    @cached_property
    def odds_pool_path(self) -> Path:
        return self.base_dir / "odds_pool.pickle"

    def get_odds_pool(self, force_scrape: bool = False) -> RaceOddsPool:
        if force_scrape or not self.prepared:
            odds_pool = get_race_source(self.race).scrape_odds_pool()
            self._save_odds_pool(odds_pool)

        return self._load_odds_pool()

    @property
    def prepared(self) -> bool:
        return self.odds_pool_path.exists()

    def _load_odds_pool(self) -> RaceOddsPool:
        # todo: read from redis by race_id

        odds_pool_path = self.odds_pool_path
        print(f"reading odds_pool from {odds_pool_path}...")
        with open(odds_pool_path, "rb") as f:
            race = pickle.load(f)
        print("reading odds_pool done.")
        return race

    def _save_odds_pool(self, odds_pool: RaceOddsPool) -> None:
        # todo: save to redis by race_id
        race_path = self.odds_pool_path
        print(f"writing odds_pool to {race_path}...")
        with open(race_path, "wb") as f:
            pickle.dump(odds_pool, f)
        print("writing odds_pool done.")
