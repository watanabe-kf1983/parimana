from typing import Collection, Optional, Sequence, Type
from parimana.race.base import Race
from parimana.race.boatrace import BoatRace, boatCategory
from parimana.race.fixture import Category, RaceInfo
from parimana.race.netkeiba.race import NetKeibaRace

_race_types: Collection[Type[Race]] = [BoatRace, NetKeibaRace]
_categories: Sequence[Category] = [boatCategory]


class CategorySelector:

    @staticmethod
    def all() -> Sequence[Category]:
        return _categories

    @staticmethod
    def select(category_id: str) -> Optional[Category]:
        if cat := next(
            filter(lambda cat: cat.id == category_id, CategorySelector.all()), None
        ):
            return cat
        else:
            raise ValueError(f"category_id: {category_id} is illegal")


class RaceSelector:
    @staticmethod
    def select(race_id: str) -> "Race":
        for race_type in _race_types:
            if found := race_type.from_id(race_id):
                return found

        raise ValueError(f"race_id: {race_id} is illegal")

    def race_info(race_id: str) -> RaceInfo:
        for category in _categories:
            if found := category.fixture_source.find_race_info(race_id):
                return found

        raise ValueError(f"race_id: {race_id} is illegal")
