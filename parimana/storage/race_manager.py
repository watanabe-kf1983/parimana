from dataclasses import dataclass
from functools import cached_property
import pickle
from typing import Collection, Type

from pathlib import Path

from parimana.base.race import Race, RaceSource
from parimana.boatrace.race import BoatRaceSource
from parimana.netkeiba.race import NetKeibaSource


race_types: Collection[Type[RaceSource]] = [BoatRaceSource, NetKeibaSource]


@dataclass
class RaceManager:
    race_id: str

    @cached_property
    def race_source(self) -> RaceSource:
        for race_type in race_types:
            if found := race_type.from_race_id(self.race_id):
                return found

        raise ValueError(f"race_id: {self} is illegal")

    @cached_property
    def base_dir(self) -> Path:
        dir = Path(".output") / self.race_id
        dir.mkdir(exist_ok=True, parents=True)
        return dir

    @cached_property
    def race_path(self) -> Path:
        return self.base_dir / "race.pickle"

    def get_race(self, force_scrape: bool = False) -> Race:
        if force_scrape or not self.prepared:
            race = self.race_source.scrape_race()
            self._save_race(race)

        return self._load_race()

    @property
    def prepared(self) -> bool:
        return self.race_path.exists()

    def _load_race(self) -> Race:
        # todo: read from redis by race_id

        race_path = self.race_path
        print(f"reading race from {race_path}...")
        with open(race_path, "rb") as f:
            race = pickle.load(f)
        print("reading race done.")
        return race

    def _save_race(self, race: Race) -> None:
        # todo: save to redis by race_id
        race_path = self.race_path
        print(f"writing race to {race_path}...")
        with open(race_path, "wb") as f:
            pickle.dump(race, f)
        print("writing race done.")
