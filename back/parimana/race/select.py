from typing import Collection, Sequence, Type
from parimana.race.base import Race
from parimana.race.schedule import Category, RaceInfo
from parimana.race.boatrace import BoatRace, category_boat
from parimana.race.netkeiba import NetKeibaRace

_race_types: Collection[Type[Race]] = [BoatRace, NetKeibaRace]
_categories: Sequence[Category] = [category_boat]


class CategorySelector:

    @staticmethod
    def all() -> Sequence[Category]:
        return _categories

    @staticmethod
    def select(category_id: str) -> Category:
        for category in CategorySelector.all():
            if category.id == category_id:
                return category

        raise ValueError(f"category_id: {category_id} is illegal")


class RaceSelector:
    @staticmethod
    def select(race_id: str) -> "Race":
        for race_type in _race_types:
            if found := race_type.from_id(race_id):
                return found

        raise ValueError(f"race_id: {race_id} is illegal")

    def race_info(race_id: str) -> RaceInfo:
        for schedule_source in (cat.schedule_source for cat in CategorySelector.all()):
            if found := schedule_source.find_race_info(race_id):
                return found

        raise ValueError(f"race_id: {race_id} is illegal")
