import datetime
from typing import Optional, Sequence
from fastapi import APIRouter, Query
from pydantic import BaseModel

import parimana.domain.schedule as sc
from parimana.app.schedule import ScheduleApp
import parimana.settings as settings


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
    name: str
    fixture: Fixture

    @classmethod
    def from_base(cls, race: sc.RaceInfo):
        return cls(
            id=race.race_id,
            name=race.name,
            fixture=Fixture.from_base(race.fixture),
        )


router = APIRouter()

app = ScheduleApp(categories=settings.categories, store=settings.schedule_storage)


@router.get("/categories")
def get_categories():
    return [Category.from_base(cat) for cat in settings.categories]


@router.get("/races")
def get_races(
    category_id: Optional[str] = Query(None),
    url: Optional[str] = Query(None),
) -> Sequence[RaceInfo]:
    if url:
        race = app.find_race(url)
        return [RaceInfo.from_base(race)] if race else []
    else:
        try:
            return [
                RaceInfo.from_base(race)
                for race in app.get_schedule(cat=_select_cat(category_id))
            ]

        except Exception:
            return []


@router.get("/races/{race_id}")
def get_race(race_id: str) -> RaceInfo:
    return RaceInfo.from_base(app.get_race(race_id))


def _select_cat(category_id: str) -> sc.Category:
    return app.select_category(category_id)
