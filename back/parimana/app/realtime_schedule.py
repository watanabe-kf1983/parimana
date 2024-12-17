import datetime
from typing import Mapping, Optional, Sequence

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
    category: Category
    course: Course
    date: datetime.date

    @classmethod
    def from_base(cls, fixture: rc.Fixture):
        return cls(
            category=Category.from_base(fixture.category),
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


class RaceSchedule(BaseModel):
    course: Course
    races: Sequence[RaceInfo]

    @classmethod
    def from_base(cls, schedule: rc.RaceSchedule):
        return cls(
            course=Course.from_base(schedule.fixture.course),
            races=[RaceInfo.from_base(race) for race in schedule.races],
        )


def get_categories() -> Sequence[Category]:
    return [Category.from_base(cat) for cat in rc.CategorySelector.all()]


def get_category(category_id: str) -> Category:
    return Category.from_base(rc.CategorySelector.select(category_id))


def get_calendar(
    cat: Category,
) -> Mapping[datetime.date, Sequence[RaceSchedule]]:

    rc_cat = rc.CategorySelector.select(cat.id)
    calendar = repo.load_schedule(rc_cat)
    return {
        date: [RaceSchedule.from_base(sc) for sc in schedules]
        for date, schedules in calendar.items()
    }


def find_race(url: str) -> Optional[RaceInfo]:
    return None


def get_race(race_id: str) -> RaceInfo:
    return RaceInfo.from_base(rc.RaceSelector.race_info(race_id))
