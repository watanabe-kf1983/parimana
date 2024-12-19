from typing import Collection, Sequence, Type
from parimana.race.base import Race
from parimana.race.schedule import Category
from parimana.race.boatrace import BoatRace, category_boat
from parimana.race.netkeiba import NetKeibaRace, category_keiba

_race_types: Collection[Type[Race]] = [BoatRace, NetKeibaRace]
_categories: Sequence[Category] = [category_boat, category_keiba]


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
