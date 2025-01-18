import datetime
from typing import Optional

from pydantic import BaseModel

import parimana.domain.schedule as sc


class Category(BaseModel):
    id: str
    name: str

    @classmethod
    def from_base(cls, category: sc.Category):
        return cls(id=category.id, name=category.name)


class Course(BaseModel):
    id: str
    name: str
    category: Category

    @classmethod
    def from_base(cls, course: sc.Course):
        return cls(
            id=course.id, name=course.name, category=Category.from_base(course.category)
        )


class Fixture(BaseModel):
    course: Course
    date: datetime.date

    @classmethod
    def from_base(cls, fixture: sc.Fixture):
        return cls(
            course=Course.from_base(fixture.course),
            date=fixture.date,
        )


class RaceInfo(BaseModel):
    id: str
    name: Optional[str]
    fixture: Optional[Fixture]

    @classmethod
    def from_base(cls, race: sc.RaceInfo):
        return cls(
            id=race.race_id,
            name=race.name,
            fixture=Fixture.from_base(race.fixture),
        )
