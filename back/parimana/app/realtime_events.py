import datetime
from itertools import groupby
from operator import attrgetter
import re
from typing import Mapping, Optional, Sequence

from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str


category_list = [
    Category(id="b", name="ボートレース"),
    Category(id="h", name="競馬"),
]

category_dict = {c.id: c for c in category_list}


class Course(BaseModel):
    id: str
    name: str
    category: Category

    @classmethod
    def of(cls, cat_id, id, name) -> "Course":
        return cls(id=id, name=name, category=category_dict[cat_id])


course_list = [
    Course.of("b", "01", name="桐生"),
    Course.of("b", "02", name="戸田"),
    Course.of("h", "03", name="府中"),
    Course.of("h", "04", name="中山"),
]

course_dict = {cr.id: cr for cr in course_list}

cat_course_dict = {
    cat.id: list(crs) for cat, crs in groupby(course_list, key=attrgetter("category"))
}


class Race(BaseModel):
    id: str
    name: str
    date: datetime.date
    course: Course


def get_categories() -> Sequence[Category]:
    return category_list


def get_category(category_id: str) -> Category:
    return category_dict[category_id]


def get_course(course_id: str) -> Course:
    return course_dict[course_id]


class DaySchedules(BaseModel):
    course: Course
    races: Sequence[Race]


def get_calendar(
    cat: Category,
) -> Mapping[datetime.date, Sequence[DaySchedules]]:
    return {
        d: [
            DaySchedules(
                course=course,
                races=[
                    Race(
                        id=f"{cat.id}{d:%Y%m%d}-{course.id}-{n:02}",
                        name=f"{n:02}R",
                        date=d,
                        course=course,
                    )
                    for n in range(1, 13)
                ],
            )
            for course in cat_course_dict[cat.id]
        ]
        for d in [
            datetime.date.today() + datetime.timedelta(days=i) for i in range(-2, 2)
        ]
    }


RACE_ID_PATTERN: re.Pattern = re.compile(
    r"(?P<cat_id>.)(?P<date>[0-9]{8})-(?P<cr_id>[0-9A-Z]{2})-(?P<no>[0-9]{2})"
)


def from_id(race_id: str) -> Optional[Race]:
    if m := re.fullmatch(RACE_ID_PATTERN, race_id):
        parsed = m.groupdict()
        return Race(
            id=race_id,
            name=f"{parsed['no']}R",
            date=datetime.datetime.strptime(parsed["date"], "%Y%m%d").date(),
            course=course_dict[parsed["cr_id"]],
        )
    else:
        return None


def find_race(url: str) -> Optional[Race]:
    return None


def get_race(race_id: str) -> Optional[Race]:
    return from_id(race_id)
