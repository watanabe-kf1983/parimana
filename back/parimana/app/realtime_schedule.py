import datetime
from typing import Optional, Sequence

from parimana.app.realtime import ResultNotExistError
from parimana.repository.file_repository import FileRepository
from pydantic import BaseModel

import parimana.race as rc

repo = FileRepository()


class Category(BaseModel):
    id: str
    name: str

    @classmethod
    def from_base(cls, category: rc.Category):
        return cls(id=category.id, name=category.name)


class Course(BaseModel):
    id: str
    name: str
    category: Category

    @classmethod
    def from_base(cls, course: rc.Course):
        return cls(
            id=course.id, name=course.name, category=Category.from_base(course.category)
        )


class Fixture(BaseModel):
    course: Course
    date: datetime.date

    @classmethod
    def from_base(cls, fixture: rc.Fixture):
        return cls(
            course=Course.from_base(fixture.course),
            date=fixture.date,
        )


class RaceInfo(BaseModel):
    id: str
    name: str
    fixture: Fixture

    @classmethod
    def from_base(cls, race: rc.RaceInfo):
        return cls(
            id=race.race_id,
            name=race.name,
            fixture=Fixture.from_base(race.fixture),
        )


def get_categories() -> Sequence[Category]:
    return [Category.from_base(cat) for cat in rc.CategorySelector.all()]


def get_category(category_id: str) -> Category:
    return Category.from_base(rc.CategorySelector.select(category_id))


def get_schedule(
    cat: Category,
) -> Sequence[RaceInfo]:

    rc_cat = rc.CategorySelector.select(cat.id)
    return [
        RaceInfo.from_base(race_info)
        for date in (repo.load_calendar(rc_cat) or [])
        for race_info in (repo.load_schedule(rc_cat, date) or [])
    ]


def find_race(url: str) -> Optional[RaceInfo]:
    return None


def get_race(race_id: str) -> RaceInfo:
    if race_info := repo.load_race_info(race_id):
        return RaceInfo.from_base(race_info)
    else:
        raise ResultNotExistError(f"{race_id} not found")
