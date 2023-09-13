from typing import Collection, Type
from parimana.base.race import Race
from parimana.race.boatrace.race import BoatRace
from parimana.race.netkeiba.race import NetKeibaRace

race_types: Collection[Type[Race]] = [BoatRace, NetKeibaRace]


def get_race(race_id: str) -> Race:
    for race_type in race_types:
        if found := race_type.from_id(race_id):
            return found

    raise ValueError(f"race_id: {race_id} is illegal")
