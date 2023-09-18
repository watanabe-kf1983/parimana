from typing import Collection, Type
from parimana.race.base import Race
from parimana.race.boatrace.race import BoatRace
from parimana.race.netkeiba.race import NetKeibaRace

_race_types: Collection[Type[Race]] = [BoatRace, NetKeibaRace]


class RaceSelector:
    @staticmethod
    def select(race_id: str) -> "Race":
        from parimana.race.select import _race_types

        for race_type in _race_types:
            if found := race_type.from_id(race_id):
                return found

        raise ValueError(f"race_id: {race_id} is illegal")
