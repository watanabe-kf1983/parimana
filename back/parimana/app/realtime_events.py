import datetime
from typing import Mapping, Optional, Sequence

from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str


categories = [
    Category(id="1", name="ボートレース"),
    Category(id="2", name="競馬(JRA)"),
]

category_dict = {c.id: c for c in categories}


class Course(BaseModel):
    id: str
    name: str
    category: Category


courses = [
    Course(id="101", name="桐生", category=category_dict["1"]),
    Course(id="102", name="戸田", category=category_dict["1"]),
    Course(id="201", name="府中", category=category_dict["2"]),
    Course(id="202", name="中山", category=category_dict["2"]),
]

course_dict = {c.id: c for c in courses}


class Race(BaseModel):
    id: str
    name: str
    date: datetime.date
    course: Course


def get_categories() -> Sequence[Category]:
    return categories


def get_category(category_id: str) -> Category:
    return category_dict[category_id]


def get_course(course_id: str) -> Course:
    return course_dict[course_id]


def get_calendar(category: Category) -> Mapping[datetime.date, Sequence[Course]]:
    if category.id == "1":
        d = datetime.date.today()
        return {d: [get_course("101"), get_course("102")]}
    else:
        return {d: [get_course("201"), get_course("202")]}


def get_races_by_course(course: Course, date: datetime.date) -> Sequence[Race]:
    return [
        Race(id=f"boatrace-20240901-1-{i+1}", name=f"{i+1}R", date=date, course=course)
        for i in range(12)
    ]


def find_race(url: str) -> Optional[Race]:
    return None


def get_race(race_id: str) -> Race:
    return Race(
        id=race_id, name=race_id, date=datetime.date.today(), course=courses["101"]
    )
