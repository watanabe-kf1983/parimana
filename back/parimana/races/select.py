from typing import Collection, Type
from parimana.base import Race, RaceSource
from parimana.races.boatrace.race import BoatRace
from parimana.races.boatrace.race_source import BoatRaceSource
from parimana.races.netkeiba.race import NetKeibaRace
from parimana.races.netkeiba.race_source import NetKeibaSource

race_types: Collection[Type[Race]] = [BoatRace, NetKeibaRace]
race_source_types: Collection[Type[RaceSource]] = [BoatRaceSource, NetKeibaSource]


def get_race(race_id: str) -> Race:
    for race_type in race_types:
        if found := race_type.from_id(race_id):
            return found

    raise ValueError(f"race_id: {race_id} is illegal")


def get_source(race: Race) -> RaceSource:
    for source_type in race_source_types:
        if found := source_type.from_race(race):
            return found

    raise ValueError(f"race_source not found: {race}")
